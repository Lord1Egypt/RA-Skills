#!/usr/bin/env python3
"""
TikTok Video — Shoppable Video Large File Upload (workflow guide)

MRD: https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d
Detail: references/large-file-upload.md

Usage:
  python large_file_upload.py
  python large_file_upload.py --help
"""

from __future__ import annotations

import sys


def main() -> None:
    print(
        "Shoppable Video Large File Upload Solution (> 10MB)\n"
        "====================================================\n"
        "\n"
        "Step 1  Initialize Upload\n"
        "        POST open/{version}/file/init\n"
        "        → upload_url, upload_token\n"
        "        Script: large_file_upload_init.py (not callable yet — open/ not whitelisted)\n"
        "\n"
        "Step 2  Upload Chunks & Merge\n"
        "        PUT binary chunks to upload_url (direct to file gateway, NOT LinkFox proxy)\n"
        "        Headers: Content-Range, Content-Length, Content-Type\n"
        "        Upload chunks sequentially.\n"
        "\n"
        "Step 3  Bind Business Resource\n"
        "        POST open/{version}/file/bind (path confirm in Lark doc)\n"
        "        → video_file.id (use as file_id in post/precheck)\n"
        "        Script: large_file_upload_bind.py (not callable yet)\n"
        "\n"
        "Docs:\n"
        "  references/large-file-upload.md\n"
        "  https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d\n"
        "\n"
        "For files ≤ 10MB, see upload_shoppable_video_file (§4 api.md).\n",
        file=sys.stderr,
    )
    sys.exit(0 if "--help" in sys.argv or "-h" in sys.argv else 0)


if __name__ == "__main__":
    main()
