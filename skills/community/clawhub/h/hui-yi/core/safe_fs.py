"""Fail-closed local file access for Hui-Yi's operator-authorized paths.

Every existing ancestor and leaf is checked without resolving links. Reads use
an identity-checked descriptor; writes stage an exclusive sibling and recheck
identities before replacement. Symlinks, Windows reparse points, multiply linked
files and special files are unsupported. These checks are not an OS sandbox:
the containing directories must not be concurrently replaced by a hostile
process (portable Python lacks Windows handle-relative / universal dirfd I/O).
"""
from __future__ import annotations

import fnmatch
import os
import re
import secrets
import stat
from pathlib import Path, PureWindowsPath


class UnsafePathError(ValueError):
    """A path failed the local filesystem boundary; never treat it as missing."""


_DEVICES = re.compile(r"^(?:CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\.|$)", re.I)
_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def _check_component(value: str) -> None:
    if (not value or value in {".", ".."} or value[-1:] in {".", " "}
            or any(ord(char) < 32 or char in '<>:"|?*' for char in value)
            or _DEVICES.match(value.split(".", 1)[0].rstrip(" ") + ".")
            or value.split(".", 1)[0].upper() in {"CONIN$", "CONOUT$", "CLOCK$"}):
        raise UnsafePathError("unsupported or ambiguous path component")


def lexical_path(value: str | Path) -> Path:
    """Make an absolute path without realpath/resolve erasing link evidence."""
    raw = os.fspath(value)
    if not raw or "\x00" in raw:
        raise UnsafePathError("empty or invalid path")
    candidate = Path(raw)
    if os.name == "nt" and candidate.drive and not candidate.is_absolute():
        raise UnsafePathError("drive-relative paths are not supported")
    if os.name == "nt" and raw.startswith(("\\\\?\\", "\\\\.\\")):
        raise UnsafePathError("device namespace paths are not supported")
    if not candidate.is_absolute():
        if candidate.anchor:
            raise UnsafePathError("root-relative paths are not supported")
        candidate = Path.cwd() / candidate
    current = Path(candidate.anchor)
    for component in candidate.parts[1:]:
        if component == "..":
            # CLI paths are operator authority and retain ordinary ../ support.
            # Validate the directory being traversed before dropping it: a
            # symlink/../ sequence must never erase evidence of the symlink.
            check_directory(current)
            current = current.parent
        else:
            _check_component(component)
            current /= component
    return current


def note_path(memory_root: Path, value: object) -> Path:
    raw = str(value or "").replace("\\", "/")
    if not raw or raw != raw.strip() or raw.startswith("/") or PureWindowsPath(raw).drive:
        raise UnsafePathError("note path must be a relative path")
    if raw.startswith("memory/cold/"):
        raw = raw[len("memory/cold/"):]
    parts = raw.split("/")
    for part in parts:
        _check_component(part)
    if not parts[-1].lower().endswith(".md") or parts[-1].lower() in {"index.md", "retrieval-log.md", "_template.md"}:
        raise UnsafePathError("note path must name an ordinary Markdown note")
    root = check_directory(memory_root)
    target = root.joinpath(*parts)
    check_file(target, allow_missing=True)
    if os.name == "nt":
        current = root
        for part in parts:
            current /= part
            try:
                current.lstat()
            except FileNotFoundError:
                break
            # An NTFS 8.3 alias may hide a reserved filename such as
            # RETRIE~1.MD. Preserve case-insensitivity, reject alternate names.
            if Path(_windows_long_path(current)).name.casefold() != part.casefold():
                raise UnsafePathError("alternate Windows note names are not supported")
    return target


def _windows_long_path(path: Path) -> str:
    import ctypes
    from ctypes import wintypes
    api = ctypes.WinDLL("kernel32", use_last_error=True).GetLongPathNameW
    api.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    api.restype = wintypes.DWORD
    needed = api(str(path), None, 0)
    if not needed:
        raise ctypes.WinError(ctypes.get_last_error())
    buffer = ctypes.create_unicode_buffer(needed)
    written = api(str(path), buffer, needed)
    if not written:
        raise ctypes.WinError(ctypes.get_last_error())
    if written >= needed:
        raise UnsafePathError("Windows path changed during name validation")
    return buffer.value


def _identity(info: os.stat_result) -> tuple[int, int, int]:
    return info.st_dev, info.st_ino, stat.S_IFMT(info.st_mode)


def _regular(info: os.stat_result, *, directory: bool) -> None:
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & _REPARSE_POINT:
        raise UnsafePathError("links and reparse points are not supported")
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise UnsafePathError("path ancestor is not a directory")
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise UnsafePathError("only regular files with one link are supported")


