#!/usr/bin/env python3
"""
Imou Device Manage Skill – CLI entry.

Commands: list (paginated account devices), get (device by serial), rename (device or channel name).
All descriptions and output in English. Requires IMOU_APP_ID, IMOU_APP_SECRET; optional IMOU_BASE_URL.
"""

import argparse
import json
import os
import sys

# Ensure scripts dir is on path when run from project root or elsewhere
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from imou_client import (
    get_access_token,
    list_device_details_by_page,
    list_device_details_by_ids,
    modify_device_name,
)

APP_ID = os.environ.get("IMOU_APP_ID", "")
APP_SECRET = os.environ.get("IMOU_APP_SECRET", "")
BASE_URL = os.environ.get("IMOU_BASE_URL", "").strip() or "https://openapi.lechange.cn"


def _ensure_token():
    if not APP_ID or not APP_SECRET:
        print("[ERROR] Set IMOU_APP_ID and IMOU_APP_SECRET.", file=sys.stderr)
        sys.exit(1)
    r = get_access_token(APP_ID, APP_SECRET, BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Get token failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    return r["access_token"]


def _print_device(d, verbose=True):
    """Print one device summary (serial, model, status, name, channels)."""
    dev_id = d.get("deviceId", "")
    name = d.get("deviceName", "")
    model = d.get("deviceModel", "")
    status = d.get("deviceStatus", "")
    ch_list = d.get("channelList", [])
    print(f"  deviceId: {dev_id}, deviceName: {name}, deviceModel: {model}, deviceStatus: {status}")
    if verbose and ch_list:
        for ch in ch_list:
            cid = ch.get("channelId", "")
            cname = ch.get("channelName", "")
            cstatus = ch.get("channelStatus", "")
            print(f"    channelId: {cid}, channelName: {cname}, channelStatus: {cstatus}")


def cmd_list(args):
    token = _ensure_token()
    page = max(1, args.page)
    page_size = max(1, min(50, args.page_size))
    r = list_device_details_by_page(token, page=page, page_size=page_size, source=args.source or "bindAndShare", base_url=BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] List failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    device_list = r.get("device_list", [])
    count = r.get("count", 0)
    print(f"[INFO] Page {page}, pageSize {page_size}, count: {count}")
    for d in device_list:
        _print_device(d, verbose=not args.brief)
    if args.json:
        print(json.dumps({"count": count, "deviceList": device_list}, ensure_ascii=False, indent=2))


def cmd_get(args):
    if not args.serials:
        print("[ERROR] At least one device serial required.", file=sys.stderr)
        sys.exit(1)
    token = _ensure_token()
    r = list_device_details_by_ids(token, args.serials, base_url=BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Get failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    device_list = r.get("device_list", [])
    for d in device_list:
        _print_device(d, verbose=True)
    if args.json:
        print(json.dumps({"deviceList": device_list}, ensure_ascii=False, indent=2))


def cmd_rename(args):
    token = _ensure_token()
    channel_id = getattr(args, "channel_id", None) or None
    product_id = getattr(args, "product_id", None) or None
    sub_device_id = getattr(args, "sub_device_id", None) or None
    r = modify_device_name(
        token,
        args.serial,
        args.name,
        channel_id=channel_id,
        product_id=product_id,
        sub_device_id=sub_device_id,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] Rename failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    target = f"channel {channel_id}" if channel_id else "device"
    print(f"[SUCCESS] Renamed {target} {args.serial} to: {args.name}")


def main():
    parser = argparse.ArgumentParser(description="Imou Device Manage – list, get, rename.")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List account devices (paginated).")
    p_list.add_argument("--page", type=int, default=1, help="Page number (default 1).")
    p_list.add_argument("--page-size", type=int, default=10, help="Page size 1-50 (default 10).")
    p_list.add_argument("--source", choices=["bind", "share", "bindAndShare"], default="bindAndShare", help="Device source (default bindAndShare).")
    p_list.add_argument("--brief", action="store_true", help="Do not print channel details.")
    p_list.add_argument("--json", action="store_true", help="Print full JSON at end.")
    p_list.set_defaults(func=cmd_list)

    # get
    p_get = sub.add_parser("get", help="Get device details by serial(s).")
    p_get.add_argument("serials", nargs="+", help="Device serial(s).")
    p_get.add_argument("--json", action="store_true", help="Print full JSON.")
    p_get.set_defaults(func=cmd_get)

    # rename
    p_rename = sub.add_parser("rename", help="Rename device or channel.")
    p_rename.add_argument("serial", help="Device serial.")
    p_rename.add_argument("name", help="New name (max 64 chars).")
    p_rename.add_argument("--channel-id", dest="channel_id", default=None, help="Channel ID; omit to set device name.")
    p_rename.add_argument("--product-id", dest="product_id", default=None, help="Product ID; must be set when device exists (e.g. from list/get).")
    p_rename.add_argument("--sub-device-id", dest="sub_device_id", default=None, help="Sub-device ID; required when renaming a sub-device.")
    p_rename.set_defaults(func=cmd_rename)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
