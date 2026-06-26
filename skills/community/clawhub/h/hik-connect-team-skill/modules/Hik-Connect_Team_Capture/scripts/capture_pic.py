#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Device Picture Capture
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

class CaptureClient(HCTOpenClient):
    """Device capture client"""
    
    def capture(self, device_serial: str, channel_no: int = 1):
        """Execute capture operation"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Requesting capture: Device={device_serial}, Channel={channel_no}")
        
        endpoint = "/api/hccgw/resource/v1/device/capturePic"
        payload = {
            "deviceSerial": device_serial,
            "channelNo": str(channel_no)
        }
        
        # Capture module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            data = result.get("data", {})
            capture_url = data.get("captureUrl")
            is_encrypted = data.get("isEncrypted")
            
            if capture_url:
                print(f"[SUCCESS] Capture successful: {capture_url}")
                if is_encrypted == 1:
                    print("[INFO] Note: Image is encrypted, need to use key to decrypt before viewing")
                
                self.exit_with_json({
                    "success": True,
                    "captureUrl": capture_url,
                    "isEncrypted": is_encrypted
                })
            else:
                print("[ERROR] Response does not contain capture URL")
                self.exit_with_json({"success": False, "error": "Capture URL not found"})
        else:
            # Use unified message field
            print(f"[ERROR] Capture failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({
                "success": False,
                "error": result.get("message", "Unknown error"),
                "errorCode": result.get("errorCode")
            })

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Device Capture")
    parser.add_argument("device_info", help="Device serial number, optional comma-separated channel number (e.g. D72821502,1)")
    args = parser.parse_args()

    parts = args.device_info.split(",")
    device_serial = parts[0].strip()
    channel_no = 1
    if len(parts) > 1:
        try:
            channel_no = int(parts[1].strip())
        except ValueError:
            print("[ERROR] Channel number must be integer")
            sys.exit(1)

    client = CaptureClient()
    client.capture(device_serial, channel_no)

if __name__ == "__main__":
    main()
