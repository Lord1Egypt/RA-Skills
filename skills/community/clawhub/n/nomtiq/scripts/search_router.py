#!/usr/bin/env python3
"""
Nomtiq 小饭票 - 智能路由搜索
自动判断用户 locale，切换对应数据源：
  - 中国境内 → 大众点评 + 小红书
  - 海外华人 → Google Places + Yelp + 小红书
  - 海外用户 → Google Places + Yelp + Reddit

用法:
  python3 search_all.py "三里屯 创意菜"
  python3 search_all.py "ramen Manhattan" --city "New York"
  python3 search_all.py "dim sum Flushing" --city "New York" --locale overseas-chinese
"""

import sys
import json
import argparse
import re
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from search import search_dianping
from search_xhs import search_xiaohongshu
from search_global import search_all_global
from search_maps import search_maps, search_serper_maps, cross_verify_social

DATA_DIR = Path(__file__).parent.parent / 'data'
PROFILE_PATH = DATA_DIR / 'taste-profile.json'


# ── Locale 自动推断 ──────────────────────────────────────────

CHINA_SIGNALS = [
    # 中文地名
    '北京', '上海', '广州', '深圳', '成都', '杭州', '武汉', '西安', '南京', '重庆',
    '三里屯', '国贸', '望京', '朝阳', '海淀', '东城', '西城',
    # 中文菜系
    '川菜', '粤菜', '湘菜', '闽菜', '苏菜', '浙菜', '鲁菜', '徽菜',
    '火锅', '串串', '烤鸭', '小笼包', '大众点评',
    # 货币
    '人均', '¥',
]

OVERSEAS_CHINESE_SIGNALS = [
    # 海外华人聚集地
    'flushing', 'chinatown', 'monterey park', 'richmond', 'markham',
    'chatswood', 'box hill', 'cabramatta',
    # 英文但搜中餐
    'dim sum', 'hot pot', 'xiaolongbao', 'malatang', 'chuan', 'cantonese',
    # 小红书相关
    '小红书', '探店', '海外',
]

OVERSEAS_SIGNALS = [
    # 英文城市
    'new york', 'manhattan', 'brooklyn', 'los angeles', 'san francisco',
    'london', 'paris', 'tokyo', 'osaka', 'seoul', 'singapore', 'sydney',
    'toronto', 'vancouver', 'melbourne', 'bangkok',
    # 英文菜系
    'italian', 'french', 'japanese', 'korean', 'thai', 'mexican', 'indian',
    'sushi', 'ramen', 'pizza', 'burger', 'steak',
    # 货币
    '$', '€', '£', '¥ jpy',
]


def detect_locale(query: str, city: str = '', profile: dict = None) -> str:
    """
    自动推断用户 locale
    返回: 'china' | 'overseas-chinese' | 'overseas'
    """
    text = f"{query} {city}".lower()

    # 1. 先看 taste-profile 里有没有记录的 locale
    if profile and profile.get('user', {}).get('locale'):
        return profile['user']['locale']

    # 2. 看 profile 里的城市
    if profile:
        user_city = profile.get('user', {}).get('city', '')
        if user_city and any(s in user_city for s in ['北京', '上海', '广州', '深圳', '成都']):
            return 'china'

    # 3. 从 query 推断
    china_score = sum(1 for s in CHINA_SIGNALS if s.lower() in text)
    oc_score = sum(1 for s in OVERSEAS_CHINESE_SIGNALS if s.lower() in text)
    overseas_score = sum(1 for s in OVERSEAS_SIGNALS if s.lower() in text)

    # 中文字符比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    if chinese_chars > 3:
        china_score += 2

    if china_score >= 2:
        return 'china'
    if oc_score >= 1 or (chinese_chars > 0 and overseas_score >= 1):
        return 'overseas-chinese'
    if overseas_score >= 1:
        return 'overseas'

    # 默认：有中文就是中国
    return 'china' if chinese_chars > 0 else 'overseas'


