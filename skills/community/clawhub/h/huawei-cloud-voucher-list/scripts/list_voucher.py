#!/usr/bin/env python3
"""List Huawei Cloud BSS (费用中心) vouchers / coupons via KooCLI.

Primary execution path is KooCLI `hcloud BSS ListSubCustomerCoupons`
(read-only GET /v2/promotions/benefits/coupons); when hcloud is not
installed the script falls back to the official `huaweicloudsdkbss` v2 SDK
(`BssClient.list_sub_customer_coupons`). It reads nothing but the active
credential profile / environment.

Supports three output modes (table / --json / --names-only), the real
`--coupon-id` and `--status` server-side filters, a client-side `--name`
filter (plan name / coupon code), automatic offset paging (BSS page limit
100), and a strict write-intent guard: any argument that looks like a
mutating coupon operation (create / reclaim / update / transfer / ...) is
rejected before a single command is executed — this skill is read-only.

Usage:
    python3 scripts/list_voucher.py [--region cn-north-1] [--json | --names-only]
                                    [--status available] [--name plan-2026]
                                    [--coupon-id CP...] [--page-size 100]
                                    [--operation ListSubCustomerCoupons]

Environment overrides (mostly for tests):
    VOUCHER_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    VOUCHER_LIST_HCLOUD_ARGS  extra args injected before the BSS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-1"
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 100
SERVICE = "BSS"
ALLOWED_OPERATION = "ListSubCustomerCoupons"
BSS_ENDPOINT = "https://bss.myhuaweicloud.com"

# The real BSS coupon-list operation is ListSubCustomerCoupons. "ListCoupons"
# is accepted as a read-only alias and normalised to the real operation.
OPERATION_ALIASES = {
    "listsubcustomercoupons": ALLOWED_OPERATION,
    "listcoupons": ALLOWED_OPERATION,
}

# Mutating BSS coupon operations / intents — strictly rejected by the guard.
# Only *specific* mutating operation names are listed for words that collide
# with legitimate read-only values (e.g. the status label "reclaimed" must not
# match a generic "reclaim" keyword).
WRITE_INTENT_KEYWORDS = (
    "createpartnercoupons",
    "reclaimpartnercoupons",
    "reclaimcouponquotas",
    "reclaimenterprisemultiaccountcoupon",
    "claimenterprisemultiaccountcoupon",
    "updatecouponquotas",
    "adjustcouponquotas",
    "transferenterprisemultiaccountcoupon",
    "retrieveenterprisemultiaccountcoupon",
    "sendcoupon",
    "issuecoupon",
    "deletecoupon",
    "freezecoupon",
    "unfreezecoupon",
    "cancelcoupon",
    "create",
    "delete",
    "update",
    "modify",
    "transfer",
    "retrieve",
    "adjust",
    "send",
    "issue",
    "cancel",
    "freeze",
    "unfreeze",
    "destroy",
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

# Human-readable labels for the numeric BSS enumerations.
STATUS_LABELS = {
    1: "UNACTIVATED",
    2: "AVAILABLE",
    3: "USED",
    4: "EXPIRED",
    5: "RECLAIMED",
}
COUPON_TYPE_LABELS = {
    1: "VOUCHER",
    2: "DISCOUNT",
    3: "PRODUCT",
    4: "CASH",
}

# Text -> numeric status accepted on --status (server-side). Anything not
# recognised here degrades to a client-side text match on the status label.
STATUS_ALIASES = {
    "1": 1, "unactivated": 1, "inactive": 1, "pending": 1, "notactivated": 1,
    "2": 2, "available": 2, "unused": 2, "valid": 2, "active": 2, "touse": 2,
    "3": 3, "used": 3,
    "4": 4, "expired": 4,
    "5": 5, "reclaimed": 5, "recycled": 5, "recalled": 5,
}

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "coupon_id",
    "coupon_code",
    "statusText",
    "couponTypeText",
    "plan_name",
    "face_value",
    "balance",
    "currency",
    "valid_time",
    "expire_time",
    "active_time",
    "create_time",
    "order_id",
    "promotion_plan_id",
    "customer_id",
    "source_id",
]

_COUPON_LIST_KEYS = ("user_coupons", "coupons", "coupon_infos", "coupon_list")

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


class VoucherListError(Exception):
    """Base error for the BSS voucher list skill."""


class GuardError(VoucherListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(VoucherListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(VoucherListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(VoucherListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-coupon`, `CreatePartnerCoupons`, and
    `create_partner_coupons` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（BSS ListSubCustomerCoupons），创建/回收/调整/转移等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def normalize_operation(operation):
    """Map a read-only operation / alias to the real BSS operation name."""
    key = re.sub(r"[\s_\-]+", "", str(operation).lower())
    if key in OPERATION_ALIASES:
        return OPERATION_ALIASES[key]
    return operation


def guard_operation(operation):
    """Only the read-only coupon-list operation may be executed."""
    normalized = normalize_operation(operation)
    if normalized != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return normalized


def parse_status(value):
    """Map a --status value to the numeric BSS status (1-5), else None.

    Returns an int for recognised numeric / textual values so it can be sent
    server-side; returns None for anything else (the caller then applies a
    client-side text filter on the status label).
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value if value in STATUS_LABELS else None
    key = re.sub(r"[\s_\-]+", "", str(value).strip().lower())
    return STATUS_ALIASES.get(key)


