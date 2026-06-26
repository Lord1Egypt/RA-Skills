from __future__ import annotations

import os
import time
import uuid
from typing import Any, Dict, List, Optional

import requests


CHAIN_ALIASES = {
    "bsc": "56",
    "solana": "CT_501",
    "base": "8453",
    "ethereum": "1",
}

STAGE_ALIASES = {
    "new": 10,
    "finalizing": 20,
    "migrated": 30,
}


class BinanceWeb3Error(RuntimeError):
    pass


class BinanceWeb3Client:
    def __init__(self, base_url: Optional[str] = None, timeout_sec: Optional[float] = None) -> None:
        self.base_url = (base_url or os.getenv("BINANCE_WEB3_BASE_URL") or "https://web3.binance.com").rstrip("/")
        self.timeout_sec = timeout_sec or float(os.getenv("BINANCE_HTTP_TIMEOUT_SEC", "12"))
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; MemeRiskRadar/0.1)",
                "Accept": "application/json",
            }
        )
        
        # Configure proxies from environment
        http_proxy = os.getenv("HTTP_PROXY", os.getenv("http_proxy"))
        https_proxy = os.getenv("HTTPS_PROXY", os.getenv("https_proxy"))
        if http_proxy or https_proxy:
            self.session.proxies = {}
            if http_proxy:
                self.session.proxies["http"] = http_proxy
            if https_proxy:
                self.session.proxies["https"] = https_proxy

    def meme_rush_scan(
        self,
        chain_id: str,
        rank_type: int,
        limit: int,
        liquidity_min: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        payload: Dict[str, Any] = {
            "chainId": chain_id,
            "rankType": rank_type,
            "limit": limit,
        }
        if liquidity_min is not None:
            payload["liquidityMin"] = str(liquidity_min)
        data = self._post(
            "/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list",
            payload,
            headers={"Accept-Encoding": "identity"},
        )
        return data.get("data", data.get("tokens", [])) if isinstance(data, dict) else []

    def token_audit(self, chain_id: str, contract_address: str) -> Dict[str, Any]:
        payload = {
            "binanceChainId": chain_id,
            "contractAddress": contract_address,
            "requestId": str(uuid.uuid4()),
        }
        return self._post(
            "/bapi/defi/v1/public/wallet-direct/security/token/audit",
            payload,
            headers={"Accept-Encoding": "identity", "source": "agent"},
        )

    def token_meta(self, chain_id: str, contract_address: str) -> Dict[str, Any]:
        data = self._get(
            "/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/meta/info",
            params={"chainId": chain_id, "contractAddress": contract_address},
            headers={"Accept-Encoding": "identity"},
        )
        return data if isinstance(data, dict) else {}

    def _post(self, path: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        return self._request(
            "post",
            url,
            json=payload,
            headers={"Content-Type": "application/json", **(headers or {})},
        )

    def _get(self, path: str, params: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        return self._request("get", url, params=params, headers=headers or {})

    def _request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        delay = 0.6
        last_error: Optional[Exception] = None
        for attempt in range(3):
            try:
                resp = self.session.request(method, url, timeout=self.timeout_sec, **kwargs)
                return self._unwrap(resp)
            except (requests.Timeout, requests.ConnectionError) as exc:
                last_error = exc
                if attempt == 2:
                    break
                time.sleep(delay)
                delay *= 2
        raise BinanceWeb3Error(str(last_error) if last_error else "binance_request_failed")

    def _unwrap(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code >= 400:
            raise BinanceWeb3Error(f"binance_http_{resp.status_code}: {resp.text[:200]}")
        try:
            payload = resp.json()
        except ValueError as exc:
            raise BinanceWeb3Error("binance_invalid_json") from exc
        if not isinstance(payload, dict):
            raise BinanceWeb3Error("binance_invalid_payload")
        if payload.get("success") is False:
            raise BinanceWeb3Error(f"binance_api_error:{payload.get('code')}")
        data = payload.get("data")
        return data if isinstance(data, dict) else {"data": data}
