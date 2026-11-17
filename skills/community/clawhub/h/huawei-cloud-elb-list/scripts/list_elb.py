#!/usr/bin/env python3
"""List Huawei Cloud Elastic Load Balance (ELB) load balancers via KooCLI.

Primary execution path is KooCLI (`hcloud ELB ListLoadbalancers`, read-only
GET /v3/{project_id}/elb/loadbalancers); when hcloud is not installed the script
falls back to the official `huaweicloudsdkelb` v3 SDK
(`ELBClient.list_load_balancers`). Reads nothing but the active credential
profile / environment.

Output modes:
  * default      standardized table — exactly two columns, `id` + `name`
  * --json       raw response array (every returned field, for downstream tooling)
  * --names-only compact name list

Whenever a list query renders the standardized `id` + `name` list (the default
table or `--names-only`), the script also writes a Markdown document containing
the standardized `id` + 名称 list (Markdown table `| ID | 名称 |`). The document
is written to `elb-list.md` by default; override with `--md-out <path>` or turn
it off with `--no-md`. `--json` never writes the document.

Also supports --id / --name / --vpc-id / --provisioning-status /
--operating-status / --enterprise-project-id / --vip-address filters (all real
server-side query parameters), marker-based paging, and a strict write-intent
guard: any argument that looks like a mutating ELB operation is rejected before
a single command is executed.

Usage:
    python3 scripts/list_elb.py [--region cn-north-4] [--json | --names-only]
                                [--id lb-0001] [--name lb-demo]
                                [--vpc-id vpc-0001] [--provisioning-status ACTIVE]
                                [--operating-status ONLINE]
                                [--enterprise-project-id 0] [--vip-address 192.168.0.10]
                                [--page-size 100] [--project-id <id>]
                                [--operation ListLoadbalancers]
                                [--md-out elb-list.md | --no-md]

Environment overrides (mostly for tests):
    ELB_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    ELB_LIST_HCLOUD_ARGS  extra args injected before the ELB operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
DEFAULT_MD_OUT = "elb-list.md"
SERVICE = "ELB"
ALLOWED_OPERATION = "ListLoadbalancers"
REST_PATH = "/v3/{project_id}/elb/loadbalancers"

# Mutating ELB operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createloadbalancer",
    "batchcreateloadbalancers",
    "deleteloadbalancer",
    "batchdeleteloadbalancers",
    "updateloadbalancer",
    "createlistener",
    "batchcreatelisteners",
    "deletelistener",
    "batchdeletelisteners",
    "updatelistener",
    "createpool",
    "deletepool",
    "updatepool",
    "createmember",
    "deletemember",
    "updatemember",
    "createhealthmonitor",
    "deletehealthmonitor",
    "updatehealthmonitor",
    "createl7policy",
    "deletel7policy",
    "updatel7policy",
    "createcertificate",
    "deletecertificate",
    "updatecertificate",
    "cloneloadbalancer",
    "restoreloadbalancer",
    "changeloadbalancerchargemode",
    "create",
    "delete",
    "update",
    "modify",
    "clone",
    "restore",
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
    "enable",
    "disable",
    "creating",
    "deleting",
    "updating",
)

# The default list output is standardized to exactly these two columns.
STANDARD_COLUMNS = ("id", "name")

_LOADBALANCER_LIST_KEYS = ("loadbalancers", "load_balancers", "loadBalancers")

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


class ElbListError(Exception):
    """Base error for the ELB list skill."""


class GuardError(ElbListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ElbListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(ElbListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ElbListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-elb`, `CreateLoadBalancer`,
    and `create_loadbalancer` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（ELB ListLoadbalancers），创建/删除/更新/绑定/解绑的变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListLoadbalancers operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, lb_id=None, name=None, vpc_id=None,
                  provisioning_status=None, operating_status=None,
                  enterprise_project_id=None, vip_address=None,
                  limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud ELB ListLoadbalancers argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only ELB
    ListLoadbalancers operation: scalar --cli-region / --limit / --marker and the
    real server-side filters --id / --name / --vpc_id / --provisioning_status /
    --operating_status / --enterprise_project_id / --vip_address. The filters are
    **array-typed** ListLoadbalancers query parameters, so KooCLI requires the
    indexed form `--key.1=value` (a bare `--key=value` is rejected with
    `[USE_ERROR]Invalid parameter`). ELB pages with `limit` + `marker` (the
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
    if lb_id:
        argv.append("--id.1=%s" % lb_id)
    if name:
        argv.append("--name.1=%s" % name)
    if vpc_id:
        argv.append("--vpc_id.1=%s" % vpc_id)
    if provisioning_status:
        argv.append("--provisioning_status.1=%s" % provisioning_status)
    if operating_status:
        argv.append("--operating_status.1=%s" % operating_status)
    if enterprise_project_id:
        argv.append("--enterprise_project_id.1=%s" % enterprise_project_id)
    if vip_address:
        argv.append("--vip_address.1=%s" % vip_address)
    return argv


def _hcloud_executable():
    return os.environ.get("ELB_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("ELB_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：ELB ListLoadbalancers "
            "真实参数清单可通过 `hcloud ELB ListLoadbalancers --help` 查看。"
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
            "无权限访问弹性负载均衡（ELB），请检查 IAM 权限（403：AK/SK 无效或未授予 ELB 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_loadbalancers(payload):
    """Pull the ELB list out of a ListLoadbalancers response."""
    if isinstance(payload, list):
        return payload
    for key in _LOADBALANCER_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _next_marker(payload):
    """Read the next_marker from a ListLoadbalancers response page_info."""
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


def list_loadbalancers_via_sdk(region, lb_id=None, name=None, vpc_id=None,
                               provisioning_status=None, operating_status=None,
                               enterprise_project_id=None, vip_address=None,
                               limit=DEFAULT_PAGE_SIZE, project_id=None,
                               max_pages=100):
    """SDK fallback: query ELB load balancers through `huaweicloudsdkelb` v3.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK (and the project id
    required by the `/v3/{project_id}/...` path) must be read explicitly.
    Region resolution uses the SDK's own `ElbRegion` catalog (official
    endpoints, no guessing), falling back to an explicit `Region(id, endpoint)`
    for custom regions.
    `ListLoadBalancersRequest` accepts `id` / `name` / `vpc_id` /
    `provisioning_status` / `operating_status` / `enterprise_project_id` /
    `vip_address` as list values; paging uses `limit` + `marker`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkelb.v3 import ElbClient, ListLoadBalancersRequest
        from huaweicloudsdkelb.v3.region.elb_region import ElbRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkelb 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkelb。详情：%s" % exc
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
            "SDK 回退缺少 project_id：ELB 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = ElbRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://elb.%s.myhuaweicloud.com" % region)
        client = ElbClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkelb 安装与区域配置。"
            % (region, exc)
        )
    loadbalancers = []
    marker = None
    for _ in range(max_pages):
        request = ListLoadBalancersRequest(
            limit=limit,
            marker=marker,
            id=[lb_id] if lb_id else None,
            name=[name] if name else None,
            vpc_id=[vpc_id] if vpc_id else None,
            provisioning_status=[provisioning_status] if provisioning_status else None,
            operating_status=[operating_status] if operating_status else None,
            enterprise_project_id=[enterprise_project_id] if enterprise_project_id else None,
            vip_address=[vip_address] if vip_address else None,
        )
        try:
            response = client.list_load_balancers(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问弹性负载均衡（ELB），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.loadbalancers or [])
        loadbalancers.extend(_jsonable(lb.to_dict()) for lb in batch)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return loadbalancers


