"""Bounded downloads from public HTTP(S) sources.

DNS validation alone cannot prevent rebinding if a client resolves the host a
second time.  This module therefore resolves and validates the complete answer
set itself, then pins the TCP connection to one of those validated addresses.
The connected peer is checked again before any response is trusted.
"""

from __future__ import annotations

import http.client
import ipaddress
import os
import queue
import secrets
import socket
import ssl
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlsplit


class DownloadError(Exception):
    """Base class for download failures."""


class DownloadSecurityError(DownloadError):
    """Raised when a URL or network endpoint is not safe to contact."""


class DownloadRedirectError(DownloadError):
    """Raised when a redirect is malformed or exceeds the hop limit."""


class DownloadNetworkError(DownloadError):
    """Raised when an HTTP request cannot be completed."""


class DownloadTimeout(DownloadNetworkError):
    """Raised when the total download deadline expires."""


class DownloadHttpError(DownloadError):
    """Raised for a non-success HTTP status."""


class DownloadMediaTypeError(DownloadError):
    """Raised when a response is not an allowed document or image type."""


class DownloadTooLarge(DownloadError):
    """Raised when declared or streamed response bytes exceed the limit."""


class DownloadStorageError(DownloadError):
    """Raised when a file cannot be published atomically."""


@dataclass(frozen=True)
class DownloadResult:
    path: Path
    source_url: str
    media_type: str
    size_bytes: int
    redirect_chain: tuple[str, ...] = ()
    declared_media_type: str | None = None

    def __post_init__(self) -> None:
        chain = tuple(self.redirect_chain) or (self.source_url,)
        if not all(isinstance(url, str) and url for url in chain):
            raise ValueError("redirect_chain must contain nonempty URLs")
        if chain[-1] != self.source_url:
            raise ValueError("redirect_chain must end at source_url")
        object.__setattr__(self, "redirect_chain", chain)
        if self.declared_media_type is None:
            object.__setattr__(self, "declared_media_type", self.media_type)


_MEDIA_TYPE_EXTENSIONS = {
    "application/csv": ".csv",
    "application/json": ".json",
    "application/pdf": ".pdf",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/xhtml+xml": ".html",
    "image/avif": ".avif",
    "image/bmp": ".bmp",
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/svg+xml": ".svg",
    "image/tiff": ".tiff",
    "image/vnd.microsoft.icon": ".ico",
    "image/webp": ".webp",
    "text/csv": ".csv",
    "text/html": ".html",
    "text/json": ".json",
}

# Keep SSRF classification stable across the supported Python 3.10+ range.
# These IANA special-purpose registry corrections changed in ipaddress 3.13
# and were only selectively backported to older maintenance releases.
_IPV4_PROTOCOL_ASSIGNMENTS = ipaddress.ip_network("192.0.0.0/24")
_IPV4_PROTOCOL_GLOBAL_EXCEPTIONS = frozenset(
    {ipaddress.ip_address("192.0.0.9"), ipaddress.ip_address("192.0.0.10")}
)
_IPV6_ALWAYS_NON_GLOBAL = (
    ipaddress.ip_network("64:ff9b:1::/48"),
    ipaddress.ip_network("2002::/16"),
)
_IPV6_PROTOCOL_ASSIGNMENTS = ipaddress.ip_network("2001::/23")
_IPV6_PROTOCOL_GLOBAL_EXCEPTIONS = (
    ipaddress.ip_network("2001:1::1/128"),
    ipaddress.ip_network("2001:1::2/128"),
    ipaddress.ip_network("2001:3::/32"),
    ipaddress.ip_network("2001:4:112::/48"),
    ipaddress.ip_network("2001:20::/28"),
    ipaddress.ip_network("2001:30::/28"),
)


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, hostname: str, port: int, address: str, timeout: float):
        super().__init__(hostname, port=port, timeout=timeout)
        self._pinned_address = address
        self._operation_deadline = time.monotonic() + timeout
        self.deadline_watchdog: _SocketDeadlineWatchdog | None = None

    def connect(self) -> None:
        self.sock = socket.create_connection(
            (self._pinned_address, self.port), self.timeout, self.source_address
        )
        self.deadline_watchdog = _SocketDeadlineWatchdog(
            self.sock, self._operation_deadline
        )
        self.deadline_watchdog.start()


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, hostname: str, port: int, address: str, timeout: float):
        super().__init__(
            hostname,
            port=port,
            timeout=timeout,
            context=ssl.create_default_context(),
        )
        self._pinned_address = address
        self._operation_deadline = time.monotonic() + timeout
        self.deadline_watchdog: _SocketDeadlineWatchdog | None = None

    def connect(self) -> None:
        raw_socket = socket.create_connection(
            (self._pinned_address, self.port), self.timeout, self.source_address
        )
        self.deadline_watchdog = _SocketDeadlineWatchdog(
            raw_socket, self._operation_deadline
        )
        self.deadline_watchdog.start()
        try:
            self.sock = self._context.wrap_socket(
                raw_socket,
                server_hostname=self.host,
                do_handshake_on_connect=False,
            )
            self.deadline_watchdog.replace_socket(self.sock)
            self.sock.do_handshake()
        except BaseException:
            self.deadline_watchdog.cancel()
            if self.sock is None:
                raw_socket.close()
            else:
                self.sock.close()
            raise


