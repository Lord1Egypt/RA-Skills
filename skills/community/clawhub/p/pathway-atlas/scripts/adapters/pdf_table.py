"""Exact integer tables from explicitly selected regions of PDF text pages.

This deliberately does not infer table boundaries, repair missing cells, OCR
images, or normalize masked score bands. Hosts must inspect extract_pdf_text's
actual parser output before selecting one page, header, and inclusive line
range. Coverage describes only that selected region.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
import re

from . import (
    CellStatus,
    ColumnMapping,
    ExtractedRow,
    ExtractedTable,
    MappingError,
    StructuredValidationError,
    coerce_column_mapping,
    derive_coverage,
    reject_duplicate_rows,
    resolve_headers,
    validate_monotonicity,
)
from .pdf_text import extract_pdf_text


class PdfTableError(StructuredValidationError):
    """The selected PDF text region cannot be mapped without ambiguity."""


_INTEGER = re.compile(r"^[0-9]+$")


def _positive_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def extract_pdf_table(
    path: str | Path,
    *,
    mapping: Mapping[str, object] | ColumnMapping,
    headers: Sequence[str],
    page_number: int,
    header_line: int,
    first_data_line: int,
    last_data_line: int,
    column_group: int = 1,
    expected_caption: str | None = None,
) -> ExtractedTable:
    """Extract one caller-selected integer table region, with PDF provenance.

    Page and line numbers are one-based positions in ``extract_pdf_text``.
    ``headers`` names one complete column group. A physical header line may
    repeat that group for side-by-side tables; ``column_group`` selects one.
    Every source row must still contain all physical columns, including the
    unselected groups. Mapped columns require explicit score/rank roles (score
    and rank field names infer them via ColumnMapping).
    """
    page_number = _positive_integer(page_number, "page_number")
    header_line = _positive_integer(header_line, "header_line")
    first_data_line = _positive_integer(first_data_line, "first_data_line")
    last_data_line = _positive_integer(last_data_line, "last_data_line")
    column_group = _positive_integer(column_group, "column_group")
    if not header_line < first_data_line <= last_data_line:
        raise PdfTableError("PDF table line range is not strictly after its header")
    if isinstance(headers, (str, bytes, bytearray)) or not isinstance(headers, Sequence):
        raise TypeError("headers must be an ordered sequence of column labels")
    labels = list(headers)
    if not labels or any(
        not isinstance(label, str) or not label or label.split() != [label]
        for label in labels
    ):
        raise PdfTableError("PDF column labels must each be one exact text token")
    if expected_caption is not None and (
        not isinstance(expected_caption, str)
        or not expected_caption
        or expected_caption != expected_caption.strip()
    ):
        raise TypeError("expected_caption must be nonempty exact text or null")
    column_mapping = coerce_column_mapping(mapping)
    try:
        positions = resolve_headers(labels, column_mapping)
    except MappingError:
        raise PdfTableError("PDF column mapping is missing or ambiguous") from None
    if set(column_mapping.roles) != set(column_mapping):
        raise PdfTableError("PDF text tables require a numeric role for every mapped column")

    document = extract_pdf_text(path)
    if page_number > document.page_count:
        raise PdfTableError("selected PDF page is unavailable")
    page = document.pages[page_number - 1]
    if not page.text or page.image_only:
        raise PdfTableError("selected PDF page has no extractable text table")
    lines = page.text.splitlines()
    if last_data_line > len(lines):
        raise PdfTableError("selected PDF table region extends beyond the page text")
    if expected_caption is not None and expected_caption not in lines[:header_line - 1]:
        raise PdfTableError("expected PDF caption is not present before the selected header")
    observed_headers = lines[header_line - 1].split()
    group_count, remainder = divmod(len(observed_headers), len(labels))
    if (
        remainder
        or not group_count
        or observed_headers != labels * group_count
        or column_group > group_count
    ):
        raise PdfTableError("selected PDF header does not exactly match the declared column groups")

    rows: list[ExtractedRow] = []
    offset = (column_group - 1) * len(labels)
    for line_number in range(first_data_line, last_data_line + 1):
        tokens = lines[line_number - 1].split()
        if len(tokens) != len(observed_headers):
            raise PdfTableError("PDF data row has missing or additional columns")
        if any(_INTEGER.fullmatch(token) is None for token in tokens):
            raise PdfTableError("PDF data row contains masked, noninteger, or uncertain cells")
        values: dict[str, int] = {}
        for field, position in positions.items():
            value = int(tokens[offset + position])
            role = column_mapping.roles[field]
            if role == "rank" and value < 1:
                raise PdfTableError("PDF rank cells must be positive integers")
            if (
                role == "score"
                and column_mapping.score_scale is not None
                and not column_mapping.score_scale[0] <= value <= column_mapping.score_scale[1]
            ):
                raise PdfTableError("PDF score is outside the declared scale")
            values[field] = value
        rows.append(ExtractedRow(
            values=values,
            cell_status={field: CellStatus.EXACT for field in values},
            location=f"page[{page_number}]/line[{line_number}]/group[{column_group}]",
            confidence=1,
        ))
    reject_duplicate_rows(rows)
    validate_monotonicity(rows, column_mapping)
    coverage, coverage_warnings = derive_coverage(rows, column_mapping)
    return ExtractedTable(
        table_id=(
            f"pdf[{document.document_id}]/page[{page_number}]"
            f"/parser[{page.extraction_method}]/header[{header_line}]"
            f"/lines[{first_data_line}-{last_data_line}]/group[{column_group}]"
        ),
        caption=expected_caption,
        sheet=None,
        rows=tuple(rows),
        coverage=coverage,
        warnings=tuple(coverage_warnings),
        extraction_method="pdf-text-table",
    )


__all__ = ["PdfTableError", "extract_pdf_table"]
