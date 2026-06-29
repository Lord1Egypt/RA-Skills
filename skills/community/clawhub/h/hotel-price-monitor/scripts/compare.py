#!/usr/bin/env python3
"""
hotel-price-monitor: 多平台酒店比价 + 降价监控
通过SCF代理查询飞猪/RG/途牛/同程4个平台实时价格

用法:
  python3 compare.py search --city "上海" --check-in 2026-07-01 --check-out 2026-07-03 [--keyword "外滩"] [--adults 2] [--rooms 1] [--price-max 800] [--star-ratings "4,5"]
  python3 compare.py compare --hotel "上海外滩华尔道夫" --city "上海" --check-in 2026-07-01 --check-out 2026-07-03 [--adults 2] [--rooms 1]
"""

import argparse
import json
import os
import re
import sys
import time

# HTTP请求（使用标准urllib，TLS证书验证默认开启）

# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# 代理地址
SCF_HOTEL_URL = "https://1439498936-4wdncmn2oj.ap-guangzhou.tencentscf.com"
SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# 酒店品牌词表（用于跨平台匹配）
HOTEL_BRANDS = [
    # 超豪华
    "华尔道夫", "半岛", "瑞吉", "宝格丽", "安缦", "文华东方", "四季", "丽思卡尔顿",
    "柏悦", "艾美", "康莱德", "费尔蒙", "悦榕庄", "六善", "阿丽拉",
    # 高端
    "万豪", "喜来登", "威斯汀", "JW万豪", "万丽", "凯悦", "君悦",
    "洲际", "皇冠假日", "英迪格", "希尔顿", "逸林", "嘉悦里",
    "香格里拉", "凯宾斯基", "索菲特", "丽笙", "朗廷",
    # 中高端
    "诺富特", "美爵", "假日", "万怡", "福朋", "源宿",
    "全季", "亚朵", "亚·朵", "喆·啡", "喆啡", "希岸", "欢朋",
    "丽枫", "桔子", "水晶", "漫心", "花间堂", "开元",
    # 中端连锁
    "如家", "汉庭", "锦江", "7天", "速8", "格林豪泰", "布丁",
    "尚客优", "城市便捷", "维也纳", "维也纳国际", "维也纳好眠",
    "怡莱", "海友", "宜必思",
    # 公寓/民宿
    "途家", "斯维登", "城家", "雅诗阁", "盛捷", "馨乐庭",
]

# 品牌中间点映射
BRAND_DOT_MAP = {
    "喆·啡": "喆啡",
    "亚·朵": "亚朵",
}


def normalize_brand(name):
    for dot_brand, no_dot in BRAND_DOT_MAP.items():
        name = name.replace(dot_brand, no_dot)
    return name


def extract_brand(name):
    name = normalize_brand(name)
    sorted_brands = sorted(HOTEL_BRANDS, key=len, reverse=True)
    for brand in sorted_brands:
        brand_normalized = normalize_brand(brand)
        if brand_normalized in name:
            return brand_normalized
    return ""


def hotel_name_similarity(name1, name2):
    """酒店名跨平台匹配：品牌+位置双维度阈值0.35"""
    name1 = normalize_brand(name1.strip())
    name2 = normalize_brand(name2.strip())

    if name1 == name2:
        return 1.0

    brand1 = extract_brand(name1)
    brand2 = extract_brand(name2)

    brand_match = 0.0
    if brand1 and brand2:
        if brand1 == brand2:
            brand_match = 1.0
        elif brand1 in brand2 or brand2 in brand1:
            brand_match = 0.8
    elif not brand1 and not brand2:
        brand_match = 0.5
    else:
        brand_match = 0.0

    rest1 = name1.replace(brand1, "").strip() if brand1 else name1
    rest2 = name2.replace(brand2, "").strip() if brand2 else name2

    if rest1 and rest2:
        set1 = set(rest1)
        set2 = set(rest2)
        intersection = set1 & set2
        union = set1 | set2
        char_sim = len(intersection) / len(union) if union else 0
    else:
        char_sim = 0.0

    score = brand_match * 0.6 + char_sim * 0.4
    return score


