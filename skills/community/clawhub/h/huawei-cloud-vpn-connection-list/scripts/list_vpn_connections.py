#!/usr/bin/env python3
"""Inventory Huawei Cloud VPN gateways and IPSec connections (strictly read-only).

Primary execution path is KooCLI:

    hcloud VPN ListVgws            -> GET /v5/{project_id}/vpn-gateways
    hcloud VPN ListVpnConnections  -> GET /v5/{project_id}/vpn-connection

Both operations were verified against KooCLI 7.3.12 (`hcloud VPN --help`) and
the official `huaweicloudsdkvpn` v5 client `_list_vgws_http_info` /
`_list_vpn_connections_http_info` metadata. When hcloud is not installed the
script falls back to the official `huaweicloudsdkvpn` v5 SDK
(`VpnClient.list_vgws` / `VpnClient.list_vpn_connections`).

Output modes:
    default        compact per-gateway list + a dedicated non-UP section
    --table        two tables: 9 gateway columns and 7 connection columns,
                   non-UP connections split into their own table
    --json         machine-readable object (vpn_gateways / vpn_connections)

The skill is read-only by design: a write-intent guard rejects any mutating
intent (create / update / delete a gateway or connection, reset a connection,
update the PSK, tag changes, SSL VPN server operations, ...) before a single
command runs. PSK material is never read, printed, or persisted — any `psk*`
key returned by an API is stripped from every output.

Usage:
    python3 scripts/list_vpn_connections.py [--region cn-north-4]
                                            [--table | --json]
                                            [--name NAME [--fuzzy]]
                                            [--gateway-id VGW_ID]
                                            [--status DOWN]
                                            [--limit 100]
                                            [--project-id <id>]
                                            [--operation ListVgws]

Environment overrides (mostly for tests):
    VPN_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    VPN_LIST_HCLOUD_ARGS  extra args injected before the VPN operation
    VPN_LIST_SQC_BIN      skill-quality-cli executable override
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

DEFAULT_REGION = "cn-north-4"
# ListVpnConnections paging size (spec range 1-100).
DEFAULT_LIMIT = 100
SERVICE = "VPN"
ALLOWED_OPERATIONS = ("ListVgws", "ListVpnConnections")
GATEWAY_REST_PATH = "/v5/{project_id}/vpn-gateways"
CONNECTION_REST_PATH = "/v5/{project_id}/vpn-connection"

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli (the mandatory wrapping 口径). When the
# CLI is unavailable — or SKILL_QUALITY_REPORT=0 — the call degrades to bare
# hcloud.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-vpn-connection-list"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# Statuses that mean "the tunnel negotiated successfully". Everything else
# that carries a real status value is treated as 非 UP (DOWN / ERROR /
# PENDING_* / ...) and rendered in the dedicated troubleshooting section.
UP_STATUSES = ("ACTIVE", "UP")

# Options whose values are user-supplied filters/parameters. They are not
# scanned by the write-intent guard: a gateway literally named `prod-start`
# or a status value must not be mistaken for a mutating operation.
_VALUE_OPTIONS = (
    "--region",
    "-r",
    "--name",
    "--status",
    "--gateway-id",
    "--vgw-id",
    "--limit",
    "--project-id",
)

# Mutating VPN operations / intents — strictly rejected by the guard.
# Includes IPSec connection lifecycle, VPN gateway lifecycle, customer
# gateways, PSK updates, SSL VPN (P2C) server/user management and tagging.
WRITE_INTENT_KEYWORDS = (
    "createvgw",
    "deletevgw",
    "updatevgw",
    "updatepostpaidvgwspecification",
    "createvpnconnection",
    "batchcreatevpnconnection",
    "deletevpnconnection",
    "batchdeletevpnconnection",
    "resetvpnconnection",
    "updatevpnconnection",
    "createcgw",
    "deletecgw",
    "updatecgw",
    "createvpnserver",
    "deletevpnserver",
    "createvpnuser",
    "deletevpnuser",
    "batchcreatevpnusers",
    "batchdeletevpnusers",
    "addvpnuserstogroup",
    "removevpnusersfromgroup",
    "resetvpnuserpassword",
    "createvpnusergroup",
    "deletevpnusergroup",
    "createvpnaccesspolicy",
    "deletevpnaccesspolicy",
    "createp2cvgw",
    "deletep2cvgw",
    "updatep2cvgw",
    "deletep2cvpnqwgatewayjob",
    "createconnectionmonitor",
    "deleteconnectionmonitor",
    "createvgwcertificate",
    "deletevgwcertificate",
    "updategwcertificate",
    "importclientca",
    "deleteclientca",
    "exportclientconfig",
    "exportvpnconnectionpeerconfiguration",
    "batchcreateresourcetags",
    "batchdeleteresourcetags",
    "deletevpnconnectionslogconfig",
    "updatepsk",
    "psk",
    "create",
    "delete",
    "update",
    "modify",
    "reset",
    "restart",
    "reboot",
    "import",
    "export",
    "associate",
    "disassociate",
    "dissociate",
    "attach",
    "detach",
    "bind",
    "unbind",
    "release",
    "remove",
    "destroy",
    "change",
    "upgrade",
    "stop",
    "start",
)

# Gateway table columns (exactly 9).
GATEWAY_COLUMNS = (
    ("id", "网关ID"),
    ("name", "名称"),
    ("status", "状态"),
    ("flavor", "规格"),
    ("attachment_type", "接入类型"),
    ("vpc_id", "VPC"),
    ("local_subnets", "本端子网"),
    ("_eip", "EIP"),
    ("_connections", "连接数"),
)

# Connection table columns (exactly 7).
CONNECTION_COLUMNS = (
    ("id", "连接ID"),
    ("name", "名称"),
    ("status", "状态"),
    ("vgw_id", "网关ID"),
    ("vgw_ip", "网关IP"),
    ("peer_subnets", "对端网段"),
    ("created_at", "创建时间"),
)

_GATEWAY_LIST_KEYS = ("vpn_gateways", "vpnGateways")
_CONNECTION_LIST_KEYS = ("vpn_connections", "vpnConnections")

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

# VPN returns 403 as `VPN.0007 ... is not authorized to perform:
# vpn:vpnGateways:list ...` (observed against cn-north-4).
_AUTH_403_PATTERNS = (
    "403",
    "not authorized",
    "notallowed",
    "permission denied",
    "权限不足",
    "无权限",
    "vpn.0007",
)

_AUTH_401_PATTERNS = (
    "401",
    "unauthorized",
    "apigw.0301",
    "认证失败",
    "token expired",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — treated as a hard failure even then.
_USE_ERROR_MARKER = "[use_error]"

_SECRET_KEY_NAMES = (
    "psk",
    "pre_shared_key",
    "pre_shared_key_encrypted",
    "psk_encrypted",
    "psk_plaintext",
)


class VpnListError(Exception):
    """Base error for the VPN connection inventory skill."""


class GuardError(VpnListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(VpnListError):
    """hcloud missing or credentials (AK/SK) / project id not configured."""


class AuthError(VpnListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(VpnListError):
    """hcloud / network / unexpected API failure."""


class NotFoundError(VpnListError):
    """--gateway-id points at a VPN gateway that does not exist."""


# --------------------------------------------------------------------------
# Write-intent guard
# --------------------------------------------------------------------------

def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-vgw`, `CreateVgw`, and
    `create_vgw` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe/table/json) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读盘点"
                "（VPN ListVgws / ListVpnConnections），VPN 网关与 IPSec 连接的"
                "创建、修改、删除、重置、PSK 变更等操作已被守卫拦截。" % keyword
            )
    return False


def guard_scan_text(argv):
    """Build the guard scan text, keeping operation/command tokens only.

    Values of user-facing filter options (``--name`` / ``--status`` / ...) are
    dropped so a legitimate read-only query is never blocked just because a
    gateway name or status value contains a mutating verb.
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
    """Only the read-only ListVgws / ListVpnConnections operations may run."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, " / ".join(ALLOWED_OPERATIONS))
        )
    return True


# --------------------------------------------------------------------------
# Command construction
# --------------------------------------------------------------------------

def build_gateway_command(region, gateway_id=None):
    """Build the hcloud VPN ListVgws argv (without the executable).

    ListVgws (GET /v5/{project_id}/vpn-gateways) takes only `vgw_id` and
    `enterprise_project_id` — it has no limit/marker, the whole list is
    returned in one response.
    """
    argv = [SERVICE, "ListVgws", "--cli-region=%s" % region]
    if gateway_id:
        argv.append("--vgw_id=%s" % gateway_id)
    return argv


def build_connection_command(region, gateway_id=None, limit=DEFAULT_LIMIT,
                             marker=None):
    """Build the hcloud VPN ListVpnConnections argv (page request).

    ListVpnConnections (GET /v5/{project_id}/vpn-connection) pages with
    `limit` + `marker`, where the marker is the creation time of the last
    record of the previous page (`page_info.next_marker`).
    """
    argv = [
        SERVICE,
        "ListVpnConnections",
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if gateway_id:
        argv.append("--vgw_id=%s" % gateway_id)
    return argv


def _hcloud_executable():
    return os.environ.get("VPN_LIST_HCLOUD_BIN") or "hcloud"


def _hcloud_resolvable():
    """True when the hcloud executable can actually be launched.

    Checked *before* wrapping the command with skill-quality-cli: the wrapper
    would otherwise swallow a missing-hcloud failure into its own non-zero exit,
    which ``run_hcloud`` cannot tell apart from a genuine CLI error — and that
    would silently disable the SDK fallback.
    """
    exe = _hcloud_executable()
    if os.path.dirname(exe):
        return os.path.isfile(exe) and os.access(exe, os.X_OK)
    return shutil.which(exe) is not None


def _quality_report_enabled():
    value = os.environ.get("SKILL_QUALITY_REPORT")
    if value is None:
        return True
    return value.strip().lower() not in _QUALITY_OFF_VALUES


def _skill_quality_executable():
    override = os.environ.get("VPN_LIST_SQC_BIN")
    if override:
        return override
    found = shutil.which("skill-quality-cli")
    if found:
        return found
    local = os.path.join(os.path.expanduser("~"), ".local", "bin",
                         "skill-quality-cli")
    if os.path.isfile(local) and os.access(local, os.X_OK):
        return local
    return None


def _hcloud_argv(argv):
    cmd = [_hcloud_executable()]
    # VPN_LIST_HCLOUD_ARGS is a test-only hook (inject fake CLI flags such as
    # `--cli-profile`); it must never be used to smuggle extra production
    # tokens, so it is documented here rather than exposed in the CLI help.
    extra = os.environ.get("VPN_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-vpn-connection-list -- hcloud ...`` (the mandatory wrapping
    口径, enforced here on the script path too). The command degrades to bare
    hcloud when the telemetry CLI is missing or ``SKILL_QUALITY_REPORT=0``; an
    explicit ``VPN_LIST_HCLOUD_BIN`` override (offline mock / verification) is
    run verbatim. When hcloud itself is not resolvable the wrapping is skipped
    so ``run_hcloud`` raises ``FileNotFoundError`` → ``ConfigError`` → SDK
    fallback.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("VPN_LIST_HCLOUD_BIN"):
        return hcloud_cmd
    if not _hcloud_resolvable():
        return hcloud_cmd
    if not _quality_report_enabled():
        return hcloud_cmd
    quality_cli = _skill_quality_executable()
    if not quality_cli:
        return hcloud_cmd
    return ([quality_cli, "run", "--skill-name", SKILL_QUALITY_SKILL_NAME, "--"]
            + hcloud_cmd)


def run_hcloud(argv):
    """Execute hcloud through skill-quality-cli when available."""
    extra = os.environ.get("VPN_LIST_HCLOUD_ARGS", "").split()
    if extra:
        guard_write_intent(" ".join(extra))
    cmd = build_hcloud_command(argv)
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


# --------------------------------------------------------------------------
# Response parsing
# --------------------------------------------------------------------------

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
    """Return the error text if a payload is an API error envelope.

    KooCLI prints HTTP-level API errors (e.g. ``VPN.0007 ... is not
    authorized``) on **stdout with exit code 0**. Such an envelope has no
    gateway/connection list key, so it must be surfaced as an explicit error
    instead of being read as an empty inventory.
    """
    if not isinstance(payload, dict):
        return None
    list_keys = _GATEWAY_LIST_KEYS + _CONNECTION_LIST_KEYS
    if any(isinstance(payload.get(key), list) for key in list_keys):
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


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：VPN ListVgws 与 "
            "ListVpnConnections 的真实参数清单可通过 `hcloud VPN ListVgws --help` / "
            "`hcloud VPN ListVpnConnections --help` 查看。详情：%s"
            % (returncode, blob[:300])
        )
    has_401 = any(p in low for p in _AUTH_401_PATTERNS)
    has_403 = any(p in low for p in _AUTH_403_PATTERNS)
    if has_401 and not has_403:
        return AuthError(
            "凭证无效（401：AK/SK 无效或已过期），请重新配置 hcloud 凭证后重试，"
            "参见 references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if has_403:
        return AuthError(
            "无权限访问 VPN 网关 / IPSec 连接，请检查 IAM 权限（403：需要 "
            "vpn:vpnGateways:list 与 vpn:vpnConnections:list），参见 "
            "references/iam-policies.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_gateways(payload):
    """Pull the VPN gateway list out of a ListVgws response."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in _GATEWAY_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def extract_connections(payload):
    """Pull the IPSec connection list out of a ListVpnConnections response."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in _CONNECTION_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def extract_next_marker(payload):
    """Return `page_info.next_marker` of a ListVpnConnections response."""
    if not isinstance(payload, dict):
        return None
    page_info = payload.get("page_info") or payload.get("pageInfo")
    if isinstance(page_info, dict):
        value = page_info.get("next_marker") or page_info.get("nextMarker")
        return str(value) if value else None
    return None


def strip_secrets(value):
    """Recursively drop PSK material from any payload before output.

    The v5 response model does not expose the PSK, but the stripping is kept as
    defence in depth: a PSK must never be printed, exported or persisted by
    this skill.
    """
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if str(key).lower() in _SECRET_KEY_NAMES:
                continue
            if "psk" in str(key).lower():
                continue
            out[key] = strip_secrets(item)
        return out
    if isinstance(value, list):
        return [strip_secrets(item) for item in value]
    return value


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


# --------------------------------------------------------------------------
# SDK fallback
# --------------------------------------------------------------------------

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


def _sdk_request_classes():
    """Import the SDK request/facade classes (raises ConfigError if absent)."""
    try:
        from huaweicloudsdkvpn.v5 import ListVgwsRequest, ListVpnConnectionsRequest
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkvpn 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkvpn。详情：%s" % exc
        )
    return ListVgwsRequest, ListVpnConnectionsRequest


def _sdk_client(region, project_id):
    """Build an authenticated huaweicloudsdkvpn v5 client.

    Credentials come from the whitelisted AK/SK environment variables
    (HW_*/HUAWEI_ACCESS_KEY family) — never from literals. The v5 REST paths
    are `/v5/{project_id}/...`, so the project id is mandatory. Credential and
    project-id checks run before the SDK import so a missing configuration is
    reported as a configuration error even on hosts without the SDK.
    """
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
            "SDK 回退缺少 project_id：VPN 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。"
            % (GATEWAY_REST_PATH + " 、" + CONNECTION_REST_PATH)
        )
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkvpn.v5 import VpnClient
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkvpn 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkvpn。详情：%s" % exc
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            from huaweicloudsdkvpn.v5.region.vpn_region import VpnRegion
            region_obj = VpnRegion.value_of(region)
        except (ImportError, ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://vpn.%s.myhuaweicloud.com" % region)
        return VpnClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkvpn 安装与区域配置。"
            % (region, exc)
        )


def _sdk_auth_error(exc):
    """Build an AuthError distinguishing 401 (bad credentials) from 403."""
    low = str(exc).lower()
    status = getattr(exc, "status_code", None)
    detail = str(exc)[:300]
    if status == 401 or "401" in low or "unauthorized" in low or "apigw.0301" in low:
        return AuthError(
            "凭证无效（401：AK/SK 无效或已过期），请重新配置 AK/SK 后重试，参见"
            " references/cli-installation-guide.md。详情：%s" % detail
        )
    return AuthError(
        "无权限访问 VPN 网关 / IPSec 连接，请检查 IAM 权限（403：未授予 VPN "
        "vpn:vpnGateways:list 与 vpn:vpnConnections:list 只读权限），参见"
        " references/iam-policies.md。详情：%s" % detail
    )


def list_vpn_gateways_via_sdk(region, gateway_id=None, project_id=None):
    """SDK fallback: query VPN gateways through `huaweicloudsdkvpn` v5."""
    ListVgwsRequest, _ = _sdk_request_classes()
    client = _sdk_client(region, project_id)
    request = ListVgwsRequest(vgw_id=gateway_id or None)
    try:
        response = client.list_vgws(request)
    except Exception as exc:
        low = str(exc).lower()
        status = getattr(exc, "status_code", None)
        if any(p in low for p in _AUTH_403_PATTERNS) or any(
                p in low for p in _AUTH_401_PATTERNS) or status in (401, 403):
            raise _sdk_auth_error(exc)
        raise ApiError("SDK 调用失败（list_vgws）：%s" % str(exc)[:300])
    gateways = [_jsonable(item.to_dict()) for item in (response.vpn_gateways or [])]
    return strip_secrets(gateways)


def list_vpn_connections_via_sdk(region, gateway_id=None, limit=DEFAULT_LIMIT,
                                 project_id=None, max_pages=100):
    """SDK fallback: query IPSec connections through `huaweicloudsdkvpn` v5."""
    _, ListVpnConnectionsRequest = _sdk_request_classes()
    client = _sdk_client(region, project_id)
    connections = []
    marker = None
    for _page in range(max_pages):
        request = ListVpnConnectionsRequest(
            limit=limit,
            marker=marker,
            vgw_id=gateway_id or None,
        )
        try:
            response = client.list_vpn_connections(request)
        except Exception as exc:
            low = str(exc).lower()
            status = getattr(exc, "status_code", None)
            if any(p in low for p in _AUTH_403_PATTERNS) or any(
                    p in low for p in _AUTH_401_PATTERNS) or status in (401, 403):
                raise _sdk_auth_error(exc)
            raise ApiError(
                "SDK 调用失败（list_vpn_connections）：%s" % str(exc)[:300])
        batch = list(response.vpn_connections or [])
        connections.extend(
            strip_secrets(_jsonable(item.to_dict())) for item in batch)
        page_info = getattr(response, "page_info", None)
        next_marker = None
        if page_info is not None:
            next_marker = getattr(page_info, "next_marker", None)
            if not next_marker and isinstance(page_info, dict):
                next_marker = page_info.get("next_marker")
        if not next_marker or str(next_marker) == str(marker or ""):
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return connections


# --------------------------------------------------------------------------
# Fetch (CLI first, SDK fallback)
# --------------------------------------------------------------------------

def list_vpn_gateways(region, gateway_id=None, project_id=None):
    """Query every VPN gateway in the region (ListVgws has no paging)."""
    argv = build_gateway_command(region, gateway_id=gateway_id)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        return list_vpn_gateways_via_sdk(
            region, gateway_id=gateway_id, project_id=project_id)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode)
    payload = extract_json(stdout)
    envelope_error = _payload_error(payload)
    if envelope_error:
        raise classify_hcloud_failure(envelope_error, stderr, returncode)
    return strip_secrets(extract_gateways(payload))


def list_vpn_connections(region, gateway_id=None, limit=DEFAULT_LIMIT,
                         project_id=None, max_pages=100):
    """Query every IPSec connection in the region (marker-paged)."""
    connections = []
    marker = None
    for _page in range(max_pages):
        argv = build_connection_command(
            region, gateway_id=gateway_id, limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            return list_vpn_connections_via_sdk(
                region, gateway_id=gateway_id, limit=limit,
                project_id=project_id, max_pages=max_pages)
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        envelope_error = _payload_error(payload)
        if envelope_error:
            raise classify_hcloud_failure(envelope_error, stderr, returncode)
        batch = strip_secrets(extract_connections(payload))
        connections.extend(batch)
        next_marker = extract_next_marker(payload)
        if not batch or not next_marker or str(next_marker) == str(marker or ""):
            break
        if len(batch) < limit:
            break
        marker = next_marker
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return connections


# --------------------------------------------------------------------------
# Filtering
# --------------------------------------------------------------------------

def _text(value):
    return "" if value is None else str(value)


def status_of(item):
    """Upper-cased status of a gateway/connection (empty string when absent)."""
    return _text(item.get("status")).strip().upper()


def is_up(item):
    """True when the tunnel state is a successful one (ACTIVE / UP)."""
    return status_of(item) in UP_STATUSES


def is_not_up(item):
    """True for a real non-UP state (DOWN / ERROR / PENDING_* / ...)."""
    status = status_of(item)
    return bool(status) and status not in UP_STATUSES


def _name_matches(name, wanted, fuzzy):
    name = _text(name)
    if not name:
        return False
    if fuzzy:
        return wanted.lower() in name.lower()
    return name == wanted


def filter_inventory(gateways, connections, name=None, fuzzy=False,
                     status=None, gateway_id=None, region=""):
    """Apply the client-side filters.

    Order: gateway-id drilldown (raises NotFoundError when the id does not
    exist) → name (gateway name or connection name) → connection status
    (narrows the gateway view to gateways that hold a matching connection).
    """
    if gateway_id:
        gateways = [g for g in gateways if _text(g.get("id")) == gateway_id]
        connections = [c for c in connections
                       if _text(c.get("vgw_id")) == gateway_id]
        if not gateways:
            raise NotFoundError(
                "未找到 VPN 网关（vgw_id=%s）：该 ID 在当前区域（%s）不存在或无权访问。"
                "请先不带 --gateway-id 运行本 skill，确认网关 ID 后再下钻。"
                % (gateway_id, region or "见 --region"))

    if name:
        gateway_ids = {_text(g.get("id")) for g in gateways
                       if _name_matches(g.get("name"), name, fuzzy)}
        for connection in connections:
            if _name_matches(connection.get("name"), name, fuzzy):
                gateway_ids.add(_text(connection.get("vgw_id")))
        gateways = [g for g in gateways if _text(g.get("id")) in gateway_ids]
        connections = [c for c in connections
                       if _text(c.get("vgw_id")) in gateway_ids]

    if status:
        wanted = status.strip().upper()
        connections = [c for c in connections if status_of(c) == wanted]
        matching_ids = {_text(c.get("vgw_id")) for c in connections}
        gateways = [g for g in gateways if _text(g.get("id")) in matching_ids]

    return gateways, connections


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def _field(item, *names, default="-"):
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _join(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value) or "-"
    return _text(value) or "-"


def gateway_eips(gateway):
    """Join the gateway public IPs (eip1 / eip2) into one cell."""
    parts = []
    for key in ("eip1", "eip2"):
        eip = gateway.get(key)
        if isinstance(eip, dict):
            ip = eip.get("ip_address") or eip.get("public_ip") or eip.get("id")
            if ip:
                parts.append(str(ip))
        elif isinstance(eip, str) and eip:
            parts.append(eip)
    return ", ".join(parts) if parts else "-"


def _connection_count_cell(gateway, connections):
    used = gateway.get("used_connection_number")
    total = gateway.get("connection_number")
    if used is None and total is None:
        return str(len([c for c in connections
                        if _text(c.get("vgw_id")) == _text(gateway.get("id"))]))
    return "%s/%s" % (used if used is not None else "-",
                      total if total is not None else "-")


def _gateway_value(gateway, key, connections):
    if key == "_eip":
        return gateway_eips(gateway)
    if key == "_connections":
        return _connection_count_cell(gateway, connections)
    if key == "local_subnets":
        return _join(gateway.get("local_subnets")) if gateway.get("local_subnets") else "-"
    return _cell(_field(gateway, key))


def _connection_value(connection, key):
    if key in ("peer_subnets", "peer_subnets_v6"):
        value = _join(connection.get(key))
        return value
    return _cell(_field(connection, key))


def _display_width(text):
    """Terminal cell width of `text` (CJK wide characters count as 2)."""
    width = 0
    for char in str(text):
        width += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
    return width


def _pad(text, width):
    return str(text) + " " * max(0, width - _display_width(text))


def _render_rows(columns, rows):
    widths = []
    for index, (_, title) in enumerate(columns):
        widths.append(max(_display_width(title),
                          *(_display_width(row[index]) for row in rows)))
    header = "  ".join(_pad(title, widths[i])
                       for i, (_, title) in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(_pad(row[i], widths[i])
                               for i in range(len(columns))))
    return lines


def render_gateway_table(gateways, connections):
    rows = [[_gateway_value(g, key, connections) for key, _ in GATEWAY_COLUMNS]
            for g in gateways]
    return _render_rows(GATEWAY_COLUMNS, rows)


def render_connection_table(connections):
    rows = [[_connection_value(c, key) for key, _ in CONNECTION_COLUMNS]
            for c in connections]
    return _render_rows(CONNECTION_COLUMNS, rows)


def _connection_brief(connection):
    return "- %s  %s  status=%s  网关=%s  对端网段=%s  隧道=%s->%s" % (
        _cell(_field(connection, "id")),
        _cell(_field(connection, "name")),
        _cell(_field(connection, "status")),
        _cell(_field(connection, "vgw_id")),
        _join(connection.get("peer_subnets")),
        _cell(_field(connection, "tunnel_local_address")),
        _cell(_field(connection, "tunnel_peer_address")),
    )


def _gateway_brief(gateway, connections):
    vpc = _field(gateway, "vpc_id", "access_vpc_id", "er_id")
    group = [c for c in connections
             if _text(c.get("vgw_id")) == _text(gateway.get("id"))]
    up = len([c for c in group if is_up(c)])
    down = len([c for c in group if is_not_up(c)])
    return "- %s  %s  %s  vpc/er=%s  EIP=%s  连接 %d 条（UP %d / 非UP %d）" % (
        _cell(_field(gateway, "id")),
        _cell(_field(gateway, "name")),
        _cell(_field(gateway, "status")),
        _cell(vpc),
        gateway_eips(gateway),
        len(group), up, down,
    )


def _split_connections(connections):
    up = [c for c in connections if is_up(c)]
    down = [c for c in connections if is_not_up(c)]
    unknown = [c for c in connections if not status_of(c)]
    return up, down, unknown


def render_default(region, gateways, connections):
    """Compact list: one line per gateway + a dedicated non-UP section."""
    lines = []
    if not gateways:
        lines.append("当前区域（%s）无 VPN 网关。" % region)
        return lines
    lines.append("Region %s 的 VPN 网关（共 %d 个）：" % (region, len(gateways)))
    for gateway in gateways:
        lines.append(_gateway_brief(gateway, connections))

    up, down, unknown = _split_connections(connections)
    lines.append("")
    if down:
        lines.append("⚠ 非 UP 连接（%d 条，需优先排查）：" % len(down))
        for connection in down:
            lines.append(_connection_brief(connection))
    else:
        lines.append("✓ 无非 UP 连接：全部 IPSec 连接均已协商成功。")

    if unknown:
        lines.append("")
        lines.append("状态未知的连接（%d 条）：" % len(unknown))
        for connection in unknown:
            lines.append(_connection_brief(connection))

    known = len(up) + len(down)
    lines.append("")
    lines.append("合计：网关 %d 个，IPSec 连接 %d 条（UP %d / 非UP %d）。"
                 % (len(gateways), known, len(up), len(down)))
    return lines


def render_tables(region, gateways, connections):
    """Two-table view: 9 gateway columns and 7 connection columns."""
    lines = []
    if not gateways:
        lines.append("当前区域（%s）无 VPN 网关。" % region)
        return lines
    lines.append("【VPN 网关】Region %s，共 %d 个" % (region, len(gateways)))
    lines.extend(render_gateway_table(gateways, connections))

    up, down, unknown = _split_connections(connections)
    lines.append("")
    lines.append("【IPSec 连接 · UP】共 %d 条" % len(up))
    if up:
        lines.extend(render_connection_table(up))
    else:
        lines.append("（无）")

    lines.append("")
    if down:
        lines.append("⚠【IPSec 连接 · 非 UP】共 %d 条，需优先排查" % len(down))
        lines.extend(render_connection_table(down))
    else:
        lines.append("✓【IPSec 连接 · 非 UP】共 0 条")

    if unknown:
        lines.append("")
        lines.append("【IPSec 连接 · 状态未知】共 %d 条" % len(unknown))
        lines.extend(render_connection_table(unknown))
    return lines


def summarize(gateways, connections):
    up, down, unknown = _split_connections(connections)
    return {
        "gateway_count": len(gateways),
        "connection_count": len(up) + len(down),
        "up_count": len(up),
        "not_up_count": len(down),
        "unknown_status_count": len(unknown),
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _limit(value):
    """Validate --limit against the documented 1-100 range."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("--limit 必须是整数：%r" % value)
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError(
            "--limit 超出范围（1-100）：%d。ListVpnConnections 分页大小取 1-100。"
            % number)
    return number


