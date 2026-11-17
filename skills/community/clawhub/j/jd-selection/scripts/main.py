#!/usr/bin/env python3
"""京东精选 — 六大频道合集（缓存版 v0.2）

整合6个独立SCF频道的统一入口：
  超级补贴(eliteId=12254) | 新品首发(109) | 历史最低价(153)
  京东秒杀(33) | 9.9包邮(10) | 实时热销(22)

每个频道独立SCF函数，故障隔离。SCF负责缓存+硬过滤+动态降级+排序+分页。
MCP负责：channel路由、参数传递、结果格式化、用户提示语。
"""

import sys
import json
import os
import socket
import urllib.request
import urllib.error

# ===== 频道配置 =====
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")

# 噪音标签：这些标签对用户无意义，过滤掉
NOISE_TAGS = {"7天无理由退货", "自营", "正品", "7天无理由", "无理由退货"}

CHANNELS = {
    "超级补贴": {
        "url": "https://1439498936-ebgg6n6ain.ap-guangzhou.tencentscf.com",
        "elite_id": 12254,
        "default_gc": 98,
        "default_sales": 5000,
        "name": "超级补贴",
        "sorts": "score=综合评分, price=到手价升序, subsidy=补贴力度降序",
        "desc": "大额补贴好货",
    },
    "新品首发": {
        "url": "https://1439498936-bhwwttt26z.ap-guangzhou.tencentscf.com",
        "elite_id": 109,
        "default_gc": 97,
        "default_sales": 1000,
        "name": "新品首发",
        "sorts": "score=综合评分, price=到手价升序, discount=优惠力度降序",
        "desc": "最新上架好货",
    },
    "历史最低价": {
        "url": "https://1439498936-fmw9ldxblp.ap-guangzhou.tencentscf.com",
        "elite_id": 153,
        "default_gc": 97,
        "default_sales": 500,
        "name": "历史最低价",
        "sorts": "score=综合评分, price=到手价升序, drop=降价幅度降序",
        "desc": "抄底捡漏好货",
    },
    "京东秒杀": {
        "url": "https://1439498936-23pvh3iikx.ap-guangzhou.tencentscf.com",
        "elite_id": 33,
        "default_gc": 98,
        "default_sales": 5000,
        "name": "京东秒杀",
        "sorts": "score=综合评分, price=到手价升序, discount=折扣力度降序",
        "desc": "限时秒杀好货",
    },
    "9.9包邮": {
        "url": "https://1439498936-ieoa5v7nf9.ap-guangzhou.tencentscf.com",
        "elite_id": 10,
        "default_gc": 98,
        "default_sales": 2000,
        "name": "9.9包邮",
        "sorts": "score=综合评分, price=到手价升序, discount=折扣力度降序",
        "desc": "超值包邮好货",
    },
    "实时热销": {
        "url": "https://1439498936-2v8x8x9kyb.ap-guangzhou.tencentscf.com",
        "elite_id": 22,
        "default_gc": 98,
        "default_sales": 2000,
        "name": "实时热销",
        "sorts": "score=综合评分, price=到手价升序, discount=折扣力度降序",
        "desc": "当前畅销好货",
    },
}

# 频道别名 → 标准名
CHANNEL_ALIASES = {
    "补贴": "超级补贴", "超级补贴": "超级补贴", "大额补贴": "超级补贴",
    "新品": "新品首发", "新品首发": "新品首发", "首发": "新品首发",
    "最低价": "历史最低价", "历史最低价": "历史最低价", "抄底": "历史最低价", "捡漏": "历史最低价",
    "秒杀": "京东秒杀", "京东秒杀": "京东秒杀",
    "9.9": "9.9包邮", "9.9包邮": "9.9包邮", "包邮": "9.9包邮",
    "热销": "实时热销", "实时热销": "实时热销", "热卖": "实时热销", "畅销": "实时热销",
}

TIMEOUT_SHORT = 15
TIMEOUT_LONG = 90
PAGE_SIZE = 50
SCARCITY_THRESHOLD = 15


def _resolve_channel(name):
    """解析频道名（支持别名）"""
    if not name:
        return "实时热销"  # 默认频道
    name = name.strip()
    if name in CHANNELS:
        return name
    if name in CHANNEL_ALIASES:
        return CHANNEL_ALIASES[name]
    return None


