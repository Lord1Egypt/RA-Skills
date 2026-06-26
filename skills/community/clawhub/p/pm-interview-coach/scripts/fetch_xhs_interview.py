#!/usr/bin/env python3
"""
读取小红书面经帖子，提取正文文本和面试题图片
用法: python3 fetch_xhs_interview.py <帖子ID> <xsec_token>
"""
import sys
import json
import urllib.request
import os

def fetch_feed_detail(feed_id, xsec_token):
    mcp_url = "http://localhost:18060/mcp"
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_feed_detail",
            "arguments": {"feed_id": feed_id, "xsec_token": xsec_token}
        },
        "id": 1
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        mcp_url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result.get("result", {})

def download_image(url, output_path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
        return False

def extract_interview_content(feed_detail):
    note = feed_detail.get("data", {}).get("note", {})
    result = {
        "title": note.get("title", ""),
        "desc": note.get("desc", ""),
        "images": []
    }
    for idx, img in enumerate(note.get("imageList", [])):
        url = img.get("urlDefault", "")
        if url:
            result["images"].append({"index": idx + 1, "url": url})
    return result

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 fetch_xhs_interview.py <feed_id> <xsec_token>")
        sys.exit(1)

    feed_id = sys.argv[1]
    xsec_token = sys.argv[2]

    print(f"Fetching feed: {feed_id}", file=sys.stderr)
    result = fetch_feed_detail(feed_id, xsec_token)
    content = extract_interview_content(result)

    print(f"Title: {content['title']}")
    print(f"Description: {content['desc']}")
    print(f"Image count: {len(content['images'])}")

    output_dir = os.path.expanduser("~/.openclaw/workspace/xhs_interview_images")
    os.makedirs(output_dir, exist_ok=True)

    for img in content["images"]:
        idx = img["index"]
        url = img["url"]
        ext = ".webp"
        output_path = os.path.join(output_dir, f"{feed_id}_{idx}{ext}")

        print(f"Downloading image {idx}...", file=sys.stderr)
        if download_image(url, output_path):
            content["images"][idx - 1]["local_path"] = output_path
            print(f"  -> {output_path}")

    print("\n=== JSON ===")
    print(json.dumps(content, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
