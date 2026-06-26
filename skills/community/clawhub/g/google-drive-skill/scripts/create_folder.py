#!/usr/bin/env python3
"""
Create a folder in Google Drive.

Usage:
    python create_folder.py --name <FOLDER_NAME> [--parent-id <PARENT_FOLDER_ID>]

Output:
    Prints the new folder ID.

Auth:
    GOOGLE_SERVICE_ACCOUNT_JSON — required (write operation)
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from drive_client import build_drive


def create_folder(drive, name: str, parent_id: str | None = None) -> str:
    metadata: dict = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = (
        drive.files()
        .create(body=metadata, fields="id, name", supportsAllDrives=True)
        .execute()
    )
    return folder["id"]


def main():
    parser = argparse.ArgumentParser(description="Create a folder in Google Drive")
    parser.add_argument("--name", required=True, help="Folder name")
    parser.add_argument(
        "--parent-id", default=None, help="Parent folder ID (root if omitted)"
    )
    args = parser.parse_args()

    drive = build_drive(readonly=False)
    folder_id = create_folder(drive, args.name, args.parent_id)
    print(f"Created folder '{args.name}'")
    print(f"Folder ID: {folder_id}")


if __name__ == "__main__":
    main()