def _abort_socket(peer_socket: socket.socket) -> None:
    try:
        peer_socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        peer_socket.close()
    except OSError:
        pass


class _SocketDeadlineWatchdog:
    """Actively abort one connected socket when its wall-clock deadline passes."""

    def __init__(self, peer_socket: socket.socket, deadline: float):
        self._peer_socket = peer_socket
        self._lock = threading.Lock()
        self.expired = threading.Event()
        self._timer = threading.Timer(
            max(0.0, deadline - time.monotonic()), self._expire
        )
        self._timer.daemon = True

    def start(self) -> None:
        self._timer.start()

    def replace_socket(self, peer_socket: socket.socket) -> None:
        with self._lock:
            self._peer_socket = peer_socket
            expired = self.expired.is_set()
        if expired:
            _abort_socket(peer_socket)

    def _expire(self) -> None:
        with self._lock:
            self.expired.set()
            peer_socket = self._peer_socket
        _abort_socket(peer_socket)

    def cancel(self) -> None:
        self._timer.cancel()


class _ManagedResponse:
    def __init__(
        self,
        response: http.client.HTTPResponse,
        connection: http.client.HTTPConnection,
        peer_socket: socket.socket,
        peer_ip: str,
        deadline_watchdog: _SocketDeadlineWatchdog,
    ):
        self._response = response
        self._connection = connection
        self._peer_socket = peer_socket
        self.peer_ip = peer_ip
        self._deadline_watchdog = deadline_watchdog
        self.status = response.status
        self.reason = response.reason

    def getheader(self, name: str, default: str | None = None) -> str | None:
        return self._response.getheader(name, default)

    def read(self, amount: int = -1) -> bytes:
        return self._response.read(amount)

    def set_timeout(self, timeout: float) -> None:
        self._peer_socket.settimeout(timeout)

    @property
    def deadline_expired(self) -> bool:
        return self._deadline_watchdog.expired.is_set()

    def close(self) -> None:
        self._deadline_watchdog.cancel()
        try:
            self._response.close()
        finally:
            self._connection.close()


