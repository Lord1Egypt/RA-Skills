#!/usr/bin/env python3
"""ShopGeni skill helper — calls the unified shopping SSE endpoint.

Supports text-only and multipart (image) modes.
Prints a single JSON object to stdout on completion.
"""

import argparse
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

TIMEOUT = 90


def parse_args():
    p = argparse.ArgumentParser(description="ShopGeni shopping assistant")
    p.add_argument("--query", default="", help="Natural language query")
    p.add_argument("--api-url", default=os.getenv("SHOPGENI_API_URL", "https://nestor-api.beyondstyle.us"), help="ShopGeni API base URL")
    p.add_argument("--image", default=None, help="Path to image file for visual search")
    p.add_argument("--thread-id", default=None, help="Thread ID for follow-up queries")
    p.add_argument("--image-url", default=None, help="Product image URL for image-based price comparison")
    return p.parse_args()


def new_uid():
    return str(uuid.uuid4())


def get_client_id() -> str:
    """Return a stable per-installation ID used for rate limiting (analogous to browser fingerprint)."""
    id_file = Path.home() / ".config" / "nestor" / "skill_id"
    id_file.parent.mkdir(parents=True, exist_ok=True)
    if id_file.exists():
        return id_file.read_text().strip()
    client_id = str(uuid.uuid4())
    id_file.write_text(client_id)
    return client_id


def build_multipart(fields, files, boundary):
    """Build a multipart/form-data body.

    fields: list of (name, value) text tuples
    files:  list of (name, filename, mime_type, data_bytes) tuples
    """
    body = b""
    sep = ("--" + boundary + "\r\n").encode()
    for name, value in fields:
        body += sep
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += value.encode() + b"\r\n"
    for name, filename, mime_type, data in files:
        body += sep
        body += (
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode()
        body += data + b"\r\n"
    body += ("--" + boundary + "--\r\n").encode()
    return body


def read_sse(response):
    """Parse SSE stream, return first 'complete' or 'error' event data dict."""
    buffer = b""
    while True:
        chunk = response.read(4096)
        if not chunk:
            break
        buffer += chunk
        lines = buffer.split(b"\n")
        buffer = lines[-1]  # keep incomplete line
        for line in lines[:-1]:
            line = line.strip()
            if not line.startswith(b"data:"):
                continue
            raw = line[len(b"data:"):].strip()
            if not raw or raw == b"[DONE]":
                continue
            try:
                event = json.loads(raw)
            except json.JSONDecodeError:
                continue
            event_type = event.get("type", "")
            if event_type == "complete":
                return event
            if event_type == "error":
                return event
    return None


def extract_result(event):
    """Normalise the SSE complete event into a clean output dict."""
    if event is None:
        return {"error": "No complete event received from server"}

    if event.get("type") == "error":
        return {"error": event.get("message", "Unknown error from server")}

    data = event.get("data", event)
    result = {
        "intent": data.get("intent", ""),
        "content": data.get("content", ""),
        "thread_id": data.get("thread_id", ""),
        "recommendations": data.get("recommendations", []),
        "price_comparison": data.get("price_comparison", {}),
    }
    return result


def call_text(api_url, query, thread_id):
    payload = json.dumps({"user_input": query, "thread_id": thread_id}).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Nst-Uid": new_uid(),
        "X-Nst-Sig": get_client_id(),
        "X-Nst-Source": "skill",
        "Accept": "text/event-stream",
    }
    url = api_url.rstrip("/") + "/api/unified-shopping/stream"
    req = Request(url, data=payload, headers=headers, method="POST")
    return urlopen(req, timeout=TIMEOUT)


def call_image(api_url, query, thread_id, image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()

    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    boundary = uuid.uuid4().hex
    fields = [
        ("user_input", query or "find best prices for this product"),
        ("thread_id", thread_id),
    ]
    files = [(
        "image",
        os.path.basename(image_path),
        mime_type,
        image_data,
    )]
    body = build_multipart(fields, files, boundary)

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "X-Nst-Uid": new_uid(),
        "X-Nst-Sig": get_client_id(),
        "X-Nst-Source": "skill",
        "Accept": "text/event-stream",
    }
    url = api_url.rstrip("/") + "/api/unified-shopping/stream"
    req = Request(url, data=body, headers=headers, method="POST")
    return urlopen(req, timeout=TIMEOUT)


def main():
    args = parse_args()
    thread_id = args.thread_id or new_uid()

    query = args.query
    if args.image_url:
        query = f"{query}\nObjective product image: {args.image_url}".strip()

    try:
        if args.image:
            if not os.path.isfile(args.image):
                print(json.dumps({"error": f"Image file not found: {args.image}"}))
                sys.exit(1)
            response = call_image(args.api_url, query, thread_id, args.image)
        else:
            if not query:
                print(json.dumps({"error": "--query is required when --image is not provided"}))
                sys.exit(1)
            response = call_text(args.api_url, query, thread_id)

        event = read_sse(response)
        result = extract_result(event)

    except HTTPError as e:
        body = e.read().decode(errors="replace")
        result = {"error": f"HTTP {e.code}: {body}"}
    except URLError as e:
        result = {"error": f"Connection error: {e.reason}"}
    except FileNotFoundError as e:
        result = {"error": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1 if "error" in result else 0)


if __name__ == "__main__":
    main()
