#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""金价查询：通过 cf-gold-ai BFF /api/v1/price/query 调用。

uniqueCode 说明（内部使用，不对客展示）：
  - WG-JDAU：京东24h金价（结合暗金、伦敦金、au9999），默认金价查询
  - WG-PAXGUSD：现货黄金（暗金参考价）
  - WG-XAUUSD：伦敦金（现货黄金）
  - SGE-Au99.99：黄金9999
  - 银行积存金：
    - CMBC-JCJ：民生银行积存金
    - CZB-JCJ：浙商银行积存金
    - CIB-JCJ0：兴业银行积存金（买入价）
    - CGB-JCJ0：广发银行积存金（买入价）
    - ICBC-JCJ：工商银行积存金
    - CNCB-JCJ：中信银行积存金
    - SPDB-JCJ0：浦发银行积存金（买入价）
"""
import argparse
import json
import sys
import re
import urllib.error
from datetime import datetime
from typing import Optional

import bff_client
import jos

# ── uniqueCode 映射表 ─────────────────────────────────────────────

# 银行 code → uniqueCode（用于浮盈浮亏按银行维度查询）
BANK_UNIQUE_CODE_MAP = {
    "CMBC": "CMBC-JCJ",     # 民生银行积存金
    "CZB":  "CZB-JCJ",      # 浙商银行积存金
    "CIB":  "CIB-JCJ0",     # 兴业银行积存金（买入价）
    "CGB":  "CGB-JCJ0",     # 广发银行积存金（买入价）
    "ICBC": "ICBC-JCJ",     # 工商银行积存金
    "CITIC": "CNCB-JCJ",    # 中信银行积存金
    "SPDB": "SPDB-JCJ0",    # 浦发银行积存金（买入价）
}

# 银行 code → 银行名称
BANK_NAME_MAP = {
    "CMBC": "民生银行",
    "CZB":  "浙商银行",
    "CIB":  "兴业银行",
    "CGB":  "广发银行",
    "ICBC": "工商银行",
    "CITIC": "中信银行",
    "SPDB": "浦发银行",
}

# uniqueCode → 显示名称（通用金价查询）
UNIQUE_CODE_LABEL = {
    "WG-JDAU":    "京东24h金价",
    "WG-PAXGUSD": "PAXGUSD暗金",
    "WG-XAUUSD":  "伦敦金（现货黄金）",
    "SGE-Au99.99": "黄金9999",
    "CMBC-JCJ":   "民生银行积存金",
    "CZB-JCJ":    "浙商银行积存金",
    "CIB-JCJ0":   "兴业银行积存金（买入价）",
    "CGB-JCJ0":   "广发银行积存金（买入价）",
    "ICBC-JCJ":   "工商银行积存金",
    "CNCB-JCJ":   "中信银行积存金",
    "SPDB-JCJ0":  "浦发银行积存金（买入价）",
}

# 用户关键词 → uniqueCode
KEYWORD_MAP = {
    # 通用金价
    r"京东.*金价|24h.*金价|综合金价": "WG-JDAU",
    r"暗金|PAXGUSD|PAXG": "WG-PAXGUSD",
    r"伦敦金|现货黄金|国际金价|XAUUSD": "WG-XAUUSD",
    r"黄金9999|au9999|Au99|沪金现货": "SGE-Au99.99",
    # 银行积存金
    r"民生|CMBC": "CMBC-JCJ",
    r"浙商|CZB": "CZB-JCJ",
    r"兴业|CIB": "CIB-JCJ0",
    r"广发|CGB": "CGB-JCJ0",
    r"工商|工行|ICBC": "ICBC-JCJ",
    r"中信|CITIC|CNCB": "CNCB-JCJ",
    r"浦发|SPDB": "SPDB-JCJ0",
}


# ── 底层接口调用 ───────────────────────────────────────────────────

def _call_price_jhub(unique_code: str) -> Optional[dict]:
    """调用 BFF 金价接口，返回业务 data。"""
    access_token = jos._valid_access_token()
    return bff_client.get(
        bff_client.PATH_PRICE_QUERY,
        {"uniqueCode": unique_code, "accessToken": access_token},
    )


# ── 对外接口 ──────────────────────────────────────────────────────


def fetch_price(unique_code: str = "WG-JDAU") -> Optional[dict]:
    """查询金价，返回 SimpleQuote 数据 dict 或 None。

    返回 dict 包含：
      - uniqueCode: 证券唯一码
      - name: 证券简称
      - lastPrice: 最新价
      - raisePercent: 涨跌幅（小数，如 0.01 表示 1%）
      - raise: 涨跌额
      - preClose: 昨日收盘价
      - openPrice: 今日开盘价
      - highPrice: 最高价
      - lowPrice: 最低价
      - tradeDateTime: 交易时间（ISO 字符串，如 "2023-03-22T09:45:29.820"）
    """
    result = _call_price_jhub(unique_code)
    if result is None:
        return None
    # 接口 data 可能是数组（含单个元素），取第一个
    if isinstance(result, list):
        return result[0] if result else None
    return result


def fetch_price_by_bank(bank_code: str) -> Optional[dict]:
    """根据银行 code 查询该银行积存金金价。

    银行 code 映射到 uniqueCode，如 CMBC → CMBC-JCJ。
    如果银行无对应 uniqueCode，返回 None。
    """
    unique_code = BANK_UNIQUE_CODE_MAP.get(bank_code)
    if not unique_code:
        return None
    return fetch_price(unique_code)


def fetch_default_price() -> Optional[dict]:
    """查询默认金价（京东24h金价指数 WG-JDAU）。"""
    return fetch_price("WG-JDAU")


# ── 解析用户关键词 ──────────────────────────────────────────────


def parse_unique_code(text: str) -> tuple:
    """从用户原文解析 uniqueCode。

    返回 (unique_code: str|None, status: str)
      status: "ok" = 匹配到具体标的
              "missing" = 通用金价查询但未指定具体标的
              "unsupported" = 不支持的标的
    """
    text = text.strip()
    if not text:
        return None, "missing"

    # 精确匹配银行/标的关键词
    for pattern, unique_code in KEYWORD_MAP.items():
        if re.search(pattern, text, re.I):
            return unique_code, "ok"

    # 通用金价查询词
    generic_patterns = [
        r"查询金价", r"金价查询", r"金价",
        r"查(?:一下|下)?(?:今天|当前|实时)?金价",
        r"黄金价格", r"黄金多少钱", r"金价多少",
    ]
    for pat in generic_patterns:
        if re.search(pat, text):
            return None, "missing"

    # 包含金价/黄金但无法匹配
    if re.search(r"金价|黄金", text):
        return None, "missing"

    return None, "unsupported"


# ── 格式化与渲染 ──────────────────────────────────────────────────


def _fmt_change(v) -> str:
    if v is None:
        return "—"
    try:
        n = float(v)
        sign = "+" if n > 0 else ""
        return f"{sign}{n:.2f}"
    except (TypeError, ValueError):
        return str(v)


def _fmt_pct(v) -> str:
    if v is None:
        return "—"
    try:
        n = float(v) * 100
        sign = "+" if n > 0 else ""
        return f"{sign}{n:.2f}%"
    except (TypeError, ValueError):
        return str(v)


def _fmt_price(v) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return str(v)


def _direction(v) -> tuple:
    """根据涨跌额判断方向，返回 (方向词, 文字)。红涨绿跌以文字标注方向，不用箭头。"""
    try:
        n = float(v)
    except (TypeError, ValueError):
        return "", ""
    if n > 0:
        return "涨", "涨"
    if n < 0:
        return "跌", "跌"
    return "平", "平"


def _dir_emoji(v) -> str:
    """红涨绿跌方向 emoji：涨🔴 跌🟢 平⚪，无数据返回空串（不使用 HTML span，避免富文本外泄）。"""
    try:
        n = float(v)
    except (TypeError, ValueError):
        return ""
    if n > 0:
        return "🔴"
    if n < 0:
        return "🟢"
    return "⚪"


def render_price(quote: dict, unique_code: str = "") -> str:
    """渲染金价信息（含开/收/高/低，红涨绿跌方向标注）。"""
    label = UNIQUE_CODE_LABEL.get(unique_code, quote.get("name", ""))
    name = quote.get("name", label) or label
    last_price = quote.get("lastPrice")
    raise_pct = quote.get("raisePercent")
    raise_val = quote.get("raise")
    pre_close = quote.get("preClose")
    # 接口未返回涨跌额时，用最新价 - 昨收兜底计算
    if raise_val is None and last_price is not None and pre_close is not None:
        try:
            raise_val = float(last_price) - float(pre_close)
        except (TypeError, ValueError):
            raise_val = None
    open_price = quote.get("openPrice")
    high_price = quote.get("highPrice")
    low_price = quote.get("lowPrice")
    trade_time = quote.get("tradeDateTime", "")

    # 判断单位：银行积存金/京东24h金价是人民币/克，国际金价是美元/盎司
    is_intl = unique_code.startswith("WG-") and unique_code not in ("WG-JDAU",)
    unit = "美元/盎司" if is_intl else "元/克"

    arrow, word = _direction(raise_val)
    lines = [f"【{name}】"]
    if last_price is not None:
        lines.append(f"实时价格：{_fmt_price(last_price)} {unit}")
    else:
        lines.append("实时价格：暂无数据")
    # 红涨绿跌：正负号即方向（+涨-跌），emoji 标注方向（🔴涨/🟢跌），不使用 HTML span
    _pct = _fmt_pct(raise_pct)
    _emoji = _dir_emoji(raise_val)
    lines.append(f"涨跌幅：{(_emoji + ' ' + _pct) if _emoji else _pct}")
    lines.append(f"涨跌额：{_fmt_change(raise_val)}")
    lines.append(f"今开：{_fmt_price(open_price)}  昨收：{_fmt_price(pre_close)}")
    lines.append(f"最高：{_fmt_price(high_price)}   最低：{_fmt_price(low_price)}")

    if trade_time and isinstance(trade_time, str):
        t = trade_time.replace("T", " ")
        lines.append(f"交易时间：{t}")

    return "\n".join(lines)


def analyze_price(quote: dict, unique_code: str = "") -> str:
    """基于实时行情做简易金价走势分析（不预测、不编造，仅解读当日数据）。"""
    label = UNIQUE_CODE_LABEL.get(unique_code, quote.get("name", ""))
    name = quote.get("name", label) or label

    def _f(k):
        try:
            return float(quote.get(k))
        except (TypeError, ValueError):
            return None

    last = _f("lastPrice")
    pre = _f("preClose")
    op = _f("openPrice")
    hi = _f("highPrice")
    lo = _f("lowPrice")
    raise_pct = _f("raisePercent")

    arrow, word = _direction(quote.get("raise"))
    lines = [f"【{name} · 走势分析】"]

    # 相对昨收的整体方向
    if raise_pct is not None:
        mag = abs(raise_pct) * 100
        if mag < 0.2:
            trend = "基本平盘，波动很小"
        elif mag < 1:
            trend = f"温和{word}"
        elif mag < 2:
            trend = f"明显{word}"
        else:
            trend = f"大幅{word}"
        lines.append(f"当日整体：较昨收{trend}（{_fmt_pct(quote.get('raisePercent'))}）。")

    # 日内振幅
    if hi is not None and lo is not None and pre:
        amp = (hi - lo) / pre * 100
        lines.append(f"日内振幅：{amp:.2f}%（最高 {_fmt_price(hi)} / 最低 {_fmt_price(lo)}）。")

    # 开盘后走势 & 当前位置
    if last is not None and op is not None:
        if last > op:
            lines.append("开盘后走高，多头占优。")
        elif last < op:
            lines.append("开盘后走低，空头占优。")
        else:
            lines.append("现价与开盘持平。")
    if last is not None and hi is not None and lo is not None and hi != lo:
        pos = (last - lo) / (hi - lo) * 100
        if pos >= 70:
            lines.append(f"现价处于日内高位区（约 {pos:.0f}%），接近当日最高。")
        elif pos <= 30:
            lines.append(f"现价处于日内低位区（约 {pos:.0f}%），接近当日最低。")
        else:
            lines.append(f"现价处于日内中部区间（约 {pos:.0f}%）。")

    lines.append("提示：以上为当日实时数据解读，非投资建议，金价受多重因素影响。")
    return "\n".join(lines)


# ── 行情速览（未指定标的时的默认输出）─────────────────────────────

# 现货/期货组：显示名 → uniqueCode（顺序即展示顺序）
OVERVIEW_SPOT = [
    ("黄金9999（上金所）", "SGE-Au99.99"),
    ("伦敦金", "WG-XAUUSD"),
    ("京东24h金价", "WG-JDAU"),
]

# 积存金组：显示名 → uniqueCode
OVERVIEW_JCJ = [
    ("浙商积存金", "CZB-JCJ"),
    ("民生积存金", "CMBC-JCJ"),
    ("兴业积存金", "CIB-JCJ0"),
]


def _overview_quote(unique_code: str) -> Optional[dict]:
    """安全查询单个标的，失败返回 None（不使整体速览失败）。

    BFF 接口偶发 code=-1 业务请求异常，故内建最多 5 次重试。
    """
    for _ in range(5):
        try:
            q = fetch_price(unique_code)
            if q:
                return q
        except (urllib.error.URLError, bff_client.BffError, RuntimeError):
            continue
    return None


def _row_change(quote: dict):
    """从行情计算涨跌额（接口无 raise 字段时用 lastPrice-preClose 兜底）。"""
    raise_val = quote.get("raise")
    last_price = quote.get("lastPrice")
    pre_close = quote.get("preClose")
    if raise_val is None and last_price is not None and pre_close is not None:
        try:
            raise_val = float(last_price) - float(pre_close)
        except (TypeError, ValueError):
            raise_val = None
    return raise_val


def _is_closed(quote: dict) -> bool:
    """现货类休市判断：最新价==开盘==昨收且无日内高低波动，视为休市/未开盘。"""
    def _f(k):
        try:
            return float(quote.get(k))
        except (TypeError, ValueError):
            return None
    last, op, pre = _f("lastPrice"), _f("openPrice"), _f("preClose")
    hi, lo = _f("highPrice"), _f("lowPrice")
    if last is None or pre is None:
        return False
    same_price = (op is None or last == op) and last == pre
    no_range = (hi is None or lo is None or hi == lo)
    return same_price and no_range


def render_market_overview(date: Optional[str] = None) -> str:
    """渲染黄金行情速览（未指定标的时的默认输出）。

    分两组：黄金基础行情组 + 积存金组，末尾统一整段总结描述金价总体走势。
    单个标的查询失败以「—」占位，不使整体失败。
    """
    if date is None:
        now = datetime.now()
        date = f"{now.year}年{now.month}月{now.day}日"

    lines = [f"📊 {date} 黄金行情速览", ""]

    # ── 第一组：黄金基础行情 ──────────────────────────
    lines.append("一、黄金基础行情")
    lines.append("")
    lines.append("| 品种 | 最新价 | 涨跌额 | 涨跌幅 | 今开 | 昨收 | 最高 | 最低 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    closed_names = []
    spot_dirs = []
    for name, code in OVERVIEW_SPOT:
        q = _overview_quote(code)
        if not q:
            lines.append(f"| {name} | — | — | — | — | — | — | — |")
            continue
        is_intl = code.startswith("WG-") and code != "WG-JDAU"
        unit = "美元/盎司" if is_intl else "元/克"
        last = _fmt_price(q.get("lastPrice"))
        chg = _fmt_change(_row_change(q))
        pct = _fmt_pct(q.get("raisePercent"))
        emoji = _dir_emoji(_row_change(q))
        pct_cell = f"{emoji} {pct}".strip() if emoji else pct
        op = _fmt_price(q.get("openPrice"))
        pre = _fmt_price(q.get("preClose"))
        hi = _fmt_price(q.get("highPrice"))
        lo = _fmt_price(q.get("lowPrice"))
        lines.append(f"| {name}（{unit}） | {last} | {chg} | {pct_cell} | {op} | {pre} | {hi} | {lo} |")
        # 京东24h金价7×24h报价，不判休市
        if code != "WG-JDAU" and _is_closed(q):
            closed_names.append(name)
        arrow, word = _direction(_row_change(q))
        if word:
            spot_dirs.append(word)

    lines.append("")
    lines.append("📝 **说明：** 京东24h金价拟合了黄金9999、伦敦金、暗金（PAXG）等标的，实现 7×24 小时连续报价，无休市。")
    if closed_names:
        lines.append(f"⏰ **提示：** {('、'.join(closed_names))}当前为休市时间，展示的为最近一次收盘/参考价，非实时行情。")
    lines.append("")

    # ── 第二组：黄金积存金 ────────────────────────────
    lines.append("二、黄金积存金实时行情")
    lines.append("")
    lines.append("| 品种 | 最新价 | 涨跌额 | 涨跌幅 | 今开 | 昨收 | 最高 | 最低 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    jcj_dirs = []
    for name, code in OVERVIEW_JCJ:
        q = _overview_quote(code)
        if not q:
            lines.append(f"| {name} | — | — | — | — | — | — | — |")
            continue
        last = _fmt_price(q.get("lastPrice"))
        chg = _fmt_change(_row_change(q))
        pct = _fmt_pct(q.get("raisePercent"))
        emoji = _dir_emoji(_row_change(q))
        pct_cell = f"{emoji} {pct}".strip() if emoji else pct
        op = _fmt_price(q.get("openPrice"))
        pre = _fmt_price(q.get("preClose"))
        hi = _fmt_price(q.get("highPrice"))
        lo = _fmt_price(q.get("lowPrice"))
        lines.append(f"| {name}（元/克） | {last} | {chg} | {pct_cell} | {op} | {pre} | {hi} | {lo} |")
        arrow, word = _direction(_row_change(q))
        if word:
            jcj_dirs.append(word)

    lines.append("")
    # 末尾统一整段小结：综合两组涨跌方向描述金价总体走势
    up_all = spot_dirs.count("涨") + jcj_dirs.count("涨")
    down_all = spot_dirs.count("跌") + jcj_dirs.count("跌")
    if up_all and not down_all:
        trend = "今日黄金整体走强，基础标的与积存金普遍上涨，市场做多情绪偏强，短线金价重心上移。"
    elif down_all and not up_all:
        trend = "今日黄金整体走弱，基础标的与积存金普遍回落，市场观望情绪升温，短线金价承压下行。"
    elif up_all and down_all:
        trend = "今日黄金涨跌互现，基础标的与积存金走势分化，市场多空交织，短线以震荡整理为主。"
    else:
        trend = "今日黄金整体波动有限，基础标的与积存金基本维持平盘，市场缺乏明确方向，短线以观望为主。"
    lines.append(f"💡 **小结：** {trend}")
    lines.append("")
    lines.append("📝 **提示：** 以上为实时行情数据，非投资建议，金价受多重因素影响。")

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────


def main(argv=None):
    p = argparse.ArgumentParser(description="通过 JHub 网关查询金价")
    p.add_argument("unique_code", nargs="?", default="WG-JDAU",
                   help="证券唯一码，如 WG-JDAU、CMBC-JCJ 等（默认 WG-JDAU）")
    p.add_argument("--parse", "-p", metavar="TEXT", help="从用户原文解析金价标的")
    p.add_argument("--bank", metavar="BANK_CODE", help="按银行 code 查询（如 CMBC、CZB）")
    p.add_argument("--json", action="store_true", help="输出原始 JSON")
    p.add_argument("--analyze", "-a", action="store_true", help="输出金价走势分析")
    p.add_argument("--overview", action="store_true", help="输出黄金行情速览（现货/期货组 + 积存金组）")
    p.add_argument("--list", action="store_true", help="列出所有支持的 uniqueCode（内部调试用，勿对客展示）")
    p.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = p.parse_args(argv)
    bff_client.set_claw(args.claw)

    if args.list:
        print("支持的 uniqueCode：")
        for code, label in UNIQUE_CODE_LABEL.items():
            print(f"  {code:15s} {label}")
        return 0

    if args.overview:
        print(render_market_overview())
        return 0

    unique_code = args.unique_code

    if args.parse is not None:
        uc, status = parse_unique_code(args.parse)
        if status == "missing":
            # 未指定具体标的：输出黄金行情速览（现货/期货 + 积存金）
            print(render_market_overview())
            return 0
        if status == "unsupported":
            print("暂不支持您要查询的黄金标的")
            return 2
        unique_code = uc
    elif args.bank:
        uc = BANK_UNIQUE_CODE_MAP.get(args.bank.upper())
        if not uc:
            print(f"不支持的银行 code：{args.bank}", file=sys.stderr)
            print(f"支持：{', '.join(BANK_UNIQUE_CODE_MAP.keys())}", file=sys.stderr)
            return 2
        unique_code = uc

    try:
        quote = fetch_price(unique_code)
    except urllib.error.URLError as e:
        print(f"金价服务不可用：{e}", file=sys.stderr)
        return 3
    except bff_client.BffError as e:
        if getattr(e, "code", None) == 403:
            print(e.message, file=sys.stderr)
            return 3
        print(str(e), file=sys.stderr)
        return 3
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 3

    if quote is None:
        print("查询暂时失败，请稍后重试", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(quote, ensure_ascii=False, indent=2))
    else:
        print(render_price(quote, unique_code))
        if args.analyze:
            print()
            print(analyze_price(quote, unique_code))
    return 0


if __name__ == "__main__":
    sys.exit(main())