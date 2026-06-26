"""Validate final local video properties for Shorts/ad delivery."""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(path)
    ], text=True)
    data = json.loads(out)
    stream = next(s for s in data["streams"] if s["codec_type"] == "video")
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "fps": stream.get("avg_frame_rate", ""),
        "duration_s": float(data["format"]["duration"]),
        "path": str(Path(path).resolve()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--orientation", choices=["portrait", "landscape", "any"], default="portrait")
    ap.add_argument("--min-duration", type=float, default=0)
    ap.add_argument("--max-duration", type=float, default=0)
    args = ap.parse_args()

    info = probe(args.video)
    errors = []
    if args.orientation == "portrait" and info["height"] <= info["width"]:
        errors.append(f"expected portrait video, got {info['width']}x{info['height']}")
    if args.orientation == "landscape" and info["width"] <= info["height"]:
        errors.append(f"expected landscape video, got {info['width']}x{info['height']}")
    if args.min_duration and info["duration_s"] + 0.05 < args.min_duration:
        errors.append(f"duration {info['duration_s']:.2f}s < min {args.min_duration:.2f}s")
    if args.max_duration and info["duration_s"] - 0.05 > args.max_duration:
        errors.append(f"duration {info['duration_s']:.2f}s > max {args.max_duration:.2f}s")

    print(json.dumps(info, indent=2, ensure_ascii=False))
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
