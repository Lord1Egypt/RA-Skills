#!/usr/bin/env python3
"""
调试脚本：检查 HTML 元素的样式解析
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import cssutils
from cssutils.css import CSSStyleSheet

# 读取嵌入后的 HTML
html_path = Path('/tmp/test_embedded.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 提取所有 <style> 标签的 CSS
all_css = ""
for style_tag in soup.find_all('style'):
    if style_tag.string:
        all_css += style_tag.string + "\n"

# 解析 CSS
cssutils.log.setLevel('CRITICAL')
sheet = cssutils.parseString(all_css)

# 收集所有 CSS 变量
css_vars = {}
for rule in sheet:
    if hasattr(rule, 'style'):
        for prop in rule.style:
            if prop.name.startswith('--'):
                css_vars[prop.name] = prop.value

print(f"✅ 找到 {len(css_vars)} 个 CSS 变量")
print("\n部分变量示例:")
for i, (name, value) in enumerate(list(css_vars.items())[:10]):
    print(f"  {name}: {value}")

# 查找带有 class="tpl-xhs-white-editorial" 的元素
body = soup.find('body')
if body:
    print(f"\n✅ Body class: {body.get('class', [])}")
    
    # 查找第一个 slide
    first_slide = body.find('section', class_='slide')
    if first_slide:
        print(f"\n✅ 找到第一个 slide")
        print(f"   Class: {first_slide.get('class', [])}")
        print(f"   Style attr: {first_slide.get('style', 'None')}")
        
        # 查找 .xw-title 元素
        title = first_slide.find(class_='xw-title')
        if title:
            print(f"\n✅ 找到 .xw-title 元素")
            print(f"   Text: {title.get_text()[:50]}...")
            print(f"   Style attr: {title.get('style', 'None')}")

# 测试 CSS 规则匹配
print("\n\n📋 测试 CSS 规则匹配:")
test_selectors = [
    '.tpl-xhs-white-editorial .xw-title',
    '.tpl-xhs-white-editorial .xw-kicker',
    '.tpl-xhs-white-editorial .slide',
]

for selector in test_selectors:
    try:
        elements = soup.select(selector)
        print(f"  {selector}: 找到 {len(elements)} 个元素")
    except Exception as e:
        print(f"  {selector}: 错误 - {e}")
