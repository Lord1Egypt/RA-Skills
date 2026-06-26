#!/usr/bin/env python3
"""
Imou Device Video Skill – CLI entry.

Commands: live (get live HLS), record-clips (local/cloud clips), playback-hls (record playback HLS).
All descriptions and output in English. Requires IMOU_APP_ID, IMOU_APP_SECRET; optional IMOU_BASE_URL.
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from imou_client import (
    get_access_token,
    get_live_hls,
    query_local_records,
    query_cloud_records,
    create_device_record_hls,
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


def cmd_live(args):
    token = _ensure_token()
    stream_id = getattr(args, "stream_id", 0)
    if stream_id not in (0, 1):
        stream_id = 0
    r = get_live_hls(
        token,
        args.device_id,
        args.channel_id,
        stream_id=stream_id,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] Live HLS failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    hls = r.get("hls", "")
    print(hls)
    if getattr(args, "json", False):
        print(json.dumps({"hls": hls}, ensure_ascii=False))


def cmd_record_clips(args):
    token = _ensure_token()
    begin = args.begin
    end = args.end
    if not begin or not end:
        print("[ERROR] --begin and --end required (yyyy-MM-dd HH:mm:ss).", file=sys.stderr)
        sys.exit(1)
    if args.local:
        r = query_local_records(
            token,
            args.device_id,
            args.channel_id,
            begin,
            end,
            count=getattr(args, "count", 100),
            base_url=BASE_URL or None,
        )
    elif args.cloud:
        qr = getattr(args, "query_range", "1-100")
        r = query_cloud_records(
            token,
            args.device_id,
            args.channel_id,
            begin,
            end,
            query_range=qr,
            base_url=BASE_URL or None,
        )
    else:
        print("[ERROR] Specify --local or --cloud.", file=sys.stderr)
        sys.exit(1)
    if not r.get("success"):
        print(f"[ERROR] Record clips failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    records = r.get("records", [])
    print(f"[INFO] Found {len(records)} record(s)")
    for rec in records:
        print(json.dumps(rec, ensure_ascii=False))
    if getattr(args, "json", False):
        print(json.dumps({"records": records}, ensure_ascii=False, indent=2))


def cmd_playback_hls(args):
    token = _ensure_token()
    begin = args.begin
    end = args.end
    record_type = getattr(args, "record_type", "localRecord")
    if not begin or not end:
        print("[ERROR] --begin and --end required (yyyy-MM-dd HH:mm:ss).", file=sys.stderr)
        sys.exit(1)
    if record_type not in ("localRecord", "cloudRecord"):
        print("[ERROR] --record-type must be localRecord or cloudRecord.", file=sys.stderr)
        sys.exit(1)
    stream_id = getattr(args, "stream_id", 0)
    if stream_id not in (0, 1):
        stream_id = 0
    r = create_device_record_hls(
        token,
        args.device_id,
        args.channel_id,
        begin,
        end,
        record_type,
        stream_id=stream_id,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] Playback HLS failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    url = r.get("url", "")
    print(url)
    if getattr(args, "json", False):
        print(json.dumps({"url": url}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Imou Device Video – live HLS, record clips, playback HLS.")
    sub = parser.add_subparsers(dest="command", required=True)

    # live
    p_live = sub.add_parser("live", help="Get live HLS URL for device channel.")
    p_live.add_argument("device_id", help="Device serial.")
    p_live.add_argument("channel_id", help="Channel ID (e.g. 0).")
    p_live.add_argument("--stream-id", type=int, default=0, choices=[0, 1], help="0 main, 1 sub (default 0).")
    p_live.add_argument("--json", action="store_true", help="Print JSON with hls key.")
    p_live.set_defaults(func=cmd_live)

    # record-clips
    p_clips = sub.add_parser("record-clips", help="Get local or cloud record clips in time range.")
    p_clips.add_argument("device_id", help="Device serial.")
    p_clips.add_argument("channel_id", help="Channel ID (e.g. 0).")
    p_clips.add_argument("--begin", required=True, help="Start time: yyyy-MM-dd HH:mm:ss")
    p_clips.add_argument("--end", required=True, help="End time: yyyy-MM-dd HH:mm:ss")
    p_clips.add_argument("--local", action="store_true", help="Query local records (queryLocalRecords).")
    p_clips.add_argument("--cloud", action="store_true", help="Query cloud records (queryCloudRecords).")
    p_clips.add_argument("--count", type=int, default=100, help="Max count for local (default 100, max 100).")
    p_clips.add_argument("--query-range", default="1-100", help="Query range for cloud (e.g. 1-100).")
    p_clips.add_argument("--json", action="store_true", help="Print full JSON at end.")
    p_clips.set_defaults(func=cmd_record_clips)

    # playback-hls
    p_play = sub.add_parser("playback-hls", help="Get record playback HLS URL for time range.")
    p_play.add_argument("device_id", help="Device serial.")
    p_play.add_argument("channel_id", help="Channel ID (e.g. 0).")
    p_play.add_argument("--begin", required=True, help="Start time: yyyy-MM-dd HH:mm:ss")
    p_play.add_argument("--end", required=True, help="End time: yyyy-MM-dd HH:mm:ss")
    p_play.add_argument("--record-type", required=True, choices=["localRecord", "cloudRecord"], help="localRecord or cloudRecord.")
    p_play.add_argument("--stream-id", type=int, default=0, choices=[0, 1], help="0 main, 1 sub (default 0).")
    p_play.add_argument("--json", action="store_true", help="Print JSON with url key.")
    p_play.set_defaults(func=cmd_playback_hls)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
