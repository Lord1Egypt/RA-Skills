#!/usr/bin/env python3
"""拼多多精选 - 搜索/详情/逛好价"""

import sys
import json
import urllib.request
import urllib.error

PROXY_URL = "https://1439498936-1iog1h3lb1.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 60

CHANNEL_MAP = {
    "销量榜": 1, "相似推荐": 3, "热销榜": 5, "秒杀": 4,
    "百亿补贴": 7, "千万补贴": 10851, "千万神券": 11879,
    "品牌黑标": 31, "精选爆品": 10564,
}

ACTIVITY_TAG_MAP = {
    "秒杀": 4, "百亿补贴": 7, "千万补贴": 10851,
    "千万神券": 11879, "品牌黑标": 31, "精选爆品": 10564,
}


def call_proxy(rtype, params):
    """调用SCF代理 - type+params格式"""
    data = json.dumps({"type": rtype, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=data, method="POST",
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_search_results(data):
    if not data.get("ok"):
        return "搜索失败：" + data.get("error", "未知错误")
    results = data.get("data", [])
    total = data.get("total", 0)
    if not results:
        return "没有找到符合条件的商品，建议换一个关键词试试。"

    lines = ["共找到 {} 件商品：\n".format(total)]
    for i, item in enumerate(results, 1):
        name = item.get("goods_name", "")
        final_price = item.get("final_price", 0)
        min_group_price = item.get("min_group_price", 0)
        coupon_discount = item.get("coupon_discount", 0)
        has_coupon = item.get("has_coupon", False)
        sales = item.get("sales_tip", "")
        mall = item.get("mall_name", "")
        category = item.get("category_name", "")
        goods_sign = item.get("goods_sign", "")
        image = item.get("goods_image_url", "")

        if coupon_discount > 0 and has_coupon:
            price_str = "到手价¥{}（拼团价¥{} - 券¥{}）".format(final_price, min_group_price, coupon_discount)
        else:
            price_str = "¥{}".format(min_group_price)

        coupon_tag = " | 有券" if has_coupon else ""
        sales_str = " | 销量{}".format(sales) if sales else ""
        mall_str = " | {}".format(mall) if mall else ""
        cat_str = " | {}".format(category) if category else ""

        line = "{}. {}{}{}\n   {}{}{}\n   goods_sign: {}".format(
            i, name, coupon_tag, sales_str, price_str, mall_str, cat_str, goods_sign)
        if image:
            line += "\n   图片: {}".format(image)
        lines.append(line)

    return "\n\n".join(lines)


def format_detail(data):
    if not data.get("ok"):
        return "查询失败：" + data.get("error", "未知错误")
    item = data.get("data", {})
    if not item:
        return "未找到该商品信息"

    name = item.get("goods_name", "")
    brand = item.get("brand_name", "")
    mall = item.get("mall_name", "")
    category = item.get("category_name", "")
    final_price = item.get("final_price", 0)
    min_group_price = item.get("min_group_price", 0)
    min_normal_price = item.get("min_normal_price", 0)
    coupon_discount = item.get("coupon_discount", 0)
    coupon_min_order = item.get("coupon_min_order", 0)
    has_coupon = item.get("has_coupon", False)
    sales = item.get("sales_tip", "")
    goods_sign = item.get("goods_sign", "")
    goods_id = item.get("goods_id", "")
    image = item.get("goods_image_url", "")
    gallery = item.get("goods_gallery_urls", [])
    sku_list = item.get("sku_list", [])

    lines = [name, "品牌：{} | 店铺：{} | 分类：{}".format(brand or "未知", mall or "未知", category or "未知")]
    if coupon_discount > 0 and has_coupon:
        lines.append("到手价：¥{}（拼团价¥{} - 优惠券¥{}，满¥{}可用）".format(
            final_price, min_group_price, coupon_discount, coupon_min_order))
    else:
        lines.append("拼团价：¥{} | 单买价：¥{}".format(min_group_price, min_normal_price))
    if sales:
        lines.append("销量：{}".format(sales))
    if image:
        lines.append("主图：{}".format(image))
    if len(gallery) > 1:
        lines.append("图库（{}张）：{}".format(len(gallery), gallery[1] if len(gallery) > 1 else ""))
    if sku_list:
        lines.append("规格：")
        for sku in sku_list[:10]:
            lines.append("  {} - ¥{}".format(sku.get("spec", ""), sku.get("price", 0)))
    lines.append("goods_sign: {}".format(goods_sign))
    lines.append("goods_id: {}".format(goods_id))
    return "\n".join(lines)


def format_explore(data):
    if not data.get("ok"):
        return "查询失败：" + data.get("error", "未知错误")
    results = data.get("data", [])
    if not results:
        return "暂无商品"

    lines = ["为您精选 {} 件好货：\n".format(len(results))]
    for i, item in enumerate(results, 1):
        name = item.get("goods_name", "")
        final_price = item.get("final_price", 0)
        min_group_price = item.get("min_group_price", 0)
        coupon_discount = item.get("coupon_discount", 0)
        has_coupon = item.get("has_coupon", False)
        sales = item.get("sales_tip", "")
        mall = item.get("mall_name", "")
        category = item.get("category_name", "")
        goods_sign = item.get("goods_sign", "")
        image = item.get("goods_image_url", "")

        if coupon_discount > 0 and has_coupon:
            price_str = "到手价¥{}".format(final_price)
        else:
            price_str = "¥{}".format(min_group_price)

        sales_str = " | 销量{}".format(sales) if sales else ""
        mall_str = " | {}".format(mall) if mall else ""
        cat_str = " | {}".format(category) if category else ""

        line = "{}. {} | {}{}{}{}\n   goods_sign: {}".format(
            i, name, price_str, sales_str, mall_str, cat_str, goods_sign)
        if image:
            line += "\n   图片: {}".format(image)
        lines.append(line)
    return "\n\n".join(lines)


def tool_search_goods(params):
    keyword = params.get("keyword", "")
    if not keyword:
        return json.dumps({"error": "keyword参数必填"}, ensure_ascii=False)

    SORT_MAP = {"综合排序": 0, "价格升序": 1, "价格降序": 2, "销量排序": 3, "优惠券面额": 9}
    p = {"keyword": keyword, "page": params.get("page", 1), "page_size": max(10, min(params.get("page_size", 20), 100))}
    if params.get("sort_type"):
        p["sort_type"] = SORT_MAP.get(params["sort_type"], 0)
    if params.get("has_coupon") is not None:
        p["with_coupon"] = "true" if params["has_coupon"] else "false"
    if params.get("price_min") is not None:
        p["range_from"] = int(params["price_min"] * 100)
    if params.get("price_max") is not None:
        p["range_to"] = int(params["price_max"] * 100)

    data = call_proxy("search", p)
    return json.dumps({"content": format_search_results(data)}, ensure_ascii=False)


def tool_get_goods_detail(params):
    goods_sign = params.get("goods_sign", "")
    if not goods_sign:
        return json.dumps({"error": "goods_sign参数必填"}, ensure_ascii=False)

    data = call_proxy("detail", {"goods_sign": goods_sign})
    return json.dumps({"content": format_detail(data)}, ensure_ascii=False)


def tool_explore_deals(params):
    channel = params.get("channel", "销量榜")
    limit = params.get("limit", 20)

    if channel in ACTIVITY_TAG_MAP:
        p = {"activity_tags": ACTIVITY_TAG_MAP[channel], "limit": max(10, min(limit, 100))}
    elif channel in CHANNEL_MAP:
        p = {"channel_type": CHANNEL_MAP[channel], "limit": max(10, min(limit, 100))}
    else:
        return json.dumps({"content": "未知频道：{}。可选频道：销量榜、热销榜、百亿补贴、秒杀、千万补贴、千万神券、品牌黑标、精选爆品、相似推荐".format(channel)}, ensure_ascii=False)

    data = call_proxy("recommend", p)
    return json.dumps({"content": format_explore(data)}, ensure_ascii=False)


TOOLS = {
    "search_goods": tool_search_goods,
    "get_goods_detail": tool_get_goods_detail,
    "explore_deals": tool_explore_deals,
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
