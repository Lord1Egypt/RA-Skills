# -*- coding: utf-8 -*-
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

"""
从微信导出的 xlsx 群聊记录中，按发送者分别提取文本消息。
用法：python extract_chat.py <xlsx路径> <输出目录>
"""

import openpyxl
import re
import argparse

def is_text_msg(row):
    """判断是否为文本消息（忽略表情、拍一拍、系统消息等）"""
    if len(row) < 5:
        return False
    msg_type = str(row[3]) if row[3] else ""
    return "文本" in msg_type or "文本消息" in msg_type

def extract_person_messages(xlsx_path, target_sender=None):
    """提取某发送者的文本消息"""
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    messages = []
    sender_counts = {}

    for row in ws.iter_rows(min_row=5, values_only=True):  # 前4行是表头
        if not row or not row[0]:  # 跳过空行
            continue

        # 识别发送者
        sender = str(row[2]).strip() if row[2] else ""
        content = str(row[4]).strip() if row[4] else ""

        if not sender or not content:
            continue

        sender_counts[sender] = sender_counts.get(sender, 0) + 1

        # 过滤消息类型
        if not is_text_msg(row):
            continue

        # 清理内容（去除开头的换行和空白）
        content = content.strip()
        if not content or content.startswith("../"):
            continue

        if target_sender is None or sender == target_sender:
            messages.append((sender, content))

    return messages, sender_counts

def format_for_distil(messages):
    """格式化为 distil.py 可接受的格式"""
    lines = []
    for sender, content in messages:
        lines.append(f"{sender}: {content}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="从微信xlsx提取群聊记录")
    parser.add_argument("xlsx", help="xlsx文件路径")
    parser.add_argument("--out", "-o", default=None, help="输出目录")
    args = parser.parse_args()

    xlsx_path = args.xlsx
    out_dir = args.out or os.path.join(os.path.dirname(xlsx_path), "extracted")
    os.makedirs(out_dir, exist_ok=True)

    print(f"读取: {xlsx_path}")
    messages, sender_counts = extract_person_messages(xlsx_path)
    print(f"\n发送者统计: {sender_counts}\n")

    # 按发送者分组
    by_sender = {}
    for sender, content in messages:
        by_sender.setdefault(sender, []).append((sender, content))

    # 每人一个文件
    for sender, msgs in by_sender.items():
        text = format_for_distil(msgs)
        safe_name = re.sub(r"[^\w\u4e00-\u9fff-]", "_", sender)
        out_path = os.path.join(out_dir, f"{safe_name}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ [{sender}] {len(msgs)} 条文本消息 → {out_path}")

    print(f"\n📂 所有文件已保存到: {out_dir}")
    print("下一步: python distil.py <文件路径> --name <人格名称>")

if __name__ == "__main__":
    main()
