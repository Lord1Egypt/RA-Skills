#!/usr/bin/env python3
"""
Keyword Selection Pipeline - S2c (filtering) + S4 (scoring/sorting/output)

Accepts S2a (Amazon search results), S2b (sellersprite reverse lookup),
S3 (Keepa product details) JSON files, applies configurable filters and
scoring, outputs sorted candidate list.

Usage:
  python run_pipeline.py \
    --s2a <s2a.json> --s2b <s2b.json> --s3 <s3.json> \
    --seed-keyword tripod --marketplace US --top-n 20

  # With profile
  python run_pipeline.py ... --profile high-value

  # With custom params
  python run_pipeline.py ... --min-price 20 --max-price 50 --sort-by score
"""
import argparse
import json
import math
import os
import sys
import time
from collections import Counter


# === Preset Templates (5 profiles from seller research) ===
PROFILES = {
    "novice": {
        "minSearches": 3000, "monopolyThreshold": 0.55, "monopolyAction": "abandon",
        "redOceanThreshold": 1.0, "minPurchaseRate": 0.03,
        "watchThreshold": 0.5, "opportunityThreshold": 1.5,
        "includeWatchlist": False, "sortBy": "sdr",
    },
    "demand-supply": {
        "minSearches": 2000, "monopolyThreshold": 0.50, "monopolyAction": "abandon",
        "redOceanThreshold": 0.8, "minPurchaseRate": 0.04, "maxCPC": 1.5,
        "watchThreshold": 0.4, "opportunityThreshold": 1.2,
        "sortBy": "custom",
    },
    "reverse-asin": {
        "minSearches": 1500, "monopolyThreshold": 0.45, "monopolyAction": "abandon",
        "redOceanThreshold": 1.0, "minPurchaseRate": 0.06, "maxCPC": 1.2,
        "sortBy": "score",
        "scoreWeights": {"sdr": 0.25, "searches": 0.15, "purchaseRate": 0.35, "monopolyPenalty": 0.15, "cpcPenalty": 0.10},
    },
    "weighted-score": {
        "minPrice": 18.0, "maxPrice": 55.0, "minSearches": 3000,
        "monopolyThreshold": 0.48, "monopolyAction": "demote",
        "redOceanThreshold": 0.6, "minPurchaseRate": 0.05, "maxCPC": 1.8,
        "watchThreshold": 0.35, "opportunityThreshold": 1.0,
        "productHighThreshold": 8000,
        "sortBy": "score",
        "scoreWeights": {"sdr": 0.30, "searches": 0.20, "purchaseRate": 0.25, "monopolyPenalty": 0.15, "cpcPenalty": 0.05},
    },
    "long-tail": {
        "minSearches": 300, "maxSearches": 10000,
        "monopolyThreshold": 0.40, "monopolyAction": "abandon",
        "redOceanThreshold": 3.0, "minPurchaseRate": 0.08, "maxCPC": 0.9,
        "minTokenCount": 3, "includeWatchlist": False,
        "sortBy": "score",
        "scoreWeights": {"sdr": 0.40, "searches": 0.0, "purchaseRate": 0.35, "monopolyPenalty": 0.15, "cpcPenalty": 0.10},
    },
}

DEFAULT_SCORE_WEIGHTS = {"sdr": 0.35, "searches": 0.25, "purchaseRate": 0.20, "monopolyPenalty": 0.15, "cpcPenalty": 0.05}


def load_json(path):
    if not path or not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def get_competition(products, sdr, monopoly, params):
    """Three-factor competition grading (parameterized)."""
    p_high = params["productHighThreshold"]
    p_low = params["productLowThreshold"]
    mono_thresh = params["monopolyThreshold"]
    watch_t = params["watchThreshold"]

    if monopoly is not None and monopoly > mono_thresh:
        return "高"
    if products is None or sdr is None:
        return "未返回"
    if products > p_high and sdr < 1:
        return "高"
    if products > p_high and sdr >= 1:
        return "中"
    if p_low <= products <= p_high and sdr > 1:
        return "中"
    if products < p_low and sdr > 1:
        return "低"
    # else: mid-low products + SDR <= 1
    if sdr < watch_t:
        return "高"
    return "中"


