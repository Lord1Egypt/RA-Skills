#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export normalized OBS bucket records to a .xlsx workbook via openpyxl.

The module is deliberately decoupled from the query script (``list_obs_buckets
_excel.py``): it only knows about plain dict records with the normalized keys
``name`` / ``creation_date`` / ``location`` / ``storage_class`` / ``policy``.

Design notes:
    - openpyxl is imported lazily so the module can be imported (and unit-tested
      for the missing-dependency branch) without the package being installed.
      When it is missing, a :class:`ExportError` with an install hint pointing to
      ``ensure_env.py`` is raised.
    - The workbook is saved to a temporary file inside the target directory and
      atomically moved over the destination, so an interrupted write never
      leaves a corrupt/partial .xlsx behind.
    - A header row (桶名称 / 创建时间 / 区域 / 存储类别 / 桶策略) is always written;
      an optional summary row (桶数量 / N) can be appended via ``summary=True``.

Usage:
    from export_xlsx import export_xlsx
    export_xlsx(buckets, "/tmp/obs_buckets_cn-north-4.xlsx", summary=True)
"""

import os
import shutil
import sys
import tempfile

XLSX_HEADERS = ["桶名称", "创建时间", "区域", "存储类别", "桶策略"]
SHEET_TITLE = "OBS 桶列表"
DEFAULT_FILENAME_PREFIX = "obs_buckets"

# Fallback markers used when a per-bucket field was not returned by OBS.
_FIELD_MISSING = "-"


class ExportError(Exception):
    """The .xlsx file could not be produced (bad path / openpyxl missing)."""


def _cell(value):
    """Render a single cell value as a plain string, ``-`` for missing data."""
    if value is None or value == "":
        return _FIELD_MISSING
    if isinstance(value, (dict, list)):
        import json
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def normalized_row(bucket):
    """Map a normalized bucket record to the fixed xlsx column order."""
    return [
        _cell(bucket.get("name")),
        _cell(bucket.get("creation_date")),
        _cell(bucket.get("location")),
        _cell(bucket.get("storage_class")),
        _cell(bucket.get("policy")),
    ]


def default_output_path(region):
    """Default .xlsx filename: obs_buckets_<region>_<timestamp>.xlsx"""
    from datetime import datetime

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.xlsx" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def _require_openpyxl():
    """Import openpyxl or raise ExportError with an install hint."""
    try:
        from openpyxl import Workbook  # noqa: F401
    except ImportError as exc:
        raise ExportError(
            "缺少依赖 openpyxl，无法生成 Excel 文件。请先运行 "
            "`python3 scripts/ensure_env.py` 自动安装（pip install openpyxl），"
            "参见 references/cli-installation-guide.md。详情：%s" % exc
        )


def export_xlsx(buckets, output_path, summary=False, region=None):
    """Write ``buckets`` into an .xlsx workbook at ``output_path``.

    Args:
        buckets:     iterable of normalized bucket dicts (name / creation_date /
                     location / storage_class / policy).
        output_path: absolute or relative path of the .xlsx file to write.
        summary:     when True, append a trailing summary row (桶数量 / N).
        region:      optional region label used in the summary row comment.

    Returns:
        The absolute path of the written file.

    Raises:
        ExportError: path unusable or openpyxl missing. No partial/corrupt file
                     is left behind.
    """
    _require_openpyxl()
    from openpyxl import Workbook

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

    wb = Workbook()
    ws = wb.active
    ws.title = SHEET_TITLE
    ws.append(XLSX_HEADERS)

    for bucket in buckets:
        ws.append(normalized_row(bucket))

    if summary:
        ws.append(["桶数量", "%d" % len(buckets),
                   "Region %s" % region if region else "", "", ""])
        _apply_bold(ws, ws.max_row)

    # Save via a temp file + atomic rename: interrupts never leave a corrupt
    # .xlsx at the destination.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
        dir=output_dir or ".")
    os.close(fd)
    try:
        wb.save(tmp_path)
        shutil.move(tmp_path, output_path)
    except Exception as exc:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise ExportError("Excel 文件写出失败：%s（%s）"
                          % (output_path, exc))
    return output_path


def _apply_bold(ws, row):
    """Bold the first cell of ``row``; best-effort (style import failure is fine)."""
    try:
        from openpyxl.styles import Font
        ws.cell(row=row, column=1).font = Font(bold=True)
    except Exception:
        pass


if __name__ == "__main__":
    # Minimal standalone demo: writes a small workbook into the system temp dir.
    demo = [
        {"name": "bucket-alpha", "creation_date": "2024-01-02T03:04:05Z",
         "location": "cn-north-4", "storage_class": "Standard"},
        {"name": "bucket-beta", "location": "cn-south-1",
         "storage_class": "Warm", "policy": "private"},
    ]
    path = os.path.join(tempfile.gettempdir(), default_output_path("cn-north-4"))
    try:
        export_xlsx(demo, path, summary=True, region="cn-north-4")
    except ExportError as exc:
        sys.stderr.write("[错误] %s\n" % exc)
        sys.exit(1)
    print("已生成示例 Excel：%s" % path)
    sys.exit(0)