#!/usr/bin/env python3
"""Validate Plan IR against schema."""
import argparse, json, sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / "assets" / "input_schema.json"

def _extract_plan_ir(raw: dict) -> dict:
    """从 reviewer 输入或纯 plan 输入中提取 Plan IR。"""
    # Reviewer 场景: existing_plan_ir
    if "existing_plan_ir" in raw:
        return raw["existing_plan_ir"]
    # Planner 场景: plan_ir
    if "plan_ir" in raw:
        return raw["plan_ir"]
    # 已经是纯 Plan IR
    return raw

def validate_schema(plan_path: str, schema_path: str = None) -> dict:
    schema_file = schema_path or SCHEMA_PATH
    with open(plan_path) as f:
        raw = json.load(f)
    plan = _extract_plan_ir(raw)
    
    try:
        import jsonschema
        with open(schema_file) as f:
            schema = json.load(f)
        errors = []
        try:
            jsonschema.validate(plan, schema)
        except jsonschema.ValidationError as e:
            errors.append(str(e.message))
        return {"schema_valid": len(errors) == 0, "errors": errors}
    except ImportError:
        return _basic_validate(plan)

def _basic_validate(plan: dict) -> dict:
    errors = []
    for key in ["nodes", "edges", "entry_nodes", "exit_nodes"]:
        if key not in plan:
            errors.append(f"Missing field: {key}")
    for node in plan.get("nodes", []):
        for key in ["node_id", "target_skill", "purpose", "scoped_state_keys"]:
            if key not in node:
                errors.append(f"Node {node.get('node_id', '?')}: missing {key}")
    for edge in plan.get("edges", []):
        for key in ["from_node", "to_node"]:
            if key not in edge:
                errors.append(f"Edge: missing {key}")
    return {"schema_valid": len(errors) == 0, "errors": errors}

def main():
    parser = argparse.ArgumentParser(description="Validate Plan IR schema")
    parser.add_argument("--plan", required=True)
    parser.add_argument("--schema")
    args = parser.parse_args()
    
    result = validate_schema(args.plan, args.schema)
    
    if result["schema_valid"]:
        print("✅ Schema validation passed")
    else:
        print(f"❌ Schema validation failed ({len(result['errors'])} errors)")
        for e in result["errors"]:
            print(f"  - {e}")
    sys.exit(0 if result["schema_valid"] else 1)

if __name__ == "__main__":
    main()
