#!/usr/bin/env python3
"""List Huawei Cloud DWS (Data Warehouse Service) clusters via KooCLI
`hcloud DWS ListClusters` (read-only GET `/v1.0/{project_id}/clusters`).

Primary execution path is KooCLI; when hcloud is not installed, the script falls
back to the official `huaweicloudsdkdws` v2 SDK (`list_clusters`). Reads nothing
but the active credential profile / environment. Supports three output modes
(table / --json / --names-only), client-side --name / --status / --cluster-id
filtering and --limit / --offset pagination (the real ListClusters API exposes
only `enterprise_project_id`; name/id/status/limit/offset are applied locally),
plus a strict write-intent guard: any argument that looks like a mutating DWS
operation is rejected before a single command is executed.

Usage:
    python3 scripts/list_dws.py [--region cn-north-4] [--json | --names-only]
                                 [--name dws-01] [--cluster-id <id>]
                                 [--status AVAILABLE] [--limit 100] [--offset 0]
                                 [--enterprise-project-id <eps-id>]
                                 [--operation ListClusters]

Environment overrides (mostly for tests):
    DWS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    DWS_LIST_HCLOUD_ARGS  extra args injected before the DWS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
SERVICE = "DWS"
ALLOWED_OPERATION = "ListClusters"
# Client-side pagination default: 0 means "no limit" (return the whole list).
DEFAULT_LIMIT = 0

# Mutating DWS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createcluster",
    "deletecluster",
    "updatecluster",
    "modifycluster",
    "restartcluster",
    "startcluster",
    "stopcluster",
    "resizecluster",
    "restorecluster",
    "rebootcluster",
    "upgradecluster",
    "resetpassword",
    "resetclusterpassword",
    "creating",
    "deleting",
    "updating",
    "restarting",
    "resizing",
    "restoring",
    "upgrading",
    "rebooting",
    "create",
    "delete",
    "update",
    "modify",
    "restart",
    "stop",
    "start",
    "resize",
    "restore",
    "reboot",
    "upgrade",
    "scale",
    "terminate",
    "destroy",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "status",
    "version",
    "node_type",
    "number_of_node",
    "availability_zone",
    "port",
    "user_name",
    "endpoint",
    "public_endpoint",
    "publicIp",
    "vpc_id",
    "subnet_id",
    "security_group_id",
    "created",
    "updated",
    "enterprise_project_id",
    "recent_event",
    "sub_status",
    "task_status",
    "failed_reasons",
    "tags",
    "nodes",
]

_CLUSTER_LIST_KEYS = ("clusters", "cluster_list", "clusterInfos")

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


class DwsListError(Exception):
    """Base error for the DWS list skill."""


class GuardError(DwsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(DwsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(DwsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(DwsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Return False for read-only text; raise GuardError if `text` is mutating.

    Normalizes separators so `--create-cluster`, `CreateCluster`, and
    `create_cluster` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（DWS ListClusters），创建/删除/扩缩容/重启等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListClusters operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, enterprise_project_id=None):
    """Build the hcloud DWS ListClusters argv (without the executable).

    Mirrors the real KooCLI parameter list (`hcloud DWS ListClusters --help`):
    --cli-region / --enterprise_project_id. The ListClusters API
    (GET /v1.0/{project_id}/clusters) has NO name / id / status / limit / offset
    query parameters — those filters are applied client-side by the script.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
    ]
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("DWS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("DWS_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：DWS ListClusters "
            "真实参数清单可通过 `hcloud DWS ListClusters --help` 查看。"
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
            "无权限访问 DWS，请检查 IAM 权限（403：AK/SK 无效或未授予 DWS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_clusters(payload):
    """Pull the cluster list out of a ListClusters response."""
    if isinstance(payload, list):
        return payload
    for key in _CLUSTER_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def filter_clusters(clusters, name=None, status=None, cluster_id=None):
    """Client-side name / status / id filter (the ListClusters API has none).

    - `name`  — case-insensitive substring match on `name`
    - `status` — case-insensitive exact match on `status`
    - `cluster_id` — exact match on `id`
    An empty result is reported as a normal empty list.
    """
    result = list(clusters)
    if name:
        wanted = str(name).strip().lower()
        result = [
            c for c in result
            if wanted in str(c.get("name", "")).lower()
        ]
    if status:
        wanted = str(status).strip().lower()
        result = [
            c for c in result
            if c.get("status") is not None and str(c.get("status")).strip().lower() == wanted
        ]
    if cluster_id:
        wanted = str(cluster_id).strip()
        result = [c for c in result if str(c.get("id", "")).strip() == wanted]
    return result


def paginate(clusters, limit=DEFAULT_LIMIT, offset=0):
    """Client-side pagination over the already-filtered list.

    `limit` <= 0 means "no limit"; `offset` skips the first N entries. The real
    ListClusters API returns the full list in a single call (no server-side
    paging), so slicing happens locally.
    """
    result = list(clusters)
    if offset and offset > 0:
        result = result[offset:]
    if limit and limit > 0:
        result = result[:limit]
    return result


def list_clusters(region, enterprise_project_id=None):
    """Query all DWS clusters; KooCLI first, one-shot SDK fallback.

    The ListClusters API returns the complete cluster list in one call
    (`supports_limit: false`), so no server-side paging loop is needed.
    """
    argv = build_command(region, enterprise_project_id=enterprise_project_id)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        # hcloud binary missing → one-shot SDK fallback (no CLI retry).
        return list_clusters_via_sdk(
            region, enterprise_project_id=enterprise_project_id)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
        raise classify_hcloud_failure(stdout, stderr, returncode)
    payload = extract_json(stdout)
    return extract_clusters(payload)


def list_clusters_via_sdk(region, enterprise_project_id=None):
    """SDK fallback: query clusters through `huaweicloudsdkdws` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    standard environment variables (HUAWEI_*/HW_*/HWC_* AK/SK markers) — never
    passed as literals here. Region resolution uses the SDK's own `DwsRegion`
    catalog (official endpoints, no guessing), falling back to an explicit
    `Region(id, endpoint)` for custom regions. `ListClustersRequest` exposes only
    `enterprise_project_id`; name/id/status/paging are applied by the caller.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkdws.v2 import DwsClient, ListClustersRequest
        from huaweicloudsdkdws.v2.region.dws_region import DwsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkdws 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkdws。详情：%s" % exc
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
            region_obj = DwsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://dws.%s.myhuaweicloud.com" % region)
        client = DwsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkdws 安装与区域配置。"
            % (region, exc)
        )
    request = ListClustersRequest(enterprise_project_id=enterprise_project_id)
    try:
        response = client.list_clusters(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问 DWS，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
    return [cluster.to_dict() for cluster in (response.clusters or [])]


def normalize_cluster(cluster):
    """Flatten nested endpoints / public_ip fields into table-friendly keys."""
    flat = dict(cluster)
    endpoints = cluster.get("endpoints")
    if isinstance(endpoints, list) and endpoints and isinstance(endpoints[0], dict):
        first = endpoints[0]
        flat.setdefault(
            "endpoint",
            first.get("connect_info") or first.get("jdbc_url") or "-",
        )
    public_endpoints = cluster.get("public_endpoints")
    if isinstance(public_endpoints, list) and public_endpoints \
            and isinstance(public_endpoints[0], dict):
        first = public_endpoints[0]
        flat.setdefault(
            "public_endpoint",
            first.get("public_connect_info") or first.get("jdbc_url") or "-",
        )
    public_ip = cluster.get("public_ip")
    if isinstance(public_ip, dict):
        flat.setdefault("publicIp", public_ip.get("eip_address") or "-")
    elif isinstance(public_ip, str):
        flat.setdefault("publicIp", public_ip)
    return flat


def _field(cluster, *names, default="-"):
    for name in names:
        if name in cluster and cluster[name] not in (None, ""):
            return cluster[name]
    return default


def cluster_names(clusters):
    names = []
    for cluster in clusters:
        name = _field(cluster, "name", "cluster_name", default=None)
        if name is None:
            name = _field(cluster, "id", "cluster_id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(clusters):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_cluster(cluster) for cluster in clusters]
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
        description="查询华为云 DWS 集群列表（KooCLI hcloud DWS ListClusters，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出集群名称清单")
    parser.add_argument("--name",
                        help="按集群名称过滤（不区分大小写子串匹配，本地过滤）")
    parser.add_argument("--status",
                        help="按集群状态过滤（如 AVAILABLE/CREATING/FAILED，"
                             "不区分大小写精确匹配，本地过滤）")
    parser.add_argument("--cluster-id", dest="cluster_id",
                        help="按集群 ID 过滤（精确匹配，本地过滤）")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="本地分页：最多返回的集群数（0=不限制，默认 %d）" % DEFAULT_LIMIT)
    parser.add_argument("--offset", type=int, default=0,
                        help="本地分页：跳过前 N 个集群（默认 0）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（真实 ListClusters API 参数）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud DWS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        for value in (args.name, args.status, args.cluster_id):
            if value:
                guard_write_intent(value)
        clusters = list_clusters(
            args.region,
            enterprise_project_id=args.enterprise_project_id,
        )
    except DwsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    clusters = filter_clusters(
        clusters,
        name=args.name,
        status=args.status,
        cluster_id=args.cluster_id,
    )
    clusters = paginate(clusters, limit=args.limit, offset=args.offset)

    if args.as_json:
        print(json.dumps(clusters, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 DWS 集群名称列表（共 %d 个）：" % (args.region, len(clusters)))
        for name in cluster_names(clusters):
            print("- %s" % name)
        return 0

    if not clusters:
        filters = []
        if args.name:
            filters.append("name=%s" % args.name)
        if args.status:
            filters.append("status=%s" % args.status)
        if args.cluster_id:
            filters.append("cluster_id=%s" % args.cluster_id)
        if args.enterprise_project_id:
            filters.append("enterprise_project_id=%s" % args.enterprise_project_id)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无 DWS 集群%s。" % (args.region, suffix))
        return 0

    print("Region %s 的 DWS 集群列表（共 %d 个，完整字段）：" % (args.region, len(clusters)))
    print(render_table(clusters))
    return 0


if __name__ == "__main__":
    sys.exit(main())