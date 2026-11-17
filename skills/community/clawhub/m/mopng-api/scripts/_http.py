#!/usr/bin/env python3
"""Shared stdlib-only JSON transport used by the MoPNG CLI entry points.

``mopng_api.py`` and ``mopng_agent.py`` talk to different hosts with different
auth headers, but the request/response handling is the same: build the URL,
serialise the body, map transport failures to ``RuntimeError`` and parse JSON.
Keeping it here means both entry points share one error vocabulary.
"""

from __future__ import annotations

import json
import mimetypes
import uuid
from urllib import error, request


class JsonHttpClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        timeout: float = 90,
        service: str = "MoPNG API",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers)
        self.timeout = timeout
        self.service = service

    def build_headers(self, data: dict | None, files: dict | None) -> dict[str, str]:
        """Extra headers for the body kind (JSON none/multipart)."""
        return dict(self.headers)

    def build_body(self, data: dict | None, files: dict | None) -> bytes | None:
        """Wire body plus the headers it needs; None means no body."""
        if files:
            # Multipart form data
            boundary = f"----OpenClaw{uuid.uuid4().hex}"
            body = bytearray()

            for k, v in (data or {}).items():
                body.extend(f"--{boundary}\r\n".encode())
                body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
                body.extend(str(v).encode())
                body.extend(b"\r\n")

            for field_name, (file_path, file_data) in files.items():
                mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
                body.extend(f"--{boundary}\r\n".encode())
                body.extend(
                    f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'.encode()
                )
                body.extend(f"Content-Type: {mime}\r\n\r\n".encode())
                body.extend(file_data)
                body.extend(b"\r\n")

            body.extend(f"--{boundary}--\r\n".encode())
            self.headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
            return bytes(body)

        if data is not None:
            self.headers["Content-Type"] = "application/json"
            return json.dumps(data).encode()

        return None

    def describe_http_error(self, status: int, body: str) -> str:
        """Error text for a non-2xx response."""
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            return f"HTTP {status}: {body}"
        message = parsed.get("message", body) if isinstance(parsed, dict) else body
        return f"API error: {message}"

    def parse_response(self, raw: str) -> dict:
        """Parse a successful response body."""
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{self.service} returned non-JSON data") from exc
        if not isinstance(parsed, dict):
            return {"data": parsed}
        return parsed

    def request(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        files: dict | None = None,
    ) -> dict:
        body = self.build_body(data, files)
        req = request.Request(
            f"{self.base_url}{path}",
            method=method,
            data=body,
            headers=self.build_headers(data, files),
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310 — URL is fixed API host + path
                raw = resp.read().decode("utf-8", "replace")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            raise RuntimeError(f"{self.service} {self.describe_http_error(exc.code, detail)}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"{self.service} unavailable: {exc.reason}") from exc
        return self.parse_response(raw)