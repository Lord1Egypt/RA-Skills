#!/usr/bin/env python3
"""
gpx-parser.py — GPX 轨迹解析器

解析 GPX 文件，提取：起终点坐标、总距离、累计爬升/下降、海拔曲线。
输出 JSON 格式，供 hike-planner.js 使用。

用法:
  python3 assets/gpx-parser.py <gpx_file> [--json]

依赖:
  pip3 install gpxpy  (可选，没有则用纯 Python 回退解析)

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
  "source": "gpxpy" | "fallback"
}
"""

import json
import sys
import os
import math
import xml.etree.ElementTree as ET

HAVERSINE_R = 6371000  # 地球半径（米）

def haversine(lat1, lng1, lat2, lng2):
    """计算两点间距离（米）"""
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    return HAVERSINE_R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def parse_with_gpxpy(filepath):
    """使用 gpxpy 库解析（精确）"""
    try:
        import gpxpy
    except ImportError:
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        gpx = gpxpy.parse(f)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for pt in segment.points:
                points.append({
                    'lat': pt.latitude,
                    'lng': pt.longitude,
                    'elevation': pt.elevation if pt.elevation else 0,
                    'time': pt.time.isoformat() if pt.time else None,
                })

    return _analyze_points(points, 'gpxpy')


def parse_fallback(filepath):
    """纯 Python XML 回退解析（无 gpxpy 依赖）"""
    NS = {'gpx': 'http://www.topografix.com/GPX/1/1'}

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except Exception as e:
        return {'error': f'解析失败: {e}'}

    points = []
    # 尝试命名空间
    for trkpt in root.findall('.//gpx:trkpt', NS) or root.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
        lat = float(trkpt.get('lat'))
        lng = float(trkpt.get('lon'))
        ele_el = trkpt.find('gpx:ele', NS) or trkpt.find('{http://www.topografix.com/GPX/1/1}ele')
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0
        time_el = trkpt.find('gpx:time', NS) or trkpt.find('{http://www.topografix.com/GPX/1/1}time')
        t = time_el.text if time_el is not None else None
        points.append({'lat': lat, 'lng': lng, 'elevation': ele, 'time': t})

    # 如果命名空间不匹配，回退到无命名空间
    if not points:
        for trkpt in root.findall('.//trkpt'):
            lat = float(trkpt.get('lat'))
            lng = float(trkpt.get('lon'))
            ele_el = trkpt.find('ele')
            ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0
            time_el = trkpt.find('time')
            t = time_el.text if time_el is not None else None
            points.append({'lat': lat, 'lng': lng, 'elevation': ele, 'time': t})

    if not points:
        return {'error': 'GPX 文件中未找到轨迹点'}

    return _analyze_points(points, 'fallback')


def _analyze_points(points, source):
    """分析轨迹点列表，计算统计数据"""
    if not points or len(points) < 2:
        return {'error': '轨迹点不足（至少需要 2 个点）'}

    total_distance = 0
    total_ascent = 0
    total_descent = 0
    elevations = []
    elevation_curve = []

    prev = points[0]
    for i, pt in enumerate(points):
        if i > 0:
            dist = haversine(prev['lat'], prev['lng'], pt['lat'], pt['lng'])
            total_distance += dist
            ele_diff = pt['elevation'] - prev['elevation']
            # 0.5m 阈值滤 GPS 噪声，保留 Garmin 1s 级真实爬升数据
            if abs(ele_diff) >= 0.5:
                if ele_diff > 0:
                    total_ascent += ele_diff
                else:
                    total_descent += abs(ele_diff)

        elevations.append(pt['elevation'])

        # 海拔曲线采样（每 200 米采一个点）
        if i == 0 or total_distance > len(elevation_curve) * 200:
            elevation_curve.append({
                'dist_km': round(total_distance / 1000, 2),
                'elevation_m': pt['elevation'],
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
        'elevation_curve': elevation_curve[:100],  # 最多 100 个采样点
        'source': source,
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '用法: python3 gpx-parser.py <gpx_file> [--json]'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(json.dumps({'error': f'文件不存在: {filepath}'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 优先使用 gpxpy
    result = parse_with_gpxpy(filepath)
    if result is None:
        result = parse_fallback(filepath)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
