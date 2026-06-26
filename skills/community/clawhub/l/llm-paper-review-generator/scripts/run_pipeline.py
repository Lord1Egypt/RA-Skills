from __future__ import annotations

import argparse
import json
import locale
import re
import subprocess
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def collect_pdfs(pdfs: list[str], dir_paths: list[str]) -> list[Path]:
    items: list[Path] = []
    for d in dir_paths:
        if d.strip():
            items.extend(sorted(Path(d).rglob('*.pdf')))
    items.extend(Path(p) for p in pdfs)

    out: list[Path] = []
    seen: set[str] = set()
    for p in items:
        k = str(p.resolve()).lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
    return out


def redact(text: str) -> str:
    if not text:
        return ''
    out = text
    out = re.sub(r'(?i)(authorization\s*:\s*bearer\s+)[^\s"\']+', r'\1***', out)
    out = re.sub(r'(?i)(api[_-]?key\s*[=:]\s*)[^\s,;"\']+', r'\1***', out)
    out = re.sub(r'(?i)(token\s*[=:]\s*)[^\s,;"\']+', r'\1***', out)
    return out


def run_capture(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True)
    enc = locale.getpreferredencoding(False) or 'utf-8'
    out = (p.stdout or b'').decode(enc, errors='replace')
    err = (p.stderr or b'').decode(enc, errors='replace')
    if p.returncode != 0:
        raise RuntimeError(f"命令失败: {' '.join(cmd)}\n{redact(err)}")
    return out


def run_with_stdin(cmd: list[str], stdin_text: str) -> str:
    enc = locale.getpreferredencoding(False) or 'utf-8'
    p = subprocess.run(cmd, input=stdin_text.encode(enc, errors='replace'), capture_output=True)
    out = (p.stdout or b'').decode(enc, errors='replace')
    err = (p.stderr or b'').decode(enc, errors='replace')
    if p.returncode != 0:
        raise RuntimeError(f"命令失败: {' '.join(cmd)}\n{redact(err)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.json')
    ap.add_argument('--prompt', default='prompt.md')
    ap.add_argument('--pdf', action='append', default=[], help='用户指定的待总结 pdf 文件路径，可重复')
    ap.add_argument('--dir', action='append', default=[], help='用户指定的待总结 pdf 目录，可重复（支持多个文件夹）')
    ap.add_argument('--output-dir', default='', help='用户指定的总结文档输出路径；不传则默认保存到每个输入 PDF 所在目录')
    ap.add_argument('--topic', default='（请填写）')
    ap.add_argument('--direction', default='（请填写）')
    args = ap.parse_args()

    config = read_json(Path(args.config))

    pdfs = collect_pdfs(args.pdf, args.dir)
    if not pdfs:
        raise SystemExit('未找到 PDF，请通过 --pdf 或 --dir 传入')

    py = 'python'
    use_ocr = bool(config.get('use_paddleocr', False))

    pdf_args: list[str] = []
    for p in pdfs:
        pdf_args += ['--pdf', str(p)]

    if use_ocr:
        extracted_jsonl = run_capture([py, 'scripts/extract_paddleocr.py', '--config', args.config, *pdf_args])
    else:
        extracted_jsonl = run_capture([py, 'scripts/extract_pdfplumber.py', *pdf_args])

    out = run_with_stdin([
        py, 'scripts/summarize_reports.py',
        '--config', args.config,
        '--prompt', args.prompt,
        '--topic', args.topic,
        '--direction', args.direction,
        '--pdf-path', '; '.join(str(p) for p in pdfs),
        '--output-dir', str(Path(args.output_dir)) if args.output_dir else '',
        '--input-from-stdin',
    ], extracted_jsonl)

    if out.strip():
        print(out.strip())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
