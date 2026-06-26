#!/usr/bin/env python3
"""
List files and folders inside a Google Drive folder.

Usage:
    python list_files.py --folder-id <FOLDER_ID> [--json]

Output:
    Tab-separated table  (default)  or JSON array (--json)

Auth:
    GOOGLE_API_KEY              — public folders (read-only)
    GOOGLE_SERVICE_ACCOUNT_JSON — service-account owned folders
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from drive_client import build_drive


def list_files(drive, folder_id: str) -> list[dict]:
    results = []
    page_token = None
    while True:
        resp = (
            drive.files()
            .list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        results.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return results


def main():
    parser = argparse.ArgumentParser(description="List files in a Google Drive folder")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder ID")
    parser.add_argument(
        "--json", action="store_true", dest="as_json", help="Output as JSON"
    )
    args = parser.parse_args()

    drive = build_drive(readonly=True)
    files = list_files(drive, args.folder_id)

    if args.as_json:
        print(json.dumps(files, indent=2))
    else:
        print(f"{'ID':<45} {'MIME TYPE':<45} {'SIZE':>10}  NAME")
        print("-" * 120)
        for f in files:
            size = f.get("size", "-")
            print(f"{f['id']:<45} {f['mimeType']:<45} {size:>10}  {f['name']}")
        print(f"\n{len(files)} item(s) found.")


if __name__ == "__main__":
    main()
