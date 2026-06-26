#!/usr/bin/env python3
"""Compatibility entry point for the Gmail attachment downloader skill."""

from scripts.download_gmail_attachments import main


if __name__ == "__main__":
    raise SystemExit(main())
