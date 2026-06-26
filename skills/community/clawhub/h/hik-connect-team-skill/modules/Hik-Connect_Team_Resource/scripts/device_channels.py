#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Device Channel List
"""

import sys
import os
import json
import argparse
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

class DeviceChannelsClient(HCTOpenClient):
    """Device channel query client"""
    
    def get_channels(self, device_serial: str, page: int = 1, page_size: int = 50):
        """Get and print device channel list"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Querying device channels: {device_serial}")
        
        endpoint = "/api/hccgw/resource/v1/areas/cameras/get"
        payload = {
            "pageIndex": page,
            "pageSize": page_size,
            "filter": {"deviceSerialNo": device_serial}
        }
        
        # Resource module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            data = result.get("data", {})
            channels = data.get("camera", [])
            total = len(channels)
            
            headers = ["No.", "Resource ID", "Channel Name", "Status", "Area", "Channel No."]
            rows = []
            for i, ch in enumerate(channels, 1):
                status = "Online" if ch.get("online") == "1" else "Offline"
                area_name = ch.get("area", {}).get("name", "Unknown")
                channel_no = ch.get("device", {}).get("channelInfo", {}).get("no", "-")
                rows.append([
                    i,
                    ch.get("id"),
                    ch.get("name", "Unknown"),
                    status,
                    area_name,
                    channel_no
                ])
            
            self.print_table(f"HCTOpen Device Channel List (Current page count: {total})", headers, rows)
            
            # Maintain output format consistent with original script
            self.exit_with_json({
                "success": True,
                "pageIndex": page,
                "pageSize": page_size,
                "total": total,
                "channels": [
                    {
                        "id": c.get("id"),
                        "name": c.get("name"),
                        # Convert to "1" or "0"
                        "online": c.get("online"),
                        # Map to root-level channelNo
                        "channelNo": c.get("device", {}).get("channelInfo", {}).get("no")
                    }
                    for c in channels
                ]
            })
        else:
            # Use unified message field
            print(f"[ERROR] Failed to get channel list: {result.get('message', 'Unknown error')}")
            self.exit_with_json({
                "success": False,
                "error": result.get("message", "Unknown error"),
                "errorCode": result.get("errorCode")
            })

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Get Device Channel List")
    parser.add_argument("device_serial", help="Device serial number")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--page-size", type=int, default=50, help="Page size")
    args = parser.parse_args()

    client = DeviceChannelsClient()
    client.get_channels(args.device_serial, page=args.page, page_size=args.page_size)

if __name__ == "__main__":
    main()
