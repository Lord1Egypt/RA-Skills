#!/usr/bin/env python3
"""
Memories.ai API Helper Script
Usage:
  python memories_api.py transcript <platform> <url>     # Sync transcript
  python memories_api.py mai <platform> <url>            # Async MAI transcript
  python memories_api.py metadata <platform> <video_id>  # Video metadata
  python memories_api.py comments <platform> <video_id>  # Video comments
  
Platforms: youtube, tiktok, instagram, twitter
"""

import sys
import json
import requests
import os

# API Configuration
BASE_URL = "https://mavi-backend.memories.ai/serve/api/v2"

def get_api_key():
    """Get API key from environment or TOOLS.md"""
    if os.environ.get("MEMORIES_API_KEY"):
        return os.environ["MEMORIES_API_KEY"]
    # Default key from TOOLS.md
    return "sk-mavi-mjLNMGVXHt52ZPvEIkx5QrsQEv6Z52GjvXa0MISOgAP5ckMGBzybxfMH9B-1tvUNFhbmDlI8juoFtJjoQJQMhwno9qDBidAblsfJMwL1NTiAqtSYgXnZKrD-uWxHFWkZ"

HEADERS = {
    "Authorization": get_api_key(),
    "Content-Type": "application/json"
}

def transcript(platform: str, video_url: str):
    """Get simple audio transcript (sync)"""
    url = f"{BASE_URL}/{platform}/video/transcript"
    data = {"video_url": video_url}
    if platform == "youtube":
        data["channel"] = "rapid"
    
    resp = requests.post(url, headers=HEADERS, json=data, timeout=30)
    return resp.json()

DEFAULT_WEBHOOK = "https://demo.memories-ai.org/webhooks/memories/callback"

def mai_transcript(platform: str, video_url: str, callback_url: str = None):
    """Submit MAI transcript task (async)"""
    url = f"{BASE_URL}/{platform}/video/mai/transcript"
    data = {"video_url": video_url}
    # Use default webhook if not specified
    data["callback_url"] = callback_url or DEFAULT_WEBHOOK
    
    resp = requests.post(url, headers=HEADERS, json=data, timeout=30)
    return resp.json()

def metadata(platform: str, video_id: str):
    """Get video metadata"""
    url = f"{BASE_URL}/{platform}/video/detail"
    data = {"video_id": video_id}
    
    resp = requests.post(url, headers=HEADERS, json=data, timeout=30)
    return resp.json()

def comments(platform: str, video_id: str, limit: int = 100):
    """Get video comments"""
    url = f"{BASE_URL}/{platform}/video/comment"
    data = {"video_id": video_id, "limit": limit}
    
    resp = requests.post(url, headers=HEADERS, json=data, timeout=30)
    return resp.json()

def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    
    action = sys.argv[1]
    platform = sys.argv[2].lower()
    target = sys.argv[3]
    
    if platform not in ["youtube", "tiktok", "instagram", "twitter"]:
        print(f"Error: Unknown platform '{platform}'")
        print("Supported: youtube, tiktok, instagram, twitter")
        sys.exit(1)
    
    if action == "transcript":
        result = transcript(platform, target)
    elif action == "mai":
        callback = sys.argv[4] if len(sys.argv) > 4 else None
        result = mai_transcript(platform, target, callback)
    elif action == "metadata":
        result = metadata(platform, target)
    elif action == "comments":
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        result = comments(platform, target, limit)
    else:
        print(f"Error: Unknown action '{action}'")
        print("Supported: transcript, mai, metadata, comments")
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
