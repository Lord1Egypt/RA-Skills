"""Private key guard — encrypted V3 keystore (Web3 Secret Storage).

AUDIT FIX (High — "Intent-Code Divergence", 98%): version 1.0.2 claimed the
key "never leaves your machine" but passed it as a command-line ARGUMENT to
`clawdbot config set`, exposing it via:

  * `ps aux` / `/proc/<pid>/cmdline` — any process on the host can read it;
  * shell history;
  * parent-process logs.

Here the key NEVER transits argv, nor an exported environment variable, nor is
it ever printed. It is encrypted at rest with scrypt+AES (`eth_account`, the
same format as official Ethereum keystores) and only decrypted in memory, at
the moment of signing an order.

Key resolution order (first one that exists wins):
  1. `POLYMARKET_KEY` in the environment — legacy/CI mode. Warns: only use with
     a dedicated, disposable wallet.
  2. Encrypted keystore at ~/.openclaw/polymarket-agent/keystore.json, opened
     with the passphrase in `POLYMARKET_PASSPHRASE` or prompted in the terminal.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Optional

from .paths import check_permissions, keystore_path, write_private

PRIVATE_KEY_RE = re.compile(r"^0x[0-9a-fA-F]{64}$")
PASSPHRASE_ENV = "POLYMARKET_PASSPHRASE"
LEGACY_KEY_ENV = "POLYMARKET_KEY"
LEGACY_ALLOW_ENV = "POLYMARKET_ALLOW_ENV_KEY"


class KeystoreError(RuntimeError):
    """Failure reading, writing or decrypting the keystore."""


@dataclass(frozen=True)
class LoadedKey:
    """Key held in memory. `source` feeds the warnings shown to the user."""

    private_key: str
    address: str
    source: str  # "keystore" | "env"

    def __repr__(self) -> str:  # pragma: no cover - anti-leak safeguard
        return f"LoadedKey(address={self.address!r}, source={self.source!r})"

    __str__ = __repr__


def normalize_private_key(raw: str) -> str:
    """Validate and normalize. NEVER includes the key material in the exception."""
    key = (raw or "").strip()
    if not key:
        raise KeystoreError("Empty private key.")
    if not key.startswith("0x"):
        key = "0x" + key
    if not PRIVATE_KEY_RE.match(key):
        raise KeystoreError(
            "Invalid private key: expected 32 bytes in hex "
            "(0x + 64 characters 0-9a-f)."
        )
    if int(key, 16) == 0:
        raise KeystoreError("Invalid private key: zero value.")
    return key.lower()


def address_for(private_key: str) -> str:
    from eth_account import Account

    return Account.from_key(private_key).address


def keystore_exists() -> bool:
    return keystore_path().exists()


def save_key(private_key: str, passphrase: str) -> str:
    """Encrypt and write the key. Returns the derived public address.

    scrypt n=2**18 (eth-account default) — ~1s and ~256MB per attempt, which
    makes offline brute-forcing of the passphrase economically infeasible.
    """
    from eth_account import Account

    key = normalize_private_key(private_key)
    if not passphrase or len(passphrase) < 8:
        raise KeystoreError("The keystore passphrase must be at least 8 characters.")

    encrypted = Account.encrypt(key, passphrase)
    address = Account.from_key(key).address
    payload = {
        "version": 1,
        "address": address,
        "keystore": encrypted,
        "note": "Encrypted V3 keystore. The passphrase is NOT stored here.",
    }
    write_private(keystore_path(), json.dumps(payload, indent=2))
    return address


def keystore_address() -> Optional[str]:
    """The keystore's public address, without needing the passphrase."""
    path = keystore_path()
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("address")
    except (OSError, json.JSONDecodeError):
        return None


def _resolve_passphrase(interactive: bool) -> str:
    env_pass = os.environ.get(PASSPHRASE_ENV)
    if env_pass:
        return env_pass
    if not interactive:
        raise KeystoreError(
            f"Encrypted keystore requires a passphrase. Set {PASSPHRASE_ENV} or "
            "run the command in an interactive terminal."
        )
    import getpass

    try:
        return getpass.getpass("Polymarket keystore passphrase: ")
    except (EOFError, KeyboardInterrupt) as exc:
        raise KeystoreError("Passphrase entry cancelled.") from exc


