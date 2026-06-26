"""Flask backend for Paytm JS Checkout - mirrors backend-node/server.js routes.

Endpoints:
  GET  /paytm-client-config.json     mid + loader_url for the browser
  POST /paytm/create-order           initiateTransaction → { orderId, txnToken, amount, mid }
  POST /paytm/order-status           server-side Transaction Status API
  GET|POST /paytm/callback           Paytm browser redirect; verifies CHECKSUMHASH

Run:  PAYTM_MID=... PAYTM_MERCHANT_KEY=... python app.py
"""
import os

from flask import Flask, jsonify, request, send_from_directory

from paytm_config import get_paytm_config
from paytm_service import (
    PaytmError,
    fetch_order_status,
    initiate_transaction,
    verify_callback_checksum,
)
from subscription_service import create_subscription
from payment_link_service import create_payment_link, fetch_link_transactions
from qr_service import create_dynamic_qr
from idempotency import get_cached, set_cached, read_key
from webhook_handler import handle_webhook

app = Flask(__name__, static_folder=None)
# Single source of truth for frontend HTMLs lives at scripts/frontend/. Each
# backend serves it directly to avoid maintaining duplicate copies.
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


def _request_base() -> str:
    proto = (request.headers.get("X-Forwarded-Proto") or request.scheme or "http").split(",")[0].strip()
    host = (request.headers.get("X-Forwarded-Host") or request.host or "localhost").split(",")[0].strip()
    return f"{proto}://{host}"


@app.get("/paytm-client-config.json")
def client_config():
    cfg = get_paytm_config()
    return jsonify({"mid": cfg["mid"], "api_host": cfg["pg_domain"], "loader_url": cfg["checkout_js_loader_url"]})


def _do_create_order(payload):
    return initiate_transaction(
        payload.get("amount"),
        payload.get("custId"),
        _request_base(),
        mobile=payload.get("mobile"),
        email=payload.get("email"),
        order_id=payload.get("orderId"),
    )


def _err_payload(e: PaytmError) -> tuple:
    body = {"error": True, "code": e.code, "message": str(e)}
    if e.order_id: body["orderId"] = e.order_id
    if e.paytm: body["paytm"] = e.paytm
    return jsonify(body), e.http_status


def _with_idempotency(handler):
    """Wrap a create-handler with Idempotency-Key support so double-clicks don't
    produce two Paytm orders. See idempotency.py for the cache contract."""
    def wrapped():
        payload = request.get_json(silent=True) or {}
        key = read_key(request.headers, payload)
        if key:
            cached = get_cached(key)
            if cached:
                status, body = cached
                resp = jsonify(body)
                resp.status_code = status
                resp.headers["Idempotent-Replayed"] = "true"
                return resp
        try:
            body = handler(payload)
            if key:
                set_cached(key, 200, body)
            return jsonify(body)
        except PaytmError as e:
            resp_body = {"error": True, "code": e.code, "message": str(e)}
            if e.order_id: resp_body["orderId"] = e.order_id
            if e.paytm: resp_body["paytm"] = e.paytm
            # Cache only definitive 4xx - never 5xx so retries can succeed.
            if key and 400 <= e.http_status < 500:
                set_cached(key, e.http_status, resp_body)
            return jsonify(resp_body), e.http_status
    wrapped.__name__ = handler.__name__
    return wrapped


def _do_create_subscription(payload):
    return create_subscription(
        amount=payload.get("amount", "2.00"),
        renewal_amount=payload.get("renewalAmount"),
        cust_id=payload.get("custId"),
        mobile=payload.get("mobile"),
        email=payload.get("email"),
        first_name=payload.get("firstName"),
        last_name=payload.get("lastName"),
        frequency=payload.get("frequency", "1"),
        frequency_unit=payload.get("frequencyUnit", "MONTH"),
        amount_type=payload.get("amountType", "FIX"),
        max_amount=payload.get("maxAmount"),
        start_date=payload.get("startDate"),
        expiry_date=payload.get("expiryDate"),
        grace_days=payload.get("graceDays", "3"),
        payment_mode=payload.get("paymentMode", "UNKNOWN"),
        mandate_type=payload.get("mandateType"),
        order_id=payload.get("orderId"),
        server_base_url=_request_base(),
    )


