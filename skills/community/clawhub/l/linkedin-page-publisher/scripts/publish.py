#!/usr/bin/env python3
"""LinkedIn Page Publisher CLI.

Usage:
    python scripts/publish.py text --text "Hello, page"
    python scripts/publish.py image photo.jpg --text "..." --alt "..."
    python scripts/publish.py multi-image a.jpg b.jpg --text "..." --alt "first" "second"
    python scripts/publish.py video demo.mp4 --text "..." --title "Demo"
    python scripts/publish.py article https://example.com --text "..."

Env vars required: LINKEDIN_ACCESS_TOKEN, LINKEDIN_ORG_ID.
Optional: LINKEDIN_API_VERSION (default 202602).

--dry-run prints the computed post body without hitting the API. Media
uploads still happen in non-dry mode — there's no clean way to dry-run
multi-step flows.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make `from lib.X import Y` work whether the user runs this from the skill
# root or from anywhere else.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.client import LinkedInClient, LinkedInAPIError  # noqa: E402
from lib.posts import (  # noqa: E402
    post_text,
    post_image,
    post_multi_image,
    post_video,
    post_article,
    _envelope,
)


def _build_parser() -> argparse.ArgumentParser:
    # `--dry-run` is declared once in this parent parser and attached to each
    # subcommand. It is NOT attached to the top-level parser — argparse's
    # subparser would overwrite the top-level value with its own default,
    # silently turning dry-runs into live API calls. Position-after-subcommand
    # (`publish.py text --dry-run ...`) is the only reliable pattern here.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request body without calling the API. Media is NOT uploaded in dry-run.",
    )

    parser = argparse.ArgumentParser(
        prog="publish.py",
        description="Publish content to a LinkedIn Company Page.",
    )

    subparsers = parser.add_subparsers(dest="kind", required=True)

    p_text = subparsers.add_parser("text", parents=[common], help="Text-only post.")
    p_text.add_argument("--text", required=True)

    p_image = subparsers.add_parser("image", parents=[common], help="Single-image post.")
    p_image.add_argument("image_path")
    p_image.add_argument("--text", required=True)
    p_image.add_argument("--alt", required=True, help="Alt text for accessibility.")

    p_multi = subparsers.add_parser("multi-image", parents=[common], help="Carousel of 2–20 images.")
    p_multi.add_argument("image_paths", nargs="+")
    p_multi.add_argument("--text", required=True)
    p_multi.add_argument(
        "--alt",
        nargs="+",
        required=True,
        help="One alt text string per image, in order.",
    )

    p_video = subparsers.add_parser("video", parents=[common], help="Video post.")
    p_video.add_argument("video_path")
    p_video.add_argument("--text", required=True)
    p_video.add_argument("--title", required=True, help="Video title shown under the post.")

    p_article = subparsers.add_parser("article", parents=[common], help="Post with an article link preview.")
    p_article.add_argument("url")
    p_article.add_argument("--text", required=True)
    p_article.add_argument("--title", help="Override OpenGraph title.")
    p_article.add_argument("--description", help="Override OpenGraph description.")

    return parser


def _dry_run(client: LinkedInClient, args: argparse.Namespace) -> None:
    """Print what the request body would look like, without uploading media."""
    if args.kind == "text":
        body = _envelope(client, args.text)
    elif args.kind == "image":
        body = _envelope(client, args.text, {
            "media": {"id": "urn:li:image:<not uploaded>", "altText": args.alt},
        })
    elif args.kind == "multi-image":
        if len(args.alt) != len(args.image_paths):
            raise SystemExit(
                f"--alt count ({len(args.alt)}) must match image count ({len(args.image_paths)})."
            )
        body = _envelope(client, args.text, {
            "multiImage": {
                "images": [
                    {"id": f"urn:li:image:<not uploaded #{i}>", "altText": alt}
                    for i, alt in enumerate(args.alt)
                ]
            }
        })
    elif args.kind == "video":
        body = _envelope(client, args.text, {
            "media": {"id": "urn:li:video:<not uploaded>", "title": args.title},
        })
    elif args.kind == "article":
        article = {"source": args.url}
        if args.title:
            article["title"] = args.title
        if args.description:
            article["description"] = args.description
        body = _envelope(client, args.text, {"article": article})
    else:
        raise SystemExit(f"Unknown kind: {args.kind}")

    print(json.dumps(body, indent=2, ensure_ascii=False))


def _live(client: LinkedInClient, args: argparse.Namespace) -> str:
    if args.kind == "text":
        return post_text(client, args.text)
    if args.kind == "image":
        return post_image(client, args.image_path, text=args.text, alt=args.alt)
    if args.kind == "multi-image":
        return post_multi_image(
            client, args.image_paths, text=args.text, alts=args.alt
        )
    if args.kind == "video":
        return post_video(client, args.video_path, text=args.text, title=args.title)
    if args.kind == "article":
        return post_article(
            client,
            args.url,
            text=args.text,
            title=args.title,
            description=args.description,
        )
    raise SystemExit(f"Unknown kind: {args.kind}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        client = LinkedInClient()
    except RuntimeError as e:
        print(f"configuration error: {e}", file=sys.stderr)
        return 2

    try:
        if args.dry_run:
            _dry_run(client, args)
            return 0
        post_urn = _live(client, args)
    except LinkedInAPIError as e:
        print(f"LinkedIn API error ({e.status}): {e.body}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"file not found: {e}", file=sys.stderr)
        return 2
    except (ValueError, RuntimeError, TimeoutError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"Published: {post_urn}")
    print(f"  URL: https://www.linkedin.com/feed/update/{post_urn}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
