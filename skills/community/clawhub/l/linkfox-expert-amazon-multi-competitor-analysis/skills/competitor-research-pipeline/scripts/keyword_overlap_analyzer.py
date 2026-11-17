#!/usr/bin/env python3
"""
Keyword Overlap Analyzer - 首页词归因分析
分析多个ASIN的卖家精灵流量词数据，区分唯一首页词和重复首页词

Usage:
  python keyword_overlap_analyzer.py --stdin < params.json
  python keyword_overlap_analyzer.py '<json params>'

Input:
{
  "asins": ["B0DFCLRVPP", "B0DK8HFY4Y", ...],
  "labels": {"B0DFCLRVPP": "目标", "B0DK8HFY4Y": "直接竞品", ...},
  "keywords_data": {
    "B0DFCLRVPP": [{"keyword":"mp3 player","page":1,"position":4,"traffic_pct":30.0,"searches":227321}, ...],
    "B0DK8HFY4Y": [{"keyword":"mp3 player","page":1,"position":9,"traffic_pct":40.0,"searches":227321}, ...]
  }
}

Output:
{
  "per_asin": {asin: {total_p1, unique_p1, shared_p1, unique_vol, unique_pct}},
  "battlefields": [{keyword, searches, asins_on_p1: [{asin, position, traffic_pct}]}],
  "summary": {total_kws, unique_kws, shared_kws}
}
"""

import json
import sys
from collections import defaultdict

def main():
    if "--stdin" in sys.argv:
        data = json.load(sys.stdin)
    else:
        data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)

    asins = data["asins"]
    labels = data.get("labels", {})
    keywords_data = data["keywords_data"]

    # Build keyword -> ASIN map (only page 1)
    keyword_asin_map = defaultdict(list)  # keyword -> [{asin, position, traffic_pct, searches}]

    for asin in asins:
        for kw in keywords_data.get(asin, []):
            keyword = kw.get("keyword", "")
            page = kw.get("page", 0)
            if page == 1:
                keyword_asin_map[keyword].append({
                    "asin": asin,
                    "position": kw.get("position", 0),
                    "traffic_pct": kw.get("traffic_pct", 0),
                    "searches": kw.get("searches", 0)
                })

    # Classify keywords
    per_asin = {asin: {"total_p1": 0, "unique_p1": 0, "shared_p1": 0, "unique_vol": 0, "shared_vol": 0} for asin in asins}
    battlefields = []

    for keyword, asin_list in keyword_asin_map.items():
        is_shared = len(asin_list) > 1
        searches = asin_list[0]["searches"] if asin_list else 0

        for entry in asin_list:
            asin = entry["asin"]
            per_asin[asin]["total_p1"] += 1
            if is_shared:
                per_asin[asin]["shared_p1"] += 1
                per_asin[asin]["shared_vol"] += searches
            else:
                per_asin[asin]["unique_p1"] += 1
                per_asin[asin]["unique_vol"] += searches

        if is_shared:
            battlefields.append({
                "keyword": keyword,
                "searches": searches,
                "asins_on_p1": [{"asin": e["asin"], "label": labels.get(e["asin"], e["asin"]),
                                  "position": e["position"], "traffic_pct": e["traffic_pct"]} for e in asin_list]
            })

    # Calculate unique percentage
    for asin in per_asin:
        total_vol = per_asin[asin]["unique_vol"] + per_asin[asin]["shared_vol"]
        per_asin[asin]["unique_pct"] = round(per_asin[asin]["unique_vol"] / total_vol * 100, 1) if total_vol > 0 else 0

    # Sort battlefields by search volume
    battlefields.sort(key=lambda x: -x["searches"])

    # Add labels to per_asin
    for asin in per_asin:
        per_asin[asin]["label"] = labels.get(asin, asin)

    output = {
        "per_asin": per_asin,
        "battlefields": battlefields[:30],  # Top 30 battlefields
        "summary": {
            "total_kws": len(keyword_asin_map),
            "unique_kws": sum(1 for v in keyword_asin_map.values() if len(v) == 1),
            "shared_kws": sum(1 for v in keyword_asin_map.values() if len(v) > 1)
        }
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
