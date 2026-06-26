#!/usr/bin/env python3
"""
Manage permissions on a Google Drive file or folder.

Usage:
    # Make public (anyone with link can read):
    python set_permissions.py --file-id <ID> --public

    # Share with a specific user:
    python set_permissions.py --file-id <ID> --email user@example.com [--role writer]

    # List current permissions:
    python set_permissions.py --file-id <ID> --list

    # Remove a permission by permission ID:
    python set_permissions.py --file-id <ID> --remove <PERMISSION_ID>

Roles: reader | commenter | writer | fileOrganizer | organizer | owner

Auth:
    GOOGLE_SERVICE_ACCOUNT_JSON — required (write operation)
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from drive_client import build_drive


def list_permissions(drive, file_id: str) -> list[dict]:
    resp = drive.permissions().list(
        fileId=file_id,
        fields="permissions(id, role, type, emailAddress, displayName)",
        supportsAllDrives=True,
    ).execute()
    return resp.get("permissions", [])


def make_public(drive, file_id: str) -> str:
    result = drive.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return result["id"]


def share_with_user(
    drive, file_id: str, email: str, role: str = "writer"
) -> str:
    result = drive.permissions().create(
        fileId=file_id,
        body={"role": role, "type": "user", "emailAddress": email},
        sendNotificationEmail=False,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return result["id"]


def remove_permission(drive, file_id: str, permission_id: str) -> None:
    drive.permissions().delete(
        fileId=file_id,
        permissionId=permission_id,
        supportsAllDrives=True,
    ).execute()


def main():
    parser = argparse.ArgumentParser(
        description="Manage Google Drive file/folder permissions"
    )
    parser.add_argument("--file-id", required=True, help="Google Drive file/folder ID")

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--public", action="store_true", help="Make file readable by anyone with link"
    )
    action.add_argument("--email", default=None, help="Share with a specific user email")
    action.add_argument(
        "--list", action="store_true", dest="list_perms", help="List current permissions"
    )
    action.add_argument(
        "--remove", default=None, metavar="PERMISSION_ID", help="Remove a permission by ID"
    )

    parser.add_argument(
        "--role",
        default="writer",
        choices=["reader", "commenter", "writer", "fileOrganizer", "organizer"],
        help="Role for --email (default: writer)",
    )
    args = parser.parse_args()

    drive = build_drive(readonly=False)
    file_id = args.file_id

    if args.list_perms:
        perms = list_permissions(drive, file_id)
        print(json.dumps(perms, indent=2))

    elif args.public:
        perm_id = make_public(drive, file_id)
        print("Made public (reader, anyone with link)")
        print(f"Permission ID: {perm_id}")

    elif args.email:
        perm_id = share_with_user(drive, file_id, args.email, args.role)
        print(f"Shared with {args.email} as {args.role}")
        print(f"Permission ID: {perm_id}")

    elif args.remove:
        remove_permission(drive, file_id, args.remove)
        print(f"Removed permission: {args.remove}")


if __name__ == "__main__":
    main()
