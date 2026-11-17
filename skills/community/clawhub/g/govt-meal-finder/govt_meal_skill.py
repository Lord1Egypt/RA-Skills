#!/usr/bin/env python3
"""
政府认证养老助餐点查询 Skill
支持城市：北京、广州、深圳（共约 4,253 条）
调用：python3 govt_meal_skill.py --city 北京 --place 天安门 --radius 1000
"""
import sys
import os
import json
import urllib.request
import urllib.parse
import argparse
import re

GAODE_BASE = os.environ.get("GAODE_POI_BASE", "").rstrip("/")
GAODE_KEY  = os.environ.get("GAODE_POI_KEY", "")

SUPPORTED_CITIES = {"北京", "广州", "深圳"}

# 深圳店名常见噪声字符（引号、换行、多余空白）
def clean_name(name: str) -> str:
    if not name:
        return name
    # 去掉全角/半角引号、换行、多余空白
    name = re.sub('[“”‘’＂＇「」]', '', name)
    name = re.sub(r'[\r\n\t]+', ' ', name)
    name = re.sub(r'\s{2,}', ' ', name).strip()
    return name

def gaode_get(path: str, params: dict) -> dict:
    if not GAODE_KEY:
        sys.stderr.write("缺少环境变量 GAODE_POI_KEY\n")
        sys.exit(1)
    url = f"{GAODE_BASE}{path}?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    req = urllib.request.Request(url, headers={
        "X-API-Key": GAODE_KEY,
        "User-Agent": "govt-meal-skill/1.0.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.stderr.write(f"API 错误 {e.code}: {body}\n")
        sys.exit(1)

def resolve_location(city: str, place: str) -> tuple[float, float, str]:
    """用 /search 把地名解析成坐标，返回 (lng, lat, 规范名称)"""
    data = gaode_get("/search", {"q": place, "city": city, "page_size": 1})
    items = data.get("items") or data.get("results", [])
    if not items:
        sys.stderr.write(f"找不到地名：{place}（{city}）\n")
        sys.exit(1)
    r = items[0]
    lng = r.get("lng") or r.get("location", "").split(",")[0]
    lat = r.get("lat") or (r.get("location", "").split(",")[1] if "," in r.get("location","") else "")
    if not lng or not lat:
        sys.stderr.write(f"地名解析无坐标：{r}\n")
        sys.exit(1)
    return float(lng), float(lat), r.get("name", place)


def query_govt_meal(lng: float, lat: float, radius: int, top: int) -> list[dict]:
    """查询附近政府认证助餐点，返回按距离排序的去重列表"""
    data = gaode_get("/nearby", {
        "lng": lng,
        "lat": lat,
        "radius": radius,
        "page_size": min(top * 2, 20),  # 多取一倍，去重后再截断
        "govt_only": "true",
    })
    items = data.get("items") or data.get("results", [])
    # 按名称去重（深圳存在同名+相似地址的重复条目），保留首次出现（距离最近）
    seen, deduped = set(), []
    for item in items:
        key = clean_name(item.get("name", ""))
        if key not in seen:
            seen.add(key)
            deduped.append(item)
        if len(deduped) >= top:
            break
    return deduped


def format_output(anchor_name: str, city: str, radius: int, results: list[dict]) -> str:
    if not results:
        return (
            f"# {city} · {anchor_name} 附近 {radius}m 内暂无政府认证助餐点\n\n"
            f"> 目前覆盖城市：北京、广州、深圳。其他城市暂不支持。\n\n"
            f"⚠️ **使用提醒**\n"
            f"- 数据来源：政府公开名录，实际开放情况请致电确认\n"
            f"- 部分助餐点仅限本街道户籍老人\n"
            f"- 距离为直线距离，实际步行可能更远\n"
        )

    lines = [
        f"# {city} · {anchor_name} 附近 {radius}m 内政府认证助餐点",
        f"\n共找到 **{len(results)}** 处（按直线距离排序）\n",
    ]

    for i, r in enumerate(results, 1):
        name = clean_name(r.get("name", "—"))
        address = clean_name(r.get("address", ""))
        phone = r.get("tel") or r.get("phone") or ""
        dist = r.get("distance", "")
        district = r.get("adname", "") or r.get("district", "")

        lines.append(f"## {i}. {name}")
        if district:
            lines.append(f"- 所属区：{district}")
        if address:
            lines.append(f"- 地址：{address}")
        if dist:
            lines.append(f"- 直线距离：约 {dist}m")
        if phone:
            lines.append(f"- 电话：{phone}")
        lines.append("")

    lines += [
        "---",
        "⚠️ **使用提醒**",
        "- 距离为直线距离，实际步行路程可能更远",
        "- 开放时间、剩余名额请致电确认，部分节假日停餐",
        "- 部分助餐点仅限本街道户籍老人，请现场核实资格",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="政府认证养老助餐点查询")
    parser.add_argument("--city",   required=True, help="城市，如 北京")
    parser.add_argument("--place",  required=True, help="参考地点，如 天安门、回龙观地铁站")
    parser.add_argument("--radius", type=int, default=1000, help="查询半径（米），默认 1000")
    parser.add_argument("--top",    type=int, default=5,    help="返回条数，默认 5，最多 20")
    parser.add_argument("--json",   action="store_true",    help="输出原始 JSON（调试用）")
    args = parser.parse_args()

    if not GAODE_KEY:
        sys.stderr.write("缺少环境变量 GAODE_POI_KEY\n")
        sys.exit(1)

    if args.city not in SUPPORTED_CITIES:
        print(f"⚠️ 暂不支持城市「{args.city}」，当前覆盖：北京、广州、深圳。")
        sys.exit(0)

    lng, lat, anchor_name = resolve_location(args.city, args.place)
    results = query_govt_meal(lng, lat, args.radius, args.top)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(anchor_name, args.city, args.radius, results))


if __name__ == "__main__":
    main()
