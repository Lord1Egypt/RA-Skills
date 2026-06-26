from __future__ import annotations

import gzip
import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from .models import BoundingBox, MultiPolygon, NATIONAL_SCOPE_BOXES, SamplePoint

BoundaryGeometry = Union[MultiPolygon, Tuple[float, float, float, float]]

MAJOR_CITIES = [
    ("乌鲁木齐", 43.83, 87.62),
    ("拉萨", 29.65, 91.12),
    ("西宁", 36.62, 101.78),
    ("兰州", 36.06, 103.83),
    ("银川", 38.48, 106.23),
    ("呼和浩特", 40.84, 111.75),
    ("西安", 34.27, 108.95),
    ("成都", 30.67, 104.07),
    ("重庆", 29.56, 106.55),
    ("昆明", 25.04, 102.71),
    ("贵阳", 26.65, 106.63),
    ("北京", 40.18, 116.71),
    ("天津", 39.13, 117.20),
    ("太原", 37.87, 112.55),
    ("石家庄", 38.04, 114.48),
    ("郑州", 34.76, 113.65),
    ("武汉", 30.58, 114.29),
    ("长沙", 28.23, 112.94),
    ("南京", 32.06, 118.80),
    ("合肥", 31.86, 117.28),
    ("杭州", 30.25, 120.15),
    ("南昌", 28.68, 115.86),
    ("福州", 26.08, 119.30),
    ("济南", 36.65, 117.12),
    ("广州", 23.13, 113.26),
    ("南宁", 22.82, 108.32),
    ("哈尔滨", 45.80, 126.53),
    ("长春", 43.88, 125.32),
    ("沈阳", 41.80, 123.43),
]

def _light_pollution_estimate(lat: float, lng: float):
    min_dist = None
    for _, clat, clng in MAJOR_CITIES:
        d = haversine_km(lat, lng, clat, clng)
        if min_dist is None or d < min_dist:
            min_dist = d
    if min_dist is None:
        return None, None
    if min_dist >= 120:
        return "1-2级（极暗）", "距最近大城市较远，光污染极低"
    if min_dist >= 70:
        return "3-4级（暗）", "距最近大城市约70km以上，光污染较轻"
    if min_dist >= 35:
        return "5-6级（中）", "距最近大城市约35-70km，光污染中等"
    if min_dist >= 15:
        return "7-8级（亮）", "距最近大城市约15-35km，光污染较重"
    return "9级（极亮）", "距最近大城市不足15km，光污染较重，不适合拍星"

def _boundary_contains(lng: float, lat: float, geom: BoundaryGeometry) -> bool:
    if isinstance(geom, tuple) and len(geom) == 4:
        min_lng, min_lat, max_lng, max_lat = geom
        return min_lng <= lng <= max_lng and min_lat <= lat <= max_lat
    return point_in_multipolygon(lng, lat, geom)

DEFAULT_PROVINCE_BOUNDARIES = Path(__file__).resolve().parent.parent.parent / "data" / "polygon-text" / "provinces"

DEFAULT_PREFECTURE_BOUNDARIES = Path(__file__).resolve().parent.parent.parent / "data" / "polygon-text" / "prefectures"

def normalize_region_name(name: str) -> str:
    text = str(name).strip()
    for suffix in ["特别行政区", "壮族自治区", "回族自治区", "维吾尔自治区", "自治州", "地区", "盟", "自治区", "省", "市"]:
        if text.endswith(suffix):
            text = text[: -len(suffix)]
            break
    return text.strip()



def feature_name(feature: dict) -> Optional[str]:
    props = feature.get("properties", {}) or {}
    for key in ["name", "NAME", "province", "admin", "region"]:
        if props.get(key):
            return str(props[key])
    return None



def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))



