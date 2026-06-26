#!/usr/bin/env python3
"""
转录音频并生成会议纪要。

转录: whisper.cpp (whisper-cli)
摘要: 默认交给 OpenClaw agent（闪电）根据模板生成；也可配置外部命令

依赖：
  brew install whisper-cpp        # whisper-cli
  npm i -g @anthropic-ai/claude-code  # claude-cli (OpenClaw 默认已装)

模型：
  下载 ggml-medium.bin / ggml-large-v3.bin 到 ~/Models/whisper/

配置（config.json）：
{
  "transcription": {
    "command": ["whisper-cli", "-m", "/Users/x/Models/whisper/ggml-medium.bin",
                "-l", "zh", "-otxt", "-of", "{{output_stem}}", "{{input}}"]
  },
  "llm": {
    "enabled": true,
    "command": ["claude", "--print", "--model", "claude-opus-4-7"]
  }
}

输出：
  <meeting>.transcript.txt  — 原始转录
  <meeting>.summary.md      — 结构化纪要
"""

import json
import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "meeting-assistant" / "config.json"

DEFAULT_TRANSCRIBE_CMD = [
    "whisper-cli",
    "-m", str(Path.home() / "Models/whisper/ggml-medium.bin"),
    "-l", "zh",
    "-otxt",
    "-of", "{{output_stem}}",
    "{{input}}",
]

DEFAULT_LLM_CMD = []  # 默认空 = 由 agent (闪电) 处理

NOTIFY_SCRIPT = Path(__file__).parent / "notify.py"

SUMMARY_PROMPT = """请将以下会议转录整理成结构化会议纪要。

会议主题：{title}

要求：
1. 列出会议基本信息（主题、时间）
2. 按议题分类讨论要点，每个议题下列出关键发言和结论
3. 提取所有 Action Items（待办事项），标注负责人和截止日期（如能从内容推断）
4. 提取关键决策结论
5. 使用中文，Markdown 格式输出，不要任何额外说明文字

会议转录：
---
{transcript}
---
"""


