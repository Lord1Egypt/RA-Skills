#!/usr/bin/env python3
"""Hermes Memory Sync — parse session logs, write daily memory summaries.

Reads Hermes session JSON files and JSONL logs from the Hermes sessions directory,
extracts key conversations per day, and writes structured daily summaries to
workspace/memory/YYYY-MM-DD.md.
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import Optional

# ── Paths ────────────────────────────────────────────────────────────────────
HERMES_SESSIONS_DIR = Path(os.environ.get(
    'HERMES_SESSIONS_DIR',
    r'C:\Users\Administrator\AppData\Local\hermes\sessions'
))
OUTPUT_DIR = Path(os.environ.get(
    'MEMORY_OUTPUT_DIR',
    r'C:\Users\Administrator\workspace\memory'
))

# ── Helpers ──────────────────────────────────────────────────────────────────

def parse_timestamp(ts_str: str) -> Optional[datetime]:
    """Parse an ISO 8601 timestamp string to datetime."""
    if not ts_str:
        return None
    try:
        ts_str = ts_str.replace('Z', '+00:00')
        return datetime.fromisoformat(ts_str)
    except (ValueError, TypeError):
        return None


def extract_text_from_content(content) -> str:
    """Extract readable text from message content (string or list)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get('type') == 'text':
                texts.append(block.get('text', ''))
        return '\n'.join(texts)
    return str(content) if content else ''


def summarize_conversation(messages: list[dict]) -> dict:
    """Extract key info from a list of message dicts."""
    topics = set()
    decisions = []
    user_preferences = []
    tool_actions = []
    model_info = set()
    question_count = 0

    for i, msg in enumerate(messages):
        role = msg.get('role', '')
        content = extract_text_from_content(msg.get('content', ''))

        if role == 'user':
            # Count questions
            if '?' in content or '吗' in content[-3:]:
                question_count += 1
            # Extract potential topics (nouns/phrases from user messages)
            words = re.findall(r'[\u4e00-\u9fff\w]+', content[:200])
            for w in words:
                if len(w) >= 2:
                    topics.add(w)

        elif role == 'assistant':
            model = msg.get('model', '') or msg.get('finish_reason', '')
            if model:
                model_info.add(model)
            # Look for decision markers
            content_lower = content[:500].lower()
            if any(kw in content_lower for kw in ['决定', '选择', '采用', '建议', '推荐', '用']):
                decisions.append(content[:200])

        elif role == 'tool':
            tc = content[:300]
            if any(kw in tc for kw in ['preference', 'prefer', '喜欢', '想要']):
                user_preferences.append(tc[:150])
            tool_actions.append(tc[:100])

    return {
        'topics': sorted(topics, key=lambda t: -len(t))[:15],
        'decisions': decisions[:5],
        'user_preferences': user_preferences[:5],
        'tool_actions': tool_actions[:10],
        'question_count': question_count,
        'models': sorted(model_info),
    }


# ── Session Parsers ──────────────────────────────────────────────────────────

def parse_session_json(filepath: Path) -> list[dict]:
    """Parse a session_*.json file and return messages with timestamps."""
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    messages = data.get('messages', [])
    session_start = parse_timestamp(data.get('session_start', ''))
    platform = data.get('platform', 'unknown')
    model = data.get('model', 'unknown')

    enriched = []
    for i, msg in enumerate(messages):
        role = msg.get('role', '')
        content = msg.get('content', '')

        # Estimate timestamp from session start + message index
        if session_start:
            ts = session_start + timedelta(seconds=i * 30)
        else:
            ts = datetime.now()

        enriched.append({
            'role': role,
            'content': content,
            'timestamp': ts,
            'platform': platform,
            'model': model,
            'session_id': data.get('session_id', filepath.stem),
        })

    return enriched


