"""
决策管理器 (Decision Manager)

负责：
- 方案检索与匹配
- 多方案比较评分
- 最优方案选择
- 决策审计日志
"""

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))

from crisis_engine import (
    CrisisLevel, CrisisClassification, SafetyScore,
    DecisionPlan, classify_crisis, match_solutions, load_solution_templates,
)

DECISIONS_DIR = PROJECT_ROOT / ".guardian" / "decisions"


def find_best_plan(snapshot: dict) -> Optional[DecisionPlan]:
    """
    端到端决策流程：分级 → 匹配 → 选择最优方案。

    Args:
        snapshot: 态势快照（扁平化格式）

    Returns:
        最优决策方案，若全部被否决则返回 None
    """
    # 步骤1: 危机分级
    classification = classify_crisis(snapshot)

    # 步骤2: 方案匹配与评分
    plans = match_solutions(classification, snapshot)

    # 步骤3: 选择最优（未被否决的第一个方案）
    valid_plans = [p for p in plans if not p.is_vetoed]

    if not valid_plans:
        return None

    best = valid_plans[0]

    # 步骤4: 记录决策审计日志
    _save_decision_audit(classification, plans, best, snapshot)

    return best


def compare_plans(plans: list) -> dict:
    """
    多方案详细对比。

    Returns:
        对比报告字典
    """
    report = {
        "total_plans": len(plans),
        "valid_plans": sum(1 for p in plans if not p.is_vetoed),
        "vetoed_plans": sum(1 for p in plans if p.is_vetoed),
        "comparison": [],
    }

    for plan in plans:
        entry = {
            "name": plan.name,
            "source": plan.source,
            "confidence": plan.confidence,
            "total_score": plan.safety_score.total_score,
            "scores": {
                "human_safety (W=0.40)": plan.safety_score.human_safety,
                "public_safety (W=0.25)": plan.safety_score.public_safety,
                "third_party (W=0.15)": plan.safety_score.third_party_property,
                "device_safety (W=0.12)": plan.safety_score.device_safety,
                "mission (W=0.08)": plan.safety_score.mission_completion,
            },
            "is_vetoed": plan.is_vetoed,
            "veto_reason": plan.veto_reason if plan.is_vetoed else "",
            "steps_count": len(plan.steps),
        }
        report["comparison"].append(entry)

    # 排名
    valid_entries = [e for e in report["comparison"] if not e["is_vetoed"]]
    valid_entries.sort(key=lambda x: x["total_score"], reverse=True)
    for i, entry in enumerate(valid_entries):
        entry["rank"] = i + 1

    return report


def _save_decision_audit(classification: CrisisClassification,
                         all_plans: list,
                         selected_plan: DecisionPlan,
                         snapshot: dict):
    """保存决策审计日志（用于事后追溯和合规）。"""
    DECISIONS_DIR.mkdir(parents=True, exist_ok=True)

    audit = {
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "classification": {
            "level": classification.level.value,
            "type": f"{classification.crisis_type}.{classification.sub_type}",
            "confidence": classification.confidence,
            "is_escalating": classification.is_escalating,
            "decision_window_s": classification.available_decision_window_s,
        },
        "plans_evaluated": len(all_plans),
        "plans_valid": sum(1 for p in all_plans if not p.is_vetoed),
        "plans_vetoed": sum(1 for p in all_plans if p.is_vetoed),
        "selected_plan": {
            "plan_id": selected_plan.plan_id,
            "name": selected_plan.name,
            "source": selected_plan.source,
            "confidence": selected_plan.confidence,
            "total_score": selected_plan.safety_score.total_score,
            "safety_scores": {
                "S0_human": selected_plan.safety_score.human_safety,
                "S1_public": selected_plan.safety_score.public_safety,
                "S2_property": selected_plan.safety_score.third_party_property,
                "S3_device": selected_plan.safety_score.device_safety,
                "S4_mission": selected_plan.safety_score.mission_completion,
            },
        },
        "snapshot_summary": {
            "device_id": snapshot.get("device_id"),
            "crisis_trigger": snapshot.get("crisis_trigger"),
            "battery": snapshot.get("battery_level"),
            "altitude": snapshot.get("altitude_agl"),
        },
    }

    audit_file = DECISIONS_DIR / f"audit_{selected_plan.plan_id}.json"
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)


