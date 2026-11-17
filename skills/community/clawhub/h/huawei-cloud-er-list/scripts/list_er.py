#!/usr/bin/env python3
"""List Huawei Cloud Enterprise Router (ER) resources via KooCLI, read-only.

Four read-only views are exposed through ``--resource``:

* ``er``           — ``hcloud ER ListEnterpriseRouters``
                     (GET /v3/{project_id}/enterprise-router/instances)
* ``attachment``   — ``hcloud ER ListVpcAttachments`` (requires ``--er-id``)
                     (GET /v3/{project_id}/enterprise-router/{er_id}/vpc-attachments)
* ``route-table``  — ``hcloud ER ListRouteTables`` (requires ``--er-id``)
                     (GET /v3/{project_id}/enterprise-router/{er_id}/route-tables)
* ``detail``       — ``hcloud ER ShowEnterpriseRouter`` (requires ``--er-id``)
                     (GET /v3/{project_id}/enterprise-router/instances/{er_id})

When the ``hcloud`` binary is missing the script falls back to the official
``huaweicloudsdker`` v3 SDK (``ErClient``). Credentials are always read by the
KooCLI profile / SDK environment — never handled by the script.

Output modes: compact list (default), fixed-column table (``--table``) and raw
JSON (``--json``). Non-``available`` enterprise routers / attachments are
rendered in a separate, explicitly flagged section instead of being mixed with
the healthy resources. Supports ``--name`` / ``--fuzzy`` local name filters,
``--er-id`` / ``--state`` / ``--region`` filters, ``--owned-by-self`` /
``--enterprise-project-id`` / ``--vpc-id`` server-side filters, ``--sort-key`` /
``--sort-dir``, and automatic ``page_info.next_marker`` paging.

The skill is strictly read-only: a write-intent guard rejects every mutating
intent before a single command is executed.

Usage:
    python3 scripts/list_er.py [--region cn-north-4]
                               [--resource er|attachment|route-table|detail]
                               [--table | --json]
                               [--name NAME] [--fuzzy TEXT]
                               [--er-id ER_ID] [--state STATE]
                               [--owned-by-self true|false]
                               [--enterprise-project-id ID]
                               [--vpc-id VPC_ID]
                               [--sort-key id|name|state]
                               [--sort-dir asc|desc]
                               [--default-association-table true|false]
                               [--default-propagation-table true|false]
                               [--page-size 100] [--project-id ID]
                               [--operation <read-only operation>]

Environment overrides (mostly for tests):
    ER_LIST_HCLOUD_BIN    hcloud executable (default "hcloud")
    ER_LIST_HCLOUD_ARGS   extra args injected before the ER operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 2000
MAX_PAGES = 100
SERVICE = "ER"
DEFAULT_RESOURCE = "er"

RESOURCE_OPERATIONS = {
    "er": "ListEnterpriseRouters",
    "attachment": "ListVpcAttachments",
    "route-table": "ListRouteTables",
    "detail": "ShowEnterpriseRouter",
}

RESOURCE_PATHS = {
    "er": "/v3/{project_id}/enterprise-router/instances",
    "attachment": "/v3/{project_id}/enterprise-router/{er_id}/vpc-attachments",
    "route-table": "/v3/{project_id}/enterprise-router/{er_id}/route-tables",
    "detail": "/v3/{project_id}/enterprise-router/instances/{er_id}",
}

ER_ITEM_KEYS = ("instances", "enterprise_routers", "enterpriseRouters")
ATTACHMENT_ITEM_KEYS = ("vpc_attachments", "vpcAttachments", "attachments")
ROUTE_TABLE_ITEM_KEYS = ("route_tables", "routeTables")

AVAILABLE_STATE = "available"

# Fixed table layouts required by the skill contract:
# enterprise router = 8 columns, VPC attachment = 6 columns.
ER_TABLE_COLUMNS = (
    ("名称", "name"),
    ("ID", "id"),
    ("状态", "state"),
    ("ASN", "asn"),
    ("企业项目ID", "enterprise_project_id"),
    ("可用区", "availability_zone_ids"),
    ("描述", "description"),
    ("创建时间", "created_at"),
)
ATTACHMENT_TABLE_COLUMNS = (
    ("名称", "name"),
    ("ID", "id"),
    ("状态", "state"),
    ("VPC ID", "vpc_id"),
    ("子网 ID", "virsubnet_id"),
    ("创建时间", "created_at"),
)
ROUTE_TABLE_COLUMNS = (
    ("名称", "name"),
    ("ID", "id"),
    ("状态", "state"),
    ("默认关联", "is_default_association"),
    ("默认传播", "is_default_propagation"),
    ("创建时间", "created_at"),
)

ER_DETAIL_FIELDS = (
    ("名称", "name"),
    ("ID", "id"),
    ("状态", "state"),
    ("ASN", "asn"),
    ("企业项目ID", "enterprise_project_id"),
    ("可用区", "availability_zone_ids"),
    ("自动接受共享连接", "auto_accept_shared_attachments"),
    ("默认关联路由表ID", "default_association_route_table_id"),
    ("默认传播路由表ID", "default_propagation_route_table_id"),
    ("计费模式", "charge_mode"),
    ("描述", "description"),
    ("创建时间", "created_at"),
    ("更新时间", "updated_at"),
)

# Values of these flags are pure local search text and are excluded from the
# write-intent scan (a search term such as "delete-test" is not an operation).
_VALUE_STRIPPED_FLAGS = ("--name", "--fuzzy")

# Mutating ER operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createenterpriserouter",
    "deleteenterpriserouter",
    "updateenterpriserouter",
    "createvpcattachment",
    "deletevpcattachment",
    "updatevpcattachment",
    "createroutetable",
    "deleteroutetable",
    "updateroutetable",
    "createstaticroute",
    "deletestaticroute",
    "updatestaticroute",
    "associateroutetable",
    "disassociateroutetable",
    "acceptattachment",
    "rejectattachment",
    "enablepropagation",
    "disablepropagation",
    "updatepropagationroutepolicy",
    "changeassociationroutepolicy",
    "changeavailabilityzone",
    "createflowlog",
    "deleteflowlog",
    "updateflowlog",
    "enableflowlog",
    "disableflowlog",
    "createresourcetag",
    "deleteresourcetag",
    "batchcreateresourcetags",
    "create",
    "delete",
    "update",
    "modify",
    "associate",
    "disassociate",
    "dissociate",
    "bind",
    "unbind",
    "release",
    "remove",
    "destroy",
    "change",
    "restart",
    "enable",
    "disable",
)

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
    "access denied",
    "apigw.0301",
    "common.01010013",
    "认证失败",
    "权限不足",
    "permission denied",
)

_NOT_FOUND_PATTERNS = (
    "not found",
    "does not exist",
    "doesn't exist",
    "not exist",
    "no such",
    "404",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class ErListError(Exception):
    """Base error for the ER list skill."""


class GuardError(ErListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ErListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(ErListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class NotFoundError(ErListError):
    """The requested enterprise router does not exist."""


class ApiError(ErListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Separators are normalized so ``--create-er``, ``CreateEnterpriseRouter``
    and ``create_enterprise_router`` all hit the same keyword. Read-only
    vocabulary (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（ER ListEnterpriseRouters / ListVpcAttachments / ListRouteTables / "
                "ShowEnterpriseRouter），创建/删除/更新/绑定/解绑等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation, allowed):
    """Only the whitelisted read-only operation may be executed."""
    if operation != allowed:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, allowed)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    ``--name`` / ``--fuzzy`` values are pure local search text and are
    stripped; a following flag is never swallowed. All other flags and their
    values (``--er-id`` / ``--operation`` etc.) stay scanned.
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    resource_skip = False
    for tok in tokens:
        if resource_skip:
            resource_skip = False
            if tok in RESOURCE_OPERATIONS:
                continue
            kept.append(tok)
            continue
        if tok == "--resource":
            resource_skip = True
            continue
        if tok.startswith("--resource="):
            value = tok.split("=", 1)[1]
            if value in RESOURCE_OPERATIONS:
                continue
            kept.append(tok)
            continue
        if tok in _VALUE_STRIPPED_FLAGS:
            skip_next = True
            continue
        if tok.startswith("-") and "=" in tok and tok.split("=", 1)[0] in _VALUE_STRIPPED_FLAGS:
            continue
        if skip_next:
            skip_next = False
            if not tok.startswith("-"):
                continue
        kept.append(tok)
    return " ".join(kept)


def _bool_flag(value):
    """Render an already-parsed boolean as the KooCLI true/false literal."""
    return "true" if value else "false"


def build_er_command(region, state=None, er_id=None, owned_by_self=None,
                     enterprise_project_id=None, sort_key=None, sort_dir=None,
                     limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud ER ListEnterpriseRouters argv (no executable).

    All filters are real server-side ListEnterpriseRouters query parameters
    verified with ``hcloud ER ListEnterpriseRouters --help``. Array query
    parameters (``state`` / ``id`` / ``enterprise_project_id`` / ``sort_key`` /
    ``sort_dir``) must use the KooCLI indexed form ``--key.1=value``.
    """
    argv = [
        SERVICE,
        RESOURCE_OPERATIONS["er"],
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if state:
        argv.append("--state.1=%s" % state)
    if er_id:
        argv.append("--id.1=%s" % er_id)
    if owned_by_self is not None:
        argv.append("--owned_by_self=%s" % _bool_flag(owned_by_self))
    if enterprise_project_id:
        argv.append("--enterprise_project_id.1=%s" % enterprise_project_id)
    if sort_key:
        argv.append("--sort_key.1=%s" % sort_key)
    if sort_dir:
        argv.append("--sort_dir.1=%s" % sort_dir)
    return argv


def build_attachment_command(region, er_id, state=None, vpc_id=None,
                             sort_key=None, sort_dir=None,
                             limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud ER ListVpcAttachments argv (no executable)."""
    argv = [
        SERVICE,
        RESOURCE_OPERATIONS["attachment"],
        "--cli-region=%s" % region,
        "--er_id=%s" % er_id,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if state:
        argv.append("--state.1=%s" % state)
    if vpc_id:
        argv.append("--vpc_id.1=%s" % vpc_id)
    if sort_key:
        argv.append("--sort_key.1=%s" % sort_key)
    if sort_dir:
        argv.append("--sort_dir.1=%s" % sort_dir)
    return argv


def build_route_table_command(region, er_id, state=None,
                              is_default_association_table=None,
                              is_default_propagation_table=None,
                              sort_key=None, sort_dir=None,
                              limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud ER ListRouteTables argv (no executable)."""
    argv = [
        SERVICE,
        RESOURCE_OPERATIONS["route-table"],
        "--cli-region=%s" % region,
        "--er_id=%s" % er_id,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if state:
        argv.append("--state.1=%s" % state)
    if is_default_association_table is not None:
        argv.append("--is_default_association_table=%s"
                    % _bool_flag(is_default_association_table))
    if is_default_propagation_table is not None:
        argv.append("--is_default_propagation_table=%s"
                    % _bool_flag(is_default_propagation_table))
    if sort_key:
        argv.append("--sort_key.1=%s" % sort_key)
    if sort_dir:
        argv.append("--sort_dir.1=%s" % sort_dir)
    return argv


def build_detail_command(region, er_id):
    """Build the hcloud ER ShowEnterpriseRouter argv (no executable)."""
    return [
        SERVICE,
        RESOURCE_OPERATIONS["detail"],
        "--cli-region=%s" % region,
        "--er_id=%s" % er_id,
    ]


def _hcloud_executable():
    return os.environ.get("ER_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("ER_LIST_HCLOUD_ARGS", "").split()
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


def _payload_error_text(payload):
    """Return the error message carried in an hcloud JSON error body, if any.

    KooCLI reports OpenAPI errors as a JSON object with ``error_code`` /
    ``error_msg`` on **stdout with exit code 0**; that must be treated as a
    hard failure instead of an empty result.
    """
    if not isinstance(payload, dict):
        return None
    code = payload.get("error_code") or payload.get("errorCode")
    message = (
        payload.get("error_msg") or payload.get("errorMsg")
        or payload.get("error_message") or payload.get("message")
    )
    if code or message:
        return ("%s %s" % (code or "", message or "")).strip()
    return None


def classify_error_text(blob, returncode=0):
    """Map an hcloud error blob to a domain error with explicit hints."""
    blob = (blob or "").strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：ER 真实参数清单"
            "可通过 `hcloud ER <Operation> --help` 查看。详情：%s"
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
        return AuthError(
            "无权限访问企业路由器（ER），请检查 IAM 权限（403：AK/SK 无效或未授予 "
            "ER 只读权限），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _NOT_FOUND_PATTERNS):
        return NotFoundError(
            "未找到指定的企业路由器（ER 不存在，或 --er-id 有误）。详情：%s"
            % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def classify_hcloud_failure(stdout, stderr, returncode, operation):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    error = classify_error_text(blob, returncode)
    if (isinstance(error, ApiError) and operation
            and "参数错误" not in str(error)):
        error = ApiError(
            "hcloud 调用 %s 失败（退出码 %s）：%s"
            % (operation, returncode, blob[:300])
        )
    return error


def check_payload_error(payload):
    """Raise a classified domain error if the payload is an hcloud error body."""
    blob = _payload_error_text(payload)
    if blob:
        raise classify_error_text(blob, 0)


def extract_items(payload, keys):
    """Pull the resource list out of a list response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def next_marker(payload):
    """Read next_marker from a response page_info (page_info may be absent)."""
    if not isinstance(payload, dict):
        return None
    page_info = payload.get("page_info") or payload.get("pageInfo")
    if isinstance(page_info, dict):
        marker = page_info.get("next_marker") or page_info.get("nextMarker")
        if marker:
            return str(marker)
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
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def resolve_project_id(explicit=None):
    if explicit:
        return explicit
    return _env_value(_PROJECT_ID_ENV_NAMES)


def _build_sdk_client(region, project_id, resource="er"):
    """Build a ``huaweicloudsdker`` v3 client from whitelisted env credentials."""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdker.v3 import ErClient
        from huaweicloudsdker.v3.region.er_region import ErRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdker 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdker。详情：%s" % exc
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
            "SDK 回退缺少 project_id：ER 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。"
            % RESOURCE_PATHS[resource]
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = ErRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://er.%s.myhuaweicloud.com" % region)
        return ErClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdker 安装与区域配置。"
            % (region, exc)
        )


def _classify_sdk_failure(exc):
    low = str(exc).lower()
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问企业路由器（ER），请检查 IAM 权限（403）。详情：%s"
            % str(exc)[:300]
        )
    if any(p in low for p in _NOT_FOUND_PATTERNS):
        return NotFoundError(
            "未找到指定的企业路由器（ER 不存在，或 --er-id 有误）。详情：%s"
            % str(exc)[:300]
        )
    return ApiError("SDK 调用失败：%s" % str(exc)[:300])


def _sdk_next_marker(response, records, limit):
    page_info = getattr(response, "page_info", None)
    marker = getattr(page_info, "next_marker", None) if page_info else None
    if marker:
        return str(marker)
    if records and len(records) >= limit:
        return records[-1].get("id")
    return None


def list_ers_via_sdk(region, state=None, er_id=None, owned_by_self=None,
                     enterprise_project_id=None, sort_key=None, sort_dir=None,
                     limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=MAX_PAGES):
    """SDK fallback for ListEnterpriseRouters."""
    client = _build_sdk_client(region, project_id, "er")
    from huaweicloudsdker.v3 import ListEnterpriseRoutersRequest
    records_all = []
    marker = None
    for _ in range(max_pages):
        request = ListEnterpriseRoutersRequest(
            limit=limit,
            marker=marker,
            state=[state] if state else None,
            id=[er_id] if er_id else None,
            owned_by_self=owned_by_self,
            enterprise_project_id=([enterprise_project_id]
                                   if enterprise_project_id else None),
            sort_key=[sort_key] if sort_key else None,
            sort_dir=[sort_dir] if sort_dir else None,
        )
        try:
            response = client.list_enterprise_routers(request)
        except Exception as exc:
            raise _classify_sdk_failure(exc)
        batch = list(getattr(response, "instances", None) or [])
        records = [_jsonable(item.to_dict()) for item in batch]
        records_all.extend(records)
        marker = _sdk_next_marker(response, records, limit)
        if not marker or not batch:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records_all


def list_attachments_via_sdk(region, er_id, state=None, vpc_id=None,
                             sort_key=None, sort_dir=None,
                             limit=DEFAULT_PAGE_SIZE, project_id=None,
                             max_pages=MAX_PAGES):
    """SDK fallback for ListVpcAttachments."""
    client = _build_sdk_client(region, project_id, "attachment")
    from huaweicloudsdker.v3 import ListVpcAttachmentsRequest
    records_all = []
    marker = None
    for _ in range(max_pages):
        request = ListVpcAttachmentsRequest(
            er_id=er_id,
            limit=limit,
            marker=marker,
            state=[state] if state else None,
            vpc_id=[vpc_id] if vpc_id else None,
            sort_key=[sort_key] if sort_key else None,
            sort_dir=[sort_dir] if sort_dir else None,
        )
        try:
            response = client.list_vpc_attachments(request)
        except Exception as exc:
            raise _classify_sdk_failure(exc)
        batch = list(getattr(response, "vpc_attachments", None) or [])
        records = [_jsonable(item.to_dict()) for item in batch]
        records_all.extend(records)
        marker = _sdk_next_marker(response, records, limit)
        if not marker or not batch:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records_all


def list_route_tables_via_sdk(region, er_id, state=None,
                              is_default_association_table=None,
                              is_default_propagation_table=None,
                              sort_key=None, sort_dir=None,
                              limit=DEFAULT_PAGE_SIZE, project_id=None,
                              max_pages=MAX_PAGES):
    """SDK fallback for ListRouteTables."""
    client = _build_sdk_client(region, project_id, "route-table")
    from huaweicloudsdker.v3 import ListRouteTablesRequest
    records_all = []
    marker = None
    for _ in range(max_pages):
        request = ListRouteTablesRequest(
            er_id=er_id,
            limit=limit,
            marker=marker,
            state=[state] if state else None,
            is_default_association_table=is_default_association_table,
            is_default_propagation_table=is_default_propagation_table,
            sort_key=[sort_key] if sort_key else None,
            sort_dir=[sort_dir] if sort_dir else None,
        )
        try:
            response = client.list_route_tables(request)
        except Exception as exc:
            raise _classify_sdk_failure(exc)
        batch = list(getattr(response, "route_tables", None) or [])
        records = [_jsonable(item.to_dict()) for item in batch]
        records_all.extend(records)
        marker = _sdk_next_marker(response, records, limit)
        if not marker or not batch:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records_all


def show_er_via_sdk(region, er_id, project_id=None):
    """SDK fallback for ShowEnterpriseRouter."""
    client = _build_sdk_client(region, project_id, "detail")
    from huaweicloudsdker.v3 import ShowEnterpriseRouterRequest
    try:
        response = client.show_enterprise_router(
            ShowEnterpriseRouterRequest(er_id=er_id))
    except Exception as exc:
        raise _classify_sdk_failure(exc)
    instance = getattr(response, "instance", None)
    if instance is None:
        return {}
    return _jsonable(instance.to_dict())


def _paged_fetch(build_argv, extract_keys, operation, sdk_fallback, limit,
                 max_pages=MAX_PAGES):
    """Shared marker-paged fetch loop: KooCLI first, SDK fallback.

    ``sdk_fallback`` is a zero-argument callable, invoked only when the
    hcloud binary is missing.
    """
    records = []
    marker = None
    for _ in range(max_pages):
        argv = build_argv(marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            return sdk_fallback()
        blob = stdout + " " + stderr
        if returncode != 0 or _USE_ERROR_MARKER in blob.lower():
            raise classify_hcloud_failure(stdout, stderr, returncode, operation)
        payload = extract_json(stdout)
        check_payload_error(payload)
        batch = extract_items(payload, extract_keys)
        records.extend(batch)
        marker = next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return records


def list_ers(region, state=None, er_id=None, owned_by_self=None,
             enterprise_project_id=None, sort_key=None, sort_dir=None,
             limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=MAX_PAGES):
    """Query all enterprise routers (marker-paged); KooCLI first, SDK fallback."""
    return _paged_fetch(
        lambda marker: build_er_command(
            region, state=state, er_id=er_id, owned_by_self=owned_by_self,
            enterprise_project_id=enterprise_project_id,
            sort_key=sort_key, sort_dir=sort_dir,
            limit=limit, marker=marker),
        ER_ITEM_KEYS,
        RESOURCE_OPERATIONS["er"],
        lambda: list_ers_via_sdk(
            region, state=state, er_id=er_id, owned_by_self=owned_by_self,
            enterprise_project_id=enterprise_project_id,
            sort_key=sort_key, sort_dir=sort_dir,
            limit=limit, project_id=project_id, max_pages=max_pages),
        limit, max_pages,
    )


def list_attachments(region, er_id, state=None, vpc_id=None, sort_key=None,
                     sort_dir=None, limit=DEFAULT_PAGE_SIZE, project_id=None,
                     max_pages=MAX_PAGES):
    """Query all VPC attachments of an ER (marker-paged); CLI first, SDK fallback."""
    return _paged_fetch(
        lambda marker: build_attachment_command(
            region, er_id, state=state, vpc_id=vpc_id,
            sort_key=sort_key, sort_dir=sort_dir,
            limit=limit, marker=marker),
        ATTACHMENT_ITEM_KEYS,
        RESOURCE_OPERATIONS["attachment"],
        lambda: list_attachments_via_sdk(
            region, er_id, state=state, vpc_id=vpc_id,
            sort_key=sort_key, sort_dir=sort_dir,
            limit=limit, project_id=project_id, max_pages=max_pages),
        limit, max_pages,
    )


def list_route_tables(region, er_id, state=None,
                      is_default_association_table=None,
                      is_default_propagation_table=None, sort_key=None,
                      sort_dir=None, limit=DEFAULT_PAGE_SIZE, project_id=None,
                      max_pages=MAX_PAGES):
    """Query all route tables of an ER (marker-paged); CLI first, SDK fallback."""
    return _paged_fetch(
        lambda marker: build_route_table_command(
            region, er_id, state=state,
            is_default_association_table=is_default_association_table,
            is_default_propagation_table=is_default_propagation_table,
            sort_key=sort_key, sort_dir=sort_dir,
            limit=limit, marker=marker),
        ROUTE_TABLE_ITEM_KEYS,
        RESOURCE_OPERATIONS["route-table"],
        lambda: list_route_tables_via_sdk(
            region, er_id, state=state,
            is_default_association_table=is_default_association_table,
            is_default_propagation_table=is_default_propagation_table,
            sort_key=sort_key, sort_dir=sort_dir,
            limit=limit, project_id=project_id, max_pages=max_pages),
        limit, max_pages,
    )


def show_er(region, er_id, project_id=None):
    """Query a single ER detail; KooCLI first, SDK fallback."""
    argv = build_detail_command(region, er_id)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        return show_er_via_sdk(region, er_id, project_id=project_id)
    blob = stdout + " " + stderr
    if returncode != 0 or _USE_ERROR_MARKER in blob.lower():
        raise classify_hcloud_failure(
            stdout, stderr, returncode, RESOURCE_OPERATIONS["detail"])
    payload = extract_json(stdout)
    check_payload_error(payload)
    if isinstance(payload, dict):
        instance = payload.get("instance")
        if isinstance(instance, dict):
            return instance
        if payload:
            return payload
    if isinstance(payload, list) and payload:
        return payload[0]
    raise NotFoundError(
        "未找到企业路由器 %s（响应为空）。请确认 --er-id 是否正确。" % er_id)


def apply_local_filters(records, name=None, fuzzy=None):
    """Apply local name filters (EXACT ``--name`` / case-insensitive ``--fuzzy``)."""
    result = list(records)
    if name:
        result = [r for r in result if str(r.get("name") or "") == name]
    if fuzzy:
        low = str(fuzzy).lower()
        result = [r for r in result
                  if low in str(r.get("name") or "").lower()]
    return result


def split_by_state(records):
    """Split records into (available, non-available) groups."""
    available = []
    abnormal = []
    for record in records:
        if str(record.get("state") or "").lower() == AVAILABLE_STATE:
            available.append(record)
        else:
            abnormal.append(record)
    return available, abnormal


def _cell(value):
    if value is None or value == "":
        return "-"
    if isinstance(value, (list, tuple)):
        return ",".join(str(v) for v in value) if value else "-"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _row(record, columns):
    return [_cell(record.get(key)) for _, key in columns]


def render_fixed_table(records, columns):
    """Render a fixed-column table; empty record lists yield a header-only table."""
    headers = [label for label, _ in columns]
    rows = [_row(record, columns) for record in records]
    widths = []
    for index, header in enumerate(headers):
        widest = len(header)
        for row in rows:
            widest = max(widest, len(row[index]))
        widths.append(widest)
    lines = [
        "  ".join(header.ljust(widths[i]) for i, header in enumerate(headers)),
        "  ".join("-" * width for width in widths),
    ]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i])
                               for i in range(len(headers))))
    return "\n".join(lines)


def render_detail(instance, region):
    """Render a single ER detail as labelled key/value lines."""
    lines = ["企业路由器（ER）详情（Region %s）：" % region]
    for label, key in ER_DETAIL_FIELDS:
        lines.append("  %s: %s" % (label, _cell(instance.get(key))))
    return "\n".join(lines)


def compact_er_line(record, abnormal=False):
    prefix = "[异常] " if abnormal else "- "
    return "%s%s (%s) [%s] ASN=%s 企业项目=%s" % (
        prefix,
        _cell(record.get("name")),
        _cell(record.get("id")),
        _cell(record.get("state")),
        _cell(record.get("asn")),
        _cell(record.get("enterprise_project_id")),
    )


def compact_attachment_line(record, abnormal=False):
    prefix = "[异常] " if abnormal else "- "
    return "%s%s (%s) [%s] VPC=%s 子网=%s" % (
        prefix,
        _cell(record.get("name")),
        _cell(record.get("id")),
        _cell(record.get("state")),
        _cell(record.get("vpc_id")),
        _cell(record.get("virsubnet_id")),
    )


def compact_route_table_line(record, abnormal=False):
    prefix = "[异常] " if abnormal else "- "
    return "%s%s (%s) [%s] 默认关联=%s 默认传播=%s" % (
        prefix,
        _cell(record.get("name")),
        _cell(record.get("id")),
        _cell(record.get("state")),
        _cell(record.get("is_default_association")),
        _cell(record.get("is_default_propagation")),
    )


def render_sections(records, columns, normal_title, abnormal_title):
    """Render available records plus a separately flagged abnormal section."""
    available, abnormal = split_by_state(records)
    lines = []
    if available:
        lines.append(normal_title % len(available))
        lines.append(render_fixed_table(available, columns))
    if abnormal:
        if lines:
            lines.append("")
        lines.append("[!] " + abnormal_title % len(abnormal))
        lines.append(render_fixed_table(abnormal, columns))
    return "\n".join(lines)


def render_compact_sections(records, compact_line, normal_title,
                            abnormal_title):
    """Compact-list equivalent of ``render_sections``."""
    available, abnormal = split_by_state(records)
    lines = []
    if available:
        lines.append(normal_title % len(available))
        lines.extend(compact_line(r) for r in available)
    if abnormal:
        if lines:
            lines.append("")
        lines.append("[!] " + abnormal_title % len(abnormal))
        lines.extend(compact_line(r, abnormal=True) for r in abnormal)
    return "\n".join(lines)


def _filter_suffix(filters):
    return "（过滤条件: %s）" % ", ".join(filters) if filters else ""


def _validate_page_size(value):
    if value < MIN_PAGE_SIZE or value > MAX_PAGE_SIZE:
        raise ErListError(
            "--page-size 必须在 %d~%d 之间（当前 %d）。"
            % (MIN_PAGE_SIZE, MAX_PAGE_SIZE, value))
    return value


def _require_er_id(args):
    if not args.er_id:
        raise ErListError(
            "%s 查询必须提供 --er-id（企业路由器 ID）。" % args.resource)


def _collect_filters(args):
    filters = []
    if args.name:
        filters.append("name=%s" % args.name)
    if args.fuzzy:
        filters.append("fuzzy=%s" % args.fuzzy)
    if args.er_id:
        filters.append("er_id=%s" % args.er_id)
    if args.state:
        filters.append("state=%s" % args.state)
    if args.vpc_id:
        filters.append("vpc_id=%s" % args.vpc_id)
    if args.enterprise_project_id:
        filters.append("enterprise_project_id=%s" % args.enterprise_project_id)
    return filters


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云企业路由器（ER）资源（只读；KooCLI hcloud ER "
                    "ListEnterpriseRouters / ListVpcAttachments / ListRouteTables / "
                    "ShowEnterpriseRouter）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--resource",
                        choices=("er", "attachment", "route-table", "detail"),
                        default=DEFAULT_RESOURCE,
                        help="查询对象：er（默认）/ attachment / route-table / detail")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--table", action="store_true",
                        help="以固定列表格输出（ER 8 列 / 连接 6 列 / 路由表 6 列）")
    parser.add_argument("--name", help="按名称精确过滤（本地过滤）")
    parser.add_argument("--fuzzy", help="按名称模糊过滤（本地过滤，不区分大小写）")
    parser.add_argument("--er-id", dest="er_id",
                        help="企业路由器 ID（attachment / route-table / detail 必填；"
                             "er 路由下作为服务端 id 过滤）")
    parser.add_argument("--state",
                        help="按状态过滤（服务端查询参数，如 available / failed / pending）")
    parser.add_argument("--owned-by-self", dest="owned_by_self",
                        choices=("true", "false"),
                        help="仅查询当前租户资源（true）或包含共享资源（false）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数，0 表示默认企业项目）")
    parser.add_argument("--vpc-id", dest="vpc_id",
                        help="按 VPC ID 过滤（仅 --resource attachment）")
    parser.add_argument("--sort-key", dest="sort_key",
                        choices=("id", "name", "state"),
                        help="排序字段（id / name / state）")
    parser.add_argument("--sort-dir", dest="sort_dir",
                        choices=("asc", "desc"), help="排序方向（asc / desc）")
    parser.add_argument("--default-association-table", dest="default_association",
                        choices=("true", "false"),
                        help="仅查询默认关联路由表（route-table；true/false）")
    parser.add_argument("--default-propagation-table", dest="default_propagation",
                        choices=("true", "false"),
                        help="仅查询默认传播路由表（route-table；true/false）")
    parser.add_argument("--page-size", "--limit", type=int,
                        default=DEFAULT_PAGE_SIZE, dest="page_size",
                        help="分页大小（默认 %d，范围 %d~%d）"
                             % (DEFAULT_PAGE_SIZE, MIN_PAGE_SIZE, MAX_PAGE_SIZE))
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退时需要）")
    parser.add_argument("--operation", default=None,
                        help="hcloud ER 操作名（缺省随 --resource 选择；仅允许只读操作）")
    raw_argv = argv if argv is not None else sys.argv[1:]

    # The write-intent guard runs on the RAW argv BEFORE argparse, so a
    # mutating flag (e.g. `--operation DeleteEnterpriseRouter`) is reported as a
    # guard violation instead of an argparse "unrecognized argument" error.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except ErListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        _validate_page_size(args.page_size)
        allowed_operation = RESOURCE_OPERATIONS[args.resource]
        guard_operation(args.operation or allowed_operation,
                        allowed=allowed_operation)

        owned_by_self = (None if args.owned_by_self is None
                         else args.owned_by_self == "true")
        default_association = (None if args.default_association is None
                               else args.default_association == "true")
        default_propagation = (None if args.default_propagation is None
                               else args.default_propagation == "true")

        if args.resource == "attachment":
            _require_er_id(args)
            records = list_attachments(
                args.region, args.er_id, state=args.state, vpc_id=args.vpc_id,
                sort_key=args.sort_key, sort_dir=args.sort_dir,
                limit=args.page_size, project_id=args.project_id)
        elif args.resource == "route-table":
            _require_er_id(args)
            records = list_route_tables(
                args.region, args.er_id, state=args.state,
                is_default_association_table=default_association,
                is_default_propagation_table=default_propagation,
                sort_key=args.sort_key, sort_dir=args.sort_dir,
                limit=args.page_size, project_id=args.project_id)
        elif args.resource == "detail":
            _require_er_id(args)
            instance = show_er(args.region, args.er_id,
                               project_id=args.project_id)
            if args.as_json:
                print(json.dumps(instance, ensure_ascii=False, indent=2))
                return 0
            if args.table:
                print(render_fixed_table([instance], ER_TABLE_COLUMNS))
                return 0
            print(render_detail(instance, args.region))
            return 0
        else:
            records = list_ers(
                args.region, state=args.state, er_id=args.er_id,
                owned_by_self=owned_by_self,
                enterprise_project_id=args.enterprise_project_id,
                sort_key=args.sort_key, sort_dir=args.sort_dir,
                limit=args.page_size, project_id=args.project_id)
    except ErListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    records = apply_local_filters(records, name=args.name, fuzzy=args.fuzzy)

    if args.as_json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
        return 0

    filters = _collect_filters(args)
    suffix = _filter_suffix(filters)

    if args.resource == "attachment":
        if not records:
            print("企业路由器 %s 无 VPC 连接（VPC Attachment）%s。"
                  % (args.er_id, suffix))
            return 0
        if args.table:
            print("企业路由器 %s 的 VPC 连接（VPC Attachment）列表（共 %d 个）："
                  % (args.er_id, len(records)))
            print(render_sections(
                records, ATTACHMENT_TABLE_COLUMNS,
                "正常（available）连接（%d 个）：",
                "非 available 状态的 VPC 连接（%d 个，单独列出，请重点关注）："))
            return 0
        print("企业路由器 %s 的 VPC 连接（VPC Attachment）列表（共 %d 个）："
              % (args.er_id, len(records)))
        print(render_compact_sections(
            records, compact_attachment_line,
            "正常（available）连接（%d 个）：",
            "非 available 状态的 VPC 连接（%d 个，单独列出，请重点关注）："))
        return 0

    if args.resource == "route-table":
        if not records:
            print("企业路由器 %s 无路由表（Route Table）%s。"
                  % (args.er_id, suffix))
            return 0
        title = ("企业路由器 %s 的路由表（Route Table）列表（共 %d 个）："
                 % (args.er_id, len(records)))
        if args.table:
            print(title)
            print(render_fixed_table(records, ROUTE_TABLE_COLUMNS))
        else:
            print(title)
            print("\n".join(compact_route_table_line(r) for r in records))
        return 0

    # --resource er
    if not records:
        print("当前区域（%s）无企业路由器（ER）%s。" % (args.region, suffix))
        return 0
    if args.table:
        print("Region %s 的企业路由器（ER）列表（共 %d 个）："
              % (args.region, len(records)))
        print(render_sections(
            records, ER_TABLE_COLUMNS,
            "正常（available）企业路由器（%d 个）：",
            "非 available 状态的企业路由器（%d 个，单独列出，请重点关注）："))
        return 0
    print("Region %s 的企业路由器（ER）列表（共 %d 个）："
          % (args.region, len(records)))
    print(render_compact_sections(
        records, compact_er_line,
        "正常（available）企业路由器（%d 个）：",
        "非 available 状态的企业路由器（%d 个，单独列出，请重点关注）："))
    return 0


if __name__ == "__main__":
    sys.exit(main())