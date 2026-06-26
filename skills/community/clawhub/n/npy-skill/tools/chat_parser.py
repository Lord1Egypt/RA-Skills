#!/usr/bin/env python3
"""
聊天记录解析工具
支持：
- 微信 MSG*.db 解析（解密后的 SQLite 数据库）
- iMessage chat.db 解析（macOS）
- 文本聊天记录文件解析

用于从聊天记录中提取信息，辅助 persona.md 创建。

用法：
# 列出微信联系人
python chat_parser.py --list-contacts --db "./decrypted/MicroMsg.db"

# 提取与某人的微信聊天记录
python chat_parser.py --extract --db-dir "./decrypted/" --target "TA的微信名"

# 提取 iMessage 聊天记录
python chat_parser.py --imessage --db "~/Library/Messages/chat.db" --target "手机号或Apple ID"

# 解析导出的聊天文本文件
python chat_parser.py --parse-file "./chats.txt"

# 分类聊天记录
python chat_parser.py --classify --db-dir "./decrypted/" --target "TA的微信名"
"""

import os
import re
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

# Apple epoch 偏移量（2001-01-01 00:00:00 UTC）
APPLE_EPOCH_OFFSET = 978307200


def list_wechat_contacts(db_path: str) -> list[dict]:
    """列出微信数据库中的所有联系人

    Args:
        db_path: MicroMsg.db 文件路径

    Returns:
        联系人列表，每个联系人包含 wxid, nickname, remark
    """
    contacts = []

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # MicroMsg.db 中的联系人表结构
        cursor.execute("""
            SELECT UsrName, NickName, Remark, Alias
            FROM Contact
            WHERE Type = 3 AND VerifyFlag = 0
        """)

        for row in cursor.fetchall():
            wxid = row[0] or ""
            nickname = row[1] or ""
            remark = row[2] or ""
            alias = row[3] or ""

            # 显示名优先用备注名，其次昵称
            display_name = remark or nickname or alias or wxid

            contacts.append({
                "wxid": wxid,
                "nickname": nickname,
                "remark": remark,
                "alias": alias,
                "display_name": display_name,
            })

        conn.close()

    except sqlite3.Error as e:
        print(f"数据库读取错误：{e}", file=__import__("sys").stderr)
        return []

    # 按显示名排序
    contacts.sort(key=lambda x: x["display_name"])
    return contacts


