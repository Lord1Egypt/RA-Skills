#!/usr/bin/env python3
"""
Home Assistant API Controller

Usage:
    python ha_control.py <entity_id> <service> [data_json]

Examples:
    python ha_control.py button.miir_ir02_8112_turn_off button/press
    python ha_control.py text.xiaomi_lx06_3ff3_execute_text_directive text/set_value '{"value": "播放音乐"}'
    python ha_control.py number.miir_ir02_8112_temperature_for_ir number/set_value '{"value": 26}'
"""

import os
import sys
import json
import urllib.request
import urllib.error

# Configuration
HA_URL = os.environ.get("HA_URL", "http://192.168.31.35:8123")
HA_TOKEN = os.environ.get("HA_TOKEN", "")

def call_service(entity_id, service, data=None):
    """Call Home Assistant service"""
    url = f"{HA_URL}/api/services/{service}"
    
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {"entity_id": entity_id}
    if data:
        payload.update(data)
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"✅ Success: {service} called on {entity_id}")
            if result:
                print(f"Response: {result}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        print(f"Response: {e.read().decode('utf-8')}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    entity_id = sys.argv[1]
    service = sys.argv[2]
    data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    
    success = call_service(entity_id, service, data)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
