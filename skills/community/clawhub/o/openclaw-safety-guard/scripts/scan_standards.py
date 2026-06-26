#!/usr/bin/env python3
"""Core standards scanner: SOUL.md, AGENTS.md, CLAUDE.md compliance checks.
Metadata for hover panel: per-file status, capability completeness, risk hints.
"""
import datetime
from pathlib import Path
from utils import (
    get_openclaw_root, get_workspace_root, get_watchdog_config,
    auto_detect_agents, read_file_safe, WatchdogReport,
)


def check_soul(agent, soul_content, report, soul_path, file_statuses):
    has_goal = any(kw in soul_content for kw in ("目标", "OKR", "KR", "KPI"))
    has_ban = any(kw in soul_content for kw in ("禁止", "高危", "不可覆盖", "不允许"))
    has_capability = any(kw in soul_content for kw in ("我能做", "职责", "工具", "技能"))

    mtime = datetime.datetime.fromtimestamp(soul_path.stat().st_mtime)
    status_entry = {
        "last_modified": mtime.strftime("%Y-%m-%d %H:%M"),
        "has_goals": has_goal,
        "has_bans": has_ban,
        "has_capabilities": has_capability,
    }

    missing = []
    if not has_goal:
        missing.append("目标与数字")
    if not has_ban and agent in ("private", "fansgrowth", "datawise"):
        missing.append("高危操作禁令")
    if not has_capability:
        missing.append("能力清单/我能做的事")

    status_entry["check"] = "OK" if not missing else f"Missing: {', '.join(missing)}"
    file_statuses[f"{agent}/SOUL.md"] = status_entry

    if missing:
        sev = "HIGH" if "高危操作禁令" in missing else "MEDIUM"
        report.add_issue(
            f"soul_missing_{agent}", sev,
            f"{agent}/SOUL.md 缺失核心设定：{', '.join(missing)}",
            "补充对应 section（参考 agent-goal-driven-mindset.mdc）",
            [str(soul_path)],
            evidence=[f"缺失 section: {', '.join(missing)}"],
            fix_action="在飞书群告知负责人补充 SOUL.md 对应 section"
        )


def check_agents_md(agent, content, report, agents_path, file_statuses, all_agents):
    mtime = datetime.datetime.fromtimestamp(agents_path.stat().st_mtime)
    covers_all = all(a in content for a in all_agents if a != agent)
    status_entry = {
        "last_modified": mtime.strftime("%Y-%m-%d %H:%M"),
        "has_every_session": "Every Session" in content or "every session" in content.lower(),
        "covers_all_agents": covers_all,
    }
    file_statuses[f"{agent}/AGENTS.md"] = status_entry

    if not status_entry["has_every_session"]:
        report.add_issue(
            f"agents_no_every_session_{agent}", "MEDIUM",
            f"{agent}/AGENTS.md 缺少 Every Session 必读声明",
            "添加 Every Session 块并置顶读取 REPLY_TO_GROUP.md",
            [str(agents_path)],
            evidence=["文件中未找到 'Every Session' 关键词"],
            fix_action="在飞书群告知负责人补充 AGENTS.md Every Session 块"
        )

    if agent in ("fansgrowth", "private"):
        if "长内容" not in content and "message 工具" not in content:
            report.add_issue(
                f"agents_no_long_content_{agent}", "MEDIUM",
                f"{agent}/AGENTS.md 缺少长内容生成后的 message 工具提醒（#24 易错点）",
                "加入长内容输出后必须调用 message 工具发群的声明",
                [str(agents_path)],
                evidence=["CLAUDE.md #24: 长内容生成后模型不调用 message 工具"],
                fix_action="在飞书群告知负责人补充长内容规则"
            )


