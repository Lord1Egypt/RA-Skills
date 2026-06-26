#!/usr/bin/env python3
"""Google Drive API — search and read files via domain-wide delegation."""

import argparse
import json
import sys
from typing import Optional

from auth import get_service


def search_files(
    user: str,
    query: str,
    max_results: int = 20,
    order_by: str = "modifiedTime desc",
) -> dict:
    """Search a user's Drive files.

    Args:
        user: Email address (impersonated via DWD).
        query: Drive search query (name contains, mimeType, modifiedTime, etc).
        max_results: Max files to return.
        order_by: Sort order.

    Returns:
        Dict with file list.
    """
    service = get_service("drive", impersonate=user)
    results = service.files().list(
        q=query,
        pageSize=max_results,
        orderBy=order_by,
        fields="files(id,name,mimeType,size,createdTime,modifiedTime,owners,shared,sharingUser,webViewLink,parents)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()

    files = results.get("files", [])

    return {
        "user": user,
        "query": query,
        "total": len(files),
        "files": [_parse_file(f) for f in files],
    }


def list_recent(
    user: str,
    max_results: int = 10,
) -> dict:
    """List a user's recently modified files.

    Args:
        user: Email address.
        max_results: Max files to return.

    Returns:
        Dict with recent files.
    """
    return search_files(user, query="trashed=false", max_results=max_results)


def get_file_metadata(
    user: str,
    file_id: str,
) -> dict:
    """Get detailed metadata for a specific file.

    Args:
        user: Email address.
        file_id: Drive file ID.

    Returns:
        File metadata dict.
    """
    service = get_service("drive", impersonate=user)
    f = service.files().get(
        fileId=file_id,
        fields="id,name,mimeType,size,createdTime,modifiedTime,owners,shared,sharingUser,webViewLink,parents,permissions,description",
        supportsAllDrives=True,
    ).execute()

    result = _parse_file(f)
    # Add permissions detail
    perms = f.get("permissions", [])
    result["permissions"] = [
        {
            "email": p.get("emailAddress", ""),
            "role": p.get("role", ""),
            "type": p.get("type", ""),
            "display_name": p.get("displayName", ""),
        }
        for p in perms
    ]
    result["description"] = f.get("description", "")
    return result


def list_shared_externally(
    user: str,
    max_results: int = 20,
) -> dict:
    """Find files shared outside the organization.

    Args:
        user: Email address.
        max_results: Max files to return.

    Returns:
        Dict with externally shared files.
    """
    # visibility = 'anyoneWithLink' or 'anyoneCanFind' catches external shares
    return search_files(
        user,
        query="visibility='anyoneWithLink' or visibility='anyoneCanFind'",
        max_results=max_results,
    )


def search_by_type(
    user: str,
    file_type: str,
    max_results: int = 20,
) -> dict:
    """Search files by type.

    Args:
        user: Email address.
        file_type: Type shorthand — 'doc', 'sheet', 'slide', 'pdf', 'image', 'folder'.
        max_results: Max files to return.

    Returns:
        Dict with matching files.
    """
    mime_map = {
        "doc": "application/vnd.google-apps.document",
        "sheet": "application/vnd.google-apps.spreadsheet",
        "slide": "application/vnd.google-apps.presentation",
        "pdf": "application/pdf",
        "image": "image/",
        "folder": "application/vnd.google-apps.folder",
    }

    mime = mime_map.get(file_type)
    if not mime:
        return {"error": f"Unknown file type: {file_type}. Valid: {', '.join(mime_map.keys())}"}

    if file_type == "image":
        query = f"mimeType contains '{mime}' and trashed=false"
    else:
        query = f"mimeType='{mime}' and trashed=false"

    return search_files(user, query=query, max_results=max_results)


def _parse_file(f: dict) -> dict:
    """Parse a Drive file into a clean dict."""
    owners = f.get("owners", [])
    owner_emails = [o.get("emailAddress", "") for o in owners]

    return {
        "id": f.get("id", ""),
        "name": f.get("name", ""),
        "mime_type": f.get("mimeType", ""),
        "size_bytes": int(f.get("size", 0)) if f.get("size") else None,
        "created": f.get("createdTime", ""),
        "modified": f.get("modifiedTime", ""),
        "owners": owner_emails,
        "shared": f.get("shared", False),
        "link": f.get("webViewLink", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Google Drive search and read")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search files")
    p_search.add_argument("--user", required=True, help="Email address")
    p_search.add_argument("--query", required=True, help="Drive query")
    p_search.add_argument("--max", type=int, default=20)

    # recent
    p_recent = sub.add_parser("recent", help="Recent files")
    p_recent.add_argument("--user", required=True)
    p_recent.add_argument("--max", type=int, default=10)

    # file
    p_file = sub.add_parser("file", help="Get file metadata")
    p_file.add_argument("--user", required=True)
    p_file.add_argument("--id", required=True, help="File ID")

    # shared
    p_shared = sub.add_parser("shared", help="Files shared externally")
    p_shared.add_argument("--user", required=True)
    p_shared.add_argument("--max", type=int, default=20)

    # type
    p_type = sub.add_parser("type", help="Search by file type")
    p_type.add_argument("--user", required=True)
    p_type.add_argument("--type", required=True, choices=["doc", "sheet", "slide", "pdf", "image", "folder"])
    p_type.add_argument("--max", type=int, default=20)

    args = parser.parse_args()

    try:
        if args.command == "search":
            result = search_files(args.user, args.query, args.max)
        elif args.command == "recent":
            result = list_recent(args.user, args.max)
        elif args.command == "file":
            result = get_file_metadata(args.user, args.id)
        elif args.command == "shared":
            result = list_shared_externally(args.user, args.max)
        elif args.command == "type":
            result = search_by_type(args.user, args.type, args.max)
        else:
            result = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
