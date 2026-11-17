#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金积存金交易记录查询：通过 cf-gold-ai BFF /api/v1/trade 调用。

  - 列表：POST /api/v1/trade/list  → cf-gold-ai 后端转下游交易服务
  - 汇总：POST /api/v1/trade/sum   → cf-gold-ai 后端转下游交易服务

  **汇总策略**：汇总接口包含退款订单且笔数不准，改为从订单列表自动翻页获取全部订单，
  自行统计各交易类型的笔数和金额，排除退款/取消/失败的订单（更准确）。

  **日期范围**：必须传 orderCreateStartDate 和 orderCreateEndDate 才能获取完整历史数据，
  不传日期只返回近期少量数据。默认传 2020-01-01 到当天。

触发词："交易记录" / "交易明细" / "最近买卖" / "买入记录" / "卖出记录"
"""
import argparse, json, sys, urllib.error
from collections import OrderedDict
from datetime import datetime, timezone, timedelta
import bff_client
import jos

# 业务标识（仅用于路由到 BFF 不同 endpoint）
ORDER_SUM_METHOD = "jingdong.cf.gold.GoldTradeOrderService.queryGoldTradeOrderSum"
ORDER_LIST_METHOD = "jingdong.cf.gold.GoldTradeOrderService.queryGoldTradeOrderList"

# 交易类型中文映射
TRADE_TYPE_MAP = {
    "BUY_GOLD": "买入",
    "SELL_GOLD": "卖出",
    "GIVE_GOLD": "赠金",
    "GET_GOLD": "提金",
    "TRANSFER_OUT": "转出",
    "TRANSFER_IN": "转入",
}

# 订单状态中文映射
STATUS_CODE_MAP = {
    "COMPLETE": "已完成",
    "REDEEM_SUCC": "赎回成功",
    "REFUND_SUCC": "退款完成",
    "REDEEM_FAIL": "赎回失败",
    "PROCESSING": "处理中",
    "WAIT_PAY": "待支付",
    "PAY_SUCC": "支付成功",
    "CANCEL": "已取消",
}

# 成功状态：只有这些状态才计入汇总
SUCCESS_STATUSES = {"COMPLETE", "REDEEM_SUCC"}

# 汇总展示顺序（买入、卖出、赠金、提金）
SUM_DISPLAY_ORDER = ["BUY_GOLD", "SELL_GOLD", "GIVE_GOLD", "GET_GOLD"]

# 银行名称提取：productName → 银行名
BANK_NAME_MAP = {
    "民生积存金": "民生银行",
    "民生金条": "民生银行",
    "浙商积存金": "浙商银行",
    "兴业积存金": "兴业银行",
    "广发积存金": "广发银行",
    "工商积存金": "工商银行",
    "工银积存金": "工商银行",
    "中信积存金": "中信银行",
    "浦发积存金": "浦发银行",
}

# 翻页上限：最多翻多少页
MAX_PAGES = 50
PAGE_SIZE = 50

# 连续N页无新增GOLD订单时停止翻页
NO_NEW_GOLD_PAGES_LIMIT = 3

# 默认日期范围起始（确保获取完整历史数据）
DEFAULT_START_DATE = "2020-01-01"


def _today_str() -> str:
    """返回今天日期字符串 YYYY-MM-DD。"""
    return datetime.now(tz=timezone(timedelta(hours=8))).strftime("%Y-%m-%d")


def _days_ago_str(days: int) -> str:
    """返回 days 天前的日期字符串 YYYY-MM-DD（东八区）。"""
    return (datetime.now(tz=timezone(timedelta(hours=8))) - timedelta(days=days)).strftime("%Y-%m-%d")


def _count_gold_orders(orders: list) -> int:
    """统计订单列表中黄金（businessCode=GOLD）订单笔数。"""
    return sum(1 for o in orders if o.get("businessCode") == "GOLD")


def _extract_bank_name(order: dict) -> str:
    """从订单中提取银行名称。非黄金交易返回空字符串。"""
    product = order.get("productName") or ""
    if order.get("businessCode") != "GOLD":
        return ""
    for key, bank in BANK_NAME_MAP.items():
        if key in product:
            return bank
    if "积存金" in product:
        return product.replace("积存金", "")
    return product


def _format_biz_time(ts_ms) -> str:
    """毫秒时间戳转日期字符串。"""
    if not ts_ms:
        return ""
    try:
        dt = datetime.fromtimestamp(int(ts_ms) / 1000, tz=timezone(timedelta(hours=8)))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (OSError, ValueError):
        return str(ts_ms)


def _trade_type_label(code: str) -> str:
    """交易类型code → 中文标签。"""
    return TRADE_TYPE_MAP.get(code, code or "未知")


def _status_label(code: str) -> str:
    """订单状态code → 中文标签。"""
    return STATUS_CODE_MAP.get(code, code or "未知")


def _parse_ext_info(ext_str: str) -> dict:
    """解析订单的extInfo JSON字符串。"""
    if not ext_str:
        return {}
    try:
        return json.loads(ext_str)
    except json.JSONDecodeError:
        return {}


def _call_trade_api(method, req_param, access_token=None):
    """通用交易接口 BFF 调用。

    后端 ``cf-gold-ai`` 已经做完了网关签名、响应解包，
    本函数把 BFF 返回的 ``TradeOrderListDTO/TradeOrderSumDTO``
    包装成原网关响应形态 ``{"code": "0000", "data": ...}``，避免下游改动。
    """
    if access_token is None:
        access_token = jos._valid_access_token()
    if method == ORDER_LIST_METHOD:
        path = bff_client.PATH_TRADE_LIST
    elif method == ORDER_SUM_METHOD:
        path = bff_client.PATH_TRADE_SUM
    else:
        raise RuntimeError(f"不支持的 trade method: {method}")

    body = dict(req_param or {})
    body["accessToken"] = access_token
    data = bff_client.post_json(path, body)
    return {"code": "0000", "data": data or {}}


def _build_req(trade_type="", start_date="", end_date="", page_no=1, page_size=PAGE_SIZE):
    """构建通用请求参数。默认补全日期范围（必须传日期才能获取完整历史数据）。"""
    if not start_date:
        start_date = DEFAULT_START_DATE
    if not end_date:
        end_date = _today_str()
    return {
        "pageNo": page_no,
        "pageSize": page_size,
        "businessCode": "",
        "statusList": [],
        "bizChannelIds": [],
        "bizProductIdList": [],
        "tradeTypeCodeList": [trade_type] if trade_type else [],
        "orderCreateStartDate": start_date,
        "orderCreateEndDate": end_date,
    }


def fetch_all_orders(trade_type="", start_date="", end_date="") -> list:
    """自动翻页获取全部订单列表。默认补全日期范围以确保数据完整。
    返回所有订单（含全部businessCode），包括退款/取消订单，由调用方过滤。
    
    翻页终止策略：接口混有大量非GOLD订单，每页始终返回50条，
    不能用"本页数<pageSize"判断终止。改用连续N页无新增GOLD订单来停止。
    """
    all_orders = []
    seen_gold_ids = set()
    no_new_gold_pages = 0
    
    for page in range(1, MAX_PAGES + 1):
        resp = _call_trade_api(ORDER_LIST_METHOD,
                               _build_req(trade_type, start_date, end_date, page_no=page, page_size=PAGE_SIZE))
        data = resp.get("data") or {}
        if resp.get("code") != "0000":
            raise RuntimeError(f"订单列表接口错误: code={resp.get('code')}, msg={resp.get('message')}")
        orders = data.get("tradeOrderVoList") or []
        if not orders:
            break
        
        # 统计本页新增GOLD订单
        new_gold = 0
        for o in orders:
            if o.get("businessCode") == "GOLD":
                oid = o.get("orderId") or o.get("id") or id(o)
                if oid not in seen_gold_ids:
                    seen_gold_ids.add(oid)
                    new_gold += 1
        
        all_orders.extend(orders)
        
        # 连续N页无新增GOLD订单，说明GOLD订单已全部获取
        if new_gold == 0:
            no_new_gold_pages += 1
            if no_new_gold_pages >= NO_NEW_GOLD_PAGES_LIMIT:
                break
        else:
            no_new_gold_pages = 0
    
    return all_orders


def _is_success_order(order: dict) -> bool:
    """判断订单是否成功（已完成/赎回成功）。只有成功的订单才计入汇总。"""
    return order.get("statusCode", "") in SUCCESS_STATUSES


def compute_sum_from_orders(orders: list) -> OrderedDict:
    """从订单列表自行统计汇总（按交易类型统计笔数和金额）。
    只统计黄金相关订单（businessCode=GOLD），且只统计成功的订单。
    返回 OrderedDict: trade_type -> {number, amount}
    """
    sum_map = OrderedDict()
    for order in orders:
        if order.get("businessCode") != "GOLD":
            continue
        if not _is_success_order(order):
            continue
        tt = order.get("tradeTypeCode", "")
        if not tt:
            continue
        amt = float(order.get("allAmount") or 0)
        if tt not in sum_map:
            sum_map[tt] = {"number": 0, "amount": 0.0}
        sum_map[tt]["number"] += 1
        sum_map[tt]["amount"] += amt
    return sum_map


def fetch_order_list_page(trade_type="", start_date="", end_date="", page_size=10, page_no=1) -> dict:
    """查询单页订单列表。默认补全日期范围。返回接口原始data（包含total等）。"""
    resp = _call_trade_api(ORDER_LIST_METHOD,
                           _build_req(trade_type, start_date, end_date, page_no=page_no, page_size=page_size))
    data = resp.get("data") or {}
    if resp.get("code") != "0000":
        raise RuntimeError(f"订单列表接口错误: code={resp.get('code')}, msg={resp.get('message')}")
    return data


def render_sum(sum_map: OrderedDict) -> str:
    """渲染交易汇总（买入、卖出、赠金、提金），以 Markdown 表格 + emoji 展示。"""
    if not sum_map:
        return "暂无交易记录。"

    sum_emoji = {"BUY_GOLD": "🟢", "SELL_GOLD": "🔴", "GIVE_GOLD": "🎁", "TAKE_GOLD": "📤"}
    rows = []

    def _row(trade_type, item):
        label = _trade_type_label(trade_type)
        emoji = sum_emoji.get(trade_type, "•")
        number = item["number"]
        amount = f"{item['amount']:,.2f}"
        return f"| {emoji} {label} | {number} 笔 | {amount} 元 |"

    # 按预设顺序展示
    for trade_type in SUM_DISPLAY_ORDER:
        item = sum_map.get(trade_type)
        if item:
            rows.append(_row(trade_type, item))
    # 补充其他类型
    for trade_type, item in sum_map.items():
        if trade_type not in SUM_DISPLAY_ORDER:
            rows.append(_row(trade_type, item))

    if not rows:
        return "暂无交易记录。"

    lines = [
        "💰 **黄金交易汇总**",
        "",
        "| 类型 | 笔数 | 金额 |",
        "|------|------|------|",
    ]
    lines.extend(rows)
    return "\n".join(lines)


def _detail_trade_type_label(order: dict) -> str:
    """交易明细中的类型标签：成功的显示正常类型，失败/退款的标注失败。"""
    tt = order.get("tradeTypeCode", "")
    st = order.get("statusCode", "")
    base = _trade_type_label(tt)
    # 退款/取消/失败的订单，标注"买金失败""卖金失败"等
    if st in ("REFUND_SUCC", "CANCEL", "REDEEM_FAIL"):
        if tt == "BUY_GOLD":
            return "买金失败"
        elif tt == "SELL_GOLD":
            return "卖金失败"
        else:
            return f"{base}(失败)"
    return base


def _type_emoji(trade_type_label: str) -> str:
    """根据交易类型标签返回对应 emoji。"""
    if "失败" in trade_type_label:
        return "⚠️"
    if "买" in trade_type_label or "买入" in trade_type_label:
        return "🟢"
    if "卖" in trade_type_label or "卖出" in trade_type_label:
        return "🔴"
    if "赠" in trade_type_label:
        return "🎁"
    if "提" in trade_type_label:
        return "📤"
    return "•"


def _status_emoji(status_label: str) -> str:
    """根据状态标签返回对应 emoji。"""
    if any(k in status_label for k in ("成功", "已完成", "完成")) and "失败" not in status_label and "退款" not in status_label:
        return "✅"
    if any(k in status_label for k in ("失败", "退款", "取消")):
        return "❌"
    return "⏳"


def render_order_list(orders: list, max_per_bank: int = 10) -> str:
    """渲染交易订单列表，按银行分组，以 Markdown 表格 + emoji 展示。
    展示所有黄金订单，失败/退款的标注失败。每家银行最多展示 max_per_bank 条最近订单。
    """
    # 保留所有黄金相关订单（包括失败/退款），按时间倒序
    gold_orders = [o for o in orders if o.get("businessCode") == "GOLD"]
    if not gold_orders:
        return "暂无黄金交易记录。"

    # 按银行分组
    bank_groups = OrderedDict()
    for order in gold_orders:
        bank = _extract_bank_name(order) or "其他"
        bank_groups.setdefault(bank, []).append(order)

    lines = ["📋 **最近交易记录**"]
    for bank, bank_orders in bank_groups.items():
        lines.append("")
        lines.append(f"🏦 **{bank}**")
        lines.append("")
        lines.append("| # | 类型 | 金额 | 克数 | 克单价 | 时间 | 状态 |")
        lines.append("|---|------|------|------|--------|------|------|")
        for i, order in enumerate(bank_orders[:max_per_bank], 1):
            trade_type = _detail_trade_type_label(order)
            amount = order.get("allAmount", "0")
            unit = order.get("unit", "元")
            biz_time = _format_biz_time(order.get("bizTime")) or "-"
            status = _status_label(order.get("statusCode", ""))

            ext = _parse_ext_info(order.get("extInfo") or "")
            grams = ext.get("og", "") or "-"
            gram_price = ext.get("ogp", "") or "-"
            grams_cell = f"{grams}克" if grams != "-" else "-"
            price_cell = f"{gram_price}元/克" if gram_price != "-" else "-"

            type_cell = f"{_type_emoji(trade_type)} {trade_type}"
            status_cell = f"{_status_emoji(status)} {status}"
            lines.append(
                f"| {i} | {type_cell} | {amount}{unit} | {grams_cell} | {price_cell} | {biz_time} | {status_cell} |"
            )

        if len(bank_orders) > max_per_bank:
            lines.append(f"> … 还有 {len(bank_orders) - max_per_bank} 笔")

    return "\n".join(lines).rstrip()


# 大额买入阈值（元）
LARGE_BUY_THRESHOLD = 10000.0
# 定投识别：单笔金额上限（元），小于此值视为小额定投
DICA_MAX_AMOUNT = 2000.0
# 定投识别：一组至少的笔数
DICA_MIN_COUNT = 2


def _order_date(order: dict) -> str:
    """订单业务日期 YYYY-MM-DD（无则空）。"""
    ts = order.get("bizTime")
    if not ts:
        return ""
    try:
        dt = datetime.fromtimestamp(int(ts) / 1000, tz=timezone(timedelta(hours=8)))
        return dt.strftime("%Y-%m-%d")
    except (OSError, ValueError):
        return ""


def _order_amount(order: dict) -> float:
    """订单金额（元）。"""
    try:
        return float(order.get("allAmount") or 0)
    except (TypeError, ValueError):
        return 0.0


def _order_gram_price(order: dict):
    """订单克单价（元/克），取不到返回 None。"""
    ext = _parse_ext_info(order.get("extInfo") or "")
    gp = ext.get("ogp")
    if gp in (None, "", "{}", "[]", "null"):
        return None
    try:
        return float(gp)
    except (TypeError, ValueError):
        return None


def _md_date(date_str: str) -> str:
    """YYYY-MM-DD → M月D日。"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.month} 月 {dt.day} 日"
    except (ValueError, TypeError):
        return date_str


