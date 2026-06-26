"""
Stripe payment gate (demo / template).

Verifies a one-time payment before unlocking premium skill behavior. Intended as a
minimal reference for in-skill payments: local receipt cache + Stripe Checkout
session lookup by customer email.

Environment (server / skill deployment — do not ask end users for the secret key):

  STRIPE_SECRET_KEY       Stripe secret key (sk_test_... or sk_live_...).
  STRIPE_PAYMENT_LINK_URL Optional. Dashboard Payment Link URL shown to the user.
                          If unset, get_payment_link() returns a clear placeholder.

Flow:

  1. check_payment_status() — valid local receipt?
  2. If not: get_payment_link() — show checkout URL.
  3. User pays, then provides checkout email.
  4. complete_payment_verification(email) — list completed Checkout Sessions,
     match email, require minimum amount, write receipt.

Receipt file: ~/.skill-payment-demo-receipt (JSON + checksum).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import stripe

RECEIPT_PATH = Path.home() / ".skill-payment-demo-receipt"
MIN_AMOUNT_CENTS = 100  # $1.00 — adjust for your product


def _stripe_secret() -> str | None:
    key = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    return key or None


# ---------------------------------------------------------------------------
# Local receipt management
# ---------------------------------------------------------------------------


def _write_receipt(email: str, session_id: str) -> None:
    payload = {
        "email": email,
        "session_id": session_id,
        "ts": int(time.time()),
        "checksum": hashlib.sha256(f"{email}:{session_id}".encode()).hexdigest(),
    }
    RECEIPT_PATH.write_text(json.dumps(payload))


def _read_receipt() -> dict | None:
    if not RECEIPT_PATH.exists():
        return None
    try:
        data = json.loads(RECEIPT_PATH.read_text())
        expected = hashlib.sha256(
            f"{data['email']}:{data['session_id']}".encode()
        ).hexdigest()
        if data.get("checksum") == expected:
            return data
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    return None


# ---------------------------------------------------------------------------
# Payment verification
# ---------------------------------------------------------------------------


def verify_payment_by_email(email: str) -> dict | None:
    """
    Search Stripe Checkout Sessions for a completed payment from this email.
    Returns the matching session dict, or None if not found.
    """
    secret = _stripe_secret()
    if not secret:
        return None
    stripe.api_key = secret

    sessions = stripe.checkout.Session.list(
        status="complete",
        limit=100,
        expand=["data.customer_details"],
    )

    for session in sessions.auto_paging_iter():
        customer_details = session.get("customer_details") or {}
        session_email = (customer_details.get("email") or "").lower().strip()
        if session_email == email.lower().strip():
            amount = session.get("amount_total", 0)
            if amount >= MIN_AMOUNT_CENTS:
                return session
    return None


# ---------------------------------------------------------------------------
# Public API (called from SKILL.md or agents)
# ---------------------------------------------------------------------------


def check_payment_status() -> bool:
    """True if a valid local receipt exists."""
    return _read_receipt() is not None


def get_payment_link() -> str:
    """
    Return the Payment Link URL from STRIPE_PAYMENT_LINK_URL, or a placeholder
    string if not configured (useful for dry runs / docs).
    """
    url = (os.environ.get("STRIPE_PAYMENT_LINK_URL") or "").strip()
    if url:
        return url
    return (
        "[configure STRIPE_PAYMENT_LINK_URL] "
        "Create a Payment Link in the Stripe Dashboard and set this env var."
    )


def complete_payment_verification(email: str) -> bool:
    """Verify via Stripe and write receipt on success."""
    if not _stripe_secret():
        return False
    session = verify_payment_by_email(email)
    if session:
        _write_receipt(email, session["id"])
        return True
    return False


if __name__ == "__main__":
    if not _stripe_secret():
        print(
            "ERROR: STRIPE_SECRET_KEY is not set.\n"
            "Export your test or live secret key before running this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    if check_payment_status():
        print("✓ Payment already verified (receipt found).")
        sys.exit(0)

    link = get_payment_link()
    print(f"Payment required. Complete checkout:\n  {link}\n")
    email = input("After paying, enter the email you used at checkout: ").strip()
    if not email:
        print("No email provided. Exiting.")
        sys.exit(1)

    print("Checking Stripe for your payment...")
    if complete_payment_verification(email):
        print("✓ Payment verified!")
        sys.exit(0)
    print("✗ No matching payment found. Complete payment and try again.")
    sys.exit(1)