def _snapshot(value: str | Path, *, directory: bool = False, allow_missing: bool = False):
    target = lexical_path(value)
    chain = [*reversed(target.parents), target]
    snapshots: list[tuple[Path, os.stat_result | None]] = []
    missing = False
    for index, current in enumerate(chain):
        try:
            info = current.lstat()
        except FileNotFoundError:
            if not allow_missing:
                raise
            missing = True
            snapshots.append((current, None))
            continue
        if missing:
            raise UnsafePathError("path changed during validation")
        _regular(info, directory=index < len(chain) - 1 or directory)
        snapshots.append((current, info))
    return target, snapshots


def _recheck(snapshots) -> None:
    for current, before in snapshots:
        try:
            after = current.lstat()
        except FileNotFoundError:
            if before is None:
                continue
            raise UnsafePathError("path disappeared during file access") from None
        if before is None:
            raise UnsafePathError("path appeared during file access")
        _regular(after, directory=stat.S_ISDIR(before.st_mode))
        if _identity(after) != _identity(before):
            raise UnsafePathError("path identity changed during file access")


def check_file(value: str | Path, *, allow_missing: bool = False) -> Path:
    return _snapshot(value, allow_missing=allow_missing)[0]


def check_directory(value: str | Path, *, allow_missing: bool = False) -> Path:
    return _snapshot(value, directory=True, allow_missing=allow_missing)[0]


def safe_exists(value: str | Path, *, kind: str = "file") -> bool:
    _, chain = _snapshot(value, directory=kind == "directory", allow_missing=True)
    return chain[-1][1] is not None


def preflight_files(*values: str | Path) -> None:
    for value in values:
        check_file(value, allow_missing=True)


def ensure_directory(value: str | Path) -> Path:
    target, chain = _snapshot(value, directory=True, allow_missing=True)
    for current, info in chain:
        if info is None:
            check_directory(current.parent)
            try:
                os.mkdir(current)
            except FileExistsError:
                pass
            check_directory(current)
    return check_directory(target)


def read_bytes(value: str | Path) -> bytes:
    target, chain = _snapshot(value)
    before = chain[-1][1]
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(target, flags)
    try:
        actual = os.fstat(fd)
        _regular(actual, directory=False)
        if before is None or _identity(actual) != _identity(before):
            raise UnsafePathError("file identity changed before read")
        _recheck(chain)
        with os.fdopen(fd, "rb", closefd=False) as stream:
            result = stream.read()
        _recheck(chain)
        return result
    finally:
        os.close(fd)


def read_text(value: str | Path, encoding: str = "utf-8", errors: str = "strict") -> str:
    return read_bytes(value).decode(encoding, errors)


def _windows_security_api():
    """Load only the DACL APIs; do not request SACL/privileged audit access."""
    import ctypes
    from ctypes import wintypes
    api = ctypes.WinDLL("advapi32", use_last_error=True)
    api.GetFileSecurityW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p,
                                    wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    api.GetFileSecurityW.restype = wintypes.BOOL
    api.SetFileSecurityW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
    api.SetFileSecurityW.restype = wintypes.BOOL
    api.SetNamedSecurityInfoW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD,
                                         ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    api.SetNamedSecurityInfoW.restype = wintypes.DWORD
    api.GetSecurityDescriptorControl.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.WORD),
                                                ctypes.POINTER(wintypes.DWORD)]
    api.GetSecurityDescriptorControl.restype = wintypes.BOOL
    api.GetSecurityDescriptorDacl.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.BOOL),
                                             ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.BOOL)]
    api.GetSecurityDescriptorDacl.restype = wintypes.BOOL
    return ctypes, wintypes, api


def _windows_read_dacl(path: Path) -> bytes:
    ctypes, wintypes, api = _windows_security_api()
    needed = wintypes.DWORD()
    if not api.GetFileSecurityW(str(path), 4, None, 0, ctypes.byref(needed)):
        error = ctypes.get_last_error()
        if error != 122:  # ERROR_INSUFFICIENT_BUFFER is the size-query result.
            raise ctypes.WinError(error)
    if not needed.value:
        raise UnsafePathError("Windows DACL descriptor is missing")
    descriptor = ctypes.create_string_buffer(needed.value)
    if not api.GetFileSecurityW(str(path), 4, descriptor, needed.value, ctypes.byref(needed)):
        raise ctypes.WinError(ctypes.get_last_error())
    return descriptor.raw[:needed.value]


def _windows_dacl_signature(descriptor: bytes) -> tuple[int, bytes | None]:
    ctypes, wintypes, api = _windows_security_api()
    buffer = ctypes.create_string_buffer(descriptor)
    control, revision = wintypes.WORD(), wintypes.DWORD()
    if not api.GetSecurityDescriptorControl(buffer, ctypes.byref(control), ctypes.byref(revision)):
        raise ctypes.WinError(ctypes.get_last_error())
    present, defaulted, acl = wintypes.BOOL(), wintypes.BOOL(), ctypes.c_void_p()
    if not api.GetSecurityDescriptorDacl(buffer, ctypes.byref(present), ctypes.byref(acl), ctypes.byref(defaulted)):
        raise ctypes.WinError(ctypes.get_last_error())
    acl_bytes = None
    if present and acl.value:
        # ACL header: BYTE revision, BYTE padding, WORD byte length.
        length = ctypes.c_ushort.from_address(acl.value + 2).value
        acl_bytes = ctypes.string_at(acl.value, length)
    # Preserve presence/defaulting, inheritance request/status and protection,
    # plus exact ACE bytes (including their inherited flags).
    return control.value & 0x150C, acl_bytes


