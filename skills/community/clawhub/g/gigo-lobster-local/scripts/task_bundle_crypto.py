from __future__ import annotations

import base64
import os
import secrets
from typing import Any

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception as error:  # pragma: no cover - exercised in runtime fallback flows
    AESGCM = None  # type: ignore[assignment]
    _CRYPTO_IMPORT_ERROR: Exception | None = error
else:
    _CRYPTO_IMPORT_ERROR = None

BUNDLE_PREFIX = "enc:v1:gcm"
DEFAULT_KEY_ENV = "GIGO_TASK_BUNDLE_KEY"


class TaskBundleCryptoError(RuntimeError):
    """Raised when an encrypted task bundle cannot be processed safely."""


def _require_crypto_backend() -> None:
    if AESGCM is not None:
        return
    detail = str(_CRYPTO_IMPORT_ERROR) if _CRYPTO_IMPORT_ERROR else "No module named 'cryptography'"
    raise TaskBundleCryptoError(
        "当前运行环境缺少 cryptography，暂时无法处理加密题包；"
        "请先安装 cryptography 或改用公开 demo 包。"
        f"（{detail}）"
    )


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _b64_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def generate_bundle_key() -> str:
    return _b64_encode(secrets.token_bytes(32))


def load_task_bundle_key(env_var: str = DEFAULT_KEY_ENV) -> bytes | None:
    raw = os.environ.get(env_var, "").strip()
    if not raw:
        return None

    key: bytes
    try:
        if len(raw) == 64 and all(char in "0123456789abcdefABCDEF" for char in raw):
            key = bytes.fromhex(raw)
        else:
            key = _b64_decode(raw)
    except Exception as error:
        raise TaskBundleCryptoError(f"{env_var} 格式不正确：{error}") from error

    if len(key) != 32:
        raise TaskBundleCryptoError(f"{env_var} 必须是 32 字节 AES-256 密钥。")
    return key


def is_encrypted_value(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(f"{BUNDLE_PREFIX}:")


def encrypt_text(plain_text: str, key: bytes) -> str:
    _require_crypto_backend()
    nonce = secrets.token_bytes(12)
    cipher = AESGCM(key).encrypt(nonce, plain_text.encode("utf-8"), None)
    return f"{BUNDLE_PREFIX}:{_b64_encode(nonce)}:{_b64_encode(cipher)}"


def decrypt_text(value: str, key: bytes) -> str:
    if not is_encrypted_value(value):
        return value
    _require_crypto_backend()

    parts = value.split(":")
    if len(parts) != 5:
        raise TaskBundleCryptoError("加密任务字段格式无效。")

    nonce = _b64_decode(parts[3])
    cipher = _b64_decode(parts[4])
    try:
        plain_text = AESGCM(key).decrypt(nonce, cipher, None)
    except Exception as error:
        raise TaskBundleCryptoError("任务包解密失败，请检查 GIGO_TASK_BUNDLE_KEY。") from error
    return plain_text.decode("utf-8")


def encrypt_task_package(plain_package: dict[str, Any], key: bytes, key_hint: str | None = None) -> dict[str, Any]:
    encrypted_tasks: list[dict[str, Any]] = []
    for task in plain_package.get("tasks", []):
        encrypted_tasks.append(
            {
                "id": task["id"],
                "prompt_encrypted": encrypt_text(task["prompt"], key),
                "rubric_encrypted": encrypt_text(task["rubric"], key),
                "dish_name": task["dish_name"],
                "dish_hint": task["dish_hint"],
                "primary_dimensions": task["primary_dimensions"],
                "secondary_dimensions": task["secondary_dimensions"],
                "timeout_seconds": int(task.get("timeout_seconds", 300)),
                "setup": task.get("setup") or {},
            }
        )

    return {
        "version": plain_package["version"],
        "tasks": encrypted_tasks,
        "encryption_key_hint": key_hint or f"{DEFAULT_KEY_ENV}:aes-256-gcm",
    }
