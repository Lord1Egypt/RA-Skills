#!/usr/bin/env python3
"""Small MinerU API client for Own Style Writer.

The client intentionally uses only the Python standard library so the skill can
try MinerU before installing the local MarkItDown fallback runtime.
"""

from __future__ import annotations

import hashlib
import io
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


BASE_URL = "https://mineru.net"
API_KEY_ENV = "MINERU_API_KEY"
MODEL_VERSION_ENV = "MINERU_MODEL_VERSION"
DEFAULT_MODEL_VERSION = "vlm"

PRECISE_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".jp2",
    ".webp",
    ".gif",
    ".bmp",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
}
AGENT_EXTENSIONS = PRECISE_EXTENSIONS
PRECISE_MAX_BYTES = 200 * 1024 * 1024
AGENT_MAX_BYTES = 10 * 1024 * 1024
PRECISE_BATCH_SIZE = 50

APPLY_TIMEOUT_SECONDS = 30
UPLOAD_TIMEOUT_SECONDS = 300
POLL_TIMEOUT_SECONDS = 30
DOWNLOAD_TIMEOUT_SECONDS = 300
DEFAULT_POLL_INTERVAL_SECONDS = 10
DEFAULT_MAX_WAIT_MINUTES = 30


class MinerUError(RuntimeError):
    """Raised when MinerU cannot complete a conversion."""


@dataclass
class MinerUResult:
    source: Path
    output: Path | None
    status: str
    mode: str
    characters: int = 0
    error: str | None = None


def env_api_key() -> str:
    return os.environ.get(API_KEY_ENV, "").strip()


def env_model_version(default: str = DEFAULT_MODEL_VERSION) -> str:
    return os.environ.get(MODEL_VERSION_ENV, "").strip() or default


def can_use_precise(path: Path) -> tuple[bool, str | None]:
    if path.suffix.lower() not in PRECISE_EXTENSIONS:
        return False, "unsupported by MinerU precise API"
    if path.stat().st_size > PRECISE_MAX_BYTES:
        return False, "file is larger than MinerU precise API 200MB limit"
    return True, None


def can_use_agent(path: Path) -> tuple[bool, str | None]:
    if path.suffix.lower() not in AGENT_EXTENSIONS:
        return False, "unsupported by MinerU agent API"
    if path.stat().st_size > AGENT_MAX_BYTES:
        return False, "file is larger than MinerU agent API 10MB limit"
    return True, None


def convert_precise_batch(
    files: list[Path],
    output_dir: Path,
    output_names: dict[Path, str],
    *,
    api_key: str | None = None,
    model_version: str | None = None,
    max_wait_minutes: int = DEFAULT_MAX_WAIT_MINUTES,
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
    base_url: str = BASE_URL,
) -> dict[Path, MinerUResult]:
    """Convert files with MinerU precise batch upload API."""

    token = (api_key or env_api_key()).strip()
    if not token:
        raise MinerUError(f"{API_KEY_ENV} is required for MinerU precise API")

    output_dir.mkdir(parents=True, exist_ok=True)
    results: dict[Path, MinerUResult] = {}
    eligible: list[Path] = []
    for source in files:
        ok, reason = can_use_precise(source)
        if ok:
            eligible.append(source)
        else:
            results[source] = MinerUResult(source, None, "failed", "mineru-precise", error=reason)

    for batch in _chunked(eligible, PRECISE_BATCH_SIZE):
        results.update(
            _convert_precise_one_batch(
                batch,
                output_dir,
                output_names,
                token,
                model_version=model_version or env_model_version(),
                max_wait_minutes=max_wait_minutes,
                poll_interval_seconds=poll_interval_seconds,
                base_url=base_url,
            )
        )

    return results