def match_hotel_cross_platform(target_name, candidates, threshold=0.35):
    """在候选列表中匹配目标酒店，返回按相似度降序的匹配列表"""
    matched = []
    for cand in candidates:
        cand_name = cand.get("name") or cand.get("hotelName") or cand.get("hotel_name") or ""
        score = hotel_name_similarity(target_name, cand_name)
        if score >= threshold:
            matched.append((score, cand))
    matched.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matched]


# ============================================================
# HTTP请求
# ============================================================

def http_post(url, body, timeout=20):
    """发送POST请求到代理服务，返回JSON结果。数据流向：用户查询参数 → 代理服务 → 旅游平台 → 结果返回。"""
    import urllib.request
    import urllib.error
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "detail": e.read().decode("utf-8", errors="replace")}


# ============================================================
# 数据源查询
# ============================================================

def search_fliggy(city, check_in, check_out, keyword=None, adults=2):
    """飞猪酒店搜索 - 浏览列表（有价格+链接）"""
    try:
        params = {
            "destName": city,
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adultCount": adults,
        }
        if keyword:
            params["keyWords"] = keyword

        resp = http_post(SCF_FLIGGY_URL, {
            "type": "search_hotels",
            "params": params,
        })
        data = resp.get("data", {})
        hotels = data.get("itemList", []) or data.get("hotelList", [])

        results = []
        for h in hotels:
            price = h.get("price", 0)
            if isinstance(price, str):
                price = re.sub(r'[¥￥,\s]', '', price)
                try:
                    price = float(price)
                except (ValueError, TypeError):
                    price = 0

            results.append({
                "source": "飞猪",
                "name": h.get("name", ""),
                "star": h.get("star", ""),
                "brand": h.get("brandName", ""),
                "price": price,
                "address": h.get("address", ""),
                "poi": h.get("interestsPoi", ""),
                "url": h.get("detailUrl", ""),
                "image": h.get("mainPic", ""),
            })
        return {"source": "飞猪", "results": results, "error": None}
    except Exception as e:
        return {"source": "飞猪", "results": [], "error": str(e)}


def search_tuniu(city, check_in, check_out, keyword=None, adults=2, rooms=1, price_max=None, star_ratings=None, page_num=1):
    """途牛酒店搜索 - 浏览列表（信息最全：评分、距离、早餐、取消政策）"""
    try:
        params = {
            "cityName": city,
            "checkIn": check_in,
            "checkOut": check_out,
            "adultNum": adults,
            "roomNum": rooms,
        }
        if keyword:
            params["keyword"] = keyword
        if price_max:
            params["prices"] = f"0-{price_max}"
        if star_ratings:
            params["starRatings"] = star_ratings

        resp = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_hotel_search",
            "params": params,
        })
        data = resp.get("data", {})

        # 检查错误
        if isinstance(data, dict) and data.get("error"):
            return {"source": "途牛", "results": [], "error": data["error"]}

        hotels = data.get("hotelList", []) or data.get("hotels", [])

        results = []
        for h in hotels:
            results.append({
                "source": "途牛",
                "name": h.get("hotelName", h.get("name", "")),
                "star": h.get("star", h.get("starRating", "")),
                "score": h.get("commentScore", h.get("score", "")),
                "price": h.get("lowestPrice", h.get("price", 0)),
                "address": h.get("address", ""),
                "distance": h.get("distance", ""),
                "brand": h.get("brandName", ""),
                "cancel_policy": h.get("refund", ""),
                "meal": h.get("meal", ""),
                "url": h.get("url", h.get("jumpUrl", "")),
            })
        return {"source": "途牛", "results": results, "error": None}
    except Exception as e:
        return {"source": "途牛", "results": [], "error": str(e)}


def compare_fliggy(hotel_name, city, check_in, check_out, adults=2):
    """飞猪精确比价"""
    try:
        resp = http_post(SCF_FLIGGY_URL, {
            "type": "search_hotels",
            "params": {
                "destName": city,
                "checkInDate": check_in,
                "checkOutDate": check_out,
                "keyWords": hotel_name,
                "adultCount": adults,
            },
        })

        data = resp.get("data", {})
        hotels = data.get("itemList", []) or data.get("hotelList", [])

        results = []
        for h in hotels:
            h_name = h.get("name", "")
            sim = hotel_name_similarity(hotel_name, h_name)
            if sim < 0.3:
                continue

            price = h.get("price", 0)
            if isinstance(price, str):
                price = re.sub(r'[¥￥,\s]', '', price)
                try:
                    price = float(price)
                except (ValueError, TypeError):
                    price = 0

            results.append({
                "name": h_name,
                "price": price,
                "star": h.get("star", ""),
                "url": h.get("detailUrl", ""),
                "similarity": round(sim, 2),
            })

        results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        if results:
            best = results[0]
            return {
                "source": "飞猪",
                "matched": True,
                "name": best["name"],
                "price": best["price"],
                "star": best["star"],
                "url": best["url"],
                "similarity": best["similarity"],
                "error": None,
            }
        return {"source": "飞猪", "matched": False, "price": None, "url": None, "error": "未找到匹配酒店"}
    except Exception as e:
        return {"source": "飞猪", "matched": False, "price": None, "url": None, "error": str(e)}