def parse_boxes(payload: str) -> List[BoundingBox]:
    data = json.loads(payload)
    return [BoundingBox(name=row.get("name") or row["province"], province=row["province"], min_lat=float(row["min_lat"]), max_lat=float(row["max_lat"]), min_lng=float(row["min_lng"]), max_lng=float(row["max_lng"])) for row in data]



def load_scope_preset(name: str) -> List[BoundingBox]:
    if name == "national":
        return [
            BoundingBox(name=row.get("name") or row["province"], province=row["province"], min_lat=float(row["min_lat"]), max_lat=float(row["max_lat"]), min_lng=float(row["min_lng"]), max_lng=float(row["max_lng"]))
            for row in NATIONAL_SCOPE_BOXES
        ]
    raise ValueError(f"Unknown scope preset: {name}")



def point_in_ring(lng: float, lat: float, ring: PolygonRing) -> bool:
    inside = False
    n = len(ring)
    if n < 3:
        return False
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        intersects = ((yi > lat) != (yj > lat)) and (lng < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi)
        if intersects:
            inside = not inside
        j = i
    return inside



def point_in_polygon(lng: float, lat: float, polygon: List[PolygonRing]) -> bool:
    if not polygon:
        return False
    if not point_in_ring(lng, lat, polygon[0]):
        return False
    for hole in polygon[1:]:
        if point_in_ring(lng, lat, hole):
            return False
    return True



def point_in_multipolygon(lng: float, lat: float, mp: MultiPolygon) -> bool:
    return any(point_in_polygon(lng, lat, poly) for poly in mp)



def normalize_geometry(geometry: dict) -> Optional[MultiPolygon]:
    gtype = geometry.get("type")
    coords = geometry.get("coordinates")
    if gtype == "Polygon":
        return [coords]
    if gtype == "MultiPolygon":
        return coords
    return None  # skip unsupported geometry types



def load_polygons(polygons_json: Optional[str], polygons_file: Optional[str]) -> Tuple[Dict[str, BoundaryGeometry], Dict[str, BoundaryGeometry]]:
    """Load two-level boundaries: (province_polygons, prefecture_polygons).
    Auto-loads bundled defaults if no explicit path given.
    """
    province_polygons: Dict[str, BoundaryGeometry] = {}
    prefecture_polygons: Dict[str, BoundaryGeometry] = {}

    def _merge_named_geometry(polygons_dict: Dict[str, BoundaryGeometry], name: str, geom) -> None:
        if not name or geom is None:
            return
        polygons_dict[name] = geom
        polygons_dict[normalize_region_name(name)] = geom

    def _merge_data(data, polygons_dict: Dict[str, BoundaryGeometry]) -> None:
        if isinstance(data, dict) and data and all(isinstance(v, list) and len(v) == 4 and all(isinstance(x, (int, float)) for x in v) for v in data.values()):
            for key, bbox in data.items():
                _merge_named_geometry(polygons_dict, key, tuple(float(x) for x in bbox))
            return
        if isinstance(data, dict) and data.get("type") == "FeatureCollection":
            for feat in data.get("features", []):
                name = feature_name(feat)
                geom = normalize_geometry(feat.get("geometry", {}))
                _merge_named_geometry(polygons_dict, name, geom)
            return
        if isinstance(data, dict) and data.get("type") == "Feature":
            name = feature_name(data) or data.get("name") or "default"
            geom = normalize_geometry(data.get("geometry", {}))
            _merge_named_geometry(polygons_dict, name, geom)
            return
        if isinstance(data, dict) and data.get("geometry"):
            name = data.get("name") or feature_name(data)
            geom = normalize_geometry(data.get("geometry", {}))
            _merge_named_geometry(polygons_dict, name, geom)
            return
        if isinstance(data, dict) and "geometry" not in data:
            for key, geom in data.items():
                if isinstance(geom, dict) and geom.get("type") in {"Polygon", "MultiPolygon"}:
                    mg = normalize_geometry(geom)
                    _merge_named_geometry(polygons_dict, key, mg)

    def _load_single(path: str, polygons_dict: Dict[str, BoundaryGeometry]) -> None:
        try:
            p = Path(path)
            if p.is_dir():
                for child in sorted(p.glob("*.json")):
                    if child.name == "index.json":
                        continue
                    try:
                        _merge_data(json.loads(child.read_text(encoding="utf-8")), polygons_dict)
                    except Exception:
                        continue
                return
            if p.suffix == '.gz':
                with gzip.open(p, 'rt', encoding='utf-8') as fh:
                    raw = fh.read()
            else:
                raw = p.read_text(encoding='utf-8')
        except Exception:
            return
        _merge_data(json.loads(raw), polygons_dict)

    # Province level: explicit file > explicit json > bundled default
    if polygons_file:
        _load_single(polygons_file, province_polygons)
    elif polygons_json:
        try:
            data = json.loads(polygons_json)
            tmp: Dict[str, MultiPolygon] = {}
            # inline load into tmp then merge
            def _inline_load(jdata, tgt):
                if isinstance(jdata, dict) and jdata.get("type") == "FeatureCollection":
                    for feat in jdata.get("features", []):
                        name = feature_name(feat)
                        if not name:
                            continue
                        geom = normalize_geometry(feat.get("geometry", {}))
                        if geom is None:
                            continue
                        tgt[name] = geom
                        tgt[normalize_region_name(name)] = geom
            _inline_load(data, province_polygons)
        except Exception:
            pass
    elif DEFAULT_PROVINCE_BOUNDARIES.exists():
        _load_single(str(DEFAULT_PROVINCE_BOUNDARIES), province_polygons)

    # Prefecture level: bundled default (no external file / json support yet)
    if DEFAULT_PREFECTURE_BOUNDARIES.exists():
        _load_single(str(DEFAULT_PREFECTURE_BOUNDARIES), prefecture_polygons)

    return province_polygons, prefecture_polygons



