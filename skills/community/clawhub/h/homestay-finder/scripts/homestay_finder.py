import os
import argparse
import json
import urllib.request
import urllib.error

# ============ Config ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
TUNIU_PROXY = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# 公寓关键词黑名单
_APARTMENT_KEYWORDS = ["公寓", "商务酒店", "连锁酒店"]


# ============ Proxy Call ============
def _post_proxy(url, payload):
    """统一代理调用，X-Proxy-Token认证"""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Proxy-Token": PROXY_TOKEN,
        },
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("data", data)
    except urllib.error.HTTPError as e:
        return {"error": "proxy error " + str(e.code)}
    except Exception as e:
        return {"error": "request error: " + str(e)}


# ============ 飞猪搜索 ============
def _fliggy_search(dest_name, key_words="", poi_name="",
                   check_in_date="", check_out_date="",
                   max_price=0, sort=""):
    """飞猪search_hotels结构化搜索，返回民宿列表"""
    params = {
        "destName": dest_name,
        "checkInDate": check_in_date or "2026-07-01",
        "checkOutDate": check_out_date or "2026-07-02",
    }
    kw_parts = []
    if key_words:
        kw_parts.append(key_words)
    if poi_name:
        kw_parts.append(poi_name)
    kw_parts.append("民宿")
    params["keyWords"] = " ".join(kw_parts)

    result = _post_proxy(FLIGGY_PROXY, {"type": "search_hotels", "params": params})
    if isinstance(result, dict) and "error" in result:
        return []
    items = result.get("itemList", []) if isinstance(result, dict) else []
    return items


def _fliggy_ai_recommend(query):
    """飞猪fliggy_ai_search语义推荐，返回AI生成文本"""
    if "民宿" not in query and "客栈" not in query and "住宿" not in query:
        query = query + " 民宿"
    result = _post_proxy(FLIGGY_PROXY, {"type": "fliggy_ai_search", "params": {"query": query}})
    return result


# ============ 途牛搜索 ============
def _tuniu_search(city_name, keyword="民宿", check_in_date="", check_out_date=""):
    """途牛tuniu_hotel_search，返回民宿列表"""
    params = {
        "cityName": city_name,
        "checkInDate": check_in_date or "2026-07-01",
        "checkOutDate": check_out_date or "2026-07-02",
        "keyword": keyword,
    }
    result = _post_proxy(TUNIU_PROXY, {"type": "tuniu_hotel_search", "params": params})
    if isinstance(result, dict) and "error" in result:
        return []
    hotels = result.get("hotels", []) if isinstance(result, dict) else []
    return hotels


# ============ 数据清洗与合并 ============
def _is_homestay(name):
    """判断是否为民宿/客栈类（过滤公寓和商务酒店）"""
    for kw in _APARTMENT_KEYWORDS:
        if kw in name:
            return False
    return True


def _normalize_homestay(source, item):
    """统一数据结构"""
    if source == "fliggy":
        name = item.get("name", "")
        price_str = item.get("price", "")
        price = _parse_price(price_str)
        return {
            "name": name,
            "price": price,
            "price_display": price_str,
            "star": item.get("star", ""),
            "score": item.get("score", "") or item.get("commentScore", ""),
            "address": item.get("address", ""),
            "poi": item.get("interestsPoi", ""),
            "url": item.get("detailUrl", ""),
            "pic": item.get("mainPic", ""),
            "source": "飞猪",
        }
    elif source == "tuniu":
        name = item.get("hotelName", "")
        price = item.get("lowestPrice", 0) or 0
        return {
            "name": name,
            "price": price,
            "price_display": "¥" + str(price) + "起" if price else "",
            "star": item.get("starName", ""),
            "score": str(item.get("commentScore", "")),
            "address": item.get("address", ""),
            "poi": "",
            "url": "",
            "source": "途牛",
        }
    return None


def _parse_price(price_str):
    """从价格字符串提取数字"""
    if not price_str:
        return 99999
    import re
    m = re.search(r'\d+', str(price_str).replace(',', ''))
    return int(m.group()) if m else 99999


def _merge_and_dedup(fliggy_items, tuniu_items, sort=""):
    """合并去重，同名取最低价"""
    all_items = []
    for item in fliggy_items:
        n = _normalize_homestay("fliggy", item)
        if n and _is_homestay(n["name"]):
            all_items.append(n)
    for item in tuniu_items:
        n = _normalize_homestay("tuniu", item)
        if n and _is_homestay(n["name"]):
            all_items.append(n)

    # 按名称去重（取低价）
    seen = {}
    for item in all_items:
        key = item["name"].strip()
        if key not in seen or item["price"] < seen[key]["price"]:
            seen[key] = item

    result = list(seen.values())

    # 排序
    if sort == "price_asc":
        result.sort(key=lambda x: x["price"])
    elif sort == "price_desc":
        result.sort(key=lambda x: -x["price"])
    elif sort == "rate_desc":
        def _score_key(x):
            try:
                return -float(x["score"])
            except (ValueError, TypeError):
                return 0
        result.sort(key=_score_key)
    else:
        result.sort(key=lambda x: x["price"])

    return result[:15]


