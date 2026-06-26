#!/usr/bin/env python3
"""Review plan — input normalization + static validation runner."""
import argparse, json, hashlib, sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from validate_schema import validate_schema
from validate_topology import validate_topology
from validate_scope import validate_scope

def review_plan(business_goal: str, plan_path: str, manifest_path: str,
                mode: str = "review_only") -> dict:
    """Run static validation and collect results."""
    review_id = f"review_{hashlib.md5(business_goal.encode()).hexdigest()[:8]}_{datetime.now().strftime('%Y%m%d')}"
    
    # Run validations
    schema_result = validate_schema(plan_path)
    topology_result = validate_topology(plan_path)
    scope_result = validate_scope(plan_path)
    
    # Bind skills check
    with open(manifest_path) as f:
        raw = json.load(f)
    manifest = raw if isinstance(raw, list) else raw.get("available_skills_manifest", raw.get("skills_manifest", []))
    allowed_skills = {s.get("skill_name") for s in manifest if isinstance(s, dict)}
    
    with open(plan_path) as f:
        plan = json.load(f)
    plan_ir = plan.get("plan_ir", plan)
    nodes = plan_ir.get("nodes", [])
    binding_errors = [f"Node {n['node_id']}: skill '{n.get('target_skill', '')}' not in manifest"
                      for n in nodes if n.get("target_skill") not in allowed_skills]
    skills_bound = len(binding_errors) == 0
    
    all_errors = schema_result["errors"] + topology_result["errors"] + scope_result["errors"] + binding_errors
    all_warnings = topology_result.get("warnings", []) + scope_result.get("warnings", [])

    # 分类问题
    critical_issues = [{"severity": "critical", "description": e, "dimension": "topology_or_schema"} for e in all_errors]
    major_issues = [{"severity": "major", "description": w, "dimension": "efficiency_or_scope"} for w in all_warnings]

    # 决策逻辑：全部通过 + 无关键问题 → pass
    all_valid = (schema_result["schema_valid"] and topology_result["dag_valid"]
                 and skills_bound and scope_result["scope_valid"])
    if not all_valid:
        decision = "reject"
        confidence = 0.95
    elif not critical_issues and not major_issues:
        decision = "pass"
        confidence = 0.9
    elif not critical_issues:
        decision = "conditional_pass"
        confidence = 0.75
    else:
        decision = "conditional_pass"
        confidence = 0.7
    
    result = {
        "review_id": review_id,
        "overall_decision": decision,
        "confidence": confidence,
        "review_mode": mode,
        "validation_report": {
            "schema_valid": schema_result["schema_valid"],
            "dag_valid": topology_result["dag_valid"],
            "skills_bound": skills_bound,
            "scope_valid": scope_result["scope_valid"],
        },
        "issues": [
            {"severity": "critical", "description": e, "dimension": "topology_or_schema"}
            for e in critical_issues
        ] + [
            {"severity": "major", "description": w, "dimension": "efficiency_or_scope"}
            for w in major_issues
        ],
        "suggested_actions": [
            "修复 critical 问题后重新评审" if critical_issues else
            "按建议修正 major 问题" if major_issues else
            "进行语义评审（LLM 主导的 7 维度评审）"
        ],
        "reviewed_at": datetime.now().isoformat()
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Review Plan IR")
    parser.add_argument("--goal", required=True, help="Business goal")
    parser.add_argument("--plan", required=True, help="Plan JSON file")
    parser.add_argument("--manifest", required=True, help="Skills manifest")
    parser.add_argument("--mode", default="review_only", choices=["review_only", "review_and_revise"])
    parser.add_argument("--output", default="review_result.json")
    args = parser.parse_args()
    
    result = review_plan(args.goal, args.plan, args.manifest, args.mode)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Review completed: {result['review_id']}")
    print(f"Decision: {result['overall_decision']} (confidence: {result['confidence']:.0%})")
    print(f"Critical issues: {len([i for i in result['issues'] if i['severity'] == 'critical'])}")
    print(f"Major issues: {len([i for i in result['issues'] if i['severity'] == 'major'])}")
    print(f"Output: {args.output}")

if __name__ == "__main__":
    main()
