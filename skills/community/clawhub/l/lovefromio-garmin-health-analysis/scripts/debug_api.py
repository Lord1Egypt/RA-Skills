#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from garmin_auth import get_client

client = get_client()
if not client:
    print("NOT_AUTHED")
    sys.exit(1)

# 先尝试获取设备
try:
    devices = client.get_devices()
    print("DEVICES:", json.dumps(devices, default=str)[:500])
except Exception as e:
    print("DEVICES_ERROR:", str(e))

# 测试睡眠数据
try:
    sleep = client.get_sleep_data("2026-04-04")
    if sleep:
        dto = sleep.get("dailySleepDTO", {})
        print("SLEEP:", json.dumps(dto, default=str)[:300])
    else:
        print("SLEEP: None")
except Exception as e:
    print("SLEEP_ERROR:", str(e))

# 测试心率
try:
    hr = client.get_heart_rates("2026-04-04")
    print("HR:", json.dumps(hr, default=str)[:300])
except Exception as e:
    print("HR_ERROR:", str(e))
