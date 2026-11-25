#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-font-fixer · fontkit —— 字体工具（找同款 / 转换 / 子集）

三个子命令
----------
  list                     列出本机所有**中文 TrueType** 字体（能安全嵌 PDF 的）
  find <family>            查某个字体名在本机有没有 TrueType 款
  to-ttf <字体文件> -o out.ttf [--text "用到的字"] [--text-file f]
                           把 OTF/CFF 转成 TrueType（glyf）。给了 --text 就先子集化再转，
                           几百字的中文卡片通常 10 秒内完成。
  subset <字体文件> -o out --text "..." | --text-file f
                           只做子集化

为什么需要 to-ttf
-----------------
CFF/OpenType 字体的子集在 PDF 里是 CID Type 0C，部分设备（华为打印预览等）画不出字形。
若某字体只有 OTF/CFF 版：
  ① 先找同族原生 TTF（find）——最省事、零损耗
  ② 没有就 to-ttf 自己转 —— 三次贝塞尔→二次贝塞尔有极小近似（实测可见差异约 0.85%）
  ③ 转完再嵌 PDF，detect 就能通过
⚠️ 商业授权字体（方正、汉仪等）多数禁止修改字体文件，转格式前先确认授权。
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C


def list_zh_ttf():
    """返回 [(path, family)]，只列 fontformat=TrueType 的中文字体。"""
    try:
        r = subprocess.run(['fc-list', ':lang=zh', 'file', 'family', 'fontformat'],
                           capture_output=True, text=True, timeout=25)
    except Exception:
        return []
    out = []
    for line in (r.stdout or '').splitlines():
        parts = line.split(':')
        if len(parts) < 3:
            continue
        p, fam, fmt = parts[0].strip(), parts[1].strip(), parts[-1].strip()
        if 'TrueType' in fmt:
            out.append((p, fam))
    return sorted(set(out))


def find_family(family):
    rows = []
    try:
        r = subprocess.run(['fc-list', ':', 'file', 'family', 'fontformat'],
                           capture_output=True, text=True, timeout=25)
    except Exception:
        return rows
    for line in (r.stdout or '').splitlines():
        parts = line.split(':')
        if len(parts) < 3:
            continue
        p, fam, fmt = parts[0].strip(), parts[1].strip(), parts[-1].strip()
        if family.lower() in fam.lower():
            rows.append((p, fam, fmt))
    return rows


def do_subset(src, dst, text=None, text_file=None):
    from fontTools import subset
    args = [src, '--output-file=' + dst, '--layout-features=*', '--no-hinting']
    if text_file:
        args.append('--text-file=' + text_file)
    elif text is not None:
        args.append('--text=' + text)
    else:
        raise SystemExit('subset 需要 --text 或 --text-file')
    subset.main(args)


def do_to_ttf(src, dst, max_err=1.0):
    """CFF/OTF → TrueType(glyf)。优先用 otf2ttf 包，没有就用内置实现。"""
    try:
        import otf2ttf
        rc = otf2ttf.main([src, '-o', dst])
        if os.path.exists(dst):
            return
    except Exception:
        pass
    # ---- 内置实现（fontTools）----
    from fontTools.ttLib import TTFont, newTable
    from fontTools.ttLib.tables._m_a_x_p import table__m_a_x_p
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen

    font = TTFont(src)
    order = font.getGlyphOrder()
    gs = font.getGlyphSet()
    glyf = newTable('glyf')
    glyf.glyphOrder = order
    glyf.glyphs = {}
    for name in order:
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, max_err, reverse_direction=True))
        glyf[name] = pen.glyph()
    font['glyf'] = glyf
    font['loca'] = newTable('loca')

    maxp = table__m_a_x_p()
    maxp.tableVersion = 0x00010000
    font['maxp'] = maxp
    # maxp.recalc() 依赖每个字形的 xMin/xMax，必须先算包围盒（否则 AttributeError: xMin）
    for name in order:
        try:
            glyf[name].recalcBounds(glyf)
        except Exception:
            pass
    try:
        maxp.recalc(font)
    except Exception:
        pass
    # ⚠️ fontTools 4.6x 的 maxp.recalc() 只填 numGlyphs 等基础字段，v1.0 的扩展字段
    #    不填 → 保存时编译 maxp 会 KeyError: 'maxZones'。这里必须补齐。
    for k, v in dict(maxZones=1, maxTwilightPoints=0, maxStorage=0,
                     maxFunctionDefs=0, maxInstructionDefs=0, maxStackElements=0,
                     maxSizeOfInstructions=0, maxComponentElements=0,
                     maxComponentDepth=0).items():
        if not hasattr(maxp, k):
            setattr(maxp, k, v)
    if not hasattr(maxp, 'numGlyphs'):
        maxp.numGlyphs = len(order)

    font['head'].indexToLocFormat = 0
    for t in ('CFF ', 'CFF2', 'VORG'):
        if t in font:
            del font[t]
    font.sfntVersion = '\000\001\000\000'
    font.save(dst)


