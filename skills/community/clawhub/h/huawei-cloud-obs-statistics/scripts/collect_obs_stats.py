#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only aggregated statistics for Huawei Cloud OBS (Object Storage Service).

For a target scope (all buckets, or a single bucket, optionally narrowed by a
key ``prefix``) this skill computes, in one shot:

    - bucket count
    - object count
    - total capacity (sum of object ``Size``, bytes; an estimate — not a
      billing figure)
    - distribution by storage class
    - distribution by region

The result is rendered as an aligned table (default), structured JSON
(``--json`` / ``--output json``) or Markdown (``--output md``).

Primary execution path is KooCLI's obsutil-backed OBS module
(``hcloud OBS ls`` — read-only ListBuckets / ListObjects). When the hcloud
binary is absent the script falls back to the official ``huaweicloudsdkobs`` v1
SDK (``ObsClient.list_buckets`` / ``ObsClient.list_objects``).

The skill is strictly read-only: a write-intent guard rejects any mutating
intent (create / delete / upload / download / copy / restore / sync ...) before
a single command runs.

Usage:
    python3 scripts/collect_obs_stats.py [--bucket <bucket>] [--prefix <prefix>]
        [--region cn-north-4] [--output table|json|md] [--json]
        [--executor auto|cli|sdk] [--max-objects N]

Environment overrides (mostly for tests):
    OBS_STATS_HCLOUD_BIN   hcloud executable (default "hcloud")
    OBS_STATS_HCLOUD_ARGS  extra args injected before the OBS operation
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 1000
DEFAULT_MAX_OBJECTS = 100000
SERVICE = "OBS"
ALLOWED_OPERATION = "ls"

# Mutating OBS intents / obsutil commands — strictly rejected by the guard.
# Read-only vocabulary (list/show/get/describe/ls) never matches.
WRITE_INTENT_KEYWORDS = (
    "createbucket",
    "deletebucket",
    "putobject",
    "deleteobject",
    "copyobject",
    "create",
    "delete",
    "upload",
    "download",
    "copy",
    "remove",
    "move",
    "restore",
    "abort",
    "sync",
    "modify",
    "update",
    "overwrite",
)

_CREDENTIAL_MISSING_PATTERNS = (
    "please set ak, sk and endpoint",
    "please set ak, sk",
    "configuration file",
    "cli-ak",
    "cli-sk",
    "access key",
    "secret key",
    "credential",
    "未配置",
    "配置为空",
    "no ak",
    "no sk",
    "ak/sk",
)

