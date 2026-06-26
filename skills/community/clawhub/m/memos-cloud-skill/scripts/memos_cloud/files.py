from __future__ import annotations

import base64
import os
from typing import BinaryIO, Dict, Iterable, Optional

from .errors import FilePayloadError, ValidationError

_MIME_MAP: dict[str, str] = {
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".json": "application/json",
    ".md": "text/markdown",
    ".xml": "application/xml",
    ".csv": "text/csv",
    ".html": "text/html",
    ".htm": "text/html",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".zip": "application/zip",
}


def infer_mime_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    return _MIME_MAP.get(ext, "application/octet-stream")


def build_file_payloads(
    files: Iterable[str],
    file_type: str = "document",
) -> list[Dict[str, str]]:
    file_list: list[Dict[str, str]] = []

    for file_spec in files:
        if is_url(file_spec):
            file_list.append({"type": file_type, "content": file_spec})
            continue

        if os.path.isfile(file_spec):
            file_list.append(build_local_file_payload(file_spec, file_type))
            continue

        raise ValidationError(
            f"Invalid file: '{file_spec}'. Must be a URL (http/https) or existing file path."
        )

    return file_list


def build_stdin_file_payload(
    stdin_buffer: BinaryIO,
    file_type: str = "document",
    name: Optional[str] = None,
) -> Dict[str, str]:
    try:
        raw = stdin_buffer.read()
        b64 = normalize_base64_content(raw)
        mime_type = infer_mime_type(name) if name else "application/octet-stream"
        file_info: Dict[str, str] = {
            "type": file_type,
            "content": to_data_uri(mime_type, b64),
        }
        if name:
            file_info["name"] = name
        return file_info
    except Exception as exc:
        if isinstance(exc, FilePayloadError):
            raise
        raise FilePayloadError("Stdin Error", f"Failed to read from stdin: {str(exc)}") from exc


def to_data_uri(mime_type: str, base64_content: str) -> str:
    return f"data:{mime_type};base64,{base64_content}"


def build_local_file_payload(file_spec: str, file_type: str = "document") -> Dict[str, str]:
    try:
        with open(file_spec, "rb") as file:
            file_data = file.read()
    except Exception as exc:
        raise FilePayloadError(
            "File Error",
            f"Failed to read file '{file_spec}': {str(exc)}",
        ) from exc

    mime_type = infer_mime_type(file_spec)
    return {
        "type": file_type,
        "name": os.path.basename(file_spec),
        "content": to_data_uri(mime_type, encode_base64(file_data)),
        "mime_type": mime_type,
    }


def normalize_base64_content(raw: bytes) -> str:
    try:
        b64_content = raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        return encode_base64(raw)

    try:
        base64.b64decode(b64_content, validate=True)
        return b64_content
    except Exception:
        return encode_base64(raw)


def encode_base64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("utf-8")


def is_url(file_spec: str) -> bool:
    return file_spec.startswith(("http://", "https://"))
