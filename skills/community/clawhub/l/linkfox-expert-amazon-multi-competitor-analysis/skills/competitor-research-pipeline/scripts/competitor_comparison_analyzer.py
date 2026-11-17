#!/usr/bin/env python3
"""
Competitor Comparison Analyzer - 7维度竞品横向对比分析
基于Keepa历史数据，对目标+全部竞品做横向对比

Usage:
  python competitor_comparison_analyzer.py --stdin < params.json

Input:
{
  "asins": ["B0XX", "B0YY", ...],
  "labels": {"B0XX": "目标", "B0YY": "直接竞品", ...},
  "keepa_data": {
    "B0XX": {
      "price": 37.99, "salesRank": 767, "reviewCount": 2813,
      "salesRank30": 698, "salesRank90": 639, "salesRank180": 1078,
      "monthlySalesUnits": 1000,
      "monthlySalesUnits1MonthsAgo": 500, ..., "monthlySalesUnits12MonthsAgo": 500,
      "monthlySalesRevenue": 37990
    },
    ...
  }
}

Output: 7维度对比JSON
"""

import json
import sys
import math
from collections import defaultdict

def get_sales_history(kd):
    """Get 12-month sales history (oldest to newest, excluding current month)"""
    sales = []
    for i in range(12, 0, -1):
        sales.append(kd.get(f"monthlySalesUnits{i}MonthsAgo", 0))
    return sales

def calc_trend(sales):
    """Classify trend: growing/declining/stable/volatile"""
    if not sales or len(sales) < 4:
        return "insufficient_data"
    n = len(sales)
    x_mean = (n - 1) / 2
    y_mean = sum(sales) / n
    num = sum((i - x_mean) * (s - y_mean) for i, s in enumerate(sales))
    den = sum((i - x_mean) ** 2 for i in range(n))
    slope = num / den if den != 0 else 0

    # Check volatility
    if y_mean > 0:
        cv = math.sqrt(sum((s - y_mean) ** 2 for s in sales) / n) / y_mean
    else:
        cv = 0

    if cv > 0.6:
        return "volatile"
    if slope > y_mean * 0.05:
        return "growing"
    elif slope < -y_mean * 0.05:
        return "declining"
    else:
        return "stable"

def detect_deal_spike(sales):
    """Detect Deal months and calculate retention rate"""
    deals = []
    for i in range(1, len(sales) - 1):
        if sales[i] > 0:
            surrounding = [sales[i-1], sales[i+1]]
            s_avg = sum(surrounding) / 2 if sum(surrounding) > 0 else 0.1
            if sales[i] >= s_avg * 3:
                retention = sales[i+1] / sales[i] if sales[i] > 0 else 0
                deals.append({"month_index": i, "sales": sales[i], "retention_rate": round(retention, 2)})

    if not deals:
        return {"has_deal": False, "deals": [], "dependency": "none"}
    avg_retention = sum(d["retention_rate"] for d in deals) / len(deals)
    if avg_retention < 0.3:
        dependency = "high"
    elif avg_retention < 0.6:
        dependency = "medium"
    else:
        dependency = "low"
    return {"has_deal": True, "deals": deals, "avg_retention": round(avg_retention, 2), "dependency": dependency}

def calc_cv(sales, exclude_deal_months=None):
    """Calculate coefficient of variation, optionally excluding Deal months"""
    filtered = []
    exclude = set(exclude_deal_months or [])
    for i, s in enumerate(sales):
        if i not in exclude:
            filtered.append(s)
    if not filtered or sum(filtered) == 0:
        return 0, "insufficient"
    mean = sum(filtered) / len(filtered)
    if mean == 0:
        return 0, "insufficient"
    cv = math.sqrt(sum((s - mean) ** 2 for s in filtered) / len(filtered)) / mean
    if cv < 0.3:
        stability = "high"
    elif cv < 0.6:
        stability = "medium"
    else:
        stability = "low"
    return round(cv, 3), stability

def calc_market_share(all_sales_by_month, asins):
    """Calculate monthly market share for each ASIN"""
    monthly_shares = []
    n_months = len(next(iter(all_sales_by_month.values()), []))
    for m in range(n_months):
        total = sum(all_sales_by_month[asin][m] for asin in asins if asin in all_sales_by_month and m < len(all_sales_by_month[asin]))
        shares = {}
        for asin in asins:
            if asin in all_sales_by_month and m < len(all_sales_by_month[asin]) and total > 0:
                shares[asin] = round(all_sales_by_month[asin][m] / total * 100, 1)
            else:
                shares[asin] = 0
        monthly_shares.append(shares)

    # Calculate share change (first vs last 3 months avg)
    changes = {}
    for asin in asins:
        first_3 = sum(s.get(asin, 0) for s in monthly_shares[:3]) / 3 if len(monthly_shares) >= 3 else 0
        last_3 = sum(s.get(asin, 0) for s in monthly_shares[-3:]) / 3 if len(monthly_shares) >= 3 else 0
        changes[asin] = round(last_3 - first_3, 1)

    return monthly_shares, changes

