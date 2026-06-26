import requests, re, json

r = requests.get('https://tophub.today/', timeout=15, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
})

# 找 app.js
js_files = re.findall(r'<script[^>]+src="([^">]+\.js[^">]*)"', r.text)
app_js = [j for j in js_files if 'app' in j.lower()][0]
print(f'App JS: {app_js}')

j = requests.get(app_js, timeout=10)
text = j.text

# 找所有 URL 或路径字符串
url_patterns = re.findall(r'["\047]/(?:[a-zA-Z][a-zA-Z0-9_-]*/?){1,6}["\047]', text)
print(f'\nURL paths found: {url_patterns[:30]}')

# 找 data-xxx 属性（可能有数据嵌入）
data_attrs = re.findall(r'data-(?:src|url|load|api)=["\'`]([^"\']+)["\'`]', r.text)
print(f'\ndata attrs: {data_attrs[:10]}')

# 找页面上的热榜数据（可能在某个 div 或 script 里）
# 先找所有 class 含 nano 的元素内容
nano_content = re.findall(r'class="[^"]*nano[^"]*"[^>]*>(.*?)</div>', r.text, re.DOTALL)
print(f'\nnano content blocks: {len(nano_content)}')

# 看看 body 里有什么结构
body_classes = set(re.findall(r'<div[^>]+class="([^"]+)"', r.text))
print(f'\ndiv classes: {list(body_classes)[:20]}')

# 找所有外链（热搜来源）
hot_sources = re.findall(r'href="(https?://[^"]+)"[^>]*>\s*([^<\n]{2,30})\s*<', r.text)
print(f'\nhot source links ({len(hot_sources)}):')
for l, t in hot_sources[:15]:
    print(f'  [{t.strip()}] -> {l[:60]}')
