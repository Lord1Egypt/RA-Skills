#!/usr/bin/env python3
"""
小饭卡 - 大众点评搜索（使用 search-hub）
用法:
  python3 search.py "三里屯 创意菜"
  python3 search.py "国贸 日料 人均 500" --city 北京
  python3 search.py "朝阳 素食" --max 50 --json
"""

import sys
import json
import argparse
import re
import os
import subprocess

def search_dianping(query: str, city: str = '', max_results: int = 50) -> list:
    """搜索大众点评上的餐厅信息（使用 search-hub）
    
    Args:
        query: 搜索关键词
        city: 城市名
        max_results: 最大结果数（默认 50 家）
    """
    city_str = f' {city}' if city else ''
    search_query = f'site:dianping.com {query}{city_str} 餐厅'
    
    try:
        # 调用 search-hub（用 python3.13 避免版本问题）
        result = subprocess.run(
            ['python3.13', 'skills/search-hub/scripts/hub.py', 'search', search_query, '-t', 'text', '-l', str(max_results)],
            cwd='/Users/mac/.openclaw/workspace',
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"search-hub 出错：{result.stderr}", file=sys.stderr)
            return []
        
        # 解析 JSON 输出
        data = json.loads(result.stdout)
        results = data.get('results', [])
        
        # 解析餐厅信息
        restaurants = []
        for r in results:
            parsed = parse_result(r)
            if parsed:
                restaurants.append(parsed)
        
        return restaurants
        
    except Exception as e:
        print(f"搜索出错：{e}", file=sys.stderr)
        return []


def parse_result(result):
    """从搜索结果中解析餐厅信息"""
    title = result.get('title', '')
    snippet = result.get('snippet', '')
    url = result.get('url', '') or result.get('link', '')
    combined = f"{title} {snippet}"

    # 过滤非大众点评链接
    if 'dianping.com' not in url:
        return None

    # 判断是否餐厅相关
    food_keywords = ['餐厅', '餐馆', '饭店', '菜', '人均', '推荐菜', '好吃', '味道', '料理', '火锅', '烤', '店', '馆']
    if not any(kw in combined for kw in food_keywords):
        return None

    # 过滤非餐厅页面
    skip_patterns = ['shopRank', 'pcChannelRanking', '/photos', '/album']
    if any(p in url for p in skip_patterns):
        return None

    non_food = ['按摩', '足浴', '养生馆', '美容', '美发', '酒店', 'KTV', '健身']
    if any(nf in combined for nf in non_food) and not any(kw in combined for kw in food_keywords[:6]):
        return None

    # 提取人均
    price_match = re.search(r'[人均¥￥](\d+)', combined)
    avg_price = int(price_match.group(1)) if price_match else None

    # 提取店名
    shop_name = None
    name_match = re.search(r'【(.+?)】', title)
    if name_match:
        shop_name = name_match.group(1)
    elif '(' in title and '大众点评' not in title:
        shop_name = title.split(' - ')[0].split('|')[0].strip()

    # 提取评分
    score_match = re.search(r'(\d\.\d)\s*分', combined)
    score = float(score_match.group(1)) if score_match else None

    # 提取菜系
    categories = []
    cat_keywords = {
        '中餐': ['中餐', '京菜', '鲁菜', '川菜', '粤菜', '湘菜', '浙菜', '苏菜', '徽菜', '闽菜'],
        '日料': ['日本料理', '日料', '寿司', '刺身', '居酒屋', 'omakase'],
        '西餐': ['西餐', '法餐', '意大利', '西班牙', '牛排'],
        '火锅': ['火锅', '涮肉', '涮锅'],
        '烧烤': ['烤肉', '烧烤', '炙子'],
        '潮汕菜': ['潮汕', '砂锅粥', '牛肉火锅'],
        '海鲜': ['海鲜', '水产', '蟹', '虾', '贝'],
    }
    for cat, kws in cat_keywords.items():
        if any(kw in combined for kw in kws):
            categories.append(cat)

    # 提取区域
    area = None
    area_keywords = ['朝阳区', '海淀区', '东城区', '西城区', '丰台区', '石景山区', '三里屯', '国贸', '中关村']
    for area_kw in area_keywords:
        if area_kw in combined:
            area = area_kw
            break

    return {
        'name': shop_name or title[:30],
        'avg_price': avg_price,
        'score': score,
        'categories': categories,
        'area': area,
        'snippet': snippet[:200],
        'url': url,
        'source': 'dianping',
        'is_shop_page': '/shop/' in url,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='小饭卡 - 大众点评搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--city', default='', help='城市')
    parser.add_argument('--max', type=int, default=50, help='最大结果数')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    args = parser.parse_args()

    results = search_dianping(args.query, args.city, max_results=args.max)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"📊 找到 {len(results)} 家餐厅\n")
        for i, r in enumerate(results[:10], 1):
            price = f"¥{r['avg_price']}" if r.get('avg_price') else ''
            score = f"⭐{r['score']}" if r.get('score') else ''
            cats = '/'.join(r.get('categories', []))
            print(f"{i}. {r['name']}")
            if price or score or cats:
                print(f"   {' | '.join(p for p in [price, score, cats] if p)}")
            print()
