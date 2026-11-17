#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export normalized OBS bucket records to a local PDF report.

The module is deliberately decoupled from the query script
(``list_obs_buckets_pdf.py``): it only knows about plain dict records with the
normalized keys ``name`` / ``creation_date`` / ``location`` / ``storage_class``
/ ``policy``.

Design notes:
    - Two PDF backends, chosen at runtime: **reportlab** (preferred, uses the
      built-in CJK CID font ``STSong-Light`` so Chinese headers render with no
      external font file) and **fpdf2** (fallback; a system CJK TTF is used when
      present, otherwise the core Helvetica font). Both imports are lazy so the
      module can be imported — and unit-tested for the missing-dependency branch
      — without the packages installed. When neither is available an
      :class:`ExportError` with an install hint pointing to ``ensure_env.py`` is
      raised.
    - The PDF is saved to a temporary file inside the target directory and
      atomically moved over the destination, so an interrupted write never
      leaves a corrupt/partial PDF behind.
    - A header row (桶名称 / 创建时间 / 区域 / 存储类别 / 桶策略) is always written; an
      optional summary row (桶数量 / N) can be appended via ``summary=True``.

Usage:
    from export_pdf import export_pdf
    export_pdf(buckets, "/tmp/obs_buckets_cn-north-4.pdf", summary=True)
"""

import os
import shutil
import sys
import tempfile

PDF_HEADERS = ["桶名称", "创建时间", "区域", "存储类别", "桶策略"]
DOC_TITLE = "OBS 桶列表"
DEFAULT_FILENAME_PREFIX = "obs_buckets"

# Fallback markers used when a per-bucket field was not returned by OBS.
_FIELD_MISSING = "-"

# Common CJK TrueType font locations for the fpdf2 fallback path.
_CJK_FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttc",
)


class ExportError(Exception):
    """The PDF file could not be produced (bad path / PDF backend missing)."""


def _cell(value):
    """Render a single cell value as a plain string, ``-`` for missing data."""
    if value is None or value == "":
        return _FIELD_MISSING
    if isinstance(value, (dict, list)):
        import json
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def normalized_row(bucket):
    """Map a normalized bucket record to the fixed PDF column order."""
    return [
        _cell(bucket.get("name")),
        _cell(bucket.get("creation_date")),
        _cell(bucket.get("location")),
        _cell(bucket.get("storage_class")),
        _cell(bucket.get("policy")),
    ]


def default_output_path(region):
    """Default .pdf filename: obs_buckets_<region>_<timestamp>.pdf"""
    from datetime import datetime

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.pdf" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def resolve_backend():
    """Return ``"reportlab"`` or ``"fpdf"``, whichever import succeeds first.

    Raises:
        ExportError: neither PDF backend is importable (install hint attached).
    """
    try:
        import reportlab  # noqa: F401
        return "reportlab"
    except ImportError:
        pass
    try:
        import fpdf  # noqa: F401
        return "fpdf"
    except ImportError as exc:
        raise ExportError(
            "缺少 PDF 依赖（reportlab / fpdf2），无法生成 PDF 文件。请先运行 "
            "`python3 scripts/ensure_env.py` 自动安装（pip install reportlab 或 "
            "fpdf2），参见 references/cli-installation-guide.md。详情：%s" % exc
        )


def _rows(buckets, summary, region):
    """Build the full table (header + data + optional summary) as string rows."""
    rows = [list(PDF_HEADERS)]
    for bucket in buckets:
        rows.append(normalized_row(bucket))
    if summary:
        rows.append(["桶数量", "%d" % len(buckets),
                     "Region %s" % region if region else "", "", ""])
    return rows


def render_reportlab(buckets, output_path, summary=False, region=None):
    """Render the report with reportlab (CJK CID font). Returns output_path."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    font_name = "Helvetica"
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        font_name = "STSong-Light"
    except Exception:
        pass

    rows = _rows(buckets, summary, region)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ObsTitle", parent=styles["Title"], fontName=font_name, fontSize=16)
    cell_style = ParagraphStyle(
        "ObsCell", parent=styles["Normal"], fontName=font_name, fontSize=9)

    table_data = [[Paragraph(_escape(c), cell_style) for c in row] for row in rows]
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f5aa8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    if summary and len(rows) > 1:
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, len(rows) - 1), (-1, len(rows) - 1),
             colors.HexColor("#eef2fa")),
        ]))

    doc = SimpleDocTemplate(
        output_path, pagesize=landscape(A4),
        title=DOC_TITLE, author="huawei-cloud-obs-list-pdf")
    doc.build([
        Paragraph(DOC_TITLE, title_style), Spacer(1, 8), table,
    ])
    return output_path


