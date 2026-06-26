#!/usr/bin/env python3
"""记忆矛盾检测：发现前后矛盾的记录（偏好变化、决策冲突）"""

import argparse
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


# 偏好矛盾模式：喜欢X vs 不喜欢X
PREFERENCE_PATTERNS = [
    (r'(?:喜欢|爱|偏好|习惯|要用|以后都)(.{1,20})', "positive"),
    (r'(?:不喜欢|讨厌|反感|不要|别用|以后别)(.{1,20})', "negative"),
]

# 决策矛盾模式
DECISION_PATTERNS = [
    r'(?:决定|确定|拍板|选[择定]|用[这个那个])(.{1,30})',
    r'(?:换成|改为|改成|切换到)(.{1,30})',
]


def load_all_conversations(memory_dir: Path) -> list[dict]:
    """加载所有对话记录"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return []

    records = []
    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        records.append({
            "date": fp.stem,
            "content": content,
            "path": str(fp),
        })
    return records


def detect_preference_contradictions(records: list[dict]) -> list[dict]:
    """检测偏好矛盾"""
    preferences = defaultdict(list)

    for rec in records:
        user_msgs = re.findall(r'\*\*用户[：:]\*\*\s*(.+)', rec["content"])
        for msg in user_msgs:
            for pattern, polarity in PREFERENCE_PATTERNS:
                matches = re.findall(pattern, msg)
                for m in matches:
                    # 提取关键对象（去掉常见虚词）
                    obj = re.sub(r'^[了的是个把那些]', '', m.strip())
                    if len(obj) >= 2:
                        preferences[obj].append({
                            "polarity": polarity,
                            "date": rec["date"],
                            "message": msg.strip()[:80],
                        })

    contradictions = []
    for obj, entries in preferences.items():
        polarities = set(e["polarity"] for e in entries)
        if len(polarities) > 1:
            contradictions.append({
                "type": "偏好矛盾",
                "object": obj,
                "details": sorted(entries, key=lambda x: x["date"]),
            })

    return contradictions


def detect_decision_contradictions(records: list[dict]) -> list[dict]:
    """检测决策矛盾"""
    decisions = defaultdict(list)

    for rec in records:
        content = rec["content"]
        for pattern in DECISION_PATTERNS:
            matches = re.findall(pattern, content)
            for m in matches:
                clean = m.strip().rstrip("。")
                if len(clean) >= 3:
                    decisions[clean].append(rec["date"])

    # 查找包含"换成/改为"的，看是否有对应的早期决策
    contradictions = []
    for content, dates in decisions.items():
        change_match = re.match(r'(?:换成|改为|改成|切换到)(.+)', content)
        if change_match:
            new_thing = change_match.group(1).strip()
            # 看看之前是否有不同的决策
            for other_content, other_dates in decisions.items():
                if other_content != content and new_thing not in other_content:
                    if other_dates[0] < dates[-1]:
                        contradictions.append({
                            "type": "决策变更",
                            "from": other_content,
                            "to": content,
                            "from_date": other_dates[0],
                            "to_date": dates[-1],
                        })

    return contradictions


def detect_todo_inconsistencies(records: list[dict]) -> list[dict]:
    """检测待办一致性：标记完成但后面又出现的"""
    todos = defaultdict(list)

    for rec in records:
        for line in rec["content"].split("\n"):
            line = line.strip()
            if line.startswith("- [ ] "):
                todos[line[6:].strip()].append({"date": rec["date"], "status": "open"})
            elif line.startswith("- [x] ") or line.startswith("- [X] "):
                todos[line[6:].strip()].append({"date": rec["date"], "status": "done"})

    inconsistencies = []
    for todo, entries in todos.items():
        statuses = [e["status"] for e in entries]
        # 完成后又打开
        if "done" in statuses and "open" in statuses:
            sorted_entries = sorted(entries, key=lambda x: x["date"])
            inconsistencies.append({
                "type": "待办反复",
                "todo": todo,
                "details": sorted_entries,
            })

    return inconsistencies


def print_contradictions(preferences: list, decisions: list, todos: list):
    all_issues = []
    all_issues.extend([{"severity": "⚠️", **p} for p in preferences])
    all_issues.extend([{"severity": "🔄", **d} for d in decisions])
    all_issues.extend([{"severity": "📋", **t} for t in todos])

    if not all_issues:
        print("✅ 未发现记忆矛盾，一切一致")
        return

    print("=" * 60)
    print(f"🔍 记忆矛盾检测（发现 {len(all_issues)} 个潜在问题）")
    print("=" * 60)

    for issue in all_issues:
        sev = issue["severity"]
        if issue["type"] == "偏好矛盾":
            print(f"\n{sev} 偏好矛盾：{issue['object']}")
            for d in issue["details"]:
                polarity = "✅ 喜欢" if d["polarity"] == "positive" else "❌ 不喜欢"
                print(f"   [{d['date']}] {polarity} — {d['message']}")

        elif issue["type"] == "决策变更":
            print(f"\n{sev} 决策变更：")
            print(f"   [{issue['from_date']}] {issue['from']}")
            print(f"   [{issue['to_date']}] {issue['to']}")

        elif issue["type"] == "待办反复":
            print(f"\n{sev} 待办反复：{issue['todo']}")
            for d in issue["details"]:
                icon = "🟢" if d["status"] == "done" else "🔴"
                print(f"   [{d['date']}] {icon} {d['status']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆矛盾检测")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    records = load_all_conversations(md)
    if not records:
        print("📭 没有对话记录")
        exit(0)

    prefs = detect_preference_contradictions(records)
    decs = detect_decision_contradictions(records)
    todos = detect_todo_inconsistencies(records)

    if args.json:
        import json
        print(json.dumps({"preferences": prefs, "decisions": decs, "todos": todos},
                         ensure_ascii=False, indent=2))
    else:
        print_contradictions(prefs, decs, todos)
