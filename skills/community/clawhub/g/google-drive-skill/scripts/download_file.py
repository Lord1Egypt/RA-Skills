#!/usr/bin/env python3
"""
Download a file from Google Drive to a local path.

Usage:
    python download_file.py --file-id <FILE_ID> --dest <LOCAL_PATH>

Auth:
    GOOGLE_API_KEY              — publicly shared files
    GOOGLE_SERVICE_ACCOUNT_JSON — private / service-account files
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from drive_client import build_drive

from googleapiclient.http import MediaIoBaseDownload


def download_file(drive, file_id: str, dest_path: str) -> None:
    # Get filename if dest_path is a directory
    if os.path.isdir(dest_path):
        meta = (
            drive.files()
            .get(fileId=file_id, fields="name", supportsAllDrives=True)
            .execute()
        )
        dest_path = os.path.join(dest_path, meta["name"])

    request = drive.files().get_media(fileId=file_id, supportsAllDrives=True)
    with open(dest_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            pct = int(status.progress() * 100)
            print(f"\rDownloading... {pct}%", end="", flush=True)
    print(f"\nSaved to: {dest_path}")


def main():
    parser = argparse.ArgumentParser(description="Download a file from Google Drive")
    parser.add_argument("--file-id", required=True, help="Google Drive file ID")
    parser.add_argument(
        "--dest", required=True, help="Local destination path or directory"
    )
    args = parser.parse_args()

    drive = build_drive(readonly=True)
    download_file(drive, args.file_id, args.dest)


if __name__ == "__main__":
    main()
