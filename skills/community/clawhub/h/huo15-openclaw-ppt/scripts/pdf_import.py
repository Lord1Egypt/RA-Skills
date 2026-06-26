#!/usr/bin/env python3
"""
pdf_import.py — v4.4 PDF → JSON deck

PDF 抽文字 → Claude 转 deck。
两个 backend auto fallback：pypdf（标准）→ PyMuPDF（更准确，已在 v7.8.5 装过）。

用法：
    python3 scripts/pdf_import.py /tmp/whitepaper.pdf --output /tmp/d.json
    python3 scripts/pdf_import.py r.pdf --output /tmp/d.json --build /tmp/d.pptx
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def extract_pdf_text(pdf_path: Path, max_chars: int = 30000) -> str:
    """优先 PyMuPDF（更准），fallback pypdf"""
    text = None
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        parts = []
        for page in doc:
            t = page.get_text('text').strip()
            if t:
                parts.append(t)
        doc.close()
        text = '\n\n'.join(parts)
    except ImportError:
        pass

    if not text:
        try:
            import pypdf
            r = pypdf.PdfReader(str(pdf_path))
            text = '\n\n'.join((p.extract_text() or '').strip() for p in r.pages)
        except ImportError:
            raise RuntimeError("装一个：pip install pymupdf（推荐）或 pip install pypdf")

    # 清理：合并多余空格 + 去掉孤立换行
    text = re.sub(r'(?<=[^\n])\n(?=[^\n])', ' ', text)
    text = re.sub(r' {3,}', '  ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    if len(text) > max_chars:
        text = text[:max_chars] + f'\n\n...（已截断，原 {len(text)} 字符）'
    return text


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.4 pdf → deck')
    parser.add_argument('pdf', help='输入 .pdf 路径')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--pack', help='强制 pack')
    parser.add_argument('--slides', type=int)
    parser.add_argument('--build', help='顺便出 PPTX')
    parser.add_argument('--print-extracted', action='store_true')
    args = parser.parse_args()

    print(f"  📄 提取 {args.pdf}...", file=sys.stderr)
    text = extract_pdf_text(Path(args.pdf))
    print(f"  ✂️  抽取 {len(text)} 字符", file=sys.stderr)

    if args.print_extracted:
        print(text)
        return

    from prompt_to_deck import call_claude, is_llm_enabled
    enabled, reason = is_llm_enabled()
    if not enabled:
        print(f"  ✗ LLM 未启用：{reason}", file=sys.stderr)
        print(f"  💡 用 --print-extracted 验证抽取流程", file=sys.stderr)
        sys.exit(1)

    full_prompt = (
        f"基于以下 PDF 内容做一份 PPT。\n\n=== PDF 内容 ===\n\n{text}"
    )
    print(f"  🤖 Claude 转 deck...", file=sys.stderr)
    deck = call_claude(full_prompt, pack_override=args.pack, slides=args.slides)

    print(f"  ✅ {len(deck.get('slides', []))} slides, pack={deck.get('pack')}",
          file=sys.stderr)
    Path(args.output).write_text(json.dumps(deck, ensure_ascii=False, indent=2))
    print(f"  📄 {args.output}", file=sys.stderr)

    if args.build:
        import subprocess
        scripts = Path(__file__).parent
        script = (scripts / 'create_pptx_combined.py'
                  if (scripts / 'create_pptx_combined.py').exists()
                  else scripts / 'create-pptx.py')
        subprocess.run([sys.executable, str(script),
                       '--spec', args.output,
                       '--pack', deck.get('pack', 'apple-light'),
                       '--output', args.build], check=True)
        print(f"  🎯 PPTX: {args.build}", file=sys.stderr)


if __name__ == '__main__':
    main()
