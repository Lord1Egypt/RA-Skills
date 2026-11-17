#!/usr/bin/env python3
"""Generate a video from a text prompt with Magic Hour.

Prints one JSON object: {project_id, status, model, url, urls, credits_charged, width, height, fps}
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prompt", help="What the video should show (be specific: subject, motion, camera, style)")
    p.add_argument("--model", default=c.DEFAULT_VIDEO_MODEL, help="Video model id (default: wan-2.2, free)")
    p.add_argument("--duration", type=int, default=5, help="Seconds (must be allowed by the model; default 5)")
    p.add_argument("--resolution", default="480p", choices=c.RESOLUTIONS)
    p.add_argument("--aspect-ratio", default="16:9", choices=c.ASPECT_RATIOS)
    p.add_argument("--audio", action="store_true", help="Request audio (veo3.1-audio etc.)")
    p.add_argument("--name", default=None, help="Project name for your records")
    p.add_argument("--download-dir", default=None, help="Download the mp4 into this directory")
    p.add_argument("--no-wait", action="store_true", help="Return immediately with status=queued")
    p.add_argument("--timeout", type=float, default=None, help="HTTP timeout seconds")
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    warn = c.validate_video(args.model, args.duration, args.resolution)
    if warn:
        print(f"warning: {warn}", file=sys.stderr)

    def go():
        client = c.get_client(timeout=args.timeout)
        kwargs = dict(
            end_seconds=float(args.duration),
            style={"prompt": args.prompt},
            model=args.model,
            resolution=args.resolution,
            aspect_ratio=args.aspect_ratio,
            name=args.name or f"clawhub: {args.prompt[:60]}",
            wait_for_completion=not args.no_wait,
            **c.download_kwargs(args.download_dir),
        )
        if args.audio:
            kwargs["audio"] = True
        resp = client.v1.text_to_video.generate(**kwargs)
        out = c.serialize(resp, model=args.model, kind="video")
        out["estimated_credits"] = c.estimate_credits(args.model, args.duration)
        return out

    c.run(go)


if __name__ == "__main__":
    main()
