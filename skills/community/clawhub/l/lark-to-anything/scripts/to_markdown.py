#!/usr/bin/env python3
"""
Convert lark-cli docs +fetch JSON output to a Markdown file (+ local assets).

Usage:
  python3 to_markdown.py <json-file> [--output-dir <dir>]

Output:
  <output-dir>/<title>/
      index.md        — converted document
      assets/         — downloaded images and whiteboard thumbnails

If --output-dir is omitted, the folder is created in the current directory.
Images and whiteboards are downloaded automatically; failures are skipped
gracefully (original URL / placeholder kept).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed


def slugify(text: str) -> str:
    text = text.strip()
    text = re.sub(r'[\\/:*?"<>|]', '_', text)
    text = re.sub(r'\s+', '_', text)
    return text or "document"


# ── Feishu element converters ────────────────────────────────────────────────

def replace_callout(m: re.Match) -> str:
    inner = m.group(1).strip()
    return '\n'.join('> ' + l if l.strip() else '>' for l in inner.split('\n'))


def html_table_to_md(match: re.Match) -> str:
    html = match.group(0)
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
    if not rows:
        return html
    md_rows: list[str] = []
    for i, row in enumerate(rows):
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
        cleaned: list[str] = []
        for cell in cells:
            cell = re.sub(r'<b>(.*?)</b>', r'**\1**', cell, flags=re.DOTALL)
            cell = re.sub(r'<br\s*/?>', ' ', cell)
            cell = re.sub(r'<[^>]+>', '', cell)
            cell = cell.strip().replace('\n', ' ').replace('|', '\\|')
            cleaned.append(cell)
        if not cleaned:
            continue
        md_rows.append('| ' + ' | '.join(cleaned) + ' |')
        if i == 0:
            md_rows.append('|' + ' --- |' * len(cleaned))
    return '\n' + '\n'.join(md_rows) + '\n'


def replace_figure(m: re.Match) -> str:
    name = re.search(r'name="([^"]*)"', m.group(0))
    token = re.search(r'token="([^"]*)"', m.group(0))
    if name:
        return f'\n> *[附件: {name.group(1)}]*\n'
    if token:
        return f'\n> *[附件，token: {token.group(1)}]*\n'
    return ''


def img_tag_to_md(m: re.Match) -> str:
    """Convert <img href="url" alt="..."/> to ![alt](url)."""
    tag = m.group(0)
    url = re.search(r'href="(https?://[^"]+)"', tag)
    alt = re.search(r'alt="([^"]*)"', tag)
    if url:
        alt_text = alt.group(1) if alt else ''
        return f'![{alt_text}]({url.group(1)})'
    return ''


def convert_xml(content: str) -> str:
    """First pass: convert Feishu XML/HTML elements to Markdown."""
    content = re.sub(r'<title>(.*?)</title>', r'# \1\n', content)
    content = re.sub(r'<cite type="user"[^>]*user-name="([^"]*)"[^>]*/>', r'@\1', content)
    content = re.sub(r'<cite[^>]*title="([^"]*)"[^>]*/>', r'[\1]', content)
    content = re.sub(r'<cite[^>]*/>', '', content)
    content = re.sub(r'<callout[^>]*>(.*?)</callout>', replace_callout, content, flags=re.DOTALL)
    content = re.sub(r'<checkbox done="false">(.*?)</checkbox>', r'- [ ] \1', content)
    content = re.sub(r'<checkbox done="true">(.*?)</checkbox>', r'- [x] \1', content)
    content = re.sub(r'<figure[^>]*>.*?</figure>', replace_figure, content, flags=re.DOTALL)
    content = re.sub(r'<readonly-block[^/]*/>', '', content)
    # <img> must run before <table> — images are often nested inside table cells
    content = re.sub(r'<img\b[^>]*/>', img_tag_to_md, content)
    content = re.sub(r'<table>.*?</table>', html_table_to_md, content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    return content.strip() + '\n'


# ── Asset downloading ────────────────────────────────────────────────────────

def _ext_from_content_type(ct: str) -> str:
    mapping = {'image/jpeg': '.jpg', 'image/png': '.png',
               'image/gif': '.gif', 'image/webp': '.webp',
               'image/svg+xml': '.svg'}
    for k, v in mapping.items():
        if k in ct:
            return v
    return '.png'


def download_image(url: str, dest: str) -> str | None:
    """Download a URL to dest (no extension) and return final path, or None."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            ct = resp.headers.get('Content-Type', 'image/png')
            ext = _ext_from_content_type(ct)
            final = dest + ext
            with open(final, 'wb') as f:
                f.write(resp.read())
            return final
    except Exception:
        return None


