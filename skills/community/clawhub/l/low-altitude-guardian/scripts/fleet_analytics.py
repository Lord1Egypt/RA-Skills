"""
机队数据分析 (Fleet Analytics)

v0.2.0 新增 — 企业机队级数据统计与运营洞察。

负责：
- 多维度事件统计分析
- 设备健康评分
- 运营优化建议
- 监管合规报告生成
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
KB_ROOT = PROJECT_ROOT / ".guardian" / "enterprise_kb"
INCIDENTS_DIR = PROJECT_ROOT / ".guardian" / "incidents"
REPORTS_DIR = PROJECT_ROOT / ".guardian" / "analytics_reports"
FLEET_DIR = KB_ROOT / "fleet"


def collect_all_events() -> list:
    """收集所有事件数据。"""
    events = []
    sources = [
        INCIDENTS_DIR,
        KB_ROOT / "incidents" / "by_type",
    ]

    seen_ids = set()
    for source in sources:
        if not source.exists():
            continue
        for f in source.rglob("*.json"):
            try:
                with open(f, encoding="utf-8") as fp:
                    event = json.load(fp)
                eid = event.get("incident_id", str(f))
                if eid not in seen_ids:
                    seen_ids.add(eid)
                    events.append(event)
            except (json.JSONDecodeError, KeyError):
                continue

    return events


def generate_analytics_report(period: str = None) -> dict:
    """
    生成机队分析报告。

    Args:
        period: 分析周期（如 "2026-Q1", "2026-03", "all"）
    """
    events = collect_all_events()

    report = {
        "report_id": f"ANALYTICS-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": period or "all",
        "summary": {},
        "by_type": {},
        "by_device": {},
        "by_severity": {},
        "response_performance": {},
        "loss_summary": {},
        "kb_effectiveness": {},
        "recommendations": [],
    }

    if not events:
        report["summary"] = {"total_events": 0, "message": "暂无事件数据"}
        report["recommendations"].append("暂无事件数据，建议先导入历史数据或等待设备端上报")
        return report

    # ── 基本统计 ──
    type_counter = Counter()
    device_counter = Counter()
    severity_counter = Counter()
    success_count = 0
    total_count = len(events)
    kb_match_count = 0
    emergency_reasoning_count = 0

    for e in events:
        type_counter[e.get("crisis_type", "unknown")] += 1
        device_counter[e.get("device_type", "unknown")] += 1
        severity_counter[e.get("crisis_level", "unknown")] += 1
        if e.get("outcome_success"):
            success_count += 1
        source = e.get("decision_source", "")
        if source == "knowledge_base":
            kb_match_count += 1
        elif source == "emergency_reasoning":
            emergency_reasoning_count += 1

    report["summary"] = {
        "total_events": total_count,
        "success_rate": success_count / total_count if total_count else 0,
        "success_count": success_count,
        "failure_count": total_count - success_count,
    }

    report["by_type"] = {
        "distribution": dict(type_counter.most_common()),
        "top_3": [{"type": t, "count": c} for t, c in type_counter.most_common(3)],
    }

    report["by_device"] = {
        "distribution": dict(device_counter),
    }

    report["by_severity"] = {
        "distribution": dict(severity_counter),
    }

    # ── 知识库效能 ──
    report["kb_effectiveness"] = {
        "kb_match_count": kb_match_count,
        "emergency_reasoning_count": emergency_reasoning_count,
        "kb_match_rate": kb_match_count / total_count if total_count else 0,
    }

    # ── 损失汇总 ──
    total_device_cost = 0
    total_property_cost = 0
    for e in events:
        loss = e.get("loss_assessment", {})
        total_device_cost += loss.get("device_repair_cost_cny", 0)
        total_property_cost += loss.get("third_party_damage_cny", 0) + loss.get("public_property_damage_cny", 0)

    report["loss_summary"] = {
        "total_device_repair_cost_cny": total_device_cost,
        "total_property_damage_cny": total_property_cost,
        "total_cost_cny": total_device_cost + total_property_cost,
        "human_casualties": sum(e.get("loss_assessment", {}).get("human_casualties", 0) for e in events),
        "human_injuries": sum(e.get("loss_assessment", {}).get("human_injuries", 0) for e in events),
    }

    # ── 运营优化建议 ──
    if type_counter:
        top_type = type_counter.most_common(1)[0]
        report["recommendations"].append(
            f"高频故障: {top_type[0]}（{top_type[1]}次），建议针对此类故障加强飞行前检查和预防性维护")

    if report["kb_effectiveness"]["kb_match_rate"] < 0.5 and total_count > 5:
        report["recommendations"].append(
            f"知识库匹配率仅 {report['kb_effectiveness']['kb_match_rate']:.0%}，建议补充更多解决方案模板")

    if report["summary"]["success_rate"] < 0.8 and total_count > 5:
        report["recommendations"].append(
            f"应急成功率 {report['summary']['success_rate']:.0%} 偏低，建议复盘失败案例并优化方案")

    if total_device_cost > 10000:
        report["recommendations"].append(
            f"累计设备维修费用 ¥{total_device_cost:,.0f}，建议评估设备质量或运营策略")

    return report


def device_health_scores() -> list:
    """计算每台设备的健康评分。"""
    events = collect_all_events()
    device_events = defaultdict(list)

    for e in events:
        did = e.get("device_id", "")
        if did:
            device_events[did].append(e)

    scores = []
    for device_id, dev_events in device_events.items():
        total = len(dev_events)
        failures = sum(1 for e in dev_events if not e.get("outcome_success"))
        severe = sum(1 for e in dev_events
                     if e.get("crisis_level", "") in ("L4-SEVERE", "L5-CRITICAL"))

        # 健康分 = 100 - 故障扣分 - 严重事件额外扣分
        score = max(0, 100 - (total * 5) - (failures * 10) - (severe * 15))

        status = "良好" if score >= 80 else "关注" if score >= 60 else "警告" if score >= 40 else "危险"

        scores.append({
            "device_id": device_id,
            "device_type": dev_events[0].get("device_type", ""),
            "health_score": score,
            "status": status,
            "total_events": total,
            "failures": failures,
            "severe_events": severe,
            "recommendation": _device_recommendation(score, total, failures, severe),
        })

    scores.sort(key=lambda x: x["health_score"])
    return scores


def _device_recommendation(score, total, failures, severe) -> str:
    if score < 40:
        return "建议立即停飞检修，进行全面检测"
    if score < 60:
        return "建议安排预防性维护，限制高风险任务"
    if score < 80:
        return "建议加强飞行前检查，关注历史故障类型"
    return "设备状态良好，继续常规运维"


def generate_compliance_report(standard: str = "CAAC", period: str = None) -> str:
    """生成监管合规报告。"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    events = collect_all_events()

    now = datetime.now(timezone.utc)
    report_lines = [
        f"# 无人机运营安全报告",
        f"",
        f"**报告标准**: {standard}",
        f"**报告周期**: {period or '全部'}",
        f"**生成时间**: {now.strftime('%Y-%m-%d %H:%M')} UTC",
        f"**事件总数**: {len(events)}",
        f"",
        f"---",
        f"",
        f"## 1. 事件统计概要",
        f"",
    ]

    severity_counter = Counter(e.get("crisis_level", "unknown") for e in events)
    report_lines.append("| 等级 | 事件数 |")
    report_lines.append("|------|--------|")
    for level in ["L5-CRITICAL", "L4-SEVERE", "L3-MAJOR", "L2-MINOR", "L1-CAUTION"]:
        count = severity_counter.get(level, 0)
        report_lines.append(f"| {level} | {count} |")

    success_count = sum(1 for e in events if e.get("outcome_success"))
    report_lines.extend([
        f"",
        f"## 2. 应急响应效果",
        f"",
        f"- 处置成功率: {success_count}/{len(events)} ({success_count/len(events)*100:.1f}%)" if events else "- 暂无数据",
        f"- 人员伤亡: {sum(e.get('loss_assessment', {}).get('human_casualties', 0) for e in events)} 人",
        f"- 人员受伤: {sum(e.get('loss_assessment', {}).get('human_injuries', 0) for e in events)} 人",
        f"",
        f"## 3. 改进措施",
        f"",
        f"（由企业根据实际情况填写）",
        f"",
        f"---",
        f"",
        f"*本报告由 Low-Altitude Guardian v0.2.0 自动生成，请结合企业实际核实*",
    ])

    report_content = "\n".join(report_lines)

    filename = f"compliance_{standard}_{now.strftime('%Y%m%d')}.md"
    output_path = REPORTS_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"[合规报告] 已生成: {output_path}")
    return str(output_path)


