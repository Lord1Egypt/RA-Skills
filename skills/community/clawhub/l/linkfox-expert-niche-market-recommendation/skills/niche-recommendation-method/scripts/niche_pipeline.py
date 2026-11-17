#!/usr/bin/env python3
"""
Niche Recommendation Pipeline - S1(filter) + S2(score) + S3(output)

Usage:
  python niche_pipeline.py --input <jiimore_niches.json> [--profile novice] [--sort-by score]
"""
import argparse
import json
import math
import os
import sys
import time
from collections import Counter

PROFILES = {
    "novice": {
        "minSearchVolume": 2000, "monopolyThreshold": 0.50, "minBrands": 10,
        "maxDeclineRate": -0.10, "sortBy": "demand",
    },
    "balanced": {
        "minSearchVolume": 1000, "monopolyThreshold": 0.60, "sortBy": "score",
    },
    "aggressive": {
        "minSearchVolume": 300, "monopolyThreshold": 0.70, "maxDeclineRate": -0.30,
        "sortBy": "growth",
    },
    "long-tail": {
        "minSearchVolume": 300, "monopolyThreshold": 0.50, "minBrands": 5,
        "productCountMax": 30, "sortBy": "score",
    },
}

DEFAULT_WEIGHTS = {"demand": 0.30, "growth": 0.25, "competition": 0.20, "diversity": 0.15, "newproduct": 0.10}


def load_json(path):
    if not path or not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def normalize(vals):
    """Min-max normalize a list to 0-1."""
    if not vals:
        return []
    mn, mx = min(vals), max(vals)
    if mx == mn:
        return [0.5] * len(vals)
    return [(v - mn) / (mx - mn) for v in vals]


def get_competition(product_count, top5_click, monopoly_threshold):
    if top5_click is not None and top5_click > monopoly_threshold:
        return "高"
    if product_count is None:
        return "未返回"
    if product_count > 50:
        return "中" if top5_click and top5_click < 0.40 else "高"
    if product_count >= 20:
        return "中"
    return "低"


def apply_filter(n, params):
    """Returns (passed, reason, competition)."""
    sv = n.get("searchVolumeWeekly", 0)
    t5 = n.get("top5ProductsClickShare", 0)
    bc = n.get("brandCount", 0)
    growth = n.get("searchVolumeGrowthQuarterly", 0)
    ret = n.get("returnRateAnnual", 0)
    price = n.get("avgPrice", 0)
    cpc = n.get("cpc", {}).get("medium", 0) if isinstance(n.get("cpc"), dict) else 0
    pc = n.get("productCount", 0)

    if sv < params["minSearchVolume"]:
        return False, f"搜索量过低({sv:,}/周)", get_competition(pc, t5, params["monopolyThreshold"])
    if t5 > params["monopolyThreshold"]:
        return False, f"头部垄断({t5*100:.0f}%)", get_competition(pc, t5, params["monopolyThreshold"])
    if bc < params["minBrands"]:
        return False, f"品牌极少({bc})", get_competition(pc, t5, params["monopolyThreshold"])
    if growth < params["maxDeclineRate"]:
        return False, f"市场萎缩({growth*100:.1f}%)", get_competition(pc, t5, params["monopolyThreshold"])
    if ret > params["maxReturnRate"]:
        return False, f"退货率高({ret*100:.1f}%)", get_competition(pc, t5, params["monopolyThreshold"])
    if params.get("minPrice") and price and price < params["minPrice"]:
        return False, f"价格过低(${price:.2f})", get_competition(pc, t5, params["monopolyThreshold"])
    if params.get("maxPrice") and price and price > params["maxPrice"]:
        return False, f"价格过高(${price:.2f})", get_competition(pc, t5, params["monopolyThreshold"])
    if params.get("maxCPC") and cpc and cpc > params["maxCPC"]:
        return False, f"广告成本过高(${cpc:.2f})", get_competition(pc, t5, params["monopolyThreshold"])
    if params.get("productCountMax") and pc and pc > params["productCountMax"]:
        return False, f"商品数超限({pc})", get_competition(pc, t5, params["monopolyThreshold"])
    return True, None, get_competition(pc, t5, params["monopolyThreshold"])


def compute_scores(niches, weights):
    """Compute weighted scores for a list of niches."""
    demands = [n.get("demand", 0) or 0 for n in niches]
    growths = [n.get("searchVolumeGrowthQuarterly", 0) or 0 for n in niches]
    t5s = [n.get("top5ProductsClickShare", 0) or 0 for n in niches]
    bcs = [n.get("brandCount", 0) or 0 for n in niches]
    launches = [n.get("successfulLaunchedSemiannual", 0) or 0 for n in niches]

    norm_d = normalize(demands)
    norm_g = normalize(growths)
    norm_t5 = normalize(t5s)
    norm_bc = normalize(bcs)
    norm_l = normalize(launches)

    # If all launches are 0, redistribute weight
    w = dict(weights)
    if all(l == 0 for l in launches):
        extra = w.pop("newproduct", 0)
        total = sum(w.values())
        if total > 0:
            for k in w:
                w[k] += extra * (w[k] / total)

    scores = []
    for i in range(len(niches)):
        raw = (w.get("demand", 0) * norm_d[i]
               + w.get("growth", 0) * norm_g[i]
               + w.get("competition", 0) * (1 - norm_t5[i])
               + w.get("diversity", 0) * norm_bc[i]
               + w.get("newproduct", 0) * norm_l[i])
        scores.append(round(max(0, min(100, raw * 100)), 1))
    return scores


