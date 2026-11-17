#!/usr/bin/env python3
"""
Competitor Selector - 三模型评分引擎
直接竞品6维 + 上升潜力股5维 + 标杆头部5维

Usage:
  python competitor_selector.py --stdin < params.json
  python competitor_selector.py '<json params>'

Input JSON:
{
  "target": {"asin":"B0XX", "bsr":767, "reviews":2813, "price":37.99, "conv_rate":4.09, "monthly_sales":1000, "launch_date":"20240827"},
  "candidates": [
    {"asin":"B0YY", "brand":"...", "price":35.98, "bsr":1966, "reviews":708, "conv_rate":7.22,
     "monthly_sales":1000, "launch_date":"20250329",
     "sales_history":[500,500,1000,2000,3000,1000,1000],  // 6 months ago -> 1 month ago
     "rank_30":1921, "rank_180":1836, "aba_kw_count":34, "image_url":"...", "features":"..."}
  ],
  "overlap_scores": {"B0YY": 0.85},  // from S4 AIGC comparison
  "options": {"price_tolerance":0.2, "overlap_threshold":0.8}
}

Output JSON:
{
  "direct_competitors": [...],
  "rising_stars": [...],
  "benchmarks": [...],
  "summary": {"total":N, "direct":N, "rising":N, "benchmark":N}
}
"""

import json
import sys
import os
from datetime import datetime

# === Scoring Functions ===

def score_bsr_diff(comp_bsr, target_bsr):
    """直接竞品: BSR差距评分 (25%)"""
    if comp_bsr == 0:
        return 2
    diff = abs(comp_bsr - target_bsr)
    if diff <= 500: return 5
    elif diff <= 2000: return 4
    elif diff <= 5000: return 3
    elif diff <= 10000: return 2
    else: return 1

def score_reviews_ratio(comp_reviews, target_reviews):
    """直接竞品: 评论数差距评分 (20%)"""
    if comp_reviews == 0 or target_reviews == 0:
        return 1
    ratio = comp_reviews / target_reviews
    if 0.5 <= ratio <= 2.0: return 5
    elif 0.3 <= ratio <= 3.0: return 3
    else: return 1

def score_conv_diff(comp_conv, target_conv):
    """直接竞品: 转化率差距评分 (20%)"""
    if comp_conv == 0 or comp_conv is None:
        return 3
    if comp_conv <= target_conv:
        return 5  # target already better
    if comp_conv <= target_conv * 2:
        return 5  # catchable
    return 2  # far exceeds

def score_price_comp(comp_price, target_price):
    """直接竞品: 价格竞争力评分 (15%)"""
    if comp_price == 0 or target_price == 0:
        return 3
    diff_pct = (comp_price - target_price) / target_price
    if diff_pct <= 0.05: return 5
    elif diff_pct <= 0.20: return 4
    else: return 2

def score_overlap(overlap_ratio):
    """直接竞品: 功能重合度评分 (25%) — 硬门槛，<0.80直接排除"""
    if overlap_ratio < 0.80:
        return 0  # HARD EXCLUDE - not a direct competitor
    elif overlap_ratio >= 0.95: return 5  # highly similar
    elif overlap_ratio >= 0.90: return 4  # strong overlap
    elif overlap_ratio >= 0.85: return 3  # moderate overlap
    else: return 2  # 0.80-0.85, barely passing

def score_launch_proximity(comp_launch, target_launch):
    """直接竞品: 上架时间接近度评分 (10%)"""
    if not comp_launch or not target_launch:
        return 3
    try:
        comp_dt = datetime.strptime(str(comp_launch)[:8], "%Y%m%d")
        target_dt = datetime.strptime(str(target_launch)[:8], "%Y%m%d")
        diff_days = abs((comp_dt - target_dt).days)
        if diff_days <= 180: return 5
        elif diff_days <= 365: return 4
        elif diff_days <= 730: return 3
        else: return 1
    except:
        return 3

