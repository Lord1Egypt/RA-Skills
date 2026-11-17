#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · gate —— 一步式交付门禁（detect + verify 合体）

其它 skill 只需要记这一条命令：

    python3 "$PDF_FONT_FIXER/scripts/gate.py" 产物.pdf

它依次做两件事：
  1. detect：PDF 里有哪些字体、轮廓类型对不对（整体）
  2. verify：**每一个字**落在哪个字体上、有没有豆腐块（逐字符）

两关都过才算通过。退出码 0=可以交付 / 2=不合格 / 1=无法检查。

为什么要逐字符（verify）而不只看整体（detect）
------------------------------------------------
排版引擎遇到主字体缺字会自动逐字回退到系统里的别的字体。实测：用 Noto Sans SC 排版时，
`𠮷`、`한국어` 被自动回退到 **Noto Sans CJK（CFF）**——字显示出来了，PDF 里却混进 CFF 字体，
手机上这些字照样乱码。整体看「有 CFF 字体」，但说不出是哪几个字、也没法针对性修。
逐字符审计能直接点出「𠮷한국어 这 4 个字落在 CFF 字体上」。

用法
----
  python3 gate.py 产物.pdf
  python3 gate.py 产物.pdf --quiet      # 只输出结论
  python3 gate.py 产物.pdf --json
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import detect
import verify


def main():
    ap = argparse.ArgumentParser(description='PDF 交付门禁（字体类型 + 逐字符归属）')
    ap.add_argument('pdf', nargs='+')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--deep', action='store_true', help='detect 阶段加查 charset 错位')
    a = ap.parse_args()

    worst = 0
    payload = []
    for p in a.pdf:
        if not os.path.isfile(p):
            print('[X] 文件不存在：%s' % p, file=sys.stderr)
            worst = max(worst, 1)
            continue

        d = detect.inspect_pdf(p, deep=a.deep)
        v = verify.audit(p)

        if a.json:
            payload.append(dict(path=p, detect_verdict=d['verdict'],
                                verify_verdict=v['verdict'],
                                bad_fonts=[f['basefont'] for f in d['bad']],
                                cff_chars={k: ''.join(r['chars']) for k, r in v['fonts'].items()
                                           if r['kind'] != 'TrueType'},
                                tofu={k: ''.join(c) for k, c in v['tofu'].items()}))
        else:
            if not a.quiet:
                print('\n文件：%s（%.2f MB，%d 页）' % (p, d['size_mb'], d['pages']))
                for f in d['fonts']:
                    mark = 'OK  ' if f['risk'] == 'ok' else 'FAIL'
                    print('  [%s] %-34s %-16s %s' % (mark, f['basefont'][:34], f['flavor'],
                                                     'p%s' % f['pages']))
                for fname, rec in v['fonts'].items():
                    if rec['kind'] != 'TrueType':
                        print('  ⚠️ %s 承载了这些字（手机可能乱码）：%s'
                              % (fname, ''.join(rec['chars'])[:60]))
                    if rec['gid0']:
                        print('  ⚠️ %s 里有豆腐块：%s' % (fname, ''.join(rec['gid0'])))

            problems = []
            if d['bad']:
                problems.append('%d 个风险字体' % len(d['bad']))
            cff_chars = [f for f, r in v['fonts'].items() if r['kind'] != 'TrueType']
            if cff_chars:
                problems.append('%d 个字体承载的字符会被手机吃掉' % len(cff_chars))
            if v['tofu']:
                problems.append('%d 个字体有豆腐块' % len(v['tofu']))

            if problems:
                print('\n❌ 门禁不通过：%s' % '；'.join(problems))
                print('   → 先换 TrueType 字体重出；缺字用 fontkit to-ttf 造兜底字体挂到 font-family 链；')
                print('     实在不行 fix.py（会牺牲复制能力，且必须告知用户）。')
                worst = max(worst, 2)
            else:
                print('\n✅ 门禁通过：字体全是 TrueType，每个字都有归属字形。')

    if a.json:
        print(json.dumps(payload if len(payload) > 1 else (payload[0] if payload else {}),
                         ensure_ascii=False, indent=1))
    return worst


if __name__ == '__main__':
    sys.exit(main())
