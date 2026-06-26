#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

"""
Extract voice features for FunAudioLLM-CosyVoice-300M from a URL audio file.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any
from urllib import error, parse, request

API_URL = "https://ai.gitee.com/v1/audio/voice-feature-extraction"
DEFAULT_MODEL = "FunAudioLLM-CosyVoice-300M"


class VoiceFeatureConfigError(RuntimeError):
    """Raised when required input parameters are invalid."""


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")


def ensure_file_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        raise VoiceFeatureConfigError("--file-url must be an http(s) URL")
    return url


def request_http(
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
        timeout: int = 30,
) -> tuple[int, dict[str, str], bytes]:
    req = request.Request(url=url, data=body, headers=headers or {}, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            return response.status, dict(response.headers.items()), response.read()
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"API request failed ({exc.code}): {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc


def download_file(file_url: str, timeout: int) -> tuple[str, str, bytes]:
    status, headers, content = request_http("GET", file_url, timeout=timeout)
    if status < 200 or status >= 300:
        raise RuntimeError(f"Failed to download file URL: HTTP {status}")

    parsed = parse.urlparse(file_url)
    filename = PurePosixPath(parsed.path).name or "audio.bin"
    content_type = headers.get("Content-Type") or mimetypes.guess_type(filename)[0]
    return filename, content_type or "application/octet-stream", content


def build_multipart_body(
        *,
        prompt: str,
        model: str,
        filename: str,
        file_content_type: str,
        file_content: bytes,
) -> tuple[str, bytes]:
    boundary = f"----CodexBoundary{uuid.uuid4().hex}"
    parts: list[bytes] = []

    def add_field(name: str, value: str) -> None:
        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8")
        )
        parts.append(value.encode("utf-8"))
        parts.append(b"\r\n")

    add_field("prompt", prompt)
    add_field("model", model)

    parts.append(f"--{boundary}\r\n".encode("utf-8"))
    parts.append(
        (
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: {file_content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    parts.append(file_content)
    parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))

    return boundary, b"".join(parts)


def extract_first_url(data: Any) -> str | None:
    if isinstance(data, str):
        if data.startswith(("http://", "https://")):
            return data
        return None

    if isinstance(data, list):
        for item in data:
            url = extract_first_url(item)
            if url:
                return url
        return None

    if isinstance(data, dict):
        for key in ("url", "voice_url", "download_url", "file_url"):
            value = data.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return value
        for value in data.values():
            url = extract_first_url(value)
            if url:
                return url
    return None


def save_binary_content(data: bytes, output_path: str | None) -> str:
    path = Path(output_path or "voice-feature-output.bin")
    path.write_bytes(data)
    return str(path.resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract voice features for FunAudioLLM-CosyVoice-300M from a URL file"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Prompt text used for voice feature extraction",
    )
    parser.add_argument(
        "--file-url",
        required=True,
        help="Source audio file URL (http/https only)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Voice feature model name. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--failover-enabled",
        choices=["true", "false"],
        default="true",
        help="X-Failover-Enabled header value. Default: true",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds. Default: 30",
    )
    parser.add_argument(
        "--output",
        help="Output path when API returns binary voice feature content",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="Gitee AI API key (overrides GITEEAI_API_KEY env var)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GITEEAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    try:
        file_url = ensure_file_url(args.file_url)
        filename, content_type, file_content = download_file(file_url, timeout=args.timeout)
        boundary, body = build_multipart_body(
            prompt=args.prompt,
            model=args.model,
            filename=filename,
            file_content_type=content_type,
            file_content=file_content,
        )
        _, headers, raw_response = request_http(
            "POST",
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Failover-Enabled": args.failover_enabled,
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            body=body,
            timeout=args.timeout,
        )
        print(f"MODEL: {args.model}")

        content_type = headers.get("Content-Type", "")
        if "application/json" in content_type:
            response = json.loads(raw_response.decode("utf-8"))
            extracted_url = extract_first_url(response)
            if extracted_url:
                print(f"VOICE_URL: {extracted_url}")
            print(f"VOICE_FEATURE_RESULT: {json.dumps(response, ensure_ascii=False)}")
            return

        output_path = save_binary_content(raw_response, args.output)
        print(f"VOICE_FEATURE_FILE: {output_path}")
        print(f"VOICE_FEATURE_RESULT: {{\"content_type\": \"{content_type}\", \"bytes\": {len(raw_response)}}}")
    except VoiceFeatureConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(2)
    except RuntimeError as exc:
        print(f"Error extracting voice features: {exc}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error parsing API response JSON: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
