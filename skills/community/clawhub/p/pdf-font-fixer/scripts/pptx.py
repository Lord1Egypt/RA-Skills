#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-font-fixer · pptx —— PPT 导出 PDF 的**递进三步法**

⚠️ 三步是**回退关系**，不是并列输出：前一步成功就不再走后面。

  第 1 步  本机同款 TrueType 字体齐全 → LibreOffice 直接导 PDF
           ✅ 保留复制/搜索，字形字重 100%（因为用的就是原字体）
           ✅ 过 detect 就结束，不产出任何别的文件

  第 2 步  第 1 步做不到（缺字体 / 只有 CFF 版）→ 导出后把文字转成矢量轮廓
           ✅ 任何设备都能显示，字形 100% 保真
           ❌ 失去复制/搜索

  第 3 步  第 2 步也做不到 → 300dpi 位图（扫描版）
           ✅ 最保险
           ❌ 失去复制/搜索，体积最大

用法
----
  python3 pptx.py 演示.pptx                    # 自动递进
  python3 pptx.py 演示.pptx --keep-copy        # 只接受第 1 步；做不到就报错并列出缺失字体
  python3 pptx.py 演示.pptx --stage 2          # 强制从第 2 步开始
  python3 pptx.py 演示.pptx -o 输出.pdf --dpi 300

退出码  0 成功 / 2 失败或 --keep-copy 下无法满足 / 1 环境缺失
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as C
from detect import inspect_pdf, report

# LibreOffice 内部占位字体名（不是真实字体）
PLACEHOLDER = re.compile(r'^\+|^major|^minor', re.I)


def pptx_fonts(path):
    """读出 pptx 里用到的字体名（latin + eastAsian）。"""
    fonts = set()
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not (n.startswith('ppt/slides/') or n.startswith('ppt/slideMasters/')
                    or n.startswith('ppt/slideLayouts/') or n.startswith('ppt/theme/')):
                continue
            try:
                data = z.read(n).decode('utf-8', 'ignore')
            except Exception:
                continue
            # 只取真正用于文字的 <a:latin>/<a:ea>/<a:cs> typeface；
            # theme 里的 <a:font script="Jpan" typeface="..."/> 是各语种备胎表，不是实际用字，
            # 全收进来会让「缺失字体」清单里冒出一堆从没用过的字体。
            for m in re.finditer(r'<a:(?:latin|ea|cs)\s+typeface="([^"]+)"', data):
                f = m.group(1).strip()
                if f and not PLACEHOLDER.match(f):
                    fonts.add(f)
            for m in re.finditer(r'<(?:a:)?(?:latin|ea|cs)\b[^>]*typeface="([^"]+)"', data):
                f = m.group(1).strip()
                if f and not PLACEHOLDER.match(f):
                    fonts.add(f)
    return sorted(fonts)


def fc_lookup(family):
    """返回该 family 在本机的所有记录 [(path, format)]。"""
    try:
        r = subprocess.run(['fc-list', ':', 'file', 'family', 'fontformat'],
                           capture_output=True, text=True, timeout=20)
    except Exception:
        return []
    out = []
    for line in (r.stdout or '').splitlines():
        parts = line.split(':')
        if len(parts) < 3:
            continue
        p, fam, fmt = parts[0].strip(), parts[1].strip(), parts[-1].strip()
        if fam.lower() == family.lower() or family.lower() in fam.lower().split(','):
            out.append((p, fmt))
    return out


def check_fonts(fonts):
    """逐个字体判断本机是否具备 TrueType 同款。返回 (ok_list, missing, only_cff)。"""
    ok, missing, only_cff = [], [], []
    for fam in fonts:
        recs = fc_lookup(fam)
        if not recs:
            missing.append(fam)
        elif any('TrueType' in fmt for _p, fmt in recs):
            ok.append(fam)
        else:
            only_cff.append(fam)
    return ok, missing, only_cff


def soffice_export(pptx, workdir):
    exe = shutil.which('soffice') or shutil.which('libreoffice')
    if not exe:
        return None, '未安装 LibreOffice（soffice）'
    rc, out = C.run([exe, '--headless', '--norestore', '--convert-to', 'pdf',
                     '--outdir', workdir, pptx], timeout=900)
    base = os.path.splitext(os.path.basename(pptx))[0] + '.pdf'
    p = os.path.join(workdir, base)
    if not os.path.exists(p):
        return None, '转换失败：%s' % out.strip()[:200]
    return p, None


