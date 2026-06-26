#!/usr/bin/env python3
"""
transform_doc_to_code.py

Turn canonical parsed document JSON into code-oriented artifacts.

Supported targets:
- react
- html-css
- json-schema
- jupyter-notebook

Outputs:
- component_map.json
- field_schema.json
- ui_blueprint.json
- traceability.json
- notes.md
- app.jsx            (for react)
- index.html         (for html-css)
- styles.css         (for html-css)
- schema.json        (for json-schema)
- notebook.ipynb     (for jupyter-notebook)
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from utils import (
    count_block_types,
    detect_title,
    ensure_dir,
    iter_blocks,
    load_json,
    make_source_ref,
    short_text,
    slugify,
    validate_document_schema,
    write_error,
    write_json,
    write_text,
)


@dataclass
class Config:
    parsed_json: Path
    out: Path
    target: str
    title: str | None
    debug: bool = False


COMMON_FIELD_KEYWORDS = {
    "name": "text",
    "full name": "text",
    "first name": "text",
    "last name": "text",
    "email": "email",
    "e-mail": "email",
    "phone": "tel",
    "mobile": "tel",
    "telephone": "tel",
    "company": "text",
    "organization": "text",
    "address": "text",
    "city": "text",
    "state": "text",
    "zip": "text",
    "postal code": "text",
    "country": "text",
    "date": "date",
    "start date": "date",
    "end date": "date",
    "birthday": "date",
    "dob": "date",
    "amount": "number",
    "price": "number",
    "quantity": "number",
    "qty": "number",
    "budget": "number",
    "password": "password",
    "search": "search",
    "comment": "text",
    "comments": "text",
    "message": "text",
    "description": "text",
}

TEXTAREA_HINTS = {
    "comment",
    "comments",
    "message",
    "description",
    "notes",
    "summary",
    "details",
    "reason",
}

SELECT_HINTS = {
    "country",
    "state",
    "status",
    "category",
    "type",
    "department",
    "team",
}


def parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="Generate code-oriented artifacts from parsed document JSON."
    )
    parser.add_argument("--parsed-json", required=True, help="Path to parsed.json")
    parser.add_argument("--out", required=True, help="Output task directory")
    parser.add_argument(
        "--target",
        default="react",
        choices=["react", "html-css", "json-schema", "jupyter-notebook"],
        help="Output target format",
    )
    parser.add_argument("--title", help="Optional app/page title override")
    parser.add_argument("--debug", action="store_true")
    ns = parser.parse_args()

    return Config(
        parsed_json=Path(ns.parsed_json).expanduser().resolve(),
        out=Path(ns.out).expanduser().resolve(),
        target=ns.target,
        title=ns.title,
        debug=ns.debug,
    )


def infer_field_type(label: str) -> str:
    normalized = label.strip().lower()
    if normalized in COMMON_FIELD_KEYWORDS:
        return COMMON_FIELD_KEYWORDS[normalized]

    for key, field_type in COMMON_FIELD_KEYWORDS.items():
        if key in normalized:
            return field_type

    return "text"


def infer_field_control(label: str, field_type: str, placeholder: str) -> str:
    normalized = label.strip().lower()
    if any(hint in normalized for hint in TEXTAREA_HINTS):
        return "textarea"
    if any(hint == normalized or hint in normalized for hint in SELECT_HINTS):
        return "select"
    if placeholder and len(placeholder) > 48:
        return "textarea"
    return "input"


def infer_field_width(label: str, control: str, placeholder: str) -> str:
    normalized = label.strip().lower()
    if control == "textarea":
        return "full"
    if len(label) > 22 or len(placeholder) > 28:
        return "full"
    if any(token in normalized for token in ["address", "description", "comment", "message"]):
        return "full"
    return "half"


def default_placeholder_for_label(label: str, field_type: str) -> str:
    label_text = label.strip()
    if field_type == "email":
        return "name@example.com"
    if field_type == "tel":
        return "+86 138 0000 0000"
    if field_type == "date":
        return "YYYY-MM-DD"
    if field_type == "number":
        return "0"
    if field_type == "password":
        return "Enter password"
    if label_text:
        return f"Enter {label_text.lower()}"
    return ""


def parse_field_candidate_from_text(text: str) -> tuple[str, str] | None:
    clean = text.strip()
    if not clean:
        return None

    if clean.endswith(":") and len(clean) <= 80:
        label = clean[:-1].strip()
        if label:
            return label, ""

    match = re.match(r"^\s*([A-Za-z][A-Za-z0-9 /&()_-]{1,80}?)\s*:\s*(.+?)\s*$", clean)
    if match:
        label = match.group(1).strip()
        value = match.group(2).strip()
        return label, value

    return None


def split_list_items(text: str) -> list[str]:
    lines = [line.strip("鈥?- \t") for line in text.splitlines()]
    return [line for line in lines if line]


def strip_html_tags(text: str) -> str:
    no_tags = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html_lib.unescape(no_tags).split())


def extract_table_from_html(text: str) -> dict[str, Any] | None:
    if "<table" not in text.lower():
        return None

    rows_html = re.findall(r"<tr[^>]*>(.*?)</tr>", text, flags=re.IGNORECASE | re.DOTALL)
    if not rows_html:
        return None

    rows: list[list[str]] = []
    for row_html in rows_html:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, flags=re.IGNORECASE | re.DOTALL)
        clean_cells = [strip_html_tags(cell) for cell in cells]
        if any(clean_cells):
            rows.append(clean_cells)

    if not rows:
        return None

    headers = rows[0]
    body = rows[1:] if len(rows) > 1 else []
    return {
        "headers": headers,
        "rows": body,
    }


def extract_image_from_html(text: str) -> dict[str, str] | None:
    if "<img" not in text.lower():
        return None

    src_match = re.search(r'src="([^"]+)"', text, flags=re.IGNORECASE)
    alt_match = re.search(r'alt="([^"]*)"', text, flags=re.IGNORECASE)
    return {
        "src": src_match.group(1) if src_match else "",
        "alt": alt_match.group(1) if alt_match else "Image",
    }


def summarize_text_blocks(document: dict[str, Any], limit: int = 4) -> list[str]:
    snippets: list[str] = []
    for row in iter_blocks(document):
        block = row["block"]
        if block.get("type") not in {"text", "paragraph", "heading", "list"}:
            continue
        raw_text = (block.get("text") or "").strip()
        text = short_text(strip_html_tags(raw_text) or raw_text, 120)
        if text and text not in snippets:
            snippets.append(text)
        if len(snippets) >= limit:
            break
    return snippets


def classify_section(section: dict[str, Any]) -> str:
    kind_counts: dict[str, int] = {}
    for item in section.get("items", []):
        kind = item.get("kind", "unknown")
        kind_counts[kind] = kind_counts.get(kind, 0) + 1

    if kind_counts.get("field", 0) >= max(2, len(section.get("items", [])) // 2):
        return "form"
    if kind_counts.get("table", 0) > 0:
        return "data"
    if kind_counts.get("text", 0) + kind_counts.get("list", 0) >= 2:
        return "content"
    if kind_counts.get("figure", 0) + kind_counts.get("chart", 0) > 0:
        return "visual"
    return "mixed"


def build_section_summary(section: dict[str, Any]) -> dict[str, Any]:
    field_items = [item for item in section["items"] if item["kind"] == "field"]
    table_items = [item for item in section["items"] if item["kind"] == "table"]
    text_items = [item for item in section["items"] if item["kind"] == "text"]
    return {
        "id": section["id"],
        "title": section["title"],
        "kind": classify_section(section),
        "item_count": len(section["items"]),
        "field_count": len(field_items),
        "table_count": len(table_items),
        "text_count": len(text_items),
    }


def count_generated_item_kinds(sections: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for section in sections:
        for item in section.get("items", []):
            kind = item.get("kind", "unknown")
            counts[kind] = counts.get(kind, 0) + 1
    return counts


def build_overview_cards(
    title: str,
    sections: list[dict[str, Any]],
    field_schema: list[dict[str, Any]],
    document: dict[str, Any],
) -> list[dict[str, str]]:
    block_counts = count_block_types(document)
    generated_counts = count_generated_item_kinds(sections)
    cards = [
        {"label": "Sections", "value": str(len(sections))},
        {"label": "Fields", "value": str(len(field_schema))},
        {
            "label": "Tables",
            "value": str(max(len(document.get("tables", [])), generated_counts.get("table", 0))),
        },
    ]
    visual_count = max(
        block_counts.get("figure", 0) + block_counts.get("chart", 0),
        generated_counts.get("figure", 0) + generated_counts.get("chart", 0),
    )
    if visual_count:
        cards.append(
            {
                "label": "Visual Blocks",
                "value": str(visual_count),
            }
        )
    if title:
        cards.append({"label": "Source Title", "value": short_text(title, 24)})
    return cards


def infer_document_profile(
    title: str,
    document: dict[str, Any],
    sections: list[dict[str, Any]],
    field_schema: list[dict[str, Any]],
) -> dict[str, Any]:
    block_counts = count_block_types(document)
    generated_counts = count_generated_item_kinds(sections)
    table_count = max(len(document.get("tables", [])), generated_counts.get("table", 0))
    heading_count = block_counts.get("heading", 0)
    field_count = len(field_schema)
    text_count = block_counts.get("text", 0) + block_counts.get("paragraph", 0)
    figure_count = max(
        block_counts.get("figure", 0) + block_counts.get("chart", 0),
        generated_counts.get("figure", 0) + generated_counts.get("chart", 0),
    )

    doc_kind = "mixed-app"
    if field_count >= 2 and field_count >= table_count * 2:
        doc_kind = "form-app"
    elif table_count >= 1 and field_count <= 3:
        doc_kind = "data-workspace"
    elif figure_count > 0 or table_count > 1:
        doc_kind = "dashboard"
    elif heading_count >= 2 and text_count >= 4:
        doc_kind = "content-page"

    actions: list[str]
    if doc_kind == "form-app":
        actions = ["Save Draft", "Submit"]
    elif doc_kind in {"data-workspace", "dashboard"}:
        actions = ["Refresh", "Export"]
    else:
        actions = ["Share", "Review"]

    return {
        "document_kind": doc_kind,
        "page_title": title,
        "section_summaries": [build_section_summary(section) for section in sections],
        "overview_cards": build_overview_cards(title, sections, field_schema, document),
        "source_snippets": summarize_text_blocks(document),
        "actions": actions,
        "counts": {
            "pages": len(document.get("pages", [])),
            "sections": len(sections),
            "fields": field_count,
            "tables": table_count,
            "figures": figure_count,
        },
    }


def infer_sections(
    document: dict[str, Any], title: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    sections: list[dict[str, Any]] = []
    component_map: list[dict[str, Any]] = []
    field_schema: list[dict[str, Any]] = []
    assumptions: list[str] = []

    def new_section(
        section_title: str,
        page_id: str | None,
        block_id: str | None,
    ) -> dict[str, Any]:
        section_id = f"section_{slugify(section_title, default='untitled')}_{len(sections) + 1}"
        trace = [make_source_ref(page_id, block_id)]
        section = {
            "id": section_id,
            "title": section_title,
            "items": [],
            "source_refs": trace,
        }
        sections.append(section)
        component_map.append(
            {
                "generated_unit_id": section_id,
                "kind": "section",
                "label": section_title,
                "props": {},
                "source_refs": trace,
                "assumption": None,
            }
        )
        return section

    current_section: dict[str, Any] | None = None

    def ensure_current_section(page_id: str | None, block_id: str | None) -> dict[str, Any]:
        nonlocal current_section
        if current_section is None:
            current_section = new_section(title, page_id, block_id)
        return current_section

    tables_by_page: dict[str, list[dict[str, Any]]] = {}
    for table in document.get("tables", []):
        page_id = table.get("page_id")
        tables_by_page.setdefault(page_id, []).append(table)

    inserted_table_pages: set[str] = set()

    def append_page_tables(page_id: str, target_section: dict[str, Any]) -> None:
        if page_id in inserted_table_pages:
            return
        page_tables = tables_by_page.get(page_id, [])
        if not page_tables:
            return

        for table in page_tables:
            table_id = table.get("table_id")
            item = {
                "kind": "table",
                "id": f"table_{slugify(str(table_id), 'table')}",
                "title": table.get("caption") or f"Table {table_id}",
                "headers": table.get("headers", []),
                "rows": table.get("rows", []),
                "source_refs": [
                    make_source_ref(page_id, bid) for bid in table.get("source_block_ids", [])
                ],
            }
            target_section["items"].append(item)
            component_map.append(
                {
                    "generated_unit_id": item["id"],
                    "kind": "table",
                    "label": item["title"],
                    "props": {
                        "column_count": len(item["headers"]),
                        "row_count": len(item["rows"]),
                    },
                    "source_refs": item["source_refs"],
                    "assumption": None,
                }
            )
        inserted_table_pages.add(page_id)

    for row in iter_blocks(document):
        page_id = row["page_id"]
        block = row["block"]
        block_id = block.get("block_id")
        block_type = block.get("type") or "unknown"
        text = (block.get("text") or "").strip()
        source_refs = [make_source_ref(page_id, block_id)]

        if block_type == "heading":
            current_section = new_section(text or "Untitled Section", page_id, block_id)
            append_page_tables(page_id, current_section)
            continue

        current_section = ensure_current_section(page_id, block_id)
        append_page_tables(page_id, current_section)

        if not text and block_type not in {"figure", "chart", "formula"}:
            continue

        embedded_table = extract_table_from_html(text) if text else None
        if embedded_table:
            table_id = f"embedded_table_{len(component_map) + 1}"
            current_section["items"].append(
                {
                    "kind": "table",
                    "id": table_id,
                    "title": f"Embedded Table {len([i for i in current_section['items'] if i.get('kind') == 'table']) + 1}",
                    "headers": embedded_table["headers"],
                    "rows": embedded_table["rows"],
                    "source_refs": source_refs,
                }
            )
            component_map.append(
                {
                    "generated_unit_id": table_id,
                    "kind": "table",
                    "label": "Embedded HTML table",
                    "props": {
                        "column_count": len(embedded_table["headers"]),
                        "row_count": len(embedded_table["rows"]),
                    },
                    "source_refs": source_refs,
                    "assumption": "Table was reconstructed from embedded HTML content in the parsed document.",
                }
            )
            assumptions.append("Embedded HTML tables were reconstructed into structured table components.")
            continue

        embedded_image = extract_image_from_html(text) if text else None
        if embedded_image:
            item_id = f"figure_{slugify(block_id or embedded_image['alt'] or 'image')}"
            current_section["items"].append(
                {
                    "kind": "figure",
                    "id": item_id,
                    "text": embedded_image["alt"] or "Image",
                    "asset_path": embedded_image["src"],
                    "source_refs": source_refs,
                }
            )
            component_map.append(
                {
                    "generated_unit_id": item_id,
                    "kind": "figure",
                    "label": embedded_image["alt"] or "Image",
                    "props": {"asset_path": embedded_image["src"]},
                    "source_refs": source_refs,
                    "assumption": "Figure placeholder was reconstructed from embedded HTML image markup.",
                }
            )
            assumptions.append("Embedded HTML image blocks are represented as figure placeholders in generated code.")
            continue

        if block_type == "kv_pair":
            pair = parse_field_candidate_from_text(text)
            label, value = pair if pair else (text, "")
            field_id = f"field_{slugify(label)}_{len(field_schema) + 1}"
            field_type = infer_field_type(label)
            control = infer_field_control(label, field_type, value)
            placeholder = value or default_placeholder_for_label(label, field_type)

            item = {
                "kind": "field",
                "id": field_id,
                "label": label,
                "placeholder": placeholder,
                "field_type": field_type,
                "control": control,
                "width": infer_field_width(label, control, placeholder),
                "source_refs": source_refs,
            }
            current_section["items"].append(item)
            field_schema.append(
                {
                    "id": field_id,
                    "name": slugify(label),
                    "label": label,
                    "type": field_type,
                    "control": control,
                    "width": item["width"],
                    "required": False,
                    "placeholder": placeholder,
                    "section": current_section["title"],
                    "source_refs": source_refs,
                }
            )
            component_map.append(
                {
                    "generated_unit_id": field_id,
                    "kind": "field",
                    "label": label,
                    "props": {
                        "type": field_type,
                        "control": control,
                        "placeholder": placeholder,
                    },
                    "source_refs": source_refs,
                    "assumption": "Required/validation rules were not explicit in the source.",
                }
            )
            continue

        field_candidate = parse_field_candidate_from_text(text)
        if field_candidate and len(text) <= 120:
            label, value = field_candidate
            field_id = f"field_{slugify(label)}_{len(field_schema) + 1}"
            field_type = infer_field_type(label)
            control = infer_field_control(label, field_type, value)
            placeholder = value or default_placeholder_for_label(label, field_type)

            item = {
                "kind": "field",
                "id": field_id,
                "label": label,
                "placeholder": placeholder,
                "field_type": field_type,
                "control": control,
                "width": infer_field_width(label, control, placeholder),
                "source_refs": source_refs,
            }
            current_section["items"].append(item)
            field_schema.append(
                {
                    "id": field_id,
                    "name": slugify(label),
                    "label": label,
                    "type": field_type,
                    "control": control,
                    "width": item["width"],
                    "required": False,
                    "placeholder": placeholder,
                    "section": current_section["title"],
                    "source_refs": source_refs,
                }
            )
            component_map.append(
                {
                    "generated_unit_id": field_id,
                    "kind": "field",
                    "label": label,
                    "props": {
                        "type": field_type,
                        "control": control,
                        "placeholder": placeholder,
                    },
                    "source_refs": source_refs,
                    "assumption": "Field inferred from label/value-like text.",
                }
            )
            assumptions.append(f"Field '{label}' was inferred from text, not explicit form metadata.")
            continue

        if block_type == "list":
            list_id = f"list_{slugify(block_id or text[:20], 'list')}"
            items = split_list_items(text)
            current_section["items"].append(
                {
                    "kind": "list",
                    "id": list_id,
                    "items": items,
                    "source_refs": source_refs,
                }
            )
            component_map.append(
                {
                    "generated_unit_id": list_id,
                    "kind": "list",
                    "label": short_text(text, 40),
                    "props": {"item_count": len(items)},
                    "source_refs": source_refs,
                    "assumption": None,
                }
            )
            continue

        if block_type in {"figure", "chart", "formula"}:
            item_id = f"{block_type}_{slugify(block_id or block_type)}"
            placeholder_text = text or block_type.title()
            current_section["items"].append(
                {
                    "kind": block_type,
                    "id": item_id,
                    "text": placeholder_text,
                    "source_refs": source_refs,
                }
            )
            component_map.append(
                {
                    "generated_unit_id": item_id,
                    "kind": block_type,
                    "label": short_text(placeholder_text, 40),
                    "props": {},
                    "source_refs": source_refs,
                    "assumption": f"{block_type.title()} is represented as a placeholder block in the scaffold.",
                }
            )
            assumptions.append(f"{block_type.title()} blocks are preserved as placeholders in generated code.")
            continue

        clean_text = strip_html_tags(text) or text
        text_id = f"text_{slugify(block_id or clean_text[:20], 'text')}"
        current_section["items"].append(
            {
                "kind": "text",
                "id": text_id,
                "text": clean_text,
                "source_refs": source_refs,
            }
        )
        component_map.append(
            {
                "generated_unit_id": text_id,
                "kind": "text",
                "label": short_text(clean_text, 50),
                "props": {},
                "source_refs": source_refs,
                "assumption": None,
            }
        )

    if not sections:
        sections.append(
            {
                "id": "section_generated_1",
                "title": title,
                "items": [],
                "source_refs": [make_source_ref(None, None)],
            }
        )

    return sections, component_map, field_schema, sorted(set(assumptions))


def build_ui_blueprint(
    title: str,
    document: dict[str, Any],
    sections: list[dict[str, Any]],
    field_schema: list[dict[str, Any]],
) -> dict[str, Any]:
    profile = infer_document_profile(title, document, sections, field_schema)
    return {
        "title": title,
        "document_profile": profile,
        "navigation": [
            {
                "id": section["id"],
                "title": section["title"],
                "kind": classify_section(section),
            }
            for section in sections
        ],
        "sections": [
            {
                "id": section["id"],
                "title": section["title"],
                "kind": classify_section(section),
                "items": section["items"],
            }
            for section in sections
        ],
    }


def build_json_schema(title: str, field_schema: list[dict[str, Any]], sections: list[dict[str, Any]]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required: list[str] = []

    for field in field_schema:
        field_name = field["name"]
        field_type = field["type"]
        schema_type = "string"
        field_format: str | None = None

        if field_type == "number":
            schema_type = "number"
        elif field_type == "email":
            field_format = "email"
        elif field_type == "tel":
            field_format = "tel"
        elif field_type == "date":
            field_format = "date"
        elif field_type == "password":
            field_format = "password"

        prop: dict[str, Any] = {
            "title": field["label"],
            "type": schema_type,
            "description": f"Inferred from section '{field['section']}'.",
        }
        if field_format:
            prop["format"] = field_format
        if field.get("placeholder"):
            prop["examples"] = [field["placeholder"]]

        properties[field_name] = prop
        if field.get("required"):
            required.append(field_name)

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "properties": properties,
        "required": required,
        "x-generated-sections": [section["title"] for section in sections],
    }


def normalize_notebook_slug(token: str) -> str:
    value = token.strip().replace(" ", "_")
    value = re.sub(r"[^A-Za-z0-9_]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def collect_clean_texts(document: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for row in iter_blocks(document):
        text = strip_html_tags((row["block"].get("text") or "").strip())
        if text:
            values.append(text)
    return values


def extract_notebook_outline(document: dict[str, Any]) -> list[str]:
    texts = collect_clean_texts(document)
    outline: list[str] = []
    index = 0
    while index < len(texts):
        current = texts[index]
        if re.match(r"^\d{2}_[A-Za-z0-9_]+_$", current) and index + 1 < len(texts):
            merged = normalize_notebook_slug(current + texts[index + 1])
            outline.append(merged)
            index += 2
            continue
        if re.match(r"^\d{2}_[A-Za-z0-9_]+$", current):
            outline.append(current)
            index += 1
            continue
        index += 1
    deduped: list[str] = []
    for item in outline:
        if item not in deduped:
            deduped.append(item)
    return deduped


def infer_notebook_workflow_steps(document: dict[str, Any]) -> list[str]:
    texts = collect_clean_texts(document)
    candidates = [
        text
        for text in texts
        if any(
            marker in text.lower()
            for marker in ["gradio", "prompt", "pipeline", "openvino", "model", "benchmark"]
        )
    ]
    steps: list[str] = []
    for item in candidates:
        if item not in steps:
            steps.append(item)
    return steps[:10]


def build_notebook_plan(title: str, document: dict[str, Any], blueprint: dict[str, Any]) -> dict[str, Any]:
    outline = extract_notebook_outline(document)
    if not outline:
        outline = [
            "00_intro",
            "01_environment_setup",
            "02_load_model",
            "03_export_or_convert_to_openvino",
            "04_optimize_model",
            "05_build_inference_pipeline",
            "06_launch_gradio_demo",
            "07_evaluation_and_benchmark",
        ]

    workflow_steps = infer_notebook_workflow_steps(document)
    model_id = "google/gemma-3-4b-it"
    if any("gemma4" in item.lower() for item in outline):
        model_id = "google/gemma-3-4b-it"

    return {
        "title": title,
        "outline": outline,
        "workflow_steps": workflow_steps,
        "model_id": model_id,
        "document_kind": blueprint["document_profile"]["document_kind"],
        "source_snippets": blueprint["document_profile"].get("source_snippets", []),
    }


def make_markdown_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.rstrip().splitlines()],
    }


def make_code_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [line + "\n" for line in source.rstrip().splitlines()],
    }


def notebook_cell_sources(plan: dict[str, Any]) -> list[dict[str, Any]]:
    title = plan["title"]
    model_id = plan["model_id"]
    outline = plan["outline"]
    workflow_steps = plan["workflow_steps"]
    workflow_bullets = "\n".join(f"- {item}" for item in workflow_steps) or "- Parse document structure\n- Build an OpenVINO notebook pipeline"
    outline_bullets = "\n".join(f"- `{item}`" for item in outline)

    cells: list[dict[str, Any]] = [
        make_markdown_cell(
            f"""# {title}

