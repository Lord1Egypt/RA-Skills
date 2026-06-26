from __future__ import annotations

import os
import time
from dataclasses import asdict, dataclass
from typing import Dict, Optional

import requests


class BillingError(RuntimeError):
    pass


@dataclass
class BillingResult:
    ok: bool
    code: str
    message: str
    provider_ref: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class BillingClient:
    def charge(self, call_name: str, amount_usdt: str, user_ref: str, idempotency_key: str) -> BillingResult:
        raise NotImplementedError


class NoopBillingClient(BillingClient):
    def charge(self, call_name: str, amount_usdt: str, user_ref: str, idempotency_key: str) -> BillingResult:
        return BillingResult(ok=True, code="noop", message="noop billing accepted", provider_ref="noop")


class SkillPayBillingClient(BillingClient):
    def __init__(self, api_key: str, skill_id: str, billing_url: Optional[str] = None, price_usdt: Optional[str] = None) -> None:
        self.api_key = api_key
        self.skill_id = skill_id
        self.billing_url = billing_url or os.getenv("SKILLPAY_BILLING_URL", "https://skillpay.me/api/v1/billing")
        self.price_usdt = price_usdt or os.getenv("SKILLPAY_PRICE_USDT", "0.002")
        self.session = requests.Session()
        
        # Configure proxies from environment
        http_proxy = os.getenv("HTTP_PROXY", os.getenv("http_proxy"))
        https_proxy = os.getenv("HTTPS_PROXY", os.getenv("https_proxy"))
        if http_proxy or https_proxy:
            self.session.proxies = {}
            if http_proxy:
                self.session.proxies["http"] = http_proxy
            if https_proxy:
                self.session.proxies["https"] = https_proxy

    def charge(self, call_name: str, amount_usdt: str, user_ref: str, idempotency_key: str) -> BillingResult:
        # SkillPay API v1 format
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        
        # Use configured price (in USDT)
        payload = {
            "user_id": user_ref,
            "skill_id": self.skill_id,
            "amount": float(self.price_usdt),  # USDT per call
        }

        delay = 0.8
        for attempt in range(3):
            try:
                resp = self.session.post(f"{self.billing_url}/charge", json=payload, headers=headers, timeout=12)
                
                if resp.status_code >= 500:
                    raise BillingError(f"skillpay_server_{resp.status_code}")
                
                if resp.status_code >= 400:
                    try:
                        error_data = resp.json()
                        return BillingResult(ok=False, code=f"http_{resp.status_code}", message=error_data.get("error", resp.text[:200]))
                    except:
                        return BillingResult(ok=False, code=f"http_{resp.status_code}", message=resp.text[:200])

                data = {}
                try:
                    data = resp.json()
                except ValueError:
                    return BillingResult(ok=False, code="invalid_json", message="invalid response")

                if data.get("success"):
                    return BillingResult(
                        ok=True, 
                        code="charged", 
                        message="charge accepted", 
                        provider_ref=str(data.get("balance", 0))
                    )
                else:
                    # Balance insufficient, return payment URL
                    payment_url = data.get("payment_url")
                    if payment_url:
                        return BillingResult(
                            ok=False,
                            code="insufficient_balance",
                            message="insufficient balance",
                            provider_ref=payment_url
                        )
                    return BillingResult(
                        ok=False,
                        code="charge_failed",
                        message=data.get("error", "charge failed")
                    )

            except (requests.Timeout, requests.ConnectionError, BillingError) as exc:
                if attempt == 2:
                    return BillingResult(ok=False, code="network_error", message=str(exc))
                time.sleep(delay)
                delay *= 2

        return BillingResult(ok=False, code="unknown", message="billing failed")


def build_billing_client() -> BillingClient:
    mode = os.getenv("SKILLPAY_BILLING_MODE", "skillpay").strip().lower()
    if mode == "noop":
        return NoopBillingClient()

    api_key = os.getenv("SKILL_BILLING_API_KEY", "").strip()
    if not api_key:
        raise BillingError("missing_skillpay_apikey")
    
    skill_id = os.getenv("SKILL_ID", "").strip()
    if not skill_id:
        raise BillingError("missing_skill_id")
    
    billing_url = os.getenv("SKILLPAY_BILLING_URL", "")
    price_usdt = os.getenv("SKILLPAY_PRICE_USDT", "0.002")
    
    return SkillPayBillingClient(api_key=api_key, skill_id=skill_id, billing_url=billing_url, price_usdt=price_usdt)
