from __future__ import annotations

import json
import os
import stat
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

API_ORIGIN = "https://cloud.pocketbook.digital"
API_V1 = API_ORIGIN + "/api/v1.0/"
PUBLIC_CLIENT_ID = "qNAx1RDb"
# PocketBook's browser client publishes this interoperability credential in client JavaScript.
# It is not a user secret; account passwords and tokens are never embedded here.
PUBLIC_CLIENT_SECRET = "K3YYSjCgDJNoWKdGVOyO1mrROp3MMZqqRNXNXTmh"
USER_AGENT = "pocketbook-cloud-openclaw/1.0.0"
PAGE_SIZE = 500
DEFAULT_MAX_UPLOAD = 256 * 1024 * 1024
DEFAULT_MIN_SAFE_EPUB_BYTES = 4096
DEFAULT_MAX_DOWNLOAD = 512 * 1024 * 1024
DEFAULT_MAX_ARCHIVE_UNPACK = 512 * 1024 * 1024
DEFAULT_MAX_ARCHIVE_ENTRIES = 5000
DEFAULT_MAX_COMPRESSION_RATIO = 250
DEFAULT_BATCH_CONFIRM_BOOKS = 10
DEFAULT_BATCH_CONFIRM_BYTES = 100 * 1024 * 1024
DEFAULT_MAX_API_RESPONSE = 32 * 1024 * 1024
DEFAULT_MAX_API_ERROR_RESPONSE = 256 * 1024
DEFAULT_MAX_REDIRECTS = 5
MAX_UNTRUSTED_TEXT = 8192
ALLOWED_EXTENSIONS = (
    ".epub", ".fb2", ".fb2.zip", ".pdf", ".djvu", ".txt", ".rtf",
    ".html", ".htm", ".chm", ".cbz", ".cbr", ".cbt",
)

class PocketBookError(RuntimeError):
    code = 1

class AuthRequired(PocketBookError):
    code = 2

class AmbiguousBook(PocketBookError):
    code = 3

    def __init__(self, query: str, candidates: list[dict[str, Any]]):
        super().__init__(f"Book query is ambiguous: {query}")
        self.query = query
        self.candidates = candidates

class NotFound(PocketBookError):
    code = 4

class AmbiguousProvider(PocketBookError):
    code = 6

    def __init__(self, providers: list[dict[str, Any]]):
        super().__init__("Multiple PocketBook authentication providers are available")
        self.providers = providers

class UnsafeOperation(PocketBookError):
    code = 5

class DownloadError(PocketBookError):
    def __init__(self, message: str, *, status: int | None = None, retryable: bool = False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable

def safe_untrusted_text(value: Any, limit: int = MAX_UNTRUSTED_TEXT) -> str:
    """Return bounded display data, never instructions for the agent."""
    text = unicodedata.normalize("NFC", str(value or ""))
    text = "".join(ch for ch in text if ch in "\n\t" or ord(ch) >= 32)
    return text[: max(0, limit)]

def _read_limited(stream: Any, limit: int, *, context: str) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = stream.read(min(1024 * 1024, limit + 1 - total))
        if not chunk:
            break
        total += len(chunk)
        if total > limit:
            raise UnsafeOperation(f"{context} exceeded configured response limit")
        chunks.append(chunk)
    return b"".join(chunks)

def _private_open_exclusive(path: Path):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    return os.fdopen(fd, "wb")

@dataclass
class Response:
    status: int
    headers: dict[str, str]
    body: bytes
    url: str

    def json(self) -> Any:
        if not self.body:
            return {}
        try:
            return json.loads(self.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PocketBookError(f"PocketBook returned invalid JSON (HTTP {self.status})") from exc

def env_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(minimum, value)

def env_bytes(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        mb = int(raw)
    except ValueError:
        return default
    return max(1, mb) * 1024 * 1024

def _commit_temp_without_overwrite(part: Path, target: Path) -> None:
    try:
        os.link(part, target)
    except FileExistsError as exc:
        raise UnsafeOperation("Refusing to overwrite an existing output file") from exc
    except OSError as exc:
        raise PocketBookError("Cannot commit downloaded file safely") from exc
    else:
        part.unlink()

__all__ = ['API_ORIGIN', 'API_V1', 'PUBLIC_CLIENT_ID', 'PUBLIC_CLIENT_SECRET', 'USER_AGENT', 'PAGE_SIZE', 'DEFAULT_MAX_UPLOAD', 'DEFAULT_MIN_SAFE_EPUB_BYTES', 'DEFAULT_MAX_DOWNLOAD', 'DEFAULT_MAX_ARCHIVE_UNPACK', 'DEFAULT_MAX_ARCHIVE_ENTRIES', 'DEFAULT_MAX_COMPRESSION_RATIO', 'DEFAULT_BATCH_CONFIRM_BOOKS', 'DEFAULT_BATCH_CONFIRM_BYTES', 'DEFAULT_MAX_API_RESPONSE', 'DEFAULT_MAX_API_ERROR_RESPONSE', 'DEFAULT_MAX_REDIRECTS', 'MAX_UNTRUSTED_TEXT', 'ALLOWED_EXTENSIONS', 'PocketBookError', 'AuthRequired', 'AmbiguousBook', 'NotFound', 'AmbiguousProvider', 'UnsafeOperation', 'DownloadError', 'safe_untrusted_text', '_read_limited', '_private_open_exclusive', 'Response', 'env_int', 'env_bytes', '_commit_temp_without_overwrite']
