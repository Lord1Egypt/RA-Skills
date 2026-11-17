"""Public image upload independent of post publication or editing."""

import sys
import uuid
from pathlib import Path

from echo_cli.compat import subparsers


def configure(commands):
    image = subparsers(commands.add_parser("image"), dest="image_command")
    upload = image.add_parser("upload", help="Upload a public image and return its Markdown URL")
    upload.add_argument("file", type=Path)
    upload.add_argument("--id", type=uuid.UUID, required=True, help="Stable UUID; reuse on retry")


def upload(api, args):
    if not 0 < args.file.stat().st_size <= 5 * 1024 * 1024:
        raise RuntimeError("Image must contain 1 byte to 5 MiB")
    with args.file.open("rb") as stream:
        data = stream.read(5 * 1024 * 1024 + 1)
    if len(data) > 5 * 1024 * 1024:
        raise RuntimeError("Image exceeds 5 MiB")
    print(f"upload_id={args.id}", file=sys.stderr)
    return api.request(
        "PUT",
        f"/v1/images/{args.id}",
        authenticated=True,
        params={"name": args.file.name},
        content=data,
        headers={"Content-Type": "application/octet-stream"},
    )