def score_direct_competitor(c, target, overlap_ratio):
    """6维可达性模型 — overlap < 0.80 硬排除"""
    # HARD GATE: overlap < 0.80 = not a direct competitor
    if overlap_ratio < 0.80:
        return {
            "score": 0,
            "scores": {"bsr": 0, "reviews": 0, "conv": 0, "price": 0, "overlap": 0, "launch": 0},
            "passed": False,
            "excluded": f"功能重合度{overlap_ratio:.0%} < 80%硬门槛，不构成直接竞品"
        }

    s_bsr = score_bsr_diff(c.get("bsr", 0), target["bsr"])
    s_rev = score_reviews_ratio(c.get("reviews", 0), target["reviews"])
    s_conv = score_conv_diff(c.get("conv_rate", 0), target["conv_rate"])
    s_price = score_price_comp(c.get("price", 0), target["price"])
    s_overlap = score_overlap(overlap_ratio)
    s_launch = score_launch_proximity(c.get("launch_date", ""), target["launch_date"])

    # New weights: overlap 25% (up from 10%), BSR 20%, reviews 15%, conv 15%, price 10%, launch 10%
    weights = {"bsr": 0.20, "reviews": 0.15, "conv": 0.15, "price": 0.10, "overlap": 0.25, "launch": 0.10}
    # Normalize to 95% (leaving 5% for bonus, which defaults to 0)
    weight_sum = sum(weights.values())
    weighted = (s_bsr * weights["bsr"] + s_rev * weights["reviews"] +
                s_conv * weights["conv"] + s_price * weights["price"] +
                s_overlap * weights["overlap"] + s_launch * weights["launch"]) / weight_sum

    return {
        "score": round(weighted, 2),
        "scores": {"bsr": s_bsr, "reviews": s_rev, "conv": s_conv, "price": s_price, "overlap": s_overlap, "launch": s_launch},
        "passed": weighted >= 3.5,
        "overlap_ratio": round(overlap_ratio, 3)
    }

# === Rising Star Functions ===

def analyze_sales_trend(sales_history):
    """Analyze 6-month sales history, return (slope, growth_ratio, has_deal_spike, recent_avg)"""
    if not sales_history or len(sales_history) < 4:
        return 0, 0, False, 0

    # Use last 3 completed months vs previous 3
    recent_3 = sales_history[-3:] if len(sales_history) >= 3 else sales_history
    older_3 = sales_history[-6:-3] if len(sales_history) >= 6 else sales_history[:3]

    recent_avg = sum(recent_3) / len(recent_3) if recent_3 else 0
    older_avg = sum(older_3) / len(older_3) if older_3 else 0

    growth = recent_avg / older_avg if older_avg > 0 else 0

    # Linear regression on last 4 months
    last_4 = sales_history[-4:] if len(sales_history) >= 4 else sales_history
    n = len(last_4)
    x_mean = (n - 1) / 2
    y_mean = sum(last_4) / n if n > 0 else 0
    num = sum((i - x_mean) * (s - y_mean) for i, s in enumerate(last_4))
    den = sum((i - x_mean) ** 2 for i in range(n))
    slope = num / den if den != 0 else 0

    # Deal spike detection
    has_deal_spike = False
    for i in range(1, len(sales_history) - 1):
        if sales_history[i] > 0:
            surrounding = [sales_history[i-1], sales_history[i+1]]
            s_avg = sum(surrounding) / 2 if sum(surrounding) > 0 else 0.1
            if sales_history[i] >= s_avg * 3:
                if i + 2 < len(sales_history):
                    next_two = (sales_history[i+1] + sales_history[i+2]) / 2
                    if next_two < sales_history[i] * 0.3:
                        has_deal_spike = True

    return slope, growth, has_deal_spike, recent_avg

