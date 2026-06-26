#!/usr/bin/env python3
"""
Amap IP geolocation fallback.
Resolves the gateway's real (non-VPN) public IP to city-level coordinates.

How it works:
1. Try multiple IP lookup services with different routing (ipip.net often
   bypasses VPNs because it's a Chinese service on China Unicom backbone).
2. Feed the real IP to Amap's /v3/ip geolocation API.
3. Compute the rectangle center as approximate coordinates (~city-level).
"""

import json
import os
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
ENV_FILE = SCRIPT_DIR.parent / ".env.local"
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

AMAP_IP_URL = "https://restapi.amap.com/v3/ip"
UA = "local-poi-planner/0.3 (+OpenClaw skill)"

# Ordered by preference: ipip.net first (Chinese service, more likely to bypass VPN)
IP_SERVICES = [
    ("ipip.net", "https://myip.ipip.net"),
    ("ifconfig.me", "https://ifconfig.me"),
    ("icanhazip", "https://icanhazip.com"),
    ("ipify", "https://api.ipify.org"),
]


def _http_get_text(url, timeout=5):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace").strip()


def _fetch_public_ips():
    """Try every IP lookup service; return list of (source_name, ip_string)."""
    results = []
    for name, url in IP_SERVICES:
        try:
            text = _http_get_text(url, timeout=5)
        except Exception:
            continue

        # ipip.net format: "当前 IP：x.x.x.x  来自于：..."
        if "IP" in text and ("：" in text or ":" in text):
            m = re.search(r"IP[：:]\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", text)
            if m:
                results.append((name, m.group(1)))
                continue

        # Plain IP format
        cleaned = text.strip()
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", cleaned):
            results.append((name, cleaned))

    return results


def _amap_ip_geolocate(ip, key=None):
    """Query Amap IP geolocation API. Returns {lat, lon, province, city, ...} or None."""
    if not key:
        key = os.getenv("AMAP_KEY", "")
    if not key or not ip:
        return None

    params = {"key": key, "ip": ip}
    url = f"{AMAP_IP_URL}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", UA)
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None

    if data.get("status") != "1":
        return None

    rectangle = data.get("rectangle", "")
    if not rectangle or ";" not in rectangle:
        return None

    # rectangle: "lon1,lat1;lon2,lat2"
    corners = rectangle.split(";")
    if len(corners) != 2:
        return None
    sw = corners[0].split(",")
    ne = corners[1].split(",")
    if len(sw) != 2 or len(ne) != 2:
        return None

    lon1, lat1 = float(sw[0]), float(sw[1])
    lon2, lat2 = float(ne[0]), float(ne[1])

    return {
        "lat": round((lat1 + lat2) / 2, 6),
        "lon": round((lon1 + lon2) / 2, 6),
        "province": data.get("province", ""),
        "city": data.get("city", ""),
        "adcode": data.get("adcode", ""),
        "rectangle": rectangle,
        "accuracy": "city",
        "source_ip": ip,
        "provider": "amap_ip",
    }


def get_ip_location():
    """
    Resolve current approximate location via IP geolocation.

    Returns dict with lat, lon, province, city, accuracy, or None if
    all services fail or Amap cannot geolocate the IP.
    """
    ip_list = _fetch_public_ips()
    if not ip_list:
        return None

    # Prefer ipip.net (most likely to see the real China IP behind a VPN)
    ip_list.sort(key=lambda x: 0 if x[0] == "ipip.net" else 1)

    for source, ip in ip_list:
        result = _amap_ip_geolocate(ip)
        if result:
            result["ip_source"] = source
            return result

    return None


if __name__ == "__main__":
    import sys
    result = get_ip_location()
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("IP location failed — no service returned a geolocatable IP", file=sys.stderr)
        sys.exit(1)
