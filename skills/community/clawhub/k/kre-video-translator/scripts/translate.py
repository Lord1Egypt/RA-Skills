"""Call the production Kre Video Translator API from an agent skill."""

from __future__ import annotations

import argparse
from contextlib import ExitStack
from email.utils import parsedate_to_datetime
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import credentials
from errors import CredentialRequiredError, ParamError, ScriptError, ToolInstallRequiredError

try:
    import requests
except ModuleNotFoundError:
    requests = None  # type: ignore[assignment]


DEFAULT_BASE_URL = "https://kretrans.com/api"
PRODUCTION_HOST = "kretrans.com"
BASE_URL_ENV_NAME = "KRE_VIDEO_TRANSLATOR_BASE_URL"
FFMPEG_ENV_NAME = "KRE_VIDEO_TRANSLATOR_FFMPEG"
DEFAULT_REQUEST_ATTEMPTS = 3
DEFAULT_POLL_INTERVAL_SECONDS = 20.0
MIN_POLL_INTERVAL_SECONDS = 20.0
MAX_POLL_INTERVAL_SECONDS = 120.0
DEFAULT_MAX_WAIT_SECONDS = 21600.0
SUPPORTED_MEDIA_EXTENSIONS = frozenset(
    ".mp3 .wav .ogg .m4a .aac .flac .wma .opus .mp4 .mov .avi .mkv .webm .mpeg .mpg .wmv .m4v".split()
)
VIDEO_EXTENSIONS = frozenset(".mp4 .mov .avi .mkv .webm .mpeg .mpg .wmv .m4v".split())
MAX_SOURCE_REFERENCE_BYTES = 1 * 1024 * 1024
SCHEMA_VERSION = 1
BALANCE_ERROR_CODES = frozenset(
    {
        "insufficient_quota",
        "insufficient_balance",
        "quota_exceeded",
        "insufficient_entitlement",
        "no_available_minutes",
    }
)
SERVICE_UNAVAILABLE_ERROR_CODES = frozenset(
    {
        "runtime_unavailable",
        "service_unavailable",
        "api_unavailable",
        "upstream_unavailable",
        "health_check_failed",
    }
)


class PollTimeoutError(ScriptError):
    """The durable task is still active after the local wait limit."""


