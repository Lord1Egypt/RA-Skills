#!/usr/bin/env python3
"""将 Markdown 转为带 KaTeX 渲染的 HTML（Python 侧完整转换）"""
import sys, os, re, base64

def md_to_html(md_path, html_path=None):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if html_path is None:
        html_path = os.path.splitext(md_path)[0] + '.html'
    
    html_dir = os.path.dirname(os.path.abspath(html_path))
    md_dir = os.path.dirname(os.path.abspath(md_path))
    
    title = "学习笔记"
    t = re.search(r'^# (.+)', content)
    if t: title = t.group(1).strip()
    
    # === Python 侧 Markdown → HTML 转换 ===
    
    # 1. 保存公式，避免被后续处理破坏
    display_maths = {}
    def save_display(m):
        k = f"@@DISP_{len(display_maths)}@@"
        display_maths[k] = m.group(0)
        return f'<div class="math-display">{k}</div>'
    content = re.sub(r'\$\$(.+?)\$\$', save_display, content, flags=re.DOTALL)
    
    inline_maths = {}
    def save_inline(m):
        k = f"@@INLN_{len(inline_maths)}@@"
        inline_maths[k] = m.group(0)
        return k
    content = re.sub(r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)', save_inline, content)
    
    # 2. 图片 ![alt](path) → <img>
    # 计算 assets 的相对路径
    assets_rel = os.path.relpath(
        os.path.join(md_dir, 'assets'),
        html_dir
    ) if os.path.isdir(os.path.join(md_dir, 'assets')) else 'assets'
    
    def replace_img(m):
        alt = m.group(1)
        src = m.group(2)
        if src.startswith('assets/'):
            src = os.path.join(assets_rel, src[7:])
        return f'<img src="{src}" alt="{alt}" loading="lazy">'
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, content)
    
    # 3. 链接
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # 4. 代码块
    content = re.sub(r'```(\w*)\n(.*?)```', lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2)}</code></pre>', content, flags=re.DOTALL)
    
    # 5. 行内代码
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
    
    # 6. 水平线
    content = re.sub(r'^---+$', '<hr>', content, flags=re.MULTILINE)
    
    # 7. 标题
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # 8. 表格
    def table_to_html(m):
        rows = m.group(0).strip().split('\n')
        if len(rows) < 2: return m.group(0)
        html_tbl = ['<table>']
        for i, row in enumerate(rows):
            if re.match(r'^[\s\|:\-]+\|[\s\|:\-]+$', row):
                continue  # 分隔行
            cells = [c.strip() for c in row.split('|')[1:-1]]
            tag = 'th' if i == 1 else 'td'
            html_tbl.append(f'<tr>{"".join(f"<{tag}>{c}</{tag}>" for c in cells)}</tr>')
        html_tbl.append('</table>')
        return ''.join(html_tbl)
    content = re.sub(r'^(\|.+\|)\n(\|[-:| ]+\|)\n(\|.+\|(?:\n\|.+\|)*)', table_to_html, content, flags=re.MULTILINE)
    content = re.sub(r'^(\|.+\|)\n(\|[-:| ]+\|)', table_to_html, content, flags=re.MULTILINE)
    
    # 9. 粗体/斜体
    content = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', content)
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', content)
    
    # 10. 无序列表
    lines = content.split('\n')
    result = []
    in_list = False
    for line in lines:
        if re.match(r'^[\s]*[-*+]\s+', line):
            text = re.sub(r'^[\s]*[-*+]\s+', '', line)
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{text}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            # 段落包装：非空行、非标题、非表格、非代码、非列表项
            stripped = line.strip()
            if stripped and not stripped.startswith('<h') and not stripped.startswith('<') and not stripped.startswith('</') and not stripped.startswith('|') and not line.strip().startswith('```'):
                result.append(f'<p>{stripped}</p>')
            else:
                result.append(line)
    if in_list:
        result.append('</ul>')
    content = '\n'.join(result)
    
    # 11. 恢复公式
    for k, v in display_maths.items():
        content = content.replace(f'<div class="math-display">{k}</div>', v)
    for k, v in inline_maths.items():
        content = content.replace(k, v)
    
    # 构建 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0d1117; color: #c9d1d9;
    font-family: Arial, 'Microsoft YaHei', '微软雅黑', sans-serif;
    line-height: 1.8; padding: 40px 20px;
    max-width: 900px; margin: 0 auto; font-size: 15px;
  }}
  h1 {{ color: #58a6ff; font-size: 26px; margin: 32px 0 8px; }}
  h2 {{ color: #58a6ff; font-size: 21px; margin: 28px 0 8px; border-bottom: 1px solid #30363d; padding-bottom: 6px; }}
  h3 {{ color: #f0883e; font-size: 17px; margin: 20px 0 6px; }}
  h4 {{ color: #8b949e; font-size: 15px; margin: 16px 0 4px; }}
  p {{ margin: 8px 0; text-align: justify; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin: 12px 0; }}
  th, td {{ border: 1px solid #30363d; padding: 6px 10px; text-align: left; }}
  th {{ background: #161b22; color: #58a6ff; font-weight: 600; }}
  td {{ background: #0d1117; }}
  pre {{ background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 14px; overflow-x: auto; margin: 12px 0; }}
  code {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 13px; }}
  pre code {{ background: none; border: none; padding: 0; }}
  p > code, li > code {{ background: #21262d; padding: 1px 5px; border-radius: 3px; font-size: 13px; }}
  img {{ max-width: 100%; border-radius: 6px; border: 1px solid #30363d; margin: 12px 0; display: block; }}
  blockquote {{
    border-left: 3px solid #58a6ff; background: #161b22;
    padding: 10px 18px; margin: 12px 0; border-radius: 0 6px 6px 0;
  }}
  ul, ol {{ margin: 8px 0; padding-left: 26px; }}
  li {{ margin: 4px 0; }}
  hr {{ border: none; border-top: 1px solid #30363d; margin: 24px 0; }}
  .math-display {{ margin: 12px 0; overflow-x: auto; text-align: center; }}
  .katex {{ font-family: 'Times New Roman', Times, serif; font-size: 1.05em; }}
  .katex-display {{ margin: 12px 0; }}
  a {{ color: #58a6ff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
{content}

<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<script>
  if (window.renderMathInElement) {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ]
    }});
  }}
</script>
</body>
</html>'''

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    size = os.path.getsize(html_path)
    print(f"✅ {os.path.basename(html_path)} ({size//1024} KB)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: md2html.py <input.md> [output.html]")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    md_to_html(sys.argv[1], out)
