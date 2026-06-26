#!/usr/bin/env python3
"""
InvoiceGuard 合规报告生成器
符合《财会便函〔2023〕18号》要求
"""

import json
import sys
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


# ─────────────────────────────────────────────────────────────────────────────
# Report Configuration
# ─────────────────────────────────────────────────────────────────────────────
REPORT_VERSION = "2.0"
GENERATOR_NAME = "InvoiceGuard 发票合规管家"

# 飞书文档默认创建位置（folder_token 可选，留空则创建在个人空间）
FEISHU_FOLDER_TOKEN = ""


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _dec(val) -> Decimal:
    """安全转换为 Decimal。"""
    try:
        return Decimal(str(val))
    except (InvalidOperation, TypeError):
        return Decimal("0")


def _fmt_currency(amount: float) -> str:
    """格式化货币为 ¥XXX,XXX.XX"""
    if amount < 0:
        return f"-¥{abs(amount):,.2f}"
    return f"¥{amount:,.2f}"


def _fmt_date(date_str: str) -> str:
    """标准化日期格式 YYYY-MM-DD"""
    if not date_str:
        return ""
    # already formatted
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        return date_str
    return date_str


def _generate_report_id() -> str:
    """生成报告编号 RPT-YYYYMMDD-XXXX"""
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    seq_part = now.strftime("%H%M%S")[-4:]
    return f"RPT-{date_part}-{seq_part}"


# ─────────────────────────────────────────────────────────────────────────────
# Invoice data structures
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class InvoiceRecord:
    invoice_code: str = ""
    invoice_no: str = ""
    invoice_type: str = ""
    date: str = ""
    amount: float = 0.0
    tax_amount: float = 0.0
    buyer_name: str = ""
    buyer_tax_id: str = ""
    seller_name: str = ""
    seller_tax_id: str = ""
    items: str = ""
    file_path: str = ""
    file_type: str = ""
    raw_text: str = ""
    status: str = "pending"   # pending / duplicate / suspicious / clean
    verify_status: str = "unchecked"  # unchecked / normal / void / red / 失控
    notes: str = ""
    fields_hash: str = ""

    def amount_decimal(self) -> Decimal:
        return _dec(self.amount)

    @classmethod
    def from_dict(cls, d: dict) -> "InvoiceRecord":
        return cls(
            invoice_code=d.get("invoice_code", ""),
            invoice_no=d.get("invoice_no", ""),
            invoice_type=d.get("invoice_type", ""),
            date=d.get("date", ""),
            amount=float(d.get("amount", 0.0) or 0.0),
            tax_amount=float(d.get("tax_amount", 0.0) or 0.0),
            buyer_name=d.get("buyer_name", ""),
            buyer_tax_id=d.get("buyer_tax_id", ""),
            seller_name=d.get("seller_name", ""),
            seller_tax_id=d.get("seller_tax_id", ""),
            items=d.get("items", ""),
            file_path=d.get("file_path", ""),
            file_type=d.get("file_type", ""),
            raw_text=d.get("raw_text", ""),
            status=d.get("status", "pending"),
            verify_status=d.get("verify_status", "unchecked"),
            notes=d.get("notes", ""),
            fields_hash=d.get("fields_hash", ""),
        )


@dataclass
class ReportSummary:
    total_invoices: int = 0
    duplicate_count: int = 0
    suspicious_count: int = 0
    clean_count: int = 0
    total_amount: float = 0.0
    duplicate_amount: float = 0.0
    by_type: Dict[str, Dict[str, Any]] = None
    by_month: Dict[str, Dict[str, Any]] = None
    tier_info: Dict[str, Any] = None

    def __post_init__(self):
        if self.by_type is None:
            self.by_type = {}
        if self.by_month is None:
            self.by_month = {}
        if self.tier_info is None:
            self.tier_info = {}

    @classmethod
    def from_dict(cls, d: dict) -> "ReportSummary":
        return cls(
            total_invoices=d.get("total_invoices", 0),
            duplicate_count=d.get("duplicate_count", 0),
            suspicious_count=d.get("suspicious_count", 0),
            clean_count=d.get("clean_count", 0),
            total_amount=float(d.get("total_amount", 0.0) or 0.0),
            duplicate_amount=float(d.get("duplicate_amount", 0.0) or 0.0),
            by_type=d.get("by_type", {}),
            by_month=d.get("by_month", {}),
            tier_info=d.get("tier", {}),
        )


