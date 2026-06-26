#!/usr/bin/env python3
"""检查内联后的样式"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

# 读取 HTML
html_path = Path('/Users/panda/.openclaw/workspace/examples/openclaw-intro/index.html')

# 运行转换器的前半部分来获取内联后的 HTML
sys.path.insert(0, str(html_path.parent.parent.parent / 'skills' / 'html2pptx-shape'))
from index import HTMLToPPTXConverter

converter = HTMLToPPTXConverter()

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 内联 CSS
inlined = converter.inline_css(html_content, str(html_path.parent))

# 解析并检查
soup = BeautifulSoup(inlined, 'html.parser')

# 检查关键元素
body = soup.find('body')
print(f"Body class: {body.get('class', [])}")
print(f"Body style: {body.get('style', 'None')[:200]}...")

first_slide = soup.find('section', class_='slide')
if first_slide:
    print(f"\nFirst slide style: {first_slide.get('style', 'None')[:200]}...")

title = soup.find(class_='xw-title')
if title:
    print(f"\n.xw-title style: {title.get('style', 'None')[:200]}...")
    print(f"Text: {title.get_text()[:50]}...")

kicker = soup.find(class_='xw-kicker')
if kicker:
    print(f"\n.xw-kicker style: {kicker.get('style', 'None')[:200]}...")

card = soup.find(class_='xw-card')
if card:
    print(f"\n.xw-card style: {card.get('style', 'None')[:200]}...")

soft_pink = soup.find(class_='soft-pink')
if soft_pink:
    print(f"\n.soft-pink style: {soft_pink.get('style', 'None')[:200]}...")

# 检查 CSS 变量是否被解析
print("\n\n=== CSS 变量检查 ===")
all_text = str(soup)
var_count = all_text.count('var(--')
print(f"未解析的 CSS 变量数量：{var_count}")

# 检查一些具体变量
if 'var(--xw-bg)' in all_text:
    print("⚠️  var(--xw-bg) 未解析")
else:
    print("✅ var(--xw-bg) 已解析")