def compare_rg(hotel_name, city, check_in, check_out, adults=2, rooms=1):
    """RG精确比价 + 佣金链接（用hotel_detail按名称精确查询）"""
    try:
        # 直接用hotel_detail按酒店名查询
        resp = http_post(SCF_HOTEL_URL, {
            "type": "hotel_detail",
            "source": "rg_detail",
            "params": {
                "name": hotel_name,
                "city": city,
                "check_in": check_in,
                "check_out": check_out,
                "adults": adults,
                "rooms": rooms,
            },
        })

        data = resp.get("data", {})

        if data and data.get("success") is not False:
            # 从房型列表中取最低价
            room_plans = data.get("roomRatePlans", [])
            lowest_price = 0
            cancel_policy = ""
            if room_plans:
                priced_plans = [p for p in room_plans if p.get("totalPrice") and isinstance(p["totalPrice"], (int, float)) and p["totalPrice"] > 0]
                if priced_plans:
                    best_plan = min(priced_plans, key=lambda p: p["totalPrice"])
                    lowest_price = best_plan["totalPrice"]
                    # 取消政策
                    cancel_policies = best_plan.get("cancellationPolicies", [])
                    if cancel_policies:
                        parts_list = []
                        for c in cancel_policies:
                            desc = c.get("description", "")
                            if not desc:
                                from_date = c.get("fromDate", "")
                                amount = c.get("amount", "")
                                desc = f"从{from_date}取消扣款{amount}元"
                            parts_list.append(desc)
                        cancel_policy = "; ".join(parts_list)
            elif data.get("totalPrice"):
                lowest_price = data["totalPrice"]

            return {
                "source": "RG",
                "matched": True,
                "name": data.get("name", hotel_name),
                "price": lowest_price,
                "star": data.get("starRating", ""),
                "url": data.get("bookingUrl", ""),
                "hotel_id": data.get("hotelId", ""),
                "cancel_policy": cancel_policy,
                "room_plans_count": len(room_plans),
                "error": None,
            }

        return {"source": "RG", "matched": False, "price": None, "url": None, "error": data.get("errorMessage", "查询失败") if data else "无返回数据"}
    except Exception as e:
        return {"source": "RG", "matched": False, "price": None, "url": None, "error": str(e)}