def _fmt_amount(v: float) -> str:
    """金额格式化（去掉无意义小数）。"""
    if abs(v - round(v)) < 0.005:
        return f"{int(round(v)):,}"
    return f"{v:,.2f}"


def analyze_trade_features(orders: list) -> str:
    """交易特征简析：从黄金订单识别买入密集期/大额买入/最新操作/卖出记录/操作风格。"""
    gold = [o for o in orders if o.get("businessCode") == "GOLD"]
    if not gold:
        return ""

    # 成功买入 / 卖出
    buys = [o for o in gold if o.get("tradeTypeCode") == "BUY_GOLD" and _is_success_order(o)]
    sells = [o for o in gold if o.get("tradeTypeCode") == "SELL_GOLD" and _is_success_order(o)]
    # 失败/退款的大额买入（用于识别"失败后重买"）
    failed_buys = [o for o in gold if o.get("tradeTypeCode") == "BUY_GOLD"
                   and o.get("statusCode") in ("REFUND_SUCC", "CANCEL")]

    points = []

    # —— 买入密集期：同一天同一行 ≥DICA_MIN_COUNT 笔小额买入 ——
    from collections import defaultdict
    day_bank = defaultdict(list)  # (date, bank) -> [orders]
    for o in buys:
        d = _order_date(o)
        if not d:
            continue
        bank = _extract_bank_name(o) or "其他"
        day_bank[(d, bank)].append(o)
    dica_groups = []
    for (d, bank), grp in day_bank.items():
        small = [o for o in grp if _order_amount(o) <= DICA_MAX_AMOUNT]
        if len(small) >= DICA_MIN_COUNT:
            dica_groups.append((d, bank, small))
    if dica_groups:
        dica_groups.sort(key=lambda x: x[0])
        d, bank, grp = dica_groups[0]
        each = _fmt_amount(_order_amount(grp[0]))
        prices = [p for p in (_order_gram_price(o) for o in grp) if p is not None]
        cost_txt = ""
        if prices:
            lo, hi = min(prices), max(prices)
            cost_txt = f"，成本在 {_fmt_amount(lo)}~{_fmt_amount(hi)}" if lo != hi else f"，成本约 {_fmt_amount(lo)}"
        extra = f"（等 {len(dica_groups)} 段）" if len(dica_groups) > 1 else ""
        points.append(f"- 买入密集期：{_md_date(d)}{bank}连续 {len(grp)} 笔小额定投（每笔 {each} 元）{cost_txt}{extra}")

    # —— 大额买入 ——
    large_buys = sorted(
        [o for o in buys if _order_amount(o) >= LARGE_BUY_THRESHOLD],
        key=lambda o: _order_date(o))
    if large_buys:
        parts = []
        for o in large_buys[:3]:
            d = _md_date(_order_date(o))
            bank = _extract_bank_name(o) or "某行"
            amt = _fmt_amount(_order_amount(o))
            # 同日同行是否有失败买入 → 标注"失败后重买"
            retry = any(_order_date(f) == _order_date(o)
                    and (_extract_bank_name(f) or "") == (_extract_bank_name(o) or "")
                        for f in failed_buys)
            note = "（失败后退款重买成功）" if retry else ""
            parts.append(f"{d}{bank}买入 {amt} 元{note}")
        points.append(f"- 大额买入：{'，'.join(parts)}")

    # —— 最新操作 ——
    dated_ops = [o for o in (buys + sells) if _order_date(o)]
    if dated_ops:
        latest = max(dated_ops, key=lambda o: _order_date(o))
        latest_date = _order_date(latest)
        same_day = [o for o in dated_ops if _order_date(o) == latest_date]
        bank = _extract_bank_name(latest) or "某行"
        is_buy = latest.get("tradeTypeCode") == "BUY_GOLD"
        action = "补仓" if is_buy else "卖出"
        prices = [p for p in (_order_gram_price(o) for o in same_day) if p is not None]
        price_txt = ""
        if prices:
            lo, hi = min(prices), max(prices)
            price_txt = f"以 {_fmt_amount(lo)}~{_fmt_amount(hi)} 元/克 " if lo != hi else f"以 {_fmt_amount(lo)} 元/克 "
        # 与历史买入均价对比
        cmp_txt = ""
        if is_buy and prices:
            hist_prices = [p for p in (_order_gram_price(o) for o in buys
                           if _order_date(o) < latest_date) if p is not None]
            if hist_prices:
                avg_hist = sum(hist_prices) / len(hist_prices)
                cur = sum(prices) / len(prices)
                if cur < avg_hist:
                    cmp_txt = "，成本较此前明显降低" if avg_hist - cur >= 30 else "，成本低于此前"
        cnt = len(same_day)
        points.append(f"- 最新操作：{_md_date(latest_date)}在{bank}{price_txt}{'低价' if cmp_txt else ''}{action} {cnt} 笔{cmp_txt}")

    # —— 卖出记录 ——
    if sells:
        s = sorted(sells, key=lambda o: _order_date(o))
        first = s[0]
        gp = _order_gram_price(first)
        gp_txt = f"在 {_fmt_amount(gp)} " if gp is not None else ""
        if len(sells) <= 2:
            points.append(f"- 卖出记录：仅 {len(sells)} 笔，{_md_date(_order_date(first))}{gp_txt}卖出，说明整体以持有为主")
        else:
            points.append(f"- 卖出记录：共 {len(sells)} 笔卖出")
    else:
        points.append("- 卖出记录：暂无卖出，整体以持有为主")

    # —— 操作风格偏向 ——
    style = []
    if dica_groups:
        style.append("定投")
    # 低价补仓：最新操作是买入且成本降低
    if any("补仓" in p and "降低" in p for p in points):
        style.append("低价补仓")
    if large_buys and not dica_groups:
        style.append("大额建仓")
    if not style:
        style.append("持有为主")
    points.append(f"- 操作风格偏向 {' + '.join(style)}")

    body = "\n".join(points)
    return f"📊 交易特征简析\n\n{body}\n\n> 💡 本信息由 京东金融 提供"


