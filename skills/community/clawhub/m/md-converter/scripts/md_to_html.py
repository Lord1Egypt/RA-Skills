#!/usr/bin/env python3
"""Convert Markdown file to a styled, responsive HTML page.

Usage:
    python3 md_to_html.py <input.md> [output.html]
    If output is omitted, writes to the same path with .html extension.
"""

import sys
import re
import os


# ── Embedded CSS template ──────────────────────────────────────────────
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --primary: #4A90D9;
    --primary-dark: #2471A3;
    --accent: #1E8449;
    --bg: #F0F4F8;
    --card-bg: #FFFFFF;
    --text: #2C3E50;
    --text-light: #5D6D7E;
    --border: #D5DDE5;
    --tag-bg: #E8F0FE;
    --tag-text: #2471A3;
    --code-bg: #F7F9FB;
    --radius: 12px;
    --shadow: 0 2px 12px rgba(0,0,0,0.06);
    --shadow-lg: 0 4px 24px rgba(0,0,0,0.10);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    padding: 0 16px 60px;
  }}
  .hero {{
    max-width: 860px;
    margin: 0 auto;
    padding: 48px 24px 32px;
    text-align: center;
  }}
  .hero h1 {{
    font-size: 36px;
    font-weight: 700;
    color: var(--primary-dark);
    margin-bottom: 8px;
  }}
  .hero .subtitle {{
    font-size: 18px;
    color: var(--text-light);
    max-width: 560px;
    margin: 0 auto;
  }}
  .container {{ max-width: 860px; margin: 0 auto; }}
  .card {{
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px 32px;
    margin-bottom: 20px;
  }}
  .card h2 {{
    font-size: 22px;
    font-weight: 700;
    color: var(--primary-dark);
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border);
  }}
  .card h3 {{
    font-size: 17px;
    font-weight: 600;
    color: var(--text);
    margin: 18px 0 8px;
  }}
  .card p {{ color: var(--text-light); margin-bottom: 10px; }}
  .card ul, .card ol {{ padding-left: 24px; color: var(--text-light); margin-bottom: 10px; }}
  .card li {{ margin-bottom: 4px; }}
  .card strong {{ color: var(--text); }}
  code {{
    background: var(--code-bg);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 13px;
    color: #C0392B;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
  }}
  pre {{
    background: var(--code-bg);
    padding: 16px 20px;
    border-radius: var(--radius);
    overflow-x: auto;
    margin: 10px 0;
    font-size: 13px;
    line-height: 1.5;
  }}
  pre code {{
    background: none;
    padding: 0;
    color: var(--text);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 14px;
  }}
  table th {{
    background: var(--primary-dark);
    color: #fff;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
  }}
  table th:first-child {{ border-radius: var(--radius) 0 0 0; }}
  table th:last-child {{ border-radius: 0 var(--radius) 0 0; }}
  table td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text-light);
  }}
  table tr:nth-child(even) {{ background: var(--code-bg); }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 16px 0; }}
  blockquote {{
    border-left: 3px solid var(--primary);
    padding: 4px 16px;
    color: var(--text-light);
    margin: 10px 0;
    background: var(--code-bg);
    border-radius: 0 var(--radius) var(--radius) 0;
  }}
  a {{ color: var(--primary-dark); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .footer {{
    text-align: center;
    color: var(--text-light);
    font-size: 13px;
    padding: 20px 16px;
    opacity: 0.7;
  }}
  @media (max-width: 640px) {{
    .hero {{ padding: 32px 12px 20px; }}
    .hero h1 {{ font-size: 26px; }}
    .card {{ padding: 20px 18px; }}
    .card h2 {{ font-size: 19px; }}
  }}
</style>
</head>
<body>

<div class="hero">
  <h1>{title}</h1>
</div>

<div class="container">
{content}
</div>

</body>
</html>'''


def parse_inline(text):
    """Convert inline Markdown: bold, italic, code, links, images."""
    # images
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%">', text)
    # links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def convert_md_to_html(md_text):
    lines = md_text.split('\n')
    output = []
    i = 0
    in_card = False
    in_code_block = False
    code_buffer = []
    in_table = False
    table_rows = []
    in_list = False
    list_type = None  # 'ul' or 'ol'
    list_buffer = []

    def close_list():
        nonlocal in_list, list_buffer
        if not in_list:
            return
        tag = list_type if list_type else 'ul'
        output.append(f'<{tag}>')
        output.extend(list_buffer)
        output.append(f'</{tag}>')
        in_list = False
        list_buffer = []
        if in_card:
            pass

    def close_card():
        nonlocal in_card
        if not in_card and not output:
            return
        if in_card:
            output.append('</div>')
            in_card = False

    def flush_output():
        nonlocal output
        result = '\n'.join(output)
        output = []
        return result

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                lang = in_code_block
                code = '\n'.join(code_buffer)
                escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                output.append(f'<pre><code class="language-{lang}">{escaped}</code></pre>')
                code_buffer = []
                in_code_block = False
                i += 1
                continue
            else:
                in_code_block = line.strip()[3:].strip() or 'plaintext'
                i += 1
                continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Tables
        if '|' in line and line.strip().startswith('|') and not in_table:
            in_table = True
            table_rows = []
            # Collect all table rows
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                row = lines[i]
                if re.match(r'^\|[\s\-:|]+\|$', row.strip()):
                    # separator row, skip
                    i += 1
                    continue
                cells = [c.strip() for c in row.strip().strip('|').split('|')]
                table_rows.append(cells)
                i += 1
            # Render table
            if table_rows:
                html = ['<table>']
                # header
                html.append('<thead><tr>')
                for cell in table_rows[0]:
                    html.append(f'<th>{parse_inline(cell)}</th>')
                html.append('</tr></thead>')
                # body
                html.append('<tbody>')
                for row in table_rows[1:]:
                    html.append('<tr>')
                    for cell in row:
                        html.append(f'<td>{parse_inline(cell)}</td>')
                    html.append('</tr>')
                html.append('</tbody></table>')
                output.append('\n'.join(html))
            in_table = False
            continue

        # Horizontal rule
        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            output.append('<hr>')
            i += 1
            continue

        # Blockquote
        if line.startswith('> '):
            close_list()
            if not in_card:
                output.append('<div class="card">')
                in_card = True
            quote_parts = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_parts.append(parse_inline(lines[i][2:]))
                i += 1
            output.append(f'<blockquote>{"<br>".join(quote_parts)}</blockquote>')
            continue

        # Headings
        h_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h_match:
            close_list()
            level = len(h_match.group(1))
            text = parse_inline(h_match.group(2))
            heading_id = re.sub(r'<[^>]+>', '', text).strip().lower().replace(' ', '-')

            if level == 1:
                close_card()
                output.append(f'<h1 id="{heading_id}">{text}</h1>')
            elif level == 2:
                close_card()
                output.append(f'<div class="card"><h2 id="{heading_id}">{text}</h2>')
                in_card = True
            else:
                output.append(f'<h{level} id="{heading_id}">{text}</h{level}>')
            i += 1
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if ol_match:
            if not in_list or list_type != 'ol':
                close_list()
                in_list = True
                list_type = 'ol'
            list_buffer.append(f'<li>{parse_inline(ol_match.group(2))}</li>')
            i += 1
            continue

        # Unordered list
        ul_match = re.match(r'^[-*+]\s+(.+)$', line)
        if ul_match:
            if not in_list or list_type != 'ul':
                close_list()
                in_list = True
                list_type = 'ul'
            list_buffer.append(f'<li>{parse_inline(ul_match.group(1))}</li>')
            i += 1
            continue

        # Paragraph
        if line.strip():
            close_list()
            if not in_card:
                output.append('<div class="card">')
                in_card = True
            output.append(f'<p>{parse_inline(line.strip())}</p>')
            i += 1
            continue

        # Empty line
        close_list()
        i += 1

    # Flush remaining
    close_list()
    close_card()

    return '\n'.join(output)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(input_path)[0] + '.html'

    with open(input_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Extract title from first h1
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.splitext(os.path.basename(input_path))[0]

    body = convert_md_to_html(md_text)
    html = HTML_TEMPLATE.format(title=title, content=body)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'HTML generated: {output_path}')


if __name__ == '__main__':
    main()
