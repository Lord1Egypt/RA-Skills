#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datum_convert.py — GCJ-02 / BD-09 / WGS-84 坐标系转换（离线，无外部依赖）

为什么需要：中国大陆地图服务（腾讯/高德=GCJ-02，百度=BD-09）返回的坐标与 EXIF
标准要求的 WGS-84 存在偏移（约 300–600 米）。给照片写 GPS 前必须统一转成
WGS-84；中国大陆以外地区无此偏移，直接使用原坐标即可，勿做转换。

模式：
  1. 单点转换:      python3 datum_convert.py gcj2wgs 29.290169 90.978425
  2. 往返校验:      python3 datum_convert.py verify 29.290169 90.978425
  3. CSV 批量转换:  python3 datum_convert.py csv in.csv out.csv --lat-col lat --lon-col lon [--src gcj]
  4. 交互模式:      python3 datum_convert.py interactive   （从剪贴板粘贴"纬度,经度"逐行转换）

用法示例：
  python3 datum_convert.py gcj2wgs 39.907333 116.391083      # 天安门 GCJ-02 → WGS-84
  python3 datum_convert.py wgs2gcj 39.908746 116.391179      # 反向（校验用）
  python3 datum_convert.py bd2wgs 39.913905 116.397475       # 百度 BD-09 → WGS-84
  python3 datum_convert.py verify 29.290169 90.978425        # GCJ→WGS→GCJ 往返，偏差应为 0

