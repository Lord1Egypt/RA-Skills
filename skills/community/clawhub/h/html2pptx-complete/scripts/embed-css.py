#!/usr/bin/env python3
"""
步骤 1: CSS 内嵌脚本
将外部 CSS 文件嵌入到 HTML 的 <style> 标签中，移除 <link> 引用
"""

import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup


def embed_css(html_path, output_path=None):
    """将外部 CSS 嵌入 HTML"""
    html_path = Path(html_path)
    
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    
    # 读取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    base_dir = html_path.parent
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有 <link rel="stylesheet" href="..."> 标签
    links = soup.find_all('link', rel='stylesheet')
    
    if not links:
        print("✅ No external CSS links found")
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Saved: {output_path}")
        return str(soup)
    
    print(f"📎 Found {len(links)} external CSS link(s)")
    
    # 收集 CSS 内容
    css_blocks = []
    removed_count = 0
    
    for link in links:
        href = link.get('href', '')
        
        # 跳过远程 CSS
        if href.startswith(('http://', 'https://')):
            print(f"  ⚠️  Skipping remote CSS: {href}")
            continue
        
        # 解析 CSS 文件路径
        css_path = base_dir / href
        
        if not css_path.exists():
            print(f"  ⚠️  CSS file not found: {css_path}")
            continue
        
        # 读取 CSS 内容
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        css_blocks.append(f"<!-- Embedded from: {href} -->\n{css_content}")
        print(f"  ✅ Embedded: {css_path.name}")
        
        # 移除 <link> 标签
        link.decompose()
        removed_count += 1
    
    # 创建 <style> 标签并插入到 <head>
    if css_blocks:
        head = soup.find('head')
        if head:
            style_tag = soup.new_tag('style')
            style_tag.string = '\n\n'.join(css_blocks)
            head.append(style_tag)
            print(f"✅ Created <style> tag in <head>")
    
    # 保存输出
    output_html = str(soup)
    
    if not output_path:
        output_path = html_path.with_name(f'{html_path.stem}_embedded.html')
    else:
        output_path = Path(output_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_html)
    
    print(f"💾 Saved: {output_path}")
    print(f"✅ Done! Removed {removed_count} <link> tag(s), embedded {len(css_blocks)} CSS file(s)")
    
    return output_html


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
