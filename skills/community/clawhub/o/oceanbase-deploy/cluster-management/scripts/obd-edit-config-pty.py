#!/usr/bin/env python3
"""Apply one reviewed complete YAML through OBD's editor path.

Run this helper on the OBD controller. It allocates a real controlling PTY,
uses itself as OBD's EDITOR, and rewrites OBD's generated temporary file
without replacing its inode. It never answers an OBD prompt.
"""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import pty
import re
import select
import shutil
import signal
import stat
import sys
import tempfile
import time
from pathlib import Path


SOURCE_ENV = "OBD_SKILL_EDIT_SOURCE"
SOURCE_SHA_ENV = "OBD_SKILL_EDIT_SOURCE_SHA256"
BEFORE_SHA_ENV = "OBD_SKILL_EDIT_BEFORE_SHA256"
RESULT_ENV = "OBD_SKILL_EDIT_RESULT"
EDITOR_MODE_ENV = "OBD_SKILL_EDITOR_MODE"
SAFE_CHILD_PATH = "/usr/bin:/bin"
UNTRUSTED_CHILD_ENV = {"BASH_ENV", "CDPATH", "ENV", "GLOBIGNORE", "PERL5OPT", "RUBYOPT", "SHELLOPTS"}

DEPLOYMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
ANSI_RE = re.compile(rb"\x1b\[[0-?]*[ -/]*[@-~]")
PROMPT_RE = re.compile(
    rb"(?i)(?:\[[yn]/[yn]\]|continue\s+(?:to\s+)?edit\?|"
    rb"start\s+a\s+redeployment\?|empty\s+configuration\.\s+continue\s+editing\?|"
    rb"(?:create|edit)\?\s*$)"
)


