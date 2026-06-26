#!/usr/bin/env python3
"""
Google Business Profile Review Manager for OpenClaw
----------------------------------------------------
Polls for unanswered reviews and posts approved replies.

Usage:
  python3 gbp_reviews.py check --client <client_id>
  python3 gbp_reviews.py reply --client <client_id> --review <review_id> --reply "Your response text"

Requires:
  pip install google-auth google-auth-oauthlib requests

Config:
  Each client has a JSON file in ./clients/<client_id>.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

try:
    import requests
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
except ImportError:
    print("Missing dependencies. Run:")
    print("  pip install google-auth google-auth-oauthlib requests")
    sys.exit(1)


# --- Paths ---
SCRIPT_DIR = Path(__file__).parent.resolve()
CLIENTS_DIR = SCRIPT_DIR / "clients"
PENDING_DIR = SCRIPT_DIR / "pending"
LOG_FILE = SCRIPT_DIR / "review_log.json"


def load_client_config(client_id: str) -> dict:
    """Load client config from clients/<client_id>.json"""
    config_path = CLIENTS_DIR / f"{client_id}.json"
    if not config_path.exists():
        print(f"Error: Client config not found at {config_path}")
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)


def get_access_token(config: dict) -> str:
    """Get a valid access token using the stored refresh token."""
    creds = Credentials(
        token=None,
        refresh_token=config["refresh_token"],
        client_id=config["oauth_client_id"],
        client_secret=config["oauth_client_secret"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    creds.refresh(Request())
    return creds.token


def load_review_log() -> dict:
    """Load the log of reviews we've already processed."""
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return {}


def save_review_log(log: dict):
    """Save the review processing log."""
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def save_pending_review(client_id: str, review: dict):
    """Save a review to the pending folder for your OpenClaw agent to process."""
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    review_id = review["reviewId"]
    pending_file = PENDING_DIR / f"{client_id}_{review_id}.json"
    with open(pending_file, "w") as f:
        json.dump({
            "client_id": client_id,
            "review_id": review_id,
            "reviewer_name": review.get("reviewer", {}).get("displayName", "A customer"),
            "star_rating": review.get("starRating", "UNKNOWN"),
            "comment": review.get("comment", "(no comment)"),
            "create_time": review.get("createTime", ""),
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2)
    return pending_file


def check_reviews(client_id: str):
    """Poll for new unanswered reviews and save them as pending."""
    config = load_client_config(client_id)
    token = get_access_token(config)
    account_id = config["account_id"]
    location_id = config["location_id"]

    # Google Business Profile API v4 endpoint
    url = (
        f"https://mybusiness.googleapis.com/v4/"
        f"accounts/{account_id}/locations/{location_id}/reviews"
    )
    headers = {"Authorization": f"Bearer {token}"}
    params = {"pageSize": 50, "orderBy": "updateTime desc"}

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print(f"API error ({resp.status_code}): {resp.text}")
        sys.exit(1)

    data = resp.json()
    reviews = data.get("reviews", [])
    log = load_review_log()
    new_count = 0

    for review in reviews:
        review_id = review.get("reviewId", "")
        has_reply = review.get("reviewReply") is not None
        already_seen = review_id in log

        if not has_reply and not already_seen:
            # New unanswered review
            pending_file = save_pending_review(client_id, review)
            log[review_id] = {
                "client_id": client_id,
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "status": "pending_approval",
            }
            new_count += 1

            # Output for your OpenClaw agent to read
            star = review.get("starRating", "UNKNOWN")
            name = review.get("reviewer", {}).get("displayName", "A customer")
            comment = review.get("comment", "(no comment)")
            print(f"\n--- NEW REVIEW ({client_id}) ---")
            print(f"Review ID: {review_id}")
            print(f"From: {name}")
            print(f"Rating: {star}")
            print(f"Comment: {comment}")
            print(f"Saved to: {pending_file}")

    save_review_log(log)

    if new_count == 0:
        print(f"No new unanswered reviews for client '{client_id}'.")
    else:
        print(f"\nFound {new_count} new unanswered review(s) for client '{client_id}'.")


def post_reply(client_id: str, review_id: str, reply_text: str):
    """Post an approved reply to a specific review."""
    config = load_client_config(client_id)
    token = get_access_token(config)
    account_id = config["account_id"]
    location_id = config["location_id"]

    url = (
        f"https://mybusiness.googleapis.com/v4/"
        f"accounts/{account_id}/locations/{location_id}/"
        f"reviews/{review_id}/reply"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {"comment": reply_text}

    resp = requests.put(url, headers=headers, json=body)
    if resp.status_code in (200, 201):
        print(f"Reply posted successfully to review {review_id}.")
        # Update log
        log = load_review_log()
        if review_id in log:
            log[review_id]["status"] = "replied"
            log[review_id]["replied_at"] = datetime.now(timezone.utc).isoformat()
            save_review_log(log)
        # Remove pending file
        pending_file = PENDING_DIR / f"{client_id}_{review_id}.json"
        if pending_file.exists():
            pending_file.unlink()
    else:
        print(f"Failed to post reply ({resp.status_code}): {resp.text}")
        sys.exit(1)


def list_pending():
    """List all pending reviews awaiting approval."""
    if not PENDING_DIR.exists():
        print("No pending reviews.")
        return
    files = sorted(PENDING_DIR.glob("*.json"))
    if not files:
        print("No pending reviews.")
        return
    print(f"Found {len(files)} pending review(s):\n")
    for f in files:
        with open(f) as fh:
            data = json.load(fh)
        print(f"  Client: {data['client_id']}")
        print(f"  Review: {data['review_id']}")
        print(f"  From: {data['reviewer_name']} ({data['star_rating']})")
        print(f"  Comment: {data['comment'][:120]}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Google Business Profile Review Manager")
    sub = parser.add_subparsers(dest="command")

    # check command
    check_p = sub.add_parser("check", help="Poll for new unanswered reviews")
    check_p.add_argument("--client", required=True, help="Client ID")

    # reply command
    reply_p = sub.add_parser("reply", help="Post an approved reply")
    reply_p.add_argument("--client", required=True, help="Client ID")
    reply_p.add_argument("--review", required=True, help="Review ID")
    reply_p.add_argument("--reply", required=True, help="Reply text to post")

    # pending command
    sub.add_parser("pending", help="List all pending reviews")

    args = parser.parse_args()

    if args.command == "check":
        check_reviews(args.client)
    elif args.command == "reply":
        post_reply(args.client, args.review, args.reply)
    elif args.command == "pending":
        list_pending()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
