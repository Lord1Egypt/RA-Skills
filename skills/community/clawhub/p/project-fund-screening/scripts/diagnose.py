#!/usr/bin/env python3
"""
project-fund-screening 诊断引擎
================================
根据项目基本事实（JSON），对照两类出资人标准输出结构化诊断：
  1. VC/PE 的 BP 阶段就绪度
  2. 政府引导/产投基金的落地契合度
输出 Markdown 诊断报告 + JSON 摘要。

用法:
  python3 diagnose.py --input project.json [--output report.md]
  python3 diagnose.py --self-test          # 用内置样例跑一遍自检

输入 JSON 字段参见 assets/diagnosis-template.md 与 references/scorecards.md。
所有缺失字段按"待核实(gap)"处理，不臆造分数。
"""
import argparse
import json
import sys

# ----------------------------------------------------------------------------
# 阶段规范化
# ----------------------------------------------------------------------------
STAGE_ALIASES = {
    "seed": "seed", "天使": "seed", "angel": "seed",
    "pre_a": "pre_a", "prea": "pre_a", "pre-a": "pre_a",
    "a": "A", "轮a": "A", "a轮": "A",
    "b": "B", "轮b": "B", "b轮": "B",
    "c": "C", "轮c": "C", "c轮": "C",
    "pe": "PE", "pre_ipo": "PE", "pre-ipo": "PE", "并购": "PE", "上市前": "PE",
}
EARLY_STAGES = {"seed", "angel", "pre_a", "A"}


def norm_stage(s):
    if not s:
        return None
    return STAGE_ALIASES.get(str(s).strip().lower(), str(s).strip())


# ----------------------------------------------------------------------------
# 城市政府基金画像（基于国办发〔2025〕1号及 2025-2026 各地细则）
# return_ratio_typical: 当地典型返投倍数（越低越宽松）
# cancel_register: 是否取消基金/管理人本地注册硬要求
# tolerance: 容亏强度 high/medium/high-early(早期项目容亏100%)
# tolerant_stages: 享受高容亏的主要阶段
# ----------------------------------------------------------------------------
CITY_PROFILES = {
    "深圳": {"return_ratio": 1.0, "cancel_register": True, "tolerance": "high-early",
             "tolerant_stages": ["seed", "angel", "pre_a", "A"], "has_relief": True},
    "广州": {"return_ratio": 1.0, "cancel_register": True, "tolerance": "high-early",
             "tolerant_stages": ["seed", "angel", "pre_a", "A"], "has_relief": True},
    "苏州": {"return_ratio": 1.2, "cancel_register": False, "tolerance": "medium",
             "tolerant_stages": ["seed", "angel"], "has_relief": False},
    "合肥": {"return_ratio": 1.0, "cancel_register": False, "tolerance": "medium-high",
             "tolerant_stages": ["pre_a", "A", "B"], "has_relief": False, "style": "产业链"},
    "长沙": {"return_ratio": 0.4, "cancel_register": False, "tolerance": "high",
             "tolerant_stages": ["seed", "angel", "pre_a", "A"], "has_relief": True},
    "温州": {"return_ratio": 0.4, "cancel_register": False, "tolerance": "high",
             "tolerant_stages": ["seed", "angel"], "has_relief": True},
    "上海": {"return_ratio": 1.0, "cancel_register": True, "tolerance": "medium",
             "tolerant_stages": [], "has_relief": True},
    "佛山": {"return_ratio": 1.0, "cancel_register": False, "tolerance": "high-early",
             "tolerant_stages": ["seed", "angel"], "has_relief": True},
}
DEFAULT_CITY = {"return_ratio": 1.5, "cancel_register": False, "tolerance": "medium",
                "tolerant_stages": [], "has_relief": False}


def city_profile(city):
    if not city:
        return DEFAULT_CITY
    return CITY_PROFILES.get(str(city).strip(), DEFAULT_CITY)


# ----------------------------------------------------------------------------
# 评分辅助
# ----------------------------------------------------------------------------
def clamp5(x):
    return max(0, min(5, x))


def score_to_label(s):
    if s is None:
        return "待核实"
    if s >= 4.5:
        return "优秀"
    if s >= 3.5:
        return "良好"
    if s >= 2.5:
        return "及格"
    if s >= 1.5:
        return "偏弱"
    return "不足"


