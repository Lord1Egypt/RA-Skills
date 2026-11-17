"""Resolve one host-decoded QR URL through the secure downloader only."""

from __future__ import annotations

from dataclasses import InitVar, dataclass
import ipaddress
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit

try:
    from scripts.downloader import (
        DownloadResult,
        _MEDIA_TYPE_EXTENSIONS,
        download_public_file,
        validate_public_url,
    )
except ImportError:  # Flat ``adapters`` import with ``scripts`` on sys.path.
    from downloader import DownloadResult, _MEDIA_TYPE_EXTENSIONS, download_public_file, validate_public_url


class QrPayloadError(ValueError):
    """Raised when host-decoded payload text is not exactly one safe URL."""


class QrResolutionError(ValueError):
    """Raised when downloader provenance is inconsistent."""


_SAFE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,127}$")
_MEDIA_TYPE = re.compile(r"^[a-z0-9][a-z0-9.+-]*/[a-z0-9][a-z0-9.+-]*$")
_RESOLUTION_AUTH = object()


def _safe_id(value: object, name: str) -> str:
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value) or value in {".", ".."}:
        raise QrPayloadError(f"{name} must be a safe logical identifier")
    return value


def _safe_source_id(value: object) -> str:
    source_id = _safe_id(value, "qr_image_source_id")
    normalized = source_id.casefold()
    compact_digits = re.sub(r"[._-]", "", normalized)
    segments = tuple(segment for segment in re.split(r"[._-]+", normalized) if segment)
    structured_secret = (
        any(segment in {"token", "secret", "password"} for segment in segments)
        or any(pair in {("api", "key"), ("sk", "live"), ("sk", "test")} for pair in zip(segments, segments[1:]))
    )
    if (
        re.search(r"\d{7,}", source_id)
        or re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)", compact_digits)
        or structured_secret
    ):
        raise QrPayloadError("qr_image_source_id cannot contain PII or secret material")
    return source_id


def _safe_url(value: object, *, require_public_literal: bool = True) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("URL must be a nonempty exact string")
    if any(ord(character) < 33 or character.isspace() for character in value):
        raise ValueError("URL cannot contain control characters or whitespace")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        parsed.port
    except (TypeError, ValueError):
        raise ValueError("URL is malformed") from None
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc or hostname is None:
        raise ValueError("URL must use HTTP or HTTPS and include a host")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URL userinfo is not allowed")
    normalized_hostname = hostname.casefold().rstrip(".")
    if normalized_hostname == "localhost" or normalized_hostname.endswith(".localhost"):
        raise ValueError("URL host is not public")
    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        if require_public_literal and not literal.is_global:
            raise ValueError("URL literal must be public")
    return value


