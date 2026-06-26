#!/usr/bin/env python3
"""Google Drive helper for OpenClaw using service-account or OAuth auth."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"
DEFAULT_SCOPE = "https://www.googleapis.com/auth/drive"
FOLDER_MIME = "application/vnd.google-apps.folder"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def load_service_account(raw_value: str) -> dict:
    candidate = raw_value.strip()
    if candidate.startswith("{"):
        data = json.loads(candidate)
    else:
        data = json.loads(Path(candidate).read_text())
    required = ["client_email", "private_key"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise SystemExit(f"GOOGLE_SERVICE_ACCOUNT_KEY is missing required field(s): {', '.join(missing)}")
    return data


def refresh_oauth_access_token(refresh_token: str) -> str:
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit(
            "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are required to exchange a refresh token for an access token"
        )

    payload = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"OAuth token refresh failed: HTTP {exc.code}: {detail}")
    return data.get("access_token") or refresh_token


def sign_rs256(message: bytes, private_key: str) -> bytes:
    key_path = tempfile.mktemp(prefix="oc_gdrive_")
    fd = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, private_key.encode("utf-8"))
        os.close(fd)
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", key_path],
            input=message,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            raise SystemExit(proc.stderr.decode("utf-8", "replace").strip() or "openssl signing failed")
        return proc.stdout
    finally:
        try:
            os.unlink(key_path)
        except OSError:
            pass


def mint_access_token(sa: dict, scope: str, subject: str | None) -> str:
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    claim = {
        "iss": sa["client_email"],
        "scope": scope,
        "aud": sa.get("token_uri", "https://oauth2.googleapis.com/token"),
        "iat": now,
        "exp": now + 3600,
    }
    if subject:
        claim["sub"] = subject

    signing_input = f"{b64url(json.dumps(header, separators=(',', ':')).encode())}.{b64url(json.dumps(claim, separators=(',', ':')).encode())}"
    signature = sign_rs256(signing_input.encode("ascii"), sa["private_key"])
    assertion = f"{signing_input}.{b64url(signature)}"

    payload = urllib.parse.urlencode(
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        sa.get("token_uri", "https://oauth2.googleapis.com/token"),
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"Token exchange failed: HTTP {exc.code}: {detail}")
    return data["access_token"]


def request_json(method: str, path: str, token: str, params: dict | None = None, body: dict | None = None) -> dict:
    url = f"{DRIVE_API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"Drive API failed: HTTP {exc.code}: {detail}")


def request_bytes(method: str, url: str, token: str, data: bytes | None = None, content_type: str | None = None) -> bytes:
    headers = {"Authorization": f"Bearer {token}"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"Drive download failed: HTTP {exc.code}: {detail}")


def common_file_params(limit: int) -> dict:
    return {
        "pageSize": limit,
        "includeItemsFromAllDrives": "true",
        "supportsAllDrives": "true",
        "fields": "files(id,name,mimeType,parents,driveId,webViewLink,createdTime,modifiedTime,size),nextPageToken",
    }


def emit_json(data: dict) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def write_output(data: bytes, out_path: str | None, text: bool = False) -> None:
    if out_path:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if text:
            path.write_text(data.decode("utf-8"))
        else:
            path.write_bytes(data)
        print(str(path))
        return
    if text:
        sys.stdout.write(data.decode("utf-8"))
        if not data.endswith(b"\n"):
            sys.stdout.write("\n")
    else:
        sys.stdout.buffer.write(data)


def cmd_whoami(args: argparse.Namespace, token: str) -> None:
    data = request_json(
        "GET",
        "/about",
        token,
        {
            "fields": "user(displayName,emailAddress,permissionId),storageQuota(limit,usage,usageInDrive,usageInDriveTrash)",
            "supportsAllDrives": "true",
        },
    )
    emit_json(data)


def cmd_search(args: argparse.Namespace, token: str) -> None:
    params = common_file_params(args.limit)
    params["q"] = args.query
    params["corpora"] = "allDrives"
    params["orderBy"] = args.order_by
    data = request_json("GET", "/files", token, params)
    emit_json(data if args.json else {"files": data.get("files", [])})


def cmd_ls(args: argparse.Namespace, token: str) -> None:
    params = common_file_params(args.limit)
    params["q"] = f"'{args.folder_id}' in parents and trashed = false"
    params["corpora"] = "allDrives"
    params["orderBy"] = args.order_by
    data = request_json("GET", "/files", token, params)
    emit_json(data if args.json else {"files": data.get("files", [])})


def cmd_info(args: argparse.Namespace, token: str) -> None:
    data = request_json(
        "GET",
        f"/files/{args.file_id}",
        token,
        {
            "fields": "id,name,mimeType,parents,driveId,owners(displayName,emailAddress),webViewLink,webContentLink,createdTime,modifiedTime,size,description,trashed,shared,capabilities",
            "supportsAllDrives": "true",
        },
    )
    emit_json(data)


def cmd_download(args: argparse.Namespace, token: str) -> None:
    url = f"{DRIVE_API_BASE}/files/{args.file_id}?alt=media&supportsAllDrives=true"
    data = request_bytes("GET", url, token)
    write_output(data, args.out)


def cmd_export(args: argparse.Namespace, token: str) -> None:
    params = urllib.parse.urlencode({"mimeType": args.mime})
    url = f"{DRIVE_API_BASE}/files/{args.file_id}/export?{params}"
    data = request_bytes("GET", url, token)
    write_output(data, args.out, text=args.text)


def cmd_cat(args: argparse.Namespace, token: str) -> None:
    info = request_json(
        "GET",
        f"/files/{args.file_id}",
        token,
        {"fields": "id,name,mimeType", "supportsAllDrives": "true"},
    )
    mime_type = info["mimeType"]
    if mime_type.startswith("application/vnd.google-apps."):
        export_mime = args.mime or "text/plain"
        params = urllib.parse.urlencode({"mimeType": export_mime})
        url = f"{DRIVE_API_BASE}/files/{args.file_id}/export?{params}"
        data = request_bytes("GET", url, token)
        write_output(data[: args.limit_bytes], None, text=True)
        return
    url = f"{DRIVE_API_BASE}/files/{args.file_id}?alt=media&supportsAllDrives=true"
    data = request_bytes("GET", url, token)
    write_output(data[: args.limit_bytes], None, text=True)


def cmd_mkdir(args: argparse.Namespace, token: str) -> None:
    body = {"name": args.name, "mimeType": FOLDER_MIME}
    if args.parent:
        body["parents"] = [args.parent]
    data = request_json(
        "POST",
        "/files",
        token,
        {"supportsAllDrives": "true", "fields": "id,name,mimeType,parents,webViewLink"},
        body,
    )
    emit_json(data)


def cmd_upload(args: argparse.Namespace, token: str) -> None:
    local_path = Path(args.path)
    if not local_path.exists():
        raise SystemExit(f"Local file not found: {local_path}")
    file_bytes = local_path.read_bytes()
    mime_type = args.mime or mimetypes.guess_type(local_path.name)[0] or "application/octet-stream"
    metadata = {"name": args.name or local_path.name}
    if args.parent:
        metadata["parents"] = [args.parent]

    boundary = "openclaw-gdrive-upload"
    parts = [
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode("utf-8"),
        json.dumps(metadata).encode("utf-8"),
        f"\r\n--{boundary}\r\nContent-Type: {mime_type}\r\n\r\n".encode("utf-8"),
        file_bytes,
        f"\r\n--{boundary}--\r\n".encode("utf-8"),
    ]
    body = b"".join(parts)
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&fields=id,name,mimeType,parents,webViewLink"
    data = request_bytes("POST", url, token, data=body, content_type=f"multipart/related; boundary={boundary}")
    emit_json(json.loads(data.decode("utf-8")))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Drive helper using Google service-account or OAuth auth")
    parser.add_argument("--scope", default=DEFAULT_SCOPE, help="OAuth scope to request")
    parser.add_argument("--subject", default=os.environ.get("GOOGLE_DRIVE_SUBJECT"), help="Optional delegated user email")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("whoami", help="Show the active Drive principal")

    search = subparsers.add_parser("search", help="Search Drive with a q expression")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=25)
    search.add_argument("--order-by", default="folder,name_natural")
    search.add_argument("--json", action="store_true")

    ls_cmd = subparsers.add_parser("ls", help="List children of a folder")
    ls_cmd.add_argument("folder_id")
    ls_cmd.add_argument("--limit", type=int, default=100)
    ls_cmd.add_argument("--order-by", default="folder,name_natural")
    ls_cmd.add_argument("--json", action="store_true")

    info = subparsers.add_parser("info", help="Show file metadata")
    info.add_argument("file_id")

    download = subparsers.add_parser("download", help="Download a binary file")
    download.add_argument("file_id")
    download.add_argument("--out", required=True)

    export = subparsers.add_parser("export", help="Export a Google-native file")
    export.add_argument("file_id")
    export.add_argument("--mime", required=True)
    export.add_argument("--out")
    export.add_argument("--text", action="store_true", help="Write output as UTF-8 text")

    cat_cmd = subparsers.add_parser("cat", help="Print a file as text")
    cat_cmd.add_argument("file_id")
    cat_cmd.add_argument("--mime", help="Export MIME type for Google-native files")
    cat_cmd.add_argument("--limit-bytes", type=int, default=200000)

    mkdir = subparsers.add_parser("mkdir", help="Create a folder")
    mkdir.add_argument("name")
    mkdir.add_argument("--parent", default="root")

    upload = subparsers.add_parser("upload", help="Upload a local file")
    upload.add_argument("path")
    upload.add_argument("--name")
    upload.add_argument("--parent", default="root")
    upload.add_argument("--mime")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    oauth_refresh_token = os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN")
    service_account_key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    if oauth_refresh_token:
        token = refresh_oauth_access_token(oauth_refresh_token)
    elif service_account_key:
        service_account = load_service_account(service_account_key)
        token = mint_access_token(service_account, args.scope, args.subject)
    else:
        raise SystemExit(
            "Set GOOGLE_OAUTH_REFRESH_TOKEN for OAuth access or GOOGLE_SERVICE_ACCOUNT_KEY for service-account access"
        )

    commands = {
        "whoami": cmd_whoami,
        "search": cmd_search,
        "ls": cmd_ls,
        "info": cmd_info,
        "download": cmd_download,
        "export": cmd_export,
        "cat": cmd_cat,
        "mkdir": cmd_mkdir,
        "upload": cmd_upload,
    }
    commands[args.command](args, token)


if __name__ == "__main__":
    main()