def _windows_apply_dacl(path: Path, descriptor: bytes) -> None:
    ctypes, wintypes, api = _windows_security_api()
    signature = _windows_dacl_signature(descriptor)
    inheritance = 0x80000000 if signature[0] & 0x1000 else 0x20000000
    buffer = ctypes.create_string_buffer(descriptor)
    if signature[0] & 0x0400:
        # The legacy SetFileSecurityW API clears SE_DACL_AUTO_INHERITED even
        # when its input descriptor contains that bit. Use the inheritance-
        # aware API for an auto-inherited source, then require exact equality
        # of control flags and every ACE before any content is written.
        present, defaulted, acl = wintypes.BOOL(), wintypes.BOOL(), ctypes.c_void_p()
        if not api.GetSecurityDescriptorDacl(buffer, ctypes.byref(present), ctypes.byref(acl), ctypes.byref(defaulted)):
            raise ctypes.WinError(ctypes.get_last_error())
        error = api.SetNamedSecurityInfoW(str(path), 1, 4 | inheritance, None, None, acl, None)
        if error:
            raise ctypes.WinError(error)
    elif not api.SetFileSecurityW(str(path), 4 | inheritance, buffer):
        raise ctypes.WinError(ctypes.get_last_error())
    if _windows_dacl_signature(_windows_read_dacl(path)) != signature:
        raise UnsafePathError("Windows DACL could not be preserved exactly")


def atomic_write_bytes(value: str | Path, data: bytes, *, exclusive: bool = False) -> None:
    target, chain = _snapshot(value, allow_missing=True)
    check_directory(target.parent)
    if exclusive and chain[-1][1] is not None:
        raise FileExistsError(target)
    previous = chain[-1][1]
    saved_dacl = _windows_read_dacl(target) if os.name == "nt" and previous is not None else None
    _recheck(chain)
    temporary = target.with_name(f".hui-yi-{secrets.token_hex(16)}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(temporary, flags, 0o600)
    staged = os.fstat(fd)
    try:
        _regular(staged, directory=False)
        _recheck(chain)
        if saved_dacl is not None:
            # A sibling inherits its parent's DACL, which may expose content
            # excluded by the original file's explicit/protected DACL. Copy
            # and verify the original permissions while the sibling is empty.
            _windows_apply_dacl(temporary, saved_dacl)
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(fd)
        if previous is not None and hasattr(os, "fchmod"):
            os.fchmod(fd, stat.S_IMODE(previous.st_mode))
        os.close(fd)
        fd = -1
        _recheck(chain)
        temp_info = temporary.lstat()
        _regular(temp_info, directory=False)
        if _identity(temp_info) != _identity(staged):
            raise UnsafePathError("temporary file identity changed")
        if saved_dacl is not None:
            signature = _windows_dacl_signature(saved_dacl)
            if (_windows_dacl_signature(_windows_read_dacl(target)) != signature
                    or _windows_dacl_signature(_windows_read_dacl(temporary)) != signature):
                raise UnsafePathError("Windows DACL changed during file access")
        os.replace(temporary, target)
    finally:
        if fd >= 0:
            os.close(fd)
        # Never remove an attacker-swapped entry or traverse a changed parent.
        try:
            _recheck(chain[:-1])
            info = temporary.lstat()
            if _identity(info) == _identity(staged):
                temporary.unlink()
        except (FileNotFoundError, UnsafePathError):
            pass


def atomic_write_text(value: str | Path, text: str, encoding: str = "utf-8", *, exclusive: bool = False) -> None:
    atomic_write_bytes(value, text.encode(encoding), exclusive=exclusive)


def iter_files(root: str | Path, pattern: str = "*", *, recursive: bool = True) -> list[Path]:
    """Validate the complete enumeration before callers start mutating files."""
    root = check_directory(root)
    files: list[Path] = []
    pending = [root]
    while pending:
        directory = check_directory(pending.pop())
        with os.scandir(directory) as entries:
            names = sorted(entry.name for entry in entries)
        for name in names:
            _check_component(name)
            candidate = directory / name
            info = candidate.lstat()
            if stat.S_ISDIR(info.st_mode):
                check_directory(candidate)
                if recursive:
                    pending.append(candidate)
            else:
                check_file(candidate)
                if fnmatch.fnmatch(name, pattern):
                    files.append(candidate)
    return sorted(files)