class ApiError(ScriptError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = 0,
        request_id: str = "",
        retryable: bool = False,
        retry_after: float = 0.0,
        error_code: str = "request_failed",
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        self.retryable = retryable
        self.retry_after = retry_after
        self.error_code = error_code


class DocsArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\nSee docs: https://kretrans.com/api\n")


def _configure_stdio_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _pip_install(package: str, *, allow_install: bool) -> None:
    if not allow_install:
        raise ToolInstallRequiredError(
            f"Python package {package} is required. Ask the user before installing it.",
            tool=package,
            install_command=f'"{sys.executable}" -m pip install {package}',
        )
    print(f"Installing missing Python package: {package}", file=sys.stderr)
    completed = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()[-800:]
        raise ParamError(f"Unable to install {package}: {detail}")


def _require_requests(*, allow_install: bool = False) -> Any:
    global requests
    if requests is None:
        _pip_install("requests", allow_install=allow_install)
        requests = importlib.import_module("requests")
    return requests


def _normalize_base_url(raw: str) -> str:
    value = str(raw or "").strip()
    if not value:
        raise ParamError("API base URL cannot be empty.")
    if not re.match(r"^https?://", value, flags=re.IGNORECASE):
        value = f"https://{value}"
    parsed = urlsplit(value)
    if parsed.scheme.lower() != "https" or parsed.hostname != PRODUCTION_HOST:
        raise ParamError(f"Only the production API host https://{PRODUCTION_HOST} is allowed.")
    path = parsed.path.rstrip("/")
    if not path:
        path = "/api"
    elif not path.endswith("/api"):
        path = f"{path}/api"
    return urlunsplit(("https", PRODUCTION_HOST, path, "", ""))


def _safe_json_response(response: Any, action: str) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        preview = str(getattr(response, "text", "") or "").strip()[:800]
        raise ApiError(
            f"{action} failed: response is not valid JSON: {preview}",
            status_code=int(getattr(response, "status_code", 0) or 0),
            retryable=int(getattr(response, "status_code", 0) or 0) == 429
            or int(getattr(response, "status_code", 0) or 0) >= 500,
            retry_after=_retry_after(response),
            error_code="invalid_response",
        ) from exc
    if not isinstance(payload, dict):
        raise ApiError(
            f"{action} failed: response JSON has an unexpected format",
            status_code=int(getattr(response, "status_code", 0) or 0),
        )
    return payload


def _retry_after(response: Any) -> float:
    value = str(getattr(response, "headers", {}).get("Retry-After", "0") or "0")
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            return max(0.0, parsedate_to_datetime(value).timestamp() - time.time())
        except (TypeError, ValueError, OverflowError):
            return 0.0


def _raise_api_error(response: Any, payload: dict[str, Any], action: str) -> None:
    error = payload.get("error") if isinstance(payload.get("error"), dict) else {}
    code = str(error.get("code") or payload.get("code") or "request_failed")
    message = str(error.get("message") or payload.get("message") or action)
    request_id = str(payload.get("request_id") or "")
    status_code = int(getattr(response, "status_code", 0) or 0)
    retryable = bool(error.get("retryable")) or status_code == 429 or status_code >= 500
    raise ApiError(
        f"{action} failed: {message} (code={code})",
        status_code=status_code,
        request_id=request_id,
        retryable=retryable,
        retry_after=_retry_after(response),
        error_code=code,
    )


def _rewind_files(kwargs: dict[str, Any]) -> None:
    files = kwargs.get("files")
    if not isinstance(files, dict):
        return
    for value in files.values():
        candidate = value[1] if isinstance(value, tuple) and len(value) >= 2 else value
        seek = getattr(candidate, "seek", None)
        if callable(seek):
            seek(0)


def _request_json(
    session: Any,
    method: str,
    url: str,
    *,
    action: str,
    timeout_seconds: float,
    attempts: int = DEFAULT_REQUEST_ATTEMPTS,
    **kwargs: Any,
) -> dict[str, Any]:
    request_lib = _require_requests()
    total_attempts = max(1, int(attempts))
    last_error: Exception | None = None
    for attempt in range(1, total_attempts + 1):
        try:
            _rewind_files(kwargs)
            response = session.request(method, url, timeout=timeout_seconds, **kwargs)
        except request_lib.RequestException as exc:
            last_error = exc
            if attempt >= total_attempts:
                break
            time.sleep(min(2 ** (attempt - 1), 8))
            continue
        try:
            payload = _safe_json_response(response, action)
        except ApiError as error:
            if error.retryable and attempt < total_attempts:
                time.sleep(error.retry_after or min(2 ** (attempt - 1), 8))
                continue
            raise
        status_code = int(getattr(response, "status_code", 0) or 0)
        if status_code < 400:
            return payload
        error = payload.get("error") if isinstance(payload.get("error"), dict) else {}
        retryable = bool(error.get("retryable")) or status_code >= 500
        if retryable and status_code != 429 and attempt < total_attempts:
            time.sleep(min(2 ** (attempt - 1), 8))
            continue
        _raise_api_error(response, payload, action)
    raise ApiError(
        f"{action} failed after {total_attempts} attempts: {last_error}",
        retryable=True,
        error_code="service_unavailable",
    )


def _authorization_headers(api_key: str, idempotency_key: str = "") -> dict[str, str]:
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    return headers


def _normalize_languages(values: list[str]) -> list[str]:
    result: list[str] = []
    for raw in values:
        for part in str(raw or "").replace("|", ",").split(","):
            code = part.strip().lower()
            if code and code not in result:
                result.append(code)
    return result


def _to_milliseconds(value: Any) -> int:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0
    return max(0, int(round(number))) if number == number else 0


def _format_srt_time(milliseconds: int) -> str:
    total_ms = _to_milliseconds(milliseconds)
    total_seconds, ms = divmod(total_ms, 1000)
    hour, remainder = divmod(total_seconds, 3600)
    minute, second = divmod(remainder, 60)
    return f"{hour:02d}:{minute:02d}:{second:02d},{ms:03d}"


def _subtitle_text(
    item: dict[str, Any], target_language: str, *, allow_source_fallback: bool
) -> str:
    field = f"{target_language}_translate"
    value = item.get(field)
    if field in item and value is not None:
        return str(value)
    if allow_source_fallback:
        return str(item.get("text") or "")
    raise ScriptError(f"Translation field {field!r} is missing; refusing to export source text")


def _build_srt_text(
    cc_list: list[dict[str, Any]],
    target_language: str,
    *,
    allow_source_fallback: bool = False,
) -> str:
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(cc_list):
        start = _to_milliseconds(raw.get("start"))
        end = max(start, _to_milliseconds(raw.get("end")))
        try:
            text = _subtitle_text(raw, target_language, allow_source_fallback=allow_source_fallback)
        except ScriptError as exc:
            raise ScriptError(f"Subtitle item {index + 1}: {exc}") from exc
        normalized.append({"start": start, "end": end, "text": text, "order": index})
    normalized.sort(key=lambda item: (item["start"], item["end"], item["order"]))
    lines: list[str] = []
    for index, item in enumerate(normalized, start=1):
        lines.extend(
            [
                str(index),
                f"{_format_srt_time(item['start'])} --> {_format_srt_time(item['end'])}",
                str(item["text"]),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _infer_target_languages(cc_list: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for item in cc_list:
        for field in item:
            if field.endswith("_translate"):
                code = field[: -len("_translate")].strip().lower()
                if code and code not in result:
                    result.append(code)
    return result


def _resolve_output_paths(
    *,
    input_path: Path | None,
    output_arg: str,
    target_languages: list[str],
    task_id: str,
) -> dict[str, Path]:
    if not target_languages:
        raise ParamError("No target language is available for export.")
    base_stem = input_path.stem if input_path else task_id or "translation-task"
    raw = str(output_arg or "").strip()
    multi = len(target_languages) > 1
    if not raw:
        parent = input_path.parent if input_path else Path.cwd()
        return {
            language: parent / (f"{base_stem}.{language}.srt" if multi else f"{base_stem}.srt")
            for language in target_languages
        }
    target = Path(raw).expanduser()
    directory = raw.endswith(("/", "\\")) or (target.exists() and target.is_dir())
    if directory:
        return {
            language: target / (f"{base_stem}.{language}.srt" if multi else f"{base_stem}.srt")
            for language in target_languages
        }
    if target.suffix.lower() != ".srt":
        target = target.with_suffix(".srt")
    if not multi:
        return {target_languages[0]: target}
    return {language: target.with_name(f"{target.stem}.{language}.srt") for language in target_languages}


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    _write_atomic(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _validate_source_reference(path: Path) -> None:
    if not path.is_file():
        raise ParamError(f"Source reference file does not exist: {path}")
    if path.suffix.lower() not in {".srt", ".txt"}:
        raise ParamError("Source reference must use the .srt or .txt extension.")
    size = path.stat().st_size
    if size <= 0:
        raise ParamError("Source reference file is empty.")
    if size > MAX_SOURCE_REFERENCE_BYTES:
        raise ParamError("Source reference must not exceed 1 MiB.")


_validate_source_subtitle = _validate_source_reference


def _task_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    task = payload.get("task")
    if not isinstance(task, dict):
        raise ScriptError("The API response did not contain a task object.")
    return task


def _task_id(task: dict[str, Any]) -> str:
    value = str(task.get("task_id") or task.get("legacy_project_id") or "").strip()
    if not value:
        raise ScriptError("The task response did not contain a reusable task ID.")
    return value


def _task_state(task: dict[str, Any]) -> str:
    status = str(task.get("status") or "").strip().lower()
    try:
        numeric = int(task.get("task_status") or 0)
    except (TypeError, ValueError):
        numeric = 0
    if numeric == 3 or status in {"success", "completed"}:
        return "completed"
    if numeric == 4 or status in {"failed", "canceled", "cancelled"}:
        return "failed"
    return "active"


def _task_progress(task: dict[str, Any]) -> dict[str, Any]:
    try:
        progress = int(task.get("progress") or task.get("process") or 0)
    except (TypeError, ValueError):
        progress = 0
    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": _task_id(task),
        "status": str(task.get("status") or "active"),
        "stage": str(task.get("stage") or ""),
        "progress": max(0, min(100, progress)),
    }


def _fetch_task(
    session: Any, base_url: str, api_key: str, task_id: str, timeout_seconds: float
) -> tuple[dict[str, Any], str]:
    payload = _request_json(
        session,
        "GET",
        f"{base_url}/external/tasks/{task_id}",
        action="Read translation task",
        timeout_seconds=timeout_seconds,
        attempts=1,
        headers=_authorization_headers(api_key),
    )
    return _task_from_payload(payload), str(payload.get("request_id") or "")


def _poll_task(
    session: Any,
    *,
    base_url: str,
    api_key: str,
    task_id: str,
    poll_interval: float,
    max_wait: float,
    timeout_seconds: float,
) -> tuple[dict[str, Any], str]:
    deadline = time.monotonic() + max_wait
    interval = min(MAX_POLL_INTERVAL_SECONDS, max(MIN_POLL_INTERVAL_SECONDS, float(poll_interval)))
    last_signature: tuple[Any, ...] | None = None
    last_request_id = ""
    while time.monotonic() < deadline:
        try:
            task, last_request_id = _fetch_task(session, base_url, api_key, task_id, timeout_seconds)
        except ApiError as error:
            if error.status_code != 429 and not error.retryable:
                raise
            if time.monotonic() >= deadline:
                raise PollTimeoutError(
                    f"Task {task_id} could not be queried before the wait limit; resume with --task-id {task_id}"
                ) from error
            wait_seconds = max(interval, error.retry_after)
            wait_status = "rate_limited" if error.status_code == 429 else "retrying"
            print(
                f"KRE_VIDEO_TRANSLATOR_PROGRESS_JSON={json.dumps({'schema_version': SCHEMA_VERSION, 'task_id': task_id, 'status': wait_status, 'retry_after_seconds': wait_seconds}, ensure_ascii=False)}",
                file=sys.stderr,
            )
            time.sleep(min(wait_seconds, max(0.0, deadline - time.monotonic())))
            interval = min(MAX_POLL_INTERVAL_SECONDS, max(interval, wait_seconds) * 1.5)
            continue
        progress = _task_progress(task)
        signature = (progress["status"], progress["stage"], progress["progress"])
        if signature != last_signature:
            print(
                f"KRE_VIDEO_TRANSLATOR_PROGRESS_JSON={json.dumps(progress, ensure_ascii=False)}",
                file=sys.stderr,
            )
            last_signature = signature
        state = _task_state(task)
        if state == "completed":
            return task, last_request_id
        if state == "failed":
            failure = task.get("error") if isinstance(task.get("error"), dict) else {}
            error_code = str(
                task.get("error_code")
                or failure.get("code")
                or task.get("code")
                or "task_failed"
            )
            error_message = str(
                task.get("error_message")
                or failure.get("message")
                or task.get("message")
                or f"Task {task_id} ended with status {task.get('status') or task.get('task_status')}"
            )
            raise ApiError(
                f"Task {task_id} failed: {error_message} (code={error_code})",
                request_id=last_request_id,
                error_code=error_code,
            )
        if time.monotonic() >= deadline:
            raise PollTimeoutError(
                f"Task {task_id} is still active after {max_wait:g} seconds; resume with --task-id {task_id}"
            )
        time.sleep(min(interval, max(0.0, deadline - time.monotonic())))
        interval = min(MAX_POLL_INTERVAL_SECONDS, interval * 1.25)
    raise PollTimeoutError(f"Task {task_id} reached the wait limit; resume with --task-id {task_id}")


def _print_models(session: Any, base_url: str, timeout_seconds: float) -> None:
    payload = _request_json(
        session,
        "GET",
        f"{base_url}/public/translation-catalog",
        action="Read translation catalog",
        timeout_seconds=timeout_seconds,
    )
    print(json.dumps(payload, ensure_ascii=False))


def _find_ffmpeg() -> str:
    configured = str(os.getenv(FFMPEG_ENV_NAME, "") or "").strip()
    candidate = configured or shutil.which("ffmpeg")
    if candidate and (Path(candidate).is_file() or shutil.which(candidate)):
        return candidate
    return ""


def _ffmpeg_install_command() -> str:
    if sys.platform == "darwin" and shutil.which("brew"):
        return "brew install ffmpeg"
    if sys.platform.startswith("linux"):
        if shutil.which("apt-get"):
            prefix = "" if os.geteuid() == 0 else "sudo "
            return f"{prefix}apt-get update && {prefix}apt-get install -y ffmpeg"
        if shutil.which("dnf"):
            prefix = "" if os.geteuid() == 0 else "sudo "
            return f"{prefix}dnf install -y ffmpeg"
    if os.name == "nt":
        if shutil.which("winget"):
            return "winget install --id Gyan.FFmpeg.Shared -e"
        if shutil.which("choco"):
            return "choco install ffmpeg -y"
    return "Install FFmpeg with your operating system's package manager."


def _subtitle_ffmpeg_install_command() -> str:
    if sys.platform == "darwin" and shutil.which("brew"):
        return "brew install ffmpeg-full"
    return _ffmpeg_install_command()


def _install_ffmpeg() -> str:
    commands: list[list[str]] = []
    if sys.platform == "darwin" and shutil.which("brew"):
        commands.append(["brew", "install", "ffmpeg"])
    elif sys.platform.startswith("linux"):
        if shutil.which("apt-get"):
            prefix = [] if os.geteuid() == 0 else (["sudo"] if shutil.which("sudo") else [])
            commands.append([*prefix, "apt-get", "update"])
            commands.append([*prefix, "apt-get", "install", "-y", "ffmpeg"])
        elif shutil.which("dnf"):
            prefix = [] if os.geteuid() == 0 else (["sudo"] if shutil.which("sudo") else [])
            commands.append([*prefix, "dnf", "install", "-y", "ffmpeg"])
    elif os.name == "nt":
        if shutil.which("winget"):
            commands.append(["winget", "install", "--id", "Gyan.FFmpeg.Shared", "-e", "--accept-source-agreements", "--accept-package-agreements"])
        elif shutil.which("choco"):
            commands.append(["choco", "install", "ffmpeg", "-y"])
    if not commands:
        raise ParamError("FFmpeg is required but no supported package manager was found. Install FFmpeg and retry.")
    for command in commands:
        print(f"Installing FFmpeg with {command[0]}", file=sys.stderr)
        completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "").strip()[-800:]
            raise ParamError(f"Unable to install FFmpeg: {detail}")
    ffmpeg = _find_ffmpeg()
    if not ffmpeg:
        raise ParamError("FFmpeg installation finished but the executable is not available on PATH.")
    return ffmpeg


def _ensure_ffmpeg(*, allow_install: bool) -> str:
    ffmpeg = _find_ffmpeg()
    if ffmpeg:
        return ffmpeg
    if not allow_install:
        raise ToolInstallRequiredError(
            "FFmpeg is required for media preparation and video export. Ask the user before installing it.",
            tool="ffmpeg",
            install_command=_ffmpeg_install_command(),
        )
    return _install_ffmpeg()


def _ffmpeg_has_filter(ffmpeg: str, filter_name: str) -> bool:
    try:
        completed = subprocess.run(
            [ffmpeg, "-hide_banner", "-filters"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError:
        return False
    output = f"{completed.stdout}\n{completed.stderr}"
    return any(
        re.search(rf"^\s*\S{{2}}\s+{re.escape(filter_name)}\s+", line)
        for line in output.splitlines()
    )


def _ensure_subtitle_ffmpeg(*, allow_install: bool, locale: str = "") -> str:
    ffmpeg = _ensure_ffmpeg(allow_install=allow_install)
    if _ffmpeg_has_filter(ffmpeg, "subtitles"):
        return ffmpeg

    if sys.platform == "darwin" and shutil.which("brew"):
        prefix = subprocess.run(
            ["brew", "--prefix", "ffmpeg-full"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        full_ffmpeg = Path(prefix) / "bin" / "ffmpeg" if prefix else Path()
        if not full_ffmpeg.is_file() and allow_install:
            installed = subprocess.run(
                ["brew", "install", "ffmpeg-full"],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if installed.returncode == 0:
                prefix = subprocess.run(
                    ["brew", "--prefix", "ffmpeg-full"],
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                ).stdout.strip()
                full_ffmpeg = Path(prefix) / "bin" / "ffmpeg" if prefix else Path()
        if full_ffmpeg.is_file() and _ffmpeg_has_filter(str(full_ffmpeg), "subtitles"):
            return str(full_ffmpeg)

        if not allow_install:
            raise ToolInstallRequiredError(
                "FFmpeg needs the subtitles/libass filter for video export. Ask the user before installing ffmpeg-full.",
                tool="ffmpeg-full",
                install_command="brew install ffmpeg-full",
            )
    if allow_install:
        installed_ffmpeg = _install_ffmpeg()
        if _ffmpeg_has_filter(installed_ffmpeg, "subtitles"):
            return installed_ffmpeg
    else:
        raise ToolInstallRequiredError(
            "FFmpeg needs the subtitles/libass filter for video export. Ask the user before installing a compatible FFmpeg build.",
            tool="ffmpeg-libass",
            install_command=_subtitle_ffmpeg_install_command(),
        )

    if locale == "zh":
        raise ParamError(
            "当前 FFmpeg 未启用 subtitles/libass 滤镜。请安装启用 libass 的 FFmpeg 后重试视频导出；"
            "字幕文件已经可以直接导出。"
        )
    raise ParamError(
        "The installed FFmpeg does not include the subtitles/libass filter. "
        "Install an FFmpeg build with libass enabled and retry video export; "
        "subtitle-file export is still available."
    )


def _run_process(
    command: list[str],
    action: str,
    *,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(cwd) if cwd else None,
        )
    except OSError as exc:
        raise ParamError(f"{action} could not start: {exc}") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()[-1200:]
        raise ScriptError(f"{action} failed: {detail}")
    return completed


def _ensure_yt_dlp(*, allow_install: bool) -> None:
    try:
        importlib.import_module("yt_dlp")
    except ModuleNotFoundError:
        _pip_install("yt-dlp", allow_install=allow_install)


def _source_cache_dir() -> Path:
    cache_home = os.getenv("XDG_CACHE_HOME", "").strip() or str(Path.home() / ".cache")
    path = Path(cache_home) / "kre-video-translator" / "sources"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _download_filename_stem(title: str, fallback: str = "media") -> str:
    value = re.sub(r"[\\/:*?\"<>|\x00-\x1f]+", " ", str(title or ""))
    value = re.sub(r"\s+", " ", value).strip(" .")
    return (value or fallback)[:120].rstrip(" .") or fallback


def _download_url(url: str, *, allow_install: bool = False) -> Path:
    _ensure_yt_dlp(allow_install=allow_install)
    cache_dir = _source_cache_dir()
    download_dir = cache_dir / uuid.uuid4().hex
    download_dir.mkdir(parents=True, exist_ok=True)
    inspect = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--no-playlist", "--dump-single-json", "--skip-download", url],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if inspect.returncode != 0:
        detail = (inspect.stderr or inspect.stdout or "").strip()[-1000:]
        raise ScriptError(f"URL analysis failed: {detail}")
    try:
        metadata = json.loads(inspect.stdout.splitlines()[-1])
    except (IndexError, json.JSONDecodeError) as exc:
        raise ScriptError("URL analysis did not return valid metadata.") from exc
    title = str(metadata.get("title") or "").strip()
    duration = metadata.get("duration")
    print(f"URL source: {title or url} ({duration or '?'}s)", file=sys.stderr)
    target = download_dir / f"{_download_filename_stem(title)}.%(ext)s"
    downloaded = _run_process(
        [
            sys.executable,
            "-m",
            "yt_dlp",
            "--no-playlist",
            "--no-warnings",
            "-f",
            "bv*+ba/b",
            "--merge-output-format",
            "mp4",
            "--print",
            "after_move:filepath",
            "-o",
            str(target),
            url,
        ],
        "URL download",
    )
    reported = [
        Path(line.strip()).expanduser()
        for line in downloaded.stdout.splitlines()
        if line.strip() and Path(line.strip()).expanduser().is_file()
    ]
    if reported:
        return reported[-1].resolve()
    matches = sorted(path for path in target.parent.glob(target.name.replace("%(ext)s", "*")) if path.is_file())
    if not matches:
        raise ScriptError("URL download completed without a media file.")
    return matches[-1].resolve()


def _resolve_input(raw: str, *, allow_install: bool = False) -> tuple[Path, str | None]:
    value = str(raw or "").strip()
    parsed = urlsplit(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        path = _download_url(value, allow_install=allow_install)
        return path, value
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ParamError(f"Media file does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_MEDIA_EXTENSIONS:
        raise ParamError(f"Unsupported media format: {path.suffix or '(none)'}")
    if path.stat().st_size <= 0:
        raise ParamError("Media file is empty.")
    return path, None


def _prepare_audio(input_path: Path, ffmpeg: str) -> Path:
    handle = tempfile.NamedTemporaryFile(prefix="kre-translator-", suffix=".mp3", delete=False)
    output = Path(handle.name)
    handle.close()
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(input_path),
        "-map",
        "0:a:0",
        "-vn",
        "-sn",
        "-dn",
        "-b:a",
        "64k",
        "-acodec",
        "mp3",
        "-ar",
        "44100",
        "-ac",
        "1",
        str(output),
    ]
    try:
        _run_process(command, "FFmpeg audio preparation")
    except Exception:
        output.unlink(missing_ok=True)
        raise
    return output


def _task_result(task: dict[str, Any]) -> dict[str, Any]:
    result = task.get("result")
    if not isinstance(result, dict):
        raise ScriptError("Task succeeded but returned no subtitle JSON.")
    raw_cc_list = result.get("cc_list")
    if not isinstance(raw_cc_list, list) or not any(isinstance(item, dict) for item in raw_cc_list):
        raise ScriptError("Task succeeded but returned no subtitle segments.")
    return result


def _result_wrapper(
    *,
    task: dict[str, Any],
    input_file: Path | None,
    source_url: str | None,
    idempotency_key: str,
    request_id: str,
) -> dict[str, Any]:
    result = _task_result(task)
    cc_list = [item for item in result.get("cc_list", []) if isinstance(item, dict)]
    targets = _infer_target_languages(cc_list)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "completed",
        "task_id": _task_id(task),
        "project_id": task.get("legacy_project_id"),
        "request_id": request_id or None,
        "idempotency_key": idempotency_key or None,
        "source_file": str(input_file) if input_file else None,
        "source_url": source_url,
        "target_languages": targets,
        "subtitle_count": len(cc_list),
        "result": result,
    }


def _write_state(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    if str(args.state_file or "").strip():
        _write_json_atomic(Path(args.state_file).expanduser(), payload)


def _build_upload_parser(parser: argparse.ArgumentParser, *, include_confirm: bool = True) -> None:
    parser.add_argument("input_file", nargs="?")
    parser.add_argument(
        "--locale",
        choices=credentials.SUPPORTED_LOCALES,
        default="",
        help="User-facing site language: zh for Chinese, en for other languages.",
    )
    parser.add_argument("--task-id", default="")
    parser.add_argument("--source-language", default="auto")
    parser.add_argument("--source-subtitle", default="")
    parser.add_argument("--target-language", action="append", default=[])
    parser.add_argument("--translation-model", default="")
    parser.add_argument("--custom-prompt", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--idempotency-key", default="")
    parser.add_argument("--state-file", default="")
    parser.add_argument("--result-json", default="")
    parser.add_argument("--base-url", default=os.getenv(BASE_URL_ENV_NAME, DEFAULT_BASE_URL))
    parser.add_argument("--request-timeout", type=float, default=30.0)
    parser.add_argument("--upload-timeout", type=float, default=600.0)
    parser.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL_SECONDS)
    parser.add_argument("--max-wait", type=float, default=DEFAULT_MAX_WAIT_SECONDS)
    parser.add_argument(
        "--allow-install-tools",
        action="store_true",
        help="Install missing local tools after the user has approved the installation.",
    )
    parser.add_argument("--no-install-tools", action="store_true", help=argparse.SUPPRESS)
    if include_confirm:
        parser.add_argument("--confirm-upload", action="store_true")


def _build_parser() -> argparse.ArgumentParser:
    parser = DocsArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    preflight = commands.add_parser("preflight", help="Validate credentials, tools, and upload parameters")
    _build_upload_parser(preflight, include_confirm=False)

    submit = commands.add_parser("submit", help="Prepare media and submit an asynchronous task")
    _build_upload_parser(submit)

    run = commands.add_parser("run", help="Submit and wait for an asynchronous task")
    _build_upload_parser(run)
    run.add_argument("--check", action="store_true")
    run.add_argument("--list-models", action="store_true")
    run.add_argument("--export-format", choices=("none", "srt", "video", "json"), default="none")
    run.add_argument("--output", default="")
    run.add_argument("--language", default="")
    run.add_argument("--allow-source-fallback", action="store_true")

    resume = commands.add_parser("resume", help="Wait for an existing asynchronous task")
    _build_upload_parser(resume, include_confirm=False)
    resume.add_argument("--export-format", choices=("none", "srt", "video", "json"), default="none")
    resume.add_argument("--output", default="")
    resume.add_argument("--language", default="")
    resume.add_argument("--allow-source-fallback", action="store_true")

    status = commands.add_parser("status", help="Read one task status without polling repeatedly")
    status.add_argument("--task-id", required=True)
    status.add_argument("--locale", choices=credentials.SUPPORTED_LOCALES, default="")
    status.add_argument("--base-url", default=os.getenv(BASE_URL_ENV_NAME, DEFAULT_BASE_URL))
    status.add_argument("--request-timeout", type=float, default=30.0)
    status.add_argument("--allow-install-tools", action="store_true")

    export = commands.add_parser("export", help="Export saved subtitle JSON as JSON, SRT, or video")
    export.add_argument("input_file", nargs="?")
    export.add_argument("--task-id", default="")
    export.add_argument("--locale", choices=credentials.SUPPORTED_LOCALES, default="")
    export.add_argument("--result-json", default="")
    export.add_argument("--base-url", default=os.getenv(BASE_URL_ENV_NAME, DEFAULT_BASE_URL))
    export.add_argument("--request-timeout", type=float, default=30.0)
    export.add_argument("--format", choices=("json", "srt", "video"), default="srt")
    export.add_argument("--output", default="")
    export.add_argument("--language", default="")
    export.add_argument("--allow-source-fallback", action="store_true")
    export.add_argument("--allow-install-tools", action="store_true")
    export.add_argument("--no-install-tools", action="store_true", help=argparse.SUPPRESS)

    return parser


def _normalize_cli_args(argv: list[str] | None) -> list[str]:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args:
        return ["run", "--help"]
    if args[0] in {"--help", "-h"}:
        return args
    commands = {"preflight", "submit", "run", "resume", "status", "export"}
    if args[0] not in commands:
        return ["run", *args]
    return args


def _preflight(args: argparse.Namespace) -> int:
    base_url = _normalize_base_url(args.base_url)
    api_key = credentials.require_key(args.locale)
    source_path = None
    source_url = None
    if args.input_file:
        _require_requests(allow_install=args.allow_install_tools)
        _ensure_ffmpeg(allow_install=args.allow_install_tools)
        source_path, source_url = _resolve_input(args.input_file, allow_install=args.allow_install_tools)
        if args.source_subtitle:
            _validate_source_reference(Path(args.source_subtitle).expanduser().resolve())
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "ready",
        "base_url": base_url,
        "api_key_configured": bool(api_key),
        "source_file": str(source_path) if source_path else None,
        "source_url": source_url,
        "source_language": args.source_language,
        "target_languages": _normalize_languages(args.target_language),
        "required_scopes": ["account:read", "task:write", "task:read"],
    }
    print(f"KRE_VIDEO_TRANSLATOR_PREFLIGHT_JSON={json.dumps(payload, ensure_ascii=False)}")
    return 0


def _submit(args: argparse.Namespace) -> tuple[dict[str, Any], Path, str | None]:
    if not args.input_file:
        raise ParamError("Provide one local media file or URL.")
    if not args.confirm_upload:
        raise ParamError("Remote upload was not confirmed; pass --confirm-upload after user confirmation.")
    target_languages = _normalize_languages(args.target_language)
    if not target_languages:
        raise ParamError("Provide at least one --target-language.")
    if args.source_subtitle:
        source_subtitle_path = Path(args.source_subtitle).expanduser().resolve()
        _validate_source_reference(source_subtitle_path)
    else:
        source_subtitle_path = None
    credentials.require_key(args.locale)
    base_url = _normalize_base_url(args.base_url)
    ffmpeg = _ensure_ffmpeg(allow_install=args.allow_install_tools)
    source_path, source_url = _resolve_input(args.input_file, allow_install=args.allow_install_tools)
    prepared_audio = _prepare_audio(source_path, ffmpeg)
    idempotency_key = str(args.idempotency_key or "").strip() or f"agent-{uuid.uuid4()}"
    try:
        request_lib = _require_requests(allow_install=args.allow_install_tools)
        with request_lib.Session() as session, ExitStack() as stack:
            media_handle = stack.enter_context(prepared_audio.open("rb"))
            files: dict[str, Any] = {"media": (f"{source_path.stem}.mp3", media_handle)}
            if source_subtitle_path is not None:
                subtitle_handle = stack.enter_context(source_subtitle_path.open("rb"))
                files["source_subtitle"] = (source_subtitle_path.name, subtitle_handle)
            payload = _request_json(
                session,
                "POST",
                f"{base_url}/external/tasks/upload",
                action="Upload prepared media and create translation task",
                timeout_seconds=max(0.1, float(args.upload_timeout)),
                headers=_authorization_headers(credentials.require_key(args.locale), idempotency_key),
                data={
                    "title": str(args.title or source_path.name),
                    "source_language": str(args.source_language or "auto"),
                    "target_languages": ",".join(target_languages),
                    "translation_model": str(args.translation_model or ""),
                    "custom_prompt": str(args.custom_prompt or ""),
                    "original_filename": source_path.name,
                    "source_is_video": str(source_path.suffix.lower() in VIDEO_EXTENSIONS).lower(),
                },
                files=files,
            )
    finally:
        prepared_audio.unlink(missing_ok=True)
    task = _task_from_payload(payload)
    task_id = _task_id(task)
    result = {
        "schema_version": SCHEMA_VERSION,
        "status": str(task.get("status") or "queued"),
        "stage": "submitted",
        "task_id": task_id,
        "request_id": str(payload.get("request_id") or "") or None,
        "idempotency_key": idempotency_key,
        "idempotent_replay": bool(payload.get("idempotent_replay")),
        "source_file": str(source_path),
        "source_url": source_url,
        "target_languages": target_languages,
    }
    _write_state(args, result)
    print(f"KRE_VIDEO_TRANSLATOR_SUBMIT_JSON={json.dumps(result, ensure_ascii=False)}")
    return result, source_path, source_url


def _read_result_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ParamError(f"Unable to read result JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ParamError("Result JSON must be an object.")
    if isinstance(payload.get("task"), dict):
        payload = payload["task"]
    if isinstance(payload.get("result"), dict):
        return payload
    if isinstance(payload.get("cc_list"), list):
        return {"schema_version": SCHEMA_VERSION, "status": "completed", "result": payload}
    raise ParamError("Result JSON does not contain a subtitle result.")


def _load_completed_task(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    if args.result_json:
        wrapper = _read_result_file(Path(args.result_json).expanduser().resolve())
        return wrapper, str(wrapper.get("request_id") or "")
    if not args.task_id:
        raise ParamError("Provide --task-id or --result-json.")
    base_url = _normalize_base_url(args.base_url)
    api_key = credentials.require_key(args.locale)
    request_lib = _require_requests(allow_install=args.allow_install_tools)
    with request_lib.Session() as session:
        task, request_id = _fetch_task(session, base_url, api_key, args.task_id, args.request_timeout)
    if _task_state(task) != "completed":
        raise ScriptError(f"Task {args.task_id} is not complete; use status or resume before export.")
    return _result_wrapper(
        task=task,
        input_file=Path(args.input_file).expanduser().resolve() if args.input_file else None,
        source_url=None,
        idempotency_key="",
        request_id=request_id,
    ), request_id


def _export(args: argparse.Namespace, wrapper: dict[str, Any] | None = None) -> dict[str, Any]:
    if wrapper is None:
        wrapper, request_id = _load_completed_task(args)
    else:
        request_id = str(wrapper.get("request_id") or "")
    result = wrapper.get("result") if isinstance(wrapper.get("result"), dict) else {}
    cc_list = [item for item in result.get("cc_list", []) if isinstance(item, dict)]
    if not cc_list:
        raise ScriptError("The result JSON contains no subtitle segments.")
    task_id = str(wrapper.get("task_id") or args.task_id or "translation-task")
    target_languages = _normalize_languages(list(wrapper.get("target_languages") or [])) or _infer_target_languages(cc_list)
    input_path = Path(args.input_file).expanduser().resolve() if args.input_file else None
    if args.format == "json":
        output = Path(args.output).expanduser() if args.output else Path.cwd() / f"{task_id}.json"
        _write_json_atomic(output, wrapper)
        return {"format": "json", "output": str(output.resolve()), "task_id": task_id}
    language = str(args.language or "").strip().lower()
    if language:
        if language not in target_languages:
            raise ParamError(f"Language {language!r} is not present in the result.")
        target_languages = [language]
    if args.format == "srt":
        outputs = _resolve_output_paths(
            input_path=input_path,
            output_arg=args.output,
            target_languages=target_languages,
            task_id=task_id,
        )
        written = {}
        for language_code, path in outputs.items():
            _write_atomic(
                path,
                _build_srt_text(cc_list, language_code, allow_source_fallback=bool(args.allow_source_fallback)),
            )
            written[language_code] = str(path.resolve())
        return {"format": "srt", "task_id": task_id, "outputs": written, "request_id": request_id or None}
    if not input_path or input_path.suffix.lower() not in VIDEO_EXTENSIONS:
        raise ParamError("Video export requires the original local video as the positional input file.")
    if len(target_languages) != 1:
        raise ParamError("Video export requires one target language; use --language.")
    ffmpeg = _ensure_subtitle_ffmpeg(allow_install=args.allow_install_tools, locale=args.locale)
    output = Path(args.output).expanduser() if args.output else input_path.with_name(f"{input_path.stem}.{target_languages[0]}.mp4")
    if output.suffix.lower() != ".mp4":
        output = output.with_suffix(".mp4")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    subtitle_directory = Path(tempfile.mkdtemp(prefix="kre-video-translator-subtitles-"))
    subtitle = subtitle_directory / "subtitles.srt"
    completed = False
    try:
        _write_atomic(subtitle, _build_srt_text(cc_list, target_languages[0], allow_source_fallback=bool(args.allow_source_fallback)))
        _run_process(
            [
                ffmpeg,
                "-y",
                "-i",
                str(input_path),
                "-vf",
                "subtitles=filename='subtitles.srt'",
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-movflags",
                "+faststart",
                str(output),
            ],
            "FFmpeg video export",
            cwd=subtitle_directory,
        )
        completed = True
    finally:
        subtitle.unlink(missing_ok=True)
        shutil.rmtree(subtitle_directory, ignore_errors=True)
        if not completed:
            output.unlink(missing_ok=True)
    return {"format": "video", "task_id": task_id, "language": target_languages[0], "output": str(output.resolve()), "request_id": request_id or None}


def _wait_for_task(args: argparse.Namespace, task_id: str, *, input_path: Path | None, source_url: str | None, idempotency_key: str, request_id: str) -> dict[str, Any]:
    base_url = _normalize_base_url(args.base_url)
    api_key = credentials.require_key(args.locale)
    request_lib = _require_requests(allow_install=args.allow_install_tools)
    with request_lib.Session() as session:
        task, poll_request_id = _poll_task(
            session,
            base_url=base_url,
            api_key=api_key,
            task_id=task_id,
            poll_interval=float(args.poll_interval),
            max_wait=max(0.1, float(args.max_wait)),
            timeout_seconds=max(0.1, float(args.request_timeout)),
        )
    wrapper = _result_wrapper(
        task=task,
        input_file=input_path,
        source_url=source_url,
        idempotency_key=idempotency_key,
        request_id=poll_request_id or request_id,
    )
    if args.result_json:
        _write_json_atomic(Path(args.result_json).expanduser(), wrapper)
    if args.state_file:
        _write_json_atomic(Path(args.state_file).expanduser(), wrapper)
    print(f"KRE_VIDEO_TRANSLATOR_RESULT_JSON={json.dumps(wrapper, ensure_ascii=False)}")
    return wrapper


def _status(args: argparse.Namespace) -> int:
    base_url = _normalize_base_url(args.base_url)
    api_key = credentials.require_key(args.locale)
    request_lib = _require_requests(allow_install=args.allow_install_tools)
    with request_lib.Session() as session:
        task, request_id = _fetch_task(session, base_url, api_key, args.task_id, args.request_timeout)
    payload = _task_progress(task)
    payload["request_id"] = request_id or None
    payload["task"] = task
    print(f"KRE_VIDEO_TRANSLATOR_STATUS_JSON={json.dumps(payload, ensure_ascii=False)}")
    return 0


def _error_next_action(error: BaseException) -> str:
    if isinstance(error, ToolInstallRequiredError):
        return "ask_user_to_approve_tool_install"
    error_code = str(getattr(error, "error_code", "") or "").strip().lower()
    status_code = int(getattr(error, "status_code", 0) or 0)
    message = str(error).lower()
    if error_code in BALANCE_ERROR_CODES or any(
        phrase in message
        for phrase in (
            "insufficient balance",
            "insufficient quota",
            "quota exceeded",
            "no available minutes",
            "余额不足",
            "配额不足",
        )
    ):
        return "user_check_balance"
    if (
        status_code in {502, 503, 504}
        or error_code in SERVICE_UNAVAILABLE_ERROR_CODES
        or isinstance(error, (ConnectionError, TimeoutError))
    ):
        return "check_skill_update_then_retry_once"
    return ""


def _emit_error(*, stage: str, task_id: str, idempotency_key: str, error: BaseException) -> None:
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "stage": stage,
        "task_id": task_id or None,
        "idempotency_key": idempotency_key or None,
        "request_id": getattr(error, "request_id", "") or None,
        "status_code": getattr(error, "status_code", 0) or None,
        "error_code": getattr(error, "error_code", "") or ("api_key_required" if isinstance(error, CredentialRequiredError) else "task_failed"),
        "error": str(error),
        "retryable": bool(getattr(error, "retryable", False)) or isinstance(error, PollTimeoutError),
    }
    next_action = _error_next_action(error)
    if next_action:
        payload["next_action"] = next_action
    if isinstance(error, ToolInstallRequiredError):
        payload.update(
            install_required=True,
            tool=error.tool,
            install_command=error.install_command,
        )
    if isinstance(error, CredentialRequiredError):
        payload.update(credentials.guidance(error.locale))
    print(f"KRE_VIDEO_TRANSLATOR_ERROR_JSON={json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)


def _emit_credential_guidance(locale: str = "") -> None:
    payload = credentials.guidance(locale)
    print(f"KRE_VIDEO_TRANSLATOR_CREDENTIAL_GUIDANCE_JSON={json.dumps(payload, ensure_ascii=False)}")
    print(payload["message"])


def main(argv: list[str] | None = None) -> int:
    _configure_stdio_utf8()
    normalized = _normalize_cli_args(argv)
    args = _build_parser().parse_args(normalized)
    stage = args.command
    active_task_id = str(getattr(args, "task_id", "") or "").strip()
    idempotency_key = str(getattr(args, "idempotency_key", "") or "").strip()
    try:
        if args.command == "preflight":
            return _preflight(args)
        if args.command == "status":
            return _status(args)
        if args.command == "export":
            payload = _export(args)
            print(f"KRE_VIDEO_TRANSLATOR_EXPORT_JSON={json.dumps(payload, ensure_ascii=False)}")
            return 0
        if getattr(args, "check", False):
            _require_requests(allow_install=args.allow_install_tools)
            payload = {
                "schema_version": SCHEMA_VERSION,
                "python": sys.version.split()[0],
                "requests": True,
                "api_key_configured": bool(credentials.resolve_key()),
                "base_url": _normalize_base_url(args.base_url),
                "ffmpeg": bool(_find_ffmpeg()),
            }
            print(f"KRE_VIDEO_TRANSLATOR_CHECK_JSON={json.dumps(payload, ensure_ascii=False)}")
            return 0
        if getattr(args, "list_models", False):
            base_url = _normalize_base_url(args.base_url)
            request_lib = _require_requests(allow_install=args.allow_install_tools)
            with request_lib.Session() as session:
                _print_models(session, base_url, args.request_timeout)
            return 0
        if args.command == "submit":
            _submit(args)
            return 0
        if args.command == "run":
            if args.export_format == "none" and args.output:
                args.export_format = "srt"
            if args.task_id:
                wrapper = _wait_for_task(args, args.task_id, input_path=Path(args.input_file).resolve() if args.input_file else None, source_url=None, idempotency_key=idempotency_key, request_id="")
            else:
                submitted, source_path, source_url = _submit(args)
                wrapper = _wait_for_task(args, submitted["task_id"], input_path=source_path, source_url=source_url, idempotency_key=submitted["idempotency_key"], request_id=str(submitted.get("request_id") or ""))
            if args.export_format != "none":
                export_args = argparse.Namespace(**vars(args))
                export_args.format = args.export_format
                export_args.result_json = args.result_json
                export_args.base_url = args.base_url
                export_args.input_file = args.input_file or wrapper.get("source_file")
                export_args.task_id = wrapper["task_id"]
                export_args.allow_install_tools = args.allow_install_tools
                export_args.no_install_tools = args.no_install_tools
                export_args.allow_source_fallback = args.allow_source_fallback
                payload = _export(export_args, wrapper)
                print(f"KRE_VIDEO_TRANSLATOR_EXPORT_JSON={json.dumps(payload, ensure_ascii=False)}")
            return 0
        if args.command == "resume":
            if not args.task_id:
                raise ParamError("resume requires --task-id.")
            wrapper = _wait_for_task(args, args.task_id, input_path=Path(args.input_file).resolve() if args.input_file else None, source_url=None, idempotency_key=idempotency_key, request_id="")
            if args.export_format != "none":
                export_args = argparse.Namespace(**vars(args))
                export_args.format = args.export_format
                export_args.result_json = args.result_json
                export_args.input_file = args.input_file or wrapper.get("source_file")
                export_args.allow_install_tools = args.allow_install_tools
                export_args.no_install_tools = args.no_install_tools
                export_args.allow_source_fallback = args.allow_source_fallback
                payload = _export(export_args, wrapper)
                print(f"KRE_VIDEO_TRANSLATOR_EXPORT_JSON={json.dumps(payload, ensure_ascii=False)}")
            return 0
        raise ParamError(f"Unsupported command: {args.command}")
    except KeyboardInterrupt as exc:
        _emit_error(stage=stage, task_id=active_task_id, idempotency_key=idempotency_key, error=exc)
        return 130
    except CredentialRequiredError as exc:
        _emit_credential_guidance(exc.locale)
        print(f"ERROR: {exc}", file=sys.stderr)
        _emit_error(stage=stage, task_id=active_task_id, idempotency_key=idempotency_key, error=exc)
        return 4
    except ParamError as exc:
        print(f"Parameter error: {exc}", file=sys.stderr)
        _emit_error(stage=stage, task_id=active_task_id, idempotency_key=idempotency_key, error=exc)
        return 2
    except PollTimeoutError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        _emit_error(stage=stage, task_id=active_task_id, idempotency_key=idempotency_key, error=exc)
        return 3
    except ScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        _emit_error(stage=stage, task_id=active_task_id, idempotency_key=idempotency_key, error=exc)
        return 1
    except Exception as exc:
        print(f"ERROR: Unexpected exception: {exc}", file=sys.stderr)
        _emit_error(stage=stage, task_id=active_task_id, idempotency_key=idempotency_key, error=exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
