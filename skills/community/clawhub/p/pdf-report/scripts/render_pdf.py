#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import json
import math
import os
import re
import sys
from pathlib import Path


def get_workspace_root() -> Path:
    # Prefer explicit env var, fall back to walking up to find .openclaw marker,
    # then fall back to parents[3] for backward compatibility.
    env_root = os.environ.get("OPENCLAW_WORKSPACE")
    if env_root:
        return Path(env_root).resolve()

    current = Path(__file__).resolve().parent
    for ancestor in [current] + list(current.parents):
        if (ancestor / ".openclaw").is_dir() or (ancestor / "AGENTS.md").is_file():
            return ancestor

    return Path(__file__).resolve().parents[3]


def resolve_workspace_path(raw_path: str, workspace: Path, must_exist: bool) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = workspace / path

    if must_exist:
        resolved = path.resolve(strict=True)
    else:
        resolved = path.resolve(strict=False)

    try:
        resolved.relative_to(workspace)
    except ValueError as exc:
        raise SystemExit(f"Path must stay inside workspace: {raw_path}") from exc

    return resolved


NULLISH_STRINGS = {
    "",
    "nan",
    "nat",
    "none",
    "null",
    "n/a",
    "na",
}

DATE_ONLY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?$"
)


def format_datetime(value: str) -> str | None:
    raw_value = value.strip()

    if DATE_ONLY_RE.match(raw_value):
        parsed = datetime.strptime(raw_value, "%Y-%m-%d")
        return parsed.strftime("%d/%m/%Y")

    if DATETIME_RE.match(raw_value):
        normalized = raw_value.replace("T", " ")
        for pattern in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                parsed = datetime.strptime(normalized, pattern)
                if parsed.time() == datetime.min.time():
                    return parsed.strftime("%d/%m/%Y")
                return parsed.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                continue

    return None


def normalize_scalar(value) -> str:
    if value is None:
        return ""

    if isinstance(value, float) and math.isnan(value):
        return ""

    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned.lower() in NULLISH_STRINGS:
            return ""

        formatted_datetime = format_datetime(cleaned)
        if formatted_datetime is not None:
            return formatted_datetime

        return cleaned

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value)

    return str(value).strip()


def normalize_table(table: dict | None) -> dict | None:
    if not table:
        return None

    headers = [normalize_scalar(value) for value in table.get("headers", [])]
    rows = []
    for row in table.get("rows", []):
        rows.append([normalize_scalar(value) for value in row])

    if not headers and not rows:
        return None

    return {
        "headers": headers,
        "rows": rows,
    }


def normalize_charts(charts: list[dict] | None, workspace: Path) -> list[dict]:
    normalized = []
    for chart in charts or []:
        src = normalize_scalar(chart.get("src", ""))
        if src:
            # Validate chart path stays inside workspace
            src_path = Path(src).expanduser()
            if not src_path.is_absolute():
                src_path = workspace / src_path
            src_resolved = src_path.resolve()
            try:
                src_resolved.relative_to(workspace)
            except ValueError:
                print(f"Warning: chart path outside workspace, skipped: {src}", file=sys.stderr)
                continue
            if not src_resolved.is_file():
                print(f"Warning: chart image not found: {src_resolved}", file=sys.stderr)
            src = str(src_resolved)
        normalized.append(
            {
                "title": normalize_scalar(chart.get("title", "")),
                "src": src,
                "caption": normalize_scalar(chart.get("caption", "")),
            }
        )
    return normalized


def normalize_sections(sections: list[dict] | None, workspace: Path) -> list[dict]:
    normalized = []
    for section in sections or []:
        normalized.append(
            {
                "title": normalize_scalar(section.get("title", "")),
                "lead": normalize_scalar(section.get("lead", "")),
                "items": [normalize_scalar(item) for item in section.get("items", [])],
                "table": normalize_table(section.get("table")),
                "charts": normalize_charts(section.get("charts"), workspace),
                "note": normalize_scalar(section.get("note", "")),
            }
        )
    return normalized


def normalize_payload(payload: dict, workspace: Path) -> dict:
    title = normalize_scalar(payload.get("title", ""))
    if not title:
        raise SystemExit("Input JSON must contain a non-empty 'title'.")

    return {
        "title": title,
        "subtitle": normalize_scalar(payload.get("subtitle", "")),
        "generated_at": normalize_scalar(payload.get("generated_at", "")),
        "summary": [normalize_scalar(item) for item in payload.get("summary", [])],
        "sections": normalize_sections(payload.get("sections"), workspace),
        "footer": normalize_scalar(payload.get("footer", "")),
    }


def load_payload(input_path: Path) -> dict:
    try:
        return json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {input_path}: {exc}") from exc


def build_environment(template_root: Path):
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    return Environment(
        loader=FileSystemLoader(str(template_root)),
        autoescape=select_autoescape(("html", "xml")),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_html(data: dict, template_path: Path) -> str:
    environment = build_environment(template_path.parent)
    template = environment.get_template(template_path.name)
    return template.render(**data)


def write_pdf(html: str, output_path: Path, base_url: str) -> None:
    from weasyprint import HTML

    output_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=base_url).write_pdf(str(output_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a PDF report from structured JSON.")
    parser.add_argument("--input", required=True, help="JSON input path inside the workspace")
    parser.add_argument("--output", required=True, help="PDF output path inside the workspace")
    parser.add_argument(
        "--template-file",
        help="Optional custom template path inside the workspace",
    )
    parser.add_argument(
        "--html-out",
        help="Optional path to save the rendered HTML inside the workspace",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = get_workspace_root()
    default_template = workspace / "skills" / "pdf-report" / "templates" / "report.html"

    input_path = resolve_workspace_path(args.input, workspace, must_exist=True)
    output_path = resolve_workspace_path(args.output, workspace, must_exist=False)
    template_path = (
        resolve_workspace_path(args.template_file, workspace, must_exist=True)
        if args.template_file
        else default_template
    )
    html_out_path = (
        resolve_workspace_path(args.html_out, workspace, must_exist=False)
        if args.html_out
        else None
    )

    payload = normalize_payload(load_payload(input_path), workspace)
    html = render_html(payload, template_path)

    if html_out_path:
        html_out_path.parent.mkdir(parents=True, exist_ok=True)
        html_out_path.write_text(html, encoding="utf-8")

    write_pdf(html, output_path, base_url=str(workspace))

    result = {
        "success": True,
        "input": str(input_path),
        "output": str(output_path),
        "template": str(template_path),
    }
    if html_out_path:
        result["html_out"] = str(html_out_path)

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