def check_rising_star_exclusions(c):
    """Check hard exclusions for rising star"""
    sales_history = c.get("sales_history", [])
    slope, growth, deal_spike, recent_avg = analyze_sales_trend(sales_history)

    if recent_avg == 0:
        return False, "近3月均销量=0(断货)"
    if deal_spike:
        return False, "Deal尖峰后回落"

    bsr = c.get("bsr", 0)
    if bsr > 50000:
        return False, f"BSR={bsr}过高"

    launch = c.get("launch_date", "")
    if launch:
        try:
            dt = datetime.strptime(str(launch)[:8], "%Y%m%d")
            months = (datetime.now() - dt).days / 30
            if months < 3:
                return False, f"上架仅{months:.0f}月"
        except:
            pass

    return True, "通过"

def score_rising_star(c, target):
    """5维增长性模型"""
    passed, reason = check_rising_star_exclusions(c)
    if not passed:
        return {"score": 0, "scores": {}, "passed": False, "excluded": reason}

    sales_history = c.get("sales_history", [])
    slope, growth, deal_spike, recent_avg = analyze_sales_trend(sales_history)

    # 1. Sales trend (35%)
    if slope > 0 and growth >= 2.0:
        s_sales = 5
    elif slope > 0 and growth >= 1.5:
        s_sales = 4
    elif slope > 0:
        s_sales = 3
    elif abs(slope) < 0.5:
        s_sales = 2
    else:
        s_sales = 1

    # 2. Review space (20%)
    reviews = c.get("reviews", 0)
    if reviews < 50: s_rev = 1
    elif reviews <= 300: s_rev = 5
    elif reviews <= 800: s_rev = 4
    elif reviews <= 1500: s_rev = 3
    else: s_rev = 2

    # 3. BSR improvement (20%)
    r30 = c.get("rank_30", 0)
    r180 = c.get("rank_180", 0)
    if r30 == 0 or r180 == 0:
        s_bsr = 3
    else:
        ratio = r30 / r180
        if ratio < 0.5: s_bsr = 5
        elif ratio < 0.8: s_bsr = 4
        elif ratio < 1.0: s_bsr = 3
        elif ratio < 1.2: s_bsr = 2
        else: s_bsr = 1

    # 4. Conversion (15%)
    conv = c.get("conv_rate", 0)
    if conv == 0:
        s_conv = 3
    elif conv > target["conv_rate"] * 1.5: s_conv = 5
    elif conv > target["conv_rate"] * 1.2: s_conv = 4
    elif conv > target["conv_rate"] * 0.8: s_conv = 3
    elif conv > target["conv_rate"] * 0.5: s_conv = 2
    else: s_conv = 1

    # 5. Launch time (10%)
    launch = c.get("launch_date", "")
    s_launch = 3
    if launch:
        try:
            dt = datetime.strptime(str(launch)[:8], "%Y%m%d")
            months = (datetime.now() - dt).days / 30
            if months < 3: s_launch = 1
            elif months <= 12: s_launch = 5
            elif months <= 18: s_launch = 4
            elif months <= 24: s_launch = 3
            elif months <= 36: s_launch = 2
            else: s_launch = 1
        except:
            pass

    weights = {"sales": 0.35, "reviews": 0.20, "bsr": 0.20, "conv": 0.15, "launch": 0.10}
    weighted = (s_sales * weights["sales"] + s_rev * weights["reviews"] +
                s_bsr * weights["bsr"] + s_conv * weights["conv"] + s_launch * weights["launch"])

    return {
        "score": round(weighted, 2),
        "scores": {"sales": s_sales, "reviews": s_rev, "bsr": s_bsr, "conv": s_conv, "launch": s_launch},
        "passed": weighted >= 3.5,
        "sales_data": {"history": sales_history, "slope": round(slope, 2), "growth": round(growth, 2), "recent_avg": round(recent_avg, 1)}
    }

# === Benchmark Functions ===

def check_benchmark_gate(c, target):
    """Check hard gate: at least 1 dimension significantly ahead"""
    reviews = c.get("reviews", 0)
    aba = c.get("aba_kw_count", 0)
    sales_history = c.get("sales_history", [])
    _, _, _, recent_avg = analyze_sales_trend(sales_history)
    bsr = c.get("bsr", 0)

    ahead = False
    if reviews >= target["reviews"] * 1.5: ahead = True
    if aba >= 5: ahead = True
    if recent_avg >= target["monthly_sales"] * 1.5: ahead = True
    if bsr < target["bsr"]: ahead = True

    return ahead

