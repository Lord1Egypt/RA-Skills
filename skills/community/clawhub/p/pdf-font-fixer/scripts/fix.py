#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · fix —— 修复已有 PDF 的字体问题

修复策略是**递进**的，能用轻手段就不用重手段：

  第 0 级  字体没问题            → 什么都不做，退出 0
  第 1 级  charset 错位（WPS 型） → 重写 charset 为 Identity（无损，文字/排版/复制全不变）
  第 2 级  CFF/未嵌入字体         → ghostscript 把文字转成矢量轮廓（显示 100% 保真，但失去复制）
  第 3 级  连轮廓都转不出/需要绝对保险 → 300dpi 位图（扫描版）

⚠️ 第 2 级会牺牲「复制文字」能力。执行后脚本会明确提示：
      「可复制性已牺牲，要保留复制请替换 XXX 字体」
   —— XXX 是按字体名推断出的同族 TrueType 字体（Noto Sans SC 等）。

用法
----
  python3 fix.py 文件.pdf                 # 自动修复（递进，尽量取轻的手段）
  python3 fix.py 文件.pdf --keep-copy     # 只接受不损失复制的修复；做不到就报错并给替换建议
  python3 fix.py 文件.pdf --outline       # 强制转轮廓
  python3 fix.py 文件.pdf --raster        # 强制出位图（扫描版）
  python3 fix.py 文件.pdf --dry-run       # 只说明会怎么修，不改文件
  python3 fix.py 文件.pdf -o 输出.pdf

退出码
------
  0  已通过 / 已修好
  2  仍有风险（修复失败或 --keep-copy 下无法修复）
  1  无法处理