def _scf_call(proxy_url, params, timeout=TIMEOUT_SHORT):
    """调用SCF代理"""
    payload = json.dumps({"type": "jingfen", "params": params}).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN}
    req = urllib.request.Request(proxy_url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (socket.timeout, TimeoutError):
        return {"ok": False, "error": "timeout"}
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            return {"ok": False, "error": "timeout"}
        return {"ok": False, "error": str(e)}
    except Exception as e:
        if "timed out" in str(e).lower():
            return {"ok": False, "error": "timeout"}
        return {"ok": False, "error": str(e)}


def _get_price(g):
    """获取到手价"""
    coupon = float(g.get("lowestCouponPrice", 0) or 0)
    if coupon > 0:
        return coupon
    return float(g.get("lowestPrice", 0) or g.get("price", 0) or 0)


def _get_ref_price(g):
    """获取参考价（原价）"""
    ref = float(g.get("price", 0) or 0)
    if ref <= 0:
        ref = float(g.get("lowestPrice", 0) or 0)
    return ref


def _get_discount_percent(g):
    """获取折扣力度（百分比）"""
    ref = _get_ref_price(g)
    coupon = _get_price(g)
    if ref > 0 and coupon > 0 and ref > coupon:
        return round((ref - coupon) / ref * 100, 1)
    return 0


def _format_item(g):
    """格式化单条商品用于返回"""
    shop_name = g.get("shopName", "")
    is_jd = 1 if (g.get("isJd") == 1 or "自营" in shop_name) else 0
    material_url = g.get("materialUrl", "")
    if material_url and not material_url.startswith("http"):
        material_url = "https://" + material_url

    return {
        "name": g.get("skuName", ""),
        "price": _get_ref_price(g),
        "coupon_price": _get_price(g),
        "discount_percent": _get_discount_percent(g),
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


def _fmt_num(n):
    """数字简写：≥10000 → X万"""
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)


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


def _build_channel_hints(current_channel):
    """构建频道互推提示（排除当前频道）"""
    others = [ch for ch in ["超级补贴", "新品首发", "历史最低价", "京东秒杀", "9.9包邮", "实时热销"] if ch != current_channel]
    if not others:
        return ""
    picks = others[:3]  # 最多推荐3个
    return "还可以逛逛：" + "、".join(picks)


def tool_get_jd_selection(params):
    """京东精选主查询函数 — 支持6大频道"""
    channel_raw = str(params.get("channel", "")).strip()
    channel_key = _resolve_channel(channel_raw)

    if not channel_key:
        available = "、".join(CHANNELS.keys())
        return json.dumps({
            "content": "",
            "summary": f'未找到频道「{channel_raw}」。可选频道：{available}。'
        }, ensure_ascii=False)

    ch = CHANNELS[channel_key]
    ch_name = ch["name"]
    ch_url = ch["url"]
    elite_id = ch["elite_id"]
    default_gc = ch["default_gc"]

    keyword = str(params.get("keyword", "")).strip()
    max_price = float(params.get("max_price", 0) or 0)
    sort_by = params.get("sort", "score")
    min_gc_user = float(params.get("min_good_comments", default_gc) or default_gc)
    page = int(params.get("page", 1) or 1)
    if page < 1:
        page = 1

    # ===== 第一步：从SCF获取缓存数据（带筛选+分页）=====
    scf_params = {
        "eliteId": elite_id,
        "page": page,
        "page_size": PAGE_SIZE,
        "sort": sort_by,
    }
    if keyword:
        scf_params["keyword"] = keyword
    if max_price > 0:
        scf_params["max_price"] = max_price
    if min_gc_user != default_gc:
        scf_params["min_good_comments"] = min_gc_user

    data = _scf_call(ch_url, scf_params, timeout=TIMEOUT_SHORT)

    # 冷启动检测
    if not data.get("ok"):
        if data.get("error") == "timeout":
            data = _scf_call(ch_url, scf_params, timeout=TIMEOUT_LONG)
            if not data.get("ok"):
                return json.dumps({
                    "content": "",
                    "summary": f"正在为您精选{ch_name}好货，数据量较大，请稍候约30秒后再次查询。"
                }, ensure_ascii=False)
        else:
            return json.dumps({
                "content": "",
                "summary": "查询失败：" + data.get("error", "未知错误") + "，请稍后重试。"
            }, ensure_ascii=False)

    if data.get("warming"):
        return json.dumps({
            "content": "",
            "summary": f"正在为您精选{ch_name}好货，数据量较大，请稍候约30秒后再次查询。"
        }, ensure_ascii=False)

    # ===== 第二步：解析SCF返回的数据 =====
    scf_data = data.get("data", {})
    items = scf_data.get("items", [])
    total = scf_data.get("total", 0)

    if not items and total == 0:
        if keyword:
            msg = f'未找到与「{keyword}」相关的{ch_name}好货。换个关键词试试。'
        else:
            msg = f"暂无符合条件的{ch_name}好货，请稍后再试。"
        return json.dumps({"content": "", "summary": msg}, ensure_ascii=False)

    # ===== 第三步：构建商品列表 =====
    results = [_format_item(g) for g in items]

    # ===== 第四步：构建场景提示语 =====
    page_start = (page - 1) * PAGE_SIZE + 1
    page_end = min(page * PAGE_SIZE, total)
    has_more = page_end < total

    hints = []
    conditions = []
    if keyword:
        conditions.append(f'符合「{keyword}」条件')
    if max_price > 0:
        conditions.append(f'{int(max_price)}元以内')
    cond_str = "且".join(conditions) if conditions else ""

    if keyword and total <= SCARCITY_THRESHOLD:
        if cond_str:
            hints.append(f'{cond_str}的{ch_name}好货仅{total}条，手慢无！')
        else:
            hints.append(f'{ch_name}好货仅{total}条，手慢无！')
        cat_str = _build_category_overview(items)
        if cat_str:
            hints.append(f'换个品类看看？{cat_str}')

    elif keyword and total > SCARCITY_THRESHOLD:
        if cond_str:
            hints.append(f'{cond_str}的{ch_name}好货共{total}条。')
        else:
            hints.append(f'{ch_name}好货共{total}条。')
        if has_more:
            hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
        else:
            hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')

    elif not keyword:
        if page > 1:
            if has_more:
                hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
            else:
                hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')
        else:
            if cond_str:
                hints.append(f'{cond_str}的{ch_name}好货共{total}条。')
            else:
                hints.append(f'{ch_name}好货共{total}条。')
            if has_more:
                hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
            else:
                hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')
            cat_str = _build_category_overview(items)
            if cat_str:
                hints.append(cat_str)

    # 频道互推
    ch_hint = _build_channel_hints(ch_name)
    if ch_hint:
        hints.append(ch_hint)

    return json.dumps({
        "content": json.dumps(results, ensure_ascii=False, indent=2),
        "summary": " ".join(hints)
    }, ensure_ascii=False)


TOOLS = {
    "get_jd_selection": tool_get_jd_selection,
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
