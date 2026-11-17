#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Owner-only filesystem hardening for the InfinityContext archive.

Portable core: Python standard library only. No shell, no subprocess, no
network access.

Why this module exists
----------------------
The archive stores conversation history. On a shared machine the process umask
(commonly 0022) would create the archive directory as 0755 and the SQLite files
as 0644, so any other local account could read them. This module closes that
gap:

* POSIX   - directories are forced to 0700 and files to 0600, then the result is
            re-read with ``lstat`` to prove the mode took effect; a new file is
            created atomically with ``O_CREAT | O_EXCL | O_NOFOLLOW`` and 0600,
            so it never exists with wider permissions (no check-then-chmod race).
* Windows - the DACL is replaced by a protected DACL that grants only the
            current user and LOCAL SYSTEM, using the documented Win32 security
            APIs through ctypes. No external program is started.

Policy (fail-closed)
--------------------
* A pre-existing archive directory owned by another account is REFUSED.
* A pre-existing archive directory that is merely too permissive is tightened.
* A symbolic link (or a Windows directory junction) anywhere on the target
  path is REFUSED: every existing component is inspected, not just the parent.
* If owner-only access cannot be enforced (unsupported filesystem, API
  unavailable, ACL call rejected), this module raises ``UnsafeArchiveError``.
  It never returns a "best effort" success. The caller decides whether to abort
  (default) or to continue after an explicit opt-out, and the opt-out is
  reported to the user.
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

IS_WINDOWS = sys.platform == "win32"

DIR_MODE = 0o700
FILE_MODE = 0o600


class UnsafeArchiveError(PermissionError):
    """Owner-only access could not be guaranteed; the archive must not be used."""


def _warn(message: str) -> None:
    print(f"SECURITY_WARN: {message}", file=sys.stderr)


def _reject_symlink(path: Path) -> None:
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise UnsafeArchiveError(f"cannot inspect {path}: {exc}") from exc
    if stat.S_ISLNK(st.st_mode):
        raise UnsafeArchiveError(f"refusing to use a symbolic link: {path}")


def _norm_path(path: os.PathLike | str) -> str:
    """Absolute, normalised, case-folded on Windows (for comparison only)."""
    text = os.path.normpath(os.path.abspath(str(path)))
    return os.path.normcase(text) if IS_WINDOWS else text


def _reject_symlinked_parent(target: Path) -> None:
    """Refuse when any existing component of the target's path is a link.

    Inspecting only ``target.parent`` misses a link higher up: for
    ``/trusted/link/subdir/archive.db`` where ``/trusted/link`` is a link and
    ``subdir`` is a real directory, ``os.path.islink(target.parent)`` is false
    and the write would follow the earlier link. Every existing ancestor is
    therefore checked twice: ``os.path.islink`` catches POSIX/Windows symbolic
    links, and the resolved-path comparison additionally catches Windows
    directory junctions, for which ``os.path.islink`` returns false.
    """
    components: list[Path] = []
    current = target.parent
    while True:
        components.append(current)
        parent = current.parent
        if parent == current:
            break
        current = parent

    for component in reversed(components):
        if os.path.islink(component):
            raise UnsafeArchiveError(
                f"refusing to operate inside a symbolic link directory: {component}"
            )
        try:
            resolved = os.path.realpath(component)
        except OSError as exc:
            raise UnsafeArchiveError(f"cannot resolve {component}: {exc}") from exc
        if _norm_path(component) != _norm_path(resolved):
            raise UnsafeArchiveError(
                "refusing to operate through a redirected path component: "
                f"{component} resolves to {resolved}"
            )


# ---------------------------------------------------------------------------
# POSIX
# ---------------------------------------------------------------------------

def _posix_tighten(path: Path, is_dir: bool) -> None:
    mode = DIR_MODE if is_dir else FILE_MODE
    _reject_symlink(path)
    try:
        os.chmod(path, mode)
    except OSError as exc:
        raise UnsafeArchiveError(
            f"cannot apply mode {oct(mode)} to {path}: {exc}"
        ) from exc

    st = os.lstat(path)
    actual = stat.S_IMODE(st.st_mode)
    if actual != mode:
        raise UnsafeArchiveError(
            f"mode was not enforced on {path}: expected {oct(mode)}, got {oct(actual)}"
        )
    getuid = getattr(os, "getuid", None)
    if getuid is not None and st.st_uid != getuid():
        raise UnsafeArchiveError(
            f"{path} is owned by uid {st.st_uid}, not the current user {getuid()}"
        )


