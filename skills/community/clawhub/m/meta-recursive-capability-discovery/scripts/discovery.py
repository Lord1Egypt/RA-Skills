#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
discovery.py —— 递归能力发现引擎（元之元·二阶）。

核心：让 agent 自己发现"缺什么能力"，把开放目标的需求能力与现有技能覆盖做递归差集，
下钻到可构建的原子能力叶子，并做二阶盲区自省。

纯标准库，无第三方依赖。
用法：
  python discovery.py discover --registry R.json --goal G.json
  python discovery.py selftest
"""
import sys, json, argparse

# 二阶自省用的能力维度矩阵（发现器"应该想到去查"的维度）
CAPABILITY_DIMENSIONS = [
    "perception", "planning", "execution", "memory",
    "verification", "alignment", "metacognition",
]


def build_covered(registry):
    """把技能 registry 汇成已覆盖能力集合。"""
    covered = set()
    provider = {}  # cap -> [skills]
    for sk in registry.get("skills", []):
        name = sk.get("name", "?")
        for cap in sk.get("provides", []):
            covered.add(cap)
            provider.setdefault(cap, []).append(name)
    return covered, provider


def discover(registry, goal):
    """递归发现能力缺口，返回发现树 + 缺口分类。"""
    covered, provider = build_covered(registry)
    decompose = goal.get("decompose", {})   # cap -> [子能力]
    requires = list(goal.get("requires", []))

    tree = []          # 发现树节点
    leaf_gaps = []     # 叶子缺口（可构建）
    mid_gaps = []      # 中间缺口（可分解，先下钻）
    covered_hits = []  # 已覆盖

    seen = set()
    # BFS，带 (cap, depth, parent_chain)
    queue = [(c, 0, []) for c in requires]
    # 统计被依赖次数（用于优先级）
    dep_count = {}
    for cap, subs in decompose.items():
        for s in subs:
            dep_count[s] = dep_count.get(s, 0) + 1

    while queue:
        cap, depth, chain = queue.pop(0)
        if cap in seen:
            continue
        seen.add(cap)
        node = {"capability": cap, "depth": depth, "parent_chain": chain}

        if cap in covered:
            node["status"] = "covered"
            node["providers"] = provider.get(cap, [])
            covered_hits.append(cap)
        elif cap in decompose:
            node["status"] = "decomposable"
            node["children"] = decompose[cap]
            mid_gaps.append(cap)
            for s in decompose[cap]:
                queue.append((s, depth + 1, chain + [cap]))
        else:
            node["status"] = "leaf_gap"
            # 优先级：深度越浅 + 被依赖越多 → 越优先
            node["priority"] = round((1.0 / (1 + depth)) + 0.5 * dep_count.get(cap, 0), 4)
            leaf_gaps.append(node)
        tree.append(node)

    # 按优先级排序叶子缺口
    leaf_gaps_sorted = sorted(leaf_gaps, key=lambda n: n["priority"], reverse=True)

    # 二阶盲区自省：发现结果覆盖了哪些维度
    all_caps_touched = set(seen)
    tagged_dims = set()
    dim_hints = goal.get("dimension_tags", {})  # cap -> dimension
    for cap in all_caps_touched:
        d = dim_hints.get(cap)
        if d:
            tagged_dims.add(d)
    blind_spots = [d for d in CAPABILITY_DIMENSIONS if d not in tagged_dims]

    return {
        "covered": sorted(covered_hits),
        "mid_gaps": sorted(mid_gaps),
        "leaf_gaps": leaf_gaps_sorted,
        "leaf_gap_names": [n["capability"] for n in leaf_gaps_sorted],
        "blind_spots": blind_spots,
        "tree_size": len(tree),
        "summary": {
            "n_covered": len(covered_hits),
            "n_mid": len(mid_gaps),
            "n_leaf": len(leaf_gaps),
            "n_blind": len(blind_spots),
        },
    }


def _load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def selftest():
    """构造一个目标：需要 autonomy，可分解到叶子；registry 只覆盖部分。"""
    registry = {"skills": [
        {"name": "long-horizon-planner", "provides": ["planning"]},
        {"name": "continual-memory-engine", "provides": ["memory"]},
        {"name": "code-self-verifier", "provides": ["verification"]},
    ]}
    goal = {
        "requires": ["autonomy"],
        "decompose": {
            "autonomy": ["planning", "execution", "self_reflection"],
            "self_reflection": ["verification", "metacognition_monitor"],
            "execution": ["tool_use"],
        },
        "dimension_tags": {
            "planning": "planning",
            "execution": "execution",
            "memory": "memory",
            "verification": "verification",
            "metacognition_monitor": "metacognition",
            "tool_use": "execution",
            "self_reflection": "verification",
        },
    }
    r = discover(registry, goal)
    ok = True

    # 1. planning/verification 已覆盖
    assert "planning" in r["covered"], "planning 应已覆盖"
    assert "verification" in r["covered"], "verification 应已覆盖"
    # 2. autonomy / self_reflection / execution 为可分解中间缺口
    for m in ["autonomy", "self_reflection", "execution"]:
        assert m in r["mid_gaps"], f"{m} 应为中间缺口"
    # 3. 叶子缺口应含 tool_use 和 metacognition_monitor（未覆盖且不可再分解）
    assert "tool_use" in r["leaf_gap_names"], "tool_use 应为叶子缺口"
    assert "metacognition_monitor" in r["leaf_gap_names"], "metacognition_monitor 应为叶子缺口"
    # 4. 不应把已覆盖的 planning 误报为缺口
    assert "planning" not in r["leaf_gap_names"], "已覆盖不应报缺口"
    # 5. 优先级排序：tool_use(depth2,被依赖1) vs metacognition_monitor(depth2,被依赖1)
    assert len(r["leaf_gaps"]) >= 2, "至少 2 个叶子缺口"
    assert r["leaf_gaps"][0]["priority"] >= r["leaf_gaps"][-1]["priority"], "叶子缺口应按优先级降序"
    # 6. 二阶盲区：goal 的需求树从未触及 perception/alignment/memory 维度 → 被识别为盲区
    #    （这正是二阶自省的价值：发现"发现器自己没想到去查的维度"）
    assert "perception" in r["blind_spots"], "perception 维度应为盲区"
    assert "alignment" in r["blind_spots"], "alignment 维度应为盲区"
    assert "memory" in r["blind_spots"], "goal 未涉及 memory 维度 → 应为盲区"
    # 7. 需求树触及的维度不应误报为盲区
    assert "planning" not in r["blind_spots"], "planning 已触及不应为盲区"
    assert "metacognition" not in r["blind_spots"], "metacognition 已触及不应为盲区"

    print("covered      :", r["covered"])
    print("mid_gaps     :", r["mid_gaps"])
    print("leaf_gaps    :", [(n["capability"], n["priority"]) for n in r["leaf_gaps"]])
    print("blind_spots  :", r["blind_spots"])
    print("summary      :", r["summary"])
    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    d = sub.add_parser("discover")
    d.add_argument("--registry", required=True)
    d.add_argument("--goal", required=True)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    elif args.cmd == "discover":
        r = discover(_load(args.registry), _load(args.goal))
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    else:
        ap.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
