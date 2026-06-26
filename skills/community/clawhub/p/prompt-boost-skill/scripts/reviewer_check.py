#!/usr/bin/env python3
"""
reviewer_check.py - 按 reviewer checklist 审查 Query Plan 完整度
输入: {"query_plan": {}, "domain": "", "task_type": ""}
输出: {"pass": bool, "reasons": [], "missing": [], "suggestions": []}
"""
import json
import sys
import os

REVIEW_RULES = {
    "data-analysis": ["analysis_goal", "data_source", "time_range", "metrics", "audience"],
    "tech-support":  ["environment", "error_message", "reproduction_steps", "expected_behavior"],
    "supply-chain":  ["business_scope", "target", "audience", "output_format"],
    "product-manager":["business_goal", "user_group", "scenario", "output_format"],
    "marketing":      ["product", "target_users", "campaign_goal", "output_format"],
    "common":        ["target", "context", "audience", "output_format"],
}

def check(query_plan: dict, domain: str) -> dict:
    required = REVIEW_RULES.get(domain, REVIEW_RULES["common"])
    filled = query_plan.get("filled_slots", {})
    missing = [k for k in required if not filled.get(k)]
    
    pass_gate = len(missing) <= 1  # 最多缺1项
    
    return {
        "pass": pass_gate,
        "filled_count": len(required) - len(missing),
        "total_required": len(required),
        "missing": missing,
        "suggestions": [f"建议补充：{m}" for m in missing[:3]],
        "reasons": ["信息完整度达标"] if pass_gate else [f"缺少 {len(missing)} 项关键信息"],
    }

if __name__ == "__main__":
    try:
        inp = json.loads(sys.stdin.read())
        result = check(inp.get("query_plan", {}), inp.get("domain", "common"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
