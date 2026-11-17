#!/usr/bin/env python3
"""Invoke ModelCLI with a validated Agent JSON envelope."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_TIMEOUT = 900.0
INSTALL_URL = "https://raw.githubusercontent.com/GraySilver/modelcli/main/install.sh"
WRAPPER_NAME = "modelcli-skill"


class InstallTimeoutError(Exception):
    """Raised when automatic installation consumes the wrapper deadline."""


def error_envelope(code: str, message: str, retryable: bool = False) -> Dict[str, Any]:
    return {
        "schema_version": "1",
        "ok": False,
        "operation": "modelcli.wrapper",
        "error": {"code": code, "message": message, "retryable": retryable},
        "meta": {"modelcli_version": "unknown", "elapsed_ms": 0, "wrapper": WRAPPER_NAME},
    }


def emit_error(code: str, message: str, exit_code: int, retryable: bool = False) -> int:
    sys.stdout.write(json.dumps(error_envelope(code, message, retryable=retryable), ensure_ascii=False, separators=(",", ":")))
    sys.stdout.write("\n")
    return exit_code


def operation_arguments(command: List[str]) -> List[str]:
    commands = {"detect", "ocr", "asr", "tts", "models", "capabilities", "doctor"}
    for index, argument in enumerate(command):
        if argument in commands:
            return command[index:]
    return command


def is_sensitive(command: List[str]) -> bool:
    if "--force" in command:
        return True
    arguments = operation_arguments(command)
    if arguments and arguments[0] == "doctor" and "--deep" in arguments[1:]:
        return True
    if arguments[:2] in (["models", "remove"], ["models", "clean"]):
        return True
    return arguments[:2] == ["models", "install"] and "--refresh" in arguments[2:]


def find_modelcli() -> Optional[str]:
    configured = os.environ.get("MODELCLI_BIN")
    if configured:
        path = Path(configured).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
        return None
    located = shutil.which("modelcli")
    if located:
        return located
    fallback = Path.home() / ".local" / "bin" / "modelcli"
    if fallback.is_file() and os.access(fallback, os.X_OK):
        return str(fallback)
    return None


def local_install_script() -> Optional[Path]:
    configured = os.environ.get("MODELCLI_INSTALL_SCRIPT")
    if configured:
        return Path(configured).expanduser()
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "install.sh"
        if (parent / "pyproject.toml").is_file() and candidate.is_file():
            return candidate
    return None


def remaining_seconds(deadline: float) -> float:
    return max(0.001, deadline - time.monotonic())


def install_modelcli(deadline: float) -> Tuple[Optional[str], Optional[str]]:
    if sys.platform not in {"darwin", "linux"}:
        return None, f"automatic ModelCLI installation is unsupported on {sys.platform}"
    script = local_install_script()
    temporary = None
    try:
        if os.environ.get("MODELCLI_INSTALL_SCRIPT") and (script is None or not script.is_file()):
            return None, "MODELCLI_INSTALL_SCRIPT does not point to a readable file"
        if script is None:
            temporary = tempfile.TemporaryDirectory(prefix="modelcli-skill-install-")
            script = Path(temporary.name) / "install.sh"
            downloader = shutil.which("curl")
            if downloader:
                download = subprocess.run(
                    [downloader, "-LsSf", INSTALL_URL, "-o", str(script)],
                    capture_output=True,
                    text=True,
                    timeout=remaining_seconds(deadline),
                    check=False,
                )
            else:
                wget = shutil.which("wget")
                if not wget:
                    return None, "curl or wget is required to install ModelCLI"
                download = subprocess.run(
                    [wget, "-qO", str(script), INSTALL_URL],
                    capture_output=True,
                    text=True,
                    timeout=remaining_seconds(deadline),
                    check=False,
                )
            if download.returncode != 0:
                return None, (download.stderr or download.stdout or "failed to download install.sh").strip()
        result = subprocess.run(
            ["sh", str(script)],
            capture_output=True,
            text=True,
            timeout=remaining_seconds(deadline),
            check=False,
        )
        if result.stdout:
            sys.stderr.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if result.returncode != 0:
            return None, (result.stderr or result.stdout or "install.sh failed").strip()
        installed = find_modelcli()
        if not installed:
            return None, "installation completed but modelcli was not found"
        return installed, None
    except subprocess.TimeoutExpired as exc:
        raise InstallTimeoutError from exc
    except OSError as exc:
        return None, str(exc)
    finally:
        if temporary is not None:
            temporary.cleanup()


def validate_envelope(stdout: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return None, f"ModelCLI stdout is not valid JSON: {exc.msg}"
    if not isinstance(payload, dict):
        return None, "ModelCLI stdout must be a JSON object"
    required = {"schema_version", "ok", "operation", "meta"}
    missing = sorted(required - payload.keys())
    if missing:
        return None, f"ModelCLI envelope is missing: {', '.join(missing)}"
    if payload["schema_version"] != "1" or not isinstance(payload["ok"], bool):
        return None, "ModelCLI envelope has an unsupported schema"
    if not isinstance(payload["operation"], str) or not payload["operation"]:
        return None, "ModelCLI envelope operation must be a non-empty string"
    if not isinstance(payload["meta"], dict):
        return None, "ModelCLI envelope meta must be an object"
    branch = "result" if payload["ok"] else "error"
    if branch not in payload:
        return None, f"ModelCLI envelope is missing: {branch}"
    if not payload["ok"] and not isinstance(payload["error"], dict):
        return None, "ModelCLI envelope error must be an object"
    return payload, None


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    value.add_argument("--approve-sensitive", action="store_true")
    value.add_argument("command", nargs=argparse.REMAINDER)
    return value


def main() -> int:
    args = parser().parse_args()
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        return emit_error("CLI_USAGE_ERROR", "A ModelCLI command is required", 2)
    if args.timeout <= 0:
        return emit_error("CLI_USAGE_ERROR", "--timeout must be greater than zero", 2)
    if is_sensitive(command) and not args.approve_sensitive:
        return emit_error(
            "CONFIRMATION_REQUIRED",
            "This operation can overwrite output, refresh models, remove data, or deeply load models; obtain explicit user confirmation and pass --approve-sensitive",
            2,
        )

    deadline = time.monotonic() + args.timeout
    configured = os.environ.get("MODELCLI_BIN")
    executable = find_modelcli()
    if configured and executable is None:
        return emit_error("MODELCLI_NOT_FOUND", f"MODELCLI_BIN is not executable: {configured}", 4)
    if executable is None:
        try:
            executable, install_error = install_modelcli(deadline)
        except InstallTimeoutError:
            return emit_error("TIMEOUT", f"ModelCLI installation exceeded {args.timeout:g} seconds", 124, retryable=True)
        if executable is None:
            return emit_error("MODELCLI_INSTALL_FAILED", install_error or "ModelCLI installation failed", 4, retryable=True)

    try:
        completed = subprocess.run(
            [executable, "--json", "--allow-download", *command],
            capture_output=True,
            text=True,
            timeout=remaining_seconds(deadline),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        if exc.stderr:
            sys.stderr.write(exc.stderr.decode() if isinstance(exc.stderr, bytes) else exc.stderr)
        return emit_error("TIMEOUT", f"ModelCLI exceeded {args.timeout:g} seconds", 124, retryable=True)
    except KeyboardInterrupt:
        return emit_error("INTERRUPTED", "Operation interrupted", 130, retryable=True)
    except OSError as exc:
        return emit_error("MODELCLI_EXEC_FAILED", str(exc), 5, retryable=True)

    if completed.stderr:
        sys.stderr.write(completed.stderr)
    payload, protocol_error = validate_envelope(completed.stdout)
    if protocol_error:
        if completed.stdout:
            sys.stderr.write(f"ModelCLI stdout: {completed.stdout}\n")
        return emit_error("PROTOCOL_ERROR", protocol_error, 5)
    sys.stdout.write(completed.stdout)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