def calc_seasonality(all_sales_by_month, asins):
    """Detect seasonality sync across ASINs"""
    peak_months = {}
    for asin in asins:
        sales = all_sales_by_month.get(asin, [])
        if sales and max(sales) > 0:
            peak_months[asin] = sales.index(max(sales))
        else:
            peak_months[asin] = None

    # Check if peaks are synchronized (within 2 months of each other)
    valid_peaks = [p for p in peak_months.values() if p is not None]
    if len(valid_peaks) >= 2:
        peak_range = max(valid_peaks) - min(valid_peaks)
        is_synced = peak_range <= 2
    else:
        is_synced = False

    return peak_months, is_synced

def calc_bsr_momentum(kd):
    """Calculate BSR momentum from 30/90/180 day averages"""
    r30 = kd.get("salesRank30", 0)
    r90 = kd.get("salesRank90", 0)
    r180 = kd.get("salesRank180", 0)

    if r30 == 0 or r180 == 0:
        return {"rank30": r30, "rank90": r90, "rank180": r180, "direction": "insufficient_data"}

    if r30 < r90 < r180:
        direction = "accelerating_up"  # BSR improving (lower = better)
    elif r30 > r90 > r180:
        direction = "declining_down"  # BSR worsening
    elif abs(r30 - r180) / r180 < 0.1:
        direction = "stable"
    else:
        direction = "mixed"

    return {"rank30": r30, "rank90": r90, "rank180": r180, "direction": direction}

def calc_elasticity(kd):
    """Estimate price-sales elasticity from Keepa data"""
    price = kd.get("price", 0)
    # Use sales history as proxy for quantity changes
    sales = get_sales_history(kd)
    if len(sales) < 4 or price == 0:
        return {"elasticity": 0, "sensitivity": "insufficient_data"}

    # Simple approximation: compare first half vs second half
    mid = len(sales) // 2
    q1_avg = sum(sales[:mid]) / mid if mid > 0 else 0
    q2_avg = sum(sales[mid:]) / (len(sales) - mid) if len(sales) - mid > 0 else 0

    # Without price history, we can't calculate true elasticity
    # Use BSR change as proxy for demand change
    r30 = kd.get("salesRank30", 0)
    r180 = kd.get("salesRank180", 0)
    if r30 > 0 and r180 > 0 and r180 != r30:
        demand_change = (r180 - r30) / r180  # positive = improving
    else:
        demand_change = 0

    if abs(demand_change) > 0.3:
        sensitivity = "sensitive"
    elif abs(demand_change) > 0.1:
        sensitivity = "neutral"
    else:
        sensitivity = "insensitive"

    return {"demand_change": round(demand_change, 3), "sensitivity": sensitivity,
            "note": "基于BSR 30d vs 180d变动估算，非严格价格弹性"}

def calc_spec_comparison(asins, keepa_data, product_details, labels, target_asin):
    """Dimension 8: 功能参数对比矩阵"""
    # Gather all spec fields from Amazon Product Detail itemSpecifications
    all_params = set()
    asin_specs = {}
    for asin in asins:
        pd = product_details.get(asin, {})
        specs = pd.get("itemSpecifications", {})
        if isinstance(specs, dict):
            asin_specs[asin] = specs
            all_params.update(specs.keys())
        else:
            asin_specs[asin] = {}

    # Add Keepa physical params
    keepa_params = ["packageWeight", "packageLength", "packageWidth", "packageHeight",
                    "variationNum", "model", "manufacturer", "color", "fbaFees",
                    "profit", "referralFeePercentage", "fulfillment"]
    all_params.update(keepa_params)

    # Build comparison matrix
    matrix = []
    for param in sorted(all_params):
        row = {"param": param, "values": {}, "labels": {}}
        for asin in asins:
            # Check Amazon Detail specs first, then Keepa
            val = asin_specs.get(asin, {}).get(param)
            if val is None:
                val = keepa_data.get(asin, {}).get(param)
            row["values"][asin] = val
            row["labels"][asin] = labels.get(asin, asin)
        matrix.append(row)

    # Logistics efficiency ranking (weight + volume)
    logistics = []
    for asin in asins:
        kd = keepa_data.get(asin, {})
        try:
            weight = float(kd.get("packageWeight", 0) or 0)
            length = float(kd.get("packageLength", 0) or 0)
            width = float(kd.get("packageWidth", 0) or 0)
            height = float(kd.get("packageHeight", 0) or 0)
        except (ValueError, TypeError):
            weight = length = width = height = 0
        volume = length * width * height if all([length, width, height]) else 0
        # Efficiency score: lower weight+volume = higher efficiency
        score = 100 / (1 + weight / 100 + volume / 10000) if weight > 0 or volume > 0 else 0
        logistics.append({
            "asin": asin, "label": labels.get(asin, asin),
            "weight": weight, "volume": round(volume, 1),
            "efficiency_score": round(score, 1)
        })
    logistics.sort(key=lambda x: -x["efficiency_score"])

    # Variant strategy
    variant_strategy = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        var_num = kd.get("variationNum", 0)
        color = kd.get("color", "")
        coverage = "high" if var_num >= 5 else "medium" if var_num >= 2 else "low"
        variant_strategy[asin] = {"variation_num": var_num, "color": color, "coverage": coverage,
                                   "label": labels.get(asin, asin)}

    # OEM analysis (group by manufacturer)
    oem = {}
    for asin in asins:
        mfr = keepa_data.get(asin, {}).get("manufacturer", "")
        if mfr:
            if mfr not in oem:
                oem[mfr] = []
            oem[mfr].append(asin)

    # Cost structure
    cost = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        price = kd.get("price", 0)
        fba_fee = kd.get("fbaFees", 0)
        profit = kd.get("profit", 0)
        referral = kd.get("referralFeePercentage", 0)
        fba_pct = round(fba_fee / price * 100, 1) if price > 0 else 0
        profit_pct = round(profit / price * 100, 1) if price > 0 else 0
        # Price cut space: how much can price drop before profit = 0
        cut_space = round(profit / price * 100, 1) if price > 0 and profit > 0 else 0
        cost[asin] = {"fba_fee": fba_fee, "fba_pct": fba_pct, "profit": profit,
                      "profit_pct": profit_pct, "price_cut_space": cut_space,
                      "label": labels.get(asin, asin)}

    # Differentiation analysis (target vs others)
    target_unique = []
    target_missing = []
    common = []
    target_specs = asin_specs.get(target_asin, {})
    for param in sorted(all_params):
        target_has = param in target_specs or param in keepa_params
        others_have = any(param in asin_specs.get(a, {}) or param in keepa_data.get(a, {}) for a in asins if a != target_asin)
        if target_has and not others_have:
            target_unique.append(param)
        elif not target_has and others_have:
            target_missing.append(param)
        elif target_has and others_have:
            common.append(param)

    return {
        "matrix": matrix,
        "logistics_ranking": logistics,
        "variant_strategy": variant_strategy,
        "oem_analysis": oem,
        "cost_structure": cost,
        "differentiation": {"target_unique": target_unique, "target_missing": target_missing, "common": common}
    }

