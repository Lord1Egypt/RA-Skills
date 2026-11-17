"""
v3.0.3 OFD 解析器 - 国标 GB/T 33190（真实税务文件结构）
关键改进：金额字段不再依赖"合 计"行（真实 OFD 没有）
策略：按数据类型特征识别 + 业务逻辑校验
  - 不含税金额 = min(所有金额)
  - 税额 = 介于中间的金额
  - 价税合计 = max(所有金额)
"""
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

def parse_ofd_invoice(ofd_path: str) -> List[Dict]:
    """解析 OFD 格式发票"""
    if not zipfile.is_zipfile(ofd_path):
        return []
    invoices = []
    try:
        with zipfile.ZipFile(ofd_path, 'r') as z:
            all_text = _extract_all_text(z)
            if not all_text.strip():
                return []
            inv = _smart_parse(all_text)
            if inv:
                inv['source_format'] = 'OFD'
                invoices.append(inv)
    except Exception as e:
        print(f'  ⚠️ OFD 解析失败: {e}')
    return invoices

def _extract_all_text(zip_handle) -> str:
    """提取所有 ofd:TextCode 文本（用换行分隔）"""
    parts = []
    for xml_name in zip_handle.namelist():
        if not xml_name.lower().endswith('.xml'):
            continue
        try:
            with zip_handle.open(xml_name) as f:
                content = f.read().decode('utf-8', errors='ignore')
                for pattern in [
                    r'<ofd:TextCode[^>]*>([^<]+)</ofd:TextCode>',
                    r'<TextCode[^>]*>([^<]+)</TextCode>',
                ]:
                    for m in re.finditer(pattern, content):
                        t = m.group(1).strip()
                        if t and not _is_template_label(t) and not _is_coordinate(t):
                            parts.append(t)
        except ET.ParseError:
            continue
    return '\n'.join(parts)

def _is_template_label(text: str) -> bool:
    template_labels = {'发票号码', '开票日期', '项目名称', '规格型号', '单位', '数量',
                      '单价', '金额', '税率', '税额', '价税合计', '开票人',
                      '名称', '统一社会信用代码', '纳税人识别号', '小写', '大写',
                      '开票', '复核', '收款', '电子'}
    # 只过滤完全等于模板标签的（不一定 rstrip，因为"6%" 不是模板）
    return text.rstrip('：:') in template_labels

def _is_coordinate(text: str) -> bool:
    """是否为坐标数据（如 '0 0 210 140' 或 'M 0.254 0.254'）"""
    # 必须包含空格（多组数字），且不含纯小数
    if ' ' not in text:
        return False
    # 排除纯小数金额（如 83.02 不算坐标）
    if re.fullmatch(r'\d+\.\d+', text):
        return False
    # 包含 M/L/Z 等路径命令
    if any(c in text for c in 'MLZmlz'):
        return True
    # 多组数字用空格分隔
    parts = text.split()
    if len(parts) >= 2 and all(re.fullmatch(r'[\d\.]+', p) for p in parts):
        return True
    return False

def _extract_money_values(lines: List[str]) -> List[float]:
    """提取所有金额数字"""
    nums = []
    for line in lines:
        for m in re.finditer(r'([0-9]+\.\d{2})', line):
            try:
                v = float(m.group(1))
                if 0.01 <= v <= 100000000:
                    nums.append(v)
            except ValueError:
                pass
    return nums

def _smart_parse(text: str) -> Optional[Dict]:
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    inv = {}
    inv['invoice_number'] = _find_invoice_number(lines)
    inv['date'] = _find_date(lines)
    # 真实 OFD 文本顺序：购买方在前、销售方在后
    # 同时用行业特征辅助判断：餐饮/酒店/餐厅/超市 → 销售方；咨询/管理/科技 → 购买方
    first_company, first_tax = _find_company_and_tax_id(lines, 'first')
    last_company, last_tax = _find_company_and_tax_id(lines, 'last')
    if _is_likely_seller(last_company):
        inv['seller_name'], inv['seller_tax_id'] = last_company, last_tax
        inv['buyer_name'], inv['buyer_tax_id'] = first_company, first_tax
    elif _is_likely_seller(first_company):
        inv['seller_name'], inv['seller_tax_id'] = first_company, first_tax
        inv['buyer_name'], inv['buyer_tax_id'] = last_company, last_tax
    else:
        # 兜底：按 OFD 标准布局（买方在前）
        inv['buyer_name'], inv['buyer_tax_id'] = first_company, first_tax
        inv['seller_name'], inv['seller_tax_id'] = last_company, last_tax
    inv['item_name'] = _find_item_name(lines)
    inv['tax_rate'] = _find_tax_rate(lines)
    inv['drawer'] = _find_drawer(lines)
    inv['total_chinese'] = _find_total_chinese(lines)
    # 金额：使用业务逻辑（amount < tax < total）
    money_values = _extract_money_values(lines)
    inv['amount'], inv['tax_amount'], inv['total'] = _split_amounts(money_values, inv.get('tax_rate', ''))
    if not (inv.get('invoice_number') or inv.get('date')):
        return None
    return inv

def _find_invoice_number(lines: List[str]) -> str:
    for line in lines:
        if re.fullmatch(r'\d{20}', line):
            return line
    for line in lines:
        if re.fullmatch(r'\d{15,25}', line):
            return line
    return ''

def _find_date(lines: List[str]) -> str:
    for line in lines:
        if '年' in line and '月' in line and '日' in line:
            m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', line)
            if m:
                return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return ''

