#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策人级餐饮选址报告生成器 (Decision Report Generator)
=====================================================
整合 roi_calculator.analyze() 的量化结论 + category_recommender.recommend() 的品类建议
+ 可选 map_data（地图 MCP 采集），输出**面向餐饮选址决策人**的 Markdown 文档。

特征：
  - 一页决策摘要（红/黄/绿 verdict + KPI 卡）
  - 地图数据勘察（商圈价值、竞品分布、可达性）
  - 客流漏斗 / 回本区间 ASCII 可视化
  - 品类决策象限与推荐排序
  - 行动清单（推进 / 条件 / 否决）与谈判筹码

用法：
  python report_generator.py --json input.json
  python report_generator.py --demo
  python report_generator.py --json input.json --map-json map_data.json
"""
import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from roi_calculator import analyze, DEMO_JSON  # noqa: E402
import category_recommender as cr  # noqa: E402

W = "\033[0m"  # 不使用终端颜色，纯文本 Markdown 输出


# ---------------- 可视化辅助 ----------------
def bar(val, maxv, width=22, ch="█"):
    if maxv <= 0:
        return " " * width
    n = max(1, min(width, int(round(val / maxv * width))))
    return ch * n + " " * (width - n)


def wan(v):
    if v is None:
        return "—"
    return f"¥{v/10000:.1f}万" if abs(v) >= 10000 else f"¥{v:.0f}"


def build_features(analysis, data, map_data):
    """从分析结果与地图数据推导品类推荐所需特征。"""
    md = map_data or {}
    # 竞争强度由综合分流率推断（无 map 时）
    div = analysis.get("total_diversion_rate", 0) or 0
    comp = md.get("competition_intensity")
    if not comp:
        comp = "Low" if div < 0.15 else ("Medium" if div < 0.4 else "High")
    return {
        "trade_area_type": md.get("trade_area_type", "社区型"),
        "consumption_level": md.get("consumption_level", "Medium"),
        "commercial_density": md.get("commercial_density", "Medium"),
        "competition_intensity": comp,
        "tqi": analysis.get("tqi", 1.0),
        "red_flags": data.get("red_flags", []),
    }


def verdict(analysis, recs):
    if analysis.get("red_flag"):
        return ("🔴 红 · 终止", "存在消防/排烟/产权硬伤，一票否决，不予推进。")
    risk = analysis.get("risk_level", "High")
    pn = (analysis.get("scenarios", {}).get("neutral", {}) or {}).get("payback_months")
    best_green = recs["ranked"][0]["score"] >= 75
    if risk in ("High",) or (pn and pn > 24):
        return ("🔴 红 · 高风险", "回本周期超出安全线或风险等级 High，建议重谈租约或放弃。")
    if best_green and risk in ("Low", "Medium"):
        return ("🟢 绿 · 推进", "核心指标达标且品类适配，可进入签约与施工排期。")
    return ("🟡 黄 · 条件推进", "指标可接受但存在约束项，须满足行动清单中的签约前条件再推进。")


def build_report(analysis, data, map_data=None):
    recs = cr.recommend(build_features(analysis, data, map_data))
    v_label, v_reason = verdict(analysis, recs)
    proj = analysis.get("project", "未命名项目")
    today = datetime.now().strftime("%Y-%m-%d")
    sc = analysis.get("scenarios", {})
    fi = analysis.get("financials", {})
    rl = analysis.get("reilly", {})
    md = map_data or {}

    L = []
    A = L.append

    # ---------- 标题 ----------
    A(f"# 餐饮选址决策报告 · {proj}")
    A(f"> 生成日期：{today} ｜ 分析引擎：Reilly + Hotelling + TQI + 三情景财务模型")
    A("")

    # ---------- 一、决策摘要 ----------
    A("## 一、决策摘要（一页结论）")
    A("")
    A(f"**综合裁定：{v_label}** —— {v_reason}")
    A("")
    # KPI 卡
    adj = analysis.get("adj_daily_traffic", 0)
    covers = analysis.get("projected_daily_covers", 0)
    pn = (sc.get("neutral", {}) or {}).get("payback_months")
    pp = (sc.get("pessimistic", {}) or {}).get("payback_months")
    po = (sc.get("optimistic", {}) or {}).get("payback_months")
    pn_txt = f"{pn:.1f} 月" if pn else "—"
    A("| 关键指标 | 数值 | 解读 |")
    A("| :--- | :--- | :--- |")
    A(f"| 有效日客流 (TQI修正) | **{adj:,.0f} 人** | 门头可视×物理阻抗后的真实进店基数 |")
    A(f"| 预计日翻台/客单 | **{covers:,.0f} 单** | 捕获率×客单后的经营强度 |")
    A(f"| 总投资 | **{wan(fi.get('total_investment'))}** | 装修+首期租金+转让费 |")
    A(f"| 回本周期 (中性) | **{pn_txt}** | 风险等级 {analysis.get('risk_level')} |")
    A(f"| 回本置信区间 | **{analysis.get('payback_confidence_interval')} 月** | 悲观→乐观跨度 |")
    A(f"| 首选品类 | **{recs['best']}** | {recs['ranked'][0]['tier']} |")
    A("")
    # 三条关键结论
    concl = []
    concl.append(f"商圈：核心商圈半径 {rl.get('trade_area_radius_km')} km，有效捕获面积 {rl.get('effective_catchment_sqkm')} km²（Buffer Zone）。")
    concl.append(f"客流：原始日客流 {analysis.get('raw_daily_traffic',0):,.0f} 人，经 TQI={analysis.get('tqi')} 修正后有效 {adj:,.0f} 人。")
    concl.append(f"财务：乐观 {po} 月 / 中性 {pn} 月 / 悲观 {pp} 月回本；风险等级 {analysis.get('risk_level')}。")
    A("**核心结论：**")
    for i, c in enumerate(concl, 1):
        A(f"{i}. {c}")
    A("")

    # ---------- 二、地图数据勘察 ----------
    A("## 二、地图数据勘察（商圈价值）")
    A("")
    if md:
        g = md.get("geocoded", {})
        coords = f"{g.get('lng')}, {g.get('lat')}" if isinstance(g, dict) else g
        A(f"- **地理坐标**：{coords}")
        acc = md.get("accessibility", {})
        if acc:
            A(f"- **可达性**：最近地铁/公交 {acc.get('nearest_metro_m', '—')} m，步行约 {acc.get('walk_min', '—')} 分钟")
        A(f"- **消费水平**：`{md.get('consumption_level', 'Medium')}` ｜ **商业密度**：`{md.get('commercial_density', 'Medium')}` ｜ **商圈类型**：`{md.get('trade_area_type', '社区型')}`")
        poi = md.get("poi_counts", {})
        if poi:
            A(f"- **业态构成（Buffer Zone POI 计数）**：" + "、".join(f"{k} {v}" for k, v in poi.items()))
        links = md.get("map_links", {})
        if links:
            A(f"- **地图核验**：[卫星图]({links.get('satellite','#')}) ｜ [街景]({links.get('street','#')})")
    else:
        A("> ⚠️ 未接入地图 MCP，以下商圈价值基于人工估算/待补。接入 tencent-map 等地图 MCP 后可自动填充竞品分布、消费能级与商业密度（见 `references/map_mcp_guide.md`）。")
    A("")

    # ---------- 三、商圈与客流 ----------
    A("## 三、商圈与客流（Space & Traffic）")
    A("")
    A(f"- **Reilly 断裂点**：距本店 {rl.get('trade_area_radius_km')} km 外的顾客更倾向来本店（引力切换边界）。")
    A(f"- **有效捕获面积 (Catchment Area)**：{rl.get('effective_catchment_sqkm')} km²。")
    A(f"- **TQI 客流质量指数**：{analysis.get('tqi')}（可视衰减×阻抗因子），将「通过人流」折算为「进店人流」。")
    A("")
    A("**客流漏斗（Network Analysis 折算）：**")
    A("")
    raw = analysis.get("raw_daily_traffic", 0)
    adjv = analysis.get("adj_daily_traffic", 0)
    cap = analysis.get("effective_capture_rate", 0) or 0.02
    cov = analysis.get("projected_daily_covers", 0)
    maxv = max(raw, 1)
    A(f"```")
    A(f"原始日客流   {bar(raw, maxv)} {raw:,.0f}")
    A(f"×TQI 修正    {bar(adjv, maxv)} {adjv:,.0f}")
    A(f"×捕获率      {bar(cov, maxv)} {cov:,.0f} 单/日")
    A(f"```")
    A("")

    # ---------- 四、竞争态势 ----------
    A("## 四、竞争态势（Competition）")
    A("")
    comps = rl.get("competitors", [])
    if comps:
        A("| 竞品 | 距离 | 规模(㎡) | 断裂点(km) | 分流率 |")
        A("| :--- | :--- | :--- | :--- | :--- |")
        for c in comps:
            A(f"| {c.get('name')} | {c.get('distance_m'):.0f} m | {c.get('scale_sqm'):.0f} | {c.get('breaking_point_km')} | {c.get('diversion_rate')*100:.0f}% |")
    else:
        A("- 无直接竞品，核心商圈默认半径 1.5 km。")
    A("")
    A(f"- **综合分流率**：{analysis.get('total_diversion_rate',0)*100:.0f}%（Hotelling 区位模型，封顶 85%）。")
    A("")

    # ---------- 五、财务预测 ----------
    A("## 五、财务预测（Financial Projection）")
    A("")
    A("| 指标 | 乐观 | 中性 | 悲观 |")
    A("| :--- | :--- | :--- | :--- |")
    A(f"| 月营收 | {wan(sc.get('optimistic',{}).get('monthly_revenue'))} | {wan(sc.get('neutral',{}).get('monthly_revenue'))} | {wan(sc.get('pessimistic',{}).get('monthly_revenue'))} |")
    A(f"| 月净利润 | {wan(sc.get('optimistic',{}).get('monthly_net_profit'))} | {wan(sc.get('neutral',{}).get('monthly_net_profit'))} | {wan(sc.get('pessimistic',{}).get('monthly_net_profit'))} |")
    A(f"| **回本周期** | **{po} 月** | **{pn} 月** | **{pp} 月** |")
    A("")
    A(f"**回本周期置信区间：{analysis.get('payback_confidence_interval')} 月 ｜ 风险等级：{analysis.get('risk_level')}**")
    A("")
    cap_months = max(pp or 24, 24) * 1.1
    A("```")
    A(f"乐观  {bar(po or 0, cap_months)} {po} 月")
    A(f"中性  {bar(pn or 0, cap_months)} {pn} 月")
    A(f"悲观  {bar(pp or 0, cap_months)} {pp} 月")
    A(f"      {'█'*int(12/cap_months*22)}↑12月安全线   {'█'*int(24/cap_months*22)}↑24月警戒线")
    A("```")
    A("")

    # ---------- 六、品类选址建议 ----------
    A("## 六、品类选址建议（Category Fit · 数据驱动）")
    A("")
    A(f"**首选品类：`{recs['best']}`** ｜ 回避品类：{', '.join(recs['avoid']) if recs['avoid'] else '无'}")
    A("")
    A("| 排名 | 品类 | 评分 | 等级 | 壁垒 | 投资 | 关键依据 |")
    A("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for i, x in enumerate(recs["ranked"], 1):
        A(f"| {i} | {x['category']} | {x['score']} | {x['tier']} | {x['barrier']} | {x['invest']} | {x['reason']} |")
    A("")
    # 决策象限：消费水平 × 竞争强度
    A("**决策象限（消费水平 × 竞争强度 → 适配品类）：**")
    A("")
    A("| 消费水平＼竞争 | 低 (Low) | 中 (Medium) | 高 (High) |")
    A("| :--- | :--- | :--- | :--- |")
    quad = {
        "High":   {"Low": "茶饮咖啡 / 火锅", "Medium": "茶饮咖啡 / 正餐", "High": "茶饮咖啡(差异化)"},
        "Medium": {"Low": "茶饮咖啡 / 快餐", "Medium": "快餐 / 轻食", "High": "快餐(刚需)"},
        "Low":    {"Low": "快餐 / 茶饮", "Medium": "快餐", "High": "快餐(价格战)"},
    }
    for cons in ("High", "Medium", "Low"):
        row = " | ".join(quad[cons][c] for c in ("Low", "Medium", "High"))
        A(f"| {cons} | {row} |")
    A("")

    # ---------- 七、行动清单 ----------
    A("## 七、行动清单（Action Plan）")
    A("")
    ng = analysis.get("negotiation", {})
    A("🟢 **立即推进**")
    if analysis.get("red_flag"):
        A("- ⛔ 终止：合规硬伤不可妥协，不进入谈判。")
    else:
        A(f"- 按首选品类 `{recs['best']}` 启动招商/设计排期。")
        A(f"- 锁定当前点位，进入租约条款磋商。")
    A("")
    A("🟡 **签约前条件（谈判筹码）**")
    if ng.get("rent_cut_pct", 0) > 0:
        A(f"- 门头可视角度偏低 → 要求租金下调 **{ng['rent_cut_pct']}%**。")
    if ng.get("free_rent_days", 0) > 0:
        A(f"- 竞争分流 {analysis.get('total_diversion_rate',0)*100:.0f}% → 要求 **{ng['free_rent_days']} 天免租期** 覆盖爬坡。")
    A("- 复核排烟/排污/消防验收与产权清晰度（一票否决项）。")
    A("- 要求房东配合提升可视性（凸面镜/侧招/骑马廊）。")
    A("")
    A("🔴 **否决项（Red Flag）**")
    A("- 无合规排烟（涉油烟品类）、消防隐患、产权不明、违建禁餐 → 直接终止。")
    A("- 悲观情景回本 > 24 月且无法重谈租约 → 放弃。")
    A("")
    A("---")
    A("*本测算基于行业平均值、空间经济模型与地图结构化数据，结果为数据推演，具体经营结果取决于实际运营能力与租约条款。*")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="决策人级餐饮选址报告生成器")
    p.add_argument("--json", help="选址输入 JSON（roi_calculator 格式）")
    p.add_argument("--map-json", help="地图 MCP 采集数据 JSON（可选）")
    p.add_argument("--demo", action="store_true", help="运行内置示例")
    p.add_argument("--out", help="输出 Markdown 文件路径（可选）")
    args = p.parse_args()

    if args.demo:
        data = DEMO_JSON
    elif args.json:
        with open(args.json, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        print("请通过 --json <file> 或 --demo 提供选址输入。", file=sys.stderr)
        sys.exit(2)

    map_data = None
    if args.map_json:
        with open(args.map_json, "r", encoding="utf-8") as fh:
            map_data = json.load(fh)

    analysis = analyze(data)
    md_text = build_report(analysis, data, map_data)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md_text)
        print(f"报告已写入：{args.out}")
    else:
        print(md_text)

    # 同时输出机器可读结论，便于串联
    print("\n===JSON===")
    print(json.dumps({"verdict_ok": not analysis.get("red_flag"),
                      "best_category": cr.recommend(build_features(analysis, data, map_data))["best"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
