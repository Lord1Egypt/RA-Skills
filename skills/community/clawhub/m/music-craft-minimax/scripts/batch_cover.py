#!/usr/bin/env python3
"""Run MiniMax cover prompts sequentially through generate_with_retry.py.

This helper batches the operator workflow without changing the MiniMax safety
contract: one cover at a time, explicit output paths, verify each output before
continuing. Use --dry-run to inspect commands without credentials or quota.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_name(value: str) -> str:
    cleaned = SAFE_NAME_RE.sub("_", value.strip()).strip("._-")
    return cleaned or "cover"


def _load_prompts(prompts_file: Path) -> list[dict[str, str]]:
    data = json.loads(prompts_file.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("prompts file must be a JSON list")

    prompts: list[dict[str, str]] = []
    for index, item in enumerate(data, start=1):
        if isinstance(item, str):
            name = f"cover_{index:02d}"
            prompt = item
        elif isinstance(item, dict):
            prompt = str(item.get("prompt", "")).strip()
            name = str(item.get("name") or f"cover_{index:02d}")
        else:
            raise ValueError(f"prompt item {index} must be a string or object")
        if not prompt:
            raise ValueError(f"prompt item {index} is missing prompt text")
        prompts.append({"name": _safe_name(name), "prompt": prompt})
    return prompts


def _ffprobe_duration_seconds(path: Path) -> float | None:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def build_cover_commands(
    audio_file: Path,
    prompts_file: Path,
    out_dir: Path,
    expected_duration_seconds: int | None = None,
    overwrite: bool = False,
) -> list[dict[str, object]]:
    if not audio_file.exists():
        raise FileNotFoundError(f"audio file not found: {audio_file}")
    prompts = _load_prompts(prompts_file)
    out_dir.mkdir(parents=True, exist_ok=True)

    commands: list[dict[str, object]] = []
    for item in prompts:
        output = out_dir / f"{item['name']}.mp3"
        command = [
            sys.executable,
            str(SCRIPT_DIR / "generate_with_retry.py"),
            "--output-path",
            str(output),
        ]
        if expected_duration_seconds is not None:
            command.extend(["--expected-duration-seconds", str(expected_duration_seconds)])
        if overwrite:
            command.append("--overwrite")
        command.extend(
            [
                "--",
                "music",
                "cover",
                "--prompt",
                str(item["prompt"]),
                "--audio-file",
                str(audio_file),
                "--out",
                str(output),
            ]
        )
        commands.append({"name": item["name"], "output": str(output), "command": command})
    return commands


def run_batch(commands: list[dict[str, object]], dry_run: bool = False) -> int:
    results: list[dict[str, object]] = []
    for item in commands:
        command = list(item["command"])  # type: ignore[arg-type]
        output = Path(str(item["output"]))
        if dry_run:
            status = "dry_run"
            returncode = 0
        else:
            result = subprocess.run(command, text=True)
            returncode = result.returncode
            status = "ok" if returncode == 0 and output.exists() and output.stat().st_size > 0 else "failed"
            if status != "ok":
                results.append(
                    {
                        "name": item["name"],
                        "status": status,
                        "returncode": returncode,
                        "output": str(output),
                        "duration_seconds": None,
                    }
                )
                print(json.dumps({"results": results}, indent=2), file=sys.stderr)
                return returncode or 1
        duration = _ffprobe_duration_seconds(output) if output.exists() else None
        results.append(
            {
                "name": item["name"],
                "status": status,
                "returncode": returncode,
                "output": str(output),
                "duration_seconds": duration,
                "command": command if dry_run else None,
            }
        )
    print(json.dumps({"results": results}, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run MiniMax cover prompts sequentially")
    parser.add_argument("--audio-file", required=True, type=Path, help="Source audio for cover")
    parser.add_argument("--prompts", required=True, type=Path, help="JSON list of prompt objects")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for cover outputs")
    parser.add_argument("--expected-duration-seconds", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without calling mmx")
    args = parser.parse_args(argv)

    commands = build_cover_commands(
        audio_file=args.audio_file.expanduser(),
        prompts_file=args.prompts.expanduser(),
        out_dir=args.out_dir.expanduser(),
        expected_duration_seconds=args.expected_duration_seconds,
        overwrite=args.overwrite,
    )
    # Keep env access explicit for real runs; dry-run must work without credentials.
    if not args.dry_run and not os.environ.get("MINIMAX_API_KEY"):
        print("ERROR: MINIMAX_API_KEY is required for real MiniMax cover runs", file=sys.stderr)
        return 2
    return run_batch(commands, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
