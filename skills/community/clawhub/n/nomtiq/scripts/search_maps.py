#!/usr/bin/env python3
from __future__ import annotations

"""
Nomtiq 小饭票 - 地图 API 搜索
中国：高德地图 Web Service API（POI 2.0）
海外：Serper Google Maps（结构化数据）

安全约束：
  - 只从 AMAP_WEBSERVICE_KEY 环境变量读取 Key。
  - 兼容旧变量 AMAP_KEY，但不再推荐使用。
  - 可选 AMAP_WEBSERVICE_SECRET 用于生成高德数字签名。
  - 不打印、不保存、不返回包含 Key 或安全密钥的请求 URL。

用法:
  python3 search_maps.py "约会餐厅 环境好" --city 长沙 --district 岳麓区
  python3 search_maps.py "romantic restaurant" --city "Changsha" --mode overseas
  python3 search_maps.py "dim sum" --city "New York" --mode overseas
"""

import sys, json, argparse, os, re, hashlib
from urllib.request import Request
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

from serper_client import search_maps_raw, search_web
from safe_http import is_allowed_https_url, open_no_redirect, quoted_search_term

# ── 高德地图 POI 搜索 ─────────────────────────────────────────

# 高德餐饮 POI 类型代码
AMAP_FOOD_TYPES = '050000'  # 餐饮服务大类
AMAP_API_BASE = 'https://restapi.amap.com'
_WARNED_LEGACY_KEY = False


def _get_amap_credentials() -> tuple[str, str]:
    """只从运行环境读取高德凭证，不读取 skill 目录内配置文件。"""
    global _WARNED_LEGACY_KEY
    key = os.environ.get('AMAP_WEBSERVICE_KEY', '').strip()
    if not key:
        key = os.environ.get('AMAP_KEY', '').strip()
        if key and not _WARNED_LEGACY_KEY:
            print("⚠️  AMAP_KEY 已废弃，请迁移到 AMAP_WEBSERVICE_KEY", file=sys.stderr)
            _WARNED_LEGACY_KEY = True
    secret = os.environ.get('AMAP_WEBSERVICE_SECRET', '').strip()
    return key, secret


def _sign_amap_params(params: dict, secret: str) -> str:
    """按高德 Web Service 数字签名规则生成 sig。"""
    canonical = '&'.join(
        f"{name}={params[name]}" for name in sorted(params) if params[name] is not None
    )
    return hashlib.md5(f"{canonical}{secret}".encode('utf-8')).hexdigest()


