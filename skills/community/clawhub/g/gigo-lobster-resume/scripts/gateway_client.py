from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request


class GatewayClient:
    def __init__(self, base_url: str, mock_mode: bool = False, auth_token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.mock_mode = mock_mode
        self.auth_token = auth_token or self._resolve_auth_token()
        self._cached_model: str | None = self._resolve_model_id()

    def check_availability(self) -> bool:
        if self.mock_mode:
            return True
        try:
            payload = self._request_json("/v1/models", timeout=5)
            data = payload.get("data")
            if payload.get("object") == "list" and isinstance(data, list):
                if not self._cached_model and data:
                    self._cached_model = data[0].get("id")
                return True
            return False
        except Exception:
            return False

    def check_lobster(self) -> dict:
        if self.mock_mode:
            return {"id": "mock-lobster", "object": "model"}
        if self._cached_model:
            return {"id": self._cached_model, "object": "model"}

        payload = self._request_json("/v1/models", timeout=5)
        data = payload.get("data") or []
        if not data:
            return {"id": "unknown-lobster", "object": "model"}
        self._cached_model = data[0]["id"]
        return data[0]

    def send_task(self, prompt: str, timeout: int = 300) -> dict:
        if self.mock_mode:
            start = time.perf_counter()
            content = "\n".join(
                [
                    "我会先拆解目标，再给出分步方案。",
                    "随后补充边界条件、验证方式和潜在风险。",
                    f"最后基于题面给出可执行回答：{prompt[:72]}...",
                ]
            )
            elapsed_ms = int((time.perf_counter() - start) * 1000) + 120
            return {
                "content": content,
                "usage": {
                    "prompt_tokens": max(24, len(prompt) // 2),
                    "completion_tokens": max(48, len(content) // 2),
                },
                "elapsed_ms": elapsed_ms,
                "timed_out": False,
                "error": None,
            }

        model = self._cached_model or self.check_lobster().get("id", "unknown-lobster")
        body = json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            self._url("/v1/chat/completions"),
            data=body,
            headers=self._headers({"Content-Type": "application/json"}),
            method="POST",
        )

        start = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=timeout + 10) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return {
                "content": "",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
                "elapsed_ms": int((time.perf_counter() - start) * 1000),
                "timed_out": False,
                "error": f"http_{error.code}",
            }
        except TimeoutError:
            return {
                "content": "",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
                "elapsed_ms": int((time.perf_counter() - start) * 1000),
                "timed_out": True,
                "error": "timeout",
            }
        except Exception as error:
            return {
                "content": "",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
                "elapsed_ms": int((time.perf_counter() - start) * 1000),
                "timed_out": False,
                "error": str(error),
            }

        return {
            "content": payload["choices"][0]["message"]["content"],
            "usage": self._extract_usage(payload),
            "elapsed_ms": int((time.perf_counter() - start) * 1000),
            "timed_out": False,
            "error": None,
        }

    def _extract_usage(self, response_json: dict) -> dict:
        usage = response_json.get("usage") or {}
        return {
            "prompt_tokens": int(usage.get("prompt_tokens", 0)),
            "completion_tokens": int(usage.get("completion_tokens", 0)),
        }

    def _resolve_auth_token(self) -> str | None:
        for env_name in (
            "GIGO_GATEWAY_TOKEN",
            "GIGO_GATEWAY_PASSWORD",
            "OPENCLAW_GATEWAY_TOKEN",
            "OPENCLAW_GATEWAY_PASSWORD",
        ):
            value = os.environ.get(env_name, "").strip()
            if value:
                return value
        return None

    def _resolve_model_id(self) -> str | None:
        for env_name in ("GIGO_GATEWAY_MODEL", "GIGO_MODEL"):
            value = os.environ.get(env_name, "").strip()
            if value:
                return value
        return None

    def _headers(self, extra_headers: dict[str, str] | None = None) -> dict[str, str]:
        headers = dict(extra_headers or {})
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def _url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        if self.base_url.endswith("/v1") and normalized_path.startswith("/v1/"):
            normalized_path = normalized_path[3:]
        return f"{self.base_url}{normalized_path}"

    def _request_json(self, path: str, *, timeout: int, headers: dict[str, str] | None = None) -> dict:
        request = urllib.request.Request(
            self._url(path),
            headers=self._headers(headers),
            method="GET",
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
