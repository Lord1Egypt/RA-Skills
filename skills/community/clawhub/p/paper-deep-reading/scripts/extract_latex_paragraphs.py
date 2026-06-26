#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


SECTION_RE = re.compile(r'\\(section|subsection|subsubsection|paragraph)\*?\{(.+?)\}')
BEGIN_RE = re.compile(r'\\begin\{([A-Za-z*]+)\}')
END_RE = re.compile(r'\\end\{([A-Za-z*]+)\}')
CAPTION_RE = re.compile(r'\\caption(?:\[[^\]]*\])?\{(.+?)\}')
INPUT_RE = re.compile(r'\\(?:input|include)\{(.+?)\}')


BLOCK_KINDS = {
    'equation': 'equation',
    'align': 'equation',
    'align*': 'equation',
    'gather': 'equation',
    'gather*': 'equation',
    'multline': 'equation',
    'multline*': 'equation',
    'theorem': 'theorem',
    'lemma': 'theorem',
    'proposition': 'theorem',
    'corollary': 'theorem',
    'definition': 'definition',
    'remark': 'remark',
    'algorithm': 'algorithm',
    'algorithm*': 'algorithm',
    'figure': 'figure',
    'figure*': 'figure',
    'table': 'table',
    'table*': 'table',
}


def sanitize_text(text: str) -> str:
    text = text.replace('\t', ' ')
    lines = []
    for raw in text.splitlines():
        line = raw.rstrip('\n')
        if not line.strip():
            lines.append('')
            continue
        if line.lstrip().startswith('%'):
            lines.append('')
            continue
        # Strip trailing comments when not escaped.
        parts = re.split(r'(?<!\\)%', line, maxsplit=1)
        lines.append(parts[0].rstrip())
    return '\n'.join(lines)


def stable_id(rel_path: str, index: int) -> str:
    slug = rel_path.replace('\\', '/').replace('/', '-').replace('.', '-')
    return f'P-{slug}-{index:04d}'


def emit_entry(entries: list[dict], rel_path: str, start: int, end: int, text: str, section_path: list[str], kind: str) -> None:
    cleaned = ' '.join(text.split())
    if not cleaned:
        return
    entry = {
        'paragraph_id': stable_id(rel_path, len(entries) + 1),
        'source_path': rel_path,
        'line_start': start,
        'line_end': end,
        'section_path': section_path[:],
        'kind': kind,
        'text': cleaned,
    }
    entries.append(entry)


def extract_blocks(rel_path: str, text: str) -> list[dict]:
    lines = text.splitlines()
    entries: list[dict] = []
    section_stack: list[str] = []
    buffer: list[str] = []
    para_start: int | None = None
    env_name: str | None = None
    env_start: int | None = None
    env_lines: list[str] = []

    def flush_paragraph(current_line: int) -> None:
        nonlocal buffer, para_start
        if buffer and para_start is not None:
            emit_entry(entries, rel_path, para_start, current_line, '\n'.join(buffer), section_stack, 'paragraph')
        buffer = []
        para_start = None

    for idx, line in enumerate(lines, start=1):
        sec_match = SECTION_RE.search(line)
        if sec_match and env_name is None:
            flush_paragraph(idx - 1)
            level, title = sec_match.groups()
            title = title.strip()
            level_order = {'section': 1, 'subsection': 2, 'subsubsection': 3, 'paragraph': 4}[level]
            section_stack[:] = section_stack[: level_order - 1]
            section_stack.append(title)
            continue

        begin_match = BEGIN_RE.search(line)
        end_match = END_RE.search(line)

        if env_name is None and begin_match:
            flush_paragraph(idx - 1)
            env_name = begin_match.group(1)
            env_start = idx
            env_lines = [line]
            continue

        if env_name is not None:
            env_lines.append(line)
            if end_match and end_match.group(1) == env_name:
                raw = '\n'.join(env_lines)
                kind = BLOCK_KINDS.get(env_name, 'environment')
                emit_entry(entries, rel_path, env_start or idx, idx, raw, section_stack, kind)
                if kind in {'figure', 'table'}:
                    for caption_match in CAPTION_RE.finditer(raw):
                        emit_entry(entries, rel_path, env_start or idx, idx, caption_match.group(1), section_stack, f'{kind}_caption')
                env_name = None
                env_start = None
                env_lines = []
            continue

        if not line.strip():
            flush_paragraph(idx - 1)
            continue

        if para_start is None:
            para_start = idx
        buffer.append(line)

    flush_paragraph(len(lines))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract structured LaTeX paragraph anchors.')
    parser.add_argument('input_dir', help='Directory containing .tex files')
    parser.add_argument('output', help='Output JSON path')
    parser.add_argument('--paper-id', default='paper', help='Paper identifier')
    args = parser.parse_args()

    root = Path(args.input_dir).resolve()
    tex_files = sorted(root.rglob('*.tex'))
    if not tex_files:
        raise SystemExit(f'No .tex files found under {root}')

    paragraphs: list[dict] = []
    for tex_file in tex_files:
        rel = tex_file.relative_to(root).as_posix()
        text = sanitize_text(tex_file.read_text(encoding='utf-8', errors='ignore'))
        paragraphs.extend(extract_blocks(rel, text))

    payload = {
        'schema_version': '1.2.0',
        'paper_id': args.paper_id,
        'paragraphs': paragraphs,
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Wrote {len(paragraphs)} anchors to {out_path}')


if __name__ == '__main__':
    main()