_AUTH_PATTERNS = (
    "invalidaccesskeyid",
    "signaturedoesnotmatch",
    "accessdenied",
    "403",
    "401",
    "forbidden",
    "unauthorized",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI / obsutil usage errors are printed with a [USE_ERROR] marker even when
# the return code looks successful — treat the marker as a hard failure.
_USE_ERROR_MARKER = "[use_error]"

_BUCKET_URL_RE = re.compile(r"obs://([A-Za-z0-9._\-]+)")
_OBJECT_URL_RE = re.compile(r"obs://([A-Za-z0-9._\-]+)/(\S+)")
_DATE_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?")
_LOCATION_RE = re.compile(r"\b([a-z]{2}-[a-z]+-\d[a-z]?)\b")
_INT_RE = re.compile(r"(?<![\d.])(\d+)(?![\d.])")

# Canonical storage classes (Huawei Cloud OBS) and alias normalization.
_STORAGE_CLASS_ALIASES = {
    "standard": "STANDARD",
    "standardstorage": "STANDARD",
    "标准": "STANDARD",
    "标准存储": "STANDARD",
    "warm": "WARM",
    "infrequentaccess": "WARM",
    "lowfrequency": "WARM",
    "低频": "WARM",
    "低频访问": "WARM",
    "低频访问存储": "WARM",
    "cold": "COLD",
    "archive": "COLD",
    "archivestorage": "COLD",
    "归档": "COLD",
    "归档存储": "COLD",
    "deeparchive": "DEEP_ARCHIVE",
    "deep_archive": "DEEP_ARCHIVE",
    "深度归档": "DEEP_ARCHIVE",
    "深度归档存储": "DEEP_ARCHIVE",
}
_STORAGE_CLASS_DISPLAY = ("Standard", "Warm", "Cold", "DeepArchive")


class ObsStatsError(Exception):
    """Base error for the OBS statistics skill."""


class GuardError(ObsStatsError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ObsStatsError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(ObsStatsError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ObsStatsError):
    """hcloud / network / unexpected API failure."""


# ── write-intent guard ───────────────────────────────────────────────────

def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-bucket``, ``CreateBucket`` and
    ``create_bucket`` hit the same keyword. Read-only vocabulary
    (list/show/get/describe/ls/stat) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读聚合统计"
                "（OBS ListBuckets / ListObjects），创建/删除/上传/变更等操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only obsutil ``ls`` operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s（列举桶 / 对象）。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


# ── CLI helpers ──────────────────────────────────────────────────────────

def _endpoint_for_region(region):
    return "obs.%s.myhuaweicloud.com" % region


def _hcloud_executable():
    return os.environ.get("OBS_STATS_HCLOUD_BIN", "hcloud")


def build_bucket_command(region, limit=DEFAULT_PAGE_SIZE, endpoint=None):
    """Build the hcloud argv (without the executable) to list all buckets."""
    return [
        SERVICE,
        ALLOWED_OPERATION,
        "-limit=%d" % limit,
        "-e=%s" % (endpoint or _endpoint_for_region(region)),
    ]


def build_object_command(bucket, prefix="", region=DEFAULT_REGION,
                         limit=DEFAULT_PAGE_SIZE, endpoint=None):
    """Build the hcloud argv to list objects under ``obs://bucket/prefix``."""
    url = "obs://%s/" % bucket
    if prefix:
        url += prefix.strip("/") + "/"
    return [
        SERVICE,
        ALLOWED_OPERATION,
        url,
        "-limit=%d" % limit,
        "-e=%s" % (endpoint or _endpoint_for_region(region)),
    ]


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("OBS_STATS_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=300, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。请先安装 KooCLI 及其 obsutil 组件并完成配置，"
            "参见 references/cli-installation-guide.md。"
        )
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（300s），请检查网络或缩小统计范围（--prefix）后重试。")
    return proc.stdout or "", proc.stderr or "", proc.returncode


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：OBS 使用 "
            "obsutil 风格的 `hcloud OBS ls`，可通过 `hcloud OBS ls --help` 查看参数。"
            "详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 OBS，请检查 IAM 权限或 AK/SK 是否有效"
            "（403 / InvalidAccessKeyId / SignatureDoesNotMatch），参见 "
            "references/iam-policies.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS):
        return ConfigError(
            "缺少 AK/SK 凭证：obsutil 未配置有效凭证或 endpoint。请在会话外运行 "
            "`hcloud obs config`（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


def parse_cli_buckets(stdout):
    """Parse obsutil ``ls`` output into a list of bucket dicts.

    Bucket lines are ``obs://<name>`` tokens that carry no object key; a
    creation date and a region are detected heuristically when columns are
    present. Duplicate names collapse to the first occurrence.
    """
    buckets = []
    seen = set()
    for line in (stdout or "").splitlines():
        match = _BUCKET_URL_RE.search(line)
        if not match:
            continue
        # Skip object lines (obs://<bucket>/<key>).
        after = line[match.end():]
        if after[:1] == "/":
            continue
        name = match.group(1)
        if name in seen:
            continue
        seen.add(name)
        record = {"name": name}
        rest = after
        date_match = _DATE_RE.search(rest)
        if date_match:
            record["creation_date"] = date_match.group(0)
        loc_match = _LOCATION_RE.search(rest)
        if loc_match:
            record["location"] = loc_match.group(1)
        buckets.append(record)
    return buckets


def _normalize_storage_class(raw):
    if not raw:
        return "STANDARD"
    key = re.sub(r"[\s_\-]+", "", str(raw).lower())
    if key in _STORAGE_CLASS_ALIASES:
        return _STORAGE_CLASS_ALIASES[key]
    upper = str(raw).strip().upper().replace(" ", "_")
    if upper in ("STANDARD", "WARM", "COLD", "DEEP_ARCHIVE"):
        return upper
    return "UNKNOWN"


def _detect_storage_class(tokens):
    for token in tokens:
        stripped = token.strip(" ,;|")
        key = re.sub(r"[\s_\-]+", "", stripped.lower())
        if key in _STORAGE_CLASS_ALIASES:
            return _STORAGE_CLASS_ALIASES[key]
    return None


def parse_cli_objects(stdout, bucket):
    """Parse obsutil ``ls`` object lines for a single bucket.

    Returns a list of ``{"key", "size", "storage_class"}``. Folder markers
    (keys ending with ``/``) and the bucket/prefix header line are skipped.
    """
    objects = []
    for line in (stdout or "").splitlines():
        match = _OBJECT_URL_RE.search(line)
        if not match:
            continue
        name, key = match.group(1), match.group(2).strip()
        if name != bucket:
            continue
        if not key or key.endswith("/"):
            # Folder marker or the prefix header — not an object.
            continue
        if key.startswith("Folder number") or key.startswith("Object number"):
            continue
        tail = line[match.end():]
        size = 0
        size_match = _INT_RE.search(tail)
        # The first standalone integer after the key is the object size (bytes).
        if size_match:
            size = int(size_match.group(1))
        storage_class = _detect_storage_class(tail.split()) or "STANDARD"
        objects.append({"key": key, "size": size, "storage_class": storage_class})
    return objects


# ── credentials / SDK ────────────────────────────────────────────────────

def _env_credential(*names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _env_credentials():
    ak = _env_credential(
        "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
        "HUAWEI_CLOUD_ACCESS_KEY",
    )
    sk = _env_credential(
        "HW_SECRET_KEY", "HUAWEI_SECRET_KEY", "HUAWEICLOUD_SDK_SK",
        "HUAWEI_CLOUD_SECRET_KEY",
    )
    token = _env_credential(
        "HW_SECURITY_TOKEN", "HUAWEI_SECURITY_TOKEN",
        "HUAWEICLOUD_SDK_SECURITY_TOKEN",
    )
    return ak, sk, token


def build_sdk_client(region):
    """Build an ``ObsClient`` from standard environment credentials."""
    ak, sk, token = _env_credentials()
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：当前环境未检测到 HW_ACCESS_KEY / "
            "HUAWEI_ACCESS_KEY / HUAWEICLOUD_SDK_AK 形式的 AK/SK 环境变量。请"
            "在会话外设置（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。"
        )
    try:
        from huaweicloudsdkobs.v1 import ObsClient
        from huaweicloudsdkobs.v1.obs_credentials import ObsCredentials
        from huaweicloudsdkobs.v1.region.obs_region import ObsRegion
        from huaweicloudsdkcore.http.http_config import HttpConfig
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkobs "
            "未安装，无法回退到 SDK。请安装 KooCLI 或 pip install "
            "huaweicloudsdkcore huaweicloudsdkobs。详情：%s" % exc
        )
    credentials = (ObsCredentials(ak, sk, token) if token
                   else ObsCredentials(ak, sk))
    try:
        region_obj = ObsRegion.value_of(region)
    except (ValueError, KeyError, AttributeError):
        raise ConfigError(
            "SDK 初始化失败：未知的 region %r，请核对区域参数。详情见 "
            "references/cli-installation-guide.md。" % region
        )
    try:
        return ObsClient.new_builder() \
            .with_http_config(HttpConfig.get_default_config()) \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .build()
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkobs 安装与区域"
            "配置。" % (region, exc)
        )


def list_buckets_via_sdk(region):
    """List account buckets through ``huaweicloudsdkobs`` v1."""
    client = build_sdk_client(region)
    try:
        from huaweicloudsdkobs.v1.model import ListBucketsRequest
        response = client.list_buckets(ListBucketsRequest())
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问 OBS，请检查 IAM 权限或 AK/SK 是否有效（403）。详情：%s"
                % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
    raw = getattr(getattr(response, "buckets", None), "bucket", None) or []
    buckets = []
    for b in raw:
        record = {"name": getattr(b, "name", None) or "-"}
        location = getattr(b, "location", None)
        creation_date = getattr(b, "creation_date", None)
        if location:
            record["location"] = location
        if creation_date:
            record["creation_date"] = creation_date
        buckets.append(record)
    return buckets


def list_objects_via_sdk(client, bucket, prefix="", max_objects=DEFAULT_MAX_OBJECTS):
    """Paginated object listing (ListObjects) for one bucket via the SDK.

    Returns ``(objects, truncated)`` where each object is
    ``{"key", "size", "storage_class"}``.
    """
    try:
        from huaweicloudsdkobs.v1.model import ListObjectsRequest
    except ImportError as exc:
        raise ConfigError("huaweicloudsdkobs 未安装：%s" % exc)

    base = prefix.rstrip("/") + "/" if prefix else None
    objects = []
    marker = None
    truncated = False
    while True:
        request = ListObjectsRequest(
            bucket_name=bucket, prefix=base, max_keys=DEFAULT_PAGE_SIZE,
            marker=marker)
        try:
            data = client.list_objects(request).to_dict()
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限读取桶 %s 的对象列表（403）。详情：%s" % (bucket, str(exc)[:300])
                )
            raise ApiError("SDK ListObjects 失败（bucket=%s）：%s" % (bucket, str(exc)[:300]))
        for c in data.get("contents") or []:
            key = c.get("key") or ""
            if base and not key.startswith(base):
                continue
            if not key or key.endswith("/"):
                continue
            size = c.get("size")
            try:
                size = int(size) if size is not None else 0
            except (TypeError, ValueError):
                size = 0
            objects.append({
                "key": key,
                "size": size,
                "storage_class": _normalize_storage_class(c.get("storage_class")),
            })
            if len(objects) >= max_objects:
                truncated = True
                return objects, truncated
        marker = data.get("next_marker")
        if not data.get("is_truncated") or not marker:
            break
    return objects, truncated


