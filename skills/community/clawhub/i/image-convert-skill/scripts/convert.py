#!/usr/bin/env python3
"""
Image Converter - Convert various image formats to WebP

Usage:
    python convert.py input output [--quality N] [--max-size N] [--lossless]
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


def check_webp_support() -> bool:
    """Check if Pillow has WebP support."""
    try:
        # Try to create a minimal WebP image to verify support
        test_img = Image.new("RGB", (1, 1), color="white")
        import io

        buffer = io.BytesIO()
        test_img.save(buffer, format="WEBP")
        return True
    except Exception:
        return False


def validate_input_path(path: str) -> Path:
    """Validate that input path exists."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")
    return p


def validate_quality(quality: int) -> int:
    """Validate quality is in range 1-100."""
    if not 1 <= quality <= 100:
        raise ValueError(f"Quality must be between 1 and 100, got {quality}")
    return quality


def validate_max_size(max_size: Optional[int]) -> Optional[int]:
    """Validate max_size is positive if provided."""
    if max_size is not None and max_size <= 0:
        raise ValueError(f"max_size must be positive, got {max_size}")
    return max_size


def validate_to_format(to_format: Optional[str]) -> Optional[str]:
    if not to_format:
        return None
    supported = {"jpeg", "jpg", "png", "webp", "gif", "bmp", "tiff", "tif"}
    if to_format.lower() not in supported:
        raise ValueError(
            f"Unsupported format: {to_format}. Supported formats are: {', '.join(sorted(list(supported)))}"
        )
    return to_format


def get_output_path(
    input_path: Path, output_dir: Path, output_path: Optional[Path] = None
) -> Path:
    """Determine output path for conversion."""
    if output_path:
        return output_path

    return output_dir / input_path.stem


def load_image(path: Path) -> Image.Image:
    """Load and validate image file."""
    try:
        img = Image.open(path)
        # Force loading to detect errors early
        img.load()
        return img
    except Exception as e:
        raise IOError(f"Failed to load image {path}: {e}")


def convert_color_mode(img: Image.Image) -> Image.Image:
    """Convert image to suitable color mode for WebP."""
    # Handle different color modes
    if img.mode == "CMYK":
        # Convert CMYK to RGB
        img = img.convert("RGB")
    elif img.mode == "P" or img.mode == "PA":
        # Convert palette to RGBA
        if "transparency" in img.info:
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
    elif img.mode == "LA" or img.mode == "L":
        # Convert grayscale with alpha to RGBA, grayscale to RGB
        if img.mode == "LA":
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
    elif img.mode == "1":
        # Convert binary to RGB
        img = img.convert("RGB")

    return img


def calculate_new_size(img: Image.Image, max_size: Optional[int]) -> Tuple[int, int]:
    """Calculate new dimensions maintaining aspect ratio."""
    if max_size is None:
        return img.size

    width, height = img.size
    longest_edge = max(width, height)

    if longest_edge <= max_size:
        return img.size

    # Scale down maintaining aspect ratio
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    return (new_width, new_height)


def resize_image(img: Image.Image, max_size: Optional[int]) -> Image.Image:
    """Resize image if needed."""
    if max_size is None:
        return img

    new_size = calculate_new_size(img, max_size)
    if new_size == img.size:
        return img

    return img.resize(new_size, Image.Resampling.LANCZOS)


def strip_exif_keep_icc(img: Image.Image) -> Image.Image:
    """Strip EXIF data but preserve ICC profile."""
    icc_profile = img.info.get("icc_profile")

    if icc_profile:
        import io

        buffer = io.BytesIO()
        img.save(buffer, format=img.format or "PNG")
        buffer.seek(0)
        new_img = Image.open(buffer)
        new_img.info["icc_profile"] = icc_profile
        new_img.load()
        return new_img

    return img


def save_webp(img: Image.Image, path: Path, quality: int, lossless: bool) -> None:
    """Save image as WebP with specified settings."""
    path.parent.mkdir(parents=True, exist_ok=True)

    save_kwargs = {
        "format": "WEBP",
        "quality": quality,
        "lossless": lossless,
        "method": 4,
    }

    if not lossless:
        save_kwargs["subsampling"] = 0

    try:
        img.save(path, **save_kwargs)
    except Exception as e:
        raise IOError(f"Failed to save WebP to {path}: {e}")


