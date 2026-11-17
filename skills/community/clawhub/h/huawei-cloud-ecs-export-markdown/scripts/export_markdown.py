#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render normalized ECS instance records to Markdown and write them atomically.

The module is deliberately decoupled from the query script
(``list_ecs_export_markdown.py``): it only knows about plain dict records with
the normalized keys ``name`` / ``id`` / ``status`` / ``flavor`` / ``vcpus`` /
``ram`` / ``availability_zone`` / ``privateIps`` / ``publicIps``.

Design notes:
    - Pure standard library — no third-party dependency is required to render
      Markdown (the export is plain text). openpyxl-style backends are avoided
      on purpose so the skill stays dependency-light.
    - The report is written to a temporary file inside the target directory and
      atomically moved over the destination, so an interrupted write never
      leaves a corrupt/partial ``.md`` behind.
    - A fixed header row (名称 / ID / 状态 / 规格 / vCPU / 内存 / 可用区 / 私网IP /
      公网IP) is always written; missing fields render as ``-``. An optional
      summary line (``--summary``) is appended after the table.

Usage:
    from export_markdown import export_markdown
    export_markdown(servers, "/tmp/ecs_instances_cn-north-4.md", summary=True)
"""

import json
import os
import sys
import tempfile

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

MD_HEADERS = [
    "名称", "ID", "状态", "规格", "vCPU", "内存", "可用区", "私网IP", "公网IP",
]
DEFAULT_FILENAME_PREFIX = "ecs_instances"
REPORT_TITLE = "华为云 ECS 实例清单"

# Fallback marker used when a per-instance field was not returned by ECS.
_FIELD_MISSING = "-"


class ExportError(Exception):
    """The Markdown file could not be produced (bad path / write failure)."""


def _cell(value):
    """Render a single cell value as a plain string, ``-`` for missing data."""
    if value is None or value == "":
        return _FIELD_MISSING
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _md_escape(value):
    """Escape pipe/newline characters so a cell cannot break the Markdown table."""
    return (_cell(value).replace("|", "\\|")
            .replace("\n", " ").replace("\r", " "))


def normalized_row(server):
    """Map a normalized ECS record to the fixed Markdown column order."""
    return [
        _md_escape(server.get("name")),
        _md_escape(server.get("id")),
        _md_escape(server.get("status")),
        _md_escape(server.get("flavor")),
        _md_escape(server.get("vcpus")),
        _md_escape(server.get("ram")),
        _md_escape(server.get("availability_zone")),
        _md_escape(server.get("privateIps")),
        _md_escape(server.get("publicIps")),
    ]


def render_markdown(servers, summary=False, region=None, filters=None):
    """Render the ECS instance list as a GitHub-flavored Markdown report."""
    lines = [
        "# %s" % REPORT_TITLE,
        "",
    ]
    meta = []
    if region:
        meta.append("Region: %s" % region)
    if filters:
        meta.append("过滤条件: %s" % ", ".join(filters))
    meta.append("实例数量: %d" % len(servers))
    lines.append("> " + " ｜ ".join(meta))
    lines.append("")
    lines.append("| " + " | ".join(MD_HEADERS) + " |")
    lines.append("| " + " | ".join(["---"] * len(MD_HEADERS)) + " |")
    for server in servers:
        lines.append("| " + " | ".join(normalized_row(server)) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 ECS 实例（Region %s）。"
                     % (len(servers), region or _FIELD_MISSING))
    return "\n".join(lines)


def default_output_path(region):
    """Default .md filename: ecs_instances_<region>_<timestamp>.md"""
    from datetime import datetime

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.md" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def export_markdown(servers, output_path, summary=False, region=None,
                    filters=None):
    """Write the ECS instance list as a Markdown report at ``output_path``.

    Args:
        servers:     iterable of normalized ECS dicts (name / id / status /
                     flavor / vcpus / ram / availability_zone / privateIps /
                     publicIps).
        output_path: absolute or relative path of the ``.md`` file to write.
        summary:     when True, append a trailing summary line (实例数量).
        region:      optional region label used in the report header/summary.
        filters:     optional list of active server-side filter descriptions.

    Returns:
        The absolute path of the written file.

    Raises:
        ExportError: path unusable or write failed. No partial/corrupt file is
                     left behind.
    """
    servers = list(servers)
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

    text = render_markdown(servers, summary=summary, region=region,
                           filters=filters)

    # Save via a temp file + os.replace (atomic rename): interrupts never leave
    # a corrupt .md at the destination.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
        dir=output_dir or ".")
    os.close(fd)
    try:
        with open(tmp_path, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        os.replace(tmp_path, output_path)
    except Exception as exc:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise ExportError("Markdown 文件写出失败：%s（%s）"
                          % (output_path, exc))
    return output_path


if __name__ == "__main__":
    # Minimal standalone demo: writes a small report into the system temp dir.
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
        export_markdown(demo, path, summary=True, region="cn-north-4")
    except ExportError as exc:
        sys.stderr.write("[错误] %s\n" % exc)
        sys.exit(1)
    print("已生成示例 Markdown：%s" % path)
    sys.exit(0)