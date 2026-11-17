#!/usr/bin/env python3
"""Ninebot vehicle location helper.

Reads the vehicle's WGS-84 coordinates through ninecli, converts them to GCJ-02
for AMap, and optionally performs reverse geocoding. No credentials are printed.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

from runtime_config import config_path, env_value, ninecli_argv, district_safe_gcj02
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error

SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG = config_path()


def amap_key() -> str:
    return env_value(("AMAP_WEBSERVICE_KEY", "AMAP_WEB_KEY"))


def load_sn() -> str:
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"配置文件不存在: {CONFIG}") from exc
    sn = str((data.get("ninebot") or {}).get("sn") or "").strip()
    if not sn or "请填写" in sn or sn.upper().startswith("REPLACE_WITH"):
        raise SystemExit("ninebot.sn 未配置")
    return sn


def wgs84_to_gcj02(lat: float, lon: float) -> tuple[float, float]:
    a, ee = 6378245.0, 0.00669342162296594323

    def tlat(x: float, y: float) -> float:
        r = -100 + 2 * x + 3 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        r += (20 * math.sin(6 * x * math.pi) + 20 * math.sin(2 * x * math.pi)) * 2 / 3
        r += (20 * math.sin(y * math.pi) + 40 * math.sin(y / 3 * math.pi)) * 2 / 3
        r += (160 * math.sin(y / 12 * math.pi) + 320 * math.sin(y * math.pi / 30)) * 2 / 3
        return r

    def tlon(x: float, y: float) -> float:
        r = 300 + x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        r += (20 * math.sin(6 * x * math.pi) + 20 * math.sin(2 * x * math.pi)) * 2 / 3
        r += (20 * math.sin(x * math.pi) + 40 * math.sin(x / 3 * math.pi)) * 2 / 3
        r += (150 * math.sin(x / 12 * math.pi) + 300 * math.sin(x * math.pi / 30)) * 2 / 3
        return r

    dl, dn = tlat(lon - 105.0, lat - 35.0), tlon(lon - 105.0, lat - 35.0)
    rl = lat / 180.0 * math.pi
    m = 1 - ee * math.sin(rl) ** 2
    sm = math.sqrt(m)
    return (
        lat + (dl * 180.0) / ((a * (1 - ee)) / (m * sm) * math.pi),
        lon + (dn * 180.0) / (a / sm * math.cos(rl) * math.pi),
    )


def read_status(sn: str) -> tuple[dict, float, float]:
    out = subprocess.run(ninecli_argv(SKILL_DIR, "status", sn, "--json"), capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise SystemExit("ninecli status 失败，请检查登录状态和 SN")
    data = json.loads(out.stdout)
    loc = data.get("loc") or {}
    try:
        return data, float(loc["lat"]), float(loc["lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit("车辆状态未返回有效坐标") from exc


def regeo(lon: float, lat: float, key: str) -> dict:
    q = urllib.parse.urlencode({
        "key": key,
        "location": f"{lon:.7f},{lat:.7f}",
        "output": "JSON",
        "radius": "500",
        "extensions": "all",
    })
    req = urllib.request.Request(
        "https://restapi.amap.com/v3/geocode/regeo?" + q,
        headers={"User-Agent": "ninebot-show-skill/3.2.1"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        # Do not echo req.full_url: it contains the AMap key and exact coordinates.
        return {"error": "高德逆地理编码请求失败"}
    if str(data.get("status")) != "1":
        return {"error": str(data.get("info") or "unknown")}
    rg = data.get("regeocode") or {}
    ac = rg.get("addressComponent") or {}
    return {
        "formatted": rg.get("formatted_address"),
        "province": ac.get("province"),
        "city": ac.get("city"),
        "district": ac.get("district"),
        "township": ac.get("township"),
        "street_number": ac.get("streetNumber"),
        "roads": [(x.get("name"), x.get("distance")) for x in (rg.get("roads") or [])[:3]],
        "pois": [(x.get("name"), x.get("distance")) for x in (rg.get("pois") or [])[:6]],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--privacy", choices=["off", "district", "exact", "coordinates"], default="district")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--include-map-link", action="store_true", help="显式输出含精确坐标的高德 marker 链接")
    args = ap.parse_args()

    if args.privacy == "off":
        payload = {"location": "已隐藏", "privacy": "off"}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else "📍 位置已隐藏")
        return

    sn = load_sn()
    status, wlat, wlon = read_status(sn)
    glat, glon = wgs84_to_gcj02(wlat, wlon)
    key = amap_key()
    info = {}
    if args.privacy in {"district", "exact"}:
        if not key:
            info = {"error": "AMAP_WEB_KEY 未配置"}
        else:
            send_lat, send_lon = (district_safe_gcj02(glat, glon) if args.privacy == "district" else (glat, glon))
            info = regeo(send_lon, send_lat, key)

    if args.privacy == "district":
        if info.get("formatted"):
            loc_text = "".join(str(info.get(k) or "") for k in ("province", "city", "district"))
        else:
            loc_text = "已获取坐标（未解析地址）"
    elif args.privacy == "exact":
        loc_text = info.get("formatted") or "已获取坐标（未解析地址）"
    else:
        loc_text = f"{glon:.6f},{glat:.6f}"

    payload = {
        "location": loc_text,
        "privacy": args.privacy,
        "curspeed": status.get("curspeed"),
        "charging": status.get("charging"),
        "barrel_lock": status.get("barrel_lock_status"),
    }

    # Never attach exact coordinates or detailed reverse-geocode data to district mode.
    if args.privacy == "district":
        payload["area"] = {
            "province": info.get("province"),
            "city": info.get("city"),
            "district": info.get("district"),
        }
    elif args.privacy == "exact":
        payload["formatted_address"] = info.get("formatted")
    elif args.privacy == "coordinates":
        payload["coords_gcj02"] = {"lat": round(glat, 7), "lon": round(glon, 7)}
        payload["coords_wgs84_raw"] = {"lat": wlat, "lon": wlon}

    if args.include_map_link and args.privacy in {"exact", "coordinates"}:
        payload["amap_url"] = (
            f"https://uri.amap.com/marker?position={glon:.6f},{glat:.6f}"
            "&name=%E4%B9%9D%E5%8F%B7%E8%BD%A6%E8%BE%86&callnative=1"
        )

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("📍 " + str(loc_text))
        if args.privacy == "coordinates":
            print(f"   GCJ-02: {glon:.6f}, {glat:.6f}")
            print(f"   WGS-84: {wlon:.6f}, {wlat:.6f}")
        if args.include_map_link and payload.get("amap_url"):
            print("   高德链接: " + str(payload["amap_url"]))


if __name__ == "__main__":
    main()