def _find_company_and_tax_id(lines: List[str], position: str) -> tuple:
    """position: 'first' or 'last'"""
    pairs = []
    i = 0
    while i < len(lines):
        if _is_company_name(lines[i]):
            if i + 1 < len(lines) and _is_tax_id(lines[i + 1]):
                pairs.append((lines[i], lines[i + 1]))
                i += 2
                continue
        i += 1
    if not pairs:
        return '', ''
    return pairs[0] if position == 'first' else pairs[-1]

def _is_company_name(text: str) -> bool:
    """
    判定是否为公司名称
    v2.4.6 修复：排除"标签行"（国际发票 OFD 排版会把
    「统一社会信用代码/纳税人识别号：」当成公司名，导致购方取错）
    """
    if len(text) < 4 or len(text) > 60:
        return False
    # 排除标签行 / 表头行
    label_kw = ('统一社会信用代码', '纳税人识别号', '名称：', '名称:', '名称',
                '项目名称', '规格型号', '销售方', '购买方', '购 买 方', '销 售 方',
                '开票人', '备注', '合计', '价税合计', '税率', '税额', '数量',
                '单价', '金额', '单位', '下载次数', '电子发票', '增值税')
    if any(kw in text for kw in label_kw):
        return False
    if re.search(r'公司|厂|店|中心|工作室|事务所|部|院|社|馆|坊', text):
        return True
    if re.fullmatch(r'[\u4e00-\u9fa5（）\(\)A-Za-z0-9·]{4,40}', text):
        return True
    return False

def _is_tax_id(text: str) -> bool:
    """
    判定是否为统一社会信用代码 / 纳税人识别号
    v2.4.6 修复：排除发票号码
    国内增值税发票号码是 20 位纯数字（2 开头），会被误判成税号
    统一社会信用代码是 15 位（老代码）或 18 位（当前），必含字母或数字混合
    """
    if not re.fullmatch(r'[A-Z0-9]{15,20}', text):
        return False
    # 排除 20 位纯数字（发票号码）
    if text.isdigit():
        return False
    # 统一社会信用代码：15 位或 18 位
    return len(text) in (15, 18)

def _find_item_name(lines: List[str]) -> str:
    candidates = []
    for line in lines:
        if re.search(r'服务|销售|租赁|咨询|培训|运输|工程|加工', line) and not _is_company_name(line):
            if 4 <= len(line) <= 80:
                candidates.append(line)
    return '|'.join(candidates[:3]) if candidates else ''

def _find_tax_rate(lines: List[str]) -> str:
    for line in lines:
        m = re.search(r'(\d+(?:\.\d+)?)\s*%', line)
        if m:
            return f"{m.group(1)}%"
    return ''

def _find_drawer(lines: List[str]) -> str:
    for line in lines:
        if re.fullmatch(r'[\u4e00-\u9fa5]{2,4}', line) and line not in ('开票人',):
            return line
    return ''

def _find_total_chinese(lines: List[str]) -> str:
    for line in lines:
        if ('圆整' in line or '元整' in line) and re.search(r'[\u4e00-\u9fa5]', line):
            return line
    return ''

def _is_likely_seller(company_name: str) -> bool:
    """通过公司名判断是否更可能是销售方"""
    if not company_name:
        return False
    # v2.4.6 扩充：国际/差旅发票的销方多为旅行社、航空
    seller_keywords = ['餐饮', '酒店', '餐厅', '商店', '超市', '商场', '百货',
                       '销售', '制造', '生产', '厂', '食品',
                       '旅行社', '旅游', '航空', '票务', '会展', '租车',
                       '出行', '滴滴', '通行', '高速', '物业', '通信', '联通',
                       '移动', '电信', '停车', '加油', '石油', '商贸', '批发']
    return any(kw in company_name for kw in seller_keywords)


def _split_amounts(money_values: List[float], tax_rate: str = '') -> tuple:
    """
    拆分金额 → (amount 不含税, tax 税额, total 价税合计)

    v2.4.6 修复：改用「勾稽关系 + 税率」双重校验
    ------------------------------------------------------------------
    旧版用 min/middle/max 三分法，会被「单价」干扰值打乱：
      例 [3843.39(单价), 3843.40(金额), 230.60(税额), 4074.00(合计)]
          三分法 → amount=3843.40, tax=3843.39 ❌（把单价当税额）

    新版用确定性勾稽：total = amount + tax，且 tax ≈ amount × 税率
    若有多个候选，按「税率也匹配」优先，再按 amount 大者优先
    """
    if not money_values:
        return 0.0, 0.0, 0.0
    nums = sorted(set(round(float(v), 2) for v in money_values))
    nums = [n for n in nums if n > 0]
    if not nums:
        return 0.0, 0.0, 0.0
    if len(nums) == 1:
        return 0.0, 0.0, nums[0]
    if len(nums) == 2:
        return nums[0], 0.0, nums[1]

    rate = None
    if tax_rate:
        try:
            rate = float(str(tax_rate).replace('%', '').strip()) / 100.0
        except Exception:
            rate = None

    TOL = 0.02
    candidates = []
    for a in nums:
        for t in nums:
            if t <= 0:
                continue
            c = round(a + t, 2)
            for total in nums:
                if abs(total - c) <= TOL:
                    score = 0
                    if rate is not None:
                        expect = round(a * rate, 2)
                        if abs(expect - t) <= max(0.02, abs(expect) * 0.02):
                            score = 2   # 勾稽 + 税率双匹配（最可信）
                        else:
                            score = 1   # 仅勾稽成立
                    candidates.append((score, a, t, total))
    if candidates:
        candidates.sort(key=lambda x: (-x[0], -x[1]))
        best = candidates[0]
        return best[1], best[2], best[3]

    # 兜底：老逻辑
    if len(nums) == 3:
        return nums[1], nums[0], nums[2]
    top3 = sorted(nums[-3:])
    return top3[1], top3[0], top3[2]