def _amap_request(path: str, params: dict, timeout: int = 10) -> dict:
    """调用高德 API，错误输出不得包含完整 URL、Key 或安全密钥。"""
    key, secret = _get_amap_credentials()
    if not key:
        print("⚠️  未配置 AMAP_WEBSERVICE_KEY，跳过高德搜索", file=sys.stderr)
        return {}

    request_params = {
        name: str(value)
        for name, value in params.items()
        if value is not None and value != ''
    }
    request_params['key'] = key
    if secret:
        request_params['sig'] = _sign_amap_params(request_params, secret)

    url = f"{AMAP_API_BASE}{path}?{urlencode(request_params)}"
    try:
        req = Request(url, headers={'User-Agent': 'Nomtiq/0.5.1'})
        with open_no_redirect(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except (HTTPError, URLError, TimeoutError):
        print("高德请求失败（网络或服务不可用）", file=sys.stderr)
        return {}
    except (json.JSONDecodeError, ValueError):
        print("高德返回了无法解析的数据", file=sys.stderr)
        return {}
    except Exception:
        print("高德请求失败", file=sys.stderr)
        return {}

    if data.get('status') != '1':
        info = str(data.get('info') or '未知错误')[:80]
        infocode = str(data.get('infocode') or '')[:20]
        suffix = f" ({infocode})" if infocode else ''
        print(f"高德 API 错误: {info}{suffix}", file=sys.stderr)
        return {}
    return data


def _geocode_amap(place: str, city: str = '') -> str:
    """将明确地点解析为高德经纬度，失败时返回空字符串。"""
    if not place:
        return ''
    data = _amap_request('/v3/geocode/geo', {
        'address': place,
        'city': city,
        'batch': 'false',
        'output': 'json',
    })
    geocodes = data.get('geocodes') or []
    if not geocodes:
        return ''
    return str(geocodes[0].get('location') or '')


def search_amap(query: str, city: str = '', district: str = '',
                max_results: int = 20, radius: int = 3000) -> list:
    """
    高德 POI 2.0 搜索。

    有明确地点时：地理编码 -> v5/place/around。
    只有城市/关键词时：v5/place/text。
    单次最多返回 25 条，避免推荐任务中的无界分页请求。
    """
    key, _ = _get_amap_credentials()
    if not key:
        print("⚠️  未配置 AMAP_WEBSERVICE_KEY，跳过高德搜索", file=sys.stderr)
        return []

    page_size = max(1, min(int(max_results), 25))
    common = {
        'types': AMAP_FOOD_TYPES,
        'show_fields': 'business',
        'page_size': page_size,
        'page_num': 1,
        'output': 'json',
    }

    data = {}
    if district:
        center = _geocode_amap(district, city)
        if center:
            data = _amap_request('/v5/place/around', {
                **common,
                'location': center,
                'keywords': query,
                'radius': max(100, min(int(radius), 50000)),
                'sortrule': 'weight',
                'region': city,
                'city_limit': 'true' if city else 'false',
            })

    if not data:
        keywords = f"{district} {query}".strip()
        data = _amap_request('/v5/place/text', {
            **common,
            'keywords': keywords,
            'region': city or district,
            'city_limit': 'true' if (city or district) else 'false',
        })

    results = []
    for poi in data.get('pois') or []:
        parsed = _parse_amap_poi(poi)
        if parsed:
            results.append(parsed)
    return results


def _parse_amap_poi(poi: dict) -> dict | None:
    """解析高德 POI 数据"""
    name = poi.get('name', '')
    if not name:
        return None

    # 过滤非餐厅（快餐/便利店/超市）
    type_name = poi.get('type', '')
    # 高德 type 格式："餐饮服务;中餐厅;湘菜" → 取最后一段
    type_display = type_name.split(';')[-1] if ';' in type_name else type_name
    poi['_type_display'] = type_display
    skip_types = ['快餐', '便利店', '超市', '食堂', '小吃', '早餐']
    if any(t in type_name for t in skip_types):
        return None

    # POI 2.0 通过 show_fields=business 返回商业字段。
    # biz_ext 仅作为旧版响应兼容。
    business = poi.get('business') or poi.get('biz_ext') or {}
    rating = None
    rating_raw = business.get('rating', '')
    if rating_raw and rating_raw != 'none':
        try:
            rating = float(rating_raw)
        except:
            pass

    # 人均消费
    avg_cost = None
    cost_raw = business.get('cost', '')
    if cost_raw and cost_raw != 'none':
        try:
            avg_cost = int(float(cost_raw))
        except:
            pass

    # 营业时间
    open_time = (
        business.get('opentime_today', '')
        or business.get('opentime_week', '')
        or business.get('open_time', '')
    )

    # 地址
    address = poi.get('address', '')
    if isinstance(address, list):
        address = ''.join(address)

    # 区域
    pname = poi.get('pname', '')   # 省
    cityname = poi.get('cityname', '')  # 市
    adname = poi.get('adname', '')  # 区

    # 菜系（从 type 字段提取）
    cuisines = _extract_cuisines_cn(
        type_name + ' ' + name + ' ' + str(business.get('tag', ''))
    )
    type_display = poi.get('_type_display', type_name)

    return {
        'name': name,
        'score': rating,
        'avg_price': avg_cost,
        'cuisines': cuisines,
        'type': type_display,
        'address': address,
        'district': adname,
        'city': cityname,
        'open_time': open_time,
        'tel': poi.get('tel', '') or business.get('tel', ''),
        'source': 'amap',
        'sources': ['amap'],
        'cross_verified': False,
        'amap_id': poi.get('id', ''),
        'location': poi.get('location', ''),  # 经纬度
        'distance': poi.get('distance', ''),
        'business_area': business.get('business_area', ''),
    }


# ── 百度地图 POI 搜索 ─────────────────────────────────────────

BMAP_KEY = os.environ.get('BMAP_KEY', '')


def search_bmap(query: str, city: str = '', district: str = '',
                max_results: int = 20) -> list:
    """百度地图地点检索"""
    if not BMAP_KEY:
        print("⚠️  未配置 BMAP_KEY，跳过百度搜索", file=sys.stderr)
        return []

    region = district or city

    params = {
        'ak': BMAP_KEY,
        'query': query,
        'region': region,
        'output': 'json',
        'page_size': min(max_results, 20),
        'page_num': 0,
        'scope': 2,  # 返回详细信息
        'filter': 'industry_type:cater',  # 只返回餐饮
    }

    url = f"https://api.map.baidu.com/place/v2/search?{urlencode(params)}"
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with open_no_redirect(req, timeout=10) as resp:
            data = json.loads(resp.read())

        if data.get('status') != 0:
            print(f"百度地图 API 错误: {data.get('message')}", file=sys.stderr)
            return []

        results = []
        for place in data.get('results', []):
            r = _parse_bmap_place(place)
            if r:
                results.append(r)
        return results

    except Exception:
        print("百度搜索出错（网络、服务或响应不可用）", file=sys.stderr)
        return []


def _parse_bmap_place(place: dict) -> dict | None:
    name = place.get('name', '')
    if not name:
        return None

    detail = place.get('detail_info', {})

    rating = None
    rating_raw = detail.get('overall_rating', '')
    if rating_raw:
        try:
            rating = float(rating_raw)
        except:
            pass

    avg_cost = None
    cost_raw = detail.get('price', '')
    if cost_raw:
        try:
            avg_cost = int(float(cost_raw))
        except:
            pass

    tag = detail.get('tag', '')
    cuisines = _extract_cuisines_cn(tag + ' ' + name)

    return {
        'name': name,
        'score': rating,
        'avg_price': avg_cost,
        'cuisines': cuisines,
        'type': tag,
        'address': place.get('address', ''),
        'district': place.get('area', ''),
        'city': '',
        'tel': place.get('telephone', ''),
        'source': 'bmap',
        'sources': ['bmap'],
        'cross_verified': False,
        'bmap_uid': place.get('uid', ''),
    }


# ── Serper Google Maps（海外）────────────────────────────────

def search_serper_maps(query: str, city: str = '', max_results: int = 20) -> list:
    """Serper Google Maps 搜索（海外场景，直接调用官方 API）。"""
    full_query = f"{query} {city}".strip()
    results = []
    for place in search_maps_raw(full_query, max_results):
        parsed = _parse_serper_place(place)
        if parsed:
            results.append(parsed)
    return results


def _parse_serper_place(p: dict) -> dict | None:
    name = p.get('title', '')
    if not name:
        return None

    # 过滤评分太低或评论太少的
    rating = p.get('rating')
    rating_count = p.get('ratingCount', 0) or 0

    # 价格档次 $ $$ $$$ $$$$
    price_level = len(p.get('priceLevel', '')) if p.get('priceLevel') else None

    type_str = p.get('type', '') or ''
    if isinstance(p.get('types'), list):
        type_str = ', '.join(p['types'])

    cuisines = _extract_cuisines_en(type_str + ' ' + name)

    return {
        'name': name,
        'score': rating,
        'rating_count': rating_count,
        'price_level': price_level,
        'cuisines': cuisines,
        'type': type_str,
        'address': p.get('address', ''),
        'open_now': p.get('openingHours') is not None,
        'opening_hours': p.get('openingHours', {}),
        'thumbnail': p.get('thumbnailUrl', ''),
        'source': 'google_maps',
        'sources': ['google_maps'],
        'cross_verified': False,
        'place_id': p.get('placeId', ''),
        'cid': p.get('cid', ''),
    }


# ── 双源合并（高德 + 百度）────────────────────────────────────

def merge_cn_sources(amap_results: list, bmap_results: list) -> list:
    """合并高德和百度结果，同名店铺交叉验证"""
    merged = {}

    for r in amap_results:
        key = _normalize_name(r['name'])
        merged[key] = r

    for r in bmap_results:
        key = _normalize_name(r['name'])
        if key in merged:
            merged[key]['cross_verified'] = True
            merged[key]['sources'].append('bmap')
            # 补充缺失的评分
            if not merged[key].get('score') and r.get('score'):
                merged[key]['score'] = r['score']
            if not merged[key].get('avg_price') and r.get('avg_price'):
                merged[key]['avg_price'] = r['avg_price']
        else:
            merged[key] = r

    return list(merged.values())


def _normalize_name(name: str) -> str:
    """标准化店名用于匹配（去掉括号内容、空格）"""
    name = re.sub(r'[（(][^）)]*[）)]', '', name)
    name = re.sub(r'\s+', '', name)
    return name.lower()


# ── 菜系提取 ─────────────────────────────────────────────────

def _extract_cuisines_cn(text: str) -> list:
    mapping = {
        '湘菜': ['湘菜', '湖南菜', '湘式'],
        '粤菜': ['粤菜', '广东菜', '顺德', '港式', '烧味', '早茶'],
        '川菜': ['川菜', '四川', '麻辣', '火锅'],
        '日料': ['日料', '日本料理', '寿司', '刺身', '居酒屋', 'omakase'],
        '西餐': ['西餐', '法餐', '意大利', '牛排', 'bistro', 'Bistro'],
        '云南菜': ['云南', '滇菜', '米线'],
        '海鲜': ['海鲜', '水产', '鱼'],
        '烧烤': ['烧烤', '烤肉', '串串'],
        '私房菜': ['私房', '私厨', '家宴'],
    }
    result = []
    for cuisine, kws in mapping.items():
        if any(kw in text for kw in kws):
            result.append(cuisine)
    return result


def _extract_cuisines_en(text: str) -> list:
    mapping = {
        'Chinese': ['chinese', 'hunan', 'cantonese', 'sichuan', 'dim sum'],
        'Japanese': ['japanese', 'sushi', 'ramen', 'izakaya'],
        'Korean': ['korean', 'bbq'],
        'Italian': ['italian', 'pizza', 'pasta'],
        'French': ['french', 'bistro', 'brasserie'],
        'Thai': ['thai'],
        'Indian': ['indian', 'curry'],
        'American': ['american', 'burger', 'steakhouse'],
        'Western': ['western', 'european'],
    }
    text_lower = text.lower()
    result = []
    for cuisine, kws in mapping.items():
        if any(kw in text_lower for kw in kws):
            result.append(cuisine)
    return result


# ── 主入口 ────────────────────────────────────────────────────

def search_maps(query: str, city: str = '', district: str = '',
                mode: str = 'china', max_results: int = 20) -> list:
    """统一地图搜索入口"""
    if mode == 'china':
        print(f"🗺️  高德地图搜索...", file=sys.stderr)
        amap = search_amap(query, city, district, max_results)
        print(f"   高德: {len(amap)} 家", file=sys.stderr)

        bmap = []
        if BMAP_KEY:
            print(f"🗺️  百度地图搜索（可选）...", file=sys.stderr)
            bmap = search_bmap(query, city or district, district, max_results)
            print(f"   百度: {len(bmap)} 家", file=sys.stderr)

        merged = merge_cn_sources(amap, bmap)
        print(f"   合并后: {len(merged)} 家（{sum(1 for r in merged if r.get('cross_verified'))} 家双源验证）", file=sys.stderr)
        return merged

    else:  # overseas
        print(f"🗺️  Google Maps 搜索...", file=sys.stderr)
        results = search_serper_maps(f"{query} restaurant", city, max_results)
        print(f"   找到: {len(results)} 家", file=sys.stderr)
        return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nomtiq - 地图 API 搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--city', default='', help='城市')
    parser.add_argument('--district', default='', help='区域（如：岳麓区）')
    parser.add_argument('--mode', choices=['china', 'overseas'], default='china')
    parser.add_argument('--max', type=int, default=20)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    results = search_maps(args.query, args.city, args.district, args.mode, args.max)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        sys.exit(0)

    print(f"\n找到 {len(results)} 家餐厅\n")
    for i, r in enumerate(results[:15], 1):
        score = f"⭐{r['score']}" if r.get('score') else ''
        price_cn = f"¥{r['avg_price']}" if r.get('avg_price') else ''
        price_en = '$' * r['price_level'] if r.get('price_level') else ''
        price = price_cn or price_en
        cuisines = '/'.join(r.get('cuisines', [])[:2])
        verified = '✅双源' if r.get('cross_verified') else ''
        district = r.get('district', '')
        info = ' | '.join(p for p in [price, score, cuisines, district, verified] if p)
        print(f"{i}. {r['name']}")
        if info:
            print(f"   {info}")
        if r.get('address'):
            print(f"   📍 {r['address'][:60]}")
        print()


# ── 社交媒体交叉验证（公开数据，无需登录）────────────────────

def cross_verify_social(restaurants: list, max_verify: int = 5) -> list:
    """
    用 Serper 搜索公开社交媒体数据做交叉验证。
    不需要用户登录任何账号。
    国内：搜小红书 + 大众点评公开页面
    """
    print(f"🔍 社交媒体交叉验证（top {max_verify}）...", file=sys.stderr)

    for r in restaurants[:max_verify]:
        name = r['name']
        clean_name = re.sub(r'[（(][^）)]*[）)]', '', name).strip()

        # 搜小红书公开页面
        xhs_query = f'site:xiaohongshu.com {quoted_search_term(clean_name)} 探店'
        hits = [
            hit for hit in search_web(xhs_query, 3, country='cn', language='zh-cn')
            if is_allowed_https_url(
                hit.get('url') or hit.get('link') or '',
                ('xiaohongshu.com',),
            )
        ]
        if hits:
            r['xhs_verified'] = True
            snippets = ' '.join(
                h.get('snippet', '') + h.get('title', '') for h in hits
            )
            neg_words = ['难吃', '踩雷', '失望', '不推荐', '差评', '坑', '后悔', '一般']
            pos_words = ['好吃', '推荐', '必去', '超棒', '喜欢', '值得', '宝藏', '惊喜']
            neg = sum(1 for w in neg_words if w in snippets)
            pos = sum(1 for w in pos_words if w in snippets)
            r['xhs_sentiment'] = 'negative' if neg > pos else ('positive' if pos > 0 else 'neutral')
            print(f"   ✅ {clean_name}: 小红书 {len(hits)} 条，情感={r['xhs_sentiment']}", file=sys.stderr)
        else:
            print(f"   — {clean_name}: 小红书无记录", file=sys.stderr)

    return restaurants




# 连锁品牌黑名单（饭卡模式过滤）
CHAIN_BRANDS = [
    '麦当劳', '肯德基', '必胜客', '星巴克', '海底捞', '西贝', '外婆家',
    '绿茶', '太二', '九毛九', '呷哺', '小龙坎', '大龙燚', '巴奴',
    '眉州东坡', '全聚德', '便宜坊', '东来顺', '旺顺阁',
    '萨莉亚', '必胜客', '棒约翰', '汉堡王', '德克士',
]

def fancard_filter(results: list, budget_low: int = 60, budget_high: int = 250) -> list:
    """
    饭卡模式过滤：
    - 评分 >= 4.3（陈晓卿定律：街边小店 3.5-4 才真实，这里用高德评分体系）
    - 人均在预算范围内
    - 非连锁品牌
    - 非快餐/食堂类型
    """
    filtered = []
    for r in results:
        # 评分过滤
        score = r.get('score')
        if score and score < 4.3:
            continue

        # 人均过滤
        price = r.get('avg_price')
        if price:
            if price < budget_low or price > budget_high:
                continue

        # 连锁过滤
        name = r.get('name', '')
        if any(brand in name for brand in CHAIN_BRANDS):
            continue

        # 类型过滤（快餐/食堂）
        type_name = r.get('type', '')
        skip = ['快餐', '食堂', '便利', '超市', '早餐', '面包', '甜品', '奶茶', '咖啡']
        if any(s in type_name for s in skip):
            continue

        filtered.append(r)

    # 按评分排序
    filtered.sort(key=lambda x: (x.get('score') or 0), reverse=True)
    return filtered


def generate_fancard_blurb(r: dict, is_explorer: bool = False) -> str:
    """饭卡模式推荐语（规则版，供 OpenClaw 润色）"""
    address = r.get('address', '') or ''
    cuisines = r.get('cuisines', [])
    price = r.get('avg_price', 0) or 0
    name = r.get('name', '')
    score = r.get('score', 0) or 0

    parts = []

    # 菜系稀缺性优先（比位置更有个性）
    rare = {
        '江苏菜': '苏帮菜在北京不多见',
        '闽菜': '闽菜在北京少见，值得试',
        '云南菜': '云南菜的香料用得讲究',
        '私房菜': '私房菜，不是连锁，有自己的风格',
        '粤菜': '粤菜讲究食材本味，不靠调料',
    }
    # cuisines 字段 + type 字段都检查
    cuisine_text = cuisines + [r.get('type', '')]
    for c in cuisine_text:
        if c in rare:
            parts.append(rare[c])
            break

    # 位置感知（菜系没命中时用）
    if not parts:
        loc_hints = {
            '798': '798 艺术区里，环境有调性，两个人坐下来不会觉得吵',
            '丽都': '藏在丽都花园里，安静，不是随便就能找到的地方',
            '将台': '将台的老街区，不靠流量，靠口碑',
            '蓝色港湾': '蓝色港湾里，环境好，适合慢慢聊',
            '酒仙桥': '酒仙桥的本地馆子，开了好几年了',
            '三里屯': '三里屯里的馆子，热闹但不嘈杂',
            '望京': '望京的街边小馆，本地人常去的那种',
        }
        for loc, hint in loc_hints.items():
            if loc in address or loc in name:
                parts.append(hint)
                break

    # 探索推荐专属
    if is_explorer and not parts:
        parts.append('你可能没去过，但值得试一次')

    # 社交媒体口碑（不暴露技术细节，只说结论）
    if r.get('xhs_verified'):
        if r.get('xhs_sentiment') == 'negative':
            parts.append('留个心眼，有差评')
        else:
            # positive 或 neutral 都算有口碑
            parts.append('小红书有探店，本地人去过')

    # 价格感知（中国逻辑：价格越高，人越少，越安静）
    if price:
        if price >= 150 and not any('安静' in p for p in parts):
            parts.append('人均过百五，人不多，安静，适合聊天')
        elif price >= 80 and price < 150:
            parts.append('人均一百左右，不会有压力')
        elif price < 80:
            parts.append('价格实惠，但可能热闹')

    if not parts and score >= 4.7:
        parts.append('4.7 分，口碑在那里，不用多说')

    return '。'.join(parts[:2]) + '。' if parts else ''


def search_fancard(location: str, city: str = '北京',
                   budget_low: int = 80, budget_high: int = 300) -> list:
    """
    饭卡模式主入口：找适合两人聊天的本地小馆
    location: 地点（如"酒仙桥"）
    """
    # 周边搜索只调用一次 POI API，再在本地做风格和预算筛选。
    results = search_amap('', city, location, max_results=25)
    filtered = fancard_filter(results, budget_low, budget_high)

    # 社交媒体交叉验证（top 5，公开数据，无需登录）
    filtered = cross_verify_social(filtered, max_verify=5)

    # 加推荐语
    for i, r in enumerate(filtered):
        r['blurb'] = generate_fancard_blurb(r, is_explorer=(i >= 2))

    return filtered
