#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to HTML Converter
将 Markdown 文件转换为带左侧目录导航的 HTML 页面
"""

import os
import re
import argparse
import html as html_module
import markdown

# 获取 lib 目录路径
LIB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')


def read_lib_file(filename):
    """读取 lib 目录下的文件内容"""
    filepath = os.path.join(LIB_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def get_embedded_resources():
    """获取内嵌的 CSS 和 JS 资源"""
    resources = {'css': '', 'js': '', 'katex_init': ''}
    
    # Prism CSS
    prism_css = read_lib_file('prism-tomorrow.min.css')
    if prism_css:
        resources['css'] += prism_css
    
    # KaTeX CSS（包含内嵌字体）
    katex_css = read_lib_file('katex.embedded.css')
    if not katex_css:
        katex_css = read_lib_file('katex.min.css')
    if katex_css:
        resources['css'] += '\n' + katex_css
    
    # KaTeX JS
    katex_js = read_lib_file('katex.min.js')
    if katex_js:
        resources['js'] += f'<script>{katex_js}</script>\n'
    
    # KaTeX auto-render
    auto_render_js = read_lib_file('auto-render.min.js')
    if auto_render_js:
        resources['js'] += f'<script>{auto_render_js}</script>\n'
    
    # Prism JS
    prism_core = read_lib_file('prism.min.js')
    if prism_core:
        resources['js'] += f'<script>{prism_core}</script>\n'
    
    for lang in ['python', 'bash', 'javascript', 'json']:
        prism_lang = read_lib_file(f'prism-{lang}.min.js')
        if prism_lang:
            resources['js'] += f'<script>{prism_lang}</script>\n'
    
    # Mermaid
    mermaid = read_lib_file('mermaid.min.js')
    if mermaid:
        resources['js'] += f'<script>{mermaid}</script>\n'
    
    return resources


def escape_html(text):
    """转义 HTML 特殊字符"""
    return html_module.escape(text)


def generate_html(title, toc_html, content_html):
    """生成完整的 HTML 页面"""
    # 获取内嵌资源
    resources = get_embedded_resources()
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)}</title>
    <style>{resources['css']}</style>
    {resources['js']}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --sidebar-bg: #1e3a5f;
            --sidebar-width: 280px;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f0f2f5;
        }}
        
        /* 侧边栏 */
        #sidebar {{
            position: fixed;
            left: 0;
            top: 0;
            width: var(--sidebar-width, 280px);
            min-width: 200px;
            max-width: 500px;
            height: 100vh;
            background: var(--sidebar-bg);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            will-change: width;
            backface-visibility: hidden;
        }}
        
        .sidebar-header {{
            padding: 16px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            flex-shrink: 0;
        }}
        
        .sidebar-title {{
            color: #fff;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        
        .controls {{
            display: flex;
            gap: 8px;
        }}
        
        .ctrl-btn {{
            padding: 6px 12px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 4px;
            color: #fff;
            cursor: pointer;
            font-size: 12px;
            transition: background 0.2s;
        }}
        
        .ctrl-btn:hover {{ background: rgba(255,255,255,0.2); }}
        
        /* 目录容器 */
        .toc-container {{
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 8px 0;
        }}
        
        .toc-container::-webkit-scrollbar {{ width: 6px; }}
        .toc-container::-webkit-scrollbar-track {{ background: transparent; }}
        .toc-container::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 3px; }}
        
        .toc-list {{ list-style: none; }}
        
        /* 目录项 - Flex布局 */
        .toc-item {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        /* 箭头按钮 */
        .toc-arrow {{
            flex-shrink: 0;
            width: 16px;
            height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background: transparent;
            border: none;
            border-radius: 4px;
            color: rgba(255,255,255,0.4);
            font-size: 8px;
            padding: 0;
            margin-right: 1px;
            transition: all 0.2s;
        }}
        
        .toc-arrow:hover {{
            color: #fff;
            background: rgba(255,255,255,0.1);
        }}
        .toc-arrow::before {{ content: "\\25B6"; }}
        
        .toc-item:not(.collapsed) > .toc-arrow::before {{
            transform: rotate(90deg);
            display: inline-block;
        }}
        
        .toc-arrow.empty {{
            visibility: hidden;
            pointer-events: none;
        }}
        
        /* 标题链接 */
        .toc-link {{
            flex: 1;
            min-width: 0;
            color: rgba(255,255,255,0.85);
            text-decoration: none;
            font-size: 13px;
            padding: 3px 6px;
            border-radius: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transition: all 0.15s;
            line-height: 1.4;
        }}
        
        .toc-link:hover {{
            background: rgba(255,255,255,0.08);
            color: #fff;
        }}
        .toc-item.active > .toc-link {{
            background: rgba(255,255,255,0.15);
            color: #fff;
        }}
        
        /* 层级缩进 - 紧凑，每级仅缩进 2px */
        .toc-item[data-level="1"] {{ padding-left: 6px; }}
        .toc-item[data-level="2"] {{ padding-left: 8px; }}
        .toc-item[data-level="3"] {{ padding-left: 10px; }}
        .toc-item[data-level="4"] {{ padding-left: 12px; }}
        .toc-item[data-level="5"] {{ padding-left: 14px; }}
        .toc-item[data-level="6"] {{ padding-left: 16px; }}
        .toc-item[data-level="1"] > .toc-link {{ font-weight: 600; color: #fff; }}
        
        /* 子目录 */
        .toc-children {{
            width: 100%;
            list-style: none;
        }}
        
        .toc-item.collapsed > .toc-children {{ display: none; }}
        
        /* 拖拽手柄 */
        #resize-handle {{
            position: fixed;
            left: var(--sidebar-width, 280px);
            top: 0;
            width: 6px;
            height: 100vh;
            cursor: col-resize;
            background: transparent;
            z-index: 100;
            transition: background 0.2s;
            will-change: left;
        }}
        
        #resize-handle:hover {{ background: rgba(66, 153, 225, 0.5); }}
        #resize-handle.dragging {{ background: rgba(66, 153, 225, 0.8); }}
        
        /* 主内容区 */
        #content {{
            margin-left: var(--sidebar-width, 280px);
            padding: 40px 60px;
            min-height: 100vh;
            background: #fff;
            will-change: margin-left;
        }}
        
        .content-wrapper {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #1a202c;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: 600;
        }}
        
        h1 {{
            font-size: 32px;
            margin-top: 0;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--sidebar-bg);
        }}
        
        h2 {{
            font-size: 24px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        h3 {{ font-size: 20px; }}
        h4 {{ font-size: 18px; }}
        
        p {{ margin-bottom: 1em; }}
        
        a {{ color: #2b6cb0; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        
        pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 16px 0;
        }}
        
        code {{
            font-family: "JetBrains Mono", "Fira Code", "Consolas", monospace;
            font-size: 14px;
        }}
        
        p code, li code {{
            background: #edf2f7;
            color: #d53f8c;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        
        pre code {{ background: none; padding: 0; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        th, td {{
            border: 1px solid #e2e8f0;
            padding: 12px 16px;
            text-align: left;
        }}
        
        th {{
            background: var(--sidebar-bg);
            color: #fff;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{ background: #f7fafc; }}
        
        blockquote {{
            border-left: 4px solid #4299e1;
            background: #ebf8ff;
            padding: 12px 20px;
            margin: 16px 0;
            color: #2c5282;
        }}
        
        blockquote p {{ margin-bottom: 0; }}
        
        ul, ol {{ margin: 16px 0; padding-left: 28px; }}
        li {{ margin-bottom: 6px; }}
        
        img {{ max-width: 100%; border-radius: 8px; margin: 16px 0; }}
        
        /* Mermaid 图表 */
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
            overflow-x: auto;
        }}
        
        /* KaTeX 公式样式 */
        .katex-display {{ margin: 1em 0; overflow-x: auto; }}
        .katex {{ font-size: 1.1em; }}
        
        /* 返回顶部 */
        #back-top {{
            position: fixed;
            right: 24px;
            bottom: 24px;
            width: 44px;
            height: 44px;
            background: var(--sidebar-bg);
            color: #fff;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            display: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 99;
        }}
        
        #back-top:hover {{ transform: translateY(-2px); }}
        
        /* 移动端 */
        #mobile-toggle {{
            display: none;
            position: fixed;
            left: 12px;
            top: 12px;
            z-index: 200;
            background: var(--sidebar-bg);
            color: #fff;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
        }}
        
        @media (max-width: 768px) {{
            :root {{ --sidebar-width: 280px !important; }}
            #sidebar {{ transform: translateX(-100%); transition: transform 0.3s; }}
            #sidebar.open {{ transform: translateX(0); }}
            #resize-handle {{ display: none; }}
            #content {{ margin-left: 0; padding: 20px; }}
            #mobile-toggle {{ display: block; }}
        }}
    </style>
</head>
<body>
    <button id="mobile-toggle">目录</button>
    
    <div id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-title">目录导航</div>
            <div class="controls">
                <button class="ctrl-btn" id="btn-expand">全部展开</button>
                <button class="ctrl-btn" id="btn-collapse">全部折叠</button>
            </div>
        </div>
        <div class="toc-container">
            <ul class="toc-list">{toc_html}</ul>
        </div>
    </div>
    
    <div id="resize-handle"></div>
    
    <div id="content">
        <div class="content-wrapper">{content_html}</div>
    </div>
    
    <button id="back-top">↑</button>

    <script>
    (function() {{
        'use strict';
        
        var sidebar = document.getElementById('sidebar');
        var content = document.getElementById('content');
        var resizeHandle = document.getElementById('resize-handle');
        var mobileToggle = document.getElementById('mobile-toggle');
        var backTop = document.getElementById('back-top');
        var btnExpand = document.getElementById('btn-expand');
        var btnCollapse = document.getElementById('btn-collapse');
        
        // 拖拽调整宽度 - 使用 CSS 变量优化性能
        var isResizing = false;
        var rafId = null;
        
        function updateWidth(width) {{
            document.documentElement.style.setProperty('--sidebar-width', width + 'px');
        }}
        
        resizeHandle.addEventListener('mousedown', function(e) {{
            isResizing = true;
            resizeHandle.classList.add('dragging');
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        }});
        
        document.addEventListener('mousemove', function(e) {{
            if (!isResizing) return;
            var width = Math.max(200, Math.min(500, e.clientX));
            if (!rafId) {{
                rafId = requestAnimationFrame(function() {{
                    updateWidth(width);
                    rafId = null;
                }});
            }}
        }});
        
        document.addEventListener('mouseup', function() {{
            if (isResizing) {{
                isResizing = false;
                resizeHandle.classList.remove('dragging');
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }}
        }});
        
        // 目录交互
        var tocItems = document.querySelectorAll('.toc-item');
        var scrollHighlightDisabled = false;
        var scrollHighlightTimer = null;
        
        tocItems.forEach(function(item) {{
            var arrow = item.querySelector('.toc-arrow');
            var link = item.querySelector('.toc-link');
            var children = item.querySelector('.toc-children');
            var hasChildren = children && children.children.length > 0;
            
            if (!hasChildren) arrow.classList.add('empty');
            
            // 点击标题：跳转并高亮
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                var anchor = this.getAttribute('data-anchor');
                var target = document.getElementById(anchor);
                if (target) {{
                    // 禁用滚动高亮1秒
                    scrollHighlightDisabled = true;
                    if (scrollHighlightTimer) clearTimeout(scrollHighlightTimer);
                    scrollHighlightTimer = setTimeout(function() {{
                        scrollHighlightDisabled = false;
                    }}, 1000);
                    
                    // 滚动到目标
                    window.scrollTo({{ top: target.offsetTop - 20, behavior: 'smooth' }});
                    
                    // 设置高亮
                    tocItems.forEach(function(t) {{ t.classList.remove('active'); }});
                    item.classList.add('active');
                }}
                if (window.innerWidth <= 768) sidebar.classList.remove('open');
            }});
            
            // 点击箭头：折叠/展开
            if (hasChildren) {{
                arrow.addEventListener('click', function(e) {{
                    e.stopPropagation();
                    item.classList.toggle('collapsed');
                }});
            }}
        }});
        
        // 全部展开
        btnExpand.addEventListener('click', function() {{
            tocItems.forEach(function(item) {{ item.classList.remove('collapsed'); }});
        }});
        
        // 全部折叠
        btnCollapse.addEventListener('click', function() {{
            tocItems.forEach(function(item) {{
                if (item.querySelector('.toc-children')) item.classList.add('collapsed');
            }});
        }});
        
        // 滚动高亮
        var headings = document.querySelectorAll('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]');
        var observer = new IntersectionObserver(function(entries) {{
            if (scrollHighlightDisabled) return;
            entries.forEach(function(entry) {{
                if (entry.isIntersecting) {{
                    var id = entry.target.id;
                    tocItems.forEach(function(item) {{
                        item.classList.remove('active');
                        if (item.querySelector('.toc-link[data-anchor="' + id + '"]')) item.classList.add('active');
                    }});
                }}
            }});
        }}, {{ rootMargin: '-20% 0px -70% 0px' }});
        
        headings.forEach(function(h) {{ observer.observe(h); }});
        
        // 移动端
        mobileToggle.addEventListener('click', function() {{ sidebar.classList.toggle('open'); }});
        content.addEventListener('click', function() {{ if (window.innerWidth <= 768) sidebar.classList.remove('open'); }});
        
        // 返回顶部
        window.addEventListener('scroll', function() {{ backTop.style.display = window.scrollY > 300 ? 'block' : 'none'; }});
        backTop.addEventListener('click', function() {{ window.scrollTo({{ top: 0, behavior: 'smooth' }}); }});
        
        // KaTeX - 自动渲染所有公式
        if (window.renderMathInElement) {{
            try {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: '$$', right: '$$', display: true}},
                        {{left: '$', right: '$', display: false}},
                        {{left: '\\\\[', right: '\\\\]', display: true}},
                        {{left: '\\\\(', right: '\\\\)', display: false}}
                    ],
                    throwOnError: false,
                    strict: false
                }});
            }} catch(e) {{
                console.warn('KaTeX rendering warning:', e);
            }}
        }}
        
        // 代码高亮
        if (window.Prism) Prism.highlightAll();
        
        // Mermaid 图表渲染 - 添加错误处理
        if (window.mermaid) {{
            mermaid.initialize({{ 
                startOnLoad: false,
                theme: 'default',
                securityLevel: 'loose',
                suppressErrorRendering: true
            }});
            // 查找所有 mermaid 代码块并渲染
            var mermaidBlocks = document.querySelectorAll('pre code.language-mermaid');
            mermaidBlocks.forEach(function(block, index) {{
                var pre = block.parentNode;
                var code = block.textContent;
                var div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = code;
                // 添加错误处理
                div.setAttribute('data-mermaid', 'true');
                pre.parentNode.replaceChild(div, pre);
            }});
            if (mermaidBlocks.length > 0) {{
                try {{
                    mermaid.run({{
                        querySelector: '.mermaid',
                        suppressErrors: true
                    }}).catch(function(err) {{
                        console.warn('Mermaid rendering warning:', err);
                    }});
                }} catch(e) {{
                    console.warn('Mermaid initialization error:', e);
                }}
            }}
        }}
    }})();
    </script>
</body>
</html>
'''


def parse_headings(md_content, max_level=4):
    """解析 Markdown 中的标题"""
    headings = []
    lines = md_content.split('\n')
    
    in_code = False
    in_frontmatter = md_content.strip().startswith('---')
    frontmatter_closed = not in_frontmatter
    code_fence_pattern = re.compile(r'^```\S*')
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        if in_frontmatter and not frontmatter_closed:
            if line.strip() == '---' and i > 0:
                frontmatter_closed = True
            continue
        
        if code_fence_pattern.match(line.strip()):
            in_code = not in_code
            continue
        
        if in_code:
            continue
        
        match = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            
            if level > max_level:
                continue
            
            title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
            title = re.sub(r'[*_`]+', '', title)
            title = re.sub(r'<[^>]+>', '', title)
            title = title.strip()
            
            if not title or len(title) > 150:
                continue
            
            # 过滤类似 # --- 的分隔线情况
            if re.match(r'^-{3,}$', title):
                continue
            
            anchor = generate_anchor(title, len(headings))
            headings.append({'level': level, 'title': title, 'anchor': anchor})
    
    return headings


def generate_anchor(title, index):
    """生成锚点 ID"""
    anchor = title.lower()
    anchor = re.sub(r'[^\w\u4e00-\u9fff-]', '-', anchor)
    anchor = re.sub(r'-+', '-', anchor)
    anchor = anchor.strip('-')
    
    if not anchor:
        anchor = f'section-{index}'
    
    if len(anchor) > 80:
        anchor = anchor[:80].rstrip('-')
    
    return anchor


def build_toc_tree(headings):
    """构建目录树"""
    if not headings:
        return []
    
    root = []
    stack = []
    
    for h in headings:
        while stack and stack[-1]['level'] >= h['level']:
            stack.pop()
        
        node = dict(h)
        
        if stack:
            parent = stack[-1]
            if 'children' not in parent:
                parent['children'] = []
            parent['children'].append(node)
        else:
            root.append(node)
        
        stack.append(node)
    
    return root


def render_toc(items):
    """渲染目录 HTML"""
    html_parts = []
    
    for item in items:
        level = item['level']
        title = escape_html(item['title'])
        anchor = item['anchor']
        children = item.get('children', [])
        has_children = bool(children)
        
        html_parts.append(f'<li class="toc-item" data-level="{level}">')
        
        # 箭头按钮
        arrow_class = 'toc-arrow'
        if not has_children:
            arrow_class += ' empty'
        html_parts.append(f'<button class="{arrow_class}"></button>')
        
        # 标题链接
        html_parts.append(f'<a class="toc-link" data-anchor="{anchor}">{title}</a>')
        
        # 子目录
        if has_children:
            html_parts.append('<ul class="toc-children">')
            html_parts.append(render_toc(children))
            html_parts.append('</ul>')
        
        html_parts.append('</li>')
    
    return '\n'.join(html_parts)


def render_content(md_content, headings, max_level=4):
    """渲染正文"""
    lines = md_content.split('\n')
    result = []
    heading_idx = 0
    
    in_code = False
    in_frontmatter = md_content.strip().startswith('---')
    frontmatter_closed = not in_frontmatter
    code_fence_pattern = re.compile(r'^```\S*')
    
    for line in lines:
        if in_frontmatter and not frontmatter_closed:
            if line.strip() == '---':
                frontmatter_closed = True
            result.append(line)
            continue
        
        if code_fence_pattern.match(line.strip()):
            in_code = not in_code
            result.append(line)
            continue
        
        if in_code:
            result.append(line)
            continue
        
        match = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if match:
            current_level = len(match.group(1))
            # 只处理在 max_level 范围内的标题
            if current_level <= max_level and heading_idx < len(headings):
                h = headings[heading_idx]
                level = h['level']
                title = escape_html(h['title'])
                anchor = h['anchor']
                result.append(f'<h{level} id="{anchor}">{title}</h{level}>')
                heading_idx += 1
            else:
                # 超出范围的标题，保留原始内容让 markdown 库处理
                result.append(line)
        else:
            result.append(line)
    
    md = markdown.Markdown(extensions=['extra', 'tables', 'fenced_code', 'toc', 'sane_lists'])
    return md.convert('\n'.join(result))


def convert(input_path, output_path=None, title=None, max_heading_level=4):
    """转换 Markdown 为 HTML"""
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    if not title:
        title = os.path.splitext(os.path.basename(input_path))[0]
    
    headings = parse_headings(md_content, max_level=max_heading_level)
    
    if not headings:
        print(f'[警告] 未找到有效的标题')
        return None
    
    toc_tree = build_toc_tree(headings)
    toc_html = render_toc(toc_tree)
    content_html = render_content(md_content, headings, max_heading_level)
    full_html = generate_html(title, toc_html, content_html)
    
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + '.html'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'[OK] 生成文件: {output_path}')
    print(f'[OK] 提取章节: {len(headings)} 个')
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Markdown 转 HTML')
    parser.add_argument('-i', '--input', required=True, help='输入 Markdown 文件')
    parser.add_argument('-o', '--output', help='输出 HTML 文件')
    parser.add_argument('-t', '--title', help='页面标题')
    parser.add_argument('-l', '--level', type=int, default=4, help='目录层级 (1-6)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f'错误: 文件不存在 {args.input}')
        return 1
    
    try:
        convert(args.input, args.output, args.title, args.level)
        return 0
    except Exception as e:
        print(f'错误: {e}')
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())