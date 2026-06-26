#!/usr/bin/env python3
"""
wechat_parser.py — 微信聊天记录解析工具（T-02）

支持格式：
  - WeChatMsg 导出（txt）
  - 留痕 JSON 格式
  - 纯文本粘贴

用法：
  python wechat_parser.py --file chat.txt --person "爷爷" --output analysis.md
  python wechat_parser.py --file chat.json --person "王建国"
"""

import argparse
import json
import os
import re
from collections import Counter
from typing import NamedTuple


class Message(NamedTuple):
    sender: str
    content: str
    timestamp: str = ""


# ── 格式检测 ──────────────────────────────────────────────────────────────────

def detect_format(content: str) -> str:
    """自动检测微信导出格式。"""
    stripped = content.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return "json"
    # WeChatMsg txt 格式：以时间戳行开头 "2023-01-01 12:00:00"
    if re.search(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", stripped[:200]):
        return "wechatmsg_txt"
    return "plaintext"


# ── 解析器 ────────────────────────────────────────────────────────────────────

def parse_wechatmsg_txt(content: str) -> list[Message]:
    """
    解析 WeChatMsg 导出的 txt 格式。
    典型行格式：
      2023-01-01 12:00:00  发送者名称
      消息内容
    """
    messages = []
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 时间戳行
        ts_match = re.match(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.*)", line)
        if ts_match:
            timestamp = ts_match.group(1)
            sender = ts_match.group(2).strip()
            # 下一行是消息内容
            content_lines = []
            i += 1
            while i < len(lines) and not re.match(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", lines[i]):
                content_lines.append(lines[i])
                i += 1
            msg_content = "\n".join(content_lines).strip()
            if msg_content:
                messages.append(Message(sender=sender, content=msg_content, timestamp=timestamp))
        else:
            i += 1
    return messages


def parse_json(content: str) -> list[Message]:
    """解析留痕 JSON 格式。"""
    data = json.loads(content)
    messages = []

    # 兼容多种 JSON 结构
    if isinstance(data, list):
        for item in data:
            sender = item.get("sender") or item.get("NickName") or item.get("from") or ""
            body = item.get("content") or item.get("Content") or item.get("text") or ""
            ts = item.get("timestamp") or item.get("CreateTime") or ""
            if body:
                messages.append(Message(sender=str(sender), content=str(body), timestamp=str(ts)))
    elif isinstance(data, dict):
        # 留痕格式：{"messages": [...]}
        items = data.get("messages") or data.get("records") or []
        for item in items:
            sender = item.get("sender") or item.get("NickName") or ""
            body = item.get("content") or item.get("Content") or ""
            ts = item.get("timestamp") or ""
            if body:
                messages.append(Message(sender=str(sender), content=str(body), timestamp=str(ts)))

    return messages


def parse_plaintext(content: str, person_name: str) -> list[Message]:
    """
    解析纯文本粘贴格式。
    假设格式为每行独立消息，或「发送者：内容」。
    """
    messages = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        # 尝试匹配「名字：内容」
        colon_match = re.match(r"^([^：:]{1,20})[：:]\s*(.+)$", line)
        if colon_match:
            messages.append(Message(
                sender=colon_match.group(1).strip(),
                content=colon_match.group(2).strip()
            ))
        else:
            # 归属不明，标注为待定
            messages.append(Message(sender="[未知]", content=line))
    return messages


# ── 分析 ──────────────────────────────────────────────────────────────────────

FILLER_WORDS = [
    "嗯", "哦", "啊", "哈", "呢", "吧", "呀", "嘛", "哎", "唉",
    "好的", "好", "知道了", "行", "可以", "没事", "没关系",
    "蛮好", "屋里", "晓得"
]

def extract_particles(text: str) -> list[str]:
    """提取语气词。"""
    found = []
    for w in FILLER_WORDS:
        if w in text:
            found.append(w)
    return found


def analyze_messages(messages: list[Message], person_name: str) -> dict:
    """分析目标人物的消息特征。"""
    # 筛选目标人物的消息
    target_msgs = [
        m for m in messages
        if person_name in m.sender or m.sender == person_name
    ]

    if not target_msgs:
        # 如果没找到匹配的发送者，返回所有消息的分析（供用户确认）
        all_senders = list({m.sender for m in messages if m.sender != "[未知]"})
        return {
            "error": f"未找到发送者包含 '{person_name}' 的消息",
            "found_senders": all_senders[:20],
            "total_messages": len(messages),
        }

    texts = [m.content for m in target_msgs]
    all_text = " ".join(texts)

    # 消息长度分布
    lengths = [len(t) for t in texts]
    avg_length = sum(lengths) / len(lengths) if lengths else 0

    # 语气词统计
    particle_counter: Counter = Counter()
    for text in texts:
        for p in extract_particles(text):
            particle_counter[p] += 1

    # 常见短句（3-10字，出现2次以上）
    short_phrases: Counter = Counter()
    for text in texts:
        sentences = re.split(r"[，。！？、\n]", text)
        for s in sentences:
            s = s.strip()
            if 3 <= len(s) <= 12:
                short_phrases[s] += 1
    common_phrases = [(p, c) for p, c in short_phrases.most_common(20) if c >= 2]

    # 消息示例（按长度分类）
    short_samples = [t for t in texts if len(t) <= 10][:5]
    medium_samples = [t for t in texts if 10 < len(t) <= 50][:5]
    long_samples = [t for t in texts if len(t) > 50][:3]

    return {
        "person": person_name,
        "total_messages": len(target_msgs),
        "avg_length": round(avg_length, 1),
        "length_distribution": {
            "short_1_10": len([l for l in lengths if l <= 10]),
            "medium_11_50": len([l for l in lengths if 10 < l <= 50]),
            "long_50+": len([l for l in lengths if l > 50]),
        },
        "particles": dict(particle_counter.most_common(10)),
        "common_phrases": common_phrases,
        "samples": {
            "short": short_samples,
            "medium": medium_samples,
            "long": long_samples,
        }
    }


# ── 输出 ──────────────────────────────────────────────────────────────────────

def format_analysis(analysis: dict) -> str:
    """将分析结果格式化为 Markdown。"""
    if "error" in analysis:
        lines = [
            "# 微信记录分析",
            "",
            f"⚠️ {analysis['error']}",
            "",
            f"文件中找到的发送者：",
        ]
        for sender in analysis.get("found_senders", []):
            lines.append(f"  - {sender}")
        lines.append(f"\n总消息数：{analysis.get('total_messages', 0)}")
        return "\n".join(lines)

    a = analysis
    lines = [
        f"# {a['person']} 的微信消息分析",
        "",
        f"**分析消息数**：{a['total_messages']} 条",
        f"**平均消息长度**：{a['avg_length']} 字",
        "",
        "## 消息长度分布",
        "",
        f"- 短消息（1-10字）：{a['length_distribution']['short_1_10']} 条",
        f"- 中等（11-50字）：{a['length_distribution']['medium_11_50']} 条",
        f"- 长消息（50字以上）：{a['length_distribution']['long_50+']} 条",
        "",
    ]

    if a.get("particles"):
        lines += [
            "## 高频语气词",
            "",
        ]
        for word, count in a["particles"].items():
            lines.append(f"- **{word}**：出现 {count} 次")
        lines.append("")

    if a.get("common_phrases"):
        lines += [
            "## 常用短句（候选口头禅）",
            "",
        ]
        for phrase, count in a["common_phrases"][:10]:
            lines.append(f"- **「{phrase}」**：出现 {count} 次")
        lines.append("")

    if a.get("samples", {}).get("short"):
        lines += ["## 短消息示例", ""]
        for s in a["samples"]["short"]:
            lines.append(f"  > {s}")
        lines.append("")

    if a.get("samples", {}).get("long"):
        lines += ["## 长消息示例", ""]
        for s in a["samples"]["long"]:
            lines.append(f"  > {s[:200]}{'...' if len(s) > 200 else ''}")
        lines.append("")

    lines += [
        "---",
        "*以上数据可用于填充 persona.md 的 Layer 2 语言风格部分。*",
    ]

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="微信聊天记录分析工具")
    parser.add_argument("--file", required=True, help="聊天记录文件路径")
    parser.add_argument("--person", required=True, help="要分析的人物名称")
    parser.add_argument("--output", help="输出分析报告的路径（默认输出到控制台）")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[错误] 找不到文件：{args.file}")
        return

    with open(args.file, encoding="utf-8", errors="replace") as f:
        content = f.read()

    fmt = detect_format(content)
    print(f"[检测] 格式：{fmt}")

    if fmt == "json":
        messages = parse_json(content)
    elif fmt == "wechatmsg_txt":
        messages = parse_wechatmsg_txt(content)
    else:
        messages = parse_plaintext(content, args.person)

    print(f"[解析] 共 {len(messages)} 条消息")

    analysis = analyze_messages(messages, args.person)
    report = format_analysis(analysis)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[输出] 分析报告已保存到 {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
