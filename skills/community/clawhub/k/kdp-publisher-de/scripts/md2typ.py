#!/usr/bin/env python3
"""
md2typ.py — Markdown → Typst für OpenClaw-Buchkapitel
Verwendung: python md2typ.py <input.md> [output.typ]
            python md2typ.py <input.md>        # stdout
"""
import re
import sys
import os


# ── Inline-Konverter ──────────────────────────────────────────────────────────

def convert_inline(text):
    """Markdown-Inline-Syntax → Typst. Code-Spans werden nicht angefasst."""
    parts = []
    last = 0
    for m in re.finditer(r'`[^`]+`', text):
        parts.append(('text', text[last:m.start()]))
        parts.append(('code', m.group(0)))
        last = m.end()
    parts.append(('text', text[last:]))

    result = []
    for kind, chunk in parts:
        if kind == 'code':
            result.append(chunk)
        else:
            # Literal # und @ zuerst mit Platzhaltern schützen (bevor wir #strong etc. erzeugen)
            chunk = chunk.replace('#', '\x05')
            chunk = chunk.replace('@', '\x06')
            chunk = chunk.replace('$', '\x07')

            # Platzhalter für Bold/Italic, damit Regex-Reihenfolge keine Rolle spielt
            # Bold+Italic: ***text*** → Platzhalter
            chunk = re.sub(r'\*\*\*(.+?)\*\*\*', lambda m: f'\x01{m.group(1)}\x02', chunk)
            # Bold: **text** → Platzhalter
            chunk = re.sub(r'\*\*(.+?)\*\*', lambda m: f'\x03{m.group(1)}\x04', chunk)
            # Italic: *text* → _text_
            chunk = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'_\1_', chunk)
            # Bold-Platzhalter auflösen — #strong[...] vermeidet Delimiter-Fehler bei /*, -*, etc.
            chunk = re.sub(r'\x01(.+?)\x02', lambda m: f'#strong[_{m.group(1)}_]', chunk)
            chunk = re.sub(r'\x03(.+?)\x04', lambda m: f'#strong[{m.group(1)}]', chunk)
            # Markdown-Links: [text](url) → #link("url")[text]
            chunk = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'#link("\2")[\1]', chunk)
            # Literal-Platzhalter zu Typst-Escapes auflösen
            chunk = chunk.replace('\x05', r'\#')
            chunk = chunk.replace('\x06', r'\@')
            chunk = chunk.replace('\x07', r'\$')
            result.append(chunk)

    return ''.join(result)


# ── Blockquote → Hint-Box ─────────────────────────────────────────────────────

_HINT_PATTERNS = [
    (r'^(?:💡\s*)?\*\*TIPP:\*\*\s*(.*)',     'box-tip'),
    (r'^(?:⚠️\s*)?\*\*WARNUNG:\*\*\s*(.*)',   'box-warning'),
    (r'^(?:✅\s*)?\*\*ERFOLG:\*\*\s*(.*)',    'box-success'),
    (r'^(?:📌\s*)?\*\*HINWEIS:\*\*\s*(.*)',   'box-note'),
    (r'^\*\*TIPP:\*\*\s*(.*)',                 'box-tip'),
    (r'^\*\*WARNUNG:\*\*\s*(.*)',              'box-warning'),
    (r'^\*\*ERFOLG:\*\*\s*(.*)',               'box-success'),
    (r'^\*\*HINWEIS:\*\*\s*(.*)',              'box-note'),
]

def convert_blockquote(lines):
    content_parts = []
    for line in lines:
        stripped = re.sub(r'^>\s?', '', line).strip()
        if stripped:
            content_parts.append(stripped)
    if not content_parts:
        return ''
    full = ' '.join(content_parts)

    for pattern, func in _HINT_PATTERNS:
        m = re.match(pattern, full, re.DOTALL)
        if m:
            inner = convert_inline(m.group(1).strip())
            return f'#{func}[\n{inner}\n]'

    # Einfaches Blockquote → Epigraph
    return f'#epigraph[\n{convert_inline(full)}\n]'


# ── Tabelle ───────────────────────────────────────────────────────────────────