def extract_wechat_messages(db_dir: str, target_name: str) -> list[dict]:
    """提取与指定联系人的微信聊天记录

    Args:
        db_dir: 解密后的数据库目录（包含 MSG*.db 和 MicroMsg.db）
        target_name: 目标联系人的微信名/备注名

    Returns:
        消息列表，每条消息包含 timestamp, sender, content, type
    """
    messages = []
    db_dir = Path(db_dir)

    # 1. 从 MicroMsg.db 找到目标的 wxid
    micro_db = db_dir / "MicroMsg.db"
    if not micro_db.exists():
        # 递归查找
        micro_db = next(db_dir.glob("**/MicroMsg.db"), None)
        if not micro_db:
            print("错误：未找到 MicroMsg.db", file=__import__("sys").stderr)
            return []

    contacts = list_wechat_contacts(str(micro_db))
    target_contact = None

    # 匹配联系人（支持部分匹配）
    for c in contacts:
        if (
            c["display_name"] == target_name
            or c["nickname"] == target_name
            or c["remark"] == target_name
            or c["wxid"] == target_name
            or target_name in c["display_name"]
            or target_name in c["nickname"]
        ):
            target_contact = c
            break

    if not target_contact:
        print(f"错误：未找到联系人 '{target_name}'", file=__import__("sys").stderr)
        print("可用的联系人：")
        for c in contacts[:20]:
            print(f"  - {c['display_name']}")
        return []

    wxid = target_contact["wxid"]
    print(f"找到联系人：{target_contact['display_name']} ({wxid})")

    # 2. 从 MSG*.db 提取消息
    msg_db_files = list(db_dir.glob("**/MSG*.db"))
    if not msg_db_files:
        msg_db_files = list(db_dir.glob("**/msg_*.db"))

    if not msg_db_files:
        print("错误：未找到 MSG*.db 文件", file=__import__("sys").stderr)
        return []

    for msg_db in msg_db_files:
        try:
            conn = sqlite3.connect(str(msg_db))
            cursor = conn.cursor()

            # MSG 表结构
            cursor.execute("""
                SELECT CreateTime, Type, StrContent, BytesContent, TalkerId
                FROM MSG
                WHERE TalkerId = ? OR StrContent LIKE ?
                ORDER BY CreateTime ASC
            """, (wxid, f"%{wxid}%"))

            for row in cursor.fetchall():
                timestamp_raw = row[0] or 0
                msg_type = row[1] or 0
                str_content = row[2] or ""
                bytes_content = row[3]

                # 时间戳转换
                try:
                    timestamp = datetime.fromtimestamp(timestamp_raw / 1000)
                except (ValueError, OSError):
                    timestamp = datetime.min

                # 内容解码
                content = str_content
                if not content and bytes_content:
                    try:
                        content = bytes_content.decode("utf-8", errors="ignore")
                    except Exception:
                        content = str(bytes_content)

                # 消息类型：1=文本, 3=图片, 34=语音, 43=视频, 47=表情, 48=位置
                type_name = {
                    1: "文本",
                    3: "图片",
                    34: "语音",
                    43: "视频",
                    47: "表情",
                    48: "位置",
                    49: "文件/链接",
                    50: "视频通话",
                    10000: "系统消息",
                }.get(msg_type, f"类型{msg_type}")

                # 判断发送者
                # 微信消息中，TalkerId 是对方的 wxid
                # 如果 BytesContent 开头有特定标记，可能是对方发的
                sender = "我" if msg_type == 1 and str_content else target_contact["display_name"]

                messages.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "content": content,
                    "type": type_name,
                    "raw_type": msg_type,
                })

            conn.close()

        except sqlite3.Error as e:
            print(f"读取 {msg_db} 出错：{e}", file=__import__("sys").stderr)
            continue

    # 按时间排序
    messages.sort(key=lambda x: x["timestamp"])
    return messages


def extract_imessage_messages(db_path: str, target_identifier: str) -> list[dict]:
    """提取 iMessage 聊天记录

    Args:
        db_path: chat.db 文件路径（~/Library/Messages/chat.db）
        target_identifier: 目标联系人（手机号或 Apple ID）

    Returns:
        消息列表
    """
    messages = []
    db_path = Path(db_path).expanduser()

    if not db_path.exists():
        print(f"错误：未找到 iMessage 数据库 {db_path}", file=__import__("sys").stderr)
        return []

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 查找目标联系人
        cursor.execute("""
            SELECT ROWID, id
            FROM handle
            WHERE id LIKE ?
        """, (f"%{target_identifier}%"))

        handle_rows = cursor.fetchall()
        if not handle_rows:
            print(f"错误：未找到联系人 '{target_identifier}'", file=__import__("sys").stderr)
            return []

        handle_ids = [row[0] for row in handle_rows]
        display_name = handle_rows[0][1] if handle_rows else target_identifier

        # 提取消息
        cursor.execute("""
            SELECT m.date, m.text, m.handle_id, m.is_from_me, m.cache_has_attachments
            FROM message m
            WHERE m.handle_id IN ({})
            ORDER BY m.date ASC
        """.format(",".join(map(str, handle_ids))))

        for row in cursor.fetchall():
            date_raw = row[0] or 0
            text = row[1] or ""
            handle_id = row[2]
            is_from_me = row[3] or 0
            has_attachment = row[4] or 0

            # Apple epoch 转换
            try:
                timestamp = datetime.fromtimestamp(date_raw / 1e9 + APPLE_EPOCH_OFFSET)
            except (ValueError, OSError):
                timestamp = datetime.min

            sender = "我" if is_from_me else display_name
            type_name = "附件" if has_attachment else "文本"

            messages.append({
                "timestamp": timestamp,
                "sender": sender,
                "content": text,
                "type": type_name,
            })

        conn.close()

    except sqlite3.Error as e:
        print(f"数据库读取错误：{e}", file=__import__("sys").stderr)
        return []

    messages.sort(key=lambda x: x["timestamp"])
    return messages


