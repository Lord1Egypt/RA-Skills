"""Interception engine: event loop, worker pool, rule matching, action execution.

Handles Fetch.requestPaused CDP events, matches them against the rule
configuration, and executes the corresponding actions (block, modify
headers, rewrite URLs/bodies, JSON-patch, HTML element replacement, etc.).
"""

from __future__ import annotations

import asyncio
import base64
import gzip
import json
import os
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Any

from bs4 import BeautifulSoup

from .cdp import CDP
from .config import Action, Condition, Config, JSONPatch, Rule
from .logger import get as get_logger

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_BODY_SIZE = 5 * 1024 * 1024       #  5 MB — skip request inspection
MAX_RESPONSE_BODY_SIZE = 10 * 1024 * 1024  # 10 MB — skip response modification
WORKER_COUNT = max(os.cpu_count() or 4, 4)
WORKER_TIMEOUT = 5.0  # seconds per event

_DEL = object()  # sentinel for multipart line deletion

# ---------------------------------------------------------------------------
# Action collectors — accumulate modifications before applying to CDP
# ---------------------------------------------------------------------------


@dataclass
class _RequestCollector:
    """Accumulates request-stage action modifications for batch CDP apply."""

    url: str | None = None
    method: str | None = None
    headers_set: dict[str, str] = field(default_factory=dict)
    headers_remove: set[str] = field(default_factory=set)
    cookies_set: dict[str, str] = field(default_factory=dict)
    cookies_remove: set[str] = field(default_factory=set)
    query_set: dict[str, str] = field(default_factory=dict)
    query_remove: set[str] = field(default_factory=set)
    form_fields_set: dict[str, str] = field(default_factory=dict)
    form_fields_remove: set[str] = field(default_factory=set)
    body_set: str | None = None
    body_appends: list[str] = field(default_factory=list)
    body_replacements: list[tuple[str, str, bool]] = field(default_factory=list)
    body_patches: list[JSONPatch] = field(default_factory=list)
    blocked: bool = False
    block_status_code: int = 200
    block_headers: dict[str, str] = field(default_factory=dict)
    block_body: str = ""

    @property
    def has_body_mods(self) -> bool:
        return bool(
            self.body_set is not None
            or self.body_appends
            or self.body_replacements
            or self.body_patches
            or self.form_fields_set
            or self.form_fields_remove
        )


@dataclass
class _ResponseCollector:
    """Accumulates response-stage action modifications for batch CDP apply."""

    status_code: int | None = None
    body_set: str | None = None
    body_appends: list[str] = field(default_factory=list)
    body_replacements: list[tuple[str, str, bool]] = field(default_factory=list)
    body_patches: list[JSONPatch] = field(default_factory=list)
    element_replacements: list[tuple[str, str]] = field(default_factory=list)
    headers_cookies_set: dict[str, str] = field(default_factory=dict)
    headers_cookies_remove: set[str] = field(default_factory=set)

    @property
    def has_body_mods(self) -> bool:
        return bool(
            self.body_set is not None
            or self.body_appends
            or self.body_replacements
            or self.body_patches
            or self.element_replacements
        )

# ---------------------------------------------------------------------------
# Regex cache
# ---------------------------------------------------------------------------

_regex_cache: dict[str, re.Pattern[str]] = {}


def _get_regex(pattern: str) -> re.Pattern[str] | None:
    if pattern not in _regex_cache:
        try:
            _regex_cache[pattern] = re.compile(pattern)
        except re.error:
            return None
    return _regex_cache[pattern]


# ---------------------------------------------------------------------------
# Intercept
# ---------------------------------------------------------------------------


