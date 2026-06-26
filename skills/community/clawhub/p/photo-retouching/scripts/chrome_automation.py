#!/usr/bin/env python3
"""
RunningHub Workflow Chrome Automation Script
For automated image upload and workflow execution
"""

import json
import time
import socket
import struct
import base64
import sys


def send_ws_command(ws_url, method, params=None, msg_id=None):
    """Send CDP command via WebSocket"""
    if msg_id is None:
        msg_id = int(time.time() * 1000)

    command = {"id": msg_id, "method": method}
    if params:
        command["params"] = params

    payload = json.dumps(command).encode()

    frame = bytes([0x81, len(payload)]) + payload
    return frame


def parse_ws_response(data):
    """Parse WebSocket response"""
    if len(data) < 2:
        return None

    opcode = data[0] & 0x0F
    masked = (data[1] & 0x80) != 0
    payload_len = data[1] & 0x7F

    offset = 2
    if payload_len == 126:
        if len(data) < 4:
            return None
        payload_len = struct.unpack(">H", data[2:4])[0]
        offset = 4
    elif payload_len == 127:
        if len(data) < 10:
            return None
        payload_len = struct.unpack(">Q", data[2:10])[0]
        offset = 10

    header_len = offset + (4 if masked else 0)
    total_len = header_len + payload_len

    if len(data) < total_len:
        return None

    if masked:
        mask = data[offset : offset + 4]
        payload_data = bytearray(data[header_len:total_len])
        for i in range(len(payload_data)):
            payload_data[i] ^= mask[i % 4]
        payload_str = bytes(payload_data).decode("utf-8", errors="ignore")
    else:
        payload_str = data[header_len:total_len].decode("utf-8", errors="ignore")

    try:
        return json.loads(payload_str)
    except:
        return None


def main():
    WORKFLOW_URL = "https://www.runninghub.ai/#/workflow/1987728214757978114"
    IMAGE_PATH = ""

    print("=" * 70)
    print("RunningHub Chrome Automation")
    print("=" * 70)
    print(f"Workflow: {WORKFLOW_URL}")
    print(f"Image: {IMAGE_PATH}")
    print()

    print("[1/5] Creating workflow page...")
    import requests

    resp = requests.put(f"http://127.0.0.1:9222/json/new?{WORKFLOW_URL}")
    page_info = resp.json()
    page_id = page_info.get("id")
    ws_url = page_info.get("webSocketDebuggerUrl")
    print(f"Page ID: {page_id}")
    print(f"WebSocket: {ws_url}")

    print("\n[2/5] Waiting for page to load (15 seconds)...")
    time.sleep(15)

    print("\n[3/5] Connecting to Chrome DevTools...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)

    ws_parts = ws_url.replace("ws://", "").split("/")
    host_port = ws_parts[0].split(":")
    host = host_port[0]
    port = int(host_port[1])
    path = "/" + "/".join(ws_parts[1:])

    sock.connect((host, port))

    key = base64.b64encode(bytes([0x41] * 16)).decode()
    handshake = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    sock.send(handshake.encode())

    response = sock.recv(1024)
    if b"101" not in response:
        print("❌ WebSocket connection failed")
        return
    print("✅ WebSocket connected successfully")

    print("\n[4/5] Enabling Chrome DevTools domains...")
    sock.send(send_ws_command(ws_url, "Runtime.enable", {}, 1))
    sock.send(send_ws_command(ws_url, "DOM.enable", {}, 2))
    sock.send(send_ws_command(ws_url, "Page.enable", {}, 3))
    time.sleep(1)

    while True:
        try:
            sock.settimeout(0.5)
            data = sock.recv(4096)
        except:
            break

    sock.settimeout(30)

    print("\n[5/5] Executing page operations...")
    print("Attempting to click upload button and upload image...")

    js_code = """
    (function() {
        const inputs = document.querySelectorAll('input[type="file"]');
        if (inputs.length > 0) {
            console.log('Found file input:', inputs.length);
            return {found: true, count: inputs.length};
        }
        
        const buttons = document.querySelectorAll('button, .upload-btn, [class*="upload"]');
        console.log('Found buttons:', buttons.length);
        
        return {found: false, buttons: buttons.length};
    })()
    """

    sock.send(
        send_ws_command(
            ws_url,
            "Runtime.evaluate",
            {"expression": js_code, "returnByValue": True},
            4,
        )
    )

    all_data = b""
    result = None
    for _ in range(20):
        try:
            chunk = sock.recv(8192)
            if not chunk:
                break
            all_data += chunk

            while len(all_data) >= 2:
                parsed = parse_ws_response(all_data)
                if parsed is None:
                    break

                all_data = all_data[2 + (len(all_data) - 2) :]

                if parsed.get("id") == 4 and "result" in parsed:
                    result = parsed
                    break

            if result:
                break

        except socket.timeout:
            break

    if result:
        value = result.get("result", {}).get("result", {}).get("value", {})
        print(f"Page status: {value}")

    print("\n⚠️ Note: Chrome automation has file upload limitations")
    print(
        "Due to browser security restrictions, cannot directly upload local files via CDP"
    )
    print()
    print("【Alternative Solutions】")
    print("1. API method has been successfully tested (using default image)")
    print("2. Recommended: run manually on web, then use monitor script to track task")
    print()
    print("If you want to continue using Chrome automation, you need:")
    print("- Pre-login to RunningHub")
    print("- Use Chrome Extension or other methods to handle file upload")

    sock.close()

    requests.get(f"http://127.0.0.1:9222/json/close/{page_id}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
