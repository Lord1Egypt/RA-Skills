#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Device List
"""

import sys
import os
import argparse
import json
from datetime import datetime

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

class DeviceListClient(HCTOpenClient):
    """Device list query client"""

    def fetch_devices(self, page: int = 1, page_size: int = 10, device_category: str = None, match_key: str = None):
        """Get device list and print"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Getting device list (page {page}, {page_size} items per page)...")

        # Validate match_key requirement
        if match_key and not device_category:
            print("[WARNING] match-key is only effective when device-category is specified.")

        endpoint = "/api/hccgw/resource/v1/devices/get"
        payload = {"pageIndex": page, "pageSize": page_size}

        # Add device category filter if specified
        if device_category:
            payload["deviceCategory"] = device_category

        if match_key:
            payload["filter"] = {"matchKey": match_key}

        print(payload)

        # Resource module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")

        if result.get("errorCode") == "0":
            data = result.get("data", {})
            devices = data.get("device", [])
            total = len(devices)

            headers = ["No.", "Device ID", "Device Serial Number", "Device Name", "Model", "Version", "Device Type", "Added Time", "Status"]
            rows = []
            for i, dev in enumerate(devices, 1):
                status = "Online" if dev.get("onlineStatus") == 1 else "Offline"
                rows.append([
                    i,
                    dev.get("id"),
                    dev.get("serialNo", "Unknown"),
                    dev.get("name", "Unknown"),
                    dev.get("type", "Unknown"),
                    dev.get("version", "-"),
                    dev.get("category", "Unknown"),
                    dev.get("addTime", "Unknown"),
                    status
                ])

            self.print_table(f"HCTOpen Device List (Current page count: {total})", headers, rows)
            self.exit_with_json({
                "success": True,
                "total": total,
                "devices": [
                    {
                        "id": d.get("id"),
                        "deviceName": d.get("name"),
                        "serialNo": d.get("serialNo"),
                        "type": d.get("type"),
                        "onlineStatus": d.get("onlineStatus"),
                        "category": d.get("category"),
                        "addTime": d.get("addTime"),
                    }
                    for d in devices
                ]
            })
        else:
            # Use unified message field
            print(f"[ERROR] Failed to get device list: {result.get('message', 'Unknown error')}")
            self.exit_with_json({
                "success": False,
                "error": result.get("message", "Unknown error"),
                "errorCode": result.get("errorCode")
            })

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Get Device List")
    parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    parser.add_argument("--page-size", type=int, default=10, help="Page size (default: 10)")
    parser.add_argument("--device-category", type=str, default=None,
                        help="Device category filter (encodingDevice, accessControllerDevice, alarmDevice, videoIntercomDevice, mobileDevice, businessDisplayDevice)")
    parser.add_argument("--match-key", type=str, default=None,
                        help="Fuzzy match key for device name or serial number. Only effective when device-category is specified.")
    args = parser.parse_args()

    client = DeviceListClient()
    client.fetch_devices(page=args.page, page_size=args.page_size, device_category=args.device_category, match_key=args.match_key)

if __name__ == "__main__":
    main()
