#!/usr/bin/env python3
"""Google Drive CLI — Composio-powered wrapper for agent tool use.

Expects COMPOSIO_API_KEY and COMPOSIO_USER_ID env vars.
(TENANT_ID is accepted as a fallback for backward compatibility.)
Composio resolves the connected account automatically from COMPOSIO_USER_ID.
Outputs JSON to stdout.
"""

import argparse
import json
import os
import shutil
import sys
import urllib.request

from composio import Composio

# ── Composio client ───────────────────────────────────────────────────────

def _client() -> Composio:
    api_key = os.environ.get("COMPOSIO_API_KEY")
    if not api_key:
        _out({"error": "COMPOSIO_API_KEY env var required"})
        sys.exit(1)
    return Composio(api_key=api_key)


def _user_id() -> str:
    user_id = os.environ.get("COMPOSIO_USER_ID") or os.environ.get("TENANT_ID")
    if not user_id:
        _out({"error": "COMPOSIO_USER_ID env var required (any stable identifier for your Composio-connected account)"})
        sys.exit(1)
    return user_id


class GoogleDriveAPIError(Exception):
    """A Composio tool call reported successful=false."""

    def __init__(self, slug: str, detail: object):
        self.slug = slug
        self.detail = detail
        super().__init__(f"{slug} failed: {detail}")


def _execute(slug: str, arguments: dict) -> dict:
    """Execute a Composio tool. Returns the result on success.
    Raises GoogleDriveAPIError when Composio reports successful=false."""
    result = _client().tools.execute(
        slug=slug,
        arguments=arguments,
        user_id=_user_id(),
        dangerously_skip_version_check=True,
    )
    if not result.get("successful"):
        raise GoogleDriveAPIError(slug, result.get("error", "Unknown error"))
    return {"success": True, "data": result.get("data", {})}


def _out(data):
    """Print JSON output."""
    print(json.dumps(data, indent=2, default=str))


# ── File payload helpers ──────────────────────────────────────────────────
# Composio returns downloaded content as a file reference rather than inline
# bytes: either a local path the SDK already materialised, or an S3-style URL.
# `--save-to` normalises both into a file the agent can open with pandas/etc.

_FILE_REF_KEYS = ("uri", "url", "s3url", "s3_url", "path", "file_path", "local_path")


def _find_file_ref(payload: object, _depth: int = 0) -> str | None:
    """Walk a Composio response looking for a local path or download URL."""
    if _depth > 4:
        return None
    if isinstance(payload, str):
        if payload.startswith(("http://", "https://")) or os.path.exists(payload):
            return payload
        return None
    if isinstance(payload, dict):
        for key in _FILE_REF_KEYS:
            ref = _find_file_ref(payload.get(key), _depth + 1)
            if ref:
                return ref
        for key in ("file", "response_data", "data"):
            ref = _find_file_ref(payload.get(key), _depth + 1)
            if ref:
                return ref
    return None


def _save_local(payload: object, dest: str) -> str:
    """Materialise a Composio file reference at `dest`. Returns the path."""
    ref = _find_file_ref(payload)
    if not ref:
        raise GoogleDriveAPIError(
            "save", "No downloadable file reference in the Composio response"
        )
    parent = os.path.dirname(os.path.abspath(dest))
    if parent:
        os.makedirs(parent, exist_ok=True)
    if ref.startswith(("http://", "https://")):
        with urllib.request.urlopen(ref) as resp, open(dest, "wb") as fh:
            shutil.copyfileobj(resp, fh)
    else:
        shutil.copyfile(ref, dest)
    return dest


def _emit(result: dict, save_to: str | None) -> None:
    """Print a tool result, first saving its file payload when asked."""
    if save_to:
        result["saved_to"] = _save_local(result.get("data", {}), save_to)
    _out(result)


# ── Discovery Commands ────────────────────────────────────────────────────

def cmd_list(args):
    arguments: dict = {"folderId": args.folder_id}
    if args.page_size:
        arguments["pageSize"] = args.page_size
    if args.page_token:
        arguments["pageToken"] = args.page_token
    if args.order_by:
        arguments["orderBy"] = args.order_by
    if args.all_drives:
        arguments["supportsAllDrives"] = True
        arguments["includeItemsFromAllDrives"] = True
    _out(_execute("GOOGLEDRIVE_LIST_FILES", arguments))


def cmd_search(args):
    clauses: list[str] = []
    if args.query:
        clauses.append(args.query)
    if args.name_contains:
        escaped = args.name_contains.replace("'", "\\'")
        clauses.append(f"name contains '{escaped}'")
    if args.mime_type:
        clauses.append(f"mimeType = '{args.mime_type}'")
    if not args.include_trashed:
        clauses.append("trashed = false")

    arguments: dict = {}
    if clauses:
        arguments["q"] = " and ".join(clauses)
    if args.folder_id:
        arguments["folder_id"] = args.folder_id
    if args.page_size:
        arguments["pageSize"] = args.page_size
    if args.page_token:
        arguments["pageToken"] = args.page_token
    if args.order_by:
        arguments["orderBy"] = args.order_by
    if args.all_drives:
        arguments["supportsAllDrives"] = True
        arguments["includeItemsFromAllDrives"] = True
    _out(_execute("GOOGLEDRIVE_FIND_FILE", arguments))