# ── collectors (CLI first, SDK fallback) ─────────────────────────────────

def collect_buckets_cli(region, limit=DEFAULT_PAGE_SIZE, endpoint=None):
    argv = build_bucket_command(region, limit=limit, endpoint=endpoint)
    stdout, stderr, returncode = run_hcloud(argv)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode)
    return parse_cli_buckets(stdout)


def collect_objects_cli(bucket, prefix, region,
                        limit=DEFAULT_PAGE_SIZE, endpoint=None):
    argv = build_object_command(bucket, prefix=prefix, region=region,
                                limit=limit, endpoint=endpoint)
    stdout, stderr, returncode = run_hcloud(argv)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode)
    return parse_cli_objects(stdout, bucket)


def resolve_listers(region, executor):
    """Return ``(bucket_lister, object_lister)`` callables for the executor.

    ``bucket_lister(region) -> [bucket dict]``
    ``object_lister(bucket, prefix) -> (objects, truncated)``
    """
    if executor == "sdk":
        client = build_sdk_client(region)
        return (
            lambda reg: list_buckets_via_sdk(reg),
            lambda bucket, prefix: list_objects_via_sdk(client, bucket, prefix),
        )
    if executor == "cli":
        return (
            lambda reg: collect_buckets_cli(reg),
            lambda bucket, prefix: (collect_objects_cli(bucket, prefix, region), False),
        )
    # auto: CLI first, SDK fallback when hcloud is missing.
    def bucket_lister(reg):
        try:
            return collect_buckets_cli(reg)
        except ConfigError:
            return list_buckets_via_sdk(reg)

    def object_lister(bucket, prefix):
        try:
            return collect_objects_cli(bucket, prefix, region), False
        except ConfigError:
            client = build_sdk_client(region)
            return list_objects_via_sdk(client, bucket, prefix)

    return bucket_lister, object_lister