def main():
    if "--stdin" in sys.argv:
        data = json.load(sys.stdin)
    else:
        data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)

    asins = data["asins"]
    labels = data.get("labels", {})
    keepa_data = data["keepa_data"]

    # Gather sales histories
    all_sales = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        all_sales[asin] = get_sales_history(kd)

    results = {}

    # Dimension 1: Sales trend comparison
    results["sales_trend"] = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        sales = all_sales[asin]
        results["sales_trend"][asin] = {
            "label": labels.get(asin, asin),
            "trend": calc_trend(sales),
            "monthly_data": sales,
            "avg": round(sum(sales) / len(sales), 1) if sales else 0,
            "latest": sales[-1] if sales else 0,
        }

    # Dimension 2: Market share tracking
    monthly_shares, share_changes = calc_market_share(all_sales, asins)
    results["market_share"] = {
        "monthly": monthly_shares,
        "change": share_changes,
        "labels": {asin: labels.get(asin, asin) for asin in asins},
    }

    # Dimension 3: Deal impact comparison
    results["deal_impact"] = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        sales = all_sales[asin]
        deal_info = detect_deal_spike(sales)
        deal_info["label"] = labels.get(asin, asin)
        results["deal_impact"][asin] = deal_info

    # Dimension 4: Sales volatility comparison
    results["volatility"] = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        sales = all_sales[asin]
        deal_info = results["deal_impact"][asin]
        deal_months = [d["month_index"] for d in deal_info.get("deals", [])]
        cv, stability = calc_cv(sales, deal_months)
        cv_raw, _ = calc_cv(sales)
        results["volatility"][asin] = {
            "label": labels.get(asin, asin),
            "cv": cv_raw,
            "cv_excl_deal": cv,
            "stability": stability,
        }

    # Dimension 5: Seasonality sync
    peak_months, is_synced = calc_seasonality(all_sales, asins)
    results["seasonality"] = {
        "peak_months": {asin: peak_months.get(asin) for asin in asins},
        "labels": {asin: labels.get(asin, asin) for asin in asins},
        "is_synchronized": is_synced,
        "note": "如果峰值月在2个月内则判定为同步(品类季节性)" if is_synced else "峰值月分散,非品类季节性",
    }

    # Dimension 6: BSR momentum
    results["bsr_momentum"] = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        momentum = calc_bsr_momentum(kd)
        momentum["label"] = labels.get(asin, asin)
        results["bsr_momentum"][asin] = momentum

    # Dimension 7: Price-sales elasticity
    results["price_elasticity"] = {}
    for asin in asins:
        kd = keepa_data.get(asin, {})
        elasticity = calc_elasticity(kd)
        elasticity["label"] = labels.get(asin, asin)
        elasticity["price"] = kd.get("price", 0)
        results["price_elasticity"][asin] = elasticity

    # Dimension 8: Spec comparison matrix
    product_details = data.get("product_details", {})
    target_asin = data.get("target_asin", asins[0])
    results["spec_comparison"] = calc_spec_comparison(asins, keepa_data, product_details, labels, target_asin)

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
