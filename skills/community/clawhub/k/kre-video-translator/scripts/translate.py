"""
KreTrans audio/video subtitle translation script for local media files.

Flow:
1) Extract a 16k mono mp3 from the input media with ffmpeg
2) Submit /external/tasks to create a translation task
3) Poll /external/tasks/{task_id} every 15 seconds
4) Write result.cc_list to an .srt file
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

import requests


DOCS_URL = "https://kretrans.com/api-docs"
API_KEY_MANAGEMENT_URL = "https://kretrans.com/console#api-management"
API_KEY_ENV_NAME = "KRETRANS_API_KEY"
API_BASE_URL = "https://api.kretrans.com/v1/api"
DEFAULT_CREATE_TIMEOUT_SECONDS = 600
DEFAULT_POLL_TIMEOUT_SECONDS = 30
DEFAULT_POLL_INTERVAL_SECONDS = 15
DEFAULT_MAX_TRANSLATE_LANGUAGES = 10

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".wmv",
    ".flv",
    ".webm",
    ".mpeg",
    ".mpg",
    ".m4v",
}


class ScriptError(RuntimeError):
    """Script execution error."""


class ParamError(ScriptError):
    """Parameter error."""


class DocsArgumentParser(argparse.ArgumentParser):
    """Append the API docs URL after argument errors."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\nSee docs: {DOCS_URL}\n")


def _configure_stdio_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            continue


def _resolve_api_key_from_env() -> str:
    return str(os.getenv(API_KEY_ENV_NAME, "") or "").strip()


def _build_api_key_setup_hint() -> str:
    return (
        "Missing API key.\n"
        f"Create or copy an API key at {API_KEY_MANAGEMENT_URL},\n"
        f"then set the {API_KEY_ENV_NAME} environment variable."
    )


def _tail(text: str, size: int = 1200) -> str:
    content = str(text or "")
    if len(content) <= size:
        return content
    return content[-size:]


def _parse_language_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    for raw in values:
        text = str(raw or "").strip()
        if not text:
            continue
        for part in text.replace("|", ",").split(","):
            code = str(part or "").strip().lower()
            if code and code not in result:
                result.append(code)
    return result


def _normalize_translate_languages(target_language: str, values: list[str]) -> list[str]:
    normalized: list[str] = []
    for code in values:
        item = str(code or "").strip().lower()
        if item and item not in normalized:
            normalized.append(item)

    target = str(target_language or "").strip().lower()
    if not target:
        raise ParamError("Invalid argument: --target-language cannot be empty.")

    if target in normalized:
        normalized.remove(target)
    normalized.insert(0, target)

    if DEFAULT_MAX_TRANSLATE_LANGUAGES > 0 and len(normalized) > DEFAULT_MAX_TRANSLATE_LANGUAGES:
        raise ParamError(
            "Invalid argument: too many translate_languages values.\n"
            f"current_count={len(normalized)}\n"
            f"max_count={DEFAULT_MAX_TRANSLATE_LANGUAGES}"
        )
    return normalized


def _resolve_output_path(input_path: Path, output_arg: str | None) -> Path:
    text = str(output_arg or "").strip()
    if not text:
        return input_path.with_suffix(".srt")

    target = Path(text).expanduser()
    if target.exists() and target.is_dir():
        return target / f"{input_path.stem}.srt"
    if target.suffix.lower() != ".srt":
        return target.with_suffix(".srt")
    return target


def _build_ffmpeg_install_guide() -> str:
    system_name = platform.system().strip().lower()
    if system_name == "windows":
        return (
            "ffmpeg was not found. Install it first and make sure it is in PATH.\n"
            "Windows installation options:\n"
            "1) winget install -e --id Gyan.FFmpeg\n"
            "2) choco install ffmpeg\n"
            "3) scoop install ffmpeg"
        )
    if system_name == "darwin":
        return "ffmpeg was not found. Install it first: brew install ffmpeg"
    return (
        "ffmpeg was not found. Install it first.\n"
        "Linux examples:\n"
        "Debian/Ubuntu: sudo apt update && sudo apt install -y ffmpeg\n"
        "Fedora: sudo dnf install -y ffmpeg\n"
        "Arch: sudo pacman -S ffmpeg"
    )


def _ensure_ffmpeg() -> str:
    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin:
        return ffmpeg_bin
    raise ScriptError(_build_ffmpeg_install_guide())


