#!/usr/bin/env python3
"""List Huawei Cloud (public) NAT gateways via KooCLI `hcloud NAT ListNatGateways`.

Primary execution path is KooCLI (`hcloud NAT ListNatGateways`, read-only
GET /v2/{project_id}/nat_gateways); when hcloud is not installed the script
falls back to the official `huaweicloudsdknat` v2 SDK
(`NatClient.list_nat_gateways`). Reads nothing but the active credential
profile / environment. Supports three output modes (table / --json /
--names-only), --name / --spec / --status / --vpc (router_id) filters (all
real server-side query parameters), id-marker paging (NAT v2 pages by
starting resource id), and a strict write-intent guard: any mutating NAT
operation is rejected before a single command is executed.

Usage:
    python3 scripts/list_nat_gateways.py [--region cn-north-4]
                                         [--json | --names-only]
                                         [--name my-nat] [--spec 1]
                                         [--status ACTIVE] [--vpc router-id]
                                         [--page-size 2000]
                                         [--project-id <id>]
                                         [--operation ListNatGateways]

Environment overrides (mostly for tests):
    NAT_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    NAT_LIST_HCLOUD_ARGS  extra args injected before the NAT operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
# NAT v2 ListNatGateways official default/upper page size.
DEFAULT_PAGE_SIZE = 2000
SERVICE = "NAT"
ALLOWED_OPERATION = "ListNatGateways"
REST_PATH = "/v2/{project_id}/nat_gateways"

# Options whose values are user-supplied filters/parameters. They are not
# scanned by the write-intent guard: a gateway literally named `prod-start`
# must not be mistaken for a mutating operation.
_VALUE_OPTIONS = (
    "--region",
    "-r",
    "--name",
    "--spec",
    "--status",
    "--vpc",
    "--router_id",
    "--page-size",
    "--project-id",
)

# Mutating NAT operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createnatgateway",
    "deletenatgateway",
    "updatenatgateway",
    "createsnatrule",
    "deletesnatrule",
    "updatesnatrule",
    "createsnatrules",
    "deletesnatrules",
    "creatednatrule",
    "deletednatrule",
    "updatednatrule",
    "batchcreatednatrules",
    "batchcreatesnatrules",
    "batchdeletednatrules",
    "createtransitip",
    "deletetransitip",
    "createtag",
    "deletetag",
    "batchcreatedeletetags",
    "createnatgatewaytoprepaid",
    "updatenatgatewaytoprepaid",
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
    "stop",
    "start",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "id",
    "name",
    "spec",
    "status",
    "router_id",
    "internal_network_id",
    "ngport_ip_address",
    "admin_state_up",
    "description",
    "created_at",
    "enterprise_project_id",
    "billing_info",
    "dnat_rules_limit",
    "snat_rule_public_ip_limit",
    "pps_max",
    "bps_max",
    "tenant_id",
]

_GATEWAY_LIST_KEYS = ("nat_gateways", "natGateways")

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


class NatListError(Exception):
    """Base error for the NAT gateway list skill."""


class GuardError(NatListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(NatListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(NatListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(NatListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-nat`, `CreateNatGateway`, and
    `create_nat_gateway` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（NAT ListNatGateways），公网NAT网关/SNAT/DNAT规则的创建、删除、"
                "更新等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_scan_text(argv):
    """Build the guard scan text, keeping operation/command tokens only.

    Values of user-facing filter options (``--name`` / ``--status`` / ...) are
    dropped so a legitimate read-only query is never blocked just because a
    gateway name or status contains a mutating verb.
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
    """Only the read-only ListNatGateways operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, name=None, spec=None, status=None, router_id=None,
                  limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud NAT ListNatGateways argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only NAT
    ListNatGateways operation: --cli-region / --limit / --marker and the real
    server-side filters --name / --spec / --status / --router_id. NAT v2
    pages with `limit` + `marker`, where marker is the starting resource id
    (last gateway id of the previous page).
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
    # KooCLI declares `spec` / `status` as array<string>, so their values must
    # use the indexed form (`--spec.1=` / `--status.1=`) instead of `--spec=`.
    if spec:
        argv.append("--spec.1=%s" % spec)
    if status:
        argv.append("--status.1=%s" % status)
    if router_id:
        argv.append("--router_id=%s" % router_id)
    return argv


def _hcloud_executable():
    return os.environ.get("NAT_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    # NAT_LIST_HCLOUD_ARGS is a test-only hook (inject fake CLI flags such as
    # `--cli-profile`); it must never be used in production to smuggle extra
    # CLI tokens, so it is documented here rather than exposed in the CLI help.
    extra = os.environ.get("NAT_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：NAT ListNatGateways "
            "真实参数清单可通过 `hcloud NAT ListNatGateways --help` 查看。"
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
        if re.search(r"\b401\b", low) and not re.search(r"\b403\b", low):
            return AuthError(
                "凭证无效（401：AK/SK 无效或已过期），请重新配置 hcloud 凭证后重试，"
                "参见 references/cli-installation-guide.md。详情：%s" % blob[:300]
            )
        return AuthError(
            "无权限访问公网NAT网关，请检查 IAM 权限（403：AK/SK 无效或未授予 NAT "
            "nat:natGateways:list 只读权限），参见 references/iam-policies.md。"
            "详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_gateways(payload):
    """Pull the NAT gateway list out of a ListNatGateways response."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in _GATEWAY_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _payload_error(payload):
    """Return the error text if a ListNatGateways payload is an error envelope.

    KooCLI returns HTTP-level API errors (e.g. ``{"error_code": "SYS.0403",
    "error_msg": "... not authorized ..."}``) on **stdout with exit code 0**.
    Such an envelope has no ``nat_gateways`` key, so it must be surfaced as an
    explicit error instead of being read as an empty gateway list.
    """
    if not isinstance(payload, dict):
        return None
    # A real list response always carries one of the gateway list keys; never
    # let an incidental error-like field shadow a successful page.
    if any(isinstance(payload.get(key), list) for key in _GATEWAY_LIST_KEYS):
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


