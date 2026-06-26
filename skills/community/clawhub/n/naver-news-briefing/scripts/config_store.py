from __future__ import annotations

import base64
import ctypes
import json
import os
import sys
import tempfile
from typing import Any, Dict, Mapping, Tuple

from _paths import CONFIG_PATH, ensure_data_dir

DEFAULT_CONFIG: Dict[str, Any] = {
    "naver_api": {
        "client_id": "",
        "client_secret": "",
        "client_secret_enc": "",
        "client_secret_storage": "plain",
        "timeout": 15,
    }
}


def _is_windows_platform() -> bool:
    return sys.platform == "win32"


def _normalize_secret_storage(value: Any) -> str:
    return "dpapi" if str(value or "").strip().lower() == "dpapi" else "plain"


def _dpapi_encrypt_text(text: str) -> str:
    if not _is_windows_platform() or not text:
        return ""
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

    source = text.encode("utf-8")
    source_buffer = (ctypes.c_byte * len(source)).from_buffer_copy(source)
    in_blob = DATA_BLOB(len(source), ctypes.cast(source_buffer, ctypes.POINTER(ctypes.c_byte)))
    out_blob = DATA_BLOB()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    ok = crypt32.CryptProtectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    if not ok:
        return ""
    try:
        encrypted = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        return base64.b64encode(encrypted).decode("ascii")
    finally:
        if out_blob.pbData:
            kernel32.LocalFree(out_blob.pbData)


def _dpapi_decrypt_text(payload: str) -> str:
    if not _is_windows_platform() or not payload:
        return ""
    from ctypes import wintypes

    raw = base64.b64decode(payload)

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

    source_buffer = (ctypes.c_byte * len(raw)).from_buffer_copy(raw)
    in_blob = DATA_BLOB(len(raw), ctypes.cast(source_buffer, ctypes.POINTER(ctypes.c_byte)))
    out_blob = DATA_BLOB()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    ok = crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    if not ok:
        return ""
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData).decode("utf-8")
    finally:
        if out_blob.pbData:
            kernel32.LocalFree(out_blob.pbData)


def encode_client_secret_for_storage(client_secret: str) -> Dict[str, str]:
    plain = str(client_secret or "").strip()
    if not plain:
        return {"client_secret": "", "client_secret_enc": "", "client_secret_storage": "plain"}
    if _is_windows_platform():
        encrypted = _dpapi_encrypt_text(plain)
        if encrypted:
            return {"client_secret": "", "client_secret_enc": encrypted, "client_secret_storage": "dpapi"}
    return {"client_secret": plain, "client_secret_enc": "", "client_secret_storage": "plain"}


def resolve_client_secret_for_runtime(settings: Mapping[str, Any]) -> Tuple[str, bool]:
    plain = str(settings.get("client_secret", "") or "")
    encrypted = str(settings.get("client_secret_enc", "") or "")
    storage = _normalize_secret_storage(settings.get("client_secret_storage", "plain"))
    if _is_windows_platform() and encrypted and storage == "dpapi":
        decrypted = _dpapi_decrypt_text(encrypted)
        if decrypted:
            return decrypted, bool(plain)
    return plain, bool(_is_windows_platform() and plain)


def _write_text_atomic(path: str, text: str) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".config_", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            if not text.endswith("\n"):
                f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def load_config() -> Dict[str, Any]:
    ensure_data_dir()
    if not CONFIG_PATH.exists():
        return json.loads(json.dumps(DEFAULT_CONFIG))
    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    if isinstance(raw, dict):
        merged.update(raw)
        if isinstance(raw.get("naver_api"), dict):
            merged["naver_api"].update(raw["naver_api"])
    return merged


def save_config(config: Dict[str, Any]) -> None:
    ensure_data_dir()
    _write_text_atomic(str(CONFIG_PATH), json.dumps(config, indent=2, ensure_ascii=False))


def set_credentials(client_id: str, client_secret: str, timeout: int = 15) -> Dict[str, Any]:
    config = load_config()
    encoded = encode_client_secret_for_storage(client_secret)
    config["naver_api"].update(
        {
            "client_id": str(client_id or "").strip(),
            "client_secret": encoded["client_secret"],
            "client_secret_enc": encoded["client_secret_enc"],
            "client_secret_storage": encoded["client_secret_storage"],
            "timeout": max(5, min(60, int(timeout))),
        }
    )
    save_config(config)
    return config


def get_runtime_credentials() -> Tuple[str, str, int, Dict[str, Any]]:
    config = load_config()
    settings = config["naver_api"]
    client_secret, needs_migration = resolve_client_secret_for_runtime(settings)
    if needs_migration and client_secret:
        updated = set_credentials(str(settings.get("client_id", "")), client_secret, int(settings.get("timeout", 15)))
        settings = updated["naver_api"]
        client_secret, _ = resolve_client_secret_for_runtime(settings)
    return str(settings.get("client_id", "")).strip(), client_secret.strip(), int(settings.get("timeout", 15)), config
