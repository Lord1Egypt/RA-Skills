#!/usr/bin/env python3
"""List Huawei Cloud Cloud Connect (CC) instances via KooCLI `hcloud CC ListCloudConnections`.

Primary execution path is KooCLI (`hcloud CC ListCloudConnections`, read-only
GET /v3/{domain_id}/ccaas/cloud-connections); when hcloud is not installed the
script falls back to the official `huaweicloudsdkcc` v3 SDK
(`CcClient.list_cloud_connections`). Reads nothing but the active credential
profile / environment. Supports three output modes (table / --json /
--names-only), --name / --status / --id filters (all real server-side query
parameters), marker-based paging, and a strict write-intent guard: any argument
that looks like a mutating CC operation is rejected before a single command is
executed.

Usage:
    python3 scripts/list_cc.py [--region cn-north-4] [--json | --names-only]
                                [--name cc-01] [--status ACTIVE] [--id cc-0001]
                                [--page-size 100] [--operation ListCloudConnections]

Environment overrides (mostly for tests):
    CC_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    CC_LIST_HCLOUD_ARGS  extra args injected before the CC operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "CC"
ALLOWED_OPERATION = "ListCloudConnections"

# Mutating CC operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createcloudconnection",
    "deletecloudconnection",
    "updatecloudconnection",
    "createbandwidthpackage",
    "deletebandwidthpackage",
    "updatebandwidthpackage",
    "associatebandwidthpackage",
    "disassociatebandwidthpackage",
    "createnetworkinstance",
    "deletenetworkinstance",
    "updatenetworkinstance",
    "createinterregionbandwidth",
    "deleteinterregionbandwidth",
    "updateinterregionbandwidth",
    "createcentralnetwork",
    "deletecentralnetwork",
    "updatecentralnetwork",
    "applycentralnetworkpolicy",
    "deletecentralnetworkpolicy",
    "tagcloudconnection",
    "untagcloudconnection",
    "creating",
    "deleting",
    "updating",
    "associating",
    "disassociating",
    "create",
    "delete",
    "update",
    "modify",
    "associate",
    "disassociate",
    "dissociate",
    "attach",
    "detach",
    "restart",
    "stop",
    "start",
    "destroy",
    "remove",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "status",
    "used_scene",
    "network_instance_number",
    "bandwidth_package_number",
    "inter_region_bandwidth_number",
    "admin_state_up",
    "enterprise_project_id",
    "domain_id",
    "description",
    "created_at",
    "updated_at",
    "tags",
]

_CONNECTION_LIST_KEYS = ("cloud_connections", "cloudConnections", "cloud_connection")

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


class CcListError(Exception):
    """Base error for the CC list skill."""


class GuardError(CcListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CcListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CcListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CcListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-connection`, `CreateCloudConnection`,
    and `create_connection` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（CC ListCloudConnections），创建/删除/更新/绑定的变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListCloudConnections operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, name=None, status=None, connection_id=None,
                  limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud CC ListCloudConnections argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only CC
    ListCloudConnections operation: --cli-region / --limit / --marker and the
    real server-side filters --name / --status / --id. CC pages with
    `limit` + `marker` (the next_marker comes from the response page_info).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if name:
        argv.append("--name=%s" % name)
    if status:
        argv.append("--status=%s" % status)
    if connection_id:
        argv.append("--id=%s" % connection_id)
    return argv


def _hcloud_executable():
    return os.environ.get("CC_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CC_LIST_HCLOUD_ARGS", "").split()
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


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：CC ListCloudConnections "
            "真实参数清单可通过 `hcloud CC ListCloudConnections --help` 查看。"
            "详情：%s" % (returncode, blob[:300])
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
            "无权限访问云连接（CC），请检查 IAM 权限（403：AK/SK 无效或未授予 CC 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_connections(payload):
    """Pull the cloud-connection list out of a ListCloudConnections response."""
    if isinstance(payload, list):
        return payload
    for key in _CONNECTION_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _next_marker(payload):
    """Read the next_marker from a ListCloudConnections response page_info."""
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


def list_connections_via_sdk(region, name=None, status=None,
                             connection_id=None, limit=DEFAULT_PAGE_SIZE,
                             max_pages=100):
    """SDK fallback: query cloud connections through `huaweicloudsdkcc` v3.

    Only invoked when hcloud is not installed. Credentials are taken from the
    standard environment variables (HUAWEI_*/HW_*/HWC_* AK/SK markers) — never
    passed as literals here. The official SDK has no env-var auto-discovery on
    `BasicCredentials()`, so AK/SK must be read explicitly. Region resolution
    uses the SDK's own `CcRegion` catalog (official endpoints, no guessing),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    `ListCloudConnectionsRequest` accepts `name` / `status` / `id` as list
    values; paging uses `limit` + `marker`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcc.v3 import CcClient, ListCloudConnectionsRequest
        from huaweicloudsdkcc.v3.region.cc_region import CcRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkcc 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkcc。详情：%s" % exc
        )

    def _env_credential(markers):
        for key, value in os.environ.items():
            upper = key.upper()
            if not upper.startswith(("HUAWEI", "HW_", "HWC")):
                continue
            if any(marker in upper for marker in markers) and value:
                return value
        return None

    ak = _env_credential(("ACCESS_KEY", "_AK"))
    sk = _env_credential(("SECRET_KEY", "_SK"))
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HUAWEI_*/HW_*/HWC_* 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = CcRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://cc.myhuaweicloud.com")
        client = CcClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkcc 安装与区域配置。"
            % (region, exc)
        )
    connections = []
    marker = None
    for _ in range(max_pages):
        request = ListCloudConnectionsRequest(
            limit=limit,
            marker=marker,
            id=[connection_id] if connection_id else None,
            name=[name] if name else None,
            status=[status] if status else None,
        )
        try:
            response = client.list_cloud_connections(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问云连接（CC），请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.cloud_connections or [])
        connections.extend(_jsonable(connection.to_dict()) for connection in batch)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return connections


