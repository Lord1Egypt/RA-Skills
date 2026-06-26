#!/usr/bin/env python3
"""
kml-parser.py — KML 轨迹解析器

解析 KML 文件（Google Earth XML 格式），提取：起终点坐标、总距离、累计爬升/下降、海拔曲线。
输出 JSON 格式，与 gpx-parser.py 完全一致，供 hike-planner.js 使用。

用法:
  python3 assets/kml-parser.py <kml_file> [--json]

依赖: 仅 Python 标准库（xml.etree.ElementTree + math）

KML 坐标格式说明:
  - KML 经纬度顺序为 lng,lat,alt（与 GPX 的 lat,lng 相反！）
  - Track/Path 数据在 <LineString> 或 <gx:Track> 中
  - Waypoints 在 <Placemark> 中
  - 坐标格式: "lng,lat,alt lng,lat,alt ..."（空格分隔元组，逗号分隔分量）

输出格式:
{
  "start": { "lat": 31.828018, "lng": 105.607799 },
  "end": { "lat": 31.891916, "lng": 105.542436 },
  "distance_km": 12.7,
  "ascent_m": 350,
  "descent_m": 490,
  "max_altitude_m": 697,
  "min_altitude_m": 450,
  "point_count": 520,
  "elevation_curve": [{"dist_km": 0.0, "elevation_m": 697}, ...],
  "source": "kml"
}
"""

import json
import sys
import os
import math
import xml.etree.ElementTree as ET

HAVERSINE_R = 6371000  # 地球半径（米）

# KML 常见命名空间
KML_URI = 'http://www.opengis.net/kml/2.2'
GX_URI = 'http://www.google.com/kml/ext/2.2'
NS_MAP = {'kml': KML_URI, 'gx': GX_URI}


def haversine(lat1, lng1, lat2, lng2):
    """计算两点间距离（米）"""
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    return HAVERSINE_R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _parse_coordinates(coord_text):
    """
    解析 KML 坐标字符串。
    格式: "lng1,lat1,alt1 lng2,lat2,alt2 ..."
    注意: KML 是 lng,lat,alt 顺序，与 GPX 的 lat,lng 相反！
    返回 [{'lng': x, 'lat': y, 'elevation': z}, ...]
    """
    points = []
    if not coord_text or not coord_text.strip():
        return points

    tuples = coord_text.strip().split()
    for t in tuples:
        parts = t.split(',')
        if len(parts) < 2:
            continue
        try:
            lng = float(parts[0].strip())
            lat = float(parts[1].strip())
            ele = float(parts[2].strip()) if len(parts) > 2 and parts[2].strip() else 0
            points.append({'lng': lng, 'lat': lat, 'elevation': ele})
        except (ValueError, IndexError):
            continue

    return points


def _find_elem(parent, tag):
    """
    查找单个子元素：先尝试 kml: 前缀，再尝试 gx: 前缀，
    然后尝试 Clark notation，最后尝试无命名空间。
    """
    # prefixed with namespace map
    result = parent.find(f'kml:{tag}', NS_MAP)
    if result is not None:
        return result
    result = parent.find(f'gx:{tag}', NS_MAP)
    if result is not None:
        return result
    # Clark notation
    result = parent.find(f'{{{KML_URI}}}{tag}')
    if result is not None:
        return result
    result = parent.find(f'{{{GX_URI}}}{tag}')
    if result is not None:
        return result
    # no namespace
    return parent.find(tag)


def _find_all_elem(parent, tag):
    """
    查找所有匹配子元素（包括后代），
    依次尝试各种命名空间形式和裸标签名。
    自动去重（基于元素 id）。
    """
    results = []
    seen = set()
    for candidate in (
        parent.findall(f'.//kml:{tag}', NS_MAP)
        + parent.findall(f'.//gx:{tag}', NS_MAP)
        + parent.findall(f'.//{{{KML_URI}}}{tag}')
        + parent.findall(f'.//{{{GX_URI}}}{tag}')
        + parent.findall(f'.//{tag}')
    ):
        eid = id(candidate)
        if eid not in seen:
            seen.add(eid)
            results.append(candidate)
    return results


def _parse_gx_track(placemark_elem):
    """
    解析 <gx:Track> 元素中的轨迹点。
    格式:
      <gx:Track>
        <when>...</when>
        <gx:coord>lng lat alt</gx:coord>
        ...
      </gx:Track>
    注意: gx:coord 使用空格分隔 lng lat alt
    """
    points = []

    track_el = _find_elem(placemark_elem, 'Track')
    if track_el is not None:
        coords = _find_all_elem(track_el, 'coord')

        for c in coords:
            text = (c.text or '').strip()
            parts = text.split()
            if len(parts) < 2:
                continue
            try:
                lng = float(parts[0])
                lat = float(parts[1])
                ele = float(parts[2]) if len(parts) > 2 else 0
                points.append({'lng': lng, 'lat': lat, 'elevation': ele})
            except (ValueError, IndexError):
                continue

    return points


