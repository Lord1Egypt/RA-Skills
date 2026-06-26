"""
MinerU wrapper that supports both hosted API parsing and local open-source CLI parsing.
"""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import tempfile
import time
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx

DEFAULT_BASE_URL = "https://mineru.net"
DEFAULT_TIMEOUT = 60.0
DEFAULT_POLL_TIMEOUT = 900.0
DEFAULT_POLL_INTERVAL = 5.0
DOCS_URL = "https://mineru.net/apiManage/docs"
LOCAL_REPO_URL = "https://github.com/opendatalab/MinerU"
TEMP_ROOT = Path(tempfile.gettempdir()) / "mineru" / "doc-parsing"
DEFAULT_LOCAL_LANG = "ch"
DEFAULT_LOCAL_BACKEND = "pipeline"
DEFAULT_LOCAL_METHOD = "auto"

TERMINAL_SUCCESS_STATES = {"done", "completed", "success", "succeeded", "finished"}
TERMINAL_FAILURE_STATES = {"failed", "error", "cancelled", "canceled"}
RUNNING_STATES = {
    "pending",
    "queued",
    "running",
    "processing",
    "in_progress",
    "waiting-file",
    "converting",
}


@dataclass(frozen=True)
class Config:
    base_url: str
    token: str
    timeout: float
    poll_timeout: float
    poll_interval: float


@dataclass(frozen=True)
class LocalConfig:
    command: list[str]
    backend: str
    method: str
    lang: str
    model_source: str | None
    device_mode: str | None
    timeout: float | None


def _get_env(key: str, *fallbacks: str) -> str:
    for candidate in (key, *fallbacks):
        value = os.getenv(candidate, "").strip()
        if value:
            return value
    return ""