# ─────────────────────────────────────────────────────────────────────────────
# Report sections
# ─────────────────────────────────────────────────────────────────────────────
def _section_basic_info(summary: ReportSummary, buyer_name: str = "", buyer_tax_id: str = "") -> str:
    """生成第一节：基本信息"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 企业信息
    ent_name = buyer_name or "（未提供）"
    ent_tax_id = buyer_tax_id or "（未提供）"

    # 异常发票统计
    abnormal_count = summary.duplicate_count + summary.suspicious_count

    rows = [
        f"| 项目 | 内容 |",
        f"|------|------|",
        f"| 报告期间 | {datetime.now().strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')} |",
        f"| 发票总数 | {summary.total_invoices} 张 |",
        f"| 价税合计总额 | {_fmt_currency(summary.total_amount)} |",
        f"| 异常发票数 | {abnormal_count} 张 |",
        f"| 涉及企业名称 | {ent_name} |",
        f"| 纳税人识别号 | {ent_tax_id} |",
    ]

    return """## 一、基本信息

""" + "\n".join(rows)


def _section_invoice_summary(summary: ReportSummary, records: List[InvoiceRecord]) -> str:
    """生成第二节：发票汇总"""
    lines = ["## 二、发票汇总\n"]

    # 2.1 按类型分布
    lines.append("### 2.1 按发票类型分布\n")
    header = "| 发票类型 | 数量 | 金额合计 |"
    sep = "|------|------|---------|"
    rows = [header, sep]

    type_totals = {}
    for r in records:
        t = r.invoice_type or "其他票据"
        type_totals.setdefault(t, {"count": 0, "amount": 0.0})
        type_totals[t]["count"] += 1
        type_totals[t]["amount"] += r.amount

    grand_total_count = 0
    grand_total_amount = 0.0

    for inv_type in sorted(type_totals.keys()):
        info = type_totals[inv_type]
        grand_total_count += info["count"]
        grand_total_amount += info["amount"]
        rows.append(f"| {inv_type} | {info['count']} | {_fmt_currency(info['amount'])} |")

    rows.append(f"| **合计** | **{grand_total_count}** | **{_fmt_currency(grand_total_amount)}** |")

    lines.append("\n".join(rows))
    lines.append("")

    # 2.2 按月份分布
    lines.append("### 2.2 按月份分布\n")
    header = "| 月份 | 发票数量 | 金额合计 |"
    sep = "|------|---------|---------|"
    rows = [header, sep]

    month_totals = {}
    for r in records:
        if r.date:
            month = r.date[:7]  # YYYY-MM
        else:
            month = "未知月份"
        month_totals.setdefault(month, {"count": 0, "amount": 0.0})
        month_totals[month]["count"] += 1
        month_totals[month]["amount"] += r.amount

    for month in sorted(month_totals.keys()):
        info = month_totals[month]
        rows.append(f"| {month} | {info['count']} | {_fmt_currency(info['amount'])} |")

    lines.append("\n".join(rows))

    return "\n".join(lines)


def _section_duplicate_result(records: List[InvoiceRecord]) -> str:
    """生成第三节：查重结果"""
    dup_records = [r for r in records if r.status in ("duplicate", "suspicious")]

    if not dup_records:
        return """## 三、查重结果

**重复发票数量**：0 张  
**重复发票金额**：¥0.00

