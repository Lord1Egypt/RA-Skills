#!/usr/bin/env python3
"""
MOSI Voice Clone: Create custom voices from audio files

Usage:
  # Upload audio file
  python3 mosi_voice.py upload --file audio.wav
  
  # Create voice from uploaded file
  python3 mosi_voice.py clone --file-id FILE_ID [--text "transcription"]
  
  # List all voices
  python3 mosi_voice.py list [--status ACTIVE]
  
  # Get voice details
  python3 mosi_voice.py get --voice-id VOICE_ID
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library required. Run: pip install requests")
    sys.exit(1)

API_BASE = "https://studio.mosi.cn"


def get_api_key(api_key: str = None) -> str:
    if not api_key:
        api_key = os.environ.get("MOSI_API_KEY")
    if not api_key:
        raise ValueError("API key required. Set MOSI_API_KEY env var or pass --api-key")
    return api_key


def upload_audio(file_path: str, api_key: str = None) -> dict:
    """Upload audio file, returns file_id"""
    api_key = get_api_key(api_key)
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    url = f"{API_BASE}/api/v1/files/upload"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    with open(path, "rb") as f:
        files = {"file": (path.name, f)}
        resp = requests.post(url, headers=headers, files=files, timeout=60)
    
    if resp.status_code != 200:
        raise RuntimeError(f"Upload failed ({resp.status_code}): {resp.text}")
    
    return resp.json()


def clone_voice(file_id: str = None, url: str = None, text: str = None, api_key: str = None) -> dict:
    """
    Create voice from audio file
    
    Args:
        file_id: Uploaded file ID (either file_id or url required)
        url: Audio URL (alternative to file_id)
        text: Optional transcription text (improves quality)
        api_key: MOSI API Key
    
    Returns:
        dict: Contains voice_id, status, etc.
    """
    api_key = get_api_key(api_key)
    
    if not file_id and not url:
        raise ValueError("Either file_id or url is required")
    if file_id and url:
        raise ValueError("Provide only one of file_id or url, not both")
    
    endpoint = f"{API_BASE}/api/v1/voice/clone"
    payload = {}
    
    if file_id:
        payload["file_id"] = file_id
    if url:
        payload["url"] = url
    if text:
        payload["text"] = text
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    resp = requests.post(endpoint, json=payload, headers=headers, timeout=120)
    
    if resp.status_code != 200:
        raise RuntimeError(f"Voice clone failed ({resp.status_code}): {resp.text}")
    
    return resp.json()


def list_voices(limit: int = 50, offset: int = 0, status: str = None, api_key: str = None) -> dict:
    """Get list of voices"""
    api_key = get_api_key(api_key)
    
    url = f"{API_BASE}/api/v1/voices"
    params = {"limit": limit, "offset": offset}
    if status:
        params["status"] = status
    
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    
    if resp.status_code != 200:
        raise RuntimeError(f"List voices failed ({resp.status_code}): {resp.text}")
    
    return resp.json()


def get_voice(voice_id: str, api_key: str = None) -> dict:
    """Get single voice details"""
    api_key = get_api_key(api_key)
    
    url = f"{API_BASE}/api/v1/voices/{voice_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(url, headers=headers, timeout=30)
    
    if resp.status_code != 200:
        raise RuntimeError(f"Get voice failed ({resp.status_code}): {resp.text}")
    
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="MOSI Voice Clone Management")
    parser.add_argument("--api-key", "-k", help="MOSI API Key (or set MOSI_API_KEY env)")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # upload
    upload_parser = subparsers.add_parser("upload", help="Upload audio file")
    upload_parser.add_argument("--file", "-f", required=True, help="Audio file path")
    
    # clone
    clone_parser = subparsers.add_parser("clone", help="Create voice from audio")
    clone_parser.add_argument("--file-id", "-i", help="Uploaded file ID")
    clone_parser.add_argument("--url", "-u", help="Audio URL (alternative to file-id)")
    clone_parser.add_argument("--text", "-t", help="Optional transcription text")
    
    # list
    list_parser = subparsers.add_parser("list", help="List all voices")
    list_parser.add_argument("--limit", "-l", type=int, default=50, help="Page size")
    list_parser.add_argument("--offset", type=int, default=0, help="Offset")
    list_parser.add_argument("--status", "-s", help="Filter by status (ACTIVE/FAILED/INACTIVE)")
    
    # get
    get_parser = subparsers.add_parser("get", help="Get voice details")
    get_parser.add_argument("--voice-id", "-v", required=True, help="Voice ID")
    
    args = parser.parse_args()
    
    try:
        if args.command == "upload":
            result = upload_audio(args.file, args.api_key)
            print(f"File uploaded successfully")
            print(f"File ID: {result.get('file_id')}")
            print(f"Filename: {result.get('filename')}")
        
        elif args.command == "clone":
            result = clone_voice(
                file_id=args.file_id,
                url=args.url,
                text=args.text,
                api_key=args.api_key,
            )
            print(f"Voice created successfully")
            print(f"Voice ID: {result.get('voice_id')}")
            print(f"Name: {result.get('voice_name')}")
            print(f"Status: {result.get('status')}")
            if result.get("transcription_text"):
                print(f"Transcription: {result.get('transcription_text')}")
        
        elif args.command == "list":
            result = list_voices(
                limit=args.limit,
                offset=args.offset,
                status=args.status,
                api_key=args.api_key,
            )
            voices = result.get("voices", [])
            print(f"Found {result.get('count', len(voices))} voices")
            for v in voices:
                status_mark = "[ACTIVE]" if v.get("status") == "ACTIVE" else f"[{v.get('status')}]"
                print(f"  {status_mark} {v.get('voice_id')} - {v.get('voice_name', 'N/A')}")
        
        elif args.command == "get":
            result = get_voice(args.voice_id, args.api_key)
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
