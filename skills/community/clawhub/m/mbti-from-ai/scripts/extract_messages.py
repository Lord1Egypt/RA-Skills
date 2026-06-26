#!/usr/bin/env python3
"""
extract_user_messages.py — 从 OpenClaw JSONL 会话文件中提取用户消息
输入：_mbti_work/session_list.txt（每行一个文件路径）
输出：_mbti_work/user_messages.txt（每条消息之间用 --- 分隔）
"""

import json
import os
import re
import sys

WORK_DIR = "_mbti_work"
SESSION_LIST = os.path.join(WORK_DIR, "session_list.txt")
OUTPUT = os.path.join(WORK_DIR, "user_messages.txt")
MAX_MESSAGES = 10000


SYSTEM_PREFIXES = [
    'Pre-compaction memory flush',
    'Store durable memories only',
    'Current time:',
    'Treat workspace bootstrap',
    'Do NOT create timestamped',
]


def is_system_message(text: str) -> bool:
    """判断是否为 OpenClaw 系统自动插入的消息（非用户实际发言）"""
    for prefix in SYSTEM_PREFIXES:
        if text.startswith(prefix):
            return True
    # 检查是否是 memory flush 类的完整消息
    if 'memory flush' in text.lower() and 'MEMORY.md' in text:
        return True
    return False


def strip_openclaw_metadata(text: str) -> str:
    """
    去除 OpenClaw 用户消息中的元数据前缀，提取实际用户文本。
    
    OpenClaw 用户消息格式通常为：
    System: ...（系统信息）
    Sender (untrusted metadata):
    ```json
    { "label": "...", "id": "..." }
    ```
    [Wed 2026-03-18 15:44 GMT+8] 实际用户消息
    """
    # 去掉 System: 开头的行
    lines = text.split('\n')
    cleaned_lines = []
    skip_until_timestamp = False
    found_sender = False
    in_json_block = False

    for line in lines:
        stripped = line.strip()

        # 跳过 System: 开头的行
        if stripped.startswith('System:'):
            continue

        # 检测 Sender (untrusted metadata): 块
        if stripped.startswith('Sender (untrusted metadata)'):
            found_sender = True
            in_json_block = False
            continue

        # 如果在 Sender 块中，跳过 json 代码块
        if found_sender:
            if stripped == '```json' or stripped == '```':
                in_json_block = not in_json_block if stripped == '```json' else False
                continue
            if in_json_block:
                continue
            if stripped.startswith('{') or stripped.startswith('}'):
                continue

        # 尝试匹配时间戳行：[Wed 2026-03-18 15:44 GMT+8] 实际消息
        ts_match = re.match(
            r'^\[(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+\w+[+-]?\d*\]\s*(.*)',
            stripped
        )
        if ts_match:
            found_sender = False
            actual_text = ts_match.group(1)
            if actual_text:
                cleaned_lines.append(actual_text)
            continue

        # 普通行，如果已经过了 metadata 部分就保留
        if not found_sender and not in_json_block:
            cleaned_lines.append(line)

    result = '\n'.join(cleaned_lines).strip()
    return result


