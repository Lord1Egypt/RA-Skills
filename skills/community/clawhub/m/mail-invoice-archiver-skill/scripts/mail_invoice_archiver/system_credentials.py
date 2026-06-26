from __future__ import annotations

import platform
import re
import shutil
import subprocess


def system_store_spec() -> dict[str, object]:
    current = platform.system()
    if current == "Darwin":
        available = shutil.which("security") is not None
        return {
            "platform": current,
            "available": available,
            "recommended": available,
            "label": "macOS Keychain",
            "notes": "Uses macOS Keychain. Best option on macOS.",
        }
    if current == "Windows":
        return {
            "platform": current,
            "available": True,
            "recommended": True,
            "label": "Windows Credential Manager",
            "notes": "Uses Windows Credential Manager. Best option on Windows.",
        }
    return {
        "platform": current or "Unknown",
        "available": False,
        "recommended": False,
        "label": "system credential store",
        "notes": "Not implemented on this platform in this runtime. Use env, config, or prompt.",
    }


def read_system_secret(service: str) -> tuple[str, str]:
    spec = system_store_spec()
    current = str(spec["platform"])
    if current == "Darwin":
        return _read_keychain_secret(service)
    if current == "Windows":
        return _read_windows_secret(service)
    raise RuntimeError("System credential store is not available on this platform")


def store_system_secret(service: str, email: str, secret: str) -> None:
    spec = system_store_spec()
    current = str(spec["platform"])
    if current == "Darwin":
        _store_keychain_secret(service, email, secret)
        return
    if current == "Windows":
        _store_windows_secret(service, email, secret)
        return
    raise RuntimeError("System credential store is not available on this platform")


def _read_keychain_secret(service: str) -> tuple[str, str]:
    raw = subprocess.check_output(
        ["security", "find-generic-password", "-s", service],
        stderr=subprocess.STDOUT,
        text=True,
    )
    match = re.search(r'"acct"<blob>="([^"]+)"', raw)
    account = match.group(1) if match else ""
    password = subprocess.check_output(
        ["security", "find-generic-password", "-s", service, "-w"],
        text=True,
    ).strip()
    if not account:
        raise RuntimeError(f"Keychain item {service!r} does not expose an account name")
    return account, password


def _store_keychain_secret(service: str, email: str, secret: str) -> None:
    subprocess.run(
        [
            "security",
            "add-generic-password",
            "-U",
            "-a",
            email,
            "-s",
            service,
            "-w",
            secret,
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def _read_windows_secret(service: str) -> tuple[str, str]:
    api = _windows_api()
    credential_ref = api["pointer_type"]()
    ok = api["read"](service, api["generic_type"], 0, api["byref"](credential_ref))
    if not ok:
        raise _windows_runtime_error(f"Windows Credential Manager could not read {service!r}")
    try:
        credential = credential_ref.contents
        account = credential.UserName or ""
        secret = ""
        if credential.CredentialBlob and credential.CredentialBlobSize:
            secret = api["string_at"](credential.CredentialBlob, credential.CredentialBlobSize).decode("utf-8")
        if not account:
            raise RuntimeError(f"Windows credential {service!r} does not expose an account name")
        return account, secret
    finally:
        api["free"](credential_ref)


def _store_windows_secret(service: str, email: str, secret: str) -> None:
    api = _windows_api()
    blob = secret.encode("utf-8")
    credential = api["credential_type"]()
    credential.Flags = 0
    credential.Type = api["generic_type"]
    credential.TargetName = service
    credential.Comment = None
    credential.CredentialBlobSize = len(blob)
    if blob:
        blob_buffer = (api["byte_type"] * len(blob)).from_buffer_copy(blob)
        credential.CredentialBlob = api["cast"](blob_buffer, api["lpbyte_type"])
    else:
        credential.CredentialBlob = None
    credential.Persist = api["persist_local_machine"]
    credential.AttributeCount = 0
    credential.Attributes = None
    credential.TargetAlias = None
    credential.UserName = email
    ok = api["write"](api["byref"](credential), 0)
    if not ok:
        raise _windows_runtime_error(f"Windows Credential Manager could not write {service!r}")


def _windows_runtime_error(prefix: str) -> RuntimeError:
    api = _windows_api()
    code = api["get_last_error"]()
    message = api["format_error"](code).strip() or f"Win32 error {code}"
    return RuntimeError(f"{prefix}: {message}")


def _windows_api() -> dict[str, object]:
    if platform.system() != "Windows":
        raise RuntimeError("Windows Credential Manager helpers were loaded on a non-Windows platform")

    import ctypes
    from ctypes import wintypes

    byte_type = ctypes.c_ubyte
    lpbyte_type = ctypes.POINTER(byte_type)

    class FILETIME(ctypes.Structure):
        _fields_ = [
            ("dwLowDateTime", wintypes.DWORD),
            ("dwHighDateTime", wintypes.DWORD),
        ]

    class CREDENTIAL_ATTRIBUTEW(ctypes.Structure):
        pass

    credential_attribute_pointer = ctypes.POINTER(CREDENTIAL_ATTRIBUTEW)
    CREDENTIAL_ATTRIBUTEW._fields_ = [
        ("Keyword", wintypes.LPWSTR),
        ("Flags", wintypes.DWORD),
        ("ValueSize", wintypes.DWORD),
        ("Value", lpbyte_type),
    ]

    class CREDENTIALW(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR),
            ("Comment", wintypes.LPWSTR),
            ("LastWritten", FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", lpbyte_type),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", credential_attribute_pointer),
            ("TargetAlias", wintypes.LPWSTR),
            ("UserName", wintypes.LPWSTR),
        ]

    credential_pointer = ctypes.POINTER(CREDENTIALW)
    advapi32 = ctypes.WinDLL("Advapi32", use_last_error=True)
    cred_read = advapi32.CredReadW
    cred_read.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(credential_pointer),
    ]
    cred_read.restype = wintypes.BOOL

    cred_write = advapi32.CredWriteW
    cred_write.argtypes = [ctypes.POINTER(CREDENTIALW), wintypes.DWORD]
    cred_write.restype = wintypes.BOOL

    cred_free = advapi32.CredFree
    cred_free.argtypes = [ctypes.c_void_p]
    cred_free.restype = None

    return {
        "byref": ctypes.byref,
        "cast": ctypes.cast,
        "string_at": ctypes.string_at,
        "get_last_error": ctypes.get_last_error,
        "format_error": ctypes.FormatError,
        "byte_type": byte_type,
        "lpbyte_type": lpbyte_type,
        "credential_type": CREDENTIALW,
        "pointer_type": credential_pointer,
        "read": cred_read,
        "write": cred_write,
        "free": cred_free,
        "generic_type": 1,
        "persist_local_machine": 2,
    }