def convert_table(lines):
    rows = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\|[-:| ]+\|$', stripped):
            continue
        cells = [c.strip() for c in stripped.strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return ''

    num_cols = len(rows[0])
    col_spec = ', '.join(['1fr'] * num_cols)
    header_cells = ', '.join(f'[{convert_inline(c)}]' for c in rows[0])

    out = [f'#table(\n  columns: ({col_spec}),\n  table.header({header_cells}),']
    for row in rows[1:]:
        # Pad/trim row to expected column count
        while len(row) < num_cols:
            row.append('')
        row = row[:num_cols]
        cells = ', '.join(f'[{convert_inline(c)}]' for c in row)
        out.append(f'  {cells},')
    out.append(')')
    return '\n'.join(out)


# ── QR-Code ───────────────────────────────────────────────────────────────────

def convert_qr(line):
    m = re.match(r'\[QR-CODE:\s*([A-Z0-9_-]+)\s*[–—-]\s*(.+?)\s*\]', line.strip())
    if m:
        qr_id = m.group(1)
        rest = m.group(2).strip()
        if '|' in rest:
            label, hint = [x.strip() for x in rest.split('|', 1)]
            return f'#qr-block(image("qr-{qr_id}.svg", width: 3cm), "{label}", "", hint: "{hint}")'
        return f'#qr-block(image("qr-{qr_id}.svg", width: 3cm), "{rest}", "")'
    return None


# ── Haupt-Konverter ───────────────────────────────────────────────────────────

def md2typ(md_text):
    lines = md_text.splitlines()
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code-Block
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            fence = f'```{lang}' if lang else '```'
            out.append(f'{fence}\n' + '\n'.join(code_lines) + '\n```')
            i += 1
            continue

        # Tabelle
        if (line.strip().startswith('|')
                and i + 1 < len(lines)
                and re.match(r'^\|[-:| ]+\|', lines[i + 1].strip())):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            out.append(convert_table(table_lines))
            continue

        # Blockquote
        if line.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                quote_lines.append(lines[i])
                i += 1
            out.append(convert_blockquote(quote_lines))
            continue

        # Überschriften
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            title = convert_inline(m.group(2).strip())
            out.append('=' * level + ' ' + title)
            i += 1
            continue

        # Horizontale Linie → überspringen
        if re.match(r'^---+\s*$', line) or re.match(r'^\*\*\*+\s*$', line):
            i += 1
            continue

        # &nbsp;
        if line.strip() == '&nbsp;':
            out.append('')
            i += 1
            continue

        # QR-Code — konsekutive QR-Zeilen als nicht-trennbare Gruppe
        qr = convert_qr(line)
        if qr:
            group = [qr]
            i += 1
            while i < len(lines):
                next_qr = convert_qr(lines[i])
                if next_qr:
                    group.append(next_qr)
                    i += 1
                elif lines[i].strip() == '':
                    i += 1  # Leerzeilen innerhalb der Gruppe überspringen
                else:
                    break
            if len(group) > 1:
                out.append('#block(breakable: false)[\n' + '\n'.join(group) + '\n]')
            else:
                out.append(group[0])
            continue

        # Ungeordnete Liste
        if re.match(r'^[-*]\s+', line):
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i]):
                text = re.sub(r'^[-*]\s+', '', lines[i])
                out.append('- ' + convert_inline(text))
                i += 1
            continue

        # Geordnete Liste
        if re.match(r'^\d+\.\s+', line):
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                text = re.sub(r'^\d+\.\s+', '', lines[i])
                out.append('+ ' + convert_inline(text))
                i += 1
            continue

        # Leerzeile
        if line.strip() == '':
            out.append('')
            i += 1
            continue

        # Normaler Absatz
        out.append(convert_inline(line))
        i += 1

    # Mehrfache Leerzeilen auf eine reduzieren
    result = []
    prev_blank = False
    for line in out:
        if line == '':
            if not prev_blank:
                result.append('')
            prev_blank = True
        else:
            result.append(line)
            prev_blank = False

    body = '\n'.join(result).strip()
    return '#import "kdp-book.typ": *\n\n' + body + '\n'


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_file):
        print(f'[md2typ] Fehler: {input_file} nicht gefunden')
        sys.exit(1)

    md_text = open(input_file, encoding='utf-8').read()
    typ_text = md2typ(md_text)

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        open(output_file, 'w', encoding='utf-8').write(typ_text)
        print(f'[md2typ] ✓ {input_file} → {output_file}')
    else:
        sys.stdout.write(typ_text)


if __name__ == '__main__':
    main()
