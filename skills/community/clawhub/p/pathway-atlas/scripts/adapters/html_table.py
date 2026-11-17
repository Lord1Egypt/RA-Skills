"""File-only extraction of one explicitly selected HTML table."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path
import re
from typing import Any

from . import (
    CellStatus,
    ColumnMapping,
    ExtractedRow,
    ExtractedTable,
    MappingError,
    StructuredValidationError,
    coerce_column_mapping,
    derive_coverage,
    read_stable_local_file,
    reject_duplicate_rows,
    resolve_headers,
    validate_monotonicity,
)


_MASKED = re.compile(r"^(?:[-—–*…]+|前\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?\s*(?:以上|及以上|以下|及以下|\+))$")
_VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}
_GLOBAL_ATTRIBUTES = {
    "accesskey",
    "autocapitalize",
    "autofocus",
    "class",
    "contenteditable",
    "dir",
    "draggable",
    "enterkeyhint",
    "exportparts",
    "hidden",
    "id",
    "inert",
    "inputmode",
    "is",
    "itemid",
    "itemprop",
    "itemref",
    "itemscope",
    "itemtype",
    "lang",
    "nonce",
    "part",
    "popover",
    "slot",
    "spellcheck",
    "style",
    "tabindex",
    "title",
    "translate",
}


class HtmlStructureError(StructuredValidationError):
    """Raised when a selected HTML table cannot preserve cell positions."""


@dataclass
class _Cell:
    kind: str
    parts: list[str] = field(default_factory=list)
    merged: bool = False

    @property
    def raw_text(self) -> str:
        return "".join(self.parts)


@dataclass
class _Row:
    section: str
    cells: list[_Cell] = field(default_factory=list)
    closed: bool = False


@dataclass
class _Table:
    index: int
    caption_parts: list[str] = field(default_factory=list)
    rows: list[_Row] = field(default_factory=list)
    closed: bool = False
    malformed: bool = False
    caption_seen: bool = False

    @property
    def caption(self) -> str | None:
        text = "".join(self.caption_parts).strip()
        return text or None


def _column_attributes(attrs: list[tuple[str, str | None]]) -> tuple[bool, bool]:
    has_span = False
    for raw_name, value in attrs:
        name = raw_name.casefold()
        if name == "span":
            if value is None or re.fullmatch(r"[0-9]+", value) is None or not 1 <= int(value) <= 1000:
                return False, False
            has_span = True
        elif name not in _GLOBAL_ATTRIBUTES and not name.startswith(("aria-", "data-")):
            return False, False
    return True, has_span


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[_Table] = []
        self._table: _Table | None = None
        self._row: _Row | None = None
        self._cell: _Cell | None = None
        self._section: str | None = None
        self._caption = False
        self._ignored_depth = 0
        self._nested_table_depth = 0
        self._inline_stack: list[str] = []
        self._colgroup = False
        self._colgroup_has_span = False
        self._column_groups_seen = False
        self._data_structure_started = False

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        normalized = tag.casefold()
        if normalized == "colgroup":
            if self._table is not None:
                self._table.malformed = True
            return
        if normalized not in _VOID_TAGS:
            self.handle_endtag(tag)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.casefold()
        if self._ignored_depth:
            if tag in {"script", "style"}:
                self._ignored_depth += 1
            return
        attribute_names = [name.casefold() for name, _ in attrs]
        duplicate_attributes = len(attribute_names) != len(set(attribute_names))
        if tag in {"script", "style"}:
            if duplicate_attributes and self._table is not None:
                self._table.malformed = True
            self._ignored_depth += 1
            return
        if tag == "table":
            if self._table is not None:
                self._table.malformed = True
                self._nested_table_depth += 1
                return
            self._table = _Table(index=len(self.tables) + 1, malformed=duplicate_attributes)
            return
        if self._nested_table_depth:
            return
        if self._table is None:
            return
        if duplicate_attributes:
            self._table.malformed = True
        if tag == "caption":
            if (
                self._caption
                or self._section is not None
                or self._row is not None
                or self._cell is not None
                or self._table.caption_seen
                or self._table.rows
                or self._column_groups_seen
            ):
                self._table.malformed = True
                return
            self._caption = True
            self._table.caption_seen = True
        elif tag == "colgroup":
            valid_attributes, has_span = _column_attributes(attrs)
            if (
                self._caption
                or self._colgroup
                or self._section is not None
                or self._row is not None
                or self._cell is not None
                or self._data_structure_started
                or not valid_attributes
            ):
                self._table.malformed = True
                return
            self._colgroup = True
            self._colgroup_has_span = has_span
            self._column_groups_seen = True
        elif tag == "col":
            valid_attributes, _ = _column_attributes(attrs)
            if not self._colgroup or self._colgroup_has_span or not valid_attributes:
                self._table.malformed = True
                return
        elif tag in {"thead", "tbody", "tfoot"}:
            if (
                self._caption
                or self._colgroup
                or self._section is not None
                or self._row is not None
                or self._cell is not None
            ):
                self._table.malformed = True
                return
            self._section = tag
            self._data_structure_started = True
        elif tag == "tr":
            if self._caption or self._colgroup or self._row is not None or self._cell is not None:
                self._table.malformed = True
                return
            self._row = _Row(section=self._section or "tbody")
            self._data_structure_started = True
        elif tag in {"th", "td"}:
            if self._caption or self._row is None or self._cell is not None:
                self._table.malformed = True
                return
            attributes = {name.casefold(): value for name, value in attrs}
            merged = attributes.get("rowspan") not in {None, "1"} or attributes.get("colspan") not in {None, "1"}
            self._cell = _Cell(kind=tag, merged=merged)
        elif self._caption or self._cell is not None:
            if tag not in _VOID_TAGS:
                self._inline_stack.append(tag)
        else:
            self._table.malformed = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag in {"script", "style"}:
            self._ignored_depth = max(0, self._ignored_depth - 1)
            return
        if self._ignored_depth:
            return
        if tag == "table" and self._nested_table_depth:
            self._nested_table_depth -= 1
            return
        if self._nested_table_depth:
            return
        if self._table is None:
            return
        if tag in {"th", "td"}:
            if self._cell is None or self._cell.kind != tag or self._row is None or self._inline_stack:
                self._table.malformed = True
                return
            self._row.cells.append(self._cell)
            self._cell = None
        elif tag == "tr":
            if self._row is None or self._cell is not None or self._caption:
                self._table.malformed = True
                return
            self._row.closed = True
            self._table.rows.append(self._row)
            self._row = None
        elif tag in {"thead", "tbody", "tfoot"}:
            if self._section != tag or self._row is not None or self._cell is not None or self._caption:
                self._table.malformed = True
                return
            self._section = None
        elif tag == "colgroup":
            if not self._colgroup or self._section is not None or self._row is not None or self._cell is not None:
                self._table.malformed = True
                return
            self._colgroup = False
            self._colgroup_has_span = False
        elif tag == "col":
            self._table.malformed = True
        elif tag == "caption":
            if (
                not self._caption
                or self._section is not None
                or self._row is not None
                or self._cell is not None
                or self._inline_stack
            ):
                self._table.malformed = True
                return
            self._caption = False
        elif tag == "table":
            if (
                self._caption
                or self._colgroup
                or self._section is not None
                or self._row is not None
                or self._cell is not None
                or self._inline_stack
            ):
                self._table.malformed = True
            self._table.closed = True
            self.tables.append(self._table)
            self._table = None
            self._row = None
            self._cell = None
            self._section = None
            self._caption = False
            self._inline_stack.clear()
            self._colgroup = False
            self._colgroup_has_span = False
            self._column_groups_seen = False
            self._data_structure_started = False
        else:
            if self._inline_stack and self._inline_stack[-1] == tag:
                self._inline_stack.pop()
            elif tag not in _VOID_TAGS or not (self._caption or self._cell is not None):
                self._table.malformed = True

    def handle_data(self, data: str) -> None:
        if self._ignored_depth or self._nested_table_depth or self._table is None:
            return
        if self._cell is not None:
            self._cell.parts.append(data)
        elif self._caption:
            self._table.caption_parts.append(data)
        elif data.strip():
            self._table.malformed = True

    def finish(self) -> None:
        self.close()
        if (
            self._table is not None
            or self._row is not None
            or self._cell is not None
            or self._caption
            or self._colgroup
            or self._section is not None
            or self._nested_table_depth
            or self._inline_stack
        ):
            raise HtmlStructureError("selected HTML structure is truncated")


def extract_html_table(
    path: str | Path,
    *,
    table_index: int,
    expected_caption: str | None,
    mapping: ColumnMapping | Mapping[str, object],
) -> ExtractedTable:
    """Extract one caller-selected table without fetching or guessing."""

    if isinstance(table_index, bool) or not isinstance(table_index, int) or table_index < 1:
        raise StructuredValidationError("table_index must be a positive one-based integer")
    if expected_caption is not None and (
        not isinstance(expected_caption, str) or not expected_caption or expected_caption != expected_caption.strip()
    ):
        raise StructuredValidationError("expected_caption must be a nonempty exact string")
    column_mapping = coerce_column_mapping(mapping)
    source = read_stable_local_file(path, suffixes=(".html", ".htm"))
    try:
        text = source.decode("utf-8-sig", errors="strict")
    except UnicodeError as error:
        raise StructuredValidationError("HTML input must be valid UTF-8") from error
    parser = _TableParser()
    try:
        parser.feed(text)
        parser.finish()
    except StructuredValidationError:
        raise
    except Exception as error:
        raise StructuredValidationError("HTML input could not be parsed") from error
    if table_index > len(parser.tables):
        raise StructuredValidationError("selected table does not exist")
    selected = parser.tables[table_index - 1]
    if not selected.closed or selected.malformed:
        raise HtmlStructureError("selected HTML table is malformed")
    if any(cell.merged for row in selected.rows for cell in row.cells):
        raise HtmlStructureError("selected HTML table contains spanning cells")
    if selected.caption != expected_caption:
        raise StructuredValidationError("selected table caption does not match")

    header_position = _header_position(selected)
    header_row = selected.rows[header_position]
    headers = [_exact_header(cell) for cell in header_row.cells]
    positions = resolve_headers(headers, column_mapping)
    data_rows = selected.rows[header_position + 1 :]
    extracted: list[ExtractedRow] = []
    body_index = 0
    for row in data_rows:
        body_index += 1
        location = f"table[{table_index}]/{row.section}/tr[{body_index}]"
        extracted.append(_extract_row(row, location, headers, positions, column_mapping))
    reject_duplicate_rows(extracted)
    validate_monotonicity(extracted, column_mapping)
    coverage, coverage_warnings = derive_coverage(extracted, column_mapping)
    table_warnings: list[str] = []
    if not extracted:
        table_warnings.append("empty-table")
    if any(any(status is not CellStatus.EXACT for status in row.cell_status.values()) for row in extracted):
        table_warnings.append("coverage-excludes-nonexact-rows")
    table_warnings.extend(coverage_warnings)
    return ExtractedTable(
        table_id=f"table[{table_index}]",
        caption=selected.caption,
        sheet=None,
        rows=tuple(extracted),
        coverage=coverage,
        warnings=tuple(table_warnings),
        extraction_method="html-table",
    )


def _header_position(table: _Table) -> int:
    for index, row in enumerate(table.rows):
        if any(cell.kind == "th" for cell in row.cells):
            if any(
                cell.raw_text.strip()
                for preceding in table.rows[:index]
                for cell in preceding.cells
            ):
                raise HtmlStructureError(
                    "selected table contains data before its explicit header"
                )
            return index
    raise MappingError("selected table has no explicit header row")


def _exact_header(cell: _Cell) -> str:
    if cell.merged:
        raise MappingError("merged headers are ambiguous")
    raw = cell.raw_text
    if not raw or raw != raw.strip():
        raise MappingError("headers must match exact non-whitespace text")
    return raw


def _extract_row(
    row: _Row,
    location: str,
    headers: list[str],
    positions: dict[str, int],
    mapping: ColumnMapping,
) -> ExtractedRow:
    warnings: list[str] = []
    if len(row.cells) < len(headers):
        warnings.append("truncated-row")
    values: dict[str, Any] = {}
    statuses: dict[str, CellStatus] = {}
    for canonical, position in positions.items():
        cell = row.cells[position] if position < len(row.cells) else None
        if cell is None:
            value, status = None, CellStatus.EMPTY
        elif cell.merged:
            raw = cell.raw_text.strip()
            value = _normalize_untyped(raw) if raw else None
            status = CellStatus.MERGED
        else:
            value, status = _normalize_cell(cell.raw_text, mapping.roles.get(canonical), mapping.score_scale)
        values[canonical] = value
        statuses[canonical] = status
        if status is CellStatus.EMPTY:
            warnings.append(f"empty-required-cell:{canonical}")
        elif status is CellStatus.MASKED:
            warnings.append(f"masked-cell:{canonical}")
        elif status is CellStatus.MERGED:
            warnings.append(f"merged-cell:{canonical}")
    nonexact = sum(status is not CellStatus.EXACT for status in statuses.values())
    confidence = max(0.0, 1.0 - (nonexact / max(1, len(statuses))) * 0.5)
    return ExtractedRow(values, statuses, location, confidence, tuple(warnings))


def _normalize_cell(
    raw: object,
    role: str | None,
    score_scale: tuple[int, int] | None,
) -> tuple[Any, CellStatus]:
    if not isinstance(raw, str):
        raise StructuredValidationError("HTML cell text has an invalid type")
    text = raw.strip()
    if not text:
        return None, CellStatus.EMPTY
    if role is not None and _MASKED.fullmatch(text):
        return None, CellStatus.MASKED
    if role is None:
        return _normalize_untyped(text), CellStatus.EXACT
    try:
        decimal = Decimal(text)
    except InvalidOperation as error:
        raise StructuredValidationError("declared numeric cell is invalid") from error
    if not decimal.is_finite():
        raise StructuredValidationError("declared numeric cell must be finite")
    if role == "rank" and decimal != decimal.to_integral_value():
        raise StructuredValidationError("rank cells must be mathematical integers")
    if role == "rank" and decimal < 1:
        raise StructuredValidationError("rank cells must be positive")
    value: int | float
    if decimal == decimal.to_integral_value():
        value = int(decimal)
    else:
        value = float(decimal)
    if role == "score" and score_scale is not None and not score_scale[0] <= value <= score_scale[1]:
        raise StructuredValidationError("score is outside the declared scale")
    return value, CellStatus.EXACT


def _normalize_untyped(text: str) -> str:
    return text


__all__ = ["HtmlStructureError", "extract_html_table"]
