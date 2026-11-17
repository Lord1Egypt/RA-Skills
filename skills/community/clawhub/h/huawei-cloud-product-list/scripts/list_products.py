#!/usr/bin/env python3
"""List the Huawei Cloud product (service) catalog via KooCLI.

Primary execution path is KooCLI `hcloud BSS ListServiceTypes` (read-only
GET /v2/products/service-types); when hcloud is not installed the script falls
back to the official `huaweicloudsdkbss` v2 SDK
(`BssClient.list_service_types`). It reads nothing but the active credential
profile / environment.

The catalog is the Huawei Cloud "云服务类型" directory: every item carries the
service (product) name (`service_type_name`), its code (`service_type_code`)
and its abbreviation (`abbreviation`).

Output modes:
  * default      table — 名称 / 编码 / 缩写 (name / code / abbreviation)
  * --json       raw response array (every returned field)
  * --names-only compact product name list

Supports `--name` (server-side fuzzy match on the service type name), `--code`
(client-side match on the service type code), region override, page-size, and a
strict write-intent guard: any argument that looks like a mutating BSS
operation is rejected before a single command is executed — this skill is
strictly read-only.

Usage:
    python3 scripts/list_products.py [--region cn-north-1] [--json | --names-only]
                                     [--name 弹性] [--code ecs]
                                     [--page-size 100]
                                     [--operation ListServiceTypes]

Environment overrides (mostly for tests):
    PRODUCT_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    PRODUCT_LIST_HCLOUD_ARGS  extra args injected before the BSS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-1"
DEFAULT_PAGE_SIZE = 100
SERVICE = "BSS"
ALLOWED_OPERATION = "ListServiceTypes"
REST_PATH = "/v2/products/service-types"
BSS_ENDPOINT = "https://bss.myhuaweicloud.com"

# Explicit AK/SK environment-variable whitelist for the SDK fallback path. Only
# these fixed keys are ever read (individually via os.environ.get); the process
# environment is never scanned or collected.
_AK_ENV_KEYS = (
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
)
_SK_ENV_KEYS = (
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
)

# Mutating BSS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createpartnercoupons",
    "reclaimpartnercoupons",
    "reclaimcouponquotas",
    "updatecouponquotas",
    "adjustcouponquotas",
    "transferenterprisemultiaccountcoupon",
    "retrieveenterprisemultiaccountcoupon",
    "create",
    "delete",
    "update",
    "modify",
    "transfer",
    "retrieve",
    "adjust",
    "reclaim",
    "send",
    "issue",
    "cancel",
    "freeze",
    "unfreeze",
    "destroy",
    "release",
    "remove",
    "创建",
    "删除",
    "修改",
    "回收",
    "发放",
    "转移",
    "认领",
    "调整",
    "冻结",
    "作废",
    "核销",
)

# The real field names returned by the 云服务类型目录 (service type catalog).
_NAME_KEYS = ("service_type_name",)
_CODE_KEYS = ("service_type_code",)
_ABBR_KEYS = ("abbreviation",)
_PRODUCT_LIST_KEYS = ("service_types", "serviceTypes", "products", "services")
_TOTAL_KEYS = ("total_count", "totalCount", "count", "total")

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

# A KooCLI build whose offline metadata does not include the BSS service answers
# `[USE_ERROR]Unsupported service: BSS.` (stdout, exit code 0). That is a
# CLI-build limitation, not a request error, so the SDK fallback is attempted
# instead of failing outright.
_SERVICE_UNSUPPORTED_PATTERNS = (
    "unsupported service",
    "service is not supported",
    "service not supported",
    "unknown service",
    "不支持的服务",
    "不支持的service",
)


class ProductListError(Exception):
    """Base error for the product catalog list skill."""


class GuardError(ProductListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(ProductListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(ProductListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ProductListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-coupon`, `CreatePartnerCoupons`, and
    `create_partner_coupons` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe/query) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（BSS ListServiceTypes，云服务类型目录），创建/删除/变更类操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListServiceTypes operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, name=None, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud BSS ListServiceTypes argv (without the executable).

    Mirrors the real KooCLI parameter list for the 云服务类型目录 API
    (`GET /v2/products/service-types`): --cli-region / --limit / --offset and
    the real server-side fuzzy query parameter --service_type_name.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--offset=%d" % offset,
        "--limit=%d" % limit,
    ]
    if name:
        argv.append("--service_type_name=%s" % name)
    return argv


def _hcloud_executable():
    return os.environ.get("PRODUCT_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("PRODUCT_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：BSS "
            "ListServiceTypes 真实参数清单可通过 "
            "`hcloud BSS ListServiceTypes --help` 查看。"
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
            "无权限访问华为云产品目录（BSS 云服务类型），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 BSS 只读权限），参见 references/iam-policies.md。"
            "详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def is_service_unsupported(stdout, stderr=""):
    """True when hcloud reports that its metadata lacks the BSS service.

    The installed KooCLI uses an offline service metadata cache; a build whose
    cache predates BSS answers `[USE_ERROR]Unsupported service: BSS.` (on stdout,
    with exit code 0). That is a CLI-build limitation rather than a bad request,
    so the caller falls back to the SDK instead of reporting a parameter error.
    """
    blob = (str(stdout) + " " + str(stderr)).lower()
    return any(pattern in blob for pattern in _SERVICE_UNSUPPORTED_PATTERNS)


def extract_products(payload):
    """Pull the service-type (product) list out of a ListServiceTypes response."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in _PRODUCT_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _total_count(payload):
    if not isinstance(payload, dict):
        return None
    for key in _TOTAL_KEYS:
        value = payload.get(key)
        if isinstance(value, int):
            return value
    return None