class Intercept:
    """Main interception engine."""

    def __init__(self, cdp: CDP, config: Config) -> None:
        self._cdp = cdp
        self._config = config
        self._worker_count = WORKER_COUNT

    # ------------------------------------------------------------------
    # Start / event loop
    # ------------------------------------------------------------------

    async def start(self, navigate_url: str | None = None) -> None:
        """Enable Network + Fetch domains and enter the event loop.

        Navigates after Fetch is enabled so the initial document request is
        covered by interception. Blocks until the CDP connection is lost.
        """
        await self._cdp.enable_network()
        queue = await self._cdp.enable_fetch()

        if navigate_url:
            try:
                await self._cdp.navigate_to(navigate_url)
                log = get_logger()
                log.info("navigated", extra={"ctx": {"url": navigate_url}})
            except Exception:
                log = get_logger()
                log.warning(
                    "navigation failed, continuing on current page",
                    extra={"ctx": {"url": navigate_url}},
                )

        worker_q: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue(maxsize=200)

        tasks: list[asyncio.Task[None]] = []
        for _ in range(self._worker_count):
            tasks.append(asyncio.create_task(self._worker(worker_q)))

        async def _watch_disconnect() -> None:
            await self._cdp.disconnected.wait()
            await queue.put({"__disconnected__": True})

        watcher = asyncio.create_task(_watch_disconnect())

        try:
            while True:
                ev = await queue.get()
                if isinstance(ev, dict) and ev.get("__disconnected__"):
                    break
                stage = "response" if ev.get("responseStatusCode") is not None else "request"

                if self._should_bypass(ev):
                    log = get_logger()
                    log.debug(
                        "request bypassed",
                        extra={"ctx": {"url": _req_url(ev), "stage": stage, "reason": "bypass"}},
                    )
                    await self._continue(ev, stage, headers=None)
                    continue

                await worker_q.put(ev)
        except asyncio.CancelledError:
            pass
        finally:
            watcher.cancel()
            for _ in range(self._worker_count):
                await worker_q.put(None)
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _worker(self, q: asyncio.Queue[dict[str, Any] | None]) -> None:
        while True:
            ev = await q.get()
            if ev is None:
                return
            try:
                await asyncio.wait_for(self._process(ev), timeout=WORKER_TIMEOUT)
            except asyncio.TimeoutError:
                pass
            except Exception:
                log = get_logger()
                log.exception("worker error", extra={"ctx": {"url": _req_url(ev)}})
            finally:
                q.task_done()

    async def _process(self, ev: dict[str, Any]) -> None:
        stage = "response" if ev.get("responseStatusCode") is not None else "request"
        rule = self._match_rules(ev, stage)
        if rule is None:
            await self._continue(ev, stage)
            return

        log = get_logger()
        log.debug(
            "rule matched",
            extra={"ctx": {"rule": rule.id, "url": _req_url(ev), "stage": stage}},
        )
        await self._execute_actions(ev, rule, stage)

    # ------------------------------------------------------------------
    # Bypass filter
    # ------------------------------------------------------------------

    def _should_bypass(self, ev: dict[str, Any]) -> bool:
        req = ev.get("request", {})
        url = req.get("url", "")

        if not (url.startswith("http://") or url.startswith("https://")):
            return True
        if ev.get("resourceType") == "WebSocket":
            return True
        if req.get("method") == "OPTIONS":
            return True

        cdp_addr = f"{self._cdp.host}:{self._cdp.port}"
        if cdp_addr in url:
            return True

        headers = _parse_headers(req.get("headers", {}))
        cl = _header_get(headers, "Content-Length")
        if cl:
            try:
                if int(cl) > MAX_BODY_SIZE:
                    return True
            except ValueError:
                pass

        return False

    # ------------------------------------------------------------------
    # Rule matching
    # ------------------------------------------------------------------

    def _match_rules(self, ev: dict[str, Any], stage: str) -> Rule | None:
        enabled = sorted(
            (r for r in self._config.rules if r.enabled and r.stage == stage),
            key=lambda r: r.priority,
            reverse=True,
        )
        for rule in enabled:
            if self._match_rule(ev, rule):
                return rule
        return None

    def _match_rule(self, ev: dict[str, Any], rule: Rule) -> bool:
        match = rule.match
        if match.all_of:
            if not all(self._match_condition(ev, c) for c in match.all_of):
                return False
        if match.any_of:
            if not any(self._match_condition(ev, c) for c in match.any_of):
                return False
        return True

    def _match_condition(self, ev: dict[str, Any], cond: Condition) -> bool:
        req = ev.get("request", {})
        url: str = req.get("url", "")
        hdrs = _parse_headers(req.get("headers", {}))

        match cond.type.value:
            case "urlEquals":
                return url == cond.value
            case "urlPrefix":
                return url.startswith(cond.value)
            case "urlSuffix":
                return url.endswith(cond.value)
            case "urlContains":
                return cond.value in url
            case "urlRegex":
                return _match_regex(cond.pattern, url)
            case "method":
                return any(
                    v.lower() == req.get("method", "").lower() for v in cond.values
                )
            case "resourceType":
                rt = ev.get("resourceType", "")
                return any(v.lower() == rt.lower() for v in cond.values)
            case "headerExists":
                return _header_has_key(hdrs, cond.name)
            case "headerNotExists":
                return not _header_has_key(hdrs, cond.name)
            case "headerEquals":
                return _header_get(hdrs, cond.name) == cond.value
            case "headerContains":
                return cond.value in _header_get(hdrs, cond.name)
            case "headerRegex":
                val = _header_get(hdrs, cond.name)
                return bool(val) and _match_regex(cond.pattern, val)
            case (
                "cookieExists"
                | "cookieNotExists"
                | "cookieEquals"
                | "cookieContains"
                | "cookieRegex"
            ):
                cookies = _parse_cookies(hdrs)
                return _match_cookie(cond, cookies)
            case (
                "queryExists"
                | "queryNotExists"
                | "queryEquals"
                | "queryContains"
                | "queryRegex"
            ):
                queries = _parse_query(url)
                return _match_query(cond, queries)
            case "bodyContains" | "bodyRegex" | "bodyJsonPath":
                body = _get_post_data_str(req)
                return _match_body(cond, body)
            case _:
                return False

    # ------------------------------------------------------------------
    # Action execution
    # ------------------------------------------------------------------

    async def _execute_actions(
        self, ev: dict[str, Any], rule: Rule, stage: str
    ) -> None:
        """Collect intent from all actions, then apply once to CDP."""
        log = get_logger()
        request_id: str = ev["requestId"]

        if stage == "request":
            col: _RequestCollector | _ResponseCollector = _RequestCollector()
        else:
            col = _ResponseCollector()

        for action in rule.actions:
            try:
                if self._collect_action(ev, rule, stage, action, col, log):
                    break  # block action stops collection
            except Exception:
                log.exception(
                    "action failed",
                    extra={"ctx": {"action": action.type.value, "rule": rule.id}},
                )

        if stage == "request":
            assert isinstance(col, _RequestCollector)
            try:
                await self._apply_request(ev, col, request_id)
            except Exception:
                log.exception("failed to apply request modifications, passing through")
                await self._continue(ev, stage)
        else:
            assert isinstance(col, _ResponseCollector)
            try:
                await self._apply_response(ev, col, request_id)
            except Exception:
                log.exception("failed to apply response modifications, passing through")
                await self._continue(ev, stage)

    # ------------------------------------------------------------------
    # Collect (declarative — writes to collector, does not touch CDP)
    # ------------------------------------------------------------------

    def _collect_action(
        self,
        ev: dict[str, Any],
        rule: Rule,
        stage: str,
        action: Action,
        col: _RequestCollector | _ResponseCollector,
        log: Any,
    ) -> bool:
        """Write the action's intent into *col*. Returns True for block (stop chain)."""
        at = action.type.value

        if at == "block":
            if stage != "request":
                log.warning("block only valid in request stage, passing through")
                return False
            log.debug("block request", extra={"ctx": {"rule": rule.id, "statusCode": action.status_code}})
            col = col  # type: _RequestCollector
            col.blocked = True
            col.block_status_code = action.status_code
            col.block_headers = action.headers
            col.block_body = action.body
            return True  # stop — block is terminal

        if at == "setHeader":
            if stage != "request":
                log.warning("setHeader only valid in request stage")
                return False
            log.debug("collect set header", extra={"ctx": {"rule": rule.id, "header": action.name}})
            col = col  # type: _RequestCollector
            col.headers_set[action.name] = str(action.value)
            return False

        if at == "removeHeader":
            if stage != "request":
                log.warning("removeHeader only valid in request stage")
                return False
            log.debug("collect remove header", extra={"ctx": {"rule": rule.id, "header": action.name}})
            col = col  # type: _RequestCollector
            col.headers_remove.add(action.name.lower())
            return False

        if at == "setUrl":
            if stage != "request":
                log.warning("setUrl only valid in request stage")
                return False
            log.debug("collect set url", extra={"ctx": {"rule": rule.id, "url": str(action.value)}})
            col = col  # type: _RequestCollector
            col.url = str(action.value)
            return False

        if at == "setMethod":
            if stage != "request":
                log.warning("setMethod only valid in request stage")
                return False
            log.debug("collect set method", extra={"ctx": {"rule": rule.id, "method": str(action.value)}})
            col = col  # type: _RequestCollector
            col.method = str(action.value)
            return False

        if at == "setQueryParam":
            if stage != "request":
                log.warning("setQueryParam only valid in request stage")
                return False
            log.debug("collect set query param", extra={"ctx": {"rule": rule.id, "param": action.name}})
            col = col  # type: _RequestCollector
            col.query_set[action.name] = str(action.value)
            return False

        if at == "removeQueryParam":
            if stage != "request":
                log.warning("removeQueryParam only valid in request stage")
                return False
            log.debug("collect remove query param", extra={"ctx": {"rule": rule.id, "param": action.name}})
            col = col  # type: _RequestCollector
            col.query_remove.add(action.name)
            return False

        if at == "setCookie":
            if stage == "response":
                log.debug("collect set response cookie", extra={"ctx": {"rule": rule.id, "cookie": action.name}})
                col = col  # type: _ResponseCollector
                col.headers_cookies_set[action.name] = str(action.value)
                return False
            log.debug("collect set cookie", extra={"ctx": {"rule": rule.id, "cookie": action.name}})
            col = col  # type: _RequestCollector
            col.cookies_set[action.name] = str(action.value)
            return False

        if at == "removeCookie":
            if stage == "response":
                log.debug("collect remove response cookie", extra={"ctx": {"rule": rule.id, "cookie": action.name}})
                col = col  # type: _ResponseCollector
                col.headers_cookies_remove.add(action.name)
                return False
            log.debug("collect remove cookie", extra={"ctx": {"rule": rule.id, "cookie": action.name}})
            col = col  # type: _RequestCollector
            col.cookies_remove.add(action.name)
            return False

        if at == "setFormField":
            if stage != "request":
                log.warning("setFormField only valid in request stage")
                return False
            log.debug("collect set form field", extra={"ctx": {"rule": rule.id, "field": action.name}})
            col = col  # type: _RequestCollector
            col.form_fields_set[action.name] = str(action.value)
            return False

        if at == "removeFormField":
            if stage != "request":
                log.warning("removeFormField only valid in request stage")
                return False
            log.debug("collect remove form field", extra={"ctx": {"rule": rule.id, "field": action.name}})
            col = col  # type: _RequestCollector
            col.form_fields_remove.add(action.name)
            return False

        if at == "setStatus":
            if stage != "response":
                log.warning("setStatus only valid in response stage, passing through")
                return False
            log.debug("collect set status", extra={"ctx": {"rule": rule.id, "status": action.status_code}})
            col = col  # type: _ResponseCollector
            col.status_code = action.status_code
            return False

        if at == "setBody":
            body = action.body or str(action.value)
            if stage == "response":
                log.debug("collect set response body", extra={"ctx": {"rule": rule.id, "bodyLen": len(body)}})
                col = col  # type: _ResponseCollector
                col.body_set = body
                return False
            log.debug("collect set request body", extra={"ctx": {"rule": rule.id, "bodyLen": len(body)}})
            col = col  # type: _RequestCollector
            col.body_set = body
            return False

        if at == "appendBody":
            if stage == "response":
                log.debug("collect append response body", extra={"ctx": {"rule": rule.id}})
                col = col  # type: _ResponseCollector
                col.body_appends.append(str(action.value))
                return False
            log.debug("collect append request body", extra={"ctx": {"rule": rule.id}})
            col = col  # type: _RequestCollector
            col.body_appends.append(str(action.value))
            return False

        if at == "replaceBodyText":
            if stage == "response":
                col = col  # type: _ResponseCollector
                col.body_replacements.append((action.search, action.replace, action.replace_all))
                log.debug("collect replace response body text", extra={"ctx": {"rule": rule.id, "search": action.search}})
                return False
            col = col  # type: _RequestCollector
            col.body_replacements.append((action.search, action.replace, action.replace_all))
            log.debug("collect replace request body text", extra={"ctx": {"rule": rule.id, "search": action.search}})
            return False

        if at == "patchBodyJson":
            if stage == "response":
                col = col  # type: _ResponseCollector
                col.body_patches.extend(action.patches)
                log.debug("collect patch response body json", extra={"ctx": {"rule": rule.id}})
                return False
            col = col  # type: _RequestCollector
            col.body_patches.extend(action.patches)
            log.debug("collect patch request body json", extra={"ctx": {"rule": rule.id}})
            return False

        if at == "replaceElement":
            if stage != "response":
                log.warning("replaceElement only valid in response stage")
                return False
            col = col  # type: _ResponseCollector
            col.element_replacements.append((action.selector, str(action.value) if action.value is not None else ""))
            log.debug("collect replace element", extra={"ctx": {"rule": rule.id, "selector": action.selector}})
            return False

        # Unknown action
        log.warning(f"unsupported action {at!r}, passing through")
        return False

    # ------------------------------------------------------------------
    # Apply (imperative — merged collector → one CDP call)
    # ------------------------------------------------------------------

    async def _apply_request(
        self,
        ev: dict[str, Any],
        col: _RequestCollector,
        request_id: str,
    ) -> None:
        """Merge all collected request modifications into one continueRequest."""
        log = get_logger()
        req = ev.get("request", {})
        original_hdrs = _parse_headers(req.get("headers", {}))

        # --- block (terminal) ---
        if col.blocked:
            headers = [
                {"name": k, "value": v} for k, v in col.block_headers.items()
            ] or None
            await self._cdp.fulfill_request(
                request_id, col.block_status_code,
                response_headers=headers,
                body=col.block_body or None,
            )
            return

        # --- headers ---
        # Start from original, apply set/remove
        merged_hdrs = dict(original_hdrs)
        for k, v in col.headers_set.items():
            # Remove existing header with different case before setting
            merged_hdrs = {
                hk: hv for hk, hv in merged_hdrs.items()
                if hk.lower() != k.lower()
            }
            merged_hdrs[k] = v
        for k in col.headers_remove:
            merged_hdrs = {
                hk: hv for hk, hv in merged_hdrs.items()
                if hk.lower() != k
            }

        # --- cookies ---
        # Merge cookie modifications into the Cookie header
        cookie_str = merged_hdrs.get("Cookie", "")
        cookies = _parse_cookie_string(cookie_str) if cookie_str else {}
        for k in col.cookies_remove:
            cookies.pop(k, None)
        for k, v in col.cookies_set.items():
            cookies[k] = v
        if cookies:
            merged_hdrs["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
        elif "Cookie" in merged_hdrs:
            del merged_hdrs["Cookie"]

        # --- URL + query ---
        final_url = col.url if col.url is not None else _req_url(ev)
        if col.query_set or col.query_remove:
            final_url = _apply_query_mods(final_url, col.query_set, col.query_remove)

        # --- method ---
        final_method = col.method

        # --- body ---
        post_data: str | None = None
        has_form = bool(col.form_fields_set or col.form_fields_remove)

        if col.body_set is not None:
            post_data = col.body_set
            # Auto-add Content-Type: application/json for JSON-looking bodies
            content_type = merged_hdrs.get("Content-Type", "")
            if (col.body_set.startswith("{") or col.body_set.startswith("[")) and "json" not in content_type.lower():
                merged_hdrs["Content-Type"] = "application/json"
        elif has_form or col.body_appends or col.body_replacements or col.body_patches:
            body_str = _get_post_data_str(req) or ""
            if has_form:
                content_type = merged_hdrs.get("Content-Type", "")
                body_str = _apply_form_field_mods(
                    body_str, content_type,
                    col.form_fields_set, col.form_fields_remove,
                    log,
                )
            body_str = _apply_body_transforms(
                body_str, col.body_appends,
                col.body_replacements, col.body_patches,
            )
            post_data = body_str

        # Only pass post_data if non-empty (empty string would override a valid None)
        if not post_data:
            post_data = None

        # Build final header list (after body section may have modified Content-Type)
        hdr_list = [{"name": k, "value": v} for k, v in merged_hdrs.items()]

        log.debug(
            "merged request modifications",
            extra={
                "ctx": {
                    "url": final_url,
                    "method": final_method,
                    "bodyLen": len(post_data) if post_data else 0,
                }
            },
        )
        await self._cdp.continue_request(
            request_id,
            url=final_url if final_url != _req_url(ev) else None,
            method=final_method,
            headers=hdr_list if hdr_list != _event_hdrs_to_list(original_hdrs) else None,
            post_data=post_data,
        )

    async def _apply_response(
        self,
        ev: dict[str, Any],
        col: _ResponseCollector,
        request_id: str,
    ) -> None:
        """Merge all collected response modifications into one fulfillRequest."""
        log = get_logger()
        resp_hdrs_raw = ev.get("responseHeaders")
        resp_hdrs = _parse_headers(resp_hdrs_raw or [])
        content_encoding = resp_hdrs.get("Content-Encoding", "")

        status = col.status_code or 200

        # --- response cookies ---
        cookie_hdrs_raw = list(resp_hdrs_raw or [])
        cookies_modified = False
        if col.headers_cookies_set or col.headers_cookies_remove:
            cookies_modified = True
            for k, v in col.headers_cookies_set.items():
                cookie_hdrs_raw = _modify_response_cookie(
                    cookie_hdrs_raw, k, v
                )
            for k in col.headers_cookies_remove:
                cookie_hdrs_raw = _remove_response_cookie(
                    cookie_hdrs_raw, k
                )

        # --- body ---
        if col.body_set is not None:
            final_body = col.body_set
        elif col.has_body_mods:
            try:
                resp = await self._cdp.get_response_body(request_id)
            except Exception:
                log.error("failed to get response body, passing through")
                await self._cdp.continue_response(request_id)
                return
            body_text = _decode_response_body(resp, content_encoding)
            body_text = _apply_body_transforms(
                body_text, col.body_appends,
                col.body_replacements, col.body_patches,
            )
            body_text = _apply_element_replacements(body_text, col.element_replacements, log)
            final_body = body_text
        elif status != 200:
            # Status changed without body changes — fulfill with original body
            try:
                resp = await self._cdp.get_response_body(request_id)
            except Exception:
                await self._cdp.continue_response(request_id)
                return
            final_body = _decode_response_body(resp, content_encoding)
        else:
            # No body/status modifications — just continue
            # Only pass headers if cookies were modified; never strip
            # Content-Encoding here since the body is still compressed.
            if cookies_modified and cookie_hdrs_raw:
                await self._cdp.continue_response(
                    request_id, response_headers=cookie_hdrs_raw,
                )
            else:
                await self._cdp.continue_response(request_id)
            return

        # Strip Content-Encoding/Content-Length since body was decoded above
        final_hdrs = _clean_resp_headers(cookie_hdrs_raw)

        log.debug(
            "merged response modifications",
            extra={"ctx": {"status": status, "bodyLen": len(final_body)}},
        )
        await self._cdp.fulfill_request(
            request_id, status,
            response_headers=final_hdrs,
            body=final_body,
        )

    # ------------------------------------------------------------------
    # Continue helpers (retained for tests and direct use)
    # ------------------------------------------------------------------

    async def _continue(
        self,
        ev: dict[str, Any],
        stage: str,
        headers: list[dict[str, str]] | None = None,
    ) -> None:
        request_id: str = ev["requestId"]
        if stage == "response":
            if headers is not None:
                await self._cdp.continue_response(request_id, response_headers=headers)
            else:
                await self._cdp.continue_response(request_id)
        else:
            await self._cdp.continue_request(request_id, headers=headers)



# ===================================================================
# Helper functions
# ===================================================================


def _req_url(ev: dict[str, Any]) -> str:
    return ev.get("request", {}).get("url", "")


# -------------------------------------------------------------------
# Regex
# -------------------------------------------------------------------


def _match_regex(pattern: str, s: str) -> bool:
    if not pattern:
        return False
    compiled = _get_regex(pattern)
    return compiled is not None and bool(compiled.search(s))


# -------------------------------------------------------------------
# Headers
# -------------------------------------------------------------------


def _parse_headers(raw: dict[str, Any] | list[Any]) -> dict[str, str]:
    if isinstance(raw, dict):
        return {k: str(v) for k, v in raw.items()}
    result: dict[str, str] = {}
    for item in raw:
        if isinstance(item, dict):
            result[item.get("name", "")] = str(item.get("value", ""))
    return result


def _header_has_key(headers: dict[str, str], name: str) -> bool:
    low = name.lower()
    return any(k.lower() == low for k in headers)


def _header_get(headers: dict[str, str], name: str) -> str:
    low = name.lower()
    for k, v in headers.items():
        if k.lower() == low:
            return v
    return ""


# -------------------------------------------------------------------
# Collector apply helpers
# -------------------------------------------------------------------


def _parse_cookie_string(raw: str) -> dict[str, str]:
    """Parse a Cookie header value string into a dict."""
    if not raw:
        return {}
    cookies: dict[str, str] = {}
    for pair in raw.split(";"):
        pair = pair.strip()
        if not pair:
            continue
        if "=" in pair:
            k, _, v = pair.partition("=")
            cookies[k.strip()] = v.strip()
        else:
            cookies[pair] = ""
    return cookies


def _event_hdrs_to_list(hdrs: dict[str, str]) -> list[dict[str, str]]:
    """Convert a parsed headers dict back to CDP list format."""
    return [{"name": k, "value": v} for k, v in hdrs.items()]


def _apply_query_mods(
    url: str, set_q: dict[str, str], remove_q: set[str],
) -> str:
    """Apply multiple query parameter modifications to a URL."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    for k in remove_q:
        params.pop(k, None)
    for k, v in set_q.items():
        params[k] = [v]
    new_query = urllib.parse.urlencode(params, doseq=True)
    return parsed._replace(query=new_query).geturl()


def _apply_form_field_mods(
    body_str: str,
    content_type: str,
    set_fields: dict[str, str],
    remove_fields: set[str],
    log: Any,
) -> str:
    """Apply form field set/remove operations to a request body.

    Handles both urlencoded and multipart/form-data content types.
    """
    if not body_str:
        return body_str
    if not set_fields and not remove_fields:
        return body_str

    if "multipart/form-data" in content_type:
        boundary = _extract_boundary(content_type)
        if not boundary:
            log.warning("form field mod: cannot extract multipart boundary")
            return body_str
        body_bytes = body_str.encode("utf-8")
        for k in remove_fields:
            try:
                body_bytes = _remove_multipart_field(body_bytes, boundary, k)
            except Exception as e:
                log.error(f"form field mod: multipart remove failed: {e}")
        for k, v in set_fields.items():
            try:
                body_bytes = _set_multipart_field(body_bytes, boundary, k, v)
            except Exception as e:
                log.error(f"form field mod: multipart set failed: {e}")
        return body_bytes.decode("utf-8", errors="replace")

    # urlencoded
    result = body_str.encode("utf-8", errors="replace")
    for k in remove_fields:
        result = _remove_form_field_value(result, k)  # type: ignore[arg-type]
    for k, v in set_fields.items():
        result = _set_form_field_value(result, k, v)  # type: ignore[arg-type]
    return result.decode("utf-8", errors="replace")


def _apply_body_transforms(
    body: str,
    appends: list[str],
    replacements: list[tuple[str, str, bool]],
    patches: list[JSONPatch],
) -> str:
    """Chain body transforms: replacements → patches → appends."""
    result = body
    for search, replace, replace_all in replacements:
        if replace_all:
            result = result.replace(search, replace)
        else:
            result = result.replace(search, replace, 1)
    if patches:
        result = _apply_json_patch(result, patches)
    for suffix in appends:
        result += suffix
    return result


def _apply_element_replacements(
    body: str,
    element_reps: list[tuple[str, str]],
    log: Any,
) -> str:
    """Apply HTML element replacements via CSS selectors."""
    if not element_reps:
        return body
    try:
        soup = BeautifulSoup(body, "html.parser")
    except Exception:
        return body
    for selector, replacement in element_reps:
        elements = soup.select(selector)
        if not elements:
            log.warning(
                f"replaceElement: selector {selector!r} matched no elements"
            )
            continue
        for el in elements:
            el.clear()
            el.append(BeautifulSoup(replacement, "html.parser"))
    return str(soup)


# -------------------------------------------------------------------
# Cookies
# -------------------------------------------------------------------


def _parse_cookies(headers: dict[str, str]) -> dict[str, str]:
    val = _header_get(headers, "Cookie")
    if not val:
        return {}
    cookies: dict[str, str] = {}
    for pair in val.split(";"):
        pair = pair.strip()
        if not pair:
            continue
        if "=" in pair:
            k, _, v = pair.partition("=")
            cookies[k.strip()] = v.strip()
        else:
            cookies[pair] = ""
    return cookies


def _match_cookie(cond: Condition, cookies: dict[str, str]) -> bool:
    if cond.type.value == "cookieExists":
        return cond.name in cookies
    if cond.type.value == "cookieNotExists":
        return cond.name not in cookies
    if cond.type.value == "cookieEquals":
        return cookies.get(cond.name) == cond.value
    if cond.type.value == "cookieContains":
        return cond.value in cookies.get(cond.name, "")
    if cond.type.value == "cookieRegex":
        return _match_regex(cond.pattern, cookies.get(cond.name, ""))
    return False


# -------------------------------------------------------------------
# Query parameters
# -------------------------------------------------------------------


def _parse_query(url: str) -> dict[str, str]:
    queries: dict[str, str] = {}
    if "?" not in url:
        return queries
    raw = url.split("?", 1)[1]
    if "#" in raw:
        raw = raw.split("#", 1)[0]
    for pair in raw.split("&"):
        if "=" in pair:
            k, _, v = pair.partition("=")
            queries[urllib.parse.unquote(k)] = urllib.parse.unquote(v)
        elif pair:
            queries[urllib.parse.unquote(pair)] = ""
    return queries


def _match_query(cond: Condition, queries: dict[str, str]) -> bool:
    if cond.type.value == "queryExists":
        return cond.name in queries
    if cond.type.value == "queryNotExists":
        return cond.name not in queries
    if cond.type.value == "queryEquals":
        return queries.get(cond.name) == cond.value
    if cond.type.value == "queryContains":
        return cond.value in queries.get(cond.name, "")
    if cond.type.value == "queryRegex":
        return _match_regex(cond.pattern, queries.get(cond.name, ""))
    return False


# -------------------------------------------------------------------
# URL query param manipulation
# -------------------------------------------------------------------


def _set_query_param_value(raw_url: str, name: str, value: str) -> str:
    parsed = urllib.parse.urlparse(raw_url)
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    params[name] = [value]
    new_query = urllib.parse.urlencode(params, doseq=True)
    return parsed._replace(query=new_query).geturl()


def _remove_query_param_value(raw_url: str, name: str) -> str:
    parsed = urllib.parse.urlparse(raw_url)
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    params.pop(name, None)
    new_query = urllib.parse.urlencode(params, doseq=True)
    return parsed._replace(query=new_query).geturl()


# -------------------------------------------------------------------
# Post data
# -------------------------------------------------------------------


def _get_post_data(req: dict[str, Any]) -> bytes | None:
    s = _get_post_data_str(req)
    return s.encode("utf-8") if s else None


def _get_post_data_str(req: dict[str, Any]) -> str:
    has_post = req.get("hasPostData", False)
    entries = req.get("postDataEntries") or []

    if has_post and entries:
        parts: list[str] = []
        for entry in entries:
            raw_bytes = entry.get("bytes", "")
            if raw_bytes:
                try:
                    parts.append(base64.b64decode(raw_bytes).decode("utf-8", errors="replace"))
                except Exception:
                    parts.append(raw_bytes)
        return "".join(parts)

    post_data = req.get("postData")
    return post_data or ""


# -------------------------------------------------------------------
# Body matching
# -------------------------------------------------------------------


def _match_body(cond: Condition, body: str) -> bool:
    if not body:
        return False
    if cond.type.value == "bodyContains":
        return cond.value in body
    if cond.type.value == "bodyRegex":
        return _match_regex(cond.pattern, body)
    if cond.type.value == "bodyJsonPath":
        return _match_body_json_path(body, cond.path, cond.value)
    return False


def _match_body_json_path(body: str, path: str, expected: str) -> bool:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return False
    try:
        actual = _resolve_json_path(data, path)
        return _json_value_to_str(actual) == expected
    except (KeyError, IndexError, TypeError):
        return False


def _json_value_to_str(value: Any) -> str:
    """Convert a JSON value to the string representation it would have in JSON."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


def _resolve_json_path(data: Any, path: str) -> Any:
    """Resolve a simplified JSONPath (slash-delimited, e.g. /foo/0/bar)."""
    path = path.strip("/")
    if not path:
        return data
    segments = path.split("/")
    current = data
    for seg in segments:
        if isinstance(current, dict):
            current = current[seg]
        elif isinstance(current, list):
            current = current[int(seg)]
        else:
            raise TypeError(f"cannot index into {type(current)}")
    return current


# -------------------------------------------------------------------
# Form field manipulation
# -------------------------------------------------------------------


def _set_form_field_value(body: bytes, name: str, value: str) -> bytes:
    try:
        vals = urllib.parse.parse_qs(body.decode("utf-8", errors="replace"))
    except Exception:
        return body
    vals[name] = [value]
    return urllib.parse.urlencode(vals, doseq=True).encode("utf-8")


def _remove_form_field_value(body: bytes, name: str) -> bytes:
    try:
        vals = urllib.parse.parse_qs(body.decode("utf-8", errors="replace"))
    except Exception:
        return body
    vals.pop(name, None)
    return urllib.parse.urlencode(vals, doseq=True).encode("utf-8")


def _extract_boundary(content_type: str) -> str:
    for part in content_type.split(";"):
        part = part.strip()
        if part.lower().startswith("boundary"):
            b = part.split("=", 1)[-1].strip()
            if b.startswith('"') and b.endswith('"'):
                b = b[1:-1]
            return b
    return ""


def _set_multipart_field(body: bytes, boundary: str, field_name: str, new_value: str) -> bytes:
    return _modify_multipart(body, boundary, field_name, _set_multipart_handler(field_name, new_value))


def _remove_multipart_field(body: bytes, boundary: str, field_name: str) -> bytes:
    return _modify_multipart(body, boundary, field_name, _remove_multipart_handler(boundary, field_name))


def _set_multipart_handler(field_name: str, new_value: str):
    def handler(lines: list[str]) -> list[str]:
        for i, line in enumerate(lines):
            if f'name="{field_name}"' in line:
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() == "" and j + 1 < len(lines):
                        lines[j + 1] = new_value
                        break
                break
        return lines
    return handler


def _remove_multipart_handler(boundary: str, field_name: str):
    def handler(lines: list[str]) -> list[str]:
        start = -1
        end = -1
        for i, line in enumerate(lines):
            if start == -1 and f'name="{field_name}"' in line:
                start = i - 1
            if start != -1 and line.startswith(f"--{boundary}") and i > start + 1:
                end = i
                break
        if start >= 0 and end > start:
            for i in range(start, end):
                lines[i] = _DEL
        return lines

    return handler


def _modify_multipart(
    body: bytes, boundary: str, field_name: str, handler_fn
) -> bytes:
    text = body.decode("utf-8", errors="replace")
    lines = text.split("\r\n")
    lines = handler_fn(lines)
    result = [line for line in lines if line is not _DEL]
    return "\r\n".join(result).encode("utf-8")


# -------------------------------------------------------------------
# Cookie header manipulation
# -------------------------------------------------------------------


def _modify_cookie_header(
    headers: dict[str, str], name: str, value: str
) -> list[dict[str, str]]:
    cookie_val = _header_get(headers, "Cookie")
    pairs = _parse_cookie_pairs(cookie_val)
    pairs[name] = value
    new_cookie = "; ".join(f"{k}={v}" for k, v in pairs.items())
    return _build_header_entries(headers, "Cookie", new_cookie)


def _remove_cookie_from_header(
    headers: dict[str, str], name: str
) -> list[dict[str, str]]:
    cookie_val = _header_get(headers, "Cookie")
    pairs = _parse_cookie_pairs(cookie_val)
    pairs.pop(name, None)
    new_cookie = "; ".join(f"{k}={v}" for k, v in pairs.items())
    return _build_header_entries(headers, "Cookie", new_cookie if pairs else "")


def _parse_cookie_pairs(cookie_str: str) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for part in cookie_str.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, _, v = part.partition("=")
            pairs[k] = v
        else:
            pairs[part] = ""
    return pairs


def _build_header_entries(
    headers: dict[str, str], skip_key: str, new_value: str
) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    skip_low = skip_key.lower()
    replaced = False
    for k, v in headers.items():
        if k.lower() == skip_low:
            if new_value:
                entries.append({"name": k, "value": new_value})
                replaced = True
            continue
        entries.append({"name": k, "value": v})
    if not replaced and new_value:
        entries.append({"name": "Cookie", "value": new_value})
    return entries


# -------------------------------------------------------------------
# Response cookie manipulation
# -------------------------------------------------------------------


def _modify_response_cookie(
    resp_headers: list[dict[str, Any]], name: str, value: str
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    found = False
    for h in resp_headers:
        h_name = h.get("name", "")
        if h_name.lower() == "set-cookie":
            cookie_str = str(h.get("value", ""))
            existing_name = cookie_str.split("=", 1)[0] if "=" in cookie_str else cookie_str
            if existing_name.lower() == name.lower():
                result.append({"name": "Set-Cookie", "value": f"{name}={value}"})
                found = True
                continue
        result.append({"name": h_name, "value": str(h.get("value", ""))})
    if not found:
        result.append({"name": "Set-Cookie", "value": f"{name}={value}"})
    return result


def _remove_response_cookie(
    resp_headers: list[dict[str, Any]], name: str
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for h in resp_headers:
        h_name = h.get("name", "")
        if h_name.lower() == "set-cookie":
            cookie_str = str(h.get("value", ""))
            existing_name = cookie_str.split("=", 1)[0] if "=" in cookie_str else cookie_str
            if existing_name.lower() == name.lower():
                continue
        result.append({"name": h_name, "value": str(h.get("value", ""))})
    return result


# -------------------------------------------------------------------
# Response body
# -------------------------------------------------------------------


def _decompress_body(body: bytes, content_encoding: str) -> bytes:
    """Decompress HTTP response body based on Content-Encoding header."""
    enc = content_encoding.lower().strip()
    if enc in ("gzip", "x-gzip"):
        return gzip.decompress(body)
    if enc == "deflate":
        import zlib
        return zlib.decompress(body)
    if enc == "br":
        try:
            import brotli  # type: ignore[import-untyped]
            return brotli.decompress(body)
        except ImportError:
            pass
    return body


def _decode_response_body(
    resp: dict[str, Any], content_encoding: str = ""
) -> str:
    """Decode CDP response body, handling base64 and Content-Encoding."""
    body: Any = resp.get("body", "")
    if resp.get("base64Encoded"):
        try:
            body = base64.b64decode(body)
        except Exception:
            return str(body)
    elif isinstance(body, str):
        body = body.encode("utf-8", errors="replace")
    elif not isinstance(body, bytes):
        body = str(body).encode("utf-8", errors="replace")

    if content_encoding and isinstance(body, bytes):
        try:
            body = _decompress_body(body, content_encoding)
        except Exception:
            pass

    if isinstance(body, bytes):
        return body.decode("utf-8", errors="replace")
    return str(body)


def _clean_resp_headers(
    headers: list[dict[str, str]] | None,
) -> list[dict[str, str]] | None:
    """Remove Content-Encoding and Content-Length from response headers.

    These headers become stale when the body is decompressed or modified.
    """
    if headers is None:
        return None
    return [
        h for h in headers
        if h.get("name", "").lower() not in ("content-encoding", "content-length")
    ]


# -------------------------------------------------------------------
# JSON Patch (RFC 6902)
# -------------------------------------------------------------------


def _apply_json_patch(body: str, patches: list[JSONPatch]) -> str:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise ValueError("body is not valid JSON")

    for p in patches:
        jp = _json_path(p.path)
        jf = _json_path(p.from_) if p.from_ else ""

        try:
            if p.op.value in ("add", "replace"):
                _json_set(data, jp, p.value)
            elif p.op.value == "remove":
                _json_delete(data, jp)
            elif p.op.value == "move":
                src_val = _json_get(data, jf)
                _json_delete(data, jf)
                _json_set(data, jp, src_val)
            elif p.op.value == "copy":
                src_val = _json_get(data, jf)
                _json_set(data, jp, src_val)
            elif p.op.value == "test":
                actual = _json_get(data, jp)
                if str(actual) != str(p.value):
                    raise ValueError(f"test failed: {actual} != {p.value}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"patch {p.op.value} {p.path}: {e}")

    return json.dumps(data, ensure_ascii=False)


def _json_path(path: str) -> list[str]:
    """Convert /foo/0/bar to ['foo', '0', 'bar']."""
    return [seg for seg in path.strip("/").split("/") if seg]


def _json_get(obj: Any, segments: list[str]) -> Any:
    current = obj
    for seg in segments:
        if isinstance(current, dict):
            current = current[seg]
        elif isinstance(current, list):
            current = current[int(seg)]
        else:
            raise TypeError(f"cannot index into {type(current)}")
    return current


def _json_set(obj: Any, segments: list[str], value: Any) -> None:
    current = obj
    for i, seg in enumerate(segments[:-1]):
        if isinstance(current, dict):
            current = current[seg]
        elif isinstance(current, list):
            current = current[int(seg)]
    last = segments[-1]
    if isinstance(current, list):
        current[int(last)] = value
    else:
        current[last] = value


def _json_delete(obj: Any, segments: list[str]) -> None:
    current = obj
    for seg in segments[:-1]:
        if isinstance(current, dict):
            current = current[seg]
        elif isinstance(current, list):
            current = current[int(seg)]
    last = segments[-1]
    if isinstance(current, list):
        del current[int(last)]
    else:
        del current[last]
