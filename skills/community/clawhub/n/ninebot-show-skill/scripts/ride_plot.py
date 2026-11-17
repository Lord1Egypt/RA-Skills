#!/usr/bin/env python3
"""九号最近一次骑行图：左侧轨迹，右侧速度-里程曲线。

用法: ride_plot.py [travel_id]
依赖: Pillow。OSM 瓦片默认直连；如需代理可设置 NINEBOT_MAP_PROXY。
"""
import datetime
import json
import math
import pathlib
import os
import subprocess
import sys
import urllib.request

from runtime_config import config_path, output_dir, ninecli_argv

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
CFG = config_path()


def load_vehicle_config():
    data = json.loads(CFG.read_text(encoding="utf-8"))
    nb = data.get("ninebot") or {}
    sn = str(nb.get("sn") or "").strip()
    if not sn or "请填写" in sn or sn.upper().startswith("REPLACE_WITH"):
        raise SystemExit("ninebot.sn 未配置")
    name = str(nb.get("vehicle_name") or "九号电动车")
    return sn, name

SN, VEHICLE_NAME = load_vehicle_config()
PROXY = os.environ.get("NINEBOT_MAP_PROXY", "").strip()
OUTDIR = output_dir()
OUTDIR.mkdir(parents=True, exist_ok=True)
ZOOM = 16

from PIL import Image, ImageDraw, ImageFont  # noqa: E402


