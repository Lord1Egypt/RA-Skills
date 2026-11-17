#!/usr/bin/env python3
"""Minimal, self-contained PDF -> text helper for hkex_li_daily_factor_monitor.

Used ONLY as a fallback when the `pdftotext` CLI (poppler-utils) is not on the
machine. The main skill (SKILL.md) prefers `pdftotext -layout`; the agent then
reads the extracted text and reasons out the factor table itself. This script
exists so the skill still works on a box that has python3 but no poppler.

Usage:
    python3 pdf_to_text.py <path-to.pdf>

Writes the extracted plain text to stdout. Exits non-zero with a one-line
reason on stderr if extraction fails, so the caller can raise an explicit
error (the skill never silently skips a failed PDF).

Dependencies: tries the stdlib-friendly options in order and uses whichever is
installed. No pinned third-party requirement is forced on the host:
    1. pdfminer.six   (import pdfminer.high_level)   -- common, pure-python
    2. pypdf          (import pypdf)
    3. PyPDF2         (import PyPDF2)
"""
import sys


def extract(path: str) -> str:
    # 1) pdfminer.six -- best layout fidelity of the pure-python options.
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        return extract_text(path) or ""
    except ImportError:
        pass

    # 2) pypdf (maintained successor to PyPDF2).
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except ImportError:
        pass

    # 3) PyPDF2 (older, still widely installed).
    try:
        from PyPDF2 import PdfReader  # type: ignore
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except ImportError:
        pass

    raise RuntimeError(
        "no PDF text library available (need pdftotext CLI, or one of "
        "pdfminer.six / pypdf / PyPDF2)"
    )


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("usage: pdf_to_text.py <path-to.pdf>\n")
        return 2
    path = sys.argv[1]
    try:
        text = extract(path)
    except Exception as exc:  # surface, never swallow -- caller raises on this.
        sys.stderr.write(f"pdf_to_text: extraction failed for {path}: {exc}\n")
        return 1
    if not text.strip():
        sys.stderr.write(f"pdf_to_text: extracted empty text from {path}\n")
        return 1
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
