#!/usr/bin/env python3
"""9.9包邮 - 超值好货查询（缓存版 v3）

配合独立SCF函数 jd-99-baoyou-proxy 使用。
SCF负责：缓存全量数据(12h TTL) + 硬过滤(自营/旗舰店 + 好评≥97%)
         + 好评/销量动态筛选+降级 + 关键词匹配 + 排序 + 分页
MCP负责：发送参数、接收结果、构建用户提示语

降级逻辑（SCF端执行，关键词结果<10条时触发，好评≥98%固定不降，只降销量）：
  默认:  好评≥98% + 销量≥2000
  降级1: 好评≥98% + 销量≥1000
  降级2: 好评≥98% + 销量≥500
  降级3: 好评≥98% + 销量≥200
  底线:  好评≥98% + 不限销量

用户指定min_good_comments=99/100时，好评率用用户值，同样只降销量。
"""

import sys
import json
import urllib.request
import urllib.error

# ===== 配置 =====
PROXY_URL = "https://1439498936-ieoa5v7nf9.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
ELITE_ID = 10  # 9.9包邮频道

TIMEOUT_SHORT = 8    # 短超时：检测冷启动
TIMEOUT_LONG = 90    # 长超时：等待缓存建立完成

PAGE_SIZE = 50       # 每页展示50条
SCARCITY_THRESHOLD = 15   # ≤15条触发稀缺提醒


def _scf_call(params, timeout=TIMEOUT_SHORT):
    """调用SCF代理"""
    payload = json.dumps({"type": "jingfen", "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=payload,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            return {"ok": False, "error": "timeout"}
        return {"ok": False, "error": str(e)}
    except Exception as e:
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
    """获取折扣力度（百分比，如30表示打了7折/省了30%）"""
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
        "tags": g.get("skuTags", []),
        "image_url": g.get("imageUrl", ""),
        "buy_url": material_url,
        "category": g.get("cid1Name", ""),
        "category2": g.get("cid2Name", ""),
        "category3": g.get("cid3Name", ""),
        "orders_30d": int(g.get("inOrderCount30Days", 0) or 0),
        "good_comments": float(g.get("goodCommentsShare", 0) or 0),
        "score": g.get("_score", 0),
    }


def _build_quality_desc(gc_min, sales_min):
    """构建品质背书描述（动态显示实际筛选标准）"""
    if sales_min > 0:
        return f"已精选好评≥{int(gc_min)}%、销量≥{sales_min}的京东自营商品"
    else:
        return f"已精选好评≥{int(gc_min)}%的京东自营商品"


def _build_category_overview(cat_list):
    """从SCF返回的分类概览构建提示语"""
    if not cat_list:
        return ""
    parts = []
    for c in cat_list[:5]:
        parts.append(f"{c['category']}({c['count']}条)")
    if parts:
        return "热门分类：" + "、".join(parts) + "…说\"看手机\"或\"看家电\"可按品类筛选。"
    return ""


def tool_get_99_baoyou_items(params):
    """9.9包邮主查询函数"""
    keyword = str(params.get("keyword", "")).strip()
    max_price = float(params.get("max_price", 0) or 0)
    sort_by = params.get("sort", "score")
    min_gc_user = float(params.get("min_good_comments", 98) or 98)
    page = int(params.get("page", 1) or 1)
    if page < 1:
        page = 1

    # ===== 第一步：从SCF获取缓存数据（带筛选+分页）=====
    scf_params = {
        "eliteId": ELITE_ID,
        "page": page,
        "page_size": PAGE_SIZE,
        "sort": sort_by,
    }
    if keyword:
        scf_params["keyword"] = keyword
    if max_price > 0:
        scf_params["max_price"] = max_price
    if min_gc_user != 98:
        scf_params["min_good_comments"] = min_gc_user

    data = _scf_call(scf_params, timeout=TIMEOUT_SHORT)

    # 冷启动检测：超时说明SCF正在全量拉取数据
    if not data.get("ok"):
        if data.get("error") == "timeout":
            # 再等一次，用长超时
            data = _scf_call(scf_params, timeout=TIMEOUT_LONG)
            if not data.get("ok"):
                return json.dumps({
                    "content": "",
                    "summary": "正在为您精选9.9包邮好货，数据量较大，请稍候约30秒后再次查询。"
                }, ensure_ascii=False)
        else:
            return json.dumps({
                "content": "",
                "summary": "查询失败：" + data.get("error", "未知错误") + "，请稍后重试。"
            }, ensure_ascii=False)

    # 冷启动中（缓存正在建立）
    if data.get("warming"):
        return json.dumps({
            "content": "",
            "summary": "正在为您精选9.9包邮好货，数据量较大，请稍候约30秒后再次查询。"
        }, ensure_ascii=False)

    # ===== 第二步：解析SCF返回的数据 =====
    scf_data = data.get("data", {})
    items = scf_data.get("items", [])
    total = scf_data.get("total", 0)
    filter_applied = scf_data.get("filter_applied", {})
    category_overview = scf_data.get("category_overview", [])
    cache_total = data.get("cache_total", 0)

    if not items and total == 0:
        # 0结果
        if keyword:
            cat_str = _build_category_overview(category_overview)
            msg = f'未找到与「{keyword}」相关的9.9包邮好货。换个关键词试试'
            if cat_str:
                msg += f'，或浏览热门分类：{cat_str}'
            else:
                msg += '。'
        else:
            msg = "暂无符合条件的9.9包邮好货，请稍后再试。"
        return json.dumps({"content": "", "summary": msg}, ensure_ascii=False)

    # ===== 第三步：获取实际筛选标准 =====
    actual_gc = filter_applied.get("min_good_comments", 98)
    actual_sales = filter_applied.get("min_sales", 0)
    quality_desc = _build_quality_desc(actual_gc, actual_sales)

    # ===== 第四步：构建商品列表 =====
    results = [_format_item(g) for g in items]

    # ===== 第五步：构建场景提示语 =====
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
        # 稀缺，全展示不分页
        if cond_str:
            hints.append(f'{cond_str}的9.9包邮好货仅{total}条，{quality_desc}，手慢无！')
        else:
            hints.append(f'9.9包邮好货仅{total}条，{quality_desc}，手慢无！')
        cat_str = _build_category_overview(category_overview)
        if cat_str:
            hints.append(f'换个品类看看？{cat_str}')

    elif keyword and total > SCARCITY_THRESHOLD:
        # 带品类词，结果较多
        if cond_str:
            hints.append(f'{cond_str}的9.9包邮好货共{total}条，{quality_desc}。')
        else:
            hints.append(f'9.9包邮好货共{total}条，{quality_desc}。')
        if has_more:
            hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
        else:
            hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')

    elif not keyword:
        if page > 1:
            # 翻页（不加品质背书）
            if has_more:
                hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
            else:
                hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')
        else:
            # 无关键词 或 仅带价格
            if cond_str:
                hints.append(f'{cond_str}的9.9包邮好货共{total}条，{quality_desc}。')
            else:
                hints.append(f'9.9包邮好货共{total}条，{quality_desc}。')
            if has_more:
                hints.append(f'当前第{page}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
            else:
                hints.append(f'当前显示第{page_start}-{page_end}条，已全部展示。')
            cat_str = _build_category_overview(category_overview)
            if cat_str:
                hints.append(cat_str)

    return json.dumps({
        "content": json.dumps(results, ensure_ascii=False, indent=2),
        "summary": " ".join(hints)
    }, ensure_ascii=False)


TOOLS = {
    "get_99_baoyou_items": tool_get_99_baoyou_items,
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
