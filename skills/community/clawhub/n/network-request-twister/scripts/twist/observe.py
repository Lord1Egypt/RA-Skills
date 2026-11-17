"""Observation engine: real-time network monitoring with JSONL output.

Receives Fetch.requestPaused CDP events, extracts data, and writes
one JSON object per line to stdout. Blocks until interrupted.
"""

from __future__ import annotations

import asyncio
import base64
import gzip
import json
import sys
from dataclasses import dataclass, field
from typing import Any

from .cdp import CDP
from .logger import get as get_logger

OBSERVE_BODY_LIMIT = 4 * 1024  # 4KB default truncation


def _decompress_str(text: str, content_encoding: str) -> str:
    """Decompress a string that was HTTP content-encoded (gzip/deflate/brotli)."""
    body_bytes = text.encode("utf-8", errors="replace")
    enc = content_encoding.lower().strip()
    try:
        if enc in ("gzip", "x-gzip"):
            return gzip.decompress(body_bytes).decode("utf-8", errors="replace")
        if enc == "deflate":
            import zlib
            return zlib.decompress(body_bytes).decode("utf-8", errors="replace")
        if enc == "br":
            try:
                import brotli  # type: ignore[import-untyped]
                return brotli.decompress(body_bytes).decode("utf-8", errors="replace")
            except ImportError:
                pass
    except Exception:
        pass
    return text


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ObserveFilter:
    """Filter conditions for observed events. Multiple fields are ANDed,
    values within a field are ORed."""

    urls: list[str] = field(default_factory=list)
    types: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.urls and not self.types

    def match(self, url: str, resource_type: str) -> bool:
        if self.urls:
            if not any(p in url for p in self.urls):
                return False
        if self.types:
            rt_lower = resource_type.lower()
            if not any(t.lower() == rt_lower for t in self.types):
                return False
        return True


@dataclass
class ObserveOptions:
    """Observation mode parameters."""

    enabled: bool = False
    full_body: bool = False
    filter: ObserveFilter = field(default_factory=ObserveFilter)


