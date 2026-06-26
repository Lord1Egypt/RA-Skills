#!/usr/bin/env python3
"""
embed-css.py — 将外部 CSS 文件嵌入到 HTML 内部

用法:
    python3 embed-css.py <input.html> [output.html]

功能:
    - 读取 HTML 中的 <link rel="stylesheet" href="xxx.css"> 标签
    - 读取对应的 CSS 文件内容
    - 替换为 <style>xxx CSS 内容</style>
    - 输出内联后的 HTML
"""

import sys
import re
from pathlib import Path


def embed_css(html_path, output_path=None):
    """将外部 CSS 嵌入 HTML"""
    html_path = Path(html_path)
    
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    
    # 读取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    base_dir = html_path.parent
    
    # 查找所有 <link rel="stylesheet" href="..."> 标签
    link_pattern = r'<link\s+rel=["\']stylesheet["\']\s+href=["\']([^"\']+)["\'][^>]*>'
    
    matches = list(re.finditer(link_pattern, html_content, re.IGNORECASE))
    
    if not matches:
        print("No external CSS links found.")
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Saved: {output_path}")
        return html_content
    
    print(f"Found {len(matches)} external CSS link(s)")
    
    # 从后往前替换，避免位置偏移
    for match in reversed(matches):
        css_href = match.group(1)
        
        # 解析 CSS 文件路径
        if css_href.startswith(('http://', 'https://')):
            print(f"  ⚠️  Skipping remote CSS: {css_href}")
            continue
        
        css_path = base_dir / css_href
        
        if not css_path.exists():
            print(f"  ⚠️  CSS file not found: {css_path}")
            continue
        
        # 读取 CSS 内容
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # 创建 <style> 标签
        style_tag = f'<style>\n{css_content}\n</style>'
        
        # 替换 <link> 标签
        html_content = html_content[:match.start()] + style_tag + html_content[match.end():]
        print(f"  ✅ Embedded: {css_path.name}")
    
    # 保存输出
    if not output_path:
        output_path = html_path.with_name(f'{html_path.stem}_embedded.html')
    else:
        output_path = Path(output_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Saved: {output_path}")
    return html_content


def run(args=None):
    """主入口"""
    if args is None:
        args = sys.argv[1:]
    
    if len(args) < 1:
        print("Usage: python3 embed-css.py <input.html> [output.html]")
        sys.exit(1)
    
    html_path = args[0]
    output_path = args[1] if len(args) > 1 else None
    
    embed_css(html_path, output_path)


if __name__ == '__main__':
    run()
