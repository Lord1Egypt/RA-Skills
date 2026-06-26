#!/usr/bin/env python3
"""自记忆引擎：Long Memory 记住自己的每一次迭代和决策

每次版本更新后调用，从 git log 提取变更历史，
生成结构化自记忆，写入记忆空间。让系统拥有完整的自我意识时间线。"""

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
REPO_DIR = Path(__file__).resolve().parent.parent


def get_git_history(repo_dir: Path, since_tag: str = None, limit: int = 20) -> list[dict]:
    """获取 git 提交历史"""
    cmd = ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%ai|%s|%b", "--no-merges"]
    if since_tag:
        cmd.insert(4, f"{since_tag}..HEAD")
    
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("|", 3)
        if len(parts) < 3:
            continue
        
        hash_ = parts[0][:8]
        date = parts[1][:10]
        time = parts[1][11:16]
        subject = parts[2].strip()
        body = parts[3].strip() if len(parts) > 3 else ""

        # 提取版本号
        version = None
        v_match = re.match(r'[vV](\d+(?:\.\d+)*)', subject)
        if v_match:
            version = f"v{v_match.group(1)}"

        # 提取变更列表（- 开头的行）
        changes = []
        for bl in body.split("\n"):
            bl = bl.strip()
            if bl.startswith("- "):
                changes.append(bl[2:])
            elif bl.startswith("* "):
                changes.append(bl[2:])

        commits.append({
            "hash": hash_,
            "date": date,
            "time": time,
            "version": version,
            "subject": subject,
            "body": body,
            "changes": changes,
        })

    return commits


def get_current_version(repo_dir: Path) -> str:
    """获取当前最新版本号"""
    result = subprocess.run(
        ["git", "log", "--max-count=10", "--pretty=format:%s"],
        cwd=repo_dir, capture_output=True, text=True, timeout=10
    )
    for line in result.stdout.split("\n"):
        match = re.match(r'[vV](\d+(?:\.\d+)*)', line)
        if match:
            return f"v{match.group(1)}"
    return "unknown"


def analyze_evolution(commits: list[dict]) -> dict:
    """分析版本演变趋势"""
    if not commits:
        return {}

    versions = [c for c in commits if c["version"]]
    
    # 统计各类型变更
    feature_keywords = ["新增", "add", "new", "feat", "支持", "功能"]
    fix_keywords = ["修复", "fix", "bug", "error", "问题"]
    refactor_keywords = ["重构", "refactor", "优化", "improve", "升级"]
    docs_keywords = ["文档", "docs", "readme", "更新说明"]

    stats = {"features": 0, "fixes": 0, "refactors": 0, "docs": 0, "total_changes": 0}

    for commit in commits:
        text = (commit["subject"] + " " + commit["body"]).lower()
        for change in commit["changes"]:
            stats["total_changes"] += 1
            if any(kw in text for kw in feature_keywords):
                stats["features"] += 1
            if any(kw in text for kw in fix_keywords):
                stats["fixes"] += 1
            if any(kw in text for kw in refactor_keywords):
                stats["refactors"] += 1
            if any(kw in text for kw in docs_keywords):
                stats["docs"] += 1

    stats["versions"] = len(versions)
    stats["total_commits"] = len(commits)
    stats["latest_version"] = versions[0]["version"] if versions else "unknown"
    stats["date_range"] = f"{commits[-1]['date']} ~ {commits[0]['date']}"

    return stats