def score_benchmark(c, target):
    """5维领先度模型"""
    if not check_benchmark_gate(c, target):
        return {"score": 0, "scores": {}, "passed": False, "excluded": "无显著领先维度"}

    # 1. BSR leadership (25%)
    bsr = c.get("bsr", 0)
    if bsr == 0:
        s_bsr = 2
    elif bsr < target["bsr"]:
        ratio = bsr / target["bsr"]
        if ratio <= 0.2: s_bsr = 5
        elif ratio <= 0.3: s_bsr = 4
        elif ratio <= 0.5: s_bsr = 3
        elif ratio <= 0.8: s_bsr = 2
        else: s_bsr = 1
    else:
        ratio = bsr / target["bsr"]
        if ratio <= 1.5: s_bsr = 3
        elif ratio <= 3: s_bsr = 2
        else: s_bsr = 1

    # 2. Review wall (20%)
    reviews = c.get("reviews", 0)
    ratio = reviews / target["reviews"] if target["reviews"] > 0 else 0
    if ratio >= 5: s_rev = 5
    elif ratio >= 3: s_rev = 4
    elif ratio >= 2: s_rev = 3
    elif ratio >= 1.5: s_rev = 2
    else: s_rev = 1

    # 3. Sales scale (20%)
    sales_history = c.get("sales_history", [])
    _, _, _, recent_avg = analyze_sales_trend(sales_history)
    ratio = recent_avg / target["monthly_sales"] if target["monthly_sales"] > 0 else 0
    if ratio >= 3: s_sales = 5
    elif ratio >= 2: s_sales = 4
    elif ratio >= 1.5: s_sales = 3
    elif ratio >= 1: s_sales = 2
    else: s_sales = 1

    # 4. ABA dominance (20%)
    aba = c.get("aba_kw_count", 0)
    if aba >= 20: s_aba = 5
    elif aba >= 10: s_aba = 4
    elif aba >= 5: s_aba = 3
    elif aba >= 1: s_aba = 2
    else: s_aba = 1

    # 5. Price relevance (15%)
    price = c.get("price", 0)
    if price == 0 or target["price"] == 0:
        s_price = 3
    else:
        ratio = price / target["price"]
        if 0.7 <= ratio <= 1.3: s_price = 5
        elif 0.5 <= ratio <= 2.0: s_price = 4
        elif 0.3 <= ratio <= 3.0: s_price = 3
        elif 0.2 <= ratio <= 5.0: s_price = 2
        else: s_price = 1

    weights = {"bsr": 0.25, "reviews": 0.20, "sales": 0.20, "aba": 0.20, "price": 0.15}
    weighted = (s_bsr * weights["bsr"] + s_rev * weights["reviews"] +
                s_sales * weights["sales"] + s_aba * weights["aba"] + s_price * weights["price"])

    # Identify lead dimensions
    leads = []
    if reviews >= target["reviews"] * 1.5: leads.append(f"评论{reviews/target['reviews']:.1f}x")
    if aba >= 5: leads.append(f"ABA {aba}词")
    if recent_avg >= target["monthly_sales"] * 1.5: leads.append(f"销量{recent_avg/target['monthly_sales']:.1f}x")
    if bsr < target["bsr"] and bsr > 0: leads.append(f"BSR领先{1-bsr/target['bsr']:.0%}")

    return {
        "score": round(weighted, 2),
        "scores": {"bsr": s_bsr, "reviews": s_rev, "sales": s_sales, "aba": s_aba, "price": s_price},
        "passed": weighted >= 3.5,
        "leads": leads
    }

# === Main ===

