#!/usr/bin/env python3
"""Gmail API — search and read emails via domain-wide delegation."""

import argparse
import base64
import json
import re
import sys
from typing import Optional

from auth import get_service


def search_messages(
    user: str,
    query: str,
    max_results: int = 10,
) -> dict:
    """Search a user's Gmail inbox.

    Args:
        user: Email address to search (impersonated via DWD).
        query: Gmail search query (from:, to:, subject:, newer_than:, etc).
        max_results: Max messages to return (default 10).

    Returns:
        Dict with message list (id, threadId).
    """
    service = get_service("gmail", impersonate=user)
    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])
    total = results.get("resultSizeEstimate", 0)

    return {
        "user": user,
        "query": query,
        "total_estimate": total,
        "returned": len(messages),
        "messages": messages,
    }


def get_message(
    user: str,
    message_id: str,
    format: str = "full",
) -> dict:
    """Get a single email message with full content.

    Args:
        user: Email address (impersonated via DWD).
        message_id: Gmail message ID.
        format: 'full', 'metadata', or 'minimal'.

    Returns:
        Parsed message dict with headers and body.
    """
    service = get_service("gmail", impersonate=user)
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format=format,
    ).execute()

    return _parse_message(msg)


def get_message_raw(
    user: str,
    message_id: str,
) -> dict:
    """Get raw message metadata without parsing body (faster).

    Args:
        user: Email address (impersonated via DWD).
        message_id: Gmail message ID.

    Returns:
        Message metadata dict.
    """
    service = get_service("gmail", impersonate=user)
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["From", "To", "Subject", "Date", "Cc", "Bcc"],
    ).execute()

    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "cc": headers.get("Cc", ""),
        "bcc": headers.get("Bcc", ""),
        "subject": headers.get("Subject", ""),
        "date": headers.get("Date", ""),
        "snippet": msg.get("snippet", ""),
        "labelIds": msg.get("labelIds", []),
    }


def search_and_summarize(
    user: str,
    query: str,
    max_results: int = 10,
) -> dict:
    """Search and return metadata summary for each result.

    Args:
        user: Email address to search.
        query: Gmail search query.
        max_results: Max messages to return.

    Returns:
        Dict with message summaries (from, to, subject, date, snippet).
    """
    search = search_messages(user, query, max_results)
    messages = search.get("messages", [])

    if not messages:
        return {
            "user": user,
            "query": query,
            "total_estimate": search.get("total_estimate", 0),
            "results": [],
        }

    service = get_service("gmail", impersonate=user)
    results = []

    for msg in messages:
        detail = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "To", "Subject", "Date"],
        ).execute()

        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        results.append({
            "id": msg["id"],
            "threadId": msg["threadId"],
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "snippet": detail.get("snippet", ""),
        })

    return {
        "user": user,
        "query": query,
        "total_estimate": search.get("total_estimate", 0),
        "returned": len(results),
        "results": results,
    }


def search_and_read(
    user: str,
    query: str,
    max_results: int = 5,
) -> dict:
    """Search and return full content for each result.

    Args:
        user: Email address to search.
        query: Gmail search query.
        max_results: Max messages to return (default 5 — full content is heavy).

    Returns:
        Dict with full message content.
    """
    search = search_messages(user, query, max_results)
    messages = search.get("messages", [])

    if not messages:
        return {
            "user": user,
            "query": query,
            "total_estimate": search.get("total_estimate", 0),
            "results": [],
        }

    results = []
    for msg in messages:
        parsed = get_message(user, msg["id"])
        results.append(parsed)

    return {
        "user": user,
        "query": query,
        "total_estimate": search.get("total_estimate", 0),
        "returned": len(results),
        "results": results,
    }


def _parse_message(msg: dict) -> dict:
    """Parse a Gmail message into a clean dict with headers and body text."""
    payload = msg.get("payload", {})
    headers = {h["name"]: h["value"] for h in payload.get("headers", [])}

    body_text = _extract_body(payload)

    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "cc": headers.get("Cc", ""),
        "bcc": headers.get("Bcc", ""),
        "subject": headers.get("Subject", ""),
        "date": headers.get("Date", ""),
        "snippet": msg.get("snippet", ""),
        "labelIds": msg.get("labelIds", []),
        "body": body_text,
        "has_attachments": _has_attachments(payload),
    }


def _extract_body(payload: dict) -> str:
    """Extract plain text body from message payload, handling multipart."""
    mime_type = payload.get("mimeType", "")

    # Direct body
    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Multipart — look for text/plain first, fall back to text/html
    parts = payload.get("parts", [])
    plain_text = ""
    html_text = ""

    for part in parts:
        part_mime = part.get("mimeType", "")
        if part_mime == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                plain_text = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        elif part_mime == "text/html":
            data = part.get("body", {}).get("data", "")
            if data:
                html_text = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                # Strip HTML tags for readable output
                html_text = re.sub(r"<[^>]+>", "", html_text)
                html_text = re.sub(r"\s+", " ", html_text).strip()
        elif part_mime.startswith("multipart/"):
            # Recurse into nested multipart
            nested = _extract_body(part)
            if nested:
                plain_text = plain_text or nested

    return plain_text or html_text or ""


def _has_attachments(payload: dict) -> bool:
    """Check if message has attachments."""
    parts = payload.get("parts", [])
    for part in parts:
        if part.get("filename"):
            return True
        if part.get("mimeType", "").startswith("multipart/"):
            if _has_attachments(part):
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Gmail search and read")
    parser.add_argument("--user", required=True, help="Email address to search")
    parser.add_argument("--query", required=True, help="Gmail search query")
    parser.add_argument("--max", type=int, default=10, help="Max results (default 10)")
    parser.add_argument("--mode", choices=["summary", "full", "read"], default="summary",
                        help="summary=metadata only, full=with body, read=single message by ID")
    parser.add_argument("--message-id", help="Message ID (for --mode read)")
    args = parser.parse_args()

    try:
        if args.mode == "read":
            if not args.message_id:
                print(json.dumps({"error": "--message-id required for --mode read"}))
                sys.exit(1)
            result = get_message(args.user, args.message_id)
        elif args.mode == "full":
            result = search_and_read(args.user, args.query, args.max)
        else:
            result = search_and_summarize(args.user, args.query, args.max)

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