def load_config():
    if not CONFIG_PATH.exists():
        print(f"Config not found at {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def render_cmd(template, **vars):
    """把命令模板里的 {{key}} 替换成实际值。"""
    rendered = []
    for tok in template:
        for k, v in vars.items():
            tok = tok.replace(f"{{{{{k}}}}}", v)
        rendered.append(tok)
    return rendered


def transcribe(audio_path, config):
    """用 whisper-cli 转录。返回转录文本。"""
    audio_path = Path(audio_path).resolve()
    cmd_template = config.get("command") or DEFAULT_TRANSCRIBE_CMD

    # whisper-cli 的 -otxt -of <stem> 会写到 <stem>.txt
    output_stem = audio_path.with_suffix("").as_posix() + ".whisper"
    output_txt = Path(f"{output_stem}.txt")

    cmd = render_cmd(cmd_template, input=str(audio_path), output_stem=output_stem)
    print(f"🎙️ whisper-cli: {shlex.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"whisper-cli failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    if not output_txt.exists():
        print(f"Transcript file not written: {output_txt}", file=sys.stderr)
        sys.exit(1)

    transcript = output_txt.read_text(encoding="utf-8").strip()
    output_txt.unlink()  # 清理 whisper 中间文件
    return transcript


def summarize(transcript, meeting_title, config):
    """生成结构化纪要。

    如果显式配置了外部命令则调用；默认不使用 claude-cli，交给 OpenClaw agent 队列处理。
    返回 markdown 字符串；None 表示需要 agent 后续生成。
    """
    cmd_template = config.get("command") or DEFAULT_LLM_CMD

    if not cmd_template:
        print("🤖 未配置外部 LLM，先生成本地草稿并请求 OpenClaw agent 生成最终摘要...")
        return None

    cmd = render_cmd(cmd_template)
    prompt = SUMMARY_PROMPT.format(title=meeting_title, transcript=transcript)
    print(f"🤖 LLM: {shlex.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        print(f"LLM failed: {result.stderr}", file=sys.stderr)
    except Exception as e:
        print(f"LLM error: {e}", file=sys.stderr)
    return None


def _send_agent_notification(title):
    """发系统通知告知转录完成，等待 agent 总结。"""
    notify = NOTIFY_SCRIPT
    subprocess.Popen(
        [sys.executable, str(notify), "remind",
         "Meeting Assistant",
         f"「{title}」转录完成，找我出纪要",
         "待总结"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _notify_agent(event_type, **kw):
    try:
        from agent_notify import notify
        notify(event_type, **kw)
    except Exception:
        pass


def fallback_summary(transcript, meeting_title):
    """无外部 LLM 时生成可直接使用的本地摘要，不再输出占位文字。"""
    import re

    lines = [line.strip() for line in transcript.splitlines() if line.strip()]
    text = " ".join(lines)
    tldr = text[:220] + ("…" if len(text) > 220 else "")

    points = []
    for line in lines:
        if len(line) >= 4 and line not in points:
            points.append(line)
        if len(points) >= 8:
            break

    action_lines = [
        line for line in lines
        if re.search(r"(需要|要做|负责|跟进|安排|确认|明天|下周|todo|action)", line, re.I)
    ]
    question_lines = [
        line for line in lines
        if "?" in line or "？" in line or re.search(r"(问题|疑问|阻塞|不确定|block)", line, re.I)
    ]
    decision_lines = [
        line for line in lines
        if re.search(r"(决定|确认|结论|同意|采用|最终)", line)
    ]

    def bullets(items, empty="无明确内容"):
        return "\n".join(f"- {x}" for x in items[:8]) if items else f"- {empty}"

    def todos(items):
        return "\n".join(f"- [ ] {x}" for x in items[:8]) if items else "- [ ] 无明确待办"

    return (
        f"# {meeting_title}\n\n"
        f"## TL;DR\n"
        f"{tldr or '转录为空，无法生成摘要。'}\n\n"
        f"## Discussion Points\n"
        f"{bullets(points)}\n\n"
        f"## Action Items\n"
        f"{todos(action_lines)}\n\n"
        f"## Open Questions / Blockers\n"
        f"{bullets(question_lines)}\n\n"
        f"## Decisions Made\n"
        f"{bullets(decision_lines, '无明确决策')}\n\n"
        f"---\n"
        f"## 原始转录\n\n{transcript}\n"
    )


def request_agent_summary(meeting_title, transcript_path, summary_path):
    """通知 OpenClaw agent 按模板生成最终 summary。"""
    template_path = Path(__file__).parent / "summary_template.md"
    _notify_agent(
        "summary_request",
        title=meeting_title,
        transcript_path=str(transcript_path),
        summary_path=str(summary_path),
        template_path=str(template_path),
    )


def process_audio(audio_path):
    config = load_config()
    trans_cfg = config.get("transcription", {})
    llm_cfg = config.get("llm", {})

    audio_path = Path(audio_path)
    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    meeting_title = audio_path.stem.rsplit("_", 1)[0].replace("_", " ")
    print(f"📁 处理: {audio_path.name}（标题: {meeting_title}）")

    # 1. 转录
    transcript = transcribe(audio_path, trans_cfg)

    # 2. 保存转录
    transcript_path = audio_path.with_suffix(".transcript.txt")
    transcript_path.write_text(transcript, encoding="utf-8")
    print(f"✅ 转录已保存: {transcript_path}")
    print(f"Transcript saved: {transcript_path}")

    # 3. 摘要
    summary = None
    if llm_cfg.get("enabled", True):
        summary = summarize(transcript, meeting_title, llm_cfg)
    agent_should_finalize = False
    if summary is None:
        # 先写一份本地可读草稿作为兜底，但不发送；随后交给 OpenClaw agent 覆盖为最终版。
        summary = fallback_summary(transcript, meeting_title)
        agent_should_finalize = True

    # 4. 保存摘要
    summary_path = audio_path.with_suffix(".summary.md")
    summary_path.write_text(summary, encoding="utf-8")
    print(f"✅ 纪要已保存: {summary_path}")
    print(f"Summary saved: {summary_path}")
    if agent_should_finalize:
        print("Summary status: draft_agent_pending")
        request_agent_summary(meeting_title, transcript_path, summary_path)
    else:
        print("Summary status: final")
        _notify_agent("summary_ready", title=meeting_title, path=str(summary_path))

    return str(transcript_path), str(summary_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: transcribe.py <audio_file_path>", file=sys.stderr)
        sys.exit(1)
    process_audio(sys.argv[1])