# ----------------------------------------------------------------------------
# VC/PE 维度：按阶段派生各准则分数(0-5 或 None)
# 返回 {criterion: (score, weight)}
# ----------------------------------------------------------------------------
def derive_vc(stage, f):
    team = f.get("team", {})
    mkt = f.get("market", {})
    val = f.get("validation", {})
    tb = f.get("tech_barrier")
    pmf = f.get("pmf", {})
    gr = f.get("growth", {})
    ue = f.get("unit_econ", {})
    moat = f.get("moat")
    fin = f.get("financials", {})
    gov = f.get("governance", {})
    comp = f.get("compliance", {})
    exit_ = f.get("exit", {})

    # 通用派生器
    def team_score():
        founders = team.get("founders", 0)
        roles = team.get("key_roles", [])
        yrs = team.get("domain_years", 0)
        completeness = team.get("completeness")
        if completeness in ("complete", "完整"):
            return 5
        if completeness in ("partial", "部分"):
            return 3
        if completeness in ("thin", "单薄"):
            return 1
        s = 0
        if founders >= 2:
            s += 2
        if "CEO" in roles and "CTO" in roles:
            s += 2
        if yrs >= 8:
            s += 1
        elif yrs >= 3:
            s += 0.5
        return clamp5(s) if (founders or roles or yrs) else None

    def market_score():
        t = mkt.get("tam_tier")
        if isinstance(t, (int, float)):
            return clamp5(t)
        return None

    def validation_score():
        if val.get("has_mvp"):
            s = 3
        elif val.get("pilot_users"):
            s = 2
        elif val.get("waitlist"):
            s = 1
        else:
            return None
        return clamp5(s)

    def tech_score():
        m = {"patent": 5, "专利": 5, "knowhow": 4, "know-how": 4, "品牌": 3,
             "brand": 3, "渠道": 3, "none": 1, "无": 1, "": None}
        return m.get(tb) if tb is not None else None

    def pmf_score():
        ret = pmf.get("retention")
        ndr = pmf.get("ndr")
        sig = pmf.get("signal")
        if ret is None and ndr is None and sig is None:
            return None
        s = 0
        if sig:
            s += 1.5
        if isinstance(ret, (int, float)):
            s += clamp5(ret * 5) * 0.35
        if isinstance(ndr, (int, float)):
            s += (clamp5((ndr - 1) * 10 + 2.5)) * 0.35
        return clamp5(s)

    def growth_score():
        mom = gr.get("mom")
        qoq = gr.get("qoq")
        g = mom if mom is not None else (qoq / 3.0 if qoq is not None else None)
        if g is None:
            return None
        # mom 30%≈5, 10%≈3, 0%≈1
        return clamp5(1 + g * 13)

    def ue_score():
        lc = ue.get("ltv_cac")
        gm = ue.get("gross_margin")
        if lc is None and gm is None:
            return None
        s = 0
        if isinstance(lc, (int, float)):
            s += clamp5(lc / 3.0 * 5) * 0.6
        if isinstance(gm, (int, float)):
            s += clamp5(gm * 5) * 0.4
        return clamp5(s)

    def moat_score():
        m = {"network": 5, "网络效应": 5, "data": 4, "数据壁垒": 4,
             "switching": 4, "切换成本": 4, "brand": 3, "品牌": 3,
             "none": 1, "无": 1}
        return m.get(moat) if moat is not None else None

    def fin_score():
        rw = fin.get("runway_months")
        p2p = fin.get("path_to_profit")
        if rw is None and p2p is None:
            return None
        s = 0
        if isinstance(rw, (int, float)):
            s += clamp5(rw / 18.0 * 5) * 0.5
        if p2p in ("visible", "可见", "清晰"):
            s += 2.5
        elif p2p in ("rough", "模糊"):
            s += 1
        return clamp5(s)

    def gov_score():
        if not gov:
            return None
        s = 0
        cnt = sum([1 for k in ("clean", "board", "audit") if gov.get(k)])
        s = cnt / 3.0 * 5
        return clamp5(s)

    def comp_score():
        if not comp:
            return None
        return 5 if comp.get("clean") else 1

    def exit_score():
        if not exit_:
            return None
        s = 0
        if exit_.get("clear"):
            s += 3
        p = exit_.get("path")
        if p in ("ipo", "并购", "ma"):
            s += 2
        return clamp5(s)

    # 阶段 -> 准则权重
    if stage in ("seed", "angel"):
        return {
            "团队完整度": (team_score(), 35),
            "市场天花板": (market_score(), 25),
            "早期验证": (validation_score(), 20),
            "技术壁垒": (tech_score(), 20),
        }
    if stage in ("pre_a", "A"):
        return {
            "PMF信号": (pmf_score(), 25),
            "单元经济": (ue_score(), 25),
            "增长动能": (growth_score(), 20),
            "团队完整度": (team_score(), 15),
            "市场天花板": (market_score(), 15),
        }
    if stage == "B":
        return {
            "规模化能力": (fin_score(), 25),
            "护城河": (moat_score(), 25),
            "增长质量": (growth_score(), 20),
            "单元经济": (ue_score(), 15),
            "团队完整度": (team_score(), 15),
        }
    if stage == "C":
        return {
            "市场地位": (moat_score(), 25),
            "盈利路径": (fin_score(), 25),
            "治理合规": (gov_score(), 20),
            "增长质量": (growth_score(), 15),
            "毛利质量": (ue_score(), 15),
        }
    if stage == "PE":
        return {
            "财务质量": (fin_score(), 30),
            "合规干净": (comp_score(), 25),
            "治理到位": (gov_score(), 20),
            "退出路径": (exit_score(), 25),
        }
    # 未知阶段：全准则
    return {
        "团队完整度": (team_score(), 20),
        "市场天花板": (market_score(), 15),
        "PMF信号": (pmf_score(), 15),
        "单元经济": (ue_score(), 15),
        "增长动能": (growth_score(), 15),
        "护城河": (moat_score(), 20),
    }