def extract_from_jsonl(filepath: str) -> list:
    """从 JSONL 文件中提取用户消息"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # OpenClaw 格式：type=message, message.role=user
                if obj.get('type') == 'message':
                    msg = obj.get('message', {})
                    if msg.get('role') == 'user':
                        content = msg.get('content', [])
                        texts = []
                        if isinstance(content, list):
                            for part in content:
                                if isinstance(part, dict) and part.get('type') == 'text':
                                    texts.append(part.get('text', ''))
                                elif isinstance(part, str):
                                    texts.append(part)
                        elif isinstance(content, str):
                            texts.append(content)

                        full_text = '\n'.join(texts).strip()
                        if full_text:
                            # 去除 OpenClaw 元数据前缀
                            cleaned = strip_openclaw_metadata(full_text)
                            if cleaned and len(cleaned) > 4:
                                # 过滤系统自动插入的消息
                                if not is_system_message(cleaned):
                                    messages.append(cleaned)
                    continue

                # 通用格式：直接有 role 字段
                role = obj.get('role', '')
                if role == 'user':
                    content = obj.get('content', obj.get('text', ''))
                    if isinstance(content, list):
                        parts = []
                        for p in content:
                            if isinstance(p, dict):
                                parts.append(p.get('text', ''))
                            elif isinstance(p, str):
                                parts.append(p)
                        content = '\n'.join(parts)
                    if isinstance(content, dict):
                        content = content.get('text', content.get('content', str(content)))
                    content = str(content).strip()
                    if content and len(content) > 4:
                        messages.append(content)

    except Exception as e:
        print(f"  ⚠️  读取失败 {filepath}: {e}", file=sys.stderr)
    return messages


def extract_from_json(filepath: str) -> list:
    """从完整 JSON 文件中提取用户消息"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        msg_list = []
        if isinstance(data, dict):
            msg_list = data.get('messages', data.get('conversation', []))
        elif isinstance(data, list):
            msg_list = data

        for msg in msg_list:
            if not isinstance(msg, dict):
                continue
            role = msg.get('role', msg.get('type', ''))
            if role != 'user':
                continue
            content = msg.get('content', msg.get('text', msg.get('message', '')))
            if isinstance(content, list):
                parts = []
                for p in content:
                    if isinstance(p, dict):
                        parts.append(p.get('text', ''))
                    elif isinstance(p, str):
                        parts.append(p)
                content = '\n'.join(parts)
            if isinstance(content, dict):
                content = content.get('text', content.get('content', str(content)))
            content = str(content).strip()
            if content and len(content) > 4:
                messages.append(content)

    except Exception as e:
        print(f"  ⚠️  读取失败 {filepath}: {e}", file=sys.stderr)
    return messages


def main():
    if not os.path.exists(SESSION_LIST):
        print(f"❌ 未找到会话列表文件: {SESSION_LIST}")
        print("   请先运行 discover-sessions.sh")
        sys.exit(1)

    with open(SESSION_LIST, 'r', encoding='utf-8') as f:
        filepaths = [line.strip() for line in f if line.strip()]

    if not filepaths:
        print("❌ 会话列表为空，无会话文件可处理")
        with open(OUTPUT, 'w', encoding='utf-8') as out:
            pass
        sys.exit(0)

    print(f"=== 提取用户消息 ===")
    print(f"   处理 {len(filepaths)} 个会话文件...")

    all_messages = []
    for filepath in filepaths:
        if not os.path.exists(filepath):
            print(f"  ⚠️  文件不存在: {filepath}")
            continue

        basename = os.path.basename(filepath)
        # OpenClaw 归档会话文件名格式：<uuid>.jsonl.reset.<timestamp>
        # 需要把 .jsonl.reset.* 也当作 JSONL 处理
        if '.jsonl' in basename:
            msgs = extract_from_jsonl(filepath)
        elif filepath.endswith('.json'):
            msgs = extract_from_json(filepath)
        else:
            continue

        print(f"  📄 {os.path.basename(filepath)}: {len(msgs)} 条用户消息")
        all_messages.extend(msgs)

        if len(all_messages) >= MAX_MESSAGES:
            print(f"⚠️  已达到最大消息数限制 ({MAX_MESSAGES})，停止提取")
            all_messages = all_messages[:MAX_MESSAGES]
            break

    # 写入输出文件
    with open(OUTPUT, 'w', encoding='utf-8') as out:
        for i, msg in enumerate(all_messages):
            out.write(msg + '\n')
            if i < len(all_messages) - 1:
                out.write('---\n')

    msg_count = len(all_messages)
    print(f"\n📊 提取到 {msg_count} 条用户消息")

    # 写入计数文件
    with open(os.path.join(WORK_DIR, "message_count.txt"), 'w') as f:
        f.write(str(msg_count))

    if msg_count < 10:
        print("⚠️  消息数量较少（< 10 条），分析置信度将标记为 low")

    print(f"📄 消息已保存到: {OUTPUT}")


if __name__ == '__main__':
    main()

