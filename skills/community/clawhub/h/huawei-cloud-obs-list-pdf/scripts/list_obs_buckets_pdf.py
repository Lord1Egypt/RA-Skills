#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud OBS buckets (read-only) and export a local PDF report.

Brings the ``huawei-cloud-obs-list`` query paradigm together with a local PDF
export. Primary execution path is KooCLI's obsutil-backed OBS module::

    hcloud OBS ls [-limit=N] [-e=obs.<region>.myhuaweicloud.com]

(``hcloud OBS`` is obsutil-backed; listing buckets is ``ls`` with no cloud_url.)
When the hcloud binary is absent, the script falls back to the official
``huaweicloudsdkobs`` v1 SDK (``ObsClient.list_buckets``).

Three output modes are supported:

- ``--format pdf`` (default): write the bucket list into a ``.pdf`` report
  (headers 桶名称 / 创建时间 / 区域 / 存储类别 / 桶策略, optional summary row) via the
  bundled ``export_pdf`` module (reportlab preferred, fpdf2 fallback).
- ``--format table``: aligned table on stdout.
- ``--format json``: structured JSON array for downstream tooling.

A strict write-intent guard rejects any mutating OBS intent so writes never
happen: the only operation ever constructed is read-only ``hcloud OBS ls`` (or
the SDK ``list_buckets`` fallback). No data is ever written back to OBS — the
PDF file is produced locally only.

Usage:
    python3 scripts/list_obs_buckets_pdf.py [--region cn-north-4]
                                            [--format pdf|table|json]
                                            [--output /path/out.pdf]
                                            [--summary]
                                            [--page-size 1000]

Environment overrides (mostly for tests):
    OBS_LIST_PDF_HCLOUD_BIN   hcloud executable (default "hcloud")
    OBS_LIST_PDF_HCLOUD_ARGS  extra args appended AFTER the read-only
                              ``OBS ls`` arguments (guard-scanned, ls-only)
"""

import argparse
import json
import os
import re
import subprocess
import sys

from export_pdf import (
    ExportError,
    PDF_HEADERS,
    default_output_path,
    export_pdf,
)

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 1000
DEFAULT_FORMAT = "pdf"
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
    "createshare",
    "create-share",
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

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "creation_date",
    "location",
    "storage_class",
    "policy",
]

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

# KooCLI / obsutil usage errors carry a [USE_ERROR] marker even on a zero return
# code — the marker is treated as a hard failure.
_USE_ERROR_MARKER = "[use_error]"

_BUCKET_URL_RE = re.compile(r"obs://([A-Za-z0-9._\-]+)")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?")
_LOCATION_RE = re.compile(r"\b([a-z]{2}-[a-z]+-\d[a-z]?)\b")
_STORAGE_CLASS_RE = re.compile(
    r"\b(Standard|Standard[- ]IA|Infrequent Access|Warm|Cold|Archive|Deep Archive|glacier)\b",
    re.IGNORECASE,
)
_POLICY_RE = re.compile(
    r"\b(private|public[- ]read[- ]?write|public[- ]read|authenticated[- ]read"
    r"|bucket[- ]owner[- ]full[- ]control)\b",
    re.IGNORECASE,
)


class ObsListError(Exception):
    """Base error for the OBS bucket-list PDF skill."""


class GuardError(ObsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ObsListError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(ObsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ObsListError):
    """hcloud / network / unexpected API failure."""


def _screen_output_value(raw_argv):
    """Return the raw argv without the ``--output`` path value.

    The local .pdf output path is not an OBS operation, so a legitimate path
    such as ``/tmp/downloads/buckets.pdf`` must not trip the write-intent
    guard. Only the *value* following ``--output``/``-o`` is removed; every
    other argument is still scanned verbatim.
    """
    result = []
    skip_next = False
    for token in raw_argv or []:
        if skip_next:
            skip_next = False
            continue
        if token in ("--output", "-o"):
            result.append(token)
            skip_next = True
            continue
        if token.startswith("--output=") or token.startswith("-o="):
            result.append(token.split("=", 1)[0] + "=<path>")
            continue
        result.append(token)
    return result


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-bucket``, ``CreateBucket`` and
    ``create_bucket`` hit the same keyword. Read-only vocabulary
    (list/show/get/describe/ls) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（OBS ListBuckets）并仅在本机生成 PDF 报表，"
                "创建/删除/上传/变更等操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only obsutil ``ls`` operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s（列出桶）。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def _endpoint_for_region(region):
    return "obs.%s.myhuaweicloud.com" % region


def build_command(region, limit=DEFAULT_PAGE_SIZE, endpoint=None):
    """Build the hcloud argv (without the executable).

    ``hcloud OBS`` is obsutil-backed; ``ls`` with no cloud_url lists the
    account's buckets. ``-limit`` caps the returned bucket count and ``-e``
    pins the OBS endpoint to the requested region.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "-limit=%d" % limit,
        "-e=%s" % (endpoint or _endpoint_for_region(region)),
    ]
    return argv


