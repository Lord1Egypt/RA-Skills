#!/usr/bin/env python3
"""Manage OneDrive files via Microsoft Graph."""
import argparse
import json
from pathlib import Path

import requests

from utils import append_log, authorized_request, graph_url, cli_main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Basic OneDrive operations via Microsoft Graph.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List files/folders.")
    p_list.add_argument("--path", default="/", help="Remote path (example: /Documents)")
    p_list.add_argument("--top", type=int, default=50)

    p_upload = sub.add_parser("upload", help="Upload a file.")
    p_upload.add_argument("--local", required=True, type=Path)
    p_upload.add_argument("--remote", required=True, help="OneDrive destination path (/Documents/file.ext)")

    p_download = sub.add_parser("download", help="Download a file.")
    p_download.add_argument("--item-id", help="Drive item ID")
    p_download.add_argument("--remote", help="Remote path (used when --item-id is not provided)")
    p_download.add_argument("--local", type=Path, required=True)

    p_move = sub.add_parser("move", help="Move item to another folder.")
    p_move.add_argument("item_id")
    p_move.add_argument("--dest", required=True, help="Destination folder ID or path")

    p_share = sub.add_parser("share", help="Generate sharing link.")
    p_share.add_argument("item_id")
    p_share.add_argument("--scope", choices=["anonymous", "organization"], default="organization")
    p_share.add_argument("--type", choices=["view", "edit"], default="view")

    return parser


def _normalize_remote_path(path: str) -> str:
    normalized = (path or "/").strip()
    if not normalized:
        return "/"
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    if normalized != "/":
        normalized = normalized.rstrip("/")
    return normalized


def _split_remote_path(path: str) -> tuple[str, str]:
    normalized = _normalize_remote_path(path)
    if normalized == "/":
        return "", ""
    parts = normalized.lstrip("/").split("/", 1)
    head = parts[0]
    tail = parts[1] if len(parts) > 1 else ""
    return head, tail


def _slug(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def _resolve_special_folder_id(head_segment: str) -> str | None:
    target = _slug(head_segment)
    if not target:
        return None
    # /me/drive/special can be empty in some personal tenants; inspect root children as fallback.
    resp = authorized_request("GET", graph_url("/me/drive/root/children"))
    for item in resp.json().get("value", []):
        display_name = _slug(item.get("name", ""))
        special_name = _slug(item.get("specialFolder", {}).get("name", ""))
        if target in {display_name, special_name}:
            return item.get("id")
    return None


def resolve_remote_item(remote: str) -> dict:
    normalized = _normalize_remote_path(remote)
    if normalized == "/":
        return authorized_request("GET", graph_url("/me/drive/root")).json()
    try:
        return authorized_request("GET", graph_url(f"/me/drive/root:{normalized}")).json()
    except requests.HTTPError as exc:
        if exc.response is None or exc.response.status_code != 404:
            raise
        head, tail = _split_remote_path(normalized)
        special_id = _resolve_special_folder_id(head)
        if not special_id:
            raise
        if tail:
            return authorized_request("GET", graph_url(f"/me/drive/items/{special_id}:/{tail}")).json()
        return authorized_request("GET", graph_url(f"/me/drive/items/{special_id}")).json()


def list_items(path: str, top: int) -> None:
    normalized = _normalize_remote_path(path)
    if normalized == "/":
        url = graph_url("/me/drive/root/children")
    else:
        item = resolve_remote_item(normalized)
        url = graph_url(f"/me/drive/items/{item['id']}/children")
    resp = authorized_request("GET", url, params={"$top": top})
    data = resp.json()
    append_log({"action": "drive_list", "path": path, "count": len(data.get("value", []))})
    print(json.dumps(data, indent=2))


def upload_file(local: Path, remote: str) -> None:
    content = local.read_bytes()
    remote_path = _normalize_remote_path(remote)
    parent_path, _, file_name = remote_path.rpartition("/")
    if not file_name:
        raise SystemExit("Remote destination must include a file name.")
    parent_path = parent_path or "/"
    if parent_path == "/":
        url = graph_url(f"/me/drive/root:/{file_name}:/content")
    else:
        parent_item = resolve_remote_item(parent_path)
        url = graph_url(f"/me/drive/items/{parent_item['id']}:/{file_name}:/content")
    resp = authorized_request("PUT", url, data=content, headers={"Content-Type": "application/octet-stream"})
    append_log({"action": "drive_upload", "name": local.name, "remote": remote})
    print(json.dumps(resp.json(), indent=2))


def resolve_item_path(remote: str) -> str:
    return resolve_remote_item(remote)["id"]


def download_file(item_id: str, remote: str, local: Path) -> None:
    if not item_id:
        if not remote:
            raise SystemExit("Provide --item-id or --remote.")
        item_id = resolve_item_path(remote)
    metadata = authorized_request("GET", graph_url(f"/me/drive/items/{item_id}"))
    download_url = metadata.json()["@microsoft.graph.downloadUrl"]
    resp = authorized_request("GET", download_url)
    local.write_bytes(resp.content)
    append_log({"action": "drive_download", "item": item_id, "local": str(local)})
    print(f"File saved to {local}")


def move_item(item_id: str, dest: str) -> None:
    payload = {}
    if dest.startswith("/"):
        payload["parentReference"] = {"id": resolve_item_path(dest)}
    else:
        payload["parentReference"] = {"id": dest}
    resp = authorized_request("PATCH", graph_url(f"/me/drive/items/{item_id}"), json=payload)
    append_log({"action": "drive_move", "item": item_id, "dest": dest})
    print(json.dumps(resp.json(), indent=2))


def share_item(item_id: str, scope: str, link_type: str) -> None:
    resp = authorized_request(
        "POST",
        graph_url(f"/me/drive/items/{item_id}/createLink"),
        json={"type": link_type, "scope": scope},
    )
    append_log({"action": "drive_share", "item": item_id, "scope": scope, "type": link_type})
    print(json.dumps(resp.json(), indent=2))


def handler():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "list":
        list_items(args.path, args.top)
    elif args.command == "upload":
        upload_file(args.local, args.remote)
    elif args.command == "download":
        download_file(args.item_id, args.remote, args.local)
    elif args.command == "move":
        move_item(args.item_id, args.dest)
    elif args.command == "share":
        share_item(args.item_id, args.scope, args.type)


if __name__ == "__main__":
    cli_main(handler)