# ── aggregation ──────────────────────────────────────────────────────────

def _human_size(num_bytes):
    units = ("B", "KB", "MB", "GB", "TB", "PB")
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return "%d %s" % (int(size), unit)
            return "%.2f %s" % (size, unit)
        size /= 1024.0
    return "%d B" % num_bytes


def aggregate(buckets, objects_by_bucket, region, prefix=None,
              bucket_filter=None, truncated=False, warnings=None):
    """Aggregate raw buckets + per-bucket objects into the report structure."""
    warnings = list(warnings or [])
    storage_class_count = {}
    storage_class_size = {}
    region_distribution = {}
    bucket_reports = []

    total_objects = 0
    total_size = 0

    for bucket in buckets:
        name = bucket.get("name", "-")
        location = bucket.get("location") or None
        objs = objects_by_bucket.get(name, [])
        b_count = len(objs)
        b_size = sum(int(o.get("size") or 0) for o in objs)
        b_sc_count = {}
        for o in objs:
            sc = o.get("storage_class") or "STANDARD"
            b_sc_count[sc] = b_sc_count.get(sc, 0) + 1
            storage_class_count[sc] = storage_class_count.get(sc, 0) + 1
            storage_class_size[sc] = storage_class_size.get(sc, 0) + int(o.get("size") or 0)
        total_objects += b_count
        total_size += b_size

        if location:
            region_distribution[location] = region_distribution.get(location, 0) + 1
        bucket_reports.append({
            "name": name,
            "location": location or region,
            "location_source": "bucket" if location else "requested_region",
            "object_count": b_count,
            "total_size_bytes": b_size,
            "storage_class_distribution": b_sc_count,
        })

    if buckets and not any(b.get("location") for b in buckets):
        warnings.append(
            "当前执行路径未返回桶的真实区域（obsutil ls 不返回 location）；"
            "区域分布按请求 region=%s 归并。" % region)
        region_distribution[region] = len(buckets)

    stats = {
        "region": region,
        "bucket_filter": bucket_filter,
        "prefix": prefix or None,
        "generated_at": datetime.datetime.now(
            datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "bucket_count": len(buckets),
            "object_count": total_objects,
            "total_size_bytes": total_size,
            "total_size_human": _human_size(total_size),
        },
        "storage_class_distribution": storage_class_count,
        "storage_class_size_bytes": storage_class_size,
        "region_distribution": region_distribution,
        "buckets": bucket_reports,
        "truncated": bool(truncated),
        "warnings": warnings,
    }
    return stats