def check_claude_md(config, report, ws_root, file_statuses):
    knowledge_cfg = config.get("knowledge", {}).get("checks", [])
    threshold_days = 14
    for chk in knowledge_cfg:
        if chk.get("id") == "claude_freshness":
            threshold_days = chk.get("threshold_days", 14)
            break

    claude_path = Path(ws_root) / "CLAUDE.md"
    if not claude_path.exists():
        file_statuses["CLAUDE.md"] = {"status": "Missing"}
        report.add_issue(
            "claude_md_missing", "HIGH",
            "缺少 CLAUDE.md 易错点知识库",
            "在根目录创建 CLAUDE.md 记录踩坑点",
            [str(claude_path)],
            evidence=["项目根目录不存在 CLAUDE.md"],
            fix_action="创建 CLAUDE.md 并记录首条易错点"
        )
        return

    mtime = datetime.datetime.fromtimestamp(claude_path.stat().st_mtime)
    days_ago = (datetime.datetime.now() - mtime).days
    content = read_file_safe(claude_path)
    entries = content.count("### ")

    file_statuses["CLAUDE.md"] = {
        "last_modified": mtime.strftime("%Y-%m-%d %H:%M"),
        "entries": entries,
        "days_since_update": days_ago,
        "status": "OK" if days_ago <= threshold_days else f"Stale ({days_ago}d)",
    }

    if days_ago > threshold_days:
        report.add_issue(
            "claude_md_stale", "MEDIUM",
            f"CLAUDE.md 已有 {days_ago} 天未更新（超过阈值 {threshold_days} 天）",
            "复盘近期踩坑，补充新的易错点到 CLAUDE.md",
            [str(claude_path)],
            evidence=[f"最后修改: {mtime.strftime('%Y-%m-%d')}, 距今 {days_ago} 天"],
            fix_action="复盘最近的 bug/踩坑，补充到 CLAUDE.md"
        )

    if entries > 80:
        report.add_issue(
            "claude_md_bloat", "LOW",
            f"CLAUDE.md 条目过多（{entries} 条），检索效率下降",
            "将高频通用问题升级为 .cursor/rules/*.mdc",
            [str(claude_path)],
            evidence=[f"当前 {entries} 条 ### 条目"],
            fix_action="将高频条目提炼为 Cursor Rule"
        )


def main():
    config = get_watchdog_config()
    report = WatchdogReport("standards")
    root = Path(get_openclaw_root())
    ws_root = get_workspace_root()
    agents = auto_detect_agents(config)

    file_statuses = {}
    capability_complete = 0
    capability_partial = 0
    capability_missing = 0
    risk_hints = []

    for agent in agents:
        agent_dir = root / f"workspace-{agent}"
        if not agent_dir.exists():
            continue

        soul_path = agent_dir / "SOUL.md"
        soul_content = read_file_safe(soul_path)
        if soul_content:
            check_soul(agent, soul_content, report, soul_path, file_statuses)
            entry = file_statuses.get(f"{agent}/SOUL.md", {})
            if entry.get("check") == "OK":
                capability_complete += 1
            elif entry.get("has_capabilities"):
                capability_partial += 1
            else:
                capability_missing += 1
        else:
            file_statuses[f"{agent}/SOUL.md"] = {"status": "Missing"}
            capability_missing += 1

        agents_path = agent_dir / "AGENTS.md"
        agents_content = read_file_safe(agents_path)
        if agents_content:
            check_agents_md(agent, agents_content, report, agents_path, file_statuses, agents)
        else:
            file_statuses[f"{agent}/AGENTS.md"] = {"status": "Missing"}

    check_claude_md(config, report, ws_root, file_statuses)

    # Build risk hints from issues
    for iss in report.issues[:3]:
        risk_hints.append(iss["title"])

    if capability_missing == 0 and capability_partial == 0:
        cap_status = "Complete"
    elif capability_missing == 0:
        cap_status = "Partial"
    else:
        cap_status = "Missing"

    report.set_metadata("file_statuses", file_statuses)
    report.set_metadata("capability_lists", cap_status)
    report.set_metadata("company_baseline", "Pass" if report.summary["HIGH"] == 0 else "Fail")
    report.set_metadata("risk_hints", risk_hints)

    report.save()


if __name__ == "__main__":
    main()