def _last_gateway_id(batch):
    """Return the id of the last gateway in a page (the next-page marker).

    NAT v2 `marker` is the starting resource id: the next request passes the
    id of the last gateway of the current page. The response carries only
    `nat_gateways`, so there is no `next_marker`/`page_info` to follow.
    """
    if not batch:
        return None
    last = batch[-1]
    if isinstance(last, dict):
        value = last.get("id")
    else:
        value = getattr(last, "id", None)
    return str(value) if value else None


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


def _sdk_auth_error(exc):
    """Build an AuthError distinguishing 401 (bad credentials) from 403.

    The official SDK raises ``ClientRequestException`` with a ``status_code``;
    an invalid/expired AK/SK surfaces as 401 and must not be reported as an
    IAM 403 permission problem.
    """
    low = str(exc).lower()
    status = getattr(exc, "status_code", None)
    detail = str(exc)[:300]
    if status == 401 or "401" in low or "unauthorized" in low or "apigw.0301" in low:
        return AuthError(
            "凭证无效（401：AK/SK 无效或已过期），请重新配置 AK/SK 后重试，参见"
            " references/cli-installation-guide.md。详情：%s" % detail
        )
    return AuthError(
        "无权限访问公网NAT网关，请检查 IAM 权限（403：未授予 NAT "
        "nat:natGateways:list 只读权限），参见 references/iam-policies.md。"
        "详情：%s" % detail
    )


