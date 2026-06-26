#!/usr/bin/env python3
"""Convert Markdown to a beautiful scrollable wide-screen HTML page.

Supports:
- Standard markdown (headings, paragraphs, lists, code blocks, images, tables)
- File trees (```tree)
- Blockquote callouts (>, 💡, ⚠️)
- ::: directive blocks (card, card-grid, compare, flow, quote, layers, cycle, cmd-list)
- Dark/light theme toggle
- Image compression + base64 embedding (--embed-images)
- Scroll-reveal animations
"""

import argparse
import base64
import html as html_module
import os
import re
import sys
from pathlib import Path

# ─── Helpers ───


def escape(text: str) -> str:
    return html_module.escape(text, quote=False)


def _file_icon(name: str) -> str:
    if name.endswith('/'):
        return '📂'
    ext = name.rsplit('.', 1)[-1] if '.' in name else ''
    icons = {
        'py': '🐍', 'js': '📜', 'ts': '📜', 'sh': '⚙️',
        'json': '🔗', 'yaml': '📝', 'yml': '📝', 'toml': '📝',
        'md': '📄', 'html': '🌐', 'css': '🎨',
    }
    if name == 'SKILL.md':
        return '⚡'
    if name == 'MEMORY.md':
        return '📋'
    return icons.get(ext, '📄')


def _parse_tree_line(line: str):
    cleaned = re.sub(r'^[│├└─┬ ]+', '', line)
    if not cleaned.strip():
        return None
    raw_prefix = line[:len(line) - len(cleaned)]
    level = raw_prefix.count('├') + raw_prefix.count('└') + raw_prefix.count('│')
    if level == 0:
        level = (len(line) - len(line.lstrip())) // 4
    parts = cleaned.strip().split('#', 1)
    name = parts[0].strip()
    desc = parts[1].strip() if len(parts) > 1 else ''
    return (level, name, desc)


def _tree_to_html(tree_text: str) -> str:
    lines = tree_text.strip().split('\n')
    parsed = []
    for line in lines:
        if not line.strip():
            continue
        result = _parse_tree_line(line)
        if result:
            parsed.append(result)
    if not parsed:
        return ''

    html_parts = ['<div class="file-tree reveal"><ul>']
    stack = []

    for idx, (level, name, desc) in enumerate(parsed):
        while stack and stack[-1] >= level:
            html_parts.append('</ul></li>')
            stack.pop()

        icon = _file_icon(name)
        is_dir = name.endswith('/')
        name_cls = 'tree-name dir' if is_dir else 'tree-name'
        desc_html = f'<span class="tree-desc">{escape(desc)}</span>' if desc else ''
        item_html = f'<span class="tree-item"><span class="tree-icon">{icon}</span><span class="{name_cls}">{escape(name)}</span>{desc_html}</span>'

        next_level = parsed[idx + 1][0] if idx + 1 < len(parsed) else -1
        if next_level > level:
            html_parts.append(f'<li>{item_html}<ul>')
            stack.append(level)
        else:
            html_parts.append(f'<li>{item_html}</li>')

    while stack:
        html_parts.append('</ul></li>')
        stack.pop()

    html_parts.append('</ul></div>')
    return '\n'.join(html_parts)


def inline_md(text: str) -> str:
    """Convert inline markdown: bold, italic, code, links, images."""
    # Images
    text = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        lambda m: f'<img src="{escape(m.group(2))}" alt="{escape(m.group(1))}" style="max-width:100%;border-radius:8px;margin:0.5rem 0">',
        text,
    )
    # Links
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: f'<a href="{escape(m.group(2))}" target="_blank" style="color:var(--accent);text-decoration:underline">{m.group(1)}</a>',
        text,
    )
    # Inline code
    text = re.sub(
        r'`([^`]+)`',
        lambda m: f'<code style="background:var(--bg-code);padding:0.15em 0.4em;border-radius:4px;font-size:0.9em">{escape(m.group(1))}</code>',
        text,
    )
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (single *)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    return text


# ─── Image Embedding ───


def embed_images_in_md(md_text: str, base_dir: Path) -> str:
    """Replace local image references with base64 data URIs."""
    def replace_img(m):
        alt = m.group(1)
        src = m.group(2)
        # Skip URLs
        if src.startswith('http://') or src.startswith('https://'):
            return m.group(0)
        if src == 'placeholder' or src.startswith('placeholder'):
            return m.group(0)

        img_path = base_dir / src
        if not img_path.exists():
            return m.group(0)

        try:
            # Try Pillow compression
            from PIL import Image as PILImage
            import io
            img = PILImage.open(img_path)
            # Convert RGBA to RGB for JPEG
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            # Resize if wider than 1200px
            if img.width > 1200:
                ratio = 1200 / img.width
                img = img.resize((1200, int(img.height * ratio)), PILImage.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=75, optimize=True)
            b64 = base64.b64encode(buf.getvalue()).decode()
            data_uri = f'data:image/jpeg;base64,{b64}'
        except ImportError:
            # Fallback: raw base64
            raw = img_path.read_bytes()
            ext = img_path.suffix.lower()
            mime_map = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                        '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml'}
            mime = mime_map.get(ext, 'image/png')
            b64 = base64.b64encode(raw).decode()
            data_uri = f'data:{mime};base64,{b64}'

        return f'![{alt}]({data_uri})'

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, md_text)


