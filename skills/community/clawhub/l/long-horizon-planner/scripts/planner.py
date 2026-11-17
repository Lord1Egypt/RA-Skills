#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
planner.py — 长程自主规划引擎（超越性元能力 #1）

设计依据（2025-2026 主流研究）：
  - HiPlan：分层规划，分离「全局里程碑 (Milestone Action Guide)」与「局部分步提示 (Step-Wise Hints)」
  - Plan-and-Act / Plan-and-Execute：PLANNER 管「做什么」(战略)，EXECUTOR 管「怎么做」(战术)，解耦以抗 goal drift
  - LaMMA-P：LLM 语义理解 + 经典规划器(PDDL)融合，把高层目标拆成带依赖的子任务
  - 最佳实践：显式层次分解 / 模块化解耦上下文 / rubric(plan anchor)防级联错误 / 闭环动态重规划 / 关键路径与依赖 DAG

本脚本不依赖 LLM，提供**确定性可复跑**的规划原语：
  - 里程碑 DAG（节点 + 依赖 + 工期估测）
  - 拓扑排序 + 环检测
  - 关键路径（最长路径）计算
  - 下一步可执行节点（依赖已满足）推荐
  - 进度推进与 Markdown 报告

用法：
  python planner.py init   --goal "..." --out plan.json [--horizon 21]
  python planner.py add    plan.json --id design --name "方案设计" --dep discover --est 5
  python planner.py graph  plan.json
  python planner.py next   plan.json
  python planner.py advance plan.json --id build --done
  python planner.py critical plan.json
  python planner.py report plan.json --out plan.md
"""
import os, sys, json, argparse, datetime

# 默认里程碑模板（领域无关的高层阶段骨架）
DEFAULT_PHASES = [
    ("discover", "探索与定义目标边界 / 约束 / 验收标准", 3),
    ("design",   "方案设计与关键架构 / 技术决策", 5),
    ("build",    "分步实现核心交付物", 8),
    ("verify",   "验证、测试与外部校验 (tool-grounded)", 3),
    ("ship",     "发布、复盘与知识沉淀", 2),
]


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def load_plan(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_plan(path, data):
    data["updated"] = now()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def topo_order(nodes):
    """返回拓扑序；若成环返回 (None, cycle_nodes)。"""
    indeg = {nid: 0 for nid in nodes}
    adj = {nid: [] for nid in nodes}
    for nid, n in nodes.items():
        for d in n.get("deps", []):
            if d in nodes:
                adj[d].append(nid)
                indeg[nid] += 1
    from collections import deque
    q = deque([n for n, d in indeg.items() if d == 0])
    order = []
    while q:
        x = q.popleft()
        order.append(x)
        for y in adj[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
    if len(order) != len(nodes):
        return None, [n for n in nodes if n not in order]
    return order, None


def longest_path(nodes):
    """关键路径：以 est 为权重的最长路径（含路径与总工期）。"""
    order, cyc = topo_order(nodes)
    if order is None:
        return None, None
    dist = {}
    parent = {}
    for n in order:
        best = 0
        par = None
        for d in nodes[n].get("deps", []):
            if d in nodes and dist.get(d, 0) > best:
                best = dist[d]
                par = d
        dist[n] = best + nodes[n].get("est", 0)
        parent[n] = par
    end = max(dist, key=lambda k: dist[k])
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path, dist[end]


def next_actions(nodes):
    res = []
    for nid, n in nodes.items():
        if n.get("status") == "done":
            continue
        deps = n.get("deps", [])
        if all(nodes.get(d, {}).get("status") == "done" for d in deps):
            res.append(nid)
    return res


# ---------------- subcommands ----------------
def cmd_init(a):
    nodes = {}
    prev = None
    for i, (pid, pname, est) in enumerate(DEFAULT_PHASES):
        nodes[pid] = {
            "id": pid, "name": pname, "est": est,
            "deps": [prev] if prev else [], "status": "todo", "note": "",
        }
        prev = pid
    data = {
        "name": "long-horizon-plan",
        "goal": a.goal,
        "horizon_days": a.horizon,
        "created": now(),
        "updated": now(),
        "nodes": nodes,
    }
    save_plan(a.out, data)
    print(f"✅ 已初始化计划 -> {a.out}")
    print(f"   目标: {a.goal}")
    print(f"   里程碑: {', '.join(DEFAULT_PHASES[i][0] for i in range(len(DEFAULT_PHASES)))}")
    print("   提示: 用 add 增删里程碑，用 graph/critical 看依赖与关键路径。")


def cmd_add(a):
    d = load_plan(a.plan)
    n = {
        "id": a.id, "name": a.name, "est": a.est,
        "deps": [x.strip() for x in (a.dep or "").split(",") if x.strip()],
        "status": "todo", "note": "",
    }
    d["nodes"][a.id] = n
    save_plan(a.plan, d)
    print(f"✅ 已添加里程碑 {a.id}（依赖: {n['deps'] or '无'}）")


def cmd_graph(a):
    d = load_plan(a.plan)
    order, cyc = topo_order(d["nodes"])
    if order is None:
        print(f"❌ 检测到依赖环: {cyc}")
        return
    print(f"📊 计划: {d.get('goal','')}  | 拓扑序:")
    for i, nid in enumerate(order, 1):
        n = d["nodes"][nid]
        print(f"  {i}. {nid} [{n.get('status','todo')}] est={n.get('est',0)}d  <- {n.get('deps',[])}")


def cmd_next(a):
    d = load_plan(a.plan)
    na = next_actions(d["nodes"])
    print("➡️  下一步可执行的里程碑（依赖已满）：")
    for nid in na:
        n = d["nodes"][nid]
        print(f"   - {nid}: {n.get('name','')} (est={n.get('est',0)}d)")


def cmd_advance(a):
    d = load_plan(a.plan)
    if a.id not in d["nodes"]:
        print(f"❌ 无此里程碑: {a.id}")
        return
    d["nodes"][a.id]["status"] = "done" if a.done else "doing"
    save_plan(a.plan, d)
    print(f"✅ {a.id} -> {d['nodes'][a.id]['status']}")


def cmd_critical(a):
    d = load_plan(a.plan)
    path, total = longest_path(d["nodes"])
    if path is None:
        print("❌ 依赖成环，无法计算关键路径")
        return
    print(f"🎯 关键路径（最长工期 {total}d）：")
    for nid in path:
        n = d["nodes"][nid]
        print(f"   {nid} (est={n.get('est',0)}d)")
    print(f"   总工期 ≈ {total}d；缩短关键路径上的里程碑最能提前交付。")


def cmd_report(a):
    d = load_plan(a.plan)
    nodes = d["nodes"]
    order, cyc = topo_order(nodes)
    path, total = longest_path(nodes)
    done = sum(1 for n in nodes.values() if n.get("status") == "done")
    lines = [
        f"# 长程规划进度报告 · {d.get('goal','')}",
        "",
        f"- 生成时间: {now()}",
        f"- 里程碑总数: {len(nodes)} ｜ 已完成: {done} ｜ 完成度: {done/len(nodes)*100:.0f}%",
        f"- 预估总工期: {total}d（关键路径）",
        "",
        "## 里程碑状态",
        "",
        "| 阶段 | 名称 | 工期 | 依赖 | 状态 |",
        "|------|------|------|------|------|",
    ]
    seq = order if order else list(nodes)
    for nid in seq:
        n = nodes[nid]
        lines.append(f"| {nid} | {n.get('name','')} | {n.get('est',0)}d | {', '.join(n.get('deps',[])) or '—'} | {n.get('status','todo')} |")
    lines += ["", "## 关键路径", ""]
    lines += [f"- {nid}" for nid in (path or [])]
    lines += ["", "## 下一步可执行", ""]
    lines += [f"- {nid}" for nid in next_actions(nodes)] or ["（无，待重规划）"]
    out = a.out or (os.path.splitext(a.plan)[0] + ".md")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"✅ 报告已写入 {out}")


def main():
    ap = argparse.ArgumentParser(description="长程自主规划引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("--goal", required=True); p.add_argument("--out", required=True); p.add_argument("--horizon", type=int, default=21)
    p.set_defaults(func=cmd_init)
    p = sub.add_parser("add"); p.add_argument("plan"); p.add_argument("--id", required=True); p.add_argument("--name", required=True); p.add_argument("--dep", default=""); p.add_argument("--est", type=int, default=3)
    p.set_defaults(func=cmd_add)
    p = sub.add_parser("graph"); p.add_argument("plan"); p.set_defaults(func=cmd_graph)
    p = sub.add_parser("next"); p.add_argument("plan"); p.set_defaults(func=cmd_next)
    p = sub.add_parser("advance"); p.add_argument("plan"); p.add_argument("--id", required=True); p.add_argument("--done", action="store_true")
    p.set_defaults(func=cmd_advance)
    p = sub.add_parser("critical"); p.add_argument("plan"); p.set_defaults(func=cmd_critical)
    p = sub.add_parser("report"); p.add_argument("plan"); p.add_argument("--out")
    p.set_defaults(func=cmd_report)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
