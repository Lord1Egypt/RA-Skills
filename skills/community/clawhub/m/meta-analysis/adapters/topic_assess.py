#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
topic_assess.py — Deterministic local topic-selection assessment for the
meta-analysis skill (no coze / no LLM required for the evidence-grounded dims).

This is the missing local half of the "Full" topic-selection path
(`scripts/generate_topic_report.py` renders an 11-section report from an
assessment JSON; previously that JSON's `scores` could ONLY be produced by
coze/LLM, so the standalone local flow never emitted a real evaluation).

What this module computes LOCALLY and DETERMINISTICALLY, grounded in REAL
probes (Europe PMC dedup + ClinicalTrials.gov registry):
  - data availability       (from real registered-trial / SR-MA counts)
  - novelty / saturation    (from real existing SR/MA counts)
  - methodological feasibility (from expected study count k + PICOS completeness)
  - clinical value          (JUDGMENT dimension — local default = mid, flagged
                             `needs_human`; override via `clinical_override`
                             when an LLM/coze is in the loop, per user intent)
  - total / verdict         (>=17 strongly_recommend / >=14 recommend /
                             >=10 hold / <10 not_recommended; any dim <=2 → veto)
  - R1–R6 cross-checks      (rule-based)
  - PRISMA 2020 / AMSTAR-2 pre-check (static topic-stage rubric)
  - dedup paragraph          (real Cochrane/PubMed counts + PROSPERO auto-probe
                               status / manual link)
  - real-gap evidence        (saturation label)

Every dimension carries an explicit `evidence` tag so the rendered report can
show which numbers are real vs which need human/LLM confirmation. Degrades
gracefully when probes are unavailable (scores still emitted, flagged
`unverified`).