✅ 未发现重复报销发票。
"""

    lines = ["## 三、查重结果\n"]

    header = "| 序号 | 发票号码 | 开票日期 | 金额 | 销售方 | 疑似重复原因 |"
    sep = "|------|---------|---------|------|--------|------------|"
    rows = [header, sep]

    total_dup_amount = 0.0

    for i, r in enumerate(dup_records, 1):
        invoice_no = r.invoice_no or "（无号码）"
        date = _fmt_date(r.date)
        amount = r.amount
        total_dup_amount += amount
        seller = r.seller_name or "（无销售方）"

        # 重复原因
        if r.status == "duplicate":
            if r.invoice_code and r.invoice_no:
                reason = "发票号码完全相同"
            else:
                reason = "关键字段一致"
        else:
            reason = "金额+日期+购买方相同但号码不同 ⚠️ 疑似篡改"

        rows.append(f"| {i} | {invoice_no} | {date} | {_fmt_currency(amount)} | {seller} | {reason} |")

    lines.append("\n".join(rows))
    lines.append("")
    lines.append(f"**重复发票数量**：{len(dup_records)} 张")
    lines.append(f"**重复发票金额**：{_fmt_currency(total_dup_amount)}")

    return "\n".join(lines)


def _section_verify_result(records: List[InvoiceRecord]) -> str:
    """生成第四节：验真结果"""
    abnormal_records = [
        r for r in records
        if r.verify_status in ("void", "red", "失控", "suspicious", "abnormal")
    ]

    if not abnormal_records:
        return """## 四、验真结果

**异常发票数量**：0 张  
**异常发票金额**：¥0.00

