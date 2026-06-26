import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.sse.com.cn/market/stockdata/firstday/'
}

# 尝试上交所新的API格式
# 1. 使用jsonp格式
url = 'https://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback123&isPagination=true&sqlId=COMMON_SSE_SCPZ_GPZLZSPL_GPLBGP_L&stockType=1&pageHelp.pageSize=5&pageHelp.pageNo=1&pageHelp.cacheSize=1'
try:
    r = requests.get(url, headers=headers, timeout=10)
    print('SSE JSONP status:', r.status_code)
    print(r.text[:500])
except Exception as e:
    print('err:', e)

print('---')

# 2. 尝试使用POST方式
url2 = 'https://query.sse.com.cn/commonQuery.do'
data = {
    'jsonCallBack': 'jsonpCallback123',
    'isPagination': 'true',
    'sqlId': 'COMMON_SSE_SCPZ_GPZLZSPL_GPLBGP_L',
    'stockType': '1',
    'pageHelp.pageSize': '5',
    'pageHelp.pageNo': '1',
    'pageHelp.cacheSize': '1',
}
try:
    r2 = requests.post(url2, data=data, headers=headers, timeout=10)
    print('SSE POST status:', r2.status_code)
    print(r2.text[:500])
except Exception as e:
    print('err:', e)

print('---')

# 3. 尝试获取上交所新股数据
url3 = 'https://query.sse.com.cn/marketdata/stock/listing/firstday.do'
params3 = {
    'jsonCallBack': '',
    'isPagination': 'true',
    'pageHelp.pageSize': '10',
}
try:
    r3 = requests.get(url3, params=params3, headers=headers, timeout=10)
    print('SSE firstday status:', r3.status_code)
    print(r3.text[:500])
except Exception as e:
    print('err:', e)
