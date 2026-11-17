"""Render structured report data into self-contained paged-report HTML."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

FAMILIES = {"proposal", "data-audit", "progress", "confirmation", "handoff"}
VARIANTS = {"blue", "green", "amber", "red"}
COMPONENTS = {
    "callout",
    "checklist",
    "divider",
    "grid",
    "kpi",
    "progress",
    "status_row",
    "table",
    "compare_table",
    "tag",
}
_MISSING = object()


class ReportValidationError(ValueError):
    """Raised when report input does not satisfy the renderer contract."""


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ReportValidationError(f"{field} must be an object")
    return value


def _reject_unknown(value: Mapping[str, Any], allowed: set[str], field: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ReportValidationError(f"{field} contains unknown field(s): {', '.join(unknown)}")


def _list(value: Any, field: str) -> list[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ReportValidationError(f"{field} must be an array")
    return list(value)


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportValidationError(f"{field} must be a non-empty string")
    return value


def _optional_text(value: Any, field: str, default: str = "") -> str:
    if value is _MISSING:
        return default
    if not isinstance(value, str):
        raise ReportValidationError(f"{field} must be a string")
    return value


def _display_text(value: Any, field: str) -> str:
    if isinstance(value, bool) or value is None or not isinstance(value, (str, int, float)):
        raise ReportValidationError(f"{field} must be a string or number")
    return str(value)


def _variant(value: Any, field: str, default: str = "blue") -> str:
    variant = default if value is _MISSING else value
    if not isinstance(variant, str):
        raise ReportValidationError(f"{field} must be a string")
    if variant not in VARIANTS:
        raise ReportValidationError(
            f"{field} must be one of {', '.join(sorted(VARIANTS))}"
        )
    return variant


def _slug(value: str, fallback: str) -> str:
    slug = re.sub(r"[^\w-]+", "-", value.strip(), flags=re.UNICODE).strip("-")
    return slug or fallback


def _percentage(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReportValidationError(f"{field} must be a number from 0 to 100")
    if not 0 <= value <= 100:
        raise ReportValidationError(f"{field} must be a number from 0 to 100")
    return float(value)


def _boolean(value: Any, field: str, default: bool = False) -> bool:
    if value is _MISSING:
        return default
    if not isinstance(value, bool):
        raise ReportValidationError(f"{field} must be a boolean")
    return value


def _normalize(data: Mapping[str, Any]) -> dict[str, Any]:
    data = _mapping(data, "report")
    _reject_unknown(data, {"family", "toc", "meta", "pages"}, "report")
    family = _required_text(data.get("family", _MISSING), "family")
    if family not in FAMILIES:
        raise ReportValidationError(
            f"family must be one of {', '.join(sorted(FAMILIES))}"
        )

    meta = _mapping(data.get("meta"), "meta")
    _reject_unknown(
        meta,
        {"language", "title", "client", "category", "subtitle", "date", "version", "project", "footer"},
        "meta",
    )
    title = _required_text(meta.get("title", _MISSING), "meta.title")
    language = _optional_text(meta.get("language", _MISSING), "meta.language", "zh-CN")
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", language):
        raise ReportValidationError("meta.language must be a valid language tag")

    pages = _list(data.get("pages"), "pages")
    if not pages:
        raise ReportValidationError("pages must contain at least one content page")

    normalized_pages: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    for page_index, page_value in enumerate(pages, start=1):
        page = _mapping(page_value, f"pages[{page_index - 1}]")
        _reject_unknown(page, {"label", "sections"}, f"pages[{page_index - 1}]")
        sections = _list(page.get("sections", _MISSING), f"pages[{page_index - 1}].sections")
        if not sections:
            raise ReportValidationError(
                f"pages[{page_index - 1}].sections must contain at least one section"
            )
        normalized_sections: list[dict[str, Any]] = []
        for section_index, section_value in enumerate(sections, start=1):
            section = _mapping(
                section_value,
                f"pages[{page_index - 1}].sections[{section_index - 1}]",
            )
            _reject_unknown(
                section,
                {"id", "title", "components"},
                f"pages[{page_index - 1}].sections[{section_index - 1}]",
            )
            section_title = _required_text(
                section.get("title", _MISSING),
                f"pages[{page_index - 1}].sections[{section_index - 1}].title",
            )
            components = _list(
                section.get("components", []),
                f"pages[{page_index - 1}].sections[{section_index - 1}].components",
            )
            normalized_components = []
            for component_index, component_value in enumerate(components, start=1):
                normalized_components.append(
                    _validate_component(
                        component_value,
                        f"pages[{page_index - 1}].sections[{section_index - 1}].components[{component_index - 1}]",
                    )
                )
            raw_id = _optional_text(section.get("id", _MISSING), "section.id", section_title)
            section_id = _slug(raw_id, f"section-{page_index}-{section_index}")
            if section_id in used_ids:
                raise ReportValidationError(f"duplicate section id: {section_id}")
            used_ids.add(section_id)
            normalized_sections.append(
                {"id": section_id, "title": section_title, "components": normalized_components}
            )
        normalized_pages.append(
            {
                "label": _optional_text(page.get("label", _MISSING), "page.label"),
                "sections": normalized_sections,
            }
        )

    normalized_meta = {
        "language": language,
        "title": title,
        "client": _optional_text(meta.get("client", _MISSING), "meta.client"),
        "category": _optional_text(meta.get("category", _MISSING), "meta.category"),
        "subtitle": _optional_text(meta.get("subtitle", _MISSING), "meta.subtitle"),
        "date": _optional_text(meta.get("date", _MISSING), "meta.date"),
        "version": _optional_text(meta.get("version", _MISSING), "meta.version"),
        "project": _optional_text(meta.get("project", _MISSING), "meta.project"),
        "footer": _optional_text(meta.get("footer", _MISSING), "meta.footer"),
    }
    if not normalized_meta["footer"]:
        footer_parts = [
            part
            for part in (
                normalized_meta["client"],
                normalized_meta["category"],
                normalized_meta["date"],
            )
            if part
        ]
        normalized_meta["footer"] = " · ".join(footer_parts)

    return {
        "family": family,
        "meta": normalized_meta,
        "toc": _boolean(data.get("toc", _MISSING), "toc", len(used_ids) >= 3),
        "pages": normalized_pages,
    }


def _validate_table_cell(value: Any, field: str) -> Any:
    if not isinstance(value, Mapping):
        return _display_text(value, field)

    _reject_unknown(value, {"text", "tag", "class"}, field)
    cell_class = _optional_text(value.get("class", _MISSING), f"{field}.class")
    if "tag" in value:
        if "text" in value:
            raise ReportValidationError(f"{field} cannot contain both text and tag")
        tag = _mapping(value["tag"], f"{field}.tag")
        _reject_unknown(tag, {"text", "variant"}, f"{field}.tag")
        normalized: dict[str, Any] = {
            "tag": {
                "text": _required_text(tag.get("text", _MISSING), f"{field}.tag.text"),
                "variant": _variant(tag.get("variant", _MISSING), f"{field}.tag.variant"),
            }
        }
    else:
        normalized = {
            "text": _display_text(value.get("text", _MISSING), f"{field}.text")
        }
    if "class" in value:
        normalized["class"] = cell_class
    return normalized


def _validate_component(value: Any, field: str) -> dict[str, Any]:
    component = dict(_mapping(value, field))
    kind = _required_text(component.get("type"), f"{field}.type")
    if kind not in COMPONENTS:
        raise ReportValidationError(
            f"{field}.type must be one of {', '.join(sorted(COMPONENTS))}"
        )
    allowed_fields = {
        "table": {"type", "columns", "rows"},
        "compare_table": {"type", "columns", "rows"},
        "callout": {"type", "variant", "label", "text"},
        "tag": {"type", "variant", "text"},
        "kpi": {"type", "value", "unit"},
        "progress": {"type", "variant", "value"},
        "status_row": {"type", "variant", "label", "status"},
        "checklist": {"type", "items"},
        "grid": {"type", "columns", "cards"},
        "divider": {"type"},
    }
    _reject_unknown(component, allowed_fields[kind], field)

    if kind in {"table", "compare_table"}:
        columns = _list(component.get("columns", _MISSING), f"{field}.columns")
        columns = [
            _display_text(column, f"{field}.columns[{index}]")
            for index, column in enumerate(columns)
        ]
        rows = _list(component.get("rows", _MISSING), f"{field}.rows")
        if not columns:
            raise ReportValidationError(f"{field}.columns must not be empty")
        normalized_rows = []
        for row_index, row_value in enumerate(rows):
            row = _list(row_value, f"{field}.rows[{row_index}]")
            if len(row) != len(columns):
                raise ReportValidationError(
                    f"{field}.rows[{row_index}] must have {len(columns)} cells"
                )
            normalized_rows.append(
                [
                    _validate_table_cell(
                        cell,
                        f"{field}.rows[{row_index}][{cell_index}]",
                    )
                    for cell_index, cell in enumerate(row)
                ]
            )
        component["columns"] = columns
        component["rows"] = normalized_rows
    elif kind == "callout":
        component["text"] = _required_text(component.get("text", _MISSING), f"{field}.text")
        component["label"] = _optional_text(component.get("label", _MISSING), f"{field}.label")
        component["variant"] = _variant(component.get("variant", _MISSING), f"{field}.variant")
    elif kind == "tag":
        component["text"] = _required_text(component.get("text", _MISSING), f"{field}.text")
        component["variant"] = _variant(component.get("variant", _MISSING), f"{field}.variant")
    elif kind == "kpi":
        component["value"] = _display_text(component.get("value", _MISSING), f"{field}.value")
        component["unit"] = _optional_text(component.get("unit", _MISSING), f"{field}.unit")
    elif kind == "progress":
        component["value"] = _percentage(component.get("value", _MISSING), f"{field}.value")
        component["variant"] = _variant(component.get("variant", _MISSING), f"{field}.variant")
    elif kind == "status_row":
        component["label"] = _required_text(component.get("label", _MISSING), f"{field}.label")
        component["status"] = _required_text(component.get("status", _MISSING), f"{field}.status")
        component["variant"] = _variant(component.get("variant", _MISSING), f"{field}.variant")
    elif kind == "checklist":
        items = _list(component.get("items"), f"{field}.items")
        normalized_items = []
        for item_index, item_value in enumerate(items):
            item = _mapping(item_value, f"{field}.items[{item_index}]")
            _reject_unknown(item, {"text", "done"}, f"{field}.items[{item_index}]")
            normalized_items.append(
                {
                    "text": _required_text(item.get("text", _MISSING), f"{field}.items[{item_index}].text"),
                    "done": _boolean(item.get("done", _MISSING), f"{field}.items[{item_index}].done"),
                }
            )
        component["items"] = normalized_items
    elif kind == "grid":
        columns = component.get("columns", 3)
        if isinstance(columns, bool) or not isinstance(columns, int) or columns not in (2, 3):
            raise ReportValidationError(f"{field}.columns must be 2 or 3")
        cards = _list(component.get("cards"), f"{field}.cards")
        normalized_cards = []
        for card_index, card_value in enumerate(cards):
            card = _mapping(card_value, f"{field}.cards[{card_index}]")
            _reject_unknown(card, {"title", "body"}, f"{field}.cards[{card_index}]")
            normalized_cards.append(
                {
                    "title": _required_text(card.get("title", _MISSING), f"{field}.cards[{card_index}].title"),
                    "body": _optional_text(card.get("body", _MISSING), f"{field}.cards[{card_index}].body"),
                }
            )
        component["columns"] = columns
        component["cards"] = normalized_cards
    return component


def _render_cell(cell: Any, table_kind: str, column_index: int) -> str:
    if isinstance(cell, Mapping):
        if "tag" in cell:
            tag = _mapping(cell["tag"], "table cell.tag")
            text = _required_text(tag.get("text"), "table cell.tag.text")
            variant = _variant(tag.get("variant", _MISSING), "table cell.tag.variant")
            content = f'<span class="tag {variant}">{_escape(text)}</span>'
        else:
            text = _display_text(cell.get("text", ""), "table cell.text")
            content = _escape(text)
        cell_class = _optional_text(cell.get("class", _MISSING), "table cell.class")
    else:
        content = _escape(_display_text(cell, "table cell"))
        cell_class = ""
    if table_kind == "compare_table" and not cell_class:
        if column_index == 1:
            cell_class = "old"
        elif column_index == 2:
            cell_class = "new"
    class_attr = f' class="{_escape(cell_class)}"' if cell_class else ""
    return f"<td{class_attr}>{content}</td>"


def _render_table(component: Mapping[str, Any], kind: str) -> str:
    columns = component["columns"]
    rows = component["rows"]
    class_attr = ' class="compare-table"' if kind == "compare_table" else ""
    parts = [f"<table{class_attr}><thead><tr>"]
    parts.extend(f'<th scope="col">{_escape(column)}</th>' for column in columns)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        parts.extend(
            _render_cell(cell, kind, index) for index, cell in enumerate(row)
        )
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def _render_component(component: Mapping[str, Any]) -> str:
    kind = component["type"]
    if kind in {"table", "compare_table"}:
        return _render_table(component, kind)
    if kind == "callout":
        label = component.get("label")
        label_html = f"<strong>{_escape(label)}：</strong>" if label else ""
        return f'<div class="callout {component["variant"]}">{label_html}{_escape(component["text"])}</div>'
    if kind == "tag":
        return f'<span class="tag {component["variant"]}">{_escape(component["text"])}</span>'
    if kind == "kpi":
        unit = f' <span class="unit">{_escape(component["unit"])}</span>' if component["unit"] else ""
        return f'<div class="kpi">{_escape(component["value"])}{unit}</div>'
    if kind == "progress":
        value = component["value"]
        display = f"{value:g}"
        return f'<div class="progress-bar {component["variant"]}" role="progressbar" aria-label="{display}%" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{display}"><div class="fill" style="width:{display}%"></div></div>'
    if kind == "status_row":
        return (
            '<div class="status-row">'
            f'<span class="label">{_escape(component["label"])}</span>'
            f'<span class="value"><span class="tag {component["variant"]}">{_escape(component["status"])}</span></span>'
            "</div>"
        )
    if kind == "checklist":
        items = []
        for item in component["items"]:
            state = "true" if item["done"] else "false"
            class_attr = ' class="done"' if item["done"] else ""
            items.append(
                f'<li role="checkbox" aria-checked="{state}"{class_attr}>{_escape(item["text"])}</li>'
            )
        return f'<ul class="checklist">{"".join(items)}</ul>'
    if kind == "grid":
        grid_class = "grid two" if component["columns"] == 2 else "grid"
        cards = []
        for card in component["cards"]:
            body = f'<p>{_escape(card["body"])}</p>' if card["body"] else ""
            cards.append(f'<div class="card"><h3>{_escape(card["title"])}</h3>{body}</div>')
        return f'<div class="{grid_class}">{"".join(cards)}</div>'
    if kind == "divider":
        return "<hr>"
    raise ReportValidationError(f"unsupported component type: {kind}")


def _default_css_path() -> Path:
    return Path(__file__).resolve().parents[1] / "templates" / "base.css"


def _decode_css_escapes(css: str) -> str:
    """Decode CSS token escapes enough to inspect protected at-rules/functions.

    CSS allows identifiers such as ``u\\72l`` and ``@im\\70ort``. A literal
    substring scan would miss those spellings even though a browser parses
    them as ``url`` and ``@import``. This small tokenizer is intentionally
    limited to escape decoding; it does not attempt to be a full CSS parser.
    """
    output: list[str] = []
    index = 0
    hex_digits = "0123456789abcdefABCDEF"
    while index < len(css):
        char = css[index]
        if char != "\\":
            output.append(char)
            index += 1
            continue

        index += 1
        if index >= len(css):
            break
        if css[index] in "\r\n\f":
            if css[index] == "\r" and index + 1 < len(css) and css[index + 1] == "\n":
                index += 2
            else:
                index += 1
            continue

        start = index
        while index < len(css) and index - start < 6 and css[index] in hex_digits:
            index += 1
        if index > start:
            codepoint = int(css[start:index], 16)
            if index < len(css) and css[index] in " \t\r\n\f":
                if css[index] == "\r" and index + 1 < len(css) and css[index + 1] == "\n":
                    index += 2
                else:
                    index += 1
            if codepoint == 0 or codepoint > 0x10FFFF or 0xD800 <= codepoint <= 0xDFFF:
                output.append("\ufffd")
            else:
                output.append(chr(codepoint))
            continue

        output.append(css[index])
        index += 1
    return "".join(output)


def _safe_css(css: Any) -> str:
    if not isinstance(css, str):
        raise ReportValidationError("css must be a string")
    if re.search(r"</style\b", css, flags=re.IGNORECASE):
        raise ReportValidationError("css must not contain an HTML style-element terminator")
    normalized_css = _decode_css_escapes(css)
    # Comments can be placed between identifier characters, so remove them
    # before scanning (for example ``u/**/rl(...)`` and ``@im/**/port``).
    normalized_css = re.sub(r"/\*.*?\*/", "", normalized_css, flags=re.DOTALL)
    if re.search(r"@import\b", normalized_css, flags=re.IGNORECASE):
        raise ReportValidationError("css must not contain @import rules")
    if re.search(r"\burl\s*\(", normalized_css, flags=re.IGNORECASE):
        raise ReportValidationError("css must not contain url() references")
    return css


def render_report(data: Mapping[str, Any], css: str | None = None) -> str:
    """Render a validated report mapping into one self-contained HTML document."""
    report = _normalize(data)
    meta = report["meta"]
    sections = [section for page in report["pages"] for section in page["sections"]]
    if css is None:
        css = _default_css_path().read_text(encoding="utf-8")
    css = _safe_css(css)

    eyebrow = " · ".join(part for part in (meta["client"], meta["category"]) if part)
    meta_values = [
        value
        for value in (meta["date"], meta["version"], meta["project"])
        if value
    ]
    parts = [
        "<!DOCTYPE html>",
        f'<html lang="{_escape(meta["language"])}">',
        "<head>",
        '<meta charset="UTF-8">',
        f'<title>{_escape(meta["title"])}</title>',
        "<style>",
        css,
        "</style>",
        "</head>",
        "<body>",
        f'<div class="page" data-family="{report["family"]}">',
        '<div class="report-page cover">',
        '<div class="hero">',
        f'<p class="eyebrow">{_escape(eyebrow)}</p>',
        f'<h1>{_escape(meta["title"])}</h1>',
    ]
    if meta["subtitle"]:
        parts.append(f'<p class="subtitle">{_escape(meta["subtitle"])}</p>')
    if meta_values:
        parts.append('<div class="meta">')
        parts.extend(f"<span>{_escape(value)}</span>" for value in meta_values)
        parts.append("</div>")
    parts.append("</div>")

    if report["toc"] and sections:
        toc_heading = "Contents" if meta["language"].lower().startswith("en") else "目录"
        parts.extend([f'<nav class="toc"><h2>{toc_heading}</h2><ol>'])
        parts.extend(
            f'<li><a href="#{_escape(section["id"])}">{_escape(section["title"])}</a></li>'
            for section in sections
        )
        parts.extend(["</ol></nav>", "</div>"])
    else:
        parts.append("</div>")

    for page in report["pages"]:
        parts.extend(['<div class="report-page flex-col">', '<div class="content-area">'])
        if page["label"]:
            parts.append(f'<p class="page-label">{_escape(page["label"])}</p>')
        for section in page["sections"]:
            parts.append(f'<section id="{_escape(section["id"])}">')
            parts.append(f'<h2>{_escape(section["title"])}</h2>')
            parts.extend(_render_component(component) for component in section["components"])
            parts.append("</section>")
        parts.extend(
            [
                "</div>",
                '<div class="footer-area">',
                f'<div class="footer"><p>{_escape(meta["footer"])}</p></div>',
                "</div>",
                "</div>",
            ]
        )
    parts.extend(["</div>", "</body>", "</html>"])
    return "".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON report data")
    parser.add_argument("-o", "--output", required=True, type=Path, help="HTML output path")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        rendered = render_report(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ReportValidationError) as exc:
        print(f"paged-report: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
