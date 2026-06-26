from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIREMENTS_PATH = Path(__file__).resolve().parent / "requirements-render.txt"


def dependency_error(package_name: str) -> RuntimeError:
    return RuntimeError(
        f"{package_name} is required to inspect rendered PDFs. "
        f"Install checker dependencies with `python3 -m pip install -r {REQUIREMENTS_PATH}`."
    )


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise dependency_error("pypdf") from exc

    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def has_table_data_after_header(extracted_text: str) -> bool:
    lines = [" ".join(line.split()) for line in extracted_text.splitlines() if line.strip()]
    table_header_pattern = re.compile(r"字段.*中文.*原文")
    non_table_noise = (
        re.compile(r"^Page\s+\d+\s*/\s*\d+$"),
        re.compile(r"^P\d+-B\d+$"),
        re.compile(r"^\[低置信度\]$"),
    )

    for index, line in enumerate(lines):
        header_match = table_header_pattern.search(line)
        if not header_match:
            continue
        trailing_content = line[header_match.end() :].strip()
        if trailing_content:
            return True
        for candidate in lines[index + 1 :]:
            if any(pattern.match(candidate) for pattern in non_table_noise):
                continue
            return True
    return False


def assert_expected_text(extracted_text: str, expected_table_markers: tuple[str, ...] = ()) -> None:
    normalized = " ".join(extracted_text.split())
    if not re.search(r"Page\s+\d+\s*/\s*\d+", normalized):
        raise AssertionError("Expected page numbering text like `Page 1 / 1` in the extracted PDF text.")
    if not re.search(r"P\d+-B\d+", extracted_text):
        raise AssertionError("Expected anchor traceability text like `P1-B3` in the extracted PDF text.")
    if "[低置信度]" not in extracted_text:
        raise AssertionError("Expected visible low-confidence marker text `[低置信度]` in the extracted PDF text.")

    table_headers = ("字段", "中文", "原文")
    if not all(header in extracted_text for header in table_headers):
        raise AssertionError("Expected preserved table headers `字段 / 中文 / 原文` in the extracted PDF text.")
    if expected_table_markers:
        missing_markers = [marker for marker in expected_table_markers if marker not in extracted_text]
        if missing_markers:
            raise AssertionError(
                f"Expected preserved table markers in the extracted PDF text: {', '.join(missing_markers)}."
            )
    elif not has_table_data_after_header(extracted_text):
        raise AssertionError("Expected preserved table content beyond the header row in the extracted PDF text.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check required visible text in a rendered translation PDF.")
    parser.add_argument("pdf_path", help="Path to the rendered PDF file.")
    parser.add_argument(
        "--expect-table-marker",
        action="append",
        default=[],
        help="Optional text that should appear in preserved table content. Repeat for multiple markers.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    pdf_path = Path(args.pdf_path)

    try:
        extracted_text = extract_pdf_text(pdf_path)
        assert_expected_text(extracted_text, expected_table_markers=tuple(args.expect_table_marker))
    except (AssertionError, FileNotFoundError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"PDF checks passed: {pdf_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