# ----------------------------------------------------------------------------
# 政府基金维度
# ----------------------------------------------------------------------------
def derive_gov(city, stage, f):
    ld = f.get("landing", {})
    align = ld.get("sector_aligns_local_plan")
    actions = ld.get("return_actions", 0)
    intent_register = ld.get("intent_register", False)
    comp_clean = f.get("compliance", {}).get("clean", None)
    prof = city_profile(city)

    def align_score():
        if align is True:
            return 5
        if align is False:
            return 1
        return None

    def return_score():
        # 返投可达性 = 可认定返投动作数 与 当地典型倍数宽松度
        if actions is None:
            return None
        ease = 2.0 - prof["return_ratio"]  # 倍数越低越易，0.4->1.6, 1.5->0.5
        s = clamp5(actions * 1.5 + ease)
        return clamp5(s)

    def tolerance_score():
        tol = prof["tolerance"]
        if tol == "high-early":
            if stage in prof["tolerant_stages"]:
                return 5
            return 3
        if tol == "high":
            return 5
        if tol == "medium-high":
            return 4
        return 3

    def register_score():
        if prof["cancel_register"]:
            return 5 if intent_register else 4
        return 4 if intent_register else 2

    def comp_score():
        if comp_clean is True:
            return 5
        if comp_clean is False:
            return 1
        return None

    return {
        "产业契合": (align_score(), 30),
        "返投可达性": (return_score(), 30),
        "容亏匹配": (tolerance_score(), 20),
        "注册地/让利": (register_score(), 10),
        "合规红线": (comp_score(), 10),
    }


# ----------------------------------------------------------------------------
# 红旗与建议
# ----------------------------------------------------------------------------
def vc_redflags(stage, f):
    flags = []
    team = f.get("team", {})
    pmf = f.get("pmf", {})
    ue = f.get("unit_econ", {})
    fin = f.get("financials", {})
    mkt = f.get("market", {})
    if team.get("completeness") in ("thin", "单薄") and stage in EARLY_STAGES:
        flags.append("团队单薄（关键岗位空缺），早期机构最看重'人和'，需补全 CEO/CTO/_domain 背景")
    if isinstance(pmf.get("retention"), (int, float)) and pmf["retention"] < 0.4:
        flags.append("留存率 < 40%，PMF 信号偏弱，需先验证留存再融资")
    if isinstance(ue.get("ltv_cac"), (int, float)) and ue["ltv_cac"] < 1:
        flags.append("LTV/CAC < 1，单元经济为负，规模化会放大亏损")
    if isinstance(fin.get("runway_months"), (int, float)) and fin["runway_months"] < 6:
        flags.append("Runway < 6 个月，资金链承压，优先补流而非扩张")
    if isinstance(mkt.get("tam_tier"), (int, float)) and mkt["tam_tier"] <= 2 and stage not in ("seed", "angel"):
        flags.append("市场天花板偏低（TAM tier ≤ 2），A 轮后机构会质疑起量空间")
    return flags