This notebook scaffold was generated from a document-to-code run.

## Intended flow
{workflow_bullets}

## Suggested notebook structure
{outline_bullets}
"""
        ),
        make_code_cell(
            f"""from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class NotebookConfig:
    model_id: str = os.getenv("MODEL_ID", "{model_id}")
    device: str = os.getenv("OPENVINO_DEVICE", "GPU")
    precision: str = os.getenv("MODEL_PRECISION", "int4")
    workspace: Path = Path.cwd()
    model_dir: Path = Path("models") / "hf"
    ov_model_dir: Path = Path("models") / "openvino"
    prompt: str = os.getenv("DEFAULT_PROMPT", "Explain how this OpenVINO notebook is structured.")
    max_new_tokens: int = int(os.getenv("MAX_NEW_TOKENS", "256"))


cfg = NotebookConfig()
cfg.model_dir.mkdir(parents=True, exist_ok=True)
cfg.ov_model_dir.mkdir(parents=True, exist_ok=True)
print(json.dumps({{k: str(v) for k, v in asdict(cfg).items()}}, ensure_ascii=False, indent=2))
"""
        ),
        make_markdown_cell("## 01 Environment Setup"),
        make_code_cell(
            """import platform
import sys

import openvino as ov

print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())
print("OpenVINO:", ov.__version__)
core = ov.Core()
print("Available devices:", core.available_devices)
"""
        ),
        make_markdown_cell("## 02 Load Base Model"),
        make_code_cell(
            """from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(cfg.model_id)
