#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odoo_utils.py — todo/project/timesheet 共用的小工具

- 时区换算：Odoo 的 Datetime 字段存 UTC，用户输入/查看用本地时间。
- Odoo Many2one 字段值（[id, name]）格式化。
- 终端表格输出（按中文显示宽度对齐）。
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
    """把用户输入的本地日期/时间字符串转成 Odoo 需要的 UTC datetime 字符串。

    接受 'YYYY-MM-DD' / 'YYYY-MM-DD HH:MM' / 'YYYY-MM-DD HH:MM:SS'。
    只给日期时补 default_time（默认当天 18:00 作为截止时间）。
    """
    s = (s or "").strip()
    if not s:
        return ""
    if len(s) == 10:  # 只有日期
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
    epoch = time.mktime(dt_local.timetuple())  # 本地 naive -> epoch
    return datetime.utcfromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")


def from_utc(utc_s: str, fmt: str = "%Y-%m-%d %H:%M") -> str:
    """UTC datetime 字符串 -> 本地时间显示。"""
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


# --------------------------------------------------------------------------- #
# 字段格式化
# --------------------------------------------------------------------------- #
def m2o_name(val) -> str:
    """Many2one 值 [id, 'name'] -> 'name'；False -> ''。"""
    if isinstance(val, (list, tuple)) and len(val) == 2:
        return str(val[1])
    return "" if not val else str(val)


def m2o_id(val):
    """Many2one 值 [id, 'name'] -> id；False -> None。"""
    if isinstance(val, (list, tuple)) and len(val) == 2:
        return val[0]
    return val or None


def hours(val) -> str:
    """小时数显示，保留 2 位，去掉无意义的 .00。"""
    try:
        f = float(val or 0)
    except (TypeError, ValueError):
        return str(val)
    return f"{f:.2f}".rstrip("0").rstrip(".") + "h"


# --------------------------------------------------------------------------- #
# 终端表格（中文宽度对齐）
# --------------------------------------------------------------------------- #
def _disp_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in str(s))


def _pad(s: str, width: int) -> str:
    return str(s) + " " * max(0, width - _disp_width(s))


def render_table(rows: list[list], headers: list[str]) -> str:
    """把二维数据渲染成对齐文本表格。"""
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


# project.task.state -> 中文 + 是否已关闭
STATE_LABELS = {
    "01_in_progress": "进行中",
    "02_changes_requested": "待修改",
    "03_approved": "已批准",
    "1_done": "已完成",
    "1_canceled": "已取消",
    "04_waiting_normal": "等待中",
}
CLOSED_STATES = ("1_done", "1_canceled")

PRIORITY_LABELS = {"0": "普通", "1": "中", "2": "高", "3": "紧急"}


def state_label(state: str) -> str:
    return STATE_LABELS.get(state, state or "")


def priority_label(p: str) -> str:
    return PRIORITY_LABELS.get(str(p), str(p))
