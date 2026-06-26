#!/usr/bin/env python3
"""
Instagram Video Downloader Script with Payment Integration
Fetches video download links from savefbs.com API

Pricing: $0.1 per download after free tier (5 downloads/day)
"""

import sys
import json
import requests
import os
from datetime import datetime, timedelta
from pathlib import Path

# API Configuration
API_BASE_URL = "https://savefbs.com"
API_ENDPOINT = "/api/v1/aio/search"

# Payment Configuration
PRICE_PER_DOWNLOAD = 0.1  # USD
FREE_DAILY_LIMIT = 5
WALLET_ADDRESS = "0xA4195EeFF370c003C5C775BE4C3f350022666305"  # Polygon USDC
PAYMENT_URL = f"https://pay.request.network/{WALLET_ADDRESS}?amount=0.1&currency=USDC&network=polygon&reason=Unlock%20unlimited%20downloads"

def get_usage_file():
    """Get path to usage tracking file"""
    home = Path.home()
    usage_dir = home / ".openclaw" / "skills" / "instagram-video-downloader"
    usage_dir.mkdir(parents=True, exist_ok=True)
    return usage_dir / "usage.json"

def load_usage():
    """Load usage data"""
    usage_file = get_usage_file()
    if not usage_file.exists():
        return {"date": str(datetime.now().date()), "count": 0, "paid": False}
    
    try:
        with open(usage_file, 'r') as f:
            data = json.load(f)
            if data.get("date") != str(datetime.now().date()):
                return {"date": str(datetime.now().date()), "count": 0, "paid": False}
            return data
    except:
        return {"date": str(datetime.now().date()), "count": 0, "paid": False}

def save_usage(usage):
    """Save usage data"""
    usage_file = get_usage_file()
    with open(usage_file, 'w') as f:
        json.dump(usage, f)

def check_quota():
    """Check if user has remaining quota"""
    usage = load_usage()
    
    if usage.get("paid"):
        return True, usage
    
    if usage["count"] < FREE_DAILY_LIMIT:
        return True, usage
    
    return False, usage

def fetch_video_links(ig_url):
    """Fetch download links for an Instagram video from savefbs.com API"""
    
    has_quota, usage = check_quota()
    
    if not has_quota:
        return {
            'success': False,
            'error': 'Free daily limit reached',
            'message': f'You have used {usage["count"]}/{FREE_DAILY_LIMIT} free downloads today.',
            'upgrade': f'Upgrade to unlimited downloads for ${PRICE_PER_DOWNLOAD} per video',
            'payment_url': PAYMENT_URL,
            'instructions': f'Visit {PAYMENT_URL} to upgrade or wait until tomorrow for free quota reset.'
        }
    
    session = requests.Session()
    
    headers = {
        'User-Agent': 'OpenClaw-Skill/1.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': API_BASE_URL,
        'Referer': f'{API_BASE_URL}/',
    }
    
    try:
        session.get(API_BASE_URL, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not establish session: {e}", file=sys.stderr)
    
    api_url = f"{API_BASE_URL}{API_ENDPOINT}"
    payload = {
        'vid': ig_url,
        'prefix': 'ig',
        'ex': '',
        'format': ''
    }
    
    try:
        response = session.post(api_url, json=payload, headers=headers, timeout=30)
        
        content_type = response.headers.get('content-type', '')
        if 'text/html' in content_type:
            return {
                'success': False,
                'error': 'API returned HTML instead of JSON. Service may be unavailable.'
            }
        
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 0:
            usage["count"] += 1
            save_usage(usage)
            
            remaining = FREE_DAILY_LIMIT - usage["count"]
            
            result = {
                'success': True,
                'title': data.get('data', {}).get('title', 'Instagram Video'),
                'author': data.get('data', {}).get('author', 'Unknown'),
                'thumbnail': data.get('data', {}).get('thumbnail'),
                'downloads': [],
                'usage': {
                    'used': usage["count"],
                    'limit': FREE_DAILY_LIMIT,
                    'remaining': remaining if remaining > 0 else 0
                },
                'powered_by': '🌐 Powered by savefbs.com',
                'upgrade_info': f'💎 Upgrade to unlimited: {PAYMENT_URL}' if remaining <= 2 else None
            }
            
            medias = data.get('data', {}).get('medias', [])
            for media in medias:
                result['downloads'].append({
                    'quality': media.get('quality', 'Unknown'),
                    'url': media.get('url'),
                    'extension': media.get('extension', 'mp4'),
                    'size': media.get('size', 'Unknown')
                })
            
            return result
        else:
            return {
                'success': False,
                'error': data.get('message', 'Failed to fetch video'),
                'code': data.get('code')
            }
            
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP error {e.response.status_code}: {e.response.reason}',
            'details': 'The video may be private or unavailable.'
        }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout. The service may be slow or unavailable.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Network error: {str(e)}'
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'error': 'Invalid JSON response from server'
        }

def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: fetch_ig_video.py <instagram_url>'
        }))
        sys.exit(1)
    
    ig_url = sys.argv[1]
    result = fetch_video_links(ig_url)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
