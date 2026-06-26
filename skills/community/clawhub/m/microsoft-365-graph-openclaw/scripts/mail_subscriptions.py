#!/usr/bin/env python3
"""Manage Microsoft Graph mail change notification subscriptions."""
import argparse
import json
from datetime import datetime, timedelta, timezone

from utils import append_log, authorized_request, cli_main, graph_url

MAX_MAIL_SUBSCRIPTION_MINUTES = 4230
DEFAULT_SUBSCRIPTION_MINUTES = 4200
DEFAULT_RESOURCE = "me/messages"
DEFAULT_CHANGE_TYPE = "created"


def _iso_utc_after(minutes: int) -> str:
    dt = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _clamp_expiration(minutes: int) -> int:
    if minutes <= 0:
        raise ValueError("Minutes must be > 0")
    return min(minutes, MAX_MAIL_SUBSCRIPTION_MINUTES)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Graph mail subscriptions.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a mail subscription.")
    p_create.add_argument("--notification-url", required=True, help="Public HTTPS webhook URL.")
    p_create.add_argument("--client-state", required=True, help="Client state secret for webhook validation.")
    p_create.add_argument("--minutes", type=int, default=DEFAULT_SUBSCRIPTION_MINUTES, help="Validity in minutes.")
    p_create.add_argument(
        "--resource",
        default=DEFAULT_RESOURCE,
        help="Graph resource path (default me/messages; Inbox-scoped resources can miss some deliveries).",
    )
    p_create.add_argument("--change-type", default=DEFAULT_CHANGE_TYPE, help="Graph change type.")
    p_create.add_argument(
        "--lifecycle-notification-url",
        help="Optional lifecycle URL for reauthorization events.",
    )

    p_status = sub.add_parser("status", help="Get one subscription by id.")
    p_status.add_argument("--id", required=True, help="Subscription ID.")

    p_renew = sub.add_parser("renew", help="Renew one subscription by id.")
    p_renew.add_argument("--id", required=True, help="Subscription ID.")
    p_renew.add_argument("--minutes", type=int, default=DEFAULT_SUBSCRIPTION_MINUTES, help="New validity in minutes.")

    p_delete = sub.add_parser("delete", help="Delete one subscription by id.")
    p_delete.add_argument("--id", required=True, help="Subscription ID.")

    p_list = sub.add_parser("list", help="List active subscriptions.")
    p_list.add_argument("--top", type=int, default=50, help="Max results.")

    return parser


def handle_create(args: argparse.Namespace) -> None:
    minutes = _clamp_expiration(args.minutes)
    payload = {
        "changeType": args.change_type,
        "notificationUrl": args.notification_url,
        "resource": args.resource,
        "expirationDateTime": _iso_utc_after(minutes),
        "clientState": args.client_state,
    }
    if args.lifecycle_notification_url:
        payload["lifecycleNotificationUrl"] = args.lifecycle_notification_url

    resp = authorized_request("POST", graph_url("/subscriptions"), json=payload)
    body = resp.json()
    append_log({"op": "mail_subscription_create", "id": body.get("id"), "resource": body.get("resource")})
    print(json.dumps(body, indent=2))


def handle_status(args: argparse.Namespace) -> None:
    resp = authorized_request("GET", graph_url(f"/subscriptions/{args.id}"))
    print(json.dumps(resp.json(), indent=2))


def handle_renew(args: argparse.Namespace) -> None:
    minutes = _clamp_expiration(args.minutes)
    payload = {"expirationDateTime": _iso_utc_after(minutes)}
    resp = authorized_request("PATCH", graph_url(f"/subscriptions/{args.id}"), json=payload)
    body = resp.json() if resp.text else {"status": "renewed", "id": args.id}
    append_log({"op": "mail_subscription_renew", "id": args.id, "minutes": minutes})
    print(json.dumps(body, indent=2))


def handle_delete(args: argparse.Namespace) -> None:
    authorized_request("DELETE", graph_url(f"/subscriptions/{args.id}"))
    append_log({"op": "mail_subscription_delete", "id": args.id})
    print(json.dumps({"status": "deleted", "id": args.id}, indent=2))


def handle_list(args: argparse.Namespace) -> None:
    # /subscriptions does not support $top; trim client-side for predictable output.
    resp = authorized_request("GET", graph_url("/subscriptions"))
    body = resp.json()
    values = body.get("value")
    if isinstance(values, list):
        body["value"] = values[: args.top]
    print(json.dumps(body, indent=2))


def handler() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "create":
        handle_create(args)
    elif args.command == "status":
        handle_status(args)
    elif args.command == "renew":
        handle_renew(args)
    elif args.command == "delete":
        handle_delete(args)
    elif args.command == "list":
        handle_list(args)


if __name__ == "__main__":
    cli_main(handler)
