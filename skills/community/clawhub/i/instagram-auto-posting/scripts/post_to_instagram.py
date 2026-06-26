"""
Post an image to Instagram Business Account via Meta Graph API.
Two-step: (1) create media container, (2) publish.

Required env vars:
  IG_ACCESS_TOKEN    - Page Access Token from Meta Graph API Explorer
  IG_BUSINESS_ACCOUNT_ID - Numeric IG Business Account ID

Usage:
  python post_to_instagram.py <image_url> <caption>
  python post_to_instagram.py <image_url>          # uses default caption
"""

import urllib.request, urllib.parse, json, os, sys

# === CREDENTIALS (from environment) ===
ACCESS_TOKEN          = os.environ.get("IG_ACCESS_TOKEN", "")
IG_BUSINESS_ACCOUNT_ID = os.environ.get("IG_BUSINESS_ACCOUNT_ID", "")
DEFAULT_CAPTION       = os.environ.get("IG_DEFAULT_CAPTION", "Posted via AI automation.")

def post_to_instagram(image_url, caption=None, access_token=None, ig_account_id=None):
    """
    Post an image to Instagram Business Account.
    Returns (success: bool, post_id: str or None, url: str or None)
    """
    token = access_token or ACCESS_TOKEN
    ig_id = ig_account_id or IG_BUSINESS_ACCOUNT_ID

    if not token:
        return False, None, "IG_ACCESS_TOKEN not set"
    if not ig_id:
        return False, None, "IG_BUSINESS_ACCOUNT_ID not set"

    cap = caption or DEFAULT_CAPTION

    # Step 1: Create media container
    payload1 = json.dumps({"image_url": image_url, "caption": cap}).encode("utf-8")
    req1 = urllib.request.Request(
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        data=payload1,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req1, timeout=30) as r:
            result1 = json.loads(r.read().decode())
            creation_id = result1.get("id")
            if not creation_id:
                return False, None, f"Container creation failed: {result1}"
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        return False, None, f"Container HTTP {e.code}: {body.get('error', {}).get('message', e.reason)}"
    except Exception as e:
        return False, None, f"Container Error: {e}"

    # Step 2: Publish
    payload2 = json.dumps({"creation_id": creation_id}).encode("utf-8")
    req2 = urllib.request.Request(
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        data=payload2,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req2, timeout=30) as r:
            result2 = json.loads(r.read().decode())
            post_id = result2.get("id")
            if post_id:
                url = "https://www.instagram.com/p/" + post_id + "/"
                print(f"[OK] Posted! ID: {post_id}")
                print(f"[OK] URL: {url}")
                return True, post_id, url
            return False, None, f"Publish returned no ID: {result2}"
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        return False, None, f"Publish HTTP {e.code}: {body.get('error', {}).get('message', e.reason)}"
    except Exception as e:
        return False, None, f"Publish Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python post_to_instagram.py <image_url> <caption>")
        print("  image_url: public URL of the image (required)")
        print("  caption:   post caption (optional, uses IG_DEFAULT_CAPTION env var)")
        sys.exit(1)

    image_url = sys.argv[1]
    caption   = sys.argv[2] if len(sys.argv) > 2 else None

    success, post_id, result = post_to_instagram(image_url, caption)
    if success:
        print(f"SUCCESS: {result}")
    else:
        print(f"FAILED: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
