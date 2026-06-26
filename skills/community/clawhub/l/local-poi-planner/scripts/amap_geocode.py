#!/usr/bin/env python3
"""Amap Geocoding Module - 高德地理编码，支持任意中文地址解析"""
import os
import json
import urllib.request
import urllib.parse
import socket
from pathlib import Path

# Load .env.local if exists
SCRIPT_DIR = Path(__file__).parent.resolve()
ENV_FILE = SCRIPT_DIR.parent / ".env.local"
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

# Load API Key from environment
AMAP_KEY = os.getenv("AMAP_KEY")
if not AMAP_KEY:
    # Fallback to placeholder - will fail gracefully
    AMAP_KEY = "<YOUR_AMAP_KEY_HERE>"

GEOCODE_API_URL = "https://restapi.amap.com/v3/geocode/geo"


def geocode_address(address: str) -> dict:
    """
    使用高德地图API解析任意中文地址
    
    Args:
        address: 中文地址，如 "天津财经大学"、"北京市朝阳区三里屯"
        
    Returns:
        {
            "lat": 39.0456,
            "lon": 117.2345,
            "name": "天津财经大学",
            "formatted_address": "天津市河西区珠江道25号",
            "provider": "amap",
            "success": True
        }
        或失败时返回 {"success": False, "error": "..."}
    """
    if AMAP_KEY == "<YOUR_AMAP_KEY_HERE>":
        return {
            "success": False,
            "error": "AMAP_KEY not configured. Please set AMAP_KEY environment variable."
        }
    
    params = {
        "key": AMAP_KEY,
        "address": address,
        "output": "json"
    }
    
    try:
        query_string = urllib.parse.urlencode(params)
        url = f"{GEOCODE_API_URL}?{query_string}"
        
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
        
        if data.get("status") != "1":
            return {
                "success": False,
                "error": f"Amap API error: {data.get('info', 'Unknown error')}"
            }
        
        geocodes = data.get("geocodes", [])
        if not geocodes:
            return {
                "success": False,
                "error": f"No geocoding results for: {address}"
            }
        
        # Take the first (best) result
        result = geocodes[0]
        location = result.get("location", "").split(",")
        
        if len(location) != 2:
            return {
                "success": False,
                "error": f"Invalid location format: {result.get('location')}"
            }
        
        return {
            "success": True,
            "lat": float(location[1]),
            "lon": float(location[0]),
            "name": address,
            "formatted_address": result.get("formatted_address", address),
            "province": result.get("province", ""),
            "city": result.get("city", ""),
            "district": result.get("district", ""),
            "provider": "amap"
        }
        
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
    except socket.timeout:
        return {
            "success": False,
            "error": "Request timeout"
        }
    except (KeyError, ValueError) as e:
        return {
            "success": False,
            "error": f"Parse error: {str(e)}"
        }


def test_geocode():
    """Test function"""
    test_addresses = [
        "天津财经大学",
        "北京三里屯",
        "上海外滩",
        "深圳科技园"
    ]
    
    for addr in test_addresses:
        print(f"\n测试: {addr}")
        result = geocode_address(addr)
        if result["success"]:
            print(f"  ✅ 成功: ({result['lat']:.4f}, {result['lon']:.4f})")
            print(f"  📍 {result['formatted_address']}")
        else:
            print(f"  ❌ 失败: {result['error']}")


if __name__ == "__main__":
    test_geocode()
