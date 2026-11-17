#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Serialize a CDN accelerated-domain list into a local result file.

Pure local rendering: given the domain dicts returned by ``list_cdn.py``,
produce one of three formats and write it atomically to disk.

    json  — the raw domain array (``--format json``, default)
    csv   — a flat RFC-4180 CSV whose columns are the union of returned fields
    md    — a Markdown table whose first column is 域名 (domain_name)

No cloud call is issued here; the file is generated on the local filesystem
only. Missing per-domain fields render as ``-``.
"""

import csv
import io
import json
import os
import tempfile
import time

FORMATS = ("json", "csv", "md")

PREFERRED_COLUMNS = [
    "domain_name",
    "domain_status",
    "cname",
    "business_type",
    "id",
    "service_area",
    "https_status",
    "disabled",
    "locked",
    "origin_status",
    "enterprise_project_id",
    "create_time",
    "modify_time",
    "tags",
]

_MD_HEADERS = {
    "domain_name": "域名",
    "domain_status": "加速域名状态",
    "cname": "CNAME",
    "business_type": "业务类型",
    "id": "ID",
    "service_area": "服务区域",
    "https_status": "HTTPS 状态",
    "disabled": "禁用",
    "locked": "锁定",
    "origin_status": "源站状态",
    "enterprise_project_id": "企业项目 ID",
    "create_time": "创建时间",
    "modify_time": "修改时间",
    "tags": "标签",
}


class ExportError(Exception):
    """A local serialization / file-write failure."""


def _flatten_tags(domain):
    """Return a copy of ``domain`` with ``tags`` rendered as ``k=v,...``."""
    flat = dict(domain)
    tags = domain.get("tags")
    if isinstance(tags, list):
        pairs = []
        for tag in tags:
            if isinstance(tag, dict):
                pairs.append("%s=%s" % (tag.get("key", ""), tag.get("value", "")))
            else:
                pairs.append(str(tag))
        flat["tags"] = ",".join(pairs) if pairs else "-"
    elif tags is None:
        flat["tags"] = "-"
    return flat


def field_value(domain, *names, default="-"):
    """First non-empty value among ``names`` (``-`` when none is present)."""
    for name in names:
        if name in domain and domain[name] not in (None, ""):
            return domain[name]
    return default


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _columns(rows):
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in row for row in rows):
            columns.append(key)
    for key in sorted({k for row in rows for k in row}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["domain_name", "domain_status"]
    return columns


def to_json(domains):
    """Raw domain array as pretty JSON (stable, non-ASCII preserved)."""
    return json.dumps(domains, ensure_ascii=False, indent=2) + "\n"


def to_csv(domains):
    """RFC-4180 CSV over the union of returned fields (tags flattened)."""
    rows = [_flatten_tags(domain) for domain in domains]
    columns = _columns(rows)
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(columns)
    for row in rows:
        writer.writerow([_cell(field_value(row, col)) for col in columns])
    return buffer.getvalue()


def to_markdown(domains, region=None, summary=False):
    """A Markdown table whose first column is 域名 (domain_name)."""
    rows = [_flatten_tags(domain) for domain in domains]
    columns = _columns(rows)
    header = "| %s |" % " | ".join(_MD_HEADERS.get(col, col) for col in columns)
    separator = "| %s |" % " | ".join("---" for _ in columns)
    lines = [header, separator]
    for row in rows:
        lines.append("| %s |" % " | ".join(
            _escape_md(_cell(field_value(row, col))) for col in columns))
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 CDN 加速域名（Region %s）。"
                     % (len(domains), region or "-"))
    return "\n".join(lines) + "\n"


def _escape_md(text):
    return text.replace("|", "\\|").replace("\n", " ")


def serialize(domains, fmt="json", region=None, summary=False):
    """Dispatch to the requested serializer; unknown format -> ExportError."""
    fmt = (fmt or "json").lower()
    if fmt == "json":
        return to_json(domains)
    if fmt == "csv":
        return to_csv(domains)
    if fmt == "md":
        return to_markdown(domains, region=region, summary=summary)
    raise ExportError("不支持的导出格式 %r（可选：%s）。" % (fmt, "/".join(FORMATS)))


def extension_for(fmt):
    fmt = (fmt or "json").lower()
    return {"json": "json", "csv": "csv", "md": "md"}.get(fmt, "txt")


def default_output_path(region, fmt="json", timestamp=None):
    """``cdn_domains_<region>_<UTCstamp>.<ext>`` (Spec default naming)."""
    stamp = timestamp or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    return "cdn_domains_%s_%s.%s" % (region or "region", stamp, extension_for(fmt))


def write_text_atomic(path, content):
    """Write ``content`` to ``path`` via a temp file + atomic rename.

    The parent directory is created automatically; an interrupted write never
    leaves a corrupt/partial target file. Returns the resolved path.
    """
    if not path:
        raise ExportError("未指定输出文件路径。")
    parent = os.path.dirname(os.path.abspath(path))
    try:
        os.makedirs(parent, exist_ok=True)
    except OSError as exc:
        raise ExportError("无法创建输出目录 %s：%s" % (parent, exc))
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(prefix=".cdn-export-", dir=parent)
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        os.replace(tmp_path, path)
    except OSError as exc:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise ExportError("导出文件写出失败（%s）：%s" % (path, exc))
    return path


def export(domains, fmt, output=None, region=None, summary=False):
    """Serialize + atomically write; returns (path, content)."""
    content = serialize(domains, fmt=fmt, region=region, summary=summary)
    path = output or default_output_path(region, fmt=fmt)
    write_text_atomic(path, content)
    return path, content