#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · detect —— PDF 字体体检（交付前门禁）

用途
----
任何要交给别人（手机预览 / 打印 / 微信发送）的 PDF，导出后都必须先跑这个。
它不修改文件，只回答一个问题：**这份 PDF 换台设备会不会显示不出来？**

判定依据（多机型实测确认）
----------------------------------
PDF 里的文字靠「字体程序」画字形，字体程序有三种轮廓格式：

  TrueType（glyf 坐标点）   → FontFile2 / CIDFontType2  → 全平台正常  ✅
  CFF / OpenType            → FontFile3 / CIDFontType0  → 华为打印预览等设备
                                                          画不出字形 → 中文乱码  ❌
  未嵌入（依赖阅读器自备）   → 换设备就缺字                ❌

除轮廓格式，还有第二类病：字体内部 charset（CID→GID 映射表）错位
（典型来源 WPS 导出），表现为「源机器正常、别人那边乱码、复制出来却是对的」。

用法
----
  python3 detect.py 文件.pdf                 # 体检，人工看
  python3 detect.py 文件.pdf --json          # 机器可读（给其它 skill 做门禁）
  python3 detect.py 文件.pdf --deep          # 加深检查 charset 错位（慢，需 fontTools）
  python3 detect.py 文件.pdf --quiet         # 只输出结论行

退出码
------
  0  通过（没有风险字体）
  2  不通过（存在风险字体，必须修复后再交付）
  1  无法检查（文件不存在 / 打不开）
