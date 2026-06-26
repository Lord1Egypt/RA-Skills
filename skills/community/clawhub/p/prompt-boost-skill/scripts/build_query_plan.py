#!/usr/bin/env python3
"""
build_query_plan.py - 将用户确认信息融合领域元数据，生成标准 Query Plan
输入: {"domain": "", "task_type": "", "confirmed_slots": {}, "missing_slots": [], "raw_query": ""}
输出: Query Plan JSON
"""
import json
import sys
import os

def load_domain_metadata(domain: str) -> dict:
    meta_path = os.path.join(os.path.dirname(__file__), "..", "assets", "domain-metadata", f"{domain}.yaml")
    # 简单解析 key: value 或 list 行
    result = {}
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            for line in f:
                line = line.strip()
                if ":" in line and not line.startswith("#"):
                    parts = line.split(":", 1)
                    key = parts[0].strip()
                    val = parts[1].strip().strip('"').strip("'")
                    if val.startswith("["):
                        result[key] = []
                    elif val == "[]":
                        result[key] = []
                    else:
                        result[key] = val
    return result

def build(confirmed: dict, domain: str, task_type: str) -> dict:
    return {
        "domain": domain,
        "task_type": task_type,
        "target": confirmed.get("target", ""),
        "audience": confirmed.get("audience", ""),
        "context": confirmed.get("context", ""),
        "constraints": confirmed.get("constraints", []),
        "output_format": confirmed.get("output_format", ""),
        "professional_level": confirmed.get("professional_level", "standard"),
        "tool_preference": confirmed.get("tool_preference", []),
        "filled_slots": confirmed,
        "missing_slots": confirmed.get("missing_slots", []),
    }

if __name__ == "__main__":
    try:
        inp = json.loads(sys.stdin.read())
        result = build(inp.get("confirmed_slots", {}), inp.get("domain", "common"), inp.get("task_type", ""))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
