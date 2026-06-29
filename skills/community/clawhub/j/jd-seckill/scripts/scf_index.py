# -*- coding: utf-8 -*-
"""
京东秒杀代理 v5.0 - 腾讯云SCF Web函数
函数名：jd-seckill-proxy
v5.0 变更：SCF端做筛选+排序+分页，只返回一页结果（解决6MB响应限制）

缓存逻辑：
- 首次请求：全量拉取京东API(~60秒)，硬过滤后缓存
- 后续请求：从缓存筛选+排序+分页，秒级返回

SCF硬过滤（缓存层，不可降级）：
- 只保留京东自营和旗舰店商品
- 好评率≥97%

SCF动态筛选（请求层，可降级）：
- 关键词匹配（类目>品牌>商品名>标签，子串+子序列）
- 好评率筛选（默认≥98%，固定不降级）
- 销量筛选（默认≥5000，可降级5000→2000→1000→500→不限）
- 价格筛选（max_price）
- 排序（score/price/discount）
- 分页（page/page_size）

接口：jingfen(带缓存+筛选) / goods_query / material / category / activity / promote
请求格式：{"type":"xxx","params":{...}}
鉴权：X-Proxy-Token header
"""
import json
import time
import os
import hashlib
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import Counter

# ===== 环境变量 =====
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
APP_KEY = os.environ.get("JD_APP_KEY", "")
APP_SECRET = os.environ.get("JD_APP_SECRET", "")
SITE_ID = os.environ.get("JD_SITE_ID", "")
UNION_ID = os.environ.get("JD_UNION_ID", "")

JD_API_URL = "https://api.jd.com/routerjson"

# ===== 京东秒杀配置 =====
ELITE_ID = 33
CACHE_TTL = 12 * 3600  # 12小时
MAX_FETCH_PAGES = 300
GOOD_COMMENTS_MIN = 97  # 好评率硬底线（SCF缓存层过滤）

# ===== 内存缓存 =====
_cache = {}

# ===== 支持的type白名单 =====
SUPPORTED_TYPES = {"goods_query", "jingfen", "material", "category", "activity", "promote"}

# ===== 爆品标签集合 =====
HOT_TAGS = {"秒杀", "限时秒杀", "限量", "限时", "爆款", "超万人正在疯抢", "同款高转化", "破价品"}


def _md5_sign(params, app_secret):
    """京东API签名: MD5(secret + key1value1key2value2... + secret)"""
    sorted_keys = sorted(params.keys())
    raw = app_secret
    for k in sorted_keys:
        raw += str(k) + str(params[k])
    raw += app_secret
    return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()


