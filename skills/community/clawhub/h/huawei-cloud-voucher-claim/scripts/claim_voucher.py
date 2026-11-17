#!/usr/bin/env python3
"""Claim (领取/划拨) Huawei Cloud BSS vouchers / coupons for an enterprise
sub-account, then list the resulting coupon inventory.

Primary execution path is the KooCLI claim operation
``ClaimEnterpriseMultiAccountCoupon`` on service ``BSS`` (the official
*enterprise master -> sub-account coupon transfer* API,
``POST /v2/enterprises/multi-accounts/transfer-coupon``): an enterprise master
account transfers (the sub-account thereby claims) an amount of a designated
coupon to one of its enterprise sub-accounts. When the KooCLI build does not
expose BSS — the current KooCLI reports "Unsupported service: BSS" — or ``hcloud``
is not installed, the script falls back to the official ``huaweicloudsdkbss`` v2
SDK (``BssClient.claim_enterprise_multi_account_coupon``).

After a successful claim the script runs the read-only coupon-list API
(``ListSubCustomerCoupons`` / ``GET /v2/promotions/benefits/coupons``) and prints
the resulting coupon inventory — 券ID / 券码 / 面额 / 余额 / 有效期 / 状态.

This is a **write / mutating** skill: a claim moves money / benefit and is
normally irreversible, therefore

* a live claim requires the explicit ``--confirm`` flag (otherwise the run stops
  with a clear message and only previews the request), and
* ``--dry-run`` previews the exact request without claiming anything.

Idempotency is enforced two ways:

* the API's ``trans_id`` (交易序列号) — when not supplied it is derived
  deterministically from (customer_id, coupon_id, amount), so a retry reuses the
  same serial number and the server rejects a duplicate submission
  (``CBC.99007009``); and
* a local ledger so a retry inside the idempotency window does not even call the
  API again.

Credentials are never handled by this script: the CLI path uses the active
``hcloud`` profile, the SDK path reads the standard Huawei Cloud environment
variables through ``config.py``.

Usage:
    python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \\
        --amount 100.00 --dry-run
    python3 scripts/claim_voucher.py --customer-id CUST001 --coupon-id CP001 \\
        --amount 100.00 --confirm

Environment overrides (mostly for tests):
    VOUCHER_CLAIM_HCLOUD_BIN   hcloud executable (default "hcloud")
    VOUCHER_CLAIM_LEDGER       idempotency ledger path
    VOUCHER_CLAIM_CLI_ARGS     extra args injected before the BSS operation
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
CLAIM_OPERATION = "ClaimEnterpriseMultiAccountCoupon"
LIST_OPERATION = "ListSubCustomerCoupons"

# Accepted (write) operation aliases -> the one real claim operation. The claim
# API is ClaimEnterpriseMultiAccountCoupon; a few plausible synonyms are mapped
# so users are not tripped up by naming, but no other operation is ever executed.
OPERATION_ALIASES = {
    "claimenterprisemultiaccountcoupon": CLAIM_OPERATION,
    "claimenterprisemultiaccountcoupon": CLAIM_OPERATION,
    "transferenterprisemultiaccountcoupon": CLAIM_OPERATION,
    "claimcoupon": CLAIM_OPERATION,
    "claimvoucher": CLAIM_OPERATION,
    "receivecoupon": CLAIM_OPERATION,
    "receivevoucher": CLAIM_OPERATION,
}

DEFAULT_IDEMPOTENCY_WINDOW = 86400  # seconds (24h)
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 100
_DEFAULT_LEDGER = os.path.join(
    os.path.expanduser("~"), ".cache", "huawei-cloud-voucher-claim", "ledger.json"
)

# Human-readable labels for the numeric BSS coupon enumerations.
STATUS_LABELS = {
    1: "UNACTIVATED",
    2: "AVAILABLE",
    3: "USED",
    4: "EXPIRED",
    5: "RECLAIMED",
}

# Response-list keys that may carry the coupon array.
_COUPON_LIST_KEYS = ("user_coupons", "coupons", "coupon_infos", "coupon_list")

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
# KooCLI does not expose a BSS service in the current build: the CLI path is
# then unavailable and the SDK fallback must run (not a hard API error).
_UNSUPPORTED_SERVICE_MARKER = "unsupported service"
# Duplicate transaction serial number (交易事务ID重复): the retry reused a
# trans_id that was already submitted.
_DUPLICATE_TRANS_ID = "cbc.99007009"


class ClaimVoucherError(Exception):
    """Base error for the BSS voucher-claim skill."""


class ConfigError(ClaimVoucherError):
    """hcloud missing / not usable, or credentials not configured."""


class AuthError(ClaimVoucherError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ClaimVoucherError):
    """hcloud / network / unexpected API failure."""


class ValidationError(ConfigError):
    """A required parameter is missing or invalid (config-class error)."""


class ConfirmationRequired(ClaimVoucherError):
    """A live write was attempted without the explicit --confirm flag."""


# --------------------------------------------------------------- validation

def parse_amount(value):
    """Validate a transfer amount and return it as a 2-decimal string.

    The API requires a value > 0 precise to two decimal places. Values with more
    than two decimals are rejected (rather than silently rounded) so the caller
    never transfers an unintended amount.
    """
    if value is None or str(value).strip() == "":
        raise ValidationError("缺少必填参数 --amount（划拨金额，单位：元）。")
    text = str(value).strip()
    try:
        amount = Decimal(text)
    except (InvalidOperation, ValueError):
        raise ValidationError("参数 --amount=%r 非法：必须是大于 0 的数字。" % value)
    if amount <= 0:
        raise ValidationError("参数 --amount=%s 非法：金额必须大于 0。" % text)
    quantized = amount.quantize(Decimal("0.01"))
    if quantized != amount:
        raise ValidationError(
            "参数 --amount=%s 非法：金额只支持精确到小数点后 2 位。" % text)
    return "%.2f" % quantized


def validate_inputs(customer_id, coupon_id, amount):
    """Fail fast on missing / invalid required parameters."""
    if not customer_id or not str(customer_id).strip():
        raise ValidationError(
            "缺少必填参数 --customer-id（企业子账号客户ID；可由企业子账号列表查询）。")
    if not coupon_id or not str(coupon_id).strip():
        raise ValidationError(
            "缺少必填参数 --coupon-id（优惠券ID；可由企业主账号可拨款优惠券列表查询）。")
    # amount validity is enforced by parse_amount when normalised.
    return True


def derive_trans_id(customer_id, coupon_id, amount):
    """Derive a deterministic, globally-unique-enough transaction serial number.

    The API asks for a UUID when the caller supplies ``trans_id``; deriving it
    from the (customer, coupon, amount) triple makes a retry reuse the same
    serial number, so the server rejects the duplicate submission.
    """
    parts = [str(customer_id), str(coupon_id), str(amount)]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:32]


# --------------------------------------------------------------- command build

def normalize_operation(operation):
    """Map an accepted alias to the single real BSS claim operation name."""
    key = re.sub(r"[\s_\-]+", "", str(operation).lower())
    if key in OPERATION_ALIASES:
        return OPERATION_ALIASES[key]
    return operation


def guard_operation(operation):
    """Only the claim-coupon operation may ever be executed."""
    normalized = normalize_operation(operation)
    if normalized != CLAIM_OPERATION:
        raise ValidationError(
            "不允许的操作 %r：本 skill 仅支持领取操作 %s。"
            % (operation, CLAIM_OPERATION))
    return normalized


def build_command(region, customer_id, coupon_id, amount, trans_id=None,
                  operation=CLAIM_OPERATION):
    """Build the KooCLI claim-coupon argv (service BSS, without the executable).

    Mirrors the KooCLI parameter list for ``POST /v2/enterprises/multi-accounts/
    transfer-coupon``: ``--cli-region`` / ``--customer_id`` / ``--coupon_id`` /
    ``--amount`` and the optional ``--trans_id``.
    """
    argv = [
        SERVICE,
        operation,
        "--cli-region=%s" % region,
        "--customer_id=%s" % customer_id,
        "--coupon_id=%s" % coupon_id,
        "--amount=%s" % amount,
    ]
    if trans_id:
        argv.append("--trans_id=%s" % trans_id)
    return argv


def build_list_command(region, coupon_id=None, customer_id=None,
                       limit=DEFAULT_PAGE_SIZE, offset=0,
                       operation=LIST_OPERATION):
    """Build the read-only coupon-list argv used for the post-claim inventory.

    Mirrors the KooCLI parameter list for ``GET /v2/promotions/benefits/
    coupons``: ``--cli-region`` / ``--offset`` / ``--limit`` and the optional
    ``--coupon_id`` (``customer_id`` has no server-side parameter and is applied
    client-side).
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
    return argv