def gov_redflags(city, f):
    flags = []
    ld = f.get("landing", {})
    comp_clean = f.get("compliance", {}).get("clean", None)
    if ld.get("sector_aligns_local_plan") is False:
        flags.append("赛道与落地城市重点投资领域清单错配，政府基金一票否决项")
    if not ld.get("return_actions"):
        flags.append("无明确返投抓手（本地子公司/研发中心/供应链/招商引荐），难以达返投")
    if comp_clean is False:
        flags.append("合规存在红线问题（关联交易/对赌/股权瑕疵），政府资金敏感度高于财务投资人")
    intents = [ld.get("intent_register"), ld.get("intent_rd_center"),
               ld.get("intent_tax"), ld.get("intent_jobs")]
    if not any(intents):
        flags.append("无任何落地意向（注册/研发/税收/就业），与政策目标背离，政府基金不会投")
    return flags


def recommendations(vc_pct, gov_pct, vc_flags, gov_flags, city, stage):
    recs = []
    if vc_flags:
        recs.append("优先补齐 VC 红旗项（" + vc_flags[0].split("，")[0] + " 等），这是财务投资人过会的前置条件")
    if gov_flags:
        recs.append("面向政府基金：先解决落地与产业契合（" + gov_flags[0].split("，")[0] + "），再谈返投条款")
    # 政策红利建议
    prof = city_profile(city)
    if prof["return_ratio"] <= 0.5:
        recs.append(f"{city or '该地'}返投倍数仅 ~{prof['return_ratio']}倍，综合资金成本低，可优先对接")
    else:
        recs.append("善用国办发〔2025〕1号 红利：优先选已出台低返投/容亏细则的城市（深圳/长沙/温州等）")
    if prof.get("has_relief"):
        recs.append(f"{city or '该地'}已建立容错/尽职免责机制，硬科技早期项目容亏空间大，敢投敢退")
    recs.append("返投前置设计：在融资方案里列明'可认定返投动作'，避免事后凑空壳公司")
    recs.append("一套材料两种讲法：主 BP 统一，另附'政府版附录'（产业匹配+税收/就业/研发中心测算）")
    return recs


# ----------------------------------------------------------------------------
# 聚合
# ----------------------------------------------------------------------------
def aggregate(criteria):
    num = 0.0
    den = 0.0
    for crit, (s, w) in criteria.items():
        if s is not None:
            num += s * w
            den += 5 * w
    pct = round(num / den * 100, 1) if den else None
    return pct


def run_diagnosis(data):
    stage = norm_stage(data.get("stage"))
    city = data.get("landing", {}).get("city") or data.get("target_city")
    f = data.get("facts", data)  # 允许 facts 平铺
    # 兼容 landing 在 facts 内或顶层
    if "landing" not in f and data.get("landing"):
        f["landing"] = data["landing"]

    vc_crit = derive_vc(stage, f) if data.get("screen_vc", True) else {}
    gov_crit = derive_gov(city, stage, f) if data.get("screen_gov", True) else {}

    vc_pct = aggregate(vc_crit)
    gov_pct = aggregate(gov_crit)
    vc_flags = vc_redflags(stage, f) if vc_crit else []
    gov_flags = gov_redflags(city, f) if gov_crit else []
    recs = recommendations(vc_pct, gov_pct, vc_flags, gov_flags, city, stage)

    return {
        "project": data.get("project_name", "未命名项目"),
        "stage": stage,
        "city": city,
        "vc": {"criteria": {k: {"score": v[0], "weight": v[1]} for k, v in vc_crit.items()},
               "pct": vc_pct, "redflags": vc_flags},
        "gov": {"criteria": {k: {"score": v[0], "weight": v[1]} for k, v in gov_crit.items()},
                "pct": gov_pct, "redflags": gov_flags},
        "recommendations": recs,
    }


