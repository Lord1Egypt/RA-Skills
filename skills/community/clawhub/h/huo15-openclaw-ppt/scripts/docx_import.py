#!/usr/bin/env python3
"""
docx_import.py — v4.4 Word .docx → JSON deck（对标 ChatPPT 文档导入）

提取 H1-H3 + 段落 + 列表 + 表格 → Claude API 转 deck。
保留 Word 的章节结构（一级标题 → section_divider，正文 → content_list 等）。

用法：
    python3 scripts/docx_import.py /path/report.docx --output /tmp/d.json
    python3 scripts/docx_import.py r.docx --output /tmp/d.json --build /tmp/d.pptx
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def extract_docx(docx_path: Path, max_chars: int = 30000) -> str:
    """docx → markdown 风格文本"""
    try:
        from docx import Document
    except ImportError:
        raise RuntimeError("pip install python-docx")

    doc = Document(str(docx_path))
    parts = []
    for block in doc.element.body:
        tag = block.tag.split('}')[-1]
        if tag == 'p':
            from docx.oxml.ns import qn
            style_elem = block.find(f'{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}pPr/{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}pStyle')
            style = style_elem.get(qn('w:val')) if style_elem is not None else ''
            text = ''.join(t.text or '' for t in block.iter()
                          if t.tag.endswith('}t')).strip()
            if not text:
                continue
            if 'Heading 1' in style or 'Heading1' in style or style == '1':
                parts.append(f'\n# {text}')
            elif 'Heading 2' in style or 'Heading2' in style or style == '2':
                parts.append(f'\n## {text}')
            elif 'Heading 3' in style or 'Heading3' in style or style == '3':
                parts.append(f'### {text}')
            elif 'List' in style:
                parts.append(f'- {text}')
            else:
                parts.append(text)
        elif tag == 'tbl':
            # 表格
            rows = []
            for row in block.iter():
                if row.tag.endswith('}tr'):
                    cells = [' '.join(t.text or '' for t in row.iter()
                                      if t.tag.endswith('}t')).strip()
                             for row in [row]
                             for r in row.iter() if r.tag.endswith('}tc')]
                    if cells:
                        rows.append(' | '.join(cells))
            if rows:
                parts.append('\n' + '\n'.join(rows))

    text = '\n'.join(parts)
    if len(text) > max_chars:
        text = text[:max_chars] + f'\n\n...（已截断，原 {len(text)} 字符）'
    return text


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.4 docx → deck')
    parser.add_argument('docx', help='输入 .docx 路径')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--pack', help='强制 pack')
    parser.add_argument('--slides', type=int, help='强制 slide 数')
    parser.add_argument('--build', help='顺便出 PPTX')
    parser.add_argument('--print-extracted', action='store_true',
                        help='只打印抽取的文本（不调 LLM）')
    args = parser.parse_args()

    print(f"  📄 读取 {args.docx}...", file=sys.stderr)
    text = extract_docx(Path(args.docx))
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
        f"基于以下 Word 文档内容做一份 PPT。\n\n"
        f"=== 文档内容 ===\n\n{text}"
    )
    print(f"  🤖 Claude 转 deck...", file=sys.stderr)
    try:
        deck = call_claude(full_prompt, pack_override=args.pack,
                           slides=args.slides)
    except Exception as e:
        print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

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
