#!/usr/bin/env python3
"""调试 CSS 变量收集"""

import cssutils
from pathlib import Path

cssutils.log.setLevel('CRITICAL')

# 读取所有 CSS 文件
css_files = [
    '/Users/panda/.openclaw/workspace/skills/html-ppt/assets/fonts.css',
    '/Users/panda/.openclaw/workspace/skills/html-ppt/assets/base.css',
    '/Users/panda/.openclaw/workspace/skills/html-ppt/assets/themes/xiaohongshu-white.css',
    '/Users/panda/.openclaw/workspace/examples/openclaw-intro/style.css',
]

all_css = ""
for css_file in css_files:
    with open(css_file, 'r', encoding='utf-8') as f:
        all_css += f.read() + "\n"

# 解析 CSS
sheet = cssutils.parseString(all_css)

# 收集变量
css_vars = {}
for rule in sheet:
    if hasattr(rule, 'style'):
        for prop in rule.style:
            if prop.name.startswith('--'):
                css_vars[prop.name] = prop.value

print(f"✅ 收集到 {len(css_vars)} 个 CSS 变量\n")

# 检查特定变量
check_vars = ['--xw-bg', '--xw-line', '--accent', '--ease', '--text-1', '--bg']
for var in check_vars:
    if var in css_vars:
        print(f"✅ {var}: {css_vars[var]}")
    else:
        print(f"❌ {var}: 未找到")