# --------------------------------------------------------------- hcloud run

def _hcloud_executable():
    return os.environ.get("VOUCHER_CLAIM_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("VOUCHER_CLAIM_CLI_ARGS", "").split()
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
    if _UNSUPPORTED_SERVICE_MARKER in low:
        return ConfigError(
            "KooCLI 不支持服务 BSS（Unsupported service）：当前 KooCLI 版本未包含 BSS"
            " 服务，CLI 路径不可用，自动回退到官方 huaweicloudsdkbss v2 SDK。详情：%s"
            % blob[:300]
        )
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：BSS "
            "ClaimEnterpriseMultiAccountCoupon 真实参数清单可通过 KooCLI "
            "`--help`（服务 BSS、operation ClaimEnterpriseMultiAccountCoupon）查看。"
            "详情：%s" % (returncode, blob[:300])
        )
    if _DUPLICATE_TRANS_ID in low or "交易事务ID重复" in blob:
        return ApiError(
            "交易事务ID（trans_id）重复：该领取请求此前已提交，勿重复领取；"
            "请先用券清单确认是否已到账，再决定是否换 trans_id 重试。详情：%s"
            % blob[:300]
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
            "无权限领取代金券，请检查 IAM 权限（403：AK/SK 无效或未授予 BSS "
            "企业多账号领取权限），参见 references/iam-policies.md。详情：%s"
            % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


# --------------------------------------------------------------- response parse

def parse_claim_response(payload):
    """Extract the resulting sub-coupon id from a claim response."""
    if not isinstance(payload, dict):
        return None
    for key in ("sub_coupon_id", "coupon_id", "subCouponId"):
        value = payload.get(key)
        if value:
            return str(value)
    return None


def extract_coupons(payload):
    """Pull the coupon list out of a ListSubCustomerCoupons response."""
    if isinstance(payload, list):
        return payload
    for key in _COUPON_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


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


def filter_coupons(coupons, coupon_id=None, customer_id=None):
    """Client-side filter by coupon id / customer id (case-insensitive)."""
    result = []
    want_coupon = str(coupon_id).strip().lower() if coupon_id else None
    want_customer = str(customer_id).strip().lower() if customer_id else None
    for coupon in coupons:
        if not isinstance(coupon, dict):
            continue
        if want_coupon:
            hay = " ".join(str(coupon.get(f) or "")
                           for f in ("coupon_id", "coupon_code", "sub_coupon_id")).lower()
            if want_coupon not in hay:
                continue
        if want_customer:
            if str(coupon.get("customer_id") or "").strip().lower() != want_customer:
                continue
        result.append(coupon)
    return result


# --------------------------------------------------------------- SDK fallback

def claim_via_sdk(region, customer_id, coupon_id, amount, trans_id=None):
    """SDK fallback: claim a coupon through ``huaweicloudsdkbss`` v2.

    Only invoked when hcloud is not installed. BSS is a *global* service, so the
    official client uses ``GlobalCredentials`` + ``with_endpoints``. Credentials
    come from the standard environment variables via ``config.load_ak_sk``.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkbss.v2 import BssClient, \
            ClaimEnterpriseMultiAccountCouponRequest, \
            TransferEnterpriseMultiAccountCouponReq
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
            "变量，且当前环境未检测到 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 这两个"
            "环境变量（只按精确变量名读取这两个值，不扫描其它环境变量）。"
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

    body = TransferEnterpriseMultiAccountCouponReq(
        customer_id=customer_id,
        coupon_id=coupon_id,
        amount=str(amount),
        trans_id=trans_id,
    )
    request = ClaimEnterpriseMultiAccountCouponRequest(body=body)
    try:
        response = client.claim_enterprise_multi_account_coupon(request)
    except Exception as exc:
        low = str(exc).lower()
        if _DUPLICATE_TRANS_ID in low or "交易事务ID重复" in str(exc):
            raise ApiError(
                "交易事务ID（trans_id）重复：该领取请求此前已提交，勿重复领取。"
                "详情：%s" % str(exc)[:300])
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限领取代金券，请检查 IAM 权限（403）。详情：%s"
                % str(exc)[:300])
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
    return _model_to_dict(response)


def list_via_sdk(region, coupon_id=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback for the post-claim coupon list (``huaweicloudsdkbss`` v2)."""
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkbss.v2 import BssClient, ListSubCustomerCouponsRequest
    except ImportError as exc:
        raise ConfigError(
            "SDK 回退缺少 huaweicloudsdkcore/huaweicloudsdkbss，无法查询券清单。"
            "详情：%s" % exc
        )
    ak, sk = load_ak_sk()
    if not ak or not sk:
        raise ConfigError("SDK 回退缺少 AK/SK 凭证，无法查询券清单。")
    credentials = GlobalCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    client = BssClient.new_builder() \
        .with_credentials(credentials) \
        .with_http_config(build_http_config()) \
        .with_endpoints([BSS_ENDPOINT]) \
        .build()
    coupons = []
    offset = 0
    for _ in range(max_pages):
        request = ListSubCustomerCouponsRequest(
            coupon_id=coupon_id, offset=offset, limit=min(limit, MAX_PAGE_SIZE))
        response = client.list_sub_customer_coupons(request)
        batch = list(getattr(response, "user_coupons", None) or [])
        coupons.extend(_model_to_dict(item) for item in batch)
        total = getattr(response, "count", None)
        if total is not None and len(coupons) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    return coupons


# --------------------------------------------------------------- list (read-only)

def _total_count(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("count", "total_count", "totalCount", "total"):
        if isinstance(payload.get(key), int):
            return payload[key]
    return None


def list_claimed_coupons(region, coupon_id=None, customer_id=None,
                         limit=DEFAULT_PAGE_SIZE, max_pages=100,
                         list_operation=LIST_OPERATION):
    """Query coupons (paged) to build the post-claim inventory.

    KooCLI first, SDK fallback. ``coupon_id`` is forwarded server-side;
    ``customer_id`` has no server-side parameter and is applied client-side.
    """
    coupons = []
    offset = 0
    used_cli = False
    for _page in range(max_pages):
        argv = build_list_command(region, coupon_id=coupon_id, limit=limit,
                                  offset=offset, operation=list_operation)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except (ConfigError, ApiError):
            coupons = list_via_sdk(region, coupon_id=coupon_id, limit=limit,
                                   max_pages=max_pages)
            used_cli = False
            break
        used_cli = True
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            err = classify_hcloud_failure(stdout, stderr, returncode)
            if isinstance(err, ConfigError):
                coupons = list_via_sdk(region, coupon_id=coupon_id, limit=limit,
                                       max_pages=max_pages)
                used_cli = False
                break
            raise err
        payload = extract_json(stdout)
        batch = extract_coupons(payload)
        coupons.extend(batch)
        total = _total_count(payload)
        if total is not None and len(coupons) >= total:
            break
        if not batch or len(batch) < limit:
            break
        offset += len(batch)
    return filter_coupons(coupons, coupon_id=coupon_id,
                          customer_id=customer_id), used_cli


# --------------------------------------------------------------- idempotency

def idempotency_key(customer_id, coupon_id, amount):
    """Stable natural key for the idempotency ledger."""
    parts = [str(customer_id), str(coupon_id), str(amount)]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:32]


def _ledger_path(explicit=None):
    return explicit or os.environ.get("VOUCHER_CLAIM_LEDGER") or _DEFAULT_LEDGER


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

def claim_voucher(region, customer_id, coupon_id, amount, *,
                  trans_id=None, operation=CLAIM_OPERATION,
                  dry_run=False, confirm=False,
                  list_after=True, list_limit=DEFAULT_PAGE_SIZE,
                  use_idempotency=True, force=False,
                  idempotency_window=DEFAULT_IDEMPOTENCY_WINDOW, ledger_path=None):
    """Claim a coupon and (optionally) list the resulting coupon inventory.

    Returns a dict with ``claimed`` / ``sub_coupon_id`` / ``skipped`` /
    ``coupons`` / ``dry_run`` / ``command``. Raises on config / auth / API errors.
    """
    validate_inputs(customer_id, coupon_id, amount)

    key = idempotency_key(customer_id, coupon_id, amount)
    effective_trans_id = trans_id or derive_trans_id(customer_id, coupon_id, amount)

    command = build_command(
        region, customer_id, coupon_id, amount,
        trans_id=effective_trans_id, operation=operation)

    result = {
        "customer_id": customer_id,
        "coupon_id": coupon_id,
        "amount": amount,
        "trans_id": effective_trans_id,
        "claimed": False,
        "sub_coupon_id": None,
        "skipped": False,
        "coupons": [],
        "list_used_cli": None,
        "dry_run": bool(dry_run),
        "command": command if dry_run else None,
    }

    if use_idempotency and not force:
        ledger_path = _ledger_path(ledger_path)
        ledger = load_ledger(ledger_path, window=idempotency_window)
        if key in ledger:
            result["skipped"] = True
            result["reason"] = "already_claimed_in_window"
            result["sub_coupon_id"] = ledger[key].get("sub_coupon_id")
            return result
    else:
        ledger_path = _ledger_path(ledger_path) if use_idempotency else None
        ledger = load_ledger(ledger_path, window=idempotency_window) \
            if (use_idempotency and ledger_path) else {}

    if dry_run:
        result["reason"] = "dry_run_preview"
        return result

    if not confirm:
        raise ConfirmationRequired(
            "领取代金券是变更类写操作（涉及资金/权益、不可逆）。请确认后加 --confirm "
            "执行，或先用 --dry-run 预览请求。")

    # ---- live claim: CLI first, SDK fallback ----
    try:
        stdout, stderr, returncode = run_hcloud(command)
    except ConfigError:
        payload = claim_via_sdk(
            region, customer_id, coupon_id, amount, trans_id=effective_trans_id)
    else:
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            err = classify_hcloud_failure(stdout, stderr, returncode)
            if isinstance(err, ConfigError):
                # CLI unavailable (e.g. KooCLI has no BSS service) -> SDK fallback
                payload = claim_via_sdk(
                    region, customer_id, coupon_id, amount,
                    trans_id=effective_trans_id)
            else:
                raise err
        else:
            payload = extract_json(stdout)

    sub_coupon_id = parse_claim_response(payload)
    result["claimed"] = True
    result["sub_coupon_id"] = sub_coupon_id

    if use_idempotency and ledger_path:
        ledger[key] = {"at": time.time(), "sub_coupon_id": sub_coupon_id}
        save_ledger(ledger_path, ledger)

    if list_after:
        coupons, used_cli = list_claimed_coupons(
            region, coupon_id=coupon_id, customer_id=customer_id,
            limit=list_limit)
        result["coupons"] = coupons
        result["list_used_cli"] = used_cli
    return result


# --------------------------------------------------------------- rendering

def _status_text(value):
    if value is None:
        return "-"
    if isinstance(value, int):
        label = STATUS_LABELS.get(value)
        return "%s(%s)" % (label, value) if label else str(value)
    try:
        as_int = int(value)
    except (TypeError, ValueError):
        return str(value)
    label = STATUS_LABELS.get(as_int)
    return "%s(%s)" % (label, as_int) if label else str(value)


def _field(coupon, *names, default="-"):
    for name in names:
        if coupon.get(name) not in (None, ""):
            return coupon[name]
    return default


def render_coupon_table(coupons):
    """Render the claimed-coupon inventory (券ID/券码/面额/余额/有效期/状态)."""
    columns = ["券ID(coupon_id)", "券码(coupon_code)", "面额(face_value)",
               "余额(balance)", "生效(valid_time)", "失效(expire_time)",
               "状态(status)"]
    rows = []
    for coupon in coupons:
        rows.append([
            str(_field(coupon, "coupon_id", "sub_coupon_id")),
            str(_field(coupon, "coupon_code")),
            str(_field(coupon, "face_value")),
            str(_field(coupon, "balance")),
            str(_field(coupon, "active_time", "valid_time")),
            str(_field(coupon, "expire_time")),
            _status_text(coupon.get("status")),
        ])
    if not rows:
        rows = [["-"] * len(columns)]
    widths = [max(len(columns[i]), *(len(r[i]) for r in rows))
              for i in range(len(columns))]
    lines = ["  ".join(columns[i].ljust(widths[i]) for i in range(len(columns))),
             "  ".join("-" * w for w in widths)]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def _render_human(result):
    lines = []
    if result.get("dry_run"):
        lines.append("DRY-RUN：以下请求不会被执行（领取操作未发生）：")
        lines.append("  hcloud " + " ".join(result.get("command") or []))
        lines.append("  交易序列号 trans_id=%s（重试复用同一值，服务端去重）"
                     % result.get("trans_id"))
        return "\n".join(lines)
    if result.get("skipped"):
        lines.append("幂等跳过：客户 %s 的券 %s（金额 %s）已在幂等窗口内领取过，"
                     "未重复调用 API。" % (result.get("customer_id"),
                                      result.get("coupon_id"),
                                      result.get("amount")))
        if result.get("sub_coupon_id"):
            lines.append("  上次返回子券 sub_coupon_id=%s" % result["sub_coupon_id"])
        return "\n".join(lines)
    lines.append("领取完成：客户 %s ← 券 %s（金额 %s）"
                 % (result.get("customer_id"), result.get("coupon_id"),
                    result.get("amount")))
    if result.get("sub_coupon_id"):
        lines.append("  返回子券 sub_coupon_id=%s" % result["sub_coupon_id"])
    if result.get("coupons"):
        lines.append("")
        lines.append("领取后代金券清单（券ID/券码/面额/余额/有效期/状态）：")
        lines.append(render_coupon_table(result["coupons"]))
    elif result.get("list_after") is False:
        lines.append("  （已跳过领取清单查询）")
    else:
        lines.append("  未查询到该客户/该券的券清单记录。")
    return "\n".join(lines)


# --------------------------------------------------------------- cli

def build_parser():
    parser = argparse.ArgumentParser(
        description="领取（企业主账号向子账号划拨）华为云 BSS 代金券，"
                    "并列出领取结果（KooCLI 服务 BSS / "
                    "ClaimEnterpriseMultiAccountCoupon，变更类写操作）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（BSS 为全局服务，默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--customer-id", dest="customer_id", required=True,
                        help="企业子账号客户ID（领取目标）")
    parser.add_argument("--coupon-id", dest="coupon_id", required=True,
                        help="优惠券ID（领取来源）")
    parser.add_argument("--amount", required=True,
                        help="划拨金额（元，>0，精确到 2 位小数）")
    parser.add_argument("--trans-id", dest="trans_id",
                        help="交易序列号（防止重复提交；缺省按客户/券/金额确定性生成）")
    parser.add_argument("--operation", default=CLAIM_OPERATION,
                        help="KooCLI BSS 操作名（仅允许领取 %s）" % CLAIM_OPERATION)
    parser.add_argument("--dry-run", action="store_true", dest="dry_run",
                        help="只预览请求，不实际领取（默认行为：无 --confirm 时只预览）")
    parser.add_argument("--confirm", action="store_true",
                        help="确认执行领取（变更类写操作，必需）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整结果")
    parser.add_argument("--no-list", action="store_true", dest="no_list",
                        help="领取后不查询代金券清单")
    parser.add_argument("--list-limit", dest="list_limit", type=int,
                        default=DEFAULT_PAGE_SIZE,
                        help="领取清单分页大小（BSS 上限 %d，默认 %d）"
                             % (MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE))
    parser.add_argument("--no-idempotency", action="store_true",
                        dest="no_idempotency", help="关闭幂等去重")
    parser.add_argument("--force", action="store_true",
                        help="忽略幂等账本，强制重新领取")
    parser.add_argument("--idempotency-window", dest="idempotency_window",
                        type=int, default=DEFAULT_IDEMPOTENCY_WINDOW,
                        help="幂等窗口（秒，默认 %d）" % DEFAULT_IDEMPOTENCY_WINDOW)
    parser.add_argument("--ledger", dest="ledger",
                        help="幂等账本文件（默认 ~/.cache/huawei-cloud-voucher-claim/ledger.json）")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        operation = guard_operation(args.operation)
        amount = parse_amount(args.amount)
        result = claim_voucher(
            args.region, args.customer_id, args.coupon_id, amount,
            trans_id=args.trans_id, operation=operation,
            dry_run=args.dry_run, confirm=args.confirm,
            list_after=not args.no_list,
            list_limit=min(max(args.list_limit, 1), MAX_PAGE_SIZE),
            use_idempotency=not args.no_idempotency, force=args.force,
            idempotency_window=args.idempotency_window, ledger_path=args.ledger,
        )
    except ConfirmationRequired as exc:
        print("[提示] %s" % exc, file=sys.stderr)
        return 2
    except ClaimVoucherError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    result["list_after"] = not args.no_list
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())