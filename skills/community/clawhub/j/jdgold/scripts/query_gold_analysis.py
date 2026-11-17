#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""
黄金分析工具集查询脚本。

功能：
- 银行积存金报价查询
- 资金炸弹
- 交易机会评分
- 挂单簿分析
- 指标共振分析
- 黄金盯盘看板信息
- 综合黄金分析概览
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime

from jdjr_config import get_fund_api_base_url, get_fund_api_key, get_source_metadata, get_claw, set_claw


SKILL_CODE = "gold-analysis-hub"
BANK_GOLD_CODES = {
    "民生积存金": "CMBC-JCJ",
    "浙商积存金": "CZB-JCJ",
}
TAB_MAP = {
    "15分钟": "20",
    "m15": "20",
    "1小时": "4",
    "一小时": "4",
    "h1": "4",
    "4小时": "21",
    "四小时": "21",
    "h4": "21",
    "日线": "5",
    "d1": "5",
}
TAB_LABEL = {"20": "近15分钟", "4": "近1小时", "21": "近4小时", "5": "日线"}
AVERAGES_LABEL = {0: "5周期均线", 1: "10周期均线", 2: "20周期均线", 3: "50周期均线", 4: "100周期均线", 5: "200周期均线"}
FIBONACCI_LABEL = {0: "23.6%", 1: "38.2%", 2: "50.0%", 3: "61.8%", 5: "161.8%", 6: "261.8%", 7: "423.6%"}
DASHBOARD_URL = "https://m.jdjygold.com/finance-gold/newgold/home/?mode=1&goldChannelAcc=MS&orderSource=msxry_sygdicon&widgetChannel=msxrycj&jrcontainer=h5&jrlogin=true"


def get_gold_base_url() -> str:
    """从基金网关地址推导黄金分析网关根地址。"""
    return get_fund_api_base_url().replace("/api/gateway", "")


