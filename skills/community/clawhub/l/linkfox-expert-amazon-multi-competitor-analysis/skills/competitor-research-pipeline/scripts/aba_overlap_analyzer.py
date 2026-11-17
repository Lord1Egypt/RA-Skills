#!/usr/bin/env python3
"""
ABA Overlap Analyzer - ABA TOP3 交叉对比分析
分析多个ASIN的ABA上榜词数据，找出交叉战场和独占词

Usage:
  python aba_overlap_analyzer.py --stdin < params.json

Input:
{
  "asins": ["B0DFCLRVPP", "B0DK8HFY4Y", ...],
  "labels": {"B0DFCLRVPP": "目标", ...},
  "aba_data": {
    "B0DFCLRVPP": [{"keyword":"mp3 player","rank":"2","click_share":"0.0715","conv_share":"0.0262"}, ...],
    "B0DK8HFY4Y": [{"keyword":"mp3 player","rank":"3","click_share":"0.0476","conv_share":"0.0"}, ...]
  }
}

Output:
{
  "per_asin": {asin: {aba_total, rank1, rank2, rank3, unique_kws}},
  "cross_battlefields": [{keyword, asins: [{asin, rank, click_share, conv_share}]}],
  "summary": {total_unique_kws, total_cross_kws}
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
    aba_data = data["aba_data"]

    # Build keyword -> ASIN map
    keyword_asin_map = defaultdict(list)
    per_asin = {asin: {"aba_total": 0, "rank1": 0, "rank2": 0, "rank3": 0, "unique_kws": 0} for asin in asins}

    for asin in asins:
        for kw in aba_data.get(asin, []):
            keyword = kw.get("searchterm") or kw.get("keyword") or ""
            rank_str = str(kw.get("clicksharerank") or kw.get("clickShareRank") or "0")
            rank = int(rank_str) if rank_str.isdigit() else 0
            click = float(kw.get("clickshare") or kw.get("clickShare") or 0)
            conv = float(kw.get("conversionshare") or kw.get("conversionShare") or 0)

            if not keyword or rank == 0:
                continue

            keyword_asin_map[keyword].append({
                "asin": asin,
                "rank": rank,
                "click_share": click,
                "conv_share": conv
            })

            per_asin[asin]["aba_total"] += 1
            if rank == 1: per_asin[asin]["rank1"] += 1
            elif rank == 2: per_asin[asin]["rank2"] += 1
            elif rank == 3: per_asin[asin]["rank3"] += 1

    # Find cross battlefields and unique keywords
    cross_battlefields = []
    for keyword, asin_list in keyword_asin_map.items():
        if len(asin_list) > 1:
            cross_battlefields.append({
                "keyword": keyword,
                "asins": [{"asin": e["asin"], "label": labels.get(e["asin"], e["asin"]),
                           "rank": e["rank"], "click_share": e["click_share"],
                           "conv_share": e["conv_share"]} for e in asin_list]
            })
        else:
            asin = asin_list[0]["asin"]
            per_asin[asin]["unique_kws"] += 1

    # Sort cross battlefields by number of ASINs (desc) then by max click share (desc)
    cross_battlefields.sort(key=lambda x: (-len(x["asins"]), -max(e["click_share"] for e in x["asins"])))

    # Add labels
    for asin in per_asin:
        per_asin[asin]["label"] = labels.get(asin, asin)

    output = {
        "per_asin": per_asin,
        "cross_battlefields": cross_battlefields[:30],
        "summary": {
            "total_unique_kws": sum(1 for v in keyword_asin_map.values() if len(v) == 1),
            "total_cross_kws": sum(1 for v in keyword_asin_map.values() if len(v) > 1)
        }
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
