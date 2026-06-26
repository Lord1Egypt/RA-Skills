#!/usr/bin/env python3
"""
qq_parser.py — QQ 聊天记录解析工具

支持格式：
  - QQ 消息管理器导出 txt
  - QQ 消息管理器导出 mht/mhtml

用法：
  python qq_parser.py --file chat.txt --person "爷爷" --output analysis.md
  python qq_parser.py --file chat.mht  --person "王建国"
"""

import argparse
import os
import re
from collections import Counter
from pathlib import Path


# ── 解析器 ────────────────────────────────────────────────────────────────────

def parse_qq_txt(file_path: str) -> list[dict]:
    """
    解析 QQ 消息管理器导出的 txt 格式。
    典型行格式：
      2024-01-15 20:30:45 张三(123456789)
      消息内容
    """
    messages = []
    current = None
    # 时间戳 + 发送者（昵称可含空格，QQ号在括号里）
    header_re = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)(?:\(\d+\))?\s*$')

    with open(file_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            m = header_re.match(line)
            if m:
                if current:
                    messages.append(current)
                current = {
                    "timestamp": m.group(1),
                    "sender": m.group(2).strip(),
                    "content": "",
                }
            elif current and line.strip() and not line.startswith("==="):
                if current["content"]:
                    current["content"] += "\n"
                current["content"] += line

    if current:
        messages.append(current)
    return messages


def parse_qq_mht(file_path: str) -> list[dict]:
    """
    解析 QQ 导出的 mht/mhtml 格式（HTML 内容）。
    提取纯文本后，尝试匹配消息结构；失败时返回整体文本供后续处理。
    """
    with open(file_path, encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # 去除 HTML 标签
    text = re.sub(r"<[^>]+>", "\n", raw)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # 尝试在纯文本里找 QQ 时间戳行
    messages = []
    header_re = re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)(?:\(\d+\))?\s*$')
    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = header_re.match(line)
        if m:
            if current:
                messages.append(current)
            current = {"timestamp": m.group(1), "sender": m.group(2).strip(), "content": ""}
        elif current:
            if current["content"]:
                current["content"] += "\n"
            current["content"] += line

    if current:
        messages.append(current)

    # 如果解析失败，返回一条整体记录供人工处理
    if not messages:
        messages = [{"timestamp": "", "sender": "[未解析]", "content": text[:20000]}]

    return messages


# ── 分析（与 wechat_parser 对齐）──────────────────────────────────────────────

FILLER_WORDS = [
    "嗯", "哦", "啊", "哈", "呢", "吧", "呀", "嘛", "哎", "唉",
    "好的", "好", "知道了", "行", "可以", "没事", "没关系",
    "蛮好", "屋里", "晓得", "嗯嗯", "哦哦",
]


def analyze_messages(messages: list[dict], person_name: str) -> dict:
    target = [m for m in messages if person_name in m.get("sender", "")]

    if not target:
        all_senders = list({m["sender"] for m in messages if m.get("sender") and m["sender"] != "[未解析]"})
        return {
            "error": f"未找到发送者包含 '{person_name}' 的消息",
            "found_senders": all_senders[:20],
            "total_messages": len(messages),
        }

    texts = [m["content"] for m in target if m.get("content")]
    lengths = [len(t) for t in texts]
    avg_length = round(sum(lengths) / len(lengths), 1) if lengths else 0

    # 语气词
    particle_counter: Counter = Counter()
    for t in texts:
        for w in FILLER_WORDS:
            if w in t:
                particle_counter[w] += 1

    # 高频短句
    short_phrases: Counter = Counter()
    for t in texts:
        for s in re.split(r"[，。！？、\n]", t):
            s = s.strip()
            if 3 <= len(s) <= 12:
                short_phrases[s] += 1
    common_phrases = [(p, c) for p, c in short_phrases.most_common(20) if c >= 2]

    short_samples = [t for t in texts if len(t) <= 10][:5]
    medium_samples = [t for t in texts if 10 < len(t) <= 50][:5]
    long_samples = [t for t in texts if len(t) > 50][:3]

    return {
        "person": person_name,
        "total_messages": len(target),
        "avg_length": avg_length,
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
        },
    }


# ── 输出 ──────────────────────────────────────────────────────────────────────

def format_analysis(analysis: dict) -> str:
    if "error" in analysis:
        lines = [
            "# QQ 消息分析",
            "",
            f"⚠️ {analysis['error']}",
            "",
            "文件中找到的发送者：",
        ]
        for s in analysis.get("found_senders", []):
            lines.append(f"  - {s}")
        lines.append(f"\n总消息数：{analysis.get('total_messages', 0)}")
        return "\n".join(lines)

    a = analysis
    lines = [
        f"# {a['person']} 的 QQ 消息分析",
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
        lines += ["## 高频语气词", ""]
        for word, count in a["particles"].items():
            lines.append(f"- **{word}**：出现 {count} 次")
        lines.append("")

    if a.get("common_phrases"):
        lines += ["## 常用短句（候选口头禅）", ""]
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
    parser = argparse.ArgumentParser(description="QQ 聊天记录分析工具")
    parser.add_argument("--file", required=True, help="聊天记录文件路径（txt 或 mht）")
    parser.add_argument("--person", required=True, help="要分析的人物名称/昵称")
    parser.add_argument("--output", help="输出分析报告的路径（默认输出到控制台）")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[错误] 找不到文件：{args.file}")
        return

    ext = Path(args.file).suffix.lower()
    if ext in (".mht", ".mhtml"):
        messages = parse_qq_mht(args.file)
        fmt = "mht"
    else:
        messages = parse_qq_txt(args.file)
        fmt = "txt"

    print(f"[检测] 格式：QQ {fmt}")
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
