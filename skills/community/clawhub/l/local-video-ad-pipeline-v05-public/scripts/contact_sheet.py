"""Create a quick visual QA sheet from a video without distorting aspect ratio."""
import argparse
import json
import subprocess
from pathlib import Path


def probe_size(video):
    out = subprocess.check_output([
        "ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(video)
    ], text=True)
    stream = next(s for s in json.loads(out)["streams"] if s["codec_type"] == "video")
    return int(stream["width"]), int(stream["height"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default="contact_sheet.jpg")
    ap.add_argument("--every", type=int, default=5, help="Sample one frame every N seconds.")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--cell", help="Cell size WxH. Default auto: 180x312 for portrait, 416x240 for landscape.")
    args = ap.parse_args()

    width, height = probe_size(args.video)
    if args.cell:
        cell_w, cell_h = [int(x) for x in args.cell.lower().replace("x", ":").split(":", 1)]
    elif height > width:
        cell_w, cell_h = 180, 312
    else:
        cell_w, cell_h = 416, 240

    tile = f"{args.cols}x{args.rows}"
    vf = (
        f"fps=1/{args.every},"
        f"scale={cell_w}:{cell_h}:force_original_aspect_ratio=decrease,"
        f"pad={cell_w}:{cell_h}:(ow-iw)/2:(oh-ih)/2:black,"
        f"tile={tile}"
    )
    cmd = [
        "ffmpeg", "-y", "-i", args.video,
        "-vf", vf,
        "-frames:v", "1", "-update", "1", args.out,
    ]
    subprocess.run(cmd, check=True)
    print(Path(args.out).resolve())


if __name__ == "__main__":
    main()
