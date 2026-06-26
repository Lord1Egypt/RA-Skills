"""
Nex Life Logger - Secure API Key Storage
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Storage methods by platform:
  - Windows: Windows Credential Manager (preferred) or DPAPI-encrypted file
  - macOS/Linux: Owner-only permission file (chmod 600). For stronger security,
    set the AI_API_KEY environment variable instead.

No API keys are stored or transmitted unless the user explicitly configures them.
"""
import sys
import os
import platform
import ctypes
import json
import base64
from pathlib import Path

SERVICE_NAME = "LifeLogger"
ACCOUNT_NAME = "AI_API_KEY"


def _get_key_file():
    data_dir = Path.home() / ".life-logger"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / ".keystore"


def _win_store(key):
    import subprocess
    subprocess.run(["cmdkey", "/delete:" + SERVICE_NAME], capture_output=True)
    result = subprocess.run(
        ["cmdkey", "/generic:" + SERVICE_NAME, "/user:" + ACCOUNT_NAME, "/pass:" + key],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Failed to store credential: " + result.stderr)


def _win_retrieve():
    try:
        import ctypes.wintypes
        CRED_TYPE_GENERIC = 1

        class CREDENTIAL(ctypes.Structure):
            _fields_ = [
                ("Flags", ctypes.wintypes.DWORD),
                ("Type", ctypes.wintypes.DWORD),
                ("TargetName", ctypes.c_wchar_p),
                ("Comment", ctypes.c_wchar_p),
                ("LastWritten", ctypes.wintypes.FILETIME),
                ("CredentialBlobSize", ctypes.wintypes.DWORD),
                ("CredentialBlob", ctypes.POINTER(ctypes.c_char)),
                ("Persist", ctypes.wintypes.DWORD),
                ("AttributeCount", ctypes.wintypes.DWORD),
                ("Attributes", ctypes.c_void_p),
                ("TargetAlias", ctypes.c_wchar_p),
                ("UserName", ctypes.c_wchar_p),
            ]

        advapi32 = ctypes.windll.advapi32
        pcred = ctypes.POINTER(CREDENTIAL)()
        ok = advapi32.CredReadW(SERVICE_NAME, CRED_TYPE_GENERIC, 0, ctypes.byref(pcred))
        if not ok:
            return None
        cred = pcred.contents
        blob = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize)
        key = blob.decode("utf-16-le").rstrip("\x00")
        advapi32.CredFree(pcred)
        return key if key else None
    except Exception:
        return None


def _win_delete():
    import subprocess
    subprocess.run(["cmdkey", "/delete:" + SERVICE_NAME], capture_output=True)


def _fallback_store(key):
    kf = _get_key_file()
    if platform.system() == "Windows":
        try:
            from ctypes import wintypes
            DATA_BLOB = type("DATA_BLOB", (ctypes.Structure,), {
                "_fields_": [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
            })
            raw = key.encode("utf-8")
            blob_in = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw), ctypes.POINTER(ctypes.c_char)))
            blob_out = DATA_BLOB()
            if ctypes.windll.crypt32.CryptProtectData(
                ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
            ):
                encrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
                kf.write_bytes(base64.b64encode(encrypted))
                ctypes.windll.kernel32.LocalFree(blob_out.pbData)
                return
        except Exception:
            pass
    kf.write_text(base64.b64encode(key.encode()).decode())
    # Set restrictive file permissions (owner read/write only)
    if platform.system() != "Windows":
        import stat
        os.chmod(str(kf), stat.S_IRUSR | stat.S_IWUSR)


def _fallback_retrieve():
    kf = _get_key_file()
    if not kf.exists():
        return None
    data = kf.read_bytes()
    if platform.system() == "Windows":
        try:
            from ctypes import wintypes
            DATA_BLOB = type("DATA_BLOB", (ctypes.Structure,), {
                "_fields_": [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
            })
            encrypted = base64.b64decode(data)
            blob_in = DATA_BLOB(len(encrypted), ctypes.cast(ctypes.create_string_buffer(encrypted), ctypes.POINTER(ctypes.c_char)))
            blob_out = DATA_BLOB()
            if ctypes.windll.crypt32.CryptUnprotectData(
                ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
            ):
                result = ctypes.string_at(blob_out.pbData, blob_out.cbData).decode("utf-8")
                ctypes.windll.kernel32.LocalFree(blob_out.pbData)
                return result
        except Exception:
            pass
    try:
        return base64.b64decode(data).decode()
    except Exception:
        return None


def store_api_key(key):
    if platform.system() == "Windows":
        try:
            _win_store(key)
            return
        except Exception:
            pass
    _fallback_store(key)


def get_api_key():
    env_key = os.environ.get("AI_API_KEY", "")
    if env_key:
        return env_key
    if platform.system() == "Windows":
        try:
            key = _win_retrieve()
            if key:
                return key
        except Exception:
            pass
    key = _fallback_retrieve()
    return key or ""


def delete_api_key():
    if platform.system() == "Windows":
        _win_delete()
    kf = _get_key_file()
    if kf.exists():
        kf.unlink()
