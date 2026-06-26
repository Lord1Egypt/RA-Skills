#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Door List
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

class DoorListClient(HCTOpenClient):
    """Door access resource list query client"""
    
    def fetch_doors(self, device_serial: str):
        """Get door access resource list and print"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Getting door access resource list (Device serial number: {device_serial if device_serial else 'All'})...")
        
        endpoint = "/api/hccgw/resource/v1/areas/doors/get"
        # pageSize=100, pageIndex=1, includeSubArea=1 are fixed values
        payload = {
            "pageIndex": 1,
            "pageSize": 100,
            "filter": {
                "includeSubArea": "1",
                "deviceSerialNo": device_serial
            }
        }
        
        # Resource module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            data = result.get("data", {})
            doors = data.get("door", [])
            total = len(doors)

            headers = ["No.", "Door Resource ID", "Door Access Name", "Status"]
            rows = []
            simplified_doors = []
            
            for i, door in enumerate(doors, 1):
                status = "Online" if door.get("online") == "1" else "Offline"
                rows.append([
                    i,
                    door.get("id"),
                    door.get("name", "Unknown"),
                    status
                ])
                # Only keep id, name, online status
                simplified_doors.append({
                    "resourceId": door.get("id"),
                    "name": door.get("name"),
                    "online": door.get("online")
                })
            
            self.print_table(f"HCTOpen Door Access Resource List (Count: {total})", headers, rows)
            self.exit_with_json({
                "success": True,
                "total": total,
                "doors": simplified_doors
            })
        else:
            # Use unified message field
            print(f"[ERROR] Failed to get door access resource list: {result.get('message', 'Unknown error')}")
            self.exit_with_json({
                "success": False,
                "error": result.get("message", "Unknown error"),
                "errorCode": result.get("errorCode")
            })

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Get Door Access Resource List")
    parser.add_argument("device_serial", help="Device serial number (optional)")
    args = parser.parse_args()

    client = DoorListClient()
    client.fetch_doors(device_serial=args.device_serial)

if __name__ == "__main__":
    main()
