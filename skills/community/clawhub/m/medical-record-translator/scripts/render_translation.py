from __future__ import annotations

import argparse
import re
import sys
from html import escape
from pathlib import Path
from string import Template


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_ROOT / "assets"
TEMPLATE_PATH = ASSETS_DIR / "translation_template.html"
CSS_PATH = ASSETS_DIR / "translation_print.css"
REQUIREMENTS_PATH = Path(__file__).resolve().parent / "requirements-render.txt"


def dependency_error(package_name: str) -> RuntimeError:
    return RuntimeError(
        f"{package_name} is required for Markdown-to-PDF export. "
        f"Install renderer dependencies with `python3 -m pip install -r {REQUIREMENTS_PATH}`."
    )


def load_weasyprint_html():
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise dependency_error("WeasyPrint") from exc
    return HTML


def load_markdown_renderer():
    try:
        import markdown as markdown_package
    except ImportError as exc:
        raise dependency_error("Markdown") from exc
    return markdown_package.markdown


def render_markdown_fragment(markdown_text: str) -> str:
    markdown_renderer = load_markdown_renderer()
    return markdown_renderer(
        markdown_text,
        extensions=["extra", "sane_lists", "tables"],
        output_format="html5",
    )


def extract_document_title(markdown_text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown_text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return fallback


def build_html_document(markdown_text: str, document_title: str, source_name: str) -> str:
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    css_text = CSS_PATH.read_text(encoding="utf-8")
    body_html = render_markdown_fragment(markdown_text)
    return template.substitute(
        document_title=escape(document_title),
        source_name=escape(source_name),
        css_text=css_text,
        body_html=body_html,
    )


def resolve_output_path(
    markdown_path: Path,
    output_dir: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    if output_path is not None:
        return output_path.resolve()
    if output_dir is not None:
        return (output_dir / f"{markdown_path.stem}.pdf").resolve()
    return markdown_path.with_suffix(".pdf")


def render_markdown_to_pdf(
    markdown_path: Path,
    output_dir: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    source_path = markdown_path.resolve()
    markdown_text = source_path.read_text(encoding="utf-8")
    document_title = extract_document_title(markdown_text, source_path.stem)
    html_document = build_html_document(markdown_text, document_title, source_path.name)
    target_path = resolve_output_path(source_path, output_dir=output_dir, output_path=output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    html_class = load_weasyprint_html()
    html = html_class(string=html_document, base_url=str(SKILL_ROOT))
    html.write_pdf(target=str(target_path))
    return target_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a medical record translation Markdown file to PDF with a fixed template.",
    )
    parser.add_argument("input_markdown", help="Path to the translation Markdown file.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory where the PDF will be written. Defaults to the input file directory.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional explicit PDF output path. Overrides --output-dir when both are provided.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    markdown_path = Path(args.input_markdown)
    output_dir = Path(args.output_dir) if args.output_dir else None
    output_path = Path(args.output) if args.output else None

    try:
        pdf_path = render_markdown_to_pdf(markdown_path, output_dir=output_dir, output_path=output_path)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
