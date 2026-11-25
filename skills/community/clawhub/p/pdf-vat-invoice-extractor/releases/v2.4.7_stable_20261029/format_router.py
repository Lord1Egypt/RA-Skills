#!/usr/bin/env python3
"""
pdf-invoice-stat v2.4.5 · 多格式路由器

设计原则（严格保证不影响 PDF）：
1. invoice_extractor.py（PDF 主路径）**零改动**，本模块只做"转发"
2. XML/OFD 解析结果经字段映射后，交给 v2.4.0 原版 create_excel() 输出
3. 表头（15 列）、样式（D9D9D9 灰表头 / A2 冻结 / 数字格式）由 create_excel() 独占
   本模块**不写任何 Excel 样式代码**，因此三种格式输出必然一致

支持格式：
- PDF   → invoice_extractor.extract_all_invoices（原版，零改动）
- XML   → xml_parser.parse_xml_invoice（数电票/全电发票，含 ZIP 自解包）
- OFD   → ofd_parser.parse_ofd_invoice（国标 GB/T 33190）
- ZIP   → 解包后递归路由（内含 PDF/XML/OFD 均支持）
- RAR   → unar 解包后递归路由（需 unar，brew install unar）
"""
import os
import re
import sys
import zipfile
import tempfile
import shutil
import subprocess

__version__ = '2.4.5'

# ============================================================
# 字段映射：XML/OFD 英文 key → v2.4.0 create_excel 需要的中文 key
# （依据 xml_parser.py / ofd_parser.py 实测输出，非猜测）
# ============================================================
FIELD_MAP = {
    'invoice_number': '发票号码',
    'date':           '开票日期',
    'buyer_name':     '购买方信息-名称',
    'buyer_tax_id':   '购买方信息-统一社会信用代码',
    'seller_name':    '销售方信息-名称',
    'seller_tax_id':  '销售方信息-统一社会信用代码',
    'item_name':      '项目名称',
    'amount':         '金额',
    'tax_rate':       '税率/征收率',
    'tax_amount':     '税额',
    'total':          '价税合计',
    'remark':         '备注',
}

# create_excel() 会访问的全部 key（缺一个就 KeyError，必须全填）
V240_REQUIRED = {
    '发票号码': '',
    '开票日期': '',
    '购买方信息-名称': '',
    '购买方信息-统一社会信用代码': '',
    '销售方信息-名称': '',
    '销售方信息-统一社会信用代码': '',
    '项目名称': '',
    '金额': 0.0,
    '税率/征收率': '',
    '税额': 0.0,
    '价税合计': 0.0,
    '备注': '',
}

_NUMERIC = {'金额', '税额', '价税合计'}


def to_v240(raw: dict) -> dict:
    """XML/OFD 英文字段 → v2.4.0 中文字段（含缺失兜底，绝不 KeyError）"""
    out = dict(V240_REQUIRED)
    for en, cn in FIELD_MAP.items():
        if en not in raw:
            continue
        val = raw[en]
        if val is None:
            continue
        if cn in _NUMERIC:
            out[cn] = _safe_float(val)
        else:
            out[cn] = str(val).strip()
    # 金额为 0 但有税额/合计时兜底（部分 OFD 只给合计）
    if not out['价税合计']:
        out['价税合计'] = round(out['金额'] + out['税额'], 2)
    if not out['金额']:
        out['金额'] = round(out['价税合计'] - out['税额'], 2)
    return out


def _safe_float(v) -> float:
    """安全转 float（处理 '1,234.56' / '¥88.00' / '***' / '' / None）"""
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return 0.0
    s = str(v).strip().replace(',', '').replace('¥', '').replace('￥', '')
    if s in ('', '-', '*', '***', 'null', 'None'):
        return 0.0
    m = re.search(r'[-+]?\d*\.?\d+', s)
    return float(m.group()) if m else 0.0


# ============================================================
# 格式识别
# ============================================================
def detect_format(path: str) -> str:
    """按内容 + 扩展名判定格式（内容优先，扩展名兜底）"""
    ext = os.path.splitext(path)[1].lower().lstrip('.')

    # ZIP/OFD 魔数
    try:
        with open(path, 'rb') as f:
            magic = f.read(8)
        if magic[:4] == b'PK\x03\x04':
            # ZIP：看内部是否有 OFD_EntryDocument.xml
            if _zip_has_ofd(path):
                return 'OFD'
            return 'ZIP'
    except Exception:
        pass

    if ext == 'rar' or magic[:4] == b'Rar!':
        return 'RAR'

    if ext == 'pdf' or magic[:5] == b'%PDF-':
        return 'PDF'
    if ext == 'xml':
        return 'XML'
    if ext == 'ofd':
        return 'OFD'
    return ext.upper() or 'UNKNOWN'


