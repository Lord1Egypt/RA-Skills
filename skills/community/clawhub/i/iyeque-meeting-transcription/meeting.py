#!/usr/bin/env python3
"""Create local Whisper transcripts, subtitles, and deterministic meeting notes."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 2 * 1024 * 1024 * 1024
MAX_SEGMENTS = 100_000
MODELS = {"tiny", "base", "small", "medium", "large", "turbo"}
ACTION_RE = re.compile(r"\b(?:action item|todo|to-do|follow up|follow-up|next step|owner|assigned to)\b[:\s-]*(.+)", re.I)


def workspace_path(raw: str, workspace: Path) -> Path:
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = workspace / candidate
    resolved = candidate.resolve(strict=True)
    if resolved != workspace and workspace not in resolved.parents:
        raise ValueError("input/output paths must stay inside the current workspace")
    return resolved


def safe_output_dir(raw: str, workspace: Path) -> Path:
    candidate = workspace_path(raw, workspace) if Path(raw).exists() else (workspace / raw).resolve()
    if candidate != workspace and workspace not in candidate.parents:
        raise ValueError("output directory must stay inside the current workspace")
    candidate.mkdir(parents=True, exist_ok=True)
    return candidate


def timestamp(seconds: float) -> str:
    total_ms = max(0, round(float(seconds) * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def srt(segments: list[dict[str, Any]]) -> str:
    blocks = []
    for number, segment in enumerate(segments, 1):
        blocks.append(f"{number}\n{timestamp(segment['start'])} --> {timestamp(segment['end'])}\n{segment['text'].strip()}\n")
    return "\n".join(blocks)


def action_candidates(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = []
    for segment in segments:
        match = ACTION_RE.search(segment.get("text", ""))
        if match:
            actions.append({"timestamp": timestamp(segment["start"]), "text": match.group(1).strip()})
    return actions


def markdown(result: dict[str, Any], actions: list[dict[str, Any]]) -> str:
    lines = ["# Meeting transcript", "", f"- **Language:** {result.get('language') or 'auto'}", f"- **Duration:** {result.get('duration_seconds', 0):.2f}s", "", "## Action-item candidates"]
    if actions:
        lines.extend(f"- `{item['timestamp']}` {item['text']}" for item in actions)
    else:
        lines.append("- None detected by the deterministic action-item pattern matcher.")
    lines.extend(["", "## Transcript", ""])
    for segment in result["segments"]:
        lines.append(f"**{timestamp(segment['start'])}** {segment['text'].strip()}")
    return "\n".join(lines) + "\n"


def transcribe(args: argparse.Namespace, workspace: Path) -> int:
    input_path = workspace_path(args.input, workspace)
    if not input_path.is_file() or input_path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("input must be a regular file no larger than 2 GiB")
    output_dir = safe_output_dir(args.output_dir, workspace)
    try:
        import whisper  # type: ignore
    except ImportError as exc:
        raise RuntimeError("openai-whisper is required; install it before running this workflow") from exc
    model = whisper.load_model(args.model)
    options = {"fp16": False, "verbose": False}
    if args.language:
        options["language"] = args.language
    if args.include_word_timestamps:
        options["word_timestamps"] = True
    raw = model.transcribe(str(input_path), **options)
    raw_segments = raw.get("segments", [])[:MAX_SEGMENTS]
    segments = [{"id": i, "start": float(x.get("start", 0)), "end": float(x.get("end", 0)), "text": str(x.get("text", "")).strip()} for i, x in enumerate(raw_segments)]
    result = {"input": input_path.name, "language": raw.get("language"), "text": str(raw.get("text", "")).strip(), "duration_seconds": segments[-1]["end"] if segments else 0, "segments": segments}
    actions = action_candidates(segments)
    outputs = []
    if args.format in {"all", "json"}:
        (output_dir / "transcript.json").write_text(json.dumps({**result, "action_item_candidates": actions}, indent=2, ensure_ascii=False) + "\n")
        outputs.append("transcript.json")
    if args.format in {"all", "srt"}:
        (output_dir / "transcript.srt").write_text(srt(segments))
        outputs.append("transcript.srt")
    if args.format in {"all", "markdown"}:
        (output_dir / "notes.md").write_text(markdown(result, actions))
        outputs.append("notes.md")
    print(json.dumps({"ok": True, "output_dir": str(output_dir.relative_to(workspace)), "files": outputs, "segments": len(segments), "action_item_candidates": len(actions)}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Create local Whisper transcripts, subtitles, and meeting notes")
    parser.add_argument("--input", required=True, help="Audio/video file inside the current workspace")
    parser.add_argument("--model", choices=sorted(MODELS), default="base")
    parser.add_argument("--language", help="Optional language code, e.g. en")
    parser.add_argument("--output-dir", default="meeting-output")
    parser.add_argument("--format", choices=["all", "json", "srt", "markdown"], default="all")
    parser.add_argument("--include-word-timestamps", action="store_true")
    args = parser.parse_args()
    workspace = Path.cwd().resolve()
    try:
        return transcribe(args, workspace)
    except (ValueError, RuntimeError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