def load_county_polygons(province_adcodes: List[str]) -> Dict[str, MultiPolygon]:
    """County/banner polygons are intentionally disabled in the bundled skill.

    Rationale:
    - avoid runtime downloading of extra GeoJSON resources
    - keep install behavior aligned with the packaged data files only
    - reduce security scan noise from optional external-boundary fetch paths
    """
    return {}



def filter_points_by_polygon(
    points: List[SamplePoint],
    province_polygons: Dict[str, BoundaryGeometry],
    prefecture_polygons: Dict[str, BoundaryGeometry],
) -> List[SamplePoint]:
    if not province_polygons and not prefecture_polygons:
        return points
    kept: List[SamplePoint] = []
    for p in points:
        geom = None
        # 1. Try prefecture-level first (more specific)
        if prefecture_polygons:
            geom = (
                prefecture_polygons.get(p.scope_name)
                or prefecture_polygons.get(normalize_region_name(p.scope_name))
            )
        # 2. Fall back to province-level
        if geom is None and province_polygons:
            geom = (
                province_polygons.get(p.province)
                or province_polygons.get(normalize_region_name(p.province))
                or province_polygons.get(p.scope_name)
                or province_polygons.get(normalize_region_name(p.scope_name))
                or province_polygons.get("default")
            )
        if geom is None:
            # No polygon matched this point; keep it instead of over-filtering.
            kept.append(p)
            continue
        if _boundary_contains(p.lng, p.lat, geom):
            kept.append(p)
    return kept



def generate_grid_points(box: BoundingBox, target_count: int) -> List[SamplePoint]:
    if target_count <= 0:
        return []
    lat_span = max(box.max_lat - box.min_lat, 0.1)
    lng_span = max(box.max_lng - box.min_lng, 0.1)
    ratio = max(0.2, min(5.0, lng_span / lat_span))
    rows = max(1, round(math.sqrt(target_count / ratio)))
    cols = max(1, math.ceil(target_count / rows))
    lat_step = lat_span / rows
    lng_step = lng_span / cols

    points: List[SamplePoint] = []
    idx = 1
    for r in range(rows):
        for c in range(cols):
            if len(points) >= target_count:
                break
            lat = box.min_lat + (r + 0.5) * lat_step
            lng = box.min_lng + (c + 0.5) * lng_step
            points.append(SamplePoint(id=f"{box.province}-{idx}", province=box.province, scope_name=box.name, lat=round(lat, 5), lng=round(lng, 5)))
            idx += 1
    return points



