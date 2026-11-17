from __future__ import annotations

import json
import math
import mimetypes
import os
import re
import time
import uuid
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, BinaryIO, Iterator, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEFAULT_BASE_URL = "https://www.link42.ai"
TERMINAL = {"succeeded", "failed", "cancelled", "timeout", "expired"}


class Link42Error(Exception):
    def __init__(self, message: str, *, status: int = 0, code: str = "connection_error", request_id: str | None = None, body: Any = None):
        super().__init__(message)
        self.status, self.code, self.request_id, self.body = status, code, request_id, body
        self.idempotency_key: str | None = None


class TaskFailedError(Link42Error):
    def __init__(self, task: Mapping[str, Any]):
        self.task = task
        error = task.get("error") or {}
        super().__init__(error.get("message") or f"Task {task.get('id')} ended with {task.get('status')}", code=error.get("code") or str(task.get("status")))


class PollTimeoutError(Link42Error):
    def __init__(self, task_id: str, last_task: Mapping[str, Any] | None = None):
        self.task_id, self.last_task = task_id, last_task
        super().__init__(f"Timed out waiting for task {task_id}; resume this task ID instead of submitting again.", code="poll_timeout")


class UploadError(Link42Error):
    def __init__(self, stage: str, upload_id: str | None, asset_id: int | None, cause: Exception):
        self.stage, self.upload_id, self.asset_id = stage, upload_id, asset_id
        super().__init__(f"Asset {stage} failed" + (f"; upload ID {upload_id}" if upload_id else ""), status=getattr(cause, "status", 0), code="upload_failed", request_id=getattr(cause, "request_id", None))


