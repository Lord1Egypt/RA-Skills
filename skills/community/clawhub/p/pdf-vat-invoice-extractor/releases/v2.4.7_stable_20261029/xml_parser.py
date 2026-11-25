"""
v3.0.1 XML 解析器 - 增值税电子发票/数电票/全电发票
支持格式（v3.0.1 修复）：
  - 🆕 数电票/全电发票（国标 2023+）：<EInvoice> 根节点 + 英文字段名
    - SellerInformation/BuyerInformation（嵌套）
    - BasicInformation（含 TotalAm*、IssueTime 等）
    - IssuItemInformation（项目明细）
    - TaxSupervisionInfo（发票号、IssueTime）
  - 老版电子发票：<Kp>/<发票> 根节点 + 中文字段名
  - 增值税电子普票 XML（兼容）
"""
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

# v3.0.1 字段映射：兼容多版本命名空间 + 中英文字段名
# 数电票/全电发票字段（国标 2023+ 标准）
NEW_FIELDS = {
    'invoice_number': ['InvoiceNumber'],  # 在 TaxSupervisionInfo 下
    'date':          ['IssueTime'],  # 在 TaxSupervisionInfo 下
    'amount':        ['TotalAmWithoutTax'],
    'tax_amount':    ['TotalTaxAm'],
    'total':         ['TotalTax-includedAmount', 'TotalTaxincludedAmount'],
    'seller_name':   ['SellerName'],
    'seller_tax_id': ['SellerIdNum'],
    'seller_addr':   ['SellerAddr'],
    'seller_tel':    ['SellerTelNum'],
    'seller_bank':   ['SellerBankName', 'SellerBankAccNum'],
    'buyer_name':    ['BuyerName'],
    'buyer_tax_id':  ['BuyerIdNum'],
    'buyer_tel':     ['BuyerTelNum'],
    'item_name':     ['ItemName'],
    'tax_rate':      ['TaxRate'],
    'drawer':        ['Drawer'],
    'request_time':  ['RequestTime'],
    'tax_bureau':    ['TaxBureauName'],
    'invoice_type':  ['GeneralOrSpecialVAT/LabelName', 'EInvoiceType/LabelName'],
}

# 老版电子发票字段
OLD_FIELDS = {
    'invoice_number': ['发票号码', 'Fphm', 'fpdm_fphm', 'Fpdm'],
    'date':          ['开票日期', 'Kprq', 'kprq'],
    'amount':        ['金额（不含税）', 'Hjje', 'hjje', '合计金额'],
    'tax_amount':    ['税额', 'Hjse', 'hjse', '合计税额'],
    'total':         ['价税合计', 'Jshj', 'jshj', '含税合计'],
    'tax_rate':      ['税率', 'Slv', 'slv'],
    'seller_name':   ['销售方名称', 'Xsfmc', 'xsf_mc'],
    'seller_tax_id': ['销售方纳税人识别号', 'Xsfnsrsbh', 'xsf_nsrsbh'],
    'buyer_name':    ['购买方名称', 'Gmfmc', 'gmf_mc'],
    'buyer_tax_id':  ['购买方纳税人识别号', 'Gmfnsrsbh', 'gmf_nsrsbh'],
    'item_name':     ['项目名称', 'Xmmc', 'xmmc'],
    'remark':        ['备注', 'Bz', 'bz'],
}

def _strip_ns(tag: str) -> str:
    """去掉 XML 命名空间（如 '{http://...}name' → 'name'）"""
    return tag.split('}')[-1] if '}' in tag else tag

def _find_by_tag(elem, tag_names: list) -> str:
    """在 elem 子树中查找指定 tag 名的第一个非空 text"""
    for cand in tag_names:
        for e in elem.iter():
            if _strip_ns(e.tag) == cand and e.text and e.text.strip():
                return e.text.strip()
    return ''

def _find_in_children(elem, tag_name: str) -> str:
    """在 elem 直接子节点中查找指定 tag"""
    for child in elem:
        if _strip_ns(child.tag) == tag_name and child.text:
            return child.text.strip()
    return ''

def _parse_rate(rate_str: str) -> str:
    """把数字型税率（0.06、6% 等）转成统一格式 '6%'"""
    if not rate_str:
        return ''
    rate_str = rate_str.strip()
    if rate_str in ('免税', '不征税', '出口零税', '零税率'):
        return rate_str
    if '%' in rate_str:
        return rate_str
    try:
        rate = float(rate_str)
        if rate < 1:  # 0.06 → 6%
            rate = rate * 100
        if rate == int(rate):
            return f"{int(rate)}%"
        return f"{rate:g}%"
    except (ValueError, TypeError):
        return rate_str

def _normalize_date(d: str) -> str:
    """日期格式统一为 YYYY-MM-DD"""
    if not d:
        return ''
    d = d.strip()
    # yyyy-MM-dd HH:MM:SS
    m = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', d)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # yyyy年MM月dd日
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', d)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # yyyy/MM/dd
    m = re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})', d)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    # yyyyMMdd
    m = re.match(r'(\d{4})(\d{2})(\d{2})', d)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return d

def _parse_amount(v) -> float:
    if v is None:
        return 0.0
    s = str(v).replace(',', '').replace('¥', '').strip()
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0

def _find_field_with_fallback(elem, new_paths: list, old_paths: list) -> str:
    """先尝试新版本字段名，找不到再用老版本"""
    val = _find_by_tag(elem, new_paths)
    if not val:
        val = _find_by_tag(elem, old_paths)
    return val