def save_with_compression(
    img: Image.Image, path: Path, quality: int, compress_level: int
) -> None:
    """Save image with compression in its original format."""
    path.parent.mkdir(parents=True, exist_ok=True)

    ext = path.suffix.lower()
    save_kwargs = {}

    if ext in (".jpg", ".jpeg"):
        save_kwargs = {
            "format": "JPEG",
            "quality": quality,
            "optimize": True,
        }
    elif ext == ".png":
        save_kwargs = {
            "format": "PNG",
            "optimize": True,
            "compress_level": compress_level,
        }
    elif ext == ".gif":
        save_kwargs = {
            "format": "GIF",
            "optimize": True,
        }
    elif ext == ".webp":
        save_kwargs = {
            "format": "WEBP",
            "quality": quality,
            "method": 4,
        }
    elif ext in (".tiff", ".tif"):
        save_kwargs = {
            "format": "TIFF",
            "compression": "tiff_deflate",
            "compress_level": compress_level,
        }
    else:
        save_kwargs = {"format": img.format or "PNG"}

    try:
        img.save(path, **save_kwargs)
    except Exception as e:
        raise IOError(f"Failed to save {path}: {e}")


def save_image_format(
    img: Image.Image,
    path: Path,
    target_format: Optional[str] = None,
    quality: int = 90,
    lossless: bool = False,
    compress_level: int = 6,
) -> None:
    """Save image in a specific format with appropriate settings."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if not target_format:
        ext = path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            target_format = "JPEG"
        elif ext == ".png":
            target_format = "PNG"
        elif ext == ".webp":
            target_format = "WEBP"
        elif ext == ".gif":
            target_format = "GIF"
        elif ext == ".bmp":
            target_format = "BMP"
        elif ext in (".tiff", ".tif"):
            target_format = "TIFF"
        else:
            target_format = img.format or "PNG"

    target_format = target_format.upper()
    save_kwargs: dict = {"format": target_format}

    if target_format == "JPEG":
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True
        if img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

    elif target_format == "PNG":
        save_kwargs["optimize"] = True
        save_kwargs["compress_level"] = compress_level

    elif target_format == "WEBP":
        save_kwargs["quality"] = quality
        save_kwargs["lossless"] = lossless
        save_kwargs["method"] = 4
        if not lossless:
            save_kwargs["subsampling"] = 0

    elif target_format == "GIF":
        save_kwargs["optimize"] = True

    elif target_format == "TIFF":
        save_kwargs["compression"] = "tiff_deflate"
        save_kwargs["compress_level"] = compress_level

    elif target_format == "BMP":
        pass

    else:
        supported_formats = Image.registered_extensions().values()
        if target_format not in supported_formats and target_format not in Image.SAVE:
            raise IOError(f"Unsupported output format: {target_format}")

    try:
        img.save(path, **save_kwargs)
    except Exception as e:
        raise IOError(f"Failed to save {target_format} to {path}: {e}")


def resolve_target_format(
    output_path: Path,
    to_format: Optional[str] = None,
    compress: bool = False,
    input_path: Optional[Path] = None,
) -> Tuple[str, Path]:
    """
    Resolve the target image format and adjust the output path.

    Precedence:
    1. to_format flag
    2. explicit output_path extension
    3. legacy defaults (compress format or webp)

    Args:
        output_path: The intended output path.
        to_format: Optional target format string (e.g., 'jpeg', 'png').
        compress: Whether compression mode is enabled.
        input_path: Optional input path to derive format from in compress mode.

    Returns:
        A tuple of (target_format_str, actual_output_path).
    """
    target_format = None
    actual_path = output_path

    if to_format:
        target_format = to_format.upper()
        if not output_path.is_dir():
            ext = f".{target_format.lower()}"
            if target_format == "JPEG":
                ext = ".jpg"
            actual_path = output_path.with_suffix(ext)

    elif not output_path.is_dir() and output_path.suffix:
        ext = output_path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            target_format = "JPEG"
        elif ext == ".png":
            target_format = "PNG"
        elif ext == ".webp":
            target_format = "WEBP"
        elif ext == ".gif":
            target_format = "GIF"
        elif ext == ".bmp":
            target_format = "BMP"
        elif ext in (".tiff", ".tif"):
            target_format = "TIFF"
        else:
            target_format = ext.lstrip(".").upper()

    if not target_format:
        if compress and input_path:
            input_ext = input_path.suffix.lower()
            if input_ext in (".jpg", ".jpeg"):
                target_format = "JPEG"
            elif input_ext == ".png":
                target_format = "PNG"
            elif input_ext == ".webp":
                target_format = "WEBP"
            elif input_ext == ".gif":
                target_format = "GIF"
            elif input_ext == ".bmp":
                target_format = "BMP"
            elif input_ext in (".tiff", ".tif"):
                target_format = "TIFF"
            else:
                target_format = "PNG"

            if not output_path.is_dir():
                actual_path = output_path.with_suffix(input_path.suffix)
        else:
            target_format = "WEBP"
            if not output_path.is_dir():
                actual_path = output_path.with_suffix(".webp")

    if target_format == "JPG":
        target_format = "JPEG"

    supported_formats = {"JPEG", "PNG", "WEBP", "GIF", "BMP", "TIFF"}
    if target_format not in supported_formats:
        raise ValueError(f"Unsupported output format: {target_format}")

    return target_format, actual_path


def process_single_file(
    input_path: Path,
    output_path: Path,
    quality: int,
    max_size: Optional[int],
    lossless: bool,
    to_format: Optional[str] = None,
    compress: bool = False,
    compress_level: int = 6,
    compress_quality: int = 85,
) -> bool:
    """Process a single image file."""
    try:
        img = load_image(input_path)
        img = convert_color_mode(img)
        img = resize_image(img, max_size)
        img = strip_exif_keep_icc(img)

        target_format, actual_output_path = resolve_target_format(
            output_path, to_format=to_format, compress=compress, input_path=input_path
        )

        effective_quality = compress_quality if compress else quality

        save_image_format(
            img,
            actual_output_path,
            target_format=target_format,
            quality=effective_quality,
            lossless=lossless,
            compress_level=compress_level,
        )

        return True

    except (IOError, ValueError) as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return False


def get_supported_extensions() -> set:
    """Get set of supported image extensions."""
    return {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".tiff",
        ".tif",
        ".ppm",
        ".pgm",
        ".pbm",
        ".webp",
    }


def is_supported_image(path: Path) -> bool:
    """Check if file is a supported image format."""
    return path.suffix.lower() in get_supported_extensions()


def expand_input_patterns(patterns: list) -> list:
    """Expand glob patterns and file paths into a list of files."""
    files = []
    for pattern in patterns:
        p = Path(pattern)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for path in p.rglob("*"):
                if path.is_file() and is_supported_image(path):
                    files.append(path)
        else:
            matches = list(Path(".").glob(pattern))
            for match in matches:
                if match.is_file() and is_supported_image(match):
                    files.append(match)
    return list(set(files))


def process_batch_files(
    input_paths: list,
    output_base: Path,
    quality: int,
    max_size: Optional[int],
    lossless: bool,
    to_format: Optional[str] = None,
    compress: bool = False,
    compress_level: int = 6,
    compress_quality: int = 85,
    workers: int = 1,
    verbose: bool = False,
) -> Tuple[int, int, list]:
    """Process multiple files with optional parallel execution."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    success_count = 0
    failed_files = []
    total_count = len(input_paths)

    if workers <= 1:
        for i, input_path in enumerate(input_paths, 1):
            if output_base.is_dir():
                output_path = output_base / f"{input_path.stem}"
            else:
                output_path = output_base

            if verbose:
                print(f"[{i}/{total_count}] Processing: {input_path}")

            if process_single_file(
                input_path,
                output_path,
                quality,
                max_size,
                lossless,
                to_format,
                compress,
                compress_level,
                compress_quality,
            ):
                success_count += 1
                if verbose:
                    print(f"  -> Success: {output_path}")
            else:
                failed_files.append(str(input_path))
                if verbose:
                    print(f"  -> Failed")
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {}
            for input_path in input_paths:
                if output_base.is_dir():
                    output_path = output_base / f"{input_path.stem}"
                else:
                    output_path = output_base

                future = executor.submit(
                    process_single_file,
                    input_path,
                    output_path,
                    quality,
                    max_size,
                    lossless,
                    to_format,
                    compress,
                    compress_level,
                    compress_quality,
                )
                futures[future] = input_path

            for i, future in enumerate(as_completed(futures), 1):
                input_path = futures[future]
                if verbose:
                    print(f"[{i}/{total_count}] Processing: {input_path}")

                try:
                    result = future.result()
                    if result:
                        success_count += 1
                        if verbose:
                            print(f"  -> Success")
                    else:
                        failed_files.append(str(input_path))
                        if verbose:
                            print(f"  -> Failed")
                except Exception as e:
                    failed_files.append(str(input_path))
                    if verbose:
                        print(f"  -> Error: {e}")

    return success_count, total_count, failed_files


