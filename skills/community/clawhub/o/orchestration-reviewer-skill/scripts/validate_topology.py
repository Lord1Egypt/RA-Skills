#!/usr/bin/env python3
"""Validate DAG topology."""
import argparse, json, sys
from collections import defaultdict

def _extract_plan_ir(raw: dict) -> dict:
    """从 reviewer 输入或纯 plan 输入中提取 Plan IR。"""
    if "existing_plan_ir" in raw:
        return raw["existing_plan_ir"]
    if "plan_ir" in raw:
        return raw["plan_ir"]
    return raw

def validate_topology(plan_path: str) -> dict:
    with open(plan_path) as f:
        plan = json.load(f)
    plan_ir = _extract_plan_ir(plan)
    nodes = plan_ir.get("nodes", [])
    edges = plan_ir.get("edges", [])

    # 保护：空 plan 不应直接 pass
    if not nodes:
        return {"dag_valid": False, "errors": ["Plan IR has no nodes — nothing to validate"],
                "warnings": [], "node_count": 0, "edge_count": 0, "depth": 0}
    if not edges and len(nodes) > 1:
        return {"dag_valid": False, "errors": ["Multiple nodes but no edges — check dependency declarations"],
                "warnings": [], "node_count": len(nodes), "edge_count": 0, "depth": 0}

    node_ids = {n["node_id"] for n in nodes}
    errors = []
    warnings = []

    # Reference integrity
    for edge in edges:
        if edge["from_node"] not in node_ids:
            errors.append(f"Edge references non-existent node: {edge['from_node']}")
        if edge["to_node"] not in node_ids:
            errors.append(f"Edge references non-existent node: {edge['to_node']}")

    # Cycle detection
    graph = defaultdict(list)
    for edge in edges:
        graph[edge["from_node"]].append(edge["to_node"])
    visited, rec_stack = set(), set()
    def has_cycle(node):
        visited.add(node); rec_stack.add(node)
        for nb in graph.get(node, []):
            if nb not in visited:
                if has_cycle(nb): return True
            elif nb in rec_stack: return True
        rec_stack.discard(node); return False
    for nid in node_ids:
        if nid not in visited and has_cycle(nid):
            errors.append("Cycle detected in DAG"); break

    # Unreachable nodes
    in_degree = defaultdict(int)
    for edge in edges:
        in_degree[edge["to_node"]] += 1
    entry_set = set(plan_ir.get("entry_nodes", []))
    for nid in node_ids:
        if in_degree[nid] == 0 and nid not in entry_set:
            warnings.append(f"Node {nid} has no incoming edge and is not in entry_nodes")

    # Depth calculation
    def calc_depth():
        q = [n for n in node_ids if in_degree[n] == 0]
        depth = 0
        while q:
            depth += 1
            nq = []
            for node in q:
                for nb in graph.get(node, []):
                    in_degree[nb] -= 1
                    if in_degree[nb] == 0: nq.append(nb)
            q = nq
        return depth

    return {"dag_valid": len(errors) == 0, "errors": errors, "warnings": warnings,
            "node_count": len(nodes), "edge_count": len(edges), "depth": calc_depth()}

def main():
    parser = argparse.ArgumentParser(description="Validate DAG topology")
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    result = validate_topology(args.plan)
    if result["dag_valid"]:
        print(f"✅ DAG validation passed (Nodes: {result['node_count']}, Edges: {result['edge_count']}, Depth: {result['depth']})")
    else:
        print(f"❌ DAG validation failed")
        for e in result["errors"]: print(f"  - {e}")
    for w in result["warnings"]: print(f"  ⚠️ {w}")
    sys.exit(0 if result["dag_valid"] else 1)

if __name__ == "__main__":
    main()
