#!/usr/bin/env python3
"""Build a deterministic manifest for visual source and output assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:  # Hash and file metadata remain available without image inspection.
    Image = None
    ImageOps = None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect(path: Path, root: Path) -> dict:
    item = {
        "path": str(path.resolve()),
        "relative_path": str(path.resolve().relative_to(root.resolve()))
        if path.resolve().is_relative_to(root.resolve())
        else path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
    }
    if Image is not None:
        try:
            with Image.open(path) as source:
                image = ImageOps.exif_transpose(source)
                item["image"] = {
                    "width_px": image.width,
                    "height_px": image.height,
                    "mode": image.mode,
                    "format": source.format,
                    "dpi": list(source.info.get("dpi", [])),
                    "has_alpha": "A" in image.getbands(),
                }
        except (OSError, ValueError):
            pass
    return item


def collect(inputs: list[Path]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        if item.is_dir():
            files.extend(path for path in item.rglob("*") if path.is_file())
        elif item.is_file():
            files.append(item)
        else:
            raise FileNotFoundError(item)
    return sorted(set(files), key=lambda path: str(path.resolve()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = {
        "schema": "moso.asset-manifest/0.2",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root": str(args.root.resolve()),
        "assets": [inspect(path, args.root) for path in collect(args.inputs)],
    }
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
