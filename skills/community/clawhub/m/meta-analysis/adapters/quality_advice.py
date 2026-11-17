#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality_advice.py — 质量评估引擎（B2/B3/B4 解耦版）

把 block_b 中的 GRADE / 过度声明 / 质量门逻辑解耦为独立函数，
供 run_analysis（独立分析路径）和 fullflow（完整流水线）共用。

用法:
    from quality_advice import evaluate_quality
    qa = evaluate_quality(stats, task="pairwise_meta")
    # qa = {"grade": {...}, "overclaims": [...], "quality_gate": {...}}

设计原则：
  - 纯本地启发式，不调用 coze。
  - 输入 stats 字典（coze 返回），输出结构化质量评估。
  - 独立路径中作为"统计顾问"层的一部分自动运行。
"""

from __future__ import annotations

from block_b import b2_grade, detect_overclaims, b4_quality_gate


def _infer_risk_of_bias(stats: dict) -> str:
    """从 stats 推断偏倚风险等级（启发式）。"""
    qg = stats.get("quality_gate") or {}
    checks = qg.get("checks") or []
    red_count = sum(1 for c in checks if isinstance(c, dict) and c.get("level") == "red")
    if red_count >= 2:
        return "high"
    if red_count == 1:
        return "moderate"
    return "low"


def _infer_publication_bias(stats: dict) -> str:
    """从 stats.bias 推断发表偏倚等级。"""
    bias = stats.get("bias") or {}
    egger_p = bias.get("egger_p") or bias.get("reg_p") or bias.get("begg_p")
    try:
        egger_p = float(egger_p)
    except (TypeError, ValueError):
        return "none"
    if egger_p < 0.10:
        return "serious"
    return "none"


def _first_scalar(v):
    """向量型 CI（网络 Meta 的 pooled 为多对比 list）→ 首个标量；标量原样返回。

    2026-09-14：旧实现直接把 pooled.ci_low 传进 float()，网络 Meta 的 list 会抛
    TypeError 并被本地 except 吞掉 → 不精确性域**恒为 "none"**（无声失效，比报错更危险）。
    """
    if isinstance(v, (list, tuple)):
        for x in v:
            try:
                return float(x)
            except (TypeError, ValueError):
                continue
        return None
    return v


def _infer_imprecision(stats: dict) -> str:
    """从 stats 推断不精确性。"""
    pooled = stats.get("pooled") or {}
    ci_lo = _first_scalar(pooled.get("ci_low_exp") or pooled.get("ci_low"))
    ci_hi = _first_scalar(pooled.get("ci_high_exp") or pooled.get("ci_high"))
    k = stats.get("k")
    try:
        k = int(k) if k is not None else 0
    except (TypeError, ValueError):
        k = 0
    if k < 3:
        return "serious"
    # CI 跨无效值
    sm = str(stats.get("sm") or "").upper()
    if ci_lo is not None and ci_hi is not None:
        try:
            ci_lo_f, ci_hi_f = float(ci_lo), float(ci_hi)
        except (TypeError, ValueError):
            return "none"
        null = 1.0 if sm in ("OR", "RR", "HR", "PLO", "PLOGIT") else 0.0
        if ci_lo_f < null < ci_hi_f:
            return "serious"
    return "none"


def evaluate_quality(stats: dict | None, task: str = "") -> dict:
    """综合质量评估。

    - **网络 Meta（nma / nma_rank / cnma）→ CINeMA 六域**（见 `cinema_grade`）。
      网络 Meta 不宜直接套用普通 GRADE：GRADE 缺少网络层面的核心域，且「间接性 /
      不一致性」在两范式下含义不同（不一致性在网络中特指 incoherence）。
    - 其他任务 → 原 GRADE 五域路径（B2 GRADE + B3 过度声明 + B4 质量门）。

    Args:
        stats: coze 返回的 stats 字典。
        task: 任务类型。

    Returns:
        quality_advice 字典：
          - grade: dict，GRADE（或 CINeMA）评估结果。
          - overclaims: list，过度声明命中列表。
          - quality_gate: dict，质量门评估。
          - summary: str，一句话总结。
    """
    if not isinstance(stats, dict):
        return {"grade": {}, "overclaims": [], "quality_gate": {}, "summary": ""}

    if _is_netmeta_stats(stats, task):
        return _evaluate_quality_cinema(stats, task)

    # 构建 pairwise 格式的输入（b2_grade 需要）
    het = stats.get("heterogeneity") or {}
    pooled = stats.get("pooled") or {}
    bias = stats.get("bias") or {}

    # 2026-09-14：CI/p 走 _first_scalar 归一，防止向量型混入 b2_grade 的数值比较
    # （`list < float` 会抛 TypeError，被上层 try/except 吞掉 → 质量评估整块失效）。
    _lo = _first_scalar(pooled.get("ci_low_exp") or pooled.get("ci_low"))
    _hi = _first_scalar(pooled.get("ci_high_exp") or pooled.get("ci_high"))
    _p = _first_scalar(pooled.get("p") or pooled.get("pval"))
    # CI 任一缺失 → 整体传 None（而不是 [None, None]）：下游据此跳过"CI 跨零"判据，
    # 而不是拿 None 去比较。部分 task（diagnostic_meta / dose_resp / bayesian_pairwise）
    # 的 stats 本就没有 pooled。
    _ci = [_lo, _hi] if (_lo is not None and _hi is not None) else None

    pairwise_input = {
        "I2": _first_scalar(het.get("I2")) or 0.0,
        "k": stats.get("k", 0),
        "effect_measure": stats.get("sm") or "OR",
        "ci_random": _ci,
        "ci_fixed": _ci,
        "p_random": _p,
        "p_fixed": _p,
    }

    # B2: GRADE
    risk = _infer_risk_of_bias(stats)
    pub_bias = _infer_publication_bias(stats)
    grade_report = b2_grade(
        pairwise_input,
        risk_of_bias=risk,
        indirectness="none",
        publication_bias=pub_bias,
    )

    # B3: 过度声明（基于 stats 中的文本字段）
    claims_parts = []
    if stats.get("conclusion"):
        claims_parts.append(str(stats["conclusion"]))
    if stats.get("note"):
        claims_parts.append(str(stats["note"]))
    claims_text = " ".join(claims_parts)
    overclaims = detect_overclaims(claims_text, stats=pairwise_input)

    # B4: 质量门 —— ⚠️ b4_quality_gate 返回 (report, next_human_action) **元组**。
    # 2026-09-14 修复：此前把元组直接当 dict 用（随后 qg_report.get("n_high")）→
    # AttributeError，被 run_analysis 的 try/except 静默吞掉 →
    # **质量评估（09-13 新增）对所有任务从未真正生效**，调用方只见空结果。
    qg_report, _nha = b4_quality_gate(grade_report, overclaims)

    # 一句话总结
    grade = grade_report.get("grade", "Low")
    n_high = qg_report.get("n_high", 0)
    n_med = qg_report.get("n_medium", 0)
    critical = qg_report.get("critical", False)

    if critical:
        summary = f"GRADE={grade}，存在 {n_high} 条高危过度声明，证据质量极低，结论需谨慎。"
    elif n_high > 0 or n_med > 0:
        summary = f"GRADE={grade}，检出 {n_high + n_med} 条过度声明，建议修改后再投稿。"
    else:
        summary = f"GRADE={grade}，未检出明显过度声明，证据质量可接受。"

    # 2026-09-14：部分 task（diagnostic_meta / dose_resp / bayesian_pairwise）的 stats
    # 不含 pooled / CI（只有 k + notes）→ GRADE 只能在研究数与异质性上评估。显式标注
    # 不完整，避免"数据缺失"被读成"质量很好"（这些任务此前质量评估整体抛异常，
    # 本改动是净新增，标注不构成对既有行为的改变）。
    if _ci is None:
        summary += "（注：本任务未返回合并效应/CI，评估仅基于研究数，不完整。）"
        if isinstance(grade_report, dict):
            grade_report["note"] = (str(grade_report.get("note") or "")
                                    + " ⚠ 缺合并效应/CI，GRADE 评估不完整；"
                                      "该 task 的统计量不在通用 stats.pooled 契约内。").strip()

    return {
        "grade": grade_report,
        "overclaims": overclaims,
        "quality_gate": qg_report,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# CINeMA 六域（网络 Meta 置信度评估）
# ---------------------------------------------------------------------------
# 2026-09-14 新增。网络 Meta 不宜套用普通 GRADE：GRADE 的「间接性」「不一致性」
# 在网络语境下含义不同（CINeMA 的 indirectness 指证据网络的间接性、incoherence 指
# 直接/间接证据冲突），且 GRADE 完全没有覆盖网络层面的一致性检验。
#
# 参考：Nikolakopoulou A, et al. CINeMA: An approach for assessing confidence in the
# results of a network meta-analysis. PLoS Med. 2020;17(4):e1003082.
#
# 评级：no_concerns / some_concerns / major_concerns / unclear（数据不足时不猜测，
# **绝不用"无数据"冒充"无问题"**）。

_CINEMA_TASKS = frozenset({"nma", "nma_rank", "cnma"})
_CINEMA_LABELS = {
    "within_study_bias": "研究内偏倚",
    "reporting_bias": "报告偏倚",
    "indirectness": "间接性",
    "imprecision": "不精确性",
    "heterogeneity": "异质性",
    "incoherence": "不一致性",
}
_CINEMA_SEV = {"no_concerns": 0, "unclear": 1, "some_concerns": 2, "major_concerns": 3}
_RATIO_SM = ("OR", "RR", "HR", "PLO", "PLOGIT", "IRR", "RRR")


def _cnum(v):
    """安全转 float（向量/None/非数值 → None）。"""
    if isinstance(v, (list, tuple)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _cnum_list(v) -> list:
    """向量 → [float, ...]（跳过非数值项）。"""
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            f = _cnum(x)
            if f is not None:
                out.append(f)
        return out
    f = _cnum(v)
    return [] if f is None else [f]


def _is_netmeta_stats(stats: dict, task: str) -> bool:
    """网络 Meta 判据：任务名命中，或 pooled.estimate 呈向量形状（兜底）。"""
    if task in _CINEMA_TASKS:
        return True
    pooled = (stats or {}).get("pooled") or {}
    return isinstance(pooled.get("estimate"), (list, tuple))


def _cin_ci_pairs(pooled: dict):
    """网络 Meta 的 (ci_low, ci_high) 对列表；跳过参考组自身占位项（log 尺度 est=lo=hi=0）。"""
    est = _cnum_list(pooled.get("estimate"))
    lo = _cnum_list(pooled.get("ci_low"))
    hi = _cnum_list(pooled.get("ci_high"))
    unit = str(pooled.get("unit") or "")
    n = min(len(est), len(lo), len(hi))
    pairs = []
    for i in range(n):
        if unit == "log" and est[i] == 0 and lo[i] == 0 and hi[i] == 0:
            continue
        pairs.append((lo[i], hi[i]))
    return pairs, unit


def cinema_grade(stats: dict, task: str = "") -> dict:
    """按 CINeMA 六域评估网络 Meta 的证据置信度（半自动启发式）。

    返回 {rating, domains{域:{rating,reason}}, domain_ratings, reasons,
          n_major, n_some, n_unclear, framework, note}。
    """
    stats = stats or {}
    het = stats.get("heterogeneity") or {}
    extra = stats.get("extra") or {}
    inc = extra.get("inconsistency") or {}
    net = extra.get("network") or {}
    add = extra.get("additivity") or {}
    pooled = stats.get("pooled") or {}
    is_cnma = task == "cnma" or stats.get("n_comp") is not None
    k = _cnum(stats.get("k"))
    sm = str(stats.get("sm") or "").upper()
    dom: dict = {}

    # ---- 1. 研究内偏倚 ----
    dom["within_study_bias"] = {
        "rating": "unclear",
        "reason": "stats 未携带偏倚风险评估结果（RoB2 / ROBINS-I）；"
                  "该域须人工按纳入研究逐条评级后填入。",
    }

    # ---- 2. 报告偏倚 ----
    bias = stats.get("bias") or {}
    eg = _cnum(bias.get("egger_p") or bias.get("reg_p") or bias.get("begg_p"))
    if eg is None:
        dom["reporting_bias"] = {
            "rating": "unclear",
            "reason": "未提供小样本效应检验；网络层面宜用比较调整漏斗图"
                      "（comparison-adjusted funnel plot）评估，须人工补做。",
        }
    elif eg < 0.10:
        dom["reporting_bias"] = {
            "rating": "major_concerns",
            "reason": f"Egger 检验 p = {eg:.3f} < 0.10，提示可能存在报告偏倚。"}
    else:
        dom["reporting_bias"] = {
            "rating": "no_concerns",
            "reason": f"Egger 检验 p = {eg:.3f}，未见明显报告偏倚信号。"}

    # ---- 3. 间接性 ----
    pd = _cnum_list(net.get("prop_direct"))
    if not pd:
        dom["indirectness"] = {
            "rating": "unclear",
            "reason": "缺各对比直接证据占比（prop_direct），间接性无法量化；"
                      "须人工核查各对比的人群 / 干预定义 / 结局是否可比。",
        }
    else:
        mn = min(pd)
        if mn < 0.25:
            dom["indirectness"] = {
                "rating": "major_concerns",
                "reason": f"最低直接证据占比仅 {mn * 100:.0f}%，"
                          "部分对比几乎完全依赖间接证据。"}
        elif mn < 0.50:
            dom["indirectness"] = {
                "rating": "some_concerns",
                "reason": f"最低直接证据占比 {mn * 100:.0f}%，"
                          "存在对间接证据的实质依赖。"}
        else:
            dom["indirectness"] = {
                "rating": "no_concerns",
                "reason": f"各对比直接证据占比均 ≥ {mn * 100:.0f}%。"}

    # ---- 4. 不精确性 ----
    # 无效值：log 尺度为 0（netmeta 输出 TE=log OR/RR/HR）；比值尺度为 1；差值尺度为 0
    pairs, unit = _cin_ci_pairs(pooled)
    null = 0.0 if unit == "log" else (1.0 if sm in _RATIO_SM else 0.0)
    n_cross = sum(1 for lo, hi in pairs if lo <= null <= hi)
    if k is not None and k < 3:
        dom["imprecision"] = {"rating": "major_concerns",
                              "reason": f"仅 {int(k)} 项研究，网络估计极不精确。"}
    elif not pairs:
        dom["imprecision"] = {"rating": "unclear",
                              "reason": "无可解析的效应量 / CI，不精确性无法评估。"}
    elif n_cross == len(pairs):
        dom["imprecision"] = {
            "rating": "major_concerns",
            "reason": f"{len(pairs)} 个对比的 95% CI 全部跨无效值。"}
    elif n_cross > 0:
        dom["imprecision"] = {
            "rating": "some_concerns",
            "reason": f"{len(pairs)} 个对比中 {n_cross} 个的 95% CI 跨无效值。"}
    else:
        dom["imprecision"] = {
            "rating": "no_concerns",
            "reason": f"{len(pairs)} 个对比的 95% CI 均未跨无效值。"}

    # ---- 5. 异质性 ----
    i2 = _cnum(het.get("I2"))
    tau = _cnum(het.get("tau"))
    if i2 is None:
        dom["heterogeneity"] = {
            "rating": "unclear",
            "reason": "未返回网络整体异质性（I² / τ²），该域无法评估。"}
    elif i2 >= 75:
        dom["heterogeneity"] = {"rating": "major_concerns",
                                "reason": f"网络整体 I² = {i2:.0f}%，异质性很高。"}
    elif i2 >= 50:
        dom["heterogeneity"] = {"rating": "some_concerns",
                                "reason": f"网络整体 I² = {i2:.0f}%，存在中等异质性。"}
    else:
        dom["heterogeneity"] = {
            "rating": "no_concerns",
            "reason": f"网络整体 I² = {i2:.0f}%"
                      + (f"，τ = {tau:.3f}" if tau is not None else "") + "。"}

    # ---- 6. 不一致性 ----
    p_inc = _cnum(inc.get("p"))
    df_inc = _cnum(inc.get("df"))
    p_add = _cnum(add.get("p_diff")) if is_cnma else None
    if p_add is not None and p_add < 0.05:
        dom["incoherence"] = {
            "rating": "major_concerns",
            "reason": f"加性假设被拒绝（Q.diff p = {p_add:.3f} < 0.05）——"
                      "成分效应不可加，成分模型自身即不自洽。"}
    elif p_inc is None or (df_inc is not None and df_inc <= 0):
        dom["incoherence"] = {
            "rating": "unclear",
            "reason": "设计-治疗交互检验不可得（网络可能仅含单一设计，或结构不足以"
                      "分解直接/间接证据）——不可检验 ≠ 已证明一致。"}
    elif p_inc < 0.05:
        dom["incoherence"] = {
            "rating": "major_concerns",
            "reason": f"显著不一致性（设计-治疗交互 p = {p_inc:.3f} < 0.05），"
                      "直接与间接证据冲突。"}
    elif p_inc < 0.10:
        dom["incoherence"] = {
            "rating": "some_concerns",
            "reason": f"不一致性边缘（设计-治疗交互 p = {p_inc:.3f}），"
                      "建议核查直接/间接差异。"}
    else:
        dom["incoherence"] = {
            "rating": "no_concerns",
            "reason": f"未见显著不一致性（设计-治疗交互 p = {p_inc:.3f}）。"
                      + ("加性假设未被拒绝。" if p_add is not None else "")}

    # ---- 汇总 ----
    n_major = sum(1 for d in dom.values() if d["rating"] == "major_concerns")
    n_some = sum(1 for d in dom.values() if d["rating"] == "some_concerns")
    n_unclear = sum(1 for d in dom.values() if d["rating"] == "unclear")
    # 整体评级只由**可评估域**决定：unclear 表示"这一域统计侧拿不到数据、须人工补"，
    # 若让它参与取最差，则 RoB / 报告偏倚恒为 unclear → 所有网络 Meta 都只能是 unclear，
    # 评级失去分辨力。unclear 域另以计数与清单显式提示，不会被静默忽略。
    judged = [_CINEMA_SEV[d["rating"]] for d in dom.values() if d["rating"] != "unclear"]
    worst = max(judged) if judged else 0
    if not judged:
        overall = "unclear"
    elif worst >= 3:
        overall = "major_concerns"
    elif worst == 2:
        overall = "some_concerns"
    else:
        overall = "no_concerns"

    reasons = [f"{_CINEMA_LABELS[name]}：{d['rating']} —— {d['reason']}"
               for name, d in dom.items()]
    return {
        "rating": overall,
        "domains": dom,
        "domain_ratings": {name: d["rating"] for name, d in dom.items()},
        "reasons": reasons,
        "n_major": n_major,
        "n_some": n_some,
        "n_unclear": n_unclear,
        "framework": "CINeMA",
        "note": "CINeMA 六域为半自动启发式评估，须人工确认；本评级是**网络整体**的"
                "域评级，不等于 CINeMA 的逐对比（per-comparison）置信度。",
    }


def _evaluate_quality_cinema(stats: dict, task: str) -> dict:
    """网络 Meta（nma / nma_rank / cnma）的质量评估：CINeMA 六域 + B3/B4 复用。"""
    cg = cinema_grade(stats, task)
    pooled = stats.get("pooled") or {}
    het = stats.get("heterogeneity") or {}
    pairs, unit = _cin_ci_pairs(pooled)
    null = 0.0 if unit == "log" else (
        1.0 if str(stats.get("sm") or "").upper() in _RATIO_SM else 0.0)
    # 过度声明检测复用同一单点实现（B3）。网络 Meta 无单一 CI → 保守地取"任一跨无效值"
    # 的对比作为 ci 判据（宁可行触发提示，也不静默放过）。
    ci_pair = None
    for lo, hi in pairs:
        if lo <= null <= hi:
            ci_pair = [lo, hi]
            break
    if ci_pair is None and pairs:
        ci_pair = [pairs[0][0], pairs[0][1]]

    claims_parts = []
    if stats.get("conclusion"):
        claims_parts.append(str(stats["conclusion"]))
    if stats.get("note"):
        claims_parts.append(str(stats["note"]))
    overclaim_stats = {
        "effect_measure": stats.get("sm") or "OR",
        "ci_random": ci_pair, "ci_fixed": ci_pair,
        "p_random": None, "p_fixed": None,
        "k": int(_cnum(stats.get("k")) or 0),
        "I2": _cnum(het.get("I2")) or 0.0,
    }
    overclaims = detect_overclaims(" ".join(claims_parts), stats=overclaim_stats)

    grade_report = {
        "grade": cg["rating"],
        "framework": "CINeMA",
        "downgrades": cg["n_major"] + 0.5 * cg["n_some"],
        "reasons": cg["reasons"],
        "domain_ratings": cg["domain_ratings"],
        "domains": cg["domains"],
        "coze_ready": False,
        "note": cg["note"],
    }
    qg_report, _nha = b4_quality_gate(grade_report, overclaims)
    # 网络 Meta：任一域达 major_concerns 即视为须人工闸放行（b4 只认 VeryLow，
    # 不覆盖 CINeMA 的语义，故此处显式提升）。
    if cg["rating"] == "major_concerns":
        qg_report["critical"] = True
    qg_report["framework"] = "CINeMA"

    label = {"major_concerns": "存在重大关切", "some_concerns": "存在一些关切",
             "no_concerns": "未见明显关切", "unclear": "各域均数据不足"}[cg["rating"]]
    n_judged = len(cg["domains"]) - cg["n_unclear"]
    summary = (f"CINeMA 六域：{label}（可评估 {n_judged}/6 域——"
               f"重大关切 {cg['n_major']}、一些关切 {cg['n_some']}；"
               f"另有 {cg['n_unclear']} 域数据不足，须人工补做）。")
    if qg_report.get("n_high"):
        summary += f"另检出 {qg_report['n_high']} 条高危过度声明。"

    return {
        "framework": "CINeMA",
        "grade": grade_report,
        "cinema": cg,
        "overclaims": overclaims,
        "quality_gate": qg_report,
        "summary": summary,
    }
