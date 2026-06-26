from __future__ import annotations

import argparse
import json
from pathlib import Path

from export_long_image import export_image
from render_markdown_mobile_long_image import render_markdown_text


def _write_markdown_input(markdown_text: str, output_dir: Path, stem: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / f"{stem}.source.md"
    markdown_path.write_text(markdown_text, encoding="utf-8")
    return markdown_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert local Markdown or pasted Markdown text into a mobile-friendly PNG/JPG long image."
    )
    parser.add_argument("--input-file", default="", help="Path to a Markdown file.")
    parser.add_argument(
        "--markdown-text",
        default="",
        help="Direct Markdown text input.",
    )
    parser.add_argument(
        "--output-image",
        default="",
        help="Output image path. Defaults beside the source or in the current directory.",
    )
    parser.add_argument(
        "--output-html",
        default="",
        help="Output HTML path. Defaults beside the source or in the current directory.",
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpg"],
        default="png",
        help="Image format. Defaults to png.",
    )
    parser.add_argument(
        "--browser-executable",
        default="",
        help="Optional explicit local browser executable path.",
    )
    args = parser.parse_args()

    if not args.input_file and not args.markdown_text:
        raise SystemExit("Provide either --input-file or --markdown-text")
    if args.input_file and args.markdown_text:
        raise SystemExit("Use either --input-file or --markdown-text, not both")

    if args.input_file:
        markdown_path = Path(args.input_file).resolve()
        markdown_text = markdown_path.read_text(encoding="utf-8")
        stem = markdown_path.stem
        base_dir = markdown_path.parent
    else:
        stem = "markdown-long-image"
        markdown_text = args.markdown_text
        if args.output_html:
            base_dir = Path(args.output_html).resolve().parent
        elif args.output_image:
            base_dir = Path(args.output_image).resolve().parent
        else:
            base_dir = Path.cwd()
        markdown_path = _write_markdown_input(markdown_text, base_dir, stem)

    output_html = (
        Path(args.output_html).resolve()
        if args.output_html
        else (base_dir / f"{stem}.mobile-long.html").resolve()
    )
    output_image = (
        Path(args.output_image).resolve()
        if args.output_image
        else (base_dir / f"{stem}.mobile-long.{args.format}").resolve()
    )

    html = render_markdown_text(markdown_text, title_hint=stem)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")

    export_result = export_image(
        html_path=output_html,
        output_image=output_image,
        image_format=args.format,
        browser_executable=args.browser_executable or None,
    )

    payload = {
        "markdown_source": str(markdown_path),
        "output_html": str(output_html),
        "output_image": str(output_image),
        "export": export_result,
    }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
