#!/usr/bin/env python3
"""Apply a pitch-preserving speech-rate change and record verified metadata."""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def run(command):
    return subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")


def probe_duration(path: Path) -> float:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ]
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def parse_range(value: str):
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*", value)
    if not match:
        raise SystemExit("Use --target-minutes MIN-MAX, for example 6-7")
    low, high = map(float, match.groups())
    if low <= 0 or high < low:
        raise SystemExit("Invalid target duration range")
    return low * 60, high * 60


def choose_speed(duration: float, explicit_speed, target_minutes: str) -> float:
    if explicit_speed is not None and target_minutes:
        raise SystemExit("Choose either --speed or --target-minutes, not both")
    if explicit_speed is not None:
        return explicit_speed
    if not target_minutes:
        return 1.0
    minimum, maximum = parse_range(target_minutes)
    if minimum <= duration <= maximum:
        return 1.0
    if duration > maximum:
        return duration / maximum
    return duration / minimum


def atempo_chain(speed: float) -> str:
    values = []
    remaining = speed
    while remaining > 2.0:
        values.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        values.append(0.5)
        remaining /= 0.5
    values.append(remaining)
    return ",".join(f"atempo={value:.8f}" for value in values)


def supports_rubberband() -> bool:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-filters"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0 and re.search(r"\brubberband\b", result.stdout) is not None


def tempo_filter(speed: float):
    if supports_rubberband():
        return (
            f"rubberband=tempo={speed:.8f}:pitch=1:transients=smooth:detector=soft:"
            "phase=laminar:window=short:smoothing=on:formant=preserved:"
            "pitchq=quality:channels=together",
            "rubberband-formant-preserved",
        )
    return atempo_chain(speed), "ffmpeg-atempo"


def encoder_args(output: Path):
    suffix = output.suffix.lower()
    if suffix == ".mp3":
        return ["-c:a", "libmp3lame", "-b:a", "192k"]
    if suffix in {".m4a", ".aac"}:
        return ["-c:a", "aac", "-b:a", "192k"]
    if suffix == ".wav":
        return ["-c:a", "pcm_s16le"]
    raise SystemExit("Output must be .mp3, .m4a, .aac, or .wav")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--speed", type=float)
    parser.add_argument("--target-minutes", default="")
    parser.add_argument("--min-speed", type=float, default=0.85)
    parser.add_argument("--max-speed", type=float, default=1.35)
    args = parser.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg and ffprobe are required")
    source = Path(args.input).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    report_path = Path(args.report).expanduser().resolve()
    if not source.is_file():
        raise SystemExit("Input audio is missing")

    source_duration = probe_duration(source)
    speed = choose_speed(source_duration, args.speed, args.target_minutes)
    if not args.min_speed <= speed <= args.max_speed:
        raise SystemExit(
            f"Calculated speed {speed:.3f}x is outside the allowed "
            f"{args.min_speed:.2f}-{args.max_speed:.2f} range"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    audio_filter, retiming_method = tempo_filter(speed)
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(source),
        "-vn",
        "-af",
        audio_filter,
        "-ar",
        "48000",
        *encoder_args(output),
        str(output),
    ]
    run(command)
    output_duration = probe_duration(output)
    report = {
        "schema_version": 1,
        "stage": "02-timing",
        "worker": "timing-and-captions",
        "status": "pass",
        "input": source.name,
        "output": output.name,
        "source_duration_seconds": round(source_duration, 3),
        "output_duration_seconds": round(output_duration, 3),
        "speech_rate": round(speed, 5),
        "retiming_method": retiming_method,
        "sample_rate": 48000,
        "issues": [],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
