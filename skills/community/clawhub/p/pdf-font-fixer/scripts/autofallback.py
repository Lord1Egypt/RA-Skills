#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · autofallback —— 主字体缺字时，自动造一个 TrueType 兜底字体

解决什么问题
------------
排版引擎遇到主字体缺字会**自动回退到系统里的别的字体**，而系统里覆盖最全的往往正是
CFF 版（Noto Sans CJK）——字显示出来了，手机上却乱码。实测就踩过：
`𠮷`、`한국어` 被悄悄回退到 Noto-Sans-CJK-SC（CID Type 0C）。

本脚本把回退目标**换成我们指定的 TrueType**：

  1. 扫文本 → 主字体缺哪些字
  2. 没有缺字 → 什么都不做（退出 0），零成本
  3. 有缺字 → 从覆盖最全的字体里**只取这些缺字**做子集，转成 TrueType
     （实测 4 个缺字：0.92 秒 / 1.9 KB / 5 个字形）
  4. 输出 @font-face 的 CSS 片段，挂到 font-family 链的第二个位置

用法
----
  # 从一段文字
  python3 autofallback.py --text "张三𠮷野家 한국" --main /path/main.ttf -o fallback.ttf

  # 从文本文件
  python3 autofallback.py --text-file cards.md --main /path/main.ttf -o fallback.ttf --css fb.css

  # 从数据 JSON（递归取所有字符串，适合 cards.json 这类结构化内容）
  python3 autofallback.py --from-json cards.json --main /path/main.ttf -o fallback.ttf

  # 先干跑看看缺不缺
  python3 autofallback.py --text-file x.md --main /path/main.ttf --dry-run

退出码
------
  0  主字体够用，无需兜底（不会产生任何文件）
  3  已生成兜底字体（**这是成功**，只是需要把 CSS 挂上去）
  2  有缺字但兜底失败（源字体也缺 / 环境问题）

CSS 用法
--------
生成的 frag 形如：
  @font-face { font-family:'CJKFALLBACK'; src:url('file:///path/fallback.ttf'); }
把主字体的 font-family 改写为：
  font-family: "主字体", "CJKFALLBACK", sans-serif;
——**顺序很重要**：兜底放第二位，引擎才不会自己乱挑。
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as C
import fontkit

# 覆盖最全的「源」字体（用来抽缺字做兜底）。按优先级尝试。
SOURCE_CANDIDATES = [
    # ① 覆盖最全的 CJK 字体（含 CJK 扩展 B / 韩文），各平台常见位置
    ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 'Noto Sans CJK SC'),
    ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 'Noto Serif CJK SC'),
    (os.path.expanduser('~/Library/Fonts/NotoSansCJK-Regular.ttc'), 'Noto Sans CJK SC'),
    ('/Library/Fonts/NotoSansCJK-Regular.ttc', 'Noto Sans CJK SC'),
    ('C:/Windows/Fonts/NotoSansCJK-Regular.ttc', 'Noto Sans CJK SC'),
    (os.path.expanduser('~/.fonts/NotoSansCJK-Regular.ttc'), 'Noto Sans CJK SC'),
]
FAMILY = 'CJKFALLBACK'


def collect_chars(text=None, text_file=None, json_file=None):
    chars = set()
    if text:
        chars.update(text)
    if text_file and os.path.exists(text_file):
        chars.update(open(text_file, encoding='utf-8').read())
    if json_file and os.path.exists(json_file):
        data = json.load(open(json_file, encoding='utf-8'))

        def walk(o):
            if isinstance(o, dict):
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
            elif isinstance(o, str):
                chars.update(o)
        walk(data)
    return sorted(c for c in chars if c.strip())


