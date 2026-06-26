"""Paytm server-side flow: initiateTransaction, order status, callback verify.

Mirrors backend-node/paytmService.js. Uses Paytm's official `paytmchecksum` package.
"""
import json
import secrets
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional

import requests
from paytmchecksum import PaytmChecksum

from paytm_config import get_paytm_config


class PaytmError(Exception):
    def __init__(self, code: str, message: str, *, http_status: int = 500,
                 order_id: Optional[str] = None, paytm: Optional[dict] = None):
        super().__init__(message)
        self.code = code
        self.http_status = http_status
        self.order_id = order_id
        self.paytm = paytm


_TWO_PLACES = Decimal("0.01")
_FALLBACK_AMT = Decimal("1.00")


def _normalize_amount(amount: Any) -> str:
    """Two-decimal currency normalization using Decimal (avoids binary-float drift).

    Paytm's `txnAmount.value` is a STRING with two decimals, so we serialize
    via Decimal's plain string form. Float arithmetic is never used.
    """
    raw = ("" if amount is None else str(amount)).strip()
    try:
        d = Decimal(raw) if raw else _FALLBACK_AMT
    except Exception:
        d = _FALLBACK_AMT
    if d <= 0:
        d = _FALLBACK_AMT
    return str(d.quantize(_TWO_PLACES, rounding=ROUND_HALF_UP))


def _require_credentials() -> dict:
    cfg = get_paytm_config()
    if not cfg["mid"]:
        raise PaytmError("MISSING_MID", "Missing PAYTM_MID")
    if not cfg["merchant_key"]:
        raise PaytmError("MISSING_MERCHANT_KEY", "Missing PAYTM_MERCHANT_KEY")
    return cfg


def initiate_transaction(
    amount: Any,
    cust_id: Optional[str],
    server_base_url: str,
    mobile: Optional[str] = None,
    email: Optional[str] = None,
    order_id: Optional[str] = None,
) -> dict:
    cfg = _require_credentials()
    # Accept a merchant-supplied orderId for reconciliation; fall back to a random one.
    order_id = (order_id or "").strip() or ("ORD_" + secrets.token_hex(10).upper())
    callback_url = cfg["callback_url"] or f"{server_base_url.rstrip('/')}/paytm/callback"

    user_info = {"custId": (cust_id or "").strip() or "CUST_DEMO"}
    # mobile + email are strongly recommended - pre-fill the consent screen and
    # drive OTP / notifications. Real merchants should always pass these through.
    if mobile and mobile.strip():
        user_info["mobile"] = mobile.strip()
    if email and email.strip():
        user_info["email"] = email.strip()

    body = {
        "requestType": "Payment",
        "mid": cfg["mid"],
        "websiteName": cfg["website_name"],
        "orderId": order_id,
        "callbackUrl": callback_url,
        "txnAmount": {"value": _normalize_amount(amount), "currency": "INR"},
        "userInfo": user_info,
    }
    signature = PaytmChecksum.generateSignature(json.dumps(body), cfg["merchant_key"])
    payload = {"body": body, "head": {"signature": signature}}

    url = f"{cfg['initiate_transaction_url']}?mid={cfg['mid']}&orderId={order_id}"
    r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
    text = r.text
    if not r.ok:
        raise _upstream("INITIATE_HTTP_ERROR", f"initiateTransaction failed (HTTP {r.status_code})", order_id, text)

    data = json.loads(text)
    info = (data.get("body") or {}).get("resultInfo") or {}
    if info.get("resultStatus") != "S":
        raise _upstream("INITIATE_FAILED", info.get("resultMsg") or "initiateTransaction failed", order_id, text)
    txn_token = (data.get("body") or {}).get("txnToken")
    if not txn_token:
        raise _upstream("MISSING_TXN_TOKEN", "Missing txnToken in Paytm response", order_id, text)

    return {
        "orderId": order_id,
        "txnToken": txn_token,
        "amount": body["txnAmount"]["value"],
        "mid": cfg["mid"],
        "tokenType": "TXN_TOKEN",
    }


def fetch_order_status(order_id: str) -> str:
    cfg = _require_credentials()
    body = {"mid": cfg["mid"], "orderId": order_id}
    signature = PaytmChecksum.generateSignature(json.dumps(body), cfg["merchant_key"])
    payload = {"body": body, "head": {"signature": signature}}
    r = requests.post(cfg["order_status_url"], json=payload,
                      headers={"Content-Type": "application/json"}, timeout=15)
    if not r.ok:
        raise PaytmError("STATUS_HTTP_ERROR", f"order status HTTP {r.status_code} - {r.text}",
                         http_status=502, order_id=order_id)
    return r.text


def verify_callback_checksum(params: dict) -> bool:
    cfg = get_paytm_config()
    signature = params.get("CHECKSUMHASH")
    if not signature or not cfg["merchant_key"]:
        return False
    to_verify = {k: v for k, v in params.items() if k != "CHECKSUMHASH"}
    try:
        return PaytmChecksum.verifySignature(to_verify, cfg["merchant_key"], signature)
    except Exception:
        return False


def _upstream(code: str, message: str, order_id: str, raw_body: str) -> PaytmError:
    paytm: dict = {}
    try:
        info = ((json.loads(raw_body) or {}).get("body") or {}).get("resultInfo") or {}
        for k in ("resultStatus", "resultCode", "resultMsg"):
            if info.get(k):
                paytm[k] = info[k]
    except Exception:
        pass
    return PaytmError(code, message, http_status=502, order_id=order_id, paytm=paytm or None)
