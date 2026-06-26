#!/usr/bin/env python3
"""
Delete or trash a file / folder in Google Drive.

Usage:
    # Move to trash (safe, recoverable):
    python delete_file.py --file-id <FILE_ID>

    # Permanently delete (irreversible):
    python delete_file.py --file-id <FILE_ID> --permanent

    # Skip confirmation prompt:
    python delete_file.py --file-id <FILE_ID> --permanent --yes

Warning:
    Permanently deleting a folder also deletes ALL its children.

Auth:
    GOOGLE_SERVICE_ACCOUNT_JSON — required (write operation)
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from drive_client import build_drive

from googleapiclient.errors import HttpError


def trash_file(drive, file_id: str) -> None:
    drive.files().update(
        fileId=file_id, body={"trashed": True}, supportsAllDrives=True
    ).execute()


def delete_file_permanent(drive, file_id: str) -> bool:
    try:
        drive.files().delete(fileId=file_id, supportsAllDrives=True).execute()
        return True
    except HttpError as e:
        if e.resp.status == 404:
            return False
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Delete or trash a Google Drive file/folder"
    )
    parser.add_argument("--file-id", required=True, help="Google Drive file/folder ID")
    parser.add_argument(
        "--permanent",
        action="store_true",
        help="Permanently delete instead of moving to trash",
    )
    parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation prompt"
    )
    args = parser.parse_args()

    if args.permanent and not args.yes:
        confirm = input(
            f"Permanently delete {args.file_id}? This cannot be undone. [y/N] "
        ).strip().lower()
        if confirm != "y":
            print("Aborted.")
            sys.exit(0)

    drive = build_drive(readonly=False)

    if args.permanent:
        found = delete_file_permanent(drive, args.file_id)
        if found:
            print(f"Permanently deleted: {args.file_id}")
        else:
            print(f"Not found (already deleted?): {args.file_id}")
    else:
        trash_file(drive, args.file_id)
        print(f"Moved to trash: {args.file_id}")


if __name__ == "__main__":
    main()
