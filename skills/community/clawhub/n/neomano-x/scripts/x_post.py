#!/usr/bin/env python3
"""Post to X (Twitter) with optional image using OAuth 1.0a.

Commands:
  dry-run  --text ... --image /path.jpg
  publish  --text ... --image /path.jpg

Env (required for publish):
  X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
"""

import argparse
import json
import os
import sys
from pathlib import Path


def require_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise SystemExit(f"ERROR: missing env {name}")
    return v


def build_oauth1():
    from requests_oauthlib import OAuth1

    return OAuth1(
        client_key=require_env("X_API_KEY"),
        client_secret=require_env("X_API_SECRET"),
        resource_owner_key=require_env("X_ACCESS_TOKEN"),
        resource_owner_secret=require_env("X_ACCESS_TOKEN_SECRET"),
    )


def upload_media(image_path: Path, oauth) -> str:
    import requests

    url = "https://upload.twitter.com/1.1/media/upload.json"
    with image_path.open("rb") as f:
        files = {"media": f}
        r = requests.post(url, auth=oauth, files=files, timeout=120)
    if r.status_code >= 300:
        raise SystemExit(f"ERROR: media upload failed: {r.status_code} {r.text}")
    data = r.json()
    media_id = data.get("media_id_string") or str(data.get("media_id"))
    if not media_id:
        raise SystemExit(f"ERROR: media upload returned no media_id: {data}")
    return media_id


def create_tweet(text: str, media_id: str | None, oauth) -> dict:
    import requests

    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}
    if media_id:
        payload["media"] = {"media_ids": [media_id]}
    r = requests.post(url, auth=oauth, json=payload, timeout=120)
    if r.status_code >= 300:
        raise SystemExit(f"ERROR: tweet create failed: {r.status_code} {r.text}")
    return r.json()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["dry-run", "publish"])
    ap.add_argument("--text", required=True)
    ap.add_argument("--image", required=False)
    args = ap.parse_args()

    text = args.text.strip()
    image_path = Path(args.image).expanduser() if args.image else None
    if image_path and not image_path.exists():
        raise SystemExit(f"ERROR: image not found: {image_path}")

    if args.command == "dry-run":
        out = {
            "ok": True,
            "mode": "dry-run",
            "text": text,
            "image": str(image_path) if image_path else None,
            "note": "Not published. Use 'publish' to post.",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    # publish
    oauth = build_oauth1()
    media_id = upload_media(image_path, oauth) if image_path else None
    result = create_tweet(text, media_id, oauth)
    print(json.dumps({"ok": True, "mode": "publish", "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