def parse_session_jsonl(filepath: Path) -> list[dict]:
    """Parse a YYYYMMDD_HHMMSS_*.jsonl file and return messages with timestamps."""
    messages = []
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            role = record.get('role', '')
            content = record.get('content', '')
            ts_str = record.get('timestamp', '')
            timestamp = parse_timestamp(ts_str)
            if not timestamp:
                timestamp = datetime.now()

            messages.append({
                'role': role,
                'content': content,
                'timestamp': timestamp,
                'platform': record.get('platform', ''),
                'model': record.get('model', ''),
                'session_id': filepath.stem,
            })

    return messages


def load_all_messages() -> dict[date, list[dict]]:
    """Load all messages from all session files, grouped by date."""
    grouped: dict[date, list[dict]] = defaultdict(list)

    # 1. Parse session_*.json files (full session records)
    for f in sorted(HERMES_SESSIONS_DIR.glob('session_*.json')):
        try:
            msgs = parse_session_json(f)
            for msg in msgs:
                msg_date = msg['timestamp'].date()
                grouped[msg_date].append(msg)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  [warn] Skipping {f.name}: {e}", file=sys.stderr)

    # 2. Parse YYYYMMDD_*.jsonl files (detailed per-message logs)
    for f in sorted(HERMES_SESSIONS_DIR.glob('[0-9]*.jsonl')):
        try:
            msgs = parse_session_jsonl(f)
            for msg in msgs:
                msg_date = msg['timestamp'].date()
                grouped[msg_date].append(msg)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  [warn] Skipping {f.name}: {e}", file=sys.stderr)

    return dict(grouped)


# ── Memory File Generation ──────────────────────────────────────────────────

def generate_memory_file(target_date: date, messages: list[dict], output_dir: Path):
    """Write a structured daily memory summary to output_dir/YYYY-MM-DD.md."""
    messages.sort(key=lambda m: m['timestamp'])

    # Skip days with only system/meta messages
    user_msgs = [m for m in messages if m['role'] == 'user']
    if not user_msgs:
        return None

    output_path = output_dir / f"{target_date}.md"
    summary = summarize_conversation(messages)

    # Build the markdown content
    lines = []
    lines.append(f"# 📅 {target_date}\n")

    # Metadata
    total_msgs = len(messages)
    asst_msgs = len([m for m in messages if m['role'] == 'assistant'])
    tool_msgs = len([m for m in messages if m['role'] == 'tool'])
    models = set(m.get('model', '') for m in messages if m.get('model'))
    sessions = set(m.get('session_id', '') for m in messages)

    lines.append(f"**会话数:** {len(sessions)} | **消息总数:** {total_msgs}")
    lines.append(f"**用户提问:** {summary['question_count']} | **助手回复:** {asst_msgs} | **工具调用:** {tool_msgs}")
    if models:
        lines.append(f"**使用的模型:** {', '.join(sorted(models))}")
    lines.append("")

    # Topics
    if summary['topics']:
        lines.append("## 🎯 讨论主题")
        for topic in summary['topics'][:10]:
            lines.append(f"- {topic}")
        lines.append("")

    # Key exchanges (first few user questions and assistant responses)
    lines.append("## 💬 关键对话\n")
    exchange_count = 0
    for i, msg in enumerate(messages):
        if exchange_count >= 5:
            break
        if msg['role'] == 'user':
            content = extract_text_from_content(msg['content'])[:300]
            lines.append(f"**Q:** {content}")
            # Find the next assistant response
            for j in range(i + 1, min(i + 5, len(messages))):
                if messages[j]['role'] == 'assistant':
                    resp = extract_text_from_content(messages[j]['content'])[:400]
                    lines.append(f"> **A:** {resp}\n")
                    exchange_count += 1
                    break

    # Decisions
    if summary['decisions']:
        lines.append("## ⚡ 决策/方案")
        for d in summary['decisions']:
            lines.append(f"- {d}")
        lines.append("")

    # Tool actions summary
    if summary['tool_actions']:
        lines.append("## 🛠️ 工具使用")
        for t in summary['tool_actions'][:5]:
            lines.append(f"- {t}")
        lines.append("")

    # Auto-generated marker
    lines.append("---")
    lines.append(f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}，来自 {len(sessions)} 个会话*")
    lines.append("")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return str(output_path)