def list_connections(region, status=None, name=None, connection_id=None,
                     limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all CC cloud connections (marker-paged); KooCLI first, SDK fallback."""
    connections = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, name=name, status=status,
                             connection_id=connection_id,
                             limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            connections = list_connections_via_sdk(
                region, name=name, status=status,
                connection_id=connection_id, limit=limit, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_connections(payload)
        connections.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return connections


def normalize_connection(connection):
    """Flatten tag lists into a table-friendly string; keep other fields as-is."""
    flat = dict(connection)
    tags = connection.get("tags")
    if isinstance(tags, list):
        pairs = []
        for tag in tags:
            if isinstance(tag, dict):
                key = tag.get("key", "")
                value = tag.get("value", "")
                pairs.append("%s=%s" % (key, value))
            else:
                pairs.append(str(tag))
        flat["tags"] = ",".join(pairs) if pairs else "-"
    elif tags is None:
        flat["tags"] = "-"
    return flat


def _field(connection, *names, default="-"):
    for name in names:
        if name in connection and connection[name] not in (None, ""):
            return connection[name]
    return default


def connection_names(connections):
    names = []
    for connection in connections:
        name = _field(connection, "name", "connection_name", default=None)
        if name is None:
            name = _field(connection, "id", "connection_id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(connections):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_connection(connection) for connection in connections]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云云连接（CC）实例列表（KooCLI hcloud CC ListCloudConnections，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出云连接实例名称清单")
    parser.add_argument("--name", help="按实例名称过滤（服务端查询参数）")
    parser.add_argument("--status", help="按实例状态过滤（如 ACTIVE，服务端查询参数）")
    parser.add_argument("--id", dest="connection_id",
                        help="按实例 ID 过滤（精确查询，服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d，范围 1~2000）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud CC 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        if args.name:
            guard_write_intent(args.name)
        if args.status:
            guard_write_intent(args.status)
        connections = list_connections(
            args.region,
            status=args.status,
            name=args.name,
            connection_id=args.connection_id,
            limit=args.page_size,
        )
    except CcListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(connections, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的云连接（CC）实例名称列表（共 %d 个）：" % (args.region, len(connections)))
        for name in connection_names(connections):
            print("- %s" % name)
        return 0

    if not connections:
        filters = []
        if args.status:
            filters.append("status=%s" % args.status)
        if args.name:
            filters.append("name=%s" % args.name)
        if args.connection_id:
            filters.append("id=%s" % args.connection_id)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无云连接（CC）实例%s。" % (args.region, suffix))
        return 0

    print("Region %s 的云连接（CC）实例列表（共 %d 个，完整字段）：" % (args.region, len(connections)))
    print(render_table(connections))
    return 0


if __name__ == "__main__":
    sys.exit(main())
