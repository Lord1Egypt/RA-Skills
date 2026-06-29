# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import xml.etree.ElementTree as ET

url = 'http://export.arxiv.org/api/query'
params = {
    'search_query': 'cat:cs.CV AND deep learning',
    'start': 0,
    'max_results': 3
}

response = requests.get(url, params=params, timeout=30)
print(f'状态码: {response.status_code}')
root = ET.fromstring(response.text)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

entries = root.findall('atom:entry', ns)
print(f'检索到 {len(entries)} 篇论文')
for entry in entries[:1]:
    title = entry.find('atom:title', ns)
    print(f'标题: {title.text if title is not None else "无"}')