def compare_tuniu(hotel_name, city, check_in, check_out, adults=2, rooms=1):
    """途牛多策略匹配比价（hotel_detail精确查 + hotel_search补充）"""
    try:
        # 策略1：直接用hotel_detail按酒店名查
        resp = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_hotel_detail",
            "params": {
                "hotelName": hotel_name,
                "cityName": city,
                "checkIn": check_in,
                "checkOut": check_out,
            },
        })
        data = resp.get("data", {})
        if data and data.get("hotelName"):
            # 从房型中取最低价
            room_types = data.get("roomTypes", [])
            lowest_price = 0
            cancel_policy = ""
            for rt in room_types:
                rate_plans = rt.get("ratePlans", [])
                for rp in rate_plans:
                    # 途牛价格字段是rmbPrices
                    p = rp.get("rmbPrices") or rp.get("price", 0)
                    if isinstance(p, str):
                        p = re.sub(r'[¥￥,\s]', '', p)
                        try:
                            p = float(p)
                        except (ValueError, TypeError):
                            p = 0
                    if p > 0 and (lowest_price == 0 or p < lowest_price):
                        lowest_price = p
                        cancel_policy = rp.get("cancelText", "") or rp.get("cancelDesc", "")

            policies = data.get("policies", {})
            if not cancel_policy and policies:
                cancel_policy = policies.get("cancelPolicy", "")

            score = data.get("commentScore", "")
            return {
                "source": "途牛",
                "matched": True,
                "name": data.get("hotelName", hotel_name),
                "price": lowest_price,
                "star": data.get("starName", ""),
                "score": score,
                "cancel_policy": cancel_policy,
                "hotel_id": data.get("hotelId", ""),
                "search_strategy": "hotel_detail",
                "error": None,
            }

        # 策略2：hotel_search按品牌名搜索
        brand = extract_brand(hotel_name)
        search_keywords = []
        if brand and brand != hotel_name:
            search_keywords.append(brand)

        parts = hotel_name.replace(brand, "").strip() if brand else ""
        if parts and len(parts) >= 2 and parts != hotel_name:
            search_keywords.append(parts[-4:] if len(parts) > 4 else parts)

        for keyword in search_keywords:
            resp = http_post(SCF_TUNIU_URL, {
                "type": "tuniu_hotel_search",
                "params": {
                    "cityName": city,
                    "checkIn": check_in,
                    "checkOut": check_out,
                    "keyword": keyword,
                    "adultNum": adults,
                    "roomNum": rooms,
                },
            })
            data = resp.get("data", {})
            if isinstance(data, dict) and data.get("error"):
                continue

            hotels = data.get("hotels", []) or data.get("hotelList", [])
            matched = match_hotel_cross_platform(hotel_name, hotels)
            if matched:
                best = matched[0]
                price = best.get("lowestPrice", best.get("price", 0))
                if isinstance(price, str):
                    try:
                        price = float(price)
                    except (ValueError, TypeError):
                        price = 0

                return {
                    "source": "途牛",
                    "matched": True,
                    "name": best.get("hotelName", best.get("name", "")),
                    "price": price,
                    "star": best.get("starName", best.get("star", "")),
                    "score": best.get("commentScore", ""),
                    "search_strategy": f"hotel_search({keyword})",
                    "error": None,
                }

        return {"source": "途牛", "matched": False, "price": None, "url": None, "error": "未找到匹配酒店"}
    except Exception as e:
        return {"source": "途牛", "matched": False, "price": None, "url": None, "error": str(e)}


def compare_tc(hotel_name, city, check_in, check_out, adults=2):
    """同程DeepTrip AI搜索比价"""
    try:
        query = f"{city}{hotel_name}酒店{check_in}至{check_out}入住价格"
        resp = http_post(SCF_HOTEL_URL, {
            "type": "deeptrip_search",
            "source": "tongcheng",
            "params": {
                "q": query,
            },
        })
        data = resp.get("data", {})
        text = data.get("text", "")

        prices = re.findall(r'[¥￥](\d+(?:[,.]\d+)?)', text)
        price = 0
        if prices:
            try:
                price = float(prices[0].replace(",", ""))
            except (ValueError, TypeError):
                price = 0

        links = data.get("产品跳转链接", {})
        url = ""
        brand = extract_brand(hotel_name)
        for name, link_obj in links.items():
            if hotel_name[:4] in name or (brand and brand in name):
                url = link_obj.get("手机链接", link_obj.get("PC链接", "")) if isinstance(link_obj, dict) else str(link_obj)
                break
        if not url and links:
            first_key = list(links.keys())[0]
            link_obj = links[first_key]
            url = link_obj.get("手机链接", link_obj.get("PC链接", "")) if isinstance(link_obj, dict) else str(link_obj)

        if price > 0:
            return {
                "source": "同程",
                "matched": True,
                "name": hotel_name,
                "price": price,
                "url": url,
                "error": None,
            }
        return {"source": "同程", "matched": False, "price": None, "url": url, "error": "未提取到价格"}
    except Exception as e:
        return {"source": "同程", "matched": False, "price": None, "url": None, "error": str(e)}


# ============================================================
# 主命令
# ============================================================

