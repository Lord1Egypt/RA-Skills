#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-font-fixer · structcheck —— 字体「字典结构」校验（渲染结果之外的第二道体检）

为什么需要它
------------------------------
detect/verify 回答的是「**能不能渲染出字形**」，判据是轮廓格式（TrueType/CFF）与逐字归属。
但还有一类病，字形完全画得出来、在电脑和 pymupdf 里都正常，**打印机却拒收**：

    简单 TrueType 字体 + /Flags 含 Symbolic(4) + 单字节伪编码 + 缺 /Encoding

这是 python-docx → LibreOffice 这条链路的典型产物（docx 里中文 run 没写 w:eastAsia，
LibreOffice 就把中文字体当「符号字体」导出）：
/FirstChar 0、/LastChar 3、/Widths 全 1000、正文只有 <010203> 这样的单字节码，
全靠 /ToUnicode 反查才认得出汉字。

后果是分层的：
  · Adobe / 系统预览 / WPS / pymupdf —— 靠 ToUnicode 容错，看着一切正常
  · 佳能 PRINT、惠普老固件这类精简 RIP —— 解析字体字典失败，直接拒收整个文件
    （佳能的提示是「未导入太大的图像或格式不受支持的文件」，与图像无关，是通用兜底文案）

所以「渲染能通过」不等于「能打印」。本模块只做结构判断，不渲染。

判定要点（避免误报）
------------------------------
1. **CID 字体（Type0 + CIDFontType2/CIDFontType0）标 Symbolic 是正常做法**，
   中文 PDF 大量如此（Chrome 导出即是）。所以不按 Flags 单独判，必须结合 /Subtype。
2. 真正可疑的是**简单字体**（/Subtype /TrueType、/Type1）：
   Flags 含 Symbolic + ToUnicode 里出现 CJK → 判 BAD（伪符号化中文字体）。
3. 简单字体 /FirstChar ≤ 31、/Encoding 缺失、/Widths 全同值 → 各自记 WARN。

另附 RIP 兼容性检查（Tagged 结构树、trailer 私有键），只作提示不拦交付。

用法
----
  python3 structcheck.py 文件.pdf
  python3 structcheck.py 文件.pdf --json

退出码：0 = 无 BAD 级问题；2 = 存在 BAD 级问题；1 = 无法检查
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _deps          # 持久依赖：环境重置后自动从持久目录补齐
_deps.activate()

try:
    import pikepdf
    HAS_PIKEPDF = True
except ImportError:                                     # pragma: no cover
    pikepdf = None
    HAS_PIKEPDF = False

# 标准 trailer 键，其余视为私有扩展
STD_TRAILER = {'/Size', '/Root', '/Info', '/ID', '/Prev', '/Encrypt', '/XRefStm',
               '/DecodeParms', '/Filter', '/Index', '/W', '/Length', '/Type'}

CJK_RANGES = ((0x2E80, 0x9FFF), (0xF900, 0xFAFF), (0xFE30, 0xFE4F),
              (0xFF00, 0xFFEF), (0x20000, 0x3FFFF))


def _is_cjk(cp):
    for lo, hi in CJK_RANGES:
        if lo <= cp <= hi:
            return True
    return False


def _parse_tounicode(font):
    """解析 /ToUnicode CMap，返回 (code→unicode dict, 是否含 CJK)。"""
    try:
        tu = font.get('/ToUnicode')
        if tu is None:
            return {}, False
        data = bytes(tu.read_bytes()).decode('latin-1', 'replace')
    except Exception:
        return {}, False

    mapping = {}
    # bfchar 段：<src> <dst> 成对
    for block in re.findall(r'beginbfchar(.*?)endbfchar', data, re.S):
        for src, dst in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', block):
            try:
                mapping[int(src, 16)] = int(dst[:4].ljust(4, '0'), 16)
            except Exception:
                pass
    # bfrange 段：<lo> <hi> <dst> 或 <lo> <hi> [<d1> <d2> ...]
    for block in re.findall(r'beginbfrange(.*?)endbfrange', data, re.S):
        for lo, hi, rest in re.findall(
                r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(<[0-9A-Fa-f]+>|\[[^\]]*\])', block):
            try:
                lo_i, hi_i = int(lo, 16), int(hi, 16)
            except Exception:
                continue
            if rest.startswith('['):
                items = re.findall(r'<([0-9A-Fa-f]+)>', rest)
                for k, d in enumerate(items):
                    mapping[lo_i + k] = int(d[:4].ljust(4, '0'), 16)
            else:
                base = int(rest.strip('<>'), 16)
                for k in range(hi_i - lo_i + 1):
                    mapping[lo_i + k] = base + k

    has_cjk = any(_is_cjk(cp) for cp in mapping.values())
    return mapping, has_cjk