hf_model = AutoModelForCausalLM.from_pretrained(
    cfg.model_id,
    trust_remote_code=True,
)
print("Loaded base model:", cfg.model_id)
"""
        ),
        make_markdown_cell("## 03 Export Or Convert To OpenVINO"),
        make_code_cell(
            """from optimum.intel import OVModelForCausalLM

ov_model = OVModelForCausalLM.from_pretrained(
    cfg.model_id,
    export=True,
    compile=False,
    trust_remote_code=True,
)
ov_model.save_pretrained(cfg.ov_model_dir)
tokenizer.save_pretrained(cfg.ov_model_dir)
print("Exported OpenVINO model to", cfg.ov_model_dir.resolve())
"""
        ),
        make_markdown_cell("## 04 Optimize Model And Compile"),
        make_code_cell(
            """compile_config = {
    "PERFORMANCE_HINT": "LATENCY",
}

core = ov.Core()
compiled_model = ov_model.compile()
print("Compiled model for device:", cfg.device)
"""
        ),
        make_markdown_cell("## 05 Build Inference Pipeline"),
        make_code_cell(
            """from optimum.intel import OVModelForCausalLM

runtime_tokenizer = AutoTokenizer.from_pretrained(cfg.ov_model_dir)
runtime_model = OVModelForCausalLM.from_pretrained(
    cfg.ov_model_dir,
    compile=False,
    trust_remote_code=True,
)


