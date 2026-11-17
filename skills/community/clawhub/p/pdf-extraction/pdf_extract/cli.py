"""Command-line interface for automatic PDF extraction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from pdf_extract import __version__
from pdf_extract.detector import MIN_TEXT_CHARS, analysis_to_dict
from pdf_extract.extract import (
    extract_pdf,
    result_to_dict,
    result_to_markdown,
    result_to_plain,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="pdf-extract",
        description=(
            "Extract text (and optionally tables/metadata) from PDFs. "
            "Automatically chooses native text extraction or OCR per page, "
            "so you do not need to decide whether the PDF is text or scanned."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  pdf-extract report.pdf
  pdf-extract scan.pdf -o out.txt
  pdf-extract mixed.pdf --json -o out.json
  pdf-extract doc.pdf --tables --format markdown -o out.md
  pdf-extract doc.pdf --pages 1-3,5 --mode auto
  pdf-extract scan.pdf --mode ocr --ocr-lang eng
  pdf-extract doc.pdf --analyze-only
""",
    )
    parser.add_argument(
        "pdf",
        type=Path,
        help="Path to the PDF file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write result to this file (default: stdout)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("text", "json", "markdown"),
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "text", "ocr"),
        default="auto",
        help="Extraction mode: auto detects per page (default: auto)",
    )
    parser.add_argument(
        "--pages",
        default=None,
        help="Pages to extract, e.g. 1-3,5 (default: all)",
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help="Also extract tables (native-text pages)",
    )
    parser.add_argument(
        "--layout",
        action="store_true",
        help="Preserve text layout for native extraction",
    )
    parser.add_argument(
        "--meta",
        action="store_true",
        help="Include document metadata in output",
    )
    parser.add_argument(
        "--ocr-lang",
        default="eng",
        help="Tesseract language(s), e.g. eng or eng+chi_tra (default: eng)",
    )
    parser.add_argument(
        "--ocr-dpi",
        type=int,
        default=200,
        help="OCR render DPI (default: 200)",
    )
    parser.add_argument(
        "--min-text-chars",
        type=int,
        default=MIN_TEXT_CHARS,
        help=f"Auto mode: min chars to treat page as text (default: {MIN_TEXT_CHARS})",
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only print per-page text/OCR classification (JSON)",
    )
    parser.add_argument(
        "--no-page-markers",
        action="store_true",
        help="Omit page separators in text output",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress progress messages on stderr",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _log(message: str, *, quiet: bool) -> None:
    if not quiet:
        print(message, file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point.

    Parameters
    ----------
    argv : sequence of str or None
        Argument list; defaults to ``sys.argv[1:]``.

    Returns
    -------
    int
        Process exit code (0 on success).
    """
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    pdf_path: Path = args.pdf
    if not pdf_path.exists():
        print(f"error: file not found: {pdf_path}", file=sys.stderr)
        return 1
    if not pdf_path.is_file():
        print(f"error: not a file: {pdf_path}", file=sys.stderr)
        return 1

    try:
        result = extract_pdf(
            pdf_path,
            pages=args.pages,
            mode=args.mode,
            include_tables=args.tables,
            layout=args.layout,
            ocr_lang=args.ocr_lang,
            ocr_dpi=args.ocr_dpi,
            min_text_chars=args.min_text_chars,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"error: unexpected failure: {exc}", file=sys.stderr)
        return 1

    modes = {a.mode.value for a in result.analyses}
    summary = ", ".join(
        f"p{a.page_number}={a.mode.value}" for a in result.analyses
    )
    _log(
        f"extracted {len(result.pages)}/{result.page_count} page(s); "
        f"modes={sorted(modes)}; {summary}",
        quiet=args.quiet,
    )

    if args.analyze_only:
        payload = {
            "path": result.path,
            "page_count": result.page_count,
            "analyses": [analysis_to_dict(a) for a in result.analyses],
        }
        output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "json":
        data = result_to_dict(result, include_analysis=True)
        if not args.meta:
            data.pop("metadata", None)
        output = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "markdown":
        output = result_to_markdown(result, include_meta=args.meta)
    else:
        chunks: list[str] = []
        if args.meta and result.metadata:
            chunks.append("# Metadata")
            for key, value in result.metadata.items():
                chunks.append(f"{key}: {value}")
            chunks.append("")
        chunks.append(
            result_to_plain(
                result,
                page_markers=not args.no_page_markers,
                include_tables=args.tables,
            ).rstrip()
        )
        output = "\n".join(chunks).rstrip() + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        _log(f"wrote {args.output}", quiet=args.quiet)
    else:
        sys.stdout.write(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