def _widths_uniform(font):
    """判断 /Widths 是否全同值（假宽度特征）。"""
    try:
        w = font.get('/Widths')
        if w is None:
            return False
        vals = [int(x) for x in w]
        return len(vals) > 1 and len(set(vals)) == 1
    except Exception:
        return False


def _inspect_font(font, name_hint=''):
    """单个字体字典的结构体检，返回 (rec, issues)。"""
    rec = dict(name=name_hint, subtype='', symbolic=False, first_char=None,
               encoding=None, widths_uniform=False, cjk_in_tounicode=False,
               cid_keyed=False)
    issues = []

    try:
        rec['subtype'] = str(font.get('/Subtype') or '')
    except Exception:
        pass

    # Type0 → 取后代字体再读描述符
    target = font
    try:
        if rec['subtype'] == '/Type0':
            df = font.get('/DescendantFonts')
            if df is not None and len(df):
                target = df[0]
                rec['cid_keyed'] = True
                rec['subtype'] = str(target.get('/Subtype') or rec['subtype'])
    except Exception:
        pass

    # 优先用 BaseFont（/F1 这类资源名对用户没意义）
    try:
        bf = target.get('/BaseFont') or font.get('/BaseFont')
        if bf is not None:
            rec['name'] = str(bf)
    except Exception:
        pass
    rec['name'] = rec['name'] or name_hint or '?'

    # Flags（在 FontDescriptor 里）
    try:
        fd = target.get('/FontDescriptor')
        if fd is not None:
            flags = int(fd.get('/Flags', 0))
            rec['symbolic'] = bool(flags & 4)
            rec['flags'] = flags
    except Exception:
        pass

    # 简单字体特有的字段
    if not rec['cid_keyed']:
        try:
            fc = font.get('/FirstChar')
            rec['first_char'] = int(fc) if fc is not None else None
        except Exception:
            pass
        try:
            enc = font.get('/Encoding')
            rec['encoding'] = str(enc) if enc is not None else None
        except Exception:
            pass
        rec['widths_uniform'] = _widths_uniform(font)

    # ToUnicode 里承载的是不是中文
    mapping, has_cjk = _parse_tounicode(font)
    if not mapping and not rec['cid_keyed']:
        mapping, has_cjk = _parse_tounicode(target)
    rec['cjk_in_tounicode'] = has_cjk
    rec['code_count'] = len(mapping)

    # ---- 判定 ----
    # ① 伪符号化的简单中文字体：打印机 RIP 高频拒收
    if (not rec['cid_keyed']
            and rec['subtype'] in ('/TrueType', '/Type1', '/MMType1')
            and rec['symbolic'] and rec['cjk_in_tounicode']):
        issues.append(dict(level='bad', code='symbolic_cjk',
                           msg='简单 TrueType 中文字体被标为 Symbolic（伪符号字体）'))

    # ② 简单字体字符码从 0 起
    if (not rec['cid_keyed'] and rec['first_char'] is not None
            and rec['first_char'] < 32):
        issues.append(dict(level='warn', code='first_char_low',
                           msg='/FirstChar = %d（规范建议 ≥32，字符码落入保留区）'
                               % rec['first_char']))

    # ③ 简单字体缺 /Encoding，全凭 ToUnicode 撑
    if (not rec['cid_keyed'] and rec['encoding'] is None
            and rec['cjk_in_tounicode']):
        issues.append(dict(level='warn', code='encoding_missing',
                           msg='缺 /Encoding，字形映射只靠 /ToUnicode（渲染器忽略它即全盘失效）'))

    # ④ 假宽度（等宽字体 Widths 全同值合法：查 Flags bit0 与字体名）
    _nm = (rec['name'] or '').lower().replace(' ', '').split('+')[-1]
    _mono = any(k in _nm for k in ('mono', 'courier', 'typewriter', 'fixed', 'nimbusmon'))
    if rec['widths_uniform'] and not (rec.get('flags', 0) & 1) and not _mono:
        issues.append(dict(level='warn', code='widths_uniform',
                           msg='/Widths 全为同一值（占位假宽度，字距靠 TJ 硬凑）'))

    # ⑤ 码位数远少于实际用字（复用度异常）
    if rec['code_count'] and rec['cjk_in_tounicode'] and rec['code_count'] < 8 \
            and not rec['cid_keyed']:
        issues.append(dict(level='warn', code='few_codes',
                           msg='整段中文只占 %d 个字符码（码位高度复用）' % rec['code_count']))
    return rec, issues