# ── 匹配度计算 ────────────────────────────────────────────────

def match_score(restaurant: dict, preferences: dict, locale: str) -> float:
    if not preferences:
        return 50

    score = 50
    liked_tags = set(preferences.get('liked_tags', []))
    disliked_tags = set(preferences.get('disliked_tags', []))
    price_range = preferences.get('price_range', [])

    # 中国版：用 categories/tags
    if locale == 'china':
        restaurant_tags = set(restaurant.get('categories', []) + restaurant.get('tags', []))
    else:
        # 海外版：用 cuisines
        restaurant_tags = set(restaurant.get('cuisines', []))

    matched = liked_tags & restaurant_tags
    score += len(matched) * 5
    anti = disliked_tags & restaurant_tags
    score -= len(anti) * 10

    # 价格匹配
    price = restaurant.get('avg_price') or restaurant.get('price_level')
    if price and price_range and len(price_range) == 2:
        low, high = price_range
        if locale != 'china' and restaurant.get('price_level'):
            # 海外：price_level 1-4 映射到价格档
            pass
        else:
            margin = (high - low) * 0.3
            if low - margin <= price <= high + margin:
                score += 5

    # 交叉验证加分
    if restaurant.get('cross_verified'):
        score += 10
    if restaurant.get('reddit_mentioned'):
        score += 8  # Reddit 本地口碑
    if restaurant.get('xhs_verified'):
        score += 6  # 小红书华人验证

    # 小红书情感
    sentiment = restaurant.get('xhs_sentiment') or restaurant.get('reddit_sentiment')
    if sentiment == 'positive':
        score += 5
    elif sentiment == 'negative':
        score -= 8

    return min(max(score, 0), 100)


def select_2plus1(merged: list) -> tuple:
    precise = [r for r in merged if r.get('match_score', 50) >= 70 and r.get('cross_verified')]
    explorer = [r for r in merged if 60 <= r.get('match_score', 50) <= 75
                and (r.get('reddit_mentioned') or r.get('xhs_sentiment') == 'positive')]

    if len(precise) < 2:
        precise = sorted(merged, key=lambda x: x.get('match_score', 50), reverse=True)[:2]
    if not explorer:
        explorer = [r for r in merged if r.get('match_score', 50) >= 65][:1]

    return precise[:2], explorer[:1]


