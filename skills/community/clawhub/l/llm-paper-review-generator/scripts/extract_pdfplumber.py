from __future__ import annotations

import argparse
import json
from pathlib import Path

import pdfplumber


def extract_text(pdf_path: Path) -> str:
    parts: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ''
            if txt.strip():
                parts.append(txt.strip())
    merged = '\n\n'.join(parts).strip()
    if not merged:
        raise ValueError(f'无可提取文本: {pdf_path.name}')
    return merged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', action='append', default=[])
    args = ap.parse_args()

    pdfs = [Path(p) for p in args.pdf]
    if not pdfs:
        raise SystemExit('缺少 --pdf')

    for pdf in pdfs:
        text = extract_text(pdf)
        print(json.dumps({'pdf_path': str(pdf), 'text': text}, ensure_ascii=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