def build_command(region, coupon_id=None, status=None,
                  limit=DEFAULT_PAGE_SIZE, offset=0,
                  operation=ALLOWED_OPERATION):
    """Build the hcloud BSS coupon-list argv (without the executable).

    Mirrors the real KooCLI parameter list for the coupon-list API
    (`GET /v2/promotions/benefits/coupons`): --cli-region / --offset /
    --limit / --coupon_id / --status. `--name` has no server-side parameter
    and is applied client-side by `filter_by_name()`.
    """
    argv = [
        SERVICE,
        operation,
        "--cli-region=%s" % region,
        "--offset=%d" % offset,
        "--limit=%d" % limit,
    ]
    if coupon_id:
        argv.append("--coupon_id=%s" % coupon_id)
    if status is not None:
        argv.append("--status=%d" % status)
    return argv


def _hcloud_executable():
    return os.environ.get("VOUCHER_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("VOUCHER_LIST_HCLOUD_ARGS", "").split()
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
            "ListSubCustomerCoupons 真实参数清单可通过 "
            "`hcloud BSS ListSubCustomerCoupons --help` 查看。"
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
            "无权限访问 BSS 代金券，请检查 IAM 权限（403：AK/SK 无效或未授予 BSS "
            "只读权限），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_coupons(payload):
    """Pull the coupon list out of a ListSubCustomerCoupons response."""
    if isinstance(payload, list):
        return payload
    for key in _COUPON_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _total_count(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("count", "total_count", "totalCount", "total"):
        if isinstance(payload.get(key), int):
            return payload[key]
    return None


def _has_more(batch, collected, limit, payload):
    if not batch:
        return False
    total = _total_count(payload)
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def _status_text(value):
    if value is None:
        return "-"
    if isinstance(value, int):
        label = STATUS_LABELS.get(value)
        return "%s(%s)" % (label, value) if label else str(value)
    return str(value)


def filter_by_name(coupons, name):
    """Client-side name filter (case-insensitive substring).

    The coupon-list API has no `name`/`plan_name` query parameter, so the
    full paged list is fetched first and filtered locally against the
    promotion plan name (and the coupon code).
    """
    if not name:
        return list(coupons)
    wanted = str(name).strip().lower()
    matched = []
    for coupon in coupons:
        if not isinstance(coupon, dict):
            continue
        haystack = " ".join(
            str(coupon.get(field) or "")
            for field in ("plan_name", "coupon_code", "coupon_id")
        ).lower()
        if wanted in haystack:
            matched.append(coupon)
    return matched


def filter_by_status(coupons, status):
    """Client-side status filter for non-numeric / unrecognised values."""
    if status is None:
        return list(coupons)
    if isinstance(status, int):
        wanted = status
    else:
        parsed = parse_status(status)
        if parsed is not None:
            wanted = parsed
        else:
            wanted = str(status).strip().lower()
    matched = []
    for coupon in coupons:
        if not isinstance(coupon, dict):
            continue
        value = coupon.get("status")
        if isinstance(wanted, int):
            if value == wanted:
                matched.append(coupon)
        elif _status_text(value).lower() == wanted or str(value).strip().lower() == wanted:
            matched.append(coupon)
    return matched


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


def list_coupons_via_sdk(region, coupon_id=None, status=None,
                         limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query coupons through `huaweicloudsdkbss` v2.

    Only invoked when hcloud is not installed. BSS is a *global* service, so
    the official client requires `GlobalCredentials` + `with_endpoints` (not
    `BasicCredentials` + `with_region`). Credentials are taken from the
    standard environment variables (HUAWEI*/HW*/HWC* AK/SK markers) — never
    passed as literals here. The endpoint is the documented global BSS
    endpoint `https://bss.myhuaweicloud.com`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkbss.v2 import BssClient, ListSubCustomerCouponsRequest
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkbss 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkbss。详情：%s" % exc
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
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 GlobalCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HUAWEI_*/HW_*/HWC_* 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
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
    coupons = []
    offset = 0
    for _ in range(max_pages):
        request = ListSubCustomerCouponsRequest(
            coupon_id=coupon_id,
            status=status,
            offset=offset,
            limit=min(limit, MAX_PAGE_SIZE),
        )
        try:
            response = client.list_sub_customer_coupons(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 BSS 代金券，请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(getattr(response, "user_coupons", None) or [])
        coupons.extend(_model_to_dict(item) for item in batch)
        total = getattr(response, "count", None)
        if total is not None and len(coupons) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return coupons


def list_coupons(region, coupon_id=None, status=None, name=None,
                 limit=DEFAULT_PAGE_SIZE, max_pages=100,
                 operation=ALLOWED_OPERATION):
    """Query all coupons (paged); KooCLI first, SDK fallback.

    `status` is forwarded server-side when it resolves to a numeric BSS
    status code; `name` has no server-side parameter and is applied
    client-side after the full list is fetched.
    """
    status_int = parse_status(status)
    client_status = None if status_int is not None else status
    coupons = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, coupon_id=coupon_id, status=status_int,
                             limit=limit, offset=offset, operation=operation)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            coupons = list_coupons_via_sdk(
                region, coupon_id=coupon_id, status=status_int,
                limit=limit, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_coupons(payload)
        coupons.extend(batch)
        if not _has_more(batch, len(coupons), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    if client_status is not None:
        coupons = filter_by_status(coupons, client_status)
    return filter_by_name(coupons, name)


def normalize_coupon(coupon):
    """Add human-readable status / type labels and flatten use_limits."""
    flat = dict(coupon)
    flat["statusText"] = _status_text(coupon.get("status"))
    coupon_type = coupon.get("coupon_type")
    if isinstance(coupon_type, int):
        label = COUPON_TYPE_LABELS.get(coupon_type)
        flat["couponTypeText"] = ("%s(%s)" % (label, coupon_type)) if label else str(coupon_type)
    else:
        flat["couponTypeText"] = "-"
    limits = coupon.get("use_limits")
    if isinstance(limits, list):
        flat["useLimits"] = json.dumps(limits, ensure_ascii=False, separators=(",", ":"))
    return flat


def _field(coupon, *names, default="-"):
    for name in names:
        if name in coupon and coupon[name] not in (None, ""):
            return coupon[name]
    return default


def coupon_names(coupons):
    names = []
    for coupon in coupons:
        name = _field(coupon, "plan_name", "coupon_code", default=None)
        if name is None:
            name = _field(coupon, "coupon_id", default="")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(coupons):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_coupon(coupon) for coupon in coupons]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["coupon_id", "coupon_code"]
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
        description="查询华为云 BSS 代金券列表"
                    "（KooCLI hcloud BSS ListSubCustomerCoupons，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（BSS 仅支持 cn-north-1 等区域，默认 %s）"
                             % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出代金券名称（促销计划名称）清单")
    parser.add_argument("--status",
                        help="按代金券状态过滤（1-5 或 available/used/expired 等；"
                             "可识别的值走服务端，否则本地过滤）")
    parser.add_argument("--name", help="按促销计划名称 / 券码过滤（本地子串匹配）")
    parser.add_argument("--coupon-id", dest="coupon_id",
                        help="按代金券 ID 过滤（精确查询，服务端参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（BSS 上限 %d，默认 %d）"
                             % (MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE))
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud BSS 操作名（仅允许只读 %s / ListSubCustomerCoupons）"
                             % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        operation = guard_operation(args.operation)
        if args.status:
            guard_write_intent(args.status)
        if args.name:
            guard_write_intent(args.name)
        if args.coupon_id:
            guard_write_intent(args.coupon_id)
        coupons = list_coupons(
            args.region,
            coupon_id=args.coupon_id,
            status=args.status,
            name=args.name,
            limit=min(max(args.page_size, 1), MAX_PAGE_SIZE),
            operation=operation,
        )
    except VoucherListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(coupons, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 BSS 代金券名称列表（共 %d 张）："
              % (args.region, len(coupons)))
        for name in coupon_names(coupons):
            print("- %s" % name)
        return 0

    if not coupons:
        filters = []
        if args.status:
            filters.append("status=%s" % args.status)
        if args.name:
            filters.append("name=%s" % args.name)
        if args.coupon_id:
            filters.append("coupon_id=%s" % args.coupon_id)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无 BSS 代金券%s。" % (args.region, suffix))
        return 0

    print("Region %s 的 BSS 代金券列表（共 %d 张，完整字段）："
          % (args.region, len(coupons)))
    print(render_table(coupons))
    return 0


if __name__ == "__main__":
    sys.exit(main())