def generate_response(prompt: str, max_new_tokens: int = 256) -> str:
    inputs = runtime_tokenizer(prompt, return_tensors="pt")
    outputs = runtime_model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
    )
    return runtime_tokenizer.decode(outputs[0], skip_special_tokens=True)


preview = generate_response(cfg.prompt, max_new_tokens=min(cfg.max_new_tokens, 96))
print(preview)
"""
        ),
        make_markdown_cell("## 06 Launch Gradio Demo"),
        make_code_cell(
            """import gradio as gr


def run_demo(prompt: str) -> str:
    return generate_response(prompt, max_new_tokens=cfg.max_new_tokens)


demo = gr.Interface(
    fn=run_demo,
    inputs=gr.Textbox(label="Prompt", lines=6, value=cfg.prompt),
    outputs=gr.Textbox(label="Response", lines=12),
    title="OpenVINO Notebook Demo",
    description="Generated notebook demo scaffold.",
)

# Uncomment the next line to launch the UI in Jupyter or locally.
# demo.launch(share=False)
demo
"""
        ),
        make_markdown_cell("## 07 Evaluation And Benchmark"),
        make_code_cell(
            """def benchmark_prompt(prompt: str, rounds: int = 3) -> dict:
    latencies = []
    response = ""
    for _ in range(rounds):
        start = time.perf_counter()
        response = generate_response(prompt, max_new_tokens=min(cfg.max_new_tokens, 64))
        latencies.append(time.perf_counter() - start)
    return {
        "rounds": rounds,
        "avg_latency_sec": sum(latencies) / len(latencies),
        "min_latency_sec": min(latencies),
        "max_latency_sec": max(latencies),
        "last_response_preview": response[:240],
    }


