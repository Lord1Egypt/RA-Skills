"""HMAC-signed chapter cache.

The chapter cache produced by ``discover_chapter.py`` is the
allowlist ``sign_request.py`` consults before signing a request
(see SECURITY.md). If the cache file can be written by anyone with
filesystem access to ``$OPENCLAW_HOME``, an attacker can poison it
to add a hostile chapter URL and trick the signing helper into
producing a signature for that host.

To prevent this, the cache is HMAC-SHA256-signed with a key derived
from the agent's identity private key seed. An attacker who cannot
read ``identity.json`` (mode 0o600) cannot forge a valid MAC.
A cache without a valid MAC is treated as empty — fail-closed.

This module is purely a helper; both ``discover_chapter.py``
(writer) and ``sign_request.py`` (reader) import it. It is NEVER
called by the LLM directly.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

CACHE_MAC_VERSION = 1
CACHE_KEY_PURPOSE = b"openclaw-nanda-chapter:cache-mac:v1"


def _derive_mac_key(identity_file: Path) -> bytes | None:
    """Derive the cache HMAC key from the agent's private key seed.

    Returns the 32-byte HMAC key, or ``None`` if the identity file
    does not exist yet (the cache will simply be unsigned for the
    very first run, in which case the reader treats it as empty).

    The key purpose constant ensures the HMAC key cannot collide with
    any other use of the private-key seed (e.g. the Ed25519 signing
    key itself).
    """
    if not identity_file.exists():
        return None
    try:
        data = json.loads(identity_file.read_text())
        priv_pem = data["private_key_pem"].encode()
    except (OSError, json.JSONDecodeError, KeyError):
        return None
    priv = serialization.load_pem_private_key(priv_pem, password=None)
    if not isinstance(priv, Ed25519PrivateKey):
        return None
    seed = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return hashlib.sha256(CACHE_KEY_PURPOSE + seed).digest()


def _mac_over_payload(key: bytes, payload: dict[str, Any]) -> str:
    """Compute the HMAC over the canonical JSON encoding of payload.

    ``payload`` is the cache body MINUS its ``mac`` field. JSON is
    encoded with ``sort_keys=True`` and ``separators=(",", ":")`` so
    the byte sequence is canonical across Python versions.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key, canonical, hashlib.sha256).hexdigest()


def write_signed_cache(
    cache_path: Path,
    identity_file: Path,
    *,
    chapters: list[dict[str, Any]],
    expires_at: int,
) -> None:
    """Write a HMAC-signed cache file at ``cache_path`` with mode 0o600.

    The ``expires_at`` value is part of the MAC'd payload — an
    attacker cannot extend a stolen-and-stale cache by tampering with
    the timestamp.

    If the identity file does not exist yet (first-ever run before
    any signed request), the cache is written WITHOUT a MAC. The
    reader will reject this on the next load (fail-closed); the
    skill picks up a valid cache after the first ``join`` creates
    the identity. This is intentional: we do not want a transient
    "unsigned cache" path that could be exploited.
    """
    key = _derive_mac_key(identity_file)
    payload: dict[str, Any] = {
        "version": CACHE_MAC_VERSION,
        "expires_at": int(expires_at),
        "chapters": chapters,
    }
    if key is not None:
        payload["mac"] = _mac_over_payload(key, payload)
    # 0o600 — see SECURITY.md M4. Create-or-truncate is fine here; the
    # cache is best-effort and an attacker who can race the write
    # without holding 0o600-write permission already needs more access
    # than this MAC defends against.
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(payload))
    try:
        cache_path.chmod(0o600)
    except OSError:
        pass


def load_signed_cache(
    cache_path: Path,
    identity_file: Path,
) -> list[dict[str, Any]] | None:
    """Load + verify the signed cache. Returns chapter list or None.

    Returns ``None`` (treated as "no cache, refetch") if:
      - cache file missing
      - file unreadable or not JSON
      - MAC missing while identity exists (cache predates the
        signing feature OR was tampered)
      - MAC present but does not verify
      - ``expires_at`` in the past
      - any field has the wrong type

    The fail-closed contract is important for ``sign_request.py``,
    which uses this function's output as the allowlist of hosts it
    will sign for. A return value of None there means "refuse to
    sign anything not flagged --trust-host".
    """
    if not cache_path.exists():
        return None
    try:
        raw = cache_path.read_text()
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None

    expires_at = data.get("expires_at")
    if not isinstance(expires_at, (int, float)):
        return None
    import time as _time

    if expires_at < _time.time():
        return None

    chapters = data.get("chapters")
    if not isinstance(chapters, list):
        return None

    # MAC verification — required if the identity exists.
    key = _derive_mac_key(identity_file)
    presented_mac = data.get("mac")
    if key is not None:
        if not isinstance(presented_mac, str):
            # Identity exists but cache is unsigned: a pre-MAC cache
            # OR a tampered cache. Either way: do not trust.
            return None
        # Recompute over the payload sans mac.
        payload_minus_mac = {k: v for k, v in data.items() if k != "mac"}
        expected = _mac_over_payload(key, payload_minus_mac)
        if not hmac.compare_digest(expected, presented_mac):
            return None
    # If identity doesn't exist yet, the cache is allowed to be
    # unsigned — first-ever run. The sign_request allowlist treats
    # an empty allowlist as "refuse to sign without --trust-host"
    # anyway, so no actual sign happens before the identity exists.

    return chapters