def classify_messages(messages: list[dict]) -> dict:
    """将聊天记录分类为不同类型的对话

    Args:
        messages: 消息列表

    Returns:
        分类结果，包含：
        - long_conversations: 长对话（连续多轮）
        - conflicts: 冲突对话（争吵、冷战）
        - sweet_moments: 甜蜜时刻（表白、关心）
        - daily_chats: 日常聊天
    """
    result = {
        "long_conversations": [],
        "conflicts": [],
        "sweet_moments": [],
        "daily_chats": [],
    }

    if not messages:
        return result

    # 冲突关键词
    conflict_keywords = [
        "生气", "吵架", "冷战", "不理", "滚", "烦", "讨厌",
        "为什么不", "怎么不", "你总是", "你每次",
        "分手", "算了", "随便", "不想说了",
        "无所谓", "随便你", "你爱怎么样就怎么样",
    ]

    # 甜蜜关键词
    sweet_keywords = [
        "爱你", "想你", "喜欢", "宝贝", "亲爱的", "抱抱",
        "亲亲", "么么", "嘻嘻", "嘿嘿", "哈", "好的呀",
        "没事的", "我在", "别怕", "乖", "爱你哦",
        "喜欢你", "想你啦", "抱你", "心疼", "关心",
        "放心", "我会", "我陪你", "别难过", "开心",
    ]

    # 检测长对话（连续 5+ 条消息）
    conversation_chunks = []
    current_chunk = []
    prev_time = None

    for msg in messages:
        if prev_time and msg["timestamp"]:
            # 间隔超过 30 分钟视为对话中断
            diff = (msg["timestamp"] - prev_time).total_seconds()
            if diff > 1800:
                if len(current_chunk) >= 5:
                    conversation_chunks.append(current_chunk)
                current_chunk = []

        current_chunk.append(msg)
        prev_time = msg["timestamp"] if msg["timestamp"] else prev_time

    # 最后一块
    if len(current_chunk) >= 5:
        conversation_chunks.append(current_chunk)

    # 分类每个对话块
    for chunk in conversation_chunks:
        chunk_text = " ".join([m["content"] for m in chunk if m["content"]])

        # 判断类型
        is_conflict = any(kw in chunk_text for kw in conflict_keywords)
        is_sweet = any(kw in chunk_text for kw in sweet_keywords)

        if is_conflict:
            result["conflicts"].append(chunk)
        elif is_sweet:
            result["sweet_moments"].append(chunk)
        else:
            result["daily_chats"].append(chunk)

    # 长对话（超过 10 条消息）
    for chunk in conversation_chunks:
        if len(chunk) >= 10:
            result["long_conversations"].append(chunk)

    return result


