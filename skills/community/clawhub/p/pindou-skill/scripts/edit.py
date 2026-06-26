"""
image + prompt -> image, via any OpenAI-compatible image-edit endpoint.

usage:
    python edit.py path/to/in.png "make the background transparent"
    python edit.py in.png "add a cyberpunk skyline behind the subject" \\
        --mask mask.png --size 1024x1024 --tag cyberpunk
"""

import argparse
import base64
import datetime as dt
import os
import re
import sys
from pathlib import Path

from openai import OpenAI

# Default endpoint targets bianxie's OpenAI-compatible relay (gpt-image-2).
# Switch to https://api.openai.com/v1 + gpt-image-1 for the official API.
DEFAULT_BASE_URL = "https://api.bianxie.ai/v1"
DEFAULT_MODEL = "gpt-image-2"
OUT_DIR = Path(__file__).parent / "outputs"


def resolve_api_key(cli_key: str | None) -> str:
    if cli_key:
        return cli_key
    for var in ("OPENAI_API_KEY", "BIANXIE_API_KEY", "IMAGE_API_KEY"):
        v = os.environ.get(var)
        if v:
            return v
    raise SystemExit(
        "[edit] no API key. Pass --api-key, or export OPENAI_API_KEY / "
        "BIANXIE_API_KEY / IMAGE_API_KEY."
    )


def slug(text: str, n: int = 24) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:n] or "edit"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="input image path (png recommended)")
    ap.add_argument("prompt", help="edit instruction")
    ap.add_argument("--mask", default=None,
                    help="optional mask png; transparent areas = edit zone")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--size", default="1024x1024",
                    help="1024x1024 / 1024x1536 / 1536x1024 / auto")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--quality", default="medium",
                    choices=["low", "medium", "high", "auto"])
    ap.add_argument("--background", default=None,
                    choices=[None, "transparent", "opaque", "auto"])
    ap.add_argument("--tag", default="")
    ap.add_argument("--out-dir", default=None,
                    help="override output dir (default <script>/outputs)")
    ap.add_argument("--api-key", default=None,
                    help="API key; falls back to OPENAI_API_KEY / "
                         "BIANXIE_API_KEY / IMAGE_API_KEY env vars")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL),
                    help=f"OpenAI-compatible base url (default {DEFAULT_BASE_URL}, "
                         "or $OPENAI_BASE_URL)")
    args = ap.parse_args()

    img_path = Path(args.image)
    if not img_path.is_file():
        raise SystemExit(f"[edit] not found: {img_path}")

    out_dir = Path(args.out_dir) if args.out_dir else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    api_key = resolve_api_key(args.api_key)
    client = OpenAI(api_key=api_key, base_url=args.base_url)

    print(f"[edit] model={args.model} size={args.size} n={args.n}", file=sys.stderr)
    print(f"[edit] image={img_path}", file=sys.stderr)
    print(f"[edit] prompt={args.prompt!r}", file=sys.stderr)
    if args.mask:
        print(f"[edit] mask={args.mask}", file=sys.stderr)

    files = [open(img_path, "rb")]
    mask_fh = open(args.mask, "rb") if args.mask else None
    try:
        kwargs = dict(
            model=args.model,
            image=files,
            prompt=args.prompt,
            size=args.size,
            n=args.n,
            quality=args.quality,
            response_format="b64_json",
        )
        if args.background:
            kwargs["background"] = args.background
        if mask_fh is not None:
            kwargs["mask"] = mask_fh
        resp = client.images.edit(**kwargs)
    finally:
        for f in files:
            f.close()
        if mask_fh is not None:
            mask_fh.close()

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    label = args.tag or f"{img_path.stem}_{slug(args.prompt, 16)}"
    saved = []
    for i, item in enumerate(resp.data):
        if not item.b64_json:
            print(f"[edit] WARN: item {i} has no b64_json (url={item.url})", file=sys.stderr)
            continue
        path = out_dir / f"{ts}_edit_{label}_{i}.png"
        path.write_bytes(base64.b64decode(item.b64_json))
        saved.append(path)
        print(f"[edit] saved -> {path}", file=sys.stderr)
        print(path)  # stdout: callers can capture the path

    if not saved:
        raise SystemExit("[edit] no images returned")


if __name__ == "__main__":
    main()
