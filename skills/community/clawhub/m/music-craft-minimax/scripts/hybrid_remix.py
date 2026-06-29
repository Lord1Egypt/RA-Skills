#!/usr/bin/env python3
"""Experimental stem remix planner for MiniMax arranger research.

The safe default requires a pre-validated transformed stem. Passing an isolated
stem to MiniMax cover is not documented as reliable, so this helper only builds
that command when --allow-stem-cover is explicitly set.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MIX_ORDER = ("vocals", "drums", "bass", "other")


def _load_stems(stems_json: Path) -> dict[str, Path]:
    data = json.loads(stems_json.read_text(encoding="utf-8"))
    raw_stems = data.get("stems")
    if not isinstance(raw_stems, dict):
        raise ValueError("stems.json must contain a 'stems' object")
    return {name: Path(path) for name, path in raw_stems.items()}


def _build_cover_command(
    source_stem: Path,
    prompt: str,
    transformed_stem: Path,
    expected_duration_seconds: int | None,
    overwrite: bool,
) -> list[str]:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "generate_with_retry.py"),
        "--output-path",
        str(transformed_stem),
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
            prompt,
            "--audio-file",
            str(source_stem),
            "--out",
            str(transformed_stem),
        ]
    )
    return command


def _build_mix_command(stems: dict[str, Path], target_stem: str, replacement: Path, output: Path) -> list[str]:
    inputs = []
    filter_inputs = []
    for index, stem_name in enumerate(MIX_ORDER):
        stem_path = replacement if stem_name == target_stem else stems.get(stem_name)
        if stem_path is None:
            raise ValueError(f"missing required stem: {stem_name}")
        inputs.extend(["-i", str(stem_path)])
        filter_inputs.append(f"[{index}:a]")
    return [
        "ffmpeg",
        "-y",
        *inputs,
        "-filter_complex",
        f"{''.join(filter_inputs)}amix=inputs={len(MIX_ORDER)}:duration=longest:normalize=0",
        str(output),
    ]


def _validate_source_stems(stems: dict[str, Path]) -> None:
    for stem_name in MIX_ORDER:
        stem_path = stems.get(stem_name)
        if stem_path is None:
            raise ValueError(f"missing required stem: {stem_name}")
        if not stem_path.exists():
            raise FileNotFoundError(f"source stem not found: {stem_path}")


def build_plan(
    stems_json: Path,
    target_stem: str,
    prompt: str,
    output: Path,
    transformed_stem: Path | None,
    allow_stem_cover: bool,
    expected_duration_seconds: int | None = None,
    overwrite: bool = False,
) -> dict[str, object]:
    stems = _load_stems(stems_json)
    if target_stem not in stems:
        raise ValueError(f"target stem {target_stem!r} not found in stems.json")
    _validate_source_stems(stems)

    cover_command = None
    if transformed_stem is None:
        if not allow_stem_cover:
            raise ValueError(
                "Refusing stem-only MiniMax cover without --allow-stem-cover; "
                "provide --transformed-stem from a validated source instead."
            )
        transformed_stem = output.with_name(f"{output.stem}_{target_stem}_cover.mp3")
        cover_command = _build_cover_command(
            stems[target_stem],
            prompt,
            transformed_stem,
            expected_duration_seconds,
            overwrite,
        )
    elif not transformed_stem.exists():
        raise FileNotFoundError(f"transformed stem not found: {transformed_stem}")

    mix_command = _build_mix_command(stems, target_stem, transformed_stem, output)
    return {
        "status": "planned",
        "target_stem": target_stem,
        "stems_json": str(stems_json),
        "transformed_stem": str(transformed_stem),
        "output": str(output),
        "cover_command": cover_command,
        "mix_command": mix_command,
        "warnings": [
            "Experimental preview only; ffmpeg amix is not production mixing.",
            "Do not use stem-only MiniMax cover unless the output is duration-aligned and stem-like.",
        ],
    }


def _run(command: list[str]) -> int:
    return subprocess.run(command, text=True).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan or run an experimental hybrid stem remix")
    parser.add_argument("--stems-json", required=True, type=Path)
    parser.add_argument("--target-stem", required=True, choices=MIX_ORDER)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--transformed-stem", type=Path)
    parser.add_argument("--allow-stem-cover", action="store_true")
    parser.add_argument("--expected-duration-seconds", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    plan = build_plan(
        stems_json=args.stems_json.expanduser(),
        target_stem=args.target_stem,
        prompt=args.prompt,
        output=args.output.expanduser(),
        transformed_stem=args.transformed_stem.expanduser() if args.transformed_stem else None,
        allow_stem_cover=args.allow_stem_cover,
        expected_duration_seconds=args.expected_duration_seconds,
        overwrite=args.overwrite,
    )
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    if args.dry_run:
        return 0
    if plan["cover_command"] is not None:
        rc = _run(plan["cover_command"])  # type: ignore[arg-type]
        if rc != 0:
            return rc
    return _run(plan["mix_command"])  # type: ignore[arg-type]


if __name__ == "__main__":
    raise SystemExit(main())
