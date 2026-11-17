#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reconstruct.py —— 认知架构自重构引擎（元之元·二阶）。

把智能体内部结构视为有向图，诊断五类架构坏味道并生成重构方案，
在虚拟图上复算健康分证明改善。纯标准库。

用法：
  python reconstruct.py diagnose --arch A.json
  python reconstruct.py selftest
"""
import sys, json, argparse
from collections import defaultdict

BOTTLENECK_DEGREE = 3          # 入度或出度 > 此值 → 瓶颈
EXPECTED_ROLES = ["planner", "executor", "verifier", "memory"]  # 关键角色
PENALTY = {"cycle": 0.30, "bottleneck": 0.15, "orphan": 0.08,
           "duplicate_role": 0.10, "missing_role": 0.12}


def find_cycles(nodes, edges):
    """Kahn 拓扑排序：残留节点即处于环中。"""
    indeg = {n: 0 for n in nodes}
    adj = defaultdict(list)
    for a, b in edges:
        if a in indeg and b in indeg:
            adj[a].append(b)
            indeg[b] += 1
    queue = [n for n, d in indeg.items() if d == 0]
    visited = 0
    while queue:
        n = queue.pop()
        visited += 1
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
    return sorted([n for n, d in indeg.items() if d > 0])


def diagnose(arch):
    nodes = {m["name"]: m.get("role", "") for m in arch.get("modules", [])}
    edges = [tuple(e) for e in arch.get("deps", [])]

    smells = []

    # 1. 环依赖
    cyc = find_cycles(set(nodes), edges)
    if cyc:
        smells.append({"type": "cycle", "nodes": cyc,
                       "fix": {"action": "break_cycle",
                               "detail": f"移除或反转环内一条边，如 {cyc[0]} 的回边，改为事件/异步解耦"}})

    # 2. 瓶颈（扇入/扇出过高）
    fan_in, fan_out = defaultdict(int), defaultdict(int)
    for a, b in edges:
        fan_out[a] += 1
        fan_in[b] += 1
    for n in sorted(nodes):
        if fan_in[n] > BOTTLENECK_DEGREE or fan_out[n] > BOTTLENECK_DEGREE:
            smells.append({"type": "bottleneck", "nodes": [n],
                           "fix": {"action": "split_module",
                                   "detail": f"把 {n} 按职责拆分为 2 个子模块分摊 {max(fan_in[n], fan_out[n])} 条依赖"}})

    # 3. 孤立模块
    connected = set()
    for a, b in edges:
        connected.add(a)
        connected.add(b)
    for n in sorted(nodes):
        if n not in connected:
            smells.append({"type": "orphan", "nodes": [n],
                           "fix": {"action": "connect_or_remove",
                                   "detail": f"{n} 无任何连边：接入主链路或归档移除"}})

    # 4. 职责重叠
    role_map = defaultdict(list)
    for n, r in nodes.items():
        if r:
            role_map[r].append(n)
    for r, ns in sorted(role_map.items()):
        if len(ns) >= 2:
            smells.append({"type": "duplicate_role", "nodes": sorted(ns),
                           "fix": {"action": "merge_modules",
                                   "detail": f"角色 {r} 有 {len(ns)} 个模块重叠：合并为一或显式分工"}})

    # 5. 缺失关键角色
    present_roles = set(nodes.values())
    for r in EXPECTED_ROLES:
        if r not in present_roles:
            smells.append({"type": "missing_role", "nodes": [],
                           "fix": {"action": "add_module",
                                   "detail": f"缺失关键角色 {r}：新增或指派模块承担"}})

    health = health_score(smells)
    return {"smells": smells, "health_before": health,
            "n_smells": len(smells),
            "proposals": [s["fix"] for s in smells]}


def health_score(smells):
    h = 1.0
    for s in smells:
        h -= PENALTY.get(s["type"], 0.05)
    return round(max(0.0, h), 4)


def apply_virtual(arch, smells):
    """在虚拟图上应用重构方案（模拟修复），返回新架构。"""
    modules = [dict(m) for m in arch.get("modules", [])]
    deps = [list(e) for e in arch.get("deps", [])]
    names = {m["name"] for m in modules}

    for s in smells:
        t = s["type"]
        if t == "cycle" and s["nodes"]:
            # 断环：删掉环内节点间的一条回边
            cyc = set(s["nodes"])
            for i, (a, b) in enumerate(deps):
                if a in cyc and b in cyc:
                    deps.pop(i)
                    break
        elif t == "bottleneck" and s["nodes"]:
            n = s["nodes"][0]
            half = n + "-aux"
            if half not in names:
                role = next((m.get("role", "") for m in modules if m["name"] == n), "")
                modules.append({"name": half, "role": role + "-aux"})
                names.add(half)
                # 把一半入边改挂到 aux
                ins = [i for i, (a, b) in enumerate(deps) if b == n]
                for i in ins[: len(ins) // 2]:
                    deps[i][1] = half
                deps.append([half, n])
        elif t == "orphan" and s["nodes"]:
            n = s["nodes"][0]
            anchor = next((m["name"] for m in modules if m["name"] != n), None)
            if anchor:
                deps.append([n, anchor])
        elif t == "duplicate_role" and len(s["nodes"]) >= 2:
            keep, drop = s["nodes"][0], s["nodes"][1]
            modules = [m for m in modules if m["name"] != drop]
            for e in deps:
                if e[0] == drop:
                    e[0] = keep
                if e[1] == drop:
                    e[1] = keep
            deps = [e for e in deps if e[0] != e[1]]
        elif t == "missing_role":
            detail = s["fix"]["detail"]
            role = detail.split("缺失关键角色 ")[1].split("：")[0] if "缺失关键角色 " in detail else "unknown"
            newname = "auto-" + role
            if newname not in names:
                modules.append({"name": newname, "role": role})
                names.add(newname)
                if modules and modules[0]["name"] != newname:
                    deps.append([modules[0]["name"], newname])
    return {"modules": modules, "deps": deps}


def reconstruct(arch):
    before = diagnose(arch)
    virt = apply_virtual(arch, before["smells"])
    after = diagnose(virt)
    return {
        "before": before,
        "health_after": after["health_before"],
        "improvement": round(after["health_before"] - before["health_before"], 4),
        "residual_smells": after["n_smells"],
        "adopt": after["health_before"] > before["health_before"],
    }


def selftest():
    # 构造一个五毒俱全的架构：
    # 环: A->B->C->A；瓶颈: hub 被 4 个模块依赖；孤儿: lonely；
    # 重复角色: p1/p2 都是 planner；缺失角色: memory 无人承担
    arch = {
        "modules": [
            {"name": "A", "role": "executor"},
            {"name": "B", "role": "verifier"},
            {"name": "C", "role": ""},
            {"name": "hub", "role": ""},
            {"name": "u1", "role": ""}, {"name": "u2", "role": ""},
            {"name": "u3", "role": ""}, {"name": "u4", "role": ""},
            {"name": "lonely", "role": ""},
            {"name": "p1", "role": "planner"},
            {"name": "p2", "role": "planner"},
        ],
        "deps": [
            ["A", "B"], ["B", "C"], ["C", "A"],
            ["u1", "hub"], ["u2", "hub"], ["u3", "hub"], ["u4", "hub"],
            ["p1", "A"], ["p2", "B"],
        ],
    }
    r = reconstruct(arch)
    before = r["before"]
    types = {s["type"] for s in before["smells"]}

    # 1. 五类坏味道全部检出
    for t in ["cycle", "bottleneck", "orphan", "duplicate_role", "missing_role"]:
        assert t in types, f"{t} 应被检出"
    # 2. 环内节点识别正确
    cyc = next(s for s in before["smells"] if s["type"] == "cycle")
    assert set(cyc["nodes"]) == {"A", "B", "C"}, f"环应为 A/B/C，实为 {cyc['nodes']}"
    # 3. 瓶颈是 hub
    bn = next(s for s in before["smells"] if s["type"] == "bottleneck")
    assert bn["nodes"] == ["hub"], "瓶颈应为 hub"
    # 4. 孤儿是 lonely
    orp = next(s for s in before["smells"] if s["type"] == "orphan")
    assert orp["nodes"] == ["lonely"], "孤儿应为 lonely"
    # 5. planner 重复
    dup = next(s for s in before["smells"] if s["type"] == "duplicate_role")
    assert set(dup["nodes"]) == {"p1", "p2"}, "重复角色应为 p1/p2"
    # 6. memory 缺失
    missing = [s for s in before["smells"] if s["type"] == "missing_role"]
    assert any("memory" in s["fix"]["detail"] for s in missing), "应报缺失 memory 角色"
    # 7. 重构后健康分上升且建议采纳
    assert r["improvement"] > 0, f"重构应提升健康分，实为 {r['improvement']}"
    assert r["adopt"] is True, "应建议采纳"
    # 8. 重构后坏味道数下降
    assert r["residual_smells"] < before["n_smells"], "重构后坏味道应减少"

    print("smells_before :", sorted(types))
    print("health_before :", before["health_before"])
    print("health_after  :", r["health_after"])
    print("improvement   :", r["improvement"])
    print("residual      :", r["residual_smells"], "/", before["n_smells"])
    print("\nSELFTEST: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    d = sub.add_parser("diagnose")
    d.add_argument("--arch", required=True)
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "selftest":
        return selftest()
    elif args.cmd == "diagnose":
        with open(args.arch, encoding="utf-8") as f:
            arch = json.load(f)
        print(json.dumps(reconstruct(arch), ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