def build_parser():
    parser = argparse.ArgumentParser(
        prog="list_vpn_connections.py",
        description="盘点华为云 VPN 网关与 IPSec 连接（KooCLI hcloud VPN ListVgws / "
                    "ListVpnConnections，严格只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--table", action="store_true",
                        help="双表格视图（网关 9 列 + 连接 7 列，非 UP 连接单独分区）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段（网关数组 + 连接数组 + 汇总）")
    parser.add_argument("--name", help="按名称过滤（网关名或连接名，客户端过滤）")
    parser.add_argument("--fuzzy", action="store_true",
                        help="配合 --name 做子串模糊匹配（默认精确匹配）")
    parser.add_argument("--gateway-id", dest="gateway_id",
                        help="按 VPN 网关 ID 下钻（同时作为服务端 vgw_id 查询参数）")
    parser.add_argument("--status",
                        help="按 IPSec 连接状态过滤（客户端过滤，如 DOWN / ACTIVE）")
    parser.add_argument("--limit", type=_limit, default=DEFAULT_LIMIT,
                        help="ListVpnConnections 分页大小（1-100，默认 %d）"
                             % DEFAULT_LIMIT)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v5/{project_id}/... 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATIONS[0],
                        help="hcloud VPN 操作名（仅允许只读 %s）"
                             % " / ".join(ALLOWED_OPERATIONS))
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    raw_argv = argv if argv is not None else sys.argv[1:]

    try:
        # Write-intent guard: scan operation/command tokens only (filter
        # values such as --name / --status are legitimate read-only input).
        guard_write_intent(guard_scan_text(raw_argv))
        guard_operation(args.operation)
        gateways = list_vpn_gateways(
            args.region, gateway_id=args.gateway_id, project_id=args.project_id)
        connections = list_vpn_connections(
            args.region, gateway_id=args.gateway_id, limit=args.limit,
            project_id=args.project_id)
        gateways, connections = filter_inventory(
            gateways, connections,
            name=args.name, fuzzy=args.fuzzy,
            status=args.status, gateway_id=args.gateway_id, region=args.region,
        )
        # Defence in depth: no PSK material may reach any output mode.
        gateways = strip_secrets(gateways)
        connections = strip_secrets(connections)
    except VpnListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps({
            "region": args.region,
            "vpn_gateways": gateways,
            "vpn_connections": connections,
            "summary": summarize(gateways, connections),
        }, ensure_ascii=False, indent=2))
        return 0

    filters = []
    if args.name:
        filters.append("name%s=%s" % ("~" if args.fuzzy else "=", args.name))
    if args.status:
        filters.append("status=%s" % args.status)
    if args.gateway_id:
        filters.append("gateway-id=%s" % args.gateway_id)

    if not gateways and (args.name or args.status):
        print("当前区域（%s）无匹配的 VPN 网关 / IPSec 连接（过滤条件: %s）。"
              % (args.region, ", ".join(filters)))
        return 0

    if args.table:
        lines = render_tables(args.region, gateways, connections)
    else:
        lines = render_default(args.region, gateways, connections)
    if filters:
        lines.append("过滤条件：%s" % ", ".join(filters))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())