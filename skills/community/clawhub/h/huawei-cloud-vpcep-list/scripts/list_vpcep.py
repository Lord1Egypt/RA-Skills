#!/usr/bin/env python3
"""List Huawei Cloud VPCEP endpoints / endpoint services / public services.

Primary execution path is KooCLI (read-only GET, verified against KooCLI
7.3.12 and the official `huaweicloudsdkvpcep` request models):

    hcloud VPCEP ListEndpoints             --cli-region=<region>   GET /v1/{project_id}/vpc-endpoints
    hcloud VPCEP ListEndpointService       --cli-region=<region>   GET /v1/{project_id}/vpc-endpoint-services
    hcloud VPCEP ListServicePublicDetails  --cli-region=<region>   GET /v1/{project_id}/vpc-endpoint-services/public

When hcloud is not installed the script falls back to the official
`huaweicloudsdkvpcep` SDK (v3 API, module path `huaweicloudsdkvpcep.v1`):
`VpcepClient.list_endpoints` / `list_endpoint_service` /
`list_service_public_details`.

Read-only by design: a write-intent guard rejects mutating vocabulary before
any command is executed. Supports three views, offset+limit paging, client-side
filters, concise/table/JSON/Markdown output, explicit Chinese error hints and
an isolated highlight section for non-available resources.

Usage:
    python3 scripts/list_vpcep.py [--view endpoint|service|public]
                                  [--region cn-north-4]
                                  [--name NAME] [--fuzzy]
                                  [--id ID] [--vpc-id VPC_ID]
                                  [--service-name NAME] [--status STATUS]
                                  [--table] [--json]
                                  [--format md] [--output FILE]
                                  [--page-size 100] [--project-id ID]
                                  [--sort-key create_at] [--sort-dir desc]

Environment overrides (mostly for tests):
    VPCEP_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    VPCEP_LIST_HCLOUD_ARGS  extra args injected before the VPCEP operation
"""

import argparse
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "VPCEP"

VIEW_ENDPOINT = "endpoint"
VIEW_SERVICE = "service"
VIEW_PUBLIC = "public"
VIEWS = (VIEW_ENDPOINT, VIEW_SERVICE, VIEW_PUBLIC)

OP_LIST_ENDPOINTS = "ListEndpoints"
OP_LIST_ENDPOINT_SERVICE = "ListEndpointService"
OP_LIST_SERVICE_PUBLIC_DETAILS = "ListServicePublicDetails"

VIEW_TO_OPERATION = {
    VIEW_ENDPOINT: OP_LIST_ENDPOINTS,
    VIEW_SERVICE: OP_LIST_ENDPOINT_SERVICE,
    VIEW_PUBLIC: OP_LIST_SERVICE_PUBLIC_DETAILS,
}
ALLOWED_OPERATIONS = (
    OP_LIST_ENDPOINTS,
    OP_LIST_ENDPOINT_SERVICE,
    OP_LIST_SERVICE_PUBLIC_DETAILS,
)

VIEW_LABEL = {
    VIEW_ENDPOINT: "终端节点",
    VIEW_SERVICE: "终端节点服务",
    VIEW_PUBLIC: "公共终端节点服务",
}

MAX_PAGE_SIZE = {
    VIEW_ENDPOINT: 500,
    VIEW_SERVICE: 1000,
    VIEW_PUBLIC: 1000,
}

# Official read-only REST paths, verified from the
# `huaweicloudsdkvpcep.v1.vpcep_client` `_list_*_http_info` metadata.
REST_PATH_ENDPOINTS = "/v1/{project_id}/vpc-endpoints"
REST_PATH_ENDPOINT_SERVICES = "/v1/{project_id}/vpc-endpoint-services"
REST_PATH_PUBLIC_SERVICES = "/v1/{project_id}/vpc-endpoint-services/public"

