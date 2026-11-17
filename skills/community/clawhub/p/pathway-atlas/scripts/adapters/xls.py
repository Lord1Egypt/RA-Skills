"""Read one selected legacy XLS worksheet without converting its source bytes."""

from __future__ import annotations

from collections.abc import Mapping
from io import StringIO
from pathlib import Path
import re
import struct
from typing import Any

from . import (
    CellStatus, ColumnMapping, ExtractedRow, ExtractedTable, MappingError,
    StructuredAdapterError, StructuredValidationError, coerce_column_mapping,
    derive_coverage, read_stable_local_file, reject_duplicate_rows,
    resolve_headers, validate_monotonicity,
)
from .spreadsheet import _header_value, _normalize_value


class XlsDependencyError(StructuredAdapterError):
    """The optional legacy workbook reader is unavailable."""


def _load_xlrd() -> Any:
    try:
        import xlrd
    except (ImportError, ModuleNotFoundError):
        raise XlsDependencyError("XLS extraction requires xlrd>=2,<3") from None
    if not re.match(r"^2\.", getattr(xlrd, "__version__", "")):
        raise XlsDependencyError("XLS extraction requires xlrd>=2,<3") from None
    return xlrd


def _formula_cells(book: Any, worksheet: Any) -> frozenset[tuple[int, int]]:
    """xlrd exposes cached formula results as values; retain the BIFF formula flag."""
    if book.biff_version < 50:
        raise StructuredValidationError("XLS extraction requires BIFF5 or BIFF8")
    source = book.mem
    position = worksheet._position
    formulas: set[tuple[int, int]] = set()
    while position + 4 <= len(source):
        code, size = struct.unpack_from("<HH", source, position)
        position += 4
        if position + size > len(source):
            raise StructuredValidationError("XLS worksheet records are truncated")
        if code == 0x000A:
            return frozenset(formulas)
        if code in {0x0006, 0x0206, 0x0406}:
            if size < 6:
                raise StructuredValidationError("XLS formula record is truncated")
            formulas.add(struct.unpack_from("<HH", source, position))
        position += size
    raise StructuredValidationError("XLS worksheet has no complete end record")


def _column_letter(number: int) -> str:
    text = ""
    while number:
        number, digit = divmod(number - 1, 26)
        text = chr(65 + digit) + text
    return text


def extract_xls(
    path: str | Path, *, sheet: str, mapping: ColumnMapping | Mapping[str, object],
) -> ExtractedTable:
    """Map exact source headers and preserve nonexact cells and physical locations."""
    if not isinstance(sheet, str) or not sheet or sheet != sheet.strip():
        raise StructuredValidationError("sheet must be a nonempty exact worksheet name")
    column_mapping = coerce_column_mapping(mapping)
    source = read_stable_local_file(path, suffixes=(".xls",))
    # Some official downloads incorrectly declare text/html; only workbook bytes count.
    if not source.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1") and source[:2] != b"\x09\x08":
        raise StructuredValidationError("XLS input is not a binary workbook")
    xlrd = _load_xlrd()
    book = None
    try:
        book = xlrd.open_workbook(
            file_contents=source, formatting_info=True, on_demand=True,
            ragged_rows=True, logfile=StringIO(),
        )
        if sheet not in book.sheet_names():
            raise StructuredValidationError("selected worksheet does not exist")
        worksheet = book.sheet_by_name(sheet)
        if not worksheet.nrows:
            raise MappingError("selected worksheet has no explicit header row")
        if worksheet.nrows * worksheet.ncols > 2_000_000:
            raise StructuredValidationError("selected XLS worksheet exceeds the cell limit")
        formulas = _formula_cells(book, worksheet)
        headers = [_header_value(cell.value) for cell in worksheet.row(0)]
        positions = resolve_headers(headers, column_mapping)
        hidden_sheet = bool(worksheet.visibility)
        hidden_header = bool(getattr(worksheet.rowinfo_map.get(0), "hidden", False))
        rows: list[ExtractedRow] = []
        for row_index in range(1, worksheet.nrows):
            cells = worksheet.row(row_index)
            if not cells or all(cell.ctype == xlrd.XL_CELL_EMPTY for cell in cells):
                continue
            values: dict[str, Any] = {}
            statuses: dict[str, CellStatus] = {}
            warnings: list[str] = []
            hidden_row = bool(getattr(worksheet.rowinfo_map.get(row_index), "hidden", False))
            truncated = any(position >= len(cells) for position in positions.values())
            if hidden_row:
                warnings.append("hidden-row")
            if truncated:
                warnings.append("truncated-row")
            for canonical, column in positions.items():
                cell = cells[column] if column < len(cells) else None
                value = cell.value if cell is not None else None
                kind = cell.ctype if cell is not None else xlrd.XL_CELL_EMPTY
                merged = any(r0 <= row_index < r1 and c0 <= column < c1 for r0, r1, c0, c1 in worksheet.merged_cells)
                hidden_column = bool(getattr(worksheet.colinfo_map.get(column), "hidden", False))
                if kind in {xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK}:
                    value = None
                if (row_index, column) in formulas:
                    status = CellStatus.FORMULA
                elif merged:
                    status = CellStatus.MERGED
                elif kind == xlrd.XL_CELL_ERROR:
                    value, status = None, CellStatus.INVALID
                elif kind == xlrd.XL_CELL_DATE:
                    value, status = xlrd.xldate_as_datetime(value, book.datemode).isoformat(), CellStatus.UNCERTAIN
                else:
                    if kind == xlrd.XL_CELL_BOOLEAN:
                        value = bool(value)
                    value, status = _normalize_value(value, column_mapping.roles.get(canonical), column_mapping.score_scale)
                if (hidden_sheet or hidden_header or hidden_row or hidden_column or truncated) and status is CellStatus.EXACT:
                    status = CellStatus.UNCERTAIN
                values[canonical], statuses[canonical] = value, status
                if status is not CellStatus.EXACT:
                    warnings.append(f"{status.value}-cell:{canonical}")
                if hidden_column:
                    warnings.append(f"hidden-column:{canonical}")
            nonexact = sum(status is not CellStatus.EXACT for status in statuses.values())
            rows.append(ExtractedRow(
                values, statuses,
                f"{sheet}!A{row_index + 1}:{_column_letter(len(headers))}{row_index + 1}",
                1.0 - nonexact / len(statuses) * 0.5, tuple(warnings),
            ))
    except (MappingError, StructuredValidationError):
        raise
    except Exception:
        raise StructuredValidationError("XLS input could not be parsed safely") from None
    finally:
        if book is not None:
            book.release_resources()
    reject_duplicate_rows(rows)
    # A score-distribution series orders score against cumulative rank. School
    # admission sheets instead follow institution/program codes: min_score and
    # min_rank vary freely between rows and must retain their original order.
    if column_mapping.roles.get("score") == "score" and "rank" in column_mapping.roles.values():
        validate_monotonicity(rows, column_mapping)
    coverage, coverage_warnings = derive_coverage(rows, column_mapping)
    warnings = []
    if not rows:
        warnings.append("empty-table")
    if hidden_sheet:
        warnings.append("hidden-sheet")
    if hidden_header:
        warnings.append("hidden-header-row")
    if any(status is not CellStatus.EXACT for row in rows for status in row.cell_status.values()):
        warnings.append("coverage-excludes-nonexact-rows")
    warnings.extend(coverage_warnings)
    return ExtractedTable(f"sheet:{sheet}", None, sheet, tuple(rows), coverage, tuple(warnings), "xls-worksheet")


__all__ = ["XlsDependencyError", "extract_xls"]
