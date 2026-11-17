#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render normalized DCS instance records to Markdown and write them atomically.

The module is deliberately decoupled from the query script
(``list_dcs_export_markdown.py``): it only knows about plain dict records with
the normalized keys ``name`` / ``instance_id`` / ``engine`` / ``engine_version``
/ ``capacity`` / ``spec_code`` / ``status`` / ``ip`` / ``port`` / ``az_codes``.

Design notes:
    - Pure standard library — no third-party dependency is required to render
      Markdown (the export is plain text). openpyxl-style backends are avoided
      on purpose so the skill stays dependency-light.
    - The report is written to a temporary file inside the target directory and
      atomically moved over the destination, so an interrupted write never
      leaves a corrupt/partial ``.md`` behind.
    - A fixed header row (名称 / ID / 引擎 / 版本 / 容量 / 规格 / 状态 / 连接地址 /
      端口 / 可用区) is always written; missing fields render as ``-``. An
      optional summary line (``--summary``) is appended after the table.

Usage:
    from export_markdown import export_markdown
    export_markdown(instances, "/tmp/dcs_instances_cn-north-4.md", summary=True)
"""

import json
import os
import shutil
import sys
import tempfile

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

MD_HEADERS = [
    "名称", "ID", "引擎", "版本", "容量", "规格", "状态", "连接地址", "端口", "可用区",
]
DEFAULT_FILENAME_PREFIX = "dcs_instances"

# Fallback marker used when a per-instance field was not returned by DCS.
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
    return _cell(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def normalized_row(instance):
    """Map a normalized DCS record to the fixed Markdown column order."""
    return [
        _md_escape(instance.get("name")),
        _md_escape(instance.get("instance_id")),
        _md_escape(instance.get("engine")),
        _md_escape(instance.get("engine_version")),
        _md_escape(instance.get("capacity")),
        _md_escape(instance.get("spec_code")),
        _md_escape(instance.get("status")),
        _md_escape(instance.get("ip")),
        _md_escape(instance.get("port")),
        _md_escape(instance.get("az_codes")),
    ]


def render_markdown(instances, summary=False, region=None):
    """Render the DCS instance list as a GitHub-flavored Markdown table."""
    lines = [
        "| " + " | ".join(MD_HEADERS) + " |",
        "| " + " | ".join(["---"] * len(MD_HEADERS)) + " |",
    ]
    for instance in instances:
        lines.append("| " + " | ".join(normalized_row(instance)) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 DCS 实例（Region %s）。"
                     % (len(instances), region or _FIELD_MISSING))
    return "\n".join(lines)


def default_output_path(region):
    """Default .md filename: dcs_instances_<region>_<timestamp>.md"""
    from datetime import datetime

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.md" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def export_markdown(instances, output_path, summary=False, region=None):
    """Write the DCS instance list as a Markdown report at ``output_path``.

    Args:
        instances:   iterable of normalized DCS dicts (name / instance_id /
                     engine / engine_version / capacity / spec_code / status /
                     ip / port / az_codes).
        output_path: absolute or relative path of the ``.md`` file to write.
        summary:     when True, append a trailing summary line (实例数量).
        region:      optional region label used in the summary line.

    Returns:
        The absolute path of the written file.

    Raises:
        ExportError: path unusable or write failed. No partial/corrupt file is
                     left behind.
    """
    instances = list(instances)
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

    text = render_markdown(instances, summary=summary, region=region)

    # Save via a temp file + atomic rename: interrupts never leave a corrupt
    # .md at the destination.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
        dir=output_dir or ".")
    os.close(fd)
    try:
        with open(tmp_path, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        shutil.move(tmp_path, output_path)
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
        {"name": "cache-demo-01", "instance_id": "dcs-0001", "engine": "Redis",
         "engine_version": "5.0", "capacity": "2", "spec_code": "redis.ha.xu1.large.r2.2",
         "status": "RUNNING", "ip": "192.168.0.10", "port": "6379",
         "az_codes": "cn-north-4a"},
        {"name": "cache-demo-02", "instance_id": "dcs-0002", "engine": "Memcached",
         "engine_version": "1.6", "capacity": "4", "spec_code": "memcached.ha.xu1.large.r2.4",
         "status": "RUNNING", "ip": "192.168.0.11", "port": "11211",
         "az_codes": "cn-north-4b"},
    ]
    path = os.path.join(tempfile.gettempdir(), default_output_path("cn-north-4"))
    try:
        export_markdown(demo, path, summary=True, region="cn-north-4")
    except ExportError as exc:
        sys.stderr.write("[错误] %s\n" % exc)
        sys.exit(1)
    print("已生成示例 Markdown：%s" % path)
    sys.exit(0)