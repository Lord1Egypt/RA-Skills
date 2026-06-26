#!/usr/bin/env python3
"""Extract clean text from an academic HTML paper, preserving LaTeX math and table structure.

Usage:
    python extract_html_text.py <html_path> <output_path>

- html_path: path to the downloaded HTML file
- output_path: path to write the extracted plain text

Math formulas are converted to LaTeX ($...$  or $$...$$).
Tables are converted to pipe-delimited rows for readability.
"""

import sys
import os
import re


def extract_text(html):
    # 1. Preserve math: extract <annotation encoding="application/x-tex"> content
    def replace_math(m):
        block = m.group(0)
        ann = re.search(
            r'<annotation[^>]*encoding=["\']application/x-tex["\'][^>]*>(.*?)</annotation>',
            block, re.DOTALL
        )
        if ann:
            latex = ann.group(1).strip()
            if 'display="block"' in block or 'mode="display"' in block:
                return f' $${latex}$$ '
            return f' ${latex}$ '
        # fallback: alttext attribute
        alt = re.search(r'alttext=["\']([^"\']+)["\']', block)
        if alt:
            return f' ${alt.group(1)}$ '
        return ' [MATH] '

    text = re.sub(r'<math[^>]*>.*?</math>', replace_math, html, flags=re.DOTALL | re.IGNORECASE)

    # 2. Preserve table structure
    text = re.sub(r'<tr[^>]*>', '\n| ', text, flags=re.IGNORECASE)
    text = re.sub(r'<t[hd][^>]*>', ' | ', text, flags=re.IGNORECASE)
    text = re.sub(r'</t[hd]>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</tr>', ' |', text, flags=re.IGNORECASE)

    # 3. Remove style / script blocks
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL)

    # 4. Heading tags → line breaks with markers
    text = re.sub(r'<(h[1-6])[^>]*>', r'\n\n[\1] ', text, flags=re.IGNORECASE)
    text = re.sub(r'<(p|li|div|section|figcaption)[^>]*>', '\n', text, flags=re.IGNORECASE)

    # 5. Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # 6. Decode HTML entities
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)

    # 7. Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <html_path> <output_path>", file=sys.stderr)
        sys.exit(1)

    html_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(html_path):
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    text = extract_text(html)

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Text extracted: {len(text)} chars -> {output_path}")


if __name__ == "__main__":
    main()