def _escape(text):
    """Escape XML-special characters for reportlab Paragraph markup."""
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def _find_cjk_font():
    for path in _CJK_FONT_CANDIDATES:
        if os.path.isfile(path):
            return path
    return None


def render_fpdf(buckets, output_path, summary=False, region=None):
    """Render the report with fpdf2. Returns output_path."""
    from fpdf import FPDF

    rows = _rows(buckets, summary, region)

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    font_path = _find_cjk_font()
    if font_path:
        try:
            pdf.add_font("CJK", "", font_path)
            family = "CJK"
        except Exception:
            family = "helvetica"
    else:
        family = "helvetica"

    pdf.set_font(family, size=14)
    pdf.cell(0, 10, _ascii_safe(DOC_TITLE, font_path),
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / len(PDF_HEADERS)
    pdf.set_font(family, size=9)
    for row in rows:
        bold = row is rows[0]
        pdf.set_font(family, style="B" if bold and family == "helvetica" else "",
                     size=9)
        for cell_value in row:
            pdf.cell(col_width, 8, _ascii_safe(cell_value, font_path), border=1)
        pdf.ln(8)

    pdf.output(output_path)
    return output_path


def _ascii_safe(value, font_path):
    """fpdf2 core fonts cannot encode CJK; transliterate only when no CJK font."""
    if font_path:
        return str(value)
    return str(value).encode("latin-1", "replace").decode("latin-1")


def export_pdf(buckets, output_path, summary=False, region=None):
    """Write ``buckets`` into a PDF report at ``output_path``.

    Args:
        buckets:     iterable of normalized bucket dicts (name / creation_date /
                     location / storage_class / policy).
        output_path: absolute or relative path of the PDF file to write.
        summary:     when True, append a trailing summary row (桶数量 / N).
        region:      optional region label used in the summary row.

    Returns:
        The absolute path of the written file.

    Raises:
        ExportError: path unusable or no PDF backend available. No
                     partial/corrupt file is left behind.
    """
    backend = resolve_backend()

    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as exc:
            raise ExportError(
                "无法创建输出目录 %r：%s。请检查 --output 路径。"
                % (output_dir, exc)
            )

    buckets = list(buckets)

    # Render into a temp file in the destination dir, then atomically rename:
    # interrupts never leave a corrupt .pdf at the destination.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
        dir=output_dir or ".")
    os.close(fd)
    try:
        if backend == "reportlab":
            render_reportlab(buckets, tmp_path, summary=summary, region=region)
        else:
            render_fpdf(buckets, tmp_path, summary=summary, region=region)
        shutil.move(tmp_path, output_path)
    except ExportError:
        raise
    except Exception as exc:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise ExportError("PDF 文件写出失败：%s（%s）" % (output_path, exc))
    return output_path


if __name__ == "__main__":
    # Minimal standalone demo: writes a small PDF into the system temp dir.
    demo = [
        {"name": "bucket-alpha", "creation_date": "2024-01-02T03:04:05Z",
         "location": "cn-north-4", "storage_class": "Standard"},
        {"name": "bucket-beta", "location": "cn-south-1",
         "storage_class": "Warm", "policy": "private"},
    ]
    path = os.path.join(tempfile.gettempdir(), default_output_path("cn-north-4"))
    try:
        export_pdf(demo, path, summary=True, region="cn-north-4")
    except ExportError as exc:
        sys.stderr.write("[错误] %s\n" % exc)
        sys.exit(1)
    print("已生成示例 PDF：%s" % path)
    sys.exit(0)