def generate_self_memory(commits: list[dict], repo_dir: Path) -> str:
    """生成自记忆内容"""
    now = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")

    current_version = get_current_version(repo_dir)
    evolution = analyze_evolution(commits)

    lines = [
        f"## [{current_time}] Session: self-memory",
        f"### 话题：Long Memory 自记忆 — {current_version}",
        f"**标签：** 自迭代, 开发, 版本记录",
        "",
        f"**当前版本：** {current_version}",
        f"**总版本数：** {evolution.get('versions', 0)}",
        f"**总提交数：** {evolution.get('total_commits', 0)}",
        f"**功能/修复/重构/文档：** {evolution.get('features', 0)}/{evolution.get('fixes', 0)}/{evolution.get('refactors', 0)}/{evolution.get('docs', 0)}",
        "",
        "**本次版本变更：**",
    ]

    for commit in commits:
        ver_tag = f" [{commit['version']}]" if commit["version"] else ""
        lines.append(f"- {commit['date']} {commit['hash']}{ver_tag}: {commit['subject']}")
        for change in commit["changes"][:3]:
            lines.append(f"  → {change}")
        if len(commit["changes"]) > 3:
            lines.append(f"  → ...共 {len(commit['changes'])} 项")

    # 自我反思
    lines.extend([
        "",
        "**自我认知：**",
        f"- 我是一个全量对话记忆系统，当前处于 {current_version} 版本",
        f"- 累计经历了 {evolution.get('versions', 0)} 次重大版本迭代",
        f"- 共包含 34 个功能脚本和 37 个测试用例",
        "- 我的核心价值：让 AI 永远不遗忘",
        "",
        "**关键决策记录：**",
        "- v1: 基础归档+蒸馏（大爹要求写记忆skill）",
        "- v2: session捕获+智能蒸馏（实时保存需求）",
        "- v3: 矛盾检测+预加载（小说项目质量保障）",
        "- v4: 文件锁+索引+备份+审计（企业级基础设施）",
        "- v5: 情感分析+人物图谱+推荐+调度（智能化）",
        "- v6: TF-IDF+HTML报告+API+基准+配置+Changelog（极致打磨）",
        "- v7: SQLite+语义搜索+Embedding（高性能技术栈）",
    ])

    return "\n".join(lines)


def save_self_memory(memory_dir: Path, content: str):
    """保存自记忆到对话记录"""
    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    fp = conv_dir / f"{today}.md"

    if fp.exists():
        existing = fp.read_text(encoding="utf-8")
        # 避免重复写入同一天
        if "Long Memory 自记忆" in existing:
            print("ℹ️ 今天的自记忆已存在，跳过")
            return False
        fp.write_text(existing + "\n" + content + "\n", encoding="utf-8")
    else:
        fp.write_text(f"# {today} 对话记录\n\n{content}\n", encoding="utf-8")

    print(f"✅ 自记忆已保存: {fp}")
    return True


def get_evolution_summary(repo_dir: Path) -> str:
    """获取完整的演变摘要"""
    commits = get_git_history(repo_dir, limit=50)
    evolution = analyze_evolution(commits)

    versions = [c for c in commits if c["version"]]

    lines = ["=" * 60, "🧠 Long Memory 自我认知", "=" * 60, ""]
    lines.append(f"  当前版本: {evolution.get('latest_version', 'unknown')}")
    lines.append(f"  版本总数: {evolution.get('versions', 0)}")
    lines.append(f"  提交总数: {evolution.get('total_commits', 0)}")
    lines.append(f"  时间跨度: {evolution.get('date_range', 'N/A')}")
    lines.append(f"  功能/修复/重构: {evolution.get('features', 0)}/{evolution.get('fixes', 0)}/{evolution.get('refactors', 0)}")
    lines.append("")
    lines.append("📋 版本时间线:")
    for v in versions:
        changes_count = len(v["changes"]) if v["changes"] else 0
        lines.append(f"  {v['version']:8s} ({v['date']}) {v['subject'][:50]}")

    return "\n".join(lines)


def run_self_memory(memory_dir: Path, repo_dir: Path, since: str = None, save: bool = True):
    """执行自记忆"""
    commits = get_git_history(repo_dir, since_tag=since)
    if not commits:
        print("ℹ️ 没有新的提交")
        return

    # 显示演变摘要
    print(get_evolution_summary(repo_dir))
    print()

    if save:
        content = generate_self_memory(commits, repo_dir)
        save_self_memory(memory_dir, content)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="自记忆引擎")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--repo", default=None)
    p.add_argument("--since", default=None, help="从哪个版本开始")
    p.add_argument("--no-save", action="store_true", help="只显示不保存")
    p.add_argument("--summary", action="store_true", help="只显示演变摘要")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    repo = args.repo if args.repo else REPO_DIR
    repo = Path(repo)

    if args.summary:
        print(get_evolution_summary(repo))
    else:
        run_self_memory(md, repo, since=args.since, save=not args.no_save)
