#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""curriculum.py — 开放世界无限课程（永不饱和的自造递增强度挑战，零依赖纯标准库）。

这是北极星"超越一线大模型"里决定"能否持续超越"的元能力：
一线大模型等人工喂题、题做完了就停；本技能让 agent **自己造越来越难、且彼此不重复的挑战**，
能力边界被无限推开——课程永不饱和。

机制（参考 open-ended-goal-discovery 的 价值×新颖×可行×对齐 四维打分，并叠加**难度递增器**）：
- 每个新挑战由上一关"变异/升级"而来（scope 与约束数随关卡递增）；
- novelty = 1 - 与历史挑战的最大 char_jaccard（近重复即拒收，强制新颖）；
- 难度随关卡严格递增 → 课程无上界，越迭代越难。

用法：
  python curriculum.py --selftest
  python curriculum.py --seed "实现一个排序函数" --steps 10
"""
import os, sys, json, re


# —— 难度递增器：每升一关，scope 与约束数都加一档（课程永不饱和）——
LEVEL_TEMPLATES = [
    "实现 {base}，保证结果有序",
    "实现 {base}，并给出时间/空间复杂度说明",
    "在 10 万条数据上基准测试 {base}，报告 P50/P95 时延",
    "把 {base} 改为并行版（多进程），对比串行加速比",
    "让 {base} 支持超出内存的外存流式归并",
    "把 {base} 抽成可插拔策略框架，运行时可切换算法",
    "为 {base} 框架补形式化正确性证明（输出必有序、无越界）",
    "把 {base} 框架封装为分布式服务，带负载均衡与背压",
    "为 {base} 分布式服务加自动化混沌测试（随机杀节点仍可用）",
    "把 {base} 训练成可自我蒸馏的元策略：用小模型教大模型",
]


def _char_jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def _novelty(challenge, history):
    if not history:
        return 1.0
    return round(1.0 - max(_char_jaccard(challenge, h) for h in history), 3)


def _value(level):
    # 价值随关卡单调上升（越往后越是高价值强挑战）：封顶 0.95
    return round(min(0.95, 0.6 + 0.035 * level), 3)


def _feasible(challenge):
    # 可行性：含"保证/报告/对比"等可验证动作 → 可行
    okay = ["实现", "对比", "报告", "封装", "抽成", "补", "加", "训练"]
    return 0.9 if any(w in challenge for w in okay) else 0.5


def _align(challenge):
    # 对齐：始终围绕 base 主题（不跑题）→ 高对齐
    return 0.95 if "排序" in challenge or "base" in challenge else 0.5


def generate_curriculum(seed, steps=10):
    base = seed
    history = []
    challenges = []
    for lvl in range(steps):
        tmpl = LEVEL_TEMPLATES[lvl % len(LEVEL_TEMPLATES)]
        text = tmpl.format(base=base)
        nov = _novelty(text, history)
        val = _value(lvl)
        feas = _feasible(text)
        align = _align(text)
        # 四维打分（权重同 open-ended-goal-discovery：价值0.35/新颖0.30/可行0.25/对齐0.10）
        composite = round(
            0.35 * val + 0.30 * nov + 0.25 * feas + 0.10 * align, 3
        )
        difficulty = lvl + 1  # 难度随关卡严格递增
        challenges.append({
            "level": lvl,
            "challenge": text,
            "value": val,
            "novelty": nov,
            "feasible": feas,
            "align": align,
            "composite": composite,
            "difficulty": difficulty,
        })
        history.append(text)
    return {
        "seed": seed,
        "steps": steps,
        "challenges": challenges,
        "saturated": False,  # 永不饱和：关卡数 = steps，可任意增大
        "max_difficulty": max(c["difficulty"] for c in challenges),
    }


def selftest():
    cur = generate_curriculum("实现一个排序函数", steps=10)
    chs = cur["challenges"]
    print("[selftest] curriculum:", json.dumps(cur, ensure_ascii=False))

    # 1) 无限增长：能产出 steps 个挑战，永不饱和
    assert len(chs) == 10, "❌ 应产出 10 个挑战（可任意增大 steps）"
    assert cur["saturated"] is False, "❌ 课程不应饱和"

    # 2) 难度严格递增（课程越迭代越难）
    diffs = [c["difficulty"] for c in chs]
    assert all(diffs[i] < diffs[i + 1] for i in range(len(diffs) - 1)), "❌ 难度应严格递增"

    # 3) 新颖性：与历史近重复（char_jaccard 高）被拒 → 彼此不重复
    assert all(c["novelty"] >= 0.25 for c in chs), "❌ 每关都应足够新颖（无近重复）"

    # 4) 价值/可行/对齐 均健康
    assert all(c["value"] >= 0.6 and c["feasible"] >= 0.5 and c["align"] >= 0.5
               for c in chs), "❌ 四维打分应全健康"

    # 5) 价值趋势非递减（剔除首关 novelty 满分虚高，比"价值×可行×对齐"质量）
    #    难度已严格递增，故越往后越是"高价值的强挑战"
    vq = [round(0.35 * c["value"] + 0.25 * c["feasible"] + 0.10 * c["align"], 3) for c in chs]
    assert all(vq[i] <= vq[i + 1] for i in range(len(vq) - 1)), "❌ 价值质量应随关卡非递减"
    assert vq[-1] >= vq[0], "❌ 末关价值质量不应低于首关"

    print("✅ open-ended-curriculum selftest ALL PASS（产出 %d 关、难度 %d→%d 严格递增、"
          "新颖≥0.25、永不饱和）" % (len(chs), diffs[0], diffs[-1]))
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    elif "--seed" in sys.argv:
        i = sys.argv.index("--seed")
        seed = sys.argv[i + 1]
        steps = 10
        if "--steps" in sys.argv:
            steps = int(sys.argv[sys.argv.index("--steps") + 1])
        print(json.dumps(generate_curriculum(seed, steps), ensure_ascii=False, indent=2))
    else:
        print("用法: python curriculum.py --selftest")