def load_profile() -> dict:
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(description='Nomtiq 小饭票 - 智能路由搜索')
    parser.add_argument('query', help='搜索关键词（中英文均可）')
    parser.add_argument('--city', default='', help='城市')
    parser.add_argument('--max', type=int, default=40, help='最大结果数')
    parser.add_argument('--locale', choices=['china', 'overseas-chinese', 'overseas', 'auto'],
                        default='auto', help='用户 locale（默认自动推断）')
    parser.add_argument('--mode', choices=['normal', '2plus1'], default='2plus1')
    parser.add_argument('--scene', default='', help='场景：birthday/ex/business/date/friends/solo')
    parser.add_argument('--people', type=int, default=2, help='人数')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    args = parser.parse_args()

    profile = load_profile()
    preferences = profile.get('preferences', {})

    # 场景 → 搜索词调整
    SCENE_QUERY_MAP = {
        'birthday':  '精致餐厅 特色',
        'ex':        '特色小馆 有调性',
        'business':  '商务餐厅 包间',
        'date':      '精致 有调性 安静',
        'friends':   '聚餐 特色',
        'solo':      '小馆 一人食',
    }
    SCENE_TONE = {
        'birthday': '环境本身就是礼物',
        'ex':       '好好吃顿饭，不用太多仪式感',
        'business': '',
        'date':     '',
        'friends':  '',
        'solo':     '',
    }
    scene = args.scene.lower()
    scene_query_suffix = SCENE_QUERY_MAP.get(scene, '')
    scene_tone = SCENE_TONE.get(scene, '')

    # 人数感知
    people = args.people
    if people >= 5:
        scene_query_suffix += ' 大桌 包间'

    # 推断 locale
    locale = args.locale if args.locale != 'auto' else detect_locale(args.query, args.city, profile)
    print(f"📍 Locale: {locale}", file=sys.stderr)

    # 按 locale 路由搜索
    if locale == 'china':
        print(f"🇨🇳 中国模式：高德/百度地图 → 大众点评/小红书补充", file=sys.stderr)

        # 从 query 里提取区域信息
        district = ''
        district_keywords = ['岳麓区', '朝阳区', '海淀区', '东城区', '西城区', '天心区',
                             '芙蓉区', '雨花区', '开福区', '望城区']
        for dk in district_keywords:
            if dk in args.query or dk in args.city:
                district = dk
                clean_city = args.city or ''.join(
                    c for c in args.query if '\u4e00' <= c <= '\u9fff' or c.isalpha()
                ).replace(dk, '').strip()
                break

        # 主数据源：高德地图（有 AMAP_KEY 就用，没有才降级）
        has_map_key = bool(os.environ.get('AMAP_KEY') or os.environ.get('BMAP_KEY'))
        if has_map_key:
            # 从 query 提取区域关键词
            district = ''
            district_patterns = ['酒仙桥', '三里屯', '望京', '国贸', '朝阳', '海淀',
                                  '亮马河', '798', '工体', '东直门', '西直门', '五道口',
                                  '岳麓区', '朝阳区', '海淀区', '东城区', '西城区']
            for dp in district_patterns:
                if dp in args.query:
                    district = dp
                    break
            map_query = re.sub(r'(酒仙桥|三里屯|望京|国贸|亮马河|798|工体)', '', args.query).strip()
            if scene_query_suffix:
                map_query = f"{map_query} {scene_query_suffix}".strip()
            merged = search_maps(map_query or args.query, args.city, district, mode='china', max_results=args.max)
            # 社交媒体交叉验证（top 5）
            merged = cross_verify_social(merged, max_verify=5)
        else:
            print(f"  ⚠️  未配置 AMAP_KEY，降级到大众点评搜索", file=sys.stderr)
            dp_results = search_dianping(args.query, args.city, max_results=args.max)
            merged = dp_results

        for r in merged:
            r['match_score'] = match_score(r, preferences, locale)

    elif locale == 'overseas-chinese':
        print(f"🌏 海外华人模式：Google Maps + 小红书", file=sys.stderr)
        merged = search_serper_maps(f"{args.query} restaurant", args.city, args.max)
        # 小红书补充
        xhs = search_xiaohongshu(f"{args.query} {args.city} 探店", max_results=10)
        for note in xhs:
            for mentioned in note.get('restaurants_mentioned', []):
                for r in merged:
                    if mentioned in r['name'] or r['name'] in mentioned:
                        r['xhs_verified'] = True
                        r['sources'].append('xiaohongshu')
        for r in merged:
            r['match_score'] = match_score(r, preferences, locale)

    else:  # overseas
        print(f"🌍 海外模式：Google Maps + Reddit", file=sys.stderr)
        merged = search_serper_maps(f"{args.query} restaurant", args.city, args.max)
        for r in merged:
            r['match_score'] = match_score(r, preferences, locale)

    merged.sort(key=lambda x: (x.get('cross_verified', False), x.get('match_score', 50)), reverse=True)

    if args.json:
        print(json.dumps(merged, ensure_ascii=False, indent=2))
        return

    if not merged:
        print("没有找到相关餐厅 / No restaurants found")
        return

    if args.mode == '2plus1':
        precise, explorer = select_2plus1(merged)
        _print_2plus1(precise, explorer, args.query, locale, preferences, scene_tone, people)
    else:
        _print_list(merged[:10], locale)


