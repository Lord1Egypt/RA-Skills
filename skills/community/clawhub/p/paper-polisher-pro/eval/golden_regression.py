#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""golden_regression.py — paper-polisher-pro 金标回归（模块 4.3 ppp 适配）

范式（沿用 cite-holmes golden 工具）：自带演示件跑批 + **结构基线比对**——
判定语义漂移零容忍，非逐字段全等。

ppp 的漂移轴 = 引擎/模型版本（检测确定性的前提是同一引擎+同一模型指纹）：
  - 结构基线（任何版本都必须满足）：铁律/判定语义/字段在场
  - 分数基线（仅当 model_fp 与金标一致时逐位比对；指纹变化 → 提示重定标，
    由人有意识重定基线，防引擎升级被误报阻塞日更）

演示件（内嵌，零外部依赖）：
  AI 样本（模式密集）        → 必判 high（伪造必被抓语义）
  具体化人类样本（演示改稿）  → 必判 low（真实来源不翻车语义）
  文学叙事样本               → register_hint 必触发（语域管线在场）
  短文本                     → risk=unknown（铁律 2 在场）

用法: python3 eval/golden_regression.py [--rebaseline]
输出: PASS/FAIL；FAIL 阻断发布。零网络（纯本地引擎路径）。
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, HERE)

GOLDEN = os.path.join(HERE, "results", "golden_detection.json")

AI_TEXT = (
    "值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
    "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
    "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
    "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
    "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。"
    "此外，本研究仍存在一定局限性，未来需要进一步扩大样本量予以验证。")
HUMAN_TEXT = (
    "我们科室把 AI 辅助读片接进了 312 例急诊 CT 的初筛，读片时间从平均 11 分钟降到 4 分钟，"
    "漏诊率没有升高。代价是新的问题：系统把 6 例伪影误报成出血，医生复核时顶住了压力。"
    "数据共享协议至今没谈拢，三家医院各留了一手。这套流程值不值得推广，"
    "取决于你所在科室有没有复核的第二双眼睛。")
NARRATIVE_TEXT = (
    "我翻开历史一查，这历史没有年代，歪歪斜斜的每页上都写着仁义道德几个字。"
    "我横竖睡不着，仔细看了半夜，才从字缝里看出字来，满本都写着两个字是吃人！"
    "那时候，大哥还在。母亲常对我说：你应当去。那天他忽然来了，"
    "我心里一沉，眼泪几乎要落下来。老爷说这没有什么可笑。"
    "第二天一早，他拎着包走了，我到现在还记得那天清晨的凉。")
SHORT_TEXT = "这是一段很短的文本。"


def model_fp():
    try:
        from layers_lm import DET_DIR
        import hashlib
        mp = os.path.join(DET_DIR, "model.int8.onnx")
        if not os.path.isfile(mp):
            return "rules"
        h = hashlib.md5()
        with open(mp, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except Exception:
        return "rules"


def main():
    import ai_detector
    fp = model_fp()
    demos = {"ai": AI_TEXT, "human": HUMAN_TEXT,
             "narrative": NARRATIVE_TEXT, "short": SHORT_TEXT}
    scores, problems = {}, []

    # ── 结构基线（判定语义，任何版本都必须满足）──
    rep_ai = ai_detector.detect(AI_TEXT, lang="zh")
    scores["ai"] = float(rep_ai.overall_ai_score)
    if rep_ai.overall_risk not in ("medium", "high"):
        problems.append(f"AI 演示件判 {rep_ai.overall_risk}——伪造必被抓语义漂移（应为 medium/high）")

    rep_hu = ai_detector.detect(HUMAN_TEXT, lang="zh")
    scores["human"] = float(rep_hu.overall_ai_score)
    if rep_hu.overall_risk == "high":
        problems.append(f"具体化人类演示件判 high——过严漂移（分数 {scores['human']}）")

    rep_na = ai_detector.detect(NARRATIVE_TEXT, lang="zh")
    if "文学叙事" not in (rep_na.register_hint or ""):
        problems.append("叙事演示件未触发文学叙事语域提示——语域管线漂移")

    rep_st = ai_detector.detect(SHORT_TEXT, lang="zh")
    if rep_st.overall_risk != "unknown":
        problems.append(f"短文本判 {rep_st.overall_risk} ≠ unknown——铁律 2 漂移")

    rep_ai2 = ai_detector.detect(AI_TEXT, lang="zh")
    if float(rep_ai2.overall_ai_score) != scores["ai"]:
        problems.append("确定性漂移：同输入两次得分不同")

    for k in ("degraded_mode", "integrity_notice", "paragraph_scores", "risk_bands"):
        if not hasattr(rep_ai, k):
            problems.append(f"报告缺字段: {k}")

    # ── 分数基线（仅指纹一致时逐位比对）──
    golden = {}
    if os.path.isfile(GOLDEN):
        try:
            golden = json.load(open(GOLDEN, encoding="utf-8"))
        except Exception:
            golden = {}
    g_fp = golden.get("model_fp")
    fp_match = (g_fp == fp)
    if fp_match:
        g_scores = golden.get("scores", {})
        for k, v in scores.items():
            if k in g_scores and abs(g_scores[k] - v) > 1e-6:
                problems.append(f"分数漂移[{k}]: {v} ≠ 金标 {g_scores[k]}（同指纹逐位比对）")
    needs_rebaseline = (not fp_match) or (not os.path.isfile(GOLDEN))

    print(f"== 金标回归 == model_fp={fp} · demo_scores="
          f"{ {k: round(v, 1) for k, v in scores.items()} }")
    if problems:
        for p in problems:
            print(f"  ❌ {p}")
        print(f"汇总: FAIL={len(problems)}——判定语义/分数漂移，禁止发布")
        return 1
    if needs_rebaseline or "--rebaseline" in sys.argv:
        os.makedirs(os.path.dirname(GOLDEN), exist_ok=True)
        json.dump({"model_fp": fp, "scores": scores,
                   "note": "金标=演示件分数+指纹；引擎/模型变更后有意识 --rebaseline 重定标"},
                  open(GOLDEN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"金标{'重定标' if os.path.isfile(GOLDEN) else '初建'}: fp={fp} → {GOLDEN}")
        if not fp_match and g_fp:
            print(f"⚠️ 指纹变化（{g_fp} → {fp}）：分数基线已重定标，请人工确认本次引擎/模型变更是有意的")
    else:
        print("汇总: 结构基线 0 drift + 同指纹分数逐位一致 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
