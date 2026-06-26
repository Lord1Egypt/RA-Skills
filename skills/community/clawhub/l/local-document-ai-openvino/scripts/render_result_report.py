#!/usr/bin/env python3
"""
render_result_report.py

Create a local HTML report plus layout visualization images for a run artifact.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any

from _local_vendor import bootstrap_local_vendor


bootstrap_local_vendor()

from PIL import Image, ImageDraw, ImageFont

from utils import ensure_dir, load_json


LABEL_COLORS = {
    "doc_title": (76, 175, 80),
    "heading": (76, 175, 80),
    "text": (33, 150, 243),
    "paragraph": (33, 150, 243),
    "kv_pair": (33, 150, 243),
    "table": (255, 152, 0),
    "image": (156, 39, 176),
    "figure": (156, 39, 176),
    "chart": (121, 85, 72),
    "formula": (126, 87, 194),
    "seal": (244, 67, 54),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a local HTML report for a run artifact.")
    parser.add_argument("--artifact-dir", required=True, help="Artifact directory from run_skill.py")
    return parser.parse_args()


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT = load_font(18)
FONT_SMALL = load_font(14)


def render_pdf_pages(pdf_path: Path, out_dir: Path) -> list[Path]:
    ensure_dir(out_dir)
    results: list[Path] = []
    try:
        import pypdfium2 as pdfium  # type: ignore

        doc = pdfium.PdfDocument(str(pdf_path))
        scale = 200 / 72.0
        for page_number in range(len(doc)):
            page = doc[page_number]
            out_path = out_dir / f"page_{page_number + 1}.png"
            page.render(scale=scale).to_pil().convert("RGB").save(out_path)
            results.append(out_path)
            page.close()
        doc.close()
        return results
    except Exception:
        pass

    import fitz  # type: ignore

    doc = fitz.open(str(pdf_path))
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        out_path = out_dir / f"page_{page_number + 1}.png"
        out_path.write_bytes(pixmap.tobytes("png"))
        results.append(out_path)
    doc.close()
    return results


def render_input_pages(parsed: dict[str, Any], artifact_dir: Path, out_dir: Path) -> list[Path]:
    source_path = Path(parsed["source"]["input_path"])
    ensure_dir(out_dir)
    if source_path.suffix.lower() == ".pdf":
        return render_pdf_pages(source_path, out_dir)
    target = out_dir / source_path.name
    shutil.copyfile(source_path, target)
    return [target]


def draw_layout_overlay(page_image: Path, layout_json: Path, out_path: Path) -> dict[str, Any]:
    res = load_json(layout_json)["res"]
    boxes = res.get("layout_det_res", {}).get("boxes", [])
    with Image.open(page_image) as base:
        image = base.convert("RGB")
    source_width = float(res.get("width") or image.width or 1)
    source_height = float(res.get("height") or image.height or 1)
    scale_x = image.width / source_width
    scale_y = image.height / source_height
    draw = ImageDraw.Draw(image)
    counts: dict[str, int] = {}
    for box in boxes:
        label = box.get("label") or "unknown"
        x0, y0, x1, y1 = box.get("coordinate", [0, 0, 0, 0])
        x0 = int(round(float(x0) * scale_x))
        y0 = int(round(float(y0) * scale_y))
        x1 = int(round(float(x1) * scale_x))
        y1 = int(round(float(y1) * scale_y))
        color = LABEL_COLORS.get(label, (0, 188, 212))
        counts[label] = counts.get(label, 0) + 1
        draw.rectangle([x0, y0, x1, y1], outline=color, width=3)
        score = box.get("score")
        text = f"{label} {score:.2f}" if isinstance(score, (int, float)) else label
        tx = max(4, x0)
        ty = max(4, y0 - 22)
        bbox = draw.textbbox((tx, ty), text, font=FONT_SMALL)
        draw.rectangle(bbox, fill=color)
        draw.text((tx, ty), text, fill=(255, 255, 255), font=FONT_SMALL)
    image.save(out_path)
    return {
        "page_image": page_image.name,
        "layout_image": out_path.name,
        "box_counts": counts,
        "total_boxes": len(boxes),
        "scale_x": scale_x,
        "scale_y": scale_y,
    }


def draw_mineru_overlay(page_image: Path, block_json: Path, out_path: Path) -> dict[str, Any]:
    payload = load_json(block_json)
    blocks = payload.get("blocks", [])
    with Image.open(page_image) as base:
        image = base.convert("RGB")
    draw = ImageDraw.Draw(image)
    counts: dict[str, int] = {}
    for block in blocks:
        label = str(block.get("type") or "unknown")
        bbox = block.get("bbox") or [0, 0, 0, 0]
        if not isinstance(bbox, list) or len(bbox) != 4:
            continue
        try:
            x0, y0, x1, y1 = [float(value) for value in bbox]
        except (TypeError, ValueError):
            continue
        if max(x0, y0, x1, y1) <= 1.5:
            x0 *= image.width
            y0 *= image.height
            x1 *= image.width
            y1 *= image.height
        color = LABEL_COLORS.get(label, (0, 188, 212))
        counts[label] = counts.get(label, 0) + 1
        draw.rectangle([x0, y0, x1, y1], outline=color, width=3)
        text = label
        tx = max(4, int(x0))
        ty = max(4, int(y0) - 22)
        bbox_text = draw.textbbox((tx, ty), text, font=FONT_SMALL)
        draw.rectangle(bbox_text, fill=color)
        draw.text((tx, ty), text, fill=(255, 255, 255), font=FONT_SMALL)
    image.save(out_path)
    return {
        "page_image": page_image.name,
        "layout_image": out_path.name,
        "box_counts": counts,
        "total_boxes": sum(counts.values()),
        "scale_x": 1,
        "scale_y": 1,
    }


def render_layout_assets(artifact_dir: Path, parsed: dict[str, Any]) -> list[dict[str, Any]]:
    report_assets = artifact_dir / "report_assets"
    pages_dir = report_assets / "pages"
    layout_dir = report_assets / "layout"
    ensure_dir(pages_dir)
    ensure_dir(layout_dir)

    page_images = render_input_pages(parsed, artifact_dir, pages_dir)
    results: list[dict[str, Any]] = []
    for idx, page_image in enumerate(page_images, start=1):
        out_path = layout_dir / f"page_{idx}_layout.png"
        mineru_json = artifact_dir / "mineru_raw" / f"page_{idx}_blocks.json"
        paddle_json = artifact_dir / "paddleocr_vl_raw" / f"page_{idx}_res.json"
        if mineru_json.exists():
            info = draw_mineru_overlay(page_image, mineru_json, out_path)
            info["page_index"] = idx
            results.append(info)
            continue
        if paddle_json.exists():
            info = draw_layout_overlay(page_image, paddle_json, out_path)
            info["page_index"] = idx
            results.append(info)
    return results


def render_full_text(parsed: dict[str, Any]) -> str:
    lines: list[str] = []
    for page in parsed.get("pages", []):
        lines.append(f"[{page['page_id']}]")
        for block in page.get("blocks", []):
            text = block.get("text") or ""
            if text:
                lines.append(text)
        lines.append("")
    return "\n".join(lines).strip()


def read_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    return load_json(path)


def read_text_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def load_table_views(artifact_dir: Path) -> list[dict[str, Any]]:
    table_index = read_json_if_exists(artifact_dir / "task_output" / "table_index.json") or []
    views: list[dict[str, Any]] = []
    for item in table_index:
        csv_rel = item.get("csv_path")
        if not csv_rel:
            continue
        csv_path = artifact_dir / "task_output" / csv_rel
        if not csv_path.exists():
            continue
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        headers = rows[0] if rows else []
        body = rows[1:] if len(rows) > 1 else []
        views.append(
            {
                "table_id": item.get("table_id"),
                "caption": item.get("caption"),
                "page_id": item.get("page_id"),
                "headers": headers,
                "rows": body,
                "row_count": len(body),
                "csv_path": csv_rel,
            }
        )
    return views


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render_field_preview(field: dict[str, Any]) -> str:
    label = escape_html(str(field.get("label") or "Field"))
    placeholder = escape_html(str(field.get("placeholder") or ""))
    width_class = "preview-field full" if field.get("width") == "full" else "preview-field"
    control = str(field.get("control") or "input")

    if control == "textarea":
        body = f"<textarea rows='4' placeholder='{placeholder}'></textarea>"
    elif control == "select":
        body = (
            f"<select><option value='' selected disabled>{placeholder or 'Select option'}</option></select>"
        )
    else:
        field_type = escape_html(str(field.get("field_type") or "text"))
        body = f"<input type='{field_type}' placeholder='{placeholder}' />"

    return f"<div class='{width_class}'><label>{label}</label>{body}</div>"


def render_preview_item(item: dict[str, Any]) -> str:
    kind = item.get("kind")
    if kind == "text":
        return f"<section class='preview-panel'><p>{escape_html(str(item.get('text') or ''))}</p></section>"
    if kind == "list":
        rows = "".join(f"<li>{escape_html(str(entry))}</li>" for entry in item.get("items", []))
        return f"<section class='preview-panel'><ul>{rows}</ul></section>"
    if kind == "table":
        headers = item.get("headers", [])
        rows = item.get("rows", [])
        header_html = "".join(f"<th>{escape_html(str(cell))}</th>" for cell in headers)
        body_html = "".join(
            "<tr>" + "".join(f"<td>{escape_html(str(cell))}</td>" for cell in row) + "</tr>"
            for row in rows[:8]
        )
        return (
            "<section class='preview-panel'>"
            f"<div class='preview-table-title'>{escape_html(str(item.get('title') or 'Table'))}</div>"
            "<div class='preview-table-wrap'><table>"
            f"<thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody>"
            "</table></div></section>"
        )
    if kind in {"figure", "chart", "formula"}:
        label = escape_html(str(item.get("text") or item.get("asset_path") or kind))
        return f"<section class='preview-panel placeholder'><strong>{escape_html(str(kind).upper())}</strong><p>{label}</p></section>"
    return f"<section class='preview-panel'><p>{escape_html(str(item))}</p></section>"


def render_blueprint_preview(blueprint: dict[str, Any]) -> str:
    profile = blueprint.get("document_profile", {})
    sections = blueprint.get("sections", [])
    navigation = blueprint.get("navigation", [])
    overview_cards = profile.get("overview_cards", [])
    source_snippets = profile.get("source_snippets", [])
    actions = profile.get("actions", [])

    nav_html = "".join(
        f"<a class='preview-nav-item' href='#{escape_html(str(item.get('id') or 'section'))}'><span>{escape_html(str(item.get('title') or 'Untitled'))}</span><small>{escape_html(str(item.get('kind') or 'mixed'))}</small></a>"
        for item in navigation
    )
    card_html = "".join(
        f"<div class='preview-stat'><span>{escape_html(str(card.get('label') or ''))}</span><strong>{escape_html(str(card.get('value') or ''))}</strong></div>"
        for card in overview_cards
    )
    action_html = "".join(
        f"<button class='preview-action{' primary' if idx == 0 else ''}' type='button'>{escape_html(str(action))}</button>"
        for idx, action in enumerate(actions)
    )

    section_html: list[str] = []
    for section in sections:
        fields = [item for item in section.get("items", []) if item.get("kind") == "field"]
        others = [item for item in section.get("items", []) if item.get("kind") != "field"]
        field_html = ""
        if fields:
            field_html = (
                "<section class='preview-panel'>"
                "<div class='preview-field-grid'>"
                + "".join(render_field_preview(field) for field in fields)
                + "</div></section>"
            )
        other_html = "".join(render_preview_item(item) for item in others)
        section_html.append(
            "<section class='preview-section' "
            f"id='{escape_html(str(section.get('id') or 'section'))}'>"
            f"<div class='preview-eyebrow'>{escape_html(str(section.get('kind') or 'mixed')).upper()}</div>"
            f"<h2>{escape_html(str(section.get('title') or 'Untitled Section'))}</h2>"
            f"{field_html}{other_html}</section>"
        )

    return f"""