def _has_more(batch, collected, limit, payload):
    if not batch:
        return False
    total = _total_count(payload)
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def _model_to_dict(model):
    if hasattr(model, "to_json_object"):
        try:
            return model.to_json_object()
        except Exception:  # pragma: no cover - defensive
            pass
    if hasattr(model, "to_dict"):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return model.to_dict()
    if isinstance(model, dict):
        return dict(model)
    return {"value": str(model)}


def list_products_via_sdk(region, name=None, limit=DEFAULT_PAGE_SIZE,
                          max_pages=100):
    """SDK fallback: query the service-type catalog through `huaweicloudsdkbss` v2.

    Only invoked when hcloud is not installed. BSS is a *global* service, so
    the official client requires `GlobalCredentials` + `with_endpoints` (not
    `BasicCredentials` + `with_region`). Credentials are read from a fixed,
    explicitly named whitelist of AK/SK environment variables — never scanned
    from the whole environment, never passed as literals here. The endpoint is
    the documented global BSS endpoint `https://bss.myhuaweicloud.com`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkbss.v2 import BssClient, ListServiceTypesRequest
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkbss 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkbss。详情：%s" % exc
        )

    def _env_credential(keys):
        # Explicit whitelist: only these fixed variable names are read, one by
        # one. The environment is never iterated or collected.
        for key in keys:
            value = os.environ.get(key)
            if value:
                return value
        return None

    ak = _env_credential(_AK_ENV_KEYS)
    sk = _env_credential(_SK_ENV_KEYS)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 GlobalCredentials 不会自动读取环境"
            "变量，且当前环境未设置受支持的 AK/SK 环境变量（HUAWEICLOUD_SDK_AK /"
            " HUAWEICLOUD_SDK_SK、HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY 或"
            " HW_ACCESS_KEY / HW_SECRET_KEY）。请在会话外设置上述固定键名（严禁在对话"
            "中粘贴 AK/SK），参见 references/cli-installation-guide.md。"
        )
    credentials = GlobalCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        client = BssClient.new_builder() \
            .with_credentials(credentials) \
            .with_http_config(HttpConfig.get_default_config()) \
            .with_endpoints([BSS_ENDPOINT]) \
            .build()
    except Exception as exc:  # config / endpoint broken
        raise ConfigError(
            "SDK 初始化失败（endpoint=%s）：%s。请检查 huaweicloudsdkbss 安装。"
            % (BSS_ENDPOINT, exc)
        )
    products = []
    offset = 0
    for _ in range(max_pages):
        request = ListServiceTypesRequest(
            service_type_name=name,
            offset=offset,
            limit=limit,
        )
        try:
            response = client.list_service_types(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问华为云产品目录（BSS 云服务类型），请检查 IAM 权限（403）。"
                    "详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(getattr(response, "service_types", None) or [])
        products.extend(_model_to_dict(item) for item in batch)
        total = getattr(response, "total_count", None)
        if total is not None and len(products) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return products


def list_products(region, name=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query the product catalog (paged); KooCLI first, SDK fallback."""
    products = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, name=name, limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            products = list_products_via_sdk(
                region, name=name, limit=limit, max_pages=max_pages)
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0. When the
            # CLI's offline metadata simply lacks the BSS service, fall back to
            # the SDK; otherwise classify and raise. If the SDK fallback itself
            # is unavailable (missing deps / credentials) keep the original CLI
            # failure so the error hint stays accurate.
            if is_service_unsupported(stdout, stderr):
                try:
                    products = list_products_via_sdk(
                        region, name=name, limit=limit, max_pages=max_pages)
                except ConfigError:
                    raise classify_hcloud_failure(stdout, stderr, returncode)
                break
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_products(payload)
        products.extend(batch)
        if not _has_more(batch, len(products), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return products


def _field(product, keys, default="-"):
    for key in keys:
        value = product.get(key)
        if value not in (None, ""):
            return value
    return default


def standardize_products(products):
    """Reduce every catalog item to ``name`` / ``code`` / ``abbreviation``."""
    standardized = []
    for product in products:
        standardized.append({
            "name": str(_field(product, _NAME_KEYS)),
            "code": str(_field(product, _CODE_KEYS)),
            "abbreviation": str(_field(product, _ABBR_KEYS)),
        })
    return standardized


def product_names(products):
    return [row["name"] for row in standardize_products(products)]


def filter_by_code(products, code):
    """Client-side filter on the service type code (case-insensitive substring)."""
    if not code:
        return list(products)
    wanted = str(code).strip().lower()
    matched = []
    for product in products:
        if not isinstance(product, dict):
            continue
        value = _field(product, _CODE_KEYS, default="")
        if wanted in str(value).lower():
            matched.append(product)
    return matched


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(products):
    """Render the 名称 / 编码 / 缩写 table (default output)."""
    rows_data = standardize_products(products)
    columns = (("name", "名称"), ("code", "编码"), ("abbreviation", "缩写"))
    rows = [[_cell(row[key]) for key, _ in columns] for row in rows_data]
    headers = [label for _, label in columns]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows))
              for i in range(len(columns))]
    header = "  ".join(headers[i].ljust(widths[i]) for i in range(len(columns)))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云产品（云服务类型）目录"
                    "（KooCLI hcloud BSS ListServiceTypes，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（BSS 仅支持 cn-north-1 等区域，默认 %s）"
                             % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出产品（服务）名称清单")
    parser.add_argument("--name", help="按产品（服务）名称模糊查询（服务端参数）")
    parser.add_argument("--code", help="按服务编码过滤（本地子串匹配）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud BSS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        products = list_products(
            args.region,
            name=args.name,
            limit=max(args.page_size, 1),
        )
    except ProductListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.code:
        products = filter_by_code(products, args.code)

    if args.as_json:
        print(json.dumps(products, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("华为云产品（服务）名称列表（共 %d 个）：" % len(products))
        for name in product_names(products):
            print("- %s" % name)
        return 0

    if not products:
        filters = []
        if args.name:
            filters.append("name=%s" % args.name)
        if args.code:
            filters.append("code=%s" % args.code)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("未查询到华为云产品（服务）目录数据%s。" % suffix)
        return 0

    print("华为云产品（服务）目录（共 %d 个，字段：名称 / 编码 / 缩写）："
          % len(products))
    print(render_table(products))
    return 0


if __name__ == "__main__":
    sys.exit(main())