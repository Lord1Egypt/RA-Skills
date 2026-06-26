"""
企业知识库管理器 (Enterprise Knowledge Base Manager)

v0.2.0 新增 — 面向运营企业的知识库构建与管理工具。

负责：
- 多源数据采集（事件日志/历史报告/行业案例/人工经验）
- 知识库结构化存储与索引
- 知识库搜索与查询
- 知识库健康度评估
- 知识库导入导出
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
KB_ROOT = PROJECT_ROOT / ".guardian" / "enterprise_kb"
INCIDENTS_DIR = PROJECT_ROOT / ".guardian" / "incidents"

# 知识库子目录
KB_INCIDENTS = KB_ROOT / "incidents"
KB_SOLUTIONS = KB_ROOT / "solutions"
KB_RULES = KB_ROOT / "rules"
KB_FLEET = KB_ROOT / "fleet"
KB_COMPLIANCE = KB_ROOT / "compliance"

# 索引子目录
IDX_BY_TYPE = KB_INCIDENTS / "by_type"
IDX_BY_DEVICE = KB_INCIDENTS / "by_device"
IDX_BY_REGION = KB_INCIDENTS / "by_region"
IDX_BY_SEVERITY = KB_INCIDENTS / "by_severity"


def init_kb():
    """初始化企业知识库目录结构。"""
    dirs = [
        IDX_BY_TYPE, IDX_BY_DEVICE, IDX_BY_REGION, IDX_BY_SEVERITY,
        KB_SOLUTIONS / "validated", KB_SOLUTIONS / "draft", KB_SOLUTIONS / "deprecated",
        KB_RULES, KB_FLEET, KB_COMPLIANCE / "audit_trail",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print("[知识库] 目录结构已初始化")


def ingest_data(source_type: str, input_path: str = None):
    """
    从指定数据源导入数据到知识库。

    Args:
        source_type: 数据源类型
        input_path: 输入文件路径
    """
    init_kb()

    handlers = {
        "incident_log": _ingest_incident_log,
        "guardian_events": _ingest_guardian_events,
        "industry_case": _ingest_industry_case,
        "vendor_bulletin": _ingest_vendor_bulletin,
        "regulation": _ingest_regulation,
        "manual_experience": _ingest_manual_experience,
    }

    handler = handlers.get(source_type)
    if not handler:
        print(f"[错误] 不支持的数据源类型: {source_type}")
        print(f"  支持的类型: {', '.join(handlers.keys())}")
        sys.exit(1)

    handler(input_path)


def _ingest_guardian_events(input_path: str = None):
    """导入本系统生成的事件报告。"""
    source_dir = Path(input_path) if input_path else INCIDENTS_DIR
    if not source_dir.exists():
        print("[警告] 暂无设备端事件数据")
        return

    files = list(source_dir.glob("INC-*.json"))
    imported = 0
    for f in files:
        try:
            with open(f, encoding="utf-8") as fp:
                event = json.load(fp)
            _index_event(event)
            imported += 1
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  [跳过] {f.name}: {e}")

    print(f"[导入] 从设备端导入 {imported} 条事件记录")


def _ingest_incident_log(input_path: str):
    """导入 CSV 格式的历史事件日志。"""
    if not input_path:
        print("[错误] 需要 --input 指定 CSV 文件路径")
        return

    path = Path(input_path)
    if not path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        return

    imported = 0
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            event = {
                "incident_id": row.get("id", f"HIST-{imported:04d}"),
                "device_id": row.get("device_id", ""),
                "device_type": row.get("device_type", ""),
                "crisis_type": row.get("crisis_type", ""),
                "crisis_level": row.get("level", ""),
                "crisis_trigger": row.get("trigger", row.get("description", "")),
                "location": row.get("location", ""),
                "outcome_success": row.get("outcome", "").lower() in ("true", "success", "1", "yes"),
                "source": "historical_import",
                "import_time": datetime.now(timezone.utc).isoformat(),
            }
            _index_event(event)
            imported += 1

    print(f"[导入] 从 CSV 导入 {imported} 条历史记录")


def _ingest_industry_case(input_path: str):
    """导入行业案例（纯文本）。"""
    if not input_path:
        print("[错误] 需要 --input 指定案例文件路径")
        return

    path = Path(input_path)
    if not path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        return

    with open(path, encoding="utf-8") as f:
        content = f.read()

    case = {
        "case_id": f"CASE-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "source_file": str(path.name),
        "content": content[:5000],  # 截断过长内容
        "import_time": datetime.now(timezone.utc).isoformat(),
        "type": "industry_case",
    }

    case_dir = KB_ROOT / "industry_cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    case_file = case_dir / f"{case['case_id']}.json"
    with open(case_file, "w", encoding="utf-8") as f:
        json.dump(case, f, ensure_ascii=False, indent=2)

    print(f"[导入] 行业案例已录入: {case['case_id']}")


def _ingest_vendor_bulletin(input_path: str):
    """导入厂商安全公告。"""
    if not input_path:
        print("[错误] 需要 --input 指定公告文件路径")
        return

    path = Path(input_path)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    bulletin = {
        "bulletin_id": f"BULL-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "content": content[:5000],
        "import_time": datetime.now(timezone.utc).isoformat(),
        "type": "vendor_bulletin",
    }

    bull_dir = KB_ROOT / "vendor_bulletins"
    bull_dir.mkdir(parents=True, exist_ok=True)
    with open(bull_dir / f"{bulletin['bulletin_id']}.json", "w", encoding="utf-8") as f:
        json.dump(bulletin, f, ensure_ascii=False, indent=2)

    print(f"[导入] 厂商公告已录入: {bulletin['bulletin_id']}")


def _ingest_regulation(input_path: str):
    """导入法规更新。"""
    if not input_path:
        print("[错误] 需要 --input 指定法规文件路径")
        return

    path = Path(input_path)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    reg = {
        "reg_id": f"REG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "content": content[:5000],
        "import_time": datetime.now(timezone.utc).isoformat(),
    }

    with open(KB_COMPLIANCE / f"{reg['reg_id']}.json", "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)

    print(f"[导入] 法规已录入: {reg['reg_id']}")


def _ingest_manual_experience(input_path: str = None):
    """交互式录入人工经验。"""
    print("\n=== 人工经验录入 ===")
    print("请依次输入以下信息（直接回车跳过可选项）：\n")

    exp = {
        "exp_id": f"EXP-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    exp["contributor"] = input("  记录人姓名/工号: ").strip()
    exp["crisis_type"] = input("  相关危机类型（如 power_failure.single_motor_loss）: ").strip()
    exp["device_type"] = input("  相关设备类型: ").strip()
    exp["scenario"] = input("  场景描述: ").strip()
    exp["lesson"] = input("  经验/教训: ").strip()
    exp["suggestion"] = input("  建议措施: ").strip()

    exp_dir = KB_ROOT / "manual_experiences"
    exp_dir.mkdir(parents=True, exist_ok=True)
    with open(exp_dir / f"{exp['exp_id']}.json", "w", encoding="utf-8") as f:
        json.dump(exp, f, ensure_ascii=False, indent=2)

    print(f"\n[录入完成] 经验记录 {exp['exp_id']}")


def _index_event(event: dict):
    """将事件按多维度索引存储。"""
    incident_id = event.get("incident_id", "unknown")

    # 按危机类型索引
    crisis_type = event.get("crisis_type", "unknown").replace(".", "_")
    if crisis_type:
        type_dir = IDX_BY_TYPE / crisis_type
        type_dir.mkdir(parents=True, exist_ok=True)
        with open(type_dir / f"{incident_id}.json", "w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2)

    # 按设备索引
    device_type = event.get("device_type", "unknown")
    if device_type:
        dev_dir = IDX_BY_DEVICE / device_type.replace(" ", "_")
        dev_dir.mkdir(parents=True, exist_ok=True)
        with open(dev_dir / f"{incident_id}.json", "w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2)

    # 按严重等级索引
    level = event.get("crisis_level", "unknown")
    if level:
        sev_dir = IDX_BY_SEVERITY / level
        sev_dir.mkdir(parents=True, exist_ok=True)
        with open(sev_dir / f"{incident_id}.json", "w", encoding="utf-8") as f:
            json.dump(event, f, ensure_ascii=False, indent=2)


def search_kb(query: str) -> list:
    """在知识库中搜索相关记录。"""
    results = []
    query_lower = query.lower()

    # 搜索事件索引
    for idx_dir in [IDX_BY_TYPE, IDX_BY_DEVICE, IDX_BY_SEVERITY]:
        if not idx_dir.exists():
            continue
        for f in idx_dir.rglob("*.json"):
            try:
                with open(f, encoding="utf-8") as fp:
                    data = json.load(fp)
                # 在多个字段中搜索
                searchable = json.dumps(data, ensure_ascii=False).lower()
                if query_lower in searchable:
                    results.append({
                        "source": str(f.relative_to(KB_ROOT)),
                        "incident_id": data.get("incident_id", ""),
                        "crisis_type": data.get("crisis_type", ""),
                        "trigger": data.get("crisis_trigger", ""),
                    })
            except (json.JSONDecodeError, KeyError):
                continue

    # 去重
    seen = set()
    unique = []
    for r in results:
        key = r.get("incident_id", id(r))
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


def health_check() -> dict:
    """评估知识库健康度。"""
    init_kb()

    report = {
        "check_time": datetime.now(timezone.utc).isoformat(),
        "coverage": {},
        "statistics": {},
        "timeliness": {},
        "recommendations": [],
    }

    # 统计事件数量
    total_events = 0
    type_counts = Counter()
    level_counts = Counter()
    device_counts = Counter()

    if IDX_BY_TYPE.exists():
        for type_dir in IDX_BY_TYPE.iterdir():
            if type_dir.is_dir():
                count = len(list(type_dir.glob("*.json")))
                type_counts[type_dir.name] = count
                total_events += count

    if IDX_BY_SEVERITY.exists():
        for sev_dir in IDX_BY_SEVERITY.iterdir():
            if sev_dir.is_dir():
                level_counts[sev_dir.name] = len(list(sev_dir.glob("*.json")))

    if IDX_BY_DEVICE.exists():
        for dev_dir in IDX_BY_DEVICE.iterdir():
            if dev_dir.is_dir():
                device_counts[dev_dir.name] = len(list(dev_dir.glob("*.json")))

    report["statistics"] = {
        "total_events": total_events,
        "by_type": dict(type_counts),
        "by_severity": dict(level_counts),
        "by_device": dict(device_counts),
    }

    # 解决方案覆盖度
    solution_count = {
        "validated": len(list((KB_SOLUTIONS / "validated").glob("*.json"))) if (KB_SOLUTIONS / "validated").exists() else 0,
        "draft": len(list((KB_SOLUTIONS / "draft").glob("*.json"))) if (KB_SOLUTIONS / "draft").exists() else 0,
        "deprecated": len(list((KB_SOLUTIONS / "deprecated").glob("*.json"))) if (KB_SOLUTIONS / "deprecated").exists() else 0,
    }
    report["coverage"]["solutions"] = solution_count

    # 危机分类树覆盖度
    all_crisis_types = [
        "power_failure", "navigation_failure", "communication_failure",
        "environment_threat", "collision_risk", "compound_failure",
    ]
    covered = [t for t in all_crisis_types if any(t in k for k in type_counts.keys())]
    uncovered = [t for t in all_crisis_types if t not in covered]
    report["coverage"]["crisis_types"] = {
        "covered": covered,
        "uncovered": uncovered,
        "coverage_rate": len(covered) / len(all_crisis_types) if all_crisis_types else 0,
    }

    # 改进建议
    if total_events < 10:
        report["recommendations"].append("事件数据量不足（<10条），建议导入更多历史数据以提高知识库价值")
    if uncovered:
        report["recommendations"].append(f"以下危机类型尚无事件记录: {', '.join(uncovered)}，建议补充行业案例")
    if solution_count["validated"] == 0:
        report["recommendations"].append("暂无已验证的企业自定义方案，建议将经过实战检验的方案标记为validated")
    if not (KB_FLEET / "device_registry.json").exists():
        report["recommendations"].append("尚未注册机队设备台账，建议完善设备注册信息")

    return report


def export_kb(output_path: str, fmt: str = "json"):
    """导出整个知识库。"""
    export_data = {
        "export_time": datetime.now(timezone.utc).isoformat(),
        "version": "0.2.0",
        "events": [],
        "solutions": [],
        "rules": {},
    }

    # 收集所有事件
    if IDX_BY_TYPE.exists():
        seen_ids = set()
        for f in IDX_BY_TYPE.rglob("*.json"):
            try:
                with open(f, encoding="utf-8") as fp:
                    event = json.load(fp)
                eid = event.get("incident_id")
                if eid and eid not in seen_ids:
                    seen_ids.add(eid)
                    export_data["events"].append(event)
            except (json.JSONDecodeError, KeyError):
                continue

    # 收集解决方案
    for status_dir in ["validated", "draft"]:
        sol_dir = KB_SOLUTIONS / status_dir
        if sol_dir.exists():
            for f in sol_dir.glob("*.json"):
                try:
                    with open(f, encoding="utf-8") as fp:
                        export_data["solutions"].append(json.load(fp))
                except (json.JSONDecodeError, KeyError):
                    continue

    # 收集规则
    if KB_RULES.exists():
        for f in KB_RULES.glob("*.json"):
            try:
                with open(f, encoding="utf-8") as fp:
                    export_data["rules"][f.stem] = json.load(fp)
            except (json.JSONDecodeError, KeyError):
                continue

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"[导出] 知识库已导出: {output_path}")
    print(f"  事件: {len(export_data['events'])} 条")
    print(f"  方案: {len(export_data['solutions'])} 条")
    print(f"  规则: {len(export_data['rules'])} 项")


def show_status():
    """显示知识库概况。"""
    report = health_check()
    stats = report["statistics"]
    coverage = report["coverage"]

    print("=" * 50)
    print("企业知识库概况")
    print("=" * 50)
    print(f"\n事件总数: {stats['total_events']}")

    if stats["by_type"]:
        print("\n按危机类型:")
        for t, c in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
            print(f"  {t}: {c} 条")

    if stats["by_severity"]:
        print("\n按严重等级:")
        for s, c in sorted(stats["by_severity"].items()):
            print(f"  {s}: {c} 条")

    if stats["by_device"]:
        print("\n按设备类型:")
        for d, c in sorted(stats["by_device"].items(), key=lambda x: -x[1]):
            print(f"  {d}: {c} 条")

    sol = coverage.get("solutions", {})
    print(f"\n解决方案: 已验证 {sol.get('validated', 0)} / 草案 {sol.get('draft', 0)} / 废弃 {sol.get('deprecated', 0)}")

    ct = coverage.get("crisis_types", {})
    print(f"危机类型覆盖率: {ct.get('coverage_rate', 0):.0%}")
    if ct.get("uncovered"):
        print(f"  未覆盖: {', '.join(ct['uncovered'])}")

    if report["recommendations"]:
        print("\n改进建议:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"  {i}. {rec}")

    print(f"\n{'=' * 50}")


# ─── CLI ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 企业知识库管理器")
    parser.add_argument("--ingest", action="store_true", help="导入数据")
    parser.add_argument("--source", type=str,
                        choices=["incident_log", "guardian_events", "industry_case",
                                 "vendor_bulletin", "regulation", "manual_experience"],
                        help="数据源类型")
    parser.add_argument("--input", type=str, help="输入文件路径")
    parser.add_argument("--status", action="store_true", help="显示知识库概况")
    parser.add_argument("--health-check", action="store_true", help="知识库健康度评估")
    parser.add_argument("--search", action="store_true", help="搜索知识库")
    parser.add_argument("--query", type=str, help="搜索关键词")
    parser.add_argument("--export", action="store_true", help="导出知识库")
    parser.add_argument("--format", type=str, default="json", help="导出格式")
    parser.add_argument("--output", type=str, help="输出路径")
    parser.add_argument("--demo", action="store_true", help="运行演示")

    args = parser.parse_args()

    if args.demo:
        _run_demo()
    elif args.ingest:
        if not args.source:
            print("错误: --ingest 需要 --source 指定数据源类型")
            sys.exit(1)
        ingest_data(args.source, args.input)
    elif args.status:
        show_status()
    elif args.health_check:
        report = health_check()
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.search:
        if not args.query:
            print("错误: --search 需要 --query 指定关键词")
            sys.exit(1)
        results = search_kb(args.query)
        print(f"找到 {len(results)} 条相关记录:")
        for r in results:
            print(f"  [{r.get('crisis_type', '?')}] {r.get('incident_id', '?')}: {r.get('trigger', '')}")
    elif args.export:
        output = args.output or "kb_export.json"
        export_kb(output, args.format)
    else:
        parser.print_help()


def _run_demo():
    """企业知识库管理演示。"""
    print("=" * 50)
    print("企业知识库管理器 - 演示")
    print("=" * 50)

    # 导入设备端事件
    print("\n[步骤1] 从设备端导入事件数据...")
    ingest_data("guardian_events")

    # 显示状态
    print("\n[步骤2] 知识库概况:")
    show_status()

    # 搜索
    print("\n[步骤3] 搜索 '电机' 相关记录:")
    results = search_kb("电机")
    for r in results:
        print(f"  [{r.get('crisis_type', '?')}] {r.get('trigger', '')}")

    print(f"\n{'=' * 50}")
    print("演示结束")


if __name__ == "__main__":
    main()
