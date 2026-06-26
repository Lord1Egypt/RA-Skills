"""Paytm merchant config - env-driven, mirrors backend-node/paytmConfig.js."""
import os
from typing import Optional

PROD_PG_DOMAIN = "https://secure.paytmpayments.com"
STAGING_PG_DOMAIN = "https://securestage.paytmpayments.com"


def _strip(v: Optional[str], default: str = "") -> str:
    return (v or default).strip().rstrip("/")


def get_paytm_config() -> dict:
    # Defaults to "staging" so a fresh clone never accidentally points at production.
    env = (os.environ.get("PAYTM_ENVIRONMENT") or "staging").strip().lower()
    default_pg = PROD_PG_DOMAIN if env == "production" else STAGING_PG_DOMAIN
    pg_domain = _strip(os.environ.get("PAYTM_PG_DOMAIN"), default_pg)

    mid = (os.environ.get("PAYTM_MID") or "").strip()
    merchant_key = (os.environ.get("PAYTM_MERCHANT_KEY") or "").strip()
    # Default mirrors PAYTM_ENVIRONMENT - "WEBSTAGING" for staging, "DEFAULT" for prod.
    website_name = (
        os.environ.get("PAYTM_WEBSITE_NAME")
        or ("DEFAULT" if env == "production" else "WEBSTAGING")
    ).strip()
    callback_base = _strip(os.environ.get("PAYTM_CALLBACK_BASE"), "http://localhost:5001")
    callback_url = (os.environ.get("PAYTM_CALLBACK_URL") or "").strip()

    return {
        "pg_domain": pg_domain,
        "mid": mid,
        "merchant_key": merchant_key,
        "website_name": website_name,
        "callback_base": callback_base,
        "callback_url": callback_url,
        "initiate_transaction_url": f"{pg_domain}/theia/api/v1/initiateTransaction",
        "order_status_url": (os.environ.get("PAYTM_STATUS_API_URL") or f"{pg_domain}/v3/order/status").strip(),
        # Subscription endpoint differs between staging (no /theia prefix) and production.
        "subscription_create_url": (
            f"{pg_domain}/theia/api/v1/subscription/create"
            if env == "production"
            else f"{pg_domain}/subscription/create"
        ),
        "link_create_url": f"{pg_domain}/link/create",
        "link_fetch_transaction_url": f"{pg_domain}/link/fetchTransaction",
        "qr_create_url": f"{pg_domain}/paymentservices/qr/create",
        # clientId is per-merchant - issued by Paytm during onboarding. "C11" works for
        # most single-merchant-key setups; override via env if your KAM gave you a different value.
        "client_id": (os.environ.get("PAYTM_CLIENT_ID") or "C11").strip(),
        "checkout_js_loader_url": (
            f"{pg_domain}/merchantpgpui/checkoutjs/merchants/{mid}.js" if mid else ""
        ),
    }
