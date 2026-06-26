#!/usr/bin/env python3
"""
Imou Device Operate Skill – CLI entry.

Commands: snapshot (capture image, optional download), ptz (PTZ move control).
All descriptions and output in English. Requires IMOU_APP_ID, IMOU_APP_SECRET; optional IMOU_BASE_URL.
"""

import argparse
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from imou_client import (
    get_access_token,
    set_device_snap_enhanced,
    control_move_ptz,
)

APP_ID = os.environ.get("IMOU_APP_ID", "")
APP_SECRET = os.environ.get("IMOU_APP_SECRET", "")
BASE_URL = os.environ.get("IMOU_BASE_URL", "").strip() or "https://openapi.lechange.cn"

# PTZ operation labels for help/output
PTZ_LABELS = {
    "0": "up",
    "1": "down",
    "2": "left",
    "3": "right",
    "4": "up-left",
    "5": "down-left",
    "6": "up-right",
    "7": "down-right",
    "8": "zoom-in",
    "9": "zoom-out",
    "10": "stop",
}


def _ensure_token():
    if not APP_ID or not APP_SECRET:
        print("[ERROR] Set IMOU_APP_ID and IMOU_APP_SECRET.", file=sys.stderr)
        sys.exit(1)
    r = get_access_token(APP_ID, APP_SECRET, BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Get token failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    return r["access_token"]


def _download_url_to_file(url: str, path: str) -> bool:
    """Download URL content to local file. Returns True on success."""
    try:
        import requests
        headers = {"Client-Type": "OpenClaw"}
        resp = requests.get(url, headers=headers, timeout=60, stream=True)
        resp.raise_for_status()
        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"[ERROR] Download failed: {e}", file=sys.stderr)
        return False


def cmd_snapshot(args):
    token = _ensure_token()
    r = set_device_snap_enhanced(
        token,
        args.device_serial,
        args.channel_id,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] Snapshot failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    url = r.get("url", "")
    if not url:
        print("[ERROR] No snapshot URL returned.", file=sys.stderr)
        sys.exit(1)
    print(url)
    if getattr(args, "save", None):
        save_path = args.save
        if os.path.isdir(save_path):
            save_path = os.path.join(save_path, f"snap_{args.device_serial}_{args.channel_id}.jpg")
        if _download_url_to_file(url, save_path):
            print(f"[INFO] Saved to {save_path}", file=sys.stderr)


def cmd_ptz(args):
    token = _ensure_token()
    op = str(args.operation).strip()
    if op not in PTZ_LABELS:
        print(f"[ERROR] Invalid operation. Use 0-10. See --help.", file=sys.stderr)
        sys.exit(1)
    r = control_move_ptz(
        token,
        args.device_serial,
        args.channel_id,
        op,
        args.duration_ms,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] PTZ failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    label = PTZ_LABELS.get(op, op)
    print(f"[SUCCESS] PTZ {label} for {args.duration_ms} ms on {args.device_serial}/{args.channel_id}")


def main():
    parser = argparse.ArgumentParser(description="Imou Device Operate – snapshot, PTZ control.")
    sub = parser.add_subparsers(dest="command", required=True)

    # snapshot
    p_snap = sub.add_parser("snapshot", help="Capture device snapshot; print URL, optionally save to file.")
    p_snap.add_argument("device_serial", help="Device serial (deviceId).")
    p_snap.add_argument("channel_id", help="Channel ID (e.g. 0).")
    p_snap.add_argument("--save", metavar="PATH", help="Download image to PATH (or directory; filename auto-generated).")
    p_snap.set_defaults(func=cmd_snapshot)

    # ptz
    p_ptz = sub.add_parser("ptz", help="PTZ move control. Operation: 0=up,1=down,2=left,3=right,4=ul,5=dl,6=ur,7=dr,8=zoom-in,9=zoom-out,10=stop.")
    p_ptz.add_argument("device_serial", help="Device serial (deviceId).")
    p_ptz.add_argument("channel_id", help="Channel ID (e.g. 0).")
    p_ptz.add_argument("operation", help="Operation code 0-10.")
    p_ptz.add_argument("duration_ms", type=int, help="Duration in milliseconds.")
    p_ptz.set_defaults(func=cmd_ptz)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
