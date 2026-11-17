#!/usr/bin/env python3
"""Generate one or more images from a text prompt with Magic Hour.

Prints one JSON object: {project_id, status, model, url, urls, credits_charged}
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prompt", help="Image description")
    p.add_argument("--model", default=c.DEFAULT_IMAGE_MODEL, help="Image model id: " + ", ".join(c.IMAGE_MODELS))
    p.add_argument("--count", type=int, default=1, help="Number of images (1-4)")
    p.add_argument("--aspect-ratio", default="16:9", choices=c.ASPECT_RATIOS)
    p.add_argument("--name", default=None)
    p.add_argument("--download-dir", default=None, help="Download the images into this directory")
    p.add_argument("--no-wait", action="store_true")
    p.add_argument("--timeout", type=float, default=None)
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    if args.model not in c.IMAGE_MODELS:
        print(f"warning: unknown image model '{args.model}'; passing through", file=sys.stderr)

    def go():
        client = c.get_client(timeout=args.timeout)
        resp = client.v1.ai_image_generator.generate(
            image_count=args.count,
            style={"prompt": args.prompt},
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            name=args.name or f"clawhub image: {args.prompt[:60]}",
            wait_for_completion=not args.no_wait,
            **c.download_kwargs(args.download_dir),
        )
        return c.serialize(resp, model=args.model, kind="image")

    c.run(go)


if __name__ == "__main__":
    main()