def to_markdown(r):
    L = []
    L.append(f"# 项目初步筛选诊断报告：{r['project']}")
    L.append("")
    L.append(f"- **融资阶段**：{r['stage'] or '未指定'}")
    L.append(f"- **拟落地城市**：{r['city'] or '未指定'}")
    L.append("")

    def block(title, d):
        L.append(f"## {title}")
        if not d["criteria"]:
            L.append("_未纳入筛选_")
            L.append("")
            return
        pct = d["pct"]
        L.append(f"**综合达标度：{pct}%** （{score_to_label(pct/20 if pct is not None else None)}）" if pct is not None else "**综合达标度：待核实**")
        L.append("")
        L.append("| 准则 | 得分(0-5) | 权重 | 评级 |")
        L.append("|------|-----------|------|------|")
        for k, v in d["criteria"].items():
            s = v["score"]
            s_disp = "—" if s is None else f"{s:.2f}"
            L.append(f"| {k} | {s_disp} | {v['weight']} | {score_to_label(s)} |")
        if d["redflags"]:
            L.append("")
            L.append("**🚩 红旗（被毙风险）：**")
            for fl in d["redflags"]:
                L.append(f"- {fl}")
        L.append("")

    block("一、VC/PE 的 BP 阶段就绪度", r["vc"])
    block("二、政府引导/产投基金落地契合度", r["gov"])

    L.append("## 三、综合结论与整改建议")
    L.append("")
    for i, rec in enumerate(r["recommendations"], 1):
        L.append(f"{i}. {rec}")
    L.append("")
    L.append("> 本诊断基于国办发〔2025〕1号 及 2025-2026 各地政府基金细则、VC/PE 分阶段 BP 标准自动生成，"
             "缺失字段标记为'待核实'，不构成正式投资建议。")
    return "\n".join(L)


def self_test():
    sample = {
        "project_name": "示例半导体科技",
        "stage": "A",
        "screen_vc": True, "screen_gov": True,
        "landing": {"city": "深圳", "sector_aligns_local_plan": True,
                    "return_actions": 2, "intent_register": True,
                    "intent_rd_center": True, "intent_tax": True, "intent_jobs": True},
        "facts": {
            "team": {"founders": 2, "key_roles": ["CEO", "CTO"], "domain_years": 12, "completeness": "complete"},
            "market": {"tam_tier": 5, "sector": "半导体"},
            "validation": {"has_mvp": True, "pilot_users": 3},
            "tech_barrier": "patent",
            "pmf": {"retention": 0.72, "ndr": 1.25, "signal": True},
            "growth": {"mom": 0.28},
            "unit_econ": {"ltv_cac": 3.4, "gross_margin": 0.62},
            "moat": "data",
            "financials": {"runway_months": 20, "path_to_profit": "visible"},
            "governance": {"clean": True, "board": True, "audit": False},
            "compliance": {"clean": True},
            "exit": {"path": "ipo", "clear": True},
        },
    }
    r = run_diagnosis(sample)
    print(to_markdown(r))
    print("\n--- JSON ---")
    print(json.dumps(r, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="项目初步筛选诊断引擎")
    p.add_argument("--input", help="项目 JSON 文件路径")
    p.add_argument("--output", help="输出 Markdown 报告路径（可选）")
    p.add_argument("--self-test", action="store_true", help="运行内置样例自检")
    args = p.parse_args()

    if args.self_test:
        self_test()
        return

    if not args.input:
        print("请提供 --input 项目JSON，或加 --self-test 试运行。", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    r = run_diagnosis(data)
    md = to_markdown(r)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(md)
        # 同时写 JSON 摘要
        with open(args.output.rsplit(".", 1)[0] + ".json", "w", encoding="utf-8") as fh:
            json.dump(r, fh, ensure_ascii=False, indent=2)
        print(f"报告已写入 {args.output}")
    else:
        print(md)
        print("\n--- JSON ---")
        print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
