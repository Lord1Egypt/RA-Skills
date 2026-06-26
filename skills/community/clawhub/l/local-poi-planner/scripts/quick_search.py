#!/usr/bin/env python3
"""Quick search: CoreLocation + Amap POI, no unified-search."""
import sys, os, json, re, time
from types import SimpleNamespace

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from providers import search_pois
from planner import (
    parse_request, _llm_extract_amap_terms, normalize_category,
)

query = "我附近的修理书包"
args = SimpleNamespace(query=query, origin=None, category=None, 
                       mode=None, preferences="", constraints="", avoid="")

print("🔍 解析请求...")
req = parse_request(args)

print("🧠 LLM 提取类别...")
llm_raw = _llm_extract_amap_terms(query)
# Grok is verbose - extract first line of comma-separated terms
llm_terms = None
if llm_raw:
    first_line = llm_raw.split("\n")[0].strip()
    # strip markdown bold markers
    first_line = first_line.replace("**", "").replace("*", "")
    # remove common verbose prefixes
    for prefix in ["The terms are:", "Terms:", "Answer:", "Reply:"]:
        if first_line.lower().startswith(prefix.lower()):
            first_line = first_line[len(prefix):].strip()
    # extract comma-separated terms
    m = re.match(r"^[\u4e00-\u9fff\w]+(?:,[\u4e00-\u9fff\w]+)*", first_line)
    if m:
        llm_terms = m.group(0)

print(f"   LLM原始: {llm_raw[:100]}...")
print(f"   解析后: {llm_terms}")

if llm_terms:
    best_term = llm_terms.split(",")[0].strip()
    req["category"] = normalize_category(best_term)
    print(f"   category: {req['category']}")
else:
    print(f"   ❌ 解析失败，fallback: {req.get('category')}")

origin = req.get("origin", "未指定起点")
loc = req.get("ip_location", {})
print(f"   origin: {origin}")
print(f"   坐标: {loc.get('lat')}, {loc.get('lon')} ({loc.get('accuracy')}/{loc.get('provider')})")

print("\n📍 搜索POI（3000m）...")
t0 = time.time()
poi_result = search_pois(
    req, origin, radius_m=3000, limit=8,
    enable_accessibility=True, ip_location=loc,
)
elapsed = time.time() - t0

results = poi_result.get("results", []) if isinstance(poi_result, dict) else []
provider = poi_result.get("provider", "unknown") if isinstance(poi_result, dict) else "unknown"
error = poi_result.get("error", None) if isinstance(poi_result, dict) else None

print(f"   provider: {provider}")
print(f"   找到 {len(results)} 条候选（{elapsed:.0f}s）")

if error:
    print(f"   ⚠️ error: {error}")

if results:
    print("\n" + "=" * 60)
    for i, r in enumerate(results[:5]):
        if isinstance(r, dict):
            print(f"\n📍 #{i+1} {r.get('name', 'N/A')}")
            print(f"   地址: {r.get('address', 'N/A')}")
            dist = r.get('distance', '')
            if dist:
                try:
                    dist_m = int(dist)
                    if dist_m >= 1000:
                        print(f"   距离: 约{dist_m/1000:.1f}km")
                    else:
                        print(f"   距离: {dist}m")
                except:
                    print(f"   距离: {dist}")
            if r.get('_base_score'):
                print(f"   基础分: {r['_base_score']}")
            acc = r.get('accessibility', {})
            if isinstance(acc, dict) and acc:
                metro = acc.get('nearest_metro_station', '')
                if metro:
                    print(f"   最近地铁: {metro}")
                walk = acc.get('walking_time_min', '')
                if walk:
                    print(f"   步行时间: {walk}min")
        else:
            print(f"\n📍 #{i+1} {r}")
    print("\n" + "=" * 60)
else:
    print("❌ 无结果")