# ---------------------------------------------------------------------------
# Windows (ctypes, no external process)
# ---------------------------------------------------------------------------

def _windows_tighten(target: Path, is_dir: bool) -> None:
    """Replace the DACL with a protected DACL for the current user + SYSTEM."""
    if not IS_WINDOWS:
        raise UnsafeArchiveError("Windows ACL helper called on a non-Windows host")

    import ctypes
    from ctypes import wintypes

    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    SE_FILE_OBJECT = 1
    DACL_SECURITY_INFORMATION = 0x00000004
    PROTECTED_DACL_SECURITY_INFORMATION = 0x80000000
    TOKEN_QUERY = 0x0008
    TOKEN_USER = 1
    ACL_REVISION = 2
    OBJECT_INHERIT_ACE = 0x1
    CONTAINER_INHERIT_ACE = 0x2
    FILE_ALL_ACCESS = 0x001F01FF
    LOCAL_SYSTEM_SID = "S-1-5-18"

    advapi32.OpenProcessToken.argtypes = [
        wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE),
    ]
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.GetTokenInformation.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
        wintypes.DWORD, ctypes.POINTER(wintypes.DWORD),
    ]
    advapi32.GetTokenInformation.restype = wintypes.BOOL
    advapi32.ConvertStringSidToSidW.argtypes = [
        wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_void_p),
    ]
    advapi32.ConvertStringSidToSidW.restype = wintypes.BOOL
    advapi32.InitializeAcl.argtypes = [ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD]
    advapi32.InitializeAcl.restype = wintypes.BOOL
    advapi32.AddAccessAllowedAceEx.argtypes = [
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
        wintypes.DWORD, ctypes.c_void_p,
    ]
    advapi32.AddAccessAllowedAceEx.restype = wintypes.BOOL
    advapi32.SetNamedSecurityInfoW.argtypes = [
        wintypes.LPWSTR, ctypes.c_int, wintypes.DWORD, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
    ]
    advapi32.SetNamedSecurityInfoW.restype = wintypes.DWORD
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]

    proc_handle = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(
        kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(proc_handle)
    ):
        raise UnsafeArchiveError(
            f"OpenProcessToken failed (winerror {ctypes.get_last_error()})"
        )

    user_sid_buffer = None
    try:
        size = wintypes.DWORD(0)
        advapi32.GetTokenInformation(proc_handle, TOKEN_USER, None, 0, ctypes.byref(size))
        if not size.value:
            raise UnsafeArchiveError("GetTokenInformation size probe failed")
        user_sid_buffer = ctypes.create_string_buffer(size.value)
        if not advapi32.GetTokenInformation(
            proc_handle, TOKEN_USER, user_sid_buffer, size.value, ctypes.byref(size)
        ):
            raise UnsafeArchiveError(
                f"GetTokenInformation failed (winerror {ctypes.get_last_error()})"
            )
    finally:
        kernel32.CloseHandle(proc_handle)

    # TOKEN_USER begins with SID_AND_ATTRIBUTES { PSID Sid; DWORD Attributes; }
    user_sid = ctypes.cast(user_sid_buffer, ctypes.POINTER(ctypes.c_void_p))[0]

    system_sid = ctypes.c_void_p()
    if not advapi32.ConvertStringSidToSidW(
        LOCAL_SYSTEM_SID, ctypes.byref(system_sid)
    ):
        raise UnsafeArchiveError(
            f"ConvertStringSidToSidW failed (winerror {ctypes.get_last_error()})"
        )

    try:
        # Generous fixed buffer: two ACEs fit far inside 1 KiB.
        acl_buffer = ctypes.create_string_buffer(1024)
        acl = ctypes.cast(acl_buffer, ctypes.c_void_p)
        if not advapi32.InitializeAcl(acl, 1024, ACL_REVISION):
            raise UnsafeArchiveError(
                f"InitializeAcl failed (winerror {ctypes.get_last_error()})"
            )
        inherit = (OBJECT_INHERIT_ACE | CONTAINER_INHERIT_ACE) if is_dir else 0
        for sid, label in ((user_sid, "current user"), (system_sid.value, "SYSTEM")):
            if not advapi32.AddAccessAllowedAceEx(
                acl, ACL_REVISION, inherit, FILE_ALL_ACCESS, sid
            ):
                raise UnsafeArchiveError(
                    f"AddAccessAllowedAceEx({label}) failed "
                    f"(winerror {ctypes.get_last_error()})"
                )
        flags = DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION
        rc = advapi32.SetNamedSecurityInfoW(
            str(target), SE_FILE_OBJECT, flags, None, None, acl, None
        )
        if rc != 0:
            raise UnsafeArchiveError(
                f"SetNamedSecurityInfoW failed for {target} (winerror {rc})"
            )
    finally:
        kernel32.LocalFree(system_sid)


