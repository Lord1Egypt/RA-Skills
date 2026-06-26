from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import struct
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

APP_NAME = "otpforge"
DEFAULT_DIGITS = 6
DEFAULT_PERIOD = 30


def _default_store_path() -> Path:
    override = os.environ.get("OTPFORGE_STORE")
    if override:
        return Path(override).expanduser().resolve()
    home = Path.home()
    return home / ".config" / APP_NAME / "secrets.json"


def _normalize_secret(secret: str) -> str:
    cleaned = "".join(secret.strip().split()).upper()
    if not cleaned:
        raise ValueError("Secret cannot be empty")
    try:
        base64.b32decode(cleaned, casefold=True)
    except Exception as exc:  # pragma: no cover - defensive branch
        raise ValueError("Secret must be valid base32") from exc
    return cleaned


def _b32decode(secret: str) -> bytes:
    padding = "=" * ((8 - (len(secret) % 8)) % 8)
    return base64.b32decode(secret + padding, casefold=True)


def totp_code(secret: str, for_time: int | None = None, digits: int = DEFAULT_DIGITS, period: int = DEFAULT_PERIOD) -> str:
    if digits < 6 or digits > 10:
        raise ValueError("Digits must be between 6 and 10")
    if period <= 0:
        raise ValueError("Period must be > 0")

    timestamp = int(for_time if for_time is not None else time.time())
    counter = timestamp // period

    key = _b32decode(secret)
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    truncated = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    code_int = truncated % (10**digits)
    return f"{code_int:0{digits}d}"


def seconds_remaining(period: int = DEFAULT_PERIOD, at_time: int | None = None) -> int:
    timestamp = int(at_time if at_time is not None else time.time())
    return period - (timestamp % period)


@dataclass(frozen=True)
class OtpEntry:
    label: str
    secret: str
    issuer: str = ""
    digits: int = DEFAULT_DIGITS
    period: int = DEFAULT_PERIOD


class Vault:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or _default_store_path()

    def _ensure_parent(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load_raw(self) -> dict:
        if not self.path.exists():
            return {"entries": []}
        with self.path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _write_raw(self, data: dict) -> None:
        self._ensure_parent()
        temp = self.path.with_suffix(".tmp")
        with temp.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")
        os.replace(temp, self.path)
        os.chmod(self.path, 0o600)

    def list_entries(self) -> list[OtpEntry]:
        data = self._load_raw()
        entries = []
        for item in data.get("entries", []):
            entries.append(
                OtpEntry(
                    label=item["label"],
                    secret=item["secret"],
                    issuer=item.get("issuer", ""),
                    digits=int(item.get("digits", DEFAULT_DIGITS)),
                    period=int(item.get("period", DEFAULT_PERIOD)),
                )
            )
        entries.sort(key=lambda e: e.label.lower())
        return entries

    def upsert(self, entry: OtpEntry) -> None:
        normalized = OtpEntry(
            label=entry.label.strip(),
            issuer=entry.issuer.strip(),
            secret=_normalize_secret(entry.secret),
            digits=entry.digits,
            period=entry.period,
        )
        if not normalized.label:
            raise ValueError("Label cannot be empty")

        data = self._load_raw()
        items = data.setdefault("entries", [])

        for item in items:
            if item["label"].lower() == normalized.label.lower():
                item.update(
                    {
                        "label": normalized.label,
                        "issuer": normalized.issuer,
                        "secret": normalized.secret,
                        "digits": normalized.digits,
                        "period": normalized.period,
                    }
                )
                self._write_raw(data)
                return

        items.append(
            {
                "label": normalized.label,
                "issuer": normalized.issuer,
                "secret": normalized.secret,
                "digits": normalized.digits,
                "period": normalized.period,
            }
        )
        self._write_raw(data)

    def remove(self, label: str) -> bool:
        data = self._load_raw()
        original = data.get("entries", [])
        kept = [item for item in original if item.get("label", "").lower() != label.lower()]
        if len(kept) == len(original):
            return False
        data["entries"] = kept
        self._write_raw(data)
        return True

    def get(self, label: str) -> OtpEntry | None:
        lowered = label.lower()
        for entry in self.list_entries():
            if entry.label.lower() == lowered:
                return entry
        return None


def format_entry_name(entry: OtpEntry) -> str:
    if entry.issuer:
        return f"{entry.issuer} ({entry.label})"
    return entry.label


def render_codes(entries: Iterable[OtpEntry], at_time: int | None = None) -> list[tuple[OtpEntry, str, int]]:
    now = int(at_time if at_time is not None else time.time())
    result = []
    for entry in entries:
        code = totp_code(entry.secret, for_time=now, digits=entry.digits, period=entry.period)
        remain = seconds_remaining(period=entry.period, at_time=now)
        result.append((entry, code, remain))
    return result
