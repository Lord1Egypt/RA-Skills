#!/usr/bin/env python3
import sys
import json
import requests

def query_location(imei):
    url = f"https://search.iwown.com/hpmservice/ai/vendor/gnss/latest?deviceid={imei}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ReturnCode") != 0:
            return None, None, None
            
        record_time = data["Data"]["record_time"]
        address = data["Data"]["address"]
        return record_time, address, data["Data"]
    except Exception as e:
        print(f"查询失败: {e}", file=sys.stderr)
        return None, None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python query_gnss.py <imei>")
        sys.exit(1)
    
    imei = sys.argv[1]
    record_time, address, raw_data = query_location(imei)
    
    if address:
        print(json.dumps({
            "status": "success",
            "record_time": record_time,
            "address": address,
            "raw": raw_data
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "status": "error",
            "message": "查不到定位记录"
        }, ensure_ascii=False))
