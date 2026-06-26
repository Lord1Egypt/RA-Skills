"""Paytm S2S webhook receiver.

See backend-node/webhookHandler.js for the same contract notes - production
expectations are identical (Redis dedup, IP whitelist, 5xx on processing
errors, fast 200 with heavy work queued).
"""
import re
import threading
from collections import deque
from datetime import datetime, timezone
from typing import Any, Optional, Tuple

from paytmchecksum import PaytmChecksum

from paytm_config import get_paytm_config

_seen: set = set()                       # "{orderId}|{status}" - at-least-once dedup
_SEEN_MAX = 50_000
_event_log = deque(maxlen=200)
_lock = threading.Lock()


def recent_events():
    with _lock:
        return list(_event_log)[::-1]


def _extract_body_bytes(raw_body: str) -> Optional[str]:
    """Substring of the raw body that corresponds to "body": {...}.

    Paytm signs those bytes verbatim - re-serializing here would change key
    order / whitespace and break the signature.
    """
    if not raw_body:
        return None
    m = re.search(r'"body"\s*:\s*\{', raw_body)
    if not m:
        return None
    start = m.end() - 1                 # position of the opening '{'
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(raw_body)):
        c = raw_body[i]
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return raw_body[start:i + 1]
    return None


def handle_webhook(raw_body: str, parsed: Any) -> Tuple[int, dict]:
    cfg = get_paytm_config()
    if not cfg["merchant_key"]:
        return 500, {"ok": False, "error": "merchant key not configured"}

    signature = ((parsed or {}).get("head") or {}).get("signature")
    if not signature:
        return 401, {"ok": False, "error": "missing head.signature"}

    body_bytes = _extract_body_bytes(raw_body)
    if body_bytes is None:
        # Fallback - but this is best-effort and may fail signature check.
        import json
        body_bytes = json.dumps((parsed or {}).get("body") or {})

    try:
        signature_ok = PaytmChecksum.verifySignature(body_bytes, cfg["merchant_key"], signature)
    except Exception:
        signature_ok = False
    if not signature_ok:
        return 401, {"ok": False, "error": "invalid signature"}

    # Persist for audit BEFORE dedup so duplicates are visible.
    with _lock:
        _event_log.append({
            "at": datetime.now(timezone.utc).isoformat(),
            "payload": parsed,
        })

    body_obj = (parsed or {}).get("body") or {}
    order_id = body_obj.get("orderId")
    status = body_obj.get("status") or body_obj.get("STATUS")
    dedup_key = f"{order_id or 'unknown'}|{status or 'unknown'}"

    with _lock:
        if dedup_key in _seen:
            return 200, {"ok": True, "dedup": True, "orderId": order_id, "status": status}
        if len(_seen) >= _SEEN_MAX:
            _seen.clear()
        _seen.add(dedup_key)

    _fulfill_order(order_id, status, parsed)
    return 200, {"ok": True, "orderId": order_id, "status": status}


def _fulfill_order(order_id, status, parsed):
    """Replace with your real DB write / queue push. Keep it FAST - webhook
    timeout is 10s; queue heavy work (emails, accounting) if needed."""
    print("[paytm webhook] fulfill stub", {
        "orderId": order_id,
        "status": status,
        "mid": ((parsed or {}).get("body") or {}).get("mid"),
    })
