#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odoo_utils.py — 家具制造业务脚本共用的小工具

- 时区换算：Odoo 的 Datetime 字段存 UTC，用户输入/查看用本地时间。
- Many2one 字段值（[id, name]）格式化。
- 终端表格输出（按中文显示宽度对齐）。
- 制造域 selection 状态值 → 中文标签（取值已对 test.heysleep.cn 实测验证）。
"""

from __future__ import annotations

import calendar
import time
import unicodedata
from datetime import datetime


# --------------------------------------------------------------------------- #
# 时区：本地 <-> UTC（零依赖，靠系统本地时区）
# --------------------------------------------------------------------------- #
_DT_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d")


def to_utc(s: str, default_time: str = "18:00:00") -> str:
    """本地日期/时间字符串 → Odoo 需要的 UTC datetime 字符串。"""
    s = (s or "").strip()
    if not s:
        return ""
    if len(s) == 10:
        s = f"{s} {default_time}"
    dt_local = None
    for fmt in _DT_FORMATS:
        try:
            dt_local = datetime.strptime(s, fmt)
            break
        except ValueError:
            continue
    if dt_local is None:
        raise ValueError(f"无法解析日期时间：{s!r}（用 YYYY-MM-DD 或 YYYY-MM-DD HH:MM）")
    epoch = time.mktime(dt_local.timetuple())
    return datetime.utcfromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")


def from_utc(utc_s: str, fmt: str = "%Y-%m-%d %H:%M") -> str:
    """UTC datetime 字符串 → 本地时间显示。"""
    if not utc_s:
        return ""
    try:
        dt_utc = datetime.strptime(utc_s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return utc_s
    local = time.localtime(calendar.timegm(dt_utc.timetuple()))
    return time.strftime(fmt, local)


def today() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def now_utc() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def day_range_utc(offset: int = 0) -> tuple[str, str]:
    """本地某天 [00:00:00, 23:59:59] → UTC 字符串区间。offset=0 今天，-1 昨天。"""
    t = time.localtime(time.time() + offset * 86400)
    start_local = datetime(t.tm_year, t.tm_mon, t.tm_mday)
    epoch = time.mktime(start_local.timetuple())
    fmt = "%Y-%m-%d %H:%M:%S"
    return (
        datetime.utcfromtimestamp(epoch).strftime(fmt),
        datetime.utcfromtimestamp(epoch + 86399).strftime(fmt),
    )


def days_ago_utc(days: int) -> str:
    """N 天前的本地 00:00 → UTC 字符串（list/stats 的时间窗下界）。"""
    return day_range_utc(-abs(days))[0]


# --------------------------------------------------------------------------- #
# 字段格式化
# --------------------------------------------------------------------------- #
def m2o_name(val) -> str:
    """Many2one 值 [id, 'name'] -> 'name'；False -> ''。"""
    if isinstance(val, (list, tuple)) and len(val) == 2:
        return str(val[1])
    return "" if not val else str(val)


def m2o_id(val):
    if isinstance(val, (list, tuple)) and len(val) == 2:
        return val[0]
    return val or None


def qty(val) -> str:
    """数量显示：去掉无意义小数尾零。"""
    try:
        f = float(val or 0)
    except (TypeError, ValueError):
        return str(val)
    return f"{f:.2f}".rstrip("0").rstrip(".")


def money(val) -> str:
    try:
        return f"¥{float(val or 0):,.2f}"
    except (TypeError, ValueError):
        return str(val)


# --------------------------------------------------------------------------- #
# 终端表格（中文宽度对齐）
# --------------------------------------------------------------------------- #
def _disp_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in str(s))


def _pad(s: str, width: int) -> str:
    return str(s) + " " * max(0, width - _disp_width(s))


def render_table(rows: list[list], headers: list[str]) -> str:
    if not rows:
        return "（无数据）"
    cols = len(headers)
    widths = [_disp_width(h) for h in headers]
    str_rows = []
    for r in rows:
        cells = [("" if c is None else str(c)) for c in r] + [""] * (cols - len(r))
        for i in range(cols):
            widths[i] = max(widths[i], _disp_width(cells[i]))
        str_rows.append(cells)
    line = "  ".join(_pad(headers[i], widths[i]) for i in range(cols))
    sep = "  ".join("-" * widths[i] for i in range(cols))
    out = [line, sep]
    out += ["  ".join(_pad(r[i], widths[i]) for i in range(cols)) for r in str_rows]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# 状态中文标签（selection 取值 2026-06-13 对 test 库 fields_get 实测）
# --------------------------------------------------------------------------- #
SO_STATE = {"draft": "报价单", "sent": "已发报价", "sale": "销售订单", "cancel": "已取消"}
DELIVERY_STATUS = {"pending": "未发货", "started": "开始发货", "partial": "部分发货", "full": "全部发货"}
INVOICE_STATUS = {"upselling": "可追加", "invoiced": "已开票", "to invoice": "待开票", "no": "无需开票"}
MO_STATE = {"draft": "草稿", "confirmed": "已确认", "progress": "生产中", "to_close": "待关闭", "done": "已完成", "cancel": "已取消"}
AVAIL_STATE = {"available": "齐料", "expected": "等料(预计可到)", "late": "等料(已迟)", "unavailable": "缺料"}
RESERVATION_STATE = {"confirmed": "等待备料", "assigned": "备料就绪", "waiting": "等待其他作业"}
PICKING_STATE = {"draft": "草稿", "waiting": "等待其他作业", "confirmed": "等待", "assigned": "就绪", "done": "已完成", "cancel": "已取消"}
QC_STATE = {"none": "待检", "pass": "合格", "fail": "不合格"}
PO_STATE = {"draft": "询价单", "sent": "已发询价", "to approve": "待审批", "purchase": "采购订单", "cancel": "已取消"}
RECEIPT_STATUS = {"pending": "未收货", "partial": "部分收货", "full": "全部收货"}


def label(mapping: dict, value) -> str:
    return mapping.get(value, str(value or ""))
