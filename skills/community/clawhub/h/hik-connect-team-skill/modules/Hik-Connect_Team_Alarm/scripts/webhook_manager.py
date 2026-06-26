#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Webhook Manager
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Robust lib directory import logic
def setup_lib_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
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
    print("[ERROR] Cannot find lib directory")
    sys.exit(1)

from token_manager import HCTOpenClient

class WebhookManager(HCTOpenClient):
    """Webhook configuration management client"""
    
    def query(self):
        """Query Webhook configuration"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Querying Webhook configuration...")
        endpoint = "/api/hccgw/webhook/v1/config/query"
        result = self.request("POST", endpoint, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            data = result.get("data", {})
            if data:
                headers = ["Configuration Item", "Content"]
                rows = [
                    ["Callback URL (callbackUrl)", data.get("callbackUrl", "-")],
                    ["Retry Count (retryTimes)", data.get("retryTimes", "-")],
                    ["Retry Interval (retryDelay)", f"{data.get('retryDelay', '-')} ms"]
                ]
                self.print_table("HCTOpen Webhook Current Configuration", headers, rows)
                self.exit_with_json({"success": True, "data": data})
            else:
                print("[INFO] Webhook not currently configured")
                self.exit_with_json({"success": True, "data": None, "message": "No webhook configuration found"})
        else:
            print(f"[ERROR] Query failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

    def save(self, callback_url: str, sign_secret: str = None, retry_times: int = 3, retry_delay: int = 1000):
        """Save/Subscribe Webhook configuration"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Saving Webhook configuration: {callback_url}")
        
        if not callback_url.startswith("https://"):
            print("[ERROR] Callback URL must use HTTPS protocol")
            self.exit_with_json({"success": False, "message": "Callback URL must use HTTPS protocol"})

        endpoint = "/api/hccgw/webhook/v1/config/save"
        payload = {
            "callbackUrl": callback_url,
            "retryTimes": retry_times,
            "retryDelay": retry_delay
        }
        if sign_secret:
            payload["signSecret"] = sign_secret
            
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            print("[SUCCESS] Webhook configuration saved successfully")
            self.exit_with_json({"success": True, "message": "Webhook configuration saved successfully"})
        else:
            print(f"[ERROR] Save failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

    def delete(self):
        """Delete Webhook configuration"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Deleting Webhook configuration...")
        endpoint = "/api/hccgw/webhook/v1/config/delete"
        result = self.request("POST", endpoint, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            print("[SUCCESS] Webhook configuration deleted successfully")
            self.exit_with_json({"success": True, "message": "Webhook configuration deleted successfully"})
        else:
            print(f"[ERROR] Delete failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Webhook Configuration Management")
    subparsers = parser.add_subparsers(dest="command", help="Operation command")
    
    # Query command
    subparsers.add_parser("query", help="Query current Webhook configuration")
    
    # Save command
    save_parser = subparsers.add_parser("save", help="Save/Subscribe Webhook configuration")
    save_parser.add_argument("--url", required=True, help="Callback URL (must be HTTPS)")
    save_parser.add_argument("--secret", help="Signing secret (optional, 8-32 alphanumeric combination)")
    save_parser.add_argument("--retries", type=int, default=3, help="Retry count (default: 3)")
    save_parser.add_argument("--delay", type=int, default=1000, help="Retry interval ms (default: 1000)")
    
    # Delete command
    subparsers.add_parser("delete", help="Delete Webhook configuration")
    
    args = parser.parse_args()
    client = WebhookManager()
    
    if args.command == "query":
        client.query()
    elif args.command == "save":
        client.save(args.url, args.secret, args.retries, args.delay)
    elif args.command == "delete":
        client.delete()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
