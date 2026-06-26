#!/usr/bin/env python3
"""
PopAI PPT Generator
Generates presentations via PopAI API.
Supports optional local file upload (max 5).
"""

import os
import sys
import json
import hashlib
import mimetypes
import argparse
from concurrent.futures import ThreadPoolExecutor
import requests

BASE_URL = "https://api.popai.pro/api/v1/chat"
PRESIGN_URL = "https://api.popai.pro/py/api/v1/chat/getPresignedPost"
S3_UPLOAD_URL = "https://popai-file.s3-accelerate.amazonaws.com/"
S3_BUCKET = "popai-file"

COMMON_HEADERS = {
    "app-name": "popai-skill",
    "content-type": "application/json",
    "origin": "https://www.popai.pro",
    "referer": "https://www.popai.pro/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
}


def _headers(api_key, accept="application/json"):
    return {**COMMON_HEADERS, "authorization": api_key, "accept": accept}


def _file_ext(filename):
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower() if ext else ""


def _file_md5(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def upload_file(api_key, file_path):
    """Upload a local file to S3 via presigned POST. Returns file info dict."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    md5 = _file_md5(file_path)
    key = f"f/{md5}/{filename}"
    file_url = f"{S3_UPLOAD_URL}{key}"
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    # Get presigned post
    resp = requests.post(
        PRESIGN_URL,
        headers=_headers(api_key),
        json={"md5": md5, "bucket": S3_BUCKET, "prefix": key, "contentType": content_type},
    )
    resp.raise_for_status()
    fields = (resp.json().get("data") or {}).get("fields") or {}
    if not isinstance(fields, dict) or not fields.get("policy"):
        raise RuntimeError(f"Invalid presign response: {resp.text[:500]}")

    # Upload to S3
    with open(file_path, "rb") as f:
        upload_resp = requests.post(
            S3_UPLOAD_URL,
            files={"file": (filename, f, content_type)},
            data={
                "Content-Type": content_type,
                "key": fields.get("key") or key,
                "AWSAccessKeyId": fields["AWSAccessKeyId"],
                "policy": fields["policy"],
                "signature": fields["signature"],
            },
        )
    if upload_resp.status_code not in (200, 201, 204):
        raise RuntimeError(f"S3 upload failed ({upload_resp.status_code}): {upload_resp.text[:500]}")

    return {"md5": md5, "filename": filename, "extname": _file_ext(filename), "url": file_url}


def create_channel(api_key, message, file_infos=None):
    """Create channel and get channelId. Does NOT trigger generation."""
    payload = {
        "templateId": "900012",
        "message": message,
        "advanceConfig": {"pptx": "layout"},
    }
    if file_infos:
        payload["docs"] = [
            {"md5": fi["md5"], "filename": fi["filename"], "extname": fi["extname"],
             "pageCount": "1", "url": fi["url"]}
            for fi in file_infos
        ]
        payload["chatType"] = "PptAgentMultiFile"
        payload["isUploadToEnhance"] = True

    print(f"getChannel payload: {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
    resp = requests.post(f"{BASE_URL}/getChannel", headers=_headers(api_key), json=payload)
    resp.raise_for_status()
    channel_id = (resp.json().get("data") or {}).get("channelId")
    if not channel_id:
        raise RuntimeError(f"Failed to get channelId: {resp.text[:500]}")
    return channel_id


def parse_sse_event(data_list):
    """Parse SSE data payload, extract tool results, summary, pptx_ready, task, error events.

    Event types handled:
    - TOOL_CALLS-update_task_list  → task progress
    - TOOL_CALLS-wide_web_search   → search results with ragList
    - TOOL_CALLS-pptx / nodeId=pptx → final pptx download
    - NODE_END                      → final summary text
    - MESSAGE_THINK-*-cot           → skip (internal COT)
    - MESSAGE_THINK-*-content-cot   → skip (content thinking)
    - pong / agentEvent=null        → skip
    """
    if not isinstance(data_list, list):
        return []

    results = []
    for item in data_list:
        if not isinstance(item, dict) or item.get("type") == "pong":
            continue

        is_last = item.get("last", False)

        agent_event_str = item.get("agentEvent")
        if agent_event_str and agent_event_str != "null":
            try:
                ae = json.loads(agent_event_str) if isinstance(agent_event_str, str) else agent_event_str
                if not isinstance(ae, dict):
                    ae = {}
                event_type = ae.get("event") or ""
                msg = ae.get("message") or {}
                if not isinstance(msg, dict):
                    msg = {}
                action = msg.get("action") or ""
                param = msg.get("param") or ""

                # Skip COT thinking events
                if "cot" in event_type.lower():
                    pass

                # Task list updates
                elif "update_task_list" in event_type:
                    try:
                        tasks = json.loads(param) if isinstance(param, str) else param
                        todos = (tasks[0] if isinstance(tasks, list) and tasks else {}).get("todos") or []
                        for t in todos:
                            if isinstance(t, dict):
                                results.append({"type": "task", "id": t.get("id", ""),
                                                "content": t.get("content", ""), "status": t.get("status", "")})
                    except (json.JSONDecodeError, TypeError, IndexError, AttributeError):
                        pass

                # Web search — extract ragList results
                elif "web_search" in event_type:
                    rag_list = ae.get("ragList") or []
                    search_results = []
                    if isinstance(rag_list, list):
                        for r in rag_list:
                            if isinstance(r, dict) and r.get("title"):
                                search_results.append({
                                    "title": r.get("title", ""),
                                    "url": r.get("url", ""),
                                    "snippet": (r.get("snippet") or "")[:200],
                                    "date": r.get("date_published") or "",
                                })
                    results.append({
                        "type": "search",
                        "action": action,
                        "results": search_results if search_results else None,
                        "snippet": (param or "")[:500] if not search_results else None,
                    })

                # PPTX ready — extract download URL and preview images
                elif event_type == "TOOL_CALLS-pptx" or ae.get("nodeId") == "pptx":
                    media_str = ae.get("media") or ""
                    try:
                        media_list = json.loads(media_str) if isinstance(media_str, str) else media_str
                        if isinstance(media_list, list) and media_list and isinstance(media_list[0], dict):
                            m = media_list[0]
                            img_list = m.get("imgList") or []
                            results.append({
                                "type": "pptx_ready",
                                "pptx_url": m.get("url") or "",
                                "file_name": m.get("fileName") or "",
                                "preview_images": img_list if isinstance(img_list, list) else [],
                                "preview_count": len(img_list) if isinstance(img_list, list) else 0,
                            })
                    except (json.JSONDecodeError, TypeError, IndexError):
                        pass

                # NODE_END — final summary
                elif event_type == "NODE_END":
                    if param:
                        results.append({"type": "summary", "text": param})

                # Other TOOL_CALLS — extract result if present
                elif event_type.startswith("TOOL_CALLS"):
                    if param:
                        results.append({
                            "type": "tool_result",
                            "event": event_type,
                            "action": action,
                            "result": (param or "")[:1000],
                        })

            except (json.JSONDecodeError, TypeError, AttributeError):
                pass

        if item.get("error"):
            results.append({"type": "error", "code": item.get("code"), "message": item.get("content") or ""})

        if is_last:
            results.append({"type": "stream_end"})

    return results


def send_generate(api_key, channel_id, message, file_infos=None, tpl_info=None):
    """Trigger PPT generation via SSE, output parsed events as JSON lines."""
    payload = {"isGetJson": True, "channelId": channel_id, "message": message}
    if file_infos:
        payload["fileUrls"] = [fi["url"] for fi in file_infos]
    else:
        payload["imageUrls"] = []
    if tpl_info:
        payload["pptTpl"] = tpl_info["url"]

    print(f"send payload: {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
    resp = requests.post(
        f"{BASE_URL}/send", headers=_headers(api_key, accept="text/event-stream"),
        json=payload, stream=True,
    )
    resp.raise_for_status()

    for line in resp.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8", errors="replace")
        if not decoded.startswith("data:"):
            continue
        data_str = decoded[5:].strip()
        if not data_str:
            continue

        try:
            data_list = json.loads(data_str)
            if not isinstance(data_list, list):
                data_list = [data_list]
        except (json.JSONDecodeError, TypeError):
            continue

        for evt in parse_sse_event(data_list):
            if evt.get("type") == "pptx_ready":
                evt["web_url"] = f"https://www.popai.pro/agentic-pptx/{channel_id}"
                evt["is_end"] = True
            line_out = json.dumps(evt, ensure_ascii=False)
            print(line_out)
            sys.stdout.flush()

            if evt.get("type") in ("stream_end", "error"):
                return


def main():
    parser = argparse.ArgumentParser(description="Generate PPT via PopAI API")
    parser.add_argument("--query", "-q", required=True, help="PPT topic or modification instruction")
    parser.add_argument("--file", "-f", nargs="*", help="Local files to upload (max 5)")
    parser.add_argument("--tpl", "-t", help="Local PPT template file to upload (ignored in modify mode)")
    parser.add_argument("--channel-id", "-c", help="Existing channel ID for multi-round modification (skips channel creation)")
    args = parser.parse_args()

    api_key = os.getenv("POPAI_ACCESS_TOKEN")
    if not api_key:
        print("Error: POPAI_ACCESS_TOKEN environment variable is required.", file=sys.stderr)
        sys.exit(1)

    try:
        file_infos = None
        tpl_info = None
        upload_tasks = []

        if args.file:
            if len(args.file) > 5:
                print("Error: Maximum 5 files allowed.", file=sys.stderr)
                sys.exit(1)
            upload_tasks.extend(args.file)
        if args.tpl and not args.channel_id:
            upload_tasks.append(args.tpl)

        if upload_tasks:
            with ThreadPoolExecutor(max_workers=min(len(upload_tasks), 6)) as pool:
                uploaded = list(pool.map(lambda fp: upload_file(api_key, fp), upload_tasks))
            if args.file:
                file_infos = uploaded[:len(args.file)]
            if args.tpl and not args.channel_id:
                tpl_info = uploaded[-1]
            print(f"Uploaded {len(uploaded)} file(s).", file=sys.stderr)

        if args.channel_id:
            # Modify mode: reuse existing channel, template cannot be changed
            channel_id = args.channel_id
            print(f"Modify mode, channel: {channel_id}", file=sys.stderr)
            print("Sending modification request...", file=sys.stderr)
            send_generate(api_key, channel_id, args.query, file_infos)
        else:
            print("Creating channel...", file=sys.stderr)
            channel_id = create_channel(api_key, args.query, file_infos)
            print(f"Channel: {channel_id}", file=sys.stderr)

            print("Generating PPT...", file=sys.stderr)
            send_generate(api_key, channel_id, args.query, file_infos, tpl_info)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
