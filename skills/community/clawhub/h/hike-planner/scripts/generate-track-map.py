#!/usr/bin/env python3
"""
generate-track-map.py — GPX/KML 轨迹地图 HTML 生成器

解析 GPX/KML 文件，生成独立的交互式 Leaflet 轨迹地图 HTML。
支持高德卫星图 + 路网标注（默认）或 OpenStreetMap 瓦片。

用法:
  python3 scripts/generate-track-map.py <gpx_or_kml_file> [--output output.html] [--tile amap|osm]

依赖: 仅 Python 标准库（无需 pip install）
  - 通过 subprocess 调用 assets/gpx-parser.py 或 assets/kml-parser.py 获取统计数据
  - 直接解析 GPX/KML XML 提取所有轨迹点坐标

高德瓦片:
  - 卫星图: webst0{s}.is.autonavi.com/appmaptile?style=6 (s=1-4)
  - 路网标注: webst0{s}.is.autonavi.com/appmaptile?style=8 (s=1-4，透明叠加层)
  - 来源: 高德地图 JS API 免费瓦片服务
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

# ── 常量 ────────────────────────────────────────────

HAVERSINE_R = 6371000  # 地球半径（米）
MAX_INLINE_POINTS = 5000  # 内联坐标最大点数，超出则均匀采样
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'assets')

GPX_PARSER = os.path.join(os.path.dirname(SCRIPT_DIR), 'assets', 'gpx-parser.py')
KML_PARSER = os.path.join(os.path.dirname(SCRIPT_DIR), 'assets', 'kml-parser.py')


# ── Haversine ───────────────────────────────────────

def haversine(lat1, lng1, lat2, lng2):
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    return HAVERSINE_R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── 文件类型检测 ────────────────────────────────────

def detect_file_type(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.gpx':
        return 'gpx'
    elif ext == '.kml':
        return 'kml'
    # Fallback: try reading first bytes
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            head = f.read(2048).strip()
            if '<kml' in head.lower() or 'xmlns:kml' in head.lower():
                return 'kml'
            if '<gpx' in head.lower():
                return 'gpx'
    except Exception:
        pass
    return None


# ── 点提取（直接从文件解析，不依赖外部库） ──────────

def extract_points_gpx(filepath):
    """直接从 GPX XML 提取所有轨迹点 (lat, lng, ele)"""
    NS = {
        'gpx': 'http://www.topografix.com/GPX/1/1',
        'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1',
    }
    tree = ET.parse(filepath)
    root = tree.getroot()

    points = []

    # 尝试命名空间
    for trkpt in root.findall('.//gpx:trkpt', NS):
        lat = float(trkpt.get('lat'))
        lng = float(trkpt.get('lon'))
        ele_el = trkpt.find('gpx:ele', NS)
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0
        points.append((lat, lng, ele))

    if not points:
        # 回退无命名空间
        for trkpt in root.findall('.//trkpt'):
            lat = float(trkpt.get('lat'))
            lng = float(trkpt.get('lon'))
            ele_el = trkpt.find('ele')
            ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0
            points.append((lat, lng, ele))

    return points


def extract_points_kml(filepath):
    """直接从 KML XML 提取所有轨迹点 (注意 KML 是 lng,lat,ele 顺序)"""
    KML_NS = 'http://www.opengis.net/kml/2.2'
    GX_NS = 'http://www.google.com/kml/ext/2.2'

    tree = ET.parse(filepath)
    root = tree.getroot()

    best_points = []

    def find_all(tag, parent=None):
        if parent is None:
            parent = root
        results = []
        for ns_uri in (KML_NS, GX_NS, ''):
            if ns_uri:
                results.extend(parent.findall(f'.//{{{ns_uri}}}{tag}'))
            else:
                results.extend(parent.findall(f'.//{tag}'))
        return results

    # 尝试 gx:Track
    for track in find_all('Track'):
        coords = track.findall(f'{{{GX_NS}}}coord') or track.findall('coord')
        pts = []
        for c in coords:
            if c.text:
                parts = c.text.strip().split()
                if len(parts) >= 2:
                    try:
                        pts.append((float(parts[1]), float(parts[0]), float(parts[2]) if len(parts) > 2 else 0))
                    except ValueError:
                        continue
        if len(pts) > len(best_points):
            best_points = pts

    # 尝试 LineString
    for ls in find_all('LineString'):
        for coord_el in find_all('coordinates', ls):
            if coord_el.text:
                pts = []
                for t in coord_el.text.strip().split():
                    parts = t.split(',')
                    if len(parts) >= 2:
                        try:
                            pts.append((float(parts[1]), float(parts[0]), float(parts[2]) if len(parts) > 2 else 0))
                        except ValueError:
                            continue
                if len(pts) > len(best_points):
                    best_points = pts

    return best_points


def extract_all_points(filepath):
    """根据文件类型提取所有轨迹点"""
    ftype = detect_file_type(filepath)
    if ftype == 'gpx':
        return extract_points_gpx(filepath)
    elif ftype == 'kml':
        return extract_points_kml(filepath)
    return []


# ── 统计计算 ────────────────────────────────────────

def compute_stats(points):
    """从点列表计算统计数据"""
    if not points or len(points) < 2:
        return None

    dists = []
    total_dist = 0
    total_ascent = 0
    total_descent = 0
    max_ele = points[0][2]
    min_ele = points[0][2]

    for i in range(1, len(points)):
        d = haversine(points[i-1][0], points[i-1][1], points[i][0], points[i][1])
        total_dist += d
        ele_diff = points[i][2] - points[i-1][2]
        # Garmin 每秒记录一次，相邻点海拔变化平均仅 0.08m
        # 3m 阈值会把所有真实爬升过滤成 0。0.5m 可滤 GPS 噪声但保留真实数据
        if abs(ele_diff) >= 0.5:
            if ele_diff > 0:
                total_ascent += ele_diff
            else:
                total_descent += abs(ele_diff)
        max_ele = max(max_ele, points[i][2])
        min_ele = min(min_ele, points[i][2])
        dists.append(d)

    return {
        'distance_km': round(total_dist / 1000, 2),
        'ascent_m': round(total_ascent),
        'descent_m': round(total_descent),
        'max_altitude_m': round(max_ele),
        'min_altitude_m': round(min_ele),
        'point_count': len(points),
    }


def find_max_point(points):
    """找出最高海拔点的索引"""
    if not points:
        return 0
    max_idx = 0
    for i, p in enumerate(points):
        if p[2] > points[max_idx][2]:
            max_idx = i
    return max_idx


# ── 调用外部解析器获取标注名称 ─────────────────────

def get_track_name(filepath):
    """尝试从文件名提取轨迹名称"""
    basename = os.path.splitext(os.path.basename(filepath))[0]
    # 替换下划线和连字符为空格
    name = basename.replace('_', ' ').replace('-', ' ').strip()
    if name:
        return name
    return '轨迹'


# ── HTML 生成 ───────────────────────────────────────

def generate_html(points, stats, title, tile_provider):
    """生成完整的轨迹地图 HTML"""

    # 坐标 JSON（包含海拔）
    coords_json = json.dumps([[round(p[0], 6), round(p[1], 6)] for p in points], ensure_ascii=False)
    elevations_json = json.dumps([round(p[2], 1) for p in points], ensure_ascii=False)

    start = points[0]
    end = points[-1]
    max_idx = find_max_point(points)
    max_pt = points[max_idx]

    # 中心点（轨迹几何中心）
    lats = [p[0] for p in points]
    lngs = [p[1] for p in points]
    center_lat = (min(lats) + max(lats)) / 2
    center_lng = (min(lngs) + max(lngs)) / 2

    stats_json = json.dumps(stats, ensure_ascii=False)

    # 高德地图的 CSS 和 JS 配置
    if tile_provider == 'amap':
        tile_layers = r'''
    // 高德卫星图
    var amapSat = L.tileLayer('https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', {
        subdomains: ['1', '2', '3', '4'],
        maxZoom: 18,
        attribution: '卫星图 © 高德地图 | 路网 © 高德地图 | 轨迹 © OpenStreetMap contributors'
    }).addTo(map);

    // 高德路网标注（透明叠加）
    var amapRoad = L.tileLayer('https://webst0{s}.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}', {
        subdomains: ['1', '2', '3', '4'],
        maxZoom: 18,
        attribution: ''
    }).addTo(map);

    // OSM fallback（备选）
    var osmFallback = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    });

    var baseMaps = {
        "高德卫星": amapSat,
        "OpenStreetMap": osmFallback
    };
    var overlayMaps = {
        "高德路网": amapRoad
    };
    L.control.layers(baseMaps, overlayMaps, {position: 'topright'}).addTo(map);'''
    else:
        tile_layers = r'''
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title} 轨迹地图</title>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ height: 100%; margin: 0; padding: 0; }}
body {{ display: flex; flex-direction: column; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f5f5; }}
.header {{ padding: 16px 20px; background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%); color: #fff; flex-shrink: 0; }}
.header h1 {{ font-size: 20px; font-weight: 600; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
.header h1 .icon {{ font-size: 24px; }}
.stats {{ display: flex; gap: 12px; flex-wrap: wrap; }}
.stat {{ background: rgba(255,255,255,0.18); padding: 8px 14px; border-radius: 20px; font-size: 13px; backdrop-filter: blur(4px); display: flex; align-items: center; gap: 4px; }}
.stat b {{ font-weight: 700; }}
#map {{ flex: 1; min-height: 300px; width: 100%; }}
.legend {{ padding: 12px 20px; background: #fff; border-bottom: 1px solid #e0e0e0; font-size: 13px; color: #555; display: flex; flex-wrap: wrap; gap: 12px; }}
.legend-item {{ display: flex; align-items: center; gap: 6px; }}
.legend-dot {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; border: 2px solid; }}
.legend-line {{ display: inline-block; width: 24px; height: 3px; border-radius: 2px; }}
.footer {{ padding: 14px 20px; text-align: center; font-size: 12px; color: #999; background: #fafafa; border-top: 1px solid #eee; }}
.footer a {{ color: #1a73e8; text-decoration: none; }}
.footer a:hover {{ text-decoration: underline; }}

/* Leaflet popup 优化 */
.leaflet-popup-content {{ font-size: 14px; line-height: 1.6; }}
.leaflet-popup-content b {{ color: #1a73e8; }}

/* 移动端适配 */
@media (max-width: 600px) {{
    .header h1 {{ font-size: 17px; }}
    .stats {{ gap: 8px; }}
    .stat {{ padding: 6px 10px; font-size: 12px; }}
    #map {{ min-height: 250px; }}
    .legend {{ font-size: 12px; gap: 8px; }}
}}

/* 轨迹悬停提示 */
.trail-hover-tooltip {{
    background: rgba(0,0,0,0.75);
    border: none;
    border-radius: 6px;
    color: #fff;
    font-size: 12px;
    padding: 4px 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}
.trail-hover-tooltip::before {{ border-top-color: rgba(0,0,0,0.75) !important; }}
</style>
</head>
<body>

<div class="header">
<h1><span class="icon">🗺️</span>{title} 轨迹地图</h1>
<div class="stats" id="statsPanel">
<span class="stat">📏 <b id="statDist">--</b> km</span>
<span class="stat">⤴️ <b id="statAscent">--</b> m</span>
<span class="stat">🏔️ <b id="statMax">--</b> m</span>
<span class="stat">📍 <b id="statPts">--</b> 点</span>
</div>
</div>

<div id="map"></div>

<div class="legend">
<div class="legend-item"><span class="legend-dot" style="background:#e74c3c;border-color:#c0392b"></span> 起点</div>
<div class="legend-item"><span class="legend-dot" style="background:#f39c12;border-color:#d68910"></span> 最高点</div>
<div class="legend-item"><span class="legend-dot" style="background:#27ae60;border-color:#1e8449"></span> 终点</div>
<div class="legend-item"><span class="legend-line" style="background:#3498db"></span> 轨迹线</div>
</div>

<div class="footer">
由 <a href="https://github.com" target="_blank">Hike Planner</a> 生成 ·
数据来源：GPX/KML 轨迹文件 ·
地图：高德卫星图 + OpenStreetMap
</div>

<script>
// ── 轨迹数据 ──────────────────────────────────────
var stats = {stats_json};
var trailCoords = {coords_json};
var trailElevations = {elevations_json};

// ── 初始化地图 ────────────────────────────────────
var map = L.map('map', {{
    center: [{center_lat}, {center_lng}],
    zoom: 13,
    zoomControl: true
}});

// ── 瓦片图层 ──────────────────────────────────────
{tile_layers}

// ── 轨迹线 ────────────────────────────────────────
var trail = L.polyline(trailCoords, {{
    color: '#3498db',
    weight: 4,
    opacity: 0.85,
    dashArray: '8, 6',
    smoothFactor: 1
}}).addTo(map);

// ── 适配视野 ──────────────────────────────────────
map.fitBounds(trail.getBounds(), {{ padding: [30, 30] }});

// ── 起点标记 ──────────────────────────────────────
var startMarker = L.circleMarker([{start[0]}, {start[1]}], {{
    color: '#e74c3c',
    fillColor: '#e74c3c',
    fillOpacity: 1,
    radius: 7,
    weight: 2
}}).addTo(map);
startMarker.bindPopup(
    '<b>🚩 起点</b><br>' +
    '坐标: {start[0]:.6f}, {start[1]:.6f}<br>' +
    '海拔: {start[2]:.0f} m'
);

// ── 最高点标记 ────────────────────────────────────
var summitMarker = L.circleMarker([{max_pt[0]}, {max_pt[1]}], {{
    color: '#f39c12',
    fillColor: '#f39c12',
    fillOpacity: 1,
    radius: 8,
    weight: 2
}}).addTo(map);
summitMarker.bindPopup(
    '<b>⛰️ 最高点</b><br>' +
    '坐标: {max_pt[0]:.6f}, {max_pt[1]:.6f}<br>' +
    '海拔: {max_pt[2]:.0f} m'
);

// ── 终点标记 ──────────────────────────────────────
var endMarker = L.circleMarker([{end[0]}, {end[1]}], {{
    color: '#27ae60',
    fillColor: '#27ae60',
    fillOpacity: 1,
    radius: 7,
    weight: 2
}}).addTo(map);
endMarker.bindPopup(
    '<b>🏁 终点</b><br>' +
    '坐标: {end[0]:.6f}, {end[1]:.6f}<br>' +
    '海拔: {end[2]:.0f} m'
);

// ── 轨迹悬停显示信息 ──────────────────────────────
var hoverTooltip = null;
trail.on('mousemove', function(e) {{
    if (hoverTooltip) {{
        map.removeLayer(hoverTooltip);
    }}
    var dist = 0;
    var idx = 0;
    var minD = Infinity;
    for (var i = 0; i < trailCoords.length; i++) {{
        var d = Math.abs(e.latlng.lat - trailCoords[i][0]) + Math.abs(e.latlng.lng - trailCoords[i][1]);
        if (d < minD) {{ minD = d; idx = i; }}
    }}
    hoverTooltip = L.tooltip({{
        className: 'trail-hover-tooltip',
        direction: 'top',
        offset: [0, -10]
    }})
    .setLatLng(trailCoords[idx])
    .setContent((idx > 0 ? '📏 ~' + (stats.distance_km * idx / trailCoords.length).toFixed(2) + ' km · ' : '') + '🏔 ' + (trailElevations[idx] || 0).toFixed(0) + ' m')
    .addTo(map);
}});
trail.on('mouseout', function() {{
    if (hoverTooltip) {{
        map.removeLayer(hoverTooltip);
        hoverTooltip = null;
    }}
}});

// ── 填充统计面板 ──────────────────────────────────
document.getElementById('statDist').textContent = stats.distance_km;
document.getElementById('statAscent').textContent = stats.ascent_m;
document.getElementById('statMax').textContent = stats.max_altitude_m;
document.getElementById('statPts').textContent = stats.point_count;
</script>
</body>
</html>'''
    return html


# ── 多轨迹对比 HTML 生成 ─────────────────────────

COMPARE_COLORS = [
    ('#3498db', '#2980b9'),  # 蓝
    ('#e74c3c', '#c0392b'),  # 红
    ('#27ae60', '#1e8449'),  # 绿
    ('#f39c12', '#d68910'),  # 橙
]


def generate_compare_html(all_data, stats_list, title, tile_provider):
    """生成多轨迹对比 HTML"""

    # 收集所有坐标用于 fitBounds
    all_lats = []
    all_lngs = []
    for data in all_data:
        for p in data['points']:
            all_lats.append(p[0])
            all_lngs.append(p[1])

    center_lat = (min(all_lats) + max(all_lats)) / 2
    center_lng = (min(all_lngs) + max(all_lngs)) / 2

    # 高德瓦片配置
    if tile_provider == 'amap':
        tile_layers = '''
    // 高德卫星图
    var amapSat = L.tileLayer('https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', {
        subdomains: ['1', '2', '3', '4'],
        maxZoom: 18,
        attribution: '卫星图 © 高德地图 | 路网 © 高德地图'
    }).addTo(map);

    // 高德路网标注（透明叠加）
    var amapRoad = L.tileLayer('https://webst0{s}.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}', {
        subdomains: ['1', '2', '3', '4'],
        maxZoom: 18,
        attribution: ''
    }).addTo(map);

    var osmFallback = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    });

    var baseMaps = {"高德卫星": amapSat, "OpenStreetMap": osmFallback};
    var overlayMaps = {"高德路网": amapRoad};
    L.control.layers(baseMaps, overlayMaps, {position: 'topright'}).addTo(map);'''
    else:
        tile_layers = '''
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);'''

    # 构建轨迹 JSON 数据
    tracks_json = []
    for i, data in enumerate(all_data):
        color = COMPARE_COLORS[i % len(COMPARE_COLORS)]
        tracks_json.append({
            'label': data['label'],
            'file': data['file'],
            'coords': [[round(p[0], 6), round(p[1], 6)] for p in data['points']],
            'color': color[0],
            'borderColor': color[1],
        })

    # 构建对比表
    compare_rows = []
    for i, (data, stats) in enumerate(zip(all_data, stats_list)):
        color = COMPARE_COLORS[i % len(COMPARE_COLORS)]
        label = data['label']
        dist = stats['distance_km'] if stats else '--'
        ascent = stats['ascent_m'] if stats else '--'
        max_alt = stats['max_altitude_m'] if stats else '--'
        pts = stats['point_count'] if stats else '--'
        compare_rows.append(
            f'<tr style="border-left: 4px solid {color[0]}">'
            f'<td><span style="color:{color[0]};font-weight:600">{label}</span></td>'
            f'<td>{dist} km</td>'
            f'<td>⤴{ascent} / ⤵{stats["descent_m"] if stats else "--"} m</td>'
            f'<td>{max_alt} m</td>'
            f'<td>{pts}</td>'
            f'</tr>'
        )

    tracks_json_str = json.dumps(tracks_json, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title} 多轨迹对比地图</title>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ height: 100%; margin: 0; padding: 0; }}
body {{ display: flex; flex-direction: column; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f5f5; }}
.header {{ padding: 16px 20px; background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%); color: #fff; flex-shrink: 0; }}
.header h1 {{ font-size: 20px; font-weight: 600; margin-bottom: 12px; }}
.stats-panel {{ background: rgba(255,255,255,0.12); border-radius: 10px; padding: 12px 16px; backdrop-filter: blur(4px); }}
.stats-panel table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.stats-panel th {{ text-align: left; padding: 4px 8px; border-bottom: 1px solid rgba(255,255,255,0.3); font-weight: 600; }}
.stats-panel td {{ padding: 3px 8px; }}
#map {{ flex: 1; min-height: 300px; width: 100%; }}
.legend {{ padding: 12px 20px; background: #fff; border-bottom: 1px solid #e0e0e0; font-size: 13px; color: #555; display: flex; flex-wrap: wrap; gap: 16px; }}
.legend-item {{ display: flex; align-items: center; gap: 6px; }}
.legend-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; }}
.legend-line {{ display: inline-block; width: 28px; height: 3px; border-radius: 2px; }}
.footer {{ padding: 14px 20px; text-align: center; font-size: 12px; color: #999; background: #fafafa; border-top: 1px solid #eee; }}
@media (max-width: 600px) {{
    .header h1 {{ font-size: 17px; }}
    .stats-panel {{ font-size: 12px; }}
    #map {{ min-height: 250px; }}
}}
</style>
</head>
<body>

<div class="header">
<h1>🗺️ {title} — 多轨迹对比</h1>
<div class="stats-panel">
<table>
<tr><th>轨迹名称</th><th>距离</th><th>爬升/下降</th><th>最高海拔</th><th>点数</th></tr>
{''.join(compare_rows)}
</table>
</div>
</div>

<div id="map"></div>

<div class="legend" id="legendDynamic">
</div>

<div class="footer">
由 <a href="https://github.com" target="_blank">Hike Planner</a> 生成 · 多轨迹对比模式 ·
地图：高德卫星图 + OpenStreetMap
</div>

<script>
var tracks = {tracks_json_str};

var map = L.map('map', {{
    center: [{center_lat}, {center_lng}],
    zoom: 13,
    zoomControl: true
}});

{tile_layers}

// 渲染所有轨迹
var allBounds = [];
tracks.forEach(function(trk) {{
    var polyline = L.polyline(trk.coords, {{
        color: trk.color,
        weight: 4,
        opacity: 0.8,
        dashArray: '8, 6',
        smoothFactor: 1
    }}).addTo(map);
    allBounds.push(polyline.getBounds());

    var startIdx = 0;
    var endIdx = trk.coords.length - 1;

    // 起点标记
    L.circleMarker(trk.coords[startIdx], {{
        color: trk.color,
        fillColor: trk.color,
        fillOpacity: 1,
        radius: 5,
        weight: 2
    }}).addTo(map).bindPopup('<b>🟢 起点:</b> ' + trk.label);

    // 终点标记
    L.circleMarker(trk.coords[endIdx], {{
        color: trk.borderColor,
        fillColor: trk.borderColor,
        fillOpacity: 1,
        radius: 5,
        weight: 2
    }}).addTo(map).bindPopup('<b>🔴 终点:</b> ' + trk.label);
}});

// 适配到所有轨迹范围
if (allBounds.length > 0) {{
    var combined = allBounds[0];
    for (var i = 1; i < allBounds.length; i++) {{
        combined.extend(allBounds[i]);
    }}
    map.fitBounds(combined, {{ padding: [30, 30] }});
}}

// 动态图例
var legendHtml = '';
tracks.forEach(function(trk) {{
    legendHtml += '<div class="legend-item"><span class="legend-line" style="background:' + trk.color + '"></span> ' + trk.label + ' <span style="font-size:11px;color:#999">(' + trk.file + ')</span></div>';
}});
document.getElementById('legendDynamic').innerHTML = legendHtml;
</script>
</body>
</html>'''
    return html


# ── 主流程 ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='GPX/KML 轨迹地图 HTML 生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''示例:
  python3 scripts/generate-track-map.py track.gpx
  python3 scripts/generate-track-map.py route.kml --output map.html
  python3 scripts/generate-track-map.py track.gpx --tile osm
  python3 scripts/generate-track-map.py track.gpx --title "海坨山环线"
  python3 scripts/generate-track-map.py track1.gpx track2.kml --compare --output combined.html'''
    )
    parser.add_argument('input', nargs='+', help='GPX 或 KML 文件路径（多文件需配合 --compare 使用）')
    parser.add_argument('--output', '-o', default=None, help='输出 HTML 文件路径（默认: <输入文件名>_轨迹地图.html）')
    parser.add_argument('--tile', '-t', choices=['amap', 'osm'], default='amap',
                        help='瓦片提供商: amap=高德卫星图(默认), osm=OpenStreetMap')
    parser.add_argument('--title', default=None, help='轨迹标题（默认从文件名提取）')
    parser.add_argument('--compare', '-c', action='store_true',
                        help='多文件对比模式：多条轨迹使用不同颜色渲染在同一地图上')
    args = parser.parse_args()

    # ── 多文件对比模式 ──
    if args.compare:
        if len(args.input) < 2:
            print(f'❌ 对比模式至少需要 2 个文件', file=sys.stderr)
            sys.exit(1)

        title = args.title or '多轨迹对比'
        output_path = args.output or os.path.join(
            os.path.dirname(os.path.abspath(args.input[0])) or '.',
            'combined_轨迹地图.html'
        )

        print(f'🗺️  多轨迹对比模式')
        print(f'🎯 标题: {title}')
        print(f'🗺️  瓦片: {"高德卫星图" if args.tile == "amap" else "OpenStreetMap"}')
        print(f'📂 文件数: {len(args.input)}')
        print()

        all_data = []
        all_stats = []

        for idx, input_path in enumerate(args.input):
            if not os.path.exists(input_path):
                print(f'  ❌ 文件不存在: {input_path}', file=sys.stderr)
                sys.exit(1)

            ftype = detect_file_type(input_path)
            if ftype is None:
                print(f'  ❌ 无法识别文件类型: {input_path}', file=sys.stderr)
                sys.exit(1)

            label = get_track_name(input_path)
            points = extract_all_points(input_path)

            # 大文件采样：限制内联点数避免 HTML 过大
            if len(points) > MAX_INLINE_POINTS:
                step = len(points) // MAX_INLINE_POINTS + 1
                points = points[::step]

            if not points or len(points) < 2:
                print(f'  ❌ 未提取到有效轨迹点: {input_path}', file=sys.stderr)
                sys.exit(1)

            stats = compute_stats(points)
            color = COMPARE_COLORS[idx % len(COMPARE_COLORS)]
            print(f'  [{idx + 1}/{len(args.input)}] 📂 {label} ({os.path.basename(input_path)}) - {ftype.upper()}')
            print(f'       📏 {stats["distance_km"]} km · ⤴ {stats["ascent_m"]} m · 🏔 {stats["max_altitude_m"]} m · 📍 {stats["point_count"]} 点 · 🎨 {color[0]}')

            all_data.append({
                'label': label,
                'file': os.path.basename(input_path),
                'points': points,
            })
            all_stats.append(stats)

        html = generate_compare_html(all_data, all_stats, title, args.tile)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'\n✅ 多轨迹对比地图已生成: {output_path}')
        print(f'   在浏览器中打开即可查看多条轨迹的交互式对比地图。')
        return

    # ── 单文件模式（原逻辑） ──
    input_path = args.input[0]

    if not os.path.exists(input_path):
        print(f'❌ 文件不存在: {input_path}', file=sys.stderr)
        sys.exit(1)

    # 检测文件类型
    ftype = detect_file_type(input_path)
    if ftype is None:
        print(f'❌ 无法识别文件类型（非 GPX/KML）: {input_path}', file=sys.stderr)
        sys.exit(1)

    title = args.title or get_track_name(input_path)
    output_path = args.output or os.path.join(
        os.path.dirname(os.path.abspath(input_path)) or '.',
        f'{os.path.splitext(os.path.basename(input_path))[0]}_轨迹地图.html'
    )

    print(f'📂 文件类型: {ftype.upper()}')
    print(f'📄 输入: {input_path}')
    print(f'🎯 标题: {title}')
    print(f'🗺️  瓦片: {"高德卫星图" if args.tile == "amap" else "OpenStreetMap"}')

    # 提取所有点
    points = extract_all_points(input_path)

    if not points or len(points) < 2:
        print(f'❌ 未提取到有效轨迹点（至少需要 2 个点）', file=sys.stderr)
        sys.exit(1)

    print(f'📍 轨迹点: {len(points)}')

    # 大文件采样：限制内联点数避免 HTML 过大
    if len(points) > MAX_INLINE_POINTS:
        step = len(points) // MAX_INLINE_POINTS + 1
        points = points[::step]
        print(f'📐 采样后: {len(points)} 点 (步长 {step})')

    # 计算统计
    stats = compute_stats(points)
    if stats is None:
        print(f'❌ 统计数据计算失败', file=sys.stderr)
        sys.exit(1)

    print(f'📏 距离: {stats["distance_km"]} km')
    print(f'⤴️  爬升: {stats["ascent_m"]} m')
    print(f'🏔️  最高海拔: {stats["max_altitude_m"]} m')

    # 生成 HTML
    html = generate_html(points, stats, title, args.tile)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'\n✅ 轨迹地图已生成: {output_path}')
    print(f'   在浏览器中打开即可查看交互式轨迹地图。')


if __name__ == '__main__':
    main()