class EditError(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular_file(path: Path, label: str) -> os.stat_result:
    try:
        info = path.lstat()
    except OSError as exc:
        raise EditError(f"{label} is unavailable: {exc}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise EditError(f"{label} must be a regular, non-symlink file")
    return info


def require_trusted_obd(path_value: str, expected_sha256: str) -> tuple[str, tuple[int, int, int, int, int]]:
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
        raise EditError("--obd-sha256 must be a 64-character hexadecimal SHA-256")

    path = Path(path_value)
    if not path.is_absolute():
        raise EditError("--obd must be an absolute path; PATH lookup and relative paths are not allowed")
    if str(path) != os.path.normpath(str(path)):
        raise EditError("--obd must be a canonical absolute path without dot segments")

    info = require_regular_file(path, "OBD executable")
    if info.st_uid not in {0, os.geteuid()}:
        raise EditError("OBD executable must be owned by root or the current controller user")
    if stat.S_IMODE(info.st_mode) & (stat.S_IWGRP | stat.S_IWOTH):
        raise EditError("OBD executable must not be writable by group or other users")
    if not os.access(path, os.X_OK):
        raise EditError("OBD executable is not executable by the current controller user")

    for parent in path.parents:
        parent_info = parent.lstat()
        if stat.S_ISLNK(parent_info.st_mode) or not stat.S_ISDIR(parent_info.st_mode):
            raise EditError("OBD executable path must not traverse symlinks or non-directories")
        if stat.S_IMODE(parent_info.st_mode) & (stat.S_IWGRP | stat.S_IWOTH):
            raise EditError("OBD executable path must not traverse group- or other-writable directories")

    actual_sha256 = file_sha256(path)
    if actual_sha256.lower() != expected_sha256.lower():
        raise EditError("OBD executable checksum does not match --obd-sha256")

    identity = (info.st_dev, info.st_ino, info.st_uid, info.st_size, info.st_mtime_ns)
    return str(path), identity


def write_result(path: Path, payload: dict[str, object]) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, 0o600)
    try:
        data = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
        os.write(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def create_editor_launcher(run_dir: Path) -> Path:
    interpreter = Path(sys.executable).resolve(strict=True)
    helper = Path(__file__).resolve(strict=True)
    if not interpreter.is_absolute() or any(char.isspace() for char in str(interpreter)):
        raise EditError("the active Python interpreter cannot be represented by a safe absolute shebang")

    launcher = run_dir / "editor-launcher"
    body = (
        f"#!{interpreter}\n"
        "import os\n"
        "import sys\n"
        f"os.execv({str(interpreter)!r}, [{str(interpreter)!r}, {str(helper)!r}, *sys.argv[1:]])\n"
    ).encode("utf-8")
    descriptor = os.open(launcher, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o700)
    try:
        os.write(descriptor, body)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return launcher


def create_child_env() -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in UNTRUSTED_CHILD_ENV
        and not key.startswith("PYTHON")
        and not key.startswith("LD_")
        and not key.startswith("DYLD_")
    }
    env["PATH"] = SAFE_CHILD_PATH
    return env


def editor_mode(target_arg: str) -> int:
    result_value = os.environ.get(RESULT_ENV)
    try:
        source_value = os.environ.get(SOURCE_ENV)
        source_sha = os.environ.get(SOURCE_SHA_ENV)
        if not source_value or not source_sha or not result_value:
            raise EditError("required editor state is missing")

        source = Path(source_value).resolve(strict=True)
        target = Path(target_arg)
        source_info = require_regular_file(source, "replacement YAML")
        if stat.S_IMODE(source_info.st_mode) & 0o077:
            raise EditError("replacement YAML must not be accessible by group or other users")
        if file_sha256(source) != source_sha:
            raise EditError("replacement YAML checksum does not match the reviewed checksum")

        replacement = source.read_bytes()
        if not replacement.strip():
            raise EditError("replacement YAML is empty")

        before = require_regular_file(target, "OBD temporary YAML")
        before_sha = file_sha256(target)
        expected_before = os.environ.get(BEFORE_SHA_ENV)
        if expected_before and before_sha != expected_before:
            raise EditError("OBD temporary YAML checksum does not match the expected pre-edit checksum")

        flags = os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(target, flags)
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                raise EditError("OBD temporary YAML changed before it could be edited")
            os.lseek(descriptor, 0, os.SEEK_SET)
            view = memoryview(replacement)
            written = 0
            while written < len(view):
                written += os.write(descriptor, view[written:])
            os.ftruncate(descriptor, len(replacement))
            os.fsync(descriptor)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)

        if (after.st_dev, after.st_ino) != (before.st_dev, before.st_ino):
            raise EditError("OBD temporary YAML inode changed during the edit")
        after_sha = file_sha256(target)
        if after_sha != source_sha:
            raise EditError("OBD temporary YAML does not match the reviewed replacement")

        write_result(
            Path(result_value),
            {
                "ok": True,
                "before_sha256": before_sha,
                "after_sha256": after_sha,
                "device": after.st_dev,
                "inode": after.st_ino,
            },
        )
        return 0
    except Exception as exc:  # Fail closed inside the editor subprocess.
        if result_value:
            try:
                write_result(Path(result_value), {"ok": False, "error": str(exc)})
            except Exception:
                pass
        print(f"obd-edit-config-pty: {exc}", file=sys.stderr)
        return 1


def terminate_child(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except OSError:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            return
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        waited, _ = os.waitpid(pid, os.WNOHANG)
        if waited == pid:
            return
        time.sleep(0.1)
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, OSError):
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def wait_status_to_code(status_value: int) -> int:
    if os.WIFEXITED(status_value):
        return os.WEXITSTATUS(status_value)
    if os.WIFSIGNALED(status_value):
        return 128 + os.WTERMSIG(status_value)
    return 1