def human_in_the_loop(plan: DecisionPlan, crisis_level: CrisisLevel) -> dict:
    """
    根据危机等级决定人在回路模式。

    Returns:
        包含执行模式和确认要求的字典
    """
    modes = {
        CrisisLevel.L5_CRITICAL: {
            "mode": "autonomous_execute",
            "description": "自主执行，事后通知",
            "wait_for_confirm": False,
            "timeout_s": 0,
            "reason": "L5危机无时间等待人工确认",
        },
        CrisisLevel.L4_SEVERE: {
            "mode": "autonomous_with_notification",
            "description": "自主执行，同步通知操作员",
            "wait_for_confirm": False,
            "timeout_s": 0,
            "reason": "L4危机需立即行动",
        },
        CrisisLevel.L3_MAJOR: {
            "mode": "recommend_with_timeout",
            "description": "推荐方案，等待5秒确认，超时自动执行",
            "wait_for_confirm": True,
            "timeout_s": 5,
            "reason": "L3危机有短暂决策窗口",
        },
        CrisisLevel.L2_MINOR: {
            "mode": "recommend_await_confirm",
            "description": "推荐方案，等待操作员确认后执行",
            "wait_for_confirm": True,
            "timeout_s": 120,
            "reason": "L2危机允许人工决策",
        },
        CrisisLevel.L1_CAUTION: {
            "mode": "advisory_only",
            "description": "仅提醒，由操作员决策",
            "wait_for_confirm": True,
            "timeout_s": 300,
            "reason": "L1级别操作员自行判断",
        },
    }

    return modes.get(crisis_level, modes[CrisisLevel.L2_MINOR])


# ─── CLI 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 决策管理器")
    parser.add_argument("--match", action="store_true", help="执行方案匹配")
    parser.add_argument("--compare", action="store_true", help="多方案对比")
    parser.add_argument("--crisis-type", type=str, help="危机类型")
    parser.add_argument("--level", type=str, help="危机等级")
    parser.add_argument("--input", type=str, help="输入快照文件")
    parser.add_argument("--list-templates", action="store_true", help="列出所有方案模板")

    args = parser.parse_args()

    if args.list_templates:
        templates = load_solution_templates()
        print(f"已加载 {len(templates)} 个解决方案模板:\n")
        for key, tmpl in templates.items():
            print(f"  [{tmpl.get('template_id', '?')}] {tmpl.get('name', key)}")
            print(f"    类型: {key}")
            print(f"    适用等级: {tmpl.get('applicable_levels', [])}")
            print(f"    历史成功率: {tmpl.get('historical_success_rate', 'N/A')}")
            print()
        return

    if args.match or args.compare:
        if not args.input:
            print("错误: 需要 --input 指定快照文件")
            sys.exit(1)

        with open(args.input, encoding="utf-8") as f:
            snapshot = json.load(f)

        classification = classify_crisis(snapshot)
        plans = match_solutions(classification, snapshot)

        if args.compare:
            report = compare_plans(plans)
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            best = find_best_plan(snapshot)
            if best:
                print(f"最优方案: {best.name}")
                print(f"得分: {best.safety_score.total_score:.2f}")
                print(f"置信度: {best.confidence:.2f}")

                hitl = human_in_the_loop(best, classification.level)
                print(f"\n人在回路模式: {hitl['description']}")
                print(f"等待确认: {'是' if hitl['wait_for_confirm'] else '否'}")
                if hitl['timeout_s'] > 0:
                    print(f"超时时间: {hitl['timeout_s']}秒")
            else:
                print("[警告] 所有方案被否决，需要人工介入！")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