def cmd_search(args):
    """搜索酒店列表"""
    # 飞猪有价格和链接，途牛信息最全——两个都搜，合并去重
    fliggy_result = search_fliggy(
        city=args.city,
        check_in=args.check_in,
        check_out=args.check_out,
        keyword=args.keyword,
        adults=args.adults,
    )
    tuniu_result = search_tuniu(
        city=args.city,
        check_in=args.check_in,
        check_out=args.check_out,
        keyword=args.keyword,
        adults=args.adults,
        rooms=args.rooms,
        price_max=args.price_max,
        star_ratings=args.star_ratings,
    )

    hotels = []
    # 途牛信息更全（评分、距离、取消政策），先放途牛
    if tuniu_result.get("results"):
        hotels.extend(tuniu_result["results"])
    # 飞猪补充（有预订链接和价格）
    if fliggy_result.get("results"):
        hotels.extend(fliggy_result["results"])

    # 去重（按酒店名相似度）
    seen = []
    unique = []
    for h in hotels:
        h_name = h.get("name", "")
        is_dup = False
        for s in seen:
            if hotel_name_similarity(h_name, s) > 0.7:
                is_dup = True
                break
        if not is_dup:
            unique.append(h)
            seen.append(h_name)

    # 按价格排序（有价格的排前面）
    unique.sort(key=lambda x: x.get("price", 999999) if isinstance(x.get("price"), (int, float)) and x.get("price", 0) > 0 else 999999)

    output = {
        "success": True,
        "action": "search",
        "city": args.city,
        "check_in": args.check_in,
        "check_out": args.check_out,
        "count": len(unique),
        "hotels": unique,
        "tip": "以上为浏览价格，选定酒店后告诉我酒店名，立刻启动多旅游平台比价！",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_compare(args):
    """多平台精确比价"""
    hotel_name = args.hotel
    city = args.city
    check_in = args.check_in
    check_out = args.check_out
    adults = args.adults or 2
    rooms = args.rooms or 1

    results = []

    # 飞猪（精确keyword搜索 + 预订链接）
    results.append(compare_fliggy(hotel_name, city, check_in, check_out, adults))

    # RG（佣金5% + booking链接）
    results.append(compare_rg(hotel_name, city, check_in, check_out, adults, rooms))

    # 途牛（多策略搜索）
    results.append(compare_tuniu(hotel_name, city, check_in, check_out, adults, rooms))

    # 同程（AI搜索）
    results.append(compare_tc(hotel_name, city, check_in, check_out, adults))

    # 按价格排序
    priced = [r for r in results if r.get("matched") and r.get("price") and isinstance(r["price"], (int, float)) and r["price"] > 0]
    unpriced = [r for r in results if r not in priced]

    # 佣金优先级：RG(5%) > 飞猪(分佣) > 途牛 > 同程
    commission_order = {"RG": 0, "飞猪": 1, "途牛": 2, "同程": 3}
    priced.sort(key=lambda x: (x["price"], commission_order.get(x.get("source", ""), 9)))

    all_sorted = priced + unpriced

    output = {
        "success": True,
        "action": "compare",
        "hotel_name": hotel_name,
        "city": city,
        "check_in": check_in,
        "check_out": check_out,
        "platforms": all_sorted,
        "lowest_price": priced[0]["price"] if priced else None,
        "lowest_platform": priced[0]["source"] if priced else None,
        "lowest_url": priced[0].get("url") if priced else None,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="酒店降价监控比价")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    search_parser = subparsers.add_parser("search", help="搜索酒店列表")
    search_parser.add_argument("--city", required=True, help="城市名")
    search_parser.add_argument("--check-in", required=True, help="入住日期 YYYY-MM-DD")
    search_parser.add_argument("--check-out", required=True, help="离店日期 YYYY-MM-DD")
    search_parser.add_argument("--keyword", default=None, help="关键词/地标")
    search_parser.add_argument("--adults", type=int, default=2, help="入住人数")
    search_parser.add_argument("--rooms", type=int, default=1, help="房间数")
    search_parser.add_argument("--price-max", type=int, default=None, help="最高价格")
    search_parser.add_argument("--star-ratings", default=None, help="星级筛选，如 '4,5'")

    compare_parser = subparsers.add_parser("compare", help="多平台精确比价")
    compare_parser.add_argument("--hotel", required=True, help="酒店名称")
    compare_parser.add_argument("--city", required=True, help="城市名")
    compare_parser.add_argument("--check-in", required=True, help="入住日期 YYYY-MM-DD")
    compare_parser.add_argument("--check-out", required=True, help="离店日期 YYYY-MM-DD")
    compare_parser.add_argument("--adults", type=int, default=2, help="入住人数")
    compare_parser.add_argument("--rooms", type=int, default=1, help="房间数")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "compare":
        cmd_compare(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