benchmark_result = benchmark_prompt("Summarize the generated OpenVINO notebook workflow.")
print(json.dumps(benchmark_result, ensure_ascii=False, indent=2))
"""
        ),
    ]
    return cells


def build_notebook_artifact(title: str, plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "cells": notebook_cell_sources(plan),
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
            "generated_from": {
                "title": title,
                "outline": plan["outline"],
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def render_react_app(title: str, blueprint: dict[str, Any]) -> str:
    sections_json = json.dumps(blueprint["sections"], ensure_ascii=False, indent=2)
    profile_json = json.dumps(blueprint["document_profile"], ensure_ascii=False, indent=2)
    nav_json = json.dumps(blueprint["navigation"], ensure_ascii=False, indent=2)

    return f'''import React from "react";

const pageTitle = {json.dumps(title, ensure_ascii=False)};
const profile = {profile_json};
const navigation = {nav_json};
const sections = {sections_json};

function ShellCard({{ children, style = {{}} }}) {{
  return (
    <div
      style={{{{
        background: "#ffffff",
        border: "1px solid #d8dee9",
        borderRadius: 8,
        boxShadow: "0 12px 40px rgba(15, 23, 42, 0.06)",
        ...style
      }}}}
    >
      {{children}}
    </div>
  );
}}

function OverviewCard({{ label, value }}) {{
  return (
    <ShellCard style={{{{ padding: 16, minHeight: 96 }}}}>
      <div style={{{{ fontSize: 12, color: "#64748b", marginBottom: 8 }}}}>{{label}}</div>
      <div style={{{{ fontSize: 22, fontWeight: 700, color: "#0f172a" }}}}>{{value}}</div>
    </ShellCard>
  );
}}

function FieldControl({{ item }}) {{
  const sharedStyle = {{
    width: "100%",
    padding: "11px 12px",
    border: "1px solid #cbd5e1",
    borderRadius: 8,
    fontSize: 14,
    color: "#0f172a",
    background: "#ffffff"
  }};

  let control = (
    <input
      type={{item.field_type === "password" ? "password" : item.field_type}}
      placeholder={{item.placeholder}}
      style={{sharedStyle}}
    />
  );

  if (item.control === "textarea") {{
    control = <textarea placeholder={{item.placeholder}} rows={{4}} style={{sharedStyle}} />;
  }} else if (item.control === "select") {{
    control = (
      <select defaultValue="" style={{sharedStyle}}>
        <option value="" disabled>
          {{item.placeholder || `Select ${{item.label}}`}}
        </option>
      </select>
    );
  }}

  return (
    <div
      style={{{{
        display: "grid",
        gap: 8,
        gridColumn: item.width === "full" ? "1 / -1" : "auto"
      }}}}
    >
      <label style={{{{ fontWeight: 600, fontSize: 14, color: "#1e293b" }}}}>{{item.label}}</label>
      {{control}}
    </div>
  );
}}

function DataTable({{ title, headers = [], rows = [] }}) {{
  return (
    <ShellCard style={{{{ overflow: "hidden" }}}}>
      <div style={{{{ padding: "16px 18px", borderBottom: "1px solid #e2e8f0" }}}}>
        <h3 style={{{{ margin: 0, fontSize: 17, color: "#0f172a" }}}}>{{title}}</h3>
      </div>
      <div style={{{{ overflowX: "auto" }}}}>
        <table style={{{{ width: "100%", borderCollapse: "collapse" }}}}>
          <thead>
            <tr style={{{{ background: "#f8fafc" }}}}>
              {{headers.map((header, idx) => (
                <th
                  key={{idx}}
                  style={{{{
                    textAlign: "left",
                    padding: "12px 16px",
                    fontSize: 13,
                    color: "#475569",
                    borderBottom: "1px solid #e2e8f0"
                  }}}}
                >
                  {{header}}
                </th>
              ))}}
            </tr>
          </thead>
          <tbody>
            {{rows.map((row, rowIdx) => (
              <tr key={{rowIdx}}>
                {{row.map((cell, cellIdx) => (
                  <td
                    key={{cellIdx}}
                    style={{{{
                      padding: "12px 16px",
                      borderBottom: "1px solid #eef2f7",
                      verticalAlign: "top",
                      color: "#0f172a"
                    }}}}
                  >
                    {{cell}}
                  </td>
                ))}}
              </tr>
            ))}}
          </tbody>
        </table>
      </div>
    </ShellCard>
  );
}}

function PlaceholderBlock({{ kind, text }}) {{
  return (
    <ShellCard
      style={{{{
        padding: 16,
        borderStyle: "dashed",
        background: "#f8fafc"
      }}}}
    >
      <div style={{{{ fontSize: 12, color: "#64748b", marginBottom: 8 }}}}>{{kind.toUpperCase()}}</div>
      <div style={{{{ color: "#0f172a" }}}}>{{text || "Placeholder block"}}</div>
    </ShellCard>
  );
}}

function SectionBlock({{ section }}) {{
  const fields = section.items.filter((item) => item.kind === "field");
  const otherItems = section.items.filter((item) => item.kind !== "field");

  return (
    <section id={{section.id}} style={{{{ display: "grid", gap: 16 }}}}>
      <div>
        <div style={{{{ fontSize: 12, color: "#2563eb", marginBottom: 6, fontWeight: 700 }}}}>
          {{section.kind.replace("-", " ").toUpperCase()}}
        </div>
        <h2 style={{{{ margin: 0, fontSize: 24, color: "#0f172a" }}}}>{{section.title}}</h2>
      </div>

      {{fields.length > 0 ? (
        <ShellCard style={{{{ padding: 20 }}}}>
          <div
            style={{{{
              display: "grid",
              gap: 16,
              gridTemplateColumns: "repeat(2, minmax(0, 1fr))"
            }}}}
          >
            {{fields.map((item) => (
              <FieldControl key={{item.id}} item={{item}} />
            ))}}
          </div>
        </ShellCard>
      ) : null}}

      {{otherItems.map((item) => {{
        if (item.kind === "text") {{
          return (
            <ShellCard key={{item.id}} style={{{{ padding: 20 }}}}>
              <p style={{{{ margin: 0, lineHeight: 1.7, color: "#334155" }}}}>{{item.text}}</p>
            </ShellCard>
          );
        }}

        if (item.kind === "list") {{
          return (
            <ShellCard key={{item.id}} style={{{{ padding: 20 }}}}>
              <ul style={{{{ margin: 0, paddingLeft: 20, color: "#334155" }}}}>
                {{item.items.map((entry, idx) => (
                  <li key={{idx}} style={{{{ marginBottom: 10 }}}}>{{entry}}</li>
                ))}}
              </ul>
            </ShellCard>
          );
        }}

        if (item.kind === "table") {{
          return (
            <DataTable
              key={{item.id}}
              title={{item.title}}
              headers={{item.headers}}
              rows={{item.rows}}
            />
          );
        }}

        return (
          <PlaceholderBlock
            key={{item.id}}
            kind={{item.kind}}
            text={{item.text || item.title || item.asset_path || ""}}
          />
        );
      }})}}
    </section>
  );
}}

export default function App() {{
  return (
    <div
      style={{{{
        minHeight: "100vh",
        background: "#eef4fb",
        color: "#0f172a",
        fontFamily: "Inter, Arial, sans-serif"
      }}}}
    >
      <div
        style={{{{
          maxWidth: 1360,
          margin: "0 auto",
          padding: 24,
          display: "grid",
          gap: 24,
          gridTemplateColumns: "280px minmax(0, 1fr)"
        }}}}
      >
        <aside style={{{{ display: "grid", gap: 18, alignContent: "start" }}}}>
          <ShellCard style={{{{ padding: 20 }}}}>
            <div style={{{{ fontSize: 12, color: "#2563eb", marginBottom: 10, fontWeight: 700 }}}}>
              {{profile.document_kind.replace("-", " ").toUpperCase()}}
            </div>
            <h1 style={{{{ margin: 0, fontSize: 26, lineHeight: 1.2 }}}}>{{pageTitle}}</h1>
            <p style={{{{ margin: "14px 0 0", color: "#475569", lineHeight: 1.6 }}}}>
              {{profile.source_snippets[0] || "Generated from structured document parsing."}}
            </p>
          </ShellCard>

          <ShellCard style={{{{ padding: 18 }}}}>
            <div style={{{{ fontSize: 12, color: "#64748b", marginBottom: 12, fontWeight: 700 }}}}>SECTIONS</div>
            <div style={{{{ display: "grid", gap: 10 }}}}>
              {{navigation.map((item) => (
                <a
                  key={{item.id}}
                  href={{`#${{item.id}}`}}
                  style={{{{
                    color: "#0f172a",
                    textDecoration: "none",
                    padding: "10px 12px",
                    borderRadius: 8,
                    background: "#f8fafc",
                    border: "1px solid #e2e8f0"
                  }}}}
                >
                  <div style={{{{ fontWeight: 600, marginBottom: 4 }}}}>{{item.title}}</div>
                  <div style={{{{ fontSize: 12, color: "#64748b" }}}}>{{item.kind}}</div>
                </a>
              ))}}
            </div>
          </ShellCard>

          <ShellCard style={{{{ padding: 18 }}}}>
            <div style={{{{ fontSize: 12, color: "#64748b", marginBottom: 12, fontWeight: 700 }}}}>ACTIONS</div>
            <div style={{{{ display: "grid", gap: 10 }}}}>
              {{profile.actions.map((action, index) => (
                <button
                  key={{action}}
                  type="button"
                  style={{{{
                    border: index === 0 ? "none" : "1px solid #cbd5e1",
                    background: index === 0 ? "#2563eb" : "#ffffff",
                    color: index === 0 ? "#ffffff" : "#0f172a",
                    borderRadius: 8,
                    padding: "11px 14px",
                    fontWeight: 600,
                    cursor: "pointer"
                  }}}}
                >
                  {{action}}
                </button>
              ))}}
            </div>
          </ShellCard>
        </aside>

        <main style={{{{ display: "grid", gap: 24, alignContent: "start" }}}}>
          <div style={{{{ display: "grid", gap: 16 }}}}>
            <div
              style={{{{
                display: "grid",
                gap: 16,
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))"
              }}}}
            >
              {{profile.overview_cards.map((card) => (
                <OverviewCard key={{card.label}} label={{card.label}} value={{card.value}} />
              ))}}
            </div>
          </div>

          {{sections.map((section) => (
            <SectionBlock key={{section.id}} section={{section}} />
          ))}}
        </main>
      </div>
    </div>
  );
}}
'''


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_html(title: str, blueprint: dict[str, Any]) -> str:
    profile = blueprint["document_profile"]

    def render_field(item: dict[str, Any]) -> str:
        label = escape_html(item["label"])
        placeholder = escape_html(item.get("placeholder", ""))
        control = item.get("control")
        width_class = "field field-full" if item.get("width") == "full" else "field"

        if control == "textarea":
            body = f'<textarea rows="4" placeholder="{placeholder}"></textarea>'
        elif control == "select":
            body = (
                f'<select><option value="" selected disabled>{placeholder or "Select option"}</option></select>'
            )
        else:
            input_type = "password" if item["field_type"] == "password" else item["field_type"]
            body = f'<input type="{escape_html(input_type)}" placeholder="{placeholder}" />'

        return f'''
<div class="{width_class}">
  <label>{label}</label>
  {body}
</div>
'''.strip()

    section_html: list[str] = []
    for section in blueprint["sections"]:
        fields = [item for item in section["items"] if item["kind"] == "field"]
        other_items = [item for item in section["items"] if item["kind"] != "field"]

        field_html = ""
        if fields:
            field_html = f'''
<div class="panel">
  <div class="field-grid">
    {"".join(render_field(item) for item in fields)}
  </div>
</div>
'''.strip()

        items_html: list[str] = []
        for item in other_items:
            kind = item["kind"]
            if kind == "text":
                items_html.append(f'<div class="panel"><p>{escape_html(item["text"])}</p></div>')
            elif kind == "list":
                lis = "".join(f"<li>{escape_html(entry)}</li>" for entry in item["items"])
                items_html.append(f'<div class="panel"><ul>{lis}</ul></div>')
            elif kind == "table":
                headers = "".join(f"<th>{escape_html(str(h))}</th>" for h in item["headers"])
                rows = []
                for row in item["rows"]:
                    tds = "".join(f"<td>{escape_html(str(cell))}</td>" for cell in row)
                    rows.append(f"<tr>{tds}</tr>")
                items_html.append(
                    f'''
<div class="panel table-panel">
  <div class="panel-head">
    <h3>{escape_html(item["title"])}</h3>
  </div>
  <div class="table-wrap">
    <table>
      <thead><tr>{headers}</tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table>
  </div>
</div>
'''.strip()
                )
            else:
                text = item.get("text") or item.get("title") or item.get("asset_path") or ""
                items_html.append(
                    f'<div class="panel placeholder"><strong>{escape_html(kind.upper())}</strong><p>{escape_html(text)}</p></div>'
                )

        section_html.append(
            f'''
<section class="section" id="{escape_html(section["id"])}">
  <div class="section-head">
    <div class="eyebrow">{escape_html(section["kind"].upper())}</div>
    <h2>{escape_html(section["title"])}</h2>
  </div>
  {field_html}
  {"".join(items_html)}
</section>
'''.strip()
        )

    sidebar_nav = "".join(
        f'''
<a class="nav-item" href="#{escape_html(item["id"])}">
  <span>{escape_html(item["title"])}</span>
  <small>{escape_html(item["kind"])}</small>
</a>
'''.strip()
        for item in blueprint["navigation"]
    )

    cards_html = "".join(
        f'''
<div class="stat-card">
  <span>{escape_html(card["label"])}</span>
  <strong>{escape_html(card["value"])}</strong>
</div>
'''.strip()
        for card in profile["overview_cards"]
    )

    action_html = "".join(
        f'<button class="action{" primary" if index == 0 else ""}" type="button">{escape_html(action)}</button>'
        for index, action in enumerate(profile["actions"])
    )

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{escape_html(title)}</title>
  <link rel="stylesheet" href="./styles.css" />
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="panel hero-panel">
        <div class="eyebrow">{escape_html(profile["document_kind"].replace("-", " ").upper())}</div>
        <h1>{escape_html(title)}</h1>
        <p>{escape_html(profile["source_snippets"][0] if profile["source_snippets"] else "Generated from structured document parsing.")}</p>
      </div>

      <div class="panel">
        <div class="panel-label">Sections</div>
        <nav class="nav-list">
          {sidebar_nav}
        </nav>
      </div>

      <div class="panel">
        <div class="panel-label">Actions</div>
        <div class="action-list">
          {action_html}
        </div>
      </div>
    </aside>

    <main class="content">
      <section class="stats-grid">
        {cards_html}
      </section>
      {"".join(section_html)}
    </main>
  </div>
</body>
</html>
'''


def render_css() -> str:
    return """* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #eef4fb;
  color: #0f172a;
  font-family: Inter, Arial, sans-serif;
}

