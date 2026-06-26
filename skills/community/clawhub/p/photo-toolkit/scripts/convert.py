#!/usr/bin/env python3
"""
Photo to JPG Thumbnail Generator

Convert camera RAW files, JPG photos, and Apple HEIC/HEIF images
to JPG thumbnails with professional-quality output.
Uses rawpy (LibRaw) for RAW, Pillow for JPG, pillow-heif for HEIC/HEIF.

Supported Formats:
    Camera RAW:
        Nikon:    .nef, .nrw
        Canon:    .cr2, .cr3, .crw
        Sony:     .arw, .srf, .sr2
        Fujifilm: .raf
        Olympus:  .orf
        Panasonic:.rw2
        Pentax:   .pef
        Samsung:  .srw
        Leica:    .rwl, .dng
        Adobe:    .dng
        Hasselblad: .3fr, .fff
        Phase One: .iiq
        Sigma:    .x3f
    Standard Image:
        JPEG:     .jpg, .jpeg
    Apple:
        HEIC/HEIF: .heic, .heif (iPhone/iPad 默认格式)

Dependencies:
    System: libraw (RedHat: dnf install LibRaw-devel / Debian: apt-get install libraw-dev)
    Python: pip install rawpy pillow numpy pillow-heif

    Check & install: bash scripts/setup_deps.sh

Configuration:
    Default paths and options from config.toml (next to scripts/ dir).
    Command-line arguments always override config values.

Usage:
    python convert.py /path/to/raw/files /path/to/output
    python convert.py /path/to/photo.NEF /path/to/output
    python convert.py --config /path/to/config.toml
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed


# ── Supported extensions ───────────────────────────────────────
RAW_EXTENSIONS = {
    # Nikon
    ".nef",
    ".nrw",
    # Canon
    ".cr2",
    ".cr3",
    ".crw",
    # Sony
    ".arw",
    ".srf",
    ".sr2",
    # Fujifilm
    ".raf",
    # Olympus / OM System
    ".orf",
    # Panasonic
    ".rw2",
    # Pentax
    ".pef",
    # Samsung
    ".srw",
    # Leica
    ".rwl",
    # Adobe DNG (universal)
    ".dng",
    # Hasselblad
    ".3fr",
    ".fff",
    # Phase One
    ".iiq",
    # Sigma
    ".x3f",
}

JPG_EXTENSIONS = {".jpg", ".jpeg"}

HEIC_EXTENSIONS = {".heic", ".heif"}

# All supported input formats
SUPPORTED_EXTENSIONS = RAW_EXTENSIONS | JPG_EXTENSIONS | HEIC_EXTENSIONS

# Check HEIC support availability
_HEIC_AVAILABLE = False
try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    _HEIC_AVAILABLE = True
except ImportError:
    pass


# ── Configuration ───────────────────────────────────────────────

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # pip install tomli  (Python 3.8-3.10)

_SKILL_DIR = Path(__file__).resolve().parent.parent
_ROOT_DIR = _SKILL_DIR.parent
_DEFAULT_CONFIG_PATH = (
    _SKILL_DIR / "config.toml" if (_SKILL_DIR / "config.toml").exists() else _ROOT_DIR / "config.toml"
)


def load_config(config_path=None):
    """Load configuration from config.toml."""
    path = Path(config_path or _DEFAULT_CONFIG_PATH).expanduser().resolve()
    if not path.exists():
        return {}
    try:
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
        if not isinstance(cfg, dict):
            print(f"⚠️  Config is not a valid mapping, ignoring: {path}", file=sys.stderr)
            return {}
        print(f"📄 Loaded config: {path}")
        return cfg
    except Exception as e:
        print(f"⚠️  Failed to read config ({path}): {e}", file=sys.stderr)
        return {}


# ── Dependency Check ────────────────────────────────────────────


def check_dependencies():
    """Check if required packages are installed and report missing ones."""
    missing = []
    for pkg, pip_name in [("rawpy", "rawpy"), ("PIL", "pillow"), ("numpy", "numpy")]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pip_name)
    if missing:
        print("❌ Missing required dependencies:", file=sys.stderr)
        for pkg in missing:
            print(f"  - {pkg}", file=sys.stderr)
        print(f"\nInstall with:\n  pip3 install {' '.join(missing)}", file=sys.stderr)
        print(f"\nOr run:\n  bash {_SKILL_DIR}/scripts/setup_deps.sh", file=sys.stderr)
        sys.exit(1)


check_dependencies()

import rawpy
from PIL import Image
import numpy as np


def get_cpu_count():
    """Get a reasonable default worker count (cpu_count * 2, max 16)."""
    try:
        count = os.cpu_count() or 4
        return min(count * 2, 16)
    except Exception:
        return 4


def process_file(raw_path, output_dir, size, quality, overwrite=False, preserve_exif=True, per_image_budget_bytes=0):
    """
    Process a single photo file (RAW/JPG/HEIC) to JPG thumbnail.

    If per_image_budget_bytes > 0 and the source is JPG/HEIC (not RAW),
    files smaller than the budget are symlinked instead of re-encoded.
    This avoids pointless re-compression of already-small images.

    Returns:
        Tuple of (filename, success, message, elapsed_seconds)
    """
    start = time.monotonic()
    raw_name = raw_path.name
    ext_lower = raw_path.suffix.lower()

    try:
        jpg_name = raw_path.stem + ".jpg"
        jpg_path = output_dir / jpg_name

        if jpg_path.exists() and not overwrite:
            elapsed = time.monotonic() - start
            return (raw_name, True, f"Skipped (exists): {jpg_name}", elapsed)

        # ── Smart skip: symlink small JPG/HEIC originals ─────────
        is_non_raw = ext_lower in (JPG_EXTENSIONS | HEIC_EXTENSIONS)
        if is_non_raw and per_image_budget_bytes > 0:
            file_size = raw_path.stat().st_size
            if file_size <= per_image_budget_bytes:
                # Original is small enough — symlink instead of re-encoding
                try:
                    os.symlink(str(raw_path.resolve()), str(jpg_path))
                except OSError:
                    # Fallback: copy if symlink fails (e.g. cross-device)
                    import shutil

                    shutil.copy2(str(raw_path), str(jpg_path))
                elapsed = time.monotonic() - start
                file_size_kb = file_size / 1024
                return (
                    raw_name,
                    True,
                    f"⚡ {jpg_name} (linked, {file_size_kb:.0f}KB ≤ budget {per_image_budget_bytes/1024:.0f}KB)",
                    elapsed,
                )

        # ── Determine processing path ────────────────────────────
        if ext_lower in RAW_EXTENSIONS:
            # RAW Processing via rawpy
            with rawpy.imread(str(raw_path)) as raw:
                rgb = raw.postprocess(
                    use_camera_wb=True,
                    use_auto_wb=False,
                    no_auto_bright=False,
                    output_bps=8,
                    half_size=True if size <= 2048 else False,
                    demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,
                    output_color=rawpy.ColorSpace.sRGB,
                )
            image = Image.fromarray(rgb)

        elif ext_lower in HEIC_EXTENSIONS:
            # HEIC/HEIF via pillow-heif
            if not _HEIC_AVAILABLE:
                elapsed = time.monotonic() - start
                return (raw_name, False, f"✗ {raw_name}: pillow-heif not installed (pip install pillow-heif)", elapsed)
            image = Image.open(str(raw_path))

        else:
            # JPG/JPEG via Pillow directly
            image = Image.open(str(raw_path))

        # ── Auto-rotate via EXIF ─────────────────────────────────
        try:
            from PIL import ImageOps

            image = ImageOps.exif_transpose(image)
        except Exception:
            pass

        # ── Resize ──────────────────────────────────────────────
        image.thumbnail((size, size), Image.Resampling.LANCZOS)

        # ── EXIF Handling ───────────────────────────────────────
        exif_bytes = None
        if preserve_exif:
            try:
                with open(str(raw_path), "rb") as f:
                    header = f.read(65536)
                exif_start = header.find(b"\xff\xe1")
                if exif_start != -1:
                    exif_length = int.from_bytes(header[exif_start + 2 : exif_start + 4], "big")
                    exif_bytes = header[exif_start : exif_start + 2 + exif_length]
            except Exception:
                exif_bytes = None

        # ── Save JPEG ──────────────────────────────────────────
        save_kwargs = {
            "format": "JPEG",
            "quality": quality,
            "optimize": True,
            "subsampling": 0 if quality >= 90 else 2,
        }
        if exif_bytes:
            save_kwargs["exif"] = exif_bytes

        image.save(jpg_path, **save_kwargs)

        elapsed = time.monotonic() - start
        file_size_kb = jpg_path.stat().st_size / 1024
        return (raw_name, True, f"✓ {jpg_name} ({image.width}×{image.height}, {file_size_kb:.0f}KB)", elapsed)

    except Exception as e:
        elapsed = time.monotonic() - start
        return (raw_name, False, f"✗ {raw_name}: {e}", elapsed)


def find_supported_files(input_path, recursive=False):
    """
    Find all supported photo files (RAW/JPG/HEIC) in directory.
    Case-insensitive matching for all supported extensions.
    Skips special directories (thumbnails, graded, sessions, .ds_store).
    """
    SKIP_DIRS = {"thumbnails", "graded", "sessions", ".ds_store"}

    if input_path.is_file():
        if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [input_path]
        return []

    results = []
    if recursive:
        for p in sorted(input_path.rglob("*")):
            # Skip special directories
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                results.append(p)
    else:
        for p in sorted(input_path.iterdir()):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                results.append(p)
    return results


def format_time(seconds):
    """Format elapsed seconds to human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds) // 60
    secs = seconds - minutes * 60
    return f"{minutes}m {secs:.0f}s"