def _zip_has_ofd(path: str) -> bool:
    """
    判断 ZIP 是否为 OFD（国标版式发票）

    实测发现两种入口文件名：
      1. 标准国标: OFD_EntryDocument.xml
      2. 实际税局: OFD.xml   ← 本次测试文件就是这个
    另外用 Doc_0/Document.xml + Pages/Content.xml 作为兜底特征
    """
    try:
        with zipfile.ZipFile(path, 'r') as z:
            names = z.namelist()
            lows = [n.lower() for n in names]
            # 特征 1: 标准 OFD 入口
            if any('ofd_entrydocument' in n for n in lows):
                return True
            # 特征 2: 税局实际用的 OFD.xml（根目录或一层）
            for n in lows:
                base = os.path.basename(n)
                if base == 'ofd.xml':
                    return True
            # 特征 3: OFD 文档结构（Doc_*/Document.xml + Content.xml + 字体/图片资源）
            has_doc = any(n.startswith('doc_') and n.endswith('/document.xml') for n in lows)
            has_content = any('content.xml' in n for n in lows)
            has_res = any(('/res/' in n) or n.endswith('.ttf') for n in lows)
            if has_doc and has_content and has_res:
                return True
    except Exception:
        pass
    return False


def magic_prefix(path: str, n: int = 8) -> bytes:
    try:
        with open(path, 'rb') as f:
            return f.read(n)
    except Exception:
        return b''


# ============================================================
# ZIP / RAR 解包
# ============================================================
def extract_archive(path: str, workdir: str) -> list:
    """解包 ZIP/RAR，返回解压后的文件路径列表"""
    fmt = detect_format(path)
    files = []

    if fmt == 'ZIP':
        try:
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall(workdir)
            for root, _dirs, names in os.walk(workdir):
                for n in names:
                    files.append(os.path.join(root, n))
        except Exception as e:
            print(f'  ⚠️  ZIP 解包失败: {e}')

    elif fmt == 'RAR':
        unar = shutil.which('unar')
        if not unar:
            print('  ⚠️  RAR 需要 unar（brew install unar），已跳过')
            return []
        try:
            subprocess.run(
                [unar, '-quiet', '-force-overwrite', '-no-directory',
                 '-output-directory', workdir, path],
                capture_output=True, timeout=120
            )
            for root, _dirs, names in os.walk(workdir):
                for n in names:
                    files.append(os.path.join(root, n))
        except Exception as e:
            print(f'  ⚠️  RAR 解包失败: {e}')

    return files


# ============================================================
# 统一入口
# ============================================================
def extract_invoices(path: str) -> list:
    """
    统一入口：自动路由 PDF / XML / OFD / ZIP / RAR
    返回 v2.4.0 中文字段格式的 dict 列表
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    fmt = detect_format(path)

    if fmt == 'PDF':
        # PDF 走 v2.4.4 原版，零改动
        from invoice_extractor import extract_all_invoices
        return extract_all_invoices(path)

    if fmt == 'XML':
        import xml_parser
        raw = xml_parser.parse_xml_invoice(path)
        return [to_v240(r) for r in raw]

    if fmt == 'OFD':
        import ofd_parser
        raw = ofd_parser.parse_ofd_invoice(path)
        return [to_v240(r) for r in raw]

    if fmt in ('ZIP', 'RAR'):
        invoices = []
        tmp = tempfile.mkdtemp(prefix='inv_archive_')
        try:
            for f in extract_archive(path, tmp):
                sub = detect_format(f)
                if sub in ('PDF', 'XML', 'OFD'):
                    invoices.extend(extract_invoices(f))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return invoices

    print(f'  ⚠️ 不支持的格式: {fmt}')
    return []


def extract_folder(folder: str, recursive: bool = True) -> list:
    """批量处理目录内所有发票文件，返回合并列表（含 _source_file）"""
    invoices = []
    supported = ('.pdf', '.xml', '.ofd', '.zip', '.rar')
    for root, _dirs, names in os.walk(folder):
        for n in sorted(names):
            if not n.lower().endswith(supported):
                continue
            f = os.path.join(root, n)
            try:
                got = extract_invoices(f)
                for inv in got:
                    inv['_source_file'] = n
                invoices.extend(got)
            except Exception as e:
                print(f'  ⚠️ {n}: {e}')
        if not recursive:
            break
    return invoices


def create_excel_any(invoices: list, output_path: str) -> str:
    """
    输出 Excel —— 直接复用 v2.4.0 原版 create_excel()
    表头/样式因此与 PDF 输出 100% 一致
    """
    from invoice_extractor import create_excel, detect_duplicates
    create_excel(invoices, detect_duplicates(invoices), output_path)
    return output_path


if __name__ == '__main__':
    import sys as _s
    if len(_s.argv) < 2:
        print('用法: python3 format_router.py <文件或目录> [输出.xlsx]')
        _s.exit(1)
    target = _s.argv[1]
    out = _s.argv[2] if len(_s.argv) > 2 else (
        target if os.path.isdir(target)
        else os.path.splitext(target)[0] + '_发票统计.xlsx')

    if os.path.isdir(target):
        invs = extract_folder(target)
    else:
        fmt = detect_format(target)
        print(f'格式: {fmt}')
        invs = extract_invoices(target)
        for i in invs:
            i['_source_file'] = os.path.basename(target)

    print(f'识别 {len(invs)} 张发票')
    if invs:
        create_excel_any(invs, out)
        print(f'✅ 已输出: {out}')