class APIResponse(dict):
    """Wire JSON stays unchanged; request_id is available as an attribute."""
    def __init__(self, value: Mapping[str, Any], request_id: str | None):
        super().__init__(value)
        self.request_id = request_id


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _positive(value: float, name: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _id(value: str | int) -> str:
    if not str(value).strip():
        raise ValueError("ID is required")
    return quote(str(value), safe="")


class Link42:
    def __init__(self, api_key: str | None = None, *, base_url: str = DEFAULT_BASE_URL, timeout: float = 60, max_retries: int = 2):
        self._api_key = api_key if api_key is not None else os.getenv("LINK42_API_KEY", "")
        if not self._api_key.strip() or "\r" in self._api_key or "\n" in self._api_key:
            raise ValueError("LINK42_API_KEY or api_key is required")
        url = urlsplit(base_url)
        if url.scheme not in {"http", "https"} or not url.netloc or url.username or url.password or url.query or url.fragment:
            raise ValueError("Invalid base_url")
        if url.scheme == "http" and url.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("base_url must use HTTPS; HTTP is permitted only for loopback development")
        self.base_url = base_url.rstrip("/").removesuffix("/v1")
        self.timeout = _positive(timeout, "timeout")
        if not isinstance(max_retries, int) or not 0 <= max_retries <= 5:
            raise ValueError("max_retries must be 0–5")
        self.max_retries = max_retries
        self._opener = build_opener(_NoRedirect())
        self.models = _Models(self)
        self.estimates = _Resource(self, "/v1/estimates")
        self.chat = _Chat(self)
        self.responses = _Resource(self, "/v1/responses")
        self.messages = _Resource(self, "/v1/messages")
        self.images = _Images(self)
        self.image_tasks = _ImageTasks(self)
        self.embeddings = _Resource(self, "/v1/embeddings")
        self.gemini = _Gemini(self)
        self.videos = _Videos(self)
        self.assets = _Assets(self)
        self.usage = _Usage(self)
        self.scores = _Scores(self)

    def _open(self, method: str, path: str, body: Any = None, *, timeout: float | None = None, idempotency_key: str | None = None, retries: int | None = None, stream: bool = False, headers: Mapping[str, str] | None = None):
        extra_headers = {}
        for name, value in (headers or {}).items():
            key = name.lower()
            if not re.fullmatch(r"[a-z0-9-]+", key) or "\r" in value or "\n" in value or key in {"authorization", "x-api-key", "x-goog-api-key", "cookie", "host", "content-length", "content-type", "transfer-encoding", "connection", "accept", "idempotency-key"}:
                raise ValueError(f"Unsafe request header: {name}")
            extra_headers[key] = value
        if retries is not None and (not isinstance(retries, int) or not 0 <= retries <= 5):
            raise ValueError("retries must be 0–5")
        headers = {"Authorization": f"Bearer {self._api_key}", "Accept": "text/event-stream" if stream else "application/json", "User-Agent": "link42-python/0.1.2"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        if path.startswith("/v1/messages"):
            headers["anthropic-version"] = "2023-06-01"
        headers.update(extra_headers)
        data = None if body is None else json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if data is not None:
            headers["Content-Type"] = "application/json"
        attempts = (self.max_retries if retries is None else retries) if method == "GET" else 0
        for attempt in range(attempts + 1):
            try:
                return self._opener.open(Request(self.base_url + path, data=data, headers=headers, method=method), timeout=_positive(self.timeout if timeout is None else timeout, "timeout"))
            except HTTPError as error:
                status, request_id, retry_after = error.code, error.headers.get("x-request-id"), error.headers.get("retry-after")
                try:
                    text = error.read(65536).decode("utf-8", "replace")
                finally:
                    error.close()
                if attempt < attempts and status in {429, 502, 503, 504}:
                    delay = .25 * 2 ** attempt
                    if retry_after:
                        try:
                            delay = float(retry_after)
                        except ValueError:
                            try:
                                delay = (parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds()
                            except (ValueError, TypeError):
                                pass
                    time.sleep(max(0, min(5, delay)))
                    continue
                try:
                    parsed = json.loads(text)
                except ValueError:
                    parsed = {"message": text}
                detail = parsed.get("error", parsed) if isinstance(parsed, dict) else {}
                if not isinstance(detail, dict):
                    detail = {}
                raise Link42Error(detail.get("message") or f"HTTP {status}", status=status, code=str(detail.get("code") or detail.get("type") or "api_error"), request_id=request_id, body=parsed) from None
            except (URLError, TimeoutError, OSError) as error:
                if attempt < attempts:
                    time.sleep(.25 * 2 ** attempt)
                    continue
                raise Link42Error("Network request failed; mutation requests are not retried automatically.") from error

    def _request(self, method: str, path: str, body: Any = None, **options):
        with self._open(method, path, body, **options) as response:
            if response.status == 204:
                return None
            try:
                value = json.load(response)
            except (ValueError, UnicodeError) as error:
                raise Link42Error("Invalid JSON response", status=response.status, code="invalid_response", request_id=response.headers.get("x-request-id")) from error
            return APIResponse(value, response.headers.get("x-request-id")) if isinstance(value, dict) else value

    def _request_text(self, method: str, path: str, body: Any = None, **options) -> str:
        with self._open(method, path, body, **options) as response:
            try:
                return response.read().decode("utf-8")
            except UnicodeError as error:
                raise Link42Error("Invalid text response", status=response.status, code="invalid_response", request_id=response.headers.get("x-request-id")) from error

    def stream(self, path: str, body: Mapping[str, Any], **options) -> Iterator[dict[str, Any]]:
        try:
            yield from self._stream(path, body, **options)
        except (TimeoutError, OSError) as error:
            raise Link42Error("Stream connection interrupted; do not replay automatically.", code="stream_interrupted") from error

    def _stream(self, path: str, body: Mapping[str, Any], **options) -> Iterator[dict[str, Any]]:
        """No reconnection: an interrupted paid stream must not be replayed."""
        if not (path.startswith("/v1/") or path.startswith("/v1beta/")):
            raise ValueError("Invalid stream path")
        with self._open("POST", path, body, stream=True, **options) as response:
            if "text/event-stream" not in response.headers.get("content-type", ""):
                raise Link42Error("Expected an SSE response", status=response.status, code="invalid_response")
            terminal_seen = False
            lines: list[str] = []
            event, event_id, size = "message", None, 0
            while True:
                raw = response.readline(8 * 1024 * 1024 + 1)
                size += len(raw)
                if size > 8 * 1024 * 1024:
                    raise Link42Error("SSE event exceeds 8 MiB", code="stream_event_too_large")
                line = raw.decode("utf-8").rstrip("\r\n") if raw else ""
                if not line:
                    text = "\n".join(lines)
                    if text.strip() == "[DONE]":
                        return
                    if text.strip():
                        try:
                            value = json.loads(text)
                        except ValueError as error:
                            raise Link42Error("Invalid SSE JSON", code="invalid_response", request_id=response.headers.get("x-request-id")) from error
                        if event == "error" or isinstance(value, dict) and value.get("error"):
                            detail = value.get("error", value)
                            raise Link42Error(detail.get("message", "Stream failed"), code=detail.get("code", "stream_error"), request_id=response.headers.get("x-request-id"), body=value)
                        if isinstance(value, dict) and value.get("type", event) in {"response.completed", "response.failed", "response.incomplete", "message_stop"}:
                            terminal_seen = True
                        yield {"event": event, "id": event_id, "data": value}
                    lines, event, size = [], "message", 0
                    if not raw:
                        if not terminal_seen and path in {"/v1/chat/completions", "/v1/responses", "/v1/messages"}:
                            raise Link42Error("Stream ended before its completion event; do not replay automatically.", code="stream_incomplete", request_id=response.headers.get("x-request-id"))
                        return
                elif not line.startswith(":"):
                    field, _, value = line.partition(":")
                    value = value.removeprefix(" ")
                    if field == "data":
                        lines.append(value)
                    elif field == "event":
                        event = value
                    elif field == "id" and "\x00" not in value:
                        event_id = value


class _Resource:
    def __init__(self, client: Link42, path: str):
        self.client, self.path = client, path

    def create(self, *, request_options: dict[str, Any] | None = None, **params):
        if params.get("stream"):
            return self.stream(request_options=request_options, **params)
        return self.client._request("POST", self.path, params, **(request_options or {}))

    def stream(self, *, request_options: dict[str, Any] | None = None, **params):
        source = self.client.stream(self.path, {**params, "stream": True}, **(request_options or {}))
        try:
            for event in source:
                yield event["data"]
        finally:
            source.close()

    def count_tokens(self, *, request_options=None, **params):
        if self.path != "/v1/messages": raise ValueError("Token counting is only supported for messages")
        return self.client._request("POST", self.path + "/count_tokens", params, **(request_options or {}))


class _Chat:
    def __init__(self, client: Link42):
        self.completions = _Resource(client, "/v1/chat/completions")


class _Models:
    def __init__(self, client: Link42): self.client = client
    def list(self, **options): return self.client._request("GET", "/v1/models", **options)
    def get(self, model: str, **options): return self.client._request("GET", "/v1/models/" + _id(model), **options)


class _Images(_Resource):
    def __init__(self, client: Link42): super().__init__(client, "/v1/images/generations")
    def generate(self, *, request_options=None, **params): return self.create(request_options=request_options, **params)
    def edit(self, *, request_options=None, **params): return self.client._request("POST", "/v1/images/edits", params, **(request_options or {}))


class _ImageTasks:
    def __init__(self, client: Link42): self.client = client
    def create(self, *, request_options=None, **params):
        options = dict(request_options or {})
        options.setdefault("idempotency_key", str(uuid.uuid4()))
        try:
            return self.client._request("POST", "/v1/images/generations/async", params, **options)
        except Link42Error as error:
            error.idempotency_key = options["idempotency_key"]
            raise
    def get(self, task_id: str, **options): return self.client._request("GET", "/v1/images/tasks/" + _id(task_id), **options)
    def wait(self, task_id: str, *, timeout: float = 600, poll_interval: float = 3, throw_on_failure: bool = True):
        deadline = time.monotonic() + _positive(timeout, "timeout")
        _positive(poll_interval, "poll_interval")
        last = None
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0: raise PollTimeoutError(task_id, last)
            try:
                last = self.get(task_id, timeout=min(self.client.timeout, remaining), retries=0)
            except Link42Error as error:
                if time.monotonic() >= deadline: raise PollTimeoutError(task_id, last) from error
                raise
            if last.get("status") in {"succeeded", "failed"}:
                if last["status"] == "failed" and throw_on_failure: raise TaskFailedError(last)
                return last
            time.sleep(min(poll_interval, max(0, deadline-time.monotonic())))


class _Gemini:
    def __init__(self, client: Link42): self.client = client
    def generate_content(self, model: str, *, request_options=None, **params): return self.client._request("POST", "/v1beta/models/" + _id(model) + ":generateContent", params, **(request_options or {}))
    def stream_generate_content(self, model: str, *, request_options=None, **params): return (event["data"] for event in self.client.stream("/v1beta/models/" + _id(model) + ":streamGenerateContent?alt=sse", params, **(request_options or {})))


class _Usage:
    def __init__(self, client: Link42): self.client = client
    @staticmethod
    def _query(filters: Mapping[str, Any]) -> str:
        encoded = urlencode({key: value for key, value in filters.items() if value is not None})
        return "?" + encoded if encoded else ""
    def report(self, *, request_options=None, **filters):
        return self.client._request("GET", "/v1/usage/report" + self._query(filters), **(request_options or {}))
    def report_csv(self, *, request_options=None, **filters) -> str:
        return self.client._request_text("GET", "/v1/usage/report" + self._query({**filters, "format": "csv"}), **(request_options or {}))
    def logs(self, *, request_options=None, **filters):
        return self.client._request("GET", "/v1/usage/logs" + self._query(filters), **(request_options or {}))


class _Scores:
    def __init__(self, client: Link42): self.client = client
    def create(self, *, request_options=None, **params):
        return self.client._request("POST", "/v1/scores", params, **(request_options or {}))


class _Videos:
    def __init__(self, client: Link42): self.client = client
    def create(self, *, request_options=None, **params):
        options = dict(request_options or {})
        options.setdefault("idempotency_key", str(uuid.uuid4()))
        try:
            return self.client._request("POST", "/v1/videos", params, **options)
        except Link42Error as error:
            error.idempotency_key = options["idempotency_key"]
            raise
    def get(self, task_id: str, **options): return self.client._request("GET", "/v1/videos/" + _id(task_id), **options)
    def list(self, *, request_options=None, **filters): return self.client._request("GET", "/v1/videos?" + urlencode({k:v for k,v in filters.items() if v is not None}), **(request_options or {}))
    def cancel(self, task_id: str, **options): return self.client._request("DELETE", "/v1/videos/" + _id(task_id), **options)
    def wait(self, task_id: str, *, timeout: float = 600, poll_interval: float = 3, throw_on_failure: bool = True):
        deadline = time.monotonic() + _positive(timeout, "timeout")
        _positive(poll_interval, "poll_interval")
        last = None
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0: raise PollTimeoutError(task_id, last)
            try:
                last = self.get(task_id, timeout=min(self.client.timeout, remaining), retries=0)
            except Link42Error as error:
                if time.monotonic() >= deadline: raise PollTimeoutError(task_id, last) from error
                raise
            if last.get("status") in TERMINAL:
                if last["status"] != "succeeded" and throw_on_failure: raise TaskFailedError(last)
                return last
            time.sleep(min(poll_interval, max(0, deadline-time.monotonic())))


class _Assets:
    def __init__(self, client: Link42): self.client = client
    def list(self, *, request_options=None, **filters): return self.client._request("GET", "/v1/assets?" + urlencode({k:v for k,v in filters.items() if v is not None}), **(request_options or {}))
    def get(self, asset_id: int, **options): return self.client._request("GET", "/v1/assets/" + _id(asset_id), **options)
    def delete(self, asset_id: int, **options): return self.client._request("DELETE", "/v1/assets/" + _id(asset_id), **options)
    def begin(self, *, name: str, type: str, content_type: str, size_bytes: int, request_options=None):
        options = dict(request_options or {})
        options.setdefault("idempotency_key", str(uuid.uuid4()))
        return self.client._request("POST", "/v1/assets", {"name":name,"type":type,"content_type":content_type,"size_bytes":size_bytes}, **options)
    def complete(self, upload_id: str, **options): return self.client._request("POST", "/v1/assets/uploads/" + _id(upload_id) + "/complete", **options)
    def upload_file(self, filename: str | Path, *, name: str | None = None, content_type: str | None = None, type: str | None = None, request_options=None):
        path = Path(filename)
        if not path.is_file(): raise ValueError("Expected a regular file")
        mime = content_type or mimetypes.guess_type(str(path))[0]
        if not mime: raise ValueError("Specify content_type for this file")
        with path.open("rb") as file:
            return self._upload(file, os.fstat(file.fileno()).st_size, name or path.name, mime, type, request_options or {})
    def upload_bytes(self, data: bytes, *, name: str, content_type: str, type: str | None = None, request_options=None):
        return self._upload(data, len(data), name, content_type, type, request_options or {})
    def _upload(self, data: bytes | BinaryIO, size: int, name: str, mime: str, kind: str | None, options: dict[str, Any]):
        _positive(size, "file size")
        kind = kind or mime.split("/", 1)[0]
        if kind not in {"image", "video", "audio"}: raise ValueError("Unsupported asset type")
        try:
            reservation = self.begin(name=name, type=kind, content_type=mime, size_bytes=size, request_options=options)
        except Exception as error:
            raise UploadError("reserve", None, None, error) from error
        upload_id, asset_id = reservation["upload_id"], reservation["asset"]["id"]
        try:
            target = reservation["upload"]
            url, base = urlsplit(target["url"]), urlsplit(self.client.base_url)
            local = {"localhost", "127.0.0.1", "::1"}
            if url.username or url.password or not (url.scheme == "https" or url.scheme == "http" and url.hostname in local and base.hostname in local): raise ValueError("Unsafe upload URL")
            if target["method"] != "PUT": raise ValueError("Unsupported upload method")
            headers = dict(target["headers"])
            if any(k.lower() in {"authorization", "cookie", "proxy-authorization", "host"} for k in headers): raise ValueError("Unsafe upload header")
            headers["Content-Length"] = str(size)
            # Do not attach the LINK42 bearer token to object storage requests.
            with self.client._opener.open(Request(target["url"], data=data, headers=headers, method="PUT"), timeout=options.get("timeout", self.client.timeout)) as response:
                if not 200 <= response.status < 300: raise Link42Error("Object upload failed", status=response.status)
        except Exception as error:
            if isinstance(error, HTTPError): error.close()
            raise UploadError("upload", upload_id, asset_id, error) from error
        try:
            return self.complete(upload_id, **options)
        except Exception as error:
            raise UploadError("complete", upload_id, asset_id, error) from error
