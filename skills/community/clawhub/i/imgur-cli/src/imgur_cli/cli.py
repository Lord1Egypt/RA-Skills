import argparse
import json
import sys
from typing import Any

from . import core


def _print(obj: Any) -> None:
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main() -> None:
    p = argparse.ArgumentParser(
        prog="imgur-cli",
        description="Imgur API CLI (anonymous Client-ID or OAuth access token)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    up = sub.add_parser("upload", help="Upload an image (file path or URL)")
    up.add_argument("source", help="Local file path or http(s) URL")
    up.add_argument("--title")
    up.add_argument("--description")
    up.add_argument("--album", help="Album hash to attach the image to")

    g = sub.add_parser("get", help="Get image metadata by image hash/id")
    g.add_argument("image_hash")

    d = sub.add_parser("delete", help="Delete image by delete-hash (anonymous) or id (authenticated)")
    d.add_argument("delete_hash_or_id")

    ac = sub.add_parser("album-create", help="Create a new album")
    ac.add_argument("--title")
    ac.add_argument("--description")
    ac.add_argument("--privacy", choices=["public", "hidden", "secret"])
    ac.add_argument("--image", action="append", dest="image_ids", default=[], help="Image id; repeatable")

    aa = sub.add_parser("album-add", help="Add images to an existing album")
    aa.add_argument("album_hash")
    aa.add_argument("--image", action="append", dest="image_ids", default=[], required=True, help="Image id; repeatable")

    args = p.parse_args()

    try:
        if args.cmd == "upload":
            _print(core.upload_image(args.source, title=args.title, description=args.description, album=args.album))
        elif args.cmd == "get":
            _print(core.get_image(args.image_hash))
        elif args.cmd == "delete":
            _print(core.delete_image(args.delete_hash_or_id))
        elif args.cmd == "album-create":
            _print(core.create_album(title=args.title, description=args.description, privacy=args.privacy, image_ids=args.image_ids or None))
        elif args.cmd == "album-add":
            _print(core.add_to_album(args.album_hash, args.image_ids))
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