def list_loadbalancers(region, lb_id=None, name=None, vpc_id=None,
                       provisioning_status=None, operating_status=None,
                       enterprise_project_id=None, vip_address=None,
                       limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """Query all ELB load balancers (marker-paged); KooCLI first, SDK fallback."""
    loadbalancers = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(
            region, lb_id=lb_id, name=name, vpc_id=vpc_id,
            provisioning_status=provisioning_status,
            operating_status=operating_status,
            enterprise_project_id=enterprise_project_id,
            vip_address=vip_address, limit=limit, marker=marker,
        )
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            loadbalancers = list_loadbalancers_via_sdk(
                region, lb_id=lb_id, name=name, vpc_id=vpc_id,
                provisioning_status=provisioning_status,
                operating_status=operating_status,
                enterprise_project_id=enterprise_project_id,
                vip_address=vip_address, limit=limit, project_id=project_id,
                max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_loadbalancers(payload)
        loadbalancers.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return loadbalancers


def _field(lb, *names, default="-"):
    for name in names:
        if name in lb and lb[name] not in (None, ""):
            return lb[name]
    return default


def loadbalancer_names(loadbalancers):
    names = []
    for lb in loadbalancers:
        name = _field(lb, "name", default=None)
        if name is None:
            name = _field(lb, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def standardize_loadbalancers(loadbalancers):
    """Reduce every load balancer to exactly ``id`` + ``name``.

    ``name`` falls back to the ``id`` when absent; both fall back to ``-`` when
    the field is missing on the response. Everything else is dropped, so the
    default list output is standardized.
    """
    standardized = []
    for lb in loadbalancers:
        lb_id = str(_field(lb, "id"))
        lb_name = _field(lb, "name", default=None)
        if lb_name in (None, ""):
            lb_name = lb_id
        standardized.append({"id": lb_id, "name": str(lb_name)})
    return standardized


def render_table(loadbalancers):
    """Render the standardized ``id`` + ``name`` table (default output)."""
    rows_data = standardize_loadbalancers(loadbalancers)
    columns = list(STANDARD_COLUMNS)
    rows = [[_cell(row[col]) for col in columns] for row in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows))
              for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def _md_cell(value):
    """Escape a value for a Markdown table cell (``|`` and newlines)."""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def render_markdown(loadbalancers, region=None):
    """Render the standardized ``id`` + 名称 list as a Markdown document."""
    lines = ["# 弹性负载均衡（ELB）列表"]
    if region:
        lines.append("")
        lines.append("- Region：%s" % region)
    lines.append("- 共 %d 个负载均衡器。" % len(loadbalancers))
    lines.append("")
    lines.append("| ID | 名称 |")
    lines.append("| --- | --- |")
    for row in standardize_loadbalancers(loadbalancers):
        lines.append("| %s | %s |" % (_md_cell(row["id"]), _md_cell(row["name"])))
    return "\n".join(lines) + "\n"


def write_markdown_file(path, content):
    """Write `content` to `path` (UTF-8); raise ElbListError on I/O failure.

    The parent directory of `path` is created automatically (``--md-out`` may
    point into a not-yet-existing directory such as ``inventory/elb-list.md``).
    """
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
    except OSError as exc:
        raise ElbListError("无法写入 Markdown 文档 %s：%s" % (path, exc))
    return path


def emit_markdown_doc(args, loadbalancers):
    """Write the standardized id+name Markdown document unless ``--no-md``.

    Returns 0 on success/skip and 1 when the document cannot be written.
    """
    if args.no_md:
        return 0
    try:
        path = write_markdown_file(
            args.md_out, render_markdown(loadbalancers, region=args.region))
    except ElbListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1
    print("Markdown 文档已生成：%s（共 %d 个负载均衡器）" % (path, len(loadbalancers)))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云弹性负载均衡（ELB）负载均衡器列表（KooCLI hcloud ELB ListLoadbalancers，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出负载均衡器名称清单")
    parser.add_argument("--id", dest="lb_id",
                        help="按负载均衡器 ID 过滤（服务端查询参数）")
    parser.add_argument("--name", help="按负载均衡器名称过滤（服务端查询参数）")
    parser.add_argument("--vpc-id", dest="vpc_id",
                        help="按所在 VPC ID 过滤（服务端查询参数）")
    parser.add_argument("--provisioning-status", dest="provisioning_status",
                        help="按配置状态过滤（如 ACTIVE / PENDING_DELETE，服务端查询参数）")
    parser.add_argument("--operating-status", dest="operating_status",
                        help="按操作状态过滤（如 ONLINE / FROZEN，服务端查询参数）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数）")
    parser.add_argument("--vip-address", dest="vip_address",
                        help="按 IPv4 私网 VIP 地址过滤（服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d，范围 0~2000）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v3/{project_id}/elb/loadbalancers 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud ELB 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    parser.add_argument("--md-out", dest="md_out", default=DEFAULT_MD_OUT,
                        help="标准化 id+名称 Markdown 文档输出路径（默认 %s）" % DEFAULT_MD_OUT)
    parser.add_argument("--no-md", action="store_true", dest="no_md",
                        help="不生成 Markdown 文档（仅输出到 stdout）")
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        if args.lb_id:
            guard_write_intent(args.lb_id)
        if args.name:
            guard_write_intent(args.name)
        if args.provisioning_status:
            guard_write_intent(args.provisioning_status)
        if args.operating_status:
            guard_write_intent(args.operating_status)
        loadbalancers = list_loadbalancers(
            args.region,
            lb_id=args.lb_id,
            name=args.name,
            vpc_id=args.vpc_id,
            provisioning_status=args.provisioning_status,
            operating_status=args.operating_status,
            enterprise_project_id=args.enterprise_project_id,
            vip_address=args.vip_address,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except ElbListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(loadbalancers, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的弹性负载均衡（ELB）名称列表（共 %d 个）：" % (args.region, len(loadbalancers)))
        for name in loadbalancer_names(loadbalancers):
            print("- %s" % name)
        return emit_markdown_doc(args, loadbalancers)

    if not loadbalancers:
        filters = []
        if args.lb_id:
            filters.append("id=%s" % args.lb_id)
        if args.name:
            filters.append("name=%s" % args.name)
        if args.vpc_id:
            filters.append("vpc_id=%s" % args.vpc_id)
        if args.provisioning_status:
            filters.append("provisioning_status=%s" % args.provisioning_status)
        if args.operating_status:
            filters.append("operating_status=%s" % args.operating_status)
        if args.enterprise_project_id:
            filters.append("enterprise_project_id=%s" % args.enterprise_project_id)
        if args.vip_address:
            filters.append("vip_address=%s" % args.vip_address)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无负载均衡器（ELB）%s。" % (args.region, suffix))
        return emit_markdown_doc(args, loadbalancers)

    print("Region %s 的弹性负载均衡（ELB）列表（共 %d 个，标准化字段 id + name）："
          % (args.region, len(loadbalancers)))
    print(render_table(loadbalancers))
    return emit_markdown_doc(args, loadbalancers)


if __name__ == "__main__":
    sys.exit(main())