# ─── Directive Parsing ───


def _parse_directive_attrs(attr_str: str) -> dict:
    """Parse {icon=💬 title="Card Title"} into a dict."""
    attrs = {}
    if not attr_str:
        return attrs
    attr_str = attr_str.strip().strip('{}')
    # Match key=value or key="value with spaces"
    for m in re.finditer(r'(\w+)=(?:"([^"]*?)"|(\S+))', attr_str):
        key = m.group(1)
        val = m.group(2) if m.group(2) is not None else m.group(3)
        attrs[key] = val
    return attrs


def _render_card(content_lines: list, attrs: dict) -> str:
    icon = attrs.get('icon', '')
    title = attrs.get('title', '')
    content = inline_md('\n'.join(content_lines).strip())

    parts = ['<div class="card reveal">']
    if icon:
        parts.append(f'  <div class="card-icon">{icon}</div>')
    if title:
        parts.append(f'  <div class="card-title">{inline_md(title)}</div>')
    if content:
        parts.append(f'  <div class="card-desc">{content}</div>')
    parts.append('</div>')
    return '\n'.join(parts)


def _render_flow(content_text: str, modifier: str) -> str:
    """Render ::: flow ... ::: block.
    *text* = highlighted step, ~text~ = dead step.
    modifier can be 'dead-suffix' to add style="opacity:0.4".
    """
    text = content_text.strip()
    # Split on arrows (→ or ←)
    parts = re.split(r'\s*(→|←)\s*', text)

    style = ''
    if modifier and 'dead-suffix' in modifier:
        style = ' style="opacity:0.4"'

    html_parts = [f'<div class="flow reveal"{style}>']
    for part in parts:
        part = part.strip()
        if part in ('→', '←'):
            html_parts.append(f'<span class="arrow">{part}</span>')
        elif part.startswith('*') and part.endswith('*'):
            inner = part.strip('*')
            html_parts.append(f'<span class="step highlight">{escape(inner)}</span>')
        elif part.startswith('~') and part.endswith('~'):
            inner = part.strip('~')
            html_parts.append(f'<span class="step dead">{escape(inner)}</span>')
        else:
            html_parts.append(f'<span class="step">{escape(part)}</span>')
    html_parts.append('</div>')
    return '\n'.join(html_parts)


def _render_quote(content_text: str) -> str:
    lines = content_text.strip().split('\n')
    # Last line starting with — is attribution
    quote_lines = []
    attr_line = ''
    for line in lines:
        if line.strip().startswith('—'):
            attr_line = line.strip()
        else:
            quote_lines.append(line)

    quote_html = inline_md('<br>'.join(quote_lines))
    parts = ['<div class="quote-block reveal">']
    parts.append(f'  <div class="quote-text">{quote_html}</div>')
    if attr_line:
        parts.append(f'  <div style="margin-top:1rem;color:var(--text-dim);font-size:0.9rem">{escape(attr_line)}</div>')
    parts.append('</div>')
    return '\n'.join(parts)


def _render_layers(content_text: str) -> str:
    lines = [l.strip() for l in content_text.strip().split('\n') if l.strip()]
    parts = ['<div class="layers reveal">']
    for line in lines:
        if '|' in line:
            tag, desc = line.split('|', 1)
            tag = tag.strip()
            desc = desc.strip()
        else:
            tag = line
            desc = ''
        parts.append(f'  <div class="layer"><span class="layer-tag">{escape(tag)}</span><span>{inline_md(desc)}</span></div>')
    parts.append('</div>')
    return '\n'.join(parts)


def _render_cycle(content_text: str, polarity: str) -> str:
    """polarity = 'negative' or 'positive'"""
    text = content_text.strip()
    parts_raw = re.split(r'\s*(→|←)\s*', text)

    html_parts = ['<div class="cycle reveal">']
    for part in parts_raw:
        part = part.strip()
        if part in ('→', '←', '↻'):
            html_parts.append(f'<span class="arrow">{part}</span>')
        elif not part:
            continue
        else:
            html_parts.append(f'<span class="node {polarity}">{escape(part)}</span>')
    html_parts.append('</div>')
    return '\n'.join(html_parts)