def resolve_output_path():
    session_id = os.environ.get("SESSION_ID", "")
    if not session_id:
        import secrets
        session_id = f"{time.strftime('%H%M%S')}-{secrets.token_hex(3)}"
    from datetime import date
    today = date.today().isoformat()
    base = os.environ.get("ACPX_WORKSPACES", "") or os.getcwd()
    path = os.path.join(base, "linkfox", today, session_id, "data")
    os.makedirs(path, exist_ok=True)
    return path


def main():
    p = argparse.ArgumentParser(description="Niche Recommendation Pipeline")
    p.add_argument("--input", required=True, help="Jiimore niches JSON file (or multiple files comma-separated)")
    p.add_argument("--seed-keyword", required=True)
    p.add_argument("--marketplace", default="US")
    p.add_argument("--profile", choices=["novice", "balanced", "aggressive", "long-tail"], default=None)
    p.add_argument("--min-search-volume", type=int, default=None)
    p.add_argument("--monopoly-threshold", type=float, default=None)
    p.add_argument("--min-brands", type=int, default=None)
    p.add_argument("--max-decline-rate", type=float, default=None)
    p.add_argument("--max-return-rate", type=float, default=None)
    p.add_argument("--min-price", type=float, default=None)
    p.add_argument("--max-price", type=float, default=None)
    p.add_argument("--max-cpc", type=float, default=None)
    p.add_argument("--product-count-max", type=int, default=None)
    p.add_argument("--sort-by", choices=["demand", "growth", "score"], default=None)
    p.add_argument("--score-weights", type=str, default=None)
    args = p.parse_args()

    # Default params
    params = {
        "minSearchVolume": 500, "monopolyThreshold": 0.60, "minBrands": 3,
        "maxDeclineRate": -0.20, "maxReturnRate": 0.10,
        "minPrice": None, "maxPrice": None, "maxCPC": None, "productCountMax": None,
        "sortBy": "demand", "scoreWeights": DEFAULT_WEIGHTS.copy(),
    }

    if args.profile:
        params.update(PROFILES[args.profile])

    if args.min_search_volume is not None: params["minSearchVolume"] = args.min_search_volume
    if args.monopoly_threshold is not None: params["monopolyThreshold"] = args.monopoly_threshold
    if args.min_brands is not None: params["minBrands"] = args.min_brands
    if args.max_decline_rate is not None: params["maxDeclineRate"] = args.max_decline_rate
    if args.max_return_rate is not None: params["maxReturnRate"] = args.max_return_rate
    if args.min_price is not None: params["minPrice"] = args.min_price
    if args.max_price is not None: params["maxPrice"] = args.max_price
    if args.max_cpc is not None: params["maxCPC"] = args.max_cpc
    if args.product_count_max is not None: params["productCountMax"] = args.product_count_max
    if args.sort_by is not None: params["sortBy"] = args.sort_by
    if args.score_weights:
        params["scoreWeights"] = json.loads(args.score_weights)

    # Load niches (support multiple files)
    all_niches = []
    for fpath in args.input.split(","):
        data = load_json(fpath.strip())
        if data and isinstance(data, list):
            all_niches.extend(data)
        elif data and isinstance(data, dict):
            all_niches.extend(data.get("data", []))

    # Deduplicate by nicheId
    seen = set()
    niches = []
    for n in all_niches:
        nid = n.get("nicheId", "")
        if nid not in seen:
            seen.add(nid)
            niches.append(n)

    print(f"Loaded {len(niches)} unique niches", flush=True)

    # S1: Hard filter
    passed = []
    eliminated = []
    for n in niches:
        ok, reason, comp = apply_filter(n, params)
        if ok:
            passed.append({**n, "_competition": comp, "_eliminationReason": None})
        else:
            eliminated.append({**n, "_competition": comp, "_eliminationReason": reason})

    # S2: Score
    if params["sortBy"] == "score":
        scores = compute_scores(passed, params["scoreWeights"])
        for i, n in enumerate(passed):
            n["_score"] = scores[i]
    else:
        for n in passed:
            n["_score"] = None

    # S3: Sort
    if params["sortBy"] == "score":
        passed.sort(key=lambda x: -x.get("_score", 0))
    elif params["sortBy"] == "growth":
        passed.sort(key=lambda x: -(x.get("searchVolumeGrowthQuarterly", 0) or 0))
    else:  # demand
        passed.sort(key=lambda x: -(x.get("demand", 0) or 0))

    # Assign ranks and recommendation levels
    results = []
    for i, n in enumerate(passed, 1):
        score = n.get("_score", 0)
        if params["sortBy"] == "score" and score >= 60:
            rec = "强烈推荐"
        elif params["sortBy"] == "score" and score >= 45:
            rec = "推荐"
        elif params["sortBy"] == "score" and score >= 30:
            rec = "谨慎考虑"
        elif params["sortBy"] != "score":
            rec = "通过"  # No scoring, just passed filter
        else:
            rec = "不推荐"

        results.append({
            "rank": i,
            "nicheTitle": n.get("nicheTitle", ""),
            "translationZh": n.get("translationZh", ""),
            "recommendation": rec,
            "score": score,
            "competition": n["_competition"],
            "demand": n.get("demand", 0),
            "searchVolumeWeekly": n.get("searchVolumeWeekly", 0),
            "unitsSoldWeekly": n.get("unitsSoldWeekly", 0),
            "productCount": n.get("productCount", 0),
            "brandCount": n.get("brandCount", 0),
            "top5ClickShare": n.get("top5ProductsClickShare", 0),
            "cpc": n.get("cpc", {}).get("medium", 0) if isinstance(n.get("cpc"), dict) else 0,
            "avgPrice": n.get("avgPrice", 0),
            "growth": n.get("searchVolumeGrowthQuarterly", 0),
            "successfulLaunches": n.get("successfulLaunchedSemiannual", 0),
            "eliminationReason": None,
        })

    for n in eliminated:
        results.append({
            "rank": None,
            "nicheTitle": n.get("nicheTitle", ""),
            "translationZh": n.get("translationZh", ""),
            "recommendation": "不推荐",
            "score": 0,
            "competition": n["_competition"],
            "demand": n.get("demand", 0),
            "searchVolumeWeekly": n.get("searchVolumeWeekly", 0),
            "unitsSoldWeekly": n.get("unitsSoldWeekly", 0),
            "productCount": n.get("productCount", 0),
            "brandCount": n.get("brandCount", 0),
            "top5ClickShare": n.get("top5ProductsClickShare", 0),
            "cpc": n.get("cpc", {}).get("medium", 0) if isinstance(n.get("cpc"), dict) else 0,
            "avgPrice": n.get("avgPrice", 0),
            "growth": n.get("searchVolumeGrowthQuarterly", 0),
            "successfulLaunches": n.get("successfulLaunchedSemiannual", 0),
            "eliminationReason": n["_eliminationReason"],
        })

    # Save
    output_dir = resolve_output_path()
    ts = int(time.time() * 1000000)
    output_path = os.path.join(output_dir, f"niche-recommendation-{ts}.json")
    output = {
        "summary": {
            "seedKeyword": args.seed_keyword,
            "marketplace": args.marketplace,
            "totalNiches": len(niches),
            "passed": len(passed),
            "eliminated": len(eliminated),
            "sortBy": params["sortBy"],
            "profile": args.profile,
        },
        "niches": results,
    }
    with open(output_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"\n{'='*150}")
    print(f"细分市场推荐结果（关键词: {args.seed_keyword}, 共{len(niches)}个, 通过{len(passed)}个, 淘汰{len(eliminated)}个）")
    if args.profile:
        print(f"模板: {args.profile} | 排序: {params['sortBy']}")
    print(f"{'='*150}")
    print(f"\n{'#':>3}  {'推荐':<6} {'细分市场':<40} {'中文':<18} {'评分':>5} {'竞争度':<4} {'需求量':>10} {'周搜索':>10} {'Top5':>5} {'CPC':>5} {'增长':>7}  {'淘汰原因'}")
    print("-" * 150)

    for r in results:
        mark = {"强烈推荐": "★", "推荐": "✓", "谨慎考虑": "?", "通过": "✓", "不推荐": "✗"}.get(r["recommendation"], "")
        growth_str = f"{r['growth']*100:+.1f}%" if r["growth"] else "N/A"
        score_str = f"{r['score']:.1f}" if r["score"] else "-"
        reason = r["eliminationReason"] or ""
        print(f"{str(r['rank'] or ''):>3}  {mark} {r['recommendation']:<4} {r['nicheTitle']:<40} {r['translationZh']:<18} {score_str:>5} {r['competition']:<4} {r['demand']:>10,} {r['searchVolumeWeekly']:>10,} {r['top5ClickShare']*100:>4.0f}% ${r['cpc']:>4} {growth_str:>7}  {reason}")

    rec_counts = Counter(r["recommendation"] for r in results)
    print(f"\n推荐分布: {dict(rec_counts)}")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