<div class="preview-shell">
  <aside class="preview-sidebar">
    <section class="preview-panel hero">
      <div class="preview-eyebrow">{escape_html(str(profile.get("document_kind") or "mixed-app")).upper()}</div>
      <h1>{escape_html(str(blueprint.get("title") or "Generated App"))}</h1>
      <p>{escape_html(str(source_snippets[0] if source_snippets else "Generated from structured document parsing."))}</p>
    </section>
    <section class="preview-panel">
      <div class="preview-panel-label">Sections</div>
      <nav class="preview-nav">{nav_html}</nav>
    </section>
    <section class="preview-panel">
      <div class="preview-panel-label">Actions</div>
      <div class="preview-actions">{action_html}</div>
    </section>
  </aside>
  <main class="preview-main">
    <section class="preview-stats">{card_html}</section>
    {''.join(section_html)}
  </main>
</div>
"""


def load_code_artifacts(artifact_dir: Path) -> dict[str, Any] | None:
    task_dir = artifact_dir / "task_output"
    blueprint = read_json_if_exists(task_dir / "ui_blueprint.json")
    app_jsx = read_text_if_exists(task_dir / "app.jsx")
    index_html = read_text_if_exists(task_dir / "index.html")
    styles_css = read_text_if_exists(task_dir / "styles.css")
    schema_json = read_json_if_exists(task_dir / "schema.json")
    notebook_json = read_json_if_exists(task_dir / "notebook.ipynb")
    notebook_plan = read_json_if_exists(task_dir / "notebook_plan.json")
    field_schema = read_json_if_exists(task_dir / "field_schema.json")
    component_map = read_json_if_exists(task_dir / "component_map.json")

    if not any([blueprint, app_jsx, index_html, schema_json, notebook_json]):
        return None

    return {
        "blueprint": blueprint,
        "app_jsx": app_jsx,
        "index_html": index_html,
        "styles_css": styles_css,
        "schema_json": schema_json,
        "notebook_json": notebook_json,
        "notebook_plan": notebook_plan,
        "field_schema": field_schema,
        "component_map": component_map,
        "has_live_html": (task_dir / "index.html").exists(),
    }


def render_key_field_rows(key_fields: dict[str, Any]) -> str:
    rows = []
    for key, item in key_fields.items():
        if not item:
            continue
        rows.append(
            f"<tr><td>{escape_html(key)}</td><td>{escape_html(str(item.get('value', '')))}</td>"
            f"<td>{escape_html(str(item.get('normalized_value', '')))}</td></tr>"
        )
    return "\n".join(rows) or "<tr><td colspan='3'>No key fields extracted.</td></tr>"


def render_line_item_rows(line_items: list[dict[str, Any]]) -> str:
    rows = []
    for item in line_items:
        rows.append(
            "<tr>"
            f"<td>{escape_html(str(item.get('name', '')))}</td>"
            f"<td>{escape_html(str(item.get('quantity_text') or ''))}</td>"
            f"<td>{escape_html(str(item.get('amount') or item.get('amount_text') or ''))}</td>"
            f"<td>{escape_html(str(item.get('note') or ''))}</td>"
            "</tr>"
        )
    return "\n".join(rows) or "<tr><td colspan='4'>No line items extracted.</td></tr>"


def render_layout_section(layout_pages: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for item in layout_pages:
        counts = ", ".join(f"{escape_html(k)}: {v}" for k, v in sorted(item["box_counts"].items()))
        cards.append(
            "<section class='band'>"
            f"<h3>Page {item['page_index']}</h3>"
            f"<p class='muted'>Detected blocks: {item['total_boxes']} ({counts})</p>"
            f"<img class='layout-image' src='report_assets/layout/{item['layout_image']}' alt='Layout page {item['page_index']}' />"
            "</section>"
        )
    return "\n".join(cards) or "<section class='band'><p>No layout assets available.</p></section>"


def render_single_table(table_view: dict[str, Any]) -> str:
    headers = table_view.get("headers", [])
    rows = table_view.get("rows", [])
    header_html = "".join(f"<th>{escape_html(str(cell))}</th>" for cell in headers)
    if not header_html and rows:
        header_html = "".join(f"<th>Column {idx + 1}</th>" for idx in range(len(rows[0])))
    row_html: list[str] = []
    for row in rows:
        cells = "".join(f"<td>{escape_html(str(cell))}</td>" for cell in row)
        row_html.append(f"<tr>{cells}</tr>")
    body_html = "\n".join(row_html) or "<tr><td>No rows.</td></tr>"
    caption = escape_html(str(table_view.get("caption") or table_view.get("table_id") or "Table"))
    page_id = escape_html(str(table_view.get("page_id") or ""))
    csv_path = escape_html(str(table_view.get("csv_path") or ""))
    return (
        "<section class='band'>"
        f"<h3>{caption}</h3>"
        f"<p class='muted'>Page: {page_id} | Rows: {table_view.get('row_count', 0)} | CSV: {csv_path}</p>"
        "<div style='overflow:auto'>"
        "<table>"
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{body_html}</tbody>"
        "</table>"
        "</div>"
        "</section>"
    )


def render_medical_table_grouped(structured_record: dict[str, Any] | None) -> str:
    invoice = (structured_record or {}).get("invoice", {}) if structured_record else {}
    groups = invoice.get("category_groups", []) if isinstance(invoice, dict) else []
    if not groups:
        return ""
    sections: list[str] = []
    for group in groups:
        rows: list[str] = []
        for item in group.get("service_lines", []):
            rows.append(
                "<tr>"
                f"<td>{escape_html(str(item.get('name') or ''))}</td>"
                f"<td>{escape_html(str(item.get('quantity_text') or ''))}</td>"
                f"<td>{escape_html(str(item.get('amount') or item.get('amount_text') or ''))}</td>"
                "</tr>"
            )
        body = "\n".join(rows) or "<tr><td colspan='3'>No matched service lines.</td></tr>"
        sections.append(
            "<section class='band'>"
            f"<h3>{escape_html(str(group.get('category_name') or 'Category'))}</h3>"
            f"<p class='muted'>Category amount: {escape_html(str(group.get('category_amount') or ''))}</p>"
            "<table>"
            "<thead><tr><th>项目名称</th><th>数量/单位</th><th>金额</th></tr></thead>"
            f"<tbody>{body}</tbody>"
            "</table>"
            "</section>"
        )
    return "\n".join(sections)


def render_tables_section(table_views: list[dict[str, Any]], structured_record: dict[str, Any] | None) -> str:
    if not table_views:
        return ""
    grouped_medical = ""
    if (structured_record or {}).get("document_subtype") == "medical_invoice":
        grouped_medical = render_medical_table_grouped(structured_record)
    raw_tables = "\n".join(render_single_table(table_view) for table_view in table_views)
    return grouped_medical + raw_tables


def notebook_cell_source(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def render_notebook_preview(notebook_json: dict[str, Any] | None, notebook_plan: dict[str, Any] | None) -> str:
    if not notebook_json:
        return ""

    plan_section = ""
    if notebook_plan:
        outline_rows = "".join(
            f"<li><code>{escape_html(str(item))}</code></li>"
            for item in notebook_plan.get("outline", [])
        )
        plan_section = (
            "<section class='band'>"
            "<h2>Notebook Plan</h2>"
            "<div class='meta-grid'>"
            f"<div class='meta-item'><strong>Model ID</strong><div>{escape_html(str(notebook_plan.get('model_id') or ''))}</div></div>"
            f"<div class='meta-item'><strong>Document Kind</strong><div>{escape_html(str(notebook_plan.get('document_kind') or ''))}</div></div>"
            "</div>"
            "<div class='band' style='margin-top:16px;'>"
            "<h3>Inferred Outline</h3>"
            f"<ul>{outline_rows}</ul>"
            "</div>"
            "</section>"
        )

    cell_sections: list[str] = []
    for index, cell in enumerate(notebook_json.get("cells", []), start=1):
        cell_type = str(cell.get("cell_type") or "unknown")
        source = notebook_cell_source(cell)
        label = f"Cell {index} · {cell_type}"
        cell_sections.append(
            "<section class='band'>"
            f"<h3>{escape_html(label)}</h3>"
            f"<pre>{escape_html(source)}</pre>"
            "</section>"
        )

    return plan_section + "".join(cell_sections)


def render_code_artifacts_section(code_artifacts: dict[str, Any] | None, include_preview: bool = True) -> str:
    if not code_artifacts:
        return ""

    blueprint = code_artifacts.get("blueprint")
    field_schema = code_artifacts.get("field_schema") or []
    component_map = code_artifacts.get("component_map") or []
    schema_json = code_artifacts.get("schema_json")
    notebook_json = code_artifacts.get("notebook_json")
    notebook_plan = code_artifacts.get("notebook_plan")
    app_jsx = code_artifacts.get("app_jsx")
    index_html = code_artifacts.get("index_html")
    styles_css = code_artifacts.get("styles_css")
    has_live_html = bool(code_artifacts.get("has_live_html"))

    sections: list[str] = []

    if blueprint and include_preview:
        sections.append(
            "<section class='band'>"
            "<h2>Preview</h2>"
            "<p class='muted'>Static preview reconstructed from <code>ui_blueprint.json</code>.</p>"
            f"{render_blueprint_preview(blueprint)}"
            "</section>"
        )

    if notebook_json and include_preview:
        sections.append(render_notebook_preview(notebook_json, notebook_plan))

    if has_live_html and include_preview:
        sections.append(
            "<section class='band'>"
            "<h2>Live HTML Demo</h2>"
            "<p class='muted'>This embeds the generated <code>task_output/index.html</code> directly.</p>"
            "<div class='iframe-shell'>"
            "<iframe class='code-preview-frame' src='task_output/index.html' title='Generated HTML Demo'></iframe>"
            "</div>"
            "</section>"
        )

    summary_rows = [
        ("Fields", str(len(field_schema))),
        ("Components", str(len(component_map))),
        ("Has React Scaffold", "Yes" if app_jsx else "No"),
        ("Has HTML Scaffold", "Yes" if index_html else "No"),
        ("Has Notebook", "Yes" if notebook_json else "No"),
        ("Has JSON Schema", "Yes" if schema_json else "No"),
    ]
    summary_table = "".join(
        f"<tr><td>{escape_html(label)}</td><td>{escape_html(value)}</td></tr>" for label, value in summary_rows
    )
    sections.append(
        "<section class='band'>"
        "<h2>Generated Artifact Summary</h2>"
        "<table><tbody>"
        f"{summary_table}"
        "</tbody></table>"
        "</section>"
    )

    if app_jsx:
        sections.append(
            "<section class='band'>"
            "<h2>app.jsx</h2>"
            f"<pre>{escape_html(app_jsx)}</pre>"
            "</section>"
        )
    if index_html:
        sections.append(
            "<section class='band'>"
            "<h2>index.html</h2>"
            f"<pre>{escape_html(index_html)}</pre>"
            "</section>"
        )
    if styles_css:
        sections.append(
            "<section class='band'>"
            "<h2>styles.css</h2>"
            f"<pre>{escape_html(styles_css)}</pre>"
            "</section>"
        )
    if schema_json is not None:
        sections.append(
            "<section class='band'>"
            "<h2>schema.json</h2>"
            f"<pre>{escape_html(json.dumps(schema_json, ensure_ascii=False, indent=2))}</pre>"
            "</section>"
        )
    if notebook_json is not None:
        sections.append(
            "<section class='band'>"
            "<h2>notebook.ipynb</h2>"
            f"<pre>{escape_html(json.dumps(notebook_json, ensure_ascii=False, indent=2))}</pre>"
            "</section>"
        )
    if notebook_plan is not None:
        sections.append(
            "<section class='band'>"
            "<h2>notebook_plan.json</h2>"
            f"<pre>{escape_html(json.dumps(notebook_plan, ensure_ascii=False, indent=2))}</pre>"
            "</section>"
        )

    return "".join(sections)


def build_code_preview_html(artifact_dir: Path, code_artifacts: dict[str, Any]) -> str:
    blueprint = code_artifacts.get("blueprint")
    notebook_json = code_artifacts.get("notebook_json")
    notebook_plan = code_artifacts.get("notebook_plan")
    title = "Generated Code Preview"
    if blueprint:
        title = str(blueprint.get("title") or title)
    elif notebook_plan:
        title = str(notebook_plan.get("title") or title)

    live_html = ""
    if code_artifacts.get("has_live_html"):
        live_html = (
            "<section class='preview-band'>"
            "<h2>Live HTML Demo</h2>"
            "<div class='iframe-shell'>"
            "<iframe class='code-preview-frame' src='task_output/index.html' title='Generated HTML Demo'></iframe>"
            "</div></section>"
        )

    if notebook_json:
        static_preview = render_notebook_preview(notebook_json, notebook_plan)
    else:
        static_preview = render_blueprint_preview(blueprint) if blueprint else "<p>No blueprint available.</p>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape_html(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #eef4fb;
      --panel: #ffffff;
      --ink: #0f172a;
      --muted: #64748b;
      --line: #d8dee9;
      --accent: #2563eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: "Segoe UI", "Microsoft YaHei", sans-serif; }}
    header {{ padding: 28px 32px 16px; }}
    .shell {{ max-width: 1440px; margin: 0 auto; padding: 0 32px 32px; }}
    .preview-band {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
    .preview-shell {{ display: grid; gap: 24px; grid-template-columns: 280px minmax(0, 1fr); }}
    .preview-sidebar, .preview-main {{ display: grid; gap: 20px; align-content: start; }}
    .preview-panel, .preview-stat {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 12px 40px rgba(15, 23, 42, 0.06); }}
    .preview-panel {{ padding: 18px; }}
    .preview-panel.hero h1 {{ margin: 0 0 10px; font-size: 28px; line-height: 1.2; }}
    .preview-panel.hero p, .preview-panel p, .preview-panel li {{ color: var(--muted); line-height: 1.7; }}
    .preview-eyebrow, .preview-panel-label {{ font-size: 12px; font-weight: 700; color: var(--accent); margin-bottom: 10px; }}
    .preview-panel-label {{ color: var(--muted); }}
    .preview-nav, .preview-actions {{ display: grid; gap: 10px; }}
    .preview-nav-item {{ text-decoration: none; color: var(--ink); padding: 10px 12px; border-radius: 8px; background: #f8fafc; border: 1px solid #e2e8f0; display: grid; gap: 4px; }}
    .preview-nav-item span {{ font-weight: 600; }}
    .preview-nav-item small {{ color: var(--muted); }}
    .preview-actions {{ grid-template-columns: 1fr; }}
    .preview-action {{ border: 1px solid #cbd5e1; background: #fff; color: var(--ink); border-radius: 8px; padding: 11px 14px; font-weight: 600; }}
    .preview-action.primary {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .preview-stats {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }}
    .preview-stat {{ padding: 16px; min-height: 96px; display: grid; gap: 8px; align-content: start; }}
    .preview-stat span {{ font-size: 12px; color: var(--muted); }}
    .preview-stat strong {{ font-size: 22px; }}
    .preview-section {{ display: grid; gap: 16px; }}
    .preview-section h2 {{ margin: 0; font-size: 24px; }}
    .preview-field-grid {{ display: grid; gap: 16px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .preview-field {{ display: grid; gap: 8px; }}
    .preview-field.full {{ grid-column: 1 / -1; }}
    .preview-field label {{ font-size: 14px; font-weight: 600; color: #1e293b; }}
    .preview-field input, .preview-field textarea, .preview-field select {{ width: 100%; padding: 11px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font: inherit; }}
    .preview-table-title {{ font-weight: 600; margin-bottom: 12px; }}
    .preview-table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 12px 16px; border-bottom: 1px solid #eef2f7; vertical-align: top; }}
    th {{ font-size: 13px; color: #475569; background: #f8fafc; }}
    .placeholder strong {{ display: block; margin-bottom: 8px; color: var(--muted); font-size: 12px; }}
    .iframe-shell {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; }}
    .code-preview-frame {{ display: block; width: 100%; height: 880px; border: 0; background: #fff; }}
    @media (max-width: 1024px) {{
      .shell {{ padding-left: 16px; padding-right: 16px; }}
      header {{ padding-left: 16px; padding-right: 16px; }}
      .preview-shell {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 720px) {{
      .preview-field-grid {{ grid-template-columns: 1fr; }}
      .preview-field.full {{ grid-column: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="shell">
      <h1>{escape_html(title)}</h1>
      <p class="muted">Artifact: {escape_html(str(artifact_dir.name))}</p>
    </div>
  </header>
  <div class="shell">
    <section class="preview-band">
      <h2>Static Preview</h2>
      <p class="muted">This view is reconstructed from the generated blueprint and can be opened directly as a local file.</p>
      {static_preview}
    </section>
    {live_html}
  </div>
</body>
</html>"""

