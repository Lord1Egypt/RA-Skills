#!/usr/bin/env python3
"""
Minimax VLM (Vision Language Model) API client.
Handles image understanding via MiniMax Token Plan API.

Usage:
    python3 minimax_image.py --api-key KEY --prompt PROMPT --image-url URL_OR_PATH
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


def download_image_as_base64(url: str) -> str:
    """Download HTTP/HTTPS image and return base64 data URL."""
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            image_data = response.read()
            content_type = response.headers.get('Content-Type', 'image/jpeg').lower()
            
            # Detect format
            if 'png' in content_type:
                fmt = 'png'
            elif 'webp' in content_type:
                fmt = 'webp'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                fmt = 'jpeg'
            else:
                fmt = 'jpeg'  # default
            
            b64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/{fmt};base64,{b64_data}"
    except urllib.error.URLError as e:
        print(f"Error downloading image: {e}", file=sys.stderr)
        sys.exit(1)


def local_file_to_base64(path: str) -> str:
    """Read local image file and return base64 data URL."""
    if not os.path.exists(path):
        # Try expanding path for Windows paths like D:\...
        if sys.platform == 'win32' and ':' in path:
            # Try as-is
            pass
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    # Detect format from extension
    lower_path = path.lower()
    if lower_path.endswith('.png'):
        fmt = 'png'
    elif lower_path.endswith('.webp'):
        fmt = 'webp'
    elif lower_path.endswith('.jpg') or lower_path.endswith('.jpeg'):
        fmt = 'jpeg'
    else:
        fmt = 'jpeg'  # default
    
    try:
        with open(path, 'rb') as f:
            image_data = f.read()
        b64_data = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/{fmt};base64,{b64_data}"
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def process_image_url(image_url: str) -> str:
    """
    Process image input and convert to base64 data URL.
    
    Handles:
    - HTTP/HTTPS URLs: downloads and converts to base64
    - Local file paths: reads file and converts to base64
    - Base64 data URLs: passes through as-is
    """
    if image_url.startswith('data:'):
        # Already a data URL
        return image_url
    elif image_url.startswith(('http://', 'https://')):
        return download_image_as_base64(image_url)
    else:
        # Local file path
        return local_file_to_base64(image_url)


def call_vlm_api(api_key: str, prompt: str, image_url: str) -> dict:
    """Call MiniMax VLM API."""
    # Process image (convert to base64 if needed)
    processed_image_url = process_image_url(image_url)
    
    url = "https://api.minimaxi.com/v1/coding_plan/vlm"
    
    payload = {
        "prompt": prompt,
        "image_url": processed_image_url
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'MM-API-Source': 'minimax-coding-plan-mcp'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        print(f"API Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Minimax VLM Image Understanding')
    parser.add_argument('--api-key', required=True, help='Minimax API key')
    parser.add_argument('--prompt', required=True, help='Prompt/question about the image')
    parser.add_argument('--image-url', required=True, help='Image URL or local file path')
    
    args = parser.parse_args()
    
    result = call_vlm_api(args.api_key, args.prompt, args.image_url)
    
    # Check for API errors
    base_resp = result.get('base_resp', {})
    if base_resp.get('status_code', 0) != 0:
        status_msg = base_resp.get('status_msg', 'Unknown error')
        print(f"API Error: {status_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Output the content
    content = result.get('content', '')
    if content:
        print(content)
    else:
        print("No content returned from API", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