def collect_stats(region, bucket=None, prefix=None, executor="auto",
                  max_objects=DEFAULT_MAX_OBJECTS, bucket_lister=None,
                  object_lister=None):
    """Collect and aggregate OBS statistics for the requested scope."""
    warnings = []
    if executor == "sdk":
        warnings.append("使用 SDK 执行路径（huaweicloudsdkobs）。")

    if bucket_lister is None or object_lister is None:
        resolved_buckets, resolved_objects = resolve_listers(region, executor)
        bucket_lister = bucket_lister or resolved_buckets
        object_lister = object_lister or resolved_objects

    if bucket:
        # Single-bucket scope: keep the requested bucket, resolve its location
        # from the account bucket list when the path provides it.
        buckets = [{"name": bucket}]
        try:
            for candidate in bucket_lister(region):
                if candidate.get("name") == bucket:
                    if candidate.get("location"):
                        buckets[0]["location"] = candidate["location"]
                    break
        except ObsStatsError:
            raise
        except Exception:
            pass
    else:
        buckets = bucket_lister(region)

    objects_by_bucket = {}
    truncated = False
    for b in buckets:
        objs, b_truncated = object_lister(b.get("name", ""), prefix)
        objects_by_bucket[b.get("name", "")] = objs
        truncated = truncated or b_truncated
        if len(objs) >= max_objects:
            truncated = True

    if truncated:
        warnings.append(
            "对象数量达到上限（--max-objects=%d），统计结果为下界。" % max_objects)

    return aggregate(buckets, objects_by_bucket, region, prefix=prefix,
                     bucket_filter=bucket, truncated=truncated, warnings=warnings)


# ── rendering ────────────────────────────────────────────────────────────

def render_table(stats):
    lines = []
    summary = stats["summary"]
    lines.append("华为云 OBS 聚合统计（region=%s%s）" % (
        stats["region"],
        "，bucket=%s" % stats["bucket_filter"] if stats.get("bucket_filter") else "",
    ))
    if stats.get("prefix"):
        lines.append("统计前缀（prefix）：%s" % stats["prefix"])
    lines.append("桶数量(bucket_count): %d" % summary["bucket_count"])
    lines.append("对象数量(object_count): %d" % summary["object_count"])
    lines.append("总容量(total_size): %d B (%s)" % (
        summary["total_size_bytes"], summary["total_size_human"]))
    if stats["truncated"]:
        lines.append("注意：结果被截断（truncated=true），以上为下界。")

    lines.append("")
    lines.append("[按存储类别分布]")
    lines.append("  storage_class  object_count  size_bytes")
    lines.append("  -------------  ------------  ----------")
    sc_dist = stats["storage_class_distribution"]
    sc_size = stats["storage_class_size_bytes"]
    if sc_dist:
        for sc in sorted(sc_dist):
            lines.append("  %-13s  %12d  %10d" % (sc, sc_dist[sc], sc_size.get(sc, 0)))
    else:
        lines.append("  （无对象）")

    lines.append("")
    lines.append("[按区域分布]")
    lines.append("  region  bucket_count")
    lines.append("  ------  ------------")
    for reg in sorted(stats["region_distribution"]):
        lines.append("  %-6s  %12d" % (reg, stats["region_distribution"][reg]))

    lines.append("")
    lines.append("[按桶明细]")
    lines.append("  bucket  location  object_count  size_bytes")
    lines.append("  ------  --------  ------------  ----------")
    for b in stats["buckets"]:
        lines.append("  %-6s  %-8s  %12d  %10d" % (
            b["name"], b["location"], b["object_count"], b["total_size_bytes"]))
    return "\n".join(lines)


