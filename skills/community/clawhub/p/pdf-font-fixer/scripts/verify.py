#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · verify —— 逐字符字体审计（回退链的验收闭环）

detect 只看「PDF 里有哪些字体」；verify 进一步回答：
**每一个字，到底落在哪个字体上？那个字体能不能在手机上显示？**

为什么需要它
------------
weasyprint / Chrome 这类排版引擎遇到主字体缺字时，会**自动逐字回退**到系统里别的字体
（fontconfig 匹配）。这带来两个坑：

1. 回退目标不可控 —— 实测一份用 Noto Sans SC 的卡片，`𠮷` 和 `한국어` 被自动回退到了
   **Noto Sans CJK SC（CFF 轮廓）**，字是显示出来了，但 PDF 里混进了 CFF 字体 →
   手机上这些字照样乱码。整体字体清单能抓到，但说不出「是哪些字」。
2. 回退失败时字会变成豆腐块（.notdef，glyph id = 0），文本层却还在，肉眼不放大看不出来。

所以验收要逐字符看两件事：
  · 该字符所属字体的轮廓类型必须是 TrueType（否则手机会乱码）
  · 该字符的 glyph id 不能是 0（否则是豆腐块，等于没这个字）

用法
----
  python3 verify.py 文件.pdf                  # 审计并给结论
  python3 verify.py 文件.pdf --list-chars     # 额外列出每个字体承载了哪些字
  python3 verify.py 文件.pdf --json           # 机器可读

退出码  0 通过 / 2 有字符落在 CFF 或为豆腐块 / 1 无法检查
"""
import argparse
import json
import os
import sys

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print('[X] 需要 pymupdf', file=sys.stderr)
        sys.exit(1)


def _font_kind(doc, fontname):
    """从 PDF 里查这个字体是 TrueType 还是 CFF。"""
    try:
        for page in doc:
            for f in page.get_fonts(full=True):
                if f[3] == fontname or f[3].split('+')[-1] in fontname:
                    ext = (f[1] or '').lower()
                    return {'ttf': 'TrueType', 'otf': 'CFF', 'cff': 'CFF',
                            'cid': 'CFF/CID', 'n/a': '未嵌入'}.get(ext, '未知(%s)' % ext)
    except Exception:
        pass
    return '未知'


def audit(path, list_chars=False):
    doc = pymupdf.open(path)
    by_font = {}          # fontname -> {'chars': [...], 'kind': str, 'gid0': [...]}
    total = 0
    for pno, page in enumerate(doc, 1):
        try:
            spans = page.get_texttrace()
        except Exception:
            continue
        for span in spans:
            fname = span['font']
            rec = by_font.setdefault(fname, dict(chars=[], gid0=[], pages=set()))
            rec['pages'].add(pno)
            for ch in span['chars']:
                u, gid = ch[0], ch[1]
                total += 1
                if u in (0, 32, 10, 13, 9):
                    continue
                c = chr(u)
                if c not in rec['chars']:
                    rec['chars'].append(c)
                if gid == 0 and c not in rec['gid0']:
                    rec['gid0'].append(c)
    for fname, rec in by_font.items():
        rec['kind'] = _font_kind(doc, fname)
    doc.close()
    bad = {f: r for f, r in by_font.items() if r['kind'] not in ('TrueType',)}
    tofu = {f: r['gid0'] for f, r in by_font.items() if r['gid0']}
    return dict(path=path, total_chars=total, fonts=by_font,
                bad_fonts=list(bad), tofu=tofu,
                verdict='fail' if (bad or tofu) else 'pass')


def main():
    ap = argparse.ArgumentParser(description='逐字符字体审计')
    ap.add_argument('pdf')
    ap.add_argument('--list-chars', action='store_true')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    if not os.path.isfile(a.pdf):
        print('[X] 文件不存在：%s' % a.pdf, file=sys.stderr)
        return 1

    res = audit(a.pdf)
    if a.json:
        out = dict(res)
        out['fonts'] = {k: dict(chars=''.join(v['chars']), kind=v['kind'],
                                gid0=''.join(v['gid0']), pages=sorted(v['pages']))
                        for k, v in res['fonts'].items()}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0 if res['verdict'] == 'pass' else 2

    print('\n文件：%s（共 %d 个字符）' % (a.pdf, res['total_chars']))
    for fname, rec in res['fonts'].items():
        ok = rec['kind'] == 'TrueType'
        mark = '✅' if ok else '❌'
        chars = ''.join(rec['chars'])
        print('%s %-36s %-14s %3d 字  p%s' % (
            mark, fname[:36], rec['kind'], len(rec['chars']),
            ','.join(str(x) for x in sorted(rec['pages'])[:6]) +
            ('…' if len(rec['pages']) > 6 else '')))
        if a.list_chars or not ok:
            print('      %s%s' % (chars[:80], '…' if len(chars) > 80 else ''))
        if rec['gid0']:
            print('      ⚠️ 豆腐块：%s' % ''.join(rec['gid0']))

    if res['verdict'] == 'pass':
        print('\n✅ 通过：每个字符都落在 TrueType 字体上，且没有豆腐块。')
        return 0

    print('\n❌ 不通过：')
    for f in res['bad_fonts']:
        print('   - 字体 %s 是 %s → 它承载的字在手机上会乱码' % (f, res['fonts'][f]['kind']))
    for f, chars in res['tofu'].items():
        print('   - 字体 %s 里有豆腐块（glyph id=0）：%s' % (f, ''.join(chars)))
    print('\n修法（按代价从低到高）：')
    print('   1) 把这些缺字从覆盖最全的字体按需造一个 TrueType 兜底字体，显式挂到 font-family 链上：')
    print('      fontkit.py to-ttf NotoSansCJK-SC.otf -o fallback.ttf --text "<缺的那些字>"')
    print('      CSS: font-family: "主字体", "兜底字体", sans-serif;')
    print('   2) 换一个覆盖这些字的 TrueType 主字体；')
    print('   3) fix.py --outline 转轮廓（字体彻底无关，但失去复制）。')
    return 2


if __name__ == '__main__':
    sys.exit(main())