def _extract_audio_to_mp3(ffmpeg_bin: str, input_file: Path, output_file: Path) -> None:
    command = [
        ffmpeg_bin,
        "-hide_banner",
        "-y",
        "-i",
        str(input_file),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "libmp3lame",
        "-b:a",
        "128k",
        str(output_file),
    ]
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0 or not output_file.is_file():
        raise ScriptError(
            "ffmpeg failed to extract mp3 audio.\n"
            f"input={input_file}\n"
            f"output={output_file}\n"
            f"exit_code={completed.returncode}\n"
            f"stderr={_tail(completed.stderr)}"
        )


def _safe_json_response(resp: requests.Response, action: str) -> dict[str, Any]:
    try:
        payload = resp.json()
    except ValueError as exc:
        body_preview = str(resp.text or "").strip()
        if len(body_preview) > 800:
            body_preview = f"{body_preview[:800]}...(truncated)"
        raise ScriptError(
            f"{action} failed: response is not valid JSON.\n"
            f"HTTP={resp.status_code}\n"
            f"URL={resp.url}\n"
            f"Body={body_preview}"
        ) from exc

    if not isinstance(payload, dict):
        raise ScriptError(
            f"{action} failed: response JSON has an unexpected format.\n"
            f"HTTP={resp.status_code}\n"
            f"URL={resp.url}\n"
            f"Payload={payload}"
        )
    return payload


def _unwrap_business_payload(payload: dict[str, Any], action: str) -> Any:
    try:
        status_code = int(payload.get("status_code") or 0)
    except Exception:
        status_code = 0
    if status_code == 200:
        return payload.get("content")

    message = str(payload.get("message") or payload.get("err_msg") or "Request failed").strip()
    error_code = str(payload.get("error_code") or "").strip()
    request_id = str(payload.get("request_id") or "").strip()
    retryable = bool(payload.get("retryable"))
    raise ScriptError(
        f"{action} failed: {message}\n"
        f"status_code={status_code}\n"
        f"error_code={error_code or '-'}\n"
        f"request_id={request_id or '-'}\n"
        f"retryable={retryable}"
    )


def _request_business_json(
    session: requests.Session,
    method: str,
    url: str,
    *,
    action: str,
    timeout_seconds: int,
    **kwargs: Any,
) -> Any:
    try:
        resp = session.request(method=method, url=url, timeout=timeout_seconds, **kwargs)
    except requests.RequestException as exc:
        raise ScriptError(f"{action} failed: network error: {exc}") from exc
    payload = _safe_json_response(resp, action=action)
    return _unwrap_business_payload(payload, action=action)


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _to_milliseconds(value: Any) -> int:
    try:
        n = float(value)
    except Exception:
        return 0
    if not (n == n):
        return 0
    return max(0, int(round(n)))


def _detect_second_unit(cc_list: list[dict[str, Any]]) -> bool:
    if not cc_list:
        return False
    durations: list[float] = []
    max_time = 0.0
    for item in cc_list:
        try:
            start = float(item.get("start"))
            end = float(item.get("end"))
        except Exception:
            continue
        max_time = max(max_time, start, end)
        if end > start:
            durations.append(end - start)
    if not durations:
        return False
    sorted_durations = sorted(durations)
    median = sorted_durations[len(sorted_durations) // 2]
    return max_time > 0 and max_time < 10000 and 0 < median < 120


def _format_srt_time(milliseconds: int) -> str:
    total_ms = _to_milliseconds(milliseconds)
    total_seconds = total_ms // 1000
    ms = total_ms % 1000
    hour = total_seconds // 3600
    minute = (total_seconds % 3600) // 60
    sec = total_seconds % 60
    return f"{hour:02d}:{minute:02d}:{sec:02d},{ms:03d}"


def _subtitle_text_for_target(item: dict[str, Any], target_language: str) -> str:
    target_field = f"{target_language}_translate"
    preferred = item.get(target_field)
    if preferred is not None and str(preferred).strip():
        return str(preferred)
    translated = item.get("translated")
    if translated is not None and str(translated).strip():
        return str(translated)
    return str(item.get("text") or "")


def _build_srt_text(cc_list: list[dict[str, Any]], target_language: str) -> str:
    scale = 1000 if _detect_second_unit(cc_list) else 1
    normalized: list[dict[str, Any]] = []
    for idx, raw in enumerate(cc_list):
        start = _to_milliseconds(_to_float(raw.get("start")) * scale)
        end = _to_milliseconds(_to_float(raw.get("end")) * scale)
        text = _subtitle_text_for_target(raw, target_language=target_language)
        normalized.append(
            {
                "start": start,
                "end": max(start, end),
                "text": text,
                "_order": idx,
            }
        )
    normalized.sort(key=lambda x: (x["start"], x["end"], x["_order"]))

    lines: list[str] = []
    for idx, item in enumerate(normalized, start=1):
        lines.append(str(idx))
        lines.append(f"{_format_srt_time(item['start'])} --> {_format_srt_time(item['end'])}")
        lines.append(str(item["text"]))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _probe_source_is_video(input_file: Path) -> bool:
    return input_file.suffix.lower() in VIDEO_EXTENSIONS


def _create_task(
    session: requests.Session,
    *,
    base_url: str,
    api_key: str,
    source_language: str,
    target_language: str,
    input_file: Path,
    audio_file: Path,
    translate_languages: list[str],
    translate_model: str,
    prompt: str,
    summary_enabled: bool,
    create_timeout_seconds: int,
) -> tuple[str, str]:
    advanced_options: dict[str, Any] = {
        "original_filename": input_file.name,
        "translate_languages": translate_languages,
        "source_is_video": _probe_source_is_video(input_file),
    }
    if prompt:
        advanced_options["prompt"] = prompt
    if summary_enabled:
        advanced_options["summary_enabled"] = True
    if translate_model:
        advanced_options["translate_model"] = translate_model

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Idempotency-Key": uuid.uuid4().hex,
    }
    with audio_file.open("rb") as fp:
        content = _request_business_json(
            session,
            "POST",
            f"{base_url}/external/tasks",
            action="Create task",
            timeout_seconds=create_timeout_seconds,
            headers=headers,
            data={
                "source_language": source_language,
                "target_language": target_language,
                "advanced_options": json.dumps(advanced_options, ensure_ascii=False),
            },
            files={
                "file": (audio_file.name, fp, "audio/mpeg"),
            },
        )

    if not isinstance(content, dict):
        raise ScriptError(f"Create task returned an unexpected payload: {content}")
    task_id = str(content.get("task_id") or "").strip()
    request_id = str(content.get("request_id") or "").strip()
    if not task_id:
        raise ScriptError(f"Create task succeeded but task_id was missing: {content}")
    return task_id, request_id