def _extract_invoice_new_format(root) -> Optional[Dict]:
    """
    v3.0.1 新增：数电票/全电发票真实结构
    根节点: <EInvoice>
    """
    inv = {}
    # 发票号：在 TaxSupervisionInfo 下
    tax_info = None
    for e in root.iter():
        if _strip_ns(e.tag) == 'TaxSupervisionInfo':
            tax_info = e
            break
    if tax_info is not None:
        inv['invoice_number'] = _find_in_children(tax_info, 'InvoiceNumber')
        issue_time = _find_in_children(tax_info, 'IssueTime')
        inv['date'] = _normalize_date(issue_time)
        inv['tax_bureau'] = _find_in_children(tax_info, 'TaxBureauName')
    # 销售方：SellerInformation
    for e in root.iter():
        if _strip_ns(e.tag) == 'SellerInformation':
            inv['seller_name']   = _find_in_children(e, 'SellerName')
            inv['seller_tax_id'] = _find_in_children(e, 'SellerIdNum')
            inv['seller_addr']   = _find_in_children(e, 'SellerAddr')
            inv['seller_tel']    = _find_in_children(e, 'SellerTelNum')
            inv['seller_bank']   = _find_in_children(e, 'SellerBankName') + ' ' + _find_in_children(e, 'SellerBankAccNum')
            break
    # 购买方：BuyerInformation
    for e in root.iter():
        if _strip_ns(e.tag) == 'BuyerInformation':
            inv['buyer_name']   = _find_in_children(e, 'BuyerName')
            inv['buyer_tax_id'] = _find_in_children(e, 'BuyerIdNum')
            inv['buyer_tel']    = _find_in_children(e, 'BuyerTelNum')
            break
    # 基本信息：BasicInformation
    for e in root.iter():
        if _strip_ns(e.tag) == 'BasicInformation':
            inv['amount']     = _parse_amount(_find_in_children(e, 'TotalAmWithoutTax'))
            inv['tax_amount'] = _parse_amount(_find_in_children(e, 'TotalTaxAm'))
            inv['total']      = _parse_amount(_find_in_children(e, 'TotalTax-includedAmount'))
            inv['drawer']     = _find_in_children(e, 'Drawer')
            inv['request_time'] = _find_in_children(e, 'RequestTime')
            break
    # 项目信息：IssuItemInformation
    items = []
    for e in root.iter():
        if _strip_ns(e.tag) == 'IssuItemInformation':
            item = {
                'name':     _find_in_children(e, 'ItemName'),
                'quantity': _find_in_children(e, 'Quantity'),
                'price':    _parse_amount(_find_in_children(e, 'UnPrice')),
                'amount':   _parse_amount(_find_in_children(e, 'Amount')),
                'tax_rate': _parse_rate(_find_in_children(e, 'TaxRate')),
                'tax':      _parse_amount(_find_in_children(e, 'ComTaxAm')),
                'total':    _parse_amount(_find_in_children(e, 'TotaltaxIncludedAmount')),
                'code':     _find_in_children(e, 'TaxClassificationCode'),
            }
            items.append(item)
    if items:
        inv['item_name'] = '|'.join(i['name'] for i in items if i['name'])
        inv['items_detail'] = items
        inv['tax_rate'] = items[0]['tax_rate']  # 用第一项的税率
    return inv

def _extract_invoice_old_format(root) -> Optional[Dict]:
    """v3.0 兼容：老版中文字段格式"""
    inv = {}
    for key, candidates in OLD_FIELDS.items():
        val = _find_by_tag(root, candidates)
        if val:
            inv[key] = val
    if not (inv.get('invoice_number') or inv.get('date')):
        return None
    return inv

def parse_xml_invoice(xml_path: str) -> List[Dict]:
    """解析 XML 格式发票（v3.0.1 升级）"""
    invoices = []
    try:
        if zipfile.is_zipfile(xml_path):
            with zipfile.ZipFile(xml_path, 'r') as z:
                xml_files = [n for n in z.namelist() if n.lower().endswith('.xml')]
                for xml_name in xml_files:
                    with z.open(xml_name) as f:
                        try:
                            tree = ET.parse(f)
                            root = tree.getroot()
                            inv = _detect_and_extract(root)
                            if inv:
                                invoices.append(inv)
                        except ET.ParseError:
                            continue
        else:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            inv = _detect_and_extract(root)
            if inv:
                invoices.append(inv)
    except Exception as e:
        print(f'  ⚠️ XML 解析失败: {e}')
    # 标准化所有字段
    for inv in invoices:
        if 'date' in inv:
            inv['date'] = _normalize_date(inv['date'])
        if 'tax_rate' in inv:
            inv['tax_rate'] = _parse_rate(inv['tax_rate'])
        for k in ('amount', 'tax_amount', 'total'):
            if k in inv:
                inv[k] = _parse_amount(inv[k])
        inv['source_format'] = 'XML'
    return invoices

def _detect_and_extract(root) -> Optional[Dict]:
    """根据根节点自动判断新/老格式"""
    root_tag = _strip_ns(root.tag)
    if root_tag == 'EInvoice':
        # 数电票/全电发票新格式
        inv = _extract_invoice_new_format(root)
        # 检查关键字段
        if not (inv.get('invoice_number') or inv.get('seller_name') or inv.get('buyer_name')):
            # 兜底：尝试老格式解析
            inv = _extract_invoice_old_format(root)
        return inv if inv and (inv.get('invoice_number') or inv.get('seller_name')) else None
    else:
        # 老格式（<Kp>、<发票>、<eInvoice>等）
        return _extract_invoice_old_format(root)
