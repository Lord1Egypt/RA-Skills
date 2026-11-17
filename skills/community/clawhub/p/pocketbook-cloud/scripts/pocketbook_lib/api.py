from __future__ import annotations

import http.client
import json
import os
import ssl
import stat
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from .common import (
    API_ORIGIN, PUBLIC_CLIENT_ID, PUBLIC_CLIENT_SECRET, USER_AGENT, PAGE_SIZE,
    DEFAULT_MAX_API_RESPONSE, DEFAULT_MAX_API_ERROR_RESPONSE, DEFAULT_MAX_UPLOAD,
    DEFAULT_MIN_SAFE_EPUB_BYTES, AuthRequired, AmbiguousProvider, NotFound,
    PocketBookError, Response, UnsafeOperation, _read_limited, env_bytes, env_int,
)
from .state import FileLock, SessionStore
from .formats import (canonical_upload_name, guess_mime, inspect_upload_input,
                      is_fb2_xml, supported_filename, verify_uploaded_record)
from .models import normalize_note

class StrictApiRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        p = urlparse(newurl)
        if (
            p.scheme != "https"
            or p.hostname != "cloud.pocketbook.digital"
            or (p.port not in (None, 443))
            or p.username
            or p.password
        ):
            raise UnsafeOperation("PocketBook API attempted an unsafe redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def _contract_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PocketBookError(f"PocketBook API schema changed: {context} is not an object")
    return value

def _contract_items(value: Any, context: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise PocketBookError(f"PocketBook API schema changed: {context} is not a list")
    if len(value) > 100000:
        raise UnsafeOperation(f"PocketBook API returned too many {context} items")
    if any(not isinstance(item, dict) for item in value):
        raise PocketBookError(f"PocketBook API schema changed: {context} contains a non-object item")
    return list(value)

def _contract_nonnegative_int(value: Any, context: str) -> int:
    if isinstance(value, bool):
        raise PocketBookError(f"PocketBook API schema changed: {context} is invalid")
    if isinstance(value, int):
        out = value
    elif isinstance(value, str) and value.isdigit():
        out = int(value)
    else:
        raise PocketBookError(f"PocketBook API schema changed: {context} is not an integer")
    if out < 0:
        raise PocketBookError(f"PocketBook API schema changed: {context} is negative")
    return out

def _parse_providers_payload(value: Any) -> list[dict[str, Any]]:
    data = _contract_dict(value, "provider discovery response")
    providers = _contract_items(data.get("providers"), "providers")
    for provider in providers:
        if not isinstance(provider.get("alias"), str) or not provider.get("alias"):
            raise PocketBookError("PocketBook API schema changed: provider alias is missing")
        if not isinstance(provider.get("shop_id"), (str, int)) or str(provider.get("shop_id")) == "":
            raise PocketBookError("PocketBook API schema changed: provider shop_id is missing")
    return providers


def _parse_token_payload(value: Any, *, require_refresh: bool) -> tuple[str, str | None, int]:
    data = _contract_dict(value, "token response")
    access = data.get("access_token")
    refresh = data.get("refresh_token")
    if not isinstance(access, str) or not access:
        raise AuthRequired("PocketBook token response did not contain a usable access token")
    if require_refresh and (not isinstance(refresh, str) or not refresh):
        raise AuthRequired("PocketBook token response did not contain a usable refresh token")
    if refresh is not None and not isinstance(refresh, str):
        raise PocketBookError("PocketBook API schema changed: refresh_token has invalid type")
    expires_in = _contract_nonnegative_int(data.get("expires_in", 7200), "token.expires_in")
    return access, refresh or None, max(60, expires_in)


def _parse_books_page(value: Any, *, require_total: bool) -> tuple[int | None, list[dict[str, Any]]]:
    data = _contract_dict(value, "books response")
    if require_total or "total" in data:
        total = _contract_nonnegative_int(data.get("total"), "books.total")
    else:
        total = None
    items = _contract_items(data.get("items"), "books.items")
    return total, items


def _parse_notes_payload(value: Any) -> tuple[int, list[dict[str, Any]]]:
    if isinstance(value, list):
        items = _contract_items(value, "notes")
        return len(items), items
    data = _contract_dict(value, "notes response")
    items = _contract_items(data.get("items"), "notes.items")
    total = _contract_nonnegative_int(data.get("total", len(items)), "notes.total")
    return total, items

class PocketBookClient:
    def __init__(self, store: SessionStore | None = None, timeout: float = 45.0):
        self.store = store or SessionStore()
        self.timeout = timeout
        self.session = self.store.load()

    def _request(
        self,
        method: str,
        path_or_url: str,
        *,
        form: dict[str, str] | None = None,
        body: bytes | None = None,
        content_type: str | None = None,
        authenticated: bool = False,
        retry_auth: bool = True,
    ) -> Response:
        url = path_or_url if path_or_url.startswith("https://") else urljoin(API_ORIGIN + "/", path_or_url.lstrip("/"))
        parsed = urlparse(url)
        if (
            parsed.scheme != "https"
            or parsed.hostname != "cloud.pocketbook.digital"
            or parsed.port not in (None, 443)
            or parsed.username
            or parsed.password
        ):
            raise UnsafeOperation("Refusing unsafe PocketBook API URL")
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "identity",
            "Cache-Control": "no-cache",
            "User-Agent": USER_AGENT,
        }
        if authenticated:
            token = str(self.session.get("access_token") or "")
            if not token:
                raise AuthRequired("PocketBook Cloud is not authenticated")
            headers["Authorization"] = "Bearer " + token
        if form is not None:
            body = urlencode(form).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif content_type:
            headers["Content-Type"] = content_type
        req = Request(url, data=body, headers=headers, method=method)
        # Ambient HTTP(S)_PROXY variables must not change the security boundary.
        opener = build_opener(ProxyHandler({}), StrictApiRedirect())
        try:
            with opener.open(req, timeout=self.timeout) as r:
                raw = _read_limited(r, DEFAULT_MAX_API_RESPONSE, context="PocketBook API response")
                response = Response(r.status, dict(r.headers.items()), raw, r.geturl())
        except HTTPError as exc:
            raw = _read_limited(exc, DEFAULT_MAX_API_ERROR_RESPONSE, context="PocketBook API error response")
            response = Response(exc.code, dict(exc.headers.items()), raw, exc.geturl())
        except (URLError, OSError, TimeoutError) as exc:
            raise PocketBookError(f"PocketBook request failed: {type(exc).__name__}") from exc
        if authenticated and response.status == 401 and retry_auth:
            failed_access = str(self.session.get("access_token") or "")
            if self.refresh(expected_access_token=failed_access):
                return self._request(method, path_or_url, form=form, body=body if form is None else None, content_type=content_type, authenticated=True, retry_auth=False)
            raise AuthRequired("PocketBook session expired; run auth login again")
        return response

    @staticmethod
    def _require_ok(response: Response, context: str) -> Any:
        if 200 <= response.status < 300:
            return response.json()
        # Never reflect upstream error bodies: auth endpoints may echo submitted values.
        raise PocketBookError(f"{context} failed with HTTP {response.status}")

    def providers(self, email: str) -> list[dict[str, Any]]:
        q = urlencode({
            "username": email,
            "client_id": PUBLIC_CLIENT_ID,
            "client_secret": PUBLIC_CLIENT_SECRET,
            "language": "en",
        })
        data = self._require_ok(self._request("GET", f"/api/v1.0/auth/login?{q}"), "Provider discovery")
        return _parse_providers_payload(data)

    def login(self, email: str, password: str, provider_alias: str | None = None) -> dict[str, Any]:
        providers = self.providers(email)
        if not providers:
            raise AuthRequired("PocketBook returned no authentication providers for this account")
        chosen = None
        if provider_alias:
            for p in providers:
                if str(p.get("alias") or "") == provider_alias:
                    chosen = p
                    break
            if chosen is None:
                raise AuthRequired(f"PocketBook provider not found: {provider_alias}")
        elif len(providers) == 1:
            chosen = providers[0]
        else:
            password_capable = [p for p in providers if "password" in str(p.get("logged_by") or p.get("login_type") or "password").lower()]
            if len(password_capable) == 1:
                chosen = password_capable[0]
            else:
                raise AmbiguousProvider([
                    {"alias": p.get("alias"), "name": p.get("name"), "shop_id": p.get("shop_id")}
                    for p in providers
                ])
        alias = str(chosen.get("alias") or "")
        shop_id = str(chosen.get("shop_id") or "")
        if not alias or not shop_id:
            raise AuthRequired("PocketBook provider response is incomplete")
        response = self._request(
            "POST",
            f"/api/v1.0/auth/login/{quote(alias, safe='')}",
            form={
                "shop_id": shop_id,
                "username": email,
                "password": password,
                "client_id": PUBLIC_CLIENT_ID,
                "client_secret": PUBLIC_CLIENT_SECRET,
                "grant_type": "password",
                "language": "en",
            },
        )
        token = self._require_ok(response, "PocketBook login")
        access, refresh, expires_in = _parse_token_payload(token, require_refresh=True)
        assert refresh is not None
        self.session = {
            "schema": 1,
            "email": email,
            "provider_alias": alias,
            "provider_name": str(chosen.get("name") or ""),
            "shop_id": shop_id,
            "access_token": access,
            "refresh_token": refresh,
            "expires_at": int(time.time()) + expires_in - 300,
        }
        self.store.save(self.session)
        return self.auth_status()

    def refresh(self, expected_access_token: str | None = None) -> bool:
        lock_path = self.store.path.with_name(self.store.path.name + ".refresh.lock")
        with FileLock(lock_path):
            latest = self.store.load()
            if latest:
                latest_access = str(latest.get("access_token") or "")
                # Another process already refreshed the exact token that failed for us.
                if expected_access_token and latest_access and latest_access != expected_access_token:
                    self.session = latest
                    return True
                # For proactive expiry refresh, reuse a still-valid token written by another process.
                if not expected_access_token and latest_access and int(latest.get("expires_at") or 0) > int(time.time()):
                    self.session = latest
                    return True
                self.session = latest
            refresh = str(self.session.get("refresh_token") or "")
            if not refresh:
                return False
            form = {"grant_type": "refresh_token", "refresh_token": refresh}
            response = self._request(
                "POST",
                "/api/v1.0/auth/renew-token",
                form=form,
                authenticated=bool(self.session.get("access_token")),
                retry_auth=False,
            )
            if not 200 <= response.status < 300:
                # Do not clear or overwrite a previously valid session on refresh failure.
                return False
            try:
                access, new_refresh, expires_in = _parse_token_payload(response.json(), require_refresh=False)
            except PocketBookError:
                return False
            updated = dict(self.session)
            updated["access_token"] = access
            if new_refresh:
                updated["refresh_token"] = new_refresh
            updated["expires_at"] = int(time.time()) + expires_in - 300
            self.store.save(updated)
            self.session = updated
            return True

    def ensure_token(self) -> None:
        if not self.session.get("access_token") or not self.session.get("refresh_token"):
            raise AuthRequired("PocketBook Cloud is not authenticated; run auth login")
        if int(self.session.get("expires_at") or 0) <= int(time.time()):
            stale_access = str(self.session.get("access_token") or "")
            if not self.refresh(expected_access_token=stale_access):
                raise AuthRequired("PocketBook session expired; run auth login again")

    def auth_status(self) -> dict[str, Any]:
        return {
            "authenticated": bool(self.session.get("access_token") and self.session.get("refresh_token")),
            "email": self.session.get("email") or None,
            "provider": self.session.get("provider_name") or self.session.get("provider_alias") or None,
            "sessionFile": str(self.store.path),
        }

    def doctor(self) -> dict[str, Any]:
        status = self.auth_status()
        if not status["authenticated"]:
            return {"ok": False, **status, "reason": "not_authenticated"}
        self.ensure_token()
        response = self._request("GET", "/api/v1.0/user", authenticated=True)
        ok = 200 <= response.status < 300
        return {"ok": ok, **self.auth_status(), "httpStatus": response.status, "reason": None if ok else "api_error"}

    def books(self) -> list[dict[str, Any]]:
        self.ensure_token()
        total, head_items = _parse_books_page(
            self._require_ok(self._request("GET", "/api/v1.0/books?limit=0", authenticated=True), "List books"),
            require_total=True,
        )
        assert total is not None
        max_books = env_int("POCKETBOOK_MAX_LIBRARY_ITEMS", 50000)
        if total > max_books:
            raise UnsafeOperation(f"PocketBook library exceeds configured item limit ({max_books})")
        if total <= 0:
            return head_items
        out: list[dict[str, Any]] = []
        offset = 0
        while offset < total:
            limit = min(PAGE_SIZE, total - offset)
            q = urlencode({"limit": limit, "offset": offset})
            _page_total, chunk = _parse_books_page(
                self._require_ok(self._request("GET", f"/api/v1.0/books?{q}", authenticated=True), "List books"),
                require_total=False,
            )
            out.extend(chunk)
            if len(out) > max_books:
                raise UnsafeOperation(f"PocketBook library exceeds configured item limit ({max_books})")
            if not chunk:
                break
            offset += len(chunk)
        return out


    def upload(self, path: Path, remote_name: str | None = None) -> dict[str, Any]:
        path = path.expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        try:
            lst = path.lstat()
        except FileNotFoundError as exc:
            raise NotFound(f"Upload file not found: {path}") from exc
        if stat.S_ISLNK(lst.st_mode) or not stat.S_ISREG(lst.st_mode):
            raise UnsafeOperation("Upload source must be a regular non-symlink file")
        path = path.absolute()
        if path.name.casefold().endswith(".xml") and is_fb2_xml(path):
            raise UnsafeOperation("Telegram/XML FB2 must be prepared as a real .fb2.zip before upload")
        name = canonical_upload_name(path, remote_name)
        if not supported_filename(name):
            raise UnsafeOperation(f"Unsupported ebook file type: {name}")
        size = lst.st_size
        if name.casefold().endswith(".epub") and size < DEFAULT_MIN_SAFE_EPUB_BYTES:
            raise UnsafeOperation("Refusing EPUB smaller than 4 KiB: PocketBook Reader for iOS can treat such downloads as corrupted and crash during sync")
        inspection = inspect_upload_input(path)
        if inspection.get("action") != "direct":
            raise UnsafeOperation("Upload input requires preparation before direct transfer")
        max_size = env_bytes("POCKETBOOK_MAX_UPLOAD_MB", DEFAULT_MAX_UPLOAD)
        if size > max_size:
            raise UnsafeOperation(f"Upload exceeds configured size limit ({max_size // (1024*1024)} MiB)")
        self.ensure_token()
        status, payload = self._upload_once(path, name, expected_stat=lst)
        if status == 401 and self.refresh():
            status, payload = self._upload_once(path, name, expected_stat=lst)
        if not 200 <= status < 300:
            raise PocketBookError(f"Upload failed with HTTP {status}")
        fast_hash = str(payload.get("fast_hash") or "") if isinstance(payload, dict) else ""
        # No server hash means there is no collision-safe way to distinguish this
        # upload from an older same-name record. Stay explicitly unverified.
        if not fast_hash:
            return {
                "ok": False, "accepted": True, "name": name, "bytes": size,
                "verified": False, "fastHash": None,
                "warning": "upload_accepted_without_fast_hash",
            }
        remote_summary: dict[str, Any] | None = None
        for _ in range(5):
            books = self.books()
            match = next((b for b in books if str(b.get("fast_hash") or "") == fast_hash), None)
            if match is not None:
                remote_summary = verify_uploaded_record(match, name, size, expected_fast_hash=fast_hash)
                break
            time.sleep(1.0)
        verified = remote_summary is not None
        return {
            "ok": verified,
            "accepted": True,
            "name": name,
            "bytes": size,
            "verified": verified,
            "fastHash": fast_hash,
            **({"remote": remote_summary} if remote_summary else {}),
            **({"warning": "upload_accepted_but_not_yet_verified"} if not verified else {}),
        }

    def _upload_once(self, path: Path, name: str, *, expected_stat: os.stat_result | None = None) -> tuple[int, dict[str, Any]]:
        token = str(self.session.get("access_token") or "")
        endpoint = "/api/v1.1/files/" + quote(name, safe="")
        conn = http.client.HTTPSConnection("cloud.pocketbook.digital", timeout=self.timeout, context=ssl.create_default_context())
        mime = guess_mime(name)
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(path, flags)
        try:
            with os.fdopen(fd, "rb", closefd=False) as fh:
                st = os.fstat(fd)
                if not stat.S_ISREG(st.st_mode):
                    raise UnsafeOperation("Upload source changed and is no longer a regular file")
                if expected_stat is not None:
                    before = (expected_stat.st_dev, expected_stat.st_ino, expected_stat.st_size, expected_stat.st_mtime_ns)
                    current = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)
                    if current != before:
                        raise UnsafeOperation("Upload source changed after validation")
                size = st.st_size
                conn.putrequest("PUT", endpoint)
                conn.putheader("Authorization", "Bearer " + token)
                conn.putheader("Content-Type", mime)
                conn.putheader("Content-Length", str(size))
                conn.putheader("Accept", "application/json")
                conn.putheader("Accept-Encoding", "identity")
                conn.putheader("User-Agent", USER_AGENT)
                conn.endheaders()
                while True:
                    chunk = fh.read(1024 * 1024)
                    if not chunk:
                        break
                    conn.send(chunk)
                r = conn.getresponse()
                raw = _read_limited(r, DEFAULT_MAX_API_RESPONSE, context="PocketBook upload response")
                status = r.status
        except (OSError, http.client.HTTPException) as exc:
            raise PocketBookError(f"Upload transport failed: {type(exc).__name__}") from exc
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
            conn.close()
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            payload = {}
        return status, payload if isinstance(payload, dict) else {}

    def notes(self, book: dict[str, Any]) -> list[dict[str, Any]]:
        self.ensure_token()
        fast_hash = str(book.get("fast_hash") or "")
        if not fast_hash:
            raise NotFound("PocketBook book has no fast_hash; notes cannot be resolved")
        q = urlencode({"fast_hash": fast_hash})
        data = self._require_ok(self._request("GET", f"/api/v1.0/notes?{q}", authenticated=True), "List notes")
        total, infos = _parse_notes_payload(data)
        if isinstance(data, dict):
            offset = len(infos)
            while offset < total:
                page_q = urlencode({"fast_hash": fast_hash, "limit": PAGE_SIZE, "offset": offset})
                page = self._require_ok(self._request("GET", f"/api/v1.0/notes?{page_q}", authenticated=True), "List notes")
                _page_total, chunk = _parse_notes_payload(page)
                if not chunk:
                    break
                infos.extend(chunk)
                offset += len(chunk)
        else:
            infos = []
        out = []
        for info in infos:
            uuid = str(info.get("uuid") or "")
            if not uuid:
                continue
            detail = self._require_ok(self._request("GET", f"/api/v1.0/notes/{quote(uuid, safe='')}?{q}", authenticated=True), "Get note")
            if isinstance(detail, dict):
                out.append(normalize_note(detail, info))
        return out

    def delete(self, book: dict[str, Any]) -> dict[str, Any]:
        self.ensure_token()
        fast_hash = str(book.get("fast_hash") or "")
        if not fast_hash:
            raise NotFound("PocketBook book has no fast_hash; cannot delete")
        q = urlencode({"fast_hash": fast_hash})
        response = self._request("POST", f"/api/v1.1/fileops/delete/?{q}", authenticated=True)
        if not 200 <= response.status < 300:
            self._require_ok(response, "Delete book")
        absent = False
        for _ in range(5):
            remaining = self.books()
            absent = not any(str(b.get("fast_hash") or "") == fast_hash for b in remaining)
            if absent:
                break
            time.sleep(1.0)
        return {
            "ok": absent,
            "accepted": True,
            "deleted": absent,
            "fastHash": fast_hash,
            "state": "verified_deleted" if absent else "accepted_unverified",
            "reconcileRequired": not absent,
        }

__all__ = ['StrictApiRedirect', '_contract_dict', '_contract_items', '_contract_nonnegative_int', '_parse_providers_payload', '_parse_token_payload', '_parse_books_page', '_parse_notes_payload', 'PocketBookClient', 'ProxyHandler', 'Request', 'build_opener']
