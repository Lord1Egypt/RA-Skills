#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared credential storage compatible with insentek-openapi CLI."""

from __future__ import annotations

import base64
import getpass
import hashlib
import json
import os
import platform
import socket
import stat
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "insentek"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
CREDENTIALS_VERSION = 2
SCRYPT_SALT = b"insentek-skill-salt-v1"
KEY_MATERIAL_SUFFIX = ":insentek-openapi-skill"
PACKAGE_NAME = "@insentek/openapi-skill"

NOT_CONNECTED_MESSAGE = """这台电脑还没有连接 Insentek API，需要先完成一次本地配置，通常 1 分钟就好。

请在终端运行：

npx @insentek/openapi-skill login

按提示输入 appid 和 secret 即可（加密保存在本机，无需发到这个对话）。配置完成后回来继续提问，我接着帮你处理。"""

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


def derive_key() -> bytes:
    username = getpass.getuser()
    hostname = socket.gethostname()
    material = f"{hostname}:{username}{KEY_MATERIAL_SUFFIX}".encode("utf-8")
    return hashlib.scrypt(material, salt=SCRYPT_SALT, n=2**14, r=8, p=1, dklen=32)


def decrypt_field(payload_b64: str) -> str:
    if not HAS_CRYPTO:
        raise RuntimeError(
            "Encrypted credentials require the cryptography package. "
            f"Install it with `pip install cryptography` or run `npx {PACKAGE_NAME} login`."
        )

    raw = base64.b64decode(payload_b64)
    nonce = raw[:12]
    tag = raw[12:28]
    ciphertext = raw[28:]
    aesgcm = AESGCM(derive_key())
    return aesgcm.decrypt(nonce, ciphertext + tag, None).decode("utf-8")


def _normalize_loaded_credentials(raw: dict | None) -> dict | None:
    if not raw or not isinstance(raw, dict):
        return None

    if raw.get("version", 0) >= CREDENTIALS_VERSION and raw.get("encrypted"):
        try:
            return {
                "appid": raw.get("appid"),
                "secret": decrypt_field(raw["secret_enc"]),
                "token": decrypt_field(raw["token_enc"]) if raw.get("token_enc") else None,
                "token_updated_at": raw.get("token_updated_at"),
                "created_at": raw.get("created_at"),
                "version": raw.get("version"),
                "encrypted": True,
            }
        except Exception:
            return None

    if raw.get("appid") and raw.get("secret"):
        return {
            "appid": raw.get("appid"),
            "secret": raw.get("secret"),
            "token": raw.get("token"),
            "token_updated_at": raw.get("token_updated_at"),
            "created_at": raw.get("created_at"),
            "version": raw.get("version", 1),
            "encrypted": False,
        }

    return None


def load_credentials() -> dict | None:
    if not CREDENTIALS_FILE.exists():
        return None

    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return _normalize_loaded_credentials(raw)
    except (json.JSONDecodeError, OSError):
        return None


def save_credentials(appid: str, secret: str, token: str | None = None) -> dict:
    if not HAS_CRYPTO:
        raise RuntimeError(
            f"Saving encrypted credentials requires cryptography or `npx {PACKAGE_NAME} login`."
        )

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone().isoformat()

    def encrypt_field(value: str) -> str:
        aesgcm = AESGCM(derive_key())
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, value.encode("utf-8"), None)
        tag = ciphertext[-16:]
        body = ciphertext[:-16]
        return base64.b64encode(nonce + tag + body).decode("ascii")

    payload = {
        "version": CREDENTIALS_VERSION,
        "encrypted": True,
        "appid": appid,
        "secret_enc": encrypt_field(secret),
        "token_enc": encrypt_field(token) if token else None,
        "token_updated_at": now if token else None,
        "created_at": now,
    }

    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    if platform.system() != "Windows":
        os.chmod(CREDENTIALS_FILE, stat.S_IRUSR | stat.S_IWUSR)

    return payload


def update_token(token: str) -> dict | None:
    creds = load_credentials()
    if not creds:
        return None
    return save_credentials(creds["appid"], creds["secret"], token=token)


def clear_credentials() -> bool:
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()
        return True
    return False


def mask_secret(secret: str | None) -> str:
    if not secret:
        return "****"
    if len(secret) <= 8:
        return "****"
    return f"{secret[:4]}****{secret[-4:]}"


def mask_token(token: str | None) -> str:
    if not token:
        return "(not cached)"
    if len(token) <= 12:
        return "****"
    return f"{token[:8]}****{token[-4:]}"
