"""
SkillPay Billing SDK — Python
1 USDT = 1000 tokens | 1 call = 1 token | Min deposit 8 USDT

Endpoints:
  POST /billing/charge       — deduct 1 token from user
  GET  /billing/balance      — query user token balance
  POST /billing/payment-link — generate top-up link
"""
import os
import httpx
from dataclasses import dataclass
from typing import Optional

BILLING_URL = "https://skillpay.me/api/v1/billing"

API_KEY: str = os.environ.get(
    "SKILL_BILLING_API_KEY",
    "sk_f6d35052e6659e9a20a240890b42949b9eeb5c3d40305513eec12333f3625b91",
)
SKILL_ID: str = os.environ.get("SKILL_ID", "e9f8947d-02b2-4287-ac49-3fb7df57526b")

_HEADERS = {}

def _get_headers() -> dict:
    return {
        "X-API-Key": os.environ.get("SKILL_BILLING_API_KEY", API_KEY),
        "Content-Type": "application/json",
    }


@dataclass
class ChargeResult:
    ok: bool
    balance: float
    payment_url: Optional[str] = None


async def charge_user(user_id: str) -> ChargeResult:
    """Deduct 1 token from user. Returns ok=False + payment_url if balance is zero."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{BILLING_URL}/charge",
            headers=_get_headers(),
            json={"user_id": user_id, "skill_id": SKILL_ID, "amount": 0.001},
        )
        resp.raise_for_status()
        data = resp.json()
        if data["success"]:
            return ChargeResult(ok=True, balance=data["balance"])
        return ChargeResult(
            ok=False,
            balance=data["balance"],
            payment_url=data.get("payment_url"),
        )


async def get_balance(user_id: str) -> float:
    """Return current token balance for a user."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BILLING_URL}/balance",
            headers=_get_headers(),
            params={"user_id": user_id},
        )
        resp.raise_for_status()
        return resp.json()["balance"]


async def get_payment_link(user_id: str, amount: float = 8.0) -> str:
    """Generate a USDT top-up link for the user. Default minimum is 8 USDT."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{BILLING_URL}/payment-link",
            headers=_get_headers(),
            json={"user_id": user_id, "amount": amount},
        )
        resp.raise_for_status()
        return resp.json()["payment_url"]


# ── Decorator ─────────────────────────────────────────────────────────────────

def require_tokens(func):
    """
    FastAPI route decorator.
    Expects the request to have a query param or header `user_id`.
    Charges 1 token before executing; returns 402 if balance is zero.

    Usage:
        @app.get("/some-endpoint")
        @require_tokens
        async def handler(user_id: str, ...):
            ...
    """
    import functools
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # FastAPI injects `request` if the function requests it, but we grab
        # user_id from kwargs directly — callers must declare `user_id: str`.
        user_id = kwargs.get("user_id") or "anonymous"
        result = await charge_user(user_id)
        if not result.ok:
            return JSONResponse(
                status_code=402,
                content={
                    "error": "Insufficient tokens",
                    "balance": result.balance,
                    "top_up_url": result.payment_url,
                    "message": "Please top up your SkillPay balance to continue. 8 USDT = 8000 calls.",
                },
            )
        return await func(*args, **kwargs)

    return wrapper