button,
input,
textarea,
select {
  font: inherit;
}

.app-shell {
  max-width: 1360px;
  margin: 0 auto;
  padding: 24px;
  display: grid;
  gap: 24px;
  grid-template-columns: 280px minmax(0, 1fr);
}

.sidebar,
.content {
  display: grid;
  gap: 24px;
  align-content: start;
}

.panel {
  background: #ffffff;
  border: 1px solid #d8dee9;
  border-radius: 8px;
  box-shadow: 0 12px 40px rgba(15, 23, 42, 0.06);
  padding: 18px;
}

.hero-panel {
  padding: 20px;
}

.hero-panel h1 {
  margin: 0;
  font-size: 26px;
  line-height: 1.2;
}

.hero-panel p,
.panel p,
.panel li {
  color: #475569;
  line-height: 1.7;
}

.eyebrow,
.panel-label {
  font-size: 12px;
  color: #2563eb;
  font-weight: 700;
  margin-bottom: 10px;
}

.panel-label {
  color: #64748b;
}

.nav-list,
.action-list {
  display: grid;
  gap: 10px;
}

.nav-item {
  text-decoration: none;
  color: #0f172a;
  padding: 10px 12px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  display: grid;
  gap: 4px;
}

.nav-item span {
  font-weight: 600;
}