def cmd_find_folder(args):
    arguments: dict = {}
    if args.name:
        arguments["name_exact"] = args.name
    if args.name_contains:
        arguments["name_contains"] = args.name_contains
    if args.parent_id:
        arguments["parent_folder_id"] = args.parent_id
    if args.modified_after:
        arguments["modified_after"] = args.modified_after
    if not arguments:
        _out({"error": "Specify at least one of --name, --name-contains, --parent-id"})
        sys.exit(1)
    _out(_execute("GOOGLEDRIVE_FIND_FOLDER", arguments))


def cmd_shared_drives(args):
    arguments: dict = {}
    if args.page_size:
        arguments["pageSize"] = args.page_size
    if args.page_token:
        arguments["pageToken"] = args.page_token
    _out(_execute("GOOGLEDRIVE_LIST_SHARED_DRIVES", arguments))


# ── Metadata Commands ─────────────────────────────────────────────────────

def cmd_info(args):
    arguments: dict = {"fileId": args.file_id}
    if args.fields:
        arguments["fields"] = args.fields
    if args.all_drives:
        arguments["supportsAllDrives"] = True
    _out(_execute("GOOGLEDRIVE_GET_FILE_METADATA", arguments))


def cmd_permissions(args):
    _out(_execute("GOOGLEDRIVE_LIST_PERMISSIONS", {"fileId": args.file_id}))


# ── Read / Download Commands ──────────────────────────────────────────────

def cmd_download(args):
    arguments: dict = {"fileId": args.file_id}
    if args.mime_type:
        arguments["mime_type"] = args.mime_type
    _emit(_execute("GOOGLEDRIVE_DOWNLOAD_FILE", arguments), args.save_to)


def cmd_export(args):
    _emit(
        _execute("GOOGLEDRIVE_EXPORT_GOOGLE_WORKSPACE_FILE", {
            "fileId": args.file_id,
            "mimeType": args.mime_type,
        }),
        args.save_to,
    )


# ── Write Commands ────────────────────────────────────────────────────────

def cmd_create_folder(args):
    arguments: dict = {"name": args.name}
    if args.parent_id:
        arguments["parent_id"] = args.parent_id
    _out(_execute("GOOGLEDRIVE_CREATE_FOLDER", arguments))


def cmd_create_file(args):
    text = args.text
    if args.from_file:
        with open(args.from_file, encoding="utf-8") as fh:
            text = fh.read()
    if text is None:
        _out({"error": "Specify --text or --from-file"})
        sys.exit(1)
    arguments: dict = {"file_name": args.name, "text_content": text}
    if args.parent_id:
        arguments["parent_id"] = args.parent_id
    if args.mime_type:
        arguments["mime_type"] = args.mime_type
    _out(_execute("GOOGLEDRIVE_CREATE_FILE_FROM_TEXT", arguments))


def cmd_update_file(args):
    arguments: dict = {"fileId": args.file_id}
    if args.name:
        arguments["name"] = args.name
    if args.description:
        arguments["description"] = args.description
    if len(arguments) == 1:
        _out({"error": "Specify at least one of --name, --description"})
        sys.exit(1)
    _out(_execute("GOOGLEDRIVE_UPDATE_FILE", arguments))


def cmd_move(args):
    _out(_execute("GOOGLEDRIVE_MOVE_FILE", {
        "file_id": args.file_id,
        "new_parents": [p.strip() for p in args.to_folder_id.split(",")],
    }))


def cmd_copy(args):
    arguments: dict = {"fileId": args.file_id}
    if args.name:
        arguments["name"] = args.name
    if args.to_folder_id:
        arguments["parents"] = [p.strip() for p in args.to_folder_id.split(",")]
    _out(_execute("GOOGLEDRIVE_COPY_FILE_ADVANCED", arguments))


def cmd_trash(args):
    _out(_execute("GOOGLEDRIVE_TRASH_FILE", {"fileId": args.file_id}))