def _render_cmd_list(content_text: str) -> str:
    lines = [l.strip() for l in content_text.strip().split('\n') if l.strip()]
    parts = ['<div class="cmd-list reveal">']
    for line in lines:
        # Split on first — or --
        m = re.match(r'^(.+?)\s*[—–]\s*(.+)$', line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            parts.append(f'  <div class="cmd"><span class="key">{inline_md(key)}</span><span class="val">{escape(val)}</span></div>')
        else:
            parts.append(f'  <div class="cmd"><span class="key">{inline_md(line)}</span></div>')
    parts.append('</div>')
    return '\n'.join(parts)


# ─── Table Parsing ───


def _render_table(header_line: str, rows: list) -> str:
    """Render a markdown table as styled HTML table."""
    def parse_cells(line):
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|'):
            line = line[:-1]
        return [c.strip() for c in line.split('|')]

    headers = parse_cells(header_line)
    parts = ['<table class="styled-table reveal">', '<thead><tr>']
    for h in headers:
        parts.append(f'  <th>{inline_md(h)}</th>')
    parts.append('</tr></thead>')
    parts.append('<tbody>')
    for row in rows:
        cells = parse_cells(row)
        parts.append('<tr>')
        for c in cells:
            parts.append(f'  <td>{inline_md(c)}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table>')
    return '\n'.join(parts)


# ─── Main Parser ───


def parse_markdown(md_text: str) -> list:
    """Parse markdown into a list of block elements."""
    blocks = []
    lines = md_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty lines
        if not stripped:
            i += 1
            continue

        # Horizontal rules
        if re.match(r'^-{3,}$|^\*{3,}$|^_{3,}$', stripped):
            i += 1
            continue

        # ::: directive blocks
        if stripped.startswith(':::'):
            i = _parse_directive(lines, i, blocks)
            continue

        # Fenced code block
        if stripped.startswith('```'):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1
            if lang == 'tree':
                blocks.append(('tree', '\n'.join(code_lines)))
            else:
                blocks.append(('code', lang, '\n'.join(code_lines)))
            continue

        # Headings
        m = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            blocks.append(('heading', level, text))
            i += 1
            continue

        # Table: header | sep | rows
        if '|' in stripped and i + 1 < len(lines):
            next_stripped = lines[i + 1].strip()
            if re.match(r'^[\|\s:_-]+$', next_stripped) and '|' in next_stripped:
                # It's a table
                header_line = stripped
                i += 2  # skip header and separator
                table_rows = []
                while i < len(lines) and '|' in lines[i].strip() and lines[i].strip():
                    table_rows.append(lines[i].strip())
                    i += 1
                blocks.append(('table', header_line, table_rows))
                continue

        # Blockquote
        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(re.sub(r'^>\s?', '', lines[i].strip()))
                i += 1
            blocks.append(('blockquote', '\n'.join(quote_lines)))
            continue

        # Unordered list
        if re.match(r'^[-*+]\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*+]\s', lines[i]):
                item_text = re.sub(r'^\s*[-*+]\s+', '', lines[i]).strip()
                items.append(item_text)
                i += 1
            blocks.append(('ul', items))
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s', lines[i]):
                item_text = re.sub(r'^\s*\d+\.\s+', '', lines[i]).strip()
                items.append(item_text)
                i += 1
            blocks.append(('ol', items))
            continue

        # Image on its own line
        img_m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', stripped)
        if img_m:
            blocks.append(('image', img_m.group(1), img_m.group(2)))
            i += 1
            continue

        # Paragraph
        para_lines = []
        while i < len(lines):
            l = lines[i].strip()
            if not l or l.startswith('#') or l.startswith('>') or l.startswith('```') \
                    or l.startswith(':::') \
                    or re.match(r'^[-*+]\s', l) or re.match(r'^\d+\.\s', l) \
                    or re.match(r'^-{3,}$|^\*{3,}$|^_{3,}$', l):
                break
            para_lines.append(l)
            i += 1
        if para_lines:
            blocks.append(('paragraph', ' '.join(para_lines)))

    return blocks


def _parse_directive(lines: list, start: int, blocks: list) -> int:
    """Parse a ::: directive block. Returns the new line index."""
    opening = lines[start].strip()
    # ::: type [modifier] [{attrs}]
    rest = opening[3:].strip()

    # Extract {attrs} if present on this line
    attr_match = re.search(r'\{([^}]*)\}', rest)
    attrs = {}
    if attr_match:
        attrs = _parse_directive_attrs(attr_match.group(0))
        rest = rest[:attr_match.start()].strip()

    parts = rest.split(None, 1)
    dtype = parts[0] if parts else ''
    modifier = parts[1] if len(parts) > 1 else ''

    i = start + 1
    # Collect content until matching :::
    # For nested directives, we need depth tracking
    content_lines = []
    depth = 1

    while i < len(lines):
        s = lines[i].strip()
        if s.startswith(':::') and len(s) > 3 and s[3:].strip():
            # Opening a nested directive
            depth += 1
            content_lines.append(lines[i])
        elif s == ':::':
            depth -= 1
            if depth == 0:
                i += 1
                break
            else:
                content_lines.append(lines[i])
        else:
            content_lines.append(lines[i])
        i += 1

    content_text = '\n'.join(content_lines)

    # Dispatch by type
    if dtype == 'card' and not _has_nested_directives(content_lines):
        blocks.append(('directive_html', _render_card(content_lines, attrs)))
    elif dtype == 'card-grid':
        blocks.append(('directive_html', _render_card_grid(content_lines)))
    elif dtype == 'compare':
        blocks.append(('directive_html', _render_compare(content_lines)))
    elif dtype == 'flow':
        blocks.append(('directive_html', _render_flow(content_text, modifier)))
    elif dtype == 'quote':
        blocks.append(('directive_html', _render_quote(content_text)))
    elif dtype == 'layers':
        blocks.append(('directive_html', _render_layers(content_text)))
    elif dtype == 'cycle':
        polarity = modifier.strip() if modifier.strip() in ('negative', 'positive') else 'positive'
        blocks.append(('directive_html', _render_cycle(content_text, polarity)))
    elif dtype == 'cmd-list':
        blocks.append(('directive_html', _render_cmd_list(content_text)))
    elif dtype == 'side':
        # Standalone side — shouldn't happen outside compare, but handle gracefully
        blocks.append(('directive_html', _render_side(content_lines, dtype, modifier, attrs)))
    else:
        # Unknown directive: render as blockquote
        blocks.append(('blockquote', content_text))

    return i


def _has_nested_directives(content_lines: list) -> bool:
    for line in content_lines:
        if line.strip().startswith(':::'):
            return True
    return False


def _render_card_grid(content_lines: list) -> str:
    """Parse nested ::: card blocks inside a card-grid."""
    cards_html = []
    i = 0
    while i < len(content_lines):
        s = content_lines[i].strip()
        if s.startswith('::: card'):
            rest = s[8:].strip()
            attr_match = re.search(r'\{([^}]*)\}', rest)
            attrs = _parse_directive_attrs(attr_match.group(0)) if attr_match else {}
            i += 1
            card_lines = []
            while i < len(content_lines) and content_lines[i].strip() != ':::':
                card_lines.append(content_lines[i])
                i += 1
            i += 1  # skip :::
            cards_html.append(_render_card(card_lines, attrs))
        else:
            i += 1

    return f'<div class="card-grid reveal">\n{"".join(cards_html)}\n</div>'


def _render_compare(content_lines: list) -> str:
    """Parse nested ::: side blocks inside a compare."""
    sides_html = []
    i = 0
    while i < len(content_lines):
        s = content_lines[i].strip()
        if s.startswith('::: side'):
            rest = s[8:].strip()
            # Parse: side_type {label="..."}
            attr_match = re.search(r'\{([^}]*)\}', rest)
            attrs = _parse_directive_attrs(attr_match.group(0)) if attr_match else {}
            side_rest = rest[:attr_match.start()].strip() if attr_match else rest
            side_type = side_rest.strip()  # 'good' or 'bad'

            i += 1
            side_lines = []
            while i < len(content_lines) and content_lines[i].strip() != ':::':
                side_lines.append(content_lines[i])
                i += 1
            i += 1  # skip :::

            label = attrs.get('label', '')
            content = inline_md('\n'.join(side_lines).strip())
            cls = f'side {side_type}'
            sides_html.append(
                f'<div class="{cls}">'
                f'<div class="side-label">{escape(label)}</div>'
                f'<div>{content}</div>'
                f'</div>'
            )
        else:
            i += 1

    return f'<div class="compare reveal">\n{"".join(sides_html)}\n</div>'


def _render_side(content_lines, dtype, modifier, attrs):
    """Fallback for standalone side blocks."""
    label = attrs.get('label', '')
    content = inline_md('\n'.join(content_lines).strip())
    cls = f'side {modifier.strip()}'
    return (
        f'<div class="{cls}">'
        f'<div class="side-label">{escape(label)}</div>'
        f'<div>{content}</div>'
        f'</div>'
    )


# ─── HTML Renderer ───


def render_html(blocks: list, title_override: str = None, footer_text: str = 'Generated by md-to-page') -> str:
    """Render parsed blocks into a full HTML page."""

    # Extract hero content from first H1
    hero_title = "Untitled"
    hero_subtitle = ""
    content_start = 0

    for idx, block in enumerate(blocks):
        if block[0] == 'heading' and block[1] == 1:
            hero_title = block[2]
            content_start = idx + 1
            if content_start < len(blocks) and blocks[content_start][0] == 'paragraph':
                hero_subtitle = blocks[content_start][1]
                content_start += 1
            break

    page_title = title_override or hero_title

    # Build content HTML
    section_num = 0
    content_html = []

    for block in blocks[content_start:]:
        btype = block[0]

        if btype == 'heading':
            level, text = block[1], block[2]
            if level == 2:
                section_num += 1
                display_text = re.sub(r'^[一二三四五六七八九十\d]+[、.．]\s*', '', text)
                content_html.append(f'''
  <div class="section-divider reveal">
    <span class="num">{section_num:02d}</span>
    <span class="label">{inline_md(display_text)}</span>
    <span class="line"></span>
  </div>''')
            elif level == 3:
                content_html.append(f'  <h3 class="reveal">{inline_md(text)}</h3>')
            elif level == 4:
                content_html.append(f'  <h4 class="reveal">{inline_md(text)}</h4>')
            else:
                tag = f'h{min(level, 6)}'
                content_html.append(f'  <{tag} class="reveal">{inline_md(text)}</{tag}>')

        elif btype == 'paragraph':
            text = inline_md(block[1])
            content_html.append(f'  <p class="reveal">{text}</p>')

        elif btype == 'blockquote':
            text = block[1]
            if text.strip().startswith('💡'):
                cls = 'callout insight reveal'
                text = text.replace('💡', '', 1).strip()
            elif text.strip().startswith('⚠️'):
                cls = 'callout warn reveal'
                text = text.replace('⚠️', '', 1).strip()
            else:
                cls = 'callout reveal'
            content_html.append(f'  <div class="{cls}">{inline_md(text)}</div>')

        elif btype == 'ul':
            items_html = '\n'.join(f'    <li>{inline_md(item)}</li>' for item in block[1])
            content_html.append(f'  <ul class="reveal">\n{items_html}\n  </ul>')

        elif btype == 'ol':
            items_html = '\n'.join(f'    <li>{inline_md(item)}</li>' for item in block[1])
            content_html.append(f'  <ol class="reveal">\n{items_html}\n  </ol>')

        elif btype == 'tree':
            content_html.append(_tree_to_html(block[1]))

        elif btype == 'code':
            lang, code = block[1], escape(block[2])
            content_html.append(f'''  <div class="code-block reveal">
    <pre><code>{code}</code></pre>
  </div>''')

        elif btype == 'image':
            alt_text, src = block[1], block[2]
            if src == 'placeholder' or src.startswith('placeholder'):
                content_html.append(f'''  <div class="img-placeholder reveal">
    <div class="icon">🖼️</div>
    {escape(alt_text) if alt_text else "图片占位符"}
  </div>''')
            else:
                content_html.append(f'''  <div class="img-slot reveal">
    <img src="{escape(src)}" alt="{escape(alt_text)}" loading="lazy">
    {f'<div class="caption">{escape(alt_text)}</div>' if alt_text else ''}
  </div>''')

        elif btype == 'table':
            header_line, rows = block[1], block[2]
            content_html.append(_render_table(header_line, rows))

        elif btype == 'directive_html':
            content_html.append(block[1])

    body_content = '\n\n'.join(content_html)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(page_title)}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');

  :root {{
    --bg: #0a0a0f;
    --bg-card: #12121a;
    --bg-code: #1a1a2e;
    --text: #e4e4e7;
    --text-dim: #8b8b9e;
    --heading: #ffffff;
    --accent: #6366f1;
    --accent-glow: rgba(99, 102, 241, 0.15);
    --accent2: #22d3ee;
    --accent3: #f472b6;
    --warn-color: #f59e0b;
    --border: rgba(255,255,255,0.06);
    --max-w: 900px;
    --callout-bg: rgba(99, 102, 241, 0.08);
    --insight-bg: rgba(34,211,238,0.06);
    --warn-bg: rgba(245,158,11,0.06);
    --hero-gradient: linear-gradient(135deg, #fff 0%, #6366f1 50%, #22d3ee 100%);
    --hero-bg-effect: radial-gradient(ellipse at 30% 50%, rgba(99,102,241,0.08) 0%, transparent 60%),
                      radial-gradient(ellipse at 70% 50%, rgba(34,211,238,0.05) 0%, transparent 60%);
    --code-text: #e4e4e7;
    --scroll-hint-color: #8b8b9e;
    --placeholder-border: rgba(255,255,255,0.1);
    --good-border: rgba(34,211,238,0.3);
    --bad-border: rgba(244,114,182,0.3);
    --negative-bg: rgba(244,114,182,0.1);
    --negative-border: rgba(244,114,182,0.3);
    --positive-bg: rgba(34,211,238,0.1);
    --positive-border: rgba(34,211,238,0.3);
    --card-hover: rgba(99,102,241,0.2);
    --quote-text: #fff;
  }}

  [data-theme="light"] {{
    --bg: #ffffff;
    --bg-card: #f8f9fa;
    --bg-code: #f1f3f5;
    --text: #2d3748;
    --text-dim: #718096;
    --heading: #1a202c;
    --accent: #4f46e5;
    --accent-glow: rgba(79, 70, 229, 0.08);
    --accent2: #0891b2;
    --accent3: #db2777;
    --warn-color: #d97706;
    --border: rgba(0,0,0,0.08);
    --callout-bg: rgba(79, 70, 229, 0.05);
    --insight-bg: rgba(8,145,178,0.05);
    --warn-bg: rgba(217,119,6,0.05);
    --hero-gradient: linear-gradient(135deg, #1a202c 0%, #4f46e5 50%, #0891b2 100%);
    --hero-bg-effect: radial-gradient(ellipse at 30% 50%, rgba(79,70,229,0.04) 0%, transparent 60%),
                      radial-gradient(ellipse at 70% 50%, rgba(8,145,178,0.03) 0%, transparent 60%);
    --code-text: #2d3748;
    --scroll-hint-color: #a0aec0;
    --placeholder-border: rgba(0,0,0,0.12);
    --good-border: rgba(8,145,178,0.4);
    --bad-border: rgba(219,39,119,0.3);
    --negative-bg: rgba(219,39,119,0.06);
    --negative-border: rgba(219,39,119,0.25);
    --positive-bg: rgba(8,145,178,0.06);
    --positive-border: rgba(8,145,178,0.25);
    --card-hover: rgba(79,70,229,0.15);
    --quote-text: #1a202c;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}

  body {{
    font-family: 'Noto Sans SC', 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
  }}

  /* Hero */
  .hero {{
    min-height: 100vh;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    text-align: center; padding: 2rem;
    position: relative; overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: var(--hero-bg-effect);
    animation: drift 20s ease-in-out infinite;
  }}
  @keyframes drift {{
    0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
    50% {{ transform: translate(-2%, 1%) rotate(1deg); }}
  }}
  .hero-content {{ position: relative; z-index: 1; }}
  .hero h1 {{
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 900; letter-spacing: -0.03em; line-height: 1.15;
    margin-bottom: 1.5rem;
    background: var(--hero-gradient);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }}
  .hero .subtitle {{
    font-size: 1.25rem; color: var(--text-dim);
    font-weight: 300; max-width: 600px; margin: 0 auto;
  }}
  .hero .scroll-hint {{
    position: absolute; bottom: 3rem; left: 50%;
    transform: translateX(-50%); color: var(--scroll-hint-color);
    font-size: 0.85rem; opacity: 0.5;
    animation: bounce 2s ease-in-out infinite;
  }}
  @keyframes bounce {{
    0%, 100% {{ transform: translateX(-50%) translateY(0); }}
    50% {{ transform: translateX(-50%) translateY(8px); }}
  }}

  /* Content */
  .content {{ max-width: var(--max-w); margin: 0 auto; padding: 0 2rem 6rem; }}

  /* Section Divider */
  .section-divider {{ display: flex; align-items: center; gap: 1.5rem; margin: 5rem 0 3rem; padding-top: 2rem; }}
  .section-divider .num {{
    font-size: 4rem; font-weight: 900;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1; flex-shrink: 0;
  }}
  .section-divider .label {{ font-size: 1.75rem; font-weight: 700; line-height: 1.3; color: var(--heading); }}
  .section-divider .line {{ flex: 1; height: 1px; background: linear-gradient(90deg, var(--border), transparent); }}

  /* Headings */
  h3 {{ font-size: 1.35rem; font-weight: 700; margin: 3rem 0 1rem; color: var(--heading); }}
  h4 {{ font-size: 1.1rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--accent2); }}
  p {{ margin-bottom: 1rem; }}
  strong {{ color: var(--heading); }}
  a {{ color: var(--accent); }}

  /* Callouts */
  .callout {{
    border-left: 3px solid var(--accent); background: var(--callout-bg);
    padding: 1.25rem 1.5rem; border-radius: 0 12px 12px 0; margin: 1.5rem 0; font-size: 0.95rem;
  }}
  .callout.insight {{ border-left-color: var(--accent2); background: var(--insight-bg); }}
  .callout.warn {{ border-left-color: var(--warn-color); background: var(--warn-bg); }}

  /* Lists */
  ul, ol {{ padding-left: 1.5rem; margin-bottom: 1rem; }}
  li {{ margin-bottom: 0.5rem; }}
  li::marker {{ color: var(--accent); }}

  /* Code */
  .code-block {{
    background: var(--bg-code); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.5rem; margin: 1rem 0; overflow-x: auto;
  }}
  .code-block pre {{ margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.6; color: var(--code-text); }}
  .code-block code {{ font-family: inherit; }}

  /* File Tree */
  .file-tree {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 1.5rem 1.5rem 1.5rem 0.5rem;
    margin: 1.5rem 0; font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem; line-height: 1.4; overflow-x: auto;
  }}
  .file-tree ul {{ list-style: none; padding-left: 0; margin: 0; }}
  .file-tree ul ul {{ padding-left: 1.25rem; border-left: 1px solid var(--border); margin-left: 0.6rem; }}
  .file-tree li {{ margin: 0; padding: 0.25rem 0; }}
  .file-tree li::marker {{ display: none; }}
  .file-tree .tree-item {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.2rem 0.6rem; border-radius: 6px; transition: background 0.15s; cursor: default;
  }}
  .file-tree .tree-item:hover {{ background: var(--accent-glow); }}
  .file-tree .tree-icon {{ font-size: 1rem; flex-shrink: 0; width: 1.2rem; text-align: center; }}
  .file-tree .tree-name {{ color: var(--text); font-weight: 500; }}
  .file-tree .tree-name.dir {{ color: var(--accent2); font-weight: 600; }}
  .file-tree .tree-desc {{
    color: var(--text-dim); font-family: 'Noto Sans SC', 'Inter', sans-serif;
    font-size: 0.8rem; font-weight: 400; margin-left: 0.25rem;
  }}

  /* Images */
  .img-slot {{ margin: 2rem 0; border-radius: 16px; overflow: hidden; border: 1px solid var(--border); }}
  .img-slot img {{ width: 100%; display: block; }}
  .img-slot .caption {{
    padding: 0.75rem 1rem; font-size: 0.85rem; color: var(--text-dim);
    background: var(--bg-card); text-align: center;
  }}
  .img-placeholder {{
    background: var(--bg-card); border: 2px dashed var(--placeholder-border);
    border-radius: 16px; padding: 3rem 2rem; text-align: center;
    color: var(--text-dim); font-size: 0.9rem; margin: 2rem 0;
  }}
  .img-placeholder .icon {{ font-size: 2.5rem; margin-bottom: 0.75rem; opacity: 0.5; }}

  /* Cards */
  .card {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 2rem; margin: 1.5rem 0; transition: border-color 0.3s;
  }}
  .card:hover {{ border-color: var(--card-hover); }}
  .card-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem; margin: 1.5rem 0;
  }}
  .card-grid .card {{ margin: 0; }}
  .card .card-icon {{ font-size: 2rem; margin-bottom: 0.75rem; }}
  .card .card-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--heading); }}
  .card .card-desc {{ font-size: 0.9rem; color: var(--text-dim); line-height: 1.6; }}

  /* Command List */
  .cmd-list {{
    background: var(--bg-code); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
    font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; overflow-x: auto;
  }}
  .cmd-list .cmd {{ display: flex; gap: 1rem; padding: 0.4rem 0; align-items: baseline; }}
  .cmd .key {{ color: var(--accent); font-weight: 500; white-space: nowrap; min-width: 120px; }}
  .cmd .val {{ color: var(--text-dim); }}

  /* Compare */
  .compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0; }}
  .compare .side {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.5rem;
  }}
  .compare .side.good {{ border-color: var(--good-border); }}
  .compare .side.bad {{ border-color: var(--bad-border); }}
  .compare .side-label {{
    font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 0.75rem;
  }}
  .compare .side.good .side-label {{ color: var(--accent2); }}
  .compare .side.bad .side-label {{ color: var(--accent3); }}

  /* Flow */
  .flow {{
    display: flex; align-items: center; justify-content: center;
    flex-wrap: wrap; gap: 0.5rem; margin: 1.5rem 0; font-size: 0.95rem;
  }}
  .flow .step {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 8px; padding: 0.5rem 1rem; white-space: nowrap;
  }}
  .flow .arrow {{ color: var(--accent); font-size: 1.2rem; }}
  .flow .step.highlight {{ border-color: var(--accent); background: var(--accent-glow); }}
  .flow .step.dead {{ opacity: 0.3; text-decoration: line-through; }}

  /* Quote Block */
  .quote-block {{ text-align: center; padding: 4rem 2rem; margin: 4rem 0; position: relative; }}
  .quote-block::before {{
    content: '\\201C'; font-size: 8rem; color: var(--accent); opacity: 0.15;
    position: absolute; top: 0; left: 50%; transform: translateX(-50%);
    line-height: 1; font-family: Georgia, serif;
  }}
  .quote-block .quote-text {{
    font-size: 1.5rem; font-weight: 500; line-height: 1.6;
    color: var(--quote-text); max-width: 700px; margin: 0 auto; position: relative;
  }}

  /* Layers */
  .layers {{ display: flex; flex-direction: column; gap: 0.5rem; margin: 1.5rem 0; }}
  .layer {{
    display: flex; align-items: center; gap: 1rem;
    padding: 1rem 1.5rem; border-radius: 12px; border: 1px solid var(--border);
    transition: transform 0.2s;
  }}
  .layer:hover {{ transform: translateX(4px); }}
  .layer .layer-tag {{
    font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; padding: 0.25rem 0.75rem; border-radius: 6px;
    white-space: nowrap; min-width: 60px; text-align: center;
  }}
  .layer:nth-child(1) {{ background: var(--accent-glow); }}
  .layer:nth-child(1) .layer-tag {{ background: rgba(99,102,241,0.2); color: var(--accent); }}
  .layer:nth-child(2) {{ background: var(--insight-bg); }}
  .layer:nth-child(2) .layer-tag {{ background: rgba(34,211,238,0.2); color: var(--accent2); }}
  .layer:nth-child(3) {{ background: var(--negative-bg); }}
  .layer:nth-child(3) .layer-tag {{ background: rgba(244,114,182,0.2); color: var(--accent3); }}
  .layer:nth-child(4) {{ background: var(--warn-bg); }}
  .layer:nth-child(4) .layer-tag {{ background: rgba(245,158,11,0.2); color: #f59e0b; }}

  /* Cycle */
  .cycle {{
    display: flex; align-items: center; justify-content: center;
    gap: 0.75rem; margin: 1.5rem 0; flex-wrap: wrap;
  }}
  .cycle .node {{
    padding: 0.6rem 1.2rem; border-radius: 999px; font-size: 0.9rem; font-weight: 500;
  }}
  .cycle .node.negative {{
    background: var(--negative-bg); border: 1px solid var(--negative-border); color: var(--accent3);
  }}
  .cycle .node.positive {{
    background: var(--positive-bg); border: 1px solid var(--positive-border); color: var(--accent2);
  }}
  .cycle .arrow {{ color: var(--text-dim); font-size: 1.1rem; }}

  /* Styled Table */
  .styled-table {{
    width: 100%; border-collapse: separate; border-spacing: 0;
    margin: 1.5rem 0; border-radius: 12px; overflow: hidden;
    border: 1px solid var(--border); font-size: 0.9rem;
  }}
  .styled-table thead {{ background: var(--bg-code); }}
  .styled-table th {{
    padding: 0.75rem 1rem; text-align: left; font-weight: 600;
    color: var(--heading); border-bottom: 1px solid var(--border);
  }}
  .styled-table td {{
    padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); color: var(--text);
  }}
  .styled-table tbody tr:last-child td {{ border-bottom: none; }}
  .styled-table tbody tr {{ background: var(--bg-card); transition: background 0.2s; }}
  .styled-table tbody tr:hover {{ background: var(--accent-glow); }}

  /* Theme Toggle */
  .theme-toggle {{
    position: fixed; top: 1.5rem; right: 1.5rem; z-index: 999;
    width: 48px; height: 48px; border-radius: 50%;
    border: 1px solid var(--border); background: var(--bg-card);
    color: var(--text); font-size: 1.3rem; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.3s ease; backdrop-filter: blur(10px);
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  }}
  .theme-toggle:hover {{ transform: scale(1.1); border-color: var(--accent); }}

  /* Footer */
  .footer {{
    text-align: center; padding: 4rem 2rem; color: var(--text-dim);
    font-size: 0.85rem; border-top: 1px solid var(--border);
    max-width: var(--max-w); margin: 0 auto;
  }}

  /* Scroll Animations */
  .reveal {{ opacity: 0; transform: translateY(30px); transition: opacity 0.6s ease, transform 0.6s ease; }}
  .reveal.visible {{ opacity: 1; transform: translateY(0); }}

  /* Responsive */
  @media (max-width: 640px) {{
    .content {{ padding: 0 1.25rem 4rem; }}
    .section-divider .num {{ font-size: 2.5rem; }}
    .section-divider .label {{ font-size: 1.3rem; }}
    .compare {{ grid-template-columns: 1fr; }}
    .card-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<button class="theme-toggle" onclick="toggleTheme()">🌙</button>

<section class="hero">
  <div class="hero-content">
    <h1>{inline_md(hero_title)}</h1>
    {f'<p class="subtitle">{inline_md(hero_subtitle)}</p>' if hero_subtitle else ''}
  </div>
  <div class="scroll-hint">↓ 向下滚动</div>
</section>

<div class="content">
{body_content}
</div>

<footer class="footer">
  {escape(footer_text)}
</footer>

<script>
  // Scroll reveal
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(e => {{
      if (e.isIntersecting) e.target.classList.add('visible');
    }});
  }}, {{ threshold: 0.1 }});
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // Theme toggle
  function toggleTheme() {{
    const html = document.documentElement;
    const btn = document.querySelector('.theme-toggle');
    if (html.getAttribute('data-theme') === 'light') {{
      html.removeAttribute('data-theme');
      btn.textContent = '🌙';
      localStorage.setItem('theme', 'dark');
    }} else {{
      html.setAttribute('data-theme', 'light');
      btn.textContent = '☀️';
      localStorage.setItem('theme', 'light');
    }}
  }}
  (function() {{
    const saved = localStorage.getItem('theme');
    if (saved === 'light') {{
      document.documentElement.setAttribute('data-theme', 'light');
      document.querySelector('.theme-toggle').textContent = '☀️';
    }}
  }})();
</script>

</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to a scrollable HTML page')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output HTML file')
    parser.add_argument('--embed-images', action='store_true', help='Embed local images as base64 data URIs (compressed via Pillow if available)')
    parser.add_argument('--title', default=None, help='Override HTML page title (default: extracted from first H1)')
    parser.add_argument('--footer', default='Generated by md-to-page', help='Footer text (default: "Generated by md-to-page")')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    md_text = input_path.read_text(encoding='utf-8')

    if args.embed_images:
        md_text = embed_images_in_md(md_text, input_path.parent)

    blocks = parse_markdown(md_text)
    html_output = render_html(blocks, title_override=args.title, footer_text=args.footer)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_output, encoding='utf-8')
    print(f"✅ Generated: {output_path}")


if __name__ == '__main__':
    main()
