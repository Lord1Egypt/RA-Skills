#!/usr/bin/env python3
# 事实锚复核：对比原文与改后稿，抽取数字、行内代码、英文专名，做集合差集。
# 它只读取文件、不修改任何东西；与读文件的接口不同，用来独立复核事实锚。
#
# 用法（Windows / WSL / Ubuntu / macOS 通用，工作区根目录执行）：
#   python <skill_dir>/scripts/fact_anchor_check.py "gongzuoliu/试跑/<日期_样本名>/01_原稿.md" "gongzuoliu/试跑/<日期_样本名>/02_二创稿.md"

import re
import sys
from pathlib import Path

RE_NUM = re.compile(r'\d+(?:[.,]\d+)*\s*%?')
RE_CODE = re.compile(r'`[^`\r\n]+`')
RE_EN = re.compile(r'[A-Za-z][A-Za-z0-9_./\-]{1,}')


def get_anchors(path):
    with open(path, encoding='utf-8', newline='') as f:
        text = f.read()
    items = []
    for m in RE_NUM.finditer(text):
        items.append('数字  ' + re.sub(r'\s', '', m.group()))
    for m in RE_CODE.finditer(text):
        items.append('代码  ' + m.group().strip('`'))
    for m in RE_EN.finditer(text):
        items.append('英文  ' + m.group())
    return sorted(set(items))


def paint(s, code):
    return '\033[{}m{}\033[0m'.format(code, s) if sys.stdout.isatty() else s


def main():
    if len(sys.argv) != 3:
        print('Usage: python fact_anchor_check.py <original.md> <revised.md>', file=sys.stderr)
        return 2
    original, revised = sys.argv[1], sys.argv[2]
    old_list = get_anchors(original)
    new_list = get_anchors(revised)

    lost = sorted(set(old_list) - set(new_list))
    added = sorted(set(new_list) - set(old_list))

    print()
    print(paint('=== 原文有、终稿没有 —— 逐条核对该不该丢 ===', 33))
    if not lost:
        print('  （无）')
    else:
        for item in lost:
            print('  ' + item)

    print()
    print(paint('=== 终稿有、原文没有 —— 逐条核对是不是编辑所加 ===', 36))
    if not added:
        print('  （无）')
    else:
        for item in added:
            print('  ' + item)

    print()
    print('原文锚点 {} 项 · 终稿锚点 {} 项'.format(len(old_list), len(new_list)))
    print('丢失 {} 项 · 新增 {} 项'.format(len(lost), len(added)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
