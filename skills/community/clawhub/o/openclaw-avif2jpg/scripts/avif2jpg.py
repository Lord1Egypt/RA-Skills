#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

try:
    import pillow_avif  # noqa: F401
except Exception:
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="avif2jpg",
        description="Convert .avif images to .jpg from folders and/or files.",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="One or more folder paths or file paths.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=92,
        help="JPEG quality (1-100). Default: 92",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output files if they exist.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan folders for .avif files.",
    )
    return parser.parse_args()


def ensure_rgb(image: Image.Image) -> Image.Image:
    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        alpha = image.split()[-1]
        background.paste(image.convert("RGB"), mask=alpha)
        return background
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


def convert_avif_to_jpg(src: Path, dst: Path, quality: int, overwrite: bool) -> bool:
    if dst.exists() and not overwrite:
        print(f"[SKIP] Output exists: {dst}")
        return True

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as img:
            rgb = ensure_rgb(img)
            rgb.save(dst, format="JPEG", quality=quality)
        print(f"[OK] {src} -> {dst}")
        return True
    except Exception as exc:
        print(f"[FAIL] {src}: {exc}")
        return False


def find_avif_files(folder: Path, recursive: bool) -> list[Path]:
    pattern = "**/*.avif" if recursive else "*.avif"
    return sorted(p for p in folder.glob(pattern) if p.is_file())


def process_folder(folder: Path, recursive: bool, quality: int, overwrite: bool) -> tuple[int, int]:
    out_root = folder.parent / f"{folder.name}_jpg"
    avif_files = find_avif_files(folder, recursive=recursive)
    ok_count = 0
    fail_count = 0

    for src in avif_files:
        relative = src.relative_to(folder)
        dst = out_root / relative.with_suffix(".jpg")
        success = convert_avif_to_jpg(src, dst, quality=quality, overwrite=overwrite)
        if success:
            ok_count += 1
        else:
            fail_count += 1

    if not avif_files:
        print(f"[WARN] No .avif files found in folder: {folder}")

    return ok_count, fail_count


def process_file(file_path: Path, quality: int, overwrite: bool) -> tuple[int, int]:
    if file_path.suffix.lower() != ".avif":
        print(f"[WARN] Not an .avif file, skipped: {file_path}")
        return 0, 0

    dst = file_path.with_suffix(".jpg")
    success = convert_avif_to_jpg(file_path, dst, quality=quality, overwrite=overwrite)
    return (1, 0) if success else (0, 1)


def main() -> int:
    args = parse_args()
    quality = max(1, min(100, args.quality))

    total_ok = 0
    total_fail = 0

    for raw in args.inputs:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            print(f"[WARN] Path does not exist, skipped: {path}")
            continue

        if path.is_dir():
            ok, fail = process_folder(
                path, recursive=args.recursive, quality=quality, overwrite=args.overwrite
            )
            total_ok += ok
            total_fail += fail
        elif path.is_file():
            ok, fail = process_file(path, quality=quality, overwrite=args.overwrite)
            total_ok += ok
            total_fail += fail
        else:
            print(f"[WARN] Unsupported path type, skipped: {path}")

    print(f"\nDone. success={total_ok}, failed={total_fail}")
    return 1 if total_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