def _is_public_address(
    address: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> bool:
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
        return _is_public_address(address.ipv4_mapped)
    if isinstance(address, ipaddress.IPv4Address):
        if address in _IPV4_PROTOCOL_ASSIGNMENTS:
            return address in _IPV4_PROTOCOL_GLOBAL_EXCEPTIONS
    else:
        if any(address in network for network in _IPV6_ALWAYS_NON_GLOBAL):
            return False
        if address in _IPV6_PROTOCOL_ASSIGNMENTS:
            return any(
                address in network
                for network in _IPV6_PROTOCOL_GLOBAL_EXCEPTIONS
            )
    return (
        address.is_global
        and not address.is_loopback
        and not address.is_private
        and not address.is_link_local
        and not address.is_multicast
        and not address.is_reserved
        and not address.is_unspecified
    )


def _require_public_address(value: str) -> None:
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise DownloadSecurityError("DNS returned an invalid address") from exc
    if not _is_public_address(address):
        raise DownloadSecurityError("URL resolves to a non-public address")


@dataclass
class _ResolverJob:
    hostname: str
    port: int
    deadline: float
    result_queue: queue.Queue[tuple[bool, object]]
    cancelled: threading.Event


class _ResolverService:
    """Fixed-size daemon resolver pool with a bounded pending-job queue."""

    def __init__(self, worker_count: int = 4, queue_capacity: int = 8):
        self._worker_count = worker_count
        self._jobs: queue.Queue[_ResolverJob] = queue.Queue(
            maxsize=queue_capacity
        )
        self._start_lock = threading.Lock()
        self._started = False

    def resolve(
        self, hostname: str, port: int, deadline: float
    ) -> list[tuple[object, ...]]:
        _remaining_timeout(deadline)
        self._ensure_started()
        job = _ResolverJob(
            hostname=hostname,
            port=port,
            deadline=deadline,
            result_queue=queue.Queue(maxsize=1),
            cancelled=threading.Event(),
        )
        try:
            self._jobs.put(job, timeout=_remaining_timeout(deadline))
        except queue.Full as exc:
            job.cancelled.set()
            raise DownloadTimeout(
                "Download timed out waiting for DNS capacity"
            ) from exc
        try:
            succeeded, value = job.result_queue.get(
                timeout=_remaining_timeout(deadline)
            )
        except queue.Empty as exc:
            job.cancelled.set()
            raise DownloadTimeout("Download timed out during DNS resolution") from exc
        try:
            _remaining_timeout(deadline)
        except DownloadTimeout:
            job.cancelled.set()
            raise
        if succeeded:
            return value  # type: ignore[return-value]
        raise value  # type: ignore[misc]

    def _ensure_started(self) -> None:
        if self._started:
            return
        with self._start_lock:
            if self._started:
                return
            for index in range(self._worker_count):
                worker = threading.Thread(
                    target=self._work,
                    name=f"public-download-resolver-{index}",
                    daemon=True,
                )
                worker.start()
            self._started = True

    def _work(self) -> None:
        while True:
            job = self._jobs.get()
            try:
                if job.cancelled.is_set() or time.monotonic() >= job.deadline:
                    continue
                try:
                    value: object = socket.getaddrinfo(
                        job.hostname,
                        job.port,
                        type=socket.SOCK_STREAM,
                    )
                    result = (True, value)
                except Exception as exc:
                    result = (False, exc)
                if job.cancelled.is_set() or time.monotonic() >= job.deadline:
                    continue
                try:
                    job.result_queue.put_nowait(result)
                except queue.Full:
                    pass
            finally:
                self._jobs.task_done()


_RESOLVER_SERVICE = _ResolverService()


def _getaddrinfo_before_deadline(
    hostname: str, port: int, deadline: float | None
) -> list[tuple[object, ...]]:
    if deadline is None:
        return socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    return _RESOLVER_SERVICE.resolve(hostname, port, deadline)


def _resolve_public_addresses(
    hostname: str, port: int, deadline: float | None = None
) -> tuple[str, ...]:
    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        _require_public_address(str(literal))
        return (str(literal),)
    try:
        results = _getaddrinfo_before_deadline(hostname, port, deadline)
    except (OSError, UnicodeError) as exc:
        raise DownloadSecurityError("URL host could not be resolved") from exc
    addresses = tuple(dict.fromkeys(result[4][0] for result in results))
    if not addresses:
        raise DownloadSecurityError("URL host has no addresses")
    for address in addresses:
        _require_public_address(address)
    return addresses


def _validated_target(
    url: str, deadline: float | None = None
) -> tuple[str, int, tuple[str, ...]]:
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
        port = parsed.port
    except (TypeError, ValueError) as exc:
        raise DownloadSecurityError("URL is malformed") from exc
    if parsed.scheme.lower() not in {"http", "https"}:
        raise DownloadSecurityError("Only HTTP and HTTPS URLs are allowed")
    if not parsed.netloc or hostname is None:
        raise DownloadSecurityError("URL must include a host")
    if parsed.username is not None or parsed.password is not None:
        raise DownloadSecurityError("URL userinfo is not allowed")
    effective_port = port or (443 if parsed.scheme.lower() == "https" else 80)
    return (
        hostname,
        effective_port,
        _resolve_public_addresses(hostname, effective_port, deadline),
    )


def validate_public_url(url: str) -> None:
    """Reject URLs whose syntax or complete DNS result set is not public."""

    _validated_target(url)


def _request_path(url: str) -> str:
    parsed = urlsplit(url)
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    return path


def _host_header(hostname: str, port: int, scheme: str) -> str:
    host = f"[{hostname}]" if ":" in hostname else hostname
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        return host
    return f"{host}:{port}"


def _open_pinned_request(
    url: str, addresses: tuple[str, ...], timeout: float
) -> _ManagedResponse:
    """Open one request without performing an unvalidated DNS lookup."""

    parsed = urlsplit(url)
    hostname = parsed.hostname
    if hostname is None:
        raise DownloadSecurityError("URL must include a host")
    port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    deadline = time.monotonic() + timeout
    last_error: BaseException | None = None
    for address in addresses:
        connection_class = (
            _PinnedHTTPSConnection
            if parsed.scheme.lower() == "https"
            else _PinnedHTTPConnection
        )
        connection = connection_class(
            hostname, port, address, _remaining_timeout(deadline)
        )
        connection._operation_deadline = deadline
        response = None
        watchdog = None
        try:
            connection.connect()
            if connection.sock is None:
                raise OSError("connection has no peer socket")
            peer_socket = connection.sock
            watchdog = getattr(connection, "deadline_watchdog", None)
            if watchdog is None:
                watchdog = _SocketDeadlineWatchdog(peer_socket, deadline)
                watchdog.start()
            connection.request(
                "GET",
                _request_path(url),
                headers={
                    "Accept": "*/*",
                    "Host": _host_header(hostname, port, parsed.scheme.lower()),
                    "User-Agent": "pathway-atlas-downloader/0.1",
                },
            )
            peer_ip = peer_socket.getpeername()[0]
            response = connection.getresponse()
            _remaining_timeout(deadline)
            return _ManagedResponse(
                response,
                connection,
                peer_socket,
                peer_ip,
                watchdog,
            )
        except DownloadTimeout:
            if response is not None:
                response.close()
            if watchdog is not None:
                watchdog.cancel()
            connection.close()
            raise
        except (OSError, http.client.HTTPException) as exc:
            if watchdog is None:
                watchdog = getattr(connection, "deadline_watchdog", None)
            expired = (
                watchdog is not None and watchdog.expired.is_set()
            ) or time.monotonic() >= deadline
            if response is not None:
                response.close()
            if watchdog is not None:
                watchdog.cancel()
            connection.close()
            if expired:
                raise DownloadTimeout("Download timed out") from exc
            last_error = exc
    if isinstance(last_error, socket.timeout):
        raise DownloadTimeout("Download timed out") from last_error
    raise DownloadNetworkError("Unable to connect to the validated host") from last_error


def download_public_file(
    url: str,
    workspace: str | Path,
    *,
    max_bytes: int = 26_214_400,
    timeout: float = 60,
) -> DownloadResult:
    """Download a public HTTP(S) resource into a validated workspace."""

    workspace_path = _validated_workspace(workspace)
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes < 1:
        raise ValueError("max_bytes must be a positive integer")
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
        raise ValueError("timeout must be positive")
    deadline = time.monotonic() + timeout
    current_url = url
    redirect_chain = [url]
    redirects_followed = 0
    while True:
        _remaining_timeout(deadline)
        _, _, addresses = _validated_target(current_url, deadline)
        _remaining_timeout(deadline)
        response = _open_pinned_request(
            current_url, addresses, _remaining_timeout(deadline)
        )
        try:
            _remaining_timeout(deadline)
            _require_public_address(response.peer_ip)
            resolved = {ipaddress.ip_address(address) for address in addresses}
            if ipaddress.ip_address(response.peer_ip) not in resolved:
                raise DownloadSecurityError(
                    "Connected peer was not in the prevalidated DNS result set"
                )
            if response.status in {301, 302, 303, 307, 308}:
                if redirects_followed >= 5:
                    raise DownloadRedirectError("Redirect limit exceeded")
                location = response.getheader("Location")
                if not location:
                    raise DownloadRedirectError("Redirect response has no Location")
                current_url = urljoin(current_url, location)
                redirect_chain.append(current_url)
                redirects_followed += 1
                continue
            if not 200 <= response.status < 300:
                raise DownloadHttpError(
                    f"HTTP request failed with status {response.status}"
                )
            media_type, extension = _validated_media_type(response)
            _validate_content_length(response, max_bytes)
            return _stream_to_workspace(
                response,
                workspace_path,
                current_url,
                media_type,
                extension,
                max_bytes,
                deadline,
                tuple(redirect_chain),
            )
        finally:
            response.close()


def _validated_workspace(workspace: str | Path) -> Path:
    try:
        candidate = Path(workspace)
    except TypeError as exc:
        raise DownloadSecurityError("Workspace must be a resolved directory") from exc
    if not candidate.is_absolute():
        raise DownloadSecurityError("Workspace must be an absolute resolved path")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise DownloadSecurityError("Workspace does not exist") from exc
    if candidate != resolved or not resolved.is_dir():
        raise DownloadSecurityError("Workspace must be a resolved directory")
    return resolved


def _remaining_timeout(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise DownloadTimeout("Download timed out")
    return remaining


def _validated_media_type(response: object) -> tuple[str, str]:
    raw_media_type = response.getheader("Content-Type")
    media_type = (raw_media_type or "").split(";", 1)[0].strip().lower()
    extension = _MEDIA_TYPE_EXTENSIONS.get(media_type)
    if extension is None:
        raise DownloadMediaTypeError("Response Content-Type is not allowed")
    return media_type, extension


def _validate_content_length(response: object, max_bytes: int) -> None:
    raw_length = response.getheader("Content-Length")
    if raw_length is None:
        return
    try:
        declared_length = int(raw_length)
    except (TypeError, ValueError) as exc:
        raise DownloadError("Response Content-Length is invalid") from exc
    if declared_length < 0:
        raise DownloadError("Response Content-Length is invalid")
    if declared_length > max_bytes:
        raise DownloadTooLarge("Response exceeds the download byte limit")


def _document_route(prefix: bytes, media_type: str, extension: str) -> tuple[str, str]:
    """Route binary attachments mislabeled HTML; the selected adapter validates them.

    An OLE signature identifies a compound document, not a proven workbook. It
    selects the XLS reader, which must still reject nonworkbooks or malformed
    bytes. Neither a URL filename nor Content-Disposition can select a parser.
    """
    if media_type not in {"text/html", "application/xhtml+xml"}:
        return media_type, extension
    if prefix.startswith(b"%PDF-"):
        return "application/pdf", ".pdf"
    compound = prefix.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
    biff = prefix[:2] == b"\x09\x08" and prefix[4:8] in {b"\x00\x05\x05\x00", b"\x00\x06\x05\x00"}
    if compound or biff:
        return "application/vnd.ms-excel", ".xls"
    return media_type, extension


def _stream_to_workspace(
    response: object,
    workspace: Path,
    source_url: str,
    media_type: str,
    extension: str,
    max_bytes: int,
    deadline: float,
    redirect_chain: tuple[str, ...],
) -> DownloadResult:
    destination = workspace / f"{secrets.token_hex(16)}{extension}"
    declared_media_type = media_type
    temporary_path: Path | None = None
    total = 0
    prefix = b""
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=workspace,
            prefix=".download-",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            while True:
                try:
                    remaining = _remaining_timeout(deadline)
                    set_timeout = getattr(response, "set_timeout", None)
                    if set_timeout is not None:
                        set_timeout(remaining)
                    chunk = response.read(64 * 1024)
                except socket.timeout as exc:
                    raise DownloadTimeout("Download timed out") from exc
                except (OSError, http.client.HTTPException) as exc:
                    expired = getattr(response, "deadline_expired", False)
                    if expired or time.monotonic() >= deadline:
                        raise DownloadTimeout("Download timed out") from exc
                    raise DownloadNetworkError("Response stream failed") from exc
                _remaining_timeout(deadline)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise DownloadTooLarge("Response exceeds the download byte limit")
                if len(prefix) < 16:
                    prefix += chunk[:16 - len(prefix)]
                temporary.write(chunk)
            temporary.flush()
            os.fsync(temporary.fileno())
        _remaining_timeout(deadline)
        media_type, extension = _document_route(prefix, media_type, extension)
        destination = destination.with_suffix(extension)
        os.replace(temporary_path, destination)
        temporary_path = None
    except DownloadError:
        raise
    except OSError as exc:
        raise DownloadStorageError("Unable to store downloaded file") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
    return DownloadResult(
        destination, source_url, media_type, total, redirect_chain,
        declared_media_type=declared_media_type,
    )


__all__ = [
    "DownloadError",
    "DownloadHttpError",
    "DownloadMediaTypeError",
    "DownloadNetworkError",
    "DownloadRedirectError",
    "DownloadResult",
    "DownloadSecurityError",
    "DownloadStorageError",
    "DownloadTimeout",
    "DownloadTooLarge",
    "download_public_file",
    "validate_public_url",
]
