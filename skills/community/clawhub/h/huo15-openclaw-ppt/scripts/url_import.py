#!/usr/bin/env python3
"""
url_import.py — v3.8 URL 抓内容 → JSON deck（媲美 Gamma URL import）

工作流：
  1. urllib 抓 HTML（带 User-Agent，遵守 robots.txt）
  2. BeautifulSoup-lite 抽核心文本（h1/h2/h3 + p + li）
  3. 截断到 30K tokens 内
  4. 调 prompt_to_deck.call_claude 生成 deck JSON

用法：
    python3 scripts/url_import.py https://example.com/article \\
        --output /tmp/deck.json --slides 8

    # 一条龙：URL → JSON → PPTX
    python3 scripts/url_import.py https://example.com \\
        --output /tmp/d.json --build /tmp/d.pptx --pack apple-light
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def fetch_url(url: str, timeout: int = 15) -> str:
    """拉 HTML 内容"""
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'huo15-ppt/3.8 (https://huo15.com; +mailto:postmaster@huo15.com)',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        # 自动检测 charset
        ctype = resp.headers.get('Content-Type', '')
        m = re.search(r'charset=([^\s;]+)', ctype)
        encoding = m.group(1) if m else 'utf-8'
        try:
            return resp.read().decode(encoding, errors='replace')
        except LookupError:
            return resp.read().decode('utf-8', errors='replace')


def html_to_text(html: str, max_chars: int = 30000) -> str:
    """轻量级 HTML → 文本（保留语义结构）"""
    # 去 script / style
    html = re.sub(r'<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<style\b[^<]*(?:(?!</style>)<[^<]*)*</style>', '', html, flags=re.IGNORECASE)
    # 去 nav / footer / aside（噪音）
    for tag in ('nav', 'footer', 'aside', 'header'):
        html = re.sub(rf'<{tag}\b[^>]*>.*?</{tag}>', '', html, flags=re.IGNORECASE | re.DOTALL)
    # 提取 title
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_m.group(1).strip() if title_m else ''
    # 提取 h1-h3 + p + li 转 markdown 风格
    parts = []
    if title:
        parts.append(f'# {title}')
    # 简单 tag 抽取
    pattern = r'<(h[1-3]|p|li)[^>]*>(.*?)</\1>'
    for m in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
        tag = m.group(1).lower()
        content = m.group(2)
        # 去内嵌标签
        content = re.sub(r'<[^>]+>', '', content)
        # decode HTML entities
        content = re.sub(r'&nbsp;', ' ', content)
        content = re.sub(r'&amp;', '&', content)
        content = re.sub(r'&lt;', '<', content)
        content = re.sub(r'&gt;', '>', content)
        content = re.sub(r'&quot;', '"', content)
        content = re.sub(r'&#39;', "'", content)
        content = re.sub(r'\s+', ' ', content).strip()
        if not content or len(content) < 5:
            continue
        if tag.startswith('h'):
            level = int(tag[1])
            parts.append(f'\n{"#" * level} {content}')
        elif tag == 'li':
            parts.append(f'- {content}')
        else:
            parts.append(content)
    text = '\n'.join(parts)
    # 截断
    if len(text) > max_chars:
        text = text[:max_chars] + f'\n\n...（已截断，原文 {len(text)} 字符）'
    return text


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v3.8 URL → JSON deck')
    parser.add_argument('url', help='待抓取的 URL')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--pack', help='强制 pack')
    parser.add_argument('--slides', type=int, help='强制 slide 数')
    parser.add_argument('--model', default=None)
    parser.add_argument('--build', help='顺便出 PPTX')
    parser.add_argument('--print-extracted', action='store_true',
                        help='只打印抽取的文本（不调 LLM，验证抓取）')
    args = parser.parse_args()

    print(f"  🌐 抓取 {args.url}", file=sys.stderr)
    try:
        html = fetch_url(args.url)
    except Exception as e:
        print(f"  ✗ 抓取失败: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"  📄 HTML {len(html)} 字符", file=sys.stderr)

    text = html_to_text(html)
    print(f"  ✂️  抽取核心文本 {len(text)} 字符", file=sys.stderr)

    if args.print_extracted:
        print(text)
        return

    # 调 prompt_to_deck
    from prompt_to_deck import call_claude, is_llm_enabled, DEFAULT_MODELS
    enabled, reason = is_llm_enabled()
    if not enabled:
        print(f"  ✗ LLM 未启用：{reason}", file=sys.stderr)
        print(f"  💡 用 --print-extracted 验证抓取流程", file=sys.stderr)
        sys.exit(1)

    full_prompt = (
        f"基于以下网页内容做一份 PPT。源 URL: {args.url}\n\n"
        f"=== 网页内容 ===\n\n{text}"
    )
    model = args.model or os.environ.get('ANTHROPIC_MODEL') or DEFAULT_MODELS['balanced']
    print(f"  🤖 调用 Claude {model}...", file=sys.stderr)

    try:
        import json as _json
        deck = call_claude(full_prompt,
                           pack_override=args.pack,
                           slides=args.slides,
                           model=model)
    except Exception as e:
        print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    pack = deck.get('pack', '?')
    n = len(deck.get('slides', []))
    print(f"  ✅ 生成 {n} 张 slide，pack={pack}", file=sys.stderr)

    Path(args.output).write_text(_json.dumps(deck, ensure_ascii=False, indent=2))
    print(f"  📄 {args.output}", file=sys.stderr)

    if args.build:
        import subprocess
        script = Path(__file__).parent / 'create_pptx_combined.py'
        if not script.exists():
            script = Path(__file__).parent / 'create-pptx.py'
        result = subprocess.run([
            sys.executable, str(script),
            '--spec', args.output, '--pack', pack, '--output', args.build,
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ PPTX 生成失败: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        print(f"  🎯 PPTX: {args.build}", file=sys.stderr)


if __name__ == '__main__':
    main()
