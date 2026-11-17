#!/usr/bin/env python3
"""把一或多趟骑行的 trail 画到高德静态图上（输出 PNG）。

用法:
  render_trail.py --out /tmp/track.png --ride <travel_id> [--ride ...]
  render_trail.py --out /tmp/today.png --today            # 今天全部骑行
  render_trail.py --out /tmp/x.png --ride <id> --sn <车辆SN> --zoom 15 --legend

要点:
  1. 点的坐标按 WGS-84 处理，绘制到高德前必须先转 GCJ-02。
  2. 高德静态图的实际分辨率比直觉高一档：meters/px = 156543.03392*cos(lat) / 2**(zoom+1+log2(scale))。
     像素换算按 Web Mercator 公式计算；不要在通用脚本注释中保留真实轨迹坐标样本。
  3. bbox 使用全部轨迹点计算，避免中段绕行超出画布。
  4. 
  轨迹字段名是 `trail`，格式 `lng,lat,col3,col4;...`；其中 **col3 是该点瞬时速度**（其最大值 == 列表接口的 `speed` 字段，可互相验算）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import pathlib
import subprocess
import sys
import urllib.request
import urllib.parse
import urllib.error

from runtime_config import config_path, env_value, ninecli_argv

from PIL import Image, ImageDraw, ImageFont

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
SIZE, SCALE = (1000, 1000), 2
PALETTE = [(255, 138, 0), (47, 107, 255), (34, 197, 94), (168, 85, 247), (236, 72, 153)]


def load_font(size: int):
    for candidate in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def amap_key():
    value = env_value(("AMAP_WEBSERVICE_KEY", "AMAP_WEB_KEY"))
    if value:
        return value
    sys.exit("no AMAP key")


def wgs2gcj(lat, lon):
    a, ee = 6378245.0, 0.00669342162296594323

    def _tlat(x, y):
        r = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        r += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        r += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return r

    def _tlon(x, y):
        r = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        r += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        r += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        r += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x * math.pi / 30.0)) * 2.0 / 3.0
        return r

    dlat, dlon = _tlat(lon - 105.0, lat - 35.0), _tlon(lon - 105.0, lat - 35.0)
    rad = lat / 180.0 * math.pi
    m = 1 - ee * math.sin(rad) ** 2
    sm = math.sqrt(m)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (m * sm) * math.pi)
    dlon = (dlon * 180.0) / (a / sm * math.cos(rad) * math.pi)
    return lat + dlat, lon + dlon


def world_px(lng, lat, n):
    x = (lng + 180.0) / 360.0 * n
    rad = math.radians(lat)
    y = (1 - math.log(math.tan(rad) + 1 / math.cos(rad)) / math.pi) / 2 * n
    return x, y


def load_ride(ride_id, sn):
    raw = subprocess.run(ninecli_argv(SKILL_DIR, "travel", sn, "--detail", ride_id, "--json"),
                         capture_output=True, text=True, timeout=90).stdout
    d = json.loads(raw)
    pts = []
    for chunk in (d.get("trail") or "").split(";"):
        parts = chunk.split(",")
        if len(parts) < 2 or not parts[0].strip():
            continue
        lng, lat = float(parts[0]), float(parts[1])
        speed = float(parts[2]) if len(parts) > 2 and parts[2] not in ("", "None") else None
        glat, glon = wgs2gcj(lat, lng)
        pts.append({"lng": glon, "lat": glat, "speed": speed})
    return {"id": ride_id, "meta": d, "points": pts}


def today_ride_ids(sn):
    raw = subprocess.run(ninecli_argv(SKILL_DIR, "travel", sn, "--json"), capture_output=True, text=True, timeout=90).stdout
    d = json.loads(raw)
    today = dt.date.today()
    ids = []
    for r in d.get("list", []):
        if float(r.get("mileages") or 0) <= 0:
            continue
        if dt.datetime.fromtimestamp(r["end_time"]).date() == today:
            ids.append(r["travel_id"])
    return ids


def configured_sn():
    cfg = config_path()
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
        sn = str((data.get("ninebot") or {}).get("sn") or "").strip()
    except Exception:
        sn = ""
    if not sn or "请填写" in sn or sn.upper().startswith("REPLACE_WITH"):
        sys.exit("need --sn <车辆SN> or configure ~/.config/ninebot-show-skill/config.json")
    return sn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--ride", action="append", default=[])
    ap.add_argument("--today", action="store_true")
    ap.add_argument("--sn", default=None)
    ap.add_argument("--zoom-min", type=int, default=13)
    ap.add_argument("--no-legend", action="store_true")
    args = ap.parse_args()
    if not args.sn:
        args.sn = configured_sn()

    ids = list(args.ride)
    if args.today:
        ids += today_ride_ids(args.sn)
    if not ids:
        sys.exit("need --ride <id> and/or --today")

    rides = [load_ride(r, args.sn) for r in ids]
    rides = [r for r in rides if r["points"]]
    allpts = [p for r in rides for p in r["points"]]
    lons = [p["lng"] for p in allpts]
    lats = [p["lat"] for p in allpts]
    center = ((min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2)
    W, H = SIZE[0] * SCALE, SIZE[1] * SCALE

    def pick_zoom(margin=0.86):
        for z in range(18, args.zoom_min - 1, -1):
            n = 256 * (2 ** (z + 1)) * SCALE
            cx, cy = world_px(*center, n)
            if all(W * (1 - margin) / 2 < (world_px(lo, la, n)[0] - cx) + W / 2 < W * (1 + margin) / 2
                   and H * (1 - margin) / 2 < (world_px(lo, la, n)[1] - cy) + H / 2 < H * (1 + margin) / 2
                   for lo, la in zip(lons, lats)):
                return z, n
        return args.zoom_min, 256 * (2 ** (args.zoom_min + 1)) * SCALE

    zoom, n = pick_zoom()
    cx, cy = world_px(*center, n)

    def px(lng, lat):
        x, y = world_px(lng, lat, n)
        return (x - cx) + W / 2, (y - cy) + H / 2

    base = pathlib.Path(args.out).with_suffix(".base.png")
    params = {
        "location": f"{center[0]:.6f},{center[1]:.6f}",
        "zoom": str(zoom),
        "size": f"{SIZE[0]}*{SIZE[1]}",
        "scale": str(SCALE),
        "key": amap_key(),
    }
    url = "https://restapi.amap.com/v3/staticmap?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ninebot-show-skill/3.2.1"})
    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            base.write_bytes(response.read())
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        # Do not expose the full URL: it contains the AMap key and the ride-area center.
        sys.exit("高德轨迹底图请求失败（已隐藏请求 URL 和参数）")
    im = Image.open(base).convert("RGB")
    dr = ImageDraw.Draw(im, "RGBA")

    for r in rides:
        dr.line([px(p["lng"], p["lat"]) for p in r["points"]], fill=(0, 0, 0, 158), width=13, joint="curve")
    rows = []
    for i, r in enumerate(rides):
        color = PALETTE[i % len(PALETTE)]
        xy = [px(p["lng"], p["lat"]) for p in r["points"]]
        dr.line(xy, fill=color + (248,), width=7, joint="curve")
        for (x, y), c in ((xy[0], (34, 197, 94)), (xy[-1], (239, 68, 68))):
            dr.ellipse([x - 12, y - 12, x + 12, y + 12], fill=c, outline=(255, 255, 255), width=3)
        m = r["meta"]
        t0 = dt.datetime.fromtimestamp(m["start_time"]).strftime("%H:%M")
        t1 = dt.datetime.fromtimestamp(m["end_time"]).strftime("%H:%M")
        rows.append(f"{t0}–{t1}  {float(m['mileages']):.1f} km  最高 {m['speed']} km/h")

    if not args.no_legend:
        f_big = load_font(34)
        f = load_font(27)
        title = "九号骑行轨迹 · 高德底图 · WGS-84→GCJ-02"
        pad = 26
        box_w = int(max([f_big.getlength(title)] + [f.getlength(t) + 78 for t in rows])) + pad * 2
        box_h = 46 + 42 * len(rows)
        lx, ly = 26, H - box_h - 26
        dr.rectangle([lx, ly, lx + box_w, ly + box_h], fill=(15, 17, 21, 225))
        dr.text((lx + pad, ly + 16), title, font=f_big, fill=(255, 255, 255))
        for i, text in enumerate(rows):
            yy = ly + 72 + i * 42
            dr.line([lx + pad, yy, lx + pad + 54, yy], fill=PALETTE[i % len(PALETTE)], width=9)
            dr.text((lx + pad + 72, yy - 16), text, font=f, fill=(238, 242, 250))

    out = pathlib.Path(args.out)
    im.save(out)
    base.unlink(missing_ok=True)
    print(f"{out} {im.size} zoom={zoom} rides={len(rides)} points={len(allpts)} bytes={out.stat().st_size}")
    for r in rows:
        print("  ", r)


if __name__ == "__main__":
    main()
