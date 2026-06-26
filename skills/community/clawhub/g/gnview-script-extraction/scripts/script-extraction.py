#!/usr/bin/env python3
import argparse
import json
import sys
import os
from typing import Dict, Optional
import requests

def upload_video(video_path: str, ark_api_key: str) -> Dict:
    """Upload local video file to VolcEngine ARK with Bearer auth and form data matching curl example"""
    url = "https://ark.cn-beijing.volces.com/api/v3/files"
    
    headers = {
        "Authorization": f"Bearer {ark_api_key}"
    }
    
    files = {
        'file': (os.path.basename(video_path), open(video_path, 'rb'), 'video/mp4')
    }
    
    data = {
        'purpose': 'user_data',
        'preprocess_configs[video][fps]': '0.3'
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        if "error" in result or ("Error" in result and "Message" in result["Error"]):
            error_msg = result.get("error") or result["Error"]["Message"]
            print(f"Upload failed: {error_msg}", file=sys.stderr)
            sys.exit(1)
        return result
    except requests.exceptions.RequestException as e:
        print(f"Upload HTTP error: {str(e)} - {response.text if 'response' in locals() else ''}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Upload failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

def analyze_script(file_id: str, model: str, prompt: str, ark_api_key: str) -> str:
    """Analyze video script using VolcEngine ARK API with Bearer token auth"""
    url = "https://ark.cn-beijing.volces.com/api/v3/responses"
    
    # Prepare request body matching the provided curl example
    request_body = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_video",
                        "file_id": file_id
                    },
                    {
                        "type": "input_text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    # Prepare headers with Bearer auth
    headers = {
        "Authorization": f"Bearer {ark_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        result = response.json()
        if "error" in result or ("Error" in result and "Message" in result["Error"]):
            error_msg = result.get("error") or result["Error"]["Message"]
            print(f"Analysis failed: {error_msg}", file=sys.stderr)
            sys.exit(1)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        print(f"Analysis HTTP error: {str(e)} - {response.text if 'response' in locals() else ''}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Analysis failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Extract video script and analyze framework using VolcEngine ARK with Bearer auth")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload local video file to VolcEngine ARK")
    upload_parser.add_argument("video_path", help="Path to local video file")
    upload_parser.add_argument("ark_api_key", help="VolcEngine ARK API Key (for Bearer token auth)")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze uploaded video file")
    analyze_parser.add_argument("file_id", help="Uploaded video file ID")
    analyze_parser.add_argument("ark_api_key", help="VolcEngine ARK API Key (for Bearer token auth)")
    analyze_parser.add_argument("--model", help="Model name for video analysis", default="doubao-seed-2-0-lite-260215")
    analyze_parser.add_argument("--prompt", help="Custom analysis prompt", default="请你描述下视频中的人物的一系列动作，以JSON格式输出开始时间（start_time）、结束时间（end_time）、事件（event）、是否危险（danger），请使用HH:mm:ss表示时间戳。")
    
    args = parser.parse_args()
    
    if args.command == "upload":
        # Upload video and print file ID
        upload_response = upload_video(args.video_path, args.ark_api_key)
        file_id = upload_response.get("video_id") or upload_response.get("VideoId") or upload_response.get("id")
        if file_id:
            print(file_id)
        else:
            print("Error: Failed to extract file ID from upload response", file=sys.stderr)
            sys.exit(1)
    elif args.command == "analyze":
        # Analyze video
        analysis_result = analyze_script(args.file_id, args.model, args.prompt, args.ark_api_key)
        print(analysis_result)

if __name__ == "__main__":
    main()