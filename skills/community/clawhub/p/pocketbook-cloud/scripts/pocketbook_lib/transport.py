from __future__ import annotations

import http.client
import ipaddress
import os
import secrets
import socket
import ssl
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request

from .common import (DEFAULT_MAX_DOWNLOAD, DEFAULT_MAX_REDIRECTS, USER_AGENT,
                     DownloadError, NotFound, PocketBookError, UnsafeOperation,
                     _commit_temp_without_overwrite, _private_open_exclusive,
                     _read_limited, env_bytes)
from .formats import sanitize_filename
from .models import display_title

def _public_https_addresses(url: str) -> tuple[Any, list[tuple[Any, ...]]]:
    p = urlparse(url)
    if p.scheme != "https" or not p.hostname:
        raise UnsafeOperation("PocketBook download link is not HTTPS")
    if p.username or p.password:
        raise UnsafeOperation("PocketBook download link contains URL credentials")
    if p.port not in (None, 443):
        raise UnsafeOperation("PocketBook download link uses a non-default HTTPS port")
    try:
        host = p.hostname.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise UnsafeOperation("PocketBook download host is invalid") from exc
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise PocketBookError("Cannot resolve PocketBook download host") from exc
    validated: list[tuple[Any, ...]] = []
    seen: set[tuple[int, str]] = set()
    for info in infos:
        family, socktype, proto, canonname, sockaddr = info
        addr = sockaddr[0]
        try:
            ip = ipaddress.ip_address(addr)
        except ValueError as exc:
            raise UnsafeOperation("PocketBook download host resolved to an invalid address") from exc
        mapped = getattr(ip, "ipv4_mapped", None)
        if not ip.is_global or (mapped is not None and not mapped.is_global):
            raise UnsafeOperation("PocketBook download link resolves to a non-public address")
        key = (family, addr)
        if key not in seen:
            seen.add(key)
            validated.append((family, socktype, proto, canonname, sockaddr))
    if not validated:
        raise UnsafeOperation("PocketBook download host has no validated public address")
    return p, validated

def ensure_public_https(url: str) -> None:
    _public_https_addresses(url)

