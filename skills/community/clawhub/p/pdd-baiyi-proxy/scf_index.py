# -*- coding: utf-8 -*-
"""
拼多多百亿补贴代理 v1.0 - 腾讯云SCF Web函数
函数名：pdd-baiyi-proxy

频道：百亿补贴 (channel_type=5 + activity_tags=[7])
API：pdd.ddk.goods.recommend.get

缓存逻辑：
- 首次请求：全量拉取~568条(12页×50条，每页间隔0.5s避免风控)，缓存5分钟
- 后续请求：从缓存筛选+排序+分页，秒级返回

SCF好货评分模型（deal_score，满分100）：
- 折扣力度 30%：(原价-拼团价)/原价
- 券后性价比 25%：券面额/拼团价
- 销量热度 25%：sales_tip解析为数值
- 品质保障 20%：旗舰店+评分+排行榜+标签

工具：list（百亿补贴好货推荐）
参数：keyword/category/max_price/min_price/brand_only/sort/page
分页：每页30条

请求格式：{"tool":"list","params":{"keyword":"手机","page":1}}
鉴权：X-Proxy-Token header
"""
import json
import time
import os
import hashlib
import urllib.request
import urllib.parse
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import Counter

# ===== 环境变量 =====
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
CLIENT_ID = os.environ.get("PDD_CLIENT_ID", "8b04834fe3c34a248424b67fe37a6ed1")
CLIENT_SECRET = os.environ.get("PDD_CLIENT_SECRET", "726ab92dda40a36b45af9f7dfad434f3815c28ed")
PID = os.environ.get("PDD_PID", "44444501_316125552")
PDD_API_URL = "https://gw-api.pinduoduo.com/api/router"

# ===== 百亿补贴配置 =====
CHANNEL_TYPE = 5
ACTIVITY_TAGS = "[7]"
CACHE_TTL = 300  # 5分钟
PAGE_SIZE = 30
MAX_FETCH_PAGES = 15  # 最多拉15页（实测14页到底）
FETCH_DELAY = 0.5  # 每页间隔0.5秒，避免PDD风控

# ===== 内存缓存 =====
_cache = {}

# ===== 日志 =====
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# ============ PDD API签名 ============

def _pdd_sign(params):
    """PDD签名: MD5(client_secret + key1value1key2value2...按key排序 + client_secret) 转大写"""
    sorted_keys = sorted(params.keys())
    sign_str = CLIENT_SECRET
    for k in sorted_keys:
        sign_str += f"{k}{params[k]}"
    sign_str += CLIENT_SECRET
    return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()


