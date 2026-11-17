#!/usr/bin/env python3
"""Render the audited cloud results into Excel Paper Sheet + Reading List.

Reads the LoomLoom result-rows JSON which contains **one row per screened paper** (V1.1
per-paper execution model), extracts the stp_build01 artifact of EVERY completed row, merges
them into one global Paper Sheet + Reading List, and writes two .xlsx workbooks:

- PaperSheet.xlsx  — one row per screened paper, full record columns (merged across all task rows)
- ReadingList.xlsx — grouped by the six Reading Role categories with the required columns (merged)

Uses only the Python standard library; no openpyxl dependency.
Writes .xlsx-compatible XML workbooks directly (no third-party packages).
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROLES = ["Foundational", "Core Evidence", "Supporting", "Counterargument", "Recent", "Methodology"]
PAPER_COLS = [
    "record_id", "priority", "primary_reading_role", "citation", "title", "authors",
    "publication_year", "source_journal_publisher", "source_type", "doi", "isbn", "url",
    "database_record", "links", "evidence_availability_level", "available_evidence",
    "missing_evidence", "assessment_limitations", "topic_relevance", "source_validity",
    "basic_credibility", "content_credibility_status", "recency_status", "summary", "notes",
]
LIST_COLS = ["priority", "reading_role", "citation", "title", "notes", "summary", "links"]


def collect_build_artifacts(rows):
    """Return (texts, missing).

    `texts` holds the stp_build01 inlineText of every completed row that carries one. `missing`
    lists the completed rows that carry no build artifact, so a partial pool is reported instead of
    being rendered as if it were complete.
    """
    texts = []
    missing = []
    for index, row in enumerate(rows):
        if row.get("status") != "completed":
            continue
        found = ""
        for a in row.get("artifacts", []):
            if a.get("stepId") == "stp_build01" and a.get("inlineText"):
                found = a["inlineText"]
                break
        if found:
            texts.append(found)
        else:
            missing.append({
                "row": index,
                "recordId": row.get("recordId") or row.get("record_id") or "",
            })
    return texts, missing


def strip_fence(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1]
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def merge_builds(texts):
    """Merge per-row build outputs into one global paper_sheet + reading_list."""
    paper_sheet = []
    reading_list = {}
    for t in texts:
        b = json.loads(strip_fence(t))
        paper_sheet.extend(b.get("paper_sheet", []))
        for cat, items in b.get("reading_list", {}).items():
            reading_list.setdefault(cat, []).extend(items)
    return paper_sheet, reading_list


def xml_escape(v):
    if v is None:
        return ""
    s = str(v)
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def write_xlsx(path, sheets):
    """sheets: list of (name, headers, rows)."""
    import io
    parts = []
    for idx, (name, headers, rows) in enumerate(sheets, start=1):
        col_letters = [chr(ord("A") + i) if i < 26 else "A" + chr(ord("A") + i - 26) for i in range(len(headers))]
        row_xmls = []
        def emit(r, values):
            cells = []
            for ci, v in enumerate(values):
                cells.append(f'<c r="{col_letters[ci]}{r}" t="inlineStr"><is><t xml:space="preserve">{xml_escape(v)}</t></is></c>')
            row_xmls.append(f'<row r="{r}">{"".join(cells)}</row>')
        emit(1, headers)
        for ri, row in enumerate(rows, start=2):
            emit(ri, row)
        sheet_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f"<sheetData>{''.join(row_xmls)}</sheetData></worksheet>"
        )
        parts.append((name, sheet_xml))
    # minimal xlsx: [Content_Types].xml, _rels/.rels, xl/workbook.xml, xl/_rels/workbook.xml.rels, xl/worksheets/sheetN.xml
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(parts) + 1))
        + "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>"
        + "".join(f'<sheet name="{xml_escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i, (name, _) in enumerate(parts, start=1))
        + "</sheets></workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(parts) + 1))
        + "</Relationships>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        for i, (_, sheet_xml) in enumerate(parts, start=1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="result-rows JSON (one row per paper; all rows are merged)")
    ap.add_argument("--out-dir", default=".", help="output directory")
    ap.add_argument("--allow-partial", action="store_true",
                    help="render even when a completed row has no build artifact (the pool is then incomplete)")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = data.get("rows", data if isinstance(data, list) else [])
    texts, missing = collect_build_artifacts(rows)
    if not texts:
        raise SystemExit("no stp_build01 artifact found in input")
    if missing:
        detail = ", ".join(m.get("recordId") or f"row {m.get('row')}" for m in missing)
        if not args.allow_partial:
            raise SystemExit(
                f"{len(missing)} completed row(s) have no stp_build01 artifact ({detail}); "
                "the rendered pool would be incomplete. Re-run with --allow-partial to render anyway."
            )
        print(f"WARNING: {len(missing)} completed row(s) have no build artifact ({detail}) "
              "— rendering a partial pool", file=sys.stderr)
    paper_sheet, reading_list = merge_builds(texts)

    paper_rows = [[p.get(c, "") for c in PAPER_COLS] for p in paper_sheet]
    list_rows = []
    for cat in ROLES:
        for it in reading_list.get(cat, []):
            list_rows.append([it.get(c, "") for c in LIST_COLS])

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paper_path = out_dir / "PaperSheet.xlsx"
    list_path = out_dir / "ReadingList.xlsx"
    for target in (paper_path, list_path):
        if target.exists():
            print(f"WARNING: overwriting existing file {target}", file=sys.stderr)
    write_xlsx(paper_path, [("PaperSheet", PAPER_COLS, paper_rows)])
    write_xlsx(list_path, [("ReadingList", LIST_COLS, list_rows)])
    print(f"wrote {paper_path} ({len(paper_rows)} rows, merged from {len(texts)} task rows)")
    print(f"wrote {list_path} ({len(list_rows)} rows)")


if __name__ == "__main__":
    main()