def parse_chat_file(file_path: str) -> list[dict]:
    """解析导出的聊天文本文件

    支持格式：
    - 时间 发送者 内容
    - [时间] 发送者: 内容
    - 发送者 时间 内容
    - 微信导出格式

    Args:
        file_path: 聊天记录文件路径

    Returns:
        消息列表
    """
    messages = []
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"错误：文件不存在 {file_path}", file=__import__("sys").stderr)
        return []

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")

    # 尝试多种解析模式
    patterns = [
        # [2024-01-01 12:00] 张三: 你好
        r"\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\]\s+([^:]+):\s+(.+)",
        # 2024-01-01 12:00 张三 你好
        r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+(\S+)\s+(.+)",
        # 张三 2024/1/1 12:00: 你好
        r"(\S+)\s+(\d{4}/\d{1,2}/\d{1,2}\s+\d{2}:\d{2}):\s+(.+)",
        # 微信导出格式
        r"(\S+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)",
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        matched = False
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                groups = match.groups()

                # 根据模式确定时间、发送者、内容
                timestamp_str = ""
                sender = ""
                content_text = ""

                if pattern == patterns[0]:
                    timestamp_str, sender, content_text = groups
                elif pattern == patterns[1]:
                    timestamp_str, sender, content_text = groups
                elif pattern == patterns[2]:
                    sender, timestamp_str, content_text = groups
                elif pattern == patterns[3]:
                    sender, timestamp_str, content_text = groups

                # 解析时间
                try:
                    # 尝试多种时间格式
                    for fmt in [
                        "%Y-%m-%d %H:%M",
                        "%Y-%m-%d %H:%M:%S",
                        "%Y/%m/%d %H:%M",
                    ]:
                        try:
                            timestamp = datetime.strptime(timestamp_str.strip(), fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        timestamp = datetime.min
                except Exception:
                    timestamp = datetime.min

                messages.append({
                    "timestamp": timestamp,
                    "sender": sender.strip(),
                    "content": content_text.strip(),
                    "type": "文本",
                })

                matched = True
                break

        # 如果没匹配到模式，作为纯文本内容处理
        if not matched and line:
            # 尝试检测发送者（开头是名字）
            parts = line.split(None, 2)
            if len(parts) >= 2:
                possible_sender = parts[0]
                possible_content = " ".join(parts[1:])
                messages.append({
                    "timestamp": datetime.min,
                    "sender": possible_sender,
                    "content": possible_content,
                    "type": "文本",
                })

    messages.sort(key=lambda x: x["timestamp"] if x["timestamp"] else datetime.min)
    return messages


def format_messages_for_output(messages: list[dict], max_lines: int = 100) -> str:
    """格式化消息列表用于输出

    Args:
        messages: 消息列表
        max_lines: 最大输出行数

    Returns:
        格式化后的文本
    """
    if not messages:
        return "暂无消息记录"

    output_lines = []
    output_lines.append(f"共 {len(messages)} 条消息\n")
    output_lines.append("=" * 60 + "\n")

    # 只输出最近的 max_lines 条
    display_messages = messages[-max_lines:] if len(messages) > max_lines else messages

    for msg in display_messages:
        ts = msg["timestamp"].strftime("%Y-%m-%d %H:%M") if msg["timestamp"] else "未知时间"
        sender = msg["sender"]
        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]

        output_lines.append(f"[{ts}] {sender}: {content}\n")

    return "".join(output_lines)


def format_classification_summary(classification: dict) -> str:
    """格式化分类结果摘要

    Args:
        classification: 分类结果

    Returns:
        格式化后的摘要文本
    """
    lines = []
    lines.append("聊天记录分类摘要\n")
    lines.append("=" * 60 + "\n")

    lines.append(f"长对话（≥10条连续消息）: {len(classification['long_conversations'])} 个\n")
    lines.append(f"冲突对话: {len(classification['conflicts'])} 个\n")
    lines.append(f"甜蜜时刻: {len(classification['sweet_moments'])} 个\n")
    lines.append(f"日常聊天: {len(classification['daily_chats'])} 个\n")

    # 输出甜蜜时刻示例
    if classification["sweet_moments"]:
        lines.append("\n--- 甜蜜时刻示例 ---\n")
        for i, chunk in enumerate(classification["sweet_moments"][:3]):
            lines.append(f"\n示例 {i+1}:\n")
            for msg in chunk[:5]:
                ts = msg["timestamp"].strftime("%H:%M") if msg["timestamp"] else "?"
                lines.append(f"  [{ts}] {msg['sender']}: {msg['content'][:50]}\n")

    # 输出冲突对话示例
    if classification["conflicts"]:
        lines.append("\n--- 冲突对话示例 ---\n")
        for i, chunk in enumerate(classification["conflicts"][:2]):
            lines.append(f"\n示例 {i+1}:\n")
            for msg in chunk[:5]:
                ts = msg["timestamp"].strftime("%H:%M") if msg["timestamp"] else "?"
                lines.append(f"  [{ts}] {msg['sender']}: {msg['content'][:50]}\n")

    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="聊天记录解析工具（用于 npy-skill）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
# 列出微信联系人
python chat_parser.py --list-contacts --db "./decrypted/MicroMsg.db"

# 提取与某人的微信聊天记录
python chat_parser.py --extract --db-dir "./decrypted/" --target "TA的微信名"

# 提取 iMessage 聊天记录
python chat_parser.py --imessage --db "~/Library/Messages/chat.db" --target "手机号"

# 解析导出的文本文件
python chat_parser.py --parse-file "./chats.txt"

# 分类聊天记录
python chat_parser.py --classify --db-dir "./decrypted/" --target "TA的微信名"
""",
    )

    parser.add_argument("--list-contacts", action="store_true", help="列出微信联系人")
    parser.add_argument("--extract", action="store_true", help="提取聊天记录")
    parser.add_argument("--classify", action="store_true", help="分类聊天记录")
    parser.add_argument("--imessage", action="store_true", help="提取 iMessage 记录")
    parser.add_argument("--parse-file", action="store_true", help="解析文本聊天文件")

    parser.add_argument("--db", help="数据库文件路径")
    parser.add_argument("--db-dir", help="数据库目录路径")
    parser.add_argument("--target", help="目标联系人（微信名/备注名/手机号）")
    parser.add_argument("--file", help="聊天文本文件路径")
    parser.add_argument("--output", default="./messages.txt", help="输出文件路径")

    args = parser.parse_args()

    if args.list_contacts:
        if not args.db:
            print("错误：需要指定 --db", file=__import__("sys").stderr)
            return

        contacts = list_wechat_contacts(args.db)
        if contacts:
            print(f"\n找到 {len(contacts)} 个联系人:\n")
            for c in contacts:
                remark_str = f" (备注: {c['remark']})" if c['remark'] else ""
                print(f"  {c['display_name']}{remark_str} [{c['wxid']}]")

    elif args.extract:
        if not args.db_dir or not args.target:
            print("错误：需要指定 --db-dir 和 --target", file=__import__("sys").stderr)
            return

        messages = extract_wechat_messages(args.db_dir, args.target)
        output = format_messages_for_output(messages)

        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n已提取 {len(messages)} 条消息")
        print(f"输出到：{args.output}")

    elif args.imessage:
        if not args.db or not args.target:
            print("错误：需要指定 --db 和 --target", file=__import__("sys").stderr)
            return

        messages = extract_imessage_messages(args.db, args.target)
        output = format_messages_for_output(messages)

        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n已提取 {len(messages)} 条 iMessage 消息")
        print(f"输出到：{args.output}")

    elif args.parse_file:
        if not args.file:
            print("错误：需要指定 --file", file=__import__("sys").stderr)
            return

        messages = parse_chat_file(args.file)
        output = format_messages_for_output(messages)

        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n已解析 {len(messages)} 条消息")
        print(f"输出到：{args.output}")

    elif args.classify:
        if not args.db_dir or not args.target:
            print("错误：需要指定 --db-dir 和 --target", file=__import__("sys").stderr)
            return

        messages = extract_wechat_messages(args.db_dir, args.target)
        classification = classify_messages(messages)
        summary = format_classification_summary(classification)

        print(summary)

        output_path = args.output.replace(".txt", "_classification.txt")
        Path(output_path).write_text(summary, encoding="utf-8")
        print(f"\n分类结果已保存到：{output_path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()