#!/usr/bin/env python3
"""
Upload a local file to Google Drive.

Usage:
    # Upload from local path:
    python upload_file.py --src <LOCAL_PATH> [--name <DRIVE_NAME>] [--parent-id <FOLDER_ID>] [--mime <MIME_TYPE>]

    # Make newly uploaded file public (anyone with link can read):
    python upload_file.py --src photo.png --parent-id <ID> --make-public

Output:
    Prints the new file ID.

Auth:
    GOOGLE_SERVICE_ACCOUNT_JSON — required (write operation)
"""

import argparse
import mimetypes
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from drive_client import build_drive

from googleapiclient.http import MediaFileUpload


def upload_file(
    drive,
    local_path: str,
    name: str,
    parent_id: str | None = None,
    mime_type: str | None = None,
) -> str:
    if not mime_type:
        guessed, _ = mimetypes.guess_type(local_path)
        mime_type = guessed or "application/octet-stream"

    metadata: dict = {"name": name}
    if parent_id:
        metadata["parents"] = [parent_id]

    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
    file = (
        drive.files()
        .create(body=metadata, media_body=media, fields="id", supportsAllDrives=True)
        .execute()
    )
    return file["id"]


def make_public(drive, file_id: str) -> None:
    drive.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
        supportsAllDrives=True,
    ).execute()


def main():
    parser = argparse.ArgumentParser(description="Upload a file to Google Drive")
    parser.add_argument("--src", required=True, help="Local file path to upload")
    parser.add_argument("--name", default=None, help="Name on Drive (default: filename)")
    parser.add_argument("--parent-id", default=None, help="Parent folder ID")
    parser.add_argument("--mime", default=None, help="MIME type (auto-detected if omitted)")
    parser.add_argument(
        "--make-public",
        action="store_true",
        help="Make the uploaded file publicly readable",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.src):
        sys.exit(f"File not found: {args.src}")

    drive_name = args.name or os.path.basename(args.src)
    drive = build_drive(readonly=False)
    file_id = upload_file(drive, args.src, drive_name, args.parent_id, args.mime)
    print(f"Uploaded '{drive_name}'")
    print(f"File ID: {file_id}")

    if args.make_public:
        make_public(drive, file_id)
        print("Visibility: public (anyone with the link can read)")


if __name__ == "__main__":
    main()
