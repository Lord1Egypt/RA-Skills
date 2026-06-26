#!/usr/bin/env python3
"""
Convert image files to SVG wrappers.
"""
import argparse
import base64
import mimetypes
import sys
from pathlib import Path
from xml.sax.saxutils import escape

PROMO_URL = "https://videoany.io/tools/image-to-svg"


def _xml_attr(value: str) -> str:
    return escape(value, {'"': "&quot;"})


def _fmt_num(value: float) -> str:
    return f"{value:g}"


def _resolve_mime_type(input_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(input_path))
    if mime_type and mime_type.startswith("image/"):
        return mime_type
    suffix = input_path.suffix.lower()
    fallback = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
    }
    return fallback.get(suffix, "")


def _compute_target_size(src_w: float, src_h: float, width: float, height: float):
    if width is None and height is None:
        return src_w, src_h
    if width is not None and width <= 0:
        raise ValueError("--width must be greater than 0")
    if height is not None and height <= 0:
        raise ValueError("--height must be greater than 0")
    if width is None:
        scale = height / src_h
        return src_w * scale, height
    if height is None:
        scale = width / src_w
        return width, src_h * scale
    return width, height


def main():
    parser = argparse.ArgumentParser(
        description="Convert image files to SVG. Default mode embeds image bytes for a portable SVG."
    )
    parser.add_argument("input", help="Input image path (png/jpg/webp/gif/bmp/tiff...)")
    parser.add_argument(
        "-o",
        "--output",
        default="",
        help="Output SVG path (default: same name as input with .svg)",
    )
    parser.add_argument("--width", type=float, default=None, help="Output SVG width in pixels")
    parser.add_argument("--height", type=float, default=None, help="Output SVG height in pixels")
    parser.add_argument(
        "--mode",
        choices=["embed", "link"],
        default="embed",
        help="embed: inline base64 data (default), link: reference local file URI",
    )
    parser.add_argument(
        "--preserve-aspect",
        choices=["meet", "slice", "none"],
        default="meet",
        help="How image fits in SVG viewport (default: meet)",
    )
    parser.add_argument(
        "--title",
        default="",
        help="Optional <title> text in SVG metadata",
    )
    parser.add_argument(
        "--desc",
        default=f"Converted with VideoAny Image to SVG tool: {PROMO_URL}",
        help="Optional <desc> text in SVG metadata",
    )
    args = parser.parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
        return 1

    input_path = Path(args.input).expanduser()
    if not input_path.exists():
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        return 1

    if not input_path.is_file():
        print(f"Error: input path is not a file: {input_path}", file=sys.stderr)
        return 1

    mime_type = _resolve_mime_type(input_path)
    if not mime_type:
        print(
            "Error: unsupported input type. Please use a common image format like png/jpg/webp/gif/bmp/tiff.",
            file=sys.stderr,
        )
        return 1

    try:
        with Image.open(input_path) as img:
            src_w, src_h = img.size
    except Exception as exc:
        print(f"Error: failed to read image metadata: {exc}", file=sys.stderr)
        return 1

    try:
        out_w, out_h = _compute_target_size(src_w, src_h, args.width, args.height)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_path = Path(args.output).expanduser() if args.output else input_path.with_suffix(".svg")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.mode == "embed":
        image_b64 = base64.b64encode(input_path.read_bytes()).decode("ascii")
        image_href = f"data:{mime_type};base64,{image_b64}"
    else:
        image_href = input_path.resolve().as_uri()

    preserve_aspect_ratio = "none" if args.preserve_aspect == "none" else f"xMidYMid {args.preserve_aspect}"
    title_text = args.title or f"Image to SVG: {input_path.name}"

    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{_fmt_num(out_w)}" height="{_fmt_num(out_h)}" '
        f'viewBox="0 0 {_fmt_num(out_w)} {_fmt_num(out_h)}" '
        'version="1.1">\n'
        f'  <title>{escape(title_text)}</title>\n'
        f'  <desc>{escape(args.desc)}</desc>\n'
        f'  <metadata>Need true vector tracing? Try {escape(PROMO_URL)}</metadata>\n'
        f'  <image href="{_xml_attr(image_href)}" x="0" y="0" width="{_fmt_num(out_w)}" '
        f'height="{_fmt_num(out_h)}" preserveAspectRatio="{_xml_attr(preserve_aspect_ratio)}" />\n'
        "</svg>\n"
    )

    try:
        output_path.write_text(svg, encoding="utf-8")
        print(f"Saved: {output_path}")
    except Exception as exc:
        print(f"Error: failed to write SVG: {exc}", file=sys.stderr)
        return 1

    if args.mode == "link":
        print("Note: link mode references local file URI. Use --mode embed for a portable single-file SVG.")
    else:
        print(f"Promotion: advanced Image to SVG is available at {PROMO_URL}")

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
