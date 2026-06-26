#!/usr/bin/env python3
import argparse
import csv
import subprocess
from pathlib import Path


def read_timings(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    required = {"slide", "start_sec", "end_sec", "duration_sec"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"Timing CSV missing columns: {sorted(missing)}")

    normalized = []
    for row in rows:
        slide = int(row["slide"])
        start = float(row["start_sec"])
        end = float(row["end_sec"])
        duration = float(row["duration_sec"])
        if end < start:
            raise SystemExit(f"Invalid timing row for slide {slide}: end before start")
        if abs((end - start) - duration) > 0.05:
            raise SystemExit(
                f"Invalid timing row for slide {slide}: duration does not match end-start"
            )
        normalized.append(
            {
                "slide": slide,
                "start_sec": start,
                "end_sec": end,
                "duration_sec": duration,
            }
        )
    return normalized


def find_slide_images(images_dir: Path):
    files = sorted(
        path
        for path in images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    if not files:
        raise SystemExit(f"No slide images found in {images_dir}")
    return files


def validate_sequence(timings, images):
    if len(timings) != len(images):
        raise SystemExit(
            f"Slide/image count mismatch: {len(timings)} timing rows vs {len(images)} images"
        )

    expected_slide = 1
    previous_end = None
    for row in timings:
        if row["slide"] != expected_slide:
            raise SystemExit(
                f"Timing CSV must use sequential slide numbers starting at 1; got {row['slide']}"
            )
        if previous_end is not None and abs(row["start_sec"] - previous_end) > 0.05:
            raise SystemExit(
                f"Gap or overlap near slide {row['slide']}: start={row['start_sec']}, previous_end={previous_end}"
            )
        previous_end = row["end_sec"]
        expected_slide += 1


def write_ffconcat(images, timings, output: Path):
    lines = ["ffconcat version 1.0"]
    for image, row in zip(images, timings):
        lines.append(f"file '{image.resolve()}'")
        lines.append(f"duration {row['duration_sec']:.3f}")
    lines.append(f"file '{images[-1].resolve()}'")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_ffmpeg(ffconcat_path: Path, audio_path: Path, output_path: Path, overwrite: bool):
    cmd = [
        "ffmpeg",
        "-y" if overwrite else "-n",
        "-safe",
        "0",
        "-f",
        "concat",
        "-i",
        str(ffconcat_path),
        "-i",
        str(audio_path),
        "-vf",
        "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Render a slide-based video from images, audio, and a timing CSV."
    )
    parser.add_argument("--images", required=True, help="Directory containing slide images.")
    parser.add_argument("--timings", required=True, help="Timing CSV path.")
    parser.add_argument("--audio", required=True, help="Audio file path.")
    parser.add_argument("--output", required=True, help="Output MP4 path.")
    parser.add_argument(
        "--ffconcat-out",
        help="Optional output path for the generated ffconcat file. Defaults next to the timing CSV.",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Fail if the output file already exists.",
    )
    args = parser.parse_args()

    images_dir = Path(args.images).expanduser().resolve()
    timings_path = Path(args.timings).expanduser().resolve()
    audio_path = Path(args.audio).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    ffconcat_path = (
        Path(args.ffconcat_out).expanduser().resolve()
        if args.ffconcat_out
        else timings_path.with_suffix(".ffconcat")
    )

    if not images_dir.exists():
        raise SystemExit(f"Images directory not found: {images_dir}")
    if not timings_path.exists():
        raise SystemExit(f"Timing CSV not found: {timings_path}")
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")

    timings = read_timings(timings_path)
    images = find_slide_images(images_dir)
    validate_sequence(timings, images)

    ffconcat_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_ffconcat(images, timings, ffconcat_path)
    run_ffmpeg(ffconcat_path, audio_path, output_path, overwrite=not args.no_overwrite)

    print(f"FFCONCAT_FILE={ffconcat_path}")
    print(f"OUTPUT_VIDEO={output_path}")
    print(f"SLIDE_COUNT={len(images)}")


if __name__ == "__main__":
    main()