def font(sz):
    for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def hav_km(la1, lo1, la2, lo2):
    R = 6371.0088
    p = math.pi / 180
    dla, dlo = (la2 - la1) * p, (lo2 - lo1) * p
    a = math.sin(dla / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def latest_ride():
    out = subprocess.run(ninecli_argv(SKILL_DIR, "travel", SN, "--json"), capture_output=True, text=True, timeout=60)
    rs = json.loads(out.stdout)["list"]
    return rs[0]


def ride_detail(tid):
    out = subprocess.run(ninecli_argv(SKILL_DIR, "travel", SN, "--detail", tid, "--json"),
                         capture_output=True, text=True, timeout=60)
    return json.loads(out.stdout)


def deg2px(lon, lat, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n * 256
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n * 256
    return x, y


def fetch_tiles(lons, lats, z=ZOOM):
    """返回 (底图 Image, 像素换算函数)。抓不到就返回 (None, 换算函数)。"""
    x0, y0 = deg2px(min(lons), max(lats), z)
    x1, y1 = deg2px(max(lons), min(lats), z)
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int(x1 // 256), int(y1 // 256)
    if (tx1 - tx0 + 1) * (ty1 - ty0 + 1) > 24:
        return None, None
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    base = Image.new("RGB", (W, H), (240, 240, 238))
    if PROXY:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    else:
        opener = urllib.request.build_opener()
    got = 0
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            url = f"https://tile.openstreetmap.org/{z}/{tx}/{ty}.png"
            req = urllib.request.Request(url, headers={"User-Agent": "ninebot-show-skill/3.2.1"})
            try:
                with opener.open(req, timeout=25) as r:
                    base.paste(Image.open(r).convert("RGB"), ((tx - tx0) * 256, (ty - ty0) * 256))
                got += 1
            except Exception:
                pass
    if got == 0:
        return None, None

    def to_px(lon, lat):
        px, py = deg2px(lon, lat, z)
        return px - tx0 * 256, py - ty0 * 256
    return base, to_px


def main():
    tid = sys.argv[1] if len(sys.argv) > 1 else latest_ride()["travel_id"]
    meta = latest_ride() if len(sys.argv) == 1 else {}
    d = ride_detail(tid)
    pts = [p.split(",") for p in d["trail"].split(";") if p]
    lon = [float(p[0]) for p in pts]
    lat = [float(p[1]) for p in pts]
    sp = [float(p[2]) for p in pts]
    dist = [0.0]
    for i in range(1, len(pts)):
        dist.append(dist[-1] + hav_km(lat[i - 1], lon[i - 1], lat[i], lon[i]))

    # ---- 左：轨迹 ----
    base, to_px = fetch_tiles(lon, lat)
    if base is not None:
        PAD = 28
        px = [to_px(a, b) for a, b in zip(lon, lat)]
        xs = [p[0] for p in px]
        ys = [p[1] for p in px]
        cx0, cx1 = max(0, int(min(xs)) - PAD), min(base.width, int(max(xs)) + PAD)
        cy0, cy1 = max(0, int(min(ys)) - PAD), min(base.height, int(max(ys)) + PAD)
        left = base.crop((cx0, cy0, cx1, cy1))
        off = (cx0, cy0)
    else:
        left = Image.new("RGB", (760, 760), (245, 245, 242))
        xs = [(x - min(lon)) / max(max(lon) - min(lon), 1e-9) * 720 + 20 for x in lon]
        ys = [740 - (y - min(lat)) / max(max(lat) - min(lat), 1e-9) * 720 for y in lat]
        off = (0, 0)
        px = list(zip(xs, ys))
    dl = ImageDraw.Draw(left)
    vmin, vmax = min(sp), max(sp)
    for i in range(len(px) - 1):
        t = 0.0 if vmax == vmin else (sp[i] - vmin) / (vmax - vmin)
        color = (int(40 + 215 * t), int(90 - 60 * t), int(230 - 190 * t))
        a = (px[i][0] - off[0], px[i][1] - off[1])
        b = (px[i + 1][0] - off[0], px[i + 1][1] - off[1])
        dl.line([a, b], fill=color, width=5)
    sx, sy = px[0][0] - off[0], px[0][1] - off[1]
    ex, ey = px[-1][0] - off[0], px[-1][1] - off[1]
    dl.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(30, 170, 60), outline=(255, 255, 255), width=2)
    dl.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(210, 40, 40), outline=(255, 255, 255), width=2)

    # ---- 右：速度曲线 ----
    right = Image.new("RGB", (760, left.height), "white")
    dr = ImageDraw.Draw(right)
    f_s, f_t = font(15), font(19)
    L, R, T, B = 70, 30, 60, 60
    vmax_y = max(70, int(vmax // 10 * 10 + 10))
    dx, dy = max(dist[-1], 0.01), vmax_y

    def X(v):
        return L + (right.width - L - R) * v / dx

    def Y(v):
        return right.height - B - (right.height - T - B) * min(v, vmax_y) / vmax_y

    for v in range(0, vmax_y + 1, 10):
        dr.line([L, Y(v), right.width - R, Y(v)], fill=(233, 233, 233))
        dr.text((L - 42, Y(v) - 7), str(v), font=f_s, fill=(95, 95, 95))
    dr.line([L, T, L, right.height - B], fill=(70, 70, 70), width=2)
    dr.line([L, right.height - B, right.width - R, right.height - B], fill=(70, 70, 70), width=2)
    dr.line([(X(a), Y(b)) for a, b in zip(dist, sp)], fill=(31, 119, 180), width=3, joint="curve")
    imax = sp.index(max(sp))
    dr.ellipse([X(dist[imax]) - 4, Y(sp[imax]) - 4, X(dist[imax]) + 4, Y(sp[imax]) + 4], fill=(214, 39, 40))
    dr.text((X(dist[imax]) - 30, Y(sp[imax]) - 26), f"最高 {max(sp):.0f} km/h", font=f_s, fill=(214, 39, 40))
    dr.text((L, 20), "速度 - 里程曲线", font=f_t, fill=(25, 25, 25))
    dr.text((L - 56, T + 4), "km/h", font=f_s, fill=(95, 95, 95))
    dr.text((right.width - R - 60, right.height - B + 22), "里程 (km)", font=f_s, fill=(95, 95, 95))

    # ---- 拼图 + 标题栏 ----
    W = left.width + right.width
    H = left.height + 92
    img = Image.new("RGB", (W, H), "white")
    img.paste(left, (0, 92))
    img.paste(right, (left.width, 92))
    dt = ImageDraw.Draw(img)
    try:
        start = datetime.datetime.fromtimestamp(int(d["start_time"])).strftime("%m/%d %H:%M")
        end = datetime.datetime.fromtimestamp(int(d["end_time"])).strftime("%H:%M")
    except Exception:
        start, end = "?", "?"
    dur = int(d.get("duration") or 0)
    dt.text((20, 16), f"{VEHICLE_NAME} · 最近一次骑行 {start}~{end}", font=font(21), fill=(15, 15, 15))
    dt.text((20, 48), f"{float(d['mileages']):.2f} km / {dur//60}分{dur%60}秒 | 最高 {max(sp):.0f} | 逐点均值 {sum(sp)/len(sp):.1f} | "
                      f"里程均速 {float(d['mileages'])/(dur/3600):.1f} km/h | {len(sp)} 个采样点",
            font=font(15), fill=(95, 95, 95))
    dt.text((20, 70), "左：轨迹（颜色=速度，绿点=起点，红点=终点；底图 © OpenStreetMap）　右：速度-里程",
            font=font(13), fill=(130, 130, 130))
    img.save(OUT := str(OUTDIR / f"ninebot-ride-{tid[:8]}.png"))
    print(OUT, img.size)


if __name__ == "__main__":
    main()
