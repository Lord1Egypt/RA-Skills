from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx


DEFAULT_BASE_URL = "https://ppt.mustgoai.com"
TERMINAL_FAILURE_STATES = {
    "failed",
    "error",
    "content_blocked",
    "quota_exceeded",
    "cancelled",
    "expired",
}


class GoAIError(RuntimeError):
    pass


def print_error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)


def print_warning(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def content_type_for_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    if suffix == ".gif":
        return "image/gif"
    if suffix == ".pdf":
        return "application/pdf"
    raise GoAIError(f"unsupported file type: {path}")


class GoAIClient:
    def __init__(self, skill_name: str) -> None:
        self.skill_name = skill_name
        self.base_url = os.environ.get("GOAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self.api_key = os.environ.get("GOAI_API_KEY", "")
        self.last_payload: dict[str, Any] | None = None
        self.last_media_url = ""
        self._http = httpx.Client(
            timeout=httpx.Timeout(60.0, connect=20.0),
            follow_redirects=True,
        )

    def close(self) -> None:
        self._http.close()

    def require_api_key(self) -> None:
        if self.api_key.strip():
            return

        home = Path(os.environ.get("USERPROFILE") or Path.home())
        config_path = home / ".openclaw" / "openclaw.json"
        raise GoAIError(
            "\n".join(
                [
                    "GOAI_API_KEY is required.",
                    "",
                    "Get an API key:",
                    "1. Visit https://mustgoai.com",
                    "2. Register or log in",
                    "3. Open Settings -> API Key",
                    "4. Create a new API key",
                    f"5. Configure this skill in {config_path}, for example:",
                    '   "skills": {',
                    '     "entries": {',
                    f'       "{self.skill_name}": {{',
                    '         "enabled": true,',
                    '         "env": {{',
                    '           "GOAI_API_KEY": "sk-..."',
                    "         }",
                    "       }",
                    "     }",
                    "   }",
                    "",
                    "Optional:",
                    "- Set GOAI_BASE_URL only if you need to override the default production endpoint",
                ]
            )
        )

    def _headers(self, auth_mode: str) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if auth_mode == "auth":
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _error_message(self, payload: Any) -> str:
        if not isinstance(payload, dict):
            return ""
        data = payload.get("data")
        candidates = []
        if isinstance(data, dict):
            candidates.append(data.get("error_message"))
        candidates.extend(
            [
                payload.get("error_message"),
                payload.get("message"),
                payload.get("msg"),
                payload.get("error"),
            ]
        )
        for value in candidates:
            if value is None:
                continue
            if isinstance(value, str) and value.strip():
                return value
            if not isinstance(value, str):
                text = str(value).strip()
                if text:
                    return text
        return ""

    def _parse_json(self, response: httpx.Response) -> dict[str, Any] | None:
        try:
            payload = response.json()
        except ValueError:
            return None
        return payload if isinstance(payload, dict) else None

    def json_request(
        self,
        method: str,
        url: str,
        auth_mode: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = self._http.request(
                method,
                url,
                headers=self._headers(auth_mode),
                params=query,
                json=body,
            )
        except httpx.RequestError:
            raise GoAIError(f"request failed: {url}") from None

        payload = self._parse_json(response)
        if response.status_code not in {200, 201}:
            message = self._error_message(payload)
            if response.status_code == 401:
                raise GoAIError("unauthorized: check GOAI_API_KEY")
            if response.status_code == 402:
                raise GoAIError("insufficient credits")
            if response.status_code == 429:
                raise GoAIError("rate limited")
            if message:
                raise GoAIError(f"request failed ({response.status_code}): {message}")
            raise GoAIError(f"request failed ({response.status_code})")

        if payload is None:
            raise GoAIError("invalid API response")

        self.last_payload = payload
        return payload

    def api_assert_ok(self, payload: dict[str, Any]) -> None:
        code = payload.get("code")
        if code is None or str(code) == "":
            raise GoAIError("invalid API response")
        if str(code) == "0":
            return

        message = self._error_message(payload)
        if str(code) == "-5":
            if message:
                raise GoAIError(f"content blocked: {message}")
            raise GoAIError("content blocked")
        if message:
            raise GoAIError(f"api error (code {code}): {message}")
        raise GoAIError(f"api error (code {code})")

    def upload_local_image(self, value: str) -> str:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        if not path.is_file():
            raise GoAIError(f"local image not found or unreadable: {value}")

        mime_type = content_type_for_file(path)
        payload = self.json_request(
            "GET",
            f"{self.base_url}/api/v2/oss/sign-url",
            "auth",
            query={
                "filename": path.name,
                "contentType": mime_type,
                "folder": "inputs",
            },
        )
        self.api_assert_ok(payload)

        data = payload.get("data")
        if not isinstance(data, dict):
            raise GoAIError("invalid upload response")
        signed_url = str(data.get("signedUrl") or "")
        final_url = str(data.get("finalUrl") or "")
        if not signed_url:
            raise GoAIError("signedUrl missing from upload response")
        if not final_url:
            raise GoAIError("finalUrl missing from upload response")

        try:
            response = self._http.put(
                signed_url,
                headers={"Content-Type": mime_type},
                content=path.read_bytes(),
            )
        except httpx.RequestError:
            raise GoAIError(f"upload failed: {value}") from None

        if response.status_code not in {200, 201}:
            raise GoAIError(f"upload failed ({response.status_code}): {value}")

        return final_url

    def upload_local_file(self, value: str) -> str:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        if not path.is_file():
            raise GoAIError(f"local file not found or unreadable: {value}")

        mime_type = content_type_for_file(path)
        payload = self.json_request(
            "GET",
            f"{self.base_url}/api/v2/oss/sign-url",
            "auth",
            query={
                "filename": path.name,
                "contentType": mime_type,
                "folder": "inputs",
            },
        )
        self.api_assert_ok(payload)

        data = payload.get("data")
        if not isinstance(data, dict):
            raise GoAIError("invalid upload response")
        signed_url = str(data.get("signedUrl") or "")
        final_url = str(data.get("finalUrl") or "")
        if not signed_url:
            raise GoAIError("signedUrl missing from upload response")
        if not final_url:
            raise GoAIError("finalUrl missing from upload response")

        try:
            response = self._http.put(
                signed_url,
                headers={"Content-Type": mime_type},
                content=path.read_bytes(),
            )
        except httpx.RequestError:
            raise GoAIError(f"upload failed: {value}") from None

        if response.status_code not in {200, 201}:
            raise GoAIError(f"upload failed ({response.status_code}): {value}")

        return final_url

    def resolve_image_inputs(self, inputs: list[str]) -> list[str]:
        resolved: list[str] = []
        for item in inputs:
            if not item.strip():
                continue
            if is_url(item):
                resolved.append(item)
            else:
                resolved.append(self.upload_local_image(item))
        return resolved

    def resolve_file_input(self, value: str) -> str:
        if not value.strip():
            raise GoAIError("file input is empty")
        if is_url(value):
            return value
        return self.upload_local_file(value)

    def _poll_request(self, url: str) -> tuple[dict[str, Any] | None, str]:
        try:
            response = self._http.get(url, headers=self._headers("auth"))
        except httpx.RequestError:
            return None, ""

        payload = self._parse_json(response)
        if response.status_code not in {200, 201}:
            return None, self._error_message(payload)
        if payload is None:
            return None, ""

        code = payload.get("code")
        if code is None or str(code) != "0":
            return None, self._error_message(payload)

        self.last_payload = payload
        return payload, ""

    def poll_task(
        self,
        task_url: str,
        media_field: str,
        interval_seconds: int = 3,
        max_attempts: int = 0,
        timeout_message: str = "generation timed out",
    ) -> str:
        attempt = 1
        while True:
            payload, message = self._poll_request(task_url)
            if payload is not None:
                data = payload.get("data")
                status = str(data.get("status") or "") if isinstance(data, dict) else ""
                if status in {"completed", "success"}:
                    media_url = str(data.get(media_field) or "") if isinstance(data, dict) else ""
                    if not media_url:
                        raise GoAIError(f"{media_field} missing in completed task response")
                    self.last_media_url = media_url
                    return media_url
                if status == "timeout":
                    raise GoAIError(self._error_message(payload) or timeout_message)
                if status in TERMINAL_FAILURE_STATES:
                    raise GoAIError(self._error_message(payload) or "generation failed")
                if not status:
                    print_warning(f"polling error for {task_url}: task status missing, retrying")
            else:
                if message:
                    print_warning(f"polling error for {task_url}: {message}, retrying")
                else:
                    print_warning(f"polling request failed for {task_url}, retrying")

            if max_attempts > 0 and attempt >= max_attempts:
                raise GoAIError(timeout_message)

            time.sleep(interval_seconds)
            attempt += 1

    def download_media(self, media_url: str, output_name: str) -> str:
        if not media_url:
            raise GoAIError("download URL is required")

        output_path = Path(output_name).expanduser()
        if not output_path.is_absolute():
            output_path = (Path.cwd() / output_name).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            response = self._http.get(media_url)
        except httpx.RequestError:
            raise GoAIError(f"download failed: {media_url}") from None

        if response.status_code not in {200, 201}:
            raise GoAIError(f"download failed: {media_url}")

        output_path.write_bytes(response.content)
        return str(output_path)