def _call_jd(method, biz_params):
    """调用京东API"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    params = {
        "method": method,
        "app_key": APP_KEY,
        "timestamp": timestamp,
        "format": "json",
        "v": "1.0",
        "sign_method": "md5",
        "360buy_param_json": json.dumps(biz_params, ensure_ascii=False, separators=(",", ":")),
    }
    params["sign"] = _md5_sign(params, APP_SECRET)

    body = "&".join(
        "{}={}".format(k, str(v)) for k, v in params.items()
    ).encode("utf-8")

    req = urllib.request.Request(
        JD_API_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error_response": {"msg": str(e)}}


def _extract_biz_data(result, method):
    """提取业务数据"""
    response_key = method.replace(".", "_") + "_response"
    response_key2 = method.replace(".", "_") + "_responce"
    biz = result.get(response_key) or result.get(response_key2)

    if not biz:
        if "error_response" in result:
            err = result["error_response"]
            return None, "查询失败：" + err.get("zh_desc", err.get("en_desc", "服务异常"))
        return None, "查询失败：未知返回格式"

    if biz.get("code") != "0":
        return None, "查询失败：" + biz.get("errorMessage", "系统错误")

    qr = biz.get("queryResult") or biz.get("getResult")
    if qr and isinstance(qr, str):
        try:
            qr = json.loads(qr)
        except Exception:
            return None, "数据解析失败"

    if isinstance(qr, dict):
        code = qr.get("code", -1)
        if code == 200:
            return qr, None
        elif code == 403:
            return None, "该接口暂无访问权限"
        else:
            return None, qr.get("message", "查询失败(code=" + str(code) + ")")

    return None, "无业务数据"


def _promote_url(material_id, coupon_url=None, sub_union_id=None):
    """转链 - jd.union.open.promotion.bysubunionid.get"""
    promo_req = {
        "materialId": material_id,
    }
    if UNION_ID:
        promo_req["unionId"] = int(UNION_ID)
    if coupon_url:
        promo_req["couponUrl"] = coupon_url
    if sub_union_id:
        promo_req["subUnionId"] = sub_union_id
    promo_req["sceneId"] = 1
    promo_req["chainType"] = 3

    method = "jd.union.open.promotion.bysubunionid.get"
    result = _call_jd(method, {"promotionCodeReq": promo_req})

    response_key = method.replace(".", "_") + "_response"
    response_key2 = method.replace(".", "_") + "_responce"
    biz = result.get(response_key) or result.get(response_key2)

    if not biz:
        if "error_response" in result:
            err = result["error_response"]
            return None, err.get("zh_desc", err.get("en_desc", "转链失败"))
        return None, "转链失败：未知返回格式"

    if biz.get("code") != "0":
        return None, biz.get("errorMessage", "转链失败")

    qr = biz.get("getResult")
    if qr and isinstance(qr, str):
        try:
            qr = json.loads(qr)
        except Exception:
            return None, "转链数据解析失败"

    if isinstance(qr, dict):
        if qr.get("code") == 200:
            data_obj = qr.get("data", {})
            if data_obj:
                return data_obj, None
            return None, "转链返回空数据"
        elif qr.get("code") == 403:
            return None, "转链接口无访问权限，需申请高级API权限"
        return None, qr.get("message", "转链失败(code=" + str(qr.get("code")) + ")")

    return None, "转链无数据"


# ===== 缓存相关函数 =====

def _simplify_for_cache(g):
    """精简京粉商品数据，只保留需要的字段"""
    price_info = g.get("priceInfo", {})
    comm_info = g.get("commissionInfo", {})
    shop_info = g.get("shopInfo", {})
    cat_info = g.get("categoryInfo", {})
    img_info = g.get("imageInfo", {})
    purchase_info = g.get("purchasePriceInfo", {})
    images = img_info.get("imageList", [])

    return {
        "skuName": g.get("skuName", ""),
        "brandName": g.get("brandName", ""),
        "isJd": g.get("isJd", 0),
        "owner": g.get("owner", ""),
        "shopName": shop_info.get("shopName", ""),
        "price": price_info.get("price", ""),
        "lowestPrice": price_info.get("lowestPrice", ""),
        "lowestCouponPrice": price_info.get("lowestCouponPrice", ""),
        "purchasePrice": purchase_info.get("purchasePrice", ""),
        "commissionShare": comm_info.get("commissionShare", ""),
        "inOrderCount30Days": int(g.get("inOrderCount30Days", 0) or 0),
        "goodCommentsShare": float(g.get("goodCommentsShare", 0) or 0),
        "comments": int(g.get("comments", 0) or 0),
        "isHot": g.get("isHot", 0),
        "materialUrl": g.get("materialUrl", ""),
        "imageUrl": images[0].get("url", "") if images else "",
        "cid1Name": cat_info.get("cid1Name", ""),
        "cid2Name": cat_info.get("cid2Name", ""),
        "cid3Name": cat_info.get("cid3Name", ""),
        "skuTags": [t.get("name", "") for t in g.get("skuTagList", []) if t.get("name")],
    }


def _is_quality_item(g):
    """SCF硬过滤：只保留自营/旗舰店 + 好评≥97%"""
    shop_name = g.get("shopInfo", {}).get("shopName", "")
    is_jd = g.get("isJd") == 1 or "自营" in shop_name
    is_flagship = "旗舰店" in shop_name
    if not (is_jd or is_flagship):
        return False
    gc = float(g.get("goodCommentsShare", 0) or 0)
    if gc < GOOD_COMMENTS_MIN:
        return False
    return True


def _fetch_and_cache(elite_id):
    """全量拉取京东京粉数据，过滤后缓存"""
    all_items = []
    for page in range(1, MAX_FETCH_PAGES + 1):
        goods_req = {
            "eliteId": elite_id,
            "pageIndex": page,
            "pageSize": 50,
        }
        method = "jd.union.open.goods.jingfen.query"
        result = _call_jd(method, {"goodsReq": goods_req})
        data, error = _extract_biz_data(result, method)
        if error or not data:
            break
        goods = data.get("data", [])
        if not goods:
            break
        for g in goods:
            if _is_quality_item(g):
                all_items.append(_simplify_for_cache(g))

    _cache[elite_id] = {"data": all_items, "ts": time.time(), "fetching": False}
    return all_items


# ===== SCF端筛选/排序/匹配函数 =====

def _is_subsequence(kw, text):
    """子序列匹配：kw的字符按顺序出现在text中，但不要求连续"""
    it = iter(text)
    return all(c in it for c in kw)


def _match_keyword_scf(g, keyword):
    """关键词匹配：类目优先 > 品牌名 > 商品名 > 标签"""
    kw = keyword.lower()
    cat1 = g.get("cid1Name", "").lower()
    cat2 = g.get("cid2Name", "").lower()
    cat3 = g.get("cid3Name", "").lower()
    brand = g.get("brandName", "").lower()
    name = g.get("skuName", "").lower()
    tags = [t.lower() for t in g.get("skuTags", [])]

    for text in [cat1, cat2, cat3]:
        if kw in text or _is_subsequence(kw, text):
            return True
    if kw in brand or _is_subsequence(kw, brand):
        return True
    if kw in name or _is_subsequence(kw, name):
        return True
    if any(kw in tag for tag in tags):
        return True
    return False


def _get_item_price(g):
    """获取到手价"""
    coupon = float(g.get("lowestCouponPrice", 0) or 0)
    if coupon > 0:
        return coupon
    return float(g.get("lowestPrice", 0) or g.get("price", 0) or 0)


def _get_item_ref_price(g):
    """获取参考价（原价）"""
    ref = float(g.get("price", 0) or 0)
    if ref <= 0:
        ref = float(g.get("lowestPrice", 0) or 0)
    return ref


def _get_item_discount(g):
    """获取折扣力度（百分比，如30表示打了7折/省了30%）"""
    ref = _get_item_ref_price(g)
    coupon = _get_item_price(g)
    if ref > 0 and coupon > 0 and ref > coupon:
        return round((ref - coupon) / ref * 100, 1)
    return 0


def _calc_score_scf(g):
    """综合评分（满分100）
    折扣力度30 + 销量25 + 推广热度15 + 好评15 + 自营10 + 爆品标签5
    """
    discount = _get_item_discount(g)
    comm_share = float(g.get("commissionShare", 0) or 0)
    orders = int(g.get("inOrderCount30Days", 0) or 0)
    good_comments = float(g.get("goodCommentsShare", 0) or 0)
    shop_name = g.get("shopName", "")
    is_jd = 1 if (g.get("isJd") == 1 or "自营" in shop_name) else 0
    tags = g.get("skuTags", [])

    # 折扣力度 0-30
    discount_score = min(discount * 0.5, 30)

    # 销量 0-25
    comm_score = min(comm_share, 15)

    if orders >= 10000:
        sales_score = 25
    elif orders >= 5000:
        sales_score = 20
    elif orders >= 2000:
        sales_score = 15
    elif orders >= 1000:
        sales_score = 10
    elif orders >= 500:
        sales_score = 6
    elif orders >= 100:
        sales_score = 3
    else:
        sales_score = 0

    comments_score = min(good_comments / 100 * 15, 15)
    jd_score = 10 if is_jd else 0
    tag_score = min(sum(2 for t in tags if t in HOT_TAGS), 5)

    return round(discount_score + comm_score + sales_score + comments_score + jd_score + tag_score, 1)


def _sort_scf(items, sort_by):
    """排序：score=综合(默认)，price=到手价升序，discount=折扣力度降序"""
    if sort_by == "price":
        return sorted(items, key=lambda g: _get_item_price(g))
    elif sort_by == "discount":
        return sorted(items, key=lambda g: _get_item_discount(g), reverse=True)
    else:
        return sorted(items, key=lambda g: _calc_score_scf(g), reverse=True)


def _build_category_overview_scf(items, top_n=5):
    """构建分类概览"""
    cat_counter = Counter()
    for g in items:
        cat = g.get("cid1Name", "")
        if cat:
            cat_counter[cat] += 1
    result = []
    for cat, cnt in cat_counter.most_common(top_n):
        result.append({"category": cat, "count": cnt})
    return result


DEGRADE_THRESHOLD = 10  # 结果<10条触发降级


def _filter_and_degrade(cached_data, keyword, min_gc_user):
    """好评+销量筛选，好评≥98%固定不降，只降销量

    降级路径（好评固定≥98%）：
      默认:  好评≥98% + 销量≥5000
      降级1: 好评≥98% + 销量≥2000
      降级2: 好评≥98% + 销量≥1000
      降级3: 好评≥98% + 销量≥500
      底线:  好评≥98% + 不限销量

    用户指定min_good_comments=99/100时，好评率用用户值，同样只降销量。

    返回: (filtered_items, actual_gc_min, actual_sales_min)
    """
    # 先做关键词匹配
    if keyword:
        kw_data = [g for g in cached_data if _match_keyword_scf(g, keyword)]
    else:
        kw_data = cached_data

    # 好评率固定，不低于98%
    gc_min = max(min_gc_user, 98)

    # 只降销量，好评不降级
    degrade_levels = [
        (gc_min, 5000),
        (gc_min, 2000),
        (gc_min, 1000),
        (gc_min, 500),
        (gc_min, 0),
    ]

    for gc, sales_min in degrade_levels:
        filtered = [g for g in kw_data
                    if float(g.get("goodCommentsShare", 0) or 0) >= gc
                    and int(g.get("inOrderCount30Days", 0) or 0) >= sales_min]
        if len(filtered) >= DEGRADE_THRESHOLD or (gc, sales_min) == degrade_levels[-1]:
            return filtered, gc, sales_min

    return [], gc_min, 0


def _filter_and_paginate(cached_data, params):
    """从缓存数据中筛选、降级、排序、分页

    返回: {
        "items": [...],      # 当前页数据（含_score）
        "total": int,         # 筛选后总数
        "page": int,
        "page_size": int,
        "filter_applied": {...},
        "category_overview": [...]
    }
    """
    keyword = str(params.get("keyword", "")).strip().lower()
    min_gc_user = float(params.get("min_good_comments", 98) or 98)

    # 1. 好评+销量筛选（含降级逻辑，好评固定不降）
    data, actual_gc, actual_sales = _filter_and_degrade(cached_data, keyword, min_gc_user)

    # 2. 价格筛选
    max_price = params.get("max_price")
    if max_price:
        try:
            max_price = float(max_price)
            data = [g for g in data if 0 < _get_item_price(g) <= max_price]
        except (ValueError, TypeError):
            max_price = None

    total = len(data)

    # 3. 排序
    sort_by = params.get("sort", "score")
    data = _sort_scf(data, sort_by)

    # 4. 分类概览（从筛选后、分页前的数据生成）
    category_overview = _build_category_overview_scf(data)

    # 5. 分页
    page = int(params.get("page", 1) or 1)
    if page < 1:
        page = 1
    page_size = int(params.get("page_size", 50) or 50)
    if page_size < 1:
        page_size = 50
    if page_size > 100:
        page_size = 100

    start = (page - 1) * page_size
    end = start + page_size
    page_data = data[start:end]

    # 为每条数据补充score和discount（用副本，不修改缓存原对象）
    scored_page = []
    for g in page_data:
        item = dict(g)
        item["_score"] = _calc_score_scf(g)
        item["_discount"] = _get_item_discount(g)
        scored_page.append(item)

    return {
        "items": scored_page,
        "total": total,
        "page": page,
        "page_size": page_size,
        "filter_applied": {
            "keyword": keyword or None,
            "min_good_comments": actual_gc,
            "min_sales": actual_sales,
            "max_price": max_price if max_price else None,
            "sort": sort_by,
        },
        "category_overview": category_overview,
    }


# ===== 原始代理函数（保留，供其他用途使用） =====

def _simplify_goods_query_item(item):
    """精简 goods.query 返回的商品数据"""
    pi = item.get("priceInfo", {})
    ci = item.get("commissionInfo", {})
    cpi = item.get("couponInfo", {})
    coupon_list = cpi.get("couponList", [])
    best_coupon = next((c for c in coupon_list if c.get("isBest") == 1), None)
    shop = item.get("shopInfo", {})
    cat = item.get("categoryInfo", {})

    return {
        "itemId": item.get("itemId", ""),
        "skuName": item.get("skuName", ""),
        "spuid": item.get("spuid", ""),
        "brandName": item.get("brandName", ""),
        "shopName": shop.get("shopName", ""),
        "isJdSale": item.get("isJdSale", 0),
        "owner": item.get("owner", ""),
        "deliveryType": item.get("deliveryType", 0),
        "price": pi.get("price", ""),
        "lowestPrice": pi.get("lowestPrice", ""),
        "lowestCouponPrice": pi.get("lowestCouponPrice", ""),
        "commissionShare": ci.get("commissionShare", ""),
        "commission": ci.get("commission", ""),
        "couponCommission": ci.get("couponCommission", ""),
        "inOrderCount30Days": item.get("inOrderCount30Days", 0),
        "goodCommentsShare": item.get("goodCommentsShare", ""),
        "comments": item.get("comments", 0),
        "materialUrl": item.get("materialUrl", ""),
        "imageUrl": (item.get("imageInfo", {}).get("imageList") or [{}])[0].get("url", ""),
        "categoryInfo": cat,
        "bestCouponDiscount": best_coupon.get("discount", "") if best_coupon else "",
        "bestCouponLink": best_coupon.get("link", "") if best_coupon else "",
        "isHot": item.get("isHot", 0),
        "isOversea": item.get("isOversea", 0),
    }


def _proxy_goods_query(params):
    """关键词搜索 - goods.query（结果自动转链）"""
    dto = {}
    if params.get("keyword"):
        dto["keyword"] = str(params["keyword"])
    if params.get("pageIndex"):
        dto["pageIndex"] = str(params["pageIndex"])
    if params.get("pageSize"):
        dto["pageSize"] = str(min(params["pageSize"], 30))
    if params.get("sortName"):
        dto["sortName"] = params["sortName"]
        dto["sort"] = params.get("sort", "desc")
    if params.get("hasCoupon"):
        dto["isCoupon"] = "1"
    if params.get("isSelf") is not None:
        dto["owner"] = "g" if params["isSelf"] else "p"
    elif params.get("owner"):
        dto["owner"] = params["owner"]
    if params.get("cid1"):
        dto["cid1"] = str(params["cid1"])
    if params.get("cid2"):
        dto["cid2"] = str(params["cid2"])
    if params.get("cid3"):
        dto["cid3"] = str(params["cid3"])
    if params.get("hasBestCoupon"):
        dto["hasBestCoupon"] = "1"
    if params.get("commissionShareStart"):
        dto["commissionShareStart"] = str(params["commissionShareStart"])
    if params.get("commissionShareEnd"):
        dto["commissionShareEnd"] = str(params["commissionShareEnd"])
    if params.get("priceFrom"):
        dto["pricefrom"] = str(params["priceFrom"])
    if params.get("priceTo"):
        dto["priceto"] = str(params["priceTo"])
    if params.get("fields"):
        dto["fields"] = params["fields"]

    method = "jd.union.open.goods.query"
    result = _call_jd(method, {"goodsReqDTO": dto})
    data, error = _extract_biz_data(result, method)
    if error:
        return {"ok": False, "error": error}

    items = data.get("data", [])
    simplified = [_simplify_goods_query_item(item) for item in items[:30]]

    for item in simplified:
        mat_url = item.get("materialUrl", "")
        coupon_link = item.get("bestCouponLink", "")
        if mat_url:
            material_id = coupon_link if coupon_link else mat_url
            promo_data, _ = _promote_url(material_id, coupon_url=coupon_link if coupon_link else None)
            if promo_data:
                item["clickUrl"] = promo_data.get("shortURL", "") or promo_data.get("clickURL", "")
                item["jCommand"] = promo_data.get("jCommand", "")
                item["wechatShortLink"] = promo_data.get("wechatShortLink", "")
        if not item.get("clickUrl"):
            item["clickUrl"] = mat_url

    return {"ok": True, "data": simplified, "total": data.get("totalCount", len(simplified))}


def _proxy_jingfen(params):
    """频道推荐 - jingfen.query
    京东秒杀(eliteId=33)使用缓存+筛选+分页
    其他eliteId走原始逻辑
    """
    elite_id = params.get("eliteId", ELITE_ID)

    if elite_id == ELITE_ID:
        # ===== 京东秒杀 - 使用缓存+筛选+分页 =====
        cached = _cache.get(elite_id)
        if not cached or (time.time() - cached.get("ts", 0)) >= CACHE_TTL:
            # 缓存未命中或已过期
            if cached and cached.get("fetching"):
                # 另一个请求正在拉取
                return {
                    "ok": True,
                    "data": {"items": [], "total": 0, "page": 1, "page_size": 50},
                    "cached": False,
                    "warming": True,
                    "msg": "缓存正在建立中，请稍候约1分钟后再次查询",
                }
            # 标记正在拉取
            if cached:
                cached["fetching"] = True
            else:
                _cache[elite_id] = {"data": [], "ts": 0, "fetching": True}
            # 全量拉取（约60秒）
            _fetch_and_cache(elite_id)
            cached = _cache.get(elite_id)

        if not cached or not cached.get("data"):
            return {
                "ok": True,
                "data": {"items": [], "total": 0, "page": 1, "page_size": 50},
                "cached": False,
                "warming": True,
                "msg": "缓存正在建立中，请稍候约1分钟后再次查询",
            }

        # 缓存命中 - 筛选+排序+分页
        result = _filter_and_paginate(cached["data"], params)
        return {
            "ok": True,
            "data": result,
            "cached": True,
            "cache_total": len(cached["data"]),
        }

    # ===== 其他eliteId - 原始逻辑，无缓存 =====
    goods_req = {
        "eliteId": elite_id,
        "pageIndex": params.get("pageIndex", 1),
        "pageSize": params.get("pageSize", 15),
    }
    if params.get("sortName"):
        goods_req["sortName"] = params["sortName"]
        goods_req["sort"] = params.get("sort", "desc")
    if params.get("hasBestCoupon"):
        goods_req["hasBestCoupon"] = 1

    method = "jd.union.open.goods.jingfen.query"
    result = _call_jd(method, {"goodsReq": goods_req})
    data, error = _extract_biz_data(result, method)
    if error:
        return {"ok": False, "error": error}
    return {"ok": True, "data": data}


def _proxy_material(params):
    """物料精选 - material.query"""
    goods_req = {
        "eliteId": params.get("eliteId", 10),
        "pageIndex": params.get("pageIndex", 1),
        "pageSize": params.get("pageSize", 15),
    }
    if params.get("sortName"):
        goods_req["sortName"] = params["sortName"]
        goods_req["sort"] = params.get("sort", "desc")
    if params.get("hasBestCoupon"):
        goods_req["hasBestCoupon"] = 1

    method = "jd.union.open.goods.material.query"
    result = _call_jd(method, {"goodsReq": goods_req})
    data, error = _extract_biz_data(result, method)
    if error:
        return {"ok": False, "error": error}
    return {"ok": True, "data": data}


def _proxy_category(params):
    """商品类目 - category.goods.get"""
    req = {}
    if params.get("parentId") is not None:
        req["parentId"] = params["parentId"]
    if params.get("grade") is not None:
        req["grade"] = params["grade"]

    method = "jd.union.open.category.goods.get"
    result = _call_jd(method, {"req": req})
    data, error = _extract_biz_data(result, method)
    if error:
        return {"ok": False, "error": error}
    return {"ok": True, "data": data}


def _proxy_activity(params):
    """促销活动 - activity.query"""
    activity_req = {
        "eliteId": params.get("eliteId", 1),
        "pageIndex": params.get("pageIndex", 1),
        "pageSize": params.get("pageSize", 20),
    }

    method = "jd.union.open.activity.query"
    result = _call_jd(method, {"activityReq": activity_req})
    data, error = _extract_biz_data(result, method)
    if error:
        return {"ok": False, "error": error}
    return {"ok": True, "data": data}


def _proxy_promote(params):
    """转链接口 - jd.union.open.promotion.bysubunionid.get"""
    material_id = params.get("materialId", "")
    if not material_id:
        return {"ok": False, "error": "materialId is required"}

    coupon_url = params.get("couponUrl")
    sub_union_id = params.get("subUnionId")

    promo_data, error = _promote_url(material_id, coupon_url=coupon_url, sub_union_id=sub_union_id)
    if error:
        return {"ok": False, "error": error}

    return {"ok": True, "data": promo_data}


# ===== 路由分发 =====
TYPE_HANDLER = {
    "goods_query": _proxy_goods_query,
    "jingfen": _proxy_jingfen,
    "material": _proxy_material,
    "category": _proxy_category,
    "activity": _proxy_activity,
    "promote": _proxy_promote,
}


class Handler(BaseHTTPRequestHandler):
    """SCF Web函数 HTTP Handler"""

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Proxy-Token")
        self.end_headers()

    def do_GET(self):
        self._json(200, {
            "status": "ok",
            "service": "jd-seckill-proxy",
            "version": "5.0",
            "types": sorted(SUPPORTED_TYPES),
        })

    def do_POST(self):
        if self.headers.get("X-Proxy-Token", "") != PROXY_TOKEN:
            return self._json(403, {"ok": False, "error": "Forbidden"})

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except Exception:
            return self._json(400, {"ok": False, "error": "Invalid JSON"})

        rtype = body.get("type", "")
        params = body.get("params", {})

        if not rtype:
            action = body.get("action", "jingfen")
            type_map = {
                "jingfen": "jingfen",
                "material": "material",
                "category": "category",
                "activity": "activity",
                "search": "goods_query",
                "query": "goods_query",
                "promote": "promote",
            }
            rtype = type_map.get(action, action)
            params = {k: v for k, v in body.items() if k not in ("action", "token")}

        if rtype not in SUPPORTED_TYPES:
            return self._json(400, {
                "ok": False,
                "error": "Unknown type: " + rtype + ". Supported: " + ", ".join(sorted(SUPPORTED_TYPES)),
            })

        handler = TYPE_HANDLER[rtype]
        result = handler(params)
        return self._json(200, result)

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
