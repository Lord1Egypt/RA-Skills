"""Clean privacy metadata from user-owned images by writing sanitized copies.

The script intentionally avoids in-place edits. It re-encodes image pixels into a
fresh output file, then reopens the result and reports whether common metadata
and provenance markers are still visible.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps, UnidentifiedImageError


SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}
PRIVACY_INFO_KEYS = {
    "author",
    "comment",
    "copyright",
    "description",
    "dpi",
    "exif",
    "icc_profile",
    "iptc",
    "photoshop",
    "software",
    "xmp",
    "xml:com.adobe.xmp",
}
PROVENANCE_MARKERS = {
    "c2pa": b"c2pa",
    "C2PA": b"C2PA",
    "JUMBF": b"JUMBF",
    "jumb": b"jumb",
    "caBX": b"caBX",
}


@dataclass
class FileReport:
    input: str
    output: str | None
    status: str
    input_bytes: int | None = None
    output_bytes: int | None = None
    dimensions: tuple[int, int] | None = None
    metadata_keys_found: list[str] = field(default_factory=list)
    provenance_markers_found: list[str] = field(default_factory=list)
    warning: str | None = None
    error: str | None = None


def format_for_source(src: Path, requested: str) -> tuple[str, str]:
    if requested == "jpg":
        return "JPEG", ".jpg"
    if requested == "png":
        return "PNG", ".png"
    if src.suffix.lower() in {".jpg", ".jpeg"}:
        return "JPEG", ".jpg"
    return "PNG", ".png"


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def supported_files(root: Path, recursive: bool, output_root: Path | None) -> list[Path]:
    candidates: Iterable[Path] = root.rglob("*") if recursive else root.iterdir()
    files: list[Path] = []
    for path in candidates:
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTS:
            continue
        if output_root is not None and is_relative_to(path, output_root):
            continue
        files.append(path)
    return sorted(files)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(1, 10000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find an unused output name for {path}")


def resolve_output(
    src: Path,
    fmt: str,
    output: str | None,
    output_dir: str | None,
    overwrite: bool,
    batch: bool,
) -> tuple[Path, str]:
    output_format, ext = format_for_source(src, fmt)

    explicit_output = False
    if output:
        explicit_output = True
        dest = Path(output)
        if dest.exists() and dest.is_dir():
            dest = dest / f"{src.stem}-clean{ext}"
    else:
        root = Path(output_dir) if output_dir else src.parent
        if batch and output_dir is None:
            root = src.parent / "metadata-cleaned"
        dest = root / f"{src.stem}-clean{ext}"

    dest = dest.expanduser()
    if dest.resolve() == src.resolve():
        raise ValueError(f"Refusing to overwrite input file: {src}")
    if dest.exists() and not overwrite:
        if explicit_output:
            raise FileExistsError(f"Output already exists: {dest}")
        dest = unique_path(dest)
    return dest, output_format


def has_transparency(img: Image.Image) -> bool:
    return img.mode in {"RGBA", "LA"} or (
        img.mode == "P" and "transparency" in img.info
    )


def clean_image(src: Path, dest: Path, output_format: str, quality: int) -> str | None:
    warning = None
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img)
        img.load()

        if output_format == "JPEG":
            if has_transparency(img):
                rgba = img.convert("RGBA")
                background = Image.new("RGB", rgba.size, (255, 255, 255))
                background.paste(rgba, mask=rgba.getchannel("A"))
                clean = background
                warning = "Transparency was composited onto a white background for JPEG output."
            elif img.mode != "RGB":
                clean = img.convert("RGB")
            else:
                clean = img.copy()
            save_kwargs = {"format": "JPEG", "quality": quality, "optimize": True}
        else:
            clean = img.convert("RGBA") if img.mode == "P" else img.copy()
            save_kwargs = {"format": "PNG", "optimize": True}

        clean.info.clear()
        clean.save(dest, **save_kwargs)
        clean.close()
    return warning


def collect_metadata_keys(path: Path) -> tuple[tuple[int, int], list[str]]:
    with Image.open(path) as img:
        keys = {
            key
            for key in img.info
            if key.lower() in PRIVACY_INFO_KEYS or "xmp" in key.lower()
        }
        try:
            if img.getexif():
                keys.add("exif")
        except Exception:
            keys.add("exif-unreadable")
        return img.size, sorted(keys)


def scan_provenance_markers(path: Path) -> list[str]:
    found: set[str] = set()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            for name, marker in PROVENANCE_MARKERS.items():
                if marker in chunk:
                    found.add(name)
    return sorted(found)


def process_file(
    src: Path,
    fmt: str,
    output: str | None,
    output_dir: str | None,
    quality: int,
    overwrite: bool,
    batch: bool,
    dry_run: bool,
) -> FileReport:
    report = FileReport(input=str(src), output=None, status="error")
    try:
        dest, output_format = resolve_output(src, fmt, output, output_dir, overwrite, batch)
        report.output = str(dest)
        report.input_bytes = src.stat().st_size

        if dry_run:
            report.status = "dry-run"
            return report

        dest.parent.mkdir(parents=True, exist_ok=True)
        warning = clean_image(src, dest, output_format, quality)
        dimensions, metadata_keys = collect_metadata_keys(dest)
        markers = scan_provenance_markers(dest)

        report.status = "ok" if not metadata_keys and not markers else "warning"
        report.output_bytes = dest.stat().st_size
        report.dimensions = dimensions
        report.metadata_keys_found = metadata_keys
        report.provenance_markers_found = markers
        report.warning = warning
        if metadata_keys or markers:
            details = []
            if metadata_keys:
                details.append(f"metadata keys still visible: {', '.join(metadata_keys)}")
            if markers:
                details.append(f"provenance marker strings still visible: {', '.join(markers)}")
            report.warning = "; ".join(filter(None, [warning, *details]))
    except (FileExistsError, ValueError, UnidentifiedImageError, OSError, RuntimeError) as exc:
        report.error = str(exc)
    return report


def write_manifest(path: Path, reports: list[FileReport]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([asdict(report) for report in reports], indent=2),
        encoding="utf-8",
    )


def human_size(num_bytes: int | None) -> str:
    if num_bytes is None:
        return "-"
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.1f} MB"


def print_human_report(reports: list[FileReport], manifest: Path | None) -> None:
    processed = sum(1 for report in reports if report.status in {"ok", "warning"})
    failures = sum(1 for report in reports if report.status == "error")
    dry_runs = sum(1 for report in reports if report.status == "dry-run")

    for report in reports:
        label = report.status.upper()
        if report.status == "error":
            print(f"{label}: {report.input}: {report.error}")
            continue
        dimensions = (
            f"{report.dimensions[0]}x{report.dimensions[1]}"
            if report.dimensions
            else "not written"
        )
        print(
            f"{label}: {report.input} -> {report.output} "
            f"({human_size(report.input_bytes)} -> {human_size(report.output_bytes)}, {dimensions})"
        )
        if report.warning:
            print(f"  warning: {report.warning}")

    print(f"\nSummary: {processed} processed, {dry_runs} dry-run, {failures} failed")
    if manifest is not None:
        print(f"Manifest: {manifest}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean privacy metadata from user-owned images by writing sanitized copies."
    )
    parser.add_argument("input", help="Input image file or folder")
    parser.add_argument("-o", "--output", help="Output file path for single-file mode")
    parser.add_argument("--output-dir", help="Directory for output copies")
    parser.add_argument(
        "-f",
        "--format",
        dest="fmt",
        default="preserve",
        choices=["preserve", "jpg", "png"],
        help="Output format: preserve JPEG inputs and write other inputs as PNG by default",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=95,
        help="JPEG quality from 1 to 100 (default: 95)",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output copies")
    parser.add_argument("--recursive", action="store_true", help="Process folders recursively")
    parser.add_argument("--dry-run", action="store_true", help="Show planned outputs without writing files")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON only")
    parser.add_argument(
        "--manifest",
        nargs="?",
        const="metadata-clean-report.json",
        help="Write a JSON manifest; optionally provide the manifest path",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.quality < 1 or args.quality > 100:
        print("Error: --quality must be between 1 and 100", file=sys.stderr)
        return 2
    if args.output and args.output_dir:
        print("Error: use either --output or --output-dir, not both", file=sys.stderr)
        return 2

    src = Path(args.input).expanduser()
    reports: list[FileReport]
    batch = src.is_dir()
    output_root = Path(args.output_dir).expanduser() if args.output_dir else None
    if batch:
        if args.output:
            print("Error: --output is only valid for single-file mode", file=sys.stderr)
            return 2
        if output_root is None:
            output_root = src / "metadata-cleaned"
        files = supported_files(src, args.recursive, output_root)
        if not files:
            print(f"No supported image files found in {src}", file=sys.stderr)
            return 2
        reports = [
            process_file(
                file,
                args.fmt,
                None,
                str(output_root),
                args.quality,
                args.overwrite,
                True,
                args.dry_run,
            )
            for file in files
        ]
    elif src.is_file():
        if src.suffix.lower() not in SUPPORTED_EXTS:
            print(f"Error: unsupported image extension: {src.suffix}", file=sys.stderr)
            return 2
        reports = [
            process_file(
                src,
                args.fmt,
                args.output,
                args.output_dir,
                args.quality,
                args.overwrite,
                False,
                args.dry_run,
            )
        ]
    else:
        print(f"Error: input path does not exist: {src}", file=sys.stderr)
        return 2

    manifest_path = None
    if args.manifest:
        manifest_path = Path(args.manifest)
        if not manifest_path.is_absolute():
            if batch:
                manifest_path = output_root / manifest_path
            else:
                first_output = reports[0].output
                manifest_path = (Path(first_output).parent if first_output else src.parent) / manifest_path
        if not args.dry_run:
            write_manifest(manifest_path, reports)

    if args.json:
        print(json.dumps([asdict(report) for report in reports], indent=2))
    else:
        print_human_report(reports, manifest_path if not args.dry_run else None)

    return 1 if any(report.status == "error" for report in reports) else 0


if __name__ == "__main__":
    raise SystemExit(main())