def _get_float_env(key: str, default: float) -> float:
    raw = os.getenv(key, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{key} must be a number, got: {raw}") from exc
    if value <= 0:
        raise ValueError(f"{key} must be greater than 0, got: {raw}")
    return value


def _get_optional_float_env(key: str) -> float | None:
    raw = os.getenv(key, "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{key} must be a number, got: {raw}") from exc
    if value <= 0:
        raise ValueError(f"{key} must be greater than 0, got: {raw}")
    return value


def _missing_api_token_message() -> str:
    if os.name == "nt":
        current_session = '$env:MINERU_API_TOKEN="YOUR_MINERU_TOKEN"'
        persist = 'setx MINERU_API_TOKEN "YOUR_MINERU_TOKEN"'
        reopen = "After setx, restart Codex/Cursor or open a new terminal."
    else:
        current_session = 'export MINERU_API_TOKEN="YOUR_MINERU_TOKEN"'
        persist = 'echo \'export MINERU_API_TOKEN="YOUR_MINERU_TOKEN"\' >> ~/.bashrc'
        reopen = "Open a new shell after updating your profile."

    return "\n".join(
        [
            "MINERU_API_TOKEN not configured for API mode.",
            "Set it in your environment before using --mode api.",
            f"Docs: {DOCS_URL}",
            f"One-shot command: {current_session}",
            f"Persist for future sessions: {persist}",
            reopen,
            "If you want local parsing instead, use --mode local with a configured MinerU runtime.",
        ]
    )


def get_config() -> Config:
    token = _get_env("MINERU_API_TOKEN", "MINERU_ACCESS_TOKEN")
    if not token:
        raise ValueError(_missing_api_token_message())

    base_url = _get_env("MINERU_API_BASE_URL") or DEFAULT_BASE_URL
    if not urlparse(base_url).scheme:
        base_url = f"https://{base_url}"
    base_url = base_url.rstrip("/")

    timeout = _get_float_env("MINERU_API_TIMEOUT", DEFAULT_TIMEOUT)
    poll_timeout = _get_float_env("MINERU_API_POLL_TIMEOUT", DEFAULT_POLL_TIMEOUT)
    poll_interval = _get_float_env("MINERU_API_POLL_INTERVAL", DEFAULT_POLL_INTERVAL)

    return Config(
        base_url=base_url,
        token=token,
        timeout=timeout,
        poll_timeout=poll_timeout,
        poll_interval=poll_interval,
    )


def get_local_config(
    *,
    language: str = "auto",
    local_cmd: str | None = None,
    local_python: str | None = None,
    local_backend: str | None = None,
    local_method: str | None = None,
    local_model_source: str | None = None,
    local_device: str | None = None,
    local_timeout: float | None = None,
) -> LocalConfig:
    command = _resolve_local_command(local_cmd=local_cmd, local_python=local_python)

    backend = (local_backend or _get_env("MINERU_LOCAL_BACKEND") or DEFAULT_LOCAL_BACKEND).strip()
    method = (local_method or _get_env("MINERU_LOCAL_METHOD") or DEFAULT_LOCAL_METHOD).strip()
    if method not in {"auto", "txt", "ocr"}:
        raise ValueError(f"Unsupported MINERU local method: {method}")

    if language and language != "auto":
        lang = language
    else:
        lang = _get_env("MINERU_LOCAL_LANG") or DEFAULT_LOCAL_LANG

    model_source = (local_model_source or _get_env("MINERU_LOCAL_MODEL_SOURCE")).strip() or None
    device_mode = (local_device or _get_env("MINERU_LOCAL_DEVICE_MODE")).strip() or None

    timeout = local_timeout
    if timeout is None:
        timeout = _get_optional_float_env("MINERU_LOCAL_TIMEOUT")

    return LocalConfig(
        command=command,
        backend=backend,
        method=method,
        lang=lang,
        model_source=model_source,
        device_mode=device_mode,
        timeout=timeout,
    )


def _resolve_local_command(*, local_cmd: str | None, local_python: str | None) -> list[str]:
    raw_cmd = (local_cmd or _get_env("MINERU_LOCAL_CMD")).strip()
    if raw_cmd:
        literal_path = Path(raw_cmd.strip("\"'")).expanduser()
        if literal_path.exists():
            return [str(literal_path.resolve())]
        return shlex.split(raw_cmd, posix=os.name != "nt")

    cmd_on_path = shutil.which("mineru.exe") or shutil.which("mineru")
    if cmd_on_path:
        return [cmd_on_path]

    python_path = (local_python or _get_env("MINERU_LOCAL_PYTHON")).strip()
    if python_path:
        return [str(Path(python_path).expanduser().resolve()), "-m", "mineru.cli.client"]

    raise ValueError(
        "MinerU local runtime not configured. Set MINERU_LOCAL_CMD, add mineru to PATH, "
        f"or set MINERU_LOCAL_PYTHON after installing the official MinerU package from {LOCAL_REPO_URL}."
    )


def _make_client(config: Config) -> httpx.Client:
    return httpx.Client(
        timeout=config.timeout,
        headers={
            "Authorization": f"Bearer {config.token}",
            "Accept": "application/json",
            "User-Agent": "mineru-ocr-local-api-skill/1.1.0",
        },
    )


def parse_document(
    *,
    file_url: str | None = None,
    file_path: str | None = None,
    mode: str = "api",
    language: str = "auto",
    enable_formula: bool = True,
    ocr: bool = False,
    wait: bool = True,
    download: bool = True,
    download_dir: str | None = None,
    local_cmd: str | None = None,
    local_python: str | None = None,
    local_backend: str | None = None,
    local_method: str | None = None,
    local_model_source: str | None = None,
    local_device: str | None = None,
    local_timeout: float | None = None,
) -> dict[str, Any]:
    if not file_url and not file_path:
        return _error("INPUT_ERROR", "file_url or file_path is required")
    if file_url and file_path:
        return _error("INPUT_ERROR", "provide only one of file_url or file_path")
    if mode not in {"api", "local", "auto"}:
        return _error("INPUT_ERROR", f"Unsupported mode: {mode}")

    responses: dict[str, Any] = {"submit": None, "batch": None, "poll": None, "local": None}
    artifacts: dict[str, Any] = {}

    try:
        resolved_mode = _resolve_mode(
            mode=mode,
            file_url=file_url,
            file_path=file_path,
            language=language,
            local_cmd=local_cmd,
            local_python=local_python,
            local_backend=local_backend,
            local_method=local_method,
            local_model_source=local_model_source,
            local_device=local_device,
            local_timeout=local_timeout,
        )
    except ValueError as exc:
        return _error("CONFIG_ERROR", str(exc), result=responses, artifacts=artifacts, mode=mode)

    artifacts["mode"] = resolved_mode

    try:
        if resolved_mode == "local":
            if file_url:
                return _error(
                    "INPUT_ERROR",
                    "Local MinerU parsing only supports --file-path. Use --mode api for --file-url.",
                    result=responses,
                    artifacts=artifacts,
                    mode=resolved_mode,
                )

            local_result, local_artifacts, text = _parse_local_document(
                file_path=file_path,
                language=language,
                enable_formula=enable_formula,
                ocr=ocr,
                download_dir=download_dir,
                local_cmd=local_cmd,
                local_python=local_python,
                local_backend=local_backend,
                local_method=local_method,
                local_model_source=local_model_source,
                local_device=local_device,
                local_timeout=local_timeout,
            )
            responses["local"] = local_result
            artifacts.update(local_artifacts)
            return {
                "ok": True,
                "mode": resolved_mode,
                "text": text,
                "result": responses,
                "artifacts": artifacts,
                "error": None,
            }

        config = get_config()
        with _make_client(config) as client:
            if file_url:
                submit_response = _create_url_task(
                    client,
                    config,
                    file_url=file_url,
                    language=language,
                    enable_formula=enable_formula,
                    ocr=ocr,
                )
                responses["submit"] = submit_response
                task_id = _extract_task_id(submit_response)
                if not task_id:
                    raise RuntimeError(
                        "MinerU did not return a task id. Inspect result.submit for details."
                    )
                artifacts["task_id"] = task_id
            else:
                batch_response, batch_id = _create_local_task(
                    client,
                    config,
                    file_path=file_path,
                    language=language,
                    enable_formula=enable_formula,
                    ocr=ocr,
                )
                responses["batch"] = batch_response
                artifacts["batch_id"] = batch_id

            if not wait:
                return {
                    "ok": True,
                    "mode": resolved_mode,
                    "text": "",
                    "result": responses,
                    "artifacts": artifacts,
                    "error": None,
                }

            if file_url:
                poll_response = _poll_task(client, config, artifacts["task_id"])
            else:
                poll_response = _poll_batch_result(
                    client,
                    config,
                    batch_id=artifacts["batch_id"],
                    filename=Path(file_path).name,
                )
            responses["poll"] = poll_response

            state = _extract_state(poll_response)
            if state:
                artifacts["state"] = state

            full_zip_url = _extract_full_zip_url(poll_response)
            if full_zip_url:
                artifacts["full_zip_url"] = full_zip_url

            text = ""
            if download and full_zip_url:
                artifact_paths = _download_and_extract(
                    client=client,
                    full_zip_url=full_zip_url,
                    task_id=artifacts.get("task_id") or artifacts.get("batch_id") or "result",
                    download_dir=download_dir,
                )
                artifacts.update(artifact_paths)
                full_md_path = artifact_paths.get("full_md_path")
                if full_md_path:
                    text = Path(full_md_path).read_text(encoding="utf-8")

            return {
                "ok": True,
                "mode": resolved_mode,
                "text": text,
                "result": responses,
                "artifacts": artifacts,
                "error": None,
            }
    except FileNotFoundError as exc:
        return _error("INPUT_ERROR", str(exc), result=responses, artifacts=artifacts, mode=resolved_mode)
    except subprocess.TimeoutExpired as exc:
        return _error(
            "LOCAL_ERROR",
            f"Local MinerU parsing timed out after {exc.timeout}s",
            result=responses,
            artifacts=artifacts,
            mode=resolved_mode,
        )
    except ValueError as exc:
        return _error("CONFIG_ERROR", str(exc), result=responses, artifacts=artifacts, mode=resolved_mode)
    except RuntimeError as exc:
        code = "LOCAL_ERROR" if resolved_mode == "local" else "API_ERROR"
        return _error(code, str(exc), result=responses, artifacts=artifacts, mode=resolved_mode)
    except OSError as exc:
        return _error("ARTIFACT_ERROR", str(exc), result=responses, artifacts=artifacts, mode=resolved_mode)


def _resolve_mode(
    *,
    mode: str,
    file_url: str | None,
    file_path: str | None,
    language: str,
    local_cmd: str | None,
    local_python: str | None,
    local_backend: str | None,
    local_method: str | None,
    local_model_source: str | None,
    local_device: str | None,
    local_timeout: float | None,
) -> str:
    if mode in {"api", "local"}:
        return mode

    if file_url:
        return "api"

    try:
        get_config()
        return "api"
    except ValueError:
        if not file_path:
            raise
        get_local_config(
            language=language,
            local_cmd=local_cmd,
            local_python=local_python,
            local_backend=local_backend,
            local_method=local_method,
            local_model_source=local_model_source,
            local_device=local_device,
            local_timeout=local_timeout,
        )
        return "local"


def _parse_local_document(
    *,
    file_path: str | None,
    language: str,
    enable_formula: bool,
    ocr: bool,
    download_dir: str | None,
    local_cmd: str | None,
    local_python: str | None,
    local_backend: str | None,
    local_method: str | None,
    local_model_source: str | None,
    local_device: str | None,
    local_timeout: float | None,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    path = Path(file_path or "").expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    config = get_local_config(
        language=language,
        local_cmd=local_cmd,
        local_python=local_python,
        local_backend=local_backend,
        local_method=local_method,
        local_model_source=local_model_source,
        local_device=local_device,
        local_timeout=local_timeout,
    )

    parse_method = "ocr" if ocr else config.method
    output_root = _resolve_local_output_root(path=path, download_dir=download_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    command = [
        *config.command,
        "-p",
        str(path),
        "-o",
        str(output_root),
        "-b",
        config.backend,
        "-m",
        parse_method,
        "-l",
        config.lang,
        "-f",
        "True" if enable_formula else "False",
    ]
    if config.model_source:
        command.extend(["--source", config.model_source])
    if config.device_mode:
        command.extend(["-d", config.device_mode])

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=config.timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Local MinerU command failed "
            f"({completed.returncode}). stderr: {_tail_text(completed.stderr)}"
        )

    artifacts, text = _collect_local_artifacts(output_root=output_root, file_stem=path.stem)
    local_result = {
        "command": command,
        "returncode": completed.returncode,
        "backend": config.backend,
        "parse_method": parse_method,
        "lang": config.lang,
        "model_source": config.model_source,
        "local_output_root": str(output_root),
        "stdout_tail": _tail_text(completed.stdout),
        "stderr_tail": _tail_text(completed.stderr),
    }
    return local_result, artifacts, text


def _resolve_local_output_root(*, path: Path, download_dir: str | None) -> Path:
    if download_dir:
        return Path(download_dir).expanduser().resolve()
    run_id = uuid.uuid4().hex[:8]
    return (TEMP_ROOT / "local" / f"{path.stem}_{run_id}").resolve()


def _collect_local_artifacts(*, output_root: Path, file_stem: str) -> tuple[dict[str, str], str]:
    doc_root = output_root / file_stem
    if not doc_root.exists():
        raise OSError(f"Local MinerU output directory not found: {doc_root}")

    full_md_path = _find_first(doc_root, f"{file_stem}.md") or _find_first_pattern(doc_root, "*.md")
    if not full_md_path:
        raise OSError(f"Local MinerU did not generate a Markdown file under: {doc_root}")

    middle_json_path = _find_first(doc_root, f"{file_stem}_middle.json")
    content_list_path = _find_first(doc_root, f"{file_stem}_content_list.json")
    content_list_v2_path = _find_first(doc_root, f"{file_stem}_content_list_v2.json")
    model_json_path = _find_first(doc_root, f"{file_stem}_model.json")
    layout_pdf_path = _find_first(doc_root, f"{file_stem}_layout.pdf")
    span_pdf_path = _find_first(doc_root, f"{file_stem}_span.pdf")
    origin_pdf_path = _find_first(doc_root, f"{file_stem}_origin.pdf")
    images_dir = _find_first_dir(doc_root, "images")

    artifacts: dict[str, str] = {
        "state": "done",
        "local_output_root": str(output_root),
        "local_doc_root": str(doc_root),
        "local_parse_dir": str(full_md_path.parent),
        "full_md_path": str(full_md_path),
    }
    if middle_json_path:
        artifacts["middle_json_path"] = str(middle_json_path)
    if content_list_path:
        artifacts["content_list_path"] = str(content_list_path)
    if content_list_v2_path:
        artifacts["content_list_v2_path"] = str(content_list_v2_path)
    if model_json_path:
        artifacts["model_json_path"] = str(model_json_path)
    if layout_pdf_path:
        artifacts["layout_pdf_path"] = str(layout_pdf_path)
    if span_pdf_path:
        artifacts["span_pdf_path"] = str(span_pdf_path)
    if origin_pdf_path:
        artifacts["origin_pdf_path"] = str(origin_pdf_path)
    if images_dir:
        artifacts["images_dir"] = str(images_dir)

    text = full_md_path.read_text(encoding="utf-8")
    return artifacts, text


def _find_first(root: Path, filename: str) -> Path | None:
    matches = sorted(root.rglob(filename), key=_path_sort_key)
    return matches[0] if matches else None


def _find_first_pattern(root: Path, pattern: str) -> Path | None:
    matches = sorted(root.rglob(pattern), key=_path_sort_key)
    return matches[0] if matches else None


def _find_first_dir(root: Path, dirname: str) -> Path | None:
    matches = sorted(
        (path for path in root.rglob(dirname) if path.is_dir()),
        key=_path_sort_key,
    )
    return matches[0] if matches else None


def _path_sort_key(path: Path) -> tuple[int, str]:
    return (len(path.parts), str(path).lower())


def _tail_text(value: str | None, limit: int = 1200) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        return ""
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[-limit:]


def _create_url_task(
    client: httpx.Client,
    config: Config,
    *,
    file_url: str,
    language: str,
    enable_formula: bool,
    ocr: bool,
) -> dict[str, Any]:
    payload = {
        "url": file_url,
        "language": language,
        "enable_formula": enable_formula,
        "is_ocr": ocr,
    }
    return _request_json(client, "POST", _endpoint(config, "/api/v4/extract/task"), json=payload)


def _create_local_task(
    client: httpx.Client,
    config: Config,
    *,
    file_path: str,
    language: str,
    enable_formula: bool,
    ocr: bool,
) -> tuple[dict[str, Any], str]:
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    payload = {
        "language": language,
        "enable_formula": enable_formula,
        "files": [{"name": path.name, "is_ocr": ocr}],
    }
    batch_response = _request_json(
        client,
        "POST",
        _endpoint(config, "/api/v4/file-urls/batch"),
        json=payload,
    )

    batch_id = _extract_batch_id(batch_response)
    if not batch_id:
        raise RuntimeError("MinerU upload flow did not return a batch_id.")

    upload_url = _extract_upload_url(batch_response)
    if not upload_url:
        raise RuntimeError("MinerU upload flow did not return a file upload URL.")

    _upload_file(upload_url=upload_url, path=path)
    return batch_response, batch_id


def _poll_task(client: httpx.Client, config: Config, task_id: str) -> dict[str, Any]:
    deadline = time.monotonic() + config.poll_timeout
    last_response: dict[str, Any] | None = None

    while time.monotonic() < deadline:
        response = _request_json(
            client,
            "GET",
            _endpoint(config, f"/api/v4/extract/task/{task_id}"),
        )
        last_response = response

        state = _extract_state(response)
        if _extract_full_zip_url(response):
            return response
        if state in TERMINAL_SUCCESS_STATES:
            return response
        if state in TERMINAL_FAILURE_STATES:
            message = _extract_message(response) or f"MinerU task failed with state={state}"
            raise RuntimeError(message)
        if state and state not in RUNNING_STATES and _looks_terminal_without_zip(response):
            return response

        time.sleep(config.poll_interval)

    message = f"Polling timed out after {config.poll_timeout:.0f}s for task {task_id}"
    if last_response is not None:
        message = f"{message}. Last state: {_extract_state(last_response) or 'unknown'}"
    raise RuntimeError(message)


def _poll_batch_result(
    client: httpx.Client,
    config: Config,
    *,
    batch_id: str,
    filename: str,
) -> dict[str, Any]:
    deadline = time.monotonic() + config.poll_timeout
    last_response: dict[str, Any] | None = None

    while time.monotonic() < deadline:
        response = _request_json(
            client,
            "GET",
            _endpoint(config, f"/api/v4/extract-results/batch/{batch_id}"),
        )
        last_response = response

        entry = _extract_batch_result_entry(response, filename=filename)
        state = _extract_state(entry or response)
        full_zip_url = _extract_full_zip_url(entry or response)

        if full_zip_url:
            return entry or response
        if state in TERMINAL_SUCCESS_STATES:
            return entry or response
        if state in TERMINAL_FAILURE_STATES:
            message = _extract_message(entry or response) or f"MinerU batch task failed with state={state}"
            raise RuntimeError(message)

        time.sleep(config.poll_interval)

    message = f"Polling timed out after {config.poll_timeout:.0f}s for batch {batch_id}"
    if last_response is not None:
        entry = _extract_batch_result_entry(last_response, filename=filename)
        state = _extract_state(entry or last_response)
        message = f"{message}. Last state: {state or 'unknown'}"
    raise RuntimeError(message)


def _download_and_extract(
    *,
    client: httpx.Client,
    full_zip_url: str,
    task_id: str,
    download_dir: str | None,
) -> dict[str, str]:
    task_root = (
        Path(download_dir).expanduser().resolve()
        if download_dir
        else (TEMP_ROOT / "tasks" / task_id).resolve()
    )
    task_root.mkdir(parents=True, exist_ok=True)

    zip_path = task_root / "result.zip"
    extracted_dir = task_root / "extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)

    del client

    try:
        with httpx.stream("GET", full_zip_url, timeout=DEFAULT_TIMEOUT, follow_redirects=True) as response:
            if response.status_code >= 400:
                raise RuntimeError(
                    f"Failed to download MinerU archive ({response.status_code}): {response.text[:200]}"
                )
            with zip_path.open("wb") as handle:
                for chunk in response.iter_bytes():
                    handle.write(chunk)
    except (httpx.TimeoutException, httpx.RequestError, RuntimeError):
        _download_with_curl(full_zip_url=full_zip_url, destination=zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extracted_dir)

    full_md_path = _find_in_tree(extracted_dir, "full.md")
    middle_json_path = _find_in_tree(extracted_dir, "middle.json")
    content_list_path = _find_in_tree(extracted_dir, "content_list.json")

    artifacts = {
        "downloaded_zip": str(zip_path),
        "extracted_dir": str(extracted_dir),
    }
    if full_md_path:
        artifacts["full_md_path"] = str(full_md_path)
    if middle_json_path:
        artifacts["middle_json_path"] = str(middle_json_path)
    if content_list_path:
        artifacts["content_list_path"] = str(content_list_path)
    return artifacts


def _download_with_curl(*, full_zip_url: str, destination: Path) -> None:
    curl_bin = shutil.which("curl.exe") or shutil.which("curl")
    if not curl_bin:
        raise RuntimeError("curl is not available for MinerU archive download fallback.")

    result = subprocess.run(
        [
            curl_bin,
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--output",
            str(destination),
            full_zip_url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise RuntimeError(
            f"Failed to download MinerU archive via curl ({result.returncode}): {stderr}"
        )


def _find_in_tree(root: Path, filename: str) -> Path | None:
    matches = sorted(root.rglob(filename), key=_path_sort_key)
    return matches[0] if matches else None


def _upload_file(*, upload_url: str, path: Path) -> None:
    with path.open("rb") as handle:
        try:
            response = httpx.put(
                upload_url,
                content=handle.read(),
                timeout=DEFAULT_TIMEOUT,
                follow_redirects=True,
            )
        except httpx.TimeoutException as exc:
            raise RuntimeError(f"Timed out while uploading {path.name} to MinerU") from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"Failed to upload {path.name} to MinerU: {exc}") from exc
    if response.status_code not in (200, 201, 204):
        raise RuntimeError(
            f"MinerU upload failed ({response.status_code}): {response.text[:200]}"
        )


def _request_json(
    client: httpx.Client,
    method: str,
    url: str,
    **kwargs: Any,
) -> dict[str, Any]:
    try:
        response = client.request(method, url, **kwargs)
    except httpx.TimeoutException as exc:
        raise RuntimeError(f"Request timed out while calling {url}") from exc
    except httpx.RequestError as exc:
        raise RuntimeError(f"Request failed while calling {url}: {exc}") from exc

    if response.status_code >= 400:
        detail = response.text[:400].strip()
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = _extract_message(payload) or detail
        except json.JSONDecodeError:
            pass
        raise RuntimeError(f"HTTP {response.status_code} from {url}: {detail}")

    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"MinerU returned invalid JSON from {url}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"MinerU returned a non-object JSON payload from {url}")

    if _is_error_payload(payload):
        raise RuntimeError(_extract_message(payload) or f"MinerU returned an error for {url}")

    return payload


def _endpoint(config: Config, path: str) -> str:
    return urljoin(config.base_url + "/", path.lstrip("/"))


def _is_error_payload(payload: dict[str, Any]) -> bool:
    for key in ("success", "ok"):
        value = payload.get(key)
        if isinstance(value, bool):
            return not value

    for key in ("code", "error_code", "status_code"):
        value = payload.get(key)
        if isinstance(value, int) and value not in {0, 200}:
            return True
        if isinstance(value, str) and value not in {"0", "200", "success"}:
            lowered = value.strip().lower()
            if lowered not in {"", "ok", "done", "success"}:
                return True

    error = payload.get("error")
    return isinstance(error, dict) and bool(error)


def _extract_message(payload: Any) -> str | None:
    for key in ("message", "msg", "detail", "error_msg"):
        value = _find_key(payload, key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    error = _find_key(payload, "error")
    if isinstance(error, dict):
        for key in ("message", "msg", "detail"):
            value = error.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _extract_task_id(payload: Any) -> str | None:
    for key in ("task_id", "taskId", "id"):
        value = _find_key(payload, key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _extract_batch_id(payload: Any) -> str | None:
    for key in ("batch_id", "batchId"):
        value = _find_key(payload, key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _extract_state(payload: Any) -> str | None:
    for key in ("state", "status", "task_status"):
        value = _find_key(payload, key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    return None


def _extract_full_zip_url(payload: Any) -> str | None:
    for key in ("full_zip_url", "zip_url"):
        value = _find_key(payload, key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _extract_upload_url(payload: dict[str, Any]) -> str | None:
    data = payload.get("data")
    if isinstance(data, dict):
        file_urls = data.get("file_urls") or data.get("files")
        if isinstance(file_urls, list) and file_urls:
            first = file_urls[0]
            if isinstance(first, str) and first.strip():
                return first.strip()
    return None


def _extract_batch_result_entry(payload: dict[str, Any], *, filename: str) -> dict[str, Any] | None:
    data = payload.get("data")
    if not isinstance(data, dict):
        return None

    entries = data.get("extract_result")
    if not isinstance(entries, list):
        return None

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        file_name = entry.get("file_name")
        if isinstance(file_name, str) and file_name == filename:
            return entry

    if len(entries) == 1 and isinstance(entries[0], dict):
        return entries[0]
    return None


def _looks_terminal_without_zip(payload: dict[str, Any]) -> bool:
    state = _extract_state(payload)
    if state in TERMINAL_SUCCESS_STATES:
        return True
    return bool(_find_key(payload, "result_url"))


def _find_key(payload: Any, target: str) -> Any:
    if isinstance(payload, dict):
        if target in payload:
            return payload[target]
        for value in payload.values():
            found = _find_key(value, target)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = _find_key(item, target)
            if found is not None:
                return found
    return None


def _error(
    code: str,
    message: str,
    *,
    result: dict[str, Any] | None = None,
    artifacts: dict[str, Any] | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "mode": mode,
        "text": "",
        "result": result or {"submit": None, "batch": None, "poll": None, "local": None},
        "artifacts": artifacts or {},
        "error": {"code": code, "message": message},
    }
