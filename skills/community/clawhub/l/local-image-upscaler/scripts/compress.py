#!/usr/bin/env python3
"""Compress an image to a target file size without stretching or overwriting it."""

from __future__ import annotations

import argparse
import math
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from upscale import read_dimensions

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def windows_environment(values: dict[str, str]) -> dict[str, str]:
    environment = {
        key: os.environ[key]
        for key in ("SystemRoot", "WINDIR", "TEMP", "TMP")
        if key in os.environ
    }
    environment.update(values)
    return environment


def trusted_windows_powershell() -> Path:
    root_value = os.environ.get("SystemRoot") or os.environ.get("WINDIR")
    if not root_value:
        raise RuntimeError("Windows system root is unavailable; refusing PATH-based PowerShell lookup")
    root = Path(root_value)
    if not root.is_absolute():
        raise RuntimeError("Windows system root is not absolute; refusing PowerShell execution")
    executable = root / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
    if not executable.is_file():
        raise RuntimeError(f"Trusted Windows PowerShell was not found at {executable}")
    return executable


def encode_jpeg(source: Path, destination: Path, width: int, height: int, quality: int) -> None:
    system = platform.system().lower()
    if system == "darwin":
        command = [
            "sips", "-z", str(height), str(width),
            "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
            str(source), "--out", str(destination),
        ]
        result = subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"macOS JPEG encoding failed: {result.stderr.decode(errors='replace').strip()}")
        return
    if system == "windows":
        script = r"""
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile($env:IC_SOURCE)
$bmp = New-Object System.Drawing.Bitmap([int]$env:IC_WIDTH, [int]$env:IC_HEIGHT)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.Clear([System.Drawing.Color]::White)
$graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.DrawImage($src, 0, 0, $bmp.Width, $bmp.Height)
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$parameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
$parameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]$env:IC_QUALITY)
$bmp.Save($env:IC_DESTINATION, $codec, $parameters)
$parameters.Dispose()
$graphics.Dispose()
$bmp.Dispose()
$src.Dispose()
"""
        environment = windows_environment({
            "IC_SOURCE": str(source),
            "IC_DESTINATION": str(destination),
            "IC_WIDTH": str(width),
            "IC_HEIGHT": str(height),
            "IC_QUALITY": str(quality),
        })
        result = subprocess.run(
            [str(trusted_windows_powershell()), "-NoProfile", "-NonInteractive", "-Command", script],
            check=False,
            env=environment,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Windows JPEG encoding failed with code {result.returncode}")
        return
    raise RuntimeError(f"Unsupported platform: {system}. Supported: macOS and Windows x64.")


def best_quality_for_dimensions(
    source: Path,
    work_dir: Path,
    width: int,
    height: int,
    target_bytes: int,
    min_quality: int,
    max_quality: int,
) -> tuple[Path | None, int | None, int]:
    low, high = min_quality, max_quality
    best_path: Path | None = None
    best_quality: int | None = None
    smallest_size = 0
    while low <= high:
        quality = (low + high) // 2
        candidate = work_dir / f"candidate-{width}x{height}-q{quality}.jpg"
        encode_jpeg(source, candidate, width, height, quality)
        size = candidate.stat().st_size
        if smallest_size == 0 or size < smallest_size:
            smallest_size = size
        if size <= target_bytes:
            best_path, best_quality = candidate, quality
            low = quality + 1
        else:
            high = quality - 1
    return best_path, best_quality, smallest_size


def compress(
    source: Path,
    destination: Path,
    target_kb: int,
    min_quality: int,
    max_quality: int,
    min_edge: int,
    keep_dimensions: bool,
) -> None:
    if source.resolve() == destination.resolve():
        raise RuntimeError("Output path must not overwrite the input image")
    width, height = read_dimensions(source)
    input_size = source.stat().st_size
    target_bytes = target_kb * 1024
    destination.parent.mkdir(parents=True, exist_ok=True)
    current_width, current_height = width, height

    with tempfile.TemporaryDirectory(prefix="image-compressor-") as temporary:
        work_dir = Path(temporary)
        for _ in range(12):
            candidate, quality, smallest_size = best_quality_for_dimensions(
                source, work_dir, current_width, current_height,
                target_bytes, min_quality, max_quality,
            )
            if candidate is not None and quality is not None:
                shutil.copy2(candidate, destination)
                out_width, out_height = read_dimensions(destination)
                print(
                    f"Compressed: {destination}\n"
                    f"Dimensions: {out_width}x{out_height}\n"
                    f"Quality: {quality}\n"
                    f"Size: {destination.stat().st_size / 1024:.1f} KiB (target <= {target_kb} KiB)\n"
                    f"Reduction: {(1 - destination.stat().st_size / input_size) * 100:.1f}%"
                )
                return
            if keep_dimensions:
                raise RuntimeError(
                    f"Cannot reach {target_kb} KiB at the original {width}x{height} dimensions "
                    f"with quality >= {min_quality}"
                )
            if smallest_size <= 0:
                raise RuntimeError("Encoder produced no usable candidate")
            factor = min(0.92, math.sqrt(target_bytes / smallest_size) * 0.94)
            if min(current_width, current_height) <= min_edge:
                break
            next_width = round(current_width * factor)
            next_height = round(current_height * factor)
            if min(next_width, next_height) < min_edge:
                floor_factor = min_edge / min(current_width, current_height)
                next_width = round(current_width * floor_factor)
                next_height = round(current_height * floor_factor)
            current_width, current_height = next_width, next_height
    raise RuntimeError(
        f"Could not reach {target_kb} KiB without shrinking below the configured minimum edge ({min_edge}px)"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--target-kb", type=int, help="Maximum output size in KiB")
    target.add_argument("--target-mb", type=float, help="Maximum output size in MiB")
    parser.add_argument("--min-quality", type=int, default=35)
    parser.add_argument("--max-quality", type=int, default=95)
    parser.add_argument("--min-edge", type=int, default=640, help="Do not shrink the short edge below this size")
    parser.add_argument("--keep-dimensions", action="store_true", help="Adjust quality only; fail instead of resizing")
    parser.add_argument("--recursive", action="store_true", help="Include subfolders for folder input")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing output file")
    parser.add_argument("--dry-run", action="store_true", help="List planned outputs without writing them")
    args = parser.parse_args()
    if args.target_mb is not None:
        args.target_kb = round(args.target_mb * 1024)
    if args.target_kb is None or args.target_kb < 10:
        parser.error("--target-kb must be at least 10")
    if not 1 <= args.min_quality <= args.max_quality <= 100:
        parser.error("quality must satisfy 1 <= min <= max <= 100")
    if args.min_edge < 32:
        parser.error("--min-edge must be at least 32")
    return args


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}-v{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    if not source.exists():
        raise RuntimeError(f"Input does not exist: {source}")
    if source.is_dir():
        if args.output is None:
            raise RuntimeError("Folder input requires --output OUTPUT_FOLDER")
        output_dir = args.output.expanduser().resolve()
        pattern = "**/*" if args.recursive else "*"
        images = sorted(path for path in source.glob(pattern) if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES)
        if not images:
            raise RuntimeError(f"No supported images found in {source}")
        for image in images:
            relative_parent = image.relative_to(source).parent if args.recursive else Path()
            destination = output_dir / relative_parent / f"{image.stem}-compressed-{args.target_kb}kb.jpg"
            if destination.exists() and not args.overwrite:
                destination = unique_path(destination)
            if args.dry_run:
                print(f"Would compress: {image} -> {destination} (<= {args.target_kb} KiB)")
            else:
                compress(
                    image, destination, args.target_kb, args.min_quality,
                    args.max_quality, args.min_edge, args.keep_dimensions,
                )
        return 0
    if source.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise RuntimeError("Supported input formats: JPG, PNG, WebP")
    destination = args.output.expanduser().resolve() if args.output else source.with_name(
        f"{source.stem}-compressed-{args.target_kb}kb.jpg"
    )
    if destination.suffix.lower() not in {".jpg", ".jpeg"}:
        destination = destination.with_suffix(".jpg")
    if destination.exists() and not args.overwrite:
        destination = unique_path(destination)
    if args.dry_run:
        print(f"Would compress: {source} -> {destination} (<= {args.target_kb} KiB)")
        return 0
    compress(
        source, destination, args.target_kb, args.min_quality,
        args.max_quality, args.min_edge, args.keep_dimensions,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