def cmd_share(args):
    arguments: dict = {
        "file_id": args.file_id,
        "role": args.role,
        "type": args.type,
    }
    if args.email:
        arguments["email_address"] = args.email
    if args.domain:
        arguments["domain"] = args.domain
    _out(_execute("GOOGLEDRIVE_CREATE_PERMISSION", arguments))


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Google Drive CLI (Composio)")
    sub = parser.add_subparsers(dest="command", required=True)

    # ── Discovery ─────────────────────────────────────────────────────────
    p = sub.add_parser("list", help="List files in a folder")
    p.add_argument("--folder-id", default="root", help="Folder ID (default: root)")
    p.add_argument("--page-size", type=int, help="Max items to return")
    p.add_argument("--page-token", help="Token from a previous page")
    p.add_argument("--order-by", help="e.g. 'modifiedTime desc', 'name'")
    p.add_argument("--all-drives", action="store_true", help="Include shared drives")

    p = sub.add_parser("search", help="Search files by name, type, or raw query")
    p.add_argument("--query", help="Raw Drive query, e.g. \"name contains 'sales'\"")
    p.add_argument("--name-contains", help="Substring of the file name")
    p.add_argument("--mime-type", help="e.g. text/csv, application/vnd.google-apps.folder")
    p.add_argument("--folder-id", help="Restrict to files inside this folder")
    p.add_argument("--page-size", type=int)
    p.add_argument("--page-token")
    p.add_argument("--order-by", help="e.g. 'modifiedTime desc'")
    p.add_argument("--include-trashed", action="store_true")
    p.add_argument("--all-drives", action="store_true", help="Include shared drives")

    p = sub.add_parser("find-folder", help="Find folders by name or parent")
    p.add_argument("--name", help="Exact folder name")
    p.add_argument("--name-contains", help="Substring of the folder name")
    p.add_argument("--parent-id", help="Parent folder ID")
    p.add_argument("--modified-after", help="RFC 3339 timestamp")

    p = sub.add_parser("shared-drives", help="List accessible shared drives")
    p.add_argument("--page-size", type=int)
    p.add_argument("--page-token")

    # ── Metadata ──────────────────────────────────────────────────────────
    p = sub.add_parser("info", help="Get file or folder metadata")
    p.add_argument("--file-id", required=True)
    p.add_argument("--fields", help="Comma-separated Drive fields to return")
    p.add_argument("--all-drives", action="store_true")

    p = sub.add_parser("permissions", help="List who has access to a file")
    p.add_argument("--file-id", required=True)

    # ── Read ──────────────────────────────────────────────────────────────
    p = sub.add_parser("download", help="Download a file's content")
    p.add_argument("--file-id", required=True)
    p.add_argument("--mime-type", help="Export MIME type for Google-native files")
    p.add_argument("--save-to", help="Local path to write the file to")

    p = sub.add_parser("export", help="Export a Google Doc/Sheet/Slide to a format")
    p.add_argument("--file-id", required=True)
    p.add_argument("--mime-type", required=True, help="e.g. text/csv, application/pdf")
    p.add_argument("--save-to", help="Local path to write the file to")

    # ── Write ─────────────────────────────────────────────────────────────
    p = sub.add_parser("create-folder", help="Create a folder")
    p.add_argument("--name", required=True)
    p.add_argument("--parent-id", help="Parent folder ID (default: My Drive root)")

    p = sub.add_parser("create-file", help="Create a text file (CSV, TXT, MD, ...)")
    p.add_argument("--name", required=True, help="File name including extension")
    p.add_argument("--text", help="File content")
    p.add_argument("--from-file", help="Read content from a local file instead")
    p.add_argument("--parent-id", help="Destination folder ID")
    p.add_argument("--mime-type", help="e.g. text/csv (default: text/plain)")

    p = sub.add_parser("update-file", help="Rename or re-describe a file")
    p.add_argument("--file-id", required=True)
    p.add_argument("--name", help="New name")
    p.add_argument("--description", help="New description")

    p = sub.add_parser("move", help="Move a file to another folder")
    p.add_argument("--file-id", required=True)
    p.add_argument("--to-folder-id", required=True, help="Comma-separated folder IDs")

    p = sub.add_parser("copy", help="Copy a file")
    p.add_argument("--file-id", required=True)
    p.add_argument("--name", help="Name for the copy")
    p.add_argument("--to-folder-id", help="Comma-separated destination folder IDs")

    p = sub.add_parser("trash", help="Move a file to the trash (soft delete)")
    p.add_argument("--file-id", required=True)

    p = sub.add_parser("share", help="Grant access to a file or folder")
    p.add_argument("--file-id", required=True)
    p.add_argument("--role", required=True, help="reader, commenter, writer, owner")
    p.add_argument("--type", required=True, help="user, group, domain, anyone")
    p.add_argument("--email", help="Email address for type=user or type=group")
    p.add_argument("--domain", help="Domain for type=domain")

    args = parser.parse_args()

    commands = {
        "list": cmd_list,
        "search": cmd_search,
        "find-folder": cmd_find_folder,
        "shared-drives": cmd_shared_drives,
        "info": cmd_info,
        "permissions": cmd_permissions,
        "download": cmd_download,
        "export": cmd_export,
        "create-folder": cmd_create_folder,
        "create-file": cmd_create_file,
        "update-file": cmd_update_file,
        "move": cmd_move,
        "copy": cmd_copy,
        "trash": cmd_trash,
        "share": cmd_share,
    }

    try:
        commands[args.command](args)
    except GoogleDriveAPIError as e:
        _out({"success": False, "error": str(e.detail), "slug": e.slug})
        sys.exit(1)
    except json.JSONDecodeError as e:
        _out({"error": f"Invalid JSON input: {e}"})
        sys.exit(1)
    except Exception as e:
        _out({"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
