#!/usr/bin/env python3
"""
Amap POI Provider - 高德地图POI搜索
使用 typecode 精确搜索，替代模糊的关键词搜索
"""
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

# POI Typecode Mapping - 高德地图POI分类编码
# 一级大类共 20 个（6位宽码 = XX0000）:
#   01=汽车服务  02=汽车销售  03=汽车维修  04=摩托车服务
#   05=餐饮服务  06=购物服务  07=生活服务  08=体育休闲服务
#   09=医疗保健  10=住宿服务  11=风景名胜    12=商务住宅
#   13=政府机构  14=科教文化  15=交通设施    16=金融保险
#   17=公司企业  18=道路附属  19=地名地址    20=公共设施
# 参考: https://lbs.amap.com/api/webservice/download
TYPECODE_MAP = {
    # ── 05 餐饮服务 ──
    "奶茶": "050407",
    "果汁": "050408",
    "酸奶": "050400|050407|050408|050409",
    "饮品": "050400|050407|050408",
    "甜品": "050409",
    "冷饮": "050400",
    "咖啡": "050405",
    "茶": "050406",
    "面包": "050201",
    "蛋糕": "050202",
    "火锅": "050000",
    "烧烤": "050000",
    "小吃": "050000",
    "快餐": "050000",
    "日料": "050000",
    "韩料": "050000",
    "西餐": "050000",
    "中餐": "050000",
    "川菜": "050000",
    "粤菜": "050000",
    "自助餐": "050000",
    "面馆": "050000",
    "粉店": "050000",
    "麻辣烫": "050000",
    "炸鸡": "050000",
    "披萨": "050000",
    "寿司": "050000",
    "冰淇淋": "050400",
    # ── 06 购物服务 ──
    "便利店": "060200",
    "超市": "060100|060400",
    "商场": "060101",
    "购物中心": "060101",
    "菜市场": "060000",
    "水果店": "060000",
    "花店": "060000",
    "书店": "060000",
    "文具店": "060000",
    "服装店": "060000",
    "数码": "060000",
    "家电": "060000",
    # ── 07 生活服务 ──
    "理发": "070000",
    "美发": "070000",
    "美容": "070000",
    "美甲": "070000",
    "洗衣": "070000",
    "干洗": "070000",
    "快递": "070000",
    "宠物": "070000",
    "宠物店": "070000",
    "摄影": "070000",
    "照相": "070000",
    "维修": "070000",
    "家政": "070000",
    "中介": "070000",
    "装修": "070000",
    "配钥匙": "070000",
    "皮具护理": "070000",
    "修鞋": "070000",
    "裁缝": "070000",
    "修理": "070000",
    "书包": "070000",
    "拉链": "070000",
    # ── 08 体育休闲 ──
    "网吧": "080000",
    "电竞": "080000",
    "网咖": "080000",
    "KTV": "080000",
    "电影院": "080000",
    "健身房": "080000",
    "台球": "080000",
    "酒吧": "080000",
    "游乐场": "080000",
    "游戏厅": "080000",
    "游泳": "080000",
    "滑雪": "080000",
    "棋牌": "080000",
    "桌游": "080000",
    "剧本杀": "080000",
    "密室": "080000",
    "密室逃脱": "080000",
    "温泉": "080000",
    "足浴": "080000",
    "按摩": "080000",
    "桑拿": "080000",
    "射箭": "080000",
    "蹦床": "080000",
    "卡丁车": "080000",
    "篮球": "080000",
    "羽毛球": "080000",
    "保龄球": "080000",
    # ── 09 医疗保健 ──
    "医院": "090000",
    "诊所": "090000",
    "药店": "090000",
    "药房": "090000",
    "牙科": "090000",
    "口腔": "090000",
    "体检": "090000",
    "眼科": "090000",
    "中医": "090000",
    # ── 10 住宿服务 ──
    "酒店": "100000",
    "宾馆": "100000",
    "民宿": "100000",
    "青旅": "100000",
    "旅馆": "100000",
    "招待所": "100000",
    # ── 11 风景名胜 ──
    "景区": "110000",
    "公园": "110000",
    "动物园": "110000",
    "植物园": "110000",
    "水族馆": "110000",
    "寺庙": "110000",
    "教堂": "110000",
    "古镇": "110000",
    "海滩": "110000",
    "登山": "110000",
    "游乐园": "080000",  # 游乐场归属体育休闲
    # ── 12 商务住宅 ──
    "写字楼": "120000",
    "商务中心": "120000",
    "小区": "120000",
    # ── 13 政府机构 ──
    "派出所": "130000",
    "公安局": "130000",
    "政务中心": "130000",
    "税务局": "130000",
    # ── 14 科教文化 ──
    "学校": "140000",
    "大学": "140000",
    "中学": "140000",
    "小学": "140000",
    "幼儿园": "140000",
    "图书馆": "140000",
    "培训": "140000",
    "驾校": "140000",
    "博物馆": "140000",
    "美术馆": "140000",
    "科技馆": "140000",
    "少年宫": "140000",
    # ── 15 交通设施 ──
    "地铁站": "150000",
    "公交站": "150000",
    "停车场": "150000",
    "加油站": "150000",
    "充电站": "150000",
    "充电桩": "150000",
    "火车站": "150000",
    "机场": "150000",
    # ── 16 金融保险 ──
    "银行": "160000",
    "ATM": "160000",
    "保险公司": "160000",
    # ── 17 公司企业 ── (太宽泛, 只加常见厂区/园区)
    "产业园": "170000",
    "工业园": "170000",
    # ── 18 道路附属 ──
    "服务区": "180000",
    "收费站": "180000",
    # ── 20 公共设施 ──
    "公厕": "200000",
    "公共厕所": "200000",
    "卫生间": "200000",
}

