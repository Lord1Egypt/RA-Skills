#!/usr/bin/env python3
"""
Meeting Analyzer — 会议分析与摘要生成
分析截屏+转录文本，生成结构化会议摘要和医疗辅助建议。
供 Agent 调用以理解会议内容。
"""

import json
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def collect_session_data(session_dir):
    """
    Collect all available data from a session directory.
    Returns a structured dict for agent consumption.
    """
    session_dir = Path(session_dir)

    data = {
        "session_dir": str(session_dir),
        "screenshots": [],
        "transcripts": [],
        "full_transcript": None,
        "session_meta": None,
    }

    # Session metadata
    meta_path = session_dir / "session.json"
    if meta_path.exists():
        with open(meta_path) as f:
            data["session_meta"] = json.load(f)

    # Screenshots (sorted by name = chronological)
    screenshots_dir = session_dir / "screenshots"
    if screenshots_dir.exists():
        data["screenshots"] = sorted([
            str(p) for p in screenshots_dir.glob("*.png")
        ])

    # Individual transcripts
    transcripts_dir = session_dir / "transcripts"
    if transcripts_dir.exists():
        for t in sorted(transcripts_dir.glob("chunk_*.txt")):
            data["transcripts"].append({
                "file": str(t),
                "name": t.stem,
                "text": t.read_text(encoding="utf-8").strip()
            })

        full = transcripts_dir / "full_transcript.txt"
        if full.exists():
            data["full_transcript"] = full.read_text(encoding="utf-8").strip()

    return data


def generate_analysis_prompt(session_data, mode="general"):
    """
    Generate a prompt for the Agent to analyze the meeting.
    Agent should use this prompt with Claude to generate the summary.
    """
    config = load_config()
    is_medical = mode == "medical" or config.get("medical", {}).get("enabled", False)

    prompt_parts = []

    prompt_parts.append("# 会议分析任务\n")
    prompt_parts.append(f"会议录制目录: {session_data['session_dir']}\n")

    if session_data.get("session_meta"):
        meta = session_data["session_meta"]
        prompt_parts.append(f"开始时间: {meta.get('start_time', 'N/A')}")
        prompt_parts.append(f"模式: {meta.get('mode', 'general')}\n")

    # Transcript
    if session_data.get("full_transcript"):
        prompt_parts.append("## 完整转录文本\n")
        prompt_parts.append(session_data["full_transcript"])
        prompt_parts.append("")

    # Screenshots for analysis
    if session_data.get("screenshots"):
        prompt_parts.append(f"\n## 截屏文件 ({len(session_data['screenshots'])} 张)\n")
        prompt_parts.append("请逐一分析以下截屏（使用 Read 工具查看图片）：")
        for s in session_data["screenshots"]:
            prompt_parts.append(f"  - {s}")
        prompt_parts.append("")

    # Analysis instructions
    prompt_parts.append("\n## 分析要求\n")
    prompt_parts.append("请生成以下内容：\n")
    prompt_parts.append("### 1. 会议摘要")
    prompt_parts.append("- 参会人员")
    prompt_parts.append("- 主要议题")
    prompt_parts.append("- 关键讨论内容")
    prompt_parts.append("- 达成的结论/决定")
    prompt_parts.append("- 待办事项\n")

    if is_medical:
        prompt_parts.append("### 2. 医疗相关分析")
        prompt_parts.append("- 提到的症状/诊断")
        prompt_parts.append("- 处方/用药信息")
        prompt_parts.append("- 医嘱和注意事项")
        prompt_parts.append("- 下次就诊安排")
        prompt_parts.append("- **患者版简明摘要**（用通俗语言解释所有医学术语）\n")

        prompt_parts.append("### 3. 医学术语解释")
        prompt_parts.append("将会议中提到的所有医学术语列出，并给出：")
        prompt_parts.append("- 中文通俗解释")
        prompt_parts.append("- 英文对照（如适用）")
        prompt_parts.append("- 相关背景说明\n")

    prompt_parts.append(f"\n请将分析结果写入: {session_data['session_dir']}/meeting_summary.md")

    return "\n".join(prompt_parts)


def find_latest_session():
    """Find the most recent session directory."""
    config = load_config()
    base = SKILL_DIR / config.get("output_base_dir", "recordings")
    if not base.exists():
        return None
    sessions = sorted(base.iterdir(), reverse=True)
    return sessions[0] if sessions else None


def generate_realtime_prompt(screenshot_path=None, transcript_text=None, mode="general"):
    """
    Generate a prompt for real-time analysis during an active meeting.
    Used by the agent in its monitoring loop.
    """
    config = load_config()
    is_medical = mode == "medical" or config.get("medical", {}).get("enabled", False)

    parts = ["# 实时会议分析\n"]

    if screenshot_path:
        parts.append(f"## 当前画面\n请分析此截屏: {screenshot_path}\n")

    if transcript_text:
        parts.append(f"## 最近对话内容\n```\n{transcript_text}\n```\n")

    parts.append("## 请提供：\n")
    parts.append("1. 当前讨论的核心话题")
    parts.append("2. 需要注意的关键信息")

    if is_medical:
        parts.append("3. 医学术语通俗解释（如果有的话）")
        parts.append("4. 给患者的建议或提醒")
        parts.append("5. 给医生的辅助信息（如需要）")
    else:
        parts.append("3. 可能的行动建议")

    parts.append("\n请简洁回答，适合在会议进行中快速阅读。")

    return "\n".join(parts)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Meeting analysis utilities")
    sub = parser.add_subparsers(dest="command")

    p_collect = sub.add_parser("collect", help="Collect session data")
    p_collect.add_argument("session_dir", nargs="?", help="Session directory")

    p_prompt = sub.add_parser("prompt", help="Generate analysis prompt")
    p_prompt.add_argument("session_dir", nargs="?")
    p_prompt.add_argument("--mode", choices=["general", "medical"], default="general")

    p_realtime = sub.add_parser("realtime", help="Generate real-time analysis prompt")
    p_realtime.add_argument("--screenshot", help="Screenshot path")
    p_realtime.add_argument("--transcript", help="Recent transcript text")
    p_realtime.add_argument("--mode", choices=["general", "medical"], default="general")

    args = parser.parse_args()

    if args.command == "collect":
        session_dir = args.session_dir or find_latest_session()
        if session_dir:
            data = collect_session_data(session_dir)
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("No session found")

    elif args.command == "prompt":
        session_dir = args.session_dir or find_latest_session()
        if session_dir:
            data = collect_session_data(session_dir)
            print(generate_analysis_prompt(data, args.mode))
        else:
            print("No session found")

    elif args.command == "realtime":
        print(generate_realtime_prompt(
            screenshot_path=args.screenshot,
            transcript_text=args.transcript,
            mode=args.mode
        ))

    else:
        parser.print_help()