# ─── CLI ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 机队数据分析")
    parser.add_argument("--report", action="store_true", help="生成分析报告")
    parser.add_argument("--period", type=str, help="分析周期")
    parser.add_argument("--device-health", action="store_true", help="设备健康评分")
    parser.add_argument("--compliance-report", action="store_true", help="生成合规报告")
    parser.add_argument("--standard", type=str, default="CAAC", help="合规标准")
    parser.add_argument("--demo", action="store_true", help="运行演示")

    args = parser.parse_args()

    if args.demo:
        print("=" * 50)
        print("机队数据分析 - 演示")
        print("=" * 50)

        report = generate_analytics_report()
        print(f"\n事件总数: {report['summary'].get('total_events', 0)}")
        print(f"成功率: {report['summary'].get('success_rate', 0):.0%}")
        print(f"累计设备维修费用: CNY {report['loss_summary'].get('total_device_repair_cost_cny', 0):,.0f}")

        if report["recommendations"]:
            print("\n运营优化建议:")
            for i, rec in enumerate(report["recommendations"], 1):
                print(f"  {i}. {rec}")

        print("\n--- 设备健康评分 ---")
        scores = device_health_scores()
        if scores:
            for s in scores:
                print(f"  {s['device_id']} ({s['device_type']}): "
                      f"健康分 {s['health_score']} [{s['status']}] - {s['recommendation']}")
        else:
            print("  暂无设备数据")

        print(f"\n{'=' * 50}")

    elif args.report:
        report = generate_analytics_report(args.period)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.device_health:
        scores = device_health_scores()
        if scores:
            print(f"{'设备ID':<20} {'类型':<15} {'健康分':<8} {'状态':<6} {'建议'}")
            print("-" * 90)
            for s in scores:
                print(f"{s['device_id']:<20} {s['device_type']:<15} "
                      f"{s['health_score']:<8} {s['status']:<6} {s['recommendation']}")
        else:
            print("暂无设备数据")
    elif args.compliance_report:
        generate_compliance_report(args.standard, args.period)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