def do_lint(font_path, text):
    """扫一遍文本，列出该字体 cmap 里没有的字符（会渲染成豆腐块/空白）。"""
    from fontTools.ttLib import TTFont
    f = TTFont(font_path, fontNumber=0)
    cm = f.getBestCmap()
    n = len(cm)
    f.close()
    chars = sorted(set(text))
    miss = [c for c in chars if ord(c) not in cm]
    return n, chars, miss


def main():
    ap = argparse.ArgumentParser(description='字体工具：找同款 / OTF→TTF / 子集')
    sub = ap.add_subparsers(dest='cmd', required=True)

    sub.add_parser('list', help='列出本机中文 TrueType 字体')

    p = sub.add_parser('find', help='查某字体名有没有 TrueType 款')
    p.add_argument('family')

    p = sub.add_parser('to-ttf', help='OTF/CFF → TrueType')
    p.add_argument('font')
    p.add_argument('-o', '--out', required=True)
    p.add_argument('--text', help='只保留这些字符（子集化后再转，速度快得多）')
    p.add_argument('--text-file')
    p.add_argument('--max-err', type=float, default=1.0,
                   help='三次→二次贝塞尔的近似容差（默认 1.0，越小越精确越慢）')

    p = sub.add_parser('lint', help='检查某字体缺哪些字符（豆腐块预警）')
    p.add_argument('font')
    p.add_argument('--text')
    p.add_argument('--text-file')

    p = sub.add_parser('subset', help='子集化')
    p.add_argument('font')
    p.add_argument('-o', '--out', required=True)
    p.add_argument('--text')
    p.add_argument('--text-file')

    a = ap.parse_args()

    if a.cmd == 'list':
        rows = list_zh_ttf()
        if not rows:
            print('（本机没有中文 TrueType 字体）')
            return 1
        print('本机中文 TrueType 字体：')
        for p, fam in rows:
            print('  %-28s %s' % (fam, p))
        return 0

    if a.cmd == 'find':
        rows = find_family(a.family)
        if not rows:
            print('❌ 本机没有字体族「%s」' % a.family)
            return 2
        print('「%s」在本机：' % a.family)
        has_tt = False
        for p, fam, fmt in rows:
            flag = 'TrueType ✓ 可安全嵌 PDF' if 'TrueType' in fmt else 'CFF/OTF ✗ 嵌入后会乱码'
            print('  %-34s %-9s %s' % (fam, fmt, flag))
            print('      ' + p)
            has_tt = has_tt or ('TrueType' in fmt)
        print('\n结论：%s' % ('有 TrueType 款，直接用' if has_tt
                             else '只有 CFF/OTF → 用 to-ttf 转换，或换同族 TTF'))
        return 0 if has_tt else 2

    if a.cmd == 'lint':
        if not os.path.isfile(a.font):
            C.die('字体不存在：%s' % a.font)
        text = a.text or ''
        if a.text_file:
            text += open(a.text_file, encoding='utf-8').read()
        if not text:
            C.die('lint 需要 --text 或 --text-file')
        n, chars, miss = do_lint(a.font, text)
        print('字体：%s（cmap %d 字形）' % (os.path.basename(a.font), n))
        print('文本：%d 个不同字符' % len(chars))
        if not miss:
            print('\n✅ 全部覆盖，无缺字。')
            return 0
        print('\n❌ 缺 %d 个字符（会渲染成豆腐块/空白）：' % len(miss))
        for c in miss:
            print('    %s  U+%04X' % (c, ord(c)))
        print('\n建议：换覆盖更全的字体，或把这些字改用图片/其他字体单独处理。')
        return 2

    if not os.path.isfile(a.font):
        C.die('字体不存在：%s' % a.font)

    if a.cmd == 'subset':
        do_subset(a.font, a.out, a.text, a.text_file)
        print('✅ 子集化完成 → %s（%s）' % (a.out, C.human(os.path.getsize(a.out))))
        return 0

    if a.cmd == 'to-ttf':
        src = a.font
        tmp = None
        if a.text or a.text_file:
            tmp = a.out + '.sub.otf'
            do_subset(src, tmp, a.text, a.text_file)
            src = tmp
        do_to_ttf(src, a.out, max_err=a.max_err)
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
        from fontTools.ttLib import TTFont
        f = TTFont(a.out)
        kind = 'glyf ✓' if 'glyf' in f else 'CFF ✗（转换失败）'
        print('✅ 转换完成 → %s（%s，%d 字形，轮廓=%s）'
              % (a.out, C.human(os.path.getsize(a.out)), f['maxp'].numGlyphs, kind))
        return 0 if 'glyf' in f else 2


if __name__ == '__main__':
    sys.exit(main())
