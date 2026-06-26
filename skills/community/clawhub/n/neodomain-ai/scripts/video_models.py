#!/usr/bin/env python3
"""
Neodomain AI - Get Available Video Models
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import os

BASE_URL = "https://story.neodomain.cn/agent/user/video"


def get_video_models(request_type: int = 2, token: str = None):
    """Get available video models with cascading configuration."""
    url = f"{BASE_URL}/models/cascading?requestType={request_type}"
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["accessToken"] = token
    
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}", file=sys.stderr)
        print(e.read().decode("utf-8"), file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Get available video generation models")
    parser.add_argument("--request-type", type=int, default=2, 
                        help="Request type: 1-视频工具, 2-画布")
    parser.add_argument("--token", "--access-token", dest="token", help="Access token")
    
    args = parser.parse_args()
    
    if not args.token:
        args.token = os.environ.get("NEODOMAIN_ACCESS_TOKEN")
    
    if not args.token:
        print("❌ Error: Access token required. Use --token or set NEODOMAIN_ACCESS_TOKEN", file=sys.stderr)
        sys.exit(1)
    
    result = get_video_models(args.request_type, args.token)
    
    if result.get("success"):
        models = result.get("data", [])
        print(f"\n🎬 Available Video Models ({len(models)}):\n")
        
        for model in models:
            print(f"  {model.get('name')} ({model.get('value')})")
            print(f"    Provider: {model.get('provider')}")
            print(f"    Description: {model.get('description')}")
            print(f"    Tags: {', '.join(model.get('tags', []))}")
            print(f"    Features:")
            print(f"      - Audio: {'✅' if model.get('supportAudio') else '❌'}")
            print(f"      - Prompt Enhance: {'✅' if model.get('supportEnhance') else '❌'}")
            print(f"      - First/Last Frame: {'✅' if model.get('supportFirstLastFrame') else '❌'}")
            print(f"      - Multi-Image Ref: {'✅' if model.get('supportReferenceToVideo') else '❌'}")
            
            # Show generation types
            for gt in model.get("generationTypes", []):
                print(f"    {gt.get('name')}:")
                for res in gt.get("resolutions", []):
                    print(f"      {res.get('name')}:")
                    for dur in res.get("durations", []):
                        print(f"        {dur.get('name')}:")
                        for ar in dur.get("aspectRatios", []):
                            cost = ar.get("basePoints", 0)
                            audio_cost = ar.get("audioPoints", 0)
                            enhance_cost = ar.get("enhancePoints", 0)
                            print(f"          {ar.get('value')}: {cost} pts" + 
                                  (f" (+{audio_cost} audio)" if audio_cost else "") +
                                  (f" (+{enhance_cost} enhance)" if enhance_cost else ""))
            print()
    else:
        print(f"❌ Error: {result.get('errMessage')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
