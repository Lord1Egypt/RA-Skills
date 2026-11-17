#!/usr/bin/env python3
"""
TikTok Video — large_file_upload_init (Large File Upload Step 1: Initialize)
MRD: https://bytedance.sg.larkoffice.com/docx/WTMvdfbTBo30Fex0r9YlYstGg0d

POST open/{version}/file/init → upload_url + upload_token

⚠️ Path prefix open/ not in developer-proxy whitelist yet; not callable via gateway.
See references/large-file-upload.md
"""

from __future__ import annotations

import json
import sys

from _video_api_runner import run_video_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: large_file_upload_init.py '<JSON>'\n"
            "Example body fields: file_size, chunk_size, file_name, content_type\n"
            "See references/large-file-upload.md — Step 1",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_video_api("large_file_upload_init", params, "large_file_upload_init.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
