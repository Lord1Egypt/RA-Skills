from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json as jsonlib
import time
import uuid
from typing import Any

import requests

from .config import BridgeConfig
from .models import IncomingMessage, OutboundCommand


@dataclass
class BridgeClient:
    config: BridgeConfig

    def __post_init__(self) -> None:
        self._session = requests.Session()
        self._max_retries = 2

    def _headers(self) -> dict[str, str]:
        return self._headers_for_payload(None)

    def _headers_for_payload(self, payload: dict[str, Any] | None, override_secret: str | None = None) -> dict[str, str]:
        secret = override_secret or self.config.shared_secret
        timestamp = str(int(time.time()))
        headers: dict[str, str] = {
            "x-bridge-ts": timestamp,
            "x-bridge-nonce": uuid.uuid4().hex,
            "content-type": "application/json",
        }
        if self.config.auth_mode == "hmac":
            payload_text = _stable_json(payload)
            raw = f"{timestamp}.{payload_text}".encode("utf-8")
            signature = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()
            headers["x-bridge-signature"] = signature
        else:
            headers["Authorization"] = f"Bearer {secret}"
        return headers

    def post_event(self, event: IncomingMessage) -> dict[str, Any]:
        url = f"{self.config.base_url}/api/v1/sidecar/events"
        response = self._request(
            method="POST",
            url=url,
            json=event.to_bridge_payload(),
        )
        return response.json()

    def claim_commands(self, sidecar_id: str, limit: int) -> list[OutboundCommand]:
        url = f"{self.config.base_url}/api/v1/sidecar/commands/claim"
        response = self._request(
            method="POST",
            url=url,
            json={"sidecarId": sidecar_id, "limit": limit},
        )
        payload = response.json()
        commands_raw = payload.get("commands", [])
        return [OutboundCommand.model_validate(item) for item in commands_raw]

    def ack_command(
        self,
        command_id: str,
        sidecar_id: str,
        status: str,
        error_code: str | None = None,
        error_message: str | None = None,
    ) -> dict[str, Any]:
        url = f"{self.config.base_url}/api/v1/sidecar/commands/{command_id}/ack"
        body: dict[str, Any] = {
            "sidecarId": sidecar_id,
            "status": status,
        }
        if error_code:
            body["errorCode"] = error_code
        if error_message:
            body["errorMessage"] = error_message

        response = self._request(
            method="POST",
            url=url,
            json=body,
        )
        return response.json()

    def health(self) -> dict[str, Any]:
        url = f"{self.config.base_url}/health"
        response = self._request(method="GET", url=url)
        return response.json()

    def heartbeat(
        self,
        sidecar_id: str,
        adapter_name: str,
        adapter_ok: bool,
        detail: str | None = None,
        groups: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.config.base_url}/api/v1/sidecar/heartbeat"
        response = self._request(
            method="POST",
            url=url,
            json={
                "sidecarId": sidecar_id,
                "adapterName": adapter_name,
                "adapterOk": adapter_ok,
                "detail": detail,
                "groups": groups or [],
            },
        )
        return response.json()

    def forward_bhmailer_webhook(self, payload: dict[str, Any], secret: str | None = None) -> dict[str, Any]:
        url = f"{self.config.base_url}/api/v1/bhmailer/webhook"
        response = self._request(
            method="POST",
            url=url,
            json=payload,
            override_secret=secret,
        )
        return response.json()

    def _request(
        self,
        method: str,
        url: str,
        json: dict[str, Any] | None = None,
        override_secret: str | None = None,
    ) -> requests.Response:
        attempts = 0
        while True:
            attempts += 1
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    json=json,
                    headers=self._headers_for_payload(json, override_secret=override_secret),
                    timeout=self.config.request_timeout_sec,
                )
                if response.status_code >= 500 and attempts <= self._max_retries:
                    time.sleep(0.2 * attempts)
                    continue
                response.raise_for_status()
                return response
            except requests.HTTPError as error:
                status = error.response.status_code if error.response is not None else None
                if status is not None and status < 500:
                    raise
                if attempts > self._max_retries:
                    raise
                time.sleep(0.2 * attempts)
            except requests.RequestException:
                if attempts > self._max_retries:
                    raise
                time.sleep(0.2 * attempts)


def _stable_json(payload: dict[str, Any] | None) -> str:
    if payload is None:
        return ""
    return jsonlib.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