def apply_filters(sdr, searches, products, monopoly, bid, purchases, purchase_rate, price, kw, params):
    """Apply hard filters + priority decision tree. Returns (funnel, action, keep)."""
    # === Layer 0: Hard filters ===
    if params["minPrice"] is not None and price is not None and price < params["minPrice"]:
        return "放弃-价格过低", "放弃", False
    if params["maxPrice"] is not None and price is not None and price > params["maxPrice"]:
        return "放弃-价格过高", "放弃", False
    if params["minSearches"] > 0 and searches is not None and searches < params["minSearches"]:
        return "放弃-需求不足", "放弃", False
    if params.get("maxSearches") is not None and searches is not None and searches > params["maxSearches"]:
        return "放弃-搜索量过大", "放弃", False
    if params["minPurchases"] is not None and purchases is not None and purchases < params["minPurchases"]:
        return "放弃-转化不足", "放弃", False
    if params["minPurchaseRate"] is not None and purchase_rate is not None and purchase_rate < params["minPurchaseRate"]:
        return "放弃-购买率过低", "放弃", False
    if params["maxCPC"] is not None and bid is not None and bid > params["maxCPC"]:
        return "放弃-广告成本过高", "放弃", False
    if params["maxProducts"] is not None and products is not None and products > params["maxProducts"]:
        return "放弃-商品数超限", "放弃", False

    # === Layer 1: Priority decision tree ===
    # 1. No ASIN
    if not kw.get("_has_asin"):
        return "放弃-无搜索结果", "放弃", False
    # 2. Not in Top100
    if kw.get("_not_in_top100"):
        return "放弃-数据不足", "放弃", False
    # 3. No data or searches=0
    if searches is None or searches == 0:
        return "放弃-假需求", "放弃", False
    # 4. Broad term
    if params["filterBroadTerms"] and kw.get("_is_broad"):
        return "放弃-词过于宽泛", "放弃", False
    # 5. Monopoly
    if monopoly is not None and monopoly > params["monopolyThreshold"]:
        action_map = {"abandon": ("放弃-垄断", "放弃", False),
                      "watch": ("观望-垄断", "观望", True),
                      "demote": (None, None, None)}  # don't change funnel, handle in scoring
        result = action_map.get(params["monopolyAction"], ("放弃-垄断", "放弃", False))
        if result[0] is not None:
            return result
    # 6. Red ocean
    if sdr is not None and sdr < params["redOceanThreshold"]:
        return "放弃-红海", "放弃", False
    # 7. Competition == 高
    comp = get_competition(products, sdr, monopoly, params)
    if comp == "高":
        return "观望-竞争激烈", "观望", True
    # 8. SDR < watchThreshold
    if sdr is not None and sdr < params["watchThreshold"]:
        return "观望-竞争激烈", "观望", True
    # 9. watchThreshold <= SDR <= opportunityThreshold
    if sdr is not None and params["watchThreshold"] <= sdr <= params["opportunityThreshold"]:
        return "可进-供需平衡", "可进", True
    # 10. SDR > opportunityThreshold
    if sdr is not None and sdr > params["opportunityThreshold"]:
        return "可进-机会型", "可进", True
    return "放弃-数据不足", "放弃", False


