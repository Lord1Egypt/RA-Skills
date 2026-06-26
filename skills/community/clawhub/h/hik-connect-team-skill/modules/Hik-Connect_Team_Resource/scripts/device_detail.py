#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Device Detail
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

class DeviceDetailClient(HCTOpenClient):
    """Device detail query client"""
    
    def get_detail(self, device_serial: str):
        """Get and print device details"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Querying device details: {device_serial}")
        
        endpoint = "/api/hccgw/resource/v1/devicedetail/get"
        payload = {"deviceSerialNo": device_serial}
        
        # Resource module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            data = result.get("data", {}).get("device", {})
            base_info = data.get("baseInfo", {})

            # 1. Define list of fields to remove
            exclude_keys = [
                "availableCameraChannelNum",
                "availableAlarmInputChannelNum",
                "availableAlarmOutputChannelNum",
                "areaId",
                "area"
            ]

            # 2. Create a simplified base_info for JSON output
            # Use dict comprehension to filter out unwanted keys
            filtered_base_info = {k: v for k, v in base_info.items() if k not in exclude_keys}
            headers = ["Device ID", "Device Name", "Device Serial Number", "Device Type", "Model", "Status", "Version", "Stream Encryption"]
            status = "Online" if data.get("onlineStatus") == 1 else "Offline"
            rows = [[
                base_info.get("id"),
                base_info.get("name", "Unknown"),
                base_info.get("serialNo", "Unknown"),
                base_info.get("category", "Unknown"),
                base_info.get("type", "Unknown"),
                status,
                base_info.get("version", "Unknown"),
                "Enabled" if base_info.get("streamEncryptEnable", "0") == "1" else "Disabled",
            ]]
            
            self.print_table("HCTOpen Device Detail", headers, rows)
            
            # Maintain output format
            self.exit_with_json({
                "success": True,
                "total": 1,
                "devices": [{
                    "base_info": filtered_base_info,
                    "onlineStatus": data.get("onlineStatus")
                }]
            })
        else:
            # Use unified message field
            print(f"[ERROR] Failed to get device details: {result.get('message', 'Unknown error')}")
            self.exit_with_json({
                "success": False,
                "error": result.get("message", "Unknown error"),
                "errorCode": result.get("errorCode")
            })

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Get Device Detail")
    parser.add_argument("device_serial", help="Device serial number")
    args = parser.parse_args()

    client = DeviceDetailClient()
    client.get_detail(args.device_serial)

if __name__ == "__main__":
    main()