def _convert_precise_one_batch(
    files: list[Path],
    output_dir: Path,
    output_names: dict[Path, str],
    api_key: str,
    *,
    model_version: str,
    max_wait_minutes: int,
    poll_interval_seconds: int,
    base_url: str,
) -> dict[Path, MinerUResult]:
    tasks = []
    for index, path in enumerate(files):
        data_id = f"file_{index}_{hashlib.sha1(str(path).encode('utf-8')).hexdigest()[:10]}"
        tasks.append({"path": path, "data_id": data_id})

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    apply_payload = {
        "files": [{"name": task["path"].name, "data_id": task["data_id"]} for task in tasks],
        "model_version": model_version,
    }
    apply_url = f"{base_url.rstrip('/')}/api/v4/file-urls/batch"
    apply_data = _request_json("POST", apply_url, headers=headers, payload=apply_payload, timeout=APPLY_TIMEOUT_SECONDS)
    if apply_data.get("code") != 0:
        raise MinerUError(f"MinerU precise upload-url request failed: {apply_data}")

    data = apply_data.get("data") or {}
    batch_id = data.get("batch_id") or data.get("batchId")
    upload_urls = data.get("file_urls") or data.get("fileUrls") or []
    if not batch_id:
        raise MinerUError("MinerU precise response missing batch_id")

    task_by_data_id = {task["data_id"]: task for task in tasks}
    results: dict[Path, MinerUResult] = {}
    upload_failed: set[str] = set()

    for task, raw_upload in zip(tasks, upload_urls):
        upload_url = _pick_upload_url(raw_upload)
        if not upload_url:
            upload_failed.add(task["data_id"])
            results[task["path"]] = MinerUResult(
                task["path"],
                None,
                "failed",
                "mineru-precise",
                error="MinerU did not return an upload URL",
            )
            continue
        try:
            _upload_file(upload_url, task["path"])
        except Exception as exc:
            upload_failed.add(task["data_id"])
            results[task["path"]] = MinerUResult(
                task["path"], None, "failed", "mineru-precise", error=f"upload failed: {exc}"
            )

    if len(upload_urls) < len(tasks):
        for task in tasks[len(upload_urls) :]:
            upload_failed.add(task["data_id"])
            results[task["path"]] = MinerUResult(
                task["path"],
                None,
                "failed",
                "mineru-precise",
                error="MinerU returned fewer upload URLs than files",
            )

    poll_url = f"{base_url.rstrip('/')}/api/v4/extract-results/batch/{urllib.parse.quote(str(batch_id))}"
    finished = set(upload_failed)
    started_at = time.monotonic()
    max_wait_seconds = max_wait_minutes * 60 if max_wait_minutes and max_wait_minutes > 0 else None

    while len(finished) < len(tasks):
        if max_wait_seconds is not None and time.monotonic() - started_at >= max_wait_seconds:
            for task in tasks:
                if task["data_id"] not in finished:
                    finished.add(task["data_id"])
                    results[task["path"]] = MinerUResult(
                        task["path"],
                        None,
                        "failed",
                        "mineru-precise",
                        error=f"parse timed out after {max_wait_minutes} minutes",
                    )
            break

        time.sleep(poll_interval_seconds)
        poll_data = _request_json("GET", poll_url, headers=headers, timeout=POLL_TIMEOUT_SECONDS)
        if poll_data.get("code") != 0:
            continue

        payload = poll_data.get("data") or {}
        extract_results = payload.get("extract_result") or payload.get("extractResult") or payload.get("results") or []
        for item in extract_results:
            data_id = item.get("data_id") or item.get("dataId")
            task = task_by_data_id.get(data_id)
            if not task or data_id in finished:
                continue

            state = str(item.get("state") or item.get("status") or "").lower()
            if state in {"done", "success", "succeeded", "completed"}:
                zip_url = item.get("full_zip_url") or item.get("fullZipUrl") or item.get("zip_url") or item.get("zipUrl")
                try:
                    output = _download_zip_markdown(zip_url, output_dir / output_names[task["path"]])
                    text = output.read_text(encoding="utf-8", errors="replace")
                    results[task["path"]] = MinerUResult(
                        task["path"], output, "converted", "mineru-precise", characters=len(text)
                    )
                except Exception as exc:
                    results[task["path"]] = MinerUResult(
                        task["path"],
                        None,
                        "failed",
                        "mineru-precise",
                        error=f"download or markdown extraction failed: {exc}",
                    )
                finished.add(data_id)
            elif state in {"failed", "error"}:
                err = item.get("err_msg") or item.get("error") or item.get("message") or "MinerU parse failed"
                results[task["path"]] = MinerUResult(task["path"], None, "failed", "mineru-precise", error=str(err))
                finished.add(data_id)

    return results


def convert_agent_file(
    source: Path,
    output: Path,
    *,
    max_wait_minutes: int = DEFAULT_MAX_WAIT_MINUTES,
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
    base_url: str = BASE_URL,
) -> MinerUResult:
    """Convert one file with MinerU's no-token agent endpoint.

    MinerU has changed response field names before, so this method accepts
    immediate markdown, a markdown URL, a poll URL, or a task id.
    """

    ok, reason = can_use_agent(source)
    if not ok:
        return MinerUResult(source, None, "failed", "mineru-agent", error=reason)

    submit_url = f"{base_url.rstrip('/')}/api/v1/agent/parse/file"
    try:
        submit = _request_multipart(submit_url, source, timeout=UPLOAD_TIMEOUT_SECONDS)
        return _handle_agent_response(
            submit,
            source,
            output,
            max_wait_minutes=max_wait_minutes,
            poll_interval_seconds=poll_interval_seconds,
            base_url=base_url,
        )
    except Exception as exc:
        return MinerUResult(source, None, "failed", "mineru-agent", error=str(exc))