def driver_mode(args: argparse.Namespace) -> int:
    if not DEPLOYMENT_RE.fullmatch(args.deployment):
        raise EditError("deployment name contains unsupported characters")

    replacement = Path(args.replacement).resolve(strict=True)
    replacement_info = require_regular_file(replacement, "replacement YAML")
    if stat.S_IMODE(replacement_info.st_mode) & 0o077:
        raise EditError("replacement YAML must have mode 0600 or stricter")
    actual_sha = file_sha256(replacement)
    if actual_sha != args.replacement_sha256:
        raise EditError("replacement YAML checksum does not match --replacement-sha256")

    obd, obd_identity = require_trusted_obd(args.obd, args.obd_sha256)

    transcript_handle = None
    if args.transcript:
        transcript_path = Path(args.transcript)
        transcript_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        transcript_handle = os.fdopen(
            os.open(transcript_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600),
            "wb",
        )

    run_dir = Path(tempfile.mkdtemp(prefix="obd-edit-config-pty-"))
    os.chmod(run_dir, 0o700)
    result_path = run_dir / "editor-result.json"
    editor_launcher = create_editor_launcher(run_dir)
    env = create_child_env()
    env.update(
        {
            "EDITOR": str(editor_launcher),
            EDITOR_MODE_ENV: "1",
            SOURCE_ENV: str(replacement),
            SOURCE_SHA_ENV: actual_sha,
            RESULT_ENV: str(result_path),
        }
    )
    if args.expected_before_sha256:
        env[BEFORE_SHA_ENV] = args.expected_before_sha256

    child_pid = -1
    master_fd = -1
    tail = b""
    deadline = time.monotonic() + args.timeout
    try:
        child_pid, master_fd = pty.fork()
        if child_pid == 0:
            _, current_identity = require_trusted_obd(args.obd, args.obd_sha256)
            if current_identity != obd_identity:
                raise EditError("OBD executable identity changed after validation")
            os.execve(obd, [obd, "cluster", "edit-config", args.deployment], env)

        while True:
            waited, status_value = os.waitpid(child_pid, os.WNOHANG)
            if waited == child_pid:
                exit_code = wait_status_to_code(status_value)
                break
            if time.monotonic() >= deadline:
                terminate_child(child_pid)
                raise EditError("edit-config timed out; the caller-owned OBD process was terminated")

            readable, _, _ = select.select([master_fd], [], [], 0.2)
            if not readable:
                continue
            try:
                chunk = os.read(master_fd, 65536)
            except OSError as exc:
                if exc.errno == errno.EIO:
                    continue
                raise
            if not chunk:
                continue
            if transcript_handle:
                transcript_handle.write(chunk)
                transcript_handle.flush()
            tail = (tail + ANSI_RE.sub(b"", chunk))[-16384:]
            if PROMPT_RE.search(tail):
                terminate_child(child_pid)
                raise EditError("OBD emitted an unexpected confirmation prompt; no answer was sent")

        if exit_code != 0:
            raise EditError(f"edit-config exited with status {exit_code}")
        if not result_path.exists():
            raise EditError("OBD exited without invoking the controlled editor")
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if not result.get("ok"):
            raise EditError(f"controlled editor failed: {result.get('error', 'unknown error')}")

        print(
            "edit-config completed: "
            f"deployment={args.deployment} "
            f"before_sha256={result['before_sha256']} "
            f"after_sha256={result['after_sha256']} "
            f"device={result['device']} inode={result['inode']}"
        )
        if args.transcript:
            print(f"protected_transcript={Path(args.transcript)}")
        return 0
    finally:
        if transcript_handle:
            transcript_handle.close()
        if master_fd >= 0:
            try:
                os.close(master_fd)
            except OSError:
                pass
        shutil.rmtree(run_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply a reviewed complete YAML through OBD edit-config using a real PTY and same-inode editor."
    )
    parser.add_argument("--deployment", required=True)
    parser.add_argument("--replacement", required=True)
    parser.add_argument("--replacement-sha256", required=True)
    parser.add_argument("--expected-before-sha256")
    parser.add_argument("--obd", required=True)
    parser.add_argument("--obd-sha256", required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--transcript")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    return args


def main() -> int:
    if os.environ.get(EDITOR_MODE_ENV) == "1":
        if len(sys.argv) != 2:
            print("obd-edit-config-pty: invalid editor invocation", file=sys.stderr)
            return 2
        return editor_mode(sys.argv[1])
    try:
        return driver_mode(parse_args())
    except EditError as exc:
        print(f"obd-edit-config-pty: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
