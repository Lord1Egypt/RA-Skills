#!/usr/bin/env python3
"""
photo_analyzer.py — 照片 EXIF 时间线提取工具（T-03）

用法：
  python photo_analyzer.py --dir /path/to/photos --output timeline.md
  python photo_analyzer.py --dir /path/to/photos --person "爷爷"
"""

import argparse
import os
from datetime import datetime
from typing import Optional


# ── EXIF 提取 ─────────────────────────────────────────────────────────────────

def try_read_exif(filepath: str) -> dict:
    """尝试读取照片 EXIF 数据，无 Pillow 时降级处理。"""
    result = {
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "datetime": None,
        "gps_lat": None,
        "gps_lon": None,
        "location_hint": None,
    }

    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS

        with Image.open(filepath) as img:
            exif_data = img._getexif()
            if not exif_data:
                return result

            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)

                if tag == "DateTimeOriginal" or tag == "DateTime":
                    try:
                        result["datetime"] = datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S")
                    except ValueError:
                        pass

                if tag == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_tag = GPSTAGS.get(t, t)
                        gps_data[sub_tag] = value[t]

                    lat = _dms_to_decimal(gps_data.get("GPSLatitude"), gps_data.get("GPSLatitudeRef"))
                    lon = _dms_to_decimal(gps_data.get("GPSLongitude"), gps_data.get("GPSLongitudeRef"))
                    if lat and lon:
                        result["gps_lat"] = lat
                        result["gps_lon"] = lon

    except ImportError:
        # Pillow 未安装，尝试从文件名/路径提取日期
        result["datetime"] = _extract_date_from_filename(os.path.basename(filepath))
    except Exception:
        result["datetime"] = _extract_date_from_filename(os.path.basename(filepath))

    return result


def _dms_to_decimal(dms, ref) -> Optional[float]:
    """将度分秒转为十进制坐标。"""
    if not dms or not ref:
        return None
    try:
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        decimal = degrees + minutes / 60 + seconds / 3600
        if ref in ("S", "W"):
            decimal = -decimal
        return round(decimal, 6)
    except (TypeError, IndexError, ValueError):
        return None


def _extract_date_from_filename(filename: str) -> Optional[datetime]:
    """从文件名中提取日期（常见命名规律）。"""
    # IMG_20231225_120000.jpg 或 20231225_120000.jpg
    match = re.search(r"(\d{4})(\d{2})(\d{2})", filename)
    if match:
        try:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            pass
    return None


import re  # 需要在模块级别


# ── 扫描目录 ──────────────────────────────────────────────────────────────────

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".tiff", ".tif"}


def scan_photos(directory: str) -> list[dict]:
    """扫描目录下所有照片，提取 EXIF 数据。"""
    results = []
    for root, _, files in os.walk(directory):
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if ext in PHOTO_EXTENSIONS:
                filepath = os.path.join(root, fname)
                data = try_read_exif(filepath)
                results.append(data)
    return results


# ── 时间线构建 ────────────────────────────────────────────────────────────────

def build_timeline(photos: list[dict]) -> list[dict]:
    """将照片按时间排序，构建时间线。"""
    dated = [p for p in photos if p["datetime"]]
    undated = [p for p in photos if not p["datetime"]]

    dated.sort(key=lambda p: p["datetime"])

    # 按年份/月份分组
    timeline = []
    current_group = None
    current_key = None

    for photo in dated:
        dt = photo["datetime"]
        key = f"{dt.year}-{dt.month:02d}"

        if key != current_key:
            if current_group:
                timeline.append(current_group)
            current_group = {
                "year": dt.year,
                "month": dt.month,
                "key": key,
                "photos": [],
            }
            current_key = key

        current_group["photos"].append(photo)

    if current_group:
        timeline.append(current_group)

    return timeline, undated


# ── GPS 地点提示 ──────────────────────────────────────────────────────────────

def guess_location(lat: float, lon: float) -> str:
    """根据 GPS 坐标猜测大致地点（中国范围）。"""
    if lat is None or lon is None:
        return ""

    # 粗略判断省份（仅供参考）
    if 39.0 <= lat <= 41.5 and 115.0 <= lon <= 117.5:
        return "（北京附近）"
    elif 29.0 <= lat <= 31.5 and 120.0 <= lon <= 122.5:
        return "（上海附近）"
    elif 22.0 <= lat <= 24.5 and 112.0 <= lon <= 114.5:
        return "（广州/深圳附近）"
    elif 27.0 <= lat <= 30.0 and 111.0 <= lon <= 114.0:
        return "（湖南附近）"
    elif 30.0 <= lat <= 32.0 and 113.0 <= lon <= 115.0:
        return "（武汉附近）"
    elif 30.5 <= lat <= 31.5 and 103.5 <= lon <= 104.5:
        return "（成都附近）"
    else:
        return f"（坐标 {lat:.2f}°N, {lon:.2f}°E）"


# ── 输出格式化 ────────────────────────────────────────────────────────────────

def format_timeline(timeline: list[dict], undated: list[dict], person_name: str = "") -> str:
    """将时间线格式化为 Markdown。"""
    header = f"# {'「' + person_name + '」的' if person_name else ''}照片时间线\n\n"

    if not timeline and not undated:
        return header + "没有找到任何照片。\n"

    lines = [header]

    total_dated = sum(len(g["photos"]) for g in timeline)
    lines.append(f"共 {total_dated + len(undated)} 张照片，"
                 f"其中 {total_dated} 张有时间信息，{len(undated)} 张无时间信息。\n")

    if timeline:
        lines.append("## 按时间排列的照片\n")
        for group in timeline:
            lines.append(f"### {group['year']}年{group['month']}月")
            for photo in group["photos"]:
                dt = photo["datetime"]
                location = ""
                if photo.get("gps_lat"):
                    location = " " + guess_location(photo["gps_lat"], photo["gps_lon"])
                lines.append(f"- `{photo['filename']}` — {dt.strftime('%Y-%m-%d %H:%M')}{location}")
            lines.append("")

    if undated:
        lines.append("## 无时间信息的照片\n")
        lines.append("（这些照片没有 EXIF 时间，可以手动注明拍摄时间）\n")
        for photo in undated:
            lines.append(f"- `{photo['filename']}` — [时间待补充]")
        lines.append("")

    lines.append("---")
    lines.append("*照片时间线可用于填充 remembrance.md 的生命时间轴部分。*")

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="照片 EXIF 时间线提取工具")
    parser.add_argument("--dir", required=True, help="照片所在目录")
    parser.add_argument("--person", default="", help="人物名称（用于报告标题）")
    parser.add_argument("--output", help="输出时间线报告的路径（默认输出到控制台）")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"[错误] 找不到目录：{args.dir}")
        return

    print(f"[扫描] 正在扫描 {args.dir} ...")
    photos = scan_photos(args.dir)
    print(f"[找到] {len(photos)} 张照片")

    timeline, undated = build_timeline(photos)
    report = format_timeline(timeline, undated, args.person)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[输出] 时间线已保存到 {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