✅ 全部发票状态正常。
"""

    lines = ["## 四、验真结果\n"]

    header = "| 序号 | 发票号码 | 开票日期 | 金额 | 验真状态 | 状态说明 |"
    sep = "|------|---------|---------|------|---------|---------|"
    rows = [header, sep]

    total_abnormal_amount = 0.0

    for i, r in enumerate(abnormal_records, 1):
        invoice_no = r.invoice_no or "（无号码）"
        date = _fmt_date(r.date)
        amount = r.amount
        total_abnormal_amount += amount
        verify_status = r.verify_status
        status_desc = {
            "void": "作废",
            "red": "红冲",
            "失控": "失控",
            "suspicious": "可疑",
            "abnormal": "异常",
        }.get(verify_status, verify_status)

        rows.append(f"| {i} | {invoice_no} | {date} | {_fmt_currency(amount)} | {verify_status} | {status_desc} |")

    lines.append("\n".join(rows))
    lines.append("")
    lines.append(f"**异常发票数量**：{len(abnormal_records)} 张")
    lines.append(f"**异常发票金额**：{_fmt_currency(total_abnormal_amount)}")

    return "\n".join(lines)


def _section_compliance_conclusion(records: List[InvoiceRecord]) -> str:
    """生成第五节：合规结论"""
    dup_susp_count = sum(1 for r in records if r.status in ("duplicate", "suspicious"))
    abnormal_verify_count = sum(
        1 for r in records if r.verify_status in ("void", "red", "失控", "suspicious", "abnormal")
    )

    # 真实性检查结论
    if dup_susp_count > 0:
        authenticity = "⚠️ 发现异常"
    else:
        authenticity = "✅ 未见异常"

    # 重复报销检查结论
    if dup_susp_count > 0:
        duplicate_check = f"⚠️ 发现 {dup_susp_count} 张重复"
    else:
        duplicate_check = "✅ 未发现重复"

    # 发票状态检查结论
    if abnormal_verify_count > 0:
        status_check = f"⚠️ 发现 {abnormal_verify_count} 张异常"
    else:
        status_check = "✅ 全部正常"

    # 格式合规性
    format_issues = sum(1 for r in records if r.status == "suspicious")
    if format_issues > 0:
        format_check = f"⚠️ 存在 {format_issues} 张格式不规范发票"
    else:
        format_check = "✅ 符合要求"

    lines = [
        "## 五、合规结论",
        "",
        "根据《财政部关于电子发票电子化报销、入账、归档管理有关问题的通知》（财会便函〔2023〕18号）要求，本报告对所述期间内企业发票进行了合规性审查。",
        "",
        "### 5.1 合规情况总结",
        "",
        "| 检查项目 | 结果 |",
        "|---------|------|",
        f"| 发票真实性 | {authenticity} |",
        f"| 重复报销检查 | {duplicate_check} |",
        f"| 发票状态检查 | {status_check} |",
        f"| 格式合规性 | {format_check} |",
        "",
        "### 5.2 风险提示",
        "",
    ]

    risk_items = []
    if dup_susp_count > 0:
        dup_amount = sum(r.amount for r in records if r.status in ("duplicate", "suspicious"))
        risk_items.append(f"- [ ] 发现 {dup_susp_count} 张发票存在重复报销风险，涉及金额 {_fmt_currency(dup_amount)}")
    if abnormal_verify_count > 0:
        ab_amount = sum(r.amount for r in records if r.verify_status in ("void", "red", "失控", "suspicious", "abnormal"))
        risk_items.append(f"- [ ] 发现 {abnormal_verify_count} 张发票状态异常（作废/红冲/失控）")
    if format_issues > 0:
        risk_items.append(f"- [ ] 建议对格式不规范发票进行进一步核实后再行报销")

    if not risk_items:
        risk_items = ["- [ ] 未发现明显合规风险"]

    lines.extend(risk_items)

    return "\n".join(lines)


def _section_attachment_list(records: List[InvoiceRecord]) -> str:
    """生成第六节：附件清单"""
    lines = [
        "## 六、附件清单",
        "",
        "| 序号 | 附件名称 | 说明 |",
        "|------|---------|------|",
        "| 1 | 原始发票影像 | 各发票图片/PDF 原件 |",
        "| 2 | 发票明细表 | 全部发票的结构化数据 |",
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Main report generator
# ─────────────────────────────────────────────────────────────────────────────
def generate_compliance_report(
    records: List[InvoiceRecord],
    summary: ReportSummary,
    buyer_name: str = "",
    buyer_tax_id: str = "",
    include_raw_details: bool = True,
) -> str:
    """
    生成完整的发票合规检查报告。

    Args:
        records: 发票记录列表
        summary: 汇总统计数据
        buyer_name: 企业名称（用于报告基本信息）
        buyer_tax_id: 纳税人识别号（用于报告基本信息）
        include_raw_details: 是否在报告末尾附上原始发票明细表

    Returns:
        Markdown 格式的完整报告
    """
    report_id = _generate_report_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# 发票合规检查报告\n",
        f"**报告编号**：`{report_id}`\n",
        f"**生成时间**：`{now}`\n",
        f"**生成机构**：{GENERATOR_NAME}\n",
        f"**版本**：{REPORT_VERSION}\n",
        "---\n",
    ]

    # 第一节：基本信息
    lines.append(_section_basic_info(summary, buyer_name, buyer_tax_id))
    lines.append("")

    # 第二节：发票汇总
    lines.append(_section_invoice_summary(summary, records))
    lines.append("")

    # 第三节：查重结果
    lines.append(_section_duplicate_result(records))
    lines.append("")

    # 第四节：验真结果
    lines.append(_section_verify_result(records))
    lines.append("")

    # 第五节：合规结论
    lines.append(_section_compliance_conclusion(records))
    lines.append("")

    # 第六节：附件清单
    lines.append(_section_attachment_list(records))
    lines.append("")

    # 附：原始发票明细表
    if include_raw_details and records:
        lines.append("---\n")
        lines.append("## 附：发票明细表\n")
        header = "| 发票号码 | 类型 | 开票日期 | 金额 | 销售方 | 状态 |"
        sep = "|------|------|---------|------|--------|------|"
        rows = [header, sep]

        for r in records:
            status_map = {
                "clean": "✅ 正常",
                "duplicate": "🔴 重复",
                "suspicious": "⚠️ 可疑",
                "pending": "⏳ 待处理",
            }
            status_display = status_map.get(r.status, r.status)
            rows.append(
                f"| {r.invoice_no or '（无）'} | {r.invoice_type or '其他票据'} | "
                f"{_fmt_date(r.date)} | {_fmt_currency(r.amount)} | "
                f"{r.seller_name or '（无）'} | {status_display} |"
            )

        lines.append("\n".join(rows))

    # 页脚
    lines.append("")
    lines.append(
        f"\n*本报告由 {GENERATOR_NAME} 自动生成，仅供内部合规参考，不作为税务申报依据。*\n"
    )
    lines.append(f"*报告编号：{report_id} · 生成时间：{now}*\n")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Feishu Native Integration (飞书原生方案)
# ─────────────────────────────────────────────────────────────────────────────
def generate_feishu_compliance_report_markdown(
    records: List[InvoiceRecord],
    summary: ReportSummary,
    buyer_name: str = "",
    buyer_tax_id: str = "",
) -> str:
    """
    生成飞书文档格式的合规报告，使用飞书原生 Markdown 语法（支持高亮块、分栏等）。
    结果可直接用于 feishu_create_doc 工具创建文档。
    
    符合《财会便函〔2023〕18号》六节结构要求，文档可分享、可评论。
    
    Args:
        records: 发票记录列表
        summary: 汇总统计数据
        buyer_name: 企业名称
        buyer_tax_id: 纳税人识别号
        
    Returns:
        Lark-flavored Markdown 格式的完整报告
    """
    report_id = _generate_report_id()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 飞书文档开头 - 不要一级标题（title 参数已经设置了文档标题）
    lines = []
    
    lines.append(f"**报告编号**：`{report_id}`\n")
    lines.append(f"**生成时间**：`{now}`\n")
    lines.append(f"**生成机构**：{GENERATOR_NAME}\n")
    lines.append(f"**版本**：{REPORT_VERSION} (飞书原生版)\n")
    lines.append("---\n")
    
    # 第一节：基本信息
    lines.append("## 一、基本信息\n")
    
    ent_name = buyer_name or "（未提供）"
    ent_tax_id = buyer_tax_id or "（未提供）"
    abnormal_count = summary.duplicate_count + summary.suspicious_count
    
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 报告期间 | {datetime.now().strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')} |")
    lines.append(f"| 发票总数 | {summary.total_invoices} 张 |")
    lines.append(f"| 价税合计总额 | {_fmt_currency(summary.total_amount)} |")
    lines.append(f"| 异常发票数 | {abnormal_count} 张 |")
    lines.append(f"| 涉及企业名称 | {ent_name} |")
    lines.append(f"| 纳税人识别号 | {ent_tax_id} |")
    lines.append("")
    
    # 第二节：发票汇总
    lines.append("## 二、发票汇总\n")
    lines.append("### 2.1 按发票类型分布\n")
    
    type_header = "| 发票类型 | 数量 | 金额合计 |"
    type_sep = "|------|------|---------|"
    type_rows = [type_header, type_sep]
    
    type_totals = {}
    for r in records:
        t = r.invoice_type or "其他票据"
        type_totals.setdefault(t, {"count": 0, "amount": 0.0})
        type_totals[t]["count"] += 1
        type_totals[t]["amount"] += r.amount
    
    grand_total_count = 0
    grand_total_amount = 0.0
    for inv_type in sorted(type_totals.keys()):
        info = type_totals[inv_type]
        grand_total_count += info["count"]
        grand_total_amount += info["amount"]
        type_rows.append(f"| {inv_type} | {info['count']} | {_fmt_currency(info['amount'])} |")
    
    type_rows.append(f"| **合计** | **{grand_total_count}** | **{_fmt_currency(grand_total_amount)}** |")
    lines.append("\n".join(type_rows))
    lines.append("")
    
    lines.append("### 2.2 按月份分布\n")
    month_header = "| 月份 | 发票数量 | 金额合计 |"
    month_sep = "|------|---------|---------|"
    month_rows = [month_header, month_sep]
    
    month_totals = {}
    for r in records:
        if r.date:
            month = r.date[:7]
        else:
            month = "未知月份"
        month_totals.setdefault(month, {"count": 0, "amount": 0.0})
        month_totals[month]["count"] += 1
        month_totals[month]["amount"] += r.amount
    
    for month in sorted(month_totals.keys()):
        info = month_totals[month]
        month_rows.append(f"| {month} | {info['count']} | {_fmt_currency(info['amount'])} |")
    
    lines.append("\n".join(month_rows))
    lines.append("")
    
    # 第三节：查重结果
    lines.append("## 三、查重结果\n")
    dup_records = [r for r in records if r.status in ("duplicate", "suspicious")]
    
    if not dup_records:
        lines.append("<callout emoji=\"✅\" background-color=\"light-green\">\n未发现重复报销发票\n</callout>\n")
        lines.append("**重复发票数量**：0 张  ")
        lines.append("**重复发票金额**：¥0.00")
    else:
        dup_header = "| 序号 | 发票号码 | 开票日期 | 金额 | 销售方 | 疑似重复原因 |"
        dup_sep = "|------|---------|---------|------|--------|------------|"
        dup_rows = [dup_header, dup_sep]
        
        total_dup_amount = 0.0
        for i, r in enumerate(dup_records, 1):
            invoice_no = r.invoice_no or "（无号码）"
            date = _fmt_date(r.date)
            amount = r.amount
            total_dup_amount += amount
            seller = r.seller_name or "（无销售方）"
            
            if r.status == "duplicate":
                reason = "发票号码完全相同"
            else:
                reason = "金额+日期+购买方相同但号码不同 ⚠️ 疑似篡改"
            
            dup_rows.append(f"| {i} | {invoice_no} | {date} | {_fmt_currency(amount)} | {seller} | {reason} |")
        
        lines.append("\n".join(dup_rows))
        lines.append("")
        lines.append(f"**重复发票数量**：{len(dup_records)} 张")
        lines.append(f"**重复发票金额**：{_fmt_currency(total_dup_amount)}")
    
    lines.append("")
    
    # 第四节：验真结果
    lines.append("## 四、验真结果\n")
    abnormal_records = [r for r in records if r.verify_status in ("void", "red", "失控", "suspicious", "abnormal")]
    
    if not abnormal_records:
        lines.append("<callout emoji=\"✅\" background-color=\"light-green\">\n全部发票状态正常\n</callout>\n")
        lines.append("**异常发票数量**：0 张  ")
        lines.append("**异常发票金额**：¥0.00")
    else:
        abnormal_header = "| 序号 | 发票号码 | 开票日期 | 金额 | 验真状态 | 状态说明 |"
        abnormal_sep = "|------|---------|---------|------|---------|---------|"
        abnormal_rows = [abnormal_header, abnormal_sep]
        
        total_abnormal_amount = 0.0
        for i, r in enumerate(abnormal_records, 1):
            invoice_no = r.invoice_no or "（无号码）"
            date = _fmt_date(r.date)
            amount = r.amount
            total_abnormal_amount += amount
            status_desc = {
                "void": "作废",
                "red": "红冲",
                "失控": "失控",
                "suspicious": "可疑",
                "abnormal": "异常",
            }.get(r.verify_status, r.verify_status)
            
            abnormal_rows.append(f"| {i} | {invoice_no} | {date} | {_fmt_currency(amount)} | {r.verify_status} | {status_desc} |")
        
        lines.append("\n".join(abnormal_rows))
        lines.append("")
        lines.append(f"**异常发票数量**：{len(abnormal_records)} 张")
        lines.append(f"**异常发票金额**：{_fmt_currency(total_abnormal_amount)}")
    
    lines.append("")
    
    # 第五节：合规结论
    lines.append("## 五、合规结论\n")
    lines.append("根据《财政部关于电子发票电子化报销、入账、归档管理有关问题的通知》（财会便函〔2023〕18号）要求，本报告对所述期间内企业发票进行了合规性审查。\n")
    lines.append("### 5.1 合规情况总结\n")
    
    dup_susp_count = sum(1 for r in records if r.status in ("duplicate", "suspicious"))
    abnormal_verify_count = sum(1 for r in records if r.verify_status in ("void", "red", "失控", "suspicious", "abnormal"))
    format_issues = sum(1 for r in records if r.status == "suspicious")
    
    authenticity = "✅ 未见异常" if dup_susp_count == 0 else "⚠️ 发现异常"
    duplicate_check = "✅ 未发现重复" if dup_susp_count == 0 else f"⚠️ 发现 {dup_susp_count} 张重复"
    status_check = "✅ 全部正常" if abnormal_verify_count == 0 else f"⚠️ 发现 {abnormal_verify_count} 张异常"
    format_check = "✅ 符合要求" if format_issues == 0 else f"⚠️ 存在 {format_issues} 张格式不规范发票"
    
    lines.append("| 检查项目 | 结果 |")
    lines.append("|---------|------|")
    lines.append(f"| 发票真实性 | {authenticity} |")
    lines.append(f"| 重复报销检查 | {duplicate_check} |")
    lines.append(f"| 发票状态检查 | {status_check} |")
    lines.append(f"| 格式合规性 | {format_check} |")
    lines.append("")
    
    lines.append("### 5.2 风险提示\n")
    risk_items = []
    
    if dup_susp_count > 0:
        dup_amount = sum(r.amount for r in records if r.status in ("duplicate", "suspicious"))
        lines.append(f"<callout emoji=\"⚠️\" background-color=\"light-yellow\">\n发现 {dup_susp_count} 张发票存在重复报销风险，涉及金额 {_fmt_currency(dup_amount)}\n</callout>\n")
    
    if abnormal_verify_count > 0:
        ab_amount = sum(r.amount for r in records if r.verify_status in ("void", "red", "失控", "suspicious", "abnormal"))
        lines.append(f"<callout emoji=\"⚠️\" background-color=\"light-yellow\">\n发现 {abnormal_verify_count} 张发票状态异常（作废/红冲/失控），涉及金额 {_fmt_currency(ab_amount)}\n</callout>\n")
    
    if format_issues > 0:
        lines.append(f"<callout emoji=\"💡\" background-color=\"light-blue\">\n建议对格式不规范发票进行进一步核实后再行报销\n</callout>\n")
    
    if dup_susp_count == 0 and abnormal_verify_count == 0 and format_issues == 0:
        lines.append("<callout emoji=\"✅\" background-color=\"light-green\">\n未发现明显合规风险\n</callout>\n")
    
    # 第六节：附件清单
    lines.append("## 六、附件清单\n")
    lines.append("| 序号 | 附件名称 | 说明 |")
    lines.append("|------|---------|------|")
    lines.append("| 1 | 原始发票影像 | 各发票图片/PDF 原件 |")
    lines.append(f"| 2 | 发票明细表 | 全部发票结构化数据存储于飞书多维表格 |")
    lines.append("")
    
    # 页脚
    lines.append("---")
    lines.append("")
    lines.append(f"*本报告由 {GENERATOR_NAME} 自动生成，仅供内部合规参考，不作为税务申报依据。*")
    lines.append(f"*报告编号：{report_id} · 生成时间：{now}*")
    lines.append("")
    
    return "\n".join(lines)


def prepare_invoices_for_feishu_bitable(records: List[InvoiceRecord]) -> List[Dict[str, Any]]:
    """
    将发票记录转换为飞书多维表格所需的批量创建格式。
    适用于 feishu_bitable_app_table_record.batch_create API。
    
    飞书多维表格预设字段：
    - 发票代码（文本）
    - 发票号码（文本）
    - 开票日期（日期）
    - 金额（数字）
    - 开票方（文本）
    - 状态（单选：正常/重复/可疑/异常）
    - 查验状态（单选：未查验/正常/作废/红冲/失控）
    
    Args:
        records: 发票记录列表
        
    Returns:
        适用于批量创建的 records 数组
    """
    bitable_records = []
    
    status_map = {
        "clean": "正常",
        "duplicate": "重复", 
        "suspicious": "可疑",
        "pending": "待处理",
        "abnormal": "异常",
    }
    
    verify_map = {
        "unchecked": "未查验",
        "normal": "正常",
        "void": "作废",
        "red": "红冲",
        "失控": "失控",
        "suspicious": "可疑",
        "abnormal": "异常",
    }
    
    for r in records:
        # 转换日期为毫秒时间戳
        if r.date and re.match(r'\d{4}-\d{2}-\d{2}', r.date):
            from datetime import datetime
            dt = datetime.strptime(r.date, "%Y-%m-%d")
            timestamp_ms = int(dt.timestamp() * 1000)
        else:
            timestamp_ms = None
        
        fields = {
            "发票代码": r.invoice_code,
            "发票号码": r.invoice_no,
            "开票方": r.seller_name,
            "金额": r.amount,
            "状态": status_map.get(r.status, r.status),
            "查验状态": verify_map.get(r.verify_status, r.verify_status),
        }
        
        if timestamp_ms:
            fields["开票日期"] = timestamp_ms
        
        bitable_records.append({
            "fields": fields
        })
    
    return bitable_records


def create_feishu_bitable_schema(app_token: str) -> Dict[str, Any]:
    """
    返回创建发票明细表所需的字段定义。
    使用 feishu_bitable_app_table.create 时传入此结构。
    
    Args:
        app_token: 多维表格 app token
        
    Returns:
        table.fields 定义
    """
    fields = [
        {
            "field_name": "发票代码",
            "type": 1,  # 文本
        },
        {
            "field_name": "发票号码", 
            "type": 1,  # 文本
        },
        {
            "field_name": "开票日期",
            "type": 5,  # 日期
        },
        {
            "field_name": "金额",
            "type": 2,  # 数字
        },
        {
            "field_name": "开票方",
            "type": 1,  # 文本
        },
        {
            "field_name": "状态",
            "type": 3,  # 单选
            "property": {
                "options": [
                    {"name": "正常"},
                    {"name": "重复"}, 
                    {"name": "可疑"},
                    {"name": "异常"},
                ]
            }
        },
        {
            "field_name": "查验状态",
            "type": 3,  # 单选
            "property": {
                "options": [
                    {"name": "未查验"},
                    {"name": "正常"},
                    {"name": "作废"},
                    {"name": "红冲"},
                    {"name": "失控"},
                ]
            }
        }
    ]
    
    return fields


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """
    CLI 用法：
    python3 compliance_report.py <summary_json> <records_json> [buyer_name] [buyer_tax_id]

    示例：
    python3 compliance_report.py '{"total_invoices":5,"duplicate_count":1,...}' '[{"invoice_no":"12345678",...}]' 'XX公司' '91440000MA5XXXXXXX'
    """
    if len(sys.argv) < 3:
        # 演示模式：无参数时生成示例报告
        print("用法: python3 compliance_report.py <summary_json> <records_json> [buyer_name] [buyer_tax_id]")
        print("")
        print("演示模式：生成示例报告...")
        summary = ReportSummary(
            total_invoices=8,
            duplicate_count=2,
            suspicious_count=1,
            clean_count=5,
            total_amount=125680.50,
            duplicate_amount=34560.00,
            by_type={
                "增值税专用发票": {"count": 3, "amount": 45600.00},
                "增值税普通发票": {"count": 2, "amount": 18900.00},
                "电子发票": {"count": 2, "amount": 51000.00},
                "机票行程单": {"count": 1, "amount": 10180.50},
            },
        )
        records = [
            InvoiceRecord(invoice_no="12345678", invoice_type="增值税专用发票", date="2026-01-15",
                         amount=25600.00, seller_name="XX科技有限公司", status="clean", verify_status="normal"),
            InvoiceRecord(invoice_no="22345678", invoice_type="增值税专用发票", date="2026-01-18",
                         amount=20000.00, seller_name="YY贸易公司", status="duplicate", verify_status="unchecked",
                         notes="跨批次重复：与历史记录发票号码重复"),
            InvoiceRecord(invoice_no="32345678", invoice_type="增值税普通发票", date="2026-02-03",
                         amount=8900.00, seller_name="ZZ商贸", status="clean", verify_status="unchecked"),
            InvoiceRecord(invoice_no="42345678", invoice_type="电子发票", date="2026-02-10",
                         amount=31000.00, seller_name="YY贸易公司", status="suspicious", verify_status="unchecked",
                         notes="金额+日期+购买方相同但号码不同 ⚠️"),
        ]
        report = generate_compliance_report(records, summary, "演示公司", "91440000MA5XXXXXXX")
        print(report)
        return

    summary = ReportSummary.from_dict(json.loads(sys.argv[1]))
    records_dict = json.loads(sys.argv[2])
    records = [InvoiceRecord.from_dict(r) for r in records_dict]

    buyer_name = sys.argv[3] if len(sys.argv) > 3 else ""
    buyer_tax_id = sys.argv[4] if len(sys.argv) > 4 else ""

    report = generate_compliance_report(records, summary, buyer_name, buyer_tax_id)
    print(report)


if __name__ == "__main__":
    main()