DEFAULT_TYPECODES = "050000"  # 默认: 餐饮大类

API_URL = "https://restapi.amap.com/v3/place/around"


def _load_key():
    """Load Amap key from environment (set by providers.py from .env.local)"""
    import os
    return os.getenv("AMAP_KEY", "")


def translate_category(category: str) -> str:
    """
    将中文类别映射为 Amap typecode
    如果找不到精确匹配，返回默认餐饮类
    """
    category = category.strip()
    
    # 直接匹配
    if category in TYPECODE_MAP:
        return TYPECODE_MAP[category]
    
    # 包含匹配
    for key, typecode in TYPECODE_MAP.items():
        if key in category or category in key:
            return typecode
    
    # 特殊处理（使用多字关键词避免单一字符误匹配，如"水族馆"不会误判为饮品）
    if any(kw in category for kw in ["奶茶", "饮品", "酸奶", "冷饮", "热饮", "咖啡", "水吧", "冰品", "果汁", "果茶", "冰沙", "冰淇淋"]):
        return TYPECODE_MAP.get("饮品", DEFAULT_TYPECODES)
    if any(kw in category for kw in ["甜品", "蛋糕", "甜点", "烘焙", "面包", "糕点"]):
        return TYPECODE_MAP.get("甜品", DEFAULT_TYPECODES)
    
    return None  # Unrecognized: caller uses keywords-only search (no typecode restriction)


def search_by_keywords(keywords: str, center_lng: float, center_lat: float, radius: int = 3000, limit: int = 25) -> List[Dict]:
    """
    向后兼容的接口，供 providers.py 调用
    将 keywords 转换为 typecode 后搜索
    """
    return search(center_lat, center_lng, radius, keywords)[:limit]


