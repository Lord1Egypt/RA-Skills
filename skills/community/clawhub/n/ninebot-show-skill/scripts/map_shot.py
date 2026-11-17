#!/usr/bin/env python3
"""Generate an AMap static-map PNG for the current vehicle location."""
from __future__ import annotations

import datetime
import json
import os
from pathlib import Path

from runtime_config import env_value, output_dir
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error

SKILL_DIR = Path(__file__).resolve().parents[1]
LOCATE = SKILL_DIR / "scripts" / "locate.py"
PYTHON = SKILL_DIR / ".venv" / "bin" / "python"
OUTDIR = output_dir()


def key() -> str:
    value = env_value(("AMAP_WEBSERVICE_KEY", "AMAP_WEB_KEY"))
    if value:
        return value
    raise SystemExit("AMAP_WEB_KEY 未配置")


def coords() -> tuple[float, float]:
    py = str(PYTHON if PYTHON.exists() else Path(sys.executable))
    out = subprocess.run([py, str(LOCATE), "--privacy", "coordinates", "--json"], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise SystemExit(out.stderr.strip() or "定位失败")
    data = json.loads(out.stdout)
    g = data["coords_gcj02"]
    return float(g["lon"]), float(g["lat"])


def main() -> None:
    zoom = sys.argv[1] if len(sys.argv) > 1 else "16"
    lon, lat = coords()
    loc = f"{lon:.6f},{lat:.6f}"
    params = {
        "location": loc,
        "zoom": zoom,
        "size": "900*600",
        "scale": "2",
        "markers": f"mid,0xFF0000,A:{loc}",
        "traffic": "0",
        "key": key(),
    }
    url = "https://restapi.amap.com/v3/staticmap?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ninebot-show-skill/3.2.1"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            ctype = r.headers.get("Content-Type", "")
            body = r.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        # Do not expose the full URL: it contains the AMap key and exact coordinates.
        raise SystemExit("高德静态地图请求失败（已隐藏请求 URL 和参数）")
    if "image" not in ctype:
        raise SystemExit("高德静态地图接口未返回图片")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = OUTDIR / f"ninebot-map-z{zoom}-{ts}.png"
    path.write_bytes(body)
    print(path)


if __name__ == "__main__":
    main()