坐标输入顺序统一为：纬度(lat) 经度(lon)，小数度。
"""
import sys
import math
import csv
import argparse

PI = math.pi
A = 6378245.0          # 长半轴
EE = 6.69342162296594323e-3  # 偏心率平方


def _out_of_china(lat: float, lon: float) -> bool:
    """粗判是否在中国大陆坐标加密范围外（境外坐标不做偏移转换）。"""
    return not (73.66 < lon < 135.05 and 3.86 < lat < 53.55)


def _transform_lat(x: float, y: float) -> float:
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320.0 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lon(x: float, y: float) -> float:
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret


def gcj02_to_wgs84(lat: float, lon: float) -> tuple:
    """GCJ-02 → WGS-84（迭代法，精度约 1e-6 度 ≈ 0.1 米）。"""
    if _out_of_china(lat, lon):
        return lat, lon  # 境外坐标无偏移，原样返回
    dlat = _transform_lat(lon - 105.0, lat - 35.0)
    dlon = _transform_lon(lon - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlon = (dlon * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    # 迭代求精（简单一次逆推已足够，迭代两次提高稳定性）
    wlat, wlon = lat - dlat, lon - dlon
    for _ in range(2):
        glat, glon = wgs84_to_gcj02(wlat, wlon)
        wlat += lat - glat
        wlon += lon - glon
    return wlat, wlon


def wgs84_to_gcj02(lat: float, lon: float) -> tuple:
    """WGS-84 → GCJ-02。"""
    if _out_of_china(lat, lon):
        return lat, lon
    dlat = _transform_lat(lon - 105.0, lat - 35.0)
    dlon = _transform_lon(lon - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlon = (dlon * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    return lat + dlat, lon + dlon


def bd09_to_gcj02(lat: float, lon: float) -> tuple:
    """BD-09 → GCJ-02（百度二次加密的逆变换）。"""
    x = lon - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PI * 3000.0 / 180.0)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PI * 3000.0 / 180.0)
    return z * math.sin(theta), z * math.cos(theta)


def gcj02_to_bd09(lat: float, lon: float) -> tuple:
    x = lon
    y = lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * PI * 3000.0 / 180.0)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * PI * 3000.0 / 180.0)
    return z * math.sin(theta) + 0.006, z * math.cos(theta) + 0.0065


def bd09_to_wgs84(lat: float, lon: float) -> tuple:
    return gcj02_to_wgs84(*bd09_to_gcj02(lat, lon))


def wgs84_to_bd09(lat: float, lon: float) -> tuple:
    return gcj02_to_bd09(*wgs84_to_gcj02(lat, lon))


CONVERTERS = {
    "gcj2wgs": (gcj02_to_wgs84, "GCJ-02", "WGS-84"),
    "wgs2gcj": (wgs84_to_gcj02, "WGS-84", "GCJ-02"),
    "bd2wgs": (bd09_to_wgs84, "BD-09", "WGS-84"),
    "wgs2bd": (wgs84_to_bd09, "WGS-84", "BD-09"),
}


def _offset_meters(lat1, lon1, lat2, lon2) -> float:
    """两点间近似距离（米），用于报告偏移量。"""
    dy = (lat2 - lat1) * 111320.0
    dx = (lon2 - lon1) * 111320.0 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.sqrt(dx * dx + dy * dy)


def cmd_point(mode, lat, lon):
    fn, src, dst = CONVERTERS[mode]
    rlat, rlon = fn(lat, lon)
    off = _offset_meters(lat, lon, rlat, rlon)
    print(f"{src} ({lat:.6f}, {lon:.6f})  ->  {dst} ({rlat:.6f}, {rlon:.6f})   偏移≈{off:.0f}m")
    return rlat, rlon


def cmd_verify(lat, lon):
    """GCJ→WGS→GCJ 往返校验：偏差应 < 0.01m，否则说明转换实现有问题。"""
    wlat, wlon = gcj02_to_wgs84(lat, lon)
    glat, glon = wgs84_to_gcj02(wlat, wlon)
    off = _offset_meters(lat, lon, glat, glon)
    status = "PASS" if off < 0.01 else "FAIL"
    print(f"原始 GCJ-02   : ({lat:.6f}, {lon:.6f})")
    print(f"转换 WGS-84   : ({wlat:.6f}, {wlon:.6f})")
    print(f"回转 GCJ-02   : ({glat:.6f}, {glon:.6f})")
    print(f"往返偏差      : {off:.6f} m  [{status}]")
    if status == "FAIL":
        sys.exit(1)


def cmd_csv(inpath, outpath, lat_col, lon_col, src):
    """批量转换 CSV 中的坐标列，原地新增/覆盖 WGS-84 列。"""
    fn, sname, dname = CONVERTERS[f"{src}2wgs"]
    with open(inpath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        wlat_col, wlon_col = f"wgs_{lat_col}", f"wgs_{lon_col}"
        for c in (wlat_col, wlon_col):
            if c not in fields:
                fields.append(c)
        rows = list(reader)
    n = 0
    for r in rows:
        try:
            lat, lon = float(r[lat_col]), float(r[lon_col])
        except (KeyError, ValueError, TypeError):
            continue
        wlat, wlon = fn(lat, lon)
        r[wlat_col], r[wlon_col] = f"{wlat:.6f}", f"{wlon:.6f}"
        n += 1
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"转换 {n}/{len(rows)} 行  {sname} -> WGS-84  输出: {outpath}")


def main():
    ap = argparse.ArgumentParser(description="GCJ-02/BD-09/WGS-84 坐标转换（写 EXIF GPS 前必转 WGS-84）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("convert", help="单点转换")
    p1.add_argument("mode", choices=list(CONVERTERS))
    p1.add_argument("lat", type=float)
    p1.add_argument("lon", type=float)

    p2 = sub.add_parser("verify", help="GCJ→WGS→GCJ 往返校验（偏差应为 0）")
    p2.add_argument("lat", type=float)
    p2.add_argument("lon", type=float)

    p3 = sub.add_parser("csv", help="CSV 批量转换（新增 wgs_ 前缀列）")
    p3.add_argument("infile")
    p3.add_argument("outfile")
    p3.add_argument("--lat-col", default="lat")
    p3.add_argument("--lon-col", default="lon")
    p3.add_argument("--src", choices=["gcj", "bd"], default="gcj")

    args = ap.parse_args()
    if args.cmd == "convert":
        cmd_point(args.mode, args.lat, args.lon)
    elif args.cmd == "verify":
        cmd_verify(args.lat, args.lon)
    elif args.cmd == "csv":
        cmd_csv(args.infile, args.outfile, args.lat_col, args.lon_col, args.src)


if __name__ == "__main__":
    main()