def compute_score(sdr, searches, purchase_rate, monopoly, cpc, all_kw_data, weights):
    """Compute weighted score (0-10 scale). Normalizes each dimension across all keywords."""
    # Collect all values for normalization
    sdr_vals = [d.get("sdr") or 0 for d in all_kw_data]
    search_vals = [d.get("searches") or 1 for d in all_kw_data]
    pr_vals = [d.get("purchaseRate") or 0 for d in all_kw_data]
    mono_vals = [d.get("monopoly") or 0 for d in all_kw_data]
    cpc_vals = [d.get("cpc") or 0 for d in all_kw_data]

    def norm(val, vals, log=False):
        if log:
            vals = [math.log1p(v) for v in vals]
            val = math.log1p(val)
        if not vals or max(vals) == min(vals):
            return 0.5
        return (val - min(vals)) / (max(vals) - min(vals))

    sdr_n = norm(sdr or 0, sdr_vals)
    search_n = norm(searches or 1, search_vals, log=True)
    pr_n = norm(purchase_rate or 0, pr_vals)
    mono_n = norm(monopoly or 0, mono_vals)
    cpc_n = norm(cpc or 0, cpc_vals)

    raw = (weights.get("sdr", 0.35) * sdr_n +
           weights.get("searches", 0.25) * search_n +
           weights.get("purchaseRate", 0.20) * pr_n -
           weights.get("monopolyPenalty", 0.15) * mono_n -
           weights.get("cpcPenalty", 0.05) * cpc_n)
    return round(max(0, min(10, raw * 10)), 1)


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
    p = argparse.ArgumentParser(description="Keyword Selection Pipeline (S2c + S4)")
    # Input files
    p.add_argument("--s2a", help="S2a Amazon search results JSON")
    p.add_argument("--s2b", help="S2b sellersprite results JSON")
    p.add_argument("--s3", help="S3 Keepa results JSON")
    p.add_argument("--candidates", help="S1 candidates JSON (optional, uses s2a keys if not provided)")
    # Basic params
    p.add_argument("--seed-keyword", required=True)
    p.add_argument("--marketplace", default="US")
    p.add_argument("--top-n", type=int, default=20)
    p.add_argument("--deep-dive-top-n", type=int, default=5)
    p.add_argument("--filter-broad", action="store_true", default=True)
    # Tier-1 filter params
    p.add_argument("--min-price", type=float, default=None)
    p.add_argument("--max-price", type=float, default=None)
    p.add_argument("--min-searches", type=int, default=0)
    p.add_argument("--max-searches", type=int, default=None)
    p.add_argument("--monopoly-threshold", type=float, default=0.6)
    p.add_argument("--monopoly-action", choices=["abandon", "watch", "demote"], default="abandon")
    p.add_argument("--red-ocean-threshold", type=float, default=0.1)
    p.add_argument("--watch-threshold", type=float, default=0.3)
    p.add_argument("--opportunity-threshold", type=float, default=1.0)
    p.add_argument("--product-low-threshold", type=int, default=1000)
    p.add_argument("--product-high-threshold", type=int, default=5000)
    p.add_argument("--min-purchases", type=int, default=None)
    p.add_argument("--min-purchase-rate", type=float, default=None)
    p.add_argument("--max-cpc", type=float, default=None)
    p.add_argument("--max-products", type=int, default=None)
    # Tier-2 params
    p.add_argument("--sort-by", choices=["sdr", "score", "custom"], default="sdr")
    p.add_argument("--score-weights", type=str, default=None, help="JSON string of weights")
    p.add_argument("--include-watchlist", action="store_true", default=True)
    p.add_argument("--risk-appetite", choices=["conservative", "balanced", "aggressive"], default="balanced")
    p.add_argument("--min-token-count", type=int, default=2)
    p.add_argument("--profile", choices=["novice", "demand-supply", "reverse-asin", "weighted-score", "long-tail"], default=None)

    args = p.parse_args()

    # === Load profile if specified ===
    params = {
        "minPrice": None, "maxPrice": None, "minSearches": 0, "maxSearches": None,
        "monopolyThreshold": 0.6, "monopolyAction": "abandon",
        "redOceanThreshold": 0.1, "watchThreshold": 0.3, "opportunityThreshold": 1.0,
        "productLowThreshold": 1000, "productHighThreshold": 5000,
        "minPurchases": None, "minPurchaseRate": None, "maxCPC": None, "maxProducts": None,
        "sortBy": "sdr", "scoreWeights": DEFAULT_SCORE_WEIGHTS.copy(),
        "includeWatchlist": True, "riskAppetite": "balanced",
        "filterBroadTerms": True, "minTokenCount": 2,
    }

    if args.profile:
        prof = PROFILES[args.profile]
        params.update(prof)
        if "scoreWeights" in prof:
            params["scoreWeights"] = prof["scoreWeights"]

    # Override with CLI args (only if explicitly provided)
    if args.min_price is not None: params["minPrice"] = args.min_price
    if args.max_price is not None: params["maxPrice"] = args.max_price
    if args.min_searches > 0: params["minSearches"] = args.min_searches
    if args.monopoly_threshold != 0.6: params["monopolyThreshold"] = args.monopoly_threshold
    if args.monopoly_action != "abandon": params["monopolyAction"] = args.monopoly_action
    if args.red_ocean_threshold != 0.1: params["redOceanThreshold"] = args.red_ocean_threshold
    if args.watch_threshold != 0.3: params["watchThreshold"] = args.watch_threshold
    if args.opportunity_threshold != 1.0: params["opportunityThreshold"] = args.opportunity_threshold
    if args.product_low_threshold != 1000: params["productLowThreshold"] = args.product_low_threshold
    if args.product_high_threshold != 5000: params["productHighThreshold"] = args.product_high_threshold
    if args.min_purchases is not None: params["minPurchases"] = args.min_purchases
    if args.min_purchase_rate is not None: params["minPurchaseRate"] = args.min_purchase_rate
    if args.max_cpc is not None: params["maxCPC"] = args.max_cpc
    if args.max_products is not None: params["maxProducts"] = args.max_products
    if args.sort_by != "sdr": params["sortBy"] = args.sort_by
    if args.risk_appetite != "balanced": params["riskAppetite"] = args.risk_appetite
    if args.score_weights:
        params["scoreWeights"] = json.loads(args.score_weights)

    # === Load data ===
    s2a = load_json(args.s2a) or {}
    s2b = load_json(args.s2b) or {}
    s3 = load_json(args.s3) or {}

    # Load candidates (S1)
    if args.candidates:
        cand_data = load_json(args.candidates)
        candidates = cand_data.get("candidates", list(s2a.keys())) if cand_data else list(s2a.keys())
    else:
        candidates = list(s2a.keys())

    # Build sellersprite keyword lookup
    ss_kw = {}
    for asin, data in s2b.items():
        if isinstance(data, dict) and data.get("error"):
            continue
        if isinstance(data, dict):
            for kw, kw_data in data.get("keywords", {}).items():
                if isinstance(kw_data, dict) and kw_data.get("status") != "keyword_not_in_top100":
                    ss_kw[kw] = {**kw_data, "_asin": asin}

    # === Process each keyword ===
    results = []
    for kw in candidates:
        s2a_data = s2a.get(kw, {})
        kw_data = ss_kw.get(kw, {})
        asin = s2a_data.get("asin", "")
        keepa = s3.get(asin, {})

        sdr = kw_data.get("supplyDemandRatio")
        searches = kw_data.get("searches")
        products = kw_data.get("products")
        monopoly = kw_data.get("monopolyClickRate")
        bid = kw_data.get("bid")
        purchases = kw_data.get("purchases")
        purchase_rate = kw_data.get("purchaseRate")

        price = keepa.get("price", s2a_data.get("price"))
        if price is not None and isinstance(price, str):
            try: price = float(price)
            except: price = None

        # Build kw meta for filter
        kw_meta = {
            "_has_asin": bool(asin),
            "_not_in_top100": not kw_data or kw_data.get("status") == "keyword_not_in_top100",
            "_is_broad": kw.lower() == args.seed_keyword.lower(),
        }

        # Apply filters
        funnel, action, keep = apply_filters(
            sdr, searches, products, monopoly, bid, purchases, purchase_rate, price, kw_meta, params
        )

        # Handle downgrade mode
        if params["monopolyAction"] == "downgrade" and monopoly is not None and monopoly > params["monopolyThreshold"]:
            # Don't change funnel, but mark for scoring penalty
            pass

        # Competition
        competition = get_competition(products, sdr, monopoly, params)

        # Demand signal
        if searches is None:
            demand_signal = "未返回"
        elif searches > 100000:
            demand_signal = f"极高({searches:,})"
        elif searches > 10000:
            demand_signal = f"高({searches:,})"
        elif searches > 1000:
            demand_signal = f"中({searches:,})"
        elif searches > 0:
            demand_signal = f"低({searches:,})"
        else:
            demand_signal = "无数据"

        # Price band
        if price is None:
            price_band = "未返回"
        elif price < 15: price_band = "低价(<$15)"
        elif price < 30: price_band = "中低($15-30)"
        elif price < 50: price_band = "中高($30-50)"
        else: price_band = "高价(>$50)"

        rep_product = None
        if asin and keep:
            rep_product = {
                "asin": asin,
                "title": keepa.get("title", s2a_data.get("title", "未返回")),
                "price": price if price is not None else "未返回",
                "brand": keepa.get("brand", "未返回"),
                "rating": keepa.get("rating", s2a_data.get("rating", "未返回")),
                "reviewCount": keepa.get("reviewCount", s2a_data.get("reviews", "未返回")),
            }

        results.append({
            "keyword": kw, "platform": f"Amazon {args.marketplace}",
            "demandSignal": demand_signal,
            "supplyDemandRatio": sdr if sdr is not None else "未返回",
            "searches": searches if searches is not None else "未返回",
            "products": products if products is not None else "未返回",
            "monopolyClickRate": f"{monopoly:.2%}" if monopoly is not None else "未返回",
            "cpc": f"${bid:.2f}" if bid is not None else "未返回",
            "purchases": f"{purchases:,}" if purchases is not None else "未返回",
            "purchaseRate": f"{purchase_rate:.2%}" if purchase_rate is not None else "未返回",
            "competition": competition, "priceBand": price_band,
            "funnelConclusion": funnel, "suggestedAction": action,
            "representativeProduct": rep_product, "keep": keep,
            # Raw values for scoring
            "_sdr": sdr, "_searches": searches, "_purchaseRate": purchase_rate,
            "_monopoly": monopoly, "_cpc": bid, "_price": price,
        })

    # === Scoring ===
    if params["sortBy"] == "score":
        all_data = [{"sdr": r["_sdr"], "searches": r["_searches"], "purchaseRate": r["_purchaseRate"],
                      "monopoly": r["_monopoly"], "cpc": r["_cpc"]} for r in results]
        for r in results:
            r["score"] = compute_score(r["_sdr"], r["_searches"], r["_purchaseRate"],
                                        r["_monopoly"], r["_cpc"], all_data, params["scoreWeights"])
            r["sortBasis"] = f"综合评分={r['score']}"
    else:
        for r in results:
            r["score"] = None
            r["sortBasis"] = f"需供比={r['_sdr']:.2f}" if r["_sdr"] is not None else "需供比=未返回"

    # === Sorting ===
    kept = [r for r in results if r["keep"]]
    eliminated = [r for r in results if not r["keep"]]

    if params["sortBy"] == "score":
        kept.sort(key=lambda x: -(x["score"] or 0))
    elif params["sortBy"] == "custom":
        kept.sort(key=lambda x: (-(x["_sdr"] or 0), -(x["_searches"] or 0), x["_monopoly"] or 1))
    else:  # sdr
        kept.sort(key=lambda x: -(x["_sdr"] or 0))

    # Risk appetite filtering
    if params["riskAppetite"] == "conservative":
        kept = [r for r in kept if r["suggestedAction"] == "可进"]

    # Assign ranks
    for i, r in enumerate(kept, 1):
        r["rank"] = i
        # Filter trace
        traces = []
        if params["minPrice"] is not None and r["_price"] is not None:
            traces.append(f"价格${r['_price']:.2f} ✓")
        if params["minSearches"] > 0 and r["_searches"] is not None:
            traces.append(f"搜索量{r['_searches']:,} ✓")
        if r["score"] is not None:
            traces.append(f"综合分{r['score']}")
        r["filterTrace"] = " | ".join(traces) if traces else "默认配置"

    for r in eliminated:
        r["rank"] = None
        r["filterTrace"] = r["funnelConclusion"]

    # Combine: kept first, then eliminated
    final = kept[:args.top_n] + eliminated

    # Clean up internal fields
    for r in final:
        for k in list(r.keys()):
            if k.startswith("_"):
                del r[k]

    # === Output ===
    output_dir = resolve_output_path()
    ts = int(time.time() * 1000000)
    output_path = os.path.join(output_dir, f"keyword-selection-method-{ts}.json")

    output = {
        "summary": {
            "seedKeyword": args.seed_keyword,
            "marketplace": args.marketplace,
            "totalCandidates": len(results),
            "kept": len(kept),
            "eliminated": len(eliminated),
            "topN": args.top_n,
            "sortBy": params["sortBy"],
            "profile": args.profile,
            "params": {k: v for k, v in params.items() if v is not None and v != "" and v != 0 and v != []},
        },
        "keywords": final,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"\n{'='*150}")
    print(f"关键词选品结果（种子词: {args.seed_keyword}, 站点: {args.marketplace}, 共{len(results)}个, 保留{len(kept)}个）")
    if args.profile:
        print(f"模板: {args.profile} | 排序: {params['sortBy']}")
    print(f"{'='*150}")
    print(f"\n{'#':>3}  {'关键词':<40} {'需供比':>8} {'搜索量':>10} {'商品数':>8} {'CPC':>6} {'垄断率':>8} {'购买率':>8} {'竞争度':<4} {'漏斗结论':<22} {'ASIN':<12}")
    print("-" * 150)

    for r in final:
        mark = "v" if r["keep"] else "x"
        sdr_s = f"{r['supplyDemandRatio']:.2f}" if isinstance(r.get("supplyDemandRatio"), (int, float)) else "未返回"
        sr_s = f"{r['searches']:,}" if isinstance(r.get("searches"), (int, float)) else "未返回"
        pr_s = f"{r['products']:,}" if isinstance(r.get("products"), (int, float)) else "未返回"
        asin_s = r["representativeProduct"]["asin"] if r.get("representativeProduct") else "N/A"
        score_s = f" [{r.get('score', '')}]" if r.get("score") else ""
        print(f"{mark}{str(r.get('rank','')):>2}  {r['keyword']:<40} {sdr_s:>8} {sr_s:>10} {pr_s:>8} {r.get('cpc',''):>6} {r.get('monopolyClickRate',''):>8} {r.get('purchaseRate',''):>8} {r.get('competition',''):<4} {r['funnelConclusion']:<22} {asin_s:<12}{score_s}")

    counts = Counter(r["suggestedAction"] for r in final)
    print(f"\n动作分布: {dict(counts)}")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
