#!/usr/bin/env python3
"""MindVault — JSONL → Markdown（基础版 · 免费）

用法：
  python jsonl_to_md.py <jsonl_file> [--style minimal] [--output <md_file>]

默认输出到 stdout，--output 写入文件。
--style minimal：仅用户+Agent 消息（默认，也是基础版唯一可用模式）
--style full / --css HTML 模板输出需按版本核对，对照表见https://www.jinengpu.chat/mindvault-detail.html
"""

import json
import sys
from datetime import datetime
from pathlib import Path


ROLE_ICONS = {
    "user": "👤",
    "agent": "🤖",
    "tool": "🔧",
    "system": "⚙️",
    "scheduled": "⏰",
}


def render_jsonl(filepath: str, style: str = "minimal") -> str:
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            role = entry.get("role", "?")
            if style == "minimal" and role not in ("user", "agent"):
                continue

            icon = ROLE_ICONS.get(role, "❓")
            ts = entry.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts)
                    ts_fmt = dt.strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    ts_fmt = ts
            else:
                ts_fmt = ""

            lines.append(f"### {icon} {role.upper()}  {ts_fmt}\n")

            if role == "user":
                content = entry.get("content", "")
                attachments = entry.get("attachments", [])
                if attachments:
                    att_lines = ["**附件：**"]
                    for att in attachments:
                        att_lines.append(f"- [{att.get('type','file')}] `{att.get('path','?')}`")
                    lines.append("\n".join(att_lines) + "\n")
                if content:
                    lines.append(f"{content}\n")

            elif role == "agent":
                reasoning = entry.get("reasoning", "")
                if reasoning:
                    lines.append(f"> *推理思路：* {reasoning}\n")
                content = entry.get("content", "")
                if content:
                    trunc = entry.get("content_truncated", False)
                    if trunc:
                        content += "\n\n*（内容已截断）*"
                    lines.append(f"{content}\n")
                tools = entry.get("tool_calls", []) or []
                if tools:
                    lines.append("**工具调用：**\n")
                    # 参数优先取 tool_calls 元素内的 args（真实工具参数）；
                    # 回退读取 Agent 条目顶层 key_params（兼容 archive_export 的扁平导出格式）
                    top_params = entry.get("key_params", {}) or {}
                    for t in tools:
                        name = t.get('name', '?')
                        args = t.get('args', {}) or {}
                        if args:
                            params_text = json.dumps(args, ensure_ascii=False)
                        elif top_params:
                            params_text = json.dumps(top_params, ensure_ascii=False)
                        else:
                            params_text = ""
                        lines.append(f"- `{name}`")
                        if params_text:
                            lines.append(f"  - {params_text}")
                    lines.append("")

            elif role == "tool":
                tool_name = entry.get("tool_name", "?")
                lines.append(f"**工具：** `{tool_name}`\n")
                # 读取 archive_export 实际导出的 v3.1 字段：
                # args_summary(key_param+计数) / files / urls / errors
                args_summary = entry.get("args_summary", "") or ""
                if args_summary:
                    lines.append(f"- {args_summary}\n")
                files = entry.get("files", []) or []
                if files:
                    lines.append("- 涉及文件：")
                    for f in files:
                        lines.append(f"  - `{f}`")
                    lines.append("")
                urls = entry.get("urls", []) or []
                if urls:
                    lines.append("- 涉及 URL：")
                    for u in urls:
                        lines.append(f"  - `{u}`")
                    lines.append("")
                errors = entry.get("errors", []) or []
                if errors:
                    lines.append("⚠️ 错误：")
                    for e in errors:
                        lines.append(f"  - {e}")
                    lines.append("")
                # 兼容旧版字段（summary / result_preview）
                if not (args_summary or files or urls or errors):
                    summary = entry.get("summary", "")
                    if summary:
                        lines.append(f"{summary}\n")
                    result = entry.get("result_preview", "")
                    if result:
                        lines.append(f"```\n{result}\n```\n")

            elif role == "system":
                content = entry.get("content", "") or entry.get("origin", "")
                lines.append(f"```\n{content}\n```\n")

            elif role == "scheduled":
                summary = entry.get("summary", "")
                lines.append(f"{summary}\n")

            lines.append("---\n")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="JSONL 归档 → Markdown 阅读器")
    parser.add_argument("jsonl_file", help="JSONL 归档文件路径")
    parser.add_argument("--style", choices=["minimal"], default="minimal",
                        help="渲染风格：minimal=仅用户+Agent 消息")
    parser.add_argument("--output", "-o", help="输出 Markdown 文件路径")
    args = parser.parse_args()

    md = render_jsonl(args.jsonl_file, style=args.style)

    # 中性提示（留针不留墙）：统计未被 minimal 渲染的消息数，N=0 不打印
    if args.style == "minimal":
        try:
            tool_n = 0
            with open(args.jsonl_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("role") not in ("user", "agent"):
                        tool_n += 1
            if tool_n:
                print(f"本分片含 {tool_n} 条工具调用记录，当前渲染仅显示用户 / Agent 消息（对照表见https://www.jinengpu.chat/mindvault-detail.html）")
        except OSError:
            pass

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(md, encoding="utf-8")
        print(f"已写入: {out_path}")
    else:
        print(md)


if __name__ == "__main__":
    main()
