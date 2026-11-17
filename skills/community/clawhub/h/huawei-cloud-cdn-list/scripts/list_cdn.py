#!/usr/bin/env python3
"""List Huawei Cloud CDN (Content Delivery Network) accelerated domains via KooCLI.

Primary execution path is KooCLI (`hcloud CDN ListDomains`, read-only
GET /v1.0/cdn/domains); when hcloud is not installed the script falls back to
the official `huaweicloudsdkcdn` v1 SDK (`CdnClient.list_domains`). Reads
nothing but the active credential profile / environment. Supports the table /
--json / --names-only output modes, server-side --domain-name / --business-type
/ --domain-status filters, page_number-based paging over the ListDomains
`total` count, and a strict write-intent guard: any argument that looks like a
mutating CDN operation is rejected before a single command is executed.

Usage:
    python3 scripts/list_cdn.py [--region cn-north-4] [--json | --names-only]
                                [--domain-name example.com]
                                [--domain-status online] [--business-type web]
                                [--service-area mainland_china]
                                [--enterprise-project-id 0]
                                [--page-size 100] [--operation ListDomains]

Environment overrides (mostly for tests):
    CDN_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    CDN_LIST_HCLOUD_ARGS  extra args injected before the CDN operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "CDN"
ALLOWED_OPERATION = "ListDomains"

# Explicit credential environment-variable whitelist. The SDK fallback reads
# only these exact names, one key at a time via os.getenv(); the process
# environment is never enumerated.
AK_ENV_KEYS = (
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HUAWEI_AK",
    "HW_AK",
)
SK_ENV_KEYS = (
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
    "HUAWEI_SK",
    "HW_SK",
)

# Mutating CDN operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createdomain",
    "deletedomain",
    "updatedomain",
    "enabledomain",
    "disabledomain",
    "modifydomain",
    "modifydomainconfig",
    "updatedomainfullconfig",
    "updatedomainmulticertificates",
    "updatedomainorigin",
    "createdomainbyfile",
    "createdomainbycopy",
    "batchcreatedomain",
    "batchdeletedomain",
    "createpreheatingtask",
    "createdomaintemplate",
    "deleteconsumerule",
    "createconsumerule",
    "createrefresh",
    "refreshtask",
    "preheating",
    "batchcopy",
    "create",
    "delete",
    "update",
    "modify",
    "enable",
    "disable",
    "refresh",
    "preheat",
    "destroy",
    "remove",
    "reset",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "domain_name",
    "domain_status",
    "cname",
    "business_type",
    "id",
    "service_area",
    "https_status",
    "disabled",
    "locked",
    "origin_status",
    "enterprise_project_id",
    "create_time",
    "modify_time",
    "tags",
]

_DOMAIN_LIST_KEYS = ("domains",)

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


class CdnListError(Exception):
    """Base error for the CDN list skill."""


class GuardError(CdnListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CdnListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CdnListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CdnListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-domain`, `CreateDomain`, and
    `create_domain` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（CDN ListDomains），创建/删除/更新/启用/停用等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListDomains operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, domain_name=None, business_type=None,
                  domain_status=None, service_area=None,
                  enterprise_project_id=None, limit=DEFAULT_PAGE_SIZE,
                  page_number=1):
    """Build the hcloud CDN ListDomains argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only CDN ListDomains
    operation: --cli-region / --page_size / --page_number plus the real
    server-side filters --domain_name / --business_type / --domain_status /
    --service_area / --enterprise_project_id. CDN pages with `page_size` +
    `page_number` (the response carries `total`).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--page_size=%d" % limit,
        "--page_number=%d" % page_number,
    ]
    if domain_name:
        argv.append("--domain_name=%s" % domain_name)
    if business_type:
        argv.append("--business_type=%s" % business_type)
    if domain_status:
        argv.append("--domain_status=%s" % domain_status)
    if service_area:
        argv.append("--service_area=%s" % service_area)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("CDN_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CDN_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：CDN ListDomains "
            "真实参数清单可通过 `hcloud CDN ListDomains --help` 查看。"
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
            "无权限访问内容分发网络（CDN），请检查 IAM 权限（403：AK/SK 无效或未授予"
            " CDN 只读权限），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_domains(payload):
    """Pull the accelerated-domain list out of a ListDomains response."""
    if isinstance(payload, list):
        return payload
    for key in _DOMAIN_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _total(payload):
    """Read the `total` domain count from a ListDomains response (0 if absent)."""
    if not isinstance(payload, dict):
        return None
    total = payload.get("total")
    try:
        return int(total)
    except (TypeError, ValueError):
        return None


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def list_domains_via_sdk(region, domain_name=None, business_type=None,
                         domain_status=None, service_area=None,
                         enterprise_project_id=None, limit=DEFAULT_PAGE_SIZE,
                         max_pages=100):
    """SDK fallback: query CDN accelerated domains through `huaweicloudsdkcdn` v1.

    Only invoked when hcloud is not installed. Credentials are read one key at
    a time from an explicit whitelist of environment-variable names
    (`AK_ENV_KEYS` / `SK_ENV_KEYS`, e.g. HUAWEICLOUD_SDK_AK / HUAWEI_ACCESS_KEY
    and HUAWEICLOUD_SDK_SK / HUAWEI_SECRET_KEY) — never passed as literals here
    and the environment is never enumerated. CDN is a global service, so the SDK
    client is authenticated with `GlobalCredentials`; the official SDK has no
    env-var auto-discovery, so AK/SK must be read explicitly. Region resolution
    uses the SDK's own `CdnRegion` catalog (official endpoints, no guessing),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    `ListDomainsRequest` accepts `domain_name` / `business_type` /
    `domain_status` / `service_area` / `enterprise_project_id` plus
    `page_size` + `page_number` paging.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcdn.v1 import CdnClient, ListDomainsRequest
        from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkcdn 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkcdn。详情：%s" % exc
        )

    def _env_credential(keys):
        for name in keys:
            value = os.getenv(name)
            if value:
                return value
        return None

    ak = _env_credential(AK_ENV_KEYS)
    sk = _env_credential(SK_ENV_KEYS)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 GlobalCredentials 不会自动读取环境"
            "变量，且当前环境未检测到白名单中的 AK/SK 环境变量（如"
            " HUAWEICLOUD_SDK_AK / HUAWEI_ACCESS_KEY 与 HUAWEICLOUD_SDK_SK /"
            " HUAWEI_SECRET_KEY）。请在会话外设置其中之一（严禁在对话中粘贴 AK/SK），"
            "参见 references/cli-installation-guide.md。"
        )
    credentials = GlobalCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = CdnRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://cdn.myhuaweicloud.com")
        client = CdnClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkcdn 安装与区域配置。"
            % (region, exc)
        )
    domains = []
    page_number = 1
    total = None
    for _ in range(max_pages):
        request = ListDomainsRequest(
            domain_name=domain_name,
            business_type=business_type,
            domain_status=domain_status,
            service_area=service_area,
            enterprise_project_id=enterprise_project_id,
            page_size=limit,
            page_number=page_number,
        )
        try:
            response = client.list_domains(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问内容分发网络（CDN），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.domains or [])
        domains.extend(_jsonable(domain.to_dict()) for domain in batch)
        total = getattr(response, "total", None)
        if not batch or len(batch) < limit:
            break
        if total is not None:
            try:
                if len(domains) >= int(total):
                    break
            except (TypeError, ValueError):
                pass
        page_number += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return domains


def list_domains(region, domain_name=None, business_type=None,
                 domain_status=None, service_area=None,
                 enterprise_project_id=None, limit=DEFAULT_PAGE_SIZE,
                 max_pages=100):
    """Query all CDN accelerated domains (page-paged); KooCLI first, SDK fallback."""
    domains = []
    page_number = 1
    total = None
    for _page in range(max_pages):
        argv = build_command(region, domain_name=domain_name,
                             business_type=business_type,
                             domain_status=domain_status,
                             service_area=service_area,
                             enterprise_project_id=enterprise_project_id,
                             limit=limit, page_number=page_number)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            domains = list_domains_via_sdk(
                region, domain_name=domain_name, business_type=business_type,
                domain_status=domain_status, service_area=service_area,
                enterprise_project_id=enterprise_project_id,
                limit=limit, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_domains(payload)
        domains.extend(batch)
        total = _total(payload)
        if not batch or len(batch) < limit:
            break
        if total is not None and len(domains) >= total:
            break
        page_number += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return domains


def normalize_domain(domain):
    """Flatten tag lists into a table-friendly string; keep other fields as-is."""
    flat = dict(domain)
    tags = domain.get("tags")
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


def _field(domain, *names, default="-"):
    for name in names:
        if name in domain and domain[name] not in (None, ""):
            return domain[name]
    return default


def domain_names(domains):
    names = []
    for domain in domains:
        name = _field(domain, "domain_name", default=None)
        if name is None:
            name = _field(domain, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(domains):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_domain(domain) for domain in domains]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["domain_name", "domain_status"]
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
        description="查询华为云 CDN 加速域名列表（KooCLI hcloud CDN ListDomains，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出加速域名清单")
    parser.add_argument("--domain-name", dest="domain_name",
                        help="按加速域名过滤（服务端查询参数，支持模糊匹配）")
    parser.add_argument("--domain-status", dest="domain_status",
                        help="按加速域名状态过滤（如 online/offline/configuring，服务端查询参数）")
    parser.add_argument("--business-type", dest="business_type",
                        help="按业务类型过滤（如 web/download/vod/live，服务端查询参数）")
    parser.add_argument("--service-area", dest="service_area",
                        help="按服务区域过滤（如 mainland_china/outside_mainland_china，服务端查询参数）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud CDN 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        for value in (args.domain_name, args.domain_status, args.business_type,
                      args.service_area, args.enterprise_project_id):
            if value:
                guard_write_intent(value)
        domains = list_domains(
            args.region,
            domain_name=args.domain_name,
            business_type=args.business_type,
            domain_status=args.domain_status,
            service_area=args.service_area,
            enterprise_project_id=args.enterprise_project_id,
            limit=args.page_size,
        )
    except CdnListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(domains, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 CDN 加速域名清单（共 %d 个）：" % (args.region, len(domains)))
        for name in domain_names(domains):
            print("- %s" % name)
        return 0

    if not domains:
        filters = []
        if args.domain_name:
            filters.append("domain_name=%s" % args.domain_name)
        if args.domain_status:
            filters.append("domain_status=%s" % args.domain_status)
        if args.business_type:
            filters.append("business_type=%s" % args.business_type)
        if args.service_area:
            filters.append("service_area=%s" % args.service_area)
        if args.enterprise_project_id:
            filters.append("enterprise_project_id=%s" % args.enterprise_project_id)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无 CDN 加速域名%s。" % (args.region, suffix))
        return 0

    print("Region %s 的 CDN 加速域名列表（共 %d 个，完整字段）：" % (args.region, len(domains)))
    print(render_table(domains))
    return 0


if __name__ == "__main__":
    sys.exit(main())