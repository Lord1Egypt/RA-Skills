#!/usr/bin/env python3
import argparse
import json
from _common import acquire_token, graph_headers
import requests
import sys

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def cancel_event(access_token, event_id, reason=None):
    url = f"{GRAPH_BASE}/me/events/{event_id}/cancel"
    payload = {"Comment": reason or "Cancelled by organizer"}
    resp = requests.post(url, headers=graph_headers(access_token), json=payload)
    if resp.status_code >= 300:
        print(f"Error cancelling event: {resp.status_code} {resp.text}")
        sys.exit(1)


def delete_event(access_token, event_id):
    url = f"{GRAPH_BASE}/me/events/{event_id}"
    resp = requests.delete(url, headers=graph_headers(access_token))
    if resp.status_code not in (204, 404):
        print(f"Error deleting event: {resp.status_code} {resp.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Cancel/delete a Microsoft Teams meeting")
    parser.add_argument('--event-id', required=True)
    parser.add_argument('--reason', default=None)
    parser.add_argument('--hard-delete', action='store_true', help='After cancel, delete the event from calendar')
    args = parser.parse_args()

    access_token, _ = acquire_token()

    cancel_event(access_token, args.event_id, args.reason)
    if args.hard_delete:
        delete_event(access_token, args.event_id)

    print(json.dumps({"status": "cancelled", "event_id": args.event_id, "deleted": bool(args.hard_delete)}))


if __name__ == '__main__':
    main()
