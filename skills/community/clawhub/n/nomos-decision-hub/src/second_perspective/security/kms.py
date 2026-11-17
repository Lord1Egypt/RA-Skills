"""KMS abstraction for signing sealed artifacts (v0.5).

NOMOS never lets the engine invent facts; likewise it never lets a stored
report be silently tampered with after sealing. The KMS layer produces a
detached signature over a report's canonical hash using a configured key.

When ``SP_KMS_SECRET`` (or ``SP_KMS_KEY_FILE``) is unset, signing is a no-op and
``is_configured()`` returns ``False`` so callers can skip it transparently. This
keeps existing deployments byte-for-byte compatible until an operator opts in.
"""

from __future__ import annotations

import hashlib
import hmac
import os


class Signer:
    def sign(self, payload: bytes) -> str: ...
    def verify(self, payload: bytes, signature: str) -> bool: ...
    def is_configured(self) -> bool: ...


class LocalKmsSigner(Signer):
    """HMAC-SHA256 signer backed by a local symmetric key.

    Suitable for single-region deployments. For envelope encryption with a
    cloud KMS, subclass :class:`Signer` and delegate to the provider SDK.
    """

    def __init__(self, secret: str | None = None) -> None:
        if secret is not None:
            self._secret = secret
        else:
            self._secret = os.getenv("SP_KMS_SECRET", "").strip()
            key_file = os.getenv("SP_KMS_KEY_FILE", "").strip()
            if not self._secret and key_file:
                try:
                    with open(key_file, "r", encoding="utf-8") as fh:
                        self._secret = fh.read().strip()
                except OSError:
                    self._secret = ""
        self._key = self._secret.encode("utf-8") if self._secret else b""

    def is_configured(self) -> bool:
        return bool(self._key)

    def sign(self, payload: bytes) -> str:
        if not self.is_configured():
            return ""
        return hmac.new(self._key, payload, hashlib.sha256).hexdigest()

    def verify(self, payload: bytes, signature: str) -> bool:
        if not self.is_configured() or not signature:
            return False
        expected = hmac.new(self._key, payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)


def get_signer() -> Signer:
    """Return the configured KMS signer (default: local HMAC signer)."""
    return LocalKmsSigner()
