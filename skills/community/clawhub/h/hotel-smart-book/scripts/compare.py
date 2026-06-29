#!/usr/bin/env python3
"""
酒店聪明订：多平台酒店比价 + 低价日历 + 订房决策建议
通过SCF代理查询飞猪/RG/途牛/同程4个平台实时价格

用法:
  python3 compare.py search --city "上海" --check-in 2026-07-01 --check-out 2026-07-03 [--keyword "外滩"] [--adults 2]
  python3 compare.py calendar --city "上海" --keyword "外滩" --start-date 2026-07-01 [--nights 2] [--days 14]
  python3 compare.py advisor --hotel "上海外滩华尔道夫" --city "上海" --check-in 2026-07-01 --check-out 2026-07-03
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta

# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = "tp_8k2mX9vQ4z"

SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
SCF_RG_URL = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"
SCF_HOTEL_URL = "https://1439498936-4wdncmn2oj.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# ============================================================
# 酒店品牌词表（跨平台匹配用）
# ============================================================

HOTEL_BRANDS = [
    "华尔道夫", "半岛", "瑞吉", "宝格丽", "安缦", "文华东方", "四季", "丽思卡尔顿",
    "柏悦", "艾美", "康莱德", "费尔蒙", "悦榕庄", "六善", "阿丽拉",
    "万豪", "喜来登", "威斯汀", "JW万豪", "万丽", "凯悦", "君悦",
    "洲际", "皇冠假日", "英迪格", "希尔顿", "逸林", "嘉悦里",
    "香格里拉", "凯宾斯基", "索菲特", "丽笙", "朗廷",
    "诺富特", "美爵", "假日", "万怡", "福朋", "源宿",
    "全季", "亚朵", "亚·朵", "喆·啡", "喆啡", "希岸", "欢朋",
    "丽枫", "桔子", "水晶", "漫心", "花间堂", "开元",
    "如家", "汉庭", "锦江", "7天", "速8", "格林豪泰", "布丁",
    "尚客优", "城市便捷", "维也纳", "维也纳国际", "维也纳好眠",
    "怡莱", "海友", "宜必思",
    "途家", "斯维登", "城家", "雅诗阁", "盛捷", "馨乐庭",
]

BRAND_DOT_MAP = {"喆·啡": "喆啡", "亚·朵": "亚朵"}


# ============================================================
# 节假日/旺季日期（2026年）
# ============================================================

PEAK_DATES = {
    "春运": ("2026-01-25", "2026-02-22"),
    "清明": ("2026-04-03", "2026-04-06"),
    "五一": ("2026-05-01", "2026-05-05"),
    "端午": ("2026-05-30", "2026-06-01"),
    "暑假": ("2026-07-01", "2026-08-31"),
    "中秋": ("2026-09-25", "2026-09-27"),
    "国庆": ("2026-10-01", "2026-10-07"),
    "寒假": ("2026-01-15", "2026-02-22"),
}

# 酒店品牌档次 → 价格分位基准偏移
BRAND_TIER = {
    # 超豪华：均价5x以上
    "华尔道夫": "ultra_luxury", "半岛": "ultra_luxury", "瑞吉": "ultra_luxury",
    "宝格丽": "ultra_luxury", "安缦": "ultra_luxury", "文华东方": "ultra_luxury",
    "四季": "ultra_luxury", "丽思卡尔顿": "ultra_luxury", "柏悦": "ultra_luxury",
    # 高端：均价2-4x
    "万豪": "luxury", "喜来登": "luxury", "威斯汀": "luxury", "JW万豪": "ultra_luxury",
    "万丽": "luxury", "凯悦": "luxury", "君悦": "ultra_luxury", "康莱德": "ultra_luxury",
    "洲际": "luxury", "皇冠假日": "upscale", "英迪格": "luxury",
    "希尔顿": "luxury", "逸林": "upscale", "香格里拉": "ultra_luxury",
    "索菲特": "luxury", "朗廷": "luxury",
    # 中高端
    "诺富特": "upscale", "假日": "upscale", "万怡": "upscale",
    "福朋": "upscale", "全季": "midscale", "亚朵": "midscale",
    "喆啡": "midscale", "希岸": "midscale", "欢朋": "midscale",
    "丽枫": "midscale", "桔子": "midscale",
    # 经济型
    "如家": "economy", "汉庭": "economy", "锦江": "economy",
    "7天": "economy", "速8": "economy", "海友": "economy",
}

# 档次对应的价格倍数（相对城市高档型均价）
TIER_MULTIPLIER = {
    "ultra_luxury": 3.0,
    "luxury": 2.0,
    "upscale": 1.2,
    "midscale": 0.7,
    "economy": 0.4,
}

# 城市酒店均价参考（经济型/舒适型/高档型，每晚元）
CITY_HOTEL_REF = {
    "上海": (250, 450, 900),
    "北京": (230, 420, 850),
    "广州": (200, 380, 700),
    "深圳": (220, 400, 750),
    "杭州": (200, 380, 750),
    "成都": (180, 330, 650),
    "重庆": (170, 300, 600),
    "南京": (190, 350, 680),
    "武汉": (170, 310, 600),
    "西安": (180, 330, 650),
    "长沙": (170, 300, 580),
    "厦门": (200, 380, 780),
    "三亚": (300, 550, 1200),
    "昆明": (180, 330, 650),
    "青岛": (190, 350, 700),
    "大连": (190, 350, 680),
    "苏州": (190, 350, 700),
    "天津": (180, 330, 630),
    "郑州": (160, 300, 580),
    "哈尔滨": (170, 310, 600),
    "福州": (180, 330, 630),
    "珠海": (200, 380, 750),
    "丽江": (220, 400, 800),
    "大理": (220, 400, 800),
}


# ============================================================
# 工具函数
# ============================================================

def normalize_brand(name):
    for dot_brand, no_dot in BRAND_DOT_MAP.items():
        name = name.replace(dot_brand, no_dot)
    return name


def extract_brand(name):
    name = normalize_brand(name.strip())
    sorted_brands = sorted(HOTEL_BRANDS, key=len, reverse=True)
    for brand in sorted_brands:
        brand_normalized = normalize_brand(brand)
        if brand_normalized in name:
            return brand_normalized
    return ""


def hotel_name_similarity(name1, name2):
    """酒店名跨平台匹配：品牌+位置双维度"""
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
        char_sim = len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0
    else:
        char_sim = 0.0

    return brand_match * 0.6 + char_sim * 0.4


def is_peak_season(date_str):
    """判断是否旺季"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        for name, (start, end) in PEAK_DATES.items():
            if datetime.strptime(start, "%Y-%m-%d") <= d <= datetime.strptime(end, "%Y-%m-%d"):
                return True, name
    except ValueError:
        pass
    return False, None


