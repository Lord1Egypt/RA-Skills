#!/usr/bin/env python3
"""Send one request to a local ACE-Step REST server and print the JSON reply.

Standard library only. The helper refuses any server that is not on the
loopback interface (127.0.0.1, localhost, ::1), ignores proxy settings,
refuses HTTP redirects, sends only what the caller passes on the command line,
and never runs downloaded content.

Examples:

    python3 scripts/acestep_request.py health
    python3 scripts/acestep_request.py release_task --print-task-id --json '{"prompt": "...", "audio_duration": 60}'
    python3 scripts/acestep_request.py release_task --json-file body.json
    python3 scripts/acestep_request.py query_result --json '{"task_ids": ["<TASK_ID>"]}'
    python3 scripts/acestep_request.py release_task --form task_type=cover --form-file src_audio=/path/to/source.wav
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
GET_ENDPOINTS = {"health", "v1/stats", "v1/models"}


def is_loopback_url(api_url: str) -> bool:
    parsed = urllib.parse.urlparse(api_url)
    return parsed.scheme in {"http", "https"} and (parsed.hostname or "") in LOOPBACK_HOSTS


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Refuse every HTTP redirect so a reply can never send us off the loopback host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401, ANN001
        raise urllib.error.HTTPError(newurl, code, f"redirect refused (loopback-only client): {newurl}", headers, fp)


def loopback_opener() -> urllib.request.OpenerDirector:
    """Opener that ignores proxy settings and refuses redirects."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), _RejectRedirects())


def split_pair(text: str, flag: str) -> tuple[str, str]:
    if "=" not in text:
        raise ValueError(f"{flag} expects key=value, got {text!r}")
    key, value = text.split("=", 1)
    if not key:
        raise ValueError(f"{flag} expects a non-empty key, got {text!r}")
    return key, value


def build_multipart(fields: list[tuple[str, str]], files: list[tuple[str, Path]]) -> tuple[bytes, str]:
    """Encode form fields and files as multipart/form-data."""
    boundary = f"----acestep-{uuid.uuid4().hex}"
    parts: list[bytes] = []
    for key, value in fields:
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode("utf-8")
        )
    for key, path in files:
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        header = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"; filename="{path.name}"\r\n'
            f"Content-Type: {mime}\r\n\r\n"
        ).encode("utf-8")
        parts.append(header + path.read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def build_request(
    api_url: str,
    endpoint: str,
    json_body: object | None,
    fields: list[tuple[str, str]],
    files: list[tuple[str, Path]],
) -> urllib.request.Request:
    url = f"{api_url.rstrip('/')}/{endpoint.strip('/')}"
    if fields or files:
        data, content_type = build_multipart(fields, files)
        return urllib.request.Request(url, data=data, headers={"Content-Type": content_type}, method="POST")
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        return urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    method = "GET" if endpoint.strip("/") in GET_ENDPOINTS else "POST"
    return urllib.request.Request(url, method=method)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Send one request to a local ACE-Step server")
    parser.add_argument("endpoint", help="e.g. health, release_task, query_result, v1/init")
    parser.add_argument("--api-url", default="http://127.0.0.1:8001", help="loopback ACE-Step server URL")
    body = parser.add_mutually_exclusive_group()
    body.add_argument("--json", dest="json_text", help="JSON request body as a string")
    body.add_argument("--json-file", type=Path, help="file holding the JSON request body")
    parser.add_argument("--form", action="append", default=[], metavar="KEY=VALUE", help="multipart form field")
    parser.add_argument("--form-file", action="append", default=[], metavar="KEY=PATH", help="multipart file field")
    parser.add_argument("--print-task-id", action="store_true", help="print only data.task_id from the reply")
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args(argv)

    if not is_loopback_url(args.api_url):
        parser.error("--api-url must point at a local ACE-Step server (127.0.0.1, localhost or ::1)")
    if (args.form or args.form_file) and (args.json_text or args.json_file):
        parser.error("use either a JSON body or form fields, not both")
    try:
        json_body = None
        if args.json_text is not None:
            json_body = json.loads(args.json_text)
        elif args.json_file is not None:
            json_body = json.loads(args.json_file.read_text(encoding="utf-8"))
        fields = [split_pair(item, "--form") for item in args.form]
        files = [(key, Path(value).expanduser()) for key, value in (split_pair(i, "--form-file") for i in args.form_file)]
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    for _, path in files:
        if not path.is_file():
            parser.error(f"--form-file path not found: {path}")

    request = build_request(args.api_url, args.endpoint, json_body, fields, files)
    if not is_loopback_url(request.full_url):
        parser.error(f"refusing non-loopback request URL: {request.full_url}")
    try:
        with loopback_opener().open(request, timeout=args.timeout) as response:
            reply = json.loads(response.read().decode("utf-8") or "{}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    if args.print_task_id:
        data = reply.get("data") if isinstance(reply, dict) else None
        task_id = data.get("task_id", "") if isinstance(data, dict) else ""
        print(task_id)
        return 0 if task_id else 1
    print(json.dumps(reply, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
