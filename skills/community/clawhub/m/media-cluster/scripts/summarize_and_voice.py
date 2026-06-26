#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read MediaCrawler JSONL output, generate a Markdown report and a short voice script.
TTS uses SenseAudio API (https://senseaudio.cn/docs/). Requires SENSEAUDIO_API_KEY env var.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent

try:
    import requests
except ImportError:
    requests = None

SENSEAUDIO_API_BASE = "https://api.senseaudio.cn"
SENSEAUDIO_TTS_URL = f"{SENSEAUDIO_API_BASE}/v1/t2a_v2"
DEFAULT_VOICE_ID = "male_0004_a"


def platform_label(platform: str) -> str:
    labels = {
        "xhs": "小红书",
        "dy": "抖音",
        "ks": "快手",
        "bili": "B站",
        "wb": "微博",
        "tieba": "贴吧",
        "zhihu": "知乎",
    }
    return labels.get(platform, platform)


def find_latest_jsonl(data_dir: Path, platform: str) -> Path | None:
    """Find latest search notes jsonl in data/<platform>/jsonl/."""
    base = data_dir / platform / "jsonl"
    if not base.exists():
        return None
    candidates = list(base.glob("search_notes_*.jsonl"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def load_notes(path: Path) -> list[dict]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def build_report(notes: list[dict], platform: str, keyword: str) -> str:
    plabel = platform_label(platform)
    lines = [
        f"# 媒体爬取报告：{keyword}",
        "",
        f"- **平台**：{plabel}",
        f"- **关键词**：{keyword}",
        f"- **爬取条数**：{len(notes)}",
        "",
        "## 内容概览",
        "",
    ]
    if not notes:
        lines.append("（无数据）")
        return "\n".join(lines)

    # Group by source_keyword if present
    by_kw: dict[str, list] = {}
    for n in notes:
        kw = n.get("source_keyword") or keyword
        by_kw.setdefault(kw, []).append(n)

    for kw, group in by_kw.items():
        lines.append(f"### 关键词「{kw}」共 {len(group)} 条")
        lines.append("")
        for i, n in enumerate(group[:20], 1):  # top 20
            title = n.get("title") or n.get("desc") or "(无标题)"
            desc = (n.get("desc") or "")[:120]
            if desc and (n.get("title") or "") != desc:
                title = f"{title}"
            nickname = n.get("nickname", "")
            liked = n.get("liked_count", "")
            comment = n.get("comment_count", "")
            lines.append(f"{i}. **{title}**")
            if desc:
                lines.append(f"   - 摘要：{desc}…")
            lines.append(f"   - 作者：{nickname} | 点赞：{liked} | 评论：{comment}")
        if len(group) > 20:
            lines.append(f"   - …其余 {len(group) - 20} 条略")
        lines.append("")

    lines.append("## 明细（前 50 条）")
    lines.append("")
    lines.append("| 标题 | 作者 | 点赞 | 评论 | 链接 |")
    lines.append("|------|------|------|------|------|")
    for n in notes[:50]:
        title = (n.get("title") or n.get("desc") or "-")[:40]
        author = (n.get("nickname") or "-")[:12]
        liked = n.get("liked_count", "-")
        comment = n.get("comment_count", "-")
        url = n.get("note_url") or n.get("video_url") or n.get("url") or "-"
        lines.append(f"| {title} | {author} | {liked} | {comment} | {url} |")

    return "\n".join(lines)


def build_voice_script(notes: list[dict], platform: str, keyword: str) -> str:
    plabel = platform_label(platform)
    n = len(notes)
    if n == 0:
        return f"在{plabel}上按关键词「{keyword}」未爬取到内容。"
    # 3–5 句简洁总结
    parts = [
        f"在{plabel}上按关键词「{keyword}」共爬取到 {n} 条内容。",
    ]
    if notes:
        titles = [n.get("title") or n.get("desc") or "" for n in notes[:5] if n.get("title") or n.get("desc")]
        if titles:
            sample = "；".join(t[:20] for t in titles if t)[:80]
            parts.append(f"例如：{sample}。")
    parts.append("报告已生成，可查看 Markdown 文件了解详情。")
    return "".join(parts)


def tts_senseaudio(
    text: str,
    api_key: str,
    voice_id: str = DEFAULT_VOICE_ID,
    output_path: str | Path | None = None,
    stream: bool = False,
) -> Path | None:
    """
    Call SenseAudio TTS API (https://senseaudio.cn/docs/).
    Returns path to saved audio file (mp3), or None on failure.
    """
    if not requests:
        print("(TTS 需要 requests: pip install requests)", file=sys.stderr)
        return None
    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": stream,
        "voice_setting": {"voice_id": voice_id},
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(SENSEAUDIO_TTS_URL, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        out = r.json()
    except requests.RequestException as e:
        print(f"SenseAudio API 请求失败: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None and e.response.text:
            print(e.response.text[:500], file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"SenseAudio 响应解析失败: {e}", file=sys.stderr)
        return None

    data = out.get("data")
    base_resp = out.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        print(f"SenseAudio 错误: {base_resp.get('status_msg', out)}", file=sys.stderr)
        return None
    if not data or "audio" not in data:
        print("SenseAudio 响应中无音频数据", file=sys.stderr)
        return None

    raw_hex = data["audio"]
    try:
        audio_bytes = bytes.fromhex(raw_hex)
    except ValueError:
        print("SenseAudio 返回的 audio 非合法 hex", file=sys.stderr)
        return None

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        output_path = Path(output_path)
    else:
        output_path = Path(output_path)
    output_path.write_bytes(audio_bytes)
    return output_path


def play_audio(path: Path) -> bool:
    """Play audio file (macOS: afplay, Windows: default player, Linux: paplay/aplay/ffplay)."""
    p = str(path.resolve())
    if sys.platform == "darwin":
        try:
            subprocess.run(["afplay", p], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    elif sys.platform == "win32":
        try:
            os.startfile(p)
            return True
        except OSError:
            pass
    else:
        for cmd in (["paplay", p], ["aplay", p], ["ffplay", "-nodisp", "-autoexit", p]):
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize MediaCrawler data and optionally speak.")
    parser.add_argument("--data-dir", type=str, default=str(_SKILL_ROOT / "MediaCrawler" / "data"),
                        help="Path to MediaCrawler data directory (default: {baseDir}/MediaCrawler/data)")
    parser.add_argument("--platform", type=str, default="xhs",
                        help="Platform: xhs, dy, ks, bili, wb, tieba, zhihu")
    parser.add_argument("--keyword", type=str, default="",
                        help="Search keyword (for report title)")
    parser.add_argument("--report", type=str, default="",
                        help="Output report path (default: media_cluster_report_<keyword>_<date>.md)")
    parser.add_argument("--voice", action="store_true",
                        help="Generate TTS with SenseAudio API and save/play audio")
    parser.add_argument("--api-key", type=str, default=os.environ.get("SENSEAUDIO_API_KEY", ""),
                        help="SenseAudio API key (default: from SENSEAUDIO_API_KEY env var)")
    parser.add_argument("--voice-id", type=str, default=os.environ.get("SENSEAUDIO_VOICE_ID", DEFAULT_VOICE_ID),
                        help="SenseAudio voice_id (default: from SENSEAUDIO_VOICE_ID env var or male_0004_a)")
    parser.add_argument("--voice-out", type=str, default="",
                        help="Path to save TTS audio (default: next to report, media_cluster_voice_<keyword>.mp3)")
    parser.add_argument("--file", type=str, default="",
                        help="Direct path to jsonl file (overrides data-dir + platform)")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            sys.exit(1)
    else:
        data_dir = Path(args.data_dir)
        path = find_latest_jsonl(data_dir, args.platform)
        if not path:
            print(f"No search_notes_*.jsonl found under {data_dir / args.platform / 'jsonl'}", file=sys.stderr)
            sys.exit(1)

    notes = load_notes(path)
    keyword = args.keyword or notes[0].get("source_keyword", "搜索") if notes else "搜索"

    report_body = build_report(notes, args.platform, keyword)
    voice_script = build_voice_script(notes, args.platform, keyword)

    if args.report:
        report_path = Path(args.report)
    else:
        safe_kw = "".join(c if c.isalnum() or c in " _-" else "_" for c in keyword)[:30]
        report_path = Path(f"media_cluster_report_{safe_kw}_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_body, encoding="utf-8")
    print(f"Report written: {report_path}")

    print("\n--- 简洁版语音稿 ---")
    print(voice_script)
    print("---")

    if args.voice:
        api_key = (args.api_key or os.environ.get("SENSEAUDIO_API_KEY") or "").strip()
        if not api_key:
            print("(TTS 未执行：请设置环境变量 SENSEAUDIO_API_KEY 或使用 --api-key，参见 https://senseaudio.cn/docs/)", file=sys.stderr)
        else:
            voice_out = args.voice_out
            if not voice_out:
                safe_kw = "".join(c if c.isalnum() or c in " _-" else "_" for c in keyword)[:30]
                voice_out = str(report_path.parent / f"media_cluster_voice_{safe_kw}.mp3")
            audio_path = tts_senseaudio(voice_script, api_key, voice_id=args.voice_id, output_path=voice_out)
            if audio_path:
                print(f"(TTS 已保存: {audio_path})")
                if play_audio(audio_path):
                    print("(已播放)")
            else:
                print("(TTS 生成失败，请查看上方错误信息)")


if __name__ == "__main__":
    main()
