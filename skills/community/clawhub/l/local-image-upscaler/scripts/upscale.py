#!/usr/bin/env python3
"""Upscale one image or a folder of images with the verified local runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((SKILL_DIR / "assets" / "manifest.json").read_text(encoding="utf-8"))
SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
ART_HINTS = {
    "anime", "animation", "cartoon", "comic", "digital-art", "drawing",
    "illustration", "lineart", "manga", "vector", "动漫", "动画", "插画", "漫画",
}


def cache_root() -> Path:
    override = os.environ.get("IMAGE_UPSCALER_CACHE")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "image-upscaler"
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "image-upscaler"


def platform_key() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "darwin":
        return "darwin-universal"
    if system == "windows" and machine in {"amd64", "x86_64"}:
        return "windows-x64"
    raise RuntimeError(f"Unsupported platform: {system}/{machine}")


def runtime_path() -> Path:
    key = platform_key()
    spec = MANIFEST["platforms"][key]
    return cache_root() / "runtime" / MANIFEST["runtime_version"] / key / spec["archive_root"] / spec["executable"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def resolve_model(source: Path, args: argparse.Namespace) -> tuple[str, str]:
    if args.model:
        return args.model, "manual model override"
    profile = args.profile
    if profile == "auto":
        normalized_name = source.stem.lower().replace("_", "-").replace(" ", "-")
        if any(hint in normalized_name for hint in ART_HINTS):
            profile = "digital-art"
            reason = "filename suggests illustration or animation content"
        else:
            profile = "default"
            reason = "conservative fallback; no reliable content hint was available to the CLI"
    else:
        reason = MANIFEST["profiles"][profile]["description"]
    return MANIFEST["profiles"][profile]["model"], f"profile={profile}; {reason}"


def read_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(32)
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            return struct.unpack(">II", header[16:24])
        if header[:2] == b"\xff\xd8":
            handle.seek(2)
            while True:
                byte = handle.read(1)
                while byte == b"\xff":
                    byte = handle.read(1)
                if not byte:
                    break
                marker = byte[0]
                if marker in {0xD8, 0xD9}:
                    continue
                length_bytes = handle.read(2)
                if len(length_bytes) != 2:
                    break
                length = struct.unpack(">H", length_bytes)[0]
                if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                    data = handle.read(5)
                    height, width = struct.unpack(">HH", data[1:5])
                    return width, height
                handle.seek(length - 2, 1)
        if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
            kind = header[12:16]
            if kind == b"VP8X":
                return 1 + int.from_bytes(header[24:27], "little"), 1 + int.from_bytes(header[27:30], "little")
            if kind == b"VP8 " and header[23:26] == b"\x9d\x01\x2a":
                width, height = struct.unpack("<HH", header[26:30])
                return width & 0x3FFF, height & 0x3FFF
            if kind == b"VP8L" and header[20] == 0x2F:
                bits = int.from_bytes(header[21:25], "little")
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    raise RuntimeError(f"Could not read dimensions from {path}")


def target_dimensions(width: int, height: int, target: str, max_edge: int | None) -> tuple[int, int] | None:
    if target == "scale4" and max_edge is None:
        return None
    preset_edges = {"1k": 1920, "2k": 2560, "4k": 3840, "8k": 7680}
    edge = max_edge or preset_edges[target]
    ratio = edge / max(width, height)
    out_width = max(2, round(width * ratio))
    out_height = max(2, round(height * ratio))
    out_width += out_width % 2
    out_height += out_height % 2
    return out_width, out_height


def output_path(source: Path, requested: Path | None, output_format: str, batch: bool) -> Path:
    extension = ".jpg" if output_format == "jpg" else f".{output_format}"
    if batch:
        assert requested is not None
        return requested / f"{source.stem}-upscaled{extension}"
    if requested is not None:
        return requested.with_suffix(extension) if requested.suffix.lower() not in SUPPORTED_SUFFIXES else requested
    return source.with_name(f"{source.stem}-upscaled{extension}")


def resize_exact(source: Path, destination: Path, dimensions: tuple[int, int], output_format: str, quality: int) -> None:
    width, height = dimensions
    system = platform.system().lower()
    if output_format == "webp":
        raise RuntimeError("Exact 2K/4K WebP output is not dependency-free; use PNG/JPG or --target scale4")
    if system == "darwin":
        image_format = "jpeg" if output_format == "jpg" else "png"
        command = [
            "sips", "-z", str(height), str(width),
            "-s", "format", image_format,
        ]
        if output_format == "jpg":
            command.extend(["-s", "formatOptions", str(quality or 95)])
        command.extend([str(source), "--out", str(destination)])
        completed = subprocess.run(command, check=False, stdout=subprocess.DEVNULL)
        if completed.returncode != 0:
            raise RuntimeError(f"macOS exact resize failed with code {completed.returncode}")
        return
    if system == "windows":
        script = r"""
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile($env:IU_SOURCE)
$bmp = New-Object System.Drawing.Bitmap([int]$env:IU_WIDTH, [int]$env:IU_HEIGHT)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.DrawImage($src, 0, 0, $bmp.Width, $bmp.Height)
if ($env:IU_FORMAT -eq 'jpg') {
  $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
  $parameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
  $parameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]$env:IU_QUALITY)
  $bmp.Save($env:IU_DESTINATION, $codec, $parameters)
  $parameters.Dispose()
} else {
  $bmp.Save($env:IU_DESTINATION, [System.Drawing.Imaging.ImageFormat]::Png)
}
$graphics.Dispose()
$bmp.Dispose()
$src.Dispose()
"""
        environment = {
            key: os.environ[key]
            for key in ("SystemRoot", "WINDIR", "TEMP", "TMP")
            if key in os.environ
        }
        environment.update({
            "IU_SOURCE": str(source),
            "IU_DESTINATION": str(destination),
            "IU_WIDTH": str(width),
            "IU_HEIGHT": str(height),
            "IU_FORMAT": output_format,
            "IU_QUALITY": str(quality or 95),
        })
        completed = subprocess.run(
            [str(trusted_windows_powershell()), "-NoProfile", "-NonInteractive", "-Command", script],
            check=False,
            env=environment,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"Windows exact resize failed with code {completed.returncode}")
        return
    raise RuntimeError(f"Exact resize is unsupported on {system}")


def run_one(source: Path, destination: Path, args: argparse.Namespace) -> None:
    executable = runtime_path()
    runtime_spec = MANIFEST["platforms"][platform_key()]
    model_key, selection_reason = resolve_model(source, args)
    model_spec = MANIFEST["models"][model_key]
    model_dir = cache_root() / "models" / model_key
    required = [model_dir / item["name"] for item in model_spec["files"]]
    missing = [str(path) for path in [executable, *required] if not path.exists()]
    if missing:
        raise RuntimeError(
            "Runtime/model cache is incomplete. Run `python scripts/setup.py --model "
            + model_key
            + "` first. Missing: "
            + ", ".join(missing)
        )
    actual_runtime_hash = sha256(executable)
    if actual_runtime_hash != runtime_spec["executable_sha256"]:
        raise RuntimeError(
            "Runtime executable failed SHA-256 verification. Refusing to execute it; "
            f"rerun setup with --force. Expected {runtime_spec['executable_sha256']}, got {actual_runtime_hash}"
        )
    for item, path in zip(model_spec["files"], required):
        actual_model_hash = sha256(path)
        if actual_model_hash != item["sha256"]:
            raise RuntimeError(
                "Model file failed SHA-256 verification. Refusing to use it; rerun setup. "
                f"File {path.name}: expected {item['sha256']}, got {actual_model_hash}"
            )
    if source.resolve() == destination.resolve():
        raise RuntimeError("Output path must not overwrite the input image")

    width, height = read_dimensions(source)
    dimensions = target_dimensions(width, height, args.target, args.max_edge)
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Selected model: {model_key} ({selection_reason})", flush=True)
    print(f"Trade-off: {model_spec.get('tradeoff', 'not documented')}", flush=True)
    print(f"Upscaling {source} ({width}x{height}) -> {destination}", flush=True)
    with tempfile.TemporaryDirectory(prefix="image-upscaler-") as temporary_dir:
        engine_output = destination if dimensions is None else Path(temporary_dir) / "native-4x.png"
        engine_format = args.format if dimensions is None else "png"
        command = [
            str(executable), "-i", str(source), "-o", str(engine_output),
            "-m", str(model_dir), "-n", model_spec["engine_name"],
            "-z", "4", "-s", "4", "-f", engine_format,
            "-c", str(args.compression), "-t", str(args.tile),
        ]
        if args.tta:
            command.append("-x")
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Upscaler exited with code {completed.returncode}")
        if dimensions:
            resize_exact(engine_output, destination, dimensions, args.format, args.compression)
    if not destination.exists() or destination.stat().st_size == 0:
        raise RuntimeError(f"Upscaler did not create a valid output: {destination}")
    out_width, out_height = read_dimensions(destination)
    if dimensions and (out_width, out_height) != dimensions:
        raise RuntimeError(f"Output verification failed: expected {dimensions}, got {(out_width, out_height)}")
    print(f"Verified: {out_width}x{out_height}, {destination.stat().st_size / 1024 / 1024:.2f} MiB")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--target", choices=("1k", "2k", "4k", "8k", "scale4"), default="4k")
    parser.add_argument("--max-edge", type=int, help="Override the target long-edge size")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--profile",
        choices=tuple(MANIFEST["profiles"]),
        default="auto",
        help="User-facing quality profile; auto is conservative unless the agent selects a content profile",
    )
    selection.add_argument("--model", choices=tuple(MANIFEST["models"]), help="Low-level model override")
    parser.add_argument("--format", choices=("png", "jpg", "webp"), default="png")
    parser.add_argument("--compression", type=int, default=0)
    parser.add_argument("--tile", type=int, default=0, help="0=automatic; try 256 or 128 on low VRAM")
    parser.add_argument("--tta", action="store_true", help="Slower test-time augmentation")
    args = parser.parse_args()
    if args.max_edge is not None and args.max_edge < 32:
        parser.error("--max-edge must be at least 32")
    if not 0 <= args.compression <= 100:
        parser.error("--compression must be between 0 and 100")
    if args.tile != 0 and args.tile < 32:
        parser.error("--tile must be 0 or at least 32")
    return args


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    if not source.exists():
        raise RuntimeError(f"Input does not exist: {source}")
    if source.is_dir():
        if args.output is None:
            raise RuntimeError("Folder input requires --output OUTPUT_FOLDER")
        output_dir = args.output.expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        images = sorted(path for path in source.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES)
        if not images:
            raise RuntimeError(f"No supported images found in {source}")
        for image in images:
            run_one(image, output_path(image, output_dir, args.format, True), args)
        return 0
    if source.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise RuntimeError("Supported input formats: JPG, PNG, WebP")
    requested = args.output.expanduser().resolve() if args.output else None
    run_one(source, output_path(source, requested, args.format, False), args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