def main():
    ap = argparse.ArgumentParser(description='PPT → PDF（递进三步法）')
    ap.add_argument('pptx')
    ap.add_argument('-o', '--out')
    ap.add_argument('--keep-copy', action='store_true',
                    help='只接受第 1 步（保留复制）；做不到就报错并列出缺失/需替换的字体')
    ap.add_argument('--stage', type=int, choices=(1, 2, 3), default=1,
                    help='从第几步开始（1=同款字体导出，2=转轮廓，3=位图）')
    ap.add_argument('--dpi', type=int, default=300)
    a = ap.parse_args()

    if not os.path.isfile(a.pptx):
        C.die('文件不存在：%s' % a.pptx)
    stem, _ = os.path.splitext(a.pptx)
    out = a.out or (stem + '.pdf')

    fonts = pptx_fonts(a.pptx)
    print('\n文件：%s' % a.pptx)
    print('用到的字体：%s' % ('、'.join(fonts) if fonts else '（未检测到，可能全部用主题默认）'))
    ok, missing, only_cff = check_fonts(fonts) if fonts else ([], [], [])
    if fonts:
        print('   本机有 TrueType 同款：%d 个' % len(ok))
        if missing:
            print('   ❌ 本机缺失：%s' % '、'.join(missing))
        if only_cff:
            print('   ⚠️ 本机只有 CFF/OTF 版（导出仍是坏字体）：%s' % '、'.join(only_cff))

    work = tempfile.mkdtemp(prefix='pptx2pdf_')
    try:
        # ---------- 第 1 步 ----------
        if a.stage <= 1:
            if not missing and not only_cff:
                print('\n[第 1 步] 字体齐全，用 LibreOffice 导出（保留复制）...')
                pdf, err = soffice_export(a.pptx, work)
                if err:
                    print('   ✗ %s' % err)
                else:
                    res = inspect_pdf(pdf)
                    if not res['bad']:
                        shutil.move(pdf, out)
                        report(res, quiet=True)
                        print('\n✅ 完成（第 1 步）：%s' % out)
                        print('   → 可复制、可搜索，字形与 PPT 完全一致。')
                        return 0
                    print('   ✗ 导出后仍有风险字体：%s' % [f['basefont'] for f in res['bad']])
                    if not os.path.exists(os.path.join(work, 'keep.pdf')):
                        shutil.copy(pdf, os.path.join(work, 'keep.pdf'))
            else:
                need = missing + only_cff
                print('\n[第 1 步] 跳过：本机没有以下字体的 TrueType 版 → %s' % '、'.join(need))
                if a.keep_copy:
                    print('\n❌ --keep-copy：无法在第 1 步完成。请先补齐/替换这些字体：')
                    for f in need:
                        print('   - %s → %s' % (f, C.suggest_replacement(f)))
                    return 2
            if a.stage == 1 and a.keep_copy:
                return 2

        keep = os.path.join(work, 'keep.pdf')
        if not os.path.exists(keep):
            keep, err = soffice_export(a.pptx, work)
            if err:
                C.die('LibreOffice 导出失败：%s' % err)

        # ---------- 第 2 步 ----------
        if a.stage <= 2:
            print('\n[第 2 步] 转矢量轮廓（显示保真，失去复制）...')
            ol = os.path.join(work, 'outline.pdf')
            okk, msg = __import__('fix').to_outline(keep, ol)
            if okk:
                res = inspect_pdf(ol)
                if not res['bad']:
                    # 双份：原生（可能有字问题，但保复制）+ 【轮廓版】（一定能显示）
                    shutil.move(keep, out)
                    out2 = C.tag_path(out, '【轮廓版】')
                    shutil.move(ol, out2)
                    print('   ✅ %s' % msg)
                    print('\n✅ 完成（第 2 步），两份都给你：')
                    print('   原生版    ：%s（可复制；先拿手机预览它，能正常显示就用这份）' % out)
                    print('   【轮廓版】：%s（100%% 能显示，但不可复制）' % out2)
                    print('   ⚠️ 可复制性已牺牲，要保留复制请替换以下字体后重做：')
                    for f in (missing + only_cff):
                        print('      - %s → %s' % (f, C.suggest_replacement(f)))
                    return 0
            print('   ✗ %s' % msg)

        # ---------- 第 3 步 ----------
        print('\n[第 3 步] 输出 300dpi 位图（扫描版）...')
        scan = os.path.join(work, 'scan.pdf')
        okk, msg = __import__('fix').to_raster(keep, scan, dpi=a.dpi)
        if not okk:
            C.die('位图导出失败：%s' % msg)
        shutil.move(keep, out)
        out3 = C.tag_path(out, '【扫描版】')
        shutil.move(scan, out3)
        print('   ✅ %s' % msg)
        print('\n✅ 完成（第 3 步），两份都给你：')
        print('   原生版    ：%s（可复制；先拿手机预览它，能正常显示就用这份）' % out)
        print('   【扫描版】：%s（一定能显示，但不可复制、不可搜索）' % out3)
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
