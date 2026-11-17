#!/usr/bin/env python3
"""Send (issue) Huawei Cloud BSS vouchers / coupons to sub-customers.

Primary execution path is KooCLI ``hcloud BSS CreatePartnerCoupons`` (the
official *issue coupon* API, ``POST /v2/promotions/benefits/partner-coupons``):
a distributor / partner issues new coupons from one of its coupon quotas to one
or more designated sub-customers. When ``hcloud`` is not installed the script
falls back to the official ``huaweicloudsdkbss`` v2 SDK
(``BssClient.create_partner_coupons``).

This is a **write / mutating** skill: issuing a coupon moves money / benefit to
the target account and is normally irreversible, therefore

* a live send requires the explicit ``--confirm`` flag (otherwise the run stops
  with a clear message), and
* ``--dry-run`` previews the exact request without issuing anything.

The skill supports **batch** targets (many sub-customers per call) and
**per-customer idempotency** (a local ledger remembers already-issued customers,
so retrying a failed batch never double-issues).

Credentials are never handled by this script: the CLI path uses the active
``hcloud`` profile, the SDK path reads the standard Huawei Cloud environment
variables through ``config.py``.

Usage:
    python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \\
        --customer-id CUST001 --customer-id CUST002 --confirm
    python3 scripts/send_voucher.py --quota-id Q001 --face-value 100.00 \\
        --customer-ids CUST001,CUST002 --dry-run

Environment overrides (mostly for tests):
    VOUCHER_SEND_HCLOUD_BIN    hcloud executable (default "hcloud")
    VOUCHER_SEND_LEDGER        idempotency ledger path
    VOUCHER_SEND_CLI_ARGS      extra args injected before the BSS operation
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from decimal import Decimal, InvalidOperation

try:  # imported as a sibling module (scripts/ on sys.path)
    from config import BSS_ENDPOINT, DEFAULT_REGION, build_http_config, load_ak_sk
except ImportError:  # pragma: no cover - direct execution fallback
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import BSS_ENDPOINT, DEFAULT_REGION, build_http_config, load_ak_sk

SERVICE = "BSS"
ALLOWED_OPERATION = "CreatePartnerCoupons"

# Accepted (write) operation aliases -> the one real BSS operation. The issue
# API is CreatePartnerCoupons; a few plausible synonyms are mapped so users are
# not tripped up by naming, but no other operation is ever executed.
OPERATION_ALIASES = {
    "createpartnercoupons": ALLOWED_OPERATION,
    "createsubcustomercoupons": ALLOWED_OPERATION,
    "sendsubcustomercoupons": ALLOWED_OPERATION,
    "sendpartnercoupons": ALLOWED_OPERATION,
    "sendcoupons": ALLOWED_OPERATION,
}

DEFAULT_IDEMPOTENCY_WINDOW = 86400  # seconds (24h)
_DEFAULT_LEDGER = os.path.join(
    os.path.expanduser("~"), ".cache", "huawei-cloud-voucher-send", "ledger.json"
)

_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

_CREDENTIAL_MISSING_PATTERNS = (
    "cli-ak", "cli-sk", "access key", "secret key", "credential", "configure",
    "未配置", "配置为空", "no ak", "no sk", "ak/sk",
)
_AUTH_PATTERNS = (
    "401", "403", "unauthorized", "forbidden", "apigw.0301",
    "认证失败", "权限不足", "permission denied",
)
# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — must be a hard failure even when rc looks fine.
_USE_ERROR_MARKER = "[use_error]"


class SendVoucherError(Exception):
    """Base error for the BSS voucher-send skill."""


class ConfigError(SendVoucherError):
    """hcloud missing / not usable, or credentials not configured."""


class AuthError(SendVoucherError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(SendVoucherError):
    """hcloud / network / unexpected API failure."""


class ValidationError(ConfigError):
    """A required parameter is missing or invalid (config-class error)."""


class ConfirmationRequired(SendVoucherError):
    """A live write was attempted without the explicit --confirm flag."""


# --------------------------------------------------------------- validation

def parse_face_value(value):
    """Validate a face value and return it as a 2-decimal string.

    The API requires a value > 0 and precise to two decimal places. Values with
    more than two decimals are rejected (rather than silently rounded) so the
    caller never issues a coupon of an unintended amount.
    """
    if value is None or str(value).strip() == "":
        raise ValidationError("缺少必填参数 --face-value（代金券面值，单位：元）。")
    text = str(value).strip()
    try:
        amount = Decimal(text)
    except (InvalidOperation, ValueError):
        raise ValidationError("参数 --face-value=%r 非法：必须是大于 0 的数字。" % value)
    if amount <= 0:
        raise ValidationError("参数 --face-value=%s 非法：面值必须大于 0。" % text)
    quantized = amount.quantize(Decimal("0.01"))
    if quantized != amount:
        raise ValidationError(
            "参数 --face-value=%s 非法：面值只支持精确到小数点后 2 位。" % text)
    return "%.2f" % quantized


def validate_time(value, name):
    """Validate an optional UTC time (yyyy-MM-ddTHH:mm:ssZ); None passes."""
    if value is None or str(value).strip() == "":
        return None
    text = str(value).strip()
    if not _TIME_RE.match(text):
        raise ValidationError(
            "参数 --%s=%s 非法：需为 UTC 时间，格式 yyyy-MM-ddTHH:mm:ssZ"
            "（如 2019-05-06T08:05:01Z）。" % (name, text))
    return text


def normalize_customer_ids(raw_values):
    """Flatten repeatable / comma-separated customer IDs; keep order, drop dups."""
    ids = []
    seen = set()
    for raw in raw_values or []:
        for part in str(raw).split(","):
            customer = part.strip()
            if not customer or customer in seen:
                continue
            seen.add(customer)
            ids.append(customer)
    return ids


def read_customers_file(path):
    """Read one customer ID per line (# comments and blanks ignored)."""
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as exc:
        raise ValidationError("无法读取 --customers-file=%s：%s" % (path, exc))
    ids = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        ids.append(stripped)
    return ids


def validate_inputs(quota_id, customer_ids, face_value):
    """Fail fast on missing / invalid required parameters."""
    if not quota_id or not str(quota_id).strip():
        raise ValidationError(
            "缺少必填参数 --quota-id（代金券额度ID；可由 BSS ListQuotaCoupons 查询）。")
    if not customer_ids:
        raise ValidationError(
            "缺少目标客户：至少提供一个 --customer-id / --customer-ids / --customers-file。")
    # face_value validity is enforced by parse_face_value when normalised.
    return True


# --------------------------------------------------------------- command build

def normalize_operation(operation):
    """Map an accepted alias to the single real BSS operation name."""
    key = re.sub(r"[\s_\-]+", "", str(operation).lower())
    if key in OPERATION_ALIASES:
        return OPERATION_ALIASES[key]
    return operation


def guard_operation(operation):
    """Only the issue-coupon operation may ever be executed."""
    normalized = normalize_operation(operation)
    if normalized != ALLOWED_OPERATION:
        raise ValidationError(
            "不允许的操作 %r：本 skill 仅支持发放操作 %s。"
            % (operation, ALLOWED_OPERATION))
    return normalized


def build_command(region, quota_id, customer_ids, face_value,
                  valid_time=None, expire_time=None,
                  cloud_service_types=None, product_ids=None,
                  memo=None, indirect_partner_id=None,
                  operation=ALLOWED_OPERATION):
    """Build the hcloud BSS issue-coupon argv (without the executable).

    Mirrors the KooCLI parameter list for ``POST /v2/promotions/benefits/
    partner-coupons``: ``--cli-region`` / ``--quota_id`` / ``--customer_ids.N``
    / ``--face_value`` and the optional body fields. Array parameters use the
    KooCLI ``<name>.<index>`` form.
    """
    argv = [
        SERVICE,
        operation,
        "--cli-region=%s" % region,
        "--quota_id=%s" % quota_id,
    ]
    for index, customer in enumerate(customer_ids, start=1):
        argv.append("--customer_ids.%d=%s" % (index, customer))
    argv.append("--face_value=%s" % face_value)
    if valid_time:
        argv.append("--valid_time=%s" % valid_time)
    if expire_time:
        argv.append("--expire_time=%s" % expire_time)
    for index, service_type in enumerate(cloud_service_types or [], start=1):
        argv.append("--cloud_service_types.%d=%s" % (index, service_type))
    for index, product_id in enumerate(product_ids or [], start=1):
        argv.append("--product_ids.%d=%s" % (index, product_id))
    if memo is not None:
        argv.append("--memo=%s" % memo)
    if indirect_partner_id:
        argv.append("--indirect_partner_id=%s" % indirect_partner_id)
    return argv


# --------------------------------------------------------------- hcloud run

def _hcloud_executable():
    return os.environ.get("VOUCHER_SEND_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("VOUCHER_SEND_CLI_ARGS", "").split()
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
    text = (stdout or "").strip()
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
    blob = ((stderr or "") + " " + (stdout or "")).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：BSS "
            "CreatePartnerCoupons 真实参数清单可通过 "
            "`hcloud BSS CreatePartnerCoupons --help` 查看。详情：%s"
            % (returncode, blob[:300])
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
            "无权限发放 BSS 代金券，请检查 IAM 权限（403：AK/SK 无效或未授予 BSS "
            "发放权限），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


# --------------------------------------------------------------- SDK fallback

def send_via_sdk(region, quota_id, customer_ids, face_value,
                 valid_time=None, expire_time=None,
                 cloud_service_types=None, product_ids=None,
                 memo=None, indirect_partner_id=None):
    """SDK fallback: issue coupons through ``huaweicloudsdkbss`` v2.

    Only invoked when hcloud is not installed. BSS is a *global* service, so the
    official client uses ``GlobalCredentials`` + ``with_endpoints``. Credentials
    come from the standard environment variables via ``config.load_ak_sk``.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkbss.v2 import BssClient, CreatePartnerCouponsRequest, \
            CreatePartnerCouponsReq
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkbss 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkbss。详情：%s" % exc
        )

    ak, sk = load_ak_sk()
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
            .with_http_config(build_http_config()) \
            .with_endpoints([BSS_ENDPOINT]) \
            .build()
    except Exception as exc:  # config / endpoint broken
        raise ConfigError(
            "SDK 初始化失败（endpoint=%s）：%s。请检查 huaweicloudsdkbss 安装。"
            % (BSS_ENDPOINT, exc)
        )

    body = CreatePartnerCouponsReq(
        quota_id=quota_id,
        customer_ids=list(customer_ids),
        face_value=Decimal(face_value),
        valid_time=valid_time,
        expire_time=expire_time,
        cloud_service_types=list(cloud_service_types or []) or None,
        product_ids=list(product_ids or []) or None,
        memo=memo,
        indirect_partner_id=indirect_partner_id,
    )
    request = CreatePartnerCouponsRequest(body=body)
    try:
        response = client.create_partner_coupons(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限发放 BSS 代金券，请检查 IAM 权限（403）。详情：%s"
                % str(exc)[:300])
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])

    return _response_to_payload(response)


# --------------------------------------------------------------- response parse

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


def _response_to_payload(response):
    """Turn an SDK response into the same shape as the hcloud JSON body."""
    coupon_infos = [_model_to_dict(item)
                    for item in (getattr(response, "coupon_infos", None) or [])]
    error_details = [_model_to_dict(item)
                     for item in (getattr(response, "error_details", None) or [])]
    return {"coupon_infos": coupon_infos, "error_details": error_details}


def parse_response(payload):
    """Extract issued coupons and per-customer errors from an API response."""
    if isinstance(payload, list):
        payload = {"coupon_infos": payload}
    if not isinstance(payload, dict):
        return [], []
    issued = list(payload.get("coupon_infos") or [])
    errors = list(payload.get("error_details") or [])
    return issued, errors


# --------------------------------------------------------------- idempotency

def idempotency_key(quota_id, customer_id, face_value, expire_time=None,
                    memo=None, cloud_service_types=None, product_ids=None,
                    indirect_partner_id=None):
    """Stable per-customer natural key for the idempotency ledger."""
    parts = [
        str(quota_id), str(customer_id), str(face_value),
        expire_time or "", memo or "",
        ",".join(cloud_service_types or []),
        ",".join(product_ids or []),
        indirect_partner_id or "",
    ]
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return digest[:32]


def _ledger_path(explicit=None):
    return explicit or os.environ.get("VOUCHER_SEND_LEDGER") or _DEFAULT_LEDGER


def load_ledger(path, window=DEFAULT_IDEMPOTENCY_WINDOW, now=None):
    """Load the ledger, dropping entries older than the idempotency window."""
    now = now if now is not None else time.time()
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, dict):
        return {}
    fresh = {}
    for key, value in entries.items():
        try:
            at = float(value.get("at", 0))
        except (AttributeError, TypeError, ValueError):
            continue
        if window <= 0 or now - at <= window:
            fresh[key] = value
    return fresh


def save_ledger(path, entries):
    """Persist the ledger atomically (best-effort; never fatal)."""
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump({"entries": entries}, handle, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except OSError:
        return False
    return True


# --------------------------------------------------------------- orchestration

def send_coupons(region, quota_id, customer_ids, face_value, *,
                 valid_time=None, expire_time=None,
                 cloud_service_types=None, product_ids=None,
                 memo=None, indirect_partner_id=None,
                 operation=ALLOWED_OPERATION, dry_run=False, confirm=False,
                 use_idempotency=True, force=False,
                 idempotency_window=DEFAULT_IDEMPOTENCY_WINDOW, ledger_path=None):
    """Issue coupons, with batch + per-customer idempotency.

    Returns a dict with ``issued`` / ``errors`` / ``skipped`` / ``pending`` /
    ``dry_run`` / ``command``. Raises on config / auth / API errors.
    """
    validate_inputs(quota_id, customer_ids, face_value)

    keys = {
        c: idempotency_key(quota_id, c, face_value, expire_time, memo,
                           cloud_service_types, product_ids, indirect_partner_id)
        for c in customer_ids
    }

    ledger = {}
    skipped = []
    pending = list(customer_ids)
    if use_idempotency and not force:
        ledger_path = _ledger_path(ledger_path)
        ledger = load_ledger(ledger_path, window=idempotency_window)
        pending = [c for c in customer_ids if keys[c] not in ledger]
        skipped = [c for c in customer_ids if keys[c] in ledger]

    command = build_command(
        region, quota_id, pending or customer_ids, face_value,
        valid_time=valid_time, expire_time=expire_time,
        cloud_service_types=cloud_service_types, product_ids=product_ids,
        memo=memo, indirect_partner_id=indirect_partner_id,
        operation=operation,
    )

    result = {
        "quota_id": quota_id,
        "face_value": face_value,
        "region": region,
        "issued": [],
        "errors": [],
        "skipped": [{"customer_id": c, "reason": "already_issued"}
                    for c in skipped],
        "pending": pending,
        "dry_run": bool(dry_run),
        "command": command if dry_run else None,
    }

    if not pending:
        result["reason"] = "all_skipped_by_idempotency"
        return result

    if dry_run:
        result["reason"] = "dry_run_preview"
        return result

    if not confirm:
        raise ConfirmationRequired(
            "发放代金券是变更类写操作（涉及资金/权益、不可逆）。请确认后加 --confirm "
            "执行，或先用 --dry-run 预览请求。")

    # ---- live call: CLI first, SDK fallback ----
    try:
        stdout, stderr, returncode = run_hcloud(command)
    except ConfigError:
        payload = send_via_sdk(
            region, quota_id, pending, face_value,
            valid_time=valid_time, expire_time=expire_time,
            cloud_service_types=cloud_service_types, product_ids=product_ids,
            memo=memo, indirect_partner_id=indirect_partner_id)
    else:
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)

    issued, errors = parse_response(payload)
    result["issued"] = issued
    result["errors"] = errors

    if use_idempotency:
        ledger_path = _ledger_path(ledger_path)
        now = time.time()
        for info in issued:
            customer_id = str(info.get("id") or info.get("customer_id") or "")
            if customer_id and customer_id in keys:
                ledger[keys[customer_id]] = {
                    "at": now, "coupon_id": info.get("coupon_id")}
        save_ledger(ledger_path, ledger)

    return result


# --------------------------------------------------------------- cli

def _collect_customer_ids(args):
    raw = []
    raw.extend(args.customer_id or [])
    if args.customer_ids:
        raw.append(args.customer_ids)
    if args.customers_file:
        raw.extend(read_customers_file(args.customers_file))
    return normalize_customer_ids(raw)


def build_parser():
    parser = argparse.ArgumentParser(
        description="发放华为云 BSS 代金券给子客户/合作伙伴"
                    "（KooCLI hcloud BSS CreatePartnerCoupons，变更类写操作）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（BSS 为全局服务，默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--quota-id", dest="quota_id", required=True,
                        help="代金券额度ID（发放来源；BSS ListQuotaCoupons 可查）")
    parser.add_argument("--customer-id", dest="customer_id", action="append",
                        default=[], help="目标子客户账号ID（可重复传入，批量）")
    parser.add_argument("--customer-ids", dest="customer_ids",
                        help="目标子客户账号ID，逗号分隔（批量）")
    parser.add_argument("--customers-file", dest="customers_file",
                        help="目标子客户账号ID 文件，每行一个（# 注释）")
    parser.add_argument("--face-value", dest="face_value", required=True,
                        help="代金券面值（元，>0，精确到 2 位小数）")
    parser.add_argument("--valid-time", dest="valid_time",
                        help="生效时间 UTC（yyyy-MM-ddTHH:mm:ssZ，可选）")
    parser.add_argument("--expire-time", dest="expire_time",
                        help="失效时间 UTC（yyyy-MM-ddTHH:mm:ssZ，可选）")
    parser.add_argument("--cloud-service-type", dest="cloud_service_type",
                        action="append", default=[],
                        help="允许使用的云服务类型（可重复，最多 10 个，可选）")
    parser.add_argument("--product-id", dest="product_id", action="append",
                        default=[], help="允许使用的产品ID（可重复，可选）")
    parser.add_argument("--memo", help="发放备注（可选）")
    parser.add_argument("--indirect-partner-id", dest="indirect_partner_id",
                        help="云经销商ID（云经销商给子客户发放时必填，可选）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud BSS 操作名（仅允许发放 %s）" % ALLOWED_OPERATION)
    parser.add_argument("--dry-run", action="store_true", dest="dry_run",
                        help="只预览请求，不实际发放")
    parser.add_argument("--confirm", action="store_true",
                        help="确认执行发放（变更类写操作，必需）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整结果")
    parser.add_argument("--no-idempotency", action="store_true",
                        dest="no_idempotency", help="关闭按客户维度的幂等去重")
    parser.add_argument("--force", action="store_true",
                        help="忽略幂等账本，强制重新发放")
    parser.add_argument("--idempotency-window", dest="idempotency_window",
                        type=int, default=DEFAULT_IDEMPOTENCY_WINDOW,
                        help="幂等窗口（秒，默认 %d）" % DEFAULT_IDEMPOTENCY_WINDOW)
    parser.add_argument("--ledger", dest="ledger",
                        help="幂等账本文件（默认 ~/.cache/huawei-cloud-voucher-send/ledger.json）")
    return parser


def _render_human(result):
    lines = []
    if result.get("dry_run"):
        lines.append("DRY-RUN：以下请求不会被执行（发放操作未发生）：")
        lines.append("  hcloud " + " ".join(result.get("command") or []))
        lines.append("  待发放客户（%d）：%s"
                     % (len(result.get("pending") or []),
                        ", ".join(result.get("pending") or [])))
        return "\n".join(lines)
    lines.append("发放完成：成功 %d / 失败 %d / 幂等跳过 %d"
                 % (len(result.get("issued") or []),
                    len(result.get("errors") or []),
                    len(result.get("skipped") or [])))
    for info in result.get("issued") or []:
        lines.append("  + 客户 %s → 代金券 %s"
                     % (info.get("id") or info.get("customer_id"),
                        info.get("coupon_id")))
    for err in result.get("errors") or []:
        lines.append("  x 客户 %s → %s %s"
                     % (err.get("id"), err.get("error_code"),
                        err.get("error_msg")))
    for skip in result.get("skipped") or []:
        lines.append("  = 客户 %s 已在幂等窗口内发放，跳过"
                     % skip.get("customer_id"))
    return "\n".join(lines)


def main(argv=None):
    args = build_parser().parse_args(argv)
    customer_ids = _collect_customer_ids(args)
    try:
        operation = guard_operation(args.operation)
        face_value = parse_face_value(args.face_value)
        valid_time = validate_time(args.valid_time, "valid-time")
        expire_time = validate_time(args.expire_time, "expire-time")
        result = send_coupons(
            args.region, args.quota_id, customer_ids, face_value,
            valid_time=valid_time, expire_time=expire_time,
            cloud_service_types=args.cloud_service_type,
            product_ids=args.product_id, memo=args.memo,
            indirect_partner_id=args.indirect_partner_id,
            operation=operation, dry_run=args.dry_run, confirm=args.confirm,
            use_idempotency=not args.no_idempotency, force=args.force,
            idempotency_window=args.idempotency_window, ledger_path=args.ledger,
        )
    except ConfirmationRequired as exc:
        print("[提示] %s" % exc, file=sys.stderr)
        return 2
    except SendVoucherError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_human(result))
    return 1 if result.get("errors") else 0


if __name__ == "__main__":
    sys.exit(main())