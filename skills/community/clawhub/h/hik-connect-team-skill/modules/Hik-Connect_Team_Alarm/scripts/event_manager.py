#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Event Manager
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

class EventManager(HCTOpenClient):
    """Event subscription management client"""
    
    def subscribe(self, msg_types: list = None):
        """Subscribe to events"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Subscribing to events: {msg_types if msg_types else 'All events'}")
        
        endpoint = "/api/hccgw/rawmsg/v1/mq/subscribe"
        payload = {
            "subscribeType": 1,
            "msgType": msg_types if msg_types else []
        }
        
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            print("[SUCCESS] Event subscription successful")
            self.exit_with_json({"success": True, "message": "Event subscription successful"})
        else:
            print(f"[ERROR] Subscription failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

    def unsubscribe(self, msg_types: list = None):
        """Unsubscribe from events"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Unsubscribing from events: {msg_types if msg_types else 'All events'}")
        
        endpoint = "/api/hccgw/rawmsg/v1/mq/subscribe"
        payload = {
            "subscribeType": 0,
            "msgType": msg_types if msg_types else []
        }
        
        result = self.request("POST", endpoint, json_data=payload, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            print("[SUCCESS] Event unsubscription successful")
            self.exit_with_json({"success": True, "message": "Event unsubscription successful"})
        else:
            print(f"[ERROR] Unsubscription failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

    def query(self):
        """Query current subscription status"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Querying current subscription status...")
        
        endpoint = "/api/hccgw/rawmsg/v1/mq/info/subscribe"
        
        result = self.request("GET", endpoint, token_header_key="Token")
        
        if result.get("errorCode") == "0":
            data = result.get("data", {})
            is_sub = data.get("isSubscribe", False)
            sub_type = "Full subscription" if data.get("subscribeType") == 1 else "Partial subscription"
            events = data.get("events", [])
            
            print(f"[SUCCESS] Query successful: {'Subscribed' if is_sub else 'Not subscribed'} ({sub_type})")
            if events:
                print(f"Subscribed event list: {', '.join(events)}")
            
            self.exit_with_json({
                "success": True, 
                "data": {
                    "isSubscribe": is_sub,
                    "subscribeType": data.get("subscribeType"),
                    "subscribeTypeText": sub_type,
                    "events": events
                }
            })
        else:
            print(f"[ERROR] Query failed: {result.get('message', 'Unknown error')}")
            self.exit_with_json({"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")})

def main():
    parser = argparse.ArgumentParser(description="HCTOpen Event Subscription Management")
    subparsers = parser.add_subparsers(dest="command", help="Operation command")
    
    # Subscribe command
    sub_parser = subparsers.add_parser("subscribe", help="Subscribe to events")
    sub_parser.add_argument("--types", help="Comma-separated event type list (e.g. Msg330001,Msg330002), leave empty to subscribe to all")
    
    # Unsubscribe command
    unsub_parser = subparsers.add_parser("unsubscribe", help="Unsubscribe from events")
    unsub_parser.add_argument("--types", help="Comma-separated event type list, leave empty to unsubscribe from all")
    
    # Query command
    subparsers.add_parser("query", help="Query current subscription status")
    
    args = parser.parse_args()
    client = EventManager()
    
    if args.command == "subscribe":
        msg_types = [t.strip() for t in args.types.split(',') if t.strip()] if args.types else []
        client.subscribe(msg_types)
    elif args.command == "unsubscribe":
        msg_types = [t.strip() for t in args.types.split(',') if t.strip()] if args.types else []
        client.unsubscribe(msg_types)
    elif args.command == "query":
        client.query()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