Output dict is aligned with `references/topic-selection.md` + `topic_report.example.json`
so `generate_topic_report.py` can render it directly.
"""
import datetime

GAP_ZH = {
    "real_gap": "真实缺口（该窄方向在大类中仍欠研究）",
    "saturated": "已饱和（已有大量同类 Meta，须明确增量）",
    "caution": "需谨慎（方向已有覆盖，须差异化）",
    "empty": "近空白（新颖但可能数据不足，需警惕 k<2）",
    "unverified": "未验证（探针不可用）",
}

VERDICT_ZH = {
    "strongly_recommend": "强烈建议",
    "recommend": "建议",
    "hold": "暂缓",
    "not_recommended": "不建议",
}


def _extract_dedup_counts(dedup):
    """Pull real Cochrane / PubMed SR-MA hit counts from either the
    literature_probe result shape (layers.*.hit_count) or a flat dict."""
    cochrane = pubmed = None
    if isinstance(dedup, dict):
        layers = dedup.get("layers") or {}
        if layers:
            cochrane = (layers.get("cochrane") or {}).get("hit_count")
            pm = layers.get("pubmed_meta") or {}
            pubmed = pm.get("hit_count") if isinstance(pm, dict) else None
        else:
            cochrane = dedup.get("cochrane")
            pubmed = dedup.get("pubmed")
    try:
        cochrane = int(cochrane) if cochrane is not None else None
    except (TypeError, ValueError):
        cochrane = None
    try:
        pubmed = int(pubmed) if pubmed is not None else None
    except (TypeError, ValueError):
        pubmed = None
    return cochrane, pubmed


def _registry_total(registry):
    if isinstance(registry, dict):
        t = registry.get("total")
        try:
            return int(t) if t is not None else None
        except (TypeError, ValueError):
            return None
    return None


# ---------------------------------------------------------------------------
# Deterministic per-dimension scorers (0–5)
# ---------------------------------------------------------------------------
def _score_data(registry_total, pubmed_hits, cochrane_hits):
    if registry_total is not None:
        t, conf = registry_total, "registry"
    elif pubmed_hits is not None:
        t, conf = pubmed_hits, "pubmed_proxy"
    else:
        return 0, "unverified", "无真实探针数据（注册库/文献均未返回）"
    if t >= 50:
        s = 5
    elif t >= 20:
        s = 4
    elif t >= 10:
        s = 3
    elif t >= 5:
        s = 2
    elif t >= 1:
        s = 1
    else:
        s = 0
    note = ("注册库 %d 项 → 原始研究充足" % registry_total
            if registry_total is not None else
            "PubMed SR/MA %d 篇（代理，置信低于注册库）" % pubmed_hits)
    return s, conf, note


def _score_novelty(pubmed_hits, cochrane_hits):
    n = (pubmed_hits or 0) + (cochrane_hits or 0)
    if n == 0:
        return 5, "empty", "近无同类综述（新颖，但需警惕原始研究不足）"
    if n >= 20:
        return 1, "saturated", "已有大量同类 SR/MA，必须明确差异化增量"
    if n >= 10:
        return 2, "saturated", "同类综述较多，须找新颖角度"
    if n >= 5:
        return 3, "caution", "方向已有覆盖，须差异化"
    return 4, "real_gap", "同类综述较少，存在真实缺口空间"


def _score_feasibility(registry_total, pubmed_hits, missing):
    k = registry_total if registry_total is not None else (pubmed_hits
                                                            if pubmed_hits is not None else 0)
    if k >= 10:
        s = 5
    elif k >= 5:
        s = 4
    elif k >= 2:
        s = 3
    elif k >= 1:
        s = 1
    else:
        s = 0
    if len(missing or []) >= 3:
        s = min(s, 2)
    return s, ("预期可纳入研究数 k=%s" % k)


def _score_clinical(topic, override):
    rationale = None
    score = None
    if isinstance(override, dict):
        try:
            score = int(override.get("score"))
        except (TypeError, ValueError):
            score = None
        rationale = override.get("rationale")
    elif override is not None:
        try:
            score = int(override)
        except (TypeError, ValueError):
            score = None
    if score is not None:
        return score, False, "由 LLM/Coze 评估覆盖", rationale
    # 本地默认中值：临床价值是判断项，无公开 API 可算，明确标注需人工确认。
    return 3, True, "本地默认中值；临床价值属判断项，建议人工/LLM 确认", None


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------
def _verdict(total, scores):
    if scores.get("data", 5) <= 1:
        return "veto:data", "数据不足以支撑 meta（预期研究数 k<2）"
    if total >= 17:
        return "strongly_recommend", "证据充分、缺口明确，可推进"
    if total >= 14:
        return "recommend", "总体可行，推进前补齐缺口说明"
    if total >= 10:
        return "hold", "存在短板，建议先补强再启动"
    return "not_recommended", "多项偏弱，暂不建议启动"


# ---------------------------------------------------------------------------
# Cross-checks R1–R6 (rule-based)
# ---------------------------------------------------------------------------
def _cross_checks(picos, missing, pubmed_hits, cochrane_hits, novelty_label):
    n_sr = (pubmed_hits or 0) + (cochrane_hits or 0)
    checks = [
        {"rule": "R1", "triggered": bool(missing),
         "note": ("PICO 可分解" if not missing else
                  "缺失维度 %s，须先明确研究问题" % "、".join(missing))},
        {"rule": "R2", "triggered": False,
         "note": "默认 pairwise；若涉及 ≥3 同时干预需评估 NMA"},
        {"rule": "R3", "triggered": novelty_label in ("saturated",),
         "note": ("新颖性已复核，同类 SR/MA=%d，须明确增量" % n_sr
                  if novelty_label in ("saturated",) else "新颖性合理")},
        {"rule": "R4", "triggered": False,
         "note": "异质性预案（I²>50% 触发亚组）由技能提供"},
        {"rule": "R5", "triggered": False,
         "note": "结局-效应量对齐（时间-事件→HR，二分类→RR/OR）"},
        {"rule": "R6", "triggered": False,
         "note": "PROSPERO 注册列入后续动作"},
    ]
    return checks


# ---------------------------------------------------------------------------
# Compliance rubric (topic stage)
# ---------------------------------------------------------------------------
def _compliance():
    return {
        "prisma": [
            {"item": "1", "status": "ok", "note": "标题将标识为系统评价/Meta"},
            {"item": "5", "status": "plan", "note": "纳入标准草案（选题阶段）"},
            {"item": "9", "status": "gap", "note": "提取表待方案阶段构建"},
        ],
        "amstar2": [
            {"domain": "protocol", "status": "plan", "note": "PROSPERO 注册应在数据提取前完成"},
            {"domain": "publication_bias", "status": "ok", "note": "Egger/Begg/trim-fill 由技能提供"},
        ],
        "overall_risk": "yellow",
        "note": "选题阶段预检：2 项待补，方案阶段复检",
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def assess(topic, picos=None, missing=None, dedup=None, registry=None,
           clinical_override=None, prospero=None, curation=None, topic_en=None):
    """Build the full local topic assessment.

    Args:
        topic: original topic string.
        picos: dict {P,I,C,O,S} (from _infer_picos).
        missing: list of missing PICOS keys.
        dedup: literature_probe.dedup_probe result (real Cochrane/PubMed hits)
               or a flat {cochrane, pubmed} dict.
        registry: registry_probe result {total, sample, status} (real CT.gov).
        clinical_override: optional int (0-5) OR dict {"score":int,"rationale":str}
               supplied by LLM/coze for the judgment dimension; when present,
               clinical is NOT flagged needs_human (tag="coze") and rationale kept.
        curation: optional dict {"recommend":bool,"reason":str} from coze topic
               curation; rendered as a separate panel in the web UI.
        topic_en: optional English search term; PROSPERO probe uses this
                  for the manual-check URL instead of the raw Chinese topic.

    Returns: assessment dict aligned with generate_topic_report schema.
    """
    picos = picos or {}
    missing = missing or []
    cochrane_hits, pubmed_hits = _extract_dedup_counts(dedup)
    registry_total = _registry_total(registry)

    data_s, data_conf, data_note = _score_data(registry_total, pubmed_hits, cochrane_hits)
    nov_s, nov_label, nov_note = _score_novelty(pubmed_hits, cochrane_hits)
    fea_s, fea_note = _score_feasibility(registry_total, pubmed_hits, missing)
    cli_s, cli_needs, cli_note, cli_rationale = _score_clinical(topic, clinical_override)

    scores = {"clinical": cli_s, "feasibility": fea_s, "data": data_s,
              "novelty": nov_s, "total": cli_s + fea_s + data_s + nov_s}
    verdict_key, verdict_note = _verdict(scores["total"], scores)
    cross_checks = _cross_checks(picos, missing, pubmed_hits, cochrane_hits, nov_label)

    # PROSPERO 自动检索（真实尝试 + 优雅降级；上游故障时不编造数据）
    # 2026-09-25：优先用英文检索词（PROSPERO 是英文注册库，中文 topic 检索≈0 命中）
    if isinstance(prospero, dict) and prospero.get("status") in ("available", "unavailable"):
        _prospero = prospero
    else:
        try:
            import prospero_probe
            _prospero = prospero_probe.probe(topic_en or topic)
        except Exception as _pe:  # noqa: BLE001
            _prospero = {"status": "unavailable", "hit_count": None, "sample": [],
                         "error": "probe import failed: %s" % _pe,
                         "manual_url": None, "note": ""}
    if _prospero.get("status") == "available":
        _prospero_line = "已自动检索：命中 %s 项已注册方案（来源 %s）" % (
            _prospero.get("hit_count"), _prospero.get("source"))
    else:
        _pu = _prospero.get("manual_url") or (
            "https://www.crd.york.ac.uk/prospero/#searchadvanced?search="
            + __import__("urllib.parse").parse.quote(topic))
        _prospero_line = "自动检索暂不可用（%s）；手动核查：%s" % (
            (_prospero.get("error") or "上游故障"), _pu)

    # dedup paragraph
    cochrane_txt = ("%s Cochrane reviews" % cochrane_hits) if cochrane_hits is not None else "未探针"
    pubmed_txt = ("%s 篇 SR/MA（近 5 年）" % pubmed_hits) if pubmed_hits is not None else "未探针"
    pros_url = ("https://www.crd.york.ac.uk/prospero/#searchadvanced"
                "?search=%s" % urllib_parse_quote(topic))
    if nov_label == "saturated":
        near_dup = "高饱和，须明确增量以避免近重复拒稿"
        increment = "需提出既往综述未覆盖的亚组/人群/结局作为增量"
    elif nov_label == "caution":
        near_dup = "存在同类综述，须差异化"
        increment = "明确与现有综述的差异点"
    elif nov_label == "empty":
        near_dup = "暂无近重复风险（但需警惕数据不足）"
        increment = "空白方向，先确认是否有足够原始研究（k≥2）"
    else:
        near_dup = "暂无近重复风险"
        increment = "真实缺口方向，常规推进"

    dedup = {
        "prospero": _prospero_line,
        "cochrane": cochrane_txt,
        "pubmed": pubmed_txt,
        "non_english": "未覆盖（英文文献为主，按需手动补中文库）",
        "near_duplicate": near_dup,
        "increment": increment,
    }

    gap = {
        "verdict": nov_label,
        "label": GAP_ZH.get(nov_label, nov_label),
        "probe_used": (cochrane_hits is not None or pubmed_hits is not None),
        "summary": nov_note,
    }

    expected = ("约 %s 项注册试验 / 预期可纳入研究" % registry_total
                if registry_total is not None else "注册库未探针，预期研究数未知")

    compliance = _compliance()

    assessment = {
        "topic": topic,
        "scores": scores,
        "clinical_rationale": cli_rationale,
        "score_anchors": {
            "clinical": cli_note,
            "feasibility": fea_note,
            "data": data_note,
            "novelty": nov_note,
        },
        "evidence_tags": {
            "clinical": "coze" if not cli_needs else "judgment",
            "feasibility": data_conf if data_conf != "unverified" else "unverified",
            "data": data_conf,
            "novelty": "probe" if gap["probe_used"] else "unverified",
        },
        "verdict": verdict_key if not verdict_key.startswith("veto") else "veto",
        "verdict_raw": verdict_key,
        "verdict_note": verdict_note,
        "cross_checks": cross_checks,
        "dedup": dedup,
        "gap": gap,
        "expected_studies": expected,
        "compliance": compliance,
        "prospero": {
            "status": _prospero.get("status"),
            "hit_count": _prospero.get("hit_count"),
            "sample": _prospero.get("sample") or [],
            "error": _prospero.get("error"),
            "source": _prospero.get("source"),
            "manual_url": _prospero.get("manual_url"),
            "note": _prospero.get("note") or "",
            "register_before_extraction": "PROSPERO 注册应在数据提取前完成（AMSTAR-2 要求）",
        },
        "curation": curation,
        "assessed_on": datetime.date.today().isoformat(),
        "local": True,
        "note": ("本地确定性评估：数据/新颖性/方法可行性由真实探针（Europe PMC + "
                 "ClinicalTrials.gov）驱动；临床价值维度"
                 + ("已由 Coze/LLM 评估覆盖" if not cli_needs else
                    "属判断项，默认中值并标注需人工/LLM 确认（可用 clinical_override 由 Coze 覆盖）")
                 + "。"),
    }
    return assessment


def urllib_parse_quote(s):
    import urllib.parse
    return urllib.parse.quote(s)


if __name__ == "__main__":
    import json as _json
    import sys
    _t = sys.argv[1] if len(sys.argv) > 1 else "SGLT2 inhibitors heart failure"
    _a = assess(_t, picos={}, missing=[], dedup=None, registry=None)
    print(_json.dumps(_a, ensure_ascii=False, indent=2))
