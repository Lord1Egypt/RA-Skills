#!/usr/bin/env python3
import argparse
import json
import os
import sys
from typing import Any, Dict

from urllib.parse import urlencode
from urllib.request import urlopen


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Baidu geocoding helper for OpenClaw skills")
    p.add_argument("--address", required=True, help="Address or hospital name")
    p.add_argument("--city", default="北京", help="City or region hint, default: 北京")
    p.add_argument("--timeout", type=int, default=10)
    return p.parse_args()


def geocode(address: str, city: str, ak: str, timeout: int) -> Dict[str, Any]:
    url = "https://api.map.baidu.com/geocoding/v3/"
    params = {
        "address": address,
        "city": city,
        "output": "json",
        "ret_coordtype": "gcj02ll",
        "ak": ak,
    }
    url = url + "?" + urlencode(params)
    with urlopen(url, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("status") != 0:
        raise RuntimeError(f"Baidu geocoding failed: status={data.get('status')}, msg={data.get('msg') or data.get('message')}")
    result = data.get("result", {})
    location = result.get("location", {})
    return {
        "query": address,
        "city": city,
        "lat": location.get("lat"),
        "lng": location.get("lng"),
        "precise": result.get("precise"),
        "confidence": result.get("confidence"),
        "comprehension": result.get("comprehension"),
        "level": result.get("level"),
    }


def main() -> int:
    args = parse_args()
    ak = os.getenv("BAIDU_MAP_AK")
    if not ak:
        print(json.dumps({"error": "Missing environment variable BAIDU_MAP_AK"}, ensure_ascii=False))
        return 2
    try:
        print(json.dumps(geocode(args.address, args.city, ak, args.timeout), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