def post_json(path: str, payload: dict) -> dict:
    """向黄金分析网关发送 JSON POST 请求。"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "apikey": get_fund_api_key(),
        "x-skill-code": SKILL_CODE,
        "x-skill-run-id": str(uuid.uuid4()),
    }
    claw = get_claw()
    if claw:
        headers["x-claw"] = claw
    req = urllib.request.Request(
        f"{get_gold_base_url()}/{path.lstrip('/')}",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_text(text: str) -> str:
    return "".join(text.lower().split())


def infer_mode(query: str) -> str:
    query_norm = normalize_text(query)
    if any(word in query_norm for word in ["打开", "启动", "弹出", "展示"]) and any(word in query_norm for word in ["看板", "盯盘", "dashboard"]):
        return "dashboard"
    if any(word in query_norm for word in ["挂单", "买卖盘", "盘口", "深度", "挂单墙", "订单簿"]):
        return "order_book"
    if any(word in query_norm for word in ["共振", "支撑", "阻力", "压力位", "关键点位", "技术分析", "斐波", "布林"]):
        return "resonance"
    if any(word in query_norm for word in ["机会", "热度", "评分", "适不适合交易", "入场时机", "现在火不火"]):
        return "opportunity"
    if any(word in query_norm for word in ["大单", "主力", "资金", "成交量异动", "放量", "多空订单占比", "市场情绪"]):
        return "bomb"
    if any(word in query_norm for word in ["全面", "综合", "现在怎么样", "全面分析", "全面看一下"]):
        return "overview"
    return "realtime_price"


def infer_tab(query: str) -> str:
    query_norm = normalize_text(query)
    for key, value in TAB_MAP.items():
        if normalize_text(key) in query_norm:
            return value
    return "20"


def infer_unique_codes(query: str):
    query_norm = normalize_text(query)
    selected = [code for name, code in BANK_GOLD_CODES.items() if normalize_text(name) in query_norm]
    return selected or list(BANK_GOLD_CODES.values())


def parse_json_data(raw_data):
    if isinstance(raw_data, list):
        if not raw_data:
            return []
        return [json.loads(item) if isinstance(item, str) else item for item in raw_data]
    if isinstance(raw_data, str):
        return json.loads(raw_data)
    return raw_data


def query_realtime_quotes(query: str):
    items = []
    for unique_code in infer_unique_codes(query):
        raw = post_json("api/gateway/gold/realtime-quote", {"uniqueCode": unique_code})
        if not raw.get("success"):
            raise ValueError(raw.get("message", "黄金报价查询失败"))
        data = raw.get("data") or {}
        items.append(
            {
                "uniqueCode": unique_code,
                "name": next((name for name, code in BANK_GOLD_CODES.items() if code == unique_code), unique_code),
                "lastPrice": data.get("lastPrice"),
                "raise": data.get("raise"),
                "raisePercent": data.get("raisePercent"),
                "tradeTime": data.get("tradeTime"),
                "unit": data.get("unit"),
            }
        )
    return {"route": "realtime_price", "quotes": items}


def query_bomb(query: str):
    query_norm = normalize_text(query)
    if "历史" in query_norm:
        raw = post_json("api/gateway/gold/bomb-details", {})
        if not raw.get("success") or raw.get("code") != "0000":
            raise ValueError(raw.get("message", "黄金资金炸弹历史查询失败"))
        groups = raw.get("data") or []
        return {"route": "bomb_history", "groups": groups}

    raw = post_json("api/gateway/gold/bomb", {})
    if not raw.get("success") or raw.get("code") != "0000":
        raise ValueError(raw.get("message", "黄金资金炸弹查询失败"))
    items = parse_json_data(raw.get("data") or [])
    return {"route": "bomb_latest", "items": items}


def query_opportunity():
    raw = post_json("api/gateway/gold/opportunity", {})
    if not raw.get("success") or raw.get("code") != "0000":
        raise ValueError(raw.get("message", "黄金机会评分查询失败"))
    item = parse_json_data(raw.get("data") or [])[0]
    publish_time = item.get("publishTime")
    return {
        "route": "opportunity",
        "opportunity": item.get("opportunity", 0),
        "publishTime": publish_time,
        "publishTimeStr": datetime.fromtimestamp(publish_time / 1000).strftime("%Y-%m-%d %H:%M") if publish_time else "",
    }


def query_order_book():
    raw = post_json("api/gateway/gold/order-book", {})
    if not raw.get("success") or raw.get("code") != "0000":
        raise ValueError(raw.get("message", "黄金挂单簿查询失败"))
    data = parse_json_data(raw.get("data") or [])[0]
    levels = json.loads(data.get("levels", "[]"))
    current_price = data.get("price")
    above = [item for item in levels if item.get("price", 0) >= current_price]
    below = [item for item in levels if item.get("price", 0) < current_price]
    long_above = sorted(above, key=lambda x: x.get("ol", 0), reverse=True)[:10]
    long_below = sorted(below, key=lambda x: x.get("ol", 0), reverse=True)[:10]
    short_above = sorted(above, key=lambda x: x.get("os", 0), reverse=True)[:10]
    short_below = sorted(below, key=lambda x: x.get("os", 0), reverse=True)[:10]
    return {
        "route": "order_book",
        "currentPrice": current_price,
        "updateTime": datetime.fromtimestamp(data.get("time", 0)).strftime("%Y-%m-%d %H:%M") if data.get("time") else "",
        "longOrders": {"above": long_above, "below": long_below},
        "shortOrders": {"above": short_above, "below": short_below},
    }


def is_range(val, range_):
    if val is None or not range_:
        return False
    return min(range_) <= val <= max(range_)


def query_resonance(query: str):
    tab = infer_tab(query)
    raw = post_json("api/gateway/gold/indicator-resonance", {})
    if not raw.get("success") or raw.get("code") != "0000":
        raise ValueError(raw.get("message", "黄金共振分析查询失败"))
    resonance_data = parse_json_data(raw.get("data") or [])[0]
    cycle_range = resonance_data.get("cycleRange", [])
    price = resonance_data.get("price", 0)
    current_cycle_range = next((item for item in cycle_range if str(item.get("type")) == str(tab)), None)
    if not current_cycle_range:
        raise ValueError("未找到对应周期的共振分析数据")

    bars = []
    min_price = current_cycle_range.get("min", 0)
    max_price = current_cycle_range.get("max", 0)
    bar_count = 20
    step = (max_price - min_price) / bar_count if max_price > min_price else 0
    for i in range(bar_count):
        max0 = max_price - step * i
        min0 = max_price - step * (i + 1)
        bars.append({"max": max0, "min": min0, "price": f"{min0:.2f}", "isCurrent": min0 <= price < max0, "weights": 0})

    def add_point(value, weight):
        for row in bars:
            if is_range(value, [row["max"], row["min"]]):
                row["weights"] += weight

    for item in resonance_data.get("woodiePivotPoint", []):
        for key in ["value", "resistance1", "resistance2", "resistance3", "support1", "support2", "support3"]:
            add_point(item.get(key), item.get("weights", 0))
    for item in resonance_data.get("classPivotPoint", []):
        for key in ["value", "resistance1", "resistance2", "support1", "support2"]:
            add_point(item.get(key), item.get("weights", 0))
    for item in resonance_data.get("hl", []):
        for key in ["high", "low"]:
            add_point(item.get(key), item.get("weights", item.get("weight", 0)))
    for item in resonance_data.get("boll", []):
        for key, weight_key in [("upperBand", "upperWeights"), ("middleBand", "middleWeights"), ("lowerBand", "lowerWeights")]:
            add_point(item.get(key), item.get(weight_key, 0))
    for item in resonance_data.get("fibonacci", []):
        for idx, value in enumerate(item.get("levels", [])):
            if idx != 4:
                add_point(value, item.get("weights", 0))
    for item in resonance_data.get("vpc", []):
        for value in item.get("value", []):
            add_point(value, item.get("weights", 0))
    for item in resonance_data.get("averages", []):
        for value in item.get("value", []):
            add_point(value, item.get("weights", 0))
    for item in resonance_data.get("optionKey", []):
        weight = item.get("weights") or item.get("weight", 0)
        add_point(item.get("minPrice"), weight)
        add_point(item.get("maxPrice"), weight)

    current_index = next((i for i, row in enumerate(bars) if row.get("isCurrent")), -1)
    total_weight = max(max((row.get("weights", 0) for row in bars), default=0), 1)
    resistance = sorted(bars[:current_index], key=lambda x: x.get("weights", 0), reverse=True)[:3] if current_index > 0 else []
    support = sorted(bars[current_index + 1 :], key=lambda x: x.get("weights", 0), reverse=True)[:3] if current_index >= 0 else []

    def pack(rows):
        return [
            {
                "price": row.get("price"),
                "weights": row.get("weights", 0),
                "weightsPercent": min(100, row.get("weights", 0) / total_weight * 100),
            }
            for row in rows
        ]

    return {
        "route": "resonance",
        "tab": tab,
        "tabLabel": TAB_LABEL.get(tab, tab),
        "currentPrice": round(price, 2),
        "topResistance3": pack(resistance),
        "topSupport3": pack(support),
    }


def query_dashboard():
    return {
        "route": "dashboard",
        "title": "京东黄金实时看板",
        "url": DASHBOARD_URL,
        "requires": "pywebview",
    }


def query_overview(query: str):
    return {
        "route": "overview",
        "quotes": query_realtime_quotes(query)["quotes"],
        "bomb": query_bomb("latest")["items"][0],
        "opportunity": query_opportunity(),
        "resonance": query_resonance(query),
    }


def query_gold_analysis(query: str):
    mode = infer_mode(query)
    if mode == "realtime_price":
        return {"success": True, "data": query_realtime_quotes(query), "source": get_source_metadata("GOLD")}
    if mode == "bomb":
        return {"success": True, "data": query_bomb(query), "source": get_source_metadata("GOLD")}
    if mode == "opportunity":
        return {"success": True, "data": query_opportunity(), "source": get_source_metadata("GOLD")}
    if mode == "order_book":
        return {"success": True, "data": query_order_book(), "source": get_source_metadata("GOLD")}
    if mode == "resonance":
        return {"success": True, "data": query_resonance(query), "source": get_source_metadata("GOLD")}
    if mode == "dashboard":
        return {"success": True, "data": query_dashboard(), "source": get_source_metadata("GOLD")}
    return {"success": True, "data": query_overview(query), "source": get_source_metadata("GOLD")}


def main() -> int:
    parser = argparse.ArgumentParser(description="查询黄金高级分析工具")
    parser.add_argument("query", help="用户查询语句")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args()
    set_claw(args.claw)

    try:
        result = query_gold_analysis(args.query.strip())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print(json.dumps({"success": False, "error": "您的账户已被限制访问，如有疑问请联系京东黄金客服"}, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": f"HTTP {exc.code}"}, ensure_ascii=False))
        return 1
    except urllib.error.URLError as exc:
        print(json.dumps({"success": False, "error": f"网络请求失败: {exc.reason}"}, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
