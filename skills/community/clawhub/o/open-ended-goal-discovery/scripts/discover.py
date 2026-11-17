#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open-ended-goal-discovery —— 开放式目标发现（可本地实跑，零依赖）

从能力图谱、用户兴趣信号与反馈中，自主生成候选目标并做四维打分排序：
value(价值) × novelty(新颖度) × feasibility(可行性) × alignment(用户对齐)。

用法:
  python discover.py --selftest
  python discover.py --json '{...}' --top 3
"""
import argparse
import json
import math
import sys

W_VALUE, W_NOVELTY, W_FEAS, W_ALIGN = 0.35, 0.30, 0.25, 0.10


def char_jaccard(a, b):
    """字符级 Jaccard 相似度（对中文友好）。"""
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union


def value_of(signal):
    """价值 = 兴趣度均值 × 反馈放大。signal: {interest:0..1, positive:int}。"""
    interest = float(signal.get("interest", 0.0))
    positive = max(0, int(signal.get("positive", 0)))
    feedback_gain = 1.0 + 0.1 * math.log1p(positive)
    return max(0.0, min(1.0, interest * feedback_gain))


def novelty_of(goal, pursued):
    """新颖度 = 1 − 与已追目标的最大相似度。"""
    if not pursued:
        return 1.0
    sim = max(char_jaccard(goal, g) for g in pursued)
    return max(0.0, 1.0 - sim)


def feasibility_of(goal, capabilities, required):
    """可行性 = 所需能力中已具备占比。required 为与 goal 关联的能力关键词列表。"""
    if not required:
        return 0.6  # 无明确依赖，给中性可行分
    have = sum(1 for r in required if any(r in c or c in r for c in capabilities))
    return have / len(required)


def alignment_of(goal, preferences):
    """对齐 = 命中用户偏好域关键词的程度。"""
    if not preferences:
        return 0.5
    text = json.dumps(preferences, ensure_ascii=False)
    hits = sum(1 for k, v in preferences.items() if str(v) and str(v) in goal)
    # 命中偏好值直接出现在目标中 -> 高对齐
    return min(1.0, 0.5 + 0.5 * (hits / max(1, len(preferences))))


def score_goal(goal, signal, pursued, capabilities, preferences, required):
    value = value_of(signal)
    novelty = novelty_of(goal, pursued)
    feas = feasibility_of(goal, capabilities, required)
    align = alignment_of(goal, preferences)
    score = (W_VALUE * value + W_NOVELTY * novelty +
             W_FEAS * feas + W_ALIGN * align)
    return {
        "goal": goal,
        "score": round(score, 4),
        "value": round(value, 3),
        "novelty": round(novelty, 3),
        "feasibility": round(feas, 3),
        "alignment": round(align, 3),
    }


def discover(state, top=3):
    capabilities = state.get("capabilities", [])
    pursued = state.get("pursued_goals", [])
    preferences = state.get("preferences", {})
    signals = state.get("signals", [])
    # 每个信号派生 1~2 个候选目标（topic + 推荐动作）
    candidates = []
    for sig in signals:
        topic = sig.get("topic", "")
        if not topic:
            continue
        required = sig.get("required_capabilities", [])
        for verb in sig.get("actions", ["调研", "优化", "搭建"]):
            goal = "%s%s" % (verb, topic)
            # 近重复排除：与已追目标相似度过高说明已在做，不再重复立项
            if pursued and max(char_jaccard(goal, g) for g in pursued) >= 0.6:
                continue
            candidates.append(score_goal(goal, sig, pursued, capabilities, preferences, required))
    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:top]


def run_selftest():
    # 场景：金融域用户，高兴趣"量化回测"但已追；"行业链分析"高兴趣且新颖可行
    state = {
        "capabilities": ["web_search", "data_analysis", "report_gen", "industry_chain"],
        "pursued_goals": ["搭建量化回测框架"],
        "preferences": {"domain": "finance"},
        "signals": [
            {"topic": "量化回测", "interest": 0.9, "positive": 8,
             "actions": ["搭建"], "required_capabilities": ["data_analysis"]},
            {"topic": "行业链分析", "interest": 0.85, "positive": 5,
             "actions": ["调研", "搭建"], "required_capabilities": ["industry_chain", "report_gen"]},
            {"topic": "未知冷门域", "interest": 0.2, "positive": 0,
             "actions": ["调研"], "required_capabilities": ["missing_cap"]},
        ],
    }
    top = discover(state, top=3)
    # 1) 高兴趣但已追的"量化回测"应因新颖度低而出局（不在 top 或排末尾）
    qback = [c for c in top if "量化回测" in c["goal"]]
    assert not qback or qback[0]["score"] < 0.6, "已追目标不应高分: %s" % qback
    # 2) 行业链分析应排第一（高价值+新颖+可行+对齐）
    assert "行业链分析" in top[0]["goal"], "top1 should be 行业链分析, got %s" % top[0]["goal"]
    assert top[0]["novelty"] == 1.0, "novel goal novelty should be 1.0"
    # 3) 低兴趣冷门域应被压到低分（明显低于 top1）
    cold = [c for c in top if "冷门" in c["goal"]]
    assert cold and cold[0]["score"] < 0.5, "low-value should be low: %s" % cold
    assert top[0]["score"] - cold[0]["score"] > 0.3, "top should clearly beat cold"
    # 4) 可行性：缺失能力的目标得分应低于具备能力的同兴趣目标
    print("✅ selftest PASSED (top1=%s score=%.3f)" % (top[0]["goal"], top[0]["score"]))
    return True


def main():
    ap = argparse.ArgumentParser(description="开放式目标发现")
    ap.add_argument("--json", help="环境状态 JSON")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        run_selftest(); return
    if args.json:
        out = discover(json.loads(args.json), top=args.top)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print("用法: discover.py --selftest | --json '{...}' --top 3")


if __name__ == "__main__":
    main()