.nav-item small {
  color: #64748b;
}

.action {
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #0f172a;
  border-radius: 8px;
  padding: 11px 14px;
  font-weight: 600;
  cursor: pointer;
}

.action.primary {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}

.stats-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.stat-card {
  background: #ffffff;
  border: 1px solid #d8dee9;
  border-radius: 8px;
  box-shadow: 0 12px 40px rgba(15, 23, 42, 0.06);
  min-height: 96px;
  padding: 16px;
  display: grid;
  gap: 8px;
  align-content: start;
}

.stat-card span {
  font-size: 12px;
  color: #64748b;
}

.stat-card strong {
  font-size: 22px;
}

.section {
  display: grid;
  gap: 16px;
}

.section-head h2 {
  margin: 0;
  font-size: 24px;
}

.field-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.field {
  display: grid;
  gap: 8px;
}

.field-full {
  grid-column: 1 / -1;
}

.field label {
  font-weight: 600;
  font-size: 14px;
  color: #1e293b;
}

.field input,
.field textarea,
.field select {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 14px;
  color: #0f172a;
  background: #ffffff;
}

.table-panel {
  overflow: hidden;
  padding: 0;
}

.panel-head {
  padding: 16px 18px;
  border-bottom: 1px solid #e2e8f0;
}

.panel-head h3 {
  margin: 0;
  font-size: 17px;
}