def _call_pdd(api_type, extra_params):
    """调用PDD联盟API"""
    params = {
        "type": api_type,
        "client_id": CLIENT_ID,
        "timestamp": str(int(time.time())),
    }
    params.update(extra_params)
    params["sign"] = _pdd_sign(params)

    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(PDD_API_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logger.error("PDD API call failed: %s | error: %s", api_type, str(e))
        return {"error_response": {"msg": str(e)}}


# ============ 推广短链接生成 ============

def _gen_promotion_urls(goods_signs):
    """批量生成PDD联盟推广短链接，返回 {goods_sign: short_url}"""
    if not goods_signs:
        return {}
    
    result_map = {}
    # PDD限制每次最多50个goods_sign，我们一页30条，一次搞定
    try:
        result = _call_pdd("pdd.ddk.goods.promotion.url.generate", {
            "goods_sign_list": json.dumps(goods_signs),
            "pid": PID,
        })
        
        resp = result.get("goods_promotion_url_generate_response", {})
        url_list = resp.get("goods_promotion_url_list", [])
        
        for item in url_list:
            gs = item.get("goods_sign", "")
            short_url = item.get("short_url", "")
            if gs and short_url:
                result_map[gs] = short_url
        
        logger.info("Generated %d/%d promotion URLs", len(result_map), len(goods_signs))
    except Exception as e:
        logger.error("Promotion URL generation failed: %s", str(e))
    
    return result_map


# ============ 全量拉取 ============

def _fetch_all_items():
    """全量拉取百亿补贴商品"""
    all_items = []
    for page in range(1, MAX_FETCH_PAGES + 1):
        offset = (page - 1) * 50
        result = _call_pdd("pdd.ddk.goods.recommend.get", {
            "channel_type": str(CHANNEL_TYPE),
            "activity_tags": ACTIVITY_TAGS,
            "limit": "50",
            "offset": str(offset),
            "pid": PID,
        })

        resp = result.get("goods_basic_detail_response")
        if not resp:
            err = result.get("error_response", {})
            err_msg = err.get("sub_msg") or err.get("error_msg", "未知错误")
            logger.error("Page %d error: %s", page, err_msg)
            if "限制使用" in err_msg:
                logger.warning("PDD risk control triggered at page %d, returning %d items", page, len(all_items))
                break
            break

        goods = resp.get("list", [])
        if not goods:
            logger.info("Page %d: empty, done.", page)
            break

        all_items.extend(goods)
        logger.info("Page %d: +%d items, total=%d", page, len(goods), len(all_items))

        if len(goods) < 50:
            break

        # 间隔延迟，避免PDD风控
        if page < MAX_FETCH_PAGES:
            time.sleep(FETCH_DELAY)

    return all_items


# ============ 数据提取 ============

def _parse_sales_tip(sales_tip):
    """解析销量文案: '36万+' → 360000, '1.1万+' → 11000, '5195' → 5195"""
    if not sales_tip:
        return 0
    s = str(sales_tip).strip()
    if "万" in s:
        try:
            num = float(s.replace("万+", "").replace("万", ""))
            return int(num * 10000)
        except ValueError:
            return 0
    try:
        return int(s.replace("+", "").replace(",", ""))
    except ValueError:
        return 0


def _extract_merchant_label(merchant_type):
    """商家类型转中文"""
    mapping = {"1": "个人店", "2": "企业店", "3": "普通店", "4": "旗舰店", "5": "专营店", "6": "专卖店"}
    return mapping.get(str(merchant_type), "普通店")


def _extract_ranking(unified_tags):
    """从unified_tags提取排行榜信息"""
    for tag in unified_tags or []:
        if tag and ("榜" in tag):
            return tag
    return ""


def _extract_quality_tags(unified_tags):
    """从unified_tags提取品质标签（排除排行榜和None）"""
    quality_keywords = {"正品险", "退货包运费", "七天退换", "顺丰包邮", "24小时内发货", "48小时内发货",
                        "正品发票", "假一赔十", "正品保障", "极速退款", "坏果包赔", "假一赔四"}
    tags = []
    for tag in unified_tags or []:
        if tag and tag in quality_keywords:
            tags.append(tag)
    return tags


def _simplify_item(g):
    """精简商品数据，标准化字段"""
    min_group_price = g.get("min_group_price", 0) or 0
    min_normal_price = g.get("min_normal_price", 0) or 0
    coupon_discount = g.get("coupon_discount", 0) or 0

    # 价格转元
    group_price = round(min_group_price / 100, 2)
    normal_price = round(min_normal_price / 100, 2)
    coupon_price = round(coupon_discount / 100, 2)
    final_price = round((min_group_price - coupon_discount) / 100, 2)

    # 折扣率
    discount_rate = 0
    if normal_price > 0:
        discount_rate = round((1 - group_price / normal_price) * 100, 1)

    # 券占比
    coupon_ratio = 0
    if group_price > 0:
        coupon_ratio = round(coupon_price / group_price * 100, 1)

    # 销量数值
    sales_tip = g.get("sales_tip", "")
    sales_num = _parse_sales_tip(sales_tip)

    merchant_type = str(g.get("merchant_type", "3"))
    merchant_label = _extract_merchant_label(merchant_type)

    unified_tags = g.get("unified_tags", [])
    quality_tags = _extract_quality_tags(unified_tags)
    ranking = _extract_ranking(unified_tags)

    # 三项评分
    desc_txt = g.get("desc_txt", "")
    serv_txt = g.get("serv_txt", "")
    lgst_txt = g.get("lgst_txt", "")

    return {
        "goods_name": g.get("goods_name", ""),
        "goods_sign": g.get("goods_sign", ""),
        "group_price": group_price,
        "normal_price": normal_price,
        "coupon_price": coupon_price,
        "final_price": final_price,
        "discount_rate": discount_rate,
        "coupon_ratio": coupon_ratio,
        "sales_tip": sales_tip,
        "sales_num": sales_num,
        "brand_name": g.get("brand_name", ""),
        "category_name": g.get("category_name", ""),
        "opt_name": g.get("opt_name", ""),
        "merchant_type": merchant_type,
        "merchant_label": merchant_label,
        "desc_txt": desc_txt,
        "serv_txt": serv_txt,
        "lgst_txt": lgst_txt,
        "quality_tags": quality_tags,
        "ranking": ranking,
        "goods_image": g.get("goods_image_url", "") or g.get("goods_thumbnail_url", ""),
    }


# ============ 好货评分 ============

def _calc_deal_score(item):
    """
    好货评分（满分100）
    - 折扣力度 30%：折扣率越高越好
    - 券后性价比 25%：券占价比越高越好
    - 销量热度 25%：销量越高越好
    - 品质保障 20%：旗舰店+评分+排行榜+标签
    """
    # 1. 折扣力度（满分30）
    discount_rate = item["discount_rate"]
    if discount_rate >= 50:
        discount_score = 30
    elif discount_rate >= 30:
        discount_score = 20 + (discount_rate - 30) * 0.5  # 20~30
    elif discount_rate >= 10:
        discount_score = 10 + (discount_rate - 10) * 0.5  # 10~20
    else:
        discount_score = discount_rate * 1.0  # 0~10

    # 2. 券后性价比（满分25）
    coupon_ratio = item["coupon_ratio"]
    if coupon_ratio >= 30:
        coupon_score = 25
    elif coupon_ratio >= 10:
        coupon_score = 15 + (coupon_ratio - 10) * 0.5  # 15~25
    elif coupon_ratio > 0:
        coupon_score = coupon_ratio * 1.5  # 0~15
    else:
        coupon_score = 0

    # 3. 销量热度（满分25）
    sales_num = item["sales_num"]
    if sales_num >= 100000:
        sales_score = 25
    elif sales_num >= 10000:
        sales_score = 15 + (sales_num - 10000) / 90000 * 10  # 15~25
    elif sales_num >= 1000:
        sales_score = 8 + (sales_num - 1000) / 9000 * 7  # 8~15
    elif sales_num >= 100:
        sales_score = 3 + (sales_num - 100) / 900 * 5  # 3~8
    else:
        sales_score = min(sales_num / 100 * 3, 3)  # 0~3

    # 4. 品质保障（满分20）
    quality_score = 0
    # 旗舰店+10，专营店+6，普通店+2
    mt = item["merchant_type"]
    if mt == "4":
        quality_score += 10
    elif mt == "5":
        quality_score += 6
    elif mt == "6":
        quality_score += 6
    else:
        quality_score += 2

    # 三项评分全"高"+4
    high_count = sum(1 for t in [item["desc_txt"], item["serv_txt"], item["lgst_txt"]] if t == "高")
    quality_score += high_count * 1.5  # 最多+4.5

    # 有排行榜名次+3
    if item["ranking"]:
        quality_score += 3

    # 品质标签每个+0.5，最多+2.5
    quality_score += min(len(item["quality_tags"]) * 0.5, 2.5)

    quality_score = min(quality_score, 20)

    total = round(discount_score + coupon_score + sales_score + quality_score, 1)
    return min(total, 100)


# ============ 关键词匹配 ============

def _is_subsequence(kw, text):
    """子序列匹配：kw的字符按顺序出现在text中，但不要求连续"""
    it = iter(text)
    return all(c in it for c in kw)


def _match_keyword(item, keyword):
    """关键词匹配：类目 > 细分类目 > 品牌 > 商品名"""
    kw = keyword.lower()
    if kw in item["category_name"].lower() or _is_subsequence(kw, item["category_name"].lower()):
        return True
    if kw in item["opt_name"].lower() or _is_subsequence(kw, item["opt_name"].lower()):
        return True
    if kw in item["brand_name"].lower() or _is_subsequence(kw, item["brand_name"].lower()):
        return True
    if kw in item["goods_name"].lower() or _is_subsequence(kw, item["goods_name"].lower()):
        return True
    return False


# ============ 排序 ============

def _sort_items(items, sort_by="deal_score"):
    """排序：deal_score(默认)/price_asc/price_desc/sales"""
    if sort_by == "price_asc":
        return sorted(items, key=lambda x: x["final_price"])
    elif sort_by == "price_desc":
        return sorted(items, key=lambda x: x["final_price"], reverse=True)
    elif sort_by == "sales":
        return sorted(items, key=lambda x: x["sales_num"], reverse=True)
    else:  # deal_score
        return sorted(items, key=lambda x: x["deal_score"], reverse=True)


# ============ 类目概览 ============

def _build_category_overview(items):
    """构建类目分布概览"""
    cat_counter = Counter(item["category_name"] for item in items if item["category_name"])
    return [{"category": cat, "count": cnt} for cat, cnt in cat_counter.most_common()]


# ============ 缓存管理 ============

def _get_cached_items():
    """获取缓存的商品列表，过期则重新拉取"""
    now = time.time()
    cached = _cache.get("items")

    if cached and (now - cached["ts"]) < CACHE_TTL:
        logger.info("Cache hit, age=%.0fs, items=%d", now - cached["ts"], len(cached["data"]))
        return cached["data"], True

    # 检查是否正在拉取（避免并发重复拉取）
    if cached and cached.get("fetching"):
        logger.info("Cache warming, returning stale data")
        return cached.get("data", []), True

    # 标记正在拉取
    if cached:
        cached["fetching"] = True
    else:
        _cache["items"] = {"data": [], "ts": 0, "fetching": True}

    # 全量拉取
    logger.info("Cache miss, fetching from PDD API...")
    raw_items = _fetch_all_items()
    logger.info("Fetched %d raw items from PDD", len(raw_items))

    # 精简+评分
    simplified = []
    for raw in raw_items:
        item = _simplify_item(raw)
        item["deal_score"] = _calc_deal_score(item)
        simplified.append(item)

    logger.info("Simplified %d items with deal_score", len(simplified))

    # 更新缓存
    _cache["items"] = {"data": simplified, "ts": time.time(), "fetching": False}

    return simplified, False


# ============ 业务处理 ============

def handle_list(params):
    """
    百亿补贴好货推荐
    参数：keyword/category/max_price/min_price/brand_only/sort/page
    """
    keyword = str(params.get("keyword", "")).strip()
    category = str(params.get("category", "")).strip()
    # keyword和category合并处理（用户可能用任一方式）
    search_kw = keyword or category

    max_price = params.get("max_price")
    min_price = params.get("min_price")
    brand_only = params.get("brand_only", False)
    sort_by = params.get("sort", "deal_score")
    page = int(params.get("page", 1) or 1)

    # 获取缓存数据
    all_items, from_cache = _get_cached_items()

    if not all_items:
        return {
            "error": "暂无商品数据，PDD接口可能被限流，请稍后重试",
            "total": 0,
            "page": page,
            "page_size": PAGE_SIZE,
            "has_more": False,
        }

    # 1. 关键词过滤
    if search_kw:
        filtered = [item for item in all_items if _match_keyword(item, search_kw)]
    else:
        filtered = list(all_items)

    # 2. 价格过滤
    if max_price:
        try:
            max_price = float(max_price)
            filtered = [item for item in filtered if item["final_price"] <= max_price]
        except (ValueError, TypeError):
            pass

    if min_price:
        try:
            min_price = float(min_price)
            filtered = [item for item in filtered if item["final_price"] >= min_price]
        except (ValueError, TypeError):
            pass

    # 3. 仅品牌店
    if brand_only:
        filtered = [item for item in filtered if item["merchant_type"] in ("4", "5", "6")]

    # 4. 排序
    sorted_items = _sort_items(filtered, sort_by)

    # 5. 分页
    total = len(sorted_items)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = sorted_items[start:end]
    has_more = end < total

    # 6. 类目概览（全量数据，不受keyword过滤影响——用于引导用户逛其他品类）
    category_overview = _build_category_overview(all_items)

    # 7. 构建输出（精简字段：只保留用户需要的7个字段，含推广短链接）
    goods_signs = [item["goods_sign"] for item in page_items]
    promo_urls = _gen_promotion_urls(goods_signs)

    results = []
    for item in page_items:
        # 品质汇总拼接
        quality_parts = []
        if item.get("merchant_label") and item["merchant_label"] != "普通店":
            quality_parts.append(item["merchant_label"])
        if item.get("quality_tags"):
            quality_parts.extend(item["quality_tags"])
        if item.get("ranking"):
            quality_parts.append(item["ranking"])
        quality_desc = " | ".join(quality_parts) if quality_parts else ""

        # 推广短链接优先，无则降级为普通商品页
        product_url = promo_urls.get(item["goods_sign"]) or \
            f"https://mobile.yangkeduo.com/goods.html?goods_sign={item['goods_sign']}"

        results.append({
            "goods_name": item["goods_name"],
            "product_url": product_url,
            "normal_price": item["normal_price"],
            "final_price": item["final_price"],
            "sales_tip": item["sales_tip"],
            "quality_desc": quality_desc,
            "goods_image": item["goods_image"],
        })

    return {
        "results": results,
        "total": total,
        "page": page,
        "page_size": PAGE_SIZE,
        "has_more": has_more,
        "category_overview": category_overview,
        "from_cache": from_cache,
        "filter_applied": {
            "keyword": search_kw or None,
            "max_price": max_price if isinstance(max_price, (int, float)) else None,
            "min_price": min_price if isinstance(min_price, (int, float)) else None,
            "brand_only": brand_only if brand_only else None,
            "sort": sort_by,
        },
    }


def handle_stats(params):
    """返回缓存统计信息（调试用）"""
    all_items, from_cache = _get_cached_items()
    cached = _cache.get("items", {})

    cat_overview = _build_category_overview(all_items)

    # 评分分布
    score_ranges = {"90+": 0, "70-89": 0, "50-69": 0, "30-49": 0, "0-29": 0}
    for item in all_items:
        s = item.get("deal_score", 0)
        if s >= 90:
            score_ranges["90+"] += 1
        elif s >= 70:
            score_ranges["70-89"] += 1
        elif s >= 50:
            score_ranges["50-69"] += 1
        elif s >= 30:
            score_ranges["30-49"] += 1
        else:
            score_ranges["0-29"] += 1

    return {
        "total_items": len(all_items),
        "from_cache": from_cache,
        "cache_age": int(time.time() - cached.get("ts", 0)) if cached else None,
        "cache_ttl": CACHE_TTL,
        "channel": "百亿补贴",
        "channel_type": CHANNEL_TYPE,
        "activity_tags": ACTIVITY_TAGS,
        "category_overview": cat_overview,
        "score_distribution": score_ranges,
    }


# ============ HTTP服务 ============

class Handler(BaseHTTPRequestHandler):
    def _check_token(self):
        token = self.headers.get("X-Proxy-Token", "")
        if PROXY_TOKEN and token != PROXY_TOKEN:
            self.send_json({"error": "鉴权失败"}, 403)
            return False
        return True

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Proxy-Token")
        self.end_headers()

    def do_POST(self):
        if not self._check_token():
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        tool = data.get("tool", "")
        arguments = data.get("params", data.get("arguments", {}))

        try:
            if tool == "list":
                result = handle_list(arguments)
            elif tool == "stats":
                result = handle_stats(arguments)
            else:
                result = {"error": "Unknown tool: " + tool + ". Available: list, stats"}
                self.send_json(result, 400)
                return
        except Exception as e:
            import traceback
            logger.error("Handler error: %s\n%s", e, traceback.format_exc())
            result = {"error": "Internal error: " + str(e)}
            self.send_json(result, 500)
            return

        self.send_json(result, 200)

    def do_GET(self):
        self.send_json({
            "service": "pdd-baiyi-proxy",
            "channel": "百亿补贴",
            "channel_type": CHANNEL_TYPE,
            "activity_tags": ACTIVITY_TAGS,
            "tools": ["list", "stats"],
            "page_size": PAGE_SIZE,
            "cache_ttl": CACHE_TTL,
            "status": "running",
        })

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        logger.info("%s - %s", self.client_address[0], format % args)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    logger.info("PDD Baiyi Proxy v1.0 running on port %d (channel_type=%d, activity_tags=%s)",
                port, CHANNEL_TYPE, ACTIVITY_TAGS)
    server.serve_forever()
