#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Device Video Stream
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone
try:
    import requests
except ImportError:
    requests = None

# Robust lib directory import logic: search upward until lib directory is found
def setup_lib_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Search upward 3 levels for root directory containing lib
    root_dir = current_dir
    for _ in range(3):
        root_dir = os.path.dirname(root_dir)
        potential_lib = os.path.join(root_dir, "lib")
        if os.path.exists(potential_lib):
            if potential_lib not in sys.path:
                sys.path.insert(0, potential_lib)
            return True
    return False

if not setup_lib_path():
    print("[ERROR] Cannot find lib directory, please ensure script is located in Hik-Connect_Team Skills directory structure")
    sys.exit(1)

from token_manager import HCTOpenClient


def verify_stream(url):
    """
    Verify stream is playable by fetching m3u8 and checking for error patterns.
    Returns: (is_valid, error_type)
    - H265 error pattern: m3u8 contains "ErrCode/9053"
    """
    if not requests:
        print("[WARN] requests library not installed, skipping stream verification")
        return True, None

    try:
        resp = requests.get(url, timeout=5, headers={"User-Agent": "HCTOpen/1.0"})
        if resp.status_code != 200:
            return True, None  # Don't block on HTTP errors, let player handle

        content = resp.text
        # Check for H265 error indicator: ErrCode/9053 in playlist
        if "ErrCode/9053" in content or "9053_0.ts" in content:
            return False, "H265_NOT_SUPPORTED"

        # Check if playlist immediately ends (no valid segments)
        lines = content.split("\n")
        segment_count = sum(1 for line in lines if line.endswith(".ts"))
        if segment_count == 0 and "#EXT-X-ENDLIST" in content:
            return False, "NO_VALID_SEGMENTS"

        return True, None
    except Exception as e:
        print(f"[WARN] Stream verification failed: {e}")
        return True, None  # Don't block on network errors


def format_expire_time(exp_time_ms):
    """Convert millisecond timestamp to yyyy-mm-dd hh:mm:ss in local timezone"""
    if not exp_time_ms:
        return None
    dt = datetime.fromtimestamp(exp_time_ms / 1000, tz=timezone.utc).astimezone()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class VideoClient(HCTOpenClient):
    """Device video stream client"""

    def get_url(self, device_serial: str, resource_id: str, video_duration: int = 600):
        """Get video stream address"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Requesting video stream: Device={device_serial}, Resource={resource_id}")

        endpoint = "/api/hccgw/video/v1/live/address/get"
        payload = {
            "resourceId": resource_id,
            "deviceSerial": device_serial,
            "protocol": 2, #HLS format: Stream retrieval supports only this format; no other formats are supported.
            "expireTime": video_duration
        }

        # Video module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")

        if result.get("errorCode") == "0":
            data = result.get("data", {})
            stream_url = data.get("url")
            exp_time_ms = data.get("expireTime")

            if stream_url:
                print(f"[SUCCESS] Got stream URL: {stream_url}")

                # Verify stream is playable (check for H265 errors)
                is_valid, error_type = verify_stream(stream_url)

                # Format expire time as yyyy-mm-dd hh:mm:ss
                expire_time_str = format_expire_time(exp_time_ms)
                print(f"[INFO] Stream URL expiration time: {expire_time_str}")

                if not is_valid:
                    print(f"[ERROR] Stream URL is not playable, the error type is : {error_type}")
                    self.exit_with_json({
                        "success": False,
                        "url": stream_url,
                        "expireTime": expire_time_str,
                        "playable": False
                    })

                self.exit_with_json({
                    "success": True,
                    "url": stream_url,
                    "expireTime": expire_time_str,
                    "playable": True
                })
            else:
                self.exit_with_json({
                    "success": False,
                    "url": None,
                    "expireTime": None,
                    "playable": False
                })
        else:
            # Use unified message field
            print(f"[ERROR] Video stream failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({
                "success": False,
                "url": None,
                "expireTime": None,
                "playable": False
            })

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Device Video Stream")
    parser.add_argument("--device-serial", required=True, help="Device serial number")
    parser.add_argument("--resource-id", required=True, help="Resource ID (Channel ID)")
    parser.add_argument("--video-duration", type=int, default=600, help="Valid duration (seconds)")
    args = parser.parse_args()

    client = VideoClient()
    client.get_url(args.device_serial, args.resource_id, args.video_duration)

if __name__ == "__main__":
    main()