def _tighten(target: Path, is_dir: bool) -> None:
    if IS_WINDOWS:
        _windows_tighten(target, is_dir)
    else:
        _posix_tighten(target, is_dir)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _assert_owned_by_current_user(target: Path) -> None:
    if IS_WINDOWS:
        return
    getuid = getattr(os, "getuid", None)
    if getuid is None:  # platform cannot report ownership
        return
    try:
        st = os.lstat(target)
    except OSError as exc:
        raise UnsafeArchiveError(f"cannot stat {target}: {exc}") from exc
    if st.st_uid != getuid():
        raise UnsafeArchiveError(
            f"archive directory {target} is owned by uid {st.st_uid}, "
            f"not the current user {getuid()}; refusing to use it"
        )


def assert_safe_directory(path: str | os.PathLike) -> None:
    """Validate an existing archive directory without creating or changing it."""
    target = Path(path).expanduser()
    _reject_symlink(target)
    if not target.is_dir():
        raise UnsafeArchiveError(f"archive path is not a directory: {target}")
    _assert_owned_by_current_user(target)


def secure_directory(path: str | os.PathLike) -> None:
    """Create the archive directory if needed and force owner-only access.

    Raises ``UnsafeArchiveError`` when owner-only access cannot be guaranteed.
    """
    target = Path(path).expanduser()
    _reject_symlinked_parent(target)

    created = False
    if target.exists():
        _reject_symlink(target)
        if not target.is_dir():
            raise UnsafeArchiveError(f"archive path is not a directory: {target}")
        _assert_owned_by_current_user(target)
    else:
        try:
            os.makedirs(target, exist_ok=False)
            created = True
        except FileExistsError:
            _reject_symlink(target)
            if not target.is_dir():
                raise UnsafeArchiveError(f"archive path is not a directory: {target}")
        except OSError as exc:
            raise UnsafeArchiveError(
                f"cannot create archive directory {target}: {exc}"
            ) from exc

    try:
        _tighten(target, is_dir=True)
    except UnsafeArchiveError:
        if created:
            # Never leave a directory we created behind in an unsecured state.
            try:
                target.rmdir()
            except OSError:
                pass
        raise


def secure_file(path: str | os.PathLike) -> None:
    """Create (atomically, owner-only) and tighten a single archive file."""
    target = Path(path).expanduser()
    _reject_symlinked_parent(target)

    if target.exists():
        _reject_symlink(target)
        if not target.is_file():
            raise UnsafeArchiveError(f"archive path is not a regular file: {target}")
    else:
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(str(target), flags, FILE_MODE)
        except FileExistsError:
            # Lost a creation race: the file exists now, so tighten it instead.
            _reject_symlink(target)
        except OSError as exc:
            raise UnsafeArchiveError(f"cannot create {target}: {exc}") from exc
        else:
            os.close(fd)

    _tighten(target, is_dir=False)


def secure_sidecars(db_path: str | os.PathLike) -> int:
    """Tighten the database and the ``-wal``/``-shm`` files SQLite creates.

    Raises on the first sidecar that cannot be secured, so the caller can roll
    the whole archive back instead of leaving a half-protected store.
    """
    base = Path(db_path).expanduser()
    locked = 0
    for suffix in ("", "-wal", "-shm"):
        candidate = Path(f"{base}{suffix}")
        if not candidate.exists():
            continue
        secure_file(candidate)
        locked += 1
    return locked


def permissions_enforced(path: str | os.PathLike, is_dir: bool) -> bool | None:
    """Report owner-only mode: True/False on POSIX, None when unreportable."""
    if IS_WINDOWS:
        return None
    try:
        mode = stat.S_IMODE(os.lstat(Path(path).expanduser()).st_mode)
    except OSError:
        return False
    return mode == (DIR_MODE if is_dir else FILE_MODE)