def _load_from_keystore(path, interactive: bool) -> LoadedKey:
    warning = check_permissions(path)
    if warning:
        raise KeystoreError(
            f"Refusing to use a keystore with insecure permissions.\n{warning}"
        )

    try:
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise KeystoreError(f"Unreadable keystore: {exc}") from exc

    encrypted = payload.get("keystore")
    if not encrypted:
        raise KeystoreError("Corrupted keystore: missing 'keystore' field.")

    from eth_account import Account

    passphrase = _resolve_passphrase(interactive)
    try:
        private_key = Account.decrypt(encrypted, passphrase).hex()
    except ValueError as exc:
        raise KeystoreError("Wrong passphrase for the keystore.") from exc

    key = normalize_private_key(private_key)
    return LoadedKey(key, address_for(key), "keystore")


def _load_from_legacy_env(raw: str) -> LoadedKey:
    """SECURITY FIX (SkillSpector E2, High, 0.93 confidence): the previous
    version checked `POLYMARKET_KEY` FIRST and used it unconditionally —
    a raw private key sitting in an environment variable took silent
    precedence over a properly configured encrypted keystore, and nothing
    warned at the moment it was actually used. Env vars are readable by
    child processes, `/proc/<pid>/environ`, crash dumps and CI logs, so this
    is a strictly weaker path than the keystore.

    Two changes close the gap:
      1. Precedence reversed — see `load_key`: the keystore is tried FIRST,
         so a stray leftover `POLYMARKET_KEY` from testing can never override
         a real keystore.
      2. This path additionally requires `POLYMARKET_ALLOW_ENV_KEY=1` — the
         presence of `POLYMARKET_KEY` alone is no longer sufficient, so it
         cannot activate by accident. A visible warning is printed every time
         it is actually used, not just in `poly doctor`.
    """
    allow = os.environ.get(LEGACY_ALLOW_ENV, "").strip().lower()
    if allow not in {"1", "true", "yes", "on"}:
        raise KeystoreError(
            f"{LEGACY_KEY_ENV} is set, but this insecure path needs explicit "
            f"opt-in: also set {LEGACY_ALLOW_ENV}=1. The key is exposed to any "
            "process that can read this process's environment (ps, "
            "/proc/<pid>/environ, crash dumps, CI logs). Prefer `poly setup`, "
            "which stores an encrypted keystore instead."
        )

    import sys

    print(
        f"⚠ Using {LEGACY_KEY_ENV} from the environment — insecure legacy "
        "path, key visible to child processes. Prefer `poly setup`.",
        file=sys.stderr,
    )
    key = normalize_private_key(raw)
    return LoadedKey(key, address_for(key), "env")


def load_key(interactive: bool = True) -> LoadedKey:
    """Resolve the private key. Raises KeystoreError if unavailable.

    Precedence: the encrypted keystore is tried FIRST, because it is
    strictly safer than an environment variable. `POLYMARKET_KEY` is only a
    gated fallback for when no keystore exists — see `_load_from_legacy_env`.
    """
    path = keystore_path()
    if path.exists():
        return _load_from_keystore(path, interactive)

    legacy = os.environ.get(LEGACY_KEY_ENV)
    if legacy:
        return _load_from_legacy_env(legacy)

    raise KeystoreError(
        "No credential configured. Run `poly setup` to create an "
        "encrypted keystore."
    )


def delete_key() -> bool:
    """Delete the keystore. Returns True if something was removed."""
    path = keystore_path()
    if not path.exists():
        return False
    try:
        # Overwrite before removing: reduces the chance of recovering the
        # ciphertext on filesystems without data journaling.
        size = path.stat().st_size
        write_private(path, "0" * size)
    except OSError:
        pass
    path.unlink(missing_ok=True)
    return True


def redact(value: Optional[str]) -> str:
    """Mask a SECRET for display — reveals none of its characters.

    Showing the last N letters of a private key is a habit inherited from
    credit-card display and makes no sense here: it shrinks the search space
    for anyone with access to the terminal/log, for nothing in return. To
    IDENTIFY which wallet is in use, use `short_address`, which operates on
    the PUBLIC address instead.
    """
    if not value:
        return "<not set>"
    return f"<hidden: {len(value)} characters>"


def short_address(address: Optional[str]) -> str:
    """Shorten a PUBLIC address (not a secret) for display."""
    if not address:
        return "<no wallet>"
    if len(address) <= 12:
        return address
    return f"{address[:6]}…{address[-4:]}"