@dataclass(frozen=True)
class QrResolution:
    qr_image_source_id: str
    original_url: str
    redirect_chain: tuple[str, ...]
    final_url: str
    media_type: str
    size_bytes: int
    downloaded_file_id: str
    _auth: InitVar[object] = None

    def __post_init__(self, _auth: object) -> None:
        if _auth is not _RESOLUTION_AUTH:
            raise QrResolutionError("QrResolution must be created from an authenticated download")
        source_id = _safe_source_id(self.qr_image_source_id)
        original = _safe_url(self.original_url)
        final = _safe_url(self.final_url)
        if isinstance(self.redirect_chain, (str, bytes, bytearray)):
            raise TypeError("redirect_chain must be an ordered URL collection")
        try:
            chain = tuple(_safe_url(item) for item in self.redirect_chain)
        except TypeError:
            raise TypeError("redirect_chain must be an ordered URL collection") from None
        if not chain or chain[0] != original or chain[-1] != final:
            raise ValueError("redirect_chain endpoints contradict original_url or final_url")
        if not isinstance(self.media_type, str) or not _MEDIA_TYPE.fullmatch(self.media_type):
            raise ValueError("media_type must be a normalized media type")
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise TypeError("size_bytes must be an integer")
        if self.size_bytes < 0:
            raise ValueError("size_bytes cannot be negative")
        file_id = _safe_id(self.downloaded_file_id, "downloaded_file_id")
        expected_extension = _MEDIA_TYPE_EXTENSIONS.get(self.media_type)
        if expected_extension is None or Path(file_id).suffix != expected_extension:
            raise ValueError("downloaded_file_id extension must match media_type")
        object.__setattr__(self, "qr_image_source_id", source_id)
        object.__setattr__(self, "original_url", original)
        object.__setattr__(self, "redirect_chain", chain)
        object.__setattr__(self, "final_url", final)
        object.__setattr__(self, "downloaded_file_id", file_id)

    @classmethod
    def _from_download(
        cls,
        qr_image_source_id: str,
        original_url: str,
        result: DownloadResult,
        downloaded_file_id: str,
    ) -> QrResolution:
        try:
            return cls(
                qr_image_source_id,
                original_url,
                result.redirect_chain,
                result.source_url,
                result.media_type,
                result.size_bytes,
                downloaded_file_id,
                _auth=_RESOLUTION_AUTH,
            )
        except QrResolutionError:
            raise
        except (TypeError, ValueError):
            raise QrResolutionError("secure downloader returned inconsistent provenance") from None

    def to_dict(self) -> dict[str, Any]:
        return {
            "qr_image_source_id": self.qr_image_source_id,
            "original_url": self.original_url,
            "redirect_chain": list(self.redirect_chain),
            "final_url": self.final_url,
            "media_type": self.media_type,
            "size_bytes": self.size_bytes,
            "downloaded_file_id": self.downloaded_file_id,
        }


def _decoded_url(payload: object, source_id: object) -> tuple[str, str]:
    logical_source = _safe_source_id(source_id)
    if not isinstance(payload, str):
        raise QrPayloadError("QR payload must be host-decoded text, not image bytes")
    normalized = payload.strip()
    if not normalized or len(normalized.split()) != 1:
        raise QrPayloadError("QR payload must contain exactly one URL")
    try:
        url = _safe_url(normalized, require_public_literal=False)
    except (TypeError, ValueError):
        raise QrPayloadError("QR payload must contain exactly one HTTP(S) URL") from None
    return url, logical_source


def _validate_result(result: DownloadResult, workspace: str | Path) -> Path:
    if not isinstance(result, DownloadResult):
        raise QrResolutionError("secure downloader returned an invalid result")
    if not isinstance(result.path, Path):
        raise QrResolutionError("downloaded file path must be a pathlib Path")
    try:
        workspace_path = Path(workspace)
        resolved_workspace = workspace_path.resolve(strict=True)
        destination = result.path
        resolved_destination = destination.resolve(strict=True)
        metadata = destination.stat()
    except (OSError, TypeError):
        raise QrResolutionError("downloaded file metadata is unavailable") from None
    if (
        workspace_path != resolved_workspace
        or not resolved_workspace.is_dir()
        or destination != resolved_destination
        or destination.parent != resolved_workspace
        or not destination.is_file()
        or metadata.st_size != result.size_bytes
    ):
        raise QrResolutionError("downloaded file metadata is inconsistent")
    return destination


def resolve_qr_payload(
    payload: object,
    workspace: str | Path,
    *,
    qr_image_source_id: str,
    max_bytes: int,
    timeout: float,
) -> QrResolution:
    original_url, source_id = _decoded_url(payload, qr_image_source_id)
    validate_public_url(original_url)
    result = download_public_file(
        original_url,
        workspace,
        max_bytes=max_bytes,
        timeout=timeout,
    )
    destination = _validate_result(result, workspace)
    return QrResolution._from_download(source_id, original_url, result, destination.name)


__all__ = [
    "QrPayloadError",
    "QrResolution",
    "QrResolutionError",
    "resolve_qr_payload",
]
