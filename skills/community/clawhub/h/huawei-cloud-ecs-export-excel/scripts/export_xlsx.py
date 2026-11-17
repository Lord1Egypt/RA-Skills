#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export normalized ECS instance records to a .xlsx workbook via openpyxl.

The module is deliberately decoupled from the query script
(``list_ecs_export_excel.py``): it only knows about plain dict records with the
normalized keys ``name`` / ``id`` / ``status`` / ``flavor`` / ``vcpus`` /
``ram`` / ``availability_zone`` / ``privateIps`` / ``publicIps``.

Design notes:
    - openpyxl is imported lazily so the module can be imported (and unit-tested
      for the missing-dependency branch) without the package being installed.
      When it is missing, an :class:`ExportError` with an install hint pointing
      to ``ensure_env.py`` is raised.
    - The workbook is saved to a temporary file inside the target directory and
      atomically moved over the destination, so an interrupted write never
      leaves a corrupt/partial .xlsx behind.
    - A fixed header row (名称 / ID / 状态 / 规格 / vCPU / 内存 / 可用区 / 私网IP /
      公网IP) is always written; an optional summary row (实例数量 / N) can be
      appended via ``summary=True``.

Usage:
    from export_xlsx import export_xlsx
    export_xlsx(servers, "/tmp/ecs_instances_cn-north-4.xlsx", summary=True)
"""

import os
import shutil
import sys
import tempfile

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

XLSX_HEADERS = [
    "名称", "ID", "状态", "规格", "vCPU", "内存", "可用区", "私网IP", "公网IP",
]
SHEET_TITLE = "ECS 实例清单"
DEFAULT_FILENAME_PREFIX = "ecs_instances"

# Fallback markers used when a per-instance field was not returned by ECS.
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


def normalized_row(server):
    """Map a normalized ECS record to the fixed xlsx column order."""
    return [
        _cell(server.get("name")),
        _cell(server.get("id")),
        _cell(server.get("status")),
        _cell(server.get("flavor")),
        _cell(server.get("vcpus")),
        _cell(server.get("ram")),
        _cell(server.get("availability_zone")),
        _cell(server.get("privateIps")),
        _cell(server.get("publicIps")),
    ]


def default_output_path(region):
    """Default .xlsx filename: ecs_instances_<region>_<timestamp>.xlsx"""
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


def export_xlsx(servers, output_path, summary=False, region=None):
    """Write ``servers`` into an .xlsx workbook at ``output_path``.

    Args:
        servers:     iterable of normalized ECS dicts (name / id / status /
                     flavor / vcpus / ram / availability_zone / privateIps /
                     publicIps).
        output_path: absolute or relative path of the .xlsx file to write.
        summary:     when True, append a trailing summary row (实例数量 / N).
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

    for server in servers:
        ws.append(normalized_row(server))

    if summary:
        ws.append(["实例数量", "%d" % len(servers),
                   "Region %s" % region if region else "", "", "", "", "", "", ""])
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
        {"name": "ecs-web-01", "id": "ecs-0001", "status": "ACTIVE",
         "flavor": "s6.large.2", "vcpus": "2", "ram": "4096",
         "availability_zone": "cn-north-4a", "privateIps": "192.168.0.10",
         "publicIps": "-"},
        {"name": "ecs-db-02", "id": "ecs-0002", "status": "SHUTOFF",
         "flavor": "s6.xlarge.2", "vcpus": "4", "ram": "8192",
         "availability_zone": "cn-north-4b", "privateIps": "192.168.0.11",
         "publicIps": "10.0.0.5"},
    ]
    path = os.path.join(tempfile.gettempdir(), default_output_path("cn-north-4"))
    try:
        export_xlsx(demo, path, summary=True, region="cn-north-4")
    except ExportError as exc:
        sys.stderr.write("[错误] %s\n" % exc)
        sys.exit(1)
    print("已生成示例 Excel：%s" % path)
    sys.exit(0)