.table-wrap {
  overflow-x: auto;
}

.table-wrap table {
  width: 100%;
  border-collapse: collapse;
}

.table-wrap th {
  text-align: left;
  padding: 12px 16px;
  font-size: 13px;
  color: #475569;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.table-wrap td {
  padding: 12px 16px;
  border-bottom: 1px solid #eef2f7;
  vertical-align: top;
}

.placeholder strong {
  display: block;
  margin-bottom: 8px;
  color: #64748b;
  font-size: 12px;
}

ul {
  margin: 0;
  padding-left: 20px;
}

@media (max-width: 1024px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    order: 1;
  }

  .content {
    order: 0;
  }
}

@media (max-width: 720px) {
  .app-shell {
    padding: 16px;
  }

  .field-grid {
    grid-template-columns: 1fr;
  }

  .field-full {
    grid-column: auto;
  }
}
"""


def build_traceability(component_map: list[dict[str, Any]], artifact_path: str) -> dict[str, Any]:
    return {
        "artifact": artifact_path,
        "mappings": [
            {
                "generated_unit_id": item["generated_unit_id"],
                "generated_text": item["label"],
                "source_refs": item.get("source_refs", []),
                "assumption": item.get("assumption"),
            }
            for item in component_map
        ],
    }


def build_notes(
    title: str,
    assumptions: list[str],
    target: str,
    field_schema: list[dict[str, Any]],
    blueprint: dict[str, Any],
) -> str:
    profile = blueprint["document_profile"]
    lines = [
        "# Generated Notes",
        "",
        f"- Title: {title}",
        f"- Target: {target}",
        f"- Document kind: {profile['document_kind']}",
        f"- Generated fields: {len(field_schema)}",
        f"- Generated sections: {len(blueprint['sections'])}",
        "",
        "## Assumptions",
    ]
    if assumptions:
        lines.extend(f"- {a}" for a in assumptions)
    else:
        lines.append("- No major heuristic assumptions were recorded.")
    lines.extend(
        [
            "",
            "## Review Checklist",
            "- Verify section grouping",
            "- Verify field labels, controls, and placeholder copy",
            "- Add validation rules and business logic manually",
            "- Replace placeholder figure/chart/formula blocks if needed",
            "- Review the generated layout against the original source before shipping",
            "- Review all generated code before running it locally or connecting it to real systems",
        ]
    )
    return "\n".join(lines) + "\n"


def build_notebook_notes(plan: dict[str, Any]) -> str:
    outline = "\n".join(f"- {item}" for item in plan["outline"])
    workflow = "\n".join(f"- {item}" for item in plan["workflow_steps"]) or "- No explicit workflow labels were detected."
    return (
        "# Generated Notebook Notes\n\n"
        "This notebook scaffold was generated for an OpenVINO notebook-style target.\n\n"
        "Review all generated notebook cells before execution. Treat the notebook as a draft, not a trusted artifact.\n\n"
        "## Inferred notebook outline\n"
        f"{outline}\n\n"
        "## Inferred workflow labels\n"
        f"{workflow}\n"
    )


def main() -> int:
    config = parse_args()
    ensure_dir(config.out)

    try:
        if not config.parsed_json.exists():
            raise FileNotFoundError(f"parsed.json not found: {config.parsed_json}")

        document = load_json(config.parsed_json)
        problems = validate_document_schema(document)
        if problems:
            raise ValueError("Invalid parsed.json: " + "; ".join(problems))

        title = detect_title(document, config.title)
        sections, component_map, field_schema, assumptions = infer_sections(document, title)
        blueprint = build_ui_blueprint(title, document, sections, field_schema)

        write_json(config.out / "component_map.json", component_map)
        write_json(config.out / "field_schema.json", field_schema)
        write_json(config.out / "ui_blueprint.json", blueprint)

        generated_files: list[str] = []

        if config.target == "react":
            write_text(
                config.out / "notes.md",
                build_notes(title, assumptions, config.target, field_schema, blueprint),
            )
            artifact_name = "app.jsx"
            write_text(config.out / artifact_name, render_react_app(title, blueprint))
            generated_files.append(artifact_name)
        elif config.target == "html-css":
            write_text(
                config.out / "notes.md",
                build_notes(title, assumptions, config.target, field_schema, blueprint),
            )
            write_text(config.out / "index.html", render_html(title, blueprint))
            write_text(config.out / "styles.css", render_css())
            generated_files.extend(["index.html", "styles.css"])
        elif config.target == "json-schema":
            write_text(
                config.out / "notes.md",
                build_notes(title, assumptions, config.target, field_schema, blueprint),
            )
            write_json(config.out / "schema.json", build_json_schema(title, field_schema, sections))
            generated_files.append("schema.json")
        elif config.target == "jupyter-notebook":
            plan = build_notebook_plan(title, document, blueprint)
            notebook = build_notebook_artifact(title, plan)
            write_json(config.out / "notebook_plan.json", plan)
            write_json(config.out / "notebook.ipynb", notebook)
            write_text(config.out / "notes.md", build_notebook_notes(plan))
            generated_files.extend(["notebook.ipynb", "notebook_plan.json"])

        traceability_target = generated_files[0] if generated_files else "component_map.json"
        write_json(
            config.out / "traceability.json",
            build_traceability(component_map, f"task_output/{traceability_target}"),
        )

        print(
            json.dumps(
                {
                    "ok": True,
                    "target": config.target,
                    "parsed_json": str(config.parsed_json),
                    "output_dir": str(config.out),
                    "generated_files": generated_files
                    + [
                        "component_map.json",
                        "field_schema.json",
                        "ui_blueprint.json",
                        "traceability.json",
                        "notes.md",
                    ],
                    "section_count": len(sections),
                    "component_count": len(component_map),
                    "field_count": len(field_schema),
                    "document_kind": blueprint["document_profile"]["document_kind"],
                },
                ensure_ascii=False,
            )
        )
        return 0

    except Exception as exc:
        write_error(
            config.out,
            stage="transform_doc_to_code",
            message=str(exc),
            parsed_json=str(config.parsed_json),
            target=config.target,
        )
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "transform_doc_to_code",
                    "message": str(exc),
                    "parsed_json": str(config.parsed_json),
                    "output_dir": str(config.out),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