def is_weekend(date_str):
    """判断是否周末（周五/周六入住算周末）"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.weekday() in (4, 5)  # 周五、周六
    except ValueError:
        return False


def get_city_price_range(city):
    """获取城市酒店参考价格"""
    return CITY_HOTEL_REF.get(city, None)


# ============================================================
# 订房决策引擎
# ============================================================

def get_hotel_tier(hotel_name):
    """根据品牌判断酒店档次"""
    brand = extract_brand(hotel_name)
    if brand and brand in BRAND_TIER:
        return BRAND_TIER[brand], brand
    return None, brand


def book_or_wait(price, city, check_in, check_out, all_prices=None, cancel_policy="", hotel_name=""):
    """
    订房决策建议引擎
    返回: {signal, confidence, reasons[], tips, dimensions}
    signal: "book" / "wait" / "watch"
    """
    reasons = []
    signal_scores = []  # 正数=建议订，负数=建议等

    # 0. 品牌档次识别
    tier, brand = get_hotel_tier(hotel_name) if hotel_name else (None, "")

    # 1. 时机：距入住天数 + 旺季判断
    try:
        checkin_dt = datetime.strptime(check_in, "%Y-%m-%d")
        days_left = (checkin_dt - datetime.now()).days

        is_peak, peak_name = is_peak_season(check_in)
        weekend = is_weekend(check_in)

        if is_peak:
            reasons.append(f"入住日处于{peak_name}旺季，酒店越晚越贵，建议尽早预订")
            signal_scores.append(4)
        elif weekend:
            reasons.append(f"入住日是周末，商务酒店可能周五降价，但景区酒店周末更贵")
            signal_scores.append(1)

        if days_left < 1:
            reasons.append(f"今天入住！立刻预订，别再等了")
            signal_scores.append(5)
        elif days_left <= 3:
            reasons.append(f"距入住仅{days_left}天，酒店一般不会临期大降，建议尽快预订")
            signal_scores.append(3)
        elif days_left <= 7:
            reasons.append(f"距入住{days_left}天，淡季可再观望1-2天，旺季建议立即预订")
            signal_scores.append(1 if not is_peak else 3)
        elif days_left <= 14:
            reasons.append(f"距入住{days_left}天，有时间余量，可以对比几天")
            signal_scores.append(0)
        elif days_left <= 30:
            reasons.append(f"距入住{days_left}天，提前量充足，价格可能还有波动，可设提醒观望")
            signal_scores.append(-1)
        else:
            reasons.append(f"距入住{days_left}天，太早了，很多酒店还没放出优惠价，建议入住前2-3周再查")
            signal_scores.append(-2)
    except ValueError:
        pass

    # 2. 性价比：与同档次均价对比
    city_ref = get_city_price_range(city)
    percentile = None
    if city_ref:
        low, mid, high = city_ref
        # 根据品牌档次调整参考区间
        if tier and tier in TIER_MULTIPLIER:
            mult = TIER_MULTIPLIER[tier]
            tier_low = int(low * mult)
            tier_mid = int(mid * mult)
            tier_high = int(high * mult)
            tier_label = {"ultra_luxury": "超豪华", "luxury": "高端", "upscale": "中高端", "midscale": "中端", "economy": "经济型"}.get(tier, "")
        else:
            tier_low, tier_mid, tier_high = low, mid, high
            tier_label = ""

        if tier_high > tier_low:
            percentile = max(0, min(1, (price - tier_low) / (tier_high - tier_low)))
        else:
            percentile = 0.5

        ref_desc = f"{tier_label}档" if tier_label else city

        if percentile <= 0.25:
            reasons.append(f"当前价¥{price}处于{ref_desc}低价区间（约{int(percentile*100)}%分位），明显划算")
            signal_scores.append(3)
        elif percentile <= 0.5:
            reasons.append(f"当前价¥{price}低于{ref_desc}均价¥{tier_mid}（约{int(percentile*100)}%分位），价格合理")
            signal_scores.append(2)
        elif percentile <= 0.75:
            reasons.append(f"当前价¥{price}接近{ref_desc}均价¥{tier_mid}（约{int(percentile*100)}%分位），中等水平")
            signal_scores.append(0)
        else:
            reasons.append(f"当前价¥{price}高于{ref_desc}均价¥{tier_mid}（约{int(percentile*100)}%分位），偏贵")
            signal_scores.append(-2)
    else:
        reasons.append(f"该城市暂无参考价格区间")

    # 3. 平台价差分析
    if all_prices and len(all_prices) >= 2:
        valid = [p for p in all_prices if p and p > 0]
        if len(valid) >= 2:
            min_p = min(valid)
            max_p = max(valid)
            spread = (max_p - min_p) / min_p * 100 if min_p > 0 else 0
            if spread > 15:
                reasons.append(f"多平台价差{spread:.0f}%，最低¥{min_p} vs 最高¥{max_p}，最低价平台优势明显")
                signal_scores.append(2)
            elif spread > 8:
                reasons.append(f"多平台价差{spread:.0f}%，最低¥{min_p} vs 最高¥{max_p}")
                signal_scores.append(1)
            else:
                reasons.append(f"多平台价差仅{spread:.0f}%，价格趋于一致")

    # 4. 房型价值（取消政策）
    if cancel_policy:
        if any(kw in cancel_policy for kw in ["免费取消", "免费退", "不可取消"]):
            if "不可取消" in cancel_policy and "免费取消" not in cancel_policy:
                reasons.append(f"当前为不可取消房型，如行程未确定建议选免费取消房型（通常贵10-20%但更灵活）")
                signal_scores.append(-1)
            elif "免费取消" in cancel_policy:
                reasons.append(f"当前房型支持免费取消，锁价无风险，建议先订后比")
                signal_scores.append(2)

    # 5. 临近降价判断（淡季+工作日+距入住3-7天）
    try:
        if not is_peak and not weekend and 3 <= days_left <= 7:
            reasons.append(f"淡季工作日+距入住{days_left}天，酒店可能临期降价清库存，可再等1-2天看看")
            signal_scores.append(-1)
    except:
        pass

    # 综合判断
    total = sum(signal_scores)

    if total >= 3:
        signal = "book"
        emoji = "🟢"
        text = "建议现在预订"
    elif total >= 1:
        signal = "book"
        emoji = "🟢"
        text = "倾向于预订"
    elif total <= -3:
        signal = "wait"
        emoji = "🔴"
        text = "建议继续观望"
    elif total <= -1:
        signal = "watch"
        emoji = "🟡"
        text = "可以再等等"
    else:
        signal = "watch"
        emoji = "🟡"
        text = "观望为主，逢低入手"

    tips = []
    if is_peak:
        tips.append("旺季出行，提前预订是最佳策略，酒店不会降价")
    try:
        if days_left and days_left > 21:
            tips.append("距入住较远，建议入住前2-3周再查价格")
        elif days_left and days_left <= 3 and not is_peak:
            tips.append("淡季临期可能降价，但也不一定，看你是赌还是稳")
    except:
        pass

    return {
        "signal": signal,
        "signal_emoji": emoji,
        "signal_text": text,
        "confidence": min(abs(total) / 8, 1.0),
        "reasons": reasons,
        "tips": tips,
        "price_percentile": int(percentile * 100) if percentile is not None else None,
        "city_price_range": {"low": city_ref[0], "mid": city_ref[1], "high": city_ref[2]} if city_ref else None,
    }


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
    """飞猪酒店搜索"""
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


def search_tuniu(city, check_in, check_out, keyword=None, adults=2, rooms=1):
    """途牛酒店搜索"""
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

        resp = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_hotel_search",
            "params": params,
        })
        data = resp.get("data", {})
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

            return {
                "source": "飞猪",
                "matched": True,
                "name": h_name,
                "price": price,
                "star": h.get("star", ""),
                "url": h.get("detailUrl", ""),
                "similarity": round(sim, 2),
                "error": None,
            }

        return {"source": "飞猪", "matched": False, "price": None, "url": None, "error": "未找到匹配酒店"}
    except Exception as e:
        return {"source": "飞猪", "matched": False, "price": None, "url": None, "error": str(e)}


def compare_rg(hotel_name, city, check_in, check_out, adults=2, rooms=1):
    """RG精确比价 + 佣金链接"""
    try:
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
            room_plans = data.get("roomRatePlans", [])
            lowest_price = 0
            cancel_policy = ""
            breakfast_info = ""

            if room_plans:
                priced_plans = [p for p in room_plans if p.get("totalPrice") and isinstance(p["totalPrice"], (int, float)) and p["totalPrice"] > 0]
                if priced_plans:
                    best_plan = min(priced_plans, key=lambda p: p["totalPrice"])
                    lowest_price = best_plan["totalPrice"]
                    cancel_policies = best_plan.get("cancellationPolicies", [])
                    if cancel_policies:
                        cancel_policy = "; ".join(c.get("description", "") for c in cancel_policies if c.get("description"))
                    breakfast_info = best_plan.get("mealPlan", "")
            elif data.get("totalPrice"):
                lowest_price = data["totalPrice"]

            return {
                "source": "RG",
                "matched": True,
                "name": data.get("name", hotel_name),
                "price": lowest_price,
                "star": data.get("starRating", ""),
                "url": data.get("bookingUrl", ""),
                "cancel_policy": cancel_policy,
                "breakfast": breakfast_info,
                "room_plans_count": len(room_plans),
                "error": None,
            }

        return {"source": "RG", "matched": False, "price": None, "url": None, "error": data.get("errorMessage", "查询失败") if data else "无返回数据"}
    except Exception as e:
        return {"source": "RG", "matched": False, "price": None, "url": None, "error": str(e)}


def compare_tuniu(hotel_name, city, check_in, check_out, adults=2, rooms=1):
    """途牛精确比价"""
    try:
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
            room_types = data.get("roomTypes", [])
            lowest_price = 0
            cancel_policy = ""
            breakfast_info = ""

            for rt in room_types:
                rate_plans = rt.get("ratePlans", [])
                for rp in rate_plans:
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
                        breakfast_info = rp.get("mealInfo", "") or rt.get("name", "")

            return {
                "source": "途牛",
                "matched": True,
                "name": data.get("hotelName", hotel_name),
                "price": lowest_price,
                "star": data.get("starName", ""),
                "score": data.get("commentScore", ""),
                "cancel_policy": cancel_policy,
                "breakfast": breakfast_info,
                "error": None,
            }

        # fallback: hotel_search
        brand = extract_brand(hotel_name)
        kw = brand if brand and brand != hotel_name else hotel_name[:4]
        resp = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_hotel_search",
            "params": {
                "cityName": city,
                "checkIn": check_in,
                "checkOut": check_out,
                "keyword": kw,
                "adultNum": adults,
                "roomNum": rooms,
            },
        })
        data = resp.get("data", {})
        if isinstance(data, dict) and data.get("error"):
            return {"source": "途牛", "matched": False, "price": None, "url": None, "error": data["error"]}

        hotels = data.get("hotels", []) or data.get("hotelList", [])
        for h in hotels:
            h_name = h.get("hotelName", h.get("name", ""))
            sim = hotel_name_similarity(hotel_name, h_name)
            if sim >= 0.35:
                price = h.get("lowestPrice", h.get("price", 0))
                if isinstance(price, str):
                    try:
                        price = float(price)
                    except (ValueError, TypeError):
                        price = 0
                return {
                    "source": "途牛",
                    "matched": True,
                    "name": h_name,
                    "price": price,
                    "star": h.get("starName", h.get("star", "")),
                    "score": h.get("commentScore", ""),
                    "similarity": round(sim, 2),
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
            "params": {"q": query},
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
# 命令：search
# ============================================================

def cmd_search(args):
    """搜索酒店列表 + 订房建议"""
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
    )

    # 合并去重
    hotels = []
    seen = []
    for src in [tuniu_result, fliggy_result]:
        for h in src.get("results", []):
            h_name = h.get("name", "")
            is_dup = any(hotel_name_similarity(h_name, s) > 0.7 for s in seen)
            if not is_dup:
                hotels.append(h)
                seen.append(h_name)

    # 按价格排序
    hotels.sort(key=lambda x: x.get("price", 999999) if isinstance(x.get("price"), (int, float)) and x.get("price", 0) > 0 else 999999)

    # 最低价酒店的订房建议
    lowest = None
    for h in hotels:
        if isinstance(h.get("price"), (int, float)) and h["price"] > 0:
            lowest = h
            break

    advice = None
    if lowest:
        all_prices = [h["price"] for h in hotels if isinstance(h.get("price"), (int, float)) and h["price"] > 0]
        cancel = lowest.get("cancel_policy", "")
        advice = book_or_wait(lowest["price"], args.city, args.check_in, args.check_out, all_prices, cancel, lowest.get("name", ""))

    output = {
        "success": True,
        "action": "search",
        "city": args.city,
        "check_in": args.check_in,
        "check_out": args.check_out,
        "count": len(hotels),
        "hotels": hotels[:20],
        "sources": {
            "飞猪": {"count": len(fliggy_result.get("results", [])), "error": fliggy_result.get("error")},
            "途牛": {"count": len(tuniu_result.get("results", [])), "error": tuniu_result.get("error")},
        },
        "lowest_price": lowest["price"] if lowest else None,
        "lowest_hotel": lowest["name"] if lowest else None,
        "lowest_url": lowest.get("url", "") if lowest else "",
        "advice": advice,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# 命令：calendar
# ============================================================

def cmd_calendar(args):
    """低价日历（扫描多入住日期价格）"""
    city = args.city
    keyword = args.keyword or city
    start_date = args.start_date
    nights = args.nights or 1
    days = min(args.days or 14, 30)

    calendar = []

    for i in range(days):
        try:
            d = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            check_in_str = d.strftime("%Y-%m-%d")
            check_out_dt = d + timedelta(days=nights)
            check_out_str = check_out_dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

        # 查飞猪（数据最全）
        result = search_fliggy(city, check_in_str, check_out_str, keyword=keyword)
        hotels = result.get("results", [])

        if hotels:
            prices = [h["price"] for h in hotels if isinstance(h.get("price"), (int, float)) and h["price"] > 0]
            lowest = min(prices) if prices else None
            best = None
            for h in hotels:
                if isinstance(h.get("price"), (int, float)) and h["price"] == lowest:
                    best = h
                    break

            calendar.append({
                "date": check_in_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()],
                "lowest_price": lowest,
                "hotel_count": len(hotels),
                "cheapest_hotel": best["name"] if best else None,
                "url": best.get("url", "") if best else "",
                "is_weekend": d.weekday() in (4, 5),
            })
        else:
            calendar.append({
                "date": check_in_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()],
                "lowest_price": None,
                "hotel_count": 0,
                "cheapest_hotel": None,
                "url": "",
                "is_weekend": d.weekday() in (4, 5),
            })

        time.sleep(0.3)

    # 价格标签
    priced_days = [d for d in calendar if d.get("lowest_price")]
    if priced_days:
        min_price = min(d["lowest_price"] for d in priced_days)
        avg_price = sum(d["lowest_price"] for d in priced_days) / len(priced_days)

        for d in calendar:
            p = d.get("lowest_price")
            if p:
                if p <= min_price * 1.05:
                    d["tag"] = "🟢 低价"
                elif p <= avg_price:
                    d["tag"] = "🟡 适中"
                else:
                    d["tag"] = "🔴 偏贵"
            else:
                d["tag"] = "— 无数据"

        cheapest = min(priced_days, key=lambda x: x["lowest_price"])
        advice = book_or_wait(cheapest["lowest_price"], city, cheapest["date"],
                              (datetime.strptime(cheapest["date"], "%Y-%m-%d") + timedelta(days=nights)).strftime("%Y-%m-%d"),
                              [d["lowest_price"] for d in priced_days],
                              "", cheapest.get("cheapest_hotel", ""))
    else:
        advice = None
        min_price = None
        avg_price = None
        cheapest = None

    output = {
        "success": True,
        "action": "calendar",
        "city": city,
        "keyword": keyword,
        "start_date": start_date,
        "nights": nights,
        "days": days,
        "calendar": calendar,
        "min_price": min_price,
        "avg_price": int(avg_price) if avg_price else None,
        "cheapest_date": cheapest["date"] if cheapest else None,
        "advice": advice,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# 命令：advisor
# ============================================================

def cmd_advisor(args):
    """指定酒店多平台精确比价 + 订房决策"""
    hotel_name = args.hotel
    city = args.city
    check_in = args.check_in
    check_out = args.check_out
    adults = args.adults or 2
    rooms = args.rooms or 1

    results = []

    results.append(compare_fliggy(hotel_name, city, check_in, check_out, adults))
    results.append(compare_rg(hotel_name, city, check_in, check_out, adults, rooms))
    results.append(compare_tuniu(hotel_name, city, check_in, check_out, adults, rooms))
    results.append(compare_tc(hotel_name, city, check_in, check_out, adults))

    # 按价格排序（同价按佣金优先级）
    priced = [r for r in results if r.get("matched") and r.get("price") and isinstance(r["price"], (int, float)) and r["price"] > 0]
    unpriced = [r for r in results if r not in priced]

    commission_order = {"RG": 0, "飞猪": 1, "途牛": 2, "同程": 3}
    priced.sort(key=lambda x: (x["price"], commission_order.get(x.get("source", ""), 9)))

    all_sorted = priced + unpriced

    # 房型/政策对比
    policy_compare = []
    for r in priced:
        entry = {
            "source": r["source"],
            "price": r["price"],
            "cancel_policy": r.get("cancel_policy", "未知"),
            "breakfast": r.get("breakfast", "未知"),
            "url": r.get("url", ""),
        }
        policy_compare.append(entry)

    # 最低价决策建议
    advice = None
    if priced:
        all_prices = [r["price"] for r in priced]
        cancel = priced[0].get("cancel_policy", "")
        advice = book_or_wait(priced[0]["price"], city, check_in, check_out, all_prices, cancel, hotel_name)

    output = {
        "success": True,
        "action": "advisor",
        "hotel_name": hotel_name,
        "city": city,
        "check_in": check_in,
        "check_out": check_out,
        "platforms": all_sorted,
        "policy_compare": policy_compare,
        "lowest_price": priced[0]["price"] if priced else None,
        "lowest_platform": priced[0]["source"] if priced else None,
        "lowest_url": priced[0].get("url") if priced else None,
        "advice": advice,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="酒店聪明订：多平台比价+低价日历+订房建议")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # search
    search_p = subparsers.add_parser("search", help="搜索酒店（多源合并+订房建议）")
    search_p.add_argument("--city", required=True, help="城市名")
    search_p.add_argument("--check-in", required=True, help="入住日期 YYYY-MM-DD")
    search_p.add_argument("--check-out", required=True, help="离店日期 YYYY-MM-DD")
    search_p.add_argument("--keyword", default=None, help="关键词/地标")
    search_p.add_argument("--adults", type=int, default=2, help="入住人数")
    search_p.add_argument("--rooms", type=int, default=1, help="房间数")

    # calendar
    cal_p = subparsers.add_parser("calendar", help="低价日历（扫描多入住日期价格）")
    cal_p.add_argument("--city", required=True, help="城市名")
    cal_p.add_argument("--keyword", default=None, help="关键词/地标")
    cal_p.add_argument("--start-date", required=True, help="起始入住日期 YYYY-MM-DD")
    cal_p.add_argument("--nights", type=int, default=1, help="住几晚")
    cal_p.add_argument("--days", type=int, default=14, help="扫描天数（最多30）")

    # advisor
    adv_p = subparsers.add_parser("advisor", help="指定酒店订房决策")
    adv_p.add_argument("--hotel", required=True, help="酒店名称")
    adv_p.add_argument("--city", required=True, help="城市名")
    adv_p.add_argument("--check-in", required=True, help="入住日期 YYYY-MM-DD")
    adv_p.add_argument("--check-out", required=True, help="离店日期 YYYY-MM-DD")
    adv_p.add_argument("--adults", type=int, default=2, help="入住人数")
    adv_p.add_argument("--rooms", type=int, default=1, help="房间数")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "calendar":
        cmd_calendar(args)
    elif args.command == "advisor":
        cmd_advisor(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
