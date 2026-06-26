#!/usr/bin/env python3
"""
create-mind-map.py — 思维导图生成器 CLI

输入（至少一个）：
    --input <文件路径>        Markdown / JSON / OPML / XMind
    --input-text "..."       直接传字符串
    --input-format <fmt>     markdown | json | opml | xmind | auto（默认 auto）

输出：
    --output <文件路径>      按扩展名决定格式：xmind / opml / md / mm / png / pdf / svg / json
    --also <fmt1,fmt2,...>   基于 --output 的同名目录，额外导出指定格式

渲染：
    --style <name>           modern | classic | dark | xiaohongshu
    --dpi <n>                PNG 分辨率，默认 200

用法示例：
    # 从 Markdown 大纲生成 XMind
    python3 create-mind-map.py --input outline.md --output map.xmind

    # 一次性生成 XMind + PNG + PDF
    python3 create-mind-map.py --input outline.md --output /tmp/map.xmind \\
        --also png,pdf --style xiaohongshu
"""

from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from mindmap_tree import (
    Node, parse_auto, parse_markdown, parse_json, parse_opml, parse_xmind,
    to_markdown, to_json, to_opml, to_xmind, to_freemind,
)

EXT_TO_WRITER = {
    'xmind': 'xmind',
    'opml': 'opml',
    'md': 'md',
    'markdown': 'md',
    'mm': 'mm',
    'json': 'json',
    'png': 'img',
    'pdf': 'img',
    'svg': 'img',
}


def _infer_format_from_ext(path):
    ext = os.path.splitext(path)[1].lstrip('.').lower()
    if ext in ('md', 'markdown', 'txt'):
        return 'markdown'
    if ext in ('json',):
        return 'json'
    if ext in ('opml', 'xml'):
        return 'opml'
    if ext == 'xmind':
        return 'xmind'
    return 'markdown'


def _read_input(args):
    fmt = args.input_format
    if fmt in ('auto', None):
        fmt = _infer_format_from_ext(args.input) if args.input else 'markdown'

    if args.input_text:
        return parse_auto(args.input_text, hint=fmt)
    if args.input:
        if fmt == 'xmind':
            return parse_xmind(args.input)
        with open(args.input, 'r', encoding='utf-8') as fh:
            text = fh.read()
        return parse_auto(text, hint=fmt)
    # 从 stdin 读
    text = sys.stdin.read()
    return parse_auto(text, hint=fmt)


def _write_one(root: Node, path, style_name, dpi, sheet_name):
    ext = os.path.splitext(path)[1].lstrip('.').lower()
    writer = EXT_TO_WRITER.get(ext)
    if writer is None:
        raise ValueError(f'未知输出扩展名：.{ext}，受支持：'
                         + ', '.join(sorted(EXT_TO_WRITER.keys())))
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)

    if writer == 'xmind':
        to_xmind(root, path, sheet_name=sheet_name or root.title)
    elif writer == 'opml':
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(to_opml(root))
    elif writer == 'md':
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(to_markdown(root))
    elif writer == 'mm':
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(to_freemind(root))
    elif writer == 'json':
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(to_json(root))
    elif writer == 'img':
        # 延迟加载 matplotlib，避免纯转换场景被阻塞
        from mindmap_render import render
        render(root, path, style_name=style_name, dpi=dpi,
               title_text=root.title if ext != 'svg' else None)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='create-mind-map',
        description='火一五思维导图生成器（XMind/OPML/Markdown + PNG/PDF）',
    )
    parser.add_argument('--input', '-i', default=None,
                        help='输入文件路径（markdown/json/opml/xmind）')
    parser.add_argument('--input-text', default=None,
                        help='直接传入 Markdown / JSON / OPML 字符串')
    parser.add_argument('--input-format', default='auto',
                        choices=['auto', 'markdown', 'md', 'json',
                                 'opml', 'xmind'])
    parser.add_argument('--output', '-o', required=True,
                        help='主输出文件路径（扩展名决定格式）')
    parser.add_argument('--also', default='',
                        help='逗号分隔的额外格式：xmind,opml,md,mm,json,png,pdf,svg')
    parser.add_argument('--style', default='modern',
                        help='渲染风格：modern | classic | dark | xiaohongshu')
    parser.add_argument('--dpi', type=int, default=200, help='PNG 分辨率')
    parser.add_argument('--sheet-name', default=None,
                        help='XMind sheet 名（默认取根节点标题）')
    parser.add_argument('--title', default=None,
                        help='覆盖根节点 title（可选）')
    args = parser.parse_args(argv)

    if not args.input and not args.input_text and sys.stdin.isatty():
        parser.error('必须提供 --input 或 --input-text，或从 stdin 传入')

    root = _read_input(args)
    if args.title:
        root.title = args.title

    outputs = [_write_one(root, args.output, args.style, args.dpi,
                          args.sheet_name)]

    extras = [e.strip().lower() for e in args.also.split(',') if e.strip()]
    if extras:
        base, _ = os.path.splitext(args.output)
        for ext in extras:
            if ext not in EXT_TO_WRITER:
                print(f'⚠️  忽略未知格式：{ext}', file=sys.stderr)
                continue
            path = base + '.' + ext
            outputs.append(_write_one(root, path, args.style, args.dpi,
                                      args.sheet_name))

    print(f'✅ 思维导图已生成：{len(outputs)} 个文件')
    for p in outputs:
        print(f'   - {p}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
