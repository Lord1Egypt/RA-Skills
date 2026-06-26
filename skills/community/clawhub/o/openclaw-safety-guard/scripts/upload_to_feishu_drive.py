#!/usr/bin/env python3
"""
Uploads dashboard.html to Feishu Drive and prints a shareable link.
Requires: FEISHU_APP_ID, FEISHU_APP_SECRET env vars.
Config: feishu_drive.folder_token in config.json.
"""
import os
import json
import urllib.request
import urllib.error
from utils import get_data_dir, get_watchdog_config


def get_tenant_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    if data.get("code") != 0:
        raise RuntimeError(f"Failed to get tenant token: {data}")
    return data["tenant_access_token"]


def upload_file(token, folder_token, file_path, file_name):
    import mimetypes
    boundary = "----WatchdogUploadBoundary"
    mime_type = mimetypes.guess_type(file_name)[0] or "text/html"

    with open(file_path, "rb") as f:
        file_data = f.read()

    body_parts = []
    # file_name field
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file_name\"\r\n\r\n{file_name}")
    # parent_type field
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parent_type\"\r\n\r\nexplorer")
    # parent_node field
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parent_node\"\r\n\r\n{folder_token}")
    # size field
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"size\"\r\n\r\n{len(file_data)}")

    body_prefix = ("\r\n".join(body_parts) + "\r\n").encode()
    file_header = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{file_name}\"\r\nContent-Type: {mime_type}\r\n\r\n".encode()
    body_suffix = f"\r\n--{boundary}--\r\n".encode()

    body = body_prefix + file_header + file_data + body_suffix

    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"Upload failed: {result}")
    return result.get("data", {}).get("file_token", "")


def main():
    config = get_watchdog_config()
    drive_cfg = config.get("feishu_drive", {})

    if not drive_cfg.get("enabled", False):
        print("Feishu Drive upload is disabled in config. Skipping.")
        return

    app_id = os.environ.get(drive_cfg.get("app_id_env", "FEISHU_APP_ID"), "")
    app_secret = os.environ.get(drive_cfg.get("app_secret_env", "FEISHU_APP_SECRET"), "")
    folder_token = drive_cfg.get("folder_token", "")

    if not app_id or not app_secret:
        print("ERROR: FEISHU_APP_ID or FEISHU_APP_SECRET not set. Skipping upload.")
        return
    if not folder_token:
        print("ERROR: feishu_drive.folder_token not configured. Skipping upload.")
        return

    data_dir = get_data_dir()
    html_path = os.path.join(data_dir, "dashboard.html")
    if not os.path.exists(html_path):
        print("ERROR: dashboard.html not found. Run generate_dashboard.py first.")
        return

    token = get_tenant_token(app_id, app_secret)
    file_token = upload_file(token, folder_token, html_path, "openclaw-watchdog-dashboard.html")
    share_url = f"https://feishu.cn/drive/file/{file_token}"
    print(f"Upload complete. File token: {file_token}")
    print(f"Share URL: {share_url}")


if __name__ == "__main__":
    main()
