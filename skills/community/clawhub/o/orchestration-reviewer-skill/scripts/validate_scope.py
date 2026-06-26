#!/usr/bin/env python3
"""Validate scoped_state_keys."""
import argparse, json, sys

def _extract_plan_ir(raw: dict) -> dict:
    """从 reviewer 输入或纯 plan 输入中提取 Plan IR。"""
    if "existing_plan_ir" in raw:
        return raw["existing_plan_ir"]
    if "plan_ir" in raw:
        return raw["plan_ir"]
    return raw

def validate_scope(plan_path: str) -> dict:
    with open(plan_path) as f:
        plan = json.load(f)
    plan_ir = _extract_plan_ir(plan)
    nodes = plan_ir.get("nodes", [])
    edges = plan_ir.get("edges", [])

    # 保护：空 plan
    if not nodes:
        return {"scope_valid": False, "errors": ["Plan IR has no nodes"], "warnings": []}

    # 识别入口节点
    entry_node_ids = set(plan_ir.get("entry_nodes", []))
    if not entry_node_ids:
        edge_targets = {e["to_node"] for e in edges}
        entry_node_ids = {n["node_id"] for n in nodes if n["node_id"] not in edge_targets}

    errors, warnings = [], []
    all_keys = set()
    for node in nodes:
        nid = node["node_id"]
        scoped = node.get("scoped_state_keys", [])
        # 入口节点允许空 scoped_state_keys（无上游依赖）
        if not scoped and nid not in entry_node_ids:
            errors.append(f"Node {nid}: scoped_state_keys is empty (non-entry node must declare state keys)")
            continue
        elif not scoped:
            warnings.append(f"Node {nid}: scoped_state_keys is empty (entry node, consider declaring expected outputs)")
            continue
        for key in scoped:
            all_keys.add(f"{nid}.{key}")
    for node in nodes:
        nid = node["node_id"]
        for key, ref in node.get("input_mapping", {}).items():
            if ref not in all_keys:
                if "." not in ref:
                    warnings.append(f"Node {nid}: references global key '{ref}'")
                else:
                    errors.append(f"Node {nid}: references non-existent key '{ref}'")
    return {"scope_valid": len(errors) == 0, "errors": errors, "warnings": warnings}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    result = validate_scope(args.plan)
    if result["scope_valid"]:
        print("✅ Scope validation passed")
    else:
        print(f"❌ Scope validation failed ({len(result['errors'])} errors)")
        for e in result["errors"]: print(f"  - {e}")
    for w in result["warnings"]: print(f"  ⚠️ {w}")
    sys.exit(0 if result["scope_valid"] else 1)

if __name__ == "__main__":
    main()
