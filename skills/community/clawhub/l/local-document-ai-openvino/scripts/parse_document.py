#!/usr/bin/env python3
"""
parse_document.py

CLI contract for local document parsing.

Primary runtime path:
1. Resolve a local MinerU 2.5 OpenVINO model bundle
2. Parse a PDF or image with OpenVINO GenAI
3. Normalize the result into the canonical schema
4. Write parsed.json and parsed.md
5. Print a concise JSON status message to stdout

When the MinerU runtime is unavailable, the script falls back to lightweight
contract/smoke parsing so the skill can still validate its artifact flow.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _local_vendor import bootstrap_local_vendor
from utils import (
    build_parse_status,
    detect_input_type,
    ensure_artifact_layout,
    make_document_id,
    now_iso,
    sha256_file,
    validate_document_schema,
    write_error,
    write_json,
    write_text,
)


bootstrap_local_vendor()


MINERU_REQUIRED_MODEL_FILES = (
    "openvino_language_model.xml",
    "openvino_vision_embeddings_model.xml",
    "openvino_tokenizer.xml",
    "openvino_detokenizer.xml",
)


@dataclass
class ParseConfig:
    file: Path
    out: Path
    mode: str = "parse"
    engine_version: str = "mineru2.5-openvino"
    save_figures: bool = True
    save_tables: bool = True
    max_pages: int | None = None
    language_hint: str | None = None
    debug: bool = False


def parse_args() -> ParseConfig:
    parser = argparse.ArgumentParser(
        description="Parse a PDF or image into canonical document JSON/Markdown."
    )
    parser.add_argument("--file", required=True, help="Input PDF or image path")
    parser.add_argument("--out", required=True, help="Output artifact directory")
    parser.add_argument(
        "--mode",
        default="parse",
        choices=["parse", "to-code", "to-data"],
    )
    parser.add_argument("--engine-version", default="mineru2.5-openvino")
    parser.add_argument("--save-figures", action="store_true", default=True)
    parser.add_argument("--save-tables", action="store_true", default=True)
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--language-hint")
    parser.add_argument("--debug", action="store_true")

    ns = parser.parse_args()

    return ParseConfig(
        file=Path(ns.file).expanduser().resolve(),
        out=Path(ns.out).expanduser().resolve(),
        mode=ns.mode,
        engine_version=ns.engine_version,
        save_figures=ns.save_figures,
        save_tables=ns.save_tables,
        max_pages=ns.max_pages,
        language_hint=ns.language_hint,
        debug=ns.debug,
    )


def build_empty_document(config: ParseConfig, input_type: str, file_hash: str) -> dict[str, Any]:
    document_id = make_document_id(config.file, file_hash)
    return {
        "schema_version": "1.0",
        "document_id": document_id,
        "source": {
            "input_path": str(config.file),
            "input_type": input_type,
            "filename": config.file.name,
            "sha256": file_hash,
        },
        "parse_info": {
            "engine": "local-document-ai-openvino",
            "engine_version": config.engine_version,
            "mode": config.mode,
            "created_at": now_iso(),
            "warnings": [],
            "confidence_note": None,
        },
        "pages": [],
        "tables": [],
        "figures": [],
        "entities": [],
        "outputs": {
            "parsed_markdown_path": "parsed.md",
            "task_outputs": [],
        },
    }


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def make_block(
    page_index: int,
    block_index: int,
    block_type: str,
    text: str,
    bbox: list[float] | None = None,
    confidence: float = 0.75,
    language: str = "unknown",
) -> dict[str, Any]:
    heading_level = 1 if block_type == "heading" else None
    markdown = f"# {text}" if block_type == "heading" and text else text
    return {
        "block_id": f"p{page_index}_b{block_index}",
        "type": block_type,
        "bbox": bbox or [0, 0, 0, 0],
        "reading_order": block_index,
        "text": text,
        "markdown": markdown,
        "latex": None,
        "html": None,
        "confidence": confidence,
        "attributes": {
            "heading_level": heading_level,
            "language": language,
            "is_rotated": False,
        },
        "relations": {
            "parent_block_id": None,
            "caption_for": None,
            "table_id": None,
            "figure_id": None,
        },
    }


def classify_line(line: str, is_first_content: bool) -> str:
    clean = line.strip()
    if is_first_content and clean:
        return "heading"
    if re.match(r"^[A-Za-z\u4e00-\u9fff][A-Za-z0-9\u4e00-\u9fff /&()_#-]{1,80}[:：]\s*.*$", clean):
        return "kv_pair"
    if clean.startswith(("- ", "* ", "+ ")):
        return "list"
    return "paragraph"


def page_from_lines(
    page_index: int,
    lines: list[str],
    width: float = 0,
    height: float = 0,
    language: str = "unknown",
    confidence: float = 0.75,
) -> dict[str, Any]:
    blocks: list[dict[str, Any]] = []
    first_content = True
    for line in lines:
        clean = " ".join(line.split())
        if not clean:
            continue
        block_type = classify_line(clean, first_content)
        blocks.append(
            make_block(
                page_index=page_index,
                block_index=len(blocks) + 1,
                block_type=block_type,
                text=clean,
                confidence=confidence,
                language=language,
            )
        )
        first_content = False

    if not blocks:
        blocks.append(
            make_block(
                page_index=page_index,
                block_index=1,
                block_type="unknown",
                text="",
                confidence=0.0,
                language=language,
            )
        )

    return {
        "page_id": f"page_{page_index}",
        "page_index": page_index,
        "width": width,
        "height": height,
        "blocks": blocks,
    }


def decode_text_file(file_path: Path) -> str | None:
    data = file_path.read_bytes()
    if not data:
        return ""

    for encoding in ("utf-8-sig", "utf-8", "utf-16", "latin-1"):
        try:
            text = data.decode(encoding)
        except UnicodeDecodeError:
            continue
        printable = sum(1 for char in text if char.isprintable() or char.isspace())
        if printable / max(len(text), 1) >= 0.85:
            return text
    return None


def parse_text_like_file(config: ParseConfig, warning: str | None = None) -> dict[str, Any]:
    text = decode_text_file(config.file)
    warnings = []
    if warning:
        warnings.append(warning)
    if text is None:
        text = ""
        warnings.append("Could not decode file as text; no local parser backend extracted content.")

    lines = text.splitlines() or [config.file.stem.replace("_", " ").replace("-", " ").title()]
    page = page_from_lines(
        page_index=1,
        lines=lines,
        language=config.language_hint or "unknown",
        confidence=0.6 if warnings else 0.85,
    )
    return {
        "pages": [page],
        "tables": [],
        "figures": [],
        "entities": [],
        "warnings": warnings,
        "backend": "contract-text",
    }


def is_valid_mineru_model_dir(path: Path) -> bool:
    return path.is_dir() and all((path / filename).exists() for filename in MINERU_REQUIRED_MODEL_FILES)


def find_mineru_model_dir(base_dir: Path) -> Path | None:
    env_candidates = [
        os.environ.get("MINERU_OPENVINO_MODEL_DIR"),
        os.environ.get("MINERU_MODEL_DIR"),
    ]
    candidates: list[Path] = []
    for raw in env_candidates:
        if raw:
            candidates.append(Path(raw).expanduser())

    local_models = base_dir / "models"
    candidates.extend(
        [
            local_models / "MinerU2.5-Pro-2604-1.2B-int4-ov",
            local_models / "mineru2.5-int4-ov",
            local_models / "MinerU2.5-Pro-2604-1.2B-ov",
        ]
    )

    cache_root = Path.home() / ".cache" / "modelscope" / "hub" / "models" / "snake7gun"
    if cache_root.exists():
        candidates.extend(path for path in cache_root.iterdir() if path.is_dir())

    seen: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if is_valid_mineru_model_dir(candidate):
            return candidate
    return None


def normalize_block_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_block_text(item) for item in value if normalize_block_text(item))
    if isinstance(value, dict):
        if "content" in value:
            return normalize_block_text(value["content"])
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def parse_markdown_table(text: str) -> tuple[list[str], list[list[str]]] | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    table_lines = [line for line in lines if "|" in line]
    if len(table_lines) < 2:
        return None

    def split_row(line: str) -> list[str]:
        line = line.strip().strip("|")
        return [cell.strip() for cell in line.split("|")]

    rows = [split_row(line) for line in table_lines]
    if len(rows) >= 2 and all(set(cell) <= {"-", ":", " "} for cell in rows[1]):
        headers = rows[0]
        body = rows[2:]
    else:
        headers = rows[0]
        body = rows[1:]
    if not headers:
        return None
    return headers, body


def parse_html_table(text: str) -> tuple[list[str], list[list[str]]] | None:
    if "<table" not in text.lower():
        return None
    row_html = re.findall(r"<tr[^>]*>(.*?)</tr>", text, flags=re.IGNORECASE | re.DOTALL)
    if not row_html:
        return None

    def strip_tags(value: str) -> str:
        value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
        value = re.sub(r"<[^>]+>", "", value)
        return " ".join(value.split())

    rows: list[list[str]] = []
    for row in row_html:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.IGNORECASE | re.DOTALL)
        parsed_cells = [strip_tags(cell) for cell in cells]
        if any(parsed_cells):
            rows.append(parsed_cells)
    if not rows:
        return None
    return rows[0], rows[1:]


def convert_bbox(bbox: Any, width: float, height: float) -> list[float]:
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return [0, 0, 0, 0]
    try:
        values = [float(item) for item in bbox]
    except (TypeError, ValueError):
        return [0, 0, 0, 0]
    if max(values) <= 1.5 and width > 0 and height > 0:
        return [
            round(values[0] * width, 2),
            round(values[1] * height, 2),
            round(values[2] * width, 2),
            round(values[3] * height, 2),
        ]
    return [round(value, 2) for value in values]


def map_mineru_block_type(raw_type: str, text: str, is_first_content: bool) -> str:
    normalized = raw_type.strip().lower()
    mapping = {
        "title": "heading",
        "section_title": "heading",
        "table": "table",
        "equation": "formula",
        "formula": "formula",
        "image": "figure",
        "figure": "figure",
        "chart": "chart",
        "list": "list",
    }
    if normalized in mapping:
        return mapping[normalized]
    return classify_line(text, is_first_content)


def build_table_record(
    page_id: str,
    block_id: str,
    table_id: str,
    bbox: list[float],
    text: str,
) -> dict[str, Any] | None:
    parsed = parse_html_table(text) or parse_markdown_table(text)
    if not parsed:
        return None
    headers, rows = parsed
    return {
        "table_id": table_id,
        "page_id": page_id,
        "bbox": bbox,
        "caption": f"Table {table_id}",
        "headers": headers,
        "rows": rows,
        "source_block_ids": [block_id],
    }


def build_figure_record(
    page_id: str,
    block_id: str,
    figure_id: str,
    bbox: list[float],
    text: str,
) -> dict[str, Any]:
    return {
        "figure_id": figure_id,
        "page_id": page_id,
        "bbox": bbox,
        "caption": text or f"Figure {figure_id}",
        "asset_path": None,
        "source_block_ids": [block_id],
    }


def save_mineru_raw_page(out_dir: Path, page_index: int, markdown: str, blocks: list[dict[str, Any]]) -> None:
    raw_dir = out_dir / "mineru_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    write_text(raw_dir / f"page_{page_index}.md", markdown)
    write_json(raw_dir / f"page_{page_index}_blocks.json", {"blocks": blocks})


def build_page_from_mineru_blocks(
    page_index: int,
    page_width: float,
    page_height: float,
    blocks: list[dict[str, Any]],
    language: str,
    save_figures: bool,
    save_tables: bool,
    table_offset: int,
    figure_offset: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    page_id = f"page_{page_index}"
    canonical_blocks: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []
    figures: list[dict[str, Any]] = []
    first_content = True

    for raw_index, raw_block in enumerate(blocks, start=1):
        text = normalize_block_text(raw_block.get("content") or raw_block.get("text"))
        raw_type = str(raw_block.get("type") or "text")
        block_type = map_mineru_block_type(raw_type, text, first_content)
        confidence = float(raw_block.get("score") or raw_block.get("confidence") or 0.9)
        bbox = convert_bbox(raw_block.get("bbox"), page_width, page_height)
        block = make_block(
            page_index=page_index,
            block_index=len(canonical_blocks) + 1,
            block_type=block_type,
            text=text,
            bbox=bbox,
            confidence=confidence,
            language=language,
        )

        if block_type == "table":
            table_id = f"table_{table_offset + len(tables) + 1}"
            if save_tables:
                table = build_table_record(page_id, block["block_id"], table_id, bbox, text)
                if table is not None:
                    tables.append(table)
                    block["relations"]["table_id"] = table_id
            if "<table" in text.lower():
                block["html"] = text
        elif block_type in {"figure", "chart"} and save_figures:
            figure_id = f"figure_{figure_offset + len(figures) + 1}"
            figures.append(build_figure_record(page_id, block["block_id"], figure_id, bbox, text))
            block["relations"]["figure_id"] = figure_id
        elif block_type == "formula":
            block["latex"] = text

        canonical_blocks.append(block)
        if text:
            first_content = False

    if not canonical_blocks:
        canonical_blocks.append(
            make_block(
                page_index=page_index,
                block_index=1,
                block_type="unknown",
                text="",
                confidence=0.0,
                language=language,
            )
        )

    return (
        {
            "page_id": page_id,
            "page_index": page_index,
            "width": page_width,
            "height": page_height,
            "blocks": canonical_blocks,
        },
        tables,
        figures,
    )


def run_mineru_openvino_on_page_images(
    config: ParseConfig,
    page_images: list[Any],
) -> dict[str, Any] | None:
    base_dir = Path(__file__).resolve().parent.parent
    model_dir = find_mineru_model_dir(base_dir)
    if model_dir is None:
        return None
    try:
        from mineru_openvino_backend import OVMinerUClient
    except Exception:
        return None

    device = os.environ.get("MINERU_OPENVINO_DEVICE", "AUTO")
    image_analysis = os.environ.get("MINERU_OPENVINO_IMAGE_ANALYSIS", "0") == "1"
    client = OVMinerUClient(
        model_dir=model_dir,
        device=device,
        image_analysis=image_analysis,
        debug=config.debug,
    )

    pages: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []
    figures: list[dict[str, Any]] = []
    warnings: list[str] = []

    for index, image in enumerate(page_images, start=1):
        markdown, extract_result = client.image_to_markdown(image)
        raw_blocks = list(extract_result)
        save_mineru_raw_page(config.out, index, markdown, raw_blocks)
        width, height = image.size
        page, page_tables, page_figures = build_page_from_mineru_blocks(
            page_index=index,
            page_width=width,
            page_height=height,
            blocks=raw_blocks,
            language=config.language_hint or "unknown",
            save_figures=config.save_figures,
            save_tables=config.save_tables,
            table_offset=len(tables),
            figure_offset=len(figures),
        )
        if not page["blocks"]:
            warnings.append(f"MinerU page {index} produced no canonical blocks.")
        pages.append(page)
        tables.extend(page_tables)
        figures.extend(page_figures)

    return {
        "pages": pages,
        "tables": tables,
        "figures": figures,
        "entities": [],
        "warnings": warnings,
        "backend": "mineru-openvino",
        "model_dir": str(model_dir),
    }


def parse_pdf_with_pymupdf(config: ParseConfig) -> dict[str, Any] | None:
    if not module_available("fitz"):
        return None

    import fitz  # type: ignore

    doc = fitz.open(str(config.file))
    pages: list[dict[str, Any]] = []
    max_pages = config.max_pages or doc.page_count
    for page_number in range(min(doc.page_count, max_pages)):
        fitz_page = doc.load_page(page_number)
        blocks = []
        raw_blocks = fitz_page.get_text("blocks")
        for raw in sorted(raw_blocks, key=lambda item: (item[1], item[0])):
            x0, y0, x1, y1, text, *_ = raw
            lines = [line.strip() for line in str(text).splitlines() if line.strip()]
            for line in lines:
                block_type = classify_line(line, len(blocks) == 0)
                blocks.append(
                    make_block(
                        page_index=page_number + 1,
                        block_index=len(blocks) + 1,
                        block_type=block_type,
                        text=line,
                        bbox=[x0, y0, x1, y1],
                        confidence=0.9,
                        language=config.language_hint or "unknown",
                    )
                )
        if not blocks:
            blocks.append(
                make_block(
                    page_index=page_number + 1,
                    block_index=1,
                    block_type="unknown",
                    text="",
                    confidence=0.0,
                    language=config.language_hint or "unknown",
                )
            )
        rect = fitz_page.rect
        pages.append(
            {
                "page_id": f"page_{page_number + 1}",
                "page_index": page_number + 1,
                "width": rect.width,
                "height": rect.height,
                "blocks": blocks,
            }
        )

    doc.close()
    return {
        "pages": pages,
        "tables": [],
        "figures": [],
        "entities": [],
        "warnings": [],
        "backend": "pymupdf",
    }


def parse_pdf_with_pypdf(config: ParseConfig) -> dict[str, Any] | None:
    if not module_available("pypdf"):
        return None

    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(config.file))
    pages: list[dict[str, Any]] = []
    max_pages = config.max_pages or len(reader.pages)
    for page_number, page in enumerate(reader.pages[:max_pages], start=1):
        text = page.extract_text() or ""
        lines = text.splitlines()
        pages.append(
            page_from_lines(
                page_index=page_number,
                lines=lines,
                language=config.language_hint or "unknown",
                confidence=0.8,
            )
        )

    return {
        "pages": pages,
        "tables": [],
        "figures": [],
        "entities": [],
        "warnings": [],
        "backend": "pypdf",
    }


def parse_pdf_document(config: ParseConfig) -> dict[str, Any]:
    try:
        from mineru_openvino_backend import pdf_to_images
    except Exception:
        pdf_to_images = None  # type: ignore[assignment]

    if pdf_to_images is not None and module_available("openvino_genai") and module_available("mineru_vl_utils"):
        try:
            dpi = int(os.environ.get("MINERU_OPENVINO_DPI", "200"))
            page_images = pdf_to_images(config.file, dpi=dpi)
            if config.max_pages is not None:
                page_images = page_images[: config.max_pages]
            parsed = run_mineru_openvino_on_page_images(config, page_images)
            if parsed is not None:
                return parsed
        except Exception as exc:
            fallback = parse_pdf_with_pymupdf(config) or parse_pdf_with_pypdf(config)
            if fallback is not None:
                fallback.setdefault("warnings", []).append(
                    f"MinerU OpenVINO parse failed; fallback backend used instead: {exc}"
                )
                return fallback

    for parser in (parse_pdf_with_pymupdf, parse_pdf_with_pypdf):
        try:
            parsed = parser(config)
        except Exception as exc:
            parsed = None
            last_error = f"{parser.__name__} failed: {exc}"
        else:
            last_error = None
        if parsed is not None:
            if last_error:
                parsed.setdefault("warnings", []).append(last_error)
            if parsed.get("backend") != "mineru-openvino":
                parsed.setdefault("warnings", []).append(
                    "MinerU OpenVINO runtime was not used for this PDF parse."
                )
            return parsed

    warning = (
        "No PDF parser backend is installed for the contract smoke path. Real document parsing "
        "requires MinerU 2.5 with OpenVINO GenAI."
    )
    return parse_text_like_file(config, warning=warning)


def parse_image_document(config: ParseConfig) -> dict[str, Any]:
    if module_available("PIL") and module_available("openvino_genai") and module_available("mineru_vl_utils"):
        try:
            from PIL import Image  # type: ignore

            with Image.open(config.file) as image:
                parsed = run_mineru_openvino_on_page_images(config, [image.convert("RGB")])
            if parsed is not None:
                return parsed
        except Exception as exc:
            warnings = [f"MinerU OpenVINO image parse failed; falling back to metadata parse: {exc}"]
        else:
            warnings = []
    else:
        warnings = []

    width = 0
    height = 0
    if module_available("PIL"):
        try:
            from PIL import Image  # type: ignore

            with Image.open(config.file) as image:
                width, height = image.size
        except Exception as exc:
            warnings.append(f"Could not inspect image dimensions with Pillow: {exc}")
    else:
        warnings.append("Pillow is not installed; image dimensions were not inspected.")

    text = decode_text_file(config.file)
    if text:
        parsed = parse_text_like_file(
            config,
            warning=(
                "Image input was decoded as text for contract smoke testing. Real image parsing must use "
                "MinerU 2.5 with OpenVINO GenAI."
            ),
        )
        parsed["pages"][0]["width"] = width
        parsed["pages"][0]["height"] = height
        parsed["warnings"].extend(warnings)
        return parsed

    figure = {
        "figure_id": "figure_1",
        "page_id": "page_1",
        "bbox": [0, 0, width, height],
        "caption": f"Image input: {config.file.name}",
        "asset_path": str(config.file),
        "source_block_ids": ["p1_b1"],
    }
    page = {
        "page_id": "page_1",
        "page_index": 1,
        "width": width,
        "height": height,
        "blocks": [
            make_block(
                page_index=1,
                block_index=1,
                block_type="figure",
                text=f"Image input: {config.file.name}. MinerU runtime not configured.",
                bbox=[0, 0, width, height],
                confidence=0.0,
                language=config.language_hint or "unknown",
            )
        ],
    }
    warnings.append(
        "MinerU OpenVINO inference is not configured, so image text/layout parsing was not run."
    )
    return {
        "pages": [page],
        "tables": [],
        "figures": [figure],
        "entities": [],
        "warnings": warnings,
        "backend": "image-metadata",
    }


def run_openvino_parse_pipeline(config: ParseConfig, input_type: str) -> dict[str, Any]:
    if input_type == "pdf":
        return parse_pdf_document(config)
    if input_type == "image":
        return parse_image_document(config)
    raise ValueError(f"Unsupported input type: {input_type}")


def render_markdown(document: dict[str, Any]) -> str:
    lines: list[str] = []

    for page in document.get("pages", []):
        lines.append(f"<!-- {page['page_id']} -->")
        for block in sorted(page.get("blocks", []), key=lambda b: b.get("reading_order", 0)):
            block_type = block.get("type")
            text = block.get("markdown") or block.get("text") or ""

            if not text and block_type not in {"figure", "chart", "formula", "table"}:
                continue

            if block_type == "heading":
                heading_level = block.get("attributes", {}).get("heading_level") or 1
                prefix = "#" * max(1, min(int(heading_level), 6))
                if not text.startswith("#"):
                    lines.append(f"{prefix} {block.get('text', '').strip()}")
                else:
                    lines.append(text)
            elif block_type == "list":
                for entry in text.splitlines():
                    entry = entry.strip()
                    if entry:
                        lines.append(f"- {entry.lstrip('-*+ ')}")
            elif block_type == "formula":
                latex = block.get("latex")
                if latex:
                    lines.append(f"$$\n{latex}\n$$")
                elif text:
                    lines.append(f"`{text}`")
            elif block_type == "table":
                lines.append(text or "| Table |\n| --- |")
            elif block_type in {"figure", "chart"}:
                label = block_type.title()
                caption = block.get("text") or f"{label} placeholder"
                lines.append(f"> [{label}] {caption}")
            else:
                lines.append(text)

            lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    config = parse_args()
    ensure_artifact_layout(config.out)

    try:
        if not config.file.exists():
            raise FileNotFoundError(f"Input file not found: {config.file}")

        input_type = detect_input_type(config.file)
        file_hash = sha256_file(config.file)

        document = build_empty_document(config, input_type, file_hash)
        parsed = run_openvino_parse_pipeline(config, input_type)

        document["pages"] = parsed.get("pages", [])
        document["tables"] = parsed.get("tables", [])
        document["figures"] = parsed.get("figures", [])
        document["entities"] = parsed.get("entities", [])
        document["parse_info"]["warnings"] = parsed.get("warnings", [])
        document["parse_info"]["backend"] = parsed.get("backend")
        if parsed.get("model_dir"):
            document["parse_info"]["model_dir"] = parsed.get("model_dir")
        if parsed.get("backend") != "mineru-openvino":
            document["parse_info"]["confidence_note"] = (
                "This run did not use MinerU OpenVINO inference. Use it only as a contract or smoke result, "
                "not as a document-understanding quality result."
            )

        problems = validate_document_schema(document)
        if problems:
            document["parse_info"]["warnings"].extend(problems)

        parsed_json_path = config.out / "parsed.json"
        parsed_md_path = config.out / "parsed.md"

        write_json(parsed_json_path, document)
        write_text(parsed_md_path, render_markdown(document))

        print(json.dumps(build_parse_status(document, config.out), ensure_ascii=False))
        return 0

    except Exception as exc:
        write_error(
            config.out,
            stage="parse",
            message=str(exc),
            input_file=str(config.file),
            mode=config.mode,
        )
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "parse",
                    "message": str(exc),
                    "input_file": str(config.file),
                    "output_dir": str(config.out),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
