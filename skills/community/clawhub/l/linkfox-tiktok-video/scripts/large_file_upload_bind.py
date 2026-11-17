#!/usr/bin/env python3
"""
TikTok Video — large_file_upload_bind (Large File Upload Step 3: Bind Business Resource)
MRD: https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d

POST open/{version}/file/bind → video_file.id (file_id)

⚠️ Path prefix open/ not in developer-proxy whitelist yet; confirm bind path in Lark doc.
See references/large-file-upload.md
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: large_file_upload_bind.py '<JSON>'\n"
            "Required: upload_token (from Step 1)\n"
            "See references/large-file-upload.md — Step 3",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api("large_file_upload_bind", params, "large_file_upload_bind.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