def render_source_pages_section(artifact_dir: Path, parsed: dict[str, Any]) -> str:
    pages_dir = artifact_dir / "report_assets" / "pages"
    if not pages_dir.exists():
        return "<section class='band'><p>No source preview available.</p></section>"

    cards: list[str] = []
    page_images = sorted(pages_dir.iterdir()) if pages_dir.exists() else []
    for index, path in enumerate(page_images, start=1):
        rel = f"report_assets/pages/{path.name}"
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            body = f"<iframe class='source-preview-frame' src='{escape_html(rel)}' title='Source PDF {index}'></iframe>"
        else:
            body = f"<img class='layout-image' src='{escape_html(rel)}' alt='Source page {index}' />"
        cards.append(
            "<section class='band'>"
            f"<h3>Source Page {index}</h3>"
            f"{body}"
            "</section>"
        )
    return "\n".join(cards) or "<section class='band'><p>No source preview available.</p></section>"


def render_parse_summary_section(parsed: dict[str, Any], code_artifacts: dict[str, Any] | None) -> str:
    block_counts: dict[str, int] = {}
    for page in parsed.get("pages", []):
        for block in page.get("blocks", []):
            block_type = str(block.get("type") or "unknown")
            block_counts[block_type] = block_counts.get(block_type, 0) + 1

    count_rows = "".join(
        f"<tr><td>{escape_html(key)}</td><td>{value}</td></tr>"
        for key, value in sorted(block_counts.items())
    ) or "<tr><td colspan='2'>No blocks found.</td></tr>"

    blueprint = (code_artifacts or {}).get("blueprint") or {}
    profile = blueprint.get("document_profile", {})
    section_rows = "".join(
        "<tr>"
        f"<td>{escape_html(str(item.get('title') or 'Untitled'))}</td>"
        f"<td>{escape_html(str(item.get('kind') or 'mixed'))}</td>"
        f"<td>{escape_html(str(item.get('item_count') or 0))}</td>"
        "</tr>"
        for item in profile.get("section_summaries", [])
    ) or "<tr><td colspan='3'>No inferred sections.</td></tr>"

    return (
        "<section class='band'>"
        "<h2>Parse Summary</h2>"
        "<table><thead><tr><th>Block Type</th><th>Count</th></tr></thead>"
        f"<tbody>{count_rows}</tbody></table>"
        "</section>"
        "<section class='band'>"
        "<h2>Inferred UI Structure</h2>"
        "<table><thead><tr><th>Section</th><th>Kind</th><th>Items</th></tr></thead>"
        f"<tbody>{section_rows}</tbody></table>"
        "</section>"
    )


