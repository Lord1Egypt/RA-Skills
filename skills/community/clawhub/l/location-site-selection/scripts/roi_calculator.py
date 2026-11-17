#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
餐饮商铺选址分析引擎 (Pro v2.0.0)
=================================
基于 Reilly 零售引力定律、Hotelling 区位模型、TQI 客流质量指数与 GIS 逻辑，
对餐饮铺位做量化评估，并输出三情景（乐观/中性/悲观）财务测算与回本周期置信区间。

输入：结构化 JSON（见 SKILL.md / references/benchmarks.md）
输出：人类可读报告 + 末尾 ===JSON=== 机器可读结果块。

用法：
  python roi_calculator.py --json input.json
  python roi_calculator.py --demo        # 运行 Spec 内置示例
"""
import argparse
import json
import math
import re
import sys

# ---------- 基准常量（详见 references/benchmarks.md） ----------

# 可视衰减因子：基于门头可视角度 visibility_angle（度）
def visibility_decay(angle: float) -> float:
    if angle <= 30:
        return 0.70
    if angle >= 60:
        return 1.00
    return 0.70 + (angle - 30) / 30.0 * 0.30   # 30~60 线性 0.70→1.00


# 阻抗因子：物理阻碍标签 → 乘性衰减
IMPEDANCE_MAP = {
    "step": 0.85, "台阶": 0.85,
    "median": 0.70, "隔离带": 0.70,
    "low_ceiling": 0.90, "挑高低": 0.90,
    "pillar": 0.92, "柱头": 0.92,
    "bad_parking": 0.85, "停车难": 0.85,
}


def impedance_factor(tags) -> (float, list):
    f = 1.0
    unknown = []
    for t in (tags or []):
        key = str(t).strip()
        if key in IMPEDANCE_MAP:
            f *= IMPEDANCE_MAP[key]
        else:
            unknown.append(key)
            f *= 0.95  # 未知阻碍保守打折
    return f, unknown


# 品类捕获率基准（foot-traffic → 进店客）
CATEGORY_CAPTURE = {
    "快餐": 0.04, "quick_service": 0.04,
    "正餐": 0.015, "dine_in": 0.015, "restaurant": 0.015,
    "茶饮": 0.06, "奶茶": 0.06, "柠檬茶": 0.06, "咖啡": 0.06, "coffee": 0.06,
    "火锅": 0.015, "hotpot": 0.015,
    "烘焙": 0.05, "面包": 0.05, "bakery": 0.05,
}
DEFAULT_CAPTURE = 0.02

# 日曝光放大系数：将"峰期过点人数"折算为全交易时段有效曝光人数
DAILY_EXPANSION = 4.0

# 回本健康线（月）
HEALTH_LINES = [(12, "Low"), (18, "Medium"), (24, "Elevated")]  # >24 => High


def parse_deposit_terms(s: str):
    """解析 '3押1付' / '押三付一' → (deposit_months, prepay_months)"""
    if not s:
        return 1, 1
    digits = re.findall(r"(\d+)\s*押\s*(\d+)\s*付", s)
    if digits:
        return int(digits[0][0]), int(digits[0][1])
    digits = re.findall(r"押\s*(\d+)\s*付\s*(\d+)", s)
    if digits:
        return int(digits[0][0]), int(digits[0][1])
    nums = re.findall(r"\d+", s)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    return 1, 1


def f(v, d=0.0):
    if v is None or v == "":
        return d
    return float(v)


def reilly_breaking_point(d_m: float, s_a: float, s_b: float) -> float:
    """Reilly 定律断裂点（km，自本店 A 起算）。
    D_ab = d / (1 + sqrt(S_b/S_a))，d 为 A、B 间距（m）。"""
    if s_a <= 0:
        return 0.0
    d_km = d_m / 1000.0
    return d_km / (1.0 + math.sqrt(s_b / s_a))


def competition_diversion(d_m: float, s_a: float, s_b: float) -> float:
    """霍特林区位模型下的客流分流率（单竞品）。"""
    if s_a + s_b <= 0:
        return 0.0
    rel = s_b / (s_a + s_b)            # 竞品规模占比 0~1
    if d_m < 100:
        base = 0.30 + 0.20 * (rel - 0.5) * 2   # 规模相当时 0.30；竞品大→0.40；本店大→0.20
        return max(0.20, min(0.40, base))
    if d_m < 300:
        # 100~300m 线性衰减 0.30→0.05
        return 0.30 + (d_m - 100) / 200.0 * (0.05 - 0.30)
    return 0.0


def analyze(data: dict) -> dict:
    out = {"project": data.get("project", "未命名项目")}

    # ---- Red Flag 终止检查 ----
    red_flags = [str(x).lower() for x in data.get("red_flags", [])]
    TERMINATION = {"no_fume", "no_vent", "排烟", "fire_hazard", "fire", "消防",
                   "no_sewage", "排污", "unknow_title", "产权", "illegal"}
    triggered = [rf for rf in red_flags if any(t in rf for t in TERMINATION)]
    out["red_flag"] = bool(triggered)
    out["red_flag_items"] = triggered

    # ---- 基础参数 ----
    loc = data.get("location", {})
    fin = data.get("financials", {})
    category = str(data.get("category", "正餐"))
    s_a = f(loc.get("scale_sqm"), 150.0)
    angle = f(loc.get("visibility_angle"), 90.0)
    ft = loc.get("foot_traffic", {}) or {}

    vis = visibility_decay(angle)
    imp, imp_unknown = impedance_factor(data.get("impedance"))
    tqi = vis * imp

    # ---- 客流质量指数 TQI ----
    wn = f(ft.get("weekday_noon"))
    wnn = f(ft.get("weekday_night"))
    we = f(ft.get("weekend_avg"))
    raw_daily = ((wn + wnn) * 5 + we * 2) / 7.0 * DAILY_EXPANSION
    adj_daily = raw_daily * tqi

    # ---- 竞争影响（Hotelling）----
    comps = data.get("competition", []) or []
    total_div = 0.0
    comp_details = []
    for c in comps:
        d_m = f(c.get("distance_m"))
        s_b = f(c.get("scale_sqm"), s_a)
        bp = reilly_breaking_point(d_m, s_a, s_b)
        div = competition_diversion(d_m, s_a, s_b)
        comp_details.append({
            "name": c.get("name", "竞品"), "distance_m": d_m,
            "scale_sqm": s_b, "breaking_point_km": round(bp, 3),
            "diversion_rate": round(div, 3),
        })
        total_div = 1 - (1 - total_div) * (1 - div)
    total_div = min(0.85, total_div)

    # 品类基准捕获率
    cap_base = CATEGORY_CAPTURE.get(category, DEFAULT_CAPTURE)
    # 悲观情景：竞品按最大分流潜力的 50% 实现（半实现假设，避免极端化）
    pes_capture = cap_base * (1 - 0.5 * total_div)

    # ---- Reilly 商圈 ----
    if comps:
        r_km = min(cd["breaking_point_km"] for cd in comp_details)
    else:
        r_km = 1.5  # 无竞品时默认核心商圈半径
    catchment = math.pi * r_km * r_km

    proj_daily_covers = adj_daily * cap_base          # 中性日翻台/客单

    # ---- 财务建模 ----
    rent = f(fin.get("rent_monthly"))
    dep, prep = parse_deposit_terms(fin.get("deposit_terms"))
    renov = f(fin.get("renovation_cost"))
    transfer = f(fin.get("transfer_fee"))
    avg_check = f(fin.get("avg_check"))
    cogs = f(fin.get("cogs_ratio"), 0.35)
    opex = f(fin.get("opex_ratio"), 0.25)

    first_period_rent = rent * (dep + prep)
    total_invest = renov + first_period_rent + transfer
    cm = max(0.01, 1 - cogs - opex)
    fixed_monthly = rent  # opex 已按营收比例计入变动成本

    breakeven_rev = fixed_monthly / cm

    neutral_rev = proj_daily_covers * avg_check * 30.0
    opt_rev = neutral_rev * 1.2                       # 乐观：客流 +20%
    pes_rev = adj_daily * pes_capture * avg_check * 30.0   # 悲观：竞品分流实现

    def scenario(rev):
        net = rev * cm - fixed_monthly
        payback = total_invest / net if net > 0 else float("inf")
        return {
            "monthly_revenue": round(rev, 2),
            "monthly_net_profit": round(net, 2),
            "payback_months": round(payback, 1) if payback != float("inf") else None,
        }

    scenarios = {
        "optimistic": scenario(opt_rev),
        "neutral": scenario(neutral_rev),
        "pessimistic": scenario(pes_rev),
    }

    # 置信区间（回本周期）
    po = scenarios["optimistic"]["payback_months"]
    pp = scenarios["pessimistic"]["payback_months"]
    pn = scenarios["neutral"]["payback_months"]
    if po and pp:
        ci = f"{pp:.1f}–{po:.1f}"
    elif pn:
        ci = f">24 (中性 {pn:.1f})"
    else:
        ci = "无法回本"

    # 风险等级
    p_pay = pp if pp else (pn or 999)
    risk = "High"
    for thr, lvl in HEALTH_LINES:
        if p_pay <= thr:
            risk = lvl
            break

    # ---- 谈判筹码 ----
    rent_cut = round((1 - vis) * 66.7) if vis < 1 else 0   # 45°→~10%
    free_rent_days = min(60, round(total_div * 150))

    out.update({
        "category": category,
        "visibility_angle": angle,
        "visibility_factor": round(vis, 3),
        "impedance_factor": round(imp, 3),
        "impedance_unknown": imp_unknown,
        "tqi": round(tqi, 3),
        "raw_daily_traffic": round(raw_daily, 1),
        "adj_daily_traffic": round(adj_daily, 1),
        "capture_rate_base": cap_base,
        "total_diversion_rate": round(total_div, 3),
        "effective_capture_rate": round(cap_base, 4),
        "pessimistic_capture_rate": round(pes_capture, 4),
        "projected_daily_covers": round(proj_daily_covers, 1),
        "reilly": {
            "trade_area_radius_km": round(r_km, 3),
            "effective_catchment_sqkm": round(catchment, 3),
            "competitors": comp_details,
        },
        "financials": {
            "deposit_months": dep, "prepay_months": prep,
            "first_period_rent": round(first_period_rent, 2),
            "total_investment": round(total_invest, 2),
            "contribution_margin": round(cm, 3),
            "fixed_monthly": round(fixed_monthly, 2),
            "breakeven_monthly_revenue": round(breakeven_rev, 2),
        },
        "scenarios": scenarios,
        "payback_confidence_interval": ci,
        "risk_level": risk,
        "negotiation": {
            "rent_cut_pct": rent_cut,
            "free_rent_days": free_rent_days,
        },
    })
    return out


def print_report(r: dict):
    def wan(v):
        return f"{v/10000:.1f}万" if v >= 10000 else f"{v:.0f}"
    print("=" * 60)
    print(f"  零售选址与 ROI 分析系统 (Pro)  ·  {r['project']}")
    print("=" * 60)
    if r.get("red_flag"):
        print("🔴 Red Flag: Project Termination")
        print(f"   触发硬伤：{', '.join(r['red_flag_items'])}")
        print("   存在消防/排烟/产权等合规硬伤，直接判定终止，不建议推进。")
        print("=" * 60)
        return
    print("\n【1. Trade Area Analysis / 商圈分析】")
    print(f"  Calculated Breaking Point : 距本店 {r['reilly']['trade_area_radius_km']} km 外的顾客更倾向来本店")
    print(f"  Effective Catchment Area  : {r['reilly']['effective_catchment_sqkm']} km² (Buffer Zone)")
    for c in r['reilly']['competitors']:
        print(f"    - {c['name']}: {c['distance_m']:.0f}m, 断裂点 {c['breaking_point_km']}km, 分流 {c['diversion_rate']*100:.0f}%")

    print("\n【2. Traffic & Conversion Forecast / 客流与转化预测】")
    print(f"  Raw Daily Traffic        : {r['raw_daily_traffic']:.0f} 人 (Network Analysis 折算)")
    print(f"  TQI (可视{int(r['visibility_angle'])}°×阻抗) : {r['tqi']}")
    print(f"  Adj. Daily Traffic       : {r['adj_daily_traffic']:.0f} 人 (有效日客流)")
    print(f"  Capture Rate (中性)      : {r['effective_capture_rate']*100:.2f}% (基准 {r['capture_rate_base']*100:.1f}%)")
    print(f"  Capture Rate (悲观)      : {r['pessimistic_capture_rate']*100:.2f}% (竞品分流 {r['total_diversion_rate']*100:.0f}% 半实现)")
    print(f"  Projected Daily Covers   : {r['projected_daily_covers']:.0f} 单")

    print("\n【3. Financial Projection / 财务预测】")
    fi = r['financials']
    print(f"  总投资 {wan(fi['total_investment'])} (首期租金{wan(fi['first_period_rent'])} + 装修设备 + 转让费)")
    print(f"  盈亏平衡月营收: ¥{fi['breakeven_monthly_revenue']:.0f}  | 贡献毛利率 {fi['contribution_margin']*100:.0f}%")
    print(f"  {'指标':<10}{'乐观':>14}{'中性':>14}{'悲观':>14}")
    sc = r['scenarios']
    print(f"  {'月营收':<10}¥{sc['optimistic']['monthly_revenue']/10000:.1f}万¥{sc['neutral']['monthly_revenue']/10000:.1f}万¥{sc['pessimistic']['monthly_revenue']/10000:.1f}万")
    print(f"  {'月净利润':<10}¥{sc['optimistic']['monthly_net_profit']/10000:.1f}万¥{sc['neutral']['monthly_net_profit']/10000:.1f}万¥{sc['pessimistic']['monthly_net_profit']/10000:.1f}万")
    po = sc['optimistic']['payback_months']; pn = sc['neutral']['payback_months']; pp = sc['pessimistic']['payback_months']
    print(f"  {'回本周期':<10}{('%.1f月'%po) if po else '亏损':>14}{('%.1f月'%pn) if pn else '亏损':>14}{('%.1f月'%pp) if pp else '亏损':>14}")
    print(f"  回本周期置信区间: {r['payback_confidence_interval']} 月  | 风险等级: {r['risk_level']}")

    print("\n【4. Negotiation Levers / 谈判筹码】")
    ng = r['negotiation']
    if ng['rent_cut_pct'] > 0:
        print(f"  · 可视角度 {int(r['visibility_angle'])}° 偏低 → 建议据此要求租金下调 {ng['rent_cut_pct']}%")
    if ng['free_rent_days'] > 0:
        print(f"  · 竞争分流 {r['total_diversion_rate']*100:.0f}% → 建议要求 {ng['free_rent_days']} 天免租期覆盖爬坡")
    print("=" * 60)


def main():
    p = argparse.ArgumentParser(description="餐饮商铺选址分析引擎 Pro")
    p.add_argument("--json", help="输入 JSON 文件路径")
    p.add_argument("--demo", action="store_true", help="运行 Spec 内置示例")
    args = p.parse_args()

    if args.demo:
        data = DEMO_JSON
    elif args.json:
        with open(args.json, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        print("请通过 --json <file> 或 --demo 提供输入。", file=sys.stderr)
        sys.exit(2)

    result = analyze(data)
    print_report(result)
    print("\n===JSON===")
    print(json.dumps(result, ensure_ascii=False, indent=2))


DEMO_JSON = {
    "project": "新店001",
    "category": "正餐",
    "location": {
        "address": "XX路XX号", "longitude": 121.47, "latitude": 31.23,
        "scale_sqm": 150, "visibility_angle": 45,
        "foot_traffic": {"weekday_noon": 2500, "weekday_night": 800, "weekend_avg": 1800},
    },
    "competition": [{"name": "竞品A", "distance_m": 50, "scale_sqm": 150}],
    "financials": {
        "rent_monthly": 50000, "deposit_terms": "3押1付", "renovation_cost": 300000,
        "avg_check": 45, "cogs_ratio": 0.35, "opex_ratio": 0.25,
    },
    "red_flags": [],
}


if __name__ == "__main__":
    main()
