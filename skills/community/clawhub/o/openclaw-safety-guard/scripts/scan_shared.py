#!/usr/bin/env python3
"""Shared layer scanner: checks shared/ directory integrity and agent mounting.
Metadata for hover panel: enabled, size, file types, permissions, sensitive config.
"""
import os
from pathlib import Path
from utils import (
    get_openclaw_root, get_watchdog_config, auto_detect_agents,
    read_file_safe, WatchdogReport,
)


def get_dir_size(path: Path) -> int:
    total = 0
    try:
        for f in path.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
    except (PermissionError, OSError):
        pass
    return total


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024*1024):.1f} MB"
    return f"{size_bytes / (1024*1024*1024):.1f} GB"


def scan_shared(config, report, root, agents):
    shared_dir = root / "shared"

    if not shared_dir.exists():
        report.mark_not_applicable("shared/ 目录不存在（单 agent 场景无需共享层）")
        report.set_metadata("enabled", False)
        return

    report.set_metadata("enabled", True)

    # Size
    dir_size = get_dir_size(shared_dir)
    report.set_metadata("size", format_size(dir_size))

    # File type distribution
    ext_counts = {}
    total_files = 0
    for f in shared_dir.rglob("*"):
        if f.is_file():
            total_files += 1
            ext = f.suffix.lower() or ".noext"
            ext_counts[ext] = ext_counts.get(ext, 0) + 1

    if total_files > 0:
        type_dist = []
        for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1])[:5]:
            pct = int(count / total_files * 100)
            type_dist.append(f"{ext} {pct}%")
        report.set_metadata("file_types", " · ".join(type_dist))
    else:
        report.set_metadata("file_types", "空目录")

    # Permission check
    wide_perms = []
    for f in shared_dir.rglob("*"):
        if f.is_file():
            try:
                mode = oct(f.stat().st_mode)[-3:]
                if mode in ("777", "776", "766"):
                    wide_perms.append(str(f.relative_to(root)))
            except OSError:
                pass
    report.set_metadata("permissions", "OK" if not wide_perms else f"Wide open ({len(wide_perms)} files)")

    # Sensitive config check
    sensitive_exts = {".env", ".json", ".key", ".pem", ".p12"}
    sensitive_names = {"credentials", "secret", "token", "password", "apikey"}
    sensitive_count = 0
    for f in shared_dir.rglob("*"):
        if f.is_file():
            name_lower = f.stem.lower()
            if f.suffix.lower() in sensitive_exts and any(s in name_lower for s in sensitive_names):
                sensitive_count += 1
    report.set_metadata("sensitive_config", sensitive_count)

    if sensitive_count > 0:
        report.add_issue(
            "shared_sensitive_config", "HIGH",
            f"shared/ 目录中发现 {sensitive_count} 个疑似凭证文件",
            "将凭证文件移出 shared/ 目录，改用环境变量",
            [],
            evidence=[f"检测到 {sensitive_count} 个文件名含 secret/token/password 且扩展名为 .env/.json/.key"],
            fix_action="在飞书群告知 techops 清理 shared/ 中的凭证文件"
        )

    # Required files check
    required_files = ["DECISIONS.md", "OKR.md", "ROSTER.md"]
    for rf in required_files:
        fpath = shared_dir / rf
        if not fpath.exists():
            report.add_issue(
                f"missing_shared_{rf}", "HIGH",
                f"核心共享文件 {rf} 丢失",
                f"在 .openclaw/shared/ 中创建 {rf}",
                [str(fpath)],
                evidence=[f"{rf} 不存在于 shared/ 目录"],
                fix_action=f"创建 shared/{rf} 并填入初始内容"
            )

    if len(agents) < 2:
        return

    for agent in agents:
        agent_dir = root / f"workspace-{agent}"
        if not agent_dir.exists():
            continue

        agents_md = agent_dir / "AGENTS.md"
        content = read_file_safe(agents_md)
        if not content:
            continue

        if "shared/OKR.md" not in content or "shared/ROSTER.md" not in content:
            report.add_issue(
                f"missing_shared_mount_{agent}", "HIGH",
                f"{agent}/AGENTS.md 未正确挂载 shared/OKR.md 或 shared/ROSTER.md",
                "在 Every Session 块添加 exec 读取 shared 文件的逻辑",
                [str(agents_md)],
                evidence=[f"AGENTS.md 中未找到 shared/OKR.md 或 shared/ROSTER.md 引用"],
                fix_action="在飞书群告知负责人补充 AGENTS.md shared 挂载"
            )


def main():
    config = get_watchdog_config()
    report = WatchdogReport("shared")
    root = Path(get_openclaw_root())
    agents = auto_detect_agents(config)

    scan_shared(config, report, root, agents)
    report.save()


if __name__ == "__main__":
    main()