def dedupe_cross_province(points: List[SamplePoint], distance_km: float = 60.0, score_gap: float = 8.0) -> List[SamplePoint]:
    kept: List[SamplePoint] = []
    for point in sorted(points, key=lambda p: (p.cloud_cover if p.cloud_cover is not None else 999.0, p.id)):
        duplicate_of: Optional[SamplePoint] = None
        for existing in kept:
            if existing.province == point.province:
                continue
            if haversine_km(point.lat, point.lng, existing.lat, existing.lng) > distance_km:
                continue
            c1 = point.cloud_cover if point.cloud_cover is not None else 100.0
            c2 = existing.cloud_cover if existing.cloud_cover is not None else 100.0
            f1 = point.final_score if point.final_score is not None else 0.0
            f2 = existing.final_score if existing.final_score is not None else 0.0
            if abs(c1 - c2) <= score_gap and abs(f1 - f2) <= 12.0:
                duplicate_of = existing
                break
        if duplicate_of is not None:
            point.merged_into = duplicate_of.id
            continue
        kept.append(point)
    return kept



def region_direction(box: BoundingBox, lat: float, lng: float) -> str:
    lat_mid = (box.min_lat + box.max_lat) / 2
    lng_mid = (box.min_lng + box.max_lng) / 2
    vertical = "北部" if lat >= lat_mid else "南部"
    horizontal = "东部" if lng >= lng_mid else "西部"
    lat_bias = abs(lat - lat_mid) / max((box.max_lat - box.min_lat) / 2, 0.1)
    lng_bias = abs(lng - lng_mid) / max((box.max_lng - box.min_lng) / 2, 0.1)
    if lat_bias > 0.25 and lng_bias > 0.25:
        mapping = {("北部", "西部"): "西北部", ("北部", "东部"): "东北部", ("南部", "西部"): "西南部", ("南部", "东部"): "东南部"}
        return mapping[(vertical, horizontal)]
    return horizontal if lng_bias >= lat_bias else vertical



HUMAN_REGION_ALIASES = {
    "海西蒙古族藏族": "海西",
    "伊犁哈萨克": "伊犁",
    "阿坝藏族羌族": "阿坝",
    "甘孜藏族": "甘孜",
    "凉山彝族": "凉山",
    "博尔塔拉蒙古": "博州",
    "克孜勒苏柯尔克孜": "克州",
}


FORCE_PREFECTURE_CONTEXT_PROVINCES = {"新疆", "西藏", "青海", "内蒙古"}



def add_province_context(label: str, provinces: List[str]) -> str:
    """Make labels immediately readable by always prefixing province-level context
    for single-province regions, unless already present. Also shorten a few overly long
    autonomous-prefecture names into more natural user-facing forms.
    """
    if not label:
        return label
    for src, dst in HUMAN_REGION_ALIASES.items():
        label = label.replace(src, dst)
    if len(provinces) != 1:
        return label
    prov = provinces[0]
    if label.startswith(prov):
        return label
    return f"{prov}{label}"



def cluster_points(points: List[SamplePoint], cluster_km: float) -> List[List[SamplePoint]]:
    clusters: List[List[SamplePoint]] = []
    for p in sorted(points, key=lambda x: (-(x.final_score or -1), x.id)):
        placed = False
        for cluster in clusters:
            if any(haversine_km(p.lat, p.lng, q.lat, q.lng) <= cluster_km for q in cluster):
                cluster.append(p)
                placed = True
                break
        if not placed:
            clusters.append([p])
    return clusters



