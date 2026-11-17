#!/usr/bin/env python3
"""List Huawei Cloud APIG dedicated instances (and their APIs) via KooCLI.

Primary execution path is KooCLI:

* instances — ``hcloud APIG ListInstancesV2`` (read-only
  ``GET /v2/{project_id}/apigw/instances``)
* APIs of one instance — ``hcloud APIG ListApisV2`` (read-only
  ``GET /v2/{project_id}/apigw/instances/{instance_id}/apis``)

When the ``hcloud`` binary is absent the script falls back to the official
``huaweicloudsdkapig`` v2 SDK (``ApigClient.list_instances_v2`` /
``ApigClient.list_apis_v2``). The script never reads, echoes or stores
credentials — authentication is delegated to the KooCLI profile / SDK
environment.

Output modes: compact list (default), ``--table`` (full-field table) and
``--json`` (raw response records). Filters: ``--name`` (exact, ``--fuzzy`` for
substring), ``--instance-id`` (drill down to that instance's API list) and
``--status`` (client-side). ``--limit`` (1-100) caps the number of records and
drives offset/limit paging.

Strictly read-only: ``build_command()`` can only construct
``ListInstancesV2`` / ``ListApisV2``; any write intent
(create/delete/update/publish/offline/bind-eip/unbind-eip/...) is rejected by
the guard before a single command is executed.

Usage:
    python3 scripts/list_apig_instances.py [--region cn-north-4]
                                           [--json | --table]
                                           [--name my-apig] [--fuzzy]
                                           [--status Running]
                                           [--instance-id <id>]
                                           [--limit 100]

Environment overrides (mostly for tests):
    APIG_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    APIG_LIST_HCLOUD_ARGS  extra args injected before the APIG operation
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

DEFAULT_REGION = "cn-north-4"
DEFAULT_LIMIT = 100
MIN_LIMIT = 1
MAX_LIMIT = 100
# Records requested per API page (offset/limit paging). Kept below MAX_LIMIT so
# a `--limit 100` run really exercises multi-page collection.
PAGE_STEP = 50
MAX_PAGES = 100

SERVICE = "APIG"
OP_LIST_INSTANCES = "ListInstancesV2"
OP_LIST_APIS = "ListApisV2"
ALLOWED_OPERATIONS = (OP_LIST_INSTANCES, OP_LIST_APIS)

REST_PATH_INSTANCES = "/v2/{project_id}/apigw/instances"
REST_PATH_APIS = "/v2/{project_id}/apigw/instances/{instance_id}/apis"

# Options whose values are user-supplied filters/parameters. Their values are
# not scanned by the write-intent guard: an instance or API literally named
# `create-api` must not be mistaken for a mutating operation.
_VALUE_OPTIONS = (
    "--region",
    "-r",
    "--name",
    "--status",
    "--instance-id",
    "--limit",
    "--project-id",
)

# Mutating APIG operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createinstance",
    "deleteinstance",
    "updateinstance",
    "createinstances",
    "deleteinstances",
    "createapi",
    "deleteapi",
    "updateapi",
    "createorupdate",
    "publishapi",
    "offlineapi",
    "batchpublish",
    "batchoffline",
    "addeip",
    "deleteeip",
    "unbindeip",
    "bindeip",
    "addingress",
    "addengress",
    "createenvironment",
    "deleteenvironment",
    "createapp",
    "deleteapp",
    "create",
    "delete",
    "update",
    "modify",
    "publish",
    "offline",
    "unpublish",
    "bind",
    "unbind",
    "attach",
    "detach",
    "associate",
    "disassociate",
    "dissociate",
    "add",
    "remove",
    "release",
    "destroy",
    "change",
    "restart",
    "reset",
    "import",
    "export",
    "enable",
    "disable",
    "freeze",
    "migrate",
    "upgrade",
    "authorize",
    "cancel",
    "creating",
    "deleting",
    "updating",
)

# Preferred column order for the instance table; other fields are appended.
INSTANCE_PREFERRED_COLUMNS = (
    ("id", "实例ID"),
    ("instance_name", "名称"),
    ("status", "状态"),
    ("spec", "规格"),
    ("version", "版本"),
    ("available_zone", "可用区"),
    ("eip_address", "EIP"),
    ("vpc_id", "VPC"),
    ("create_time", "创建时间"),
)

API_PREFERRED_COLUMNS = (
    ("id", "API_ID"),
    ("name", "名称"),
    ("type", "类型"),
    ("version", "版本"),
    ("req_method", "请求方法"),
    ("req_protocol", "协议"),
    ("req_uri", "路径"),
    ("auth_type", "认证方式"),
    ("status", "状态"),
    ("group_name", "分组"),
    ("register_time", "注册时间"),
)

# Extra aliases used when a response spells the same concept differently.
_INSTANCE_COLUMN_ALIASES = {
    "version": ("version", "instance_version", "spec_version"),
    "available_zone": ("available_zone", "available_zones", "az", "zone_id"),
    "vpc_id": ("vpc_id", "vpc", "vpc_name"),
}

_CREDENTIAL_MISSING_PATTERNS = (
    "cli-ak",
    "cli-sk",
    "access key",
    "secret key",
    "credential",
    "configure",
    "未配置",
    "配置为空",
    "no ak",
    "no sk",
    "ak/sk",
)

_AUTH_PATTERNS = (
    "401",
    "403",
    "unauthorized",
    "forbidden",
    "apigw.0301",
    "apig.0301",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors on stdout WITH exit code 0 — the marker must be
# treated as a hard failure even when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class ApigListError(Exception):
    """Base error for the APIG instance list skill."""


class GuardError(ApigListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ApigListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(ApigListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ApigListError):
    """hcloud / network / unexpected API failure."""


class InstanceNotFoundError(ApigListError):
    """The requested --instance-id does not exist in the target region."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so ``--delete-api``, ``DeleteApiV2`` and
    ``delete_api`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（APIG ListInstancesV2 / ListApisV2），实例与 API 的创建、删除、"
                "更新、发布、下线、绑定/解绑 EIP 等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_scan_text(argv):
    """Build the guard scan text, keeping operation/command tokens only.

    Values of user-facing filter options (``--name`` / ``--status`` /
    ``--instance-id`` / ...) are dropped so a legitimate read-only query is
    never blocked just because a resource name contains a mutating verb.
    """
    tokens = []
    skip_next = False
    for token in argv:
        if skip_next:
            skip_next = False
            continue
        if token in _VALUE_OPTIONS:
            tokens.append(token)
            skip_next = True
            continue
        matched = False
        for option in _VALUE_OPTIONS:
            if token.startswith(option + "="):
                tokens.append(option)
                matched = True
                break
        if not matched:
            tokens.append(token)
    return " ".join(tokens)


def guard_operation(operation):
    """Only the read-only list operations may be executed."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, " / ".join(ALLOWED_OPERATIONS))
        )
    return True


def _page_size(limit):
    """Records requested per page: --limit capped at the paging step."""
    return max(1, min(int(limit), PAGE_STEP, MAX_LIMIT))


def build_instance_command(region, limit=DEFAULT_LIMIT, offset=0,
                           instance_id=None):
    """Build the hcloud APIG ListInstancesV2 argv (without the executable).

    Real KooCLI parameters (verified with ``hcloud APIG ListInstancesV2
    --help``): ``--cli-region``, ``--project_id`` (resolved from the profile),
    ``--limit`` (1-500), ``--offset`` and the server-side filters
    ``--instance_id`` / ``--instance_name`` / ``--status``. ``--name`` /
    ``--status`` are applied client-side by this skill (so ``--fuzzy`` works);
    only ``--instance_id`` is forwarded, for the existence check.
    """
    argv = [
        SERVICE,
        OP_LIST_INSTANCES,
        "--cli-region=%s" % region,
        "--limit=%d" % max(1, min(int(limit), MAX_LIMIT)),
        "--offset=%d" % max(0, int(offset)),
    ]
    if instance_id:
        argv.append("--instance_id=%s" % instance_id)
    return argv


def build_apis_command(region, instance_id, limit=DEFAULT_LIMIT, offset=0):
    """Build the hcloud APIG ListApisV2 argv (without the executable).

    ``instance_id`` is a **required path parameter** of
    ``GET /v2/{project_id}/apigw/instances/{instance_id}/apis``.
    """
    if not instance_id:
        raise GuardError(
            "ListApisV2 必须提供 instance_id（路径参数）：本 skill 只允许"
            "按实例下钻查询 API 列表。"
        )
    return [
        SERVICE,
        OP_LIST_APIS,
        "--cli-region=%s" % region,
        "--instance_id=%s" % instance_id,
        "--limit=%d" % max(1, min(int(limit), MAX_LIMIT)),
        "--offset=%d" % max(0, int(offset)),
    ]


def _hcloud_executable():
    return os.environ.get("APIG_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    # APIG_LIST_HCLOUD_ARGS is a test-only hook (inject fake CLI flags such as
    # `--cli-profile`); it must never be used in production to smuggle extra
    # CLI tokens, so it is documented here rather than exposed in the CLI help.
    extra = os.environ.get("APIG_LIST_HCLOUD_ARGS", "").split()
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
            "未找到 hcloud（KooCLI）。请先安装 KooCLI 并完成认证配置，"
            "参见 references/cli-installation-guide.md。"
        )
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（120s），请检查网络后重试。")
    return proc.stdout or "", proc.stderr or "", proc.returncode


def extract_json(stdout):
    """Parse hcloud stdout as JSON; tolerate wrapper/noise lines."""
    text = (stdout or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = ((stderr or "") + " " + (stdout or "")).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）："
            "APIG ListInstancesV2 / ListApisV2 的真实参数清单可通过 "
            "`hcloud APIG ListInstancesV2 --help` 查看。详情：%s"
            % (returncode, blob[:300])
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _AUTH_PATTERNS):
        if (re.search(r"\b401\b", low) and not re.search(r"\b403\b", low)) \
                or "apigw.0301" in low or "apig.0301" in low:
            return AuthError(
                "凭证无效（401：AK/SK 无效或已过期），请重新配置 hcloud 凭证后重试，"
                "参见 references/cli-installation-guide.md。详情：%s" % blob[:300]
            )
        return AuthError(
            "无权限访问 APIG 实例，请检查 IAM 权限（403：未授予 "
            "apig:instances:list / apig:apis:list 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def _payload_error(payload):
    """Return the error text if an APIG payload is an error envelope.

    KooCLI returns HTTP-level API errors (e.g. ``{"error_code": "APIGW.0301",
    "error_msg": "..."}``) on **stdout with exit code 0**. Such an envelope has
    no record list key, so it must be surfaced as an explicit error instead of
    being read as an empty list.
    """
    if not isinstance(payload, dict):
        return None
    if isinstance(payload.get("instances"), list) or isinstance(
            payload.get("apis"), list):
        return None
    err = payload.get("error")
    if isinstance(err, dict):
        code = str(err.get("error_code") or err.get("code") or "")
        msg = str(err.get("error_msg") or err.get("message") or "")
        text = ("%s %s" % (code, msg)).strip()
        return text or None
    if isinstance(err, str) and err.strip():
        return err.strip()
    code = payload.get("error_code") or payload.get("errorCode")
    msg = (payload.get("error_msg") or payload.get("errorMsg")
           or payload.get("error_message") or payload.get("message"))
    text = ("%s %s" % (code or "", msg or "")).strip()
    return text or None


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def extract_records(payload, list_key, total_key="total"):
    """Return (records, total) from a list response payload."""
    if isinstance(payload, list):
        return payload, None
    if not isinstance(payload, dict):
        return [], None
    records = payload.get(list_key)
    if not isinstance(records, list):
        return [], None
    total = payload.get(total_key)
    try:
        total = int(total) if total is not None else None
    except (TypeError, ValueError):
        total = None
    return records, total


# Whitelisted credential environment variables — read by name only, never by
# enumerating os.environ (avoids harvesting unrelated environment variables).
_AK_ENV_NAMES = (
    "HW_ACCESS_KEY",
    "HUAWEI_ACCESS_KEY",
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_CLOUD_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HW_SECRET_KEY",
    "HUAWEI_SECRET_KEY",
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_CLOUD_SECRET_KEY",
)
_PROJECT_ID_ENV_NAMES = (
    "HW_PROJECT_ID",
    "HUAWEI_PROJECT_ID",
    "HUAWEICLOUD_SDK_PROJECT_ID",
    "HUAWEI_CLOUD_PROJECT_ID",
)


def _env_value(names):
    """Read the first non-empty value from an explicit whitelist of env names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def resolve_project_id(explicit=None):
    """Resolve the project id from --project-id or the whitelisted env names."""
    if explicit:
        return explicit
    return _env_value(_PROJECT_ID_ENV_NAMES)


def _sdk_auth_error(exc):
    """Build an AuthError distinguishing 401 (bad credentials) from 403."""
    low = str(exc).lower()
    status = getattr(exc, "status_code", None)
    detail = str(exc)[:300]
    if status == 401 or "401" in low or "unauthorized" in low \
            or "apigw.0301" in low or "apig.0301" in low:
        return AuthError(
            "凭证无效（401：AK/SK 无效或已过期），请重新配置 AK/SK 后重试，参见"
            " references/cli-installation-guide.md。详情：%s" % detail
        )
    return AuthError(
        "无权限访问 APIG 实例，请检查 IAM 权限（403：未授予 "
        "apig:instances:list / apig:apis:list 只读权限），"
        "参见 references/iam-policies.md。详情：%s" % detail
    )


def _build_sdk_client(region, project_id=None):
    """Build a `huaweicloudsdkapig` v2 ApigClient (SDK fallback only)."""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkapig.v2 import ApigClient
        from huaweicloudsdkapig.v2.region.apig_region import ApigRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkapig "
            "未安装，无法回退到 SDK。请安装 KooCLI 或 pip install "
            "huaweicloudsdkcore huaweicloudsdkapig。详情：%s" % exc
        )

    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HW_ACCESS_KEY / HUAWEI_ACCESS_KEY / "
            "HUAWEICLOUD_SDK_AK 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    resolved_project_id = resolve_project_id(project_id)
    if not resolved_project_id:
        raise ConfigError(
            "SDK 回退缺少 project_id：APIG 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。"
            % REST_PATH_INSTANCES
        )
    credentials = BasicCredentials(
        ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = ApigRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://apig.%s.myhuaweicloud.com" % region)
        return ApigClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkapig 安装与区域配置。"
            % (region, exc)
        )


def _sdk_call(call, request):
    """Run one SDK call, mapping auth failures to explicit domain errors."""
    try:
        return call(request)
    except Exception as exc:
        low = str(exc).lower()
        status = getattr(exc, "status_code", None)
        if any(p in low for p in _AUTH_PATTERNS) or status in (401, 403):
            raise _sdk_auth_error(exc)
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])


def list_instances_via_sdk(region, limit=DEFAULT_LIMIT, instance_id=None,
                           project_id=None, max_pages=MAX_PAGES):
    """SDK fallback: query APIG instances through `huaweicloudsdkapig` v2."""
    from huaweicloudsdkapig.v2 import ListInstancesV2Request

    client = _build_sdk_client(region, project_id=project_id)
    records = []
    offset = 0
    for _ in range(max_pages):
        size = _page_size(limit)
        request = ListInstancesV2Request(
            offset=offset,
            limit=size,
            instance_id=instance_id or None,
        )
        response = _sdk_call(client.list_instances_v2, request)
        batch = list(response.instances or [])
        records.extend(_jsonable(item.to_dict()) for item in batch)
        if len(records) >= limit or len(batch) < size:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records[:limit]


def list_apis_via_sdk(region, instance_id, limit=DEFAULT_LIMIT,
                      project_id=None, max_pages=MAX_PAGES):
    """SDK fallback: query one instance's APIs through `huaweicloudsdkapig` v2."""
    if not instance_id:
        raise GuardError(
            "ListApisV2 必须提供 instance_id（路径参数）：本 skill 只允许"
            "按实例下钻查询 API 列表。"
        )
    from huaweicloudsdkapig.v2 import ListApisV2Request

    client = _build_sdk_client(region, project_id=project_id)
    records = []
    offset = 0
    for _ in range(max_pages):
        size = _page_size(limit)
        request = ListApisV2Request(
            instance_id=instance_id,
            offset=offset,
            limit=size,
        )
        response = _sdk_call(client.list_apis_v2, request)
        batch = list(response.apis or [])
        records.extend(_jsonable(item.to_dict()) for item in batch)
        if len(records) >= limit or len(batch) < size:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records[:limit]


def _call_hcloud_page(build_page, list_key, limit, max_pages=MAX_PAGES,
                      sdk_fallback=None):
    """Paged read: KooCLI first, one-shot SDK fallback when hcloud is missing."""
    records = []
    offset = 0
    for _ in range(max_pages):
        size = _page_size(limit)
        argv = build_page(size, offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            if sdk_fallback is None:
                raise
            return sdk_fallback()
        stdout, stderr = stdout or "", stderr or ""
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        # KooCLI prints HTTP-level API errors on stdout with exit code 0;
        # handle them before extract_records(), otherwise a 403 would be
        # silently read as an empty list (exit 0).
        envelope_error = _payload_error(payload)
        if envelope_error:
            raise classify_hcloud_failure(envelope_error, stderr, returncode)
        batch, total = extract_records(payload, list_key)
        records.extend(batch)
        if len(records) >= limit or not batch or len(batch) < size:
            break
        if total is not None and offset + len(batch) >= total:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records[:limit]


def list_instances(region, limit=DEFAULT_LIMIT, instance_id=None,
                   project_id=None):
    """Query APIG instances (offset/limit paged); KooCLI first, SDK fallback."""
    return _call_hcloud_page(
        lambda size, offset: build_instance_command(
            region, limit=size, offset=offset, instance_id=instance_id),
        "instances",
        limit,
        sdk_fallback=lambda: list_instances_via_sdk(
            region, limit=limit, instance_id=instance_id, project_id=project_id),
    )


def list_apis(region, instance_id, limit=DEFAULT_LIMIT, project_id=None):
    """Query one APIG instance's APIs (offset/limit paged); CLI first, SDK fallback."""
    return _call_hcloud_page(
        lambda size, offset: build_apis_command(
            region, instance_id, limit=size, offset=offset),
        "apis",
        limit,
        sdk_fallback=lambda: list_apis_via_sdk(
            region, instance_id, limit=limit, project_id=project_id),
    )


def _field(record, *names, default="-"):
    for name in names:
        if name in record and record[name] not in (None, ""):
            return record[name]
    return default


def filter_records(records, name=None, fuzzy=False, status=None,
                   name_keys=("instance_name", "name")):
    """Client-side --name / --status filtering (fuzzy = substring match)."""
    result = []
    wanted_status = str(status).lower() if status is not None else None
    wanted_name = str(name).lower() if name else None
    for record in records:
        if wanted_name:
            value = _field(record, *name_keys, default=None)
            if value is None:
                continue
            value = str(value).lower()
            if fuzzy:
                if wanted_name not in value:
                    continue
            elif value != wanted_name:
                continue
        if wanted_status is not None:
            value = _field(record, "status", default=None)
            if value is None or str(value).lower() != wanted_status:
                continue
        result.append(record)
    return result


def find_instance(region, instance_id, project_id=None):
    """Return the instance record for `instance_id`, or None when absent."""
    records = list_instances(region, limit=MIN_LIMIT, instance_id=instance_id,
                             project_id=project_id)
    for record in records:
        if str(_field(record, "id", default="")) == str(instance_id):
            return record
    return records[0] if records else None


def format_create_time(value):
    """Render an APIG millisecond epoch timestamp as UTC datetime text."""
    if value in (None, "", "-"):
        return "-"
    try:
        number = int(value)
    except (TypeError, ValueError):
        return str(value)
    # APIG instance create_time is epoch **milliseconds**.
    if number > 10 ** 11:
        number = number / 1000.0
    try:
        return datetime.fromtimestamp(number, tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC")
    except (OverflowError, OSError, ValueError):
        return str(value)


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _render_table(records, preferred, aliases=None):
    """Render the fixed-column table (missing fields show as ``-``).

    ``--json`` carries the complete raw response; the table deliberately keeps
    the documented column set so it stays readable in a terminal.
    """
    aliases = aliases or {}
    rows_data = [dict(record) for record in records]
    columns = [(key, label) for key, label in preferred]
    rows = []
    for record in rows_data:
        row = []
        for key, _label in columns:
            names = aliases.get(key, (key,))
            row.append(_cell(_field(record, *names)))
        rows.append(row)
    widths = [max(len(label), *(len(row[i]) for row in rows))
              for i, (_key, label) in enumerate(columns)]
    header = "  ".join(label.ljust(widths[i])
                       for i, (_key, label) in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def render_instance_table(instances):
    """Full-field table for instances."""
    prepared = []
    for instance in instances:
        item = dict(instance)
        if "create_time" in item:
            item["create_time"] = format_create_time(item["create_time"])
        prepared.append(item)
    return _render_table(prepared, INSTANCE_PREFERRED_COLUMNS,
                         aliases=_INSTANCE_COLUMN_ALIASES)


def render_api_table(apis):
    """Full-field table for APIs."""
    return _render_table(apis, API_PREFERRED_COLUMNS)


def compact_instance_lines(instances):
    """Default compact landscape: one line per instance (名称 / ID / 状态)."""
    lines = []
    for instance in instances:
        lines.append("- %s  %s  %s" % (
            _field(instance, "instance_name", "name"),
            _field(instance, "id"),
            _field(instance, "status"),
        ))
    return lines


def compact_api_lines(apis):
    """Default compact landscape: one line per API (名称 / 方法 路径 / ID / 状态)."""
    lines = []
    for api in apis:
        lines.append("- %s  %s %s  %s  %s" % (
            _field(api, "name"),
            _field(api, "req_method"),
            _field(api, "req_uri"),
            _field(api, "id"),
            _field(api, "status"),
        ))
    return lines


def _limit_type(value):
    """Validate --limit against the documented 1-100 range."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("--limit 必须是整数：%r" % value)
    if not MIN_LIMIT <= number <= MAX_LIMIT:
        raise argparse.ArgumentTypeError(
            "--limit 超出范围（%d-%d）：%d。" % (MIN_LIMIT, MAX_LIMIT, number))
    return number


def _empty_hint(region, args):
    filters = []
    if args.name:
        filters.append("name%s%s" % ("~" if args.fuzzy else "=", args.name))
    if args.status:
        filters.append("status=%s" % args.status)
    if filters:
        return "当前区域（%s）无 APIG 专享版实例（过滤条件: %s）。" % (
            region, ", ".join(filters))
    return "当前区域（%s）无 APIG 专享版实例。" % region


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]
    # Write-intent guard runs BEFORE argparse: a mutating flag such as
    # `--delete-api` must be rejected with exit code 1 (guard error) instead of
    # argparse's "unrecognized arguments" exit code 2.
    try:
        guard_write_intent(guard_scan_text(raw_argv))
    except GuardError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description="查询华为云 APIG 专享版实例列表（可选下钻实例 API 列表），"
                    "KooCLI hcloud APIG ListInstancesV2 / ListApisV2，只读。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出原始响应记录")
    parser.add_argument("--table", action="store_true", dest="as_table",
                        help="输出完整字段表格（默认仅简洁列表）")
    parser.add_argument("--name", help="按实例名（下钻时为 API 名）过滤，默认精确匹配")
    parser.add_argument("--fuzzy", action="store_true",
                        help="--name 使用模糊（子串）匹配")
    parser.add_argument("--instance-id", dest="instance_id",
                        help="下钻指定实例：先校验实例存在，再列出该实例的 API 列表")
    parser.add_argument("--status", help="按状态过滤（客户端过滤）")
    parser.add_argument("--limit", type=_limit_type, default=DEFAULT_LIMIT,
                        help="最多返回的记录数（%d-%d，默认 %d；超出则自动分页）"
                             % (MIN_LIMIT, MAX_LIMIT, DEFAULT_LIMIT))
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v2/{project_id}/apigw/... "
                             "路径中需要）")
    args = parser.parse_args(argv)

    try:
        if args.instance_id:
            guard_operation(OP_LIST_APIS)
            instance = find_instance(args.region, args.instance_id,
                                     project_id=args.project_id)
            if instance is None:
                raise InstanceNotFoundError(
                    "实例不存在：region %s 下未找到实例 %s。请通过"
                    " `python3 scripts/list_apig_instances.py --region %s` 确认"
                    " 实例 ID。" % (args.region, args.instance_id, args.region)
                )
            apis = list_apis(args.region, args.instance_id, limit=args.limit,
                             project_id=args.project_id)
            apis = filter_records(apis, name=args.name, fuzzy=args.fuzzy,
                                  status=args.status,
                                  name_keys=("name", "id"))
            if args.as_json:
                print(json.dumps({
                    "region": args.region,
                    "instance_id": args.instance_id,
                    "instance": instance,
                    "count": len(apis),
                    "apis": apis,
                }, ensure_ascii=False, indent=2))
                return 0
            if not apis:
                filters = "（name=%s%s, status=%s）" % (
                    args.name, " fuzzy" if args.fuzzy else "", args.status
                ) if (args.name or args.status) else ""
                print("实例 %s（%s）下无 API%s。" % (
                    args.instance_id, args.region, filters))
                return 0
            print("Region %s 实例 %s 的 API 列表（共 %d 个）：" % (
                args.region, args.instance_id, len(apis)))
            if args.as_table:
                print(render_api_table(apis))
            else:
                for line in compact_api_lines(apis):
                    print(line)
            return 0

        guard_operation(OP_LIST_INSTANCES)
        instances = list_instances(args.region, limit=args.limit,
                                   project_id=args.project_id)
        instances = filter_records(instances, name=args.name,
                                   fuzzy=args.fuzzy, status=args.status)
    except ApigListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps({
            "region": args.region,
            "count": len(instances),
            "instances": instances,
        }, ensure_ascii=False, indent=2))
        return 0

    if not instances:
        print(_empty_hint(args.region, args))
        return 0

    print("Region %s 的 APIG 专享版实例（共 %d 个）：" % (
        args.region, len(instances)))
    if args.as_table:
        print(render_instance_table(instances))
    else:
        for line in compact_instance_lines(instances):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())