# ============ 格式化输出 ============
def _format_homestay_list(items):
    """格式化民宿列表输出"""
    if not items:
        return "未找到符合条件的特色民宿，建议换关键词或扩大搜索范围。"

    lines = []
    for i, item in enumerate(items, 1):
        line = f"**{i}. {item['name']}**\n"
        if item.get("star"):
            line += f"   类型：{item['star']}\n"
        if item.get("score") and str(item["score"]).strip():
            line += f"   评分：{item['score']}\n"
        if item.get("price_display"):
            line += f"   价格：{item['price_display']}\n"
        if item.get("address"):
            line += f"   地址：{item['address']}\n"
        if item.get("poi"):
            line += f"   附近：{item['poi']}\n"
        if item.get("url"):
            line += f"   [{item['source']}预订]({item['url']})\n"
        if item.get("pic"):
            line += f"   ![{item['name']}]({item['pic']})\n"
        lines.append(line)

    sources = set(item["source"] for item in items)
    lines.append(f"\n数据来源：{'/'.join(sources)} | 价格实时变动，以实际下单为准")
    return "\n".join(lines)


def _format_ai_result(data):
    """格式化AI推荐结果"""
    if isinstance(data, str):
        text = data
    elif isinstance(data, dict):
        if "error" in data:
            return "推荐失败: " + data["error"]
        if "raw_text" in data:
            text = data["raw_text"]
        elif "itemList" in data:
            items = []
            for h in data.get("itemList", []):
                info = h.get("info", h)
                name = info.get("title", "")
                url = info.get("jumpUrl", "")
                if name:
                    entry = f"- **{name}**"
                    if url:
                        entry += f" [查看详情]({url})"
                    items.append(entry)
            return "\n".join(items) + "\n\n数据来源：飞猪旅行"
        else:
            text = json.dumps(data, ensure_ascii=False)
    else:
        text = str(data)

    if "飞猪" not in text:
        text = text.rstrip() + "\n\n数据来源：飞猪旅行"
    return text


# ============ 跨服务提示 ============
_DEST_TIPS = [
    "大理", "莫干山", "三亚", "丽江", "成都", "杭州", "厦门", "桂林", "苏州",
    "西安", "黄山", "张家界", "九寨沟", "凤凰古城", "平遥", "乌镇", "西塘",
    "阳朔", "婺源", "泸沽湖", "香格里拉", "稻城", "青海湖", "敦煌",
]


def _build_tips(text):
    dest = ""
    for d in _DEST_TIPS:
        if d in text:
            dest = d
            break
    if dest:
        tips = f"🗺️规划{dest}行程 | 🚄查去{dest}的火车票 | ✈️查去{dest}的机票 | 🏨推荐{dest}酒店 | 🎫推荐{dest}景点 | 🍜推荐{dest}美食"
    else:
        tips = "🗺️行程规划 | 🚄火车票查询 | ✈️机票查询 | 🏨酒店搜索 | 🎫景点门票 | 🍜美食推荐"
    return "\n\n💡 我还能帮你：" + tips


# ============ Main ============
def main():
    parser = argparse.ArgumentParser(description="特色民宿搜索推荐")
    sub = parser.add_subparsers(dest="action", required=True)

    # search_homestay
    s = sub.add_parser("search", help="结构化搜索特色民宿")
    s.add_argument("--dest_name", required=True, help="目的地，如大理、莫干山、三亚")
    s.add_argument("--key_words", default="", help="关键词，如海景、亲子、山景")
    s.add_argument("--poi_name", default="", help="附近景点，如洱海、灵隐寺")
    s.add_argument("--check_in_date", default="", help="入住日期 YYYY-MM-DD")
    s.add_argument("--check_out_date", default="", help="退房日期 YYYY-MM-DD")
    s.add_argument("--max_price", type=int, default=0, help="最高价格，0不限")
    s.add_argument("--sort", default="", help="排序：price_asc/price_desc/rate_desc")

    # recommend_homestay
    r = sub.add_parser("recommend", help="AI语义推荐特色民宿")
    r.add_argument("--query", required=True, help="自然语言需求描述")

    args = parser.parse_args()

    if args.action == "search":
        # 结构化搜索：飞猪+途牛双源
        fliggy_items = _fliggy_search(
            args.dest_name, args.key_words, args.poi_name,
            args.check_in_date, args.check_out_date,
            args.max_price, args.sort
        )
        tuniu_items = _tuniu_search(
            args.dest_name, "民宿",
            args.check_in_date, args.check_out_date
        )

        merged = _merge_and_dedup(fliggy_items, tuniu_items, args.sort)

        # 价格过滤
        if args.max_price > 0:
            merged = [h for h in merged if h["price"] <= args.max_price]

        text = _format_homestay_list(merged)
        text += _build_tips(args.dest_name)
        print(text)

    elif args.action == "recommend":
        # AI语义推荐：飞猪AI搜索
        result = _fliggy_ai_recommend(args.query)
        text = _format_ai_result(result)
        text += _build_tips(args.query)
        print(text)


if __name__ == "__main__":
    main()