def render_markdown(stats):
    summary = stats["summary"]
    lines = []
    lines.append("# 华为云 OBS 聚合统计")
    lines.append("")
    lines.append("- Region：`%s`" % stats["region"])
    if stats.get("bucket_filter"):
        lines.append("- Bucket：`%s`" % stats["bucket_filter"])
    if stats.get("prefix"):
        lines.append("- Prefix：`%s`" % stats["prefix"])
    lines.append("- 生成时间：`%s`" % stats["generated_at"])
    lines.append("")
    lines.append("## 汇总")
    lines.append("")
    lines.append("| 指标 | 值 |")
    lines.append("| --- | --- |")
    lines.append("| 桶数量 | %d |" % summary["bucket_count"])
    lines.append("| 对象数量 | %d |" % summary["object_count"])
    lines.append("| 总容量 | %d B（%s） |" % (
        summary["total_size_bytes"], summary["total_size_human"]))
    lines.append("| 结果截断 | %s |" % ("是" if stats["truncated"] else "否"))
    lines.append("")
    lines.append("## 存储类别分布")
    lines.append("")
    lines.append("| 存储类别 | 对象数量 | 容量(字节) |")
    lines.append("| --- | --- | --- |")
    sc_dist = stats["storage_class_distribution"]
    sc_size = stats["storage_class_size_bytes"]
    if sc_dist:
        for sc in sorted(sc_dist):
            lines.append("| %s | %d | %d |" % (sc, sc_dist[sc], sc_size.get(sc, 0)))
    else:
        lines.append("| （无对象） | 0 | 0 |")
    lines.append("")
    lines.append("## 区域分布")
    lines.append("")
    lines.append("| Region | 桶数量 |")
    lines.append("| --- | --- |")
    for reg in sorted(stats["region_distribution"]):
        lines.append("| %s | %d |" % (reg, stats["region_distribution"][reg]))
    lines.append("")
    lines.append("## 桶明细")
    lines.append("")
    lines.append("| Bucket | Region | 对象数量 | 容量(字节) |")
    lines.append("| --- | --- | --- | --- |")
    for b in stats["buckets"]:
        lines.append("| %s | %s | %d | %d |" % (
            b["name"], b["location"], b["object_count"], b["total_size_bytes"]))
    if stats.get("warnings"):
        lines.append("")
        lines.append("## 提示")
        lines.append("")
        for w in stats["warnings"]:
            lines.append("- %s" % w)
    return "\n".join(lines)


# ── entrypoint ───────────────────────────────────────────────────────────

def _build_parser():
    parser = argparse.ArgumentParser(
        description="华为云 OBS 只读聚合统计：桶数量 / 对象数量 / 总容量 / "
                    "存储类别分布 / 区域分布（hcloud OBS ls 优先，SDK 回退）。")
    parser.add_argument("-b", "--bucket", default=None, help="仅统计指定桶（默认统计账号全部桶）")
    parser.add_argument("-p", "--prefix", default="", help="限定统计的对象前缀（prefix）")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-o", "--output", default="table",
                        choices=["table", "json", "md"],
                        help="输出模式：table（默认）/ json / md")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="等价于 --output json")
    parser.add_argument("--md", action="store_true", dest="as_md",
                        help="等价于 --output md")
    parser.add_argument("--executor", default="auto",
                        choices=["auto", "cli", "sdk"],
                        help="执行方式：auto（默认，CLI 优先）/ cli / sdk")
    parser.add_argument("--max-objects", type=int, default=DEFAULT_MAX_OBJECTS,
                        dest="max_objects",
                        help="单桶最多统计对象数（上限，默认 %d）" % DEFAULT_MAX_OBJECTS)
    parser.add_argument("--endpoint", default=None,
                        help="自定义 OBS endpoint（默认 obs.<region>.myhuaweicloud.com）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud OBS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    mode = args.output
    if args.as_json:
        mode = "json"
    if args.as_md:
        mode = "md"

    raw_argv = argv if argv is not None else sys.argv[1:]
    try:
        guard_write_intent(" ".join(raw_argv))
        guard_operation(args.operation)
        stats = collect_stats(
            args.region, bucket=args.bucket, prefix=args.prefix,
            executor=args.executor, max_objects=args.max_objects)
    except ObsStatsError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if mode == "json":
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0
    if mode == "md":
        print(render_markdown(stats))
        return 0
    print(render_table(stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())