def process_directory(
    input_dir: Path,
    output_dir: Path,
    quality: int,
    max_size: Optional[int],
    lossless: bool,
    to_format: Optional[str] = None,
    compress: bool = False,
    compress_level: int = 6,
    compress_quality: int = 85,
) -> Tuple[int, int]:
    """Process all images in a directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    total_count = 0

    for path in input_dir.rglob("*"):
        if not path.is_file():
            continue
        if not is_supported_image(path):
            continue

        total_count += 1

        rel_path = path.relative_to(input_dir)
        output_path = output_dir / rel_path.parent / rel_path.stem

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if process_single_file(
            path,
            output_path,
            quality,
            max_size,
            lossless,
            to_format,
            compress,
            compress_level,
            compress_quality,
        ):
            success_count += 1
            print(f"Converted: {path} -> {output_path}")
        else:
            print(f"Failed: {path}", file=sys.stderr)

    return success_count, total_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert images between common formats (JPEG, PNG, WebP, GIF, BMP, TIFF)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic conversion:
    %(prog)s input.png output.jpg
    %(prog)s input.jpg output_dir/ --to-format webp
    %(prog)s photos/ webp_photos/ --max-size 1920

  Batch processing (multiple files):
    %(prog)s "*.jpg" output_dir/ --to-format png
    %(prog)s "img1.png img2.jpg img3.webp" output_dir/ --to-format webp
    %(prog)s file1.jpg,file2.png,file3.gif output_dir/ --threads 4

  WebP-specific:
    %(prog)s input.jpg output.webp
    %(prog)s input.png output/ --quality 85
    %(prog)s image.png lossless.webp --lossless

  Compression:
    %(prog)s input.png output.png --compress --compress-quality 75
        """,
    )

    parser.add_argument(
        "input", help="Input file, directory, glob pattern, or comma-separated files"
    )
    parser.add_argument("output", help="Output file or directory")
    parser.add_argument(
        "--quality",
        type=int,
        default=90,
        help="Quality for lossy formats like JPEG, WebP (1-100, default: 90)",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        help="Maximum dimension in pixels (longest edge). No scaling if not specified.",
    )
    parser.add_argument(
        "--lossless",
        action="store_true",
        help="Use lossless compression (ignores --quality)",
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Compress in original format (keep format, don't convert to WebP)",
    )
    parser.add_argument(
        "--compress-quality",
        type=int,
        default=85,
        help="Quality for --compress mode (1-100, default: 85)",
    )
    parser.add_argument(
        "--compress-level",
        type=int,
        default=6,
        help="Compression level for PNG/TIFF (0-9, default: 6)",
    )
    parser.add_argument(
        "--to-format",
        type=str,
        help="Explicitly specify target format (jpeg, png, webp, gif, bmp, tiff). Takes precedence over output extension.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Number of parallel threads for batch processing (default: 1)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed progress information",
    )

    args = parser.parse_args()

    # Check WebP support
    if not check_webp_support():
        print("ERROR: WebP support not available in Pillow.", file=sys.stderr)
        print(
            "Please install Pillow with WebP support: pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate inputs
    quality = validate_quality(args.quality)
    max_size = validate_max_size(args.max_size)
    to_format = validate_to_format(args.to_format)

    # Process based on input type
    output_path = Path(args.output)
    compress = args.compress
    compress_level = args.compress_level
    compress_quality = args.compress_quality
    verbose = args.verbose
    workers = args.threads

    # Check for batch input (comma-separated or glob pattern)
    if "," in args.input or "*" in args.input or "?" in args.input:
        if "," in args.input:
            input_items = [item.strip() for item in args.input.split(",")]
        else:
            input_items = [args.input]

        input_files = expand_input_patterns(input_items)

        if not input_files:
            print(
                f"ERROR: No matching files found for pattern: {args.input}",
                file=sys.stderr,
            )
            sys.exit(1)

        if output_path.is_file() and len(input_files) > 1:
            print(
                f"ERROR: Cannot output multiple files to a single file: {output_path}",
                file=sys.stderr,
            )
            sys.exit(1)

        output_path.mkdir(parents=True, exist_ok=True)

        print(f"Processing {len(input_files)} files with {workers} thread(s)...")

        success, total, failed = process_batch_files(
            input_files,
            output_path,
            quality,
            max_size,
            args.lossless,
            to_format,
            compress,
            compress_level,
            compress_quality,
            workers,
            verbose,
        )

        print(f"\nBatch completed: {success}/{total} files converted successfully")
        if failed:
            print(f"Failed files: {', '.join(failed)}", file=sys.stderr)

        if success < total:
            sys.exit(1)
        sys.exit(0)

    # Single file or directory input
    try:
        input_path = validate_input_path(args.input)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if input_path.is_file():
        if output_path.is_dir():
            output_path = get_output_path(input_path, output_path)

        success = process_single_file(
            input_path,
            output_path,
            quality,
            max_size,
            args.lossless,
            to_format,
            compress,
            compress_level,
            compress_quality,
        )

        if success:
            print(f"Converted: {input_path} -> {output_path}")
            sys.exit(0)
        else:
            sys.exit(1)

    elif input_path.is_dir():
        output_path.mkdir(parents=True, exist_ok=True)

        success, total = process_directory(
            input_path,
            output_path,
            quality,
            max_size,
            args.lossless,
            to_format,
            compress,
            compress_level,
            compress_quality,
        )

        print(f"\nCompleted: {success}/{total} files converted successfully")

        if success < total:
            sys.exit(1)
        sys.exit(0)

    else:
        print(
            f"ERROR: Input path is neither a file nor a directory: {input_path}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