def _poll_task_until_done(
    session: requests.Session,
    *,
    base_url: str,
    task_id: str,
    api_key: str,
    poll_timeout_seconds: int,
    poll_interval_seconds: int,
) -> dict[str, Any]:
    while True:
        detail_content = _request_business_json(
            session,
            "GET",
            f"{base_url}/external/tasks/{task_id}",
            action="Fetch task details",
            timeout_seconds=poll_timeout_seconds,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        if not isinstance(detail_content, dict):
            raise ScriptError(f"Fetch task details returned an unexpected payload: {detail_content}")

        status = str(detail_content.get("status") or "").strip().lower()
        progress = detail_content.get("progress")
        logs = detail_content.get("logs") if isinstance(detail_content.get("logs"), list) else []
        latest_log = ""
        if logs:
            last = logs[-1] if isinstance(logs[-1], dict) else {}
            latest_log = str(last.get("msg") or "").strip()

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] status={status or '-'} progress={progress} latest_log={latest_log or '-'}")

        if status == "success":
            return detail_content
        if status == "failed":
            error = str(detail_content.get("error") or "").strip()
            error_code = str(detail_content.get("error_code") or "").strip()
            retryable = bool(detail_content.get("retryable"))
            provider_error_code = str(detail_content.get("provider_error_code") or "").strip()
            raise ScriptError(
                "Task execution failed:\n"
                f"task_id={task_id}\n"
                f"error={error or '-'}\n"
                f"error_code={error_code or '-'}\n"
                f"provider_error_code={provider_error_code or '-'}\n"
                f"retryable={retryable}"
            )

        time.sleep(poll_interval_seconds)


def _build_parser() -> argparse.ArgumentParser:
    parser = DocsArgumentParser(
        description="Translate local audio/video into subtitles using the built-in KreTrans API, ffmpeg mp3 extraction, task polling, and SRT export.",
    )
    parser.add_argument("input_file", help="Path to a local audio or video file")
    parser.add_argument("--source-language", default="auto", help="Source language, default: auto")
    parser.add_argument("--target-language", default="zh", help="Target language, default: zh")
    parser.add_argument(
        "--translate-languages",
        nargs="*",
        default=None,
        help="Optional additional target languages, separated by spaces or commas; target_language is always placed first",
    )
    parser.add_argument("--translate-model", default="", help="Optional translation model")
    parser.add_argument("--prompt", default="", help="Optional custom prompt")
    parser.add_argument("--summary-enabled", action="store_true", help="Optional: enable summary")
    parser.add_argument("--output", default="", help="Output SRT path; defaults to the input filename with .srt")
    parser.add_argument(
        "--create-timeout-seconds",
        type=int,
        default=DEFAULT_CREATE_TIMEOUT_SECONDS,
        help=f"Timeout in seconds for task creation requests (default: {DEFAULT_CREATE_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=DEFAULT_POLL_TIMEOUT_SECONDS,
        help=f"Timeout in seconds for polling requests (default: {DEFAULT_POLL_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=DEFAULT_POLL_INTERVAL_SECONDS,
        help=f"Polling interval in seconds (default: {DEFAULT_POLL_INTERVAL_SECONDS})",
    )
    return parser


