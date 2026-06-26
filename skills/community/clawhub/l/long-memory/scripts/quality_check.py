#!/usr/bin/env python3
"""记忆质量评分：检测低质量记录并标记"""

import argparse
import re
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# 质量规则
QUALITY_RULES = [
    {
        "id": "short_user_msg",
        "name": "用户消息过短",
        "severity": "low",
        "check": lambda msg, ctx: len(msg) < ctx.get("min_length", 5),
        "desc": "用户消息少于 {min_length} 字，信息量可能不足",
    },
    {
        "id": "short_assistant_reply",
        "name": "助手回复过短",
        "severity": "low",
        "check": lambda msg, ctx: len(msg) < 10 and not any(kw in msg for kw in ["✅", "搞定", "好的"]),
        "desc": "助手回复过短，可能未充分回答",
    },
    {
        "id": "no_decision_extracted",
        "name": "缺少关键信息标记",
        "severity": "medium",
        "check": lambda msg, ctx: ctx.get("has_decision_markers") == False and ctx.get("msg_count", 0) > 5,
        "desc": "对话超过5轮但无关键决策/待办标记，可能遗漏了重要信息",
    },
    {
        "id": "repetitive_topic",
        "name": "话题重复",
        "severity": "medium",
        "check": lambda msg, ctx: ctx.get("topic_repeat_count", 0) > 2,
        "desc": "同一话题讨论超过3次，可能需要整合",
    },
    {
        "id": "orphan_entry",
        "name": "孤立记录",
        "severity": "high",
        "check": lambda msg, ctx: ctx.get("session_count", 1) == 1 and len(msg) < 50,
        "desc": "单条记录且内容少，可能是误记录",
    },
    {
        "id": "has_redacted",
        "name": "包含脱敏标记",
        "severity": "info",
        "check": lambda msg, ctx: "🔴" in msg or "[已脱敏]" in msg or "[REDACTED]" in msg.upper(),
        "desc": "记录包含脱敏内容",
    },
    {
        "id": "empty_tags",
        "name": "缺少标签",
        "severity": "low",
        "check": lambda msg, ctx: ctx.get("has_tags") == False,
        "desc": "对话记录缺少标签，影响检索效率",
    },
]


def analyze_file(filepath: Path) -> dict:
    """分析单个文件的质量"""
    content = safe_read(filepath)
    if not content.strip():
        return {"file": filepath.name, "score": 0, "issues": [{"rule": "empty_file", "severity": "high", "desc": "空文件"}]}

    issues = []
    ctx = {
        "min_length": 5,
        "msg_count": 0,
        "has_decision_markers": False,
        "topic_repeat_count": 0,
        "session_count": content.count("## ["),
        "has_tags": bool(re.findall(r'\*\*标签[：:]\*\*', content)),
    }

    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        
        # 统计用户消息
        if stripped.startswith("**用户：**"):
            ctx["msg_count"] += 1
            msg = re.sub(r'\*\*用户[：:]\*\*\s*', '', stripped)
            for rule in QUALITY_RULES:
                try:
                    if rule["check"](msg, ctx):
                        issues.append({
                            "rule": rule["id"],
                            "severity": rule["severity"],
                            "desc": rule["desc"].format(**ctx),
                            "line": line,
                        })
                except (KeyError, TypeError):
                    pass
        
        # 统计助手回复
        elif stripped.startswith("**助手：**"):
            msg = re.sub(r'\*\*助手[：:]\*\*\s*', '', stripped)
            if len(msg) < 10 and not any(kw in msg for kw in ["✅", "搞定", "好的"]):
                issues.append({
                    "rule": "short_assistant_reply",
                    "severity": "low",
                    "desc": f"助手回复仅 {len(msg)} 字",
                    "line": line,
                })

        # 检查决策标记
        if "**关键决策" in stripped or "**待办" in stripped or "**重要" in stripped:
            ctx["has_decision_markers"] = True

    # 去重
    seen = set()
    unique_issues = []
    for issue in issues:
        key = (issue["rule"], issue.get("line", ""))
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # 计算分数（0-100）
    score = 100
    severity_penalty = {"info": 0, "low": 3, "medium": 8, "high": 15}
    for issue in unique_issues:
        score -= severity_penalty.get(issue["severity"], 5)
    score = max(0, min(100, score))

    return {
        "file": filepath.name,
        "score": score,
        "issues": unique_issues,
        "stats": {
            "sessions": ctx["session_count"],
            "user_messages": ctx["msg_count"],
            "has_decisions": ctx["has_decision_markers"],
            "has_tags": ctx["has_tags"],
        },
    }


def analyze_all(memory_dir: Path) -> dict:
    """分析所有记忆文件"""
    conv_dir = memory_dir / "conversations"
    results = []
    total_score = 0

    if conv_dir.exists():
        for fp in sorted(conv_dir.glob("*.md")):
            result = analyze_file(fp)
            results.append(result)
            total_score += result["score"]

    avg_score = total_score / len(results) if results else 0
    return {
        "files": results,
        "total": len(results),
        "average_score": round(avg_score, 1),
        "timestamp": datetime.now().isoformat(),
    }


def print_quality_report(report: dict):
    print("=" * 60)
    print(f"📊 记忆质量报告（平均分: {report['average_score']}/100）")
    print("=" * 60)

    # 按分数排序
    sorted_files = sorted(report["files"], key=lambda x: x["score"])

    for r in sorted_files:
        score = r["score"]
        if score >= 80:
            icon = "🟢"
        elif score >= 60:
            icon = "🟡"
        else:
            icon = "🔴"

        print(f"\n{icon} {r['file']} — {score} 分")
        stats = r["stats"]
        print(f"   {stats['sessions']} sessions, {stats['user_messages']} 用户消息, "
              f"{'有' if stats['has_decisions'] else '无'}决策标记, "
              f"{'有' if stats['has_tags'] else '无'}标签")

        if r["issues"]:
            severity_icons = {"info": "ℹ️", "low": "⚠️", "medium": "🔶", "high": "🔴"}
            for issue in r["issues"][:5]:
                icon = severity_icons.get(issue["severity"], "❓")
                print(f"   {icon} [{issue['severity']}] {issue['desc']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆质量评分")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--file", "-f", default=None, help="分析单个文件")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.file:
        result = analyze_file(Path(args.file))
        if args.json:
            import json
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"📄 {result['file']} — {result['score']} 分")
            for issue in result["issues"]:
                print(f"  ⚠️ {issue['desc']}")
    else:
        report = analyze_all(md)
        if args.json:
            import json
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print_quality_report(report)
