#!/usr/bin/env python3

import argparse
import http.client
import json
import sys
import auth
import debug_utils
from urllib.parse import urlencode

# Note: xplai API uses "video" nomenclature internally for all media types,
# including audio-only content. The endpoint and field names (video_id, video_url)
# are from xplai's API; this skill only generates audio (monologue with BGM).
API_HOST = "eagle-api.xplai.ai"
API_BASE_URL = f"https://{API_HOST}"
API_ENDPOINT = "/api/solve/video_status_mcp"


def query_audio_status(audio_id):
    url = f"{API_BASE_URL}{API_ENDPOINT}"
    params = {"video_id": audio_id}  # xplai API uses "video_id" for all media types

    debug_utils.log_request("GET", url, params=params)

    try:
        conn = http.client.HTTPSConnection(API_HOST, timeout=30)
        query_string = urlencode(params)
        full_url = f"{API_ENDPOINT}?{query_string}"
        token = auth.get_or_refresh_token()
        if not token:
            print("Error: Failed to get authentication token", file=sys.stderr)
            sys.exit(1)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        conn.request("GET", full_url, headers=headers)
        response = conn.getresponse()
        response_body = response.read().decode("utf-8")
        
        if response.status >= 400:
            print(f"HTTP Error: {response.status} {response.reason}", file=sys.stderr)
            sys.exit(1)
        
        debug_utils.log_response(response, response_body)
        
        result = json.loads(response_body)
        conn.close()

        if result.get("code") == 0:
            data = result.get("data", {})
            card = data.get("card", {})
            
            status = card.get("status")
            audio_url = card.get("video_url")  # xplai API field name

            print(f"Audio ID: {data.get('video_id')}")
            print(f"Title: {card.get('title')}")
            print(f"Subject: {card.get('subject')}")
            print(f"Status: {status}")

            if audio_url and status == "v_succ":
                print(f"Audio URL: {audio_url}")
                print(f"Xplai web page URL: https://www.xplai.ai/#/video/{audio_id}")
            elif status == "v_fail":
                print("Audio generation failed")
            else:
                print(f"Queue Index: {data.get('queue_index', 'N/A')}")
                print("Audio is still processing...")
            
            return status
        else:
            print(f"Error: {result.get('msg')}", file=sys.stderr)
            sys.exit(1)
    except (http.client.HTTPException, OSError) as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query audio generation status from xplai API")
    parser.add_argument("audio_id", type=str, help="Audio ID to query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print request/response details")

    args = parser.parse_args()

    debug_utils.set_debug(args.debug)

    query_audio_status(args.audio_id)


if __name__ == "__main__":
    main()