"""
import argparse
import io
import json
import os
import sys

try:
    import pymupdf
except ImportError:                                     # pragma: no cover
    try:
        import fitz as pymupdf
    except ImportError:
        print('[X] 需要 pymupdf：pip install pymupdf', file=sys.stderr)
        sys.exit(1)

# 轮廓格式 → 风险等级
RISK_OK, RISK_BAD, RISK_WARN, RISK_INFO = 'ok', 'bad', 'warn', 'info'

FLAVOR = {
    'ttf': ('TrueType', RISK_OK),
    'otf': ('CFF/OpenType', RISK_BAD),
    'cff': ('CFF/OpenType', RISK_BAD),
    'n/a': ('未嵌入', RISK_BAD),
    '': ('未嵌入', RISK_BAD),
    'type1': ('Type1 未嵌入', RISK_BAD),
    'type1c': ('CFF/OpenType', RISK_BAD),
    'type3': ('Type3（位图字形）', RISK_INFO),
    # pymupdf 对 CIDFontType0（CFF/CID-keyed）返回 'cid'，同样会乱码，必须判风险
    'cid': ('CFF/CID（CIDFontType0）', RISK_BAD),
}

HINT = {
    'CFF/OpenType': '换同款 TrueType 字体重出（首选）；无 TTF 版可用 fix --outline 转轮廓',
    'CFF/CID（CIDFontType0）': '先试 fix（charset 重写可无损修好 WPS 型）；否则换同款 TrueType 重出',
    '未嵌入': '必须换字体重出，或 fix --outline 转轮廓',
    'Type1 未嵌入': '必须换字体重出，或 fix --outline 转轮廓',
}


def _filesize_mb(n):
    return n / 1024.0 / 1024.0


def inspect_pdf(path, deep=False):
    """返回 dict：{path, pages, fonts:[…], bad:[…], warn:[…], verdict}"""
    doc = pymupdf.open(path)
    seen = {}
    fonts = []
    for pno, page in enumerate(doc, 1):
        try:
            flist = page.get_fonts(full=True)
        except Exception:
            continue
        for item in flist:
            xref, ext, ftype, basefont = item[0], item[1], item[2], item[3]
            key = (xref, basefont)
            if key in seen:
                seen[key]['pages'].add(pno)
                continue
            ext_l = (ext or '').lower()
            flavor, risk = FLAVOR.get(ext_l, ('未知（%s）' % ext, RISK_WARN))
            if (ftype or '').lower() == 'type1' and ext_l in ('n/a', ''):
                flavor, risk = FLAVOR['type1']
            if (ftype or '').lower() == 'type3':
                flavor, risk = FLAVOR['type3']
            # 判断 FontFile3 的具体子类型（/OpenType 还是裸 /CIDFontType0C）
            sub = ''
            try:
                keys = doc.xref_get_keys(xref)
                if 'FontFile3' in keys:
                    obj = doc.xref_object(xref, compressed=True)
                    sub = 'OpenType 包装' if '/OpenType' in obj else '裸 CFF'
            except Exception:
                pass
            rec = dict(xref=xref, basefont=str(basefont), type=str(ftype), ext=ext_l,
                       flavor=flavor, risk=risk, sub=sub, pages={pno}, charmap=None)
            seen[key] = rec
            fonts.append(rec)
    for rec in fonts:
        rec['pages'] = sorted(rec['pages'])

    # 深度检查：CFF 字体的 charset 是否与 ToUnicode 对齐（WPS 型错位）
    if deep:
        for rec in fonts:
            if rec['ext'] in ('otf', 'cff', 'cid') and rec['risk'] != RISK_OK:
                rec['charmap'] = _check_charset(doc, rec['xref'], path=path)

    bad = [f for f in fonts if f['risk'] == RISK_BAD]
    warn = [f for f in fonts if f['risk'] in (RISK_WARN, RISK_INFO)]
    out = dict(path=path, pages=doc.page_count,
               size_mb=_filesize_mb(os.path.getsize(path)),
               fonts=fonts, bad=bad, warn=warn,
               verdict='fail' if bad else 'pass')
    doc.close()
    return out


def _check_charset(doc, xref, path=None):
    """检查裸 CFF 的 charset 是否 Identity（WPS 型错位用这个判）。

    返回 dict(ok=bool|None, ratio, note)。优先用 pikepdf 直接读 FontFile3 流
    （pymupdf 的 extract_font 对这种字体常取不到）。
    """
    try:
        from fontTools.cffLib import CFFFontSet
        from fontTools.ttLib import TTFont
    except ImportError:
        return dict(ok=None, ratio=None, note='未安装 fontTools，跳过')
    raw = None
    try:
        import pikepdf
        pdf = pikepdf.open(path)
        for page in pdf.pages:
            fonts = (page.get('/Resources') or {}).get('/Font')
            if fonts is None:
                continue
            for _k, f in fonts.items():
                try:
                    if f.objgen[0] != xref:
                        continue
                    df = f.get('/DescendantFonts')
                    if df is None or len(df) == 0:
                        continue
                    fd = df[0].get('/FontDescriptor')
                    if fd is None:
                        continue
                    ff = fd.get('/FontFile3')
                    if ff is not None:
                        raw = bytes(ff.read_bytes())
                        break
                except Exception:
                    continue
            if raw:
                break
        pdf.close()
    except Exception:
        raw = None
    if raw is None:
        try:
            _nm, _ext, _ft, buf = doc.extract_font(xref)
            raw = buf or None
        except Exception:
            raw = None
    if not raw:
        return dict(ok=None, ratio=None, note='取不到字体流')
    try:
        otf = TTFont()
        cff = CFFFontSet()
        cff.decompile(io.BytesIO(raw), otf)
        td = cff[cff.fontNames[0]]
        charset = list(td.charset)
        n = len(charset)
        if not n:
            return dict(ok=None, ratio=None, note='字体不含字形')
        ident = sum(1 for i, nm in enumerate(charset) if nm == 'cid%05d' % i)
        ratio = ident / float(n)
        return dict(ok=ratio > 0.9, ratio=round(ratio, 4),
                    note='charset 与 Identity 一致' if ratio > 0.9 else 'charset 错位（WPS 型）')
    except Exception as e:
        return dict(ok=None, ratio=None, note='解析失败：%s' % str(e)[:60])


def report(res, quiet=False):
    if not quiet:
        print('\n文件：%s（%.2f MB，%d 页）' % (res['path'], res['size_mb'], res['pages']))
        if not res['fonts']:
            print('  （未发现任何字体 —— 可能是扫描件/纯图形 PDF）')
        for f in res['fonts']:
            mark = {'ok': 'OK  ', 'bad': 'FAIL', 'warn': 'WARN', 'info': 'INFO'}[f['risk']]
            extra = (' ' + f['sub']) if f['sub'] else ''
            cm = f.get('charmap')
            if cm and cm.get('ok') is False:
                extra += '  charset 错位！'
            print('  [%s] %-34s %-16s %s%s' % (
                mark, f['basefont'][:34], f['flavor'], 'p%s' % f['pages'], extra))
        if res['bad']:
            print('\n  ⚠️ 风险字体（这些在部分设备上画不出字形 → 中文乱码）：')
            for f in res['bad']:
                print('     - %s  [%s]' % (f['basefont'], f['flavor']))
            flavors = sorted(set(f['flavor'] for f in res['bad']))
            for fl in flavors:
                if fl in HINT:
                    print('     修法：%s' % HINT[fl])
    if res['verdict'] == 'pass':
        print('\n✅ 通过：所有字体都是全平台可渲染的格式。')
    else:
        print('\n❌ 不通过：发现 %d 个风险字体，必须修复后再交付。' % len(res['bad']))
        print('   修复：python3 scripts/fix.py %s' % res['path'])


def main():
    ap = argparse.ArgumentParser(description='PDF 字体体检（交付前门禁）')
    ap.add_argument('pdf', nargs='+')
    ap.add_argument('--json', action='store_true', help='输出 JSON（供其它 skill 程序化调用）')
    ap.add_argument('--deep', action='store_true', help='加深检查 CFF charset 错位（需 fontTools）')
    ap.add_argument('--quiet', action='store_true', help='只输出结论')
    a = ap.parse_args()

    worst = 0
    results = []
    for p in a.pdf:
        if not os.path.isfile(p):
            print('[X] 文件不存在：%s' % p, file=sys.stderr)
            worst = max(worst, 1)
            continue
        try:
            res = inspect_pdf(p, deep=a.deep)
        except Exception as e:
            print('[X] 无法检查 %s：%s' % (p, e), file=sys.stderr)
            worst = max(worst, 1)
            continue
        results.append(res)
        if not a.json:
            report(res, quiet=a.quiet)
        if res['verdict'] == 'fail':
            worst = max(worst, 2)
    if a.json:
        print(json.dumps(results if len(results) > 1 else results[0],
                         ensure_ascii=False, indent=1))
    return worst


if __name__ == '__main__':
    sys.exit(main())
