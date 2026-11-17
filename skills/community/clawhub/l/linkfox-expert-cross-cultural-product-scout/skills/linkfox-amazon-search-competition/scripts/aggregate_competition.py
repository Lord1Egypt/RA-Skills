#!/usr/bin/env python3
"""前台搜索 6 段竞争格局聚合 - LinkFox Skill

读取合并后的亚马逊前台搜索商品 JSON（建议已含 page / organic_rank），
做 6 段分析 + 新品清单，输出聚合 JSON。

Usage:
  python aggregate_competition.py <merged_products.json>
  python aggregate_competition.py <merged_products.json> --fixed-buckets
  python aggregate_competition.py <merged_products.json> --buckets <file.json>
  python aggregate_competition.py <merged_products.json> --inline
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime

from linkfox_paths import resolve_data_path

SLUG = "linkfox-amazon-search-competition"
SMALL_THRESHOLD = 8000
MISSING_UNITS_DEFAULT = 50  # 月销缺失记为 50
NEW_PRODUCT_RATINGS_LT = 100  # 新品代理：评分数 < 100

DEFAULT_BUCKETS = {
    "price": [
        {"label": "<$20", "min": 0, "max": 20},
        {"label": "$20-50", "min": 20, "max": 50},
        {"label": "$50-100", "min": 50, "max": 100},
        {"label": "$100-200", "min": 100, "max": 200},
        {"label": "$200+", "min": 200, "max": None},
    ],
    "ratingCount": [
        {"label": "<100", "min": 0, "max": 100},
        {"label": "100-500", "min": 100, "max": 500},
        {"label": "500-2k", "min": 500, "max": 2000},
        {"label": "2k-10k", "min": 2000, "max": 10000},
        {"label": "10k+", "min": 10000, "max": None},
    ],
    "ratingValue": [
        {"label": "<3.5", "min": 0, "max": 3.5},
        {"label": "3.5-4.0", "min": 3.5, "max": 4.0},
        {"label": "4.0-4.5", "min": 4.0, "max": 4.5},
        {"label": "4.5-5.0", "min": 4.5, "max": None},
    ],
}

RANK_SEGMENTS = [
    {"label": "Top10", "min": 1, "max": 10},
    {"label": "11-20", "min": 11, "max": 20},
    {"label": "21-48", "min": 21, "max": 48},
    {"label": "49+", "min": 49, "max": None},
]


# ── helpers ─────────────────────────────────────────────────────

def safe_float(val, default=None):
    if val is None or val == "":
        return default
    try:
        if isinstance(val, str):
            val = val.replace(",", "").replace("$", "").strip()
        return float(val)
    except (TypeError, ValueError):
        return default


def safe_int(val, default=None):
    f = safe_float(val, None)
    if f is None:
        return default
    try:
        return int(f)
    except (TypeError, ValueError):
        return default


def get_price(p):
    return safe_float(p.get("extractedPrice"), None) or safe_float(p.get("price"), 0.0) or 0.0


def get_units(p):
    """有值用原值；缺失记 50，并标记 imputed。"""
    raw = p.get("monthlySalesUnits")
    if raw is None or raw == "":
        return MISSING_UNITS_DEFAULT, True
    v = safe_int(raw, None)
    if v is None:
        return MISSING_UNITS_DEFAULT, True
    return max(v, 0), False


def get_revenue(p, units, price):
    raw = p.get("monthlySalesRevenue")
    if raw not in (None, ""):
        v = safe_float(raw, None)
        if v is not None:
            return v, False
    return float(units) * float(price or 0), True


def has_variant(p):
    opt = p.get("options")
    return opt not in (None, "", [], {})


def load_products(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "products" in data:
            return data["products"]
        if "items" in data:
            return data["items"]
    raise ValueError("Input must be a list of products or an object with products/items")


def load_buckets(arg):
    if os.path.exists(arg):
        with open(arg, encoding="utf-8") as f:
            return json.load(f)
    return json.loads(arg)


def ensure_organic_rank(products):
    """若已有 organic_rank 则规范化；否则在存在 page 时按 page 重算。"""
    if products and all(p.get("organic_rank") is not None for p in products):
        out = sorted(products, key=lambda p: (safe_int(p.get("organic_rank"), 10**9), p.get("asin") or ""))
        return out, "provided"

    has_page = any(p.get("page") is not None for p in products)
    if not has_page:
        # 无 page 时按列表顺序编号（调用方应在 Step2 写好 page）
        out = []
        for i, p in enumerate(products, 1):
            q = dict(p)
            q["organic_rank"] = i
            q.setdefault("page_position", p.get("position"))
            out.append(q)
        return out, "sequential-fallback"

    by_page = defaultdict(list)
    for p in products:
        if p.get("sponsored") is True:
            continue
        pg = safe_int(p.get("page"), 1) or 1
        by_page[pg].append(p)

    ranked = []
    rank = 0
    for pg in sorted(by_page.keys()):
        page_items = sorted(
            by_page[pg],
            key=lambda x: safe_int(x.get("page_position") or x.get("position"), 999) or 999,
        )
        for p in page_items:
            rank += 1
            q = dict(p)
            q["page"] = pg
            q["page_position"] = p.get("page_position") or p.get("position")
            q["organic_rank"] = rank
            ranked.append(q)

    # ASIN 去重保留最小 rank
    best = {}
    for item in ranked:
        a = item.get("asin")
        if not a:
            continue
        if a not in best or item["organic_rank"] < best[a]["organic_rank"]:
            best[a] = item
    out = sorted(best.values(), key=lambda x: x["organic_rank"])
    return out, "recomputed"


def enrich(products):
    """补 units / revenue / has_variant / units_imputed。"""
    out = []
    raw_units = 0
    for p in products:
        q = dict(p)
        price = get_price(q)
        units, imputed = get_units(q)
        rev, rev_imputed = get_revenue(q, units, price)
        q["_price"] = price
        q["_units"] = units
        q["_revenue"] = rev
        q["units_imputed"] = imputed
        q["revenue_imputed"] = rev_imputed
        q["has_variant"] = has_variant(q)
        if not imputed:
            raw_units += 1
        out.append(q)
    return out, raw_units


def _in_bucket(val, b):
    if val is None:
        return False
    lo = b["min"]
    hi = b["max"]
    if hi is None:
        return val >= lo
    return lo <= val < hi


def bucket_stats(items, value_fn, bucket_defs):
    """返回各桶商品数、销量、销量占比。"""
    total_units = sum(x["_units"] for x in items) or 1
    labels, counts, unit_shares = [], [], []
    for b in bucket_defs:
        sub = [x for x in items if _in_bucket(value_fn(x), b)]
        u = sum(x["_units"] for x in sub)
        labels.append(b["label"])
        counts.append(len(sub))
        unit_shares.append(round(100.0 * u / total_units, 1))
    return {
        "labels": labels,
        "productCounts": counts,
        "salesShares": unit_shares,
    }


# ── 6 段计算 ────────────────────────────────────────────────────

def calc_page_traffic(items):
    total_u = sum(x["_units"] for x in items) or 1
    total_r = sum(x["_revenue"] for x in items) or 1
    by_page = defaultdict(lambda: {"n": 0, "units": 0, "revenue": 0.0})
    for x in items:
        pg = safe_int(x.get("page"), 0) or 0
        by_page[pg]["n"] += 1
        by_page[pg]["units"] += x["_units"]
        by_page[pg]["revenue"] += x["_revenue"]
    pages = []
    for pg in sorted(by_page.keys()):
        d = by_page[pg]
        pages.append({
            "page": pg,
            "productCount": d["n"],
            "units": d["units"],
            "revenue": round(d["revenue"], 2),
            "unitsShare": round(100.0 * d["units"] / total_u, 1),
            "revenueShare": round(100.0 * d["revenue"] / total_r, 1),
        })
    return {
        "dimension": 1,
        "name": "页流量占比",
        "type": "table",
        "data": {"pages": pages, "totalUnits": sum(x["_units"] for x in items),
                 "totalRevenue": round(sum(x["_revenue"] for x in items), 2)},
    }


def calc_rank_concentration(items):
    total_u = sum(x["_units"] for x in items) or 1
    segments = []
    cum = 0
    for seg in RANK_SEGMENTS:
        lo, hi = seg["min"], seg["max"]
        if hi is None:
            sub = [x for x in items if (x.get("organic_rank") or 0) >= lo]
        else:
            sub = [x for x in items if lo <= (x.get("organic_rank") or 0) <= hi]
        u = sum(x["_units"] for x in sub)
        cum += u
        segments.append({
            "label": seg["label"],
            "productCount": len(sub),
            "units": u,
            "unitsShare": round(100.0 * u / total_u, 1),
            "cumulativeShare": round(100.0 * cum / total_u, 1),
        })
    top10 = [x for x in items if 1 <= (x.get("organic_rank") or 0) <= 10]
    top10_share = round(100.0 * sum(x["_units"] for x in top10) / total_u, 1)
    return {
        "dimension": 2,
        "name": "自然位集中度",
        "type": "pareto",
        "data": {
            "segments": segments,
            "top10UnitsShare": top10_share,
            "labels": [s["label"] for s in segments],
            "units": [s["units"] for s in segments],
            "cumulativeShare": [s["cumulativeShare"] for s in segments],
        },
    }


def calc_price_distribution(items, bucket_defs):
    stats = bucket_stats(items, lambda x: x["_price"], bucket_defs)
    total_u = sum(x["_units"] for x in items) or 1
    weighted = sum(x["_price"] * x["_units"] for x in items) / total_u
    simple = (sum(x["_price"] for x in items) / len(items)) if items else 0
    return {
        "dimension": 3,
        "name": "价格分布",
        "type": "distribution",
        "data": {
            **stats,
            "salesWeightedAvgPrice": round(weighted, 2),
            "simpleAvgPrice": round(simple, 2),
        },
    }


def calc_rating_count_distribution(items, bucket_defs):
    def rc(x):
        return safe_int(x.get("ratings"), None)

    stats = bucket_stats(items, rc, bucket_defs)
    return {
        "dimension": 4,
        "name": "评分数分布",
        "type": "distribution",
        "data": stats,
    }


def calc_rating_value_distribution(items, bucket_defs):
    def rv(x):
        return safe_float(x.get("rating"), None)

    stats = bucket_stats(items, rv, bucket_defs)
    return {
        "dimension": 5,
        "name": "评分分布",
        "type": "distribution",
        "data": stats,
    }


def calc_has_variant(items):
    total = len(items) or 1
    total_u = sum(x["_units"] for x in items) or 1
    with_v = [x for x in items if x.get("has_variant")]
    u = sum(x["_units"] for x in with_v)
    return {
        "dimension": 6,
        "name": "是否含变体",
        "type": "data",
        "data": {
            "totalProducts": len(items),
            "hasVariantCount": len(with_v),
            "hasVariantRatio": round(100.0 * len(with_v) / total, 1),
            "hasVariantUnitsShare": round(100.0 * u / total_u, 1),
            "note": "options 非空视为含变体（多为 See options）；未返回不代表一定无变体",
        },
    }


def calc_new_product_list(items, limit=50):
    """新品清单代理：ratings < 100，按 organic_rank 排序。"""
    rows = []
    for x in items:
        rc = safe_int(x.get("ratings"), None)
        if rc is None or rc >= NEW_PRODUCT_RATINGS_LT:
            continue
        rows.append({
            "organic_rank": x.get("organic_rank"),
            "page": x.get("page"),
            "asin": x.get("asin"),
            "title": (x.get("title") or "")[:80],
            "price": x["_price"],
            "rating": safe_float(x.get("rating")),
            "ratings": rc,
            "units": x["_units"],
            "units_imputed": x.get("units_imputed", False),
            "has_variant": bool(x.get("has_variant")),
        })
    rows.sort(key=lambda r: r.get("organic_rank") or 10**9)
    return {
        "name": "新品清单（代理）",
        "type": "table",
        "data": {
            "rule": f"自然结果中 ratings < {NEW_PRODUCT_RATINGS_LT}，按 organic_rank 升序",
            "note": "数据源无上架时间，以低评分数作新品代理，可能含老品低评论链接",
            "count": len(rows),
            "items": rows[:limit],
        },
    }


# ── smart buckets（仅价格/评分数/评分） ─────────────────────────

def _percentile(sorted_vals, p):
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * p / 100.0
    f = int(k)
    c = k - f
    if f + 1 < len(sorted_vals):
        return sorted_vals[f] + c * (sorted_vals[f + 1] - sorted_vals[f])
    return float(sorted_vals[f])


def generate_smart_buckets(items):
    prices = sorted(x["_price"] for x in items if x["_price"] is not None)
    rcounts = sorted(safe_int(x.get("ratings"), 0) or 0 for x in items)
    rvalues = sorted(safe_float(x.get("rating"), 0) or 0 for x in items if x.get("rating") is not None)

    def price_buckets():
        if len(prices) < 4:
            return list(DEFAULT_BUCKETS["price"])
        breaks = [0]
        for p in (20, 40, 60, 80):
            breaks.append(max(0, round(_percentile(prices, p) / 5) * 5))
        breaks.append(None)
        # dedupe
        out, prev = [], -1
        for b in breaks:
            if b is None:
                out.append(None)
            elif b > prev:
                out.append(b)
                prev = b
        if len(out) < 3:
            return list(DEFAULT_BUCKETS["price"])
        buckets = []
        for i in range(len(out) - 1):
            lo, hi = out[i], out[i + 1]
            if hi is None:
                buckets.append({"label": f"${int(lo)}+", "min": lo, "max": None})
            else:
                buckets.append({"label": f"${int(lo)}-{int(hi)}", "min": lo, "max": hi})
        return buckets

    return {
        "price": price_buckets(),
        "ratingCount": list(DEFAULT_BUCKETS["ratingCount"]),
        "ratingValue": list(DEFAULT_BUCKETS["ratingValue"]),
    }


def aggregate(products, buckets=None, use_smart=True):
    ranked, rank_mode = ensure_organic_rank(products)
    items, raw_units_cnt = enrich(ranked)

    if buckets is not None:
        bucket_mode = "custom"
    elif use_smart:
        buckets = generate_smart_buckets(items)
        bucket_mode = "smart"
    else:
        buckets = {k: list(v) for k, v in DEFAULT_BUCKETS.items()}
        bucket_mode = "fixed"

    dims = [
        calc_page_traffic(items),
        calc_rank_concentration(items),
        calc_price_distribution(items, buckets["price"]),
        calc_rating_count_distribution(items, buckets["ratingCount"]),
        calc_rating_value_distribution(items, buckets["ratingValue"]),
        calc_has_variant(items),
    ]
    appendix = calc_new_product_list(items)

    return {
        "meta": {
            "totalProducts": len(items),
            "rawUnitsCoverage": round(100.0 * raw_units_cnt / len(items), 1) if items else 0,
            "rawUnitsCount": raw_units_cnt,
            "imputedUnitsCount": len(items) - raw_units_cnt,
            "missingUnitsDefault": MISSING_UNITS_DEFAULT,
            "rankMode": rank_mode,
            "aggregatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dimensions": 6,
            "bucketMode": bucket_mode,
            "disclaimer": (
                "样本=默认排序前3页自然结果；organic_rank为按页去广告后连续编号，非官方rank/BSR；"
                f"月销缺失按{MISSING_UNITS_DEFAULT}计；新品清单为ratings<{NEW_PRODUCT_RATINGS_LT}代理"
            ),
        },
        "bucketDefs": buckets,
        "dimensions": dims,
        "appendix": appendix,
    }


def summarize(result):
    print(f"Top-level keys: {list(result.keys())}")
    meta = result.get("meta", {})
    for k, v in meta.items():
        print(f"  {k}: {v}")
    dims = result.get("dimensions", [])
    print(f"\nDimensions: {len(dims)}")
    for d in dims:
        print(f"  [{d.get('dimension')}] {d.get('name')} ({d.get('type')})")
    ap = result.get("appendix", {})
    print(f"\nAppendix: {ap.get('name')} count={ap.get('data', {}).get('count')}")


def main():
    argv = sys.argv[1:]
    inline = "--inline" in argv
    argv = [a for a in argv if a != "--inline"]
    fixed_buckets = "--fixed-buckets" in argv
    argv = [a for a in argv if a != "--fixed-buckets"]

    buckets_arg = None
    remaining = []
    i = 0
    while i < len(argv):
        if argv[i] == "--buckets" and i + 1 < len(argv):
            buckets_arg = argv[i + 1]
            i += 2
        else:
            remaining.append(argv[i])
            i += 1
    argv = remaining

    if not argv:
        print(
            f"Usage: {os.path.basename(__file__)} <merged_products.json> "
            f"[--inline] [--fixed-buckets] [--buckets <file.json|json_string>]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = argv[0]
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    products = load_products(input_path)
    if not products:
        print("No products found in input file", file=sys.stderr)
        sys.exit(1)

    if buckets_arg:
        result = aggregate(products, buckets=load_buckets(buckets_arg))
    elif fixed_buckets:
        result = aggregate(products, use_smart=False)
    else:
        result = aggregate(products, use_smart=True)

    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    ts = int(time.time())
    out_path = resolve_data_path(SLUG, ts)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(serialized)
        print(f"Saved full response: {out_path} ({len(serialized)} bytes)")
    except OSError as e:
        print(f"Failed to save to {out_path}: {e}", file=sys.stderr)

    if inline or len(serialized.encode("utf-8")) <= SMALL_THRESHOLD:
        print(serialized)
    else:
        summarize(result)


if __name__ == "__main__":
    main()