def _do_create_link(payload):
    return create_payment_link(
        amount=payload.get("amount", "1.00"),
        link_name=payload.get("linkName"),
        link_description=payload.get("linkDescription"),
        customer_name=payload.get("customerName"),
            customer_email=payload.get("customerEmail"),
            customer_mobile=payload.get("customerMobile"),
            customer_id=payload.get("customerId"),
        expiry_date=payload.get("expiryDate"),
        order_id=payload.get("orderId"),
        send_sms=payload.get("sendSms", True),
        send_email=payload.get("sendEmail", True),
        callback_url=payload.get("callbackUrl"),
        merchant_unique_reference=payload.get("merchantUniqueReference"),
        server_base_url=_request_base(),
    )


def _do_create_qr(payload):
    return create_dynamic_qr(
        amount=payload.get("amount", "1.00"),
        pos_id=payload.get("posId", "POS001"),
        display_name=payload.get("displayName"),
        expiry_date=payload.get("expiryDate"),
        image_required=payload.get("imageRequired", True),
        order_id=payload.get("orderId"),
    )


# Register all four create endpoints with idempotency support.
app.add_url_rule("/paytm/create-order",        view_func=_with_idempotency(_do_create_order),       methods=["POST"])
app.add_url_rule("/paytm/create-subscription", view_func=_with_idempotency(_do_create_subscription), methods=["POST"])
app.add_url_rule("/paytm/create-link",         view_func=_with_idempotency(_do_create_link),        methods=["POST"])
app.add_url_rule("/paytm/create-qr",           view_func=_with_idempotency(_do_create_qr),          methods=["POST"])


@app.post("/paytm/link-transactions")
def link_transactions():
    """Reconcile a Payment Link via /link/fetchTransaction.

    Use this for Payment Link flows instead of /v3/order/status - the response
    wraps each payer's order under body.orders[].
    """
    payload = request.get_json(silent=True) or {}
    try:
        out = fetch_link_transactions(
            link_id=payload.get("linkId"),
            page_no=payload.get("pageNo", 1),
            page_size=payload.get("pageSize", 10),
            fetch_all_txns=payload.get("fetchAllTxns", True),
        )
        return jsonify(out)
    except PaytmError as e:
        return _err_payload(e)


@app.post("/paytm/webhook")
def webhook():
    """Paytm S2S webhook receiver - verifies head.signature, dedupes,
    applies state transition. See webhook_handler.py for the contract."""
    raw_body = request.get_data(as_text=True)
    parsed = request.get_json(silent=True) or {}
    try:
        status, body = handle_webhook(raw_body, parsed)
        return jsonify(body), status
    except Exception as e:
        # 5xx so Paytm retries - never silently swallow a webhook we couldn't process.
        app.logger.exception("[paytm webhook] handler crash")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/paytm/order-status")
def order_status():
    order_id = (request.get_json(silent=True) or {}).get("orderId")
    if not order_id:
        return jsonify({"error": True, "message": "orderId required"}), 400
    try:
        return app.response_class(fetch_order_status(order_id), mimetype="application/json")
    except PaytmError as e:
        return jsonify({"error": True, "message": str(e)}), e.http_status


def _callback_html(params: dict, ok: bool) -> str:
    # Paytm posts callback fields directly from the user's browser, so EVERY value
    # is untrusted input. HTML-escape before rendering or you've shipped reflected XSS.
    from html import escape
    lines = "\n".join(f"{escape(str(k))}={escape(str(v))}" for k, v in params.items())
    verdict = "OK (signature verified)" if ok else "FAILED or CHECKSUMHASH missing - do not treat as paid"
    return (
        '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Paytm callback</title></head><body>'
        f'<h1>Paytm callback</h1><p><strong>CHECKSUMHASH validation:</strong> {verdict}</p>'
        '<p>Also verify via Transaction Status API (or webhook) before confirming an order.</p>'
        f'<pre>{lines}</pre></body></html>'
    )


@app.route("/paytm/callback", methods=["GET", "POST"])
def callback():
    params = request.form.to_dict() if request.method == "POST" else request.args.to_dict()
    return _callback_html(params, verify_callback_checksum(params)), 200, {"Content-Type": "text/html"}


@app.get("/<path:path>")
def static_files(path):
    return send_from_directory(PUBLIC_DIR, path)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5001)), debug=False)