def render_trade_records(sum_map: OrderedDict, orders: list, range_note: str = "") -> str:
    """综合渲染：查询区间说明 + 汇总 + 最近订单列表 + 交易特征简析。"""
    sum_text = render_sum(sum_map)
    list_text = render_order_list(orders)
    parts = []
    if range_note:
        parts.append(f"🗓️ 查询区间：{range_note}")
    parts.extend([sum_text, list_text])
    analysis = analyze_trade_features(orders)
    if analysis:
        parts.append(analysis)
    return "\n\n".join(parts)


def main(argv=None):
    parser = argparse.ArgumentParser(description="黄金积存金交易记录查询")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--type", "-t", default="", help="交易类型过滤(BUY_GOLD/SELL_GOLD等)")
    parser.add_argument("--start-date", default="", help="起始日期(YYYY-MM-DD)")
    parser.add_argument("--end-date", default="", help="结束日期(YYYY-MM-DD)")
    parser.add_argument("--page-size", type=int, default=10, help="展示用每页条数(默认10)")
    parser.add_argument("--page-no", type=int, default=1, help="展示用页码(默认1)")
    parser.add_argument("--sum-only", action="store_true", help="仅查询汇总")
    parser.add_argument("--list-only", action="store_true", help="仅查询订单列表")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args(argv)
    bff_client.set_claw(args.claw)

    # 默认时间范围：用户未指定日期时，先查近一月；若近一月无黄金订单，回退查近三月。
    # 用户显式指定 --start-date / --end-date 时，完全尊重用户，不做回退。
    user_specified_range = bool(args.start_date or args.end_date)
    default_range_note = ""
    if not user_specified_range:
        args.end_date = _today_str()
        args.start_date = _days_ago_str(30)
        default_range_note = "近一月"

    try:
        # 自动翻页获取全部订单用于汇总+明细展示
        all_orders = fetch_all_orders(
            trade_type=args.type,
            start_date=args.start_date,
            end_date=args.end_date,
        )
        # 默认区间回退：近一月无黄金订单则改查近三月
        if not user_specified_range and _count_gold_orders(all_orders) == 0:
            args.start_date = _days_ago_str(90)
            default_range_note = "近三月"
            all_orders = fetch_all_orders(
                trade_type=args.type,
                start_date=args.start_date,
                end_date=args.end_date,
            )
        # 自行统计汇总
        sum_map = compute_sum_from_orders(all_orders)

    except urllib.error.URLError as e:
        print(f"[内部] 网络错误: {e}", file=sys.stderr)
        print("查询暂时失败，请稍后重试")
        sys.exit(3)
    except bff_client.BffError as e:
        if getattr(e, "code", None) == 403:
            print(e.message)
            sys.exit(3)
        print(f"[内部] {e}", file=sys.stderr)
        print("查询暂时失败，请稍后重试")
        sys.exit(3)
    except RuntimeError as e:
        print(f"[内部] {e}", file=sys.stderr)
        print("查询暂时失败，请稍后重试")
        sys.exit(3)

    if args.json:
        out = {
            "sum": {tt: item for tt, item in sum_map.items()},
            "total_orders": len(all_orders),
            "list": [o for o in all_orders if o.get("businessCode") == "GOLD"],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(0)

    # 查询区间说明：默认区间用中文档位，用户指定区间用具体日期
    if not user_specified_range:
        range_note = default_range_note
    else:
        range_note = f"{args.start_date or '不限'} ~ {args.end_date or '至今'}"

    # 格式化输出
    if args.sum_only:
        print(render_sum(sum_map))
    elif args.list_only:
        print(render_order_list(all_orders))
    else:
        print(render_trade_records(sum_map, all_orders, range_note=range_note))

    sys.exit(0)


if __name__ == "__main__":
    main()