def search(lat: float, lon: float, radius: int = 3000, keyword: str = "") -> List[Dict]:
    """
    搜索附近POI (使用组合查询：typecode + keywords 同时传，服务端过滤)
    
    Args:
        lat: 纬度
        lon: 经度  
        radius: 搜索半径(米)
        keyword: 搜索关键词/类别 (同时用于typecode映射和keywords参数)
    
    Returns:
        List of POI dicts
    """
    key = _load_key()
    if not key or "YOUR_AMAP_KEY" in key:
        return []
    
    if keyword:
        # 纯关键词搜索 — 不传 typecode。
        # typecode 过于粗糙（如 080000 把酒吧+网吧+KTV+影吧混在一起），
        # 会污染关键词精度（搜"酒吧"混入网吧）。关键词本身信号足够。
        return _search_with_typecode(lat, lon, radius, None, keywords=keyword)
    
    # 无关键词 → 用默认 typecode 做宽泛搜索
    results = _search_with_typecode(lat, lon, radius, DEFAULT_TYPECODES)
    if not results:
        results = _search_with_typecode(lat, lon, radius, "050000")
    return results



def _search_with_typecode(lat: float, lon: float, radius: int, typecode: Optional[str] = None, keywords: str = "") -> List[Dict]:
    """
    底层API调用：使用指定typecode搜索，支持同时传入keywords进行服务端过滤
    
    组合查询优势：
    - keywords和types同时作用，Amap服务端进行AND逻辑过滤
    - 比本地过滤更智能，支持品牌名匹配（如"益禾堂"）
    - 减少API调用次数
    """
    key = _load_key()
    if not key:
        return []
    
    params = {
        "key": key,
        "location": f"{lon},{lat}",
        "radius": radius,
        "offset": 25,
        "page": 1,
        "output": "json",
    }
    
    if typecode:
        params["types"] = typecode
    
    # 组合查询：同时传入keywords，让服务端完成过滤
    if keywords:
        params["keywords"] = keywords
    
    query_string = urllib.parse.urlencode(params)
    url = f"{API_URL}?{query_string}"
    
    ctx = ssl.create_default_context()
    
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
            
            if data.get("status") != "1":
                error_info = data.get("info", "Unknown error")
                print(f"Amap POI API error: {error_info}")
                return []
            
            pois = data.get("pois", [])
            if not pois:
                return []
            
            results = []
            for poi in pois:
                try:
                    location = poi.get("location", "").split(",")
                    if len(location) != 2:
                        continue
                    
                    poi_lon, poi_lat = float(location[0]), float(location[1])
                    
                    results.append({
                        "name": poi.get("name", ""),
                        "lat": poi_lat,
                        "lon": poi_lon,
                        "address": poi.get("address", ""),
                        "type": poi.get("type", ""),
                        "typecode": poi.get("typecode", ""),
                        "distance": int(poi.get("distance", 0)),
                        "tel": poi.get("tel", ""),
                        "pcode": poi.get("pcode", ""),
                        "citycode": poi.get("citycode", ""),
                        "adcode": poi.get("adcode", ""),
                    })
                except (ValueError, TypeError) as e:
                    print(f"Parse POI error: {e}")
                    continue
            
            return results
            
    except urllib.error.URLError as e:
        print(f"Request failed: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def test_search():
    """Test function"""
    # 天津财经大学坐标
    test_cases = [
        (39.0639, 117.2769, "酸奶"),
        (39.0639, 117.2769, "奶茶"),
        (39.0639, 117.2769, "咖啡"),
        (39.0639, 117.2769, "益禾堂"),  # 测试品牌名搜索
        (39.0639, 117.2769, "茶百道"),  # 测试品牌名搜索
    ]
    
    for lat, lon, keyword in test_cases:
        print(f"\n搜索: {keyword} 附近")
        results = search(lat, lon, radius=5000, keyword=keyword)
        print(f"找到 {len(results)} 个结果")
        for i, r in enumerate(results[:3]):
            print(f"  {i+1}. {r['name']} ({r['type']}) - {r['distance']}m")


if __name__ == "__main__":
    test_search()
