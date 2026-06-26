#!/usr/bin/env python3
"""
Update a Google Drive file — rename, move, or replace content.

Usage:
    # Rename:
    python update_file.py --file-id <ID> --name <NEW_NAME>

    # Move to a different folder:
    python update_file.py --file-id <ID> --move-to <NEW_PARENT_ID> --old-parent <OLD_PARENT_ID>

    # Replace file content:
    python update_file.py --file-id <ID> --src <LOCAL_PATH> [--mime <MIME_TYPE>]

    # Combine rename + content update:
    python update_file.py --file-id <ID> --name <NEW_NAME> --src <LOCAL_PATH>

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


def main():
    parser = argparse.ArgumentParser(description="Update a Google Drive file")
    parser.add_argument("--file-id", required=True, help="ID of the file to update")
    parser.add_argument("--name", default=None, help="New file name (rename)")
    parser.add_argument("--move-to", default=None, help="New parent folder ID (move)")
    parser.add_argument(
        "--old-parent",
        default=None,
        help="Current parent folder ID (required when --move-to is used)",
    )
    parser.add_argument("--src", default=None, help="Local file to replace content with")
    parser.add_argument("--mime", default=None, help="MIME type for content update")
    args = parser.parse_args()

    if args.move_to and not args.old_parent:
        sys.exit("--old-parent is required when using --move-to")
    if not any([args.name, args.move_to, args.src]):
        sys.exit("Specify at least one of: --name, --move-to, --src")

    drive = build_drive(readonly=False)
    file_id = args.file_id

    # Build metadata update body
    body: dict = {}
    if args.name:
        body["name"] = args.name

    # Prepare media if replacing content
    media = None
    if args.src:
        if not os.path.isfile(args.src):
            sys.exit(f"File not found: {args.src}")
        mime_type = args.mime or mimetypes.guess_type(args.src)[0] or "application/octet-stream"
        media = MediaFileUpload(args.src, mimetype=mime_type, resumable=True)

    # Prepare kwargs
    kwargs: dict = dict(
        fileId=file_id,
        body=body,
        fields="id, name",
        supportsAllDrives=True,
    )
    if args.move_to:
        kwargs["addParents"] = args.move_to
        kwargs["removeParents"] = args.old_parent
    if media:
        kwargs["media_body"] = media

    result = drive.files().update(**kwargs).execute()

    if args.name:
        print(f"Renamed to: {result.get('name', args.name)}")
    if args.move_to:
        print(f"Moved to folder: {args.move_to}")
    if args.src:
        print(f"Content replaced from: {args.src}")
    print(f"File ID: {file_id}")


if __name__ == "__main__":
    main()
