#!/usr/bin/env python3
"""
competitor-reverse-analysis S3: 量化分析脚本
读取 S1（4 源）+ S2（可选）的 JSON 输出，计算 10 个分析维度，输出统一 JSON。
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from statistics import mean, median, stdev

# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def load_json(path):
    if not path or not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_float(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default

def safe_int(v, default=None):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default

def extract_timeseries(keepa_data, field_name):
    """从 Keepa Series 响应中提取时间序列 [{time, value}, ...]
    Keepa Series 顶层字段直接是时间序列: buyboxPrice, rating, ratingCount, monthlySold
    bsrSub 结构特殊: [{categoryName, points: [{time, value}]}]
    """
    if not keepa_data or not isinstance(keepa_data, dict):
        return []
    # bsrSub special case: [{categoryName, points: [{time, value}]}]
    if field_name == "salesRank" or field_name == "bsrSub":
        bsr_sub = keepa_data.get("bsrSub", [])
        if bsr_sub and isinstance(bsr_sub, list) and isinstance(bsr_sub[0], dict):
            return bsr_sub[0].get("points", [])
        return []
    # Direct top-level field
    series = keepa_data.get(field_name, [])
    return series if isinstance(series, list) else []

def extract_sorftime_trend(sorftime_data, field_name):
    """从 Sorftime 响应中提取趋势数组
    Sorftime 数据在 products[0] 下, trend 格式为 [date_int, value, date_int, value, ...]
    bsrRankTrend 格式特殊: [{NodeId, Rank: [date_int, rank, ...]}]
    """
    if not sorftime_data or not isinstance(sorftime_data, dict):
        return []
    products = sorftime_data.get("products", [])
    if not products or not isinstance(products[0], dict):
        return []
    p = products[0]
    # bsrRankTrend special case
    if field_name == "bsrRankTrend":
        bsr = p.get("bsrRankTrend", [])
        if bsr and isinstance(bsr, list) and isinstance(bsr[0], dict):
            return bsr[0].get("Rank", [])
        return []
    trend = p.get(field_name, [])
    return trend if isinstance(trend, list) else []

def ts_to_pairs(ts):
    """将 [{time, value}, ...] 转为 [(time_str, value), ...]
    Keepa time 字段为字符串如 '2025-06-25 01:40'
    """
    pairs = []
    for p in ts:
        if isinstance(p, dict):
            t = p.get("time") or p.get("timestamp") or p.get("x")
            v = p.get("value") if p.get("value") is not None else p.get("y")
            if t is not None and v is not None:
                pairs.append((t, safe_float(v)))
        elif isinstance(p, (list, tuple)) and len(p) >= 2:
            pairs.append((p[0], safe_float(p[1])))
    return pairs

def sorftime_trend_to_pairs(trend):
    """将 [date, value, ...] 交错数组转为 [(date_str, value), ...]"""
    pairs = []
    for i in range(0, len(trend) - 1, 2):
        d = trend[i]
        v = safe_float(trend[i + 1])
        if v is not None and v != -1:
            pairs.append((d, v))
    return pairs

def month_key(ts_or_str):
    """从 timestamp (ms), date string '2025-06-25 01:40', or int 20260724 提取 YYYY-MM"""
    if isinstance(ts_or_str, (int, float)):
        # Could be timestamp in ms or YYYYMMDD format
        if ts_or_str > 1e12:  # timestamp in ms
            dt = datetime.fromtimestamp(ts_or_str / 1000)
        elif ts_or_str > 10000000:  # YYYYMMDD format
            s = str(int(ts_or_str))
            try:
                dt = datetime.strptime(s, "%Y%m%d")
            except ValueError:
                return None
        else:
            return None
    elif isinstance(ts_or_str, str):
        s = ts_or_str.strip()[:10]
        try:
            dt = datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            try:
                dt = datetime.strptime(s, "%Y%m%d")
            except ValueError:
                return None
    else:
        return None
    return dt.strftime("%Y-%m")

def resolve_data_path(slug):
    """尝试将结果落盘到会话目录"""
    cwd = os.environ.get("ACPX_WORKSPACES", os.getcwd())
    session = os.environ.get("SESSION_ID", "default")
    today = datetime.now().strftime("%Y-%m-%d")
    d = os.path.join(cwd, "linkfox", today, session, "data")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, slug)

# ---------------------------------------------------------------------------
# Analysis modules
# ---------------------------------------------------------------------------

def analyze_price_strategy(keepa_series, sorftime):
    """1. 价格策略：三阶段演变 + 弹性 + 促销"""
    prices = ts_to_pairs(extract_timeseries(keepa_series, "buyBoxPrice"))
    if not prices:
        # Fallback: Sorftime priceTrend
        prices = sorftime_trend_to_pairs(extract_sorftime_trend(sorftime, "priceTrend"))

    if not prices:
        return {"status": "no_data", "stages": [], "elasticity": None, "promo_types": []}

    n = len(prices)
    third = max(1, n // 3)
    segments = [prices[:third], prices[third:2*third], prices[2*third:]]

    stages = []
    for i, seg in enumerate(segments):
        vals = [v for _, v in seg if v is not None and v > 0]
        if not vals:
            continue
        stages.append({
            "period": f"stage_{i+1}",
            "start": seg[0][0] if seg else None,
            "end": seg[-1][0] if seg else None,
            "mean": round(mean(vals), 2),
            "median": round(median(vals), 2),
            "std": round(stdev(vals), 2) if len(vals) > 1 else 0,
        })

    # Price elasticity: simple regression Δsales ~ Δprice (if sales data available)
    elasticity = None  # Requires sales data; agent can compute in S4 if needed

    # Detect promo types from price drops
    promo_types = []
    if len(prices) > 2:
        for i in range(1, len(prices)):
            prev, curr = prices[i-1][1], prices[i][1]
            if prev and curr and prev > 0:
                drop_pct = (prev - curr) / prev * 100
                if drop_pct > 20:
                    promo_types.append({"date": prices[i][0], "drop_pct": round(drop_pct, 1)})

    return {
        "status": "ok",
        "stages": stages,
        "elasticity": elasticity,
        "promo_types": promo_types[:20],
    }

def analyze_deal_effectiveness(keepa_series, sorftime):
    """2. Deal 效果：前后 BSR 对比 + 回落 + 恢复"""
    deal_trend = extract_sorftime_trend(sorftime, "dealTrend")
    bsr_pairs = ts_to_pairs(extract_timeseries(keepa_series, "salesRank"))
    if not bsr_pairs:
        bsr_pairs = sorftime_trend_to_pairs(extract_sorftime_trend(sorftime, "bsrRankTrend"))

    if not deal_trend or not bsr_pairs:
        return {"status": "no_data", "deals": []}

    # Parse deal events (Sorftime dealTrend is [date, type, date, type, ...] or [date, value, ...])
    deals = []
    for i in range(0, len(deal_trend) - 1, 2):
        deal_date = deal_trend[i]
        deal_val = deal_trend[i + 1] if i + 1 < len(deal_trend) else None
        if deal_val is None or deal_val == 0:
            continue

        # Find BSR around deal date
        deal_dt = None
        if isinstance(deal_date, str):
            try:
                deal_dt = datetime.strptime(deal_date[:10], "%Y-%m-%d")
            except ValueError:
                continue
        elif isinstance(deal_date, (int, float)):
            deal_dt = datetime.fromtimestamp(deal_date / 1000)
        else:
            continue

        bsr_during = []
        bsr_after = []
        for ts, val in bsr_pairs:
            if isinstance(ts, (int, float)):
                dt = datetime.fromtimestamp(ts / 1000)
            elif isinstance(ts, str):
                try:
                    dt = datetime.strptime(ts[:10], "%Y-%m-%d")
                except ValueError:
                    continue
            else:
                continue
            delta = (dt - deal_dt).days
            if -3 <= delta <= 3:
                bsr_during.append(val)
            elif 4 <= delta <= 10:
                bsr_after.append(val)

        if bsr_during and bsr_after:
            bsr_min = min(bsr_during)
            bsr_after_mean = mean(bsr_after)
            drop_pct = ((bsr_after_mean - bsr_min) / bsr_min * 100) if bsr_min > 0 else 0
            deals.append({
                "date": str(deal_date)[:10],
                "bsr_during_min": round(bsr_min),
                "bsr_after_7d_avg": round(bsr_after_mean),
                "drop_pct": round(drop_pct, 1),
                "recovery_days": None,
            })

    return {"status": "ok" if deals else "no_events", "deals": deals}

def analyze_review_anomaly(keepa_series, sorftime):
    """3. 评论异常检测"""
    rc_pairs = ts_to_pairs(extract_timeseries(keepa_series, "ratingCount"))
    if not rc_pairs:
        rc_pairs = sorftime_trend_to_pairs(extract_sorftime_trend(sorftime, "ratingCountTrend"))

    if not rc_pairs or len(rc_pairs) < 2:
        return {"status": "no_data", "anomalies": [], "monthly": [], "rating_trend": []}

    # Daily increments
    anomalies = []
    for i in range(1, len(rc_pairs)):
        delta = (rc_pairs[i][1] or 0) - (rc_pairs[i-1][1] or 0)
        if delta > 20:
            anomalies.append({"date": str(rc_pairs[i][0])[:10], "count": round(delta)})

    # Monthly aggregation
    monthly_map = {}
    for ts, val in rc_pairs:
        mk = month_key(ts)
        if mk:
            if mk not in monthly_map:
                monthly_map[mk] = []
            monthly_map[mk].append(val)
    monthly = []
    prev = None
    for mk in sorted(monthly_map.keys()):
        vals = monthly_map[mk]
        current = vals[-1] if vals else 0
        delta = (current - prev) if prev is not None else 0
        monthly.append({"month": mk, "delta": round(delta)})
        prev = current

    # Rating trend
    rating_pairs = ts_to_pairs(extract_timeseries(keepa_series, "rating"))
    rating_trend = [{"date": str(t)[:10], "rating": round(v, 2)} for t, v in rating_pairs[-20:]]

    return {
        "status": "ok",
        "anomalies": anomalies[:20],
        "monthly": monthly,
        "rating_trend": rating_trend,
    }

def analyze_lifecycle(keepa_series, sorftime):
    """4. 生命周期阶段判定"""
    sales_pairs = ts_to_pairs(extract_timeseries(keepa_series, "monthlySales"))
    if not sales_pairs:
        sales_pairs = sorftime_trend_to_pairs(extract_sorftime_trend(sorftime, "salesTrend"))

    if not sales_pairs or len(sales_pairs) < 3:
        return {"status": "no_data", "stages": []}

    vals = [v for _, v in sales_pairs if v is not None and v > 0]
    if not vals:
        return {"status": "no_data", "stages": []}

    avg_val = mean(vals)
    stages = []
    current_stage = "unknown"
    stage_start = sales_pairs[0][0]

    for i, (ts, val) in enumerate(sales_pairs):
        if val is None or val <= 0:
            continue
        ratio = val / avg_val if avg_val > 0 else 1

        if ratio < 0.5:
            label = "introduction"
        elif i > 0 and sales_pairs[i-1][1] and val > sales_pairs[i-1][1] * 1.2:
            label = "growth"
        elif 0.9 <= ratio <= 1.1:
            label = "maturity"
        elif i > 0 and sales_pairs[i-1][1] and val < sales_pairs[i-1][1] * 0.8:
            label = "decline"
        else:
            label = current_stage

        if label != current_stage and label != "unknown":
            if current_stage != "unknown":
                stages.append({
                    "name": current_stage,
                    "start": str(stage_start)[:10],
                    "end": str(ts)[:10],
                })
            current_stage = label
            stage_start = ts

    if current_stage != "unknown":
        stages.append({
            "name": current_stage,
            "start": str(stage_start)[:10],
            "end": str(sales_pairs[-1][0])[:10],
        })

    return {"status": "ok", "stages": stages, "avg_sales": round(avg_val)}

def analyze_bsr_volatility(keepa_series, sorftime):
    """5. BSR 月度波动"""
    bsr_pairs = ts_to_pairs(extract_timeseries(keepa_series, "salesRank"))
    if not bsr_pairs:
        bsr_pairs = sorftime_trend_to_pairs(extract_sorftime_trend(sorftime, "bsrRankTrend"))

    if not bsr_pairs:
        return {"status": "no_data", "monthly": [], "subcategory": None}

    monthly_map = {}
    for ts, val in bsr_pairs:
        mk = month_key(ts)
        if mk and val is not None and val > 0:
            if mk not in monthly_map:
                monthly_map[mk] = []
            monthly_map[mk].append(val)

    monthly = []
    for mk in sorted(monthly_map.keys()):
        vals = monthly_map[mk]
        monthly.append({
            "month": mk,
            "mean": round(mean(vals)),
            "median": round(median(vals)),
            "std": round(stdev(vals)) if len(vals) > 1 else 0,
            "cv": round(stdev(vals) / mean(vals) * 100, 1) if len(vals) > 1 and mean(vals) > 0 else 0,
        })

    # Extract subcategory from Keepa bsrSub
    subcategory = None
    if isinstance(keepa_series, dict):
        bsr_sub = keepa_series.get("bsrSub", [])
        if bsr_sub and isinstance(bsr_sub, list) and isinstance(bsr_sub[0], dict):
            subcategory = bsr_sub[0].get("categoryName")

    return {"status": "ok", "monthly": monthly, "subcategory": subcategory}

def analyze_traffic_structure(sif_summary, sif_keywords):
    """6. 流量结构分析"""
    result = {"status": "no_data", "natural_ratio": None, "paid_ratio": None,
              "kw_in": None, "kw_out": None, "ac_count": None, "top_keywords": []}

    summary_data = sif_summary
    if isinstance(summary_data, dict) and "data" in summary_data:
        summary_data = summary_data["data"]
    if isinstance(summary_data, list) and summary_data:
        summary_data = summary_data[0] if isinstance(summary_data[0], dict) else {}
    elif not isinstance(summary_data, dict):
        summary_data = {}

    if summary_data:
        result["status"] = "ok"
        result["natural_ratio"] = safe_float(summary_data.get("naturalSearchExposureRatio"))
        result["paid_ratio"] = safe_float(summary_data.get("sponsoredProductsExposureRatio"))
        result["kw_in"] = safe_int(summary_data.get("totalTrafficKeywordCountIn"))
        result["kw_out"] = safe_int(summary_data.get("totalTrafficKeywordCountOut"))
        result["ac_count"] = safe_int(summary_data.get("amazonsChoiceKeywordCount"))
        result["ac_exposure"] = safe_float(summary_data.get("amazonsChoiceExposureScore"))
        result["total_kw"] = safe_int(summary_data.get("totalTrafficKeywordCount"))
        result["total_exposure"] = safe_float(summary_data.get("totalExposureScore"))

    # Top keywords from SIF Keywords
    kw_data = sif_keywords
    if isinstance(kw_data, dict) and "data" in kw_data:
        kw_data = kw_data["data"]
    if isinstance(kw_data, list):
        sorted_kws = sorted(kw_data, key=lambda x: safe_float(x.get("trafficShare", 0), 0), reverse=True)
        result["top_keywords"] = [
            {
                "keyword": kw.get("keyword", ""),
                "traffic_share": safe_float(kw.get("trafficShare")),
                "natural_rank": safe_int(kw.get("productNaturalRank")),
                "ad_rank": safe_int(kw.get("productAdRank")),
                "search_volume": safe_int(kw.get("weeklySearchVolume")),
                "conversion_rate": safe_float(kw.get("clickToPurchaseConversionRate")),
            }
            for kw in sorted_kws[:10]
        ]
        if result["status"] == "no_data":
            result["status"] = "partial"

    return result

def analyze_sales_seasonality(keepa_series, sorftime):
    """7. 销量季节性"""
    sales_pairs = ts_to_pairs(extract_timeseries(keepa_series, "monthlySales"))
    if not sales_pairs:
        sales_pairs = sorftime_trend_to_pairs(extract_sorftime_trend(sorftime, "salesTrend"))

    if not sales_pairs:
        return {"status": "no_data", "monthly": [], "peak_months": [], "trough_months": []}

    monthly_map = {}
    for ts, val in sales_pairs:
        mk = month_key(ts)
        if mk and val is not None and val > 0:
            if mk not in monthly_map:
                monthly_map[mk] = []
            monthly_map[mk].append(val)

    monthly = []
    for mk in sorted(monthly_map.keys()):
        vals = monthly_map[mk]
        daily_avg = mean(vals)
        total = sum(vals)
        monthly.append({"month": mk, "daily_avg": round(daily_avg), "total": round(total)})

    # Compute MoM growth
    for i in range(1, len(monthly)):
        prev_total = monthly[i-1]["total"]
        if prev_total > 0:
            monthly[i]["mom_growth"] = round((monthly[i]["total"] - prev_total) / prev_total * 100, 1)
        else:
            monthly[i]["mom_growth"] = None

    # Peak / trough
    if monthly:
        avg_total = mean([m["total"] for m in monthly])
        peak_months = [m["month"] for m in monthly if m["total"] > avg_total * 1.2]
        trough_months = [m["month"] for m in monthly if m["total"] < avg_total * 0.8]
    else:
        peak_months, trough_months = [], []

    return {
        "status": "ok",
        "monthly": monthly,
        "peak_months": peak_months,
        "trough_months": trough_months,
    }

def analyze_kpi_overview(keepa_product, sorftime):
    """8. KPI 总览"""
    # Extract products[0] from Keepa Product response
    kp = {}
    if isinstance(keepa_product, dict):
        products = keepa_product.get("products", [])
        if products and isinstance(products[0], dict):
            kp = products[0]
        elif "price" in keepa_product or "rating" in keepa_product:
            kp = keepa_product

    # Extract products[0] from Sorftime response
    sorf = {}
    if isinstance(sorftime, dict):
        products = sorftime.get("products", [])
        if products and isinstance(products[0], dict):
            sorf = products[0]
        elif "price" in sorftime or "rating" in sorftime:
            sorf = sorftime

    price = safe_float(kp.get("price")) or safe_float(kp.get("currentPrice")) or safe_float(sorf.get("currentPrice"))
    fba_fee = safe_float(kp.get("fbaFee")) or safe_float(sorf.get("fbaFee"))
    rating = safe_float(kp.get("rating")) or safe_float(sorf.get("rating"))
    review_count = safe_int(kp.get("reviewCount")) or safe_int(kp.get("ratingCount")) or safe_int(sorf.get("reviewCount"))
    bsr = safe_int(kp.get("salesRank")) or safe_int(sorf.get("currentBsr"))

    # Monthly sales
    monthly_sales = None
    if kp.get("monthlySales"):
        ms = kp["monthlySales"]
        if isinstance(ms, list) and ms:
            monthly_sales = safe_int(ms[-1]) if isinstance(ms[-1], (int, float)) else safe_int(ms[-1].get("value"))
        elif isinstance(ms, (int, float)):
            monthly_sales = safe_int(ms)
    if not monthly_sales:
        monthly_sales = safe_int(sorf.get("monthlySales"))

    # Profit margin (if price and fba_fee available)
    profit_margin = None
    if price and price > 0 and fba_fee is not None:
        referral_fee = price * 0.15  # Default 15% referral
        profit = price - fba_fee - referral_fee
        profit_margin = round(profit / price * 100, 1)

    result = {
        "status": "ok" if price else "partial",
        "price": price,
        "fba_fee": fba_fee,
        "rating": rating,
        "review_count": review_count,
        "bsr": bsr,
        "monthly_sales": monthly_sales,
        "profit_margin": profit_margin,
    }

    # Add BSR averages if available from S2
    avg30 = safe_int(kp.get("avg30"))
    avg90 = safe_int(kp.get("avg90"))
    avg180 = safe_int(kp.get("avg180"))
    if avg30:
        result["bsr_avg_30d"] = avg30
    if avg90:
        result["bsr_avg_90d"] = avg90
    if avg180:
        result["bsr_avg_180d"] = avg180

    return result

def analyze_timeline(keepa_product, keepa_series):
    """9. 关键时间线"""
    kp = {}
    if isinstance(keepa_product, dict):
        products = keepa_product.get("products", [])
        if products and isinstance(products[0], dict):
            kp = products[0]
        elif "availableDate" in keepa_product or "listedSince" in keepa_product:
            kp = keepa_product

    listed_since = kp.get("listedSince") or kp.get("releaseDate")

    # First sale from Keepa Series
    sales_pairs = ts_to_pairs(extract_timeseries(keepa_series, "monthlySales"))
    first_sale = None
    for ts, val in sales_pairs:
        if val and val > 0:
            first_sale = str(ts)[:10] if isinstance(ts, str) else datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
            break

    # BSR milestones
    bsr_pairs = ts_to_pairs(extract_timeseries(keepa_series, "salesRank"))
    milestones = []
    targets = [1000, 500, 100]
    achieved = set()
    for ts, val in bsr_pairs:
        if val and val > 0:
            for t in targets:
                if t not in achieved and val <= t:
                    achieved.add(t)
                    dt_str = str(ts)[:10] if isinstance(ts, str) else datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
                    milestones.append({"date": dt_str, "bsr": round(val), "label": f"Top {t}"})

    return {
        "status": "ok",
        "listed_since": str(listed_since)[:10] if listed_since else None,
        "first_sale": first_sale,
        "milestones": milestones,
    }

def analyze_swot(all_results):
    """10. SWOT 综合研判"""
    strengths, weaknesses, opportunities, threats = [], [], [], []

    # Traffic
    ts = all_results.get("traffic_structure", {})
    nat = ts.get("natural_ratio")
    paid = ts.get("paid_ratio")
    kw_in = ts.get("kw_in")
    kw_out = ts.get("kw_out")
    if nat and nat > 0.7:
        strengths.append(f"自然流量占比 {nat*100:.0f}%，流量底盘扎实")
    if paid and paid > 0.5:
        weaknesses.append(f"广告依赖度 {paid*100:.0f}%，付费驱动型")
    if kw_in is not None and kw_out is not None and kw_in > kw_out:
        opportunities.append(f"关键词净增 {kw_in - kw_out} 个，流量扩张中")
    elif kw_in is not None and kw_out is not None and kw_out > kw_in:
        threats.append(f"关键词净流失 {kw_out - kw_in} 个，流量收缩")

    # Rating
    kpi = all_results.get("kpi_overview", {})
    rating = kpi.get("rating")
    if rating and rating > 4.2:
        strengths.append(f"评分 {rating}，口碑良好")
    elif rating and rating < 3.8:
        weaknesses.append(f"评分 {rating}，口碑风险")

    # Review anomaly
    ra = all_results.get("review_anomaly", {})
    anomalies = ra.get("anomalies", [])
    if anomalies:
        weaknesses.append(f"检测到 {len(anomalies)} 次评论异常激增（>20条/天）")

    # Lifecycle
    lc = all_results.get("lifecycle", {})
    stages = lc.get("stages", [])
    if stages:
        last_stage = stages[-1].get("name", "")
        if last_stage == "decline":
            threats.append("生命周期进入衰退期")
        elif last_stage == "growth":
            opportunities.append("生命周期处于成长期")

    # BSR trend
    bsr = all_results.get("bsr_volatility", {})
    monthly_bsr = bsr.get("monthly", [])
    if len(monthly_bsr) >= 2:
        recent = monthly_bsr[-1]["mean"]
        prev = monthly_bsr[-2]["mean"]
        if recent < prev:
            strengths.append("BSR 近月环比改善")
        else:
            threats.append("BSR 近月环比恶化")

    # Seasonality
    season = all_results.get("sales_seasonality", {})
    peaks = season.get("peak_months", [])
    if peaks:
        opportunities.append(f"存在季节性高峰月：{', '.join(peaks[-3:])}")

    # Deal
    deal = all_results.get("deal_effectiveness", {})
    deals = deal.get("deals", [])
    if deals:
        avg_drop = mean([d.get("drop_pct", 0) for d in deals])
        if avg_drop < 50:
            opportunities.append(f"Deal 后 BSR 回落幅度仅 {avg_drop:.0f}%，恢复能力强")
        else:
            weaknesses.append(f"Deal 后 BSR 回落幅度 {avg_drop:.0f}%，依赖促销")

    return {
        "status": "ok",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "opportunities": opportunities,
        "threats": threats,
    }

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-reverse-analysis S3: 量化分析")
    parser.add_argument("--keepa-series", default=None, help="S1.1 Keepa Series JSON")
    parser.add_argument("--sorftime", default=None, help="S1.2 Sorftime JSON")
    parser.add_argument("--sif-keywords", default=None, help="S1.3 SIF Keywords JSON")
    parser.add_argument("--sif-summary", default=None, help="S1.4 SIF Summary JSON")
    parser.add_argument("--keepa-product", default=None, help="S2 Keepa Product Request JSON (optional)")
    args = parser.parse_args()

    # Load data
    keepa_series = load_json(args.keepa_series)
    sorftime = load_json(args.sorftime)
    sif_keywords = load_json(args.sif_keywords)
    sif_summary = load_json(args.sif_summary)
    keepa_product = load_json(args.keepa_product)

    data_sources = []
    if keepa_series: data_sources.append("keepa_series")
    if sorftime: data_sources.append("sorftime")
    if sif_keywords: data_sources.append("sif_keywords")
    if sif_summary: data_sources.append("sif_summary")
    if keepa_product: data_sources.append("keepa_product")

    print(f"[数据源] 已加载: {', '.join(data_sources)}", file=sys.stderr)
    if not keepa_series and not sorftime:
        print("[⚠️ 警告] Keepa Series 和 Sorftime 均为空，价格/BSR/销量分析将无数据", file=sys.stderr)

    # Run 10 analysis modules
    results = {}

    print("[分析] 1/10 价格策略...", file=sys.stderr)
    results["price_strategy"] = analyze_price_strategy(keepa_series, sorftime)

    print("[分析] 2/10 Deal 效果...", file=sys.stderr)
    results["deal_effectiveness"] = analyze_deal_effectiveness(keepa_series, sorftime)

    print("[分析] 3/10 评论异常...", file=sys.stderr)
    results["review_anomaly"] = analyze_review_anomaly(keepa_series, sorftime)

    print("[分析] 4/10 生命周期...", file=sys.stderr)
    results["lifecycle"] = analyze_lifecycle(keepa_series, sorftime)

    print("[分析] 5/10 BSR 波动...", file=sys.stderr)
    results["bsr_volatility"] = analyze_bsr_volatility(keepa_series, sorftime)

    print("[分析] 6/10 流量结构...", file=sys.stderr)
    results["traffic_structure"] = analyze_traffic_structure(sif_summary, sif_keywords)

    print("[分析] 7/10 销量季节性...", file=sys.stderr)
    results["sales_seasonality"] = analyze_sales_seasonality(keepa_series, sorftime)

    print("[分析] 8/10 KPI 总览...", file=sys.stderr)
    results["kpi_overview"] = analyze_kpi_overview(keepa_product, sorftime)

    print("[分析] 9/10 时间线...", file=sys.stderr)
    results["timeline"] = analyze_timeline(keepa_product, keepa_series)

    print("[分析] 10/10 SWOT...", file=sys.stderr)
    results["swot"] = analyze_swot(results)

    # Assemble final output
    output = {
        "analysis_time": datetime.now().isoformat(),
        "data_sources": data_sources,
        "data_source_count": len(data_sources),
        **results,
    }

    # Output JSON to stdout
    print(json.dumps(output, ensure_ascii=False, indent=2))

    # Persist to session dir
    try:
        out_path = resolve_data_path(f"competitor-reverse-analysis-s3-{int(datetime.now().timestamp()*1000)}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"[落盘] {out_path}", file=sys.stderr)
    except Exception as e:
        print(f"[⚠️ 落盘失败] {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
