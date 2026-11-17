#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""native-autonomous-discovery: 开放问题的自主假设-实验-收敛科研闭环。

用法:
  python discover.py --selftest
  python discover.py --space space.json --observe observer.py [--budget 30] [--threshold 0.85]

约定：
  - space: 候选假设列表 ["H1","H2",...]（或 {"hypotheses":[...], "constraints":{}}）
  - observe(hyp) -> float in [0,1]：观测器对假设的评分（证据强度）
  - 闭环：每轮对各假设累加证据(指数滑动平均)，达 threshold 且轮次>=min_rounds 即收敛；
          长期低证据假设被剪枝(停止再抽样)，剩余假设按比例分配抽样预算。
"""
import os, sys, json, random


def load_space(path):
    if isinstance(path, (list, tuple)):
        return list(path)
    d = json.load(open(path, encoding="utf-8"))
    if isinstance(d, list):
        return d
    return d.get("hypotheses", [])


def run(hypotheses, observe, budget=30, threshold=0.85, min_rounds=5, seed=0):
    """返回 (best, confidence, rounds, trajectory, converged)。"""
    rng = random.Random(seed)
    evid = {h: 0.0 for h in hypotheses}      # 累计证据(EMA)
    counts = {h: 0 for h in hypotheses}
    alpha = 0.5                               # EMA 平滑
    trajectory = []
    alive = list(hypotheses)
    rounds = 0
    while rounds < budget:
        rounds += 1
        # 给仍存活、累计采样少的假设分配观测（兼顾探索与利用）
        target = min(alive, key=lambda h: (counts[h], -evid[h]))
        s = float(observe(target))
        evid[target] = alpha * s + (1 - alpha) * evid[target]
        counts[target] += 1
        best = max(alive, key=lambda h: evid[h])
        trajectory.append({"round": rounds, "hyp": best, "score": round(evid[best], 3)})
        # 剪枝：远低于当前最优且已采样足够的假设
        top = evid[best]
        alive = [h for h in alive
                 if not (counts[h] >= 3 and evid[h] < top - 0.3)]
        # 收敛：最优证据达标且已过最少轮次
        if evid[best] >= threshold and rounds >= min_rounds and len(alive) <= 1:
            return best, round(evid[best], 3), rounds, trajectory, True
    best = max(evid, key=lambda h: evid[h])
    return best, round(evid[best], 3), rounds, trajectory, evid[best] >= threshold


def selftest():
    # 真实目标 H3，观测器对 H3 给高分、其余给低分（带轻微噪声）
    rng = random.Random(7)
    truth = "H3"
    def observe(h):
        base = 0.95 if h == truth else 0.2
        return max(0.0, min(1.0, base + rng.uniform(-0.05, 0.05)))
    hyps = ["H1", "H2", "H3", "H4", "H5"]
    best, conf, rounds, traj, conv = run(hyps, observe, budget=40, threshold=0.85, seed=3)
    try:
        assert best == truth, f"应收敛到 {truth}，实际 {best}（conf={conf}）"
        assert conf >= 0.85, f"置信度应达阈值: {conf}"
        assert conv is True, f"应已收敛: {conv}"
        assert rounds < 40, f"应能在预算内收敛: rounds={rounds}"
        # 证据轨迹末端应稳定指向 H3
        assert traj[-1]["hyp"] == truth, f"末轮未指向最优: {traj[-1]}"
        print("🧪 selftest PASS：best=%s conf=%.2f rounds=%d converged=%s"
              % (best, conf, rounds, conv))
        return 0
    except AssertionError as e:
        print("❌ selftest FAIL:", e); return 1


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    # 真实模式：从 --space / --observe 载入（此处仅做骨架校验）
    space = next((a for i, a in enumerate(args) if a == "--space" and i + 1 < len(args)), None)
    obs = next((a for i, a in enumerate(args) if a == "--observe" and i + 1 < len(args)), None)
    if not space or not obs:
        print("⚠️ 未提供 --space/--observe，回退到 --selftest 演示。")
        return selftest()
    hyps = load_space(space)
    import importlib.util
    spec = importlib.util.spec_from_file_location("obs", obs)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    best, conf, rounds, traj, conv = run(hyps, mod.observe)
    print(json.dumps({"best": best, "confidence": conf, "rounds": rounds,
                      "converged": conv, "trajectory": traj}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
