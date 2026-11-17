"""美团连锁酒店特价搜索 — ClawHub技能"""

import os
import json
import urllib.request
import urllib.error

# ============ SCF代理配置（硬编码，安全评分要求）============
PROXY_URL = "https://1439498936-cltb2hszg7.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
PROXY_TIMEOUT = 30


def _call_proxy(route, params):
    """调用SCF代理"""
    payload = {"type": route, "params": params}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN}
    req = urllib.request.Request(PROXY_URL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=PROXY_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result if result is not None else {}
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"error": "代理错误 " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "请求失败: " + str(e)}


def _format_hotel(hotel, index):
    """格式化单个酒店"""
    if not hotel or not isinstance(hotel, dict):
        return ""

    name = hotel.get("name", "") or "未知酒店"
    sell_price = hotel.get("sellPrice", 0)
    original_price = hotel.get("originalPrice", 0)
    discount_label = hotel.get("discountLabel", "")
    save_amount = hotel.get("saveAmount", 0)
    head_url = hotel.get("headUrl", "")
    referral_link = hotel.get("referralLink", "")
    brand = hotel.get("brand", "")
    city = hotel.get("city", "")
    rating = hotel.get("rating", "")
    valid_until = hotel.get("validUntil", "")
    price_label = hotel.get("priceLabel", "")

    # 安全转换价格为数字
    try:
        sell_price = float(sell_price) if sell_price else 0
    except (ValueError, TypeError):
        sell_price = 0
    try:
        original_price = float(original_price) if original_price else 0
    except (ValueError, TypeError):
        original_price = 0
    try:
        save_amount = float(save_amount) if save_amount else 0
    except (ValueError, TypeError):
        save_amount = 0

    lines = []

    # 图片
    if head_url:
        lines.append("![]({})".format(head_url))

    # 名称（加粗，不带链接）
    lines.append("**{}. {}**".format(index, name))

    # 价格行
    if sell_price > 0 and original_price > 0 and original_price > sell_price:
        if discount_label:
            lines.append("💰 ¥{:.0f} ← ¥{:.0f}（{}，省¥{:.0f}）".format(
                sell_price, original_price, discount_label, save_amount))
        else:
            discount = round(sell_price / original_price * 10, 1)
            lines.append("💰 ¥{:.0f} ← ¥{:.0f}（{}折，省¥{:.0f}）".format(
                sell_price, original_price, discount, save_amount))
    elif sell_price > 0:
        lines.append("💰 ¥{:.0f}".format(sell_price))

    # 详情行
    detail_parts = []
    if city:
        detail_parts.append("📍 " + str(city))
    if valid_until:
        detail_parts.append("⏰ 截至 " + str(valid_until))
    brand_rating = []
    if brand:
        brand_rating.append(str(brand))
    if rating:
        brand_rating.append("⭐" + str(rating))
    if price_label:
        brand_rating.append("🏷️" + str(price_label))
    if brand_rating:
        detail_parts.append(" | ".join(brand_rating))
    if detail_parts:
        lines.append(" ".join(detail_parts))

    # 购买链接
    if referral_link:
        lines.append("👉 [立即抢购]({})".format(referral_link))

    return "\n".join(lines)


def hotel_deals(city="", brand="", sort="discount"):
    """搜索美团全国连锁品牌酒店特价套餐

    Args:
        city: 城市名（选填），如"北京"、"上海"、"三亚"。留空返回全国热门。
        brand: 品牌名（选填），如"希尔顿"、"万豪"、"亚朵"。留空返回所有品牌。
        sort: 排序方式（选填），"discount"按折扣力度（默认），"price"按价格低到高。

    Returns:
        格式化后的酒店列表文本
    """
    params = {
        "city": city,
        "brand": brand,
        "sort": sort,
        "pageSize": 20,
    }

    result = _call_proxy("hotel_deals", params)

    # 错误处理
    if not result or not isinstance(result, dict):
        return "❌ 查询出错：服务返回异常"

    if "error" in result:
        return "❌ 查询出错: " + result["error"]

    if result.get("code") != 0:
        return "❌ 查询失败: " + result.get("message", "未知错误")

    # 解析数据（null防护）
    hotels = result.get("hotels", []) or []
    query = result.get("query", {}) or {}
    total = result.get("total", len(hotels))

    if not hotels:
        return "未找到符合条件的特价酒店，请尝试更换城市或品牌"

    # 格式化输出
    lines = []

    # 标题
    search_desc = city or "全国"
    if brand:
        search_desc = brand + "（" + search_desc + "）"
    lines.append("🏨 美团特价酒店")
    lines.append("🔍 搜索：" + search_desc)
    lines.append("共 {} 个特价套餐：".format(total))
    lines.append("")

    # 酒店列表
    for i, hotel in enumerate(hotels[:20], 1):
        hotel_text = _format_hotel(hotel, i)
        if hotel_text:
            lines.append(hotel_text)
            lines.append("")
            lines.append("---")
            lines.append("")

    # 底部提示
    lines.append("⚠️ 价格和库存实时变动，以实际下单为准")

    # 附加服务引导
    dest = city or "目的地"
    lines.append("")
    lines.append("📋 附加服务：🚄查去{}的火车票 | ✈️查去{}的机票".format(dest, dest))

    return "\n".join(lines)