class SafeRedirect(HTTPRedirectHandler):
    """Compatibility validator; downloads themselves use pinned manual redirects."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        ensure_public_https(newurl)
        return Request(newurl, headers={"User-Agent": USER_AGENT, "Accept": "*/*", "Accept-Encoding": "identity"}, method="GET")

class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, addrinfo: tuple[Any, ...], timeout: float):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context())
        self._addrinfo = addrinfo

    def connect(self) -> None:
        family, socktype, proto, _canonname, sockaddr = self._addrinfo
        sock = socket.socket(family, socktype, proto)
        sock.settimeout(self.timeout)
        try:
            sock.connect(sockaddr)
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except Exception:
            sock.close()
            raise

def _open_pinned_download(url: str, timeout: float) -> tuple[http.client.HTTPSConnection, http.client.HTTPResponse, str]:
    current = url
    for redirect_count in range(DEFAULT_MAX_REDIRECTS + 1):
        parsed, infos = _public_https_addresses(current)
        host = parsed.hostname.encode("idna").decode("ascii")
        target = parsed.path or "/"
        if parsed.query:
            target += "?" + parsed.query
        last_error: Exception | None = None
        redirected = False
        for info in infos:
            conn = _PinnedHTTPSConnection(host, info, timeout)
            try:
                conn.request(
                    "GET",
                    target,
                    headers={"User-Agent": USER_AGENT, "Accept": "*/*", "Accept-Encoding": "identity"},
                )
                response = conn.getresponse()
            except (OSError, ssl.SSLError, http.client.HTTPException, TimeoutError) as exc:
                last_error = exc
                conn.close()
                continue
            if response.status in {301, 302, 303, 307, 308}:
                location = response.getheader("Location")
                try:
                    _read_limited(response, 64 * 1024, context="PocketBook redirect response")
                finally:
                    conn.close()
                if not location:
                    raise DownloadError("Download redirect did not include a Location header")
                if redirect_count >= DEFAULT_MAX_REDIRECTS:
                    raise DownloadError("Download redirect limit exceeded")
                current = urljoin(current, location)
                # Validate now; the next loop resolves and pins the new destination.
                ensure_public_https(current)
                redirected = True
                break
            return conn, response, current
        if redirected:
            continue
        if last_error is not None:
            raise DownloadError(f"Download failed: {type(last_error).__name__}", retryable=True) from last_error
        raise DownloadError("Download failed: no reachable validated address", retryable=True)
    raise DownloadError("Download redirect limit exceeded")

def download_book(book: dict[str, Any], output_dir: Path, timeout: float = 60.0) -> dict[str, Any]:
    if bool(book.get("isDrm") or book.get("is_drm") or book.get("isLcp") or book.get("is_lcp")):
        raise UnsafeOperation("PocketBook marks this book as DRM/LCP protected; download bypass is not attempted")
    link = str(book.get("link") or "")
    if not link:
        raise NotFound("PocketBook did not provide a download link for this book")
    ensure_public_https(link)
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    name = sanitize_filename(str(book.get("name") or "") or (display_title(book) + ("." + str(book.get("format"))) if book.get("format") else ""))
    target = (output_dir / name).resolve()
    if target.parent != output_dir:
        raise UnsafeOperation("Unsafe download filename")
    if target.exists():
        marker = str(book.get("fast_hash") or book.get("id") or "duplicate")[:8]
        suffixes = "".join(target.suffixes)
        stem = target.name[:-len(suffixes)] if suffixes else target.name
        candidate = (output_dir / f"{stem} [{marker}]{suffixes}").resolve()
        n = 2
        while candidate.exists():
            candidate = (output_dir / f"{stem} [{marker}-{n}]{suffixes}").resolve()
            n += 1
        target = candidate
        if target.parent != output_dir:
            raise UnsafeOperation("Unsafe download filename")
    max_size = env_bytes("POCKETBOOK_MAX_DOWNLOAD_MB", DEFAULT_MAX_DOWNLOAD)
    part = target.with_name(target.name + f".part.{os.getpid()}.{secrets.token_hex(4)}")
    total = 0
    conn: http.client.HTTPSConnection | None = None
    try:
        conn, response, _final_url = _open_pinned_download(link, timeout)
        if not 200 <= response.status < 300:
            status = response.status
            _read_limited(response, 256 * 1024, context="PocketBook download error response")
            raise DownloadError(f"Download failed: HTTP {status}", status=status, retryable=status in {401, 403, 404, 408, 429, 500, 502, 503, 504})
        encoding = str(response.getheader("Content-Encoding") or "").strip().casefold()
        if encoding not in {"", "identity"}:
            raise UnsafeOperation("Compressed HTTP transfer encoding is not accepted for ebook downloads")
        declared: int | None = None
        length = response.getheader("Content-Length")
        if length is not None:
            try:
                declared = int(length)
            except ValueError as exc:
                raise DownloadError("Download returned an invalid Content-Length") from exc
            if declared < 0:
                raise DownloadError("Download returned a negative Content-Length")
            if declared > max_size:
                raise UnsafeOperation("Download exceeds configured size limit")
        with _private_open_exclusive(part) as fh:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise UnsafeOperation("Download exceeded configured size limit")
                fh.write(chunk)
            fh.flush()
            os.fsync(fh.fileno())
        if declared is not None and total != declared:
            raise DownloadError("Download ended before the declared Content-Length", retryable=True)
        _commit_temp_without_overwrite(part, target)
        os.chmod(target, 0o600)
    except (socket.timeout, http.client.IncompleteRead, ConnectionError) as exc:
        raise DownloadError(f"Download failed: {type(exc).__name__}", retryable=True) from exc
    finally:
        if conn is not None:
            conn.close()
        try:
            part.unlink()
        except FileNotFoundError:
            pass
    return {"ok": True, "path": str(target), "filename": target.name, "bytes": total}

__all__ = ['_public_https_addresses', 'ensure_public_https', 'SafeRedirect', '_PinnedHTTPSConnection', '_open_pinned_download', 'download_book']
