#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud OBS buckets (read-only).

Primary execution path is KooCLI's obsutil-backed OBS module:
    hcloud OBS ls [-limit=N] [-e=obs.<region>.myhuaweicloud.com]
(``hcloud OBS`` is obsutil-backed; listing buckets is ``ls`` with no cloud_url.
There is no PascalCase ``hcloud OBS ListBuckets`` command.)

When the hcloud binary is absent, the script falls back to the official
``huaweicloudsdkobs`` v1 SDK (``ObsClient.list_buckets``).

Supports three output modes (table / json / names), a strict write-intent guard
(any mutating OBS intent is rejected before a single command runs) and explicit
error classification (missing AK/SK / hcloud missing / auth failure / API error).

Usage:
    python3 scripts/list_obs_buckets.py [--region cn-north-4]
                                        [--output table|json|names]
                                        [--json] [--names-only]
                                        [--page-size 1000]

Environment overrides (mostly for tests):
    OBS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    OBS_LIST_HCLOUD_ARGS  extra args injected before the OBS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 1000
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
    "create-share",
    "createshare",
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
    "bucket_type",
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

# KooCLI / obsutil usage errors are printed with a [USE_ERROR] marker even when
# the return code looks successful — treat the marker as a hard failure.
_USE_ERROR_MARKER = "[use_error]"

_BUCKET_URL_RE = re.compile(r"obs://([A-Za-z0-9._\-]+)")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?")
_LOCATION_RE = re.compile(r"\b([a-z]{2}-[a-z]+-\d[a-z]?)\b")


class ObsListError(Exception):
    """Base error for the OBS bucket-list skill."""


class GuardError(ObsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ObsListError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(ObsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ObsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so ``--create-bucket``, ``CreateBucket`` and
    ``create_bucket`` hit the same keyword. Read-only vocabulary
    (list/show/get/describe/ls) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（OBS ListBuckets），创建/删除/上传/变更等操作已被守卫拦截。" % keyword
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
    account's buckets.  ``-limit`` caps the returned bucket count and
    ``-e`` pins the OBS endpoint to the requested region.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "-limit=%d" % limit,
        "-e=%s" % (endpoint or _endpoint_for_region(region)),
    ]
    return argv


def _hcloud_executable():
    return os.environ.get("OBS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("OBS_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
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
    present (e.g. ``-sc`` storage class), a creation date and a region are
    detected heuristically and attached as ``creation_date`` / ``location``.
    Duplicate names collapse to the first occurrence.
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
        buckets.append(record)
    return buckets


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


def bucket_names(buckets):
    names = []
    for bucket in buckets:
        name = bucket.get("name")
        names.append(str(name) if name not in (None, "") else "-")
    return names


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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云账号 OBS 桶列表（KooCLI hcloud OBS ls，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s，影响 OBS endpoint）" % DEFAULT_REGION)
    parser.add_argument("-o", "--output", default="table",
                        choices=["table", "json", "names"],
                        help="输出模式：table（默认）/ json / names")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="等价于 --output json")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="等价于 --output names")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="最大返回桶数（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--endpoint", default=None,
                        help="自定义 OBS endpoint（默认 obs.<region>.myhuaweicloud.com）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud OBS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    mode = args.output
    if args.as_json:
        mode = "json"
    if args.names_only:
        mode = "names"

    raw_argv = argv if argv is not None else sys.argv[1:]
    try:
        guard_write_intent(" ".join(raw_argv))
        guard_operation(args.operation)
        buckets = list_buckets(
            args.region, limit=args.page_size, endpoint=args.endpoint)
    except ObsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if mode == "json":
        print(json.dumps(buckets, ensure_ascii=False, indent=2))
        return 0

    if mode == "names":
        print("Region %s 的 OBS 桶名称列表（共 %d 个）：" % (args.region, len(buckets)))
        for name in bucket_names(buckets):
            print("- %s" % name)
        return 0

    if not buckets:
        print("当前账号（Region %s）无 OBS 桶。" % args.region)
        return 0

    print("华为云账号 OBS 桶列表（Region %s，共 %d 个）：" % (args.region, len(buckets)))
    print(render_table(buckets))
    return 0


if __name__ == "__main__":
    sys.exit(main())