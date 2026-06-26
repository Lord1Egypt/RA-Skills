"""
企业应急预案生成器 (Emergency Plan Generator)

v0.2.0 新增 — 基于企业知识库自动生成定制化应急预案文档。

负责：
- 根据企业设备类型、运营区域、历史数据自动生成应急预案
- 支持 Markdown / JSON 格式输出
- 预案版本管理
- 差异对比
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
KB_ROOT = PROJECT_ROOT / ".guardian" / "enterprise_kb"
PLANS_DIR = PROJECT_ROOT / ".guardian" / "emergency_plans"
SOLUTION_TEMPLATES = PROJECT_ROOT / "assets" / "solution_templates"
PLAN_TEMPLATES = PROJECT_ROOT / "assets" / "enterprise_templates"

sys.path.insert(0, str(Path(__file__).parent))


def generate_plan(enterprise: str, scope: str = "通用",
                  device_types: list = None,
                  output_format: str = "markdown") -> str:
    """
    生成企业应急预案。

    Args:
        enterprise: 企业名称
        scope: 业务范围（城市配送/巡检/测绘等）
        device_types: 使用的设备类型列表
        output_format: 输出格式 (markdown/json)
    """
    PLANS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    version = _get_next_version()
    device_types = device_types or ["multirotor"]

    # 收集知识库数据
    kb_stats = _collect_kb_statistics()
    solutions = _collect_solutions(device_types)

    if output_format == "markdown":
        content = _render_markdown_plan(enterprise, scope, device_types,
                                         version, now, kb_stats, solutions)
    else:
        content = _render_json_plan(enterprise, scope, device_types,
                                    version, now, kb_stats, solutions)

    # 保存
    ext = "md" if output_format == "markdown" else "json"
    filename = f"emergency_plan_v{version}.{ext}"
    output_path = PLANS_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 保存版本元数据
    meta = {
        "version": version,
        "generated_at": now.isoformat(),
        "enterprise": enterprise,
        "scope": scope,
        "device_types": device_types,
        "format": output_format,
        "file": filename,
        "status": "draft",
    }
    meta_file = PLANS_DIR / f"meta_v{version}.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[预案生成] v{version} 已生成: {output_path}")
    return str(output_path)


def _get_next_version() -> str:
    """获取下一个版本号。"""
    if not PLANS_DIR.exists():
        return "1.0"

    existing = list(PLANS_DIR.glob("meta_v*.json"))
    if not existing:
        return "1.0"

    versions = []
    for f in existing:
        try:
            with open(f, encoding="utf-8") as fp:
                meta = json.load(fp)
            versions.append(float(meta.get("version", "0")))
        except (json.JSONDecodeError, ValueError):
            continue

    return f"{max(versions) + 1.0:.1f}" if versions else "1.0"


def _collect_kb_statistics() -> dict:
    """收集知识库统计数据。"""
    stats = {"total_events": 0, "by_type": {}, "by_severity": {}, "top_causes": []}

    idx_type = KB_ROOT / "incidents" / "by_type"
    if idx_type.exists():
        for type_dir in idx_type.iterdir():
            if type_dir.is_dir():
                count = len(list(type_dir.glob("*.json")))
                stats["by_type"][type_dir.name] = count
                stats["total_events"] += count

    idx_sev = KB_ROOT / "incidents" / "by_severity"
    if idx_sev.exists():
        for sev_dir in idx_sev.iterdir():
            if sev_dir.is_dir():
                stats["by_severity"][sev_dir.name] = len(list(sev_dir.glob("*.json")))

    stats["top_causes"] = sorted(stats["by_type"].items(), key=lambda x: -x[1])[:5]
    return stats


def _collect_solutions(device_types: list) -> list:
    """收集适用的解决方案。"""
    solutions = []
    if SOLUTION_TEMPLATES.exists():
        for f in SOLUTION_TEMPLATES.glob("*.json"):
            try:
                with open(f, encoding="utf-8") as fp:
                    sol = json.load(fp)
                # 检查设备类型兼容性
                applicable = sol.get("applicable_devices", [])
                if not applicable or any(d in applicable for d in device_types):
                    solutions.append(sol)
            except (json.JSONDecodeError, KeyError):
                continue
    return solutions


def _render_markdown_plan(enterprise, scope, device_types, version,
                           now, kb_stats, solutions) -> str:
    """渲染 Markdown 格式的应急预案。"""
    lines = []

    # 封面
    lines.extend([
        f"# {enterprise} 无人设备应急预案",
        "",
        f"> 版本: v{version} | 生成时间: {now.strftime('%Y-%m-%d %H:%M')} UTC",
        f"> 适用范围: {scope} | 设备类型: {', '.join(device_types)}",
        f"> 本预案由 Low-Altitude Guardian 自动生成，请结合企业实际情况审核修订",
        "",
        "---",
        "",
        "## 1. 总则",
        "",
        "### 1.1 编制目的",
        "",
        f"为规范 {enterprise} 无人设备运营中的应急响应工作，建立健全应急管理体系，",
        "提高突发事件的应对能力，最大限度降低事故造成的人员伤害和财产损失，制定本预案。",
        "",
        "### 1.2 适用范围",
        "",
        f"本预案适用于 {enterprise} 在 {scope} 业务中使用的以下类型无人设备：",
        "",
    ])

    device_desc = {
        "multirotor": "多旋翼无人机",
        "fixed_wing": "固定翼无人机",
        "evtol": "电动垂直起降飞行器 (eVTOL)",
        "delivery_vehicle": "无人配送车",
    }
    for dt in device_types:
        lines.append(f"- {device_desc.get(dt, dt)}")

    lines.extend([
        "",
        "### 1.3 编制依据",
        "",
        "- 《中华人民共和国民用航空法》",
        "- 《无人驾驶航空器飞行管理暂行条例》",
        "- 《民用无人驾驶航空器运行安全管理规则》(CCAR-92)",
        "- 企业安全管理制度",
        "- Low-Altitude Guardian 危机响应知识库",
        "",
        "### 1.4 损失优先级原则",
        "",
        "所有应急决策严格遵循以下不可逆转的优先级排序：",
        "",
        "| 优先级 | 保护对象 | 决策权重 | 说明 |",
        "|--------|---------|---------|------|",
        "| P0 | 人员安全 | 40% | 绝对最高，不可妥协 |",
        "| P1 | 公共安全 | 25% | 公共设施、交通安全 |",
        "| P2 | 第三方财产 | 15% | 他人财产 |",
        "| P3 | 本机安全 | 12% | 设备完整性 |",
        "| P4 | 任务完成 | 8% | 原定业务目标 |",
        "",
        "---",
        "",
        "## 2. 组织架构与职责",
        "",
        "### 2.1 应急指挥体系",
        "",
        "| 角色 | 职责 | 响应要求 |",
        "|------|------|---------|",
        "| 应急总指挥 | 统一指挥应急行动，审批重大决策 | L4-L5事件15分钟内到位 |",
        "| 运维主管 | 协调现场处置，指导操作员 | L3以上事件5分钟内响应 |",
        "| 飞行操作员 | 直接操控设备，执行应急程序 | 即时响应 |",
        "| 安全监督员 | 监督应急操作合规性，记录过程 | L3以上事件到场 |",
        "| 外联协调员 | 与空管/消防/医疗/监管机构联络 | L4以上事件10分钟内启动 |",
        "",
        "---",
        "",
        "## 3. 风险识别与评估",
        "",
    ])

    # 基于知识库数据生成风险分析
    if kb_stats["total_events"] > 0:
        lines.extend([
            "### 3.1 历史事件统计",
            "",
            f"基于企业知识库 {kb_stats['total_events']} 条历史事件记录分析：",
            "",
        ])
        if kb_stats["top_causes"]:
            lines.append("**高频危机类型排名：**")
            lines.append("")
            lines.append("| 排名 | 危机类型 | 事件数 |")
            lines.append("|------|---------|--------|")
            for i, (cause, count) in enumerate(kb_stats["top_causes"], 1):
                lines.append(f"| {i} | {cause} | {count} |")
            lines.append("")
    else:
        lines.extend([
            "### 3.1 历史事件统计",
            "",
            "> 注意: 企业知识库中暂无历史事件数据。随着运营数据的积累，此章节将自动更新。",
            "",
        ])

    lines.extend([
        "### 3.2 主要风险类型",
        "",
        "| 风险类别 | 典型场景 | 发生概率 | 影响等级 |",
        "|---------|---------|---------|---------|",
        "| 动力系统故障 | 电机失效、电池异常 | 中 | L3-L5 |",
        "| 导航定位故障 | GPS丢失、IMU漂移 | 中低 | L2-L4 |",
        "| 通信故障 | 链路断开、信号干扰 | 低 | L2-L3 |",
        "| 环境威胁 | 极端天气、鸟击 | 中 | L2-L4 |",
        "| 碰撞风险 | 障碍物、空中冲突 | 低 | L3-L5 |",
        "",
        "---",
        "",
        "## 4. 分级响应程序",
        "",
        "### 4.1 危机等级定义",
        "",
        "| 等级 | 名称 | 定义 | 响应时限 | 人工介入 |",
        "|------|------|------|---------|---------|",
        "| L5 | 灾难性 | 即刻威胁人员生命 | < 3秒 | 设备自主执行，事后通知 |",
        "| L4 | 严重 | 高概率人员伤害/重大损失 | < 10秒 | 设备自主执行，同步通知 |",
        "| L3 | 重大 | 设备功能严重降级 | < 30秒 | 推荐方案，5秒超时自动执行 |",
        "| L2 | 一般 | 设备功能部分降级 | < 2分钟 | 等待操作员确认 |",
        "| L1 | 注意 | 潜在风险因素 | < 5分钟 | 仅提醒 |",
        "",
        "### 4.2 各等级响应流程",
        "",
        "**L5-灾难性**：设备自主执行最高人员安全得分方案 → 即时通知应急指挥部 → 启动外部救援联络 → 现场保护",
        "",
        "**L4-严重**：设备自主执行最优方案 → 同步通知运维主管 → 评估是否升级 → 事件记录",
        "",
        "**L3-重大**：系统推荐方案 → 操作员5秒内确认/修改 → 超时自动执行 → 持续监控",
        "",
        "**L2-一般**：系统推荐方案 → 操作员确认后执行 → 记录处理过程",
        "",
        "**L1-注意**：系统发出提醒 → 操作员评估是否需要干预 → 纳入值班日志",
        "",
        "---",
        "",
        "## 5. 专项应急处置方案",
        "",
    ])

    # 从解决方案模板生成专项处置方案
    for sol in solutions:
        name = sol.get("name", "未命名方案")
        crisis_type = sol.get("crisis_type", "")
        levels = sol.get("applicable_levels", [])
        actions = sol.get("actions", [])
        success_rate = sol.get("historical_success_rate", 0)

        lines.extend([
            f"### 5.x {name}",
            "",
            f"- **适用危机**: {crisis_type}",
            f"- **适用等级**: {', '.join(levels)}",
            f"- **历史成功率**: {success_rate:.0%}",
            "",
            "**处置步骤：**",
            "",
        ])
        for action in actions:
            step = action.get("step", "?")
            desc = action.get("description", action.get("action", ""))
            timeout = action.get("timeout_ms")
            timeout_str = f"（超时 {timeout}ms）" if timeout else ""
            lines.append(f"{step}. {desc}{timeout_str}")

        lines.extend(["", ""])

    lines.extend([
        "---",
        "",
        "## 6. 事后处置",
        "",
        "### 6.1 现场保护",
        "- L3以上事件：保护现场不少于24小时",
        "- 拍照记录设备状态、坠落位置、周边环境",
        "- 提取设备飞行记录仪（黑匣子）数据",
        "",
        "### 6.2 事件调查",
        "- 72小时内完成初步事件报告",
        "- 收集传感器日志、决策链路记录、通信记录",
        "- 分析根本原因，区分设备故障/操作失误/环境因素",
        "",
        "### 6.3 整改与预防",
        "- 将事件经验录入企业知识库",
        "- 更新解决方案模板参数",
        "- 必要时修订本应急预案",
        "- 组织全员安全培训",
        "",
        "---",
        "",
        "## 7. 保障措施",
        "",
        "### 7.1 培训与演练",
        "- 新入职操作员完成应急响应培训后方可上岗",
        "- 每季度至少进行一次应急演练（可使用模拟场景）",
        "- 每次重大事件后进行全员复盘",
        "",
        "### 7.2 物资保障",
        "- 各运营站点配备应急工具包",
        "- 关键备件库存不低于安全库存",
        "- 应急通信设备定期检查",
        "",
        "---",
        "",
        f"*本预案由 Low-Altitude Guardian v0.2.0 自动生成*",
        f"*生成时间: {now.strftime('%Y-%m-%d %H:%M')} UTC*",
        f"*下次建议更新: 知识库发生重大变更时或每季度定期更新*",
    ])

    return "\n".join(lines)


def _render_json_plan(enterprise, scope, device_types, version,
                      now, kb_stats, solutions) -> str:
    """渲染 JSON 格式的应急预案。"""
    plan = {
        "metadata": {
            "enterprise": enterprise,
            "scope": scope,
            "device_types": device_types,
            "version": version,
            "generated_at": now.isoformat(),
            "generator": "low-altitude-guardian v0.2.0",
        },
        "risk_assessment": kb_stats,
        "response_levels": {
            "L5": {"name": "灾难性", "response_time_s": 3, "human_mode": "autonomous"},
            "L4": {"name": "严重", "response_time_s": 10, "human_mode": "autonomous_notify"},
            "L3": {"name": "重大", "response_time_s": 30, "human_mode": "recommend_timeout_5s"},
            "L2": {"name": "一般", "response_time_s": 120, "human_mode": "await_confirm"},
            "L1": {"name": "注意", "response_time_s": 300, "human_mode": "advisory"},
        },
        "solutions": [{
            "name": s.get("name"),
            "crisis_type": s.get("crisis_type"),
            "applicable_levels": s.get("applicable_levels"),
            "success_rate": s.get("historical_success_rate"),
            "steps_count": len(s.get("actions", [])),
        } for s in solutions],
    }
    return json.dumps(plan, ensure_ascii=False, indent=2)


def list_versions():
    """列出所有预案版本。"""
    if not PLANS_DIR.exists():
        print("暂无预案版本")
        return

    metas = sorted(PLANS_DIR.glob("meta_v*.json"))
    if not metas:
        print("暂无预案版本")
        return

    print("预案版本列表:\n")
    for f in metas:
        with open(f, encoding="utf-8") as fp:
            meta = json.load(fp)
        status_mark = " [正式]" if meta.get("status") == "published" else " [草案]"
        print(f"  v{meta['version']}{status_mark}")
        print(f"    生成时间: {meta['generated_at']}")
        print(f"    企业: {meta['enterprise']}")
        print(f"    范围: {meta['scope']}")
        print(f"    文件: {meta['file']}")
        print()


def publish_version(version: str):
    """标记预案版本为正式发布。"""
    meta_file = PLANS_DIR / f"meta_v{version}.json"
    if not meta_file.exists():
        print(f"[错误] 版本 v{version} 不存在")
        return

    with open(meta_file, encoding="utf-8") as f:
        meta = json.load(f)

    meta["status"] = "published"
    meta["published_at"] = datetime.now(timezone.utc).isoformat()

    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[发布] v{version} 已标记为正式发布版本")


# ─── CLI ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="低空卫士 - 企业应急预案生成器")
    parser.add_argument("--generate", action="store_true", help="生成应急预案")
    parser.add_argument("--enterprise", type=str, default="示例企业", help="企业名称")
    parser.add_argument("--scope", type=str, default="通用运营", help="业务范围")
    parser.add_argument("--device-types", type=str, default="multirotor", help="设备类型（逗号分隔）")
    parser.add_argument("--output-format", type=str, default="markdown", choices=["markdown", "json"])
    parser.add_argument("--versions", action="store_true", help="列出预案版本")
    parser.add_argument("--publish", action="store_true", help="发布预案版本")
    parser.add_argument("--version", type=str, help="版本号")
    parser.add_argument("--demo", action="store_true", help="运行演示")

    args = parser.parse_args()

    if args.demo:
        print("=" * 50)
        print("企业应急预案生成器 - 演示")
        print("=" * 50)
        path = generate_plan("顺丰低空物流运营部", "城市无人机配送", ["multirotor"])
        print(f"\n预案文件: {path}")
        print("\n--- 预案前30行预览 ---")
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 30:
                    print("  ...")
                    break
                print(f"  {line}", end="")
        print(f"\n{'=' * 50}")
    elif args.generate:
        device_types = [d.strip() for d in args.device_types.split(",")]
        generate_plan(args.enterprise, args.scope, device_types, args.output_format)
    elif args.versions:
        list_versions()
    elif args.publish:
        if not args.version:
            print("错误: --publish 需要 --version")
            sys.exit(1)
        publish_version(args.version)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