def _hcloud_executable():
    return os.environ.get("OBS_LIST_PDF_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    cmd.extend(argv)
    extra = os.environ.get("OBS_LIST_PDF_HCLOUD_ARGS", "").split()
    if extra:
        # Extra args may only tail the read-only ``OBS ls`` argv (they can
        # never rewrite the service/operation) and are guard-scanned for
        # write intent before being appended.
        guard_write_intent(" ".join(extra))
        cmd.extend(extra)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=120, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。请先安装 KooCLI 及其 obsutil 组件并完成配置，"
            "参见 references/cli-installation-guide.md。"
        )
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（120s），请检查网络后重试。")
    return proc.stdout or "", proc.stderr or "", proc.returncode


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：OBS 桶列表使用 "
            "obsutil 风格的 `hcloud OBS ls`，可通过 `hcloud OBS ls --help` 查看参数。"
            "详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 OBS，请检查 IAM 权限或 AK/SK 是否有效"
            "（403 / InvalidAccessKeyId / SignatureDoesNotMatch），参见"
            " references/iam-policies.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS):
        return ConfigError(
            "缺少 AK/SK 凭证：obsutil 未配置有效凭证或 endpoint。请在会话外运行 "
            "`hcloud obs config`（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def parse_cli_buckets(stdout):
    """Parse obsutil ``ls`` output into a list of bucket dicts.

    Each ``obs://<name>`` token becomes one bucket. When extra columns are
    present, a creation date, region, storage class and bucket policy are
    detected heuristically and attached as ``creation_date`` / ``location`` /
    ``storage_class`` / ``policy``. Duplicate names collapse to the first
    occurrence.
    """
    buckets = []
    seen = set()
    for line in (stdout or "").splitlines():
        match = _BUCKET_URL_RE.search(line)
        if not match:
            continue
        name = match.group(1)
        if name in seen:
            continue
        seen.add(name)
        record = {"name": name}
        rest = line[match.end():]
        date_match = _DATE_RE.search(rest)
        if date_match:
            record["creation_date"] = date_match.group(0)
        loc_match = _LOCATION_RE.search(rest)
        if loc_match:
            record["location"] = loc_match.group(1)
        sc_match = _STORAGE_CLASS_RE.search(rest)
        if sc_match:
            record["storage_class"] = _titlecase_storage_class(sc_match.group(0))
        pol_match = _POLICY_RE.search(rest)
        if pol_match:
            record["policy"] = pol_match.group(0).lower()
        buckets.append(record)
    return buckets


def _titlecase_storage_class(token):
    mapping = {
        "standard-ia": "Standard-IA",
        "infrequent access": "Standard-IA",
        "standard": "Standard",
        "warm": "Warm",
        "cold": "Cold",
        "archive": "Archive",
        "deep archive": "Deep Archive",
        "glacier": "Glacier",
    }
    return mapping.get(token.lower(), token)


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


def list_buckets_via_sdk(region, page_size=DEFAULT_PAGE_SIZE):
    """SDK fallback: list buckets through ``huaweicloudsdkobs`` v1.

    Only invoked when hcloud is not installed. Credentials come from the
    standard environment variables (never literals). Region resolution uses the
    SDK's own ``ObsRegion`` catalog (official endpoints — no guessing).
    """
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
        from huaweicloudsdkobs.v1.model import ListBucketsRequest
        from huaweicloudsdkcore.http.http_config import HttpConfig
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkobs "
            "未安装，无法回退到 SDK。请安装 KooCLI 或先运行 "
            "`python3 scripts/ensure_env.py`（pip install "
            "huaweicloudsdkcore huaweicloudsdkobs）。详情：%s" % exc
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
        client = ObsClient.new_builder() \
            .with_http_config(HttpConfig.get_default_config()) \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .build()
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkobs 安装与区域"
            "配置。" % (region, exc)
        )
    try:
        response = client.list_buckets(ListBucketsRequest())
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问 OBS，请检查 IAM 权限或 AK/SK 是否有效（403）。详情：%s"
                % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
    buckets_obj = getattr(response, "buckets", None)
    raw = getattr(buckets_obj, "bucket", None) or []
    return [normalize_sdk_bucket(b) for b in raw]