def _print_docs_hint() -> None:
    print(f"See docs: {DOCS_URL}", file=sys.stderr)
    print(f"API key management: {API_KEY_MANAGEMENT_URL}", file=sys.stderr)


def main() -> int:
    _configure_stdio_utf8()
    parser = _build_parser()
    args = parser.parse_args()

    try:
        api_key = _resolve_api_key_from_env()
        if not api_key:
            raise ParamError(_build_api_key_setup_hint())

        input_file = Path(str(args.input_file or "").strip()).expanduser().resolve()
        if not input_file.is_file():
            raise ParamError(f"Input file does not exist: {input_file}")

        if int(args.create_timeout_seconds or 0) <= 0:
            raise ParamError("--create-timeout-seconds must be greater than 0.")
        if int(args.poll_timeout_seconds or 0) <= 0:
            raise ParamError("--poll-timeout-seconds must be greater than 0.")
        if int(args.poll_interval_seconds or 0) <= 0:
            raise ParamError("--poll-interval-seconds must be greater than 0.")

        base_url = API_BASE_URL
        source_language = str(args.source_language or "").strip().lower() or "auto"
        target_language = str(args.target_language or "").strip().lower()
        translate_languages = _normalize_translate_languages(
            target_language=target_language,
            values=_parse_language_list(args.translate_languages),
        )
        translate_model = str(args.translate_model or "").strip()
        prompt = str(args.prompt or "").strip()
        output_path = _resolve_output_path(input_file, args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        ffmpeg_bin = _ensure_ffmpeg()

        with requests.Session() as session:
            print(f"[1/4] Extracting mp3 audio with ffmpeg: {input_file.name}")
            with tempfile.TemporaryDirectory(prefix="kre_video_translator_audio_") as tmp_dir:
                audio_file = Path(tmp_dir) / f"{input_file.stem}.mp3"
                _extract_audio_to_mp3(ffmpeg_bin=ffmpeg_bin, input_file=input_file, output_file=audio_file)

                print(f"[2/4] Creating task: POST {base_url}/external/tasks")
                task_id, request_id = _create_task(
                    session=session,
                    base_url=base_url,
                    api_key=api_key,
                    source_language=source_language,
                    target_language=target_language,
                    input_file=input_file,
                    audio_file=audio_file,
                    translate_languages=translate_languages,
                    translate_model=translate_model,
                    prompt=prompt,
                    summary_enabled=bool(args.summary_enabled),
                    create_timeout_seconds=int(args.create_timeout_seconds),
                )

            print(f"Task created: task_id={task_id} request_id={request_id or '-'}")
            print(f"[3/4] Polling task details every {int(args.poll_interval_seconds)} seconds")
            detail = _poll_task_until_done(
                session=session,
                base_url=base_url,
                task_id=task_id,
                api_key=api_key,
                poll_timeout_seconds=int(args.poll_timeout_seconds),
                poll_interval_seconds=int(args.poll_interval_seconds),
            )

        result = detail.get("result")
        if not isinstance(result, dict):
            raise ScriptError(f"Task succeeded but result has an unexpected format: {result}")
        cc_list = result.get("cc_list")
        if not isinstance(cc_list, list):
            raise ScriptError(f"Task succeeded but result.cc_list is missing or invalid: {result}")

        cc_items = [item for item in cc_list if isinstance(item, dict)]
        if not cc_items:
            raise ScriptError("Task succeeded but no valid subtitle items were returned (cc_list is empty).")

        srt_text = _build_srt_text(cc_items, target_language=target_language)
        print(f"[4/4] Writing SRT: {output_path}")
        output_path.write_text(srt_text, encoding="utf-8")
        print(f"Done: {output_path} ({len(cc_items)} subtitles, language {target_language})")
        return 0

    except ParamError as exc:
        print(f"Parameter error: {exc}", file=sys.stderr)
        _print_docs_hint()
        return 2
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
        return 130
    except ScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        _print_docs_hint()
        return 1
    except Exception as exc:
        print(f"ERROR: Unexpected exception: {exc}", file=sys.stderr)
        _print_docs_hint()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
