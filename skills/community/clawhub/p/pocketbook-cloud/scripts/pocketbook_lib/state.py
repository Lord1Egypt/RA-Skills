from __future__ import annotations

import hashlib
import json
import os
import secrets
import stat
import time
import unicodedata
from pathlib import Path
from typing import Any

from .common import PocketBookError, UnsafeOperation, _private_open_exclusive

def _read_private_bytes(path: Path, max_size: int, *, label: str) -> bytes | None:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise UnsafeOperation(f"{label} cannot be opened safely") from exc
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or stat.S_IMODE(st.st_mode) != 0o600:
            raise UnsafeOperation(f"{label} must be a regular file with mode 0600")
        if st.st_size > max_size:
            raise UnsafeOperation(f"{label} is unexpectedly large")
        with os.fdopen(fd, "rb", closefd=False) as fh:
            data = fh.read(max_size + 1)
        if len(data) > max_size:
            raise UnsafeOperation(f"{label} exceeded its size limit while reading")
        return data
    finally:
        os.close(fd)


def _account_fingerprint(session: dict[str, Any]) -> str:
    email = unicodedata.normalize("NFKC", str(session.get("email") or "")).strip().casefold()
    alias = unicodedata.normalize("NFKC", str(session.get("provider_alias") or "")).strip().casefold()
    shop = unicodedata.normalize("NFKC", str(session.get("shop_id") or "")).strip().casefold()
    if not email or not alias or not shop:
        return ""
    return hashlib.sha256(f"{email}\n{alias}\n{shop}".encode("utf-8")).hexdigest()

class FileLock:
    """Small cross-platform lock based on atomic file creation."""
    def __init__(self, path: Path, timeout: float = 15.0, stale_after: float = 120.0):
        self.path = path
        self.timeout = timeout
        self.stale_after = stale_after
        self.fd: int | None = None

    def __enter__(self):
        deadline = time.monotonic() + self.timeout
        parent = self.path.parent
        if parent.exists():
            pst = parent.lstat()
            if stat.S_ISLNK(pst.st_mode) or not stat.S_ISDIR(pst.st_mode):
                raise UnsafeOperation("PocketBook state lock directory is unsafe")
            if stat.S_IMODE(pst.st_mode) != 0o700:
                os.chmod(parent, 0o700)
        else:
            parent.mkdir(parents=True, exist_ok=False, mode=0o700)
            os.chmod(parent, 0o700)
        while True:
            try:
                flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
                if hasattr(os, "O_NOFOLLOW"):
                    flags |= os.O_NOFOLLOW
                self.fd = os.open(self.path, flags, 0o600)
                os.write(self.fd, f"{os.getpid()} {int(time.time())}\n".encode("ascii"))
                return self
            except FileExistsError:
                try:
                    st = self.path.lstat()
                    if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
                        raise UnsafeOperation("PocketBook state lock path is unsafe")
                    if time.time() - st.st_mtime > self.stale_after:
                        self.path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.monotonic() >= deadline:
                    raise PocketBookError("Timed out waiting for PocketBook state lock")
                time.sleep(0.05)

    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = None
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass

class SessionStore:
    REQUIRED_STRING_FIELDS = ("email", "provider_alias", "shop_id", "access_token", "refresh_token")

    def __init__(self, path: Path | None = None):
        override = os.environ.get("POCKETBOOK_SESSION_FILE", "").strip()
        self.path = path or (Path(override).expanduser() if override else Path.home() / ".config" / "openclaw" / "pocketbook-cloud" / "session.json")

    def _validate_parent(self, *, create: bool) -> None:
        parent = self.path.parent
        if parent.exists():
            st = parent.lstat()
            if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
                raise UnsafeOperation("PocketBook state directory is not a private regular directory")
            if create and stat.S_IMODE(st.st_mode) != 0o700:
                os.chmod(parent, 0o700)
                st = parent.lstat()
            if stat.S_IMODE(st.st_mode) != 0o700:
                raise UnsafeOperation("PocketBook state directory must have mode 0700")
        elif create:
            parent.mkdir(parents=True, exist_ok=False, mode=0o700)
            os.chmod(parent, 0o700)

    def _validate_data(self, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict) or int(data.get("schema") or 0) != 1:
            raise UnsafeOperation("PocketBook session file has invalid schema")
        for field in self.REQUIRED_STRING_FIELDS:
            if not isinstance(data.get(field), str) or not data[field]:
                raise UnsafeOperation("PocketBook session file has invalid field types")
        if not isinstance(data.get("expires_at"), int):
            raise UnsafeOperation("PocketBook session file has invalid expiry")
        if data.get("provider_name") is not None and not isinstance(data.get("provider_name"), str):
            raise UnsafeOperation("PocketBook session file has invalid provider name")
        return data

    def load(self) -> dict[str, Any]:
        self._validate_parent(create=False)
        raw = _read_private_bytes(self.path, 1024 * 1024, label="PocketBook session file")
        if raw is None:
            return {}
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PocketBookError("Cannot read PocketBook session file") from exc
        return self._validate_data(data)

    def save(self, data: dict[str, Any]) -> None:
        self._validate_parent(create=True)
        data = self._validate_data(data)
        payload = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        tmp = self.path.with_name(self.path.name + f".tmp.{os.getpid()}.{secrets.token_hex(4)}")
        try:
            with _private_open_exclusive(tmp) as fh:
                fh.write(payload)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, self.path)
            os.chmod(self.path, 0o600)
        finally:
            try:
                tmp.unlink()
            except FileNotFoundError:
                pass

    def clear(self) -> None:
        for candidate in (self.path, self.path.with_name("delete-pending.json")):
            try:
                candidate.unlink()
            except FileNotFoundError:
                pass

def _private_json_write(path: Path, data: dict[str, Any]) -> None:
    parent = path.parent
    if parent.exists():
        pst = parent.lstat()
        if stat.S_ISLNK(pst.st_mode) or not stat.S_ISDIR(pst.st_mode):
            raise UnsafeOperation("PocketBook state directory is unsafe")
        if stat.S_IMODE(pst.st_mode) != 0o700:
            os.chmod(parent, 0o700)
    else:
        parent.mkdir(parents=True, exist_ok=False, mode=0o700)
        os.chmod(parent, 0o700)
    payload = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}.{secrets.token_hex(4)}")
    try:
        with _private_open_exclusive(tmp) as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass

__all__ = ['_read_private_bytes', '_account_fingerprint', 'FileLock', 'SessionStore', '_private_json_write']
