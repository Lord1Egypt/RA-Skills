import requests, re

app_js_url = 'https://file.ipadown.com/tophub/assets/js/app.2025.js?202505150004'
j = requests.get(app_js_url, timeout=10)
text = j.text
print(f'JS size: {len(text)}')

# 找所有 URL 相关的字符串
urls = re.findall(r'["\047]/(?:[a-zA-Z][a-zA-Z0-9_/-]/?){1,8}["\047\s,\)]+', text)
print(f'\nAll path patterns ({len(urls)}):')
seen = set()
for u in urls:
    clean = u.strip().strip('",\'\s)')
    if clean not in seen and len(clean) > 4:
        seen.add(clean)
        print(f'  {clean}')

# 找 fetch / ajax / XMLHttpRequest 调用
ajax_patterns = re.findall(r'(fetch|ajax|axios|http\.get|http\.post|getJSON)\s*\([^)]+', text)
print(f'\nAjax patterns ({len(ajax_patterns)}):')
for p in ajax_patterns[:10]:
    print(f'  {p}')

# 找字符串中包含 api 或 url 或 endpoint
api_refs = re.findall(r'["\047][^"\']*(?:api|fetch|node|route|url)[^"\']{2,60}["\047]', text, re.IGNORECASE)
print(f'\nAPI refs ({len(api_refs)}):')
seen2 = set()
for a in api_refs:
    if a not in seen2:
        seen2.add(a)
        print(f'  {a[:80]}')
