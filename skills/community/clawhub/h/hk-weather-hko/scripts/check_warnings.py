#!/usr/bin/env python3
"""
檢查香港天氣警告

用法:
    python3 check_warnings.py [--json] [--critical]

快速檢查所有生效中的天氣警告。
"""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


BASE_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"

WARNING_NAMES = {
    "RAINSTM": "暴雨警告",
    "TYHOON": "颱風警告",
    "HEAT": "高溫天氣",
    "COLD": "寒冷天氣",
    "FIRE": "火災危險警告",
    "FLOOD": "山洪暴發警告",
    "LANDSLP": "山泥傾瀉警告",
    "WIND": "強烈季候風信號",
    "RS": "暴雨警告",
    "TC": "颱風警告",
}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="檢查香港天氣警告")
    parser.add_argument("--json", action="store_true", help="輸出原始 JSON")
    parser.add_argument("--critical", action="store_true", help="僅顯示關鍵警告")
    args = parser.parse_args()
    
    # 獲取警告數據
    url = f"{BASE_URL}?dataType=warnsum&lang=tc"
    critical_types = ["RAINSTM", "TYHOON", "LANDSLP", "FLOOD", "RS", "TC"]
    
    try:
        req = Request(url, headers={"User-Agent": "HKO-Weather-Skill/1.0"})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ 錯誤：{e}", file=sys.stderr)
        sys.exit(1)
    
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    
    # 檢查是否有警告
    warnings = []
    if isinstance(data, dict) and "warningSummary" in data:
        warnings = data["warningSummary"]
    
    if not warnings:
        print("✅ 目前無生效中天氣警告")
        return
    
    if args.critical:
        critical = [w for w in warnings if w.get("warningType") in critical_types]
        if critical:
            print("🚨 關鍵天氣警告:")
            for w in critical:
                w_type = w.get("warningType", "")
                w_name = w.get("name", {}).get("tc", WARNING_NAMES.get(w_type, w_type))
                print(f"   ⚠️ {w_name}")
        else:
            print("✅ 無關鍵天氣警告")
        return
    
    # 顯示所有警告
    print("⚠️ 生效中天氣警告:")
    for w in warnings:
        w_type = w.get("warningType", "")
        w_name = w.get("name", {}).get("tc", WARNING_NAMES.get(w_type, w_type))
        status = w.get("status", "")
        effective = w.get("effectiveTime", "")
        
        status_text = "🟢 生效中" if status == "ISSUED" else f"狀態：{status}"
        print(f"   {w_name}")
        print(f"      {status_text}")
        if effective:
            effective = effective.replace("T", " ").split("+")[0]
            print(f"      生效時間：{effective}")


if __name__ == "__main__":
    main()