"""
import argparse
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as C
from detect import inspect_pdf, report


# ---------------- 第 1 级：charset 错位（WPS 型，无损） ----------------

def _rewrite_charset_to_identity(raw):
    """把 CFF 的 charset 重写为 Identity（第 N 号 CID ↔ 第 N 号字形）。"""
    from fontTools.cffLib import CFFFontSet
    from fontTools.ttLib import TTFont
    otf = TTFont()
    cff = CFFFontSet()
    cff.decompile(io.BytesIO(raw), otf)
    td = cff[cff.fontNames[0]]
    n = len(td.charset)
    if n == 0:
        raise ValueError('字体不含字形')
    new_names = ['.notdef'] + ['cid%05d' % i for i in range(1, n)]
    cs = td.CharStrings
    if getattr(cs, 'charStringsAreIndexed', 0) == 1:
        cs.charStrings = {name: i for i, name in enumerate(new_names)}
        for i in range(n):
            try:
                cs.charStringsIndex[i].glyphName = new_names[i]
            except Exception:
                pass
    else:
        mapped = {}
        for i, old in enumerate(list(td.charset)):
            ch = cs[old]
            ch.glyphName = new_names[i]
            mapped[new_names[i]] = ch
        cs.charStrings = mapped
    td.charset = new_names
    otf.setGlyphOrder(new_names)
    out = io.BytesIO()
    cff.compile(out, otf)
    return out.getvalue()


def fix_charset(path, out_path):
    """只修 charset 错位。返回 (是否改了, 说明)。"""
    try:
        import pikepdf
    except ImportError:
        return False, '未安装 pikepdf，跳过 charset 修复'
    try:
        pdf = pikepdf.open(path)
    except Exception as e:
        return False, '打不开：%s' % e
    changed = 0
    seen = set()
    for page in pdf.pages:
        fonts = (page.get('/Resources') or {}).get('/Font')
        if fonts is None:
            continue
        for _k, font in fonts.items():
            try:
                if str(font.get('/Subtype')) != '/Type0':
                    continue
                df = font.get('/DescendantFonts')
                if df is None or len(df) == 0:
                    continue
                cid = df[0]
                if str(cid.get('/Subtype')) != '/CIDFontType0':
                    continue
                fd = cid.get('/FontDescriptor')
                if fd is None:
                    continue
                ff = fd.get('/FontFile3')
                if ff is None or str(ff.get('/Subtype')) != '/CIDFontType0C':
                    continue                      # 只处理裸 CFF（WPS 型）；OpenType 包装不在此列
                key = font.objgen
                if key in seen:
                    continue
                seen.add(key)
                raw = bytes(ff.read_bytes())
                new = _rewrite_charset_to_identity(raw)
                ff.write(new)
                changed += 1
            except Exception:
                continue
    if changed == 0:
        pdf.close()
        return False, '没有找到可修 charset 的裸 CFF 字体'
    pdf.save(out_path)
    pdf.close()
    return True, '重写 %d 个字体的 charset（无损，复制能力保留）' % changed


# ---------------- 第 2 级：转矢量轮廓 ----------------

def to_outline(src, dst):
    gs = C.find_gs()
    if not gs:
        return False, '未安装 ghostscript（apt install ghostscript / brew install ghostscript）'
    rc, out = C.run([gs, '-q', '-dNOPAUSE', '-dBATCH', '-dSAFER',
                     '-sDEVICE=pdfwrite', '-dNoOutputFonts',
                     '-dCompatibilityLevel=1.7',
                     '-sOutputFile=' + dst, src], timeout=600)
    if rc != 0 or not os.path.exists(dst):
        return False, 'gs 转轮廓失败：%s' % out.strip()[:200]
    return True, '已转矢量轮廓（PDF 内 0 个字体）'


# ---------------- 第 3 级：位图（扫描版） ----------------

def to_raster(src, dst, dpi=300):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            return False, '需要 pymupdf'
    doc = pymupdf.open(src)
    out = pymupdf.open()
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        p = out.new_page(width=page.rect.width, height=page.rect.height)
        p.insert_image(p.rect, stream=pix.tobytes('jpeg', jpg_quality=92))
    out.save(dst, garbage=4, deflate=True)
    out.close()
    doc.close()
    return True, '%d dpi 位图（扫描版）' % dpi


# ---------------- 主流程 ----------------

def main():
    ap = argparse.ArgumentParser(description='修复 PDF 字体问题（递进式）')
    ap.add_argument('pdf')
    ap.add_argument('-o', '--out', help='输出路径（默认 xxx_已修复.pdf）')
    ap.add_argument('--keep-copy', action='store_true',
                    help='只接受不牺牲复制能力的修复；做不到就报错并给出替换字体的建议')
    ap.add_argument('--outline', action='store_true', help='强制转矢量轮廓')
    ap.add_argument('--raster', action='store_true', help='强制出位图（扫描版）')
    ap.add_argument('--dpi', type=int, default=300)
    ap.add_argument('--charset-only', action='store_true',
                    help='只做 charset 重写（无损、保留复制）；修完仍有字体风险就如实报告')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    if not os.path.isfile(a.pdf):
        C.die('文件不存在：%s' % a.pdf)

    res = inspect_pdf(a.pdf, deep=True)
    report(res)

    if not res['bad']:
        print('\n✅ 无需修复。')
        return 0

    stem, _ = os.path.splitext(a.pdf)
    out = a.out or (stem + '.pdf')

    # 列出要替换的字体（提示文案用）
    names = []
    for f in res['bad']:
        sug = C.suggest_replacement(f['basefont'])
        names.append('%s → 换成 %s' % (f['basefont'], sug))
    charset_broken = any((f.get('charmap') or {}).get('ok') is False for f in res['bad'])

    print('\n[计划] 需要修复 %d 个风险字体' % len(res['bad']))
    if charset_broken:
        print('   1) 先尝试 charset 重写（无损、保留复制）')
    print('   2) 再转矢量轮廓（显示 100% 保真，但失去复制）')
    if a.dry_run:
        print('\n（--dry-run：未改动文件）')
        return 2

    work = a.pdf
    done = []

    # 第 1 级
    if charset_broken and not (a.outline or a.raster):
        tmp = C.unique_path(stem + '_cs.pdf')
        ok, msg = fix_charset(a.pdf, tmp)
        if ok:
            print('   ✓ ' + msg)
            done.append('charset 重写：' + msg)
            work = tmp
            r2 = inspect_pdf(work, deep=True)
            left = [f for f in r2['bad'] if (f.get('charmap') or {}).get('ok') is False]
            if r2['bad'] and not left:
                print('   （charset 已全部对齐，但这些字体仍是 CFF 轮廓，'
                      '能否显示取决于设备是否支持 CFF —— 需要真机验证）')
            if a.charset_only:
                shutil.move(work, out)
                print('\n✅ 已输出「仅修 charset」版本 -> %s（复制能力保留）' % out)
                print('   注意：轮廓仍是 CFF，若设备不支持 CFF 仍会乱码，请真机预览确认。')
                return 0 if not left else 2
            if not r2['bad']:
                shutil.move(work, out)
                print('\n✅ 修复完成（第 1 级：无损）-> %s' % out)
                for d in done:
                    print('   - ' + d)
                return 0
        else:
            print('   （%s，继续下一级）' % msg)

    # 第 2 级
    if not a.raster:
        tmp = C.unique_path(stem + '_ol.pdf')
        ok, msg = to_outline(work, tmp)
        if ok:
            r2 = inspect_pdf(tmp)
            if not r2['bad']:
                out2 = C.tag_path(out, '【轮廓版】')
                shutil.move(tmp, out2)
                print('\n✅ 修复完成（第 2 级：转矢量轮廓）-> %s' % out2)
                print('   原生版仍在原处：%s（先用手机预览它，能正常显示就不用轮廓版）' % a.pdf)
                print('\n   ⚠️ 可复制性已牺牲，要保留复制请替换以下字体后重新生成：')
                for n in names:
                    print('      - ' + n)
                return 0
            print('   （转轮廓后仍有风险字体：%s）' % [f['basefont'] for f in r2['bad']])
            if a.keep_copy:
                pass
            else:
                shutil.move(tmp, C.tag_path(out, '【轮廓版】'))
                print('\n⚠️ 已输出轮廓版，但仍残留风险字体，建议检查：%s'
                      % C.tag_path(out, '【轮廓版】'))
                return 2
        else:
            print('   （%s）' % msg)

    if a.keep_copy:
        print('\n❌ 无法在不牺牲复制能力的前提下修复。请替换字体后重新生成：')
        for n in names:
            print('   - ' + n)
        return 2

    # 第 3 级
    tmp = C.unique_path(stem + '_scan.pdf')
    ok, msg = to_raster(work, tmp, dpi=a.dpi)
    if ok:
        out3 = C.tag_path(out, '【扫描版】')
        shutil.move(tmp, out3)
        print('\n✅ 修复完成（第 3 级：%s）-> %s' % (msg, out3))
        print('   原生版仍在原处：%s（先用手机预览它，能正常显示就不用扫描版）' % a.pdf)
        print('   ⚠️ 已转为位图：不能复制/搜索文字，但任何设备都能正常显示。')
        print('   要保留复制请替换以下字体后重新生成：')
        for n in names:
            print('      - ' + n)
        return 0
    print('\n❌ 修复失败：%s' % msg)
    return 2


if __name__ == '__main__':
    sys.exit(main())
