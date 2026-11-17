#!/usr/bin/env python3
"""List Huawei Cloud VPC subnets via KooCLI `hcloud VPC ListSubnets`.

Primary execution path is KooCLI (`hcloud VPC ListSubnets`, read-only
GET /v1/{project_id}/subnets); when hcloud is not installed the script falls
back to the official `huaweicloudsdkvpc` v2 SDK (`VpcClient.list_subnets`).
Reads nothing but the active credential profile / environment. Supports three
output modes (table / --json / --names-only), an optional --vpc-id filter (a
real server-side ListSubnets query parameter), marker-based paging, and a
strict write-intent guard: any argument that looks like a mutating VPC/subnet
operation is rejected before a single command is executed.

Usage:
    python3 scripts/list_subnet.py [--region cn-north-4] [--json | --names-only]
                                   [--vpc-id <vpc-id>] [--page-size 100]
                                   [--project-id <id>] [--operation ListSubnets]

Environment overrides (mostly for tests):
    SUBNET_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    SUBNET_LIST_HCLOUD_ARGS  extra args injected before the VPC operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "VPC"
ALLOWED_OPERATION = "ListSubnets"
REST_PATH = "/v1/{project_id}/subnets"

# Mutating VPC / subnet operations or intents — strictly rejected by the guard.
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
# Covers the fields the requirement calls out: 名称/ID/CIDR/网关/VPC ID/状态.
PREFERRED_COLUMNS = [
    "id",
    "name",
    "vpc_id",
    "cidr",
    "gateway_ip",
    "status",
    "description",
    "availability_zone",
    "available_ip_address_count",
    "neutron_network_id",
    "neutron_subnet_id",
    "dhcp_enable",
    "primary_dns",
    "secondary_dns",
    "dns_list",
    "ipv6_enable",
    "cidr_v6",
    "gateway_ip_v6",
    "neutron_subnet_id_v6",
    "scope",
    "tenant_id",
    "extra_dhcp_opts",
    "enable_network_address_usage_metrics",
    "created_at",
    "updated_at",
]

_SUBNET_LIST_KEYS = ("subnets", "subnet")

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


class SubnetListError(Exception):
    """Base error for the VPC subnet list skill."""


class GuardError(SubnetListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(SubnetListError):
    """hcloud missing or credentials (AK/SK) / project id not configured."""


class AuthError(SubnetListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(SubnetListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-subnet`, `CreateSubnet`, and
    `create_subnet` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（VPC ListSubnets），创建/删除/更新/绑定/解绑的变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListSubnets operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, vpc_id=None, limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud VPC ListSubnets argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only VPC ListSubnets
    operation: --cli-region / --limit / --marker and the real server-side
    filter --vpc_id (verified against the `huaweicloudsdkvpc` v2
    `ListSubnetsRequest` model). Subnet pages with `limit` + `marker` (the
    next_marker comes from the response page_info).
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
        argv.append("--vpc_id=%s" % vpc_id)
    return argv


def _hcloud_executable():
    return os.environ.get("SUBNET_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("SUBNET_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：VPC ListSubnets "
            "真实参数清单可通过 `hcloud VPC ListSubnets --help` 查看。"
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
            "无权限访问 VPC 子网（Subnet），请检查 IAM 权限（403：AK/SK 无效或未授予"
            " VPC 只读权限），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_subnets(payload):
    """Pull the subnet list out of a ListSubnets response."""
    if isinstance(payload, list):
        return payload
    for key in _SUBNET_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _next_marker(payload):
    """Read the next_marker from a ListSubnets response page_info."""
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


def list_subnets_via_sdk(region, vpc_id=None, limit=DEFAULT_PAGE_SIZE,
                         project_id=None, max_pages=100):
    """SDK fallback: query subnets through `huaweicloudsdkvpc` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK (and the project id
    required by the `/v1/{project_id}/...` path) must be read explicitly.
    Region resolution uses the SDK's own `VpcRegion` catalog (official
    endpoints, no guessing), falling back to an explicit `Region(id,
    endpoint)` for custom regions.
    `ListSubnetsRequest` accepts `vpc_id` as a string value; paging uses
    `limit` + `marker`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkvpc.v2 import VpcClient, ListSubnetsRequest
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
            "SDK 回退缺少 project_id：VPC 子网的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = VpcRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://vpc.%s.myhuaweicloud.com" % region)
        client = VpcClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkvpc 安装与区域配置。"
            % (region, exc)
        )
    subnets = []
    marker = None
    for _ in range(max_pages):
        request = ListSubnetsRequest(
            limit=limit,
            marker=marker,
            vpc_id=vpc_id,
        )
        try:
            response = client.list_subnets(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 VPC 子网（Subnet），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.subnets or [])
        records = [_jsonable(subnet.to_dict()) for subnet in batch]
        subnets.extend(records)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker and records and len(records) >= limit:
            # The typed ListSubnetsResponse does not surface page_info; the
            # subnet marker is the resource id, so continue from the last
            # returned id when the page is full.
            next_marker = records[-1].get("id")
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return subnets


def list_subnets(region, vpc_id=None, limit=DEFAULT_PAGE_SIZE,
                 project_id=None, max_pages=100):
    """Query all subnets (marker-paged); KooCLI first, SDK fallback."""
    subnets = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, vpc_id=vpc_id, limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            subnets = list_subnets_via_sdk(
                region, vpc_id=vpc_id,
                limit=limit, project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_subnets(payload)
        subnets.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return subnets


def normalize_subnet(subnet):
    """Flatten a subnet record for the table view.

    Nested list/object cells (`extra_dhcp_opts`, `dns_list`) are compacted into
    single JSON cells so the table stays readable; scalar fields are preserved.
    """
    flat = dict(subnet)
    for key in ("extra_dhcp_opts", "dns_list"):
        value = flat.get(key)
        if isinstance(value, (list, dict)):
            flat[key] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return flat


def _field(subnet, *names, default="-"):
    for name in names:
        if name in subnet and subnet[name] not in (None, ""):
            return subnet[name]
    return default


def subnet_names(subnets):
    names = []
    for subnet in subnets:
        name = _field(subnet, "name", default=None)
        if name is None:
            name = _field(subnet, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(subnets):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_subnet(subnet) for subnet in subnets]
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
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 VPC 子网（Subnet）列表（KooCLI hcloud VPC ListSubnets，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出子网名称清单")
    parser.add_argument("--vpc-id", dest="vpc_id",
                        help="按 VPC ID 过滤（服务端查询参数；企业项目细粒度授权场景下必传）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v1/{project_id}/subnets 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud VPC 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        if args.vpc_id:
            guard_write_intent(args.vpc_id)
        subnets = list_subnets(
            args.region,
            vpc_id=args.vpc_id,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except SubnetListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(subnets, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 VPC 子网（Subnet）名称列表（共 %d 个）：" % (args.region, len(subnets)))
        for name in subnet_names(subnets):
            print("- %s" % name)
        return 0

    if not subnets:
        filters = []
        if args.vpc_id:
            filters.append("vpc_id=%s" % args.vpc_id)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无 VPC 子网（Subnet）%s。" % (args.region, suffix))
        return 0

    print("Region %s 的 VPC 子网（Subnet）列表（共 %d 个，完整字段）：" % (args.region, len(subnets)))
    print(render_table(subnets))
    return 0


if __name__ == "__main__":
    sys.exit(main())