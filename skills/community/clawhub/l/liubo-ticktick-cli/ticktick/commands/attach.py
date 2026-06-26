import json
import secrets
import sys
from pathlib import Path

import requests

from ..api import api
from ..auth import load_config
from ..util import is_task_id


def _get_session_config() -> tuple[str, str]:
    config = load_config()
    if not config or not config.get("sessionCookie"):
        raise RuntimeError(
            "sessionCookie not found in config. "
            "Add it to ~/.clawdbot/credentials/ticktick-cli/config.json"
        )
    return config["sessionCookie"], config.get("v2DeviceId", "clawagent00000000000001")


def _generate_attachment_id() -> str:
    return secrets.token_hex(12)  # 12 bytes → 24 hex chars


def attach_command(args) -> None:
    try:
        session_cookie, v2_device_id = _get_session_config()

        task_name_or_id = args.task
        if is_task_id(task_name_or_id) and not args.list:
            found = api.find_task_by_id(task_name_or_id)
        else:
            found = api.find_task_by_title(task_name_or_id, args.list)

        if not found:
            print(f"Task not found: {task_name_or_id}", file=sys.stderr)
            sys.exit(1)

        task = found["task"]
        project_id = found["projectId"]

        file_path = Path(args.file_path)
        if not file_path.exists():
            print(f"File not found: {args.file_path}", file=sys.stderr)
            sys.exit(1)

        attachment_id = _generate_attachment_id()
        file_name = file_path.name
        file_bytes = file_path.read_bytes()

        url = f"https://api.ticktick.com/api/v1/attachment/upload/{project_id}/{task['id']}/{attachment_id}"
        x_device = json.dumps({"platform": "web", "version": 6430, "id": v2_device_id})

        # Do NOT set Content-Type — requests sets it with the multipart boundary automatically
        resp = requests.post(
            url,
            headers={
                "Cookie": f"t={session_cookie}",
                "X-Device": x_device,
                "User-Agent": "Mozilla/5.0 (rv:145.0) Firefox/145.0",
                "Origin": "https://ticktick.com",
                "Referer": "https://ticktick.com/webapp/",
            },
            files={"file": (file_name, file_bytes)},
        )

        if not resp.ok:
            raise RuntimeError(f"Upload failed ({resp.status_code}): {resp.text}")

        result = resp.json()

        if args.json:
            print(json.dumps(result, indent=2))
            return

        print(f'✓ File attached to "{task["title"]}"')
        print(f"  File: {file_name}")
        print(f"  Attachment ID: {attachment_id}")
        if result.get("size"):
            print(f"  Size: {result['size']} bytes")
        if result.get("fileType"):
            print(f"  Type: {result['fileType']}")

    except (RuntimeError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
