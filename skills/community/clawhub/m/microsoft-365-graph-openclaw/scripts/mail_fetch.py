#!/usr/bin/env python3
"""List or fetch Outlook email via Microsoft Graph."""
import argparse
import json

from utils import append_log, authorized_request, graph_url, cli_main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List or fetch Outlook messages via Microsoft Graph.")
    parser.add_argument("--folder", default="Inbox", help="Mailbox folder name.")
    parser.add_argument("--top", type=int, default=25, help="Maximum number of messages.")
    parser.add_argument("--filter", help="Custom OData filter expression.")
    parser.add_argument("--from", dest="from_addr", help="Filter by sender email address.")
    parser.add_argument("--subject", help="Filter by subject snippet.")
    parser.add_argument("--unread", action="store_true", help="Return only unread messages.")
    parser.add_argument("--select", nargs="*", help="Specific fields to return (default: summary fields).")
    parser.add_argument("--id", help="Fetch a specific message by ID.")
    parser.add_argument("--include-body", action="store_true", help="Include full message body in output.")
    parser.add_argument("--mark-read", action="store_true", help="Mark message passed with --id as read.")
    parser.add_argument("--move-to", help="Move message passed with --id to destination folder ID.")
    return parser


def handler():
    parser = build_parser()
    args = parser.parse_args()
    if args.id:
        result = fetch_single(args)
    else:
        result = list_messages(args)
    print(json.dumps(result, indent=2))


def list_messages(args: argparse.Namespace) -> dict:
    params = {"$top": args.top}
    selects = args.select or [
        "id",
        "receivedDateTime",
        "subject",
        "from",
        "toRecipients",
        "isRead",
        "hasAttachments",
    ]
    params["$select"] = ",".join(selects)
    filters = []
    if args.filter:
        filters.append(f"({args.filter})")
    if args.from_addr:
        filters.append(f"from/emailAddress/address eq '{args.from_addr}'")
    if args.subject:
        filters.append(f"contains(subject,'{args.subject}')")
    if args.unread:
        filters.append("isRead eq false")
    if filters:
        params["$filter"] = " and ".join(filters)
    path = f"/me/mailFolders('{args.folder}')/messages"
    resp = authorized_request("GET", graph_url(path), params=params)
    data = resp.json()
    append_log({"action": "mail_list", "folder": args.folder, "count": len(data.get('value', []))})
    return data


def fetch_single(args: argparse.Namespace) -> dict:
    select_fields = args.select
    params = {"$select": ",".join(select_fields)} if select_fields else {}
    if args.include_body and select_fields:
        if "body" not in select_fields:
            select_fields.append("body")
            params["$select"] = ",".join(select_fields)
    elif args.include_body and not select_fields:
        params["$select"] = "body,subject,from,receivedDateTime,toRecipients,ccRecipients"
    resp = authorized_request("GET", graph_url(f"/me/messages/{args.id}"), params=params)
    message = resp.json()
    if args.mark_read:
        authorized_request("PATCH", graph_url(f"/me/messages/{args.id}"), json={"isRead": True})
        message["isRead"] = True
    if args.move_to:
        move_resp = authorized_request(
            "POST",
            graph_url(f"/me/messages/{args.id}/move"),
            json={"destinationId": args.move_to},
        )
        message["movedTo"] = move_resp.json().get("id")
    append_log({"action": "mail_get", "id": args.id, "markRead": args.mark_read, "move": args.move_to})
    return message


if __name__ == "__main__":
    cli_main(handler)