def dominant_province(cluster: List[SamplePoint]) -> str:
    counts: Dict[str, int] = {}
    scores: Dict[str, float] = {}
    for p in cluster:
        counts[p.province] = counts.get(p.province, 0) + 1
        scores[p.province] = scores.get(p.province, 0.0) + (p.final_score or 0.0)
    return sorted(counts.keys(), key=lambda k: (counts[k], scores[k]), reverse=True)[0]



def cluster_centroid(cluster: List[SamplePoint]) -> Tuple[float, float]:
    lat = sum(p.lat for p in cluster) / len(cluster)
    lng = sum(p.lng for p in cluster) / len(cluster)
    return lat, lng


# ---------------------------------------------------------------------------
# Geographic reference table: (name, lat, lng, radius_deg, terrain_tag)
# radius_deg ≈ ~50km natural threshold for "nearby" check
# terrain_tag drives the label suffix
# ---------------------------------------------------------------------------

GEOGRAPHIC_FEATURES = [
    # (name, lat, lng, radius_deg, terrain_tag)
    # ---- 甘肃 / 青海 交界北部 ----
    ("阿尔金山", 39.2, 94.0, 1.2, "阿尔金山区域"),
    ("祁连山", 38.5, 99.5, 1.5, "祁连山区"),
    ("河西走廊", 40.5, 95.5, 1.8, "河西走廊"),
    ("敦煌", 40.1, 94.7, 0.8, "敦煌周边"),
    ("马鬃山", 41.5, 96.5, 1.0, "马鬃山区域"),
    ("安西", 40.5, 95.8, 0.8, "安西盆地"),
    # ---- 青海 ----
    ("柴达木盆地", 37.2, 95.5, 2.0, "柴达木盆地"),
    ("可可西里", 35.3, 93.0, 1.5, "可可西里边缘"),
    ("昆仑山", 35.8, 94.5, 1.5, "昆仑山区域"),
    ("巴颜喀拉山", 33.5, 97.0, 1.5, "巴颜喀拉山区域"),
    ("阿尼玛卿山", 34.5, 99.5, 1.2, "阿尼玛卿山区"),
    ("青海湖", 36.9, 100.4, 0.8, "青海湖周边"),
    ("茶卡盐湖", 36.7, 99.1, 0.5, "茶卡盐湖周边"),
    ("德令哈", 37.4, 97.4, 0.6, "德令哈周边"),
    ("格尔木", 36.4, 94.9, 0.6, "格尔木周边"),
    ("西宁", 36.6, 101.8, 0.6, "西宁周边"),
    ("玉树", 33.0, 97.0, 0.8, "玉树周边"),
    # ---- 甘肃 ----
    ("张掖", 38.9, 100.5, 0.6, "张掖周边"),
    ("酒泉", 39.7, 98.5, 0.6, "酒泉周边"),
    ("武威", 37.9, 102.6, 0.6, "武威周边"),
    ("白银", 36.5, 104.2, 0.6, "白银周边"),
    ("定西", 35.6, 104.6, 0.6, "定西周边"),
    # ---- 西藏 ----
    ("纳木错", 30.7, 88.6, 0.8, "纳木错周边"),
    ("羊卓雍错", 29.2, 90.6, 0.6, "羊卓雍错周边"),
    ("珠峰", 28.0, 86.9, 1.0, "珠峰区域"),
    ("阿里地区", 32.5, 80.0, 2.5, "阿里高原"),
    ("那曲", 31.5, 92.0, 0.8, "那曲周边"),
    # ---- 四川 ----
    ("康定", 30.0, 101.9, 0.6, "康定周边"),
    ("稻城亚丁", 28.9, 100.3, 0.6, "稻城亚丁周边"),
    ("若尔盖", 33.6, 102.9, 0.8, "若尔盖周边"),
    # ---- 新疆 ----
    ("喀纳斯", 49.0, 87.0, 0.6, "喀纳斯周边"),
    ("赛里木湖", 44.5, 81.0, 0.6, "赛里木湖周边"),
    ("巴音布鲁克", 43.0, 84.2, 0.8, "巴音布鲁克周边"),
    ("天山", 42.0, 86.0, 2.0, "天山区域"),
    ("塔克拉玛干", 38.5, 82.5, 2.5, "塔克拉玛干沙漠边缘"),
    ("库尔勒", 41.7, 86.1, 0.6, "库尔勒周边"),
    # ---- 内蒙古 ----
    ("额济纳旗", 41.9, 101.1, 0.8, "额济纳旗周边"),
    ("巴丹吉林沙漠", 39.5, 105.0, 1.5, "巴丹吉林沙漠边缘"),
    ("乌兰察布", 41.0, 113.0, 0.8, "乌兰察布周边"),
    ("阿尔山", 47.2, 119.9, 0.6, "阿尔山周边"),
]