# Mutating VPCEP operations / intents — strictly rejected by the guard.
# State words (creating / available / deleting) are deliberately NOT listed:
# `--status creating` is a legitimate read-only filter.
WRITE_INTENT_KEYWORDS = (
    "createendpoint",
    "createendpointservice",
    "updateendpoint",
    "updateendpointservice",
    "deleteendpoint",
    "deleteendpointservice",
    "updateendpointconnectionsdesc",
    "updateendpointpolicy",
    "updateendpointroutetable",
    "updateendpointservicename",
    "updateendpointwhite",
    "upgradeendpoint",
    "batchaddendpointservicepermissions",
    "batchremoveendpointservicepermissions",
    "addendpointserviceserverresource",
    "removeendpointserviceserverresource",
    "addorremoveservicepermissions",
    "acceptorrejectendpoint",
    "batchaddorremoveresourceinstance",
    "create",
    "delete",
    "update",
    "modify",
    "batchadd",
    "batchremove",
    "addwhitelist",
    "removewhitelist",
    "addserverresource",
    "removeserverresource",
    "accept",
    "reject",
    "bind",
    "unbind",
    "associate",
    "disassociate",
    "dissociate",
    "attach",
    "detach",
    "release",
    "remove",
    "destroy",
    "change",
    "transfer",
    "restore",
    "enable",
    "disable",
    "import",
    "export",
    "restart",
)

# Fixed columns per view: (Chinese header, source field, renderer).
ENDPOINT_COLUMNS = (
    ("终端节点ID", "id", "text"),
    ("名称", "endpoint_service_name", "text"),
    ("状态", "status", "status"),
    ("所属服务名", "endpoint_service_name", "text"),
    ("服务ID", "endpoint_service_id", "text"),
    ("服务类型", "service_type", "text"),
    ("IP", "ip", "text"),
    ("VPC ID", "vpc_id", "text"),
    ("是否启用DNS", "enable_dns", "yesno"),
    ("是否启用白名单", "enable_whitelist", "yesno"),
    ("创建时间", "created_at", "text"),
)
SERVICE_COLUMNS = (
    ("服务ID", "id", "text"),
    ("名称", "service_name", "text"),
    ("状态", "status", "status"),
    ("后端类型", "server_type", "text"),
    ("创建时间", "created_at", "text"),
)
PUBLIC_COLUMNS = (
    ("服务ID", "id", "text"),
    ("名称", "service_name", "text"),
    ("服务类型", "service_type", "text"),
    ("创建时间", "created_at", "text"),
)
VIEW_COLUMNS = {
    VIEW_ENDPOINT: ENDPOINT_COLUMNS,
    VIEW_SERVICE: SERVICE_COLUMNS,
    VIEW_PUBLIC: PUBLIC_COLUMNS,
}

_ITEM_LIST_KEYS = ("endpoints", "endpoint_services", "endpointServices")

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
    "not authorized",
    "no identity-based policy",
    "permission denied",
    "认证失败",
    "权限不足",
    "apigw.0301",
)