def inspect_structure(path):
    """整体结构体检。返回 dict(fonts, page, issues, verdict)。"""
    if not HAS_PIKEPDF:
        return dict(path=path, fonts=[], issues=[], bad=[], verdict='pass',
                    page={}, skipped='未安装 pikepdf，跳过结构校验')
    pdf = pikepdf.open(path)
    fonts, font_issues = [], []
    seen = set()

    for page in pdf.pages:
        try:
            fres = (page.get('/Resources') or {}).get('/Font')
        except Exception:
            continue
        if fres is None:
            continue
        for key, font in fres.items():
            try:
                oid = font.objgen
            except Exception:
                oid = None
            if oid in seen:
                continue
            seen.add(oid)
            try:
                rec, iss = _inspect_font(font, name_hint=str(key))
            except Exception:
                continue
            fonts.append(rec)
            for i in iss:
                i['font'] = rec['name']
            font_issues.extend(iss)

    # ---- RIP 兼容性（提示项，不拦交付）----
    page_info = dict(version=str(pdf.pdf_version), tagged=False,
                     struct_tree=False, private_trailer=[])
    rip_issues = []
    try:
        root = pdf.Root
        page_info['struct_tree'] = '/StructTreeRoot' in root
        page_info['tagged'] = '/MarkInfo' in root or page_info['struct_tree']
        if page_info['tagged']:
            rip_issues.append(dict(level='info', code='tagged',
                                   msg='带 Tagged 结构树（老固件 RIP 兼容性偏弱，可去除）'))
    except Exception:
        pass
    try:
        for k in pdf.trailer.keys():
            if k not in STD_TRAILER:
                page_info['private_trailer'].append(k)
        if page_info['private_trailer']:
            rip_issues.append(dict(level='info', code='private_trailer',
                                   msg='trailer 含非标准键 %s（多为导出器私有，部分 RIP 不容忍）'
                                       % ' '.join(page_info['private_trailer'])))
    except Exception:
        pass

    issues = font_issues + rip_issues
    bad = [i for i in issues if i['level'] == 'bad']
    pdf.close()
    return dict(path=path, fonts=fonts, page=page_info, issues=issues,
                bad=bad, verdict='fail' if bad else 'pass')


def report(res):
    if not res['fonts']:
        print('  （未发现任何字体字典）')
        return
    for rec in res['fonts']:
        marks = []
        if rec.get('symbolic'):
            marks.append('Symbolic')
        if rec.get('first_char') is not None and rec['first_char'] < 32:
            marks.append('FirstChar=%d' % rec['first_char'])
        if rec.get('widths_uniform'):
            marks.append('假宽度')
        if rec.get('encoding') is None and not rec.get('cid_keyed'):
            marks.append('无Encoding')
        tag = (' ⚠️ ' + ' / '.join(marks)) if marks else ''
        print('  [结构] %-32s %-16s%s' % (rec['name'][:32], rec['subtype'], tag))
    if res['issues']:
        print('\n  结构问题：')
        for i in res['issues']:
            icon = {'bad': '❌', 'warn': '⚠️', 'info': 'ℹ️'}[i['level']]
            owner = ('  ← %s' % i['font']) if i.get('font') else ''
            print('   %s %s%s' % (icon, i['msg'], owner))


def main():
    ap = argparse.ArgumentParser(description='PDF 字体字典结构校验')
    ap.add_argument('pdf')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    if not os.path.isfile(a.pdf):
        print('[X] 文件不存在：%s' % a.pdf, file=sys.stderr)
        return 1
    try:
        res = inspect_structure(a.pdf)
    except Exception as e:
        print('[X] 无法检查：%s' % e, file=sys.stderr)
        return 1

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
        return 0 if res['verdict'] == 'pass' else 2

    if not a.quiet:
        print('\n结构体检：%s' % a.pdf)
        report(res)
    if res['verdict'] == 'pass':
        print('\n✅ 字体字典结构正常。')
        return 0
    print('\n❌ 字体字典结构异常：%d 项会让打印机/精简 RIP 直接拒收。' % len(res['bad']))
    print('   修复：python3 scripts/fix.py %s' % a.pdf)
    return 2


if __name__ == '__main__':
    sys.exit(main())