def find_nearby_feature(lat: float, lng: float) -> Optional[Tuple[str, str, float]]:
    """Return (feature_name, terrain_tag, distance_km) for the nearest geographic feature within range."""
    best_dist = float("inf")
    best = None
    for name, feat_lat, feat_lng, radius, tag in GEOGRAPHIC_FEATURES:
        d = haversine_km(lat, lng, feat_lat, feat_lng)
        if d < best_dist:
            best_dist = d
            best = (name, tag, d)
    if best_dist > 130.0:  # > ~130km → too far for useful human naming hint
        return None
    return best



def terrain_altitude_tag(cluster: List[SamplePoint]) -> str:
    """Derive terrain/altitude tag from cluster point elevations."""
    elevs = [p.elevation_m for p in cluster if p.elevation_m is not None]
    if not elevs:
        return ""
    avg = sum(elevs) / len(elevs)
    if avg >= 4000:
        return "超高海拔地带"
    if avg >= 3500:
        return "高海拔地带"
    if avg >= 3000:
        return "中高海拔地带"
    if avg >= 2500:
        return "山地区域"
    if avg >= 1500:
        return "低山丘陵地带"
    return ""



def is_admin_like_name(name: str) -> bool:
    return any(name.endswith(s) for s in ["市", "盟", "地区", "自治州", "旗", "县", "区"])



def find_containing_admin_name(
    lat: float,
    lng: float,
    prefecture_polygons: Dict[str, BoundaryGeometry],
    county_polygons: Optional[Dict[str, BoundaryGeometry]] = None,
) -> Optional[str]:
    """Lightweight reverse naming layer.
    Checks county/banner polygons first (most specific), then prefecture-level.
    For equal administrative level, prefer shorter (less redundant) names.
    """
    ADMIN_LEVEL_PRIORITY = {"县": 0, "旗": 0, "区": 0, "市": 1, "盟": 2, "地区": 2, "自治州": 2}

    def name_key(n: str) -> tuple:
        """Sort key: county-level first, then by string length."""
        suffix = next((s for s in ADMIN_LEVEL_PRIORITY if n.endswith(s)), "")
        level = ADMIN_LEVEL_PRIORITY.get(suffix, 3)
        return (level, len(n), n)

    # County/banner level first: most specific administrative naming.
    if county_polygons:
        seen = set()
        candidates = []
        for name, geom in county_polygons.items():
            if name in seen or not is_admin_like_name(name):
                continue
            seen.add(name)
            try:
                if _boundary_contains(lng, lat, geom):
                    candidates.append(name)
            except Exception:
                continue
        if candidates:
            candidates.sort(key=name_key)
            return candidates[0]

    # Prefecture/league-level fallback when county/banner match is unavailable.
    seen = set()
    candidates = []
    for name, geom in prefecture_polygons.items():
        if name in seen:
            continue
        seen.add(name)
        if not is_admin_like_name(name):
            continue
        try:
            if _boundary_contains(lng, lat, geom):
                candidates.append(name)
        except Exception:
            continue
    if not candidates:
        return None
    candidates.sort(key=name_key)
    return candidates[0]



