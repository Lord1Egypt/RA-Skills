import requests, re

url = 'https://tophub.today/'
r = requests.get(url, timeout=15, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://tophub.today/',
})
print(f'status: {r.status_code}, len: {len(r.text)}')
print(f'content-type: {r.headers.get("content-type")}')

# 看页面结构
# 1. 找所有分类/平台名
platforms = re.findall(r'class="[^"]*name[^"]*"[^>]*>([^<]+)<', r.text)
print(f'\nplatforms: {platforms[:10]}')

# 2. 找热搜条目
items = re.findall(r'<a[^>]+class="[^"]*hot[^"]*"[^>]*>([^<]+)<', r.text, re.IGNORECASE)
print(f'\nhot items: {items[:10]}')

# 3. 找链接
links = re.findall(r'href="(/[^"]+)"[^>]*>[^<]*(?:知乎|微博|抖音|36kr|虎嗅)', r.text)
print(f'\nrelevant links: {links[:10]}')

# 4. 看看有什么 class
classes = set(re.findall(r'class="([^"]+)"', r.text))
print(f'\nclasses: {list(classes)[:20]}')

# 5. 打印一段正文
print('\n--- first 3000 chars ---')
print(r.text[:3000])