def _print_2plus1(precise, explorer, query, locale, preferences, scene_tone='', people=2):
    print(f"\n🎫 小饭票 2+1 推荐：{query}")
    if scene_tone:
        print(f"   {scene_tone}\n")
    elif preferences.get('liked_tags'):
        print(f"   (已根据你的口味画像筛选)\n")

    print("━━━ 精准推荐 ━━━\n")
    for i, r in enumerate(precise, 1):
        _print_one(i, r, locale, preferences=preferences)

    if explorer:
        print("\n━━━ 探索推荐 ━━━\n")
        _print_one(1, explorer[0], locale, is_explorer=True, preferences=preferences)

    if people >= 5:
        print("\n⚠️  5 个人以上建议提前打电话预约，别白跑一趟。")


def _print_list(results, locale):
    for i, r in enumerate(results, 1):
        _print_one(i, r, locale)


def _generate_personal_blurb(r: dict, preferences: dict) -> str:
    """根据口味画像生成个性化推荐语（普通模式专用）"""
    liked_tags = set(preferences.get('liked_tags', []))
    disliked_tags = set(preferences.get('disliked_tags', []))
    price_range = preferences.get('price_range', [])

    name = r.get('name', '')
    type_label = r.get('type', '')
    cuisines = set(r.get('cuisines', []) + [type_label])
    address = r.get('address', '') or ''
    price = r.get('avg_price', 0) or 0
    score = r.get('score', 0) or 0

    parts = []

    # 口味匹配 — 说"为什么适合你"
    taste_hints = {
        '云南菜': '你喜欢香料，这家云南菜对你路子',
        '潮汕': '潮汕菜讲究食材本味，你应该会喜欢',
        '粤菜': '粤菜讲究食材，符合你的口味',
        '日料': '日料，你喜欢的方向',
        '私房菜': '私房菜，不是连锁，有自己的风格',
        '精致小馆': '精致小馆，你喜欢的那种',
        'Bistro': 'Bistro 风格，你喜欢的调性',
        '有调性': '环境有调性，你应该会喜欢',
    }
    for tag, hint in taste_hints.items():
        if tag in liked_tags and tag in cuisines:
            parts.append(hint)
            break

    # 不喜欢的标签 — 主动说"不是那种"
    if '连锁' in disliked_tags and any(kw in name for kw in ['老店', '创始', '本店']):
        parts.append('本地老店，不是连锁')

    # 小红书口碑
    if r.get('xhs_verified'):
        if r.get('xhs_sentiment') == 'negative':
            parts.append('留个心眼，有差评')
        else:
            parts.append('小红书有探店，本地人去过')

    # 价格匹配
    if price and price_range and len(price_range) == 2:
        low, high = price_range
        if low <= price <= high:
            parts.append(f'人均 ¥{price}，在你的预算里')
        elif price > high * 1.3:
            parts.append(f'人均 ¥{price}，稍微贵一点，但值得')

    # 高分背书（没有其他内容时）
    if not parts and score >= 4.7:
        parts.append(f'4.7 分，口碑在那里')

    return '。'.join(parts[:2]) + '。' if parts else ''


def _print_one(index, r, locale, is_explorer=False, preferences=None):
    name = r['name']
    prefix = "🎁 " if is_explorer else ""

    if locale == 'china':
        price = f"¥{r['avg_price']}" if r.get('avg_price') else ''
        score = f"⭐{r['score']}" if r.get('score') else ''
    else:
        price = '$' * r['price_level'] if r.get('price_level') else ''
        score = f"⭐{r['score']}" if r.get('score') else ''

    info = ' | '.join(p for p in [price, score] if p)
    print(f"{prefix}{index}. {name}")
    if info:
        print(f"   {info}")

    # 个性化推荐语
    blurb = r.get('blurb', '')
    if not blurb and preferences:
        blurb = _generate_personal_blurb(r, preferences)
    if blurb:
        print(f"   {blurb}")

    if r.get('address'):
        print(f"   📍 {r['address'][:55]}")
    print()


if __name__ == '__main__':
    main()
