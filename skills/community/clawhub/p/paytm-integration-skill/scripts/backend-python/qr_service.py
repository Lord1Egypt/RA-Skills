"""Create Dynamic QR - POST /paymentservices/qr/create.

Doc: https://www.paytmpayments.com/docs/api/create-qr-code-api
Defaults & gotchas baked in:
- posId is REQUIRED (omitting it returns 400)
- amount must be a STRING with two decimals
- head requires clientId + version + signature
- Response `image` is RAW base64 - we prepend `data:image/png;base64,` here so
  the frontend can drop it straight into <img src>.
"""
import json
import secrets
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional

import requests
from paytmchecksum import PaytmChecksum

from paytm_config import get_paytm_config
from paytm_service import PaytmError


_TWO_PLACES = Decimal("0.01")
_FALLBACK = Decimal("1.00")


def _normalize_amount(amount: Any) -> str:
    """Two-decimal currency normalization using Decimal (avoids binary-float drift).

    Paytm QR API takes `amount` as a STRING with two decimals.
    """
    raw = ("" if amount is None else str(amount)).strip()
    try:
        d = Decimal(raw) if raw else _FALLBACK
    except Exception:
        d = _FALLBACK
    if d <= 0:
        d = _FALLBACK
    return str(d.quantize(_TWO_PLACES, rounding=ROUND_HALF_UP))


def create_dynamic_qr(
    *,
    amount: Any = "1.00",
    pos_id: str = "POS001",
    display_name: Optional[str] = None,
    expiry_date: Optional[str] = None,
    image_required: bool = True,
    order_id: Optional[str] = None,
) -> dict:
    cfg = get_paytm_config()
    if not cfg["mid"]:
        raise PaytmError("MISSING_MID", "Missing PAYTM_MID")
    if not cfg["merchant_key"]:
        raise PaytmError("MISSING_MERCHANT_KEY", "Missing PAYTM_MERCHANT_KEY")
    if not pos_id or not str(pos_id).strip():
        raise PaytmError("MISSING_POS_ID",
                         "posId is required for QR creation (Paytm returns 400 without it)")

    order_id = (order_id or "").strip() or ("QR_" + secrets.token_hex(10).upper())

    body: dict = {
        "mid": cfg["mid"],
        "orderId": order_id,
        "amount": _normalize_amount(amount),
        "businessType": "UPI_QR_CODE",
        "posId": str(pos_id).strip(),
        "imageRequired": bool(image_required),
    }
    if display_name and display_name.strip():
        body["displayName"] = display_name.strip()[:30]
    if expiry_date and expiry_date.strip():
        body["expiryDate"] = expiry_date.strip()

    signature = PaytmChecksum.generateSignature(json.dumps(body), cfg["merchant_key"])
    head = {
        "clientId": cfg["client_id"],
        "version": "v1",
        "signature": signature,
    }

    r = requests.post(cfg["qr_create_url"], json={"head": head, "body": body},
                      headers={"Content-Type": "application/json"}, timeout=15)
    text = r.text
    if not r.ok:
        raise _upstream("QR_HTTP_ERROR", f"qr/create HTTP {r.status_code}", order_id, text)

    data = json.loads(text)
    info = (data.get("body") or {}).get("resultInfo") or {}
    status = info.get("resultStatus")
    if status and status not in ("SUCCESS", "S"):
        raise _upstream("QR_FAILED", info.get("resultMsg") or "qr/create failed", order_id, text)

    body_resp = data.get("body") or {}
    raw_image = body_resp.get("image")
    image = f"data:image/png;base64,{raw_image}" if raw_image else None

    return {
        "orderId": order_id,
        "qrCodeId": body_resp.get("qrCodeId"),
        "qrData": body_resp.get("qrData"),
        "image": image,
        "mid": cfg["mid"],
    }


def _upstream(code: str, message: str, order_id: str, raw: str) -> PaytmError:
    paytm: dict = {}
    try:
        info = ((json.loads(raw) or {}).get("body") or {}).get("resultInfo") or {}
        for k in ("resultStatus", "resultCode", "resultMsg"):
            if info.get(k):
                paytm[k] = info[k]
    except Exception:
        pass
    return PaytmError(code, message, http_status=502, order_id=order_id, paytm=paytm or None)