def humanize_prefecture_name(name: str) -> str:
    raw = str(name or "").strip()
    if not raw:
        return raw
    if raw.endswith("自治州"):
        base = raw[:-3]
        for src, dst in HUMAN_REGION_ALIASES.items():
            base = base.replace(src, dst)
        return f"{base}州"
    if raw.endswith("地区") or raw.endswith("盟") or raw.endswith("市"):
        return raw
    return raw



def build_admin_context_label(province: str, county_or_city: str, direction: str, prefecture_polygons: Optional[Dict[str, BoundaryGeometry]], lat: float, lng: float) -> str:
    county_or_city = normalize_region_name(county_or_city)
    if province in FORCE_PREFECTURE_CONTEXT_PROVINCES and prefecture_polygons:
        prefecture = find_containing_admin_name(lat, lng, prefecture_polygons, county_polygons=None)
        if prefecture:
            prefecture_human = humanize_prefecture_name(prefecture)
            pref_norm = normalize_region_name(prefecture_human)
            # Avoid awkward repeats like "青海海西州海西..."
            if pref_norm and (county_or_city == pref_norm or county_or_city.startswith(pref_norm)):
                return f"{province}{prefecture_human}{direction}"
            if prefecture_human and pref_norm not in county_or_city:
                return f"{province}{prefecture_human}{county_or_city}{direction}"
    return f"{province}{county_or_city}{direction}"



def cluster_label(cluster: List[SamplePoint], boxes: List[BoundingBox], prefecture_polygons: Optional[Dict[str, BoundaryGeometry]] = None, county_polygons: Optional[Dict[str, BoundaryGeometry]] = None) -> str:
    provinces = sorted({p.province for p in cluster})
    box_map = {b.province: b for b in boxes}
    lat, lng = cluster_centroid(cluster)
    feature = find_nearby_feature(lat, lng)
    altitude_tag = terrain_altitude_tag(cluster)

    # Prefer county/banner-level naming; add nearby geographic hint when useful.
    if len(provinces) == 1 and prefecture_polygons:
        prov = provinces[0]
        admin_name = find_containing_admin_name(lat, lng, prefecture_polygons, county_polygons=county_polygons)
        if admin_name:
            direction = region_direction(box_map[prov], lat, lng)
            base = build_admin_context_label(prov, admin_name, direction, prefecture_polygons, lat, lng)
            if feature:
                feat_name, terrain_tag, feature_distance = feature
                norm_admin = normalize_region_name(admin_name)
                norm_feat = normalize_region_name(feat_name)
                if norm_feat and norm_feat not in norm_admin and feature_distance <= 130:
                    return f"{base}，靠{feat_name}方向"
            return base

    # Try geographic feature name second
    if feature:
        feat_name, terrain_tag, feature_distance = feature
        if len(provinces) == 1:
            prov = provinces[0]
            parts = [prov, terrain_tag]
            if altitude_tag and altitude_tag not in terrain_tag:
                parts.append(altitude_tag)
            return "".join(parts)
        else:
            parts = [terrain_tag]
            if altitude_tag and altitude_tag not in terrain_tag:
                parts.append(altitude_tag)
            return "".join(parts)

    # Fallback to province + direction
    if len(provinces) == 1:
        prov = provinces[0]
        direction = region_direction(box_map[prov], lat, lng)
        suffix = f"{altitude_tag}·{direction}" if altitude_tag else direction
        return f"{prov}{suffix}"
    main_prov = dominant_province(cluster)
    top_two = provinces[:2]
    direction = region_direction(box_map[main_prov], lat, lng)
    suffix = f"{altitude_tag}·{direction}" if altitude_tag else direction
    return f"{'-'.join(top_two)}交界{suffix}"


