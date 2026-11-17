#!/usr/bin/env python3
"""List Huawei Cloud Virtual Private Cloud (VPC) resources via KooCLI.

Read-only entry point for two resource families of the VPC service:

* ``--resource vpc`` (default) — ``hcloud VPC ListVpcs`` (GET
  /v1/{project_id}/vpcs); when hcloud is not installed the script falls back
  to the official ``huaweicloudsdkvpc`` v2 SDK (``VpcClient.list_vpcs``).
* ``--resource peering`` — ``hcloud VPC ListVpcPeerings`` (GET
  /v2.0/{project_id}/vpc/peerings); SDK fallback uses
  ``ListVpcPeeringsRequest`` / ``VpcClient.list_vpc_peerings``.

Reads nothing but the active credential profile / environment. Supports
full-field table (default), --json, --names-only and --format md (local
Markdown report for the VPC resource; optional --output / --summary),
--id / --enterprise-project-id filters (real server-side query parameters;
ListVpcs ``--id`` is an array query parameter, emitted as ``--id.1=<vpc-id>``),
marker-based paging, and a strict write-intent guard: any argument that looks
like a mutating VPC operation is rejected before a single command is executed.

Usage:
    python3 scripts/list_vpc.py [--region cn-north-4] [--resource vpc|peering]
                                [--json | --names-only]
                                [--format table|json|names|md]
                                [--output <path.md>] [--summary]
                                [--id <vpc-id>] [--enterprise-project-id <id>]
                                [--page-size 100] [--project-id <id>]
                                [--operation ListVpcs|ListVpcPeerings]

Environment overrides (mostly for tests):
    VPC_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    VPC_LIST_HCLOUD_ARGS  extra args injected before the VPC operation
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
DEFAULT_FORMAT = "table"
SERVICE = "VPC"
ALLOWED_OPERATION = "ListVpcs"
PEERING_OPERATION = "ListVpcPeerings"
RESOURCE_OPERATIONS = {
    "vpc": ALLOWED_OPERATION,
    "peering": PEERING_OPERATION,
}
REST_PATH = "/v1/{project_id}/vpcs"
PEERING_REST_PATH = "/v2.0/{project_id}/vpc/peerings"
PEERING_TABLE_COLUMNS = ("name", "local_vpc", "peer_vpc", "status")

# Markdown report column order (the first column is the required VPC name) —
# kept identical to huawei-cloud-vpc-export-markdown (8 fixed columns).
MD_HEADERS = [
    "VPC 名称", "VPC ID", "区域", "网段", "状态",
    "企业项目 ID", "描述", "创建时间",
]
DEFAULT_FILENAME_PREFIX = "vpc_list"
_FIELD_MISSING = "-"

# Values of these flags are pure file-path / format data and are excluded from
# the write-intent scan (e.g. a local path "vpc-delete-report.md").
_VALUE_STRIPPED_FLAGS = (
    "--output",
    "-o",
    "--format",
    "-f",
)

# Mutating VPC operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createvpc",
    "batchcreatevpcs",
    "deletevpc",
    "batchdeletevpcs",
    "updatevpc",
    "createsubnet",
    "batchcreatesubnets",
    "deletesubnet",
    "batchdeletesubnets",
    "updatesubnet",
    "createsecuritygroup",
    "deletesecuritygroup",
    "updatesecuritygroup",
    "createsecuritygrouprule",
    "deletesecuritygrouprule",
    "updatepublicip",
    "createport",
    "deleteport",
    "updateport",
    "createroutetable",
    "deleteroutetable",
    "createroute",
    "deleteroute",
    "createflowlog",
    "deleteflowlog",
    "updateflowlog",
    "createvpcpeering",
    "deletevpcpeering",
    "acceptvpcpeering",
    "rejectvpcpeering",
    "updatevpcpeering",
    "create",
    "delete",
    "update",
    "modify",
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
    "restart",
    "creating",
    "deleting",
    "updating",
    "associating",
    "disassociating",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "id",
    "name",
    "cidr",
    "status",
    "description",
    "enterprise_project_id",
    "tenant_id",
    "routes",
    "block_service_endpoint_states",
    "enable_network_address_usage_metrics",
    "created_at",
    "updated_at",
]

_VPC_LIST_KEYS = ("vpcs", "vpc")

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
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class VpcListError(Exception):
    """Base error for the VPC list skill."""


class GuardError(VpcListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(VpcListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(VpcListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(VpcListError):
    """hcloud / network / unexpected API failure."""


class ExportError(VpcListError):
    """The Markdown file could not be produced (bad path / write failure)."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-vpc`, `CreateVpc`, and `create_vpc` all
    hit the same keyword. Read-only vocabulary (list/show/get/describe) never
    matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（VPC ListVpcs / ListVpcPeerings），创建/删除/更新/绑定/解绑的变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation, allowed=ALLOWED_OPERATION):
    """Only the whitelisted read-only operation may be executed."""
    if operation != allowed:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, allowed)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Flag names and positional tokens are scanned, but the values of the local
    output/format flags (``--output`` / ``-o`` / ``--format`` / ``-f``) are
    stripped: they are pure file-path / format data and may legitimately
    contain write-looking words (e.g. a report path ``vpc-delete-report.md``).
    Filter values (``--id`` etc.) are still scanned, so a mutating value cannot
    hide behind a filter flag.

    A *flag* following such an option is never swallowed: a following token
    that starts with ``-`` is still scanned.
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    for tok in tokens:
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


