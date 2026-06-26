"""
text -> image, via any OpenAI-compatible image-generate endpoint.

usage:
    python generate.py "a red panda holding a soldering iron, studio light"
    python generate.py "..." --size 1024x1024 --n 2 --tag panda
"""

import argparse
import base64
import datetime as dt
import re
import sys
from pathlib import Path

from openai import OpenAI

API_KEY = "xxx"
BASE_URL = "https://api.bianxie.ai/v1"
# bianxie: gpt-image-2 调用方式与 gpt-image-1 完全一致 (官方教程
# https://bianxieai.com/how-to-use-gpt-image-1.html), 只是模型名不同。
# 想退回到 -1 试对比, --model gpt-image-1。
DEFAULT_MODEL = "gpt-image-2"
OUT_DIR = Path(__file__).parent / "outputs"


def slug(text: str, n: int = 24) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:n] or "img"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", help="text prompt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--size", default="1024x1024",
                    help="1024x1024 / 1024x1536 / 1536x1024 / auto; "
                         "gpt-image-2 also takes larger (e.g. 2048x2048) up to 3840 max edge")
    ap.add_argument("--n", type=int, default=1, help="how many images")
    ap.add_argument("--quality", default="medium",
                    choices=["low", "medium", "high", "auto"])
    ap.add_argument("--background", default=None,
                    choices=[None, "transparent", "opaque", "auto"],
                    help="optional; pass 'transparent' to get png with alpha")
    ap.add_argument("--tag", default="", help="short label baked into filename")
    ap.add_argument("--out-dir", default=None,
                    help="override output dir (default <script>/outputs)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    print(f"[gen] model={args.model} size={args.size} n={args.n} quality={args.quality}", file=sys.stderr)
    print(f"[gen] prompt={args.prompt!r}", file=sys.stderr)

    kwargs = dict(
        model=args.model,
        prompt=args.prompt,
        size=args.size,
        n=args.n,
        quality=args.quality,
        response_format="b64_json",  # OpenAI default is "url"; force b64 so we can save locally
    )
    if args.background:
        kwargs["background"] = args.background
    resp = client.images.generate(**kwargs)

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    label = args.tag or slug(args.prompt)
    saved = []
    for i, item in enumerate(resp.data):
        if not item.b64_json:
            print(f"[gen] WARN: item {i} has no b64_json (url={item.url})", file=sys.stderr)
            continue
        path = out_dir / f"{ts}_{label}_{i}.png"
        path.write_bytes(base64.b64decode(item.b64_json))
        saved.append(path)
        print(f"[gen] saved -> {path}", file=sys.stderr)
        print(path)  # stdout: callers can capture the path

    if not saved:
        raise SystemExit("[gen] no images returned")


if __name__ == "__main__":
    main()
