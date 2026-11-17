#!/usr/bin/env python3
"""Check a Magic Hour project created with --no-wait. Prints the same JSON shape as the generate scripts."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as c  # noqa: E402


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("project_id")
    p.add_argument("--kind", choices=("video", "image"), default="video")
    p.add_argument("--wait", action="store_true", help="Poll until complete/error")
    p.add_argument("--download-dir", default=None)
    args = p.parse_args(argv)

    def go():
        client = c.get_client()
        res = client.v1.video_projects if args.kind == "video" else client.v1.image_projects
        resp = res.check_result(
            id=args.project_id,
            wait_for_completion=args.wait,
            **c.download_kwargs(args.download_dir),
        )
        return c.serialize(resp, model="", kind=args.kind)

    c.run(go)


if __name__ == "__main__":
    main()