def download_whiteboard(token: str, dest: str) -> str | None:
    """Download a whiteboard thumbnail via lark-cli and return final path."""
    try:
        result = subprocess.run(
            ['lark-cli', 'docs', '+media-download',
             '--type', 'whiteboard', '--token', token, '--output', dest],
            capture_output=True, text=True, timeout=30
        )
        for ext in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
            if os.path.exists(dest + ext):
                return dest + ext
        parent = os.path.dirname(dest)
        base = os.path.basename(dest)
        for f in os.listdir(parent):
            if f.startswith(base):
                return os.path.join(parent, f)
    except Exception:
        pass
    return None


def localise_assets(markdown: str, raw_xml: str, assets_dir: str) -> tuple[str, dict]:
    """
    Download images and whiteboards, rewrite markdown links to local paths.
    Returns (updated_markdown, stats).
    """
    os.makedirs(assets_dir, exist_ok=True)
    stats = {'images': 0, 'images_failed': 0, 'whiteboards': 0, 'whiteboards_failed': 0}

    # ── Images already rendered as ![alt](feishu-url) ──
    img_pattern = re.compile(r'!\[([^\]]*)\]\((https://[^)]+feishu\.cn[^)]*)\)')
    img_jobs: list[tuple[str, str, str]] = []  # (original_url, dest_base, alt)
    seen_urls: dict[str, str] = {}

    for i, m in enumerate(img_pattern.finditer(markdown)):
        url = m.group(2)
        if url in seen_urls:
            continue
        dest_base = os.path.join(assets_dir, f'image-{i + 1}')
        seen_urls[url] = dest_base
        img_jobs.append((url, dest_base, m.group(1)))

    def _dl_img(job):
        url, dest_base, alt = job
        return url, download_image(url, dest_base)

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(_dl_img, j): j for j in img_jobs}
        for fut in as_completed(futures):
            url, local_path = fut.result()
            if local_path:
                rel = os.path.relpath(local_path, os.path.dirname(assets_dir))
                # rewrite all occurrences of this URL
                markdown = markdown.replace(url, rel)
                stats['images'] += 1
            else:
                stats['images_failed'] += 1

    # ── Whiteboards from raw XML ──
    wb_tokens = re.findall(r'<whiteboard[^>]*token="([^"]*)"', raw_xml)
    for i, token in enumerate(wb_tokens):
        dest_base = os.path.join(assets_dir, f'whiteboard-{i + 1}')
        local_path = download_whiteboard(token, dest_base)
        placeholder = '> *[白板内容，请在飞书中查看]*'
        if local_path:
            rel = os.path.relpath(local_path, os.path.dirname(assets_dir))
            markdown = markdown.replace(
                placeholder, f'![白板缩略图]({rel})', 1
            )
            stats['whiteboards'] += 1
        else:
            stats['whiteboards_failed'] += 1

    return markdown, stats


# ── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Feishu JSON → Markdown + assets")
    parser.add_argument('json_file', help="Path to lark-cli JSON output")
    parser.add_argument('--output-dir', '-o', default=None,
                        help="Directory to create doc folder in (default: cwd)")
    args = parser.parse_args()

    with open(args.json_file, encoding='utf-8') as f:
        raw = f.read()

    lines = raw.split('\n')
    start = next((i for i, l in enumerate(lines) if l.strip().startswith('{')), 0)
    try:
        data = json.loads('\n'.join(lines[start:]))
    except json.JSONDecodeError as e:
        print(f"ERROR: failed to parse JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get('ok'):
        print(f"ERROR: lark-cli returned error — {data}", file=sys.stderr)
        sys.exit(1)

    raw_xml: str = data['data']['document']['content']

    # Step 1: whiteboard placeholder substitution (before XML strip)
    markdown = re.sub(r'<whiteboard[^/]*/>', '\n> *[白板内容，请在飞书中查看]*\n', raw_xml)
    # Step 2: convert all other XML/HTML
    markdown = convert_xml(markdown)

    # Derive output folder
    title_match = re.match(r'# (.+)', markdown)
    title = title_match.group(1).strip() if title_match else "document"
    folder_name = slugify(title)
    base_dir = args.output_dir or os.getcwd()
    doc_dir = os.path.join(base_dir, folder_name)
    assets_dir = os.path.join(doc_dir, 'assets')
    os.makedirs(doc_dir, exist_ok=True)

    # Step 3: download images + whiteboards, rewrite paths
    print("Downloading assets...", flush=True)
    markdown, stats = localise_assets(markdown, raw_xml, assets_dir)

    # Step 4: save
    md_path = os.path.join(doc_dir, 'index.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    # Report
    print(f"Saved: {os.path.abspath(md_path)} ({len(markdown):,} chars)")
    if stats['images'] or stats['images_failed']:
        print(f"  Images: {stats['images']} downloaded"
              + (f", {stats['images_failed']} failed (URL kept)" if stats['images_failed'] else ""))
    if stats['whiteboards'] or stats['whiteboards_failed']:
        print(f"  Whiteboards: {stats['whiteboards']} downloaded"
              + (f", {stats['whiteboards_failed']} failed (placeholder kept)" if stats['whiteboards_failed'] else ""))


if __name__ == '__main__':
    main()
