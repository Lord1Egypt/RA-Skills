"""Local wallet for the JerithChain OpenClaw skill.

The Ed25519 secret key is generated ON this machine, encrypted at rest
(Fernet, key derived from a machine-local secret file, 0600 perms), and
NEVER sent to the node. Transactions are signed locally; only the signed
tx dict is submitted to the node's /x/tx/sendraw endpoint.

Wallet file (0600 JSON): address, vk_hex, enc_sk (Fernet token), created_at.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

try:
    import nacl.signing
except ImportError as e:  # pragma: no cover
    raise SystemExit("jerith: missing dependency pynacl (pip install pynacl)") from e

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError as e:  # pragma: no cover
    raise SystemExit("jerith: missing dependency cryptography") from e


def addr_from_vk(vk: bytes) -> str:
    return "JER" + hashlib.sha256(b"jerith-addr" + vk).hexdigest()[:32].upper()


def _keydir() -> Path:
    d = Path(os.environ.get("JERITH_SKILL_KEYDIR",
                            Path.home() / ".config" / "jerith"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _fernet() -> Fernet:
    """Keyfile: random 32B secret, 0600, created on first use. Encrypts the
    wallet secret key at rest so a leaked wallet file alone is not enough."""
    kf = _keydir() / "wallet.key"
    if kf.exists():
        raw = kf.read_bytes()
    else:
        raw = secrets.token_bytes(32)
        fd = os.open(kf, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
    return Fernet(base64.urlsafe_b64encode(
        hashlib.sha256(b"jerith-skill-wallet" + raw).digest()))


def wallet_path(cfg: dict) -> Path:
    return Path(cfg["wallet_path"]).expanduser()


def wallet_exists(cfg: dict) -> bool:
    return wallet_path(cfg).exists()


def create_wallet(cfg: dict) -> dict:
    """Generate a new keypair and store it encrypted. Refuses to overwrite."""
    p = wallet_path(cfg)
    if p.exists():
        raise SystemExit(f"jerith: wallet already exists at {p} (use `jerith-skill wallet`)")
    sk = nacl.signing.SigningKey.generate()
    vk = bytes(sk.verify_key)
    rec = {
        "address": addr_from_vk(vk),
        "vk_hex": vk.hex(),
        "enc_sk": _fernet().encrypt(bytes(sk)).decode(),
        "created_at": int(time.time()),
    }
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(rec, f, indent=2)
    return rec


def load_wallet(cfg: dict) -> dict:
    p = wallet_path(cfg)
    if not p.exists():
        raise SystemExit("jerith: no wallet yet — run `jerith-skill wallet-create` first")
    try:
        rec = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise SystemExit(f"jerith: wallet file corrupted: {e}")
    for k in ("address", "vk_hex", "enc_sk"):
        if k not in rec:
            raise SystemExit(f"jerith: wallet file missing field {k}")
    return rec


def secret_key(cfg: dict) -> bytes:
    """Decrypt and return the secret key (NEVER print or log this)."""
    rec = load_wallet(cfg)
    try:
        return _fernet().decrypt(rec["enc_sk"].encode())
    except InvalidToken:
        raise SystemExit("jerith: wallet decryption failed (key file mismatch "
                         "or corrupted wallet) — restore from backup")


def export_secret(cfg: dict) -> str:
    """Explicit, user-requested only. Returns hex seed for backup. The caller
    must NEVER log or transmit it."""
    return secret_key(cfg).hex()