def _handle_agent_response(
    data: dict[str, Any],
    source: Path,
    output: Path,
    *,
    max_wait_minutes: int,
    poll_interval_seconds: int,
    base_url: str,
) -> MinerUResult:
    current = data
    started_at = time.monotonic()
    max_wait_seconds = max_wait_minutes * 60 if max_wait_minutes and max_wait_minutes > 0 else None

    while True:
        saved = _save_agent_markdown_if_present(current, output)
        if saved:
            text = saved.read_text(encoding="utf-8", errors="replace")
            return MinerUResult(source, saved, "converted", "mineru-agent", characters=len(text))

        state = _extract_state(current)
        if state in {"failed", "error"}:
            return MinerUResult(source, None, "failed", "mineru-agent", error=_extract_error(current))

        poll_url = _extract_poll_url(current, base_url=base_url)
        if not poll_url:
            return MinerUResult(
                source,
                None,
                "failed",
                "mineru-agent",
                error=f"MinerU agent response missing markdown_url, poll_url, and task id: {current}",
            )

        if max_wait_seconds is not None and time.monotonic() - started_at >= max_wait_seconds:
            return MinerUResult(
                source,
                None,
                "failed",
                "mineru-agent",
                error=f"parse timed out after {max_wait_minutes} minutes",
            )

        time.sleep(poll_interval_seconds)
        current = _request_json("GET", poll_url, headers={}, timeout=POLL_TIMEOUT_SECONDS)


def _save_agent_markdown_if_present(data: dict[str, Any], output: Path) -> Path | None:
    payload = _flatten_response(data)
    markdown = payload.get("markdown") or payload.get("md") or payload.get("content")
    if isinstance(markdown, str) and markdown.strip():
        _write_text(output, markdown)
        return output

    markdown_url = (
        payload.get("markdown_url")
        or payload.get("markdownUrl")
        or payload.get("md_url")
        or payload.get("mdUrl")
        or payload.get("url")
    )
    if isinstance(markdown_url, str) and markdown_url.startswith(("http://", "https://")):
        text = _download_text(markdown_url)
        _write_text(output, text)
        return output

    return None


def _extract_poll_url(data: dict[str, Any], *, base_url: str) -> str | None:
    payload = _flatten_response(data)
    for key in ("poll_url", "pollUrl", "result_url", "resultUrl"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return urllib.parse.urljoin(base_url, value)

    task_id = payload.get("task_id") or payload.get("taskId") or payload.get("id")
    if task_id:
        quoted = urllib.parse.quote(str(task_id))
        return f"{base_url.rstrip('/')}/api/v1/agent/parse/result/{quoted}"
    return None


def _extract_state(data: dict[str, Any]) -> str:
    payload = _flatten_response(data)
    return str(payload.get("state") or payload.get("status") or "").lower()


def _extract_error(data: dict[str, Any]) -> str:
    payload = _flatten_response(data)
    return str(payload.get("err_msg") or payload.get("error") or payload.get("message") or "MinerU agent parse failed")


def _flatten_response(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    nested = payload.get("data")
    if isinstance(nested, dict):
        payload.update(nested)
    return payload


def _request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int,
) -> dict[str, Any]:
    body = None
    request_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise MinerUError(f"HTTP {exc.code} from {url}: {raw}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise MinerUError(f"non-JSON response from {url}: {raw[:500]}") from exc


def _request_multipart(url: str, source: Path, *, timeout: int) -> dict[str, Any]:
    boundary = "----OwnStyleWriter" + uuid.uuid4().hex
    mime_type = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{source.name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = head + source.read_bytes() + tail
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise MinerUError(f"HTTP {exc.code} from {url}: {raw}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise MinerUError(f"non-JSON response from {url}: {raw[:500]}") from exc


def _upload_file(upload_url: str, source: Path) -> None:
    request = urllib.request.Request(upload_url, data=source.read_bytes(), method="PUT")
    with urllib.request.urlopen(request, timeout=UPLOAD_TIMEOUT_SECONDS) as response:
        if response.status < 200 or response.status >= 300:
            raise MinerUError(f"upload returned HTTP {response.status}")


def _download_zip_markdown(zip_url: str | None, output: Path) -> Path:
    if not zip_url:
        raise MinerUError("missing full_zip_url")
    data = _download_bytes(zip_url, timeout=DOWNLOAD_TIMEOUT_SECONDS)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith(".md")]
        if not names:
            raise MinerUError("result ZIP does not contain Markdown")
        names.sort(key=lambda name: (0 if name.lower().endswith("full.md") else 1, len(name), name))
        text = archive.read(names[0]).decode("utf-8", errors="replace")
    _write_text(output, text)
    return output


def _download_text(url: str) -> str:
    data = _download_bytes(url, timeout=DOWNLOAD_TIMEOUT_SECONDS)
    return data.decode("utf-8", errors="replace")


def _download_bytes(url: str, *, timeout: int) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        if response.status < 200 or response.status >= 300:
            raise MinerUError(f"download returned HTTP {response.status}")
        return response.read()


def _write_text(output: Path, text: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8", newline="\n")


def _pick_upload_url(raw: Any) -> str | None:
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict):
        for key in ("url", "upload_url", "uploadUrl", "file_url", "fileUrl"):
            value = raw.get(key)
            if isinstance(value, str):
                return value
    return None


def _chunked(items: list[Path], size: int) -> Iterable[list[Path]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]
