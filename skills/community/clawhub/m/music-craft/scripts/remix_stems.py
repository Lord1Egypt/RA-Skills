#!/usr/bin/env python3
"""Preview-quality stem remix helper using ffmpeg amix.

Runs `ffmpeg` with an explicit argument list (no shell), only on stem files
listed in a local `stems.json`, and never overwrites an existing output unless
`--overwrite` is passed.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_ORDER = ("vocals", "drums", "bass", "other")


def load_stems_json(stems_json: Path) -> dict[str, Path]:
    data = json.loads(stems_json.read_text(encoding="utf-8"))
    raw = data.get("stems")
    if not isinstance(raw, dict):
        raise ValueError("stems.json must contain a 'stems' object")
    stems = {name: Path(path) for name, path in raw.items()}
    missing = [name for name in DEFAULT_ORDER if name not in stems]
    if missing:
        raise ValueError(f"missing required stems: {', '.join(missing)}")
    return stems


def _safe_path_arg(path: Path) -> str:
    """Path as an ffmpeg argument that can never be read as an option."""
    text = str(path)
    return f"./{text}" if text.startswith("-") else text


def build_ffmpeg_command(
    stems: dict[str, Path],
    output: Path,
    order: tuple[str, ...] = DEFAULT_ORDER,
    overwrite: bool = False,
) -> list[str]:
    inputs: list[str] = []
    filter_inputs: list[str] = []
    for index, stem_name in enumerate(order):
        stem_path = stems[stem_name]
        if not stem_path.exists():
            raise FileNotFoundError(f"stem not found: {stem_path}")
        if not stem_path.is_file():
            raise ValueError(f"stem is not a regular file: {stem_path}")
        inputs.extend(["-i", _safe_path_arg(stem_path)])
        filter_inputs.append(f"[{index}:a]")
    return [
        "ffmpeg",
        "-y" if overwrite else "-n",
        *inputs,
        "-filter_complex",
        f"{''.join(filter_inputs)}amix=inputs={len(order)}:duration=longest:normalize=0",
        _safe_path_arg(output),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mix stems into a preview-quality output")
    parser.add_argument("--stems-json", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true", help="replace an existing output file")
    args = parser.parse_args(argv)

    try:
        stems = load_stems_json(args.stems_json.expanduser())
        output = args.output.expanduser()
        if output.exists() and not args.overwrite:
            raise FileExistsError(f"output exists: {output} (pass --overwrite to replace it)")
        command = build_ffmpeg_command(stems, output, overwrite=args.overwrite)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    if args.dry_run:
        print(json.dumps({"status": "dry_run", "command": command}, indent=2, ensure_ascii=False))
        return 0
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        print(json.dumps({"status": "error", "error": "ffmpeg not found on PATH"}, indent=2), file=sys.stderr)
        return 1
    print("WARNING: ffmpeg amix is preview-quality, not DAW-quality mixing.", file=sys.stderr)
    return subprocess.run([ffmpeg, *command[1:]], shell=False, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