def build_data_html(
    parsed: dict[str, Any],
    normalized: dict[str, Any] | None,
    structured_record: dict[str, Any] | None,
    layout_pages: list[dict[str, Any]],
    table_views: list[dict[str, Any]],
    code_artifacts: dict[str, Any] | None,
) -> str:
    profile = (normalized or {}).get("document_profile", {})
    classification = profile.get("classification", {})
    key_fields = (structured_record or {}).get("key_fields", {})
    line_items = (structured_record or {}).get("line_items", [])
    invoice = (structured_record or {}).get("invoice", {})
    full_text = render_full_text(parsed)
    parsed_json_pretty = json.dumps(parsed, ensure_ascii=False, indent=2)
    normalized_pretty = json.dumps(normalized or {}, ensure_ascii=False, indent=2)
    structured_pretty = json.dumps(structured_record or {}, ensure_ascii=False, indent=2)
    payment_breakdown = invoice.get("payment_breakdown", {}) if isinstance(invoice, dict) else {}
    payment_rows = render_key_field_rows(payment_breakdown)

    code_tab_button = "<button data-tab='code'>Code Preview</button>" if code_artifacts else ""
    code_tab_section = (
        "<section class='tab' id='code'>" + render_code_artifacts_section(code_artifacts) + "</section>"
        if code_artifacts
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape_html(str(parsed.get("document_id") or "Document Report"))}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7fb;
      --panel: #ffffff;
      --ink: #141824;
      --muted: #5f6780;
      --line: #d9deeb;
      --accent: #1967d2;
      --accent-soft: #e8f0fe;
      --ok: #1e8e3e;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: "Segoe UI", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--ink); }}
    header {{ padding: 28px 32px 20px; background: var(--panel); border-bottom: 1px solid var(--line); }}
    h1, h2, h3 {{ margin: 0 0 10px; }}
    .muted {{ color: var(--muted); }}
    .shell {{ max-width: 1400px; margin: 0 auto; }}
    .top-grid {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; padding: 24px 32px; }}
    .band {{ background: var(--panel); padding: 20px; border: 1px solid var(--line); border-radius: 8px; margin-bottom: 20px; }}
    .pills {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }}
    .pill {{ display: inline-flex; align-items: center; min-height: 32px; padding: 0 12px; background: var(--accent-soft); color: var(--accent); border-radius: 999px; font-size: 14px; }}
    .nav {{ display: flex; gap: 8px; padding: 0 32px 16px; flex-wrap: wrap; }}
    .nav button {{ border: 1px solid var(--line); background: var(--panel); color: var(--ink); padding: 10px 14px; border-radius: 8px; cursor: pointer; }}
    .nav button.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .tab {{ display: none; padding: 0 32px 32px; }}
    .tab.active {{ display: block; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .meta-item {{ padding: 14px; background: #fbfcff; border: 1px solid var(--line); border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid var(--line); text-align: left; padding: 10px 12px; vertical-align: top; }}
    th {{ color: var(--muted); font-weight: 600; background: #fbfcff; }}
    pre {{ margin: 0; white-space: pre-wrap; word-break: break-word; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5; }}
    .layout-image {{ width: 100%; height: auto; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
    .json-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }}
    .preview-shell {{ display: grid; gap: 24px; grid-template-columns: 280px minmax(0, 1fr); }}
    .preview-sidebar, .preview-main {{ display: grid; gap: 20px; align-content: start; }}
    .preview-panel, .preview-stat {{ background: #ffffff; border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 12px 40px rgba(15, 23, 42, 0.06); }}
    .preview-panel {{ padding: 18px; }}
    .preview-panel.hero h1 {{ margin: 0 0 10px; font-size: 28px; line-height: 1.2; }}
    .preview-panel.hero p, .preview-panel p, .preview-panel li {{ color: var(--muted); line-height: 1.7; }}
    .preview-eyebrow, .preview-panel-label {{ font-size: 12px; font-weight: 700; color: var(--accent); margin-bottom: 10px; }}
    .preview-panel-label {{ color: var(--muted); }}
    .preview-nav, .preview-actions {{ display: grid; gap: 10px; }}
    .preview-nav-item {{ text-decoration: none; color: var(--ink); padding: 10px 12px; border-radius: 8px; background: #f8fafc; border: 1px solid #e2e8f0; display: grid; gap: 4px; }}
    .preview-nav-item span {{ font-weight: 600; }}
    .preview-nav-item small {{ color: var(--muted); }}
    .preview-action {{ border: 1px solid #cbd5e1; background: #fff; color: var(--ink); border-radius: 8px; padding: 11px 14px; font-weight: 600; }}
    .preview-action.primary {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .preview-stats {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }}
    .preview-stat {{ padding: 16px; min-height: 96px; display: grid; gap: 8px; align-content: start; }}
    .preview-stat span {{ font-size: 12px; color: var(--muted); }}
    .preview-stat strong {{ font-size: 22px; }}
    .preview-section {{ display: grid; gap: 16px; }}
    .preview-section h2 {{ margin: 0; font-size: 24px; }}
    .preview-field-grid {{ display: grid; gap: 16px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .preview-field {{ display: grid; gap: 8px; }}
    .preview-field.full {{ grid-column: 1 / -1; }}
    .preview-field label {{ font-size: 14px; font-weight: 600; color: #1e293b; }}
    .preview-field input, .preview-field textarea, .preview-field select {{ width: 100%; padding: 11px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font: inherit; }}
    .preview-table-title {{ font-weight: 600; margin-bottom: 12px; }}
    .preview-table-wrap {{ overflow-x: auto; }}
    .placeholder strong {{ display: block; margin-bottom: 8px; color: var(--muted); font-size: 12px; }}
    .iframe-shell {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; }}
    .code-preview-frame {{ display: block; width: 100%; height: 880px; border: 0; background: #fff; }}
    @media (max-width: 960px) {{
      .top-grid, .json-grid, .meta-grid, .preview-shell {{ grid-template-columns: 1fr; }}
      header, .top-grid, .nav, .tab {{ padding-left: 16px; padding-right: 16px; }}
    }}
    @media (max-width: 720px) {{
      .preview-field-grid {{ grid-template-columns: 1fr; }}
      .preview-field.full {{ grid-column: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="shell">
      <h1>{escape_html(str(parsed.get("source", {}).get("filename", "Document")))}</h1>
      <p class="muted">{escape_html(str(parsed.get("source", {}).get("input_path", "")))}</p>
      <div class="pills">
        <span class="pill">Category: {escape_html(str(classification.get("document_category") or profile.get("document_type") or "unknown"))}</span>
        <span class="pill">Subtype: {escape_html(str(classification.get("document_subtype") or profile.get("document_subtype") or "n/a"))}</span>
        <span class="pill">Backend: {escape_html(str(parsed.get("parse_info", {}).get("backend", "unknown")))}</span>
        <span class="pill">Pages: {len(parsed.get("pages", []))}</span>
      </div>
    </div>
  </header>
  <div class="shell">
    <div class="top-grid">
      <section class="band">
        <h2>Classification</h2>
        <div class="meta-grid">
          <div class="meta-item"><strong>Title</strong><div>{escape_html(str((normalized or {}).get("summary", {}).get("title", "")))}</div></div>
          <div class="meta-item"><strong>Evidence</strong><div>{escape_html("; ".join(classification.get("evidence", [])))}</div></div>
          <div class="meta-item"><strong>Page Count</strong><div>{len(parsed.get("pages", []))}</div></div>
          <div class="meta-item"><strong>Line Items</strong><div>{len(line_items)}</div></div>
        </div>
      </section>
      <section class="band">
        <h2>Key Fields</h2>
        <table>
          <thead><tr><th>Field</th><th>Value</th><th>Normalized</th></tr></thead>
          <tbody>{render_key_field_rows(key_fields)}</tbody>
        </table>
      </section>
    </div>
    <div class="nav">
      <button class="active" data-tab="layout">Layout</button>
      <button data-tab="text">Full Text</button>
      <button data-tab="structured">Structured</button>
      {code_tab_button}
      <button data-tab="json">JSON</button>
      {"<button data-tab='table'>Table</button>" if table_views else ""}
    </div>
    <section class="tab active" id="layout">
      {render_layout_section(layout_pages)}
    </section>
    <section class="tab" id="text">
      <section class="band">
        <h2>Extracted Text</h2>
        <pre>{escape_html(full_text)}</pre>
      </section>
    </section>
    <section class="tab" id="structured">
      <section class="band">
        <h2>Structured Record</h2>
        <pre>{escape_html(structured_pretty)}</pre>
      </section>
      <section class="band">
        <h2>Invoice Line Items</h2>
        <table>
          <thead><tr><th>Name</th><th>Quantity</th><th>Amount</th><th>Note</th></tr></thead>
          <tbody>{render_line_item_rows(line_items)}</tbody>
        </table>
      </section>
      <section class="band">
        <h2>Payment Breakdown</h2>
        <table>
          <thead><tr><th>Field</th><th>Value</th><th>Normalized</th></tr></thead>
          <tbody>{payment_rows}</tbody>
        </table>
      </section>
    </section>
    {code_tab_section}
    <section class="tab" id="json">
      <div class="json-grid">
        <section class="band"><h2>parsed.json</h2><pre>{escape_html(parsed_json_pretty)}</pre></section>
        <section class="band"><h2>normalized.json</h2><pre>{escape_html(normalized_pretty)}</pre></section>
      </div>
    </section>
    {"<section class='tab' id='table'>" + render_tables_section(table_views, structured_record) + "</section>" if table_views else ""}
  </div>
  <script>
    const buttons = document.querySelectorAll('.nav button');
    const tabs = document.querySelectorAll('.tab');
    for (const button of buttons) {{
      button.addEventListener('click', () => {{
        for (const b of buttons) b.classList.remove('active');
        for (const tab of tabs) tab.classList.remove('active');
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');
      }});
    }}
  </script>
</body>
</html>"""


def build_code_html(
    artifact_dir: Path,
    parsed: dict[str, Any],
    code_artifacts: dict[str, Any] | None,
) -> str:
    parsed_json_pretty = json.dumps(parsed, ensure_ascii=False, indent=2)
    blueprint = (code_artifacts or {}).get("blueprint")
    component_map = (code_artifacts or {}).get("component_map") or []
    field_schema = (code_artifacts or {}).get("field_schema") or []
    component_map_pretty = json.dumps(component_map, ensure_ascii=False, indent=2)
    field_schema_pretty = json.dumps(field_schema, ensure_ascii=False, indent=2)
    blueprint_pretty = json.dumps(blueprint or {}, ensure_ascii=False, indent=2)
    full_text = render_full_text(parsed)
    code_preview_path = "code_preview.html" if (artifact_dir / "code_preview.html").exists() else None

    preview_tab = render_code_artifacts_section(code_artifacts, include_preview=True)
    source_tab = render_source_pages_section(artifact_dir, parsed)
    parse_tab = (
        "<section class='band'><h2>Extracted Text</h2>"
        f"<pre>{escape_html(full_text)}</pre></section>"
        + render_parse_summary_section(parsed, code_artifacts)
    )
    json_tab = (
        "<div class='json-grid'>"
        f"<section class='band'><h2>parsed.json</h2><pre>{escape_html(parsed_json_pretty)}</pre></section>"
        f"<section class='band'><h2>ui_blueprint.json</h2><pre>{escape_html(blueprint_pretty)}</pre></section>"
        "</div>"
        "<div class='json-grid'>"
        f"<section class='band'><h2>field_schema.json</h2><pre>{escape_html(field_schema_pretty)}</pre></section>"
        f"<section class='band'><h2>component_map.json</h2><pre>{escape_html(component_map_pretty)}</pre></section>"
        "</div>"
    )

    open_preview_link = (
        f"<a class='link-button' href='{escape_html(code_preview_path)}' target='_blank' rel='noreferrer'>Open Standalone Preview</a>"
        if code_preview_path
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape_html(str(parsed.get("document_id") or "Code Generation Report"))}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7fb;
      --panel: #ffffff;
      --ink: #141824;
      --muted: #5f6780;
      --line: #d9deeb;
      --accent: #1967d2;
      --accent-soft: #e8f0fe;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: "Segoe UI", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--ink); }}
    header {{ padding: 28px 32px 20px; background: var(--panel); border-bottom: 1px solid var(--line); }}
    h1, h2, h3 {{ margin: 0 0 10px; }}
    .muted {{ color: var(--muted); }}
    .shell {{ max-width: 1400px; margin: 0 auto; }}
    .top-grid {{ display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; padding: 24px 32px; }}
    .band {{ background: var(--panel); padding: 20px; border: 1px solid var(--line); border-radius: 8px; margin-bottom: 20px; }}
    .pills {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }}
    .pill {{ display: inline-flex; align-items: center; min-height: 32px; padding: 0 12px; background: var(--accent-soft); color: var(--accent); border-radius: 999px; font-size: 14px; }}
    .nav {{ display: flex; gap: 8px; padding: 0 32px 16px; flex-wrap: wrap; }}
    .nav button {{ border: 1px solid var(--line); background: var(--panel); color: var(--ink); padding: 10px 14px; border-radius: 8px; cursor: pointer; }}
    .nav button.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .tab {{ display: none; padding: 0 32px 32px; }}
    .tab.active {{ display: block; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .meta-item {{ padding: 14px; background: #fbfcff; border: 1px solid var(--line); border-radius: 8px; }}
    .link-button {{ display: inline-flex; align-items: center; min-height: 40px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--accent); color: #fff; background: var(--accent); text-decoration: none; font-weight: 600; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid var(--line); text-align: left; padding: 10px 12px; vertical-align: top; }}
    th {{ color: var(--muted); font-weight: 600; background: #fbfcff; }}
    pre {{ margin: 0; white-space: pre-wrap; word-break: break-word; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5; }}
    .layout-image {{ width: 100%; height: auto; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
    .source-preview-frame {{ width: 100%; min-height: 720px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
    .json-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-bottom: 20px; }}
    .preview-shell {{ display: grid; gap: 24px; grid-template-columns: 280px minmax(0, 1fr); }}
    .preview-sidebar, .preview-main {{ display: grid; gap: 20px; align-content: start; }}
    .preview-panel, .preview-stat {{ background: #ffffff; border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 12px 40px rgba(15, 23, 42, 0.06); }}
    .preview-panel {{ padding: 18px; }}
    .preview-panel.hero h1 {{ margin: 0 0 10px; font-size: 28px; line-height: 1.2; }}
    .preview-panel.hero p, .preview-panel p, .preview-panel li {{ color: var(--muted); line-height: 1.7; }}
    .preview-eyebrow, .preview-panel-label {{ font-size: 12px; font-weight: 700; color: var(--accent); margin-bottom: 10px; }}
    .preview-panel-label {{ color: var(--muted); }}
    .preview-nav, .preview-actions {{ display: grid; gap: 10px; }}
    .preview-nav-item {{ text-decoration: none; color: var(--ink); padding: 10px 12px; border-radius: 8px; background: #f8fafc; border: 1px solid #e2e8f0; display: grid; gap: 4px; }}
    .preview-nav-item span {{ font-weight: 600; }}
    .preview-nav-item small {{ color: var(--muted); }}
    .preview-action {{ border: 1px solid #cbd5e1; background: #fff; color: var(--ink); border-radius: 8px; padding: 11px 14px; font-weight: 600; }}
    .preview-action.primary {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    .preview-stats {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }}
    .preview-stat {{ padding: 16px; min-height: 96px; display: grid; gap: 8px; align-content: start; }}
    .preview-stat span {{ font-size: 12px; color: var(--muted); }}
    .preview-stat strong {{ font-size: 22px; }}
    .preview-section {{ display: grid; gap: 16px; }}
    .preview-section h2 {{ margin: 0; font-size: 24px; }}
    .preview-field-grid {{ display: grid; gap: 16px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .preview-field {{ display: grid; gap: 8px; }}
    .preview-field.full {{ grid-column: 1 / -1; }}
    .preview-field label {{ font-size: 14px; font-weight: 600; color: #1e293b; }}
    .preview-field input, .preview-field textarea, .preview-field select {{ width: 100%; padding: 11px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font: inherit; }}
    .preview-table-title {{ font-weight: 600; margin-bottom: 12px; }}
    .preview-table-wrap {{ overflow-x: auto; }}
    .placeholder strong {{ display: block; margin-bottom: 8px; color: var(--muted); font-size: 12px; }}
    .iframe-shell {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; }}
    .code-preview-frame {{ display: block; width: 100%; height: 880px; border: 0; background: #fff; }}
    @media (max-width: 960px) {{
      .top-grid, .json-grid, .meta-grid, .preview-shell {{ grid-template-columns: 1fr; }}
      header, .top-grid, .nav, .tab {{ padding-left: 16px; padding-right: 16px; }}
    }}
    @media (max-width: 720px) {{
      .preview-field-grid {{ grid-template-columns: 1fr; }}
      .preview-field.full {{ grid-column: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="shell">
      <h1>{escape_html(str(parsed.get("source", {}).get("filename", "Document")))}</h1>
      <p class="muted">{escape_html(str(parsed.get("source", {}).get("input_path", "")))}</p>
      <div class="pills">
        <span class="pill">Mode: to-code</span>
        <span class="pill">Backend: {escape_html(str(parsed.get("parse_info", {}).get("backend", "unknown")))}</span>
        <span class="pill">Pages: {len(parsed.get("pages", []))}</span>
        <span class="pill">Fields: {len(field_schema)}</span>
      </div>
    </div>
  </header>
  <div class="shell">
    <div class="top-grid">
      <section class="band">
        <h2>Workflow</h2>
        <div class="meta-grid">
          <div class="meta-item"><strong>Step 1</strong><div>Parse image or document into structured blocks.</div></div>
          <div class="meta-item"><strong>Step 2</strong><div>Infer page structure, sections, and form fields.</div></div>
          <div class="meta-item"><strong>Step 3</strong><div>Generate scaffold code and preview artifacts.</div></div>
          <div class="meta-item"><strong>Result</strong><div>Open the generated code preview or inspect the emitted files.</div></div>
        </div>
      </section>
      <section class="band">
        <h2>Output</h2>
        <table>
          <tbody>
            <tr><td>Sections</td><td>{len((blueprint or {}).get("sections", []))}</td></tr>
            <tr><td>Fields</td><td>{len(field_schema)}</td></tr>
            <tr><td>Components</td><td>{len(component_map)}</td></tr>
            <tr><td>Standalone Preview</td><td>{open_preview_link or "Not available"}</td></tr>
          </tbody>
        </table>
      </section>
    </div>
    <div class="nav">
      <button class="active" data-tab="source">Source</button>
      <button data-tab="parse">Parse</button>
      <button data-tab="preview">Generated App</button>
      <button data-tab="artifacts">Code</button>
      <button data-tab="json">JSON</button>
    </div>
    <section class="tab active" id="source">
      {source_tab}
    </section>
    <section class="tab" id="parse">
      {parse_tab}
    </section>
    <section class="tab" id="preview">
      {preview_tab}
    </section>
    <section class="tab" id="artifacts">
      {render_code_artifacts_section(code_artifacts, include_preview=False)}
    </section>
    <section class="tab" id="json">
      {json_tab}
    </section>
  </div>
  <script>
    const buttons = document.querySelectorAll('.nav button');
    const tabs = document.querySelectorAll('.tab');
    for (const button of buttons) {{
      button.addEventListener('click', () => {{
        for (const b of buttons) b.classList.remove('active');
        for (const tab of tabs) tab.classList.remove('active');
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');
      }});
    }}
  </script>
</body>
</html>"""


def main() -> int:
    args = parse_args()
    artifact_dir = Path(args.artifact_dir).expanduser().resolve()
    parsed = load_json(artifact_dir / "parsed.json")
    normalized = read_json_if_exists(artifact_dir / "task_output" / "normalized.json")
    structured_record = read_json_if_exists(artifact_dir / "task_output" / "structured_record.json")
    code_artifacts = load_code_artifacts(artifact_dir)
    effective_config = read_json_if_exists(artifact_dir / "effective_config.json") or {}
    mode = str(effective_config.get("mode") or parsed.get("parse_info", {}).get("mode") or "parse")
    layout_pages = render_layout_assets(artifact_dir, parsed)
    table_views = load_table_views(artifact_dir)
    if mode == "to-code":
        html = build_code_html(artifact_dir, parsed, code_artifacts)
    else:
        html = build_data_html(parsed, normalized, structured_record, layout_pages, table_views, code_artifacts)
    out_path = artifact_dir / "result_report.html"
    out_path.write_text(html, encoding="utf-8")
    code_preview_path: Path | None = None
    if code_artifacts:
        code_preview_path = artifact_dir / "code_preview.html"
        code_preview_path.write_text(
            build_code_preview_html(artifact_dir, code_artifacts),
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "ok": True,
                "artifact_dir": str(artifact_dir),
                "report_html": str(out_path),
                "code_preview_html": str(code_preview_path) if code_preview_path else None,
                "layout_pages": len(layout_pages),
                "layout_assets_dir": str(artifact_dir / "report_assets" / "layout"),
                "table_views": len(table_views),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