def build_command(region, vpc_id=None, enterprise_project_id=None,
                  limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud VPC ListVpcs argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only VPC ListVpcs
    v3 operation: --cli-region / --limit / --marker and the real server-side
    filters --id / --enterprise_project_id. KooCLI only accepts the *array*
    form for the VPC id filter (`--id.1=<vpc-id>`, as declared in the
    operation help listing); the scalar `--id=<vpc-id>` spelling is rejected
    with `[USE_ERROR]Invalid parameter: id`. VPC pages with `limit` + `marker`
    (the next_marker comes from the response page_info).

    ListVpcs is a v3 API where `id` is declared as ``array<string>``, so KooCLI
    only accepts the indexed form ``--id.1=<vpc-id>``; a bare ``--id=<vpc-id>``
    is rejected with ``[USE_ERROR]Invalid parameter: id``.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if vpc_id:
        argv.append("--id.1=%s" % vpc_id)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def build_peering_command(region, limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud VPC ListVpcPeerings argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only ListVpcPeerings
    operation: --cli-region / --limit / --marker. Paging uses the
    `next_marker` returned in the response `page_info`.
    """
    argv = [
        SERVICE,
        PEERING_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    return argv


def _hcloud_executable():
    return os.environ.get("VPC_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("VPC_LIST_HCLOUD_ARGS", "").split()
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


def classify_hcloud_failure(stdout, stderr, returncode, operation=ALLOWED_OPERATION):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：VPC %s "
            "真实参数清单可通过 `hcloud VPC %s --help` 查看。"
            "详情：%s" % (returncode, operation, operation, blob[:300])
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
            "无权限访问虚拟私有云（VPC），请检查 IAM 权限（403：AK/SK 无效或未授予 VPC 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_vpcs(payload):
    """Pull the VPC list out of a ListVpcs response."""
    if isinstance(payload, list):
        return payload
    for key in _VPC_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


_PEERING_LIST_KEYS = ("peerings", "peering")


def extract_peerings(payload):
    """Pull the VPC peering list out of a ListVpcPeerings response."""
    if isinstance(payload, list):
        return payload
    for key in _PEERING_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _next_marker(payload):
    """Read the next_marker from a ListVpcs / ListVpcPeerings page_info."""
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


def _build_sdk_client(region, project_id, rest_path=REST_PATH):
    """Build a `huaweicloudsdkvpc` v2 client from whitelisted env credentials.

    The official SDK has no env-var auto-discovery on `BasicCredentials()`, so
    AK/SK (and the project id required by the `/v1/{project_id}/...` or
    `/v2.0/{project_id}/...` path) must be read explicitly. Region resolution
    uses the SDK's own `VpcRegion` catalog (official endpoints, no guessing),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkvpc.v2 import VpcClient
        from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkvpc 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkvpc。详情：%s" % exc
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
            "SDK 回退缺少 project_id：VPC 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % rest_path
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = VpcRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://vpc.%s.myhuaweicloud.com" % region)
        return VpcClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkvpc 安装与区域配置。"
            % (region, exc)
        )


def list_vpcs_via_sdk(region, vpc_id=None, enterprise_project_id=None,
                      limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """SDK fallback: query VPCs through `huaweicloudsdkvpc` v2.

    Only invoked when hcloud is not installed.
    `ListVpcsRequest` accepts `id` / `enterprise_project_id` as string values;
    paging uses `limit` + `marker`.
    """
    client = _build_sdk_client(region, project_id, REST_PATH)
    from huaweicloudsdkvpc.v2 import ListVpcsRequest
    vpcs = []
    marker = None
    for _ in range(max_pages):
        request = ListVpcsRequest(
            limit=limit,
            marker=marker,
            id=vpc_id,
            enterprise_project_id=enterprise_project_id,
        )
        try:
            response = client.list_vpcs(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问虚拟私有云（VPC），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.vpcs or [])
        records = [_jsonable(vpc.to_dict()) for vpc in batch]
        vpcs.extend(records)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker and records and len(records) >= limit:
            # The typed ListVpcsResponse does not surface page_info; the VPC
            # marker is the resource id, so continue from the last returned id
            # when the page is full.
            next_marker = records[-1].get("id")
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return vpcs


def list_vpcs(region, vpc_id=None, enterprise_project_id=None,
              limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """Query all VPCs (marker-paged); KooCLI first, SDK fallback."""
    vpcs = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, vpc_id=vpc_id,
                             enterprise_project_id=enterprise_project_id,
                             limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            vpcs = list_vpcs_via_sdk(
                region, vpc_id=vpc_id,
                enterprise_project_id=enterprise_project_id,
                limit=limit, project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_vpcs(payload)
        vpcs.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return vpcs


def list_peerings_via_sdk(region, limit=DEFAULT_PAGE_SIZE, project_id=None,
                          max_pages=100):
    """SDK fallback: query VPC peerings through `huaweicloudsdkvpc` v2.

    Only invoked when hcloud is not installed. Uses `ListVpcPeeringsRequest`
    (`limit` + `marker`); a typed response has no `page_info`, so a full page
    continues from the last returned peering id (the marker is a resource id).
    """
    client = _build_sdk_client(region, project_id, PEERING_REST_PATH)
    from huaweicloudsdkvpc.v2 import ListVpcPeeringsRequest
    peerings = []
    marker = None
    for _ in range(max_pages):
        request = ListVpcPeeringsRequest(limit=limit, marker=marker)
        try:
            response = client.list_vpc_peerings(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问虚拟私有云（VPC），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(getattr(response, "peerings", None) or [])
        records = [_jsonable(peering.to_dict()) for peering in batch]
        peerings.extend(records)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker and records and len(records) >= limit:
            next_marker = records[-1].get("id")
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return peerings


def list_peerings(region, limit=DEFAULT_PAGE_SIZE, project_id=None,
                  max_pages=100):
    """Query all VPC peerings (marker-paged); KooCLI first, SDK fallback."""
    peerings = []
    marker = None
    for _page in range(max_pages):
        argv = build_peering_command(region, limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            peerings = list_peerings_via_sdk(
                region, limit=limit, project_id=project_id,
                max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(
                stdout, stderr, returncode, operation=PEERING_OPERATION)
        payload = extract_json(stdout)
        batch = extract_peerings(payload)
        peerings.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return peerings


def normalize_peering(peering):
    """Flatten a peering record to name / local VPC / peer VPC / status.

    `request_vpc_info.vpc_id` is the local (requesting) VPC and
    `accept_vpc_info.vpc_id` is the peer (accepting) VPC; either side may be
    absent in a partial response and is then rendered as `-`.
    """
    request_info = peering.get("request_vpc_info")
    accept_info = peering.get("accept_vpc_info")
    local_vpc = request_info.get("vpc_id") if isinstance(request_info, dict) else None
    peer_vpc = accept_info.get("vpc_id") if isinstance(accept_info, dict) else None
    return {
        "name": _field(peering, "name", "id"),
        "local_vpc": local_vpc if local_vpc else "-",
        "peer_vpc": peer_vpc if peer_vpc else "-",
        "status": _field(peering, "status"),
    }


def render_peering_table(peerings):
    """Render the fixed four-column VPC peering table."""
    rows = [normalize_peering(peering) for peering in peerings]
    widths = [max(len(col), *(len(str(row[col])) for row in rows))
              for col in PEERING_TABLE_COLUMNS]
    lines = [
        "  ".join(col.ljust(widths[i]) for i, col in enumerate(PEERING_TABLE_COLUMNS)),
        "  ".join("-" * w for w in widths),
    ]
    for row in rows:
        lines.append("  ".join(str(row[col]).ljust(widths[i])
                               for i, col in enumerate(PEERING_TABLE_COLUMNS)))
    return "\n".join(lines)


def peering_names(peerings):
    names = []
    for peering in peerings:
        name = _field(peering, "name", default=None)
        if name is None:
            name = _field(peering, "id")
        names.append(str(name))
    return names


def normalize_vpc(vpc):
    """Flatten a VPC record for the table view.

    The nested `routes` array is compacted into a single JSON cell so the table
    stays readable; all other scalar fields are preserved.
    """
    flat = dict(vpc)
    routes = vpc.get("routes")
    if isinstance(routes, list):
        flat["routes"] = json.dumps(routes, ensure_ascii=False,
                                    separators=(",", ":"))
    return flat


def _field(vpc, *names, default="-"):
    for name in names:
        if name in vpc and vpc[name] not in (None, ""):
            return vpc[name]
    return default


def vpc_names(vpcs):
    names = []
    for vpc in vpcs:
        name = _field(vpc, "name", default=None)
        if name is None:
            name = _field(vpc, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(vpcs):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_vpc(vpc) for vpc in vpcs]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["id", "name"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in rows_data]
    if rows:
        widths = [max(len(col), *(len(row[i]) for row in rows))
                  for i, col in enumerate(columns)]
    else:
        widths = [len(col) for col in columns]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def _md_escape(value):
    """Escape pipe/newline characters so a cell cannot break the Markdown table."""
    return _cell(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def normalized_row(vpc, region=None):
    """Map a VPC record to the fixed Markdown column order (8 columns)."""
    return [
        _md_escape(_field(vpc, "name")),
        _md_escape(_field(vpc, "id")),
        _md_escape(region if region else _FIELD_MISSING),
        _md_escape(_field(vpc, "cidr")),
        _md_escape(_field(vpc, "status")),
        _md_escape(_field(vpc, "enterprise_project_id")),
        _md_escape(_field(vpc, "description")),
        _md_escape(_field(vpc, "created_at")),
    ]


def render_markdown(vpcs, summary=False, region=None):
    """Render the VPC list as a GitHub-flavored Markdown table.

    An empty list still renders a valid (header-only) table, so "no VPC" never
    produces a corrupt file — it produces an explicit empty table. The contract
    is identical to huawei-cloud-vpc-export-markdown.
    """
    lines = [
        "| " + " | ".join(MD_HEADERS) + " |",
        "| " + " | ".join(["---"] * len(MD_HEADERS)) + " |",
    ]
    for vpc in vpcs:
        lines.append("| " + " | ".join(normalized_row(vpc, region=region)) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 VPC（Region %s）。"
                     % (len(vpcs), region or _FIELD_MISSING))
    return "\n".join(lines)


def default_output_path(region):
    """Default .md filename: vpc_list_<region>_<timestamp>.md"""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.md" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def export_markdown(vpcs, output_path, summary=False, region=None):
    """Write the VPC list as a Markdown report at ``output_path``.

    The parent directory is created automatically and the file is written via a
    temporary file + atomic rename, so an interrupted write never leaves a
    corrupt/partial ``.md``. Returns the absolute path of the written file.
    """
    vpcs = list(vpcs)
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

    text = render_markdown(vpcs, summary=summary, region=region)

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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 VPC / VPC 对等连接（只读；KooCLI hcloud VPC ListVpcs / ListVpcPeerings）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--resource", choices=("vpc", "peering"), default="vpc",
                        help="查询对象：vpc（默认，ListVpcs）或 peering（ListVpcPeerings）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出名称清单")
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["table", "json", "names", "md"],
                        help="输出格式：table（默认）/ json / names / md（md 仅 --resource vpc）")
    parser.add_argument("-o", "--output", default=None,
                        help="Markdown 输出路径（仅 --format md 且 --resource vpc；默认 "
                             "vpc_list_<region>_<timestamp>.md）")
    parser.add_argument("--summary", action="store_true",
                        help="Markdown 报表末尾追加汇总行（VPC 数量）")
    parser.add_argument("--id", dest="vpc_id",
                        help="按 VPC ID 过滤（服务端查询参数，仅 --resource vpc）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数，0 表示默认企业项目；仅 --resource vpc）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d，范围 0~2000）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v1/{project_id}/vpcs 或 "
                             "/v2.0/{project_id}/vpc/peerings 路径中需要）")
    parser.add_argument("--operation", default=None,
                        help="hcloud VPC 操作名（缺省随 --resource 选择；仅允许只读 ListVpcs / ListVpcPeerings）")
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag (e.g. `--operation DeleteVpc`) is reported as a guard
    # violation instead of an argparse "unrecognized argument" error. The
    # values of --output / --format are pure local path / format data and are
    # excluded (a path like vpc-delete-report.md must not trip the guard).
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except VpcListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        expected_operation = RESOURCE_OPERATIONS[args.resource]
        guard_operation(args.operation or expected_operation, allowed=expected_operation)
        if args.resource == "peering":
            if args.vpc_id or args.enterprise_project_id:
                raise VpcListError(
                    "对等连接查询不支持 --id / --enterprise-project-id 过滤"
                    "（这两个参数仅用于 --resource vpc）。")
            if args.format == "md":
                raise VpcListError(
                    "Markdown 导出仅支持 --resource vpc"
                    "（对等连接请使用 table / json / names 输出）。")
            peerings = list_peerings(
                args.region,
                limit=args.page_size,
                project_id=args.project_id,
            )
        else:
            if args.vpc_id:
                guard_write_intent(args.vpc_id)
            vpcs = list_vpcs(
                args.region,
                vpc_id=args.vpc_id,
                enterprise_project_id=args.enterprise_project_id,
                limit=args.page_size,
                project_id=args.project_id,
            )
    except VpcListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.resource == "peering":
        return _render_peering_output(args, peerings)

    filters = []
    if args.vpc_id:
        filters.append("id=%s" % args.vpc_id)
    if args.enterprise_project_id:
        filters.append("enterprise_project_id=%s" % args.enterprise_project_id)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    # Legacy flags keep their precedence: --names-only -> --json -> --format.
    if args.names_only or args.format == "names":
        print("Region %s 的虚拟私有云（VPC）名称列表（共 %d 个）：" % (args.region, len(vpcs)))
        for name in vpc_names(vpcs):
            print("- %s" % name)
        return 0

    if args.as_json or args.format == "json":
        print(json.dumps(vpcs, ensure_ascii=False, indent=2))
        return 0

    if args.format == "md":
        output_path = args.output or default_output_path(args.region)
        try:
            written = export_markdown(vpcs, output_path,
                                      summary=args.summary, region=args.region)
        except ExportError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        if not vpcs:
            print("当前区域（%s）无虚拟私有云（VPC）%s，已生成空表（仅表头）：%s"
                  % (args.region, filter_suffix, written))
            return 0
        print("已生成 VPC 列表 Markdown 报表（Region %s，共 %d 个 VPC，"
              "含 VPC 名称列）：%s" % (args.region, len(vpcs), written))
        return 0

    if not vpcs:
        print("当前区域（%s）无虚拟私有云（VPC）%s。" % (args.region, filter_suffix))
        return 0

    print("Region %s 的虚拟私有云（VPC）列表（共 %d 个，完整字段）：" % (args.region, len(vpcs)))
    print(render_table(vpcs))
    return 0


def _render_peering_output(args, peerings):
    """Render peering results (table / --json / --names-only / empty)."""
    if args.as_json:
        print(json.dumps(peerings, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 VPC 对等连接名称列表（共 %d 个）：" % (args.region, len(peerings)))
        for name in peering_names(peerings):
            print("- %s" % name)
        return 0

    if not peerings:
        print("当前区域（%s）无对等连接（VPC Peering）。" % args.region)
        return 0

    print("Region %s 的 VPC 对等连接列表（共 %d 个）：" % (args.region, len(peerings)))
    print(render_peering_table(peerings))
    return 0


if __name__ == "__main__":
    sys.exit(main())