def list_nat_gateways_via_sdk(region, name=None, spec=None, status=None,
                              router_id=None, limit=DEFAULT_PAGE_SIZE,
                              project_id=None, max_pages=100):
    """SDK fallback: query NAT gateways through `huaweicloudsdknat` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK (and the project id
    required by the `/v2/{project_id}/nat_gateways` path) must be read
    explicitly. Region resolution uses the SDK's own `NatRegion` catalog
    (official endpoints, no guessing), falling back to an explicit
    `Region(id, endpoint)` for custom regions. `ListNatGatewaysRequest`
    takes `name` / `router_id` as plain strings while `spec` / `status` are
    csv list values; paging uses `limit` + an id marker (last gateway id of
    the previous page).
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdknat.v2 import ListNatGatewaysRequest, NatClient
        from huaweicloudsdknat.v2.region.nat_region import NatRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdknat 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdknat。详情：%s" % exc
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
            "SDK 回退缺少 project_id：NAT 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = NatRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://nat.%s.myhuaweicloud.com" % region)
        client = NatClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdknat 安装与区域配置。"
            % (region, exc)
        )
    gateways = []
    marker = None
    for _ in range(max_pages):
        request = ListNatGatewaysRequest(
            limit=limit,
            marker=marker,
            name=name or None,
            spec=[spec] if spec else None,
            status=[status] if status else None,
            router_id=router_id or None,
        )
        try:
            response = client.list_nat_gateways(request)
        except Exception as exc:
            low = str(exc).lower()
            status = getattr(exc, "status_code", None)
            if any(p in low for p in _AUTH_PATTERNS) or status in (401, 403):
                raise _sdk_auth_error(exc)
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.nat_gateways or [])
        gateways.extend(_jsonable(gateway.to_dict()) for gateway in batch)
        if len(batch) < limit:
            break
        next_marker = _last_gateway_id(batch)
        if not next_marker or next_marker == marker:
            break
        marker = next_marker
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return gateways


def list_nat_gateways(region, name=None, spec=None, status=None,
                      router_id=None, limit=DEFAULT_PAGE_SIZE,
                      project_id=None, max_pages=100):
    """Query all public NAT gateways (marker-paged); KooCLI first, SDK fallback."""
    gateways = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, name=name, spec=spec, status=status,
                             router_id=router_id, limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            gateways = list_nat_gateways_via_sdk(
                region, name=name, spec=spec, status=status,
                router_id=router_id, limit=limit, project_id=project_id,
                max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        # KooCLI prints HTTP-level API errors (e.g. SYS.0403 not authorized) as
        # a JSON error envelope on stdout with exit code 0. Handle it before
        # extract_gateways(), otherwise the error is silently read as an empty
        # gateway list (exit 0 + 「无公网NAT网关」), contradicting the 403 branch.
        envelope_error = _payload_error(payload)
        if envelope_error:
            raise classify_hcloud_failure(envelope_error, stderr, returncode)
        batch = extract_gateways(payload)
        gateways.extend(batch)
        if len(batch) < limit:
            break
        next_marker = _last_gateway_id(batch)
        if not next_marker or next_marker == marker:
            break
        marker = next_marker
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return gateways


def normalize_gateway(gateway):
    """Expand nested objects (currently none on NAT gateways) into flat columns."""
    return dict(gateway)


def _field(gateway, *names, default="-"):
    for name in names:
        if name in gateway and gateway[name] not in (None, ""):
            return gateway[name]
    return default


def gateway_names(gateways):
    names = []
    for gateway in gateways:
        name = _field(gateway, "name", default=None)
        if name is None:
            name = _field(gateway, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(gateways):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_gateway(gateway) for gateway in gateways]
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


def _page_size(value):
    """Validate --page-size against the KooCLI limit range (1-2000)."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("--page-size 必须是整数：%r" % value)
    if not 1 <= number <= 2000:
        raise argparse.ArgumentTypeError(
            "--page-size 超出范围（1-2000）：%d。KooCLI 的 limit 参数下限为 1、"
            "上限为 2000。" % number)
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云公网NAT网关列表（KooCLI hcloud NAT ListNatGateways，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出 NAT 网关名称清单")
    parser.add_argument("--name", help="按 NAT 网关名称过滤（服务端查询参数，精确匹配）")
    parser.add_argument("--spec", help="按规格过滤：1 小型 / 2 中型 / 3 大型 / 4 超大型 / 5 企业型（服务端查询参数）")
    parser.add_argument("--status", help="按 NAT 网关状态过滤（如 ACTIVE，服务端查询参数）")
    parser.add_argument("--vpc", dest="router_id",
                        help="按关联 VPC 的 router_id 过滤（服务端查询参数）")
    parser.add_argument("--page-size", type=_page_size, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（1-2000，默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v2/{project_id}/nat_gateways 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud NAT 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan operation/command tokens only (filter
        # values such as --name / --status are legitimate read-only input).
        raw_argv = argv if argv is not None else sys.argv[1:]
        guard_write_intent(guard_scan_text(raw_argv))
        guard_operation(args.operation)
        gateways = list_nat_gateways(
            args.region,
            name=args.name,
            spec=args.spec,
            status=args.status,
            router_id=args.router_id,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except NatListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(gateways, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的公网NAT网关名称列表（共 %d 个）：" % (args.region, len(gateways)))
        for name in gateway_names(gateways):
            print("- %s" % name)
        return 0

    if not gateways:
        filters = []
        if args.name:
            filters.append("name=%s" % args.name)
        if args.spec:
            filters.append("spec=%s" % args.spec)
        if args.status:
            filters.append("status=%s" % args.status)
        if args.router_id:
            filters.append("vpc(router_id)=%s" % args.router_id)
        if filters:
            print("当前区域（%s）无公网NAT网关（过滤条件: %s）。"
                  % (args.region, ", ".join(filters)))
        else:
            print("当前区域（%s）无公网NAT网关。" % args.region)
        return 0

    print("Region %s 的公网NAT网关列表（共 %d 个，完整字段）：" % (args.region, len(gateways)))
    print(render_table(gateways))
    return 0


if __name__ == "__main__":
    sys.exit(main())