def normalize_sdk_bucket(bucket):
    record = {"name": getattr(bucket, "name", None) or "-"}
    creation_date = getattr(bucket, "creation_date", None)
    location = getattr(bucket, "location", None)
    if creation_date:
        record["creation_date"] = creation_date
    if location:
        record["location"] = location
    storage_class = getattr(bucket, "storage_class", None)
    if storage_class:
        record["storage_class"] = storage_class
    policy = getattr(bucket, "policy", None)
    if policy:
        record["policy"] = policy
    return record


def list_buckets(region, limit=DEFAULT_PAGE_SIZE, endpoint=None):
    """Query the account's OBS buckets; KooCLI first, SDK fallback."""
    argv = build_command(region, limit=limit, endpoint=endpoint)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        # hcloud binary missing → one-shot SDK fallback (no CLI retry).
        return list_buckets_via_sdk(region, page_size=limit)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode)
    return parse_cli_buckets(stdout)


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(buckets):
    """Render a full-field table (union of all returned fields)."""
    rows_data = [dict(b) for b in buckets]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in r for r in rows_data):
            columns.append(key)
    for key in sorted({k for r in rows_data for k in r}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name"]
    rows = [[_cell(r.get(col, "-")) for col in columns] for r in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云账号 OBS 桶列表并导出 PDF 报表（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s，影响 OBS endpoint）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["table", "json", "pdf"],
                        help="输出格式：pdf（默认）/ table / json")
    parser.add_argument("-o", "--output", default=None,
                        help="PDF 输出路径（--format pdf；默认 "
                             "obs_buckets_<region>_<timestamp>.pdf）")
    parser.add_argument("--summary", action="store_true",
                        help="PDF 报表末尾追加汇总行（桶数量）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="最大返回桶数（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--endpoint", default=None,
                        help="自定义 OBS endpoint（默认 obs.<region>.myhuaweicloud.com）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud OBS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    raw_argv = argv if argv is not None else sys.argv[1:]

    try:
        guarding_text = " ".join(_screen_output_value(raw_argv))
        guard_write_intent(guarding_text)
        guard_operation(args.operation)
        buckets = list_buckets(args.region, limit=args.page_size, endpoint=args.endpoint)
    except ObsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    fmt = args.format
    if fmt == "json":
        print(json.dumps(buckets, ensure_ascii=False, indent=2))
        return 0

    if fmt == "table":
        if not buckets:
            print("当前账号（Region %s）无 OBS 桶。" % args.region)
            return 0
        print("华为云账号 OBS 桶列表（Region %s，共 %d 个）：" % (args.region, len(buckets)))
        print(render_table(buckets))
        return 0

    # fmt == "pdf": empty bucket list → friendly hint, never a broken file.
    if not buckets:
        print("当前账号（Region %s）无 OBS 桶，未生成 PDF 文件。" % args.region)
        return 0

    output_path = args.output or default_output_path(args.region)
    try:
        written = export_pdf(buckets, output_path,
                             summary=args.summary, region=args.region)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    print("已生成 OBS 桶列表 PDF 报表（Region %s，共 %d 个桶）：%s"
          % (args.region, len(buckets), written))
    return 0


if __name__ == "__main__":
    sys.exit(main())