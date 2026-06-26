#!/usr/bin/env python3
"""捕获 OpenClaw session 历史并自动归档"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# OpenClaw session 存储路径
SESSIONS_DIR = Path.home() / ".openclaw" / "sessions"


def detect_topic(messages: list[dict]) -> str:
    """根据前几轮对话推断话题"""
    user_msgs = [m for m in messages if m.get("role") == "user"]
    if not user_msgs:
        return "未知话题"
    first = user_msgs[0].get("content", "")
    # 取第一句话的前 40 字符
    first_line = first.split("\n")[0].strip()
    # 去掉元数据标记
    first_line = re.sub(r'^\[[\w\-\s]+\]\s*', '', first_line)
    return first_line[:40] + ("..." if len(first_line) > 40 else "")


def detect_tags(messages: list[dict]) -> list[str]:
    """根据对话内容自动打标签"""
    text = " ".join(m.get("content", "") for m in messages)
    tags = []
    tag_rules = {
        "skill": ["skill", "技能包", "SKILL"],
        "小说": ["小说", "novel", "写作", "章节", "读者"],
        "决策": ["决定", "拍板", "确定了", "方案确定", "就用这个"],
        "待办": ["待办", "todo", "记得", "别忘了", "回头"],
        "代码": ["代码", "script", "脚本", "python", "git", "bug"],
        "赚钱": ["赚钱", "收入", "商业化", "付费", "卖"],
        "部署": ["部署", "deploy", "发布", "上线", "push"],
    }
    for tag, keywords in tag_rules.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    return tags or ["日常"]


def format_conversation(messages: list[dict]) -> str:
    """将 session 消息格式化为归档格式"""
    lines = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if not content or not isinstance(content, str):
            continue
        # 跳过系统消息
        if role == "system":
            continue
        # 清理元数据
        clean = re.sub(r'```json\s*\{[^}]*"schema":\s*"openclaw\.inbound_meta[^`]*```', '', content, flags=re.DOTALL)
        clean = re.sub(r'\[Sat \d{4}-\d{2}-\d{2} \d{2}:\d{2} GMT\+8\]', '', clean)
        clean = clean.strip()
        if not clean:
            continue

        label = {"user": "用户", "assistant": "助手"}.get(role, role)
        lines.append(f"**{label}：** {clean}\n")
    return "\n".join(lines)


def find_session_files(session_id: str | None) -> list[Path]:
    """查找 session 文件"""
    if not SESSIONS_DIR.exists():
        return []
    if session_id:
        # 精确匹配
        matches = list(SESSIONS_DIR.glob(f"*{session_id}*"))
        return matches
    # 返回最近的几个 session
    files = sorted(SESSIONS_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    return files[:3]


def capture_session(session_id: str | None, memory_dir: Path, auto: bool = False):
    """捕获 session 并归档"""
    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = conv_dir / f"{date_str}.md"

    session_files = find_session_files(session_id)
    if not session_files:
        print("⚠️ 未找到 session 文件")
        print(f"  查找路径: {SESSIONS_DIR}")
        print("  提示: 确认 OpenClaw session 存储路径是否正确")
        return

    all_entries = []
    for sf in session_files:
        try:
            data = json.loads(sf.read_text(encoding="utf-8"))
            messages = data if isinstance(data, list) else data.get("messages", data.get("conversation", []))
        except (json.JSONDecodeError, AttributeError):
            continue

        if not messages:
            continue

        topic = detect_topic(messages)
        tags = detect_tags(messages)
        formatted = format_conversation(messages)
        now = datetime.now().strftime("%H:%M")

        entry = f"\n## [{now}] Session: {sf.stem}\n### 话题：{topic}\n"
        entry += f"**标签：** {', '.join(tags)}\n\n"
        entry += formatted
        all_entries.append(entry)

    if not all_entries:
        print("⚠️ 未提取到有效对话内容")
        return

    full_content = f"# {date_str} 对话记录\n" + "\n".join(all_entries)
    if filepath.exists():
        filepath.write_text(full_content, encoding="utf-8")
    else:
        filepath.write_text(full_content, encoding="utf-8")

    print(f"✅ 已捕获 {len(all_entries)} 个 session → {filepath}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="捕获 OpenClaw session 历史并归档")
    p.add_argument("--session", "-s", default=None, help="Session ID（不指定则捕获最近的）")
    p.add_argument("--memory-dir", default=None, help="记忆目录路径")
    p.add_argument("--auto", "-a", action="store_true", help="自动模式（配合 cron 使用）")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    md.mkdir(parents=True, exist_ok=True)
    capture_session(args.session, md, args.auto)