def main():
    # Read input
    if "--stdin" in sys.argv:
        data = json.load(sys.stdin)
    else:
        data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)

    target = data["target"]
    candidates = data["candidates"]
    overlap_scores = data.get("overlap_scores", {})
    options = data.get("options", {})

    # VALIDATION: overlap_scores must be provided for all candidates (S4 AIGC comparison is mandatory)
    missing_overlap = [c["asin"] for c in candidates if c["asin"] not in overlap_scores]
    if missing_overlap:
        # Candidates without overlap scores can only participate in benchmark/rising star scoring
        # They CANNOT be direct competitors (S4 AIGC comparison was skipped)
        pass  # Will be handled per-candidate below

    direct_results = []
    rising_results = []
    benchmark_results = []

    for c in candidates:
        asin = c["asin"]
        # Overlap score MUST come from S4 AIGC comparison - no defaults allowed
        overlap = overlap_scores.get(asin, None)
        if overlap is None:
            # No AIGC comparison performed - cannot be direct competitor
            overlap = -1  # Flag as "not evaluated"

        # Score all three models
        direct = score_direct_competitor(c, target, overlap)
        if direct["passed"]:
            entry = {"asin": asin, "brand": c.get("brand", ""), "price": c.get("price", 0),
                     "bsr": c.get("bsr", 0), "reviews": c.get("reviews", 0),
                     "conv_rate": c.get("conv_rate", 0), "score": direct["score"],
                     "scores": direct["scores"]}
            direct_results.append(entry)

        rising = score_rising_star(c, target)
        if rising["passed"]:
            entry = {"asin": asin, "brand": c.get("brand", ""), "price": c.get("price", 0),
                     "reviews": c.get("reviews", 0), "score": rising["score"],
                     "scores": rising["scores"], "sales_data": rising.get("sales_data", {})}
            rising_results.append(entry)

        bench = score_benchmark(c, target)
        if bench["passed"]:
            entry = {"asin": asin, "brand": c.get("brand", ""), "price": c.get("price", 0),
                     "bsr": c.get("bsr", 0), "reviews": c.get("reviews", 0),
                     "score": bench["score"], "scores": bench["scores"], "leads": bench.get("leads", [])}
            benchmark_results.append(entry)

    # Sort by score descending
    direct_results.sort(key=lambda x: -x["score"])
    rising_results.sort(key=lambda x: -x["score"])
    benchmark_results.sort(key=lambda x: -x["score"])

    # Limit quantities
    max_direct = 5
    max_rising = 2
    max_benchmark = 2
    max_total = options.get("max_competitors", 10)

    direct_results = direct_results[:max_direct]
    rising_results = rising_results[:max_rising]
    benchmark_results = benchmark_results[:max_benchmark]

    # If no benchmark passed, take top 1 as quasi-benchmark
    if not benchmark_results and candidates:
        for c in candidates:
            bench = score_benchmark(c, target)
            if bench["score"] > 0:
                benchmark_results = [{
                    "asin": c["asin"], "brand": c.get("brand", ""),
                    "price": c.get("price", 0), "bsr": c.get("bsr", 0),
                    "reviews": c.get("reviews", 0), "score": bench["score"],
                    "scores": bench["scores"], "leads": bench.get("leads", []),
                    "note": "准标杆(未达3.5分门槛,取最高分)"
                }]
                break

    # Ensure total doesn't exceed max
    while len(direct_results) + len(rising_results) + len(benchmark_results) > max_total:
        if len(direct_results) > 3:
            direct_results.pop()
        elif len(rising_results) > 1:
            rising_results.pop()
        elif len(benchmark_results) > 1:
            benchmark_results.pop()
        else:
            break

    output = {
        "target_asin": target["asin"],
        "product_type": data.get("product_type", "standard"),
        "search_date": datetime.now().strftime("%Y-%m-%d"),
        "direct_competitors": direct_results,
        "rising_stars": rising_results,
        "benchmarks": benchmark_results,
        "summary": {
            "total": len(direct_results) + len(rising_results) + len(benchmark_results),
            "direct": len(direct_results),
            "rising": len(rising_results),
            "benchmark": len(benchmark_results)
        }
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
