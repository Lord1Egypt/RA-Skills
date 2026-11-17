# -*- coding: utf-8 -*-
"""把 chapters/ 中指定章节正文同步回 notes-personal/正文草稿.md"""
import re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')

DRAFT = 'notes-personal/正文草稿.md'
NUMS = sys.argv[1:] or ['042', '028', '030', '033', '037']

src = {}
for p in glob.glob('chapters/**/*.md', recursive=True):
    m = re.search(r'第(\d+)章', os.path.basename(p))
    if m:
        src[str(int(m.group(1)))] = p

t = open(DRAFT, encoding='utf-8').read()
lines = t.split('\n')

for n in NUMS:
    key = str(int(n))
    if key not in src:
        print('缺少章节文件', n); continue
    body = open(src[key], encoding='utf-8').read().strip('\n')
    pat = re.compile(r'^## 第0*' + str(int(n)) + r'章')
    start = next((i for i, l in enumerate(lines) if pat.match(l)), None)
    if start is None:
        print('草稿中未找到 第%s章' % n); continue
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r'^## 第\d+章', lines[j]) or re.match(r'^# ', lines[j]):
            end = j; break
    lines[start:end] = body.split('\n') + ['']
    print('同步 第%s章 -> 草稿' % n)

open(DRAFT, 'w', encoding='utf-8').write('\n'.join(lines))

# 校验：章标题零差异
d = set(re.findall(r'^## 第(\d+)章 (.+)$', '\n'.join(lines), re.M))
c = set()
for k, p in src.items():
    m = re.search(r'^## 第(\d+)章 (.+)$', open(p, encoding='utf-8').read(), re.M)
    if m: c.add((m.group(1), m.group(2)))
print('草稿章数', len(d), 'chapters 章数', len(c), '标题差异', len(d ^ c))
