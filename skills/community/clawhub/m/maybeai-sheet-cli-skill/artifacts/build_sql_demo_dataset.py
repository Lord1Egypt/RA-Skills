#!/usr/bin/env python3

from __future__ import annotations

import os
import zipfile
from xml.sax.saxutils import escape


OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "sql-formula-demo-dataset.xlsx",
)


SHEETS = [
    {
        "name": "Orders",
        "rows": [
            ["Order ID", "Order Date", "Region", "SKU", "Revenue"],
            ["ORD-1001", "2026-06-01", "North", "SKU-001", 120.50],
            ["ORD-1002", "2026-06-01", "South", "SKU-002", 89.90],
            ["ORD-1003", "2026-06-02", "East", "SKU-003", 210.00],
            ["ORD-1004", "2026-06-02", "West", "SKU-004", 145.20],
            ["ORD-1005", "2026-06-03", "North", "SKU-005", 310.40],
            ["ORD-1006", "2026-06-03", "South", "SKU-001", 98.30],
            ["ORD-1007", "2026-06-04", "East", "SKU-002", 76.80],
            ["ORD-1008", "2026-06-04", "West", "SKU-003", 188.50],
            ["ORD-1009", "2026-06-05", "North", "SKU-004", 132.00],
            ["ORD-1010", "2026-06-05", "South", "SKU-005", 275.75],
            ["ORD-1011", "2026-06-06", "East", "SKU-001", 110.10],
            ["ORD-1012", "2026-06-06", "West", "SKU-002", 95.45],
            ["ORD-1013", "2026-06-07", "North", "SKU-003", 225.00],
            ["ORD-1014", "2026-06-07", "South", "SKU-004", 165.35],
            ["ORD-1015", "2026-06-08", "East", "SKU-005", 340.90],
            ["ORD-1016", "2026-06-08", "West", "SKU-001", 101.25],
            ["ORD-1017", "2026-06-09", "North", "SKU-002", 84.60],
            ["ORD-1018", "2026-06-09", "South", "SKU-003", 199.99],
            ["ORD-1019", "2026-06-10", "East", "SKU-004", 154.80],
            ["ORD-1020", "2026-06-10", "West", "SKU-005", 289.10],
        ],
    },
    {
        "name": "Products",
        "rows": [
            ["SKU", "Category", "Product Name"],
            ["SKU-001", "Accessories", "Travel Cable Organizer"],
            ["SKU-002", "Accessories", "Magnetic Phone Stand"],
            ["SKU-003", "Electronics", "Wireless Earbuds"],
            ["SKU-004", "Home", "Desk Lamp"],
            ["SKU-005", "Home", "Air Purifier"],
        ],
    },
    {
        "name": "Report",
        "rows": [
            ["SQL Formula Demo"],
            ["A live =SQL(...) formula will be written starting at A4 after upload."],
            [""],
        ],
    },
]


def col_name(index: int) -> str:
    result = []
    while index > 0:
        index, rem = divmod(index - 1, 26)
        result.append(chr(65 + rem))
    return "".join(reversed(result))


def cell_xml(ref: str, value) -> str:
    if value is None:
        return f'<c r="{ref}"/>'
    if isinstance(value, (int, float)):
        return f'<c r="{ref}"><v>{value}</v></c>'
    text = escape(str(value))
    return (
        f'<c r="{ref}" t="inlineStr">'
        f"<is><t>{text}</t></is>"
        f"</c>"
    )


def worksheet_xml(rows: list[list[object]]) -> str:
    row_xml = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            ref = f"{col_name(c_idx)}{r_idx}"
            cells.append(cell_xml(ref, value))
        row_xml.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    dimension = f"A1:{col_name(max(len(row) for row in rows))}{len(rows)}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{dimension}"/>'
        "<sheetViews><sheetView workbookViewId=\"0\"/></sheetViews>"
        "<sheetFormatPr defaultRowHeight=\"15\"/>"
        f"<sheetData>{''.join(row_xml)}</sheetData>"
        "</worksheet>"
    )


def workbook_xml() -> str:
    sheets_xml = []
    for idx, sheet in enumerate(SHEETS, start=1):
        name = escape(sheet["name"])
        sheets_xml.append(
            f'<sheet name="{name}" sheetId="{idx}" r:id="rId{idx}"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<bookViews><workbookView/></bookViews>"
        f"<sheets>{''.join(sheets_xml)}</sheets>"
        "</workbook>"
    )


def workbook_rels_xml() -> str:
    rels = []
    for idx in range(1, len(SHEETS) + 1):
        rels.append(
            '<Relationship '
            f'Id="rId{idx}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
    rels.append(
        '<Relationship Id="rId999" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f"{''.join(rels)}"
        "</Relationships>"
    )


def root_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
        'Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
        'Target="docProps/app.xml"/>'
        "</Relationships>"
    )


def content_types_xml() -> str:
    overrides = [
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" '
        'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for idx in range(1, len(SHEETS) + 1):
        overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f"{''.join(overrides)}"
        "</Types>"
    )


def styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill></fills>'
        '<borders count="1"><border/></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )


def core_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>Codex</dc:creator>'
        '<cp:lastModifiedBy>Codex</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-06-17T00:00:00Z</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-06-17T00:00:00Z</dcterms:modified>'
        '</cp:coreProperties>'
    )


def app_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Codex</Application>'
        '</Properties>'
    )


def build_xlsx() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with zipfile.ZipFile(OUTPUT_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml())
        zf.writestr("_rels/.rels", root_rels_xml())
        zf.writestr("docProps/core.xml", core_xml())
        zf.writestr("docProps/app.xml", app_xml())
        zf.writestr("xl/workbook.xml", workbook_xml())
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml())
        zf.writestr("xl/styles.xml", styles_xml())
        for idx, sheet in enumerate(SHEETS, start=1):
            zf.writestr(
                f"xl/worksheets/sheet{idx}.xml",
                worksheet_xml(sheet["rows"]),
            )
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build_xlsx()