# ── CLI ──────────────────────────────────────────────────────────────────────

def cmd_compare():
    """Compare sessions vs existing memory files, show gaps."""
    grouped = load_all_messages()
    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    existing = {f.stem for f in output_dir.glob('*.md') if f.stem.count('-') == 2}

    print(f"会话目录: {HERMES_SESSIONS_DIR}")
    print(f"记忆目录: {output_dir}")
    print(f"")

    dates = sorted(grouped.keys())
    if not dates:
        print("未找到任何会话数据。")
        return

    print(f"覆盖日期范围: {dates[0]} ~ {dates[-1]} ({len(dates)} 天)")
    print("")

    gaps = []
    covered = []
    for d in dates:
        date_str = d.isoformat()
        user_count = len([m for m in grouped[d] if m['role'] == 'user'])
        msg_count = len(grouped[d])

        if date_str in existing:
            covered.append(d)
        else:
            gaps.append((d, msg_count, user_count))

    if covered:
        print(f"✅ 已有记忆文件: {len(covered)} 天")
        for d in covered[-5:]:
            print(f"   {d}")
        if len(covered) > 5:
            print(f"   ... 共 {len(covered)} 天")

    if gaps:
        print(f"\n⚠️  缺失记忆: {len(gaps)} 天")
        for d, total, user in gaps[-10:]:
            print(f"   {d} — {total} 条消息 ({user} 条用户)")
        if len(gaps) > 10:
            print(f"   ... 共 {len(gaps)} 天")
        print(f"\n👉 运行: python {__file__} backfill --all")
    else:
        if covered:
            print(f"\n✅ 全部覆盖，无需回填。")


def cmd_backfill(target: str):
    """Backfill memory files for specific dates."""
    grouped = load_all_messages()
    dates = sorted(grouped.keys())

    if target == 'all':
        to_process = dates
    elif target == 'today':
        to_process = [datetime.now().date()]
    else:
        try:
            to_process = [date.fromisoformat(target)]
        except ValueError:
            print(f"错误: 日期格式无效 '{target}'，请使用 YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    created = []
    skipped = []
    for d in to_process:
        if d not in grouped:
            print(f"  跳过 {d}: 无会话数据")
            continue
        result = generate_memory_file(d, grouped[d], OUTPUT_DIR)
        if result:
            created.append(result)
            print(f"  ✅ {result}")
        else:
            skipped.append(d)

    print(f"\n✅ 创建 {len(created)} 个记忆文件")
    if skipped:
        print(f"⏭️  跳过 {len(skipped)} 天（无用户消息）")


def cmd_stats():
    """Show high-level stats about sessions and memory."""
    grouped = load_all_messages()
    output_dir = OUTPUT_DIR

    total_msgs = sum(len(v) for v in grouped.values())
    total_sessions = len(set(
        m['session_id'] for msgs in grouped.values() for m in msgs
    ))
    user_msgs = sum(
        len([m for m in msgs if m['role'] == 'user'])
        for msgs in grouped.values()
    )

    print(f"会话日志路径: {HERMES_SESSIONS_DIR}")
    print(f"记忆文件路径: {output_dir}")
    print(f"")
    print(f"📊 统计")
    print(f"  活跃天数: {len(grouped)}")
    print(f"  总消息数: {total_msgs}")
    print(f"  用户消息: {user_msgs}")
    print(f"  会话数:   {total_sessions}")
    print(f"")
    existing = list(output_dir.glob('*.md'))
    print(f"📁 已有记忆文件: {len(existing)}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Hermes Memory Sync')
    parser.add_argument('command', nargs='?', default='compare',
                        choices=['compare', 'backfill', 'stats'],
                        help='操作: compare (默认), backfill, stats')
    parser.add_argument('target', nargs='?', default=None,
                        help='backfill 目标: all, today, YYYY-MM-DD')

    args = parser.parse_args()

    if args.command == 'compare':
        cmd_compare()
    elif args.command == 'backfill':
        target = args.target or 'today'
        cmd_backfill(target)
    elif args.command == 'stats':
        cmd_stats()