def _find_longest_linestring(root):
    """
    查找最长的轨迹（LineString 或 gx:Track 中坐标点最多者）。
    返回 points 列表。
    """
    best_points = []

    # 查找所有 Placemark
    all_placemarks = _find_all_elem(root, 'Placemark')
    if not all_placemarks:
        return best_points

    # 去重
    seen = set()
    unique_placemarks = []
    for pm in all_placemarks:
        pid = pm.get('id', '')
        text_repr = ET.tostring(pm, encoding='unicode')[:100]
        key = pid + text_repr
        if key not in seen:
            seen.add(key)
            unique_placemarks.append(pm)

    for pm in unique_placemarks:
        # 1. 先检查 gx:Track
        track_points = _parse_gx_track(pm)
        if track_points and len(track_points) > len(best_points):
            best_points = track_points
            continue

        # 2. 再检查 LineString
        linestring = _find_elem(pm, 'LineString')
        if linestring is not None:
            coord_el = _find_elem(linestring, 'coordinates')
            if coord_el is not None:
                pts = _parse_coordinates(coord_el.text)
                if len(pts) > len(best_points):
                    best_points = pts

    return best_points


def _analyze_points(points):
    """分析轨迹点列表，计算统计数据（与 gpx-parser.py 一致）"""
    if not points or len(points) < 2:
        return {'error': '轨迹点不足（至少需要 2 个点）'}

    total_distance = 0
    total_ascent = 0
    total_descent = 0
    elevations = []
    elevation_curve = []

    prev = points[0]
    for i, pt in enumerate(points):
        ele = pt.get('elevation', 0)
        elevations.append(ele)

        if i > 0:
            dist = haversine(prev['lat'], prev['lng'], pt['lat'], pt['lng'])
            total_distance += dist
            ele_diff = pt['elevation'] - prev['elevation']
            # Garmin 每秒记录一次，相邻点海拔变化平均仅 0.08m
            # 3m 阈值会把所有真实爬升过滤成 0。0.5m 可滤 GPS 噪声但保留真实数据
            if abs(ele_diff) >= 0.5:
                if ele_diff > 0:
                    total_ascent += ele_diff
                else:
                    total_descent += abs(ele_diff)

        # 海拔曲线采样（每 200 米采一个点）
        if i == 0 or total_distance > len(elevation_curve) * 200:
            elevation_curve.append({
                'dist_km': round(total_distance / 1000, 2),
                'elevation_m': ele,
            })

        prev = pt

    return {
        'start': {'lat': points[0]['lat'], 'lng': points[0]['lng']},
        'end': {'lat': points[-1]['lat'], 'lng': points[-1]['lng']},
        'distance_km': round(total_distance / 1000, 2),
        'ascent_m': round(total_ascent, 0),
        'descent_m': round(total_descent, 0),
        'max_altitude_m': round(max(elevations), 0) if elevations else None,
        'min_altitude_m': round(min(elevations), 0) if elevations else None,
        'point_count': len(points),
        'elevation_curve': elevation_curve[:100],
        'source': 'kml',
    }


def parse_kml(filepath):
    """解析 KML 文件，返回统计 JSON"""
    if not os.path.exists(filepath):
        return {'error': f'文件不存在: {filepath}'}

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        return {'error': f'KML XML 格式错误: {e}'}
    except Exception as e:
        return {'error': f'文件读取失败: {e}'}

    points = _find_longest_linestring(root)

    if not points:
        return {'error': 'KML 文件中未找到有效轨迹坐标（需要 LineString 或 gx:Track）'}

    return _analyze_points(points)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        help_text = (
            "用法: python3 kml-parser.py <kml_file> [--json]\n"
            "\n"
            "解析 KML 轨迹文件，输出 JSON 格式统计信息。\n"
            "\n"
            "参数:\n"
            "  <kml_file>    KML 文件路径\n"
            "  --json        格式化 JSON 输出（默认也输出 JSON）\n"
            "  -h, --help    显示此帮助信息\n"
            "\n"
            "输出字段:\n"
            "  start / end       起终点经纬度\n"
            "  distance_km       总距离（公里）\n"
            "  ascent_m          累计爬升（米）\n"
            "  descent_m         累计下降（米）\n"
            "  max_altitude_m    最高海拔\n"
            "  min_altitude_m    最低海拔\n"
            "  point_count       轨迹点数量\n"
            "  elevation_curve   海拔曲线采样点\n"
            "  source            数据来源（固定为 'kml'）\n"
        )
        print(help_text)
        sys.exit(0)

    filepath = sys.argv[1]
    result = parse_kml(filepath)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
