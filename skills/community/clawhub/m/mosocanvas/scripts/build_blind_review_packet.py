#!/usr/bin/env python3
"""Build a prompt-blind HTML packet from image artifacts."""

from __future__ import annotations

import argparse
import hashlib
import html
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", default="Blind artifact review")
    args = parser.parse_args()

    missing = [str(path) for path in args.images if not path.exists()]
    if missing:
        parser.error("missing images: " + ", ".join(missing))

    cards = []
    for index, path in enumerate(args.images, start=1):
        absolute = path.resolve()
        cards.append(
            "<article>"
            f"<h2>Frame {index:02d}</h2>"
            f"<img src=\"{html.escape(absolute.as_uri())}\" alt=\"Frame {index:02d}\">"
            f"<p>sha256 {digest(absolute)}</p>"
            "</article>"
        )
    document = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(args.title)}</title>
<style>
body{{margin:32px;background:#111;color:#eee;font:14px system-ui}}
main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}
article{{background:#1c1c1c;padding:16px}} img{{width:100%;height:auto;display:block}}
p{{font-family:ui-monospace,monospace;font-size:10px;overflow-wrap:anywhere;color:#aaa}}
</style>
<h1>{html.escape(args.title)}</h1>
<p>Prompt, intended interpretation, generator, and self-review intentionally omitted.</p>
<main>{''.join(cards)}</main>
</html>
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
