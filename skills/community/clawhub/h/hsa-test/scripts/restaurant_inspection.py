#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ezviz Restaurant Inspection Skill
萤石餐饮行业智能巡检脚本

Usage:
    python3 restaurant_inspection.py [app_key] [app_secret] [device_serial] [channel_no] [agent_id] [analysis_text]

Environment Variables (alternative to command line args):
    EZVIZ_APP_KEY, EZVIZ_APP_SECRET, EZVIZ_DEVICE_SERIAL, EZVIZ_AGENT_ID, EZVIZ_CHANNEL_NO, EZVIZ_ANALYSIS_TEXT
"""

import os
import sys
import time
import json
import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta

# Default values
DEFAULT_CHANNEL_NO = "1"
DEFAULT_ANALYSIS_TEXT = "请对这张餐饮场所图片进行智能巡检，重点关注：1.地面卫生（污渍、积水、垃圾）2.动火离人（厨房明火无人看管）3.垃圾桶状态（是否盖紧盖子）4.货品存放（食品/原料是否离地存放）5.口罩佩戴（员工口罩佩戴合规性）。请按风险等级分类输出结果，动火离人属于高危告警。"

# API Endpoints
TOKEN_URL = "https://open.ys7.com/api/lapp/token/get"
CAPTURE_URL = "https://open.ys7.com/api/lapp/device/capture"
ANALYSIS_URL = "https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis"

def get_env_or_arg(env_var, arg_value, default=None):
    """Get value from environment variable or command line argument"""
    return os.getenv(env_var) or arg_value or default

def get_access_token(app_key, app_secret):
    """Get access token from Ezviz API"""
    print("=" * 70)
    print("[Step 1] Getting access token...")
    
    payload = {
        'appKey': app_key,
        'appSecret': app_secret
    }
    
    try:
        response = requests.post(TOKEN_URL, data=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == '200':
            token = result['data']['accessToken']
            expire_time = datetime.now() + timedelta(days=7)
            print(f"[SUCCESS] Token obtained, expires: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
            return token
        else:
            print(f"[ERROR] Failed to get token: {result.get('msg', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when getting token: {str(e)}")
        return None

def capture_image(access_token, device_serial, channel_no):
    """Capture image from device"""
    payload = {
        'accessToken': access_token,
        'deviceSerial': device_serial,
        'channelNo': channel_no
    }
    
    try:
        response = requests.post(CAPTURE_URL, data=payload, timeout=30)
        result = response.json()
        
        if result.get('code') == '200':
            pic_url = result['data']['picUrl']
            print(f"[SUCCESS] Image captured: {pic_url[:50]}...")
            return pic_url
        else:
            print(f"[ERROR] Failed to capture image: {result.get('msg', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when capturing image: {str(e)}")
        return None

def analyze_image(access_token, agent_id, pic_url, analysis_text):
    """Analyze image using AI agent with proper authentication"""
    payload = {
        "appId": agent_id,
        "mediaType": "image",
        "text": analysis_text,
        "dataType": "url",
        "data": pic_url
    }
    
    headers = {
        'Content-Type': 'application/json',
        'accessToken': access_token
    }
    
    try:
        print(f"[INFO] Sending analysis request to: {ANALYSIS_URL}")
        response = requests.post(ANALYSIS_URL, json=payload, headers=headers, timeout=60)
        
        # Debug output
        print(f"[DEBUG] Payload: appId={agent_id[:8]}..., mediaType=image, text={analysis_text[:50]}..., dataType=url, data={pic_url[:30]}...")
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"[DEBUG] Raw response: {json.dumps(result)[:200]}...")
            print(f"[DEBUG] Parsed JSON: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")
            
            if result.get('meta', {}).get('code') == 200:
                print("[SUCCESS] Analysis completed!")
                return result.get('data')
            else:
                error_msg = result.get('meta', {}).get('message', 'Unknown error')
                print(f"[ERROR] API Error: {error_msg}")
                return None
        else:
            print(f"[ERROR] HTTP {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when analyzing image: {str(e)}")
        return None

def parse_device_list(device_serial_str):
    """Parse device serial string with optional channel numbers"""
    devices = []
    for item in device_serial_str.split(','):
        item = item.strip()
        if ':' in item:
            serial, channel = item.split(':', 1)
            devices.append((serial, channel))
        else:
            devices.append((item, DEFAULT_CHANNEL_NO))
    return devices

def main():
    # Get configuration from command line args or environment variables
    if len(sys.argv) >= 6:
        app_key = sys.argv[1]
        app_secret = sys.argv[2]
        device_serial = sys.argv[3]
        channel_no = sys.argv[4]
        agent_id = sys.argv[5]
        analysis_text = sys.argv[6] if len(sys.argv) > 6 else DEFAULT_ANALYSIS_TEXT
    else:
        app_key = get_env_or_arg('EZVIZ_APP_KEY', None)
        app_secret = get_env_or_arg('EZVIZ_APP_SECRET', None)
        device_serial = get_env_or_arg('EZVIZ_DEVICE_SERIAL', None)
        channel_no = get_env_or_arg('EZVIZ_CHANNEL_NO', DEFAULT_CHANNEL_NO)
        agent_id = get_env_or_arg('EZVIZ_AGENT_ID', None)
        analysis_text = get_env_or_arg('EZVIZ_ANALYSIS_TEXT', DEFAULT_ANALYSIS_TEXT)
    
    # Validate required parameters
    if not all([app_key, app_secret, device_serial, agent_id]):
        print("Error: Missing required parameters!")
        print("Please provide via command line args or environment variables:")
        print("  EZVIZ_APP_KEY, EZVIZ_APP_SECRET, EZVIZ_DEVICE_SERIAL, EZVIZ_AGENT_ID")
        sys.exit(1)
    
    # Print header
    print("=" * 70)
    print("Ezviz Restaurant Inspection Skill (萤石餐饮智能巡检)")
    print("=" * 70)
    print(f"[Time] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse devices
    devices = parse_device_list(device_serial)
    print(f"[INFO] Target devices: {len(devices)}")
    for i, (serial, chan) in enumerate(devices, 1):
        print(f" - {serial} (Channel: {chan})")
    print(f"[INFO] Agent ID: {agent_id[:8]}...")
    print(f"[INFO] Analysis: {analysis_text[:50]}{'...' if len(analysis_text) > 50 else ''}")
    
    # Get access token
    access_token = get_access_token(app_key, app_secret)
    if not access_token:
        print("Failed to get access token. Exiting.")
        sys.exit(1)
    
    # Process each device
    print("\n" + "=" * 70)
    print("[Step 2] Capturing and analyzing images...")
    print("=" * 70)
    
    results = []
    success_count = 0
    
    for i, (device_serial, channel_no) in enumerate(devices):
        if i > 0:
            time.sleep(1)  # Rate limiting
        
        print(f"\n[Device] {device_serial} (Channel: {channel_no})")
        
        # Capture image
        pic_url = capture_image(access_token, device_serial, channel_no)
        if not pic_url:
            continue
        
        # Analyze image
        analysis_result = analyze_image(access_token, agent_id, pic_url, analysis_text)
        if not analysis_result:
            continue
        
        success_count += 1
        results.append({
            'device': device_serial,
            'channel': channel_no,
            'pic_url': pic_url,
            'analysis': analysis_result
        })
        
        # Print analysis result
        print("\n[Inspection Result]")
        print(str(analysis_result))
    
    # Print summary
    print("\n" + "=" * 70)
    print("INSPECTION SUMMARY")
    print("=" * 70)
    print(f" Total devices: {len(devices)}")
    print(f" Success: {success_count}")
    print(f" Failed: {len(devices) - success_count}")

if __name__ == "__main__":
    main()