def main():
    parser = argparse.ArgumentParser(
        description="Convert photos to JPG thumbnails (supports RAW/JPG/HEIC/HEIF)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats:
  Camera RAW: Nikon (.nef .nrw), Canon (.cr2 .cr3 .crw), Sony (.arw .srf .sr2),
    Fujifilm (.raf), Olympus (.orf), Panasonic (.rw2), Pentax (.pef),
    Samsung (.srw), Leica (.rwl .dng), Adobe (.dng), Hasselblad (.3fr .fff),
    Phase One (.iiq), Sigma (.x3f)
  Standard: JPEG (.jpg .jpeg)
  Apple: HEIC (.heic .heif) — requires: pip install pillow-heif

Examples:
  %(prog)s ~/Photos/raw ~/Photos/thumbs
  %(prog)s ~/Photos/raw ~/Photos/thumbs --size 800 --quality 90
  %(prog)s ~/Photos/DSC_0001.NEF ~/Photos/thumbs
  %(prog)s ~/Photos/IMG_0001.HEIC ~/Photos/thumbs
  %(prog)s ~/Photos/raw ~/Photos/thumbs -r --overwrite
        """,
    )
    parser.add_argument("input", nargs="?", default=None, help="Photo file or directory (default: from config.toml)")
    parser.add_argument(
        "output_dir", nargs="?", default=None, help="Directory for output JPG files (default: {input}/thumbnails/)"
    )
    parser.add_argument("--config", type=str, default=None, help="Path to config.toml")
    parser.add_argument("--size", type=int, default=None, help="Maximum thumbnail dimension in pixels (default: 1200)")
    parser.add_argument("--quality", type=int, default=None, help="JPEG quality 1-100 (default: 85)")
    parser.add_argument("--workers", type=int, default=None, help="Number of parallel workers (default: auto, max 8)")
    parser.add_argument("--recursive", "-r", action="store_true", default=None, help="Search subdirectories")
    parser.add_argument("--overwrite", action="store_true", default=None, help="Overwrite existing JPG files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without converting")
    parser.add_argument("--no-exif", action="store_true", default=None, help="Do not copy EXIF metadata")
    parser.add_argument(
        "--max-total-mb",
        type=float,
        default=None,
        help="Total image budget in MB for LLM vision input. "
        "JPG/HEIC files smaller than (budget / n_files) are symlinked "
        "instead of re-encoded. Set 0 to disable. (default: 50)",
    )
    parser.add_argument("--report", type=str, default=None, help="处理报告输出 JSON 路径")
    parser.add_argument("--from-stdin", action="store_true", help="从 stdin 读取文件路径列表（JSON 格式）")

    args = parser.parse_args()

    # ── Load config and merge ───────────────────────────────────
    cfg = load_config(args.config)

    input_raw = args.input or cfg.get("raw_dir") or cfg.get("input_dir")
    if not input_raw and not args.from_stdin:
        parser.error("input path is required. Provide it as an argument or set 'raw_dir' in config.toml")

    output_raw = args.output_dir or cfg.get("output_dir")
    if not output_raw:
        if input_raw:
            output_raw = str(Path(input_raw).expanduser().resolve() / "thumbnails")
        elif args.from_stdin:
            parser.error("--output is required when using --from-stdin without an input directory")
        else:
            parser.error("output path is required. Provide it as an argument or set 'output_dir' in config.toml")

    size = args.size if args.size is not None else cfg.get("max_size", 1200)
    quality = args.quality if args.quality is not None else cfg.get("jpeg_quality", 85)
    workers = args.workers if args.workers is not None else cfg.get("workers") or get_cpu_count()
    recursive = args.recursive if args.recursive is not None else cfg.get("recursive", False)
    overwrite = args.overwrite if args.overwrite is not None else cfg.get("overwrite", False)
    preserve_exif = not args.no_exif if args.no_exif is not None else cfg.get("preserve_exif", True)
    max_total_mb = args.max_total_mb if args.max_total_mb is not None else cfg.get("thumbnail_budget_mb", 50)

    if not 1 <= quality <= 100:
        print("Error: --quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    if size < 100:
        print("Error: --size must be at least 100", file=sys.stderr)
        sys.exit(1)

    input_path = Path(input_raw).expanduser().resolve() if input_raw else None
    output_path = Path(output_raw).expanduser().resolve()

    if input_path and not input_path.exists():
        print(f"Error: Input does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # ── Find photo files ─────────────────────────────────────────
    if args.from_stdin:
        stdin_data = json.load(sys.stdin)
        file_list = stdin_data.get("files", [])
        photo_files = [Path(f) for f in file_list if Path(f).suffix.lower() in SUPPORTED_EXTENSIONS]
    else:
        photo_files = find_supported_files(input_path, recursive)

    if not photo_files:
        print("No supported photo files found.")
        # Show supported extensions
        ext_list = sorted(SUPPORTED_EXTENSIONS)
        print(f"Supported extensions: {', '.join(ext_list)}")
        if not _HEIC_AVAILABLE:
            print("  Note: HEIC/HEIF support requires: pip install pillow-heif")
        sys.exit(0)

    # Summarize formats found
    ext_counts = {}
    for f in photo_files:
        ext = f.suffix.upper()
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
    ext_summary = ", ".join(f"{ext}: {cnt}" for ext, cnt in sorted(ext_counts.items()))
    print(f"📷 Found {len(photo_files)} photo file(s) ({ext_summary})")

    # ── Dry run ─────────────────────────────────────────────────
    if args.dry_run:
        print(f"\n🔍 Dry run — files that would be converted:")
        for photo in photo_files:
            jpg_name = photo.stem + ".jpg"
            jpg_path = output_path / jpg_name
            if jpg_path.exists() and not overwrite:
                print(f"  ⏭  {photo.name} → {jpg_name} (exists, skip)")
            else:
                print(f"  📸 {photo.name} → {jpg_name}")
        sys.exit(0)

    output_path.mkdir(parents=True, exist_ok=True)

    # ── Process files ───────────────────────────────────────────
    # Calculate per-image budget for smart-skip of small JPG/HEIC
    n_files = len(photo_files)
    if max_total_mb > 0 and n_files > 0:
        per_image_budget_bytes = int(max_total_mb * 1024 * 1024 / n_files)
    else:
        per_image_budget_bytes = 0

    print(f"\n⚙️  Converting: size={size}px, quality={quality}, workers={workers}")
    if per_image_budget_bytes > 0:
        print(
            f"   Budget: {max_total_mb:.0f}MB total → {per_image_budget_bytes/1024:.0f}KB/image (small JPG/HEIC will be linked)"
        )
    print(f"   Input:  {input_path or 'stdin'}")
    print(f"   Output: {output_path}\n")

    total_start = time.monotonic()
    success_count = 0
    skip_count = 0
    linked_count = 0
    error_count = 0
    total = len(photo_files)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                process_file, photo, output_path, size, quality, overwrite, preserve_exif, per_image_budget_bytes
            ): photo
            for photo in photo_files
        }

        done = 0
        for future in as_completed(futures):
            done += 1
            raw_name, success, message, elapsed = future.result()
            progress = f"[{done}/{total}]"
            print(f"  {progress} {message} ({format_time(elapsed)})")

            if success:
                if "Skipped" in message:
                    skip_count += 1
                elif "linked" in message:
                    linked_count += 1
                else:
                    success_count += 1
            else:
                error_count += 1

    # ── Summary ─────────────────────────────────────────────────
    total_elapsed = time.monotonic() - total_start
    print(f"\n{'─' * 55}")
    print(f"✅ Done in {format_time(total_elapsed)}")
    parts = [f"Converted: {success_count}"]
    if linked_count > 0:
        parts.append(f"Linked: {linked_count}")
    parts.extend([f"Skipped: {skip_count}", f"Errors: {error_count}"])
    print(f"   {'  |  '.join(parts)}")
    print(f"   Output: {output_path}")

    if error_count > 0:
        sys.exit(1)

    # ── Write report ────────────────────────────────────────────
    if args.report:
        report = {
            "input": str(input_path) if input_path else "stdin",
            "output": str(output_path),
            "total": len(photo_files),
            "converted": success_count,
            "linked": linked_count,
            "skipped": skip_count,
            "errors": error_count,
        }
        report_path = Path(args.report).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📄 报告已保存: {report_path}")


if __name__ == "__main__":
    main()
