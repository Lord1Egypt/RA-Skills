# -*- coding: utf-8 -*-
"""逐页统计 PDF 的文字量与首尾片段，用于判断分页是否合理。"""
import re
import sys
from pypdf import PdfReader


def clean(t):
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def report(path):
    r = PdfReader(path)
    print('=' * 78)
    print(path, ' pages =', len(r.pages))
    print('=' * 78)
    lens = []
    for i, pg in enumerate(r.pages):
        t = clean(pg.extract_text() or '')
        lens.append(len(t))
        head = t[:34]
        tail = t[-26:]
        print(f'  p{i+1:02d}  {len(t):5d} 字   {head}  ……  {tail}')
    if lens:
        avg = sum(lens) / len(lens)
        print(f'  --- 平均 {avg:.0f} 字/页；最短 {min(lens)}（p{lens.index(min(lens))+1}）'
              f'；最长 {max(lens)}（p{lens.index(max(lens))+1}）')
        thin = [i + 1 for i, n in enumerate(lens) if n < avg * 0.55]
        print(f'  --- 内容明显偏少的页: {thin if thin else "无"}')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        report(p)
        print()
