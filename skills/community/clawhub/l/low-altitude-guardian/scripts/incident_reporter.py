"""
事件记录与上报模块 (Incident Reporter)

负责：
- 生成完整事件报告
- 分级上报
- 生成模型学习反馈数据包
- 管理事件历史
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
INCIDENTS_DIR = PROJECT_ROOT / ".guardian" / "incidents"
FEEDBACK_DIR = PROJECT_ROOT / ".guardian" / "feedback"
REPORTS_DIR = PROJECT_ROOT / ".guardian" / "reports"


@dataclass
class TimelineEvent:
    """时间线事件。"""
    timestamp: str
    event_type: str  # trigger/detection/classification/decision/action/result
    description: str
    data: dict = field(default_factory=dict)


@dataclass
class LossAssessment:
    """损失评估。"""
    human_casualties: int = 0
    human_injuries: int = 0
    public_property_damage_cny: float = 0
    third_party_damage_cny: float = 0
    device_damage_level: str = "none"  # none/minor/moderate/severe/destroyed
    device_repair_cost_cny: float = 0
    mission_completed: bool = False
    payload_status: str = "intact"  # intact/damaged/lost
    environmental_impact: str = "none"


@dataclass
class IncidentReport:
    """完整事件报告。"""
    incident_id: str
    created_at: str
    closed_at: str = ""
    status: str = "open"  # open/resolved/escalated

    # 事件摘要
    device_id: str = ""
    device_type: str = ""
    location: str = ""
    crisis_type: str = ""
    crisis_level: str = ""
    crisis_trigger: str = ""

    # 详细记录
    timeline: list = field(default_factory=list)
    decision_id: str = ""
    decision_name: str = ""
    decision_source: str = ""
    alternative_decisions: list = field(default_factory=list)

    # 结果
    outcome_success: bool = False
    loss_assessment: dict = field(default_factory=dict)
    lessons_learned: list = field(default_factory=list)

    # 上报
    escalation_level: str = ""
    escalation_targets: list = field(default_factory=list)
    escalation_sent: bool = False


def create_incident(snapshot: dict, classification: dict,
                    decision: dict) -> IncidentReport:
    """创建事件记录。"""
    now = datetime.now(timezone.utc)
    incident_id = f"INC-{now.strftime('%Y%m%d-%H%M%S')}"

    report = IncidentReport(
        incident_id=incident_id,
        created_at=now.isoformat(),
        device_id=snapshot.get("device_id", ""),
        device_type=snapshot.get("device_type", ""),
        location=f"{snapshot.get('location', 'unknown')}",
        crisis_type=classification.get("crisis_type", ""),
        crisis_level=classification.get("level", ""),
        crisis_trigger=snapshot.get("crisis_trigger", ""),
        decision_id=decision.get("plan_id", ""),
        decision_name=decision.get("name", ""),
        decision_source=decision.get("source", ""),
    )

    # 初始时间线
    report.timeline = [
        asdict(TimelineEvent(
            timestamp=snapshot.get("timestamp", now.isoformat()),
            event_type="trigger",
            description=f"危机触发: {snapshot.get('crisis_trigger', '')}",
            data={"snapshot_summary": {
                "battery": snapshot.get("battery_level"),
                "altitude": snapshot.get("altitude_agl"),
            }},
        )),
        asdict(TimelineEvent(
            timestamp=now.isoformat(),
            event_type="classification",
            description=f"危机分级: {classification.get('level', '')} - {classification.get('crisis_type', '')}",
        )),
        asdict(TimelineEvent(
            timestamp=now.isoformat(),
            event_type="decision",
            description=f"决策选定: {decision.get('name', '')}",
            data={"confidence": decision.get("confidence", 0)},
        )),
    ]

    return report


def close_incident(report: IncidentReport, success: bool,
                   loss: LossAssessment = None,
                   lessons: list = None) -> IncidentReport:
    """关闭事件并记录结果。"""
    now = datetime.now(timezone.utc)
    report.closed_at = now.isoformat()
    report.status = "resolved"
    report.outcome_success = success
    report.loss_assessment = asdict(loss) if loss else {}
    report.lessons_learned = lessons or []

    # 添加结束时间线事件
    report.timeline.append(asdict(TimelineEvent(
        timestamp=now.isoformat(),
        event_type="result",
        description=f"事件解决: {'成功' if success else '失败'}",
        data={"loss_summary": report.loss_assessment},
    )))

    return report


def save_incident(report: IncidentReport, output_path: str = None) -> str:
    """保存事件报告。"""
    if output_path is None:
        INCIDENTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = str(INCIDENTS_DIR / f"{report.incident_id}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2)

    return output_path


# ─── 分级上报 ─────────────────────────────────────────────

# 上报规则
_ESCALATION_RULES = {
    "L5-CRITICAL": {
        "targets": ["regulatory_authority", "operations_executive", "ai_model_layer"],
        "method": "immediate_push + formal_report",
        "deadline_hours": 0,
        "description": "即时推送 + 正式报告",
    },
    "L4-SEVERE": {
        "targets": ["operations_management", "ai_model_layer"],
        "method": "immediate_push + detailed_report",
        "deadline_hours": 1,
        "description": "即时推送 + 详细报告",
    },
    "L3-MAJOR": {
        "targets": ["operations_team", "ai_model_layer"],
        "method": "auto_report",
        "deadline_hours": 4,
        "description": "自动报告",
    },
    "L2-MINOR": {
        "targets": ["operations_log", "ai_model_layer"],
        "method": "auto_record",
        "deadline_hours": 24,
        "description": "自动记录",
    },
    "L1-CAUTION": {
        "targets": ["device_log", "ai_model_layer"],
        "method": "batch_summary",
        "deadline_hours": 168,  # 7天
        "description": "批量汇总",
    },
}


def determine_escalation(crisis_level: str) -> dict:
    """确定上报级别和目标。"""
    return _ESCALATION_RULES.get(crisis_level, _ESCALATION_RULES["L2-MINOR"])


def execute_escalation(report: IncidentReport) -> dict:
    """
    执行上报（模拟）。

    真实系统中会：
    - 通过 API 推送到运营平台
    - 发送短信/邮件给管理人员
    - 向监管系统提交报告
    - 向 AI 模型层发送学习数据
    """
    escalation = determine_escalation(report.crisis_level)

    print(f"[上报] 事件 {report.incident_id}")
    print(f"  危机等级: {report.crisis_level}")
    print(f"  上报方式: {escalation['description']}")
    print(f"  上报对象: {', '.join(escalation['targets'])}")
    print(f"  截止时间: {escalation['deadline_hours']}小时内")

    report.escalation_level = report.crisis_level
    report.escalation_targets = escalation["targets"]
    report.escalation_sent = True

    return {
        "escalation_executed": True,
        "targets": escalation["targets"],
        "method": escalation["method"],
        "deadline_hours": escalation["deadline_hours"],
    }


# ─── 模型学习反馈 ─────────────────────────────────────────────

def generate_model_feedback(report: IncidentReport) -> dict:
    """
    生成标准化的模型学习反馈数据包。

    这些数据将被发送到 AI 模型层，用于：
    - 更新危机响应知识库
    - 调整方案参数
    - 识别新的危机模式
    - 改进决策算法
    """
    feedback = {
        "feedback_type": "crisis_response_outcome",
        "incident_id": report.incident_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "crisis_signature": {
            "type": report.crisis_type,
            "level": report.crisis_level,
            "trigger": report.crisis_trigger,
            "device_type": report.device_type,
        },
        "decision_made": report.decision_name,
        "decision_source": report.decision_source,
        "outcome": {
            "success": report.outcome_success,
            "loss_assessment": report.loss_assessment,
            "timeline_duration_s": _calculate_duration(report),
        },
        "lessons": report.lessons_learned,
        "suggested_kb_update": _suggest_kb_update(report),
    }

    # 保存反馈数据
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    feedback_path = FEEDBACK_DIR / f"feedback_{report.incident_id}.json"
    with open(feedback_path, "w", encoding="utf-8") as f:
        json.dump(feedback, f, ensure_ascii=False, indent=2)

    print(f"[反馈] 已生成模型学习数据: {feedback_path}")
    return feedback


def _calculate_duration(report: IncidentReport) -> float:
    """计算事件持续时间（秒）。"""
    if not report.created_at or not report.closed_at:
        return 0

    try:
        start = datetime.fromisoformat(report.created_at)
        end = datetime.fromisoformat(report.closed_at)
        return (end - start).total_seconds()
    except (ValueError, TypeError):
        return 0


def _suggest_kb_update(report: IncidentReport) -> Optional[dict]:
    """基于事件结果建议知识库更新。"""
    if not report.lessons_learned:
        return None

    # 简单的规则：如果事件失败，建议收紧参数
    if not report.outcome_success:
        return {
            "action": "tighten_preconditions",
            "crisis_type": report.crisis_type,
            "reason": f"事件 {report.incident_id} 处理失败，建议收紧适用条件",
            "lessons": report.lessons_learned,
        }

    return {
        "action": "reinforce_success",
        "crisis_type": report.crisis_type,
        "reason": f"事件 {report.incident_id} 处理成功，强化方案权重",
    }


# ─── 报告生成 ─────────────────────────────────────────────

def generate_human_readable_report(report: IncidentReport) -> str:
    """生成人类可读的事件报告。"""
    lines = [
        "=" * 60,
        f"事件报告: {report.incident_id}",
        "=" * 60,
        "",
        "【事件摘要】",
        f"  设备: {report.device_id} ({report.device_type})",
        f"  位置: {report.location}",
        f"  时间: {report.created_at}",
        f"  状态: {report.status}",
        f"  危机等级: {report.crisis_level}",
        f"  危机类型: {report.crisis_type}",
        f"  触发原因: {report.crisis_trigger}",
        "",
        "【决策信息】",
        f"  选定方案: {report.decision_name}",
        f"  方案来源: {report.decision_source}",
        f"  方案ID: {report.decision_id}",
        "",
        "【事件时间线】",
    ]

    for event in report.timeline:
        lines.append(f"  [{event.get('timestamp', '?')}] "
                     f"{event.get('event_type', '').upper()}: "
                     f"{event.get('description', '')}")

    lines.extend([
        "",
        "【处理结果】",
        f"  成功: {'是' if report.outcome_success else '否'}",
    ])

    if report.loss_assessment:
        lines.append("  损失评估:")
        for key, val in report.loss_assessment.items():
            lines.append(f"    {key}: {val}")

    if report.lessons_learned:
        lines.extend(["", "【经验教训】"])
        for i, lesson in enumerate(report.lessons_learned, 1):
            lines.append(f"  {i}. {lesson}")

    if report.escalation_sent:
        lines.extend([
            "",
            "【上报信息】",
            f"  上报等级: {report.escalation_level}",
            f"  上报对象: {', '.join(report.escalation_targets)}",
        ])

    lines.extend(["", "=" * 60])
    return "\n".join(lines)


# ─── CLI 入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 事件记录与上报")
    parser.add_argument("--generate-report", action="store_true",
                        help="生成事件报告")
    parser.add_argument("--incident-id", type=str, help="事件ID")
    parser.add_argument("--list-incidents", action="store_true",
                        help="列出所有事件")
    parser.add_argument("--demo", action="store_true", help="运行演示")

    args = parser.parse_args()

    if args.demo:
        _run_demo()
    elif args.list_incidents:
        _list_incidents()
    elif args.generate_report and args.incident_id:
        _load_and_display(args.incident_id)
    else:
        parser.print_help()


def _run_demo():
    """运行事件报告演示。"""
    print("=" * 60)
    print("低空卫士 - 事件报告演示")
    print("=" * 60)

    # 模拟创建事件
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": "UAV-SH-00142",
        "device_type": "多旋翼无人机",
        "location": "31.2304°N, 121.4737°E, ALT:120m",
        "battery_level": 34,
        "altitude_agl": 120,
        "crisis_trigger": "左前电机异常振动，转速下降30%",
    }

    classification = {
        "level": "L3-MAJOR",
        "crisis_type": "power_failure.single_motor_loss",
        "confidence": 0.85,
    }

    decision = {
        "plan_id": "DEC-20260310-142301-SOL-PWR-001",
        "name": "三电机降级返航",
        "source": "knowledge_base",
        "confidence": 0.92,
    }

    # 创建事件
    report = create_incident(snapshot, classification, decision)
    print(f"\n[创建] 事件 {report.incident_id}")

    # 模拟关闭事件
    loss = LossAssessment(
        device_damage_level="minor",
        device_repair_cost_cny=500,
        mission_completed=False,
        payload_status="intact",
    )

    lessons = [
        "三电机模式下风速>10m/s时降速更大，需更早触发返航",
        "备降点A距离过远，应优先选择备降点B",
        "电机异常振动检测阈值可以适当降低以提前预警",
    ]

    report = close_incident(report, success=True, loss=loss, lessons=lessons)

    # 保存
    path = save_incident(report)
    print(f"[保存] 事件报告: {path}")

    # 上报
    execute_escalation(report)

    # 生成模型反馈
    feedback = generate_model_feedback(report)

    # 显示人类可读报告
    print(f"\n{generate_human_readable_report(report)}")


def _list_incidents():
    """列出所有事件记录。"""
    if not INCIDENTS_DIR.exists():
        print("暂无事件记录")
        return

    files = sorted(INCIDENTS_DIR.glob("INC-*.json"), reverse=True)
    if not files:
        print("暂无事件记录")
        return

    print(f"共 {len(files)} 条事件记录:\n")
    for f in files:
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
            print(f"  [{data.get('crisis_level', '?')}] {data.get('incident_id', f.stem)}")
            print(f"    设备: {data.get('device_id', '?')}")
            print(f"    触发: {data.get('crisis_trigger', '?')}")
            print(f"    状态: {data.get('status', '?')}")
            print(f"    结果: {'成功' if data.get('outcome_success') else '失败/进行中'}")
            print()
        except (json.JSONDecodeError, KeyError):
            print(f"  [错误] 无法读取: {f.name}")


def _load_and_display(incident_id: str):
    """加载并显示事件报告。"""
    incident_file = INCIDENTS_DIR / f"{incident_id}.json"
    if not incident_file.exists():
        print(f"错误: 事件 {incident_id} 不存在")
        sys.exit(1)

    with open(incident_file, encoding="utf-8") as f:
        data = json.load(f)

    report = IncidentReport(**{
        k: v for k, v in data.items()
        if k in IncidentReport.__dataclass_fields__
    })
    print(generate_human_readable_report(report))


if __name__ == "__main__":
    main()