@dataclass
class ObserveEvent:
    """A single observed network event, serialized as JSONL."""

    type: str  # "request" or "response"
    request_id: str
    url: str = ""
    method: str = ""
    resource_type: str = ""
    request_headers: dict[str, str] = field(default_factory=dict)
    post_data: str = ""
    status_code: int = 0
    status_text: str = ""
    response_headers: dict[str, str] = field(default_factory=dict)
    body: str = ""
    body_truncated: bool = False
    body_size: int = 0
    error_reason: str = ""

    def to_json(self) -> str:
        d: dict[str, Any] = {"type": self.type, "requestId": self.request_id}
        if self.url:
            d["url"] = self.url
        if self.method:
            d["method"] = self.method
        if self.resource_type:
            d["resourceType"] = self.resource_type
        if self.request_headers:
            d["requestHeaders"] = self.request_headers
        if self.post_data:
            d["postData"] = self.post_data
        if self.status_code:
            d["statusCode"] = self.status_code
        if self.status_text:
            d["statusText"] = self.status_text
        if self.response_headers:
            d["responseHeaders"] = self.response_headers
        if self.body:
            d["body"] = self.body
        if self.body_truncated:
            d["bodyTruncated"] = True
        if self.body_size:
            d["bodySize"] = self.body_size
        if self.error_reason:
            d["errorReason"] = self.error_reason
        return json.dumps(d, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Observe engine
# ---------------------------------------------------------------------------


class Observe:
    """Receives Fetch events, extracts data, writes JSONL to stdout."""

    def __init__(self, cdp: CDP, opts: ObserveOptions) -> None:
        self._cdp = cdp
        self._opts = opts

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    async def start(self, navigate_url: str | None = None) -> None:
        """Enter the observation event loop. Blocks until interrupted.

        Navigates after Fetch is enabled so the initial document request is
        captured in the observation output.
        """
        # Windows: force UTF-8 to avoid GBK encoding errors with binary bodies
        import os
        if os.name == "nt":
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")

        await self._cdp.enable_network()
        queue = await self._cdp.enable_fetch()

        if navigate_url:
            try:
                await self._cdp.navigate_to(navigate_url)
                get_logger().info("navigated", extra={"ctx": {"url": navigate_url}})
            except Exception:
                get_logger().warning(
                    "navigation failed, continuing on current page",
                    extra={"ctx": {"url": navigate_url}},
                )

        async def _watch_disconnect() -> None:
            await self._cdp.disconnected.wait()
            await queue.put({"__disconnected__": True})

        watcher = asyncio.create_task(_watch_disconnect())

        try:
            while True:
                ev = await queue.get()
                if isinstance(ev, dict) and ev.get("__disconnected__"):
                    return

                stage = "response" if (
                    ev.get("responseStatusCode") is not None
                    or ev.get("responseErrorReason") is not None
                ) else "request"

                request_id: str = ev["requestId"]

                if self._should_bypass(ev):
                    await self._continue(request_id, stage)
                    continue

                if not self._opts.filter.is_empty:
                    url = ev.get("request", {}).get("url", "")
                    rt = ev.get("resourceType", "")
                    if not self._opts.filter.match(url, rt):
                        await self._continue(request_id, stage)
                        continue

                obs = await self._build_event(ev, stage)

                sys.stdout.write(obs.to_json() + "\n")
                sys.stdout.flush()

                await self._continue(request_id, stage)
        except asyncio.CancelledError:
            pass
        finally:
            watcher.cancel()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _should_bypass(ev: dict[str, Any]) -> bool:
        url = ev.get("request", {}).get("url", "")
        if not (url.startswith("http://") or url.startswith("https://")):
            return True
        if ev.get("resourceType") == "WebSocket":
            return True
        return False

    async def _build_event(self, ev: dict[str, Any], stage: str) -> ObserveEvent:
        req = ev.get("request", {})
        url = req.get("url", "")
        rt = ev.get("resourceType", "")

        if stage == "request":
            headers = _parse_headers(req.get("headers", {}))
            post_data = ""
            if req.get("hasPostData"):
                post_data = _get_post_data_str(req)

            return ObserveEvent(
                type="request",
                request_id=ev["requestId"],
                url=url,
                method=req.get("method", ""),
                resource_type=rt,
                request_headers=headers,
                post_data=post_data,
            )
        else:
            # Response stage
            error_reason = ev.get("responseErrorReason", "")
            status_code = ev.get("responseStatusCode", 0) or 0
            status_text = ev.get("responseStatusText", "") or ""
            resp_headers = _parse_response_headers(ev.get("responseHeaders", []))

            body = ""
            body_truncated = False
            body_size = 0

            if not error_reason:
                resp_hdrs = _parse_response_headers(ev.get("responseHeaders", []))
                content_encoding = resp_hdrs.get("Content-Encoding", "")
                body, body_truncated, body_size = await self._get_body(ev["requestId"], content_encoding)

            return ObserveEvent(
                type="response",
                request_id=ev["requestId"],
                url=url,
                resource_type=rt,
                status_code=status_code,
                status_text=status_text,
                response_headers=resp_headers,
                body=body,
                body_truncated=body_truncated,
                body_size=body_size,
                error_reason=error_reason,
            )

    async def _get_body(
        self, request_id: str, content_encoding: str = ""
    ) -> tuple[str, bool, int]:
        try:
            resp = await self._cdp.get_response_body(request_id)
        except Exception:
            return "", False, 0

        raw = resp.get("body", "")
        if resp.get("base64Encoded"):
            try:
                raw_bytes = base64.b64decode(raw)
                raw = raw_bytes.decode("utf-8", errors="replace")
            except Exception:
                pass
        elif isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")

        if content_encoding:
            try:
                raw = _decompress_str(raw, content_encoding)
            except Exception:
                pass

        total = len(raw)
        limit = total if self._opts.full_body else OBSERVE_BODY_LIMIT

        if len(raw) > limit:
            return raw[:limit], True, total
        return raw, False, total

    async def _continue(self, request_id: str, stage: str) -> None:
        log = get_logger()
        try:
            if stage == "response":
                await self._cdp.continue_response(request_id)
            else:
                await self._cdp.continue_request(request_id)
        except Exception as e:
            log.error(f"observe continue failed: {e}", extra={"ctx": {"requestId": request_id}})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_headers(raw: dict[str, Any]) -> dict[str, str]:
    return {k: str(v) for k, v in raw.items()} if raw else {}


def _parse_response_headers(raw: list[dict[str, Any]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for h in raw:
        name = h.get("name", "")
        if name:
            result[name] = str(h.get("value", ""))
    return result


def _get_post_data_str(req: dict[str, Any]) -> str:
    entries = req.get("postDataEntries") or []
    if entries:
        parts: list[str] = []
        for entry in entries:
            raw_bytes = entry.get("bytes", "")
            if raw_bytes:
                try:
                    parts.append(base64.b64decode(raw_bytes).decode("utf-8", errors="replace"))
                except Exception:
                    parts.append(raw_bytes)
        return "".join(parts)
    return req.get("postData", "")


def parse_filter(raw_filters: list[str]) -> ObserveFilter:
    """Parse raw --observe-filter values into an ObserveFilter.

    Format: key=val1,val2 (repeatable, values ORed within a key,
    multiple keys ANDed).
    """
    f = ObserveFilter()
    for item in raw_filters:
        if "=" not in item:
            continue
        key, _, vals = item.partition("=")
        parts = [v.strip() for v in vals.split(",") if v.strip()]
        if key == "url":
            f.urls.extend(parts)
        elif key == "type":
            f.types.extend(parts)
    return f