_INVALID_ID_PATTERNS = (
    "invalid id",
    "invalid parameter",
    "invalid request",
    "bad request",
    "size must be between",
    "must be an",
    "sys.0400",
    "not found",
    "does not exist",
    "no such",
    "无效",
    "不存在",
    "格式错误",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class VpcepListError(Exception):
    """Base error for the VPCEP list skill."""


class GuardError(VpcepListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(VpcepListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(VpcepListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class InvalidRequestError(VpcepListError):
    """Invalid resource ID or unsupported query parameter."""


class ApiError(VpcepListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Separators are normalized so `--create-endpoint`, `CreateEndpoint`, and
    `create_endpoint` hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（VPCEP ListEndpoints / ListEndpointService / "
                "ListServicePublicDetails），创建/更新/删除/审批/白名单等变更操作"
                "已被守卫拦截。" % keyword
            )
    return False


_GUARD_EXEMPT_OPTIONS = (
    "--status",
    "--sort-key",
    "--sort-dir",
    "--view",
    "--format",
    "--region",
    "-r",
    "--page-size",
)


def guard_argv(argv):
    """Scan user argv for write intents, skipping benign query-only values.

    Values of `--status` (e.g. `rejected`), `--sort-key` (e.g. `update_at`) and
    similar read-only options legitimately contain mutating-looking words and
    must not trip the guard. Every other token — including `--name`, `--id`,
    `--service-name` and `--action` — is scanned.
    """
    tokens = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if token in _GUARD_EXEMPT_OPTIONS:
            index += 2
            continue
        if any(token.startswith(option + "=") for option in _GUARD_EXEMPT_OPTIONS):
            index += 1
            continue
        tokens.append(token)
        index += 1
    return guard_write_intent(" ".join(tokens))


def guard_operation(operation):
    """Only the three read-only list operations may be executed."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, " / ".join(ALLOWED_OPERATIONS))
        )
    return True


def resolve_operation(view=None, operation=None):
    """Resolve the concrete read-only operation from --view / --operation."""
    if operation:
        return operation
    return VIEW_TO_OPERATION.get(view or VIEW_ENDPOINT, OP_LIST_ENDPOINTS)


def _max_page_size(view):
    return MAX_PAGE_SIZE.get(view, 500)


def build_command(region, operation, view=VIEW_ENDPOINT, name=None,
                  item_id=None, vpc_id=None, service_name=None, status=None,
                  limit=DEFAULT_PAGE_SIZE, offset=0, sort_key=None,
                  sort_dir=None):
    """Build the hcloud VPCEP argv (without the executable).

    Mirrors the real KooCLI parameter lists verified with
    `hcloud VPCEP <Operation> --help` (KooCLI 7.3.12). Only read-only query
    parameters are ever added.
    """
    argv = [
        SERVICE,
        operation,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    server_name = service_name or name
    endpoint_like = view in (VIEW_ENDPOINT, VIEW_SERVICE, VIEW_PUBLIC)
    if server_name and endpoint_like:
        argv.append("--endpoint_service_name=%s" % server_name)
    if item_id:
        argv.append("--id=%s" % item_id)
    if vpc_id and view == VIEW_ENDPOINT:
        argv.append("--vpc_id=%s" % vpc_id)
    if status and view == VIEW_SERVICE:
        argv.append("--status=%s" % status)
    if sort_key:
        argv.append("--sort_key=%s" % sort_key)
    if sort_dir:
        argv.append("--sort_dir=%s" % sort_dir)
    return argv


def _hcloud_executable():
    return os.environ.get("VPCEP_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("VPCEP_LIST_HCLOUD_ARGS", "").split()
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
    text = stdout.strip()
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


def _payload_error(payload):
    """Return (code, message) when the payload is an API error body."""
    if not isinstance(payload, dict):
        return None, None
    code = payload.get("error_code") or payload.get("errorCode")
    message = (payload.get("error_msg") or payload.get("error_message")
               or payload.get("errorMessage") or payload.get("message"))
    if code or message:
        return code, message or ""
    error = payload.get("error")
    if isinstance(error, dict) and (error.get("code") or error.get("message")):
        return error.get("code"), error.get("message") or ""
    return None, None


def _classify_error_text(text, returncode, item_id=None, view=VIEW_ENDPOINT):
    blob = str(text or "").strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：VPCEP 列表操作"
            "真实参数清单可通过 `hcloud VPCEP %s --help` 查看。详情：%s"
            % (returncode, VIEW_TO_OPERATION.get(view, OP_LIST_ENDPOINTS),
               blob[:300])
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请在会话外运行 hcloud configure"
            " 或设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问终端节点服务（VPCEP），请检查 IAM 权限（403：缺少 "
            "vpcep:endpoints:list / vpcep:endpointServices:list / "
            "vpcep:endpointServices:listPublic），参见 references/iam-policies.md。"
            "详情：%s" % blob[:300]
        )
    if any(p in low for p in _INVALID_ID_PATTERNS):
        hint = "（--id=%s）" % item_id if item_id else ""
        return InvalidRequestError(
            "参数或资源 ID 无效%s：请确认 ID 为该区域真实存在的 VPCEP 资源 ID"
            "（形如 8-4-4-4-12 的 UUID），且与当前视图匹配。详情：%s"
            % (hint, blob[:300])
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def classify_hcloud_failure(stdout, stderr, returncode, item_id=None,
                            view=VIEW_ENDPOINT):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    return _classify_error_text(
        (stderr + " " + stdout).strip(), returncode, item_id=item_id, view=view)


def classify_payload_error(payload, item_id=None, view=VIEW_ENDPOINT):
    """Map a JSON error body (KooCLI returns rc=0 for API errors) to an error."""
    code, message = _payload_error(payload)
    text = "%s %s" % (code or "", message or "")
    return _classify_error_text(text, "0", item_id=item_id, view=view)


def extract_items(payload, view=VIEW_ENDPOINT):
    """Pull the endpoint / service list out of a VPCEP list response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _ITEM_LIST_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _total_count(payload):
    """Read `total_count` from a VPCEP list response, if present."""
    if isinstance(payload, dict):
        total = payload.get("total_count")
        if total is None:
            total = payload.get("totalCount")
        if total is None:
            meta = payload.get("metadata") or payload.get("page_info") \
                or payload.get("pageInfo")
            if isinstance(meta, dict):
                total = meta.get("total_count")
        if isinstance(total, int) and not isinstance(total, bool):
            return total
    return None


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


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


def _load_sdk():
    """Import the official `huaweicloudsdkvpcep` modules (v3 API / v1 module).

    Returns a dict with the client class, request models, region catalog and
    the core credential/config classes. Kept as one helper so tests can inject
    a fake SDK without network or credentials.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcore.region.region import Region
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore 未安装，无法回退到 SDK。"
            "请安装 KooCLI 或执行 pip install huaweicloudsdkcore "
            "huaweicloudsdkvpcep。详情：%s" % exc
        )
    last_error = None
    for version in ("v3", "v2", "v1"):
        try:
            module = importlib.import_module("huaweicloudsdkvpcep.%s" % version)
            region_module = importlib.import_module(
                "huaweicloudsdkvpcep.%s.region.vpcep_region" % version)
            return {
                "BasicCredentials": BasicCredentials,
                "HttpConfig": HttpConfig,
                "Region": Region,
                "VpcepClient": module.VpcepClient,
                "VpcepRegion": region_module.VpcepRegion,
                "ListEndpointsRequest": module.ListEndpointsRequest,
                "ListEndpointServiceRequest": module.ListEndpointServiceRequest,
                "ListServicePublicDetailsRequest":
                    module.ListServicePublicDetailsRequest,
                "version": version,
            }
        except (ImportError, AttributeError) as exc:
            last_error = exc
    raise ConfigError(
        "未找到 hcloud（KooCLI），且 huaweicloudsdkvpcep 不可用，无法回退到 SDK。"
        "请安装 KooCLI 或执行 pip install huaweicloudsdkcore "
        "huaweicloudsdkvpcep。详情：%s" % last_error
    )


def list_vpcep_via_sdk(view, region, name=None, item_id=None, vpc_id=None,
                       service_name=None, status=None, limit=DEFAULT_PAGE_SIZE,
                       project_id=None, sort_key=None, sort_dir=None,
                       max_pages=100):
    """SDK fallback: query VPCEP through `huaweicloudsdkvpcep`.

    Only invoked when hcloud is absent. Credentials are taken from the
    whitelisted AK/SK environment variables — never passed as literals. The
    official SDK has no env-var auto-discovery on `BasicCredentials()`, so AK/SK
    and the project id are read explicitly.
    """
    sdk = _load_sdk()
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
            "SDK 回退缺少 project_id：VPCEP 的 REST 路径为 %s 等，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。"
            % REST_PATH_ENDPOINTS
        )
    credentials = sdk["BasicCredentials"](
        ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = sdk["VpcepRegion"].value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = sdk["Region"](
                region, "https://vpcep.%s.myhuaweicloud.com" % region)
        client = sdk["VpcepClient"].new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(sdk["HttpConfig"].get_default_config()) \
            .build()
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkvpcep 安装与区域配置。"
            % (region, exc)
        )
    server_name = service_name or name
    items = []
    offset = 0
    limit = min(max(int(limit), 1), _max_page_size(view))
    for _ in range(max_pages):
        if view == VIEW_ENDPOINT:
            request = sdk["ListEndpointsRequest"](
                endpoint_service_name=server_name, vpc_id=vpc_id,
                id=item_id, limit=limit, offset=offset,
                sort_key=sort_key, sort_dir=sort_dir,
            )
            call = client.list_endpoints
            response_key = "endpoints"
        elif view == VIEW_SERVICE:
            request = sdk["ListEndpointServiceRequest"](
                endpoint_service_name=server_name, id=item_id,
                status=status, limit=limit, offset=offset,
                sort_key=sort_key, sort_dir=sort_dir,
            )
            call = client.list_endpoint_service
            response_key = "endpoint_services"
        else:
            request = sdk["ListServicePublicDetailsRequest"](
                limit=limit, offset=offset, endpoint_service_name=server_name,
                id=item_id, sort_key=sort_key, sort_dir=sort_dir,
            )
            call = client.list_service_public_details
            response_key = "endpoint_services"
        try:
            response = call(request)
            batch_objs = list(getattr(response, response_key) or [])
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问终端节点服务（VPCEP），请检查 IAM 权限（403）。"
                    "参见 references/iam-policies.md。详情：%s" % str(exc)[:300]
                )
            if any(p in low for p in _INVALID_ID_PATTERNS):
                raise InvalidRequestError(
                    "参数或资源 ID 无效：请确认 ID 为该区域真实存在的 VPCEP 资源 ID。"
                    "详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = [_jsonable(obj.to_dict()) for obj in batch_objs]
        items.extend(batch)
        try:
            total = _total_count(_jsonable(response.to_dict()))
        except Exception:
            total = None
        if total is not None and len(items) >= total:
            break
        if not batch or len(batch) < limit:
            break
        offset += limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def list_vpcep(view, region, name=None, item_id=None, vpc_id=None,
               service_name=None, status=None, limit=DEFAULT_PAGE_SIZE,
               project_id=None, sort_key=None, sort_dir=None, max_pages=100):
    """Query all VPCEP resources (offset-paged); KooCLI first, SDK fallback."""
    operation = VIEW_TO_OPERATION[view]
    server_name = service_name or name
    items = []
    offset = 0
    limit = min(max(int(limit), 1), _max_page_size(view))
    for _page in range(max_pages):
        argv = build_command(
            region, operation, view=view, name=name, item_id=item_id,
            vpc_id=vpc_id, service_name=service_name, status=status,
            limit=limit, offset=offset, sort_key=sort_key, sort_dir=sort_dir,
        )
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            items = list_vpcep_via_sdk(
                view, region, name=name, item_id=item_id, vpc_id=vpc_id,
                service_name=service_name, status=status, limit=limit,
                project_id=project_id, sort_key=sort_key, sort_dir=sort_dir,
                max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(
                stdout, stderr, returncode, item_id=item_id, view=view)
        payload = extract_json(stdout)
        if _payload_error(payload)[0] or _payload_error(payload)[1]:
            # KooCLI returns rc=0 for API error bodies — classify explicitly.
            raise classify_payload_error(payload, item_id=item_id, view=view)
        batch = extract_items(payload, view=view)
        items.extend(batch)
        total = _total_count(payload)
        if total is not None and len(items) >= total:
            break
        if not batch or len(batch) < limit:
            break
        offset += limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def _field(item, *names, default="-"):
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def item_name(item, view=VIEW_ENDPOINT):
    """Human-readable resource name for the selected view."""
    if view == VIEW_ENDPOINT:
        name = _field(item, "endpoint_service_name", "name", default=None)
    else:
        name = _field(item, "service_name", "endpoint_service_name", "name",
                      default=None)
    if name is None:
        name = _field(item, "id")
    return str(name)


def item_service_name(item, view=VIEW_ENDPOINT):
    if view == VIEW_ENDPOINT:
        return _field(item, "endpoint_service_name")
    return _field(item, "service_name", "endpoint_service_name")


def item_status(item):
    return str(_field(item, "status", default=""))


def is_available(item):
    return item_status(item).strip().lower() == "available"


def is_non_available(item):
    status = item_status(item).strip()
    return bool(status) and status.lower() != "available"


def filter_items(items, view=VIEW_ENDPOINT, name=None, fuzzy=False,
                 item_id=None, vpc_id=None, service_name=None, status=None):
    """Apply client-side filters (exact by default, substring with --fuzzy)."""
    result = []
    for item in items:
        if item_id and str(_field(item, "id", default="")) != str(item_id):
            continue
        if vpc_id and str(_field(item, "vpc_id", default="")) != str(vpc_id):
            continue
        if status and item_status(item).lower() != str(status).lower():
            continue
        matched = True
        for wanted in (name, service_name):
            if not wanted:
                continue
            actual = item_name(item, view).lower()
            wanted_low = str(wanted).lower()
            if fuzzy:
                if wanted_low not in actual:
                    matched = False
                    break
            elif actual != wanted_low:
                matched = False
                break
        if matched:
            result.append(item)
    return result


def _cell(value, renderer="text"):
    if renderer == "yesno":
        if value in (None, ""):
            return "-"
        if isinstance(value, bool):
            return "是" if value else "否"
        low = str(value).lower()
        if low in ("true", "1", "yes"):
            return "是"
        if low in ("false", "0", "no"):
            return "否"
        return str(value)
    if renderer == "status":
        if value in (None, ""):
            return "-"
        text = str(value)
        if text.strip().lower() != "available":
            return "[异常] %s" % text
        return text
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _raw_cell(item, field_name):
    if field_name == "server_type":
        return _field(item, "server_type", "service_type")
    return _field(item, field_name)


def render_table(items, view=VIEW_ENDPOINT, region=DEFAULT_REGION):
    """Render the fixed-column table for the selected view."""
    columns = VIEW_COLUMNS[view]
    include_region = view != VIEW_PUBLIC
    headers = [c[0] for c in columns] + (["region"] if include_region else [])
    rows = []
    for item in items:
        row = [_cell(_raw_cell(item, field_name), renderer)
               for _header, field_name, renderer in columns]
        if include_region:
            row.append(str(region))
        rows.append(row)
    if not rows:
        rows = [["-" for _ in headers]]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows))
              for i in range(len(headers))]
    lines = [
        "  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))),
        "  ".join("-" * w for w in widths),
    ]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i])
                               for i in range(len(headers))))
    return "\n".join(lines)


def _md_cell(value):
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown_section(items, view, region):
    """Render one fixed-column Markdown table (header-only when empty)."""
    columns = VIEW_COLUMNS[view]
    include_region = view != VIEW_PUBLIC
    headers = [c[0] for c in columns] + (["region"] if include_region else [])
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for item in items:
        row = [_cell(_raw_cell(item, field_name), renderer)
               for _header, field_name, renderer in columns]
        if include_region:
            row.append(str(region))
        lines.append("| " + " | ".join(_md_cell(c) for c in row) + " |")
    return "\n".join(lines)


def render_markdown(items, view=VIEW_ENDPOINT, region=DEFAULT_REGION):
    """Build the full Markdown report body (fixed columns, '-' for missing)."""
    available = [i for i in items if is_available(i)]
    abnormal = [i for i in items if is_non_available(i)]
    statuses = [_field(i, "status", default="-") for i in items]
    lines = [
        "# 华为云 VPCEP %s列表" % VIEW_LABEL[view],
        "",
        "- Region: %s" % region,
        "- 视图: %s（%s）" % (VIEW_LABEL[view], VIEW_TO_OPERATION[view]),
        "- 生成时间: %s" % datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "- 总数: %d" % len(items),
        "",
    ]
    if not items:
        lines.append("当前过滤条件下无 %s。" % VIEW_LABEL[view])
        lines.append("")
        lines.append(render_markdown_section([], view, region))
        lines.append("")
        return "\n".join(lines)

    if view == VIEW_PUBLIC:
        lines.append(render_markdown_section(items, view, region))
        lines.append("")
        return "\n".join(lines)

    if abnormal:
        lines.append("## AVAILABLE（%d 个）" % len(available))
        lines.append("")
        lines.append(render_markdown_section(available, view, region))
        lines.append("")
        lines.append("## 非 AVAILABLE（%d 个，需关注）" % len(abnormal))
        lines.append("")
        lines.append(render_markdown_section(abnormal, view, region))
    else:
        lines.append(render_markdown_section(items, view, region))
    lines.append("")
    lines.append("- 状态汇总: %s" % (
        ", ".join("%s=%d" % (s, statuses.count(s)) for s in sorted(set(statuses)))
        or "-"))
    lines.append("")
    return "\n".join(lines)


def write_markdown_atomic(path, content):
    """Atomically write the Markdown report (tmp file + os.replace)."""
    target = os.path.abspath(path)
    directory = os.path.dirname(target) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".vpcep-md-", suffix=".tmp",
                                    dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return target


def _filter_summary(args):
    parts = []
    if args.name:
        parts.append("name%s%s" % ("~" if args.fuzzy else "=", args.name))
    if args.item_id:
        parts.append("id=%s" % args.item_id)
    if args.vpc_id:
        parts.append("vpc_id=%s" % args.vpc_id)
    if args.service_name:
        parts.append("service_name%s%s"
                     % ("~" if args.fuzzy else "=", args.service_name))
    if args.status:
        parts.append("status=%s" % args.status)
    return "（过滤条件: %s）" % ", ".join(parts) if parts else ""


def _print_grouped(items, view, args):
    """Concise grouped list: available first, non-available highlighted apart."""
    print("Region %s 的 VPCEP %s列表（共 %d 个）："
          % (args.region, VIEW_LABEL[view], len(items)))
    if view == VIEW_PUBLIC:
        for item in items:
            _print_concise_item(item, view, prefix="-")
        return
    available = [i for i in items if is_available(i)]
    abnormal = [i for i in items if is_non_available(i)]
    others = [i for i in items if not is_available(i) and not is_non_available(i)]
    if available:
        print("AVAILABLE（%d 个）：" % len(available))
        for item in available:
            _print_concise_item(item, view, prefix="-")
    if others:
        print("状态未知（%d 个）：" % len(others))
        for item in others:
            _print_concise_item(item, view, prefix="-")
    if abnormal:
        print("异常（非 AVAILABLE，%d 个，需关注）：" % len(abnormal))
        for item in abnormal:
            _print_concise_item(item, view, prefix="[!]")
    else:
        print("无异常（非 AVAILABLE）%s。" % VIEW_LABEL[view])


def _print_concise_item(item, view, prefix="-"):
    name = item_name(item, view)
    status = item_status(item) or "-"
    if view == VIEW_ENDPOINT:
        service = item_service_name(item, view)
        print("%s %s  [%s]  服务=%s" % (prefix, name, status, service))
    elif view == VIEW_SERVICE:
        backend = _field(item, "server_type", "service_type")
        print("%s %s  [%s]  后端类型=%s" % (prefix, name, status, backend))
    else:
        service_type = _field(item, "service_type")
        print("%s %s  类型=%s" % (prefix, name, service_type))


def _print_table_grouped(items, view, args):
    if view == VIEW_PUBLIC:
        print("Region %s 的 VPCEP %s列表（共 %d 个）："
              % (args.region, VIEW_LABEL[view], len(items)))
        print(render_table(items, view, args.region))
        return
    available = [i for i in items if is_available(i)]
    abnormal = [i for i in items if is_non_available(i)]
    others = [i for i in items if not is_available(i) and not is_non_available(i)]
    print("Region %s 的 VPCEP %s列表（共 %d 个，AVAILABLE %d 个）："
          % (args.region, VIEW_LABEL[view], len(items), len(available)))
    if available or others:
        print(render_table(available + others, view, args.region))
    if abnormal:
        print("异常（非 AVAILABLE，共 %d 个，需关注）：" % len(abnormal))
        print("[!] 以下 %s状态不是 available，请优先排查。" % VIEW_LABEL[view])
        print(render_table(abnormal, view, args.region))
    else:
        print("无异常（非 AVAILABLE）%s。" % VIEW_LABEL[view])


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs BEFORE argparse so `--action delete` is rejected
    # with rc=1 (not argparse's rc=2).
    try:
        guard_argv(raw_argv)
    except VpcepListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description="查询华为云终端节点服务（VPCEP）的终端节点 / 终端节点服务 / "
                    "公共终端节点服务列表（KooCLI 只读：ListEndpoints / "
                    "ListEndpointService / ListServicePublicDetails）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--view", choices=VIEWS, default=VIEW_ENDPOINT,
                        help="视图：endpoint 终端节点（默认）/ service 终端节点服务 / "
                             "public 公共终端节点服务")
    parser.add_argument("--name",
                        help="按名称过滤（默认精确匹配，大小写不敏感）")
    parser.add_argument("--fuzzy", action="store_true",
                        help="--name / --service-name 改为模糊（子串）匹配")
    parser.add_argument("--id", dest="item_id",
                        help="按资源 ID 精确过滤")
    parser.add_argument("--vpc-id", dest="vpc_id",
                        help="按 VPC ID 过滤（仅终端节点视图）")
    parser.add_argument("--service-name", dest="service_name",
                        help="按所属终端节点服务名称过滤")
    parser.add_argument("--status",
                        help="按状态过滤（客户端精确匹配，如 failed / creating）")
    parser.add_argument("--table", action="store_true",
                        help="输出固定列表格")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--format", choices=("md",), default=None,
                        help="导出本地 Markdown 报告（固定列，原子写盘）")
    parser.add_argument("--output",
                        help="Markdown 报告输出路径（默认 vpcep-<view>-<时间>.md）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d；终端节点上限 500，服务/公共上限 1000）"
                             % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退路径需要）")
    parser.add_argument("--sort-key", dest="sort_key",
                        choices=("create_at", "update_at"), default=None,
                        help="排序字段（create_at / update_at）")
    parser.add_argument("--sort-dir", dest="sort_dir",
                        choices=("asc", "desc"), default=None,
                        help="排序方向（asc / desc）")
    parser.add_argument("--operation", default=None,
                        help="hcloud VPCEP 操作名（仅允许只读 %s）"
                             % " / ".join(ALLOWED_OPERATIONS))
    parser.add_argument("--action", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    view = args.view
    try:
        operation = resolve_operation(view, args.operation)
        guard_operation(operation)
        if view not in VIEW_TO_OPERATION:
            raise GuardError("不支持的视图 %r" % view)
        items = list_vpcep(
            view, args.region, name=args.name, item_id=args.item_id,
            vpc_id=args.vpc_id, service_name=args.service_name,
            status=args.status, limit=args.page_size,
            project_id=args.project_id, sort_key=args.sort_key,
            sort_dir=args.sort_dir,
        )
        items = filter_items(
            items, view=view, name=args.name, fuzzy=args.fuzzy,
            item_id=args.item_id, vpc_id=args.vpc_id,
            service_name=args.service_name, status=args.status,
        )
    except VpcepListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("[错误] 查询已中断。", file=sys.stderr)
        return 1
    except Exception as exc:  # no traceback for unexpected failures
        print("[错误] 查询失败：%s" % str(exc)[:300], file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0

    if args.format == "md":
        output = args.output or "vpcep-%s-%s.md" % (
            view, datetime.now().strftime("%Y%m%d-%H%M%S"))
        try:
            path = write_markdown_atomic(
                output, render_markdown(items, view, args.region))
        except OSError as exc:
            print("[错误] 无法写入 Markdown 报告 %s：%s" % (output, exc),
                  file=sys.stderr)
            return 1
        print("已导出 VPCEP %s Markdown 报告（%d 个）：%s"
              % (VIEW_LABEL[view], len(items), path))
        return 0

    if not items:
        print("当前区域（%s）无 VPCEP %s%s。"
              % (args.region, VIEW_LABEL[view], _filter_summary(args)))
        return 0

    if args.table:
        _print_table_grouped(items, view, args)
    else:
        _print_grouped(items, view, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())