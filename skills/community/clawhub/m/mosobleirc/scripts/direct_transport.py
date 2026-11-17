"""Direct MosOblEIRC transport.

This module implements the same public call(action, **payload) contract as
the Yandex relay client while keeping provider HTTP independent from the
cloud-function implementation.
"""
from __future__ import annotations

import http.client
import json
import os
import socket
import stat
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from mosobleirc_core import (
    MosOblEIRCError,
    RelayNetworkError,
    SecretPermissionError,
    load_inventory,
    provider_submission_verified,
)

DEFAULT_BASE_URL = "https://lkk.mosobleirc.ru"
USER_AGENT = "OpenClaw-MosOblEIRC/1.0"
READ_ATTEMPTS = 2
TRANSIENT_WRITE_STATUSES = {408, 409, 425, 429}
VERSION = "1.0.1"


def provider_base_url(value: str) -> str:
    raw = str(value or "").strip()
    try:
        parsed = urlsplit(raw)
        port = parsed.port
    except ValueError as exc:
        raise MosOblEIRCError("provider URL is invalid") from exc
    if (
        parsed.scheme.lower() != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
        or port not in (None, 443)
    ):
        raise MosOblEIRCError(
            "provider URL must be an HTTPS origin on port 443 without credentials"
        )
    return raw.rstrip("/")


def _posix_mode_supported() -> bool:
    """On Windows os.chmod cannot enforce owner-only permissions, so the
    0600 check would reject every file regardless of real ACLs."""
    return os.name == "posix"


def read_token(path: str | Path) -> str:
    """Read a token from a non-symlink regular file private to its owner."""
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(Path(path), os.O_RDONLY | nofollow | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(fd, "r", encoding="utf-8") as stream:
            info = os.fstat(stream.fileno())
            mode = stat.S_IMODE(info.st_mode)
            if not stat.S_ISREG(info.st_mode) or (
                _posix_mode_supported() and mode & 0o077
            ):
                raise SecretPermissionError(
                    "provider token file permissions must be 0600 or stricter"
                )
            token = stream.read(16385).strip()
    except SecretPermissionError:
        raise
    except (OSError, UnicodeError) as exc:
        raise MosOblEIRCError("provider token file is unavailable") from exc
    if (
        not token
        or len(token) > 16384
        or any(ch.isspace() or ord(ch) < 32 for ch in token)
    ):
        raise MosOblEIRCError("provider token file is invalid")
    return token


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _decode_json(raw: bytes):
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


def _positive_int(value, error: str) -> int:
    if isinstance(value, bool):
        raise ValueError(error)
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(error) from exc
    if result <= 0:
        raise ValueError(error)
    return result


class DirectClient:
    def __init__(
        self,
        token_path: str | Path,
        inventory_path: str | Path,
        base_url: str = DEFAULT_BASE_URL,
        *,
        opener=None,
        sleep=time.sleep,
        read_attempts: int = READ_ATTEMPTS,
    ) -> None:
        self.base_url = provider_base_url(base_url)
        self.token_path = Path(token_path).expanduser()
        self.inventory_path = Path(inventory_path).expanduser()
        self.opener = opener or urllib.request.build_opener(_NoRedirect()).open
        self.sleep = sleep
        self.read_attempts = max(1, min(int(read_attempts), 3))

    def _inventory(self) -> list[dict]:
        return load_inventory(self.inventory_path)

    def _request(self, method: str, path: str, *, payload=None, timeout=10):
        token = read_token(self.token_path)
        headers = {
            "X-Auth-Tenant-Token": token,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        body = None
        if payload is not None:
            headers["Content-Type"] = "application/json; charset=utf-8"
            body = json.dumps(
                payload, ensure_ascii=False, separators=(",", ":")
            ).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path, data=body, headers=headers, method=method
        )
        try:
            with self.opener(request, timeout=timeout) as response:
                return int(response.status), _decode_json(response.read())
        except urllib.error.HTTPError as exc:
            return int(exc.code), {}
        except (
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
            OSError,
            http.client.HTTPException,
        ):
            raise RelayNetworkError("provider network error") from None

    def _read(self, path: str):
        for attempt in range(self.read_attempts):
            try:
                status, data = self._request("GET", path, timeout=8)
            except RelayNetworkError:
                if attempt + 1 < self.read_attempts:
                    self.sleep(0)
                    continue
                raise
            if 500 <= status <= 599 and attempt + 1 < self.read_attempts:
                self.sleep(0)
                continue
            return status, data
        return 503, {}

    @staticmethod
    def _meter_entry(entries, meter_id: int):
        if not isinstance(entries, list):
            return None
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            meter = entry.get("meter")
            if not isinstance(meter, dict):
                continue
            try:
                if int(meter.get("id")) == int(meter_id):
                    return entry
            except (TypeError, ValueError):
                continue
        return None

    @staticmethod
    def _inventory_allows(inventory, item_id: int, meter_id: int) -> bool:
        for item in inventory:
            if not isinstance(item, dict):
                continue
            try:
                if int(item.get("item_id")) != int(item_id):
                    continue
            except (TypeError, ValueError):
                continue
            for meter in item.get("meters") or []:
                if not isinstance(meter, dict):
                    continue
                try:
                    if int(meter.get("meter_id")) == int(meter_id):
                        return True
                except (TypeError, ValueError):
                    continue
        return False

    @staticmethod
    def _provider_error(status: int, *, operation_id=None) -> dict:
        payload = {
            "ok": False,
            "provider_contacted": True,
            "error": "AUTH_REQUIRED" if status in (401, 403) else "MOSOBLEIRC_API_ERROR",
            "upstream_status": int(status),
        }
        if operation_id is not None:
            payload["operation_id"] = operation_id
            payload["status"] = "AUTH_REQUIRED" if status in (401, 403) else "FAILED"
        return payload

    def _readback(self, item_id: int, meter_id: int, value: int):
        try:
            status, entries = self._read(
                f"/api/api/clients/meters/for-item/{int(item_id)}"
            )
        except (RelayNetworkError, MosOblEIRCError):
            return None, False
        if not 200 <= status < 300:
            return None, False
        entry = self._meter_entry(entries, meter_id)
        verified = provider_submission_verified(
            entry or {}, value, require_current_period=True
        )
        return entry, verified

    def _local_configuration_error(self, action: str, exc: MosOblEIRCError, payload: dict):
        result = {
            "ok": False,
            "provider_contacted": False,
            "error": "TOKEN_FILE_ERROR",
            "message": str(exc)[:200],
        }
        if action == "submit":
            result.update(
                {
                    "operation_id": str(payload.get("operation_id") or ""),
                    "status": "FAILED",
                    "post_attempted": False,
                }
            )
        return result

    def call(self, action: str, **payload) -> dict:
        action = str(action)
        if action in {"ping", "status"}:
            try:
                inventory = self._inventory()
            except (OSError, ValueError, json.JSONDecodeError, MosOblEIRCError):
                inventory = []
            return {
                "ok": True,
                "service": "mosobleirc-direct",
                "provider_contacted": False,
                "token_configured": self.token_path.is_file(),
                "writes_enabled": True,
                "inventory_items": len(inventory),
                "inventory_meters": sum(
                    len(x.get("meters") or [])
                    for x in inventory
                    if isinstance(x, dict)
                ),
            }
        if action == "inventory":
            try:
                inventory = self._inventory()
            except (OSError, ValueError, json.JSONDecodeError, MosOblEIRCError):
                return {
                    "ok": False,
                    "provider_contacted": False,
                    "error": "INVENTORY_NOT_CONFIGURED",
                }
            return {"ok": True, "provider_contacted": False, "data": inventory}
        if action == "write-status":
            return {
                "ok": True,
                "provider_contacted": False,
                "writes_enabled": True,
            }

        if action == "accounts":
            path = "/api/api/clients"
        elif action == "items":
            path = "/api/api/clients/configuration-items"
        elif action == "meters":
            try:
                item_id = _positive_int(payload.get("item_id"), "INVALID_ITEM_ID")
            except ValueError as exc:
                return {"ok": False, "provider_contacted": False, "error": str(exc)}
            path = f"/api/api/clients/meters/for-item/{item_id}"
        elif action == "submit":
            return self._submit(payload)
        else:
            return {
                "ok": False,
                "provider_contacted": False,
                "error": "UNKNOWN_ACTION",
            }

        try:
            status, data = self._read(path)
        except RelayNetworkError:
            return {
                "ok": False,
                "provider_contacted": True,
                "error": "RETRYABLE_EGRESS",
            }
        except (SecretPermissionError, MosOblEIRCError) as exc:
            return self._local_configuration_error(action, exc, payload)
        if 200 <= status < 300:
            return {"ok": True, "provider_contacted": True, "data": data}
        return self._provider_error(status)

    def _submit(self, payload: dict) -> dict:
        operation_id = str(payload.get("operation_id") or "").strip()
        if not operation_id:
            return {
                "ok": False,
                "provider_contacted": False,
                "error": "OPERATION_ID_REQUIRED",
                "status": "FAILED",
                "post_attempted": False,
            }
        try:
            item_id = _positive_int(payload.get("item_id"), "INVALID_ITEM_ID")
            meter_id = _positive_int(payload.get("meter_id"), "INVALID_METER_ID")
        except ValueError as exc:
            return {
                "ok": False,
                "provider_contacted": False,
                "error": str(exc),
                "operation_id": operation_id,
                "status": "FAILED",
                "post_attempted": False,
            }
        value = payload.get("value")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return {
                "ok": False,
                "provider_contacted": False,
                "error": "INVALID_VALUE",
                "operation_id": operation_id,
                "status": "FAILED",
                "post_attempted": False,
            }
        try:
            inventory = self._inventory()
        except (OSError, ValueError, json.JSONDecodeError, MosOblEIRCError):
            return {
                "ok": False,
                "provider_contacted": False,
                "error": "INVENTORY_NOT_CONFIGURED",
                "operation_id": operation_id,
                "status": "FAILED",
                "post_attempted": False,
            }
        if not self._inventory_allows(inventory, item_id, meter_id):
            return {
                "ok": False,
                "provider_contacted": False,
                "error": "METER_BINDING_MISMATCH",
                "operation_id": operation_id,
                "status": "FAILED",
                "post_attempted": False,
            }

        write_path = (
            f"/api/api/clients/meters/{meter_id}/values?withOptionalCheck=true"
        )
        post_uncertain = False
        upstream_status = None
        try:
            upstream_status, _ = self._request(
                "POST", write_path, payload={"value1": value}, timeout=10
            )
        except RelayNetworkError:
            post_uncertain = True
        except (SecretPermissionError, MosOblEIRCError) as exc:
            return self._local_configuration_error("submit", exc, payload)

        if upstream_status in (401, 403):
            result = self._provider_error(upstream_status, operation_id=operation_id)
            result["post_attempted"] = True
            return result

        if upstream_status is not None and not (200 <= upstream_status < 300):
            if upstream_status in TRANSIENT_WRITE_STATUSES or 500 <= upstream_status <= 599:
                post_uncertain = True
            else:
                result = self._provider_error(
                    upstream_status, operation_id=operation_id
                )
                result["post_attempted"] = True
                return result

        entry, verified = self._readback(item_id, meter_id, value)
        if verified:
            return {
                "ok": True,
                "provider_contacted": True,
                "operation_id": operation_id,
                "status": (
                    "VERIFIED_AFTER_UNCERTAIN_RESPONSE"
                    if post_uncertain
                    else "VERIFIED"
                ),
                "value": value,
                "readback_meter": entry,
                "post_attempted": True,
                **(
                    {"upstream_status": upstream_status}
                    if upstream_status is not None and post_uncertain
                    else {}
                ),
            }
        result = {
            "ok": False,
            "provider_contacted": True,
            "operation_id": operation_id,
            "status": "UNCERTAIN_NO_RETRY",
            "value": value,
            "post_attempted": True,
        }
        if upstream_status is not None and post_uncertain:
            result["upstream_status"] = upstream_status
        return result
