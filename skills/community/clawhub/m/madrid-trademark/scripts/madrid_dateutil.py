"""马德里技能共享日期工具（被 madrid_deadline.py / madrid_renewal.py 复用）。

设计要点：
- 日期一律按「自然月」推进（马德里各期限均以自然月计），月末与闰年 2/29 自动兜底；
- 所有计算函数都接受 today 参数，便于复现与单元测试（默认取系统当日）；
- 纯标准库，无第三方依赖。
"""

from __future__ import annotations

from datetime import date, datetime
import calendar

ISO_FORMAT = "%Y-%m-%d"


def parse_date(value) -> date:
    """解析 ISO 日期（YYYY-MM-DD）。date/datetime 原样返回。"""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise TypeError(f"无法解析日期：{value!r}（应为 YYYY-MM-DD 字符串）")
    try:
        return datetime.strptime(value.strip(), ISO_FORMAT).date()
    except ValueError as exc:
        raise ValueError(f"日期格式不合法：{value!r}，应为 YYYY-MM-DD") from exc


def today(override=None) -> date:
    """返回当日；传入 override 时返回该日期（用于 --today 与测试）。"""
    return parse_date(override) if override else date.today()


def month_end_day(year: int, month: int) -> int:
    """该年该月的最后一天（处理闰年 2/29 与月末）。"""
    return calendar.monthrange(year, month)[1]


def add_months(source: date, months: int) -> date:
    """按自然月加减：源日期为月末而目标月更短时，取目标月最后一天。"""
    total = source.month - 1 + months
    year = source.year + total // 12
    month = total % 12 + 1
    day = min(source.day, month_end_day(year, month))
    return date(year, month, day)


def add_years(source: date, years: int) -> date:
    """按年推进（等价于 add_months(source, years * 12)）。"""
    return add_months(source, years * 12)


def days_between(start: date, end: date) -> int:
    """end - start 的天数（可为负，不截断）。"""
    return (end - start).days


def formalize(value: date) -> str:
    """格式化为 YYYY-MM-DD。"""
    return value.strftime(ISO_FORMAT)
