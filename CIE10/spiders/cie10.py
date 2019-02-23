import scrapy
from scrapy.shell import inspect_response

class Cie10Spider(scrapy.Spider):
    name = "cie10"

    def start_requests(self):
        url = 'https://icdcode.info/espanol/cie-10/codigos.html'
        yield scrapy.Request(url=url, callback=self.parseLevel0)
        
    def parseLevel0(self, response):
        for row in response.css('.full_width'):
            url = row.css('.first > a::attr(href)').extract()[0]
            code = self.clearCode(row.css('.first > a::text').extract()[0])
            description = row.css('.four_fifth > a::text').extract()[0]
            data = {
                'level': 0,
                'code': code,
                'description': description
                }
            yield data
            request = scrapy.Request(url=url, callback=self.parseLevel)
            request.meta['level'] = 1
            yield request

    def parseLevel(self, response):
        level = response.meta['level']
        #print('Parsing ({}): {}'.format(level, response.url))
        # if(level >= 5):
        #     return
        codes = {}
        codes[level-1] = response.css('div.sidebar-right > div.border > h2::text').extract()[0]
        #print(codes)
        for c, row in enumerate(response.css('.full_width')):
            #print(c)
            if c >= 1 and c <= level-1:
                if level == 2:
                    pass
                    #print('B1=>Code_{} = {} ({})'.format(c-1, self.clearCode(row.css('.first > a::text').extract()[0]), response.url))
                i = c -1
                codes[i] = self.clearCode(row.css('.first > a::text').extract()[0])[2:]
            elif c >= level:
                code = self.clearCode(row.css('.first > a::text').extract()[0])
                #code = row.css('.first > a::text').extract()[0]
                description = row.css('.four_fifth > a::text').extract()[0]
                data = {
                    'code': code,
                    'level': level,
                    'description': description
                }
                #print(codes)
                for index, value in codes.items():
                    if level == 2:
                        #print('B2=>code_{} = {} ({})'.format(index, value, code))
                        pass
                    data['code_{}'.format(index)] = value
                yield data
                if len(code) <= 3 or '-' in code:
                    url = row.css('.first > a::attr(href)').extract()[0]
                    #print('Yielding: {} => '.format(code, url))
                    request = scrapy.Request(url=url, callback=self.parseLevel)
                    request.meta['level'] = level + 1
                    yield request
                else:
                    #print('Not yielding: {}'.format(code))
                    pass


    def clearCode(self, code):
        return code.replace("\u2013", '-').replace('.', '')
            
    # def parseLevel1(self, response):
    #     code0 = response.css('div.sidebar-right > div.border > h2::text').extract()[0]
    #     for c, row in enumerate(response.css('.full_width')):
    #         if c > 0:
    #             code = self.clearCode(row.css('.first > a::text').extract()[0])
    #             url = row.css('.first > a::attr(href)').extract()[0]
    #             description = row.css('.four_fifth > a::text').extract()[0]
    #             data = {
    #                 'level': 1,
    #                 'code0': code0,
    #                 'code': code,
    #                 'description': description
    #                 }
    #             yield data
    #             yield scrapy.Request(url=url, callback=self.parseLevel2)
    #
    # def parseLevel2(self, response):
    #     code1 = response.css('div.sidebar-right > div.border > h2::text').extract()[0]
    #     for c, row in enumerate(response.css('.full_width')):
    #         if c == 1:
    #             code0 = self.clearCode(row.css('.first > a::text').extract()[0][2:])
    #         if c > 1:
    #             url = row.css('.first > a::attr(href)').extract()[0]
    #             code = self.clearCode(row.css('.first > a::text').extract()[0])
    #             description = row.css('.four_fifth > a::text').extract()[0]
    #             data = {
    #                 'level': 2,
    #                 'code0': code0,
    #                 'code1': code1,
    #                 'code': code,
    #                 'description': description
    #                 }
    #             yield data
    #             yield scrapy.Request(url=url, callback=self.parseLevel3)
    #
    #
    # def parseLevel3(self, response):
    #     code2 = response.css('div.sidebar-right > div.border > h2::text').extract()[0]
    #     for c, row in enumerate(response.css('.full_width')):
    #         if c == 1:
    #             code0 = self.clearCode(row.css('.first > a::text').extract()[0][2:])
    #         if c == 2:
    #             code1 = self.clearCode(row.css('.first > a::text').extract()[0][2:])
    #         if c > 2:
    #             code = row.css('.first > a::text').extract()[0]
    #             description = row.css('.four_fifth > a::text').extract()[0]
    #             data = {
    #                 'level': 3,
    #                 'code0': code0,
    #                 'code1': code1,
    #                 'code2': code2,
    #                 'code': code,
    #                 'description': description
    #                 }
    #             yield data
    #             if len(code) <= 3:
    #                 url = row.css('.first > a::attr(href)').extract()[0]
    #                 yield scrapy.Request(url=url, callback=self.parseLevel4)
    #
    # def parseLevel4(self, response):
    #     code3 = response.css('div.sidebar-right > div.border > h2::text').extract()[0]
    #     for c, row in enumerate(response.css('.full_width')):
    #         if c == 1:
    #             code0 = self.clearCode(row.css('.first > a::text').extract()[0][2:])
    #         if c == 2:
    #             code1 = self.clearCode(row.css('.first > a::text').extract()[0][2:])
    #         if c == 3:
    #             code2 = self.clearCode(row.css('.first > a::text').extract()[0][2:])
    #         if c > 3:
    #             code = row.css('.first > a::text').extract()[0]
    #             description = row.css('.four_fifth > a::text').extract()[0]
    #             data = {
    #                 'level': 4,
    #                 'code0': code0,
    #                 'code1': code1,
    #                 'code2': code2,
    #                 'code3': code3,
    #                 'code': code,
    #                 'description': description
    #             }
    #             yield data
    #             if len(code) <= 3:
    #                 url = row.css('.first > a::attr(href)').extract()[0]
    #                 yield scrapy.Request(url=url, callback=self.parseLevel5)