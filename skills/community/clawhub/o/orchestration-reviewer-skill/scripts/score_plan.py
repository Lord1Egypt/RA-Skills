#!/usr/bin/env python3
"""Score a plan based on structural metrics."""
import argparse, json, sys
from collections import defaultdict

WEIGHTS = {
    "goal_alignment": 0.25,
    "topology_soundness": 0.20,
    "skill_binding": 0.15,
    "scope_safety": 0.15,
    "executability": 0.10,
    "efficiency_complexity": 0.10,
    "risk_governance": 0.05,
}

def _extract_plan_ir(raw: dict) -> dict:
    """从 reviewer 输入或纯 plan 输入中提取 Plan IR。"""
    if "existing_plan_ir" in raw:
        return raw["existing_plan_ir"]
    if "plan_ir" in raw:
        return raw["plan_ir"]
    return raw

def score_plan(plan_path: str, manifest_path: str, business_goal: str = "") -> dict:
    with open(plan_path) as f:
        raw = json.load(f)
    plan_ir = _extract_plan_ir(raw)
    nodes = plan_ir.get("nodes", [])
    edges = plan_ir.get("edges", [])
    node_ids = {n["node_id"] for n in nodes}
    
    with open(manifest_path) as f:
        raw = json.load(f)
    manifest = raw if isinstance(raw, list) else raw.get("available_skills_manifest", [])
    allowed = {s.get("skill_name") for s in manifest if isinstance(s, dict)}
    
    # 1. Goal alignment: 检查节点 purpose/target_skill 是否覆盖业务目标关键词
    goal_keywords = [k for k in ["创建", "审核", "生成", "通知", "审批", "导入", "导出", "开通",
                                  "安排", "采购", "配置", "培训", "处理", "汇总",
                                  "create", "review", "generate", "notify", "approve", "import", "export",
                                  "provision", "setup", "book", "bookings", "process", "aggregate"]
                     if k.lower() in business_goal.lower()]
    
    if goal_keywords:
        # 提取所有节点的 purpose + target_skill 文本
        node_text = " ".join(
            f"{n.get('purpose', '')} {n.get('target_skill', '')}" for n in nodes
        ).lower()
        matched = sum(1 for kw in goal_keywords if kw.lower() in node_text)
        goal_score = round((matched / len(goal_keywords)) * 100)
    else:
        # 无关键词时，用节点数做基础估算
        goal_score = min(100, max(30, len(nodes) * 15))
    
    # 2. Topology soundness
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for e in edges:
        graph[e["from_node"]].append(e["to_node"])
        in_degree[e["to_node"]] += 1
    has_unreachable = any(in_degree[n] == 0 and n not in plan_ir.get("entry_nodes", []) for n in node_ids)
    topo_score = 100 if not has_unreachable else 60
    
    # 3. Skill binding
    bound_skills = sum(1 for n in nodes if n.get("target_skill") in allowed)
    skill_score = (bound_skills / max(len(nodes), 1)) * 100
    
    # 4. Scope safety
    empty_scope = sum(1 for n in nodes if not n.get("scoped_state_keys"))
    scope_score = max(0, 100 - empty_scope * 25)
    
    # 5. Executability (all nodes have required fields)
    complete = sum(1 for n in nodes if all(k in n for k in ["node_id", "target_skill", "purpose", "scoped_state_keys"]))
    exec_score = (complete / max(len(nodes), 1)) * 100
    
    # 6. Efficiency & complexity
    entry = set(plan_ir.get("entry_nodes", []))
    can_parallel = sum(1 for n in nodes if in_degree.get(n["node_id"], 0) == 0 and n["node_id"] in entry)
    parallelism_bonus = min(15, can_parallel * 5)
    complexity_penalty = max(0, (len(nodes) - 10) * 3) if len(nodes) > 10 else 0
    eff_score = min(100, max(30, 70 + parallelism_bonus - complexity_penalty))
    
    # 7. Risk & governance
    has_human_review = sum(1 for n in nodes if n.get("human_review_required"))
    has_timeout = sum(1 for n in nodes if n.get("timeout_seconds"))
    has_failure_route = sum(1 for e in edges if e.get("on_failure_route"))
    risk_score = min(100, (has_human_review + has_timeout + has_failure_route) * 15 + 25)
    
    scores = {
        "goal_alignment": round(goal_score),
        "topology_soundness": round(topo_score),
        "skill_binding": round(skill_score),
        "scope_safety": round(scope_score),
        "executability": round(exec_score),
        "efficiency_complexity": round(eff_score),
        "risk_governance": round(risk_score),
    }
    
    weighted = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    
    if weighted >= 90:
        decision = "pass"
    elif weighted >= 70:
        decision = "conditional_pass"
    elif weighted >= 50:
        decision = "conditional_pass"
    else:
        decision = "reject"
    
    return {
        "scorecard": scores,
        "weighted_score": round(weighted, 1),
        "decision": decision,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--goal", default="")
    parser.add_argument("--output", default="score.json")
    args = parser.parse_args()
    
    result = score_plan(args.plan, args.manifest, args.goal)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Score: {result['weighted_score']}/100 ({result['decision']})")
    for k, v in result["scorecard"].items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
