#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金收益日历查询：通过 JHub 网关调用 CalendarService.queryCalendar。

查询当前登录账号的黄金收益数据。
接口全限定名：com.jd.jrjydcgl.gold.analysis.query.client.calendar.api.CalendarService#queryCalendar

接口 time 格式规则（根据调试结果）：
  - day / week 维度：time 格式为 yyyyMM（如 202607）
  - year 维度：time 格式为 yyyy（如 2026）

数据提取规则（根据调试结果）：
  - 完整收益数据在 JHub 响应的 log.result.data 中
  - testResult.response.data 的 incomeDetailMap 为空，不可用
  - incomeDetailMap 的 key 是时间值（year→"2018", day→"20260607"）
  - incomeDetailMap 中有一个特殊 key "fromAll"，表示全银行累计卖出收益
  - 每个 value 包含 incomeAmount（收益金额）、startDate、endDate

单位规则：
  - 收益金额均为人民币（元）
  - 不要与美元/盎司混用

默认行为：全局查询获取 fromAll 累计总收益，再逐银行查询各银行明细。
用户指定时间段时：按月/日维度查询并累加展示明细。
"""
import argparse
import json
import os
import sys
import urllib.error
from datetime import datetime
from typing import List, Optional

import jos
import bff_client

# 已知银行编码对照表
BANK_CODE_MAP = {
    "CMBC": "民生银行",
    "CZB": "浙商银行",
    "CIB": "兴业银行",
    "CITIC": "中信银行",
    "ICBC": "工商银行",
    "CCB": "建设银行",
    "ABC": "农业银行",
    "BOC": "中国银行",
    "PSBC": "邮储银行",
        "CGB": "广发银行",
    "SPDB": "浦发银行",
    "CMB": "招商银行",
    "HXB": "华夏银行",
    "BOS": "上海银行",
    "NBCB": "宁波银行",
    "BJB": "北京银行",
}

# ── time 格式规则 ──────────────────────────────────────────────


def _fmt_time(time_type: str, time_value: Optional[str] = None) -> str:
    if time_value:
        return time_value
    now = datetime.now()
    if time_type in ("day", "week"):
        return now.strftime("%Y%m")
    else:
        return str(now.year)


# ── 低层接口调用 ───────────────────────────────────────────────


def _raw_call(calendar_param: dict) -> dict:
    """通过 BFF 调用收益日历接口，返回业务 data。"""
    access_token = jos._valid_access_token()
    result = bff_client.post_json(
        bff_client.PATH_INCOME_CALENDAR,
        {"accessToken": access_token, "calendarParam": calendar_param},
    )
    if not isinstance(result, dict):
        raise RuntimeError("收益日历响应无有效数据")
    data = result.get("data")
    if not data:
        raise RuntimeError("收益日历响应无有效数据")
    return data


def fetch_income_calendar(
    time_type: str = "day",
    time_value: Optional[str] = None,
    trade_type: str = "1",
) -> dict:
    """单次调用收益日历接口（不传 bankCode）。"""
    time_str = _fmt_time(time_type, time_value)
    calendar_param = {
        "timeType": time_type,
        "time": time_str,
        "tradeType": trade_type,
    }
    return _raw_call(calendar_param)


# ── 银行收益汇总 ───────────────────────────────────────────────


def _bank_name(bank_code: str) -> str:
    """从对照表查找银行名称，未知编码则原样返回。"""
    return BANK_CODE_MAP.get(bank_code, bank_code)


def _discover_banks_from_income(data: dict) -> List[str]:
    """从全局收益数据中推断有收益的银行。

    fromAll 是全银行汇总；各年度 key 里的 incomeAmount 是该年度所有银行合计。
    无法从全局数据直接拆分银行，需逐银行探测。
    """
    im = data.get("incomeDetailMap") or {}
    # 如果各年度合计 ≈ fromAll，说明无需拆分（只有一家或数据不分银行）
    yearly_total = sum(
        float(v.get("incomeAmount") or 0)
        for k, v in im.items()
        if k != "fromAll" and isinstance(v, dict)
    )
    from_all = float((im.get("fromAll") or {}).get("incomeAmount") or 0)
    # 如果 fromAll > 0，需要逐银行探测
    return from_all > 0


def _discover_bank_codes(data: dict) -> List[str]:
    """探测哪些银行有收益数据。

    策略：
    1. 先从持仓接口获取有持仓的银行列表
    2. 补充常见银行编码逐一探测（找出如工行等持仓接口未返回但有收益的银行）
    """
    known_codes = set()

    # 从持仓接口获取
    try:
        holdings_data = jos.fetch_holdings()
        for h in (holdings_data.get("holdingList") or []):
            bc = h.get("bankCode")
            if bc and float(h.get("totalGram") or 0) > 0:
                known_codes.add(bc)
    except Exception:
        pass

    # 补充常见银行编码（可能有历史收益但当前无持仓）
    for code in BANK_CODE_MAP:
        known_codes.add(code)

    return sorted(known_codes)


def fetch_income_by_banks(
    time_type: str = "year",
    time_value: Optional[str] = None,
    trade_type: str = "1",
) -> dict:
    """查询各银行收益汇总。

    策略：
    1. 先做一次全局查询，获取 fromAll（全银行累计总收益）
    2. 逐银行查询，排除 fromAll 后计算各银行收益
    3. 只展示有收益的银行（收益 ≠ 0）

    返回 dict: {
        "fromAll": float,  # 全银行累计总收益
        "banks": [{"bankCode", "bankName", "income"}, ...]
    }
    """
    time_str = _fmt_time(time_type, time_value)

    # 1. 全局查询获取 fromAll
    global_data = fetch_income_calendar(time_type, time_value, trade_type)
    im_global = global_data.get("incomeDetailMap") or {}
    from_all_val = im_global.get("fromAll")
    from_all_income = float(from_all_val.get("incomeAmount") or 0) if isinstance(from_all_val, dict) else 0.0

    # 2. 逐银行探测
    bank_codes = _discover_bank_codes(global_data)
    banks = []
    for bank_code in bank_codes:
        try:
            param = {
                "timeType": time_type,
                "time": time_str,
                "tradeType": trade_type,
                "bankCode": bank_code,
            }
            data = _raw_call(param)
            im = data.get("incomeDetailMap") or {}
            # 排除 fromAll，计算该银行各年度合计
            bank_income = sum(
                float(v.get("incomeAmount") or 0)
                for k, v in im.items()
                if k != "fromAll" and isinstance(v, dict)
            )
            if bank_income != 0.0:
                banks.append({
                    "bankCode": bank_code,
                    "bankName": _bank_name(bank_code),
                    "income": bank_income,
                })
        except RuntimeError:
            pass  # 单银行失败不阻断

    return {"fromAll": from_all_income, "banks": banks}


# ── 指定时间段累加明细 ─────────────────────────────────────────


def fetch_income_detail_months(
    start_month: str,
    end_month: str,
    trade_type: str = "1",
) -> List[dict]:
    """按月逐月查询收益，用于月度明细。"""
    results = []
    y_start, m_start = int(start_month[:4]), int(start_month[4:6])
    y_end, m_end = int(end_month[:4]), int(end_month[4:6])

    y, m = y_start, m_start
    while (y, m) <= (y_end, m_end):
        month_str = "%d%02d" % (y, m)
        try:
            data = fetch_income_calendar("day", month_str, trade_type)
            im = data.get("incomeDetailMap") or {}
            month_total = sum(
                float(v.get("incomeAmount") or 0)
                for k, v in im.items()
                if k != "fromAll" and isinstance(v, dict)
            )
            results.append({"month": month_str, "income": month_total, "data": data})
        except RuntimeError:
            results.append({"month": month_str, "income": 0.0, "data": None})
        m += 1
        if m > 12:
            m = 1
            y += 1

    return results


def fetch_income_detail_days(
    month_str: str,
    trade_type: str = "1",
) -> List[dict]:
    """查询某月的日收益明细列表。"""
    data = fetch_income_calendar("day", month_str, trade_type)
    im = data.get("incomeDetailMap") or {}
    days = []
    for key, val in im.items():
        if key == "fromAll" or not isinstance(val, dict):
            continue
        days.append({
            "date": key,
            "startDate": val.get("startDate", key),
            "endDate": val.get("endDate", key),
            "incomeAmount": float(val.get("incomeAmount") or 0),
        })
    days.sort(key=lambda d: d["date"])
    return days


# ── 格式化工具 ─────────────────────────────────────────────────


def _fmt_income(v, emoji=False) -> str:
    if v is None:
        return "—"
    try:
        n = float(v)
        sign = "+" if n > 0 else ""
        text = f"{sign}{n:,.2f}"
        if emoji:
            if n > 0:
                return f"🔺 {text}"
            if n < 0:
                return f"🔻 {text}"
            return f"➖ {text}"
        return text
    except (TypeError, ValueError):
        return str(v)


def _fmt_num(v, digits=2) -> str:
    if v is None:
        return "—"
    try:
        n = float(v)
        return f"{n:,.{digits}f}"
    except (TypeError, ValueError):
        return str(v)


# ── 渲染 ───────────────────────────────────────────────────────


def render_income_by_banks(result: dict) -> str:
    """按银行维度渲染累计卖出收益汇总。"""
    from_all = result.get("fromAll", 0.0)
    banks = result.get("banks") or []

    lines = ["💰【黄金收益 · 累计汇总】"]

    if not banks and from_all == 0.0:
        lines.append("")
        lines.append("暂无收益数据。")
        return "\n".join(lines)

    for bank in banks:
        lines.append("")
        lines.append("🏦 %s" % bank["bankName"])
        lines.append("  💰 累计卖出收益：%s 元" % _fmt_income(bank["income"]))

    lines.append("")
    lines.append("📊 总累计卖出收益：%s 元" % _fmt_income(from_all))

    return "\n".join(lines)


def render_income_detail_months(month_results: List[dict]) -> str:
    """按月明细渲染收益。"""
    lines = ["📅【黄金收益 · 月度明细】"]

    total_income = 0.0
    has_data = False

    for item in month_results:
        month_str = item.get("month", "")
        income = item.get("income", 0.0)
        data = item.get("data")

        if data is not None:
            im = data.get("incomeDetailMap") or {}
            if im:
                has_data = True
                total_income += income
                lines.append("  %s：%s 元" % (month_str, _fmt_income(income)))
            else:
                lines.append("  %s：暂无数据" % month_str)
        else:
            lines.append("  %s：查询失败" % month_str)

    if has_data:
        lines.append("")
        lines.append("累计卖出收益：%s 元" % _fmt_income(total_income))

    return "\n".join(lines)


def render_income_detail_days(day_list: List[dict], month_str: str) -> str:
    """按日明细渲染收益。"""
    lines = ["📆【黄金收益 · 日明细（%s）】" % month_str]

    total_income = 0.0
    has_data = False

    for item in day_list:
        date = item.get("startDate") or item.get("date") or ""
        amount = item.get("incomeAmount", 0)
        has_data = True
        total_income += amount
        lines.append("  %s：%s 元" % (date, _fmt_income(amount)))

    if has_data:
        lines.append("")
        lines.append("月累计卖出收益：%s 元" % _fmt_income(total_income))
    else:
        lines.append("暂无收益数据。")

    return "\n".join(lines)


# ── 浮盈浮亏计算 ──────────────────────────────────────────────


def _fetch_realtime_price_cny() -> Optional[float]:
    """尝试获取人民币实时金价（元/克），失败返回 None。

    通过 JHub 网关调用 RealtimeQuoteService.getSimpleQuoteUseUniqueCode。
    默认使用京东24h金价指数（WG-JDAU），银行积存金价场景使用银行维度 uniqueCode。
    金价服务不可达或返回异常时，返回 None，绝不编造数据。
    """
    try:
        import query_price_jhub
        quote = query_price_jhub.fetch_default_price()
        if quote and quote.get("lastPrice") is not None:
            return float(quote["lastPrice"])
    except Exception:
        pass
    return None


def _fetch_realtime_price_by_bank(bank_code: str) -> Optional[float]:
    """按银行维度获取人民币实时金价（元/克），失败返回 None。

    银行 code 映射到 uniqueCode（如 CMBC → CMBC-JCJ），查询该银行积存金价格。
    如果该银行无对应 uniqueCode 或接口失败，返回 None。
    """
    try:
        import query_price_jhub
        quote = query_price_jhub.fetch_price_by_bank(bank_code)
        if quote and quote.get("lastPrice") is not None:
            return float(quote["lastPrice"])
    except Exception:
        pass
    return None


def fetch_unrealized_pnl() -> dict:
    """计算浮盈浮亏（需持仓 + 实时金价）。

    返回 dict: {
        "priceAvailable": bool,        # 金价是否可获取
        "realtimePrice": float|None,   # 实时金价（元/克），金价不可用时为 None
        "banks": [{                     # 各银行浮盈浮亏（仅持仓 > 0 的银行）
            "bankCode": str,
            "bankName": str,
            "totalGram": float,         # 持仓克数
            "avgCostPrice": float,      # 成本均价（元/克）
            "unrealizedPnl": float,     # 浮动盈亏金额（元）
        }, ...],
        "totalGram": float,             # 总持仓克数
        "totalUnrealizedPnl": float,    # 总浮动盈亏金额（元）
    }

    核心原则：金价查不到时 priceAvailable=False，banks 中不含 unrealizedPnl，
    一切以准确为第一优先级，绝不编造金价数据。
    """
    # 1. 获取持仓数据
    holdings_data = jos.fetch_holdings()
    holding_list = holdings_data.get("holdingList") or []
    active = [h for h in holding_list if float(h.get("totalGram") or 0) > 0]

    total_gram = float(holdings_data.get("totalGramAll") or 0)

    result = {
        "priceAvailable": False,
        "realtimePrice": None,
        "banks": [],
        "totalGram": total_gram,
        "totalUnrealizedPnl": None,
    }

    # 2. 无持仓则无需计算
    if not active:
        result["totalUnrealizedPnl"] = 0.0
        return result

    # 3. 尝试获取实时金价（按银行维度查询精确金价，回退到默认金价）
    # 先尝试获取默认金价作为兜底
    default_price = _fetch_realtime_price_cny()

    # 4. 计算各银行浮盈浮亏（优先用银行维度金价）
    realtime_price = default_price  # 兜底金价
    total_pnl = 0.0
    price_available = default_price is not None

    for h in active:
        gram = float(h.get("totalGram") or 0)
        avg_cost = float(h.get("avgCostPrice") or 0)
        bank_code = h.get("bankCode", "")

        # 优先使用银行维度金价
        bank_price = _fetch_realtime_price_by_bank(bank_code)
        use_price = bank_price if bank_price is not None else default_price

        if use_price is not None:
            # 如果是第一个有银行金价的，更新realtimePrice为实际使用的价格
            if not price_available:
                price_available = True
                realtime_price = use_price
            pnl = (use_price - avg_cost) * gram
            total_pnl += pnl
            result["banks"].append({
                "bankCode": bank_code,
                "bankName": h.get("bankName") or h.get("bankCode") or "未知银行",
                "totalGram": gram,
                "avgCostPrice": avg_cost,
                "unrealizedPnl": round(pnl, 2),
                "realtimePrice": use_price,  # 该银行实际使用的金价
                "priceSource": "bank" if bank_price is not None else "default",
            })
        else:
            result["banks"].append({
                "bankCode": bank_code,
                "bankName": h.get("bankName") or h.get("bankCode") or "未知银行",
                "totalGram": gram,
                "avgCostPrice": avg_cost,
                "unrealizedPnl": None,  # 金价不可用，不计算
                "realtimePrice": None,
                "priceSource": None,
            })

    if price_available:
        result["priceAvailable"] = True
        result["realtimePrice"] = realtime_price

    result["totalUnrealizedPnl"] = round(total_pnl, 2)
    return result


def render_unrealized_pnl(result: dict) -> str:
    """渲染浮盈浮亏信息（Markdown 表格 + emoji）。

    金价不可用时，仅展示持仓信息，不展示浮盈浮亏。
    """
    banks = result.get("banks") or []
    total_gram = result.get("totalGram", 0.0)
    price_available = result.get("priceAvailable", False)
    realtime_price = result.get("realtimePrice")

    lines = ["## 💰 我的黄金持仓与浮动盈亏"]
    lines.append("")

    if not banks:
        lines.append("您当前暂无积存金持仓。")
        return "\n".join(lines)

    # ── 汇总 ──
    lines.append("### 📊 汇总")
    lines.append("")
    total_pnl = result.get("totalUnrealizedPnl")
    if price_available and total_pnl is not None:
        lines.append("| ⚖️ 总持仓(克) | 📉 参考金价(元/克) | 📈 总浮动盈亏(元) |")
        lines.append("| ---: | ---: | ---: |")
        price_cell = _fmt_num(realtime_price) if realtime_price is not None else "—"
        lines.append("| {g} | {p} | {pnl} |".format(
            g=_fmt_num(total_gram, 4), p=price_cell,
            pnl=_fmt_income(total_pnl, emoji=True)))
    else:
        lines.append("| ⚖️ 总持仓(克) | 📈 总浮动盈亏(元) |")
        lines.append("| ---: | ---: |")
        lines.append("| {g} | 当前无法获取实时金价，暂无法计算 |".format(
            g=_fmt_num(total_gram, 4)))
    lines.append("")

    # ── 各银行明细 ──
    lines.append("### 🏦 各银行明细")
    lines.append("")
    lines.append("| 🏦 银行 | ⚖️ 持仓(克) | 💵 成本均价(元/克) | 📈 实时金价(元/克) | 📊 浮动盈亏(元) |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for bank in banks:
        bank_rt_price = bank.get("realtimePrice")
        if bank_rt_price is not None:
            price_cell = _fmt_num(bank_rt_price)
            if bank.get("priceSource") == "bank":
                price_cell += "（{name}积存金）".format(name=bank["bankName"])
        else:
            price_cell = "—"
        pnl = bank.get("unrealizedPnl")
        pnl_cell = _fmt_income(pnl, emoji=True) if (price_available and pnl is not None) else "—"
        lines.append("| {name} | {g} | {c} | {p} | {pnl} |".format(
            name=bank["bankName"], g=_fmt_num(bank["totalGram"], 4),
            c=_fmt_num(bank["avgCostPrice"]), p=price_cell, pnl=pnl_cell))

    if not (price_available and result.get("totalUnrealizedPnl") is not None):
        lines.append("")
        lines.append("> ℹ️ 当前无法获取实时金价，暂无法计算浮动盈亏。")

    return "\n".join(lines)


# ── 持仓诊断分析 ──────────────────────────────────────────────


def _fetch_morning_report_data() -> Optional[dict]:
    """尝试获取最新一条早报数据，失败返回 None。

    从 articleList 中按 publishTime 降序排序，取最近一条。
    """
    try:
        import query_morning_report
        data = query_morning_report.fetch_morning_report(page_size=5)
        items = data.get("articleList") or data.get("list") or []
        if not items or not isinstance(items, list):
            return data if data else None
        # 按 publishTime 降序排序，取最新一条
        def _get_time(item):
            pt = item.get("publishTime", "")
            return pt or ""
        items_sorted = sorted(items, key=_get_time, reverse=True)
        return items_sorted[0]
    except Exception:
        pass
    return None


def _extract_usd_price_from_report(report: dict) -> Optional[float]:
    """从早报内容中提取美元/盎司金价，失败返回 None。

    早报内容示例：
    - "目前价格在4210美元附近"
    - "周线三连阴收4155美元"
    - "收报每盎司4155.44美元"
    - "现货黄金窄幅震荡于4160美元附近"

    提取策略：优先提取最新/当前价格（"目前""当前""今日"等），
    回退到历史价格（"收于""收报"等），最后取任意匹配。
    """
    content = report.get("content", "") or ""
    title = report.get("title", "") or ""
    full_text = content + " " + title
    import re

    # 所有匹配结果
    all_matches = []

    # 第一优先：目前/当前/今日...X美元（最新价格）
    current_patterns = [
        r'(?:目前|当前|今日|今天)[^。]*?(\d{3,5}(?:\.\d+)?)\s*美元',
        r'(\d{3,5}(?:\.\d+)?)\s*美元(?:附近|关口|上方|下方)',
    ]
    # 第二优先：每盎司/收报（近期收盘价）
    recent_patterns = [
        r'(?:收报|报|收于)?每盎司\s*(\d{3,5}(?:\.\d+)?)\s*美元',
        r'(\d{3,5}(?:\.\d+)?)\s*美元/盎司',
        r'(?:周线|月线|日线)[^。]*?收\s*(\d{3,5}(?:\.\d+)?)\s*美元',
    ]
    # 第三优先：COMEX
    fallback_patterns = [
        r'COMEX[^。]*?(\d{3,5}(?:\.\d+)?)',
    ]

    def _try_patterns(patterns):
        for pat in patterns:
            for m in re.finditer(pat, full_text):
                price_str = m.group(1).replace(",", "")
                try:
                    val = float(price_str)
                    if 500 <= val <= 20000:  # 合理范围：500-20000美元/盎司
                        return val
                except ValueError:
                    continue
        return None

    # 按优先级依次尝试
    result = _try_patterns(current_patterns)
    if result:
        return result
    result = _try_patterns(recent_patterns)
    if result:
        return result
    result = _try_patterns(fallback_patterns)
    return result


def _usd_per_ounce_to_cny_per_gram(usd_per_ounce: float) -> Optional[float]:
    """将美元/盎司转换为人民币/克（粗略估算）。

    使用固定汇率和单位换算：
    - 1 盎司 ≈ 31.1035 克
    - 美元/人民币汇率取近似值 7.25（仅供估算）
    - 公式：人民币/克 = 美元/盎司 × 汇率 / 31.1035

    注意：这是粗略估算，实际汇率有波动。返回值会标注为估算。
    """
    CNY_USD_RATE = 7.25
    OUNCE_TO_GRAM = 31.1035
    return round(usd_per_ounce * CNY_USD_RATE / OUNCE_TO_GRAM, 2)


def fetch_holdings_analysis() -> dict:
    """持仓诊断分析：综合持仓、收益、金价、早报给出诊断建议。

    返回 dict: {
        "holdings": dict,              # 持仓原始数据
        "incomeByBanks": dict,         # 各银行累计卖出收益
        "realtimePrice": float|None,   # 实时金价（元/克）
        "priceSource": str|None,       # 金价来源："api"=金价接口, "report"=早报估算, None=不可用
        "priceIsEstimate": bool,       # 金价是否为估算值（早报换算）
        "morningReport": dict|None,    # 早报数据
        "banks": [{                    # 各银行持仓+收益+浮盈浮亏
            "bankCode": str,
            "bankName": str,
            "totalGram": float,
            "avgCostPrice": float,
            "totalIncome": float,      # 累计卖出收益
            "unrealizedPnl": float|None, # 浮动盈亏（金价不可用时为None）
        }, ...],
        "totalGram": float,
        "totalCost": float,            # 总成本（元）
        "totalIncome": float,          # 总累计卖出收益（元）
        "totalUnrealizedPnl": float|None,
        "pnlPercent": float|None,      # 浮盈浮亏百分比
        "diagnosis": dict,             # 诊断结论
    }
    """
    # 1. 获取持仓数据
    holdings_data = jos.fetch_holdings()
    holding_list = holdings_data.get("holdingList") or []
    active = [h for h in holding_list if float(h.get("totalGram") or 0) > 0]
    total_gram = float(holdings_data.get("totalGramAll") or 0)

    # 2. 获取各银行累计卖出收益
    income_result = {"fromAll": 0.0, "banks": []}
    try:
        income_result = fetch_income_by_banks(time_type="year")
    except Exception:
        pass  # 收益查询失败不阻断分析

    # 3. 获取实时金价（优先金价接口按银行维度查询，回退早报估算）
    realtime_price = None
    price_source = None
    price_is_estimate = False
    report_data = None

    # 3a. 尝试默认金价接口（京东24h金价指数）
    default_price = _fetch_realtime_price_cny()
    if default_price is not None:
        realtime_price = default_price
        price_source = "api"
    else:
        # 3b. 金价接口不可用，尝试从早报提取美元/盎司换算
        report_data = _fetch_morning_report_data()
        if report_data:
            usd_price = _extract_usd_price_from_report(report_data)
            if usd_price:
                realtime_price = _usd_per_ounce_to_cny_per_gram(usd_price)
                if realtime_price:
                    price_source = "report"
                    price_is_estimate = True

    report_for_output = report_data

    # 4. 组装各银行数据
    income_map = {b["bankCode"]: b["income"] for b in income_result.get("banks", [])}
    banks = []
    total_cost = 0.0
    total_unrealized = 0.0
    total_income = 0.0

    for h in active:
        gram = float(h.get("totalGram") or 0)
        avg_cost = float(h.get("avgCostPrice") or 0)
        bank_cost = avg_cost * gram
        total_cost += bank_cost
        bank_code = h.get("bankCode", "")
        bank_income = income_map.get(bank_code, 0.0)
        total_income += bank_income

        # 优先使用银行维度金价，回退到默认金价
        bank_price = None
        bank_price_source = None
        if bank_code:
            bank_price = _fetch_realtime_price_by_bank(bank_code)
            if bank_price is not None:
                bank_price_source = "bank"

        use_price = bank_price if bank_price is not None else realtime_price

        bank_pnl = None
        if use_price is not None:
            bank_pnl = round((use_price - avg_cost) * gram, 2)
            total_unrealized += bank_pnl
            if price_source is None and bank_price_source == "bank":
                price_source = "api"

        banks.append({
            "bankCode": bank_code,
            "bankName": h.get("bankName") or h.get("bankCode") or "未知银行",
            "totalGram": gram,
            "avgCostPrice": avg_cost,
            "totalIncome": bank_income,
            "unrealizedPnl": bank_pnl,
            "realtimePrice": use_price,
            "priceSource": bank_price_source or (price_source if use_price else None),
        })

    # 5. 计算浮盈浮亏百分比
    pnl_percent = None
    if total_cost > 0 and realtime_price is not None:
        pnl_percent = round((total_unrealized / total_cost) * 100, 2)

    # 6. 四维诊断
    diagnosis = _diagnose(total_gram, total_cost, total_unrealized, pnl_percent,
                          realtime_price, banks)

    return {
        "holdings": holdings_data,
        "incomeByBanks": income_result,
        "realtimePrice": realtime_price,
        "priceSource": price_source,
        "priceIsEstimate": price_is_estimate,
        "morningReport": report_for_output,
        "banks": banks,
        "totalGram": total_gram,
        "totalCost": round(total_cost, 2),
        "totalIncome": round(total_income, 2),
        "totalUnrealizedPnl": round(total_unrealized, 2) if realtime_price is not None else None,
        "pnlPercent": pnl_percent,
        "diagnosis": diagnosis,
    }


def _diagnose(total_gram: float, total_cost: float,
              total_unrealized: float, pnl_percent: Optional[float],
              realtime_price: Optional[float], banks: list) -> dict:
    """四维诊断框架：仓位占比、持有时长、交易风格、浮盈浮亏 → 场景匹配+建议。"""
    # 维度1：仓位占比（无法获取用户总资产，仅做持仓金额判断）
    position_level = "unknown"
    if total_cost > 0:
        if total_cost <= 50000:
            position_level = "light"
        elif total_cost <= 200000:
            position_level = "medium"
        else:
            position_level = "heavy"

    # 维度2：浮盈浮亏状态
    pnl_status = "unknown"
    if total_unrealized is not None and realtime_price is not None:
        if pnl_percent is not None:
            if pnl_percent > 5:
                pnl_status = "profit"
            elif pnl_percent < -5:
                pnl_status = "loss"
            else:
                pnl_status = "neutral"
        else:
            pnl_status = "neutral"

    # 维度3：成本分布（多银行对比，判断是否分散）
    cost_spread = len([b for b in banks if b["totalGram"] > 0])
    is_concentrated = cost_spread <= 1 and total_gram > 0

    # 维度4：各银行盈亏详情
    bank_pnl_details = []
    for b in banks:
        if b.get("unrealizedPnl") is not None:
            bank_pnl_details.append(b)

    # 场景匹配
    scenario = "unknown"
    advice = []
    mindset = ""

    if pnl_status == "loss" and position_level in ("light", "medium"):
        scenario = "light_position_loss"
        advice = [
            "短期波动无需过度焦虑，黄金作为避险资产具有长期配置价值",
            "可考虑逢回调小额定投摊薄成本",
            "无需恐慌止损，耐心等待反弹",
        ]
        mindset = "短期浮亏但仓位可控，时间站在你这边，保持定力"
    elif pnl_status == "profit" and position_level in ("light", "medium"):
        scenario = "light_position_profit"
        advice = [
            "当前浮盈状态良好，可继续持有",
            "如金价涨幅超过成本20%以上，可考虑部分止盈，但保留核心底仓",
            "关注市场信号，设置合理的止盈目标",
        ]
        mindset = "理想状态，保持纪律，不因短期盈利而过度加仓"
    elif pnl_status == "loss" and position_level == "heavy":
        scenario = "heavy_position_loss"
        advice = [
            "不建议恐慌性割肉，但需控制仓位风险",
            "暂停新增投入，等待反弹后逐步减仓",
            "利用定投纪律化降仓，避免情绪化决策",
        ]
        mindset = "仓位偏重但短期浮亏，需要耐心和纪律，避免追跌"
    elif pnl_status == "profit" and position_level == "heavy":
        scenario = "heavy_position_profit"
        advice = [
            "优先减仓，将黄金仓位降至合理水平",
            "分批止盈落袋为安，保留底仓享受长期趋势",
            "释放资金配置其他资产，降低集中度风险",
        ]
        mindset = "盈利但风险暴露过高，及时锁定利润是最明智的选择"
    elif pnl_status == "neutral":
        scenario = "neutral_position"
        advice = [
            "当前持仓成本接近市场价，风险相对均衡",
            "可继续持有观察，关注市场方向信号",
            "保持定投节奏，等待趋势明确后再做决策",
        ]
        mindset = "持仓成本合理，无需急于操作，耐心等待机会"
    elif pnl_status == "unknown" and realtime_price is None:
        scenario = "price_unavailable"
        advice = [
            "无法获取实时金价，建议关注最新金价走势后再做决策",
            "可查看今日黄金早报了解市场动态",
            "避免在信息不充分时做出交易决策",
        ]
        mindset = "信息不足时，观望是最好的策略"

    return {
        "positionLevel": position_level,
        "pnlStatus": pnl_status,
        "isConcentrated": is_concentrated,
        "scenario": scenario,
        "advice": advice,
        "mindset": mindset,
        "bankPnlDetails": bank_pnl_details,
    }


def render_holdings_analysis(result: dict) -> str:
    """渲染持仓诊断分析结果（Markdown 表格 + emoji）。"""
    lines = ["## 🩺 黄金持仓诊断分析"]

    total_gram = result.get("totalGram", 0.0)
    total_cost = result.get("totalCost", 0.0)
    total_income = result.get("totalIncome", 0.0)
    total_unrealized = result.get("totalUnrealizedPnl")
    pnl_percent = result.get("pnlPercent")
    realtime_price = result.get("realtimePrice")
    price_source = result.get("priceSource")
    price_is_estimate = result.get("priceIsEstimate", False)
    banks = result.get("banks") or []
    diagnosis = result.get("diagnosis") or {}
    report = result.get("morningReport")

    # ── 一、持仓概览 ──
    lines.append("")
    lines.append("### 一、📊 持仓概览")
    lines.append("")
    lines.append("| 项目 | 数值 |")
    lines.append("| --- | ---: |")
    lines.append("| ⚖️ 总持仓 | **{g} 克** |".format(g=_fmt_num(total_gram, 4)))
    lines.append("| 💵 总成本 | {c} 元 |".format(c=_fmt_num(total_cost)))
    lines.append("| 💰 累计卖出收益 | **{i} 元** |".format(i=_fmt_income(total_income)))
    if realtime_price is not None:
        price_label = _fmt_num(realtime_price)
        if price_is_estimate:
            price_label += "（早报美元/盎司换算估算）"
        lines.append("| 📉 参考金价 | {p} 元/克 |".format(p=price_label))
    if total_unrealized is not None:
        lines.append("| 📈 浮动盈亏 | **{pnl} 元** |".format(
            pnl=_fmt_income(total_unrealized, emoji=True)))
    if pnl_percent is not None:
        lines.append("| 📊 浮盈浮亏比 | **{pct}%** |".format(pct=_fmt_income(pnl_percent)))

    # ── 二、各银行明细 ──
    if banks:
        lines.append("")
        lines.append("### 二、🏦 各银行明细")
        lines.append("")
        lines.append("| 🏦 银行 | ⚖️ 持仓(克) | 💵 成本均价(元/克) | 📈 实时金价(元/克) | 💰 累计卖出收益(元) | 📊 浮动盈亏(元) |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for bank in banks:
            bank_rt_price = bank.get("realtimePrice")
            bank_price_src = bank.get("priceSource")
            if bank_rt_price is not None:
                price_cell = _fmt_num(bank_rt_price)
                if bank_price_src == "bank":
                    price_cell += "（{name}积存金）".format(name=bank["bankName"])
                elif price_is_estimate:
                    price_cell += "（早报估算）"
            else:
                price_cell = "—"
            pnl = bank.get("unrealizedPnl")
            pnl_cell = _fmt_income(pnl, emoji=True) if pnl is not None else "—"
            lines.append("| {name} | {g} | {c} | {p} | {inc} | {pnl} |".format(
                name=bank["bankName"], g=_fmt_num(bank["totalGram"], 4),
                c=_fmt_num(bank["avgCostPrice"]), p=price_cell,
                inc=_fmt_income(bank["totalIncome"]), pnl=pnl_cell))

    # ── 三、市场参考 ──
    if report:
        lines.append("")
        lines.append("### 三、市场参考（黄金早报）")
        title = report.get("title", "")
        content = report.get("content", "")
        if title:
            lines.append("- 📅 {title}".format(title=title))
        # 提取关键要点（截取前200字）
        if content:
            short = content[:200].replace("\n", " ").strip()
            if len(content) > 200:
                short += "..."
            lines.append("- {content}".format(content=short))
        jump_url = report.get("jumpUrl")
        if jump_url:
            lines.append("- 查看完整早报：{url}".format(url=jump_url))
        lines.append("")
        lines.append("> （注：早报金价多为美元/盎司，仅作市场趋势参考，不用于元/克口径的浮盈计算）")

    # ── 四、诊断结论与建议 ──
    lines.append("")
    lines.append("### 四、诊断结论与建议")

    scenario = diagnosis.get("scenario", "unknown")
    advice_list = diagnosis.get("advice", [])
    mindset = diagnosis.get("mindset", "")

    # 一句话诊断
    scenario_labels = {
        "light_position_loss": "轻仓浮亏",
        "light_position_profit": "轻仓浮盈",
        "heavy_position_loss": "重仓浮亏",
        "heavy_position_profit": "重仓浮盈",
        "neutral_position": "成本接近平价",
        "price_unavailable": "金价暂不可用",
        "unknown": "待定",
    }
    label = scenario_labels.get(scenario, "待定")
    lines.append("- **诊断**：{label}".format(label=label))

    if mindset:
        lines.append("- **心态建议**：{mindset}".format(mindset=mindset))

    if advice_list:
        lines.append("- **操作建议**：")
        for i, a in enumerate(advice_list, 1):
            lines.append("  {idx}. {advice}".format(idx=i, advice=a))

    # ── 五、风险提示 ──
    lines.append("")
    lines.append("### 五、风险提示")
    lines.append("- 以上分析仅供参考，不构成投资建议")
    lines.append("- 黄金价格受国际政治、经济等多重因素影响，存在波动风险")
    lines.append("- 投资决策请结合个人风险承受能力谨慎做出")
    if price_is_estimate:
        lines.append("- 当前金价为早报美元/盎司换算估算值，与实际积存金价格可能存在偏差")

    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────

QUERY_MODES = ("summary", "detail-month", "detail-day", "unrealized-pnl", "analysis")


def main(argv=None):
    parser = argparse.ArgumentParser(description="黄金收益日历查询")
    parser.add_argument(
        "--mode",
        choices=QUERY_MODES,
        default="summary",
        help="查询模式：summary=按银行汇总，detail-month=月度明细，detail-day=日明细，unrealized-pnl=浮动盈亏，analysis=持仓诊断",
    )
    parser.add_argument(
        "--time-type",
        choices=("day", "week", "year"),
        default="year",
        help="时间维度（summary 默认 year）",
    )
    parser.add_argument(
        "--time",
        dest="time_value",
        help="时间值：day/week→yyyyMM，year→yyyy",
    )
    parser.add_argument("--start-month", help="月明细起始月（yyyyMM）")
    parser.add_argument("--end-month", help="月明细结束月（yyyyMM）")
    parser.add_argument("--month", help="日明细月份（yyyyMM）")
    parser.add_argument("--trade-type", default="1", help="交易类型（默认 1）")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args(argv)
    bff_client.set_claw(args.claw)

    # ── summary 模式：按银行汇总 ──
    if args.mode == "summary":
        try:
            result = fetch_income_by_banks(
                time_type=args.time_type,
                time_value=args.time_value,
                trade_type=args.trade_type,
            )
        except urllib.error.URLError as e:
            print("[内部] 网络错误: %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)
        except RuntimeError as e:
            if getattr(e, "code", None) == 403:
                print(e.message, file=sys.stderr)
                sys.exit(3)
            print("[内部] %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(render_income_by_banks(result))
        sys.exit(0)

    # ── detail-month 模式：月度明细 ──
    elif args.mode == "detail-month":
        now = datetime.now()
        start = args.start_month or now.strftime("%Y01")
        end = args.end_month or now.strftime("%Y%m")

        try:
            results = fetch_income_detail_months(start, end, args.trade_type)
        except urllib.error.URLError as e:
            print("[内部] 网络错误: %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)
        except RuntimeError as e:
            if getattr(e, "code", None) == 403:
                print(e.message, file=sys.stderr)
                sys.exit(3)
            print("[内部] %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(render_income_detail_months(results))
        sys.exit(0)

    # ── detail-day 模式：日明细 ──
    elif args.mode == "detail-day":
        month_str = args.month or datetime.now().strftime("%Y%m")

        try:
            day_list = fetch_income_detail_days(month_str, args.trade_type)
        except urllib.error.URLError as e:
            print("[内部] 网络错误: %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)
        except RuntimeError as e:
            if getattr(e, "code", None) == 403:
                print(e.message, file=sys.stderr)
                sys.exit(3)
            print("[内部] %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)

        if args.json:
            print(json.dumps(day_list, ensure_ascii=False, indent=2))
        else:
            print(render_income_detail_days(day_list, month_str))
        sys.exit(0)

    # ── unrealized-pnl 模式：浮动盈亏 ──
    elif args.mode == "unrealized-pnl":
        try:
            result = fetch_unrealized_pnl()
        except urllib.error.URLError as e:
            print("[内部] 网络错误: %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)
        except RuntimeError as e:
            if getattr(e, "code", None) == 403:
                print(e.message, file=sys.stderr)
                sys.exit(3)
            print("[内部] %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(render_unrealized_pnl(result))
        sys.exit(0)

    # ── analysis 模式：持仓诊断分析 ──
    elif args.mode == "analysis":
        try:
            result = fetch_holdings_analysis()
        except urllib.error.URLError as e:
            print("[内部] 网络错误: %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)
        except RuntimeError as e:
            if getattr(e, "code", None) == 403:
                print(e.message, file=sys.stderr)
                sys.exit(3)
            print("[内部] %s" % e, file=sys.stderr)
            print("查询暂时失败，请稍后重试", file=sys.stderr)
            sys.exit(3)

        if args.json:
            # JSON模式输出精简版（去掉holdings原始数据）
            output = {k: v for k, v in result.items() if k != "holdings"}
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(render_holdings_analysis(result))
        sys.exit(0)


if __name__ == "__main__":
    main()