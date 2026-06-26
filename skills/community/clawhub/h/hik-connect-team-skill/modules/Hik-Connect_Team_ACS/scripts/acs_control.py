#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen ACS Control
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

class ACSControlClient(HCTOpenClient):
    """Door access control client"""
    
    def control(self, action_type: int, element_list: list):
        """Execute door access control operation"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executing door access control: Type={action_type}, Count={len(element_list) if element_list else 'All'}")

        # Check if element_list is empty
        if not element_list:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] element_list cannot be empty. Please provide at least one resource ID.")
            self.exit_with_json({
                "success": False,
                "error": "element_list is required and cannot be empty",
                "errorCode": "PARAMETER_EMPTY"
            })

        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executing door access control: Type={action_type}, Count={len(element_list)}")

        endpoint = "/api/hccgw/acs/v1/remote/control"
        payload = {
            "remoteControl": {
                "actionType": action_type,
                "elementlist": element_list
            }
        }
            
        # ACS module API uses "Token" as Header Key
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            op_result = result.get("data", {}).get("operationResult", [])
            if op_result:
                print("[WARNING] Some devices operation failed:")
                headers = ["No.", "Door Resource ID", "Door Name", "Area", "Error Code"]
                rows = []
                for i, res in enumerate(op_result, 1):
                    rows.append([
                        i,
                        res.get("elementId", "-"),
                        res.get("elementName", "-"),
                        res.get("areaName", "-"),
                        res.get("errorCode", "-")
                    ])
                self.print_table("Failed Device List", headers, rows)
                self.exit_with_json({"success": False, "operationResult": op_result, "error": "Some operations failed"})
            else:
                print("[SUCCESS] All door access operations executed successfully")
                self.exit_with_json({"success": True, "operationResult": []})
        else:
            # Use unified message field
            print(f"[ERROR] Door access control failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "error": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Door Access Remote Control")
    parser.add_argument("--action-type", type=int, required=True, choices=[1, 2, 3, 4], help="1-open door, 2-close door, 3-normally open, 4-normally closed")
    parser.add_argument("--element-list", type=str, default="", help="Comma-separated resource ID list")
    args = parser.parse_args()

    elements = [e.strip() for e in args.element_list.split(',') if e.strip()] if args.element_list else []
    
    client = ACSControlClient()
    client.control(args.action_type, elements)

if __name__ == "__main__":
    main()
