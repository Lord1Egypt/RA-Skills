#!/usr/bin/env python3
"""京东自营秒杀 — SCF代理脚本

通过SCF代理查询京东秒杀频道好货，仅筛选京东自营商品，
好评≥98%、销量≥5000的品质精选。
"""

import sys
import json
import os
import socket
import urllib.request
import urllib.error

# ===== 配置 =====
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")
PROXY_URL = os.environ.get("PROXY_URL", "https://1439498936-23pvh3iikx.ap-guangzhou.tencentscf.com")
TOOL_NAME = "get_seckill_items"
CHANNEL_NAME = "京东秒杀"
TIMEOUT_SHORT = 15
TIMEOUT_LONG = 90

# 噪音标签：这些标签对用户无意义，过滤掉
NOISE_TAGS = {"7天无理由退货", "自营", "正品", "7天无理由", "无理由退货"}


def _scf_call(tool_name, params, timeout=TIMEOUT_SHORT):
    """调用SCF代理"""
    payload = json.dumps({"tool": tool_name, "params": params}).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN}
    req = urllib.request.Request(PROXY_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (socket.timeout, TimeoutError):
        return {"ok": False, "error": "timeout"}
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            return {"ok": False, "error": "timeout"}
        return {"ok": False, "error": str(e)}
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"JSON解析失败: {e}"}
    except Exception as e:
        if "timed out" in str(e).lower():
            return {"ok": False, "error": "timeout"}
        return {"ok": False, "error": str(e)}


def _fmt_num(n):
    """数字简写：≥10000 → X万"""
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)


def _format_item(g):
    """格式化单条商品"""
    shop_name = g.get("shopName", "")
    is_jd = 1 if (g.get("isJd") == 1 or "自营" in shop_name) else 0
    material_url = g.get("materialUrl", "")
    if material_url and not material_url.startswith("http"):
        material_url = "https://" + material_url

    coupon = float(g.get("lowestCouponPrice", 0) or 0)
    ref = float(g.get("price", 0) or 0)
    if coupon <= 0:
        coupon = float(g.get("lowestPrice", 0) or ref or 0)
    if ref <= 0:
        ref = float(g.get("lowestPrice", 0) or 0)
    discount_pct = round((ref - coupon) / ref * 100, 1) if ref > 0 and coupon > 0 and ref > coupon else 0

    return {
        "name": g.get("skuName", ""),
        "price": ref,
        "coupon_price": coupon,
        "discount_percent": discount_pct,
        "shop_name": shop_name,
        "brand_name": g.get("brandName", ""),
        "is_self": bool(is_jd),
        "tags": [t for t in g.get("skuTags", []) if t not in NOISE_TAGS],
        "image_url": g.get("imageUrl", ""),
        "buy_url": material_url,
        "category": g.get("cid1Name", ""),
        "category2": g.get("cid2Name", ""),
        "category3": g.get("cid3Name", ""),
        "orders_30d": int(g.get("inOrderCount30Days", 0) or 0),
        "good_comments": float(g.get("goodCommentsShare", 0) or 0),
        "score": g.get("_score", 0),
    }


def _build_category_overview(items):
    """从商品列表提取品类概览，生成动态示例关键词"""
    cat_counter = {}
    for g in items:
        cat = g.get("cid1Name", "")
        if cat:
            cat_counter[cat] = cat_counter.get(cat, 0) + 1
    top_cats = sorted(cat_counter.items(), key=lambda x: -x[1])[:3]
    if not top_cats:
        return ""
    keywords = [cat[:2] for cat, _ in top_cats]
    return "试试搜「" + "」「".join(keywords) + "」"


def _build_summary(total, page, page_size, items_len, channel_name, keyword, max_price):
    """构建summary提示语"""
    page_start = (page - 1) * page_size + 1
    page_end = min(page * page_size, total)
    has_more = page_end < total

    parts = []
    conditions = []
    if keyword:
        conditions.append(f"符合「{keyword}」条件")
    if max_price and max_price > 0:
        conditions.append(f"{int(max_price)}元以内")
    cond_str = "且".join(conditions) if conditions else ""

    if cond_str:
        parts.append(f"{cond_str}的{channel_name}好货共{total}条。")
    else:
        parts.append(f"{channel_name}好货共{total}条。")

    if has_more:
        parts.append(f"当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说\"下一页\"查看更多。")
    else:
        parts.append(f"当前显示第{page_start}-{page_end}条，已全部展示。")

    return " ".join(parts)


def tool_get_seckill_items(params):
    """查询京东秒杀商品"""
    keyword = str(params.get("keyword", "")).strip()
    max_price = float(params.get("max_price", 0) or 0)
    sort_by = params.get("sort", "score")
    min_gc_user = float(params.get("min_good_comments", 98) or 98)
    page = int(params.get("page", 1) or 1)
    if page < 1:
        page = 1

    scf_params = {
        "keyword": keyword,
        "max_price": max_price,
        "sort": sort_by,
        "min_good_comments": min_gc_user,
        "page": page,
    }

    data = _scf_call(TOOL_NAME, scf_params, timeout=TIMEOUT_SHORT)

    if not data.get("ok"):
        if data.get("error") == "timeout":
            data = _scf_call(TOOL_NAME, scf_params, timeout=TIMEOUT_LONG)
            if not data.get("ok"):
                return json.dumps({
                    "content": "",
                    "summary": f"正在为您精选{CHANNEL_NAME}好货，数据量较大，请稍候约30秒后再次查询。"
                }, ensure_ascii=False)
        else:
            return json.dumps({
                "content": "",
                "summary": "查询失败：" + data.get("error", "未知错误") + "，请稍后重试。"
            }, ensure_ascii=False)

    if data.get("warming"):
        return json.dumps({
            "content": "",
            "summary": f"正在为您精选{CHANNEL_NAME}好货，数据量较大，请稍候约30秒后再次查询。"
        }, ensure_ascii=False)

    items = data.get("items", [])
    total = data.get("total", 0)
    page = data.get("page", page)
    page_size = data.get("page_size", 50)

    if not items and total == 0:
        if keyword:
            msg = f"未找到与「{keyword}」相关的{CHANNEL_NAME}好货。换个关键词试试。"
        else:
            msg = f"暂无符合条件的{CHANNEL_NAME}好货，请稍后再试。"
        return json.dumps({"content": "", "summary": msg}, ensure_ascii=False)

    results = [_format_item(g) for g in items]
    summary = _build_summary(total, page, page_size, len(results), CHANNEL_NAME, keyword, max_price)
    cat_overview = _build_category_overview(items)
    if cat_overview:
        summary += " " + cat_overview

    return json.dumps({
        "content": json.dumps(results, ensure_ascii=False, indent=2),
        "summary": summary
    }, ensure_ascii=False)


TOOLS = {
    "get_seckill_items": tool_get_seckill_items,
}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": f"未知工具: {tool}，可用工具: {', '.join(TOOLS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
