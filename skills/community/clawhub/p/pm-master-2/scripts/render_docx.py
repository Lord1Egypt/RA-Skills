#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Markdown -> DOCX rendering
-------------------------------------------------
Dual-track output: Markdown is the single source of truth, and this script renders
it into a formal Word document.
Prefer pandoc; if unavailable, fall back to python-docx for basic rendering
(supports #~###### headings, paragraphs, ordered/unordered lists, tables, bold **x**).

Usage:
  python3 render_docx.py <input.md> [--out output.docx]
"""
import os
import sys
import argparse
import subprocess
import shutil
import re


def _add_code(doc, body, size=9):
    """Write plain text as a code block in a monospace font (fallback for mermaid source)."""
    from docx.shared import Pt
    p = doc.add_paragraph()
    run = p.add_run(body)
    run.font.name = 'Courier New'
    run.font.size = Pt(size)


def _try_mermaid_png(src):
    """If the mermaid CLI (mmdc) is installed, render the mermaid source to a PNG and return its path;
    otherwise return None (the caller falls back to a code block). Failures do not raise."""
    mmdc = shutil.which('mmdc')
    if not mmdc:
        return None
    try:
        import tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.mmd', delete=False,
                                         encoding='utf-8') as f:
            f.write(src)
            mmd = f.name
        png = mmd[:-4] + '.png'
        subprocess.run([mmdc, '-i', mmd, '-o', png, '-b', 'white'],
                       check=True, capture_output=True, timeout=60)
        if os.path.exists(png):
            return png
    except Exception:
        return None
    return None


def try_pandoc(md_path, out_path):
    try:
        subprocess.run(['pandoc', md_path, '-o', out_path],
                       check=True, capture_output=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def render_with_python_docx(md_path, out_path):
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # Fenced code block (``` ... ```): prefer rendering mermaid as an image; otherwise output as a
        # code block to avoid garbled text
        stripped = line.lstrip()
        if stripped.startswith('```'):
            lang = stripped.strip('`').strip().lower()
            fence_body = []
            i += 1
            while i < n and not lines[i].lstrip().startswith('```'):
                fence_body.append(lines[i])
                i += 1
            if i < n:
                i += 1  # skip the closing fence
            body = '\n'.join(fence_body)
            if lang == 'mermaid':
                img = _try_mermaid_png(body)
                if img:
                    try:
                        doc.add_picture(img)
                    except Exception:
                        img = None
                if not img:
                    doc.add_paragraph('[Mermaid source not rendered to image in this document]',
                                     style='Intense Quote')
                    _add_code(doc, body, 8)
            else:
                _add_code(doc, body, 9)
            continue
        # Heading
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            doc.add_heading(m.group(2).strip(), level=min(level, 6))
            i += 1
            continue
        # Table (consecutive | lines)
        if line.strip().startswith('|'):
            tbl_lines = []
            while i < n and lines[i].strip().startswith('|'):
                tbl_lines.append(lines[i])
                i += 1
            # drop the separator row (---)
            rows = [r for r in tbl_lines if not re.match(r'^\s*\|?[\s:\-\|]+\|?\s*$', r)]
            if rows:
                cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
                table = doc.add_table(rows=1, cols=len(cells))
                table.style = 'Light Grid Accent 1'
                hdr = table.rows[0].cells
                for j, c in enumerate(cells):
                    hdr[j].text = _strip_inline(c)
                for r in rows[1:]:
                    rc = [c.strip() for c in r.strip().strip('|').split('|')]
                    cells_row = table.add_row().cells
                    for j, c in enumerate(rc):
                        if j < len(cells_row):
                            cells_row[j].text = _strip_inline(c)
            continue
        # Unordered list
        if re.match(r'^[-*]\s+', line):
            doc.add_paragraph(_strip_inline(re.sub(r'^[-*]\s+', '', line)), style='List Bullet')
            i += 1
            continue
        # Ordered list
        if re.match(r'^\d+\.\s+', line):
            doc.add_paragraph(_strip_inline(re.sub(r'^\d+\.\s+', '', line)), style='List Number')
            i += 1
            continue
        # Plain paragraph (merge consecutive lines until a blank line)
        para = [line]
        i += 1
        while i < n and lines[i].strip() and not lines[i].lstrip().startswith(('#', '|', '-', '*')) and not re.match(r'^\d+\.\s', lines[i]):
            para.append(lines[i])
            i += 1
        doc.add_paragraph(_strip_inline(' '.join(para)))
    doc.save(out_path)


def _strip_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    return text


def main():
    ap = argparse.ArgumentParser(description="PM Master MD->DOCX renderer")
    ap.add_argument('input')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    out = a.out or (os.path.splitext(a.input)[0] + '.docx')
    if try_pandoc(a.input, out):
        print(f"[docx] rendered with pandoc -> {out}")
    else:
        try:
            render_with_python_docx(a.input, out)
            print(f"[docx] rendered with python-docx -> {out}")
        except ImportError:
            print("[docx] python-docx is required: pip install python-docx", file=sys.stderr)
            sys.exit(2)
    print(f"[docx] done: {out}")


if __name__ == '__main__':
    main()
