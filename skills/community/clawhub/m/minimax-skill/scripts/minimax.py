#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
AUDIO_SCRIPT = SKILL_DIR / "generate_audio.py"
IMAGE_SCRIPT = SKILL_DIR / "generate_image.py"
VIDEO_SCRIPT = SKILL_DIR / "generate_video.py"


def run(script: Path, args: list[str]) -> int:
    command = [sys.executable, str(script), *args]
    completed = subprocess.run(command)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified MiniMax entrypoint")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    audio = subparsers.add_parser("audio", help="Generate audio")
    audio.add_argument("--text", required=True)
    audio.add_argument("--output", required=True)
    audio.add_argument("--model", default="speech-2.8-turbo")
    audio.add_argument("--voice-id", default=None)
    audio.add_argument("--output-format", default="hex", choices=["hex", "url"])

    image = subparsers.add_parser("image", help="Generate image")
    image.add_argument("--prompt", required=True)
    image.add_argument("--output", required=True)
    image.add_argument("--model", default="image-01")
    image.add_argument("--aspect-ratio", default="1:1")
    image.add_argument("--image-file", default=None)
    image.add_argument("--n", type=int, default=1)

    video = subparsers.add_parser("video", help="Generate video")
    video.add_argument("--prompt", required=True)
    video.add_argument("--output", required=True)
    video.add_argument("--model", default="MiniMax-Hailuo-2.3")
    video.add_argument("--first-frame-image", default=None)
    video.add_argument("--last-frame-image", default=None)
    video.add_argument("--subject-reference", default=None)
    video.add_argument("--timeout", type=int, default=1800)

    args = parser.parse_args()

    if args.mode == "audio":
        forwarded = [
            "--text", args.text,
            "--output", args.output,
            "--model", args.model,
            "--output-format", args.output_format,
        ]
        if args.voice_id:
            forwarded.extend(["--voice-id", args.voice_id])
        return run(AUDIO_SCRIPT, forwarded)

    if args.mode == "image":
        forwarded = [
            "--prompt", args.prompt,
            "--output", args.output,
            "--model", args.model,
            "--aspect-ratio", args.aspect_ratio,
            "--n", str(args.n),
        ]
        if args.image_file:
            forwarded.extend(["--image-file", args.image_file])
        return run(IMAGE_SCRIPT, forwarded)

    forwarded = [
        "--prompt", args.prompt,
        "--output", args.output,
        "--model", args.model,
        "--timeout", str(args.timeout),
    ]
    if args.first_frame_image:
        forwarded.extend(["--first-frame-image", args.first_frame_image])
    if args.last_frame_image:
        forwarded.extend(["--last-frame-image", args.last_frame_image])
    if args.subject_reference:
        forwarded.extend(["--subject-reference", args.subject_reference])
    return run(VIDEO_SCRIPT, forwarded)


if __name__ == "__main__":
    raise SystemExit(main())