def load_source_face(path, want_family):
    """从 .ttf/.otf/.ttc 里取出可用的字体面并返回一个 otf/ttf 临时路径。"""
    if not os.path.exists(path):
        return None
    if not path.lower().endswith('.ttc'):
        return path
    from fontTools.ttLib.ttCollection import TTCollection
    coll = TTCollection(path)
    pick = None
    for f in coll.fonts:
        fam = f['name'].getDebugName(1) or ''
        if fam == want_family:
            pick = f
            break
    if pick is None:
        return None
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(), 'src.otf')
    pick.save(tmp)
    return tmp


def main():
    ap = argparse.ArgumentParser(description='主字体缺字 → 自动造 TrueType 兜底字体')
    ap.add_argument('--text')
    ap.add_argument('--text-file')
    ap.add_argument('--from-json')
    ap.add_argument('--main', required=True, help='主字体文件路径')
    ap.add_argument('-o', '--out', default='fallback.ttf')
    ap.add_argument('--css', help='同时输出 CSS 片段到该路径')
    ap.add_argument('--source', help='抽缺字的源字体（默认自动找覆盖最全的）')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    if not os.path.isfile(a.main):
        C.die('主字体不存在：%s' % a.main)
    chars = collect_chars(a.text, a.text_file, a.from_json)
    if not chars:
        C.die('没有拿到任何文字（--text / --text-file / --from-json 三选一）')

    n, allchars, miss = fontkit.do_lint(a.main, ''.join(chars))
    print('主字体：%s（cmap %d 字形）' % (os.path.basename(a.main), n))
    print('文本：%d 个不同字符' % len(allchars))
    if not miss:
        print('\n✅ 主字体全部覆盖，无需兜底（未产生任何文件）。')
        return 0

    print('缺 %d 个字：%s' % (len(miss), ''.join(miss)[:60]))
    if a.dry_run:
        print('\n（--dry-run：未生成文件）')
        return 3

    # 找源字体
    srcs = [(a.source, None)] if a.source else SOURCE_CANDIDATES
    src = None
    for path, fam in srcs:
        p = load_source_face(path, fam)
        if p:
            _n, _c, m2 = fontkit.do_lint(p, ''.join(miss))
            if len(m2) < len(miss):        # 能补上一些就算有效
                src = p
                print('源字体：%s（还能补上 %d/%d）' % (os.path.basename(path), len(miss) - len(m2), len(miss)))
                if m2:
                    print('   ⚠️ 源字体也缺：%s（这些字任何 TrueType 都补不了）' % ''.join(m2))
                break
            os.remove(p) if p != path else None
    if not src:
        C.die('找不到能覆盖这些缺字的源字体。换主字体，或改用 fix.py --outline 转轮廓。')

    # 子集 + 转 TrueType
    tmp_otf = a.out + '.sub.otf'
    try:
        fontkit.do_subset(src, tmp_otf, text=''.join(miss))
        fontkit.do_to_ttf(tmp_otf, a.out)
    finally:
        if os.path.exists(tmp_otf):
            os.remove(tmp_otf)

    # 验收：兜底字体必须真的覆盖这些字
    _n2, _c2, m3 = fontkit.do_lint(a.out, ''.join(miss))
    if m3:
        C.die('兜底字体仍缺 %s，放弃（避免生成豆腐块）' % ''.join(m3))
    print('\n✅ 兜底字体：%s（%s）' % (a.out, C.human(os.path.getsize(a.out))))

    css = ("@font-face { font-family:'%s'; font-weight: 400; "
           "src: url('file://%s'); }\n"
           "@font-face { font-family:'%s'; font-weight: 700 900; "
           "src: url('file://%s'); }\n"
           "/* 用法：font-family: \"主字体\", \"%s\", sans-serif; */\n"
           % (FAMILY, os.path.abspath(a.out), FAMILY, os.path.abspath(a.out), FAMILY))
    if a.css:
        open(a.css, 'w', encoding='utf-8').write(css)
        print('CSS 片段 → %s' % a.css)
    else:
        print('\n' + css)
    return 3


if __name__ == '__main__':
    sys.exit(main())
