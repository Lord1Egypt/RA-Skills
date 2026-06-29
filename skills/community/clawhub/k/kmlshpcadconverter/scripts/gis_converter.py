#!/usr/bin/env python3
"""
KML/SHP/CAD 格式转换 V1.0 — 坤图_GIS
========================================
零配置 GIS 格式互转引擎。DWG/SHP/DXF/KML/KMZ/GeoJSON/OVKML/OVJSN/
DJI-WPMZ/GeoPackage/GeoParquet/Huace-KML 任意双向转换。

architecture:
  Layer 0   - CoordinateEngine:  GCJ-02 <-> WGS84, CRS management
  Layer 0.5 - AutoCRS:          Coordinate system auto-detection
  Layer 0.6 - DWG Engine:       Auto ODA File Converter install + DWG->DXF
  Layer 1   - FormatReaders:    Any format -> GeoDataFrame(WGS84)
  Layer 2   - FormatWriters:    GeoDataFrame(WGS84) -> Any format
  Layer 3   - Converter:        Smart orchestrator with auto-detection

requirements: geopandas>=0.14 pyproj>=3.6 ezdxf>=1.3 shapely>=2.0 pyarrow
"""

import os
import sys
import json
import math
import logging
import zipfile
import tempfile
import traceback
import subprocess
import shutil
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple, Callable

# ──────────────────────────────────────────────
#  KERNEL PARAMETERS (locked — do not modify)
# ──────────────────────────────────────────────
WGS84_EPSG = "EPSG:4326"
CGCS2000_EPSG = "EPSG:4490"
WEB_MERCATOR = "EPSG:3857"
GCJ_A = 6378245.0
GCJ_EE = 0.00669342162296594
PI = math.pi
RAD = PI / 180.0

# CRS auto-detection confidence thresholds
_CONFIDENCE_HIGH = 0.5     # Below this residual: silent auto-accept
_CONFIDENCE_MEDIUM = 2.0   # Below this: auto-accept with warning
# Above _CONFIDENCE_MEDIUM: will ask user confirmation (in interactive mode)

LOG_FILE: Optional[str] = None

def _setup_logging(output_dir: Optional[str] = None):
    global LOG_FILE
    log_dir = Path(output_dir) if output_dir else (Path(__file__).parent.parent / "logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE = str(log_dir / f"gis_convert_{datetime.now():%Y%m%d_%H%M%S}.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stderr)
        ]
    )

LOG = logging.getLogger("gis_converter")

# ──────────────────────────────────────────────
#  DJI WPML Enum Mapping Tables
# ──────────────────────────────────────────────
DJI_DRONE_ENUM = {
    "M350 RTK": ("67", "89"), "M350": ("67", "89"),
    "M300 RTK": ("60", "70"), "M300": ("60", "70"),
    "Matrice 3D": ("77", ""), "Matrice 3E": ("77", ""),
    "Mavic 3E": ("78", ""), "Mavic 3T": ("78", ""),
    "Mavic 3M": ("78", ""), "Mini 4 Pro": ("80", ""),
    "DJI M350 RTK": ("67", "89"), "DJI M300 RTK": ("60", "70"),
}

DJI_PAYLOAD_ENUM = {
    "Zenmuse H20": "42", "H20": "42",
    "Zenmuse H20T": "43", "H20T": "43",
    "Zenmuse H20N": "47", "H20N": "47",
    "Zenmuse P1": "65534", "P1": "65534",
    "Zenmuse L1": "52", "L1": "52",
    "Zenmuse L2": "61", "L2": "61",
    "M3D Camera": "38", "M3D": "38",
    "M3E Camera": "51", "M3E": "51",
    "M3E-T Camera": "53", "M3E-T": "53",
    "M3M Camera": "71", "M3M": "71",
}

DJI_ACTION_MAP = {
    "takePhoto": "18", "startRecord": "19", "stopRecord": "20",
    "hover": "21", "gimbalRotate": "5",
}

# ──────────────────────────────────────────────
#  Legacy CRS Diagnostic Table (BJ54/XA80)
# ──────────────────────────────────────────────
LEGACY_CRS_DIAGNOSTIC = {
    "EPSG:4214": {"name": "Beijing 1954", "status": "deprecated(2008)", "offset": "100-200m"},
    "EPSG:4610": {"name": "Xian 1980", "status": "deprecated(2018)", "offset": "100-200m"},
}


# ═══════════════════════════════════════════════════════════════
#  LAYER 0: Coordinate Engine (GCJ-02 <-> WGS84)
# ═══════════════════════════════════════════════════════════════

class CoordinateEngine:
    """GCJ-02 <-> WGS84 bidirectional correction (8-iteration, <1e-6 deg)."""

    @staticmethod
    def _out_of_china(lon, lat):
        return not (72.004 <= lon <= 137.8347 and 0.8293 <= lat <= 55.8271)

    @staticmethod
    def _d_lat(lon_diff, lat_diff):
        r = -100.0 + 2.0*lon_diff + 3.0*lat_diff + 0.2*lat_diff*lat_diff
        r += 0.1*lon_diff*lat_diff + 0.2*abs(lon_diff)
        r += (20.0*math.sin(6.0*lon_diff*PI) + 20.0*math.sin(2.0*lon_diff*PI)) * 2.0/3.0
        r += (20.0*math.sin(lat_diff*PI) + 40.0*math.sin(lat_diff/3.0*PI)) * 2.0/3.0
        r += (160.0*math.sin(lat_diff/12.0*PI) + 320.*math.sin(lat_diff*PI/30.0)) * 2.0/3.0
        return r

    @staticmethod
    def _d_lon(lon_diff, lat_diff):
        r = 300.0 + lon_diff + 2.0*lat_diff + 0.1*lon_diff*lon_diff
        r += 0.1*lon_diff*lat_diff + 0.1*abs(lon_diff)
        r += (20.0*math.sin(6.0*lon_diff*PI) + 20.0*math.sin(2.0*lon_diff*PI)) * 2.0/3.0
        r += (20.0*math.sin(lon_diff*PI) + 40.0*math.sin(lon_diff/3.0*PI)) * 2.0/3.0
        r += (150.0*math.sin(lon_diff/12.0*PI) + 300.*math.sin(lon_diff/30.0*PI)) * 2.0/3.0
        return r

    @staticmethod
    def wgs84_to_gcj02(lon, lat):
        if CoordinateEngine._out_of_china(lon, lat):
            return lon, lat
        d_lat = CoordinateEngine._d_lat(lon - 105.0, lat - 35.0)
        d_lon = CoordinateEngine._d_lon(lon - 105.0, lat - 35.0)
        rad_lat = lat * RAD
        magic = 1 - GCJ_EE * math.sin(rad_lat) ** 2
        sqrt_magic = math.sqrt(magic)
        d_lat_m = (d_lat * 180.0) / ((GCJ_A * (1 - GCJ_EE)) / (magic * sqrt_magic) * PI)
        d_lon_m = (d_lon * 180.0) / (GCJ_A / sqrt_magic * math.cos(rad_lat) * PI)
        return lon + d_lon_m, lat + d_lat_m

    @staticmethod
    def gcj02_to_wgs84(lon, lat, max_iter=8):
        if CoordinateEngine._out_of_china(lon, lat):
            return lon, lat
        w_lon, w_lat = lon, lat
        for _ in range(max_iter):
            c_lon, c_lat = CoordinateEngine.wgs84_to_gcj02(w_lon, w_lat)
            d_lon, d_lat = c_lon - lon, c_lat - lat
            if abs(d_lon) < 1e-7 and abs(d_lat) < 1e-7:
                break
            w_lon -= d_lon
            w_lat -= d_lat
        return round(w_lon, 7), round(w_lat, 7)


def _apply_gcj02_to_wgs84(geom):
    if geom is None or geom.is_empty:
        return geom
    from shapely.ops import transform as shapely_transform
    def _correct(x, y, z=None):
        nx, ny = CoordinateEngine.gcj02_to_wgs84(x, y)
        return (nx, ny, z) if z is not None else (nx, ny)
    return shapely_transform(_correct, geom)


def _apply_wgs84_to_gcj02(geom):
    if geom is None or geom.is_empty:
        return geom
    from shapely.ops import transform as shapely_transform
    def _offset(x, y, z=None):
        nx, ny = CoordinateEngine.wgs84_to_gcj02(x, y)
        return (nx, ny, z) if z is not None else (nx, ny)
    return shapely_transform(_offset, geom)


# ═══════════════════════════════════════════════════════════════
#  LAYER 0.5: Auto CRS Detection
# ═══════════════════════════════════════════════════════════════

# CGCS2000 3-degree GK zone: CM -> EPSG
_CGCS2000_3DEG = {cm: 4534 + (cm - 75) // 3 for cm in range(75, 136, 3)}

# CGCS2000 6-degree GK zone (non-sequential)
_CGCS2000_6DEG = {
    75: 4550, 81: 4551, 87: 4552, 93: 4553, 99: 4554,
    105: 4555, 111: 4558, 117: 4559, 123: 4560, 129: 4561, 135: 4562,
}


def auto_detect_crs(gdf):
    """Auto-detect CRS from GeoDataFrame coordinates.

    Returns: (epsg_str|None, description_str, confidence_float)
      confidence: residuals in degrees. lower = better.
    """
    if len(gdf) == 0:
        return None, "empty data", 999

    bounds = gdf.total_bounds
    x_center = (bounds[0] + bounds[2]) / 2
    y_center = (bounds[1] + bounds[3]) / 2
    x_range = abs(bounds[2] - bounds[0])
    y_range = abs(bounds[3] - bounds[1])

    # Strip GK zone-number prefix from X coordinates
    _ZONE_STRIP = 1_000_000
    if abs(x_center) > _ZONE_STRIP:
        prefix = int(abs(x_center) // _ZONE_STRIP)
        if 10 <= prefix <= 60:
            x_center = x_center % _ZONE_STRIP
            bounds = [bounds[0] % _ZONE_STRIP, bounds[1],
                      bounds[2] % _ZONE_STRIP, bounds[3]]

    # 1. Geographic (WGS84)
    if (abs(bounds[0]) <= 180 and abs(bounds[2]) <= 180 and
            abs(bounds[1]) <= 90 and abs(bounds[3]) <= 90):
        if x_range < 20 and y_range < 20 and any(abs(v) > 1 for v in bounds):
            return "EPSG:4326", "WGS84 (geographic)", 0.0

    # 2. Chinese GK projection
    if 100_000 < y_center < 6_000_000:
        result = _detect_chinese_gk(x_center, y_center)
        if result:
            epsg, desc, confidence = result
            return epsg, desc, confidence

    # 3. Web Mercator
    if all(2e7 >= abs(v) >= 1_000_000 for v in bounds):
        try:
            from pyproj import Transformer
            t = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
            lon, lat = t.transform(x_center, y_center)
            if -180 <= lon <= 180 and -85 <= lat <= 85:
                return "EPSG:3857", "Web Mercator (EPSG:3857)", 0.0
        except Exception:
            pass

    return None, "cannot detect CRS (out of China projection range)", 999


def _detect_chinese_gk(x_center, y_center):
    """Detect Chinese GK zone using geographic heuristic.

    Returns: (epsg, description, confidence_residual) or None
    """
    from pyproj import Transformer

    # Strip GK zone-number prefix from X (e.g. 37524151 -> 524151)
    _ZONE_STRIP = 1_000_000
    if abs(x_center) > _ZONE_STRIP:
        prefix = int(abs(x_center) // _ZONE_STRIP)
        if 10 <= prefix <= 60:
            x_center = x_center % _ZONE_STRIP

    lat_est = y_center / 111000.0
    if not (0 < lat_est < 55):
        return None

    cos_lat = math.cos(lat_est * RAD)
    if cos_lat < 0.01:
        return None

    delta_lon = (x_center - 500000.0) / (111000.0 * cos_lat)

    _BANDS = [
        (0, 22, 110.0), (22, 28, 108.5), (28, 33, 112.0),
        (33, 38, 115.0), (38, 43, 117.0), (43, 48, 123.0),
        (48, 55, 128.0),
    ]
    ref_lon = 112.0
    for lo, hi, ref in _BANDS:
        if lo <= lat_est < hi:
            ref_lon = ref
            break

    lon_est = ref_lon + delta_lon
    candidates = []

    cm_3 = round(lon_est / 3) * 3
    for offset in (-3, 0, 3, 6, -6):
        cm = cm_3 + offset
        if 75 <= cm <= 135:
            epsg = 4534 + (cm - 75) // 3
            residual = abs(lon_est - cm)
            candidates.append((residual, epsg, cm, "CGCS2000", "3deg"))

    for cm, epsg in _CGCS2000_6DEG.items():
        residual = abs(lon_est - cm)
        candidates.append((residual, epsg, cm, "CGCS2000", "6deg"))

    candidates.sort(key=lambda x: x[0])

    for residual, epsg, cm, family, band_label in candidates:
        if residual > 3.0:
            continue
        try:
            t = Transformer.from_crs(epsg, 4326, always_xy=True)
            lon_inv, lat_inv = t.transform(x_center, y_center)
            if 73 <= lon_inv <= 135 and 0 <= lat_inv <= 55:
                zone_num = int((cm + 1.5) // 3)
                return (
                    f"EPSG:{epsg}",
                    f"{family} {band_label} zone{zone_num} (CM {cm}\u00b0E)",
                    residual,
                )
        except Exception:
            pass
    return None


def _extract_dxf_coords(dxf_path):
    """Extract (x,y) pairs from DXF for CRS detection."""
    import ezdxf
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    coords = []
    for ent in msp:
        dt = ent.dxftype()
        try:
            if dt == "LWPOLYLINE":
                for p in ent.get_points():
                    coords.append((p[0], p[1]))
            elif dt == "LINE":
                coords.append((ent.dxf.start.x, ent.dxf.start.y))
                coords.append((ent.dxf.end.x, ent.dxf.end.y))
            elif dt == "POINT":
                coords.append((ent.dxf.location.x, ent.dxf.location.y))
            elif dt in ("CIRCLE", "ARC"):
                coords.append((ent.dxf.center.x, ent.dxf.center.y))
            elif dt == "INSERT":
                coords.append((ent.dxf.insert.x, ent.dxf.insert.y))
        except Exception:
            continue
    return coords


def detect_dxf_crs(dxf_path):
    """Detect CRS of a DXF file from raw coordinates."""
    coords = _extract_dxf_coords(dxf_path)
    if not coords:
        return None, "no extractable coordinates in DXF", 999
    from shapely.geometry import Point
    import geopandas as gpd
    pts = [Point(x, y) for x, y in coords]
    gdf = gpd.GeoDataFrame(geometry=pts)
    return auto_detect_crs(gdf)


def _ask_user_confirm(epsg, description, confidence):
    """Ask user to confirm auto-detected CRS (interactive mode only)."""
    if not sys.stdin.isatty():
        return epsg  # Non-interactive: accept auto-detection
    try:
        answer = input(
            f"\n  Auto-detected CRS: {description}\n"
            f"  Confidence: {'HIGH' if confidence < _CONFIDENCE_HIGH else 'MEDIUM' if confidence < _CONFIDENCE_MEDIUM else 'LOW'}\n"
            f"  Is this correct? [Y/n]: "
        ).strip().lower()
        if answer in ("n", "no"):
            manual = input("  Please enter the correct EPSG code (e.g. EPSG:4546): ").strip()
            return manual if manual else epsg
    except (EOFError, KeyboardInterrupt):
        pass
    return epsg


# ═══════════════════════════════════════════════════════════════
#  LAYER 0.6: DWG Auto-Conversion (ODA File Converter)
# ═══════════════════════════════════════════════════════════════

_ODA_DOWNLOAD_URL = (
    "https://www.opendesign.com/guestfiles/get"
    "?filename=ODAFileConverter_QT6_vc16_amd64dll_27.1.msi"
)
_ODA_SEARCH_PATHS = [
    "C:/Program Files/ODA",
    "C:/Program Files (x86)/ODA",
    "D:/Program Files/ODA",
]


def _find_oda_converter():
    for base in _ODA_SEARCH_PATHS:
        if not os.path.isdir(base):
            continue
        for root, _dirs, files in os.walk(base):
            if "ODAFileConverter.exe" in files:
                return os.path.join(root, "ODAFileConverter.exe")
    return None


def _install_oda_converter():
    msi_path = os.path.join(tempfile.gettempdir(), "ODAFileConverter.msi")
    LOG.info("[DWG] Downloading ODA File Converter (~28MB) ...")
    try:
        urllib.request.urlretrieve(_ODA_DOWNLOAD_URL, msi_path)
        LOG.info(f"[DWG] Downloaded: {os.path.getsize(msi_path)/1024/1024:.1f} MB")
    except Exception as e:
        raise RuntimeError(
            f"Failed to download ODA File Converter. Please check network.\n"
            f"Alternatively, install manually from: https://www.opendesign.com/guestfiles/oda_file_converter\n"
            f"Error: {e}"
        ) from e
    LOG.info("[DWG] Installing silently (may take 30-60s) ...")
    result = subprocess.run(
        ["msiexec", "/i", msi_path, "/qn", "/norestart"],
        capture_output=True, text=True, timeout=180,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ODA File Converter install failed (exit={result.returncode}).\n"
            f"Try running as administrator or install manually."
        )
    oda_exe = _find_oda_converter()
    if not oda_exe:
        raise RuntimeError("ODA installed but executable not found. Please reinstall manually.")
    LOG.info(f"[DWG] ODA installed: {oda_exe}")
    return oda_exe


def auto_convert_dwg(dwg_path):
    """Convert DWG to DXF using ODA File Converter (auto-install)."""
    with open(dwg_path, "rb") as f:
        magic = f.read(6)
    if not magic.startswith(b"AC"):
        raise ValueError(f"Not a valid DWG file (magic={magic!r})")

    oda_exe = _find_oda_converter()
    if not oda_exe:
        LOG.info("[DWG] ODA File Converter not found, auto-installing ...")
        oda_exe = _install_oda_converter()

    tmp_in = tempfile.mkdtemp(prefix="gis_dwg_in_")
    tmp_out = tempfile.mkdtemp(prefix="gis_dwg_out_")
    shutil.copy2(dwg_path, os.path.join(tmp_in, os.path.basename(dwg_path)))

    dwg_name = os.path.basename(dwg_path)
    LOG.info(f"[DWG] Converting DWG->DXF: {dwg_name}")
    try:
        subprocess.run(
            [oda_exe, tmp_in, tmp_out, "ACAD2018", "DXF", "0", "0", dwg_name],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("ODA File Converter timed out (120s). File may be too large or corrupted.")

    dxf_name = dwg_name.rsplit(".", 1)[0] + ".dxf"
    dxf_path = os.path.join(tmp_out, dxf_name)
    if not os.path.exists(dxf_path):
        listing = os.listdir(tmp_out)
        raise RuntimeError(f"DWG conversion produced no DXF. Output dir contains: {listing}")
    LOG.info(f"[DWG] DXF generated successfully")
    return dxf_path


# ═══════════════════════════════════════════════════════════════
#  LAYER 1: Format Readers
# ═══════════════════════════════════════════════════════════════

def _gdf_to_wgs84(gdf):
    import geopandas as gpd
    if gdf.crs is None:
        gdf = gdf.set_crs(WGS84_EPSG)
    return gdf.to_crs(WGS84_EPSG)


def read_shp(path, **kwargs):
    import geopandas as gpd
    encoding = kwargs.get("encoding", "utf-8")
    try:
        gdf = gpd.read_file(path, encoding=encoding)
    except (UnicodeDecodeError, Exception):
        LOG.warning("SHP UTF-8 read failed, retrying with GBK encoding")
        gdf = gpd.read_file(path, encoding="gbk")
    LOG.info(f"[READ] SHP: {len(gdf)} features, CRS={gdf.crs}")
    return _gdf_to_wgs84(gdf)


def read_geojson(path, **kwargs):
    import geopandas as gpd
    gdf = gpd.read_file(path)
    LOG.info(f"[READ] GeoJSON: {len(gdf)} features")
    return _gdf_to_wgs84(gdf)


def read_gpkg(path, **kwargs):
    import geopandas as gpd
    layer = kwargs.get("layer")
    gdf = gpd.read_file(path, layer=layer) if layer else gpd.read_file(path)
    LOG.info(f"[READ] GeoPackage: {len(gdf)} features, CRS={gdf.crs}")
    return _gdf_to_wgs84(gdf)


def read_parquet(path, **kwargs):
    import geopandas as gpd
    gdf = gpd.read_parquet(path)
    LOG.info(f"[READ] GeoParquet: {len(gdf)} features")
    return _gdf_to_wgs84(gdf)


def read_kml(path, **kwargs):
    import geopandas as gpd
    gdf = gpd.read_file(path, driver="KML")
    LOG.info(f"[READ] KML: {len(gdf)} features")
    return _gdf_to_wgs84(gdf)


def read_kmz(path, **kwargs):
    import geopandas as gpd
    with zipfile.ZipFile(path, "r") as z:
        kml_files = [f for f in z.namelist() if f.lower().endswith(".kml")]
        if not kml_files:
            raise ValueError(f"No KML found in KMZ: {path}")
        with tempfile.TemporaryDirectory() as tmpdir:
            z.extract(kml_files[0], tmpdir)
            gdf = gpd.read_file(os.path.join(tmpdir, kml_files[0]), driver="KML")
    LOG.info(f"[READ] KMZ: {len(gdf)} features")
    return _gdf_to_wgs84(gdf)


def read_dxf(path, **kwargs):
    import geopandas as gpd
    import ezdxf
    from shapely.geometry import Point, LineString, Polygon
    from shapely import ops

    source_crs = kwargs.get("source_crs")
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    records = []

    # --- collect raw coords for zone-prefix detection ---
    all_x = []

    for ent in msp:
        geom = None
        attrs = {"layer": ent.dxf.layer, "dxf_type": ent.dxftype()}
        if ent.dxftype() == "POINT":
            x, y = ent.dxf.location.x, ent.dxf.location.y
            all_x.append(x)
            geom = Point(x, y)
        elif ent.dxftype() == "LWPOLYLINE":
            pts = list(ent.get_points())
            coords = [(p[0], p[1]) for p in pts]
            for p in pts:
                all_x.append(p[0])
            if len(coords) < 2:
                continue
            if ent.closed and len(coords) >= 4:
                if coords[0] == coords[-1]:
                    coords.pop()
                geom = Polygon(coords) if len(coords) >= 3 else LineString(coords)
            else:
                geom = LineString(coords)
        elif ent.dxftype() == "CIRCLE":
            c = ent.dxf.center
            all_x.append(c.x)
            geom = Point(c.x, c.y).buffer(ent.dxf.radius, resolution=32)
        elif ent.dxftype() == "LINE":
            all_x.extend([ent.dxf.start.x, ent.dxf.end.x])
            geom = LineString([(ent.dxf.start.x, ent.dxf.start.y),
                              (ent.dxf.end.x, ent.dxf.end.y)])
        elif ent.dxftype() == "ARC":
            c = ent.dxf.center; r = ent.dxf.radius
            all_x.append(c.x)
            sa, ea = math.radians(ent.dxf.start_angle), math.radians(ent.dxf.end_angle)
            n = max(4, int(abs(ea - sa) / (PI / 16)))
            pts = [(c.x + r * math.cos(sa + (ea - sa) * i / n),
                    c.y + r * math.sin(sa + (ea - sa) * i / n)) for i in range(n + 1)]
            geom = LineString(pts) if len(pts) >= 2 else None
        elif ent.dxftype() == "INSERT":
            x, y = ent.dxf.insert.x, ent.dxf.insert.y
            all_x.append(x)
            geom = Point(x, y)
            attrs["block_name"] = ent.dxf.name
        if geom is not None and not geom.is_empty:
            records.append({"geometry": geom, **attrs})

    if not records:
        LOG.warning("[READ] DXF: 0 valid entities found")
        return gpd.GeoDataFrame([], crs=WGS84_EPSG)

    # --- strip GK zone prefix from X coords ---
    _STRIP_ZONE_THRESHOLD = 2_000_000  # X above 2M likely has zone prefix
    if all_x and max(abs(x) for x in all_x) > _STRIP_ZONE_THRESHOLD:
        zone_prefix = int(max(all_x) // 1_000_000)
        if 10 <= zone_prefix <= 60:
            LOG.info(f"[READ] DXF: stripping GK zone prefix '{zone_prefix}' from X coords")
            stripped_records = []
            for rec in records:
                g = rec["geometry"]
                new_g = ops.transform(lambda x, y, z=None: (x % 1_000_000, y), g)
                stripped_records.append({"geometry": new_g, **{k: v for k, v in rec.items() if k != "geometry"}})
            records = stripped_records

    gdf = gpd.GeoDataFrame(records, crs=source_crs or WGS84_EPSG)
    LOG.info(f"[READ] DXF: {len(gdf)} features")
    return _gdf_to_wgs84(gdf)


def read_ovkml(path, **kwargs):
    import geopandas as gpd
    auto_correct = kwargs.get("auto_correct_gcj02", True)
    gdf = gpd.read_file(path, driver="KML")
    if auto_correct:
        gdf["geometry"] = gdf["geometry"].apply(_apply_gcj02_to_wgs84)
        LOG.info(f"[READ] OVKML: {len(gdf)} features (GCJ-02 corrected)")
    else:
        LOG.info(f"[READ] OVKML: {len(gdf)} features (GCJ-02 preserved)")
    return _gdf_to_wgs84(gdf)


def read_ovjsn(path, **kwargs):
    import geopandas as gpd
    from shapely.geometry import Point, LineString, Polygon
    auto_correct = kwargs.get("auto_correct_gcj02", True)
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"Failed to parse OVJSN: {e}")
    objitems = data.get("ObjItems", [])
    records = []

    def _collect(items):
        for item in items:
            obj = item.get("Object", {})
            detail = obj.get("ObjectDetail", {})
            lat = float(detail.get("Lat", detail.get("lat", 0)))
            lng = float(detail.get("Lng", detail.get("lng", 0)))
            gcj_flag = int(detail.get("Gcj02", detail.get("gcj02", 0)))
            name = str(obj.get("Name", ""))
            obj_type = int(obj.get("Type", 0))
            altitude = float(detail.get("Altitude", 0))
            point_list = detail.get("PointList", detail.get("Points", []))
            if auto_correct and gcj_flag:
                lng, lat = CoordinateEngine.gcj02_to_wgs84(lng, lat)
            if point_list and len(point_list) >= 2:
                coords = []
                for p in point_list:
                    px = float(p.get("Lng", p.get("lng", 0)))
                    py = float(p.get("Lat", p.get("lat", 0)))
                    if auto_correct and gcj_flag:
                        px, py = CoordinateEngine.gcj02_to_wgs84(px, py)
                    coords.append((px, py))
                geom = Polygon(coords) if (len(coords) >= 3 and obj_type == 10) else LineString(coords) if len(coords) >= 2 else Point(coords[0])
            else:
                geom = Point(lng, lat)
            records.append({
                "geometry": geom, "name": name, "obj_type": obj_type,
                "altitude": altitude, "ovital_gcj02": gcj_flag,
            })
            children = obj.get("ObjChildren", [])
            if children:
                _collect(children)

    _collect(objitems)
    gdf = gpd.GeoDataFrame(records, crs=WGS84_EPSG) if records else gpd.GeoDataFrame([], crs=WGS84_EPSG)
    LOG.info(f"[READ] OVJSN: {len(gdf)} features")
    return _gdf_to_wgs84(gdf)


# ═══════════════════════════════════════════════════════════════
#  LAYER 2: Format Writers
# ═══════════════════════════════════════════════════════════════

def write_shp(gdf, path, **kwargs):
    wgdf = gdf.copy()
    target_crs = kwargs.get("target_crs")
    if target_crs:
        wgdf = wgdf.to_crs(target_crs)
    rename = {}
    for col in wgdf.columns:
        if col == "geometry":
            continue
        if len(col) > 10:
            new = col[:10]; i = 1
            while new in rename.values() or new in wgdf.columns:
                new = col[:9] + str(i); i += 1
            rename[col] = new
    if rename:
        wgdf = wgdf.rename(columns=rename)
        LOG.info(f"[WRT] SHP fields truncated: {rename}")
    encoding = kwargs.get("encoding", "utf-8")
    wgdf.to_file(path, encoding=encoding)
    LOG.info(f"[WRT] SHP: {len(gdf)} features")


def write_geojson(gdf, path, **kwargs):
    gdf.to_file(path, driver="GeoJSON", encoding="utf-8")
    LOG.info(f"[WRT] GeoJSON: {len(gdf)} features")


def write_kml(gdf, path, **kwargs):
    wgdf = gdf.copy().to_crs(WGS84_EPSG)
    name_field = kwargs.get("name_field", "name")
    desc_field = kwargs.get("description_field")
    if name_field not in wgdf.columns:
        wgdf[name_field] = [f"Feature_{i}" for i in range(len(wgdf))]
    wgdf["Description"] = wgdf[desc_field].astype(str) if (desc_field and desc_field in wgdf.columns) else ""
    wgdf.to_file(path, driver="KML")
    LOG.info(f"[WRT] KML: {len(gdf)} features")


def write_ovkml(gdf, path, **kwargs):
    wgdf = gdf.copy().to_crs(WGS84_EPSG)
    wgdf["geometry"] = wgdf["geometry"].apply(_apply_wgs84_to_gcj02)
    wgdf.to_file(path, driver="KML")
    LOG.info(f"[WRT] OVKML: {len(gdf)} features (GCJ-02 offset applied)")


def write_dxf(gdf, path, **kwargs):
    import ezdxf
    wgdf = gdf.copy()
    source_crs = kwargs.get("target_crs")
    if source_crs:
        wgdf = wgdf.to_crs(source_crs)
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    layer_field = kwargs.get("layer_field")
    processed = 0
    for idx, row in wgdf.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            continue
        lay = str(row[layer_field]) if (layer_field and layer_field in wgdf.columns) else "GIS_EXPORT"
        try:
            doc.layers.add(lay)
        except ezdxf.const.DXFValueError:
            pass
        if geom.geom_type == "Point":
            msp.add_point(geom.coords[0], dxfattribs={"layer": lay})
        elif geom.geom_type == "LineString":
            coords = list(geom.coords)
            if len(coords) >= 2:
                msp.add_lwpolyline(coords, close=False, dxfattribs={"layer": lay})
        elif geom.geom_type in ("Polygon", "MultiPolygon"):
            polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
            for poly in polys:
                if poly.exterior and len(poly.exterior.coords) >= 3:
                    msp.add_lwpolyline(list(poly.exterior.coords), close=True, dxfattribs={"layer": lay})
        elif geom.geom_type == "MultiLineString":
            for line in geom.geoms:
                coords = list(line.coords)
                if len(coords) >= 2:
                    msp.add_lwpolyline(coords, close=False, dxfattribs={"layer": lay})
        else:
            continue
        processed += 1
    doc.saveas(path)
    LOG.info(f"[WRT] DXF: {processed}/{len(gdf)} entities")


def write_dji_wpmz(gdf, path, **kwargs):
    wgdf = gdf.copy().to_crs(WGS84_EPSG)
    drone = kwargs.get("drone_model", "M350 RTK")
    payload = kwargs.get("payload_model", "Zenmuse H20")
    altitude = kwargs.get("altitude", 50.0)
    speed = kwargs.get("speed", 8.0)
    heading = kwargs.get("heading_mode", "followWayline")
    gimbal_pitch = kwargs.get("gimbal_pitch", -90)
    action = kwargs.get("action_type", "takePhoto")
    altitude_mode = kwargs.get("altitude_mode", "relativeToGround")

    waypoints = []
    for geom in wgdf.geometry:
        if geom is None or geom.is_empty:
            continue
        if geom.geom_type == "Point":
            waypoints.append((geom.x, geom.y))
        elif geom.geom_type == "LineString":
            waypoints.extend([(c[0], c[1]) for c in geom.coords])
        elif geom.geom_type == "Polygon":
            waypoints.extend([(c[0], c[1]) for c in geom.exterior.coords])
        elif geom.geom_type == "MultiPoint":
            for pt in geom.geoms:
                waypoints.append((pt.x, pt.y))
        else:
            waypoints.append((geom.centroid.x, geom.centroid.y))
    if not waypoints:
        raise ValueError("No waypoints extracted from input")

    drone_key = drone.replace("DJI ", "").strip()
    drone_enum, drone_sub = DJI_DRONE_ENUM.get(drone_key, DJI_DRONE_ENUM.get(drone, (drone, "")))
    payload_enum = DJI_PAYLOAD_ENUM.get(payload, DJI_PAYLOAD_ENUM.get(payload.replace("Zenmuse ", ""), payload))
    action_enum = DJI_ACTION_MAP.get(action, action)
    now_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    tpl_pms = []
    for i, (lon, lat) in enumerate(waypoints):
        tpl_pms.append(
            f'        <Placemark>\n'
            f'          <name>WP_{i+1}</name>\n'
            f'          <Point><coordinates>{lon},{lat},0</coordinates></Point>\n'
            f'          <wpml:index>{i+1}</wpml:index>\n'
            f'        </Placemark>'
        )
    template_kml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
     xmlns:wpml="http://www.dji.com/wpmz/1.0.3">
  <Document>
    <wpml:author>KML/SHP/CAD Converter - 坤图_GIS</wpml:author>
    <wpml:createTime>{now_ts}</wpml:createTime>
    <wpml:updateTime>{now_ts}</wpml:updateTime>
    <wpml:missionConfig>
      <wpml:flyToWaylineMode>safely</wpml:flyToWaylineMode>
      <wpml:finishAction>goHome</wpml:finishAction>
      <wpml:exitOnRCLost>executeLostAction</wpml:exitOnRCLost>
      <wpml:takeOffSecurityHeight>20</wpml:takeOffSecurityHeight>
      <wpml:globalTransitionalSpeed>{speed}</wpml:globalTransitionalSpeed>
      <wpml:droneInfo>
        <wpml:droneEnumValue>{drone_enum}</wpml:droneEnumValue>
        <wpml:droneSubEnumValue>{drone_sub}</wpml:droneSubEnumValue>
      </wpml:droneInfo>
      <wpml:payloadInfo>
        <wpml:payloadEnumValue>{payload_enum}</wpml:payloadEnumValue>
      </wpml:payloadInfo>
    </wpml:missionConfig>
    <Folder>
      <wpml:templateType>waypoint</wpml:templateType>
      <wpml:templateId>0</wpml:templateId>
      <wpml:waylineCoordinateSysParam>
        <wpml:coordinateMode>WGS84</wpml:coordinateMode>
      </wpml:waylineCoordinateSysParam>
      <wpml:autoFlightSpeed>{speed}</wpml:autoFlightSpeed>
      <wpml:executeHeight>
        <wpml:waylineAltitudeMode>{altitude_mode}</wpml:waylineAltitudeMode>
        <wpml:waylineAltitude>{altitude}</wpml:waylineAltitude>
      </wpml:executeHeight>
      <wpml:gimbalPitchAngle>{gimbal_pitch}</wpml:gimbalPitchAngle>
      <wpml:headingMode>{heading}</wpml:headingMode>
      <wpml:globalWaypointTurnMode>coordinateTurn</wpml:globalWaypointTurnMode>
{chr(10).join(tpl_pms)}
    </Folder>
  </Document>
</kml>'''

    wpml_entries = []
    for i, (lon, lat) in enumerate(waypoints):
        wpml_entries.append(
            f'        <Placemark>\n'
            f'          <Point><coordinates>{lon},{lat}</coordinates></Point>\n'
            f'          <wpml:index>{i+1}</wpml:index>\n'
            f'          <wpml:ellipsoidHeight>{altitude}</wpml:ellipsoidHeight>\n'
            f'          <wpml:height>{altitude}</wpml:height>\n'
            f'          <wpml:waypointSpeed>{speed}</wpml:waypointSpeed>\n'
            f'          <wpml:waypointHeadingParam>\n'
            f'            <wpml:waypointHeadingMode>{heading}</wpml:waypointHeadingMode>\n'
            f'          </wpml:waypointHeadingParam>\n'
            f'          <wpml:actionGroup>\n'
            f'            <wpml:actionGroupId>{i+1}</wpml:actionGroupId>\n'
            f'            <wpml:actionGroupStartIndex>{i+1}</wpml:actionGroupStartIndex>\n'
            f'            <wpml:actionGroupEndIndex>{i+1}</wpml:actionGroupEndIndex>\n'
            f'            <wpml:actionGroupMode>sequence</wpml:actionGroupMode>\n'
            f'            <wpml:actionTrigger>\n'
            f'              <wpml:actionTriggerType>reachPoint</wpml:actionTriggerType>\n'
            f'            </wpml:actionTrigger>\n'
            f'            <wpml:action>\n'
            f'              <wpml:actionId>{i+1}</wpml:actionId>\n'
            f'              <wpml:actionActuatorFunc>\n'
            f'                <wpml:actionActuatorFuncEnum>{action_enum}</wpml:actionActuatorFuncEnum>\n'
            f'              </wpml:actionActuatorFunc>\n'
            f'            </wpml:action>\n'
            f'          </wpml:actionGroup>\n'
            f'        </Placemark>'
        )

    waylines_wpml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
     xmlns:wpml="http://www.dji.com/wpmz/1.0.3">
  <Document>
    <wpml:missionConfig>
      <wpml:flyToWaylineMode>safely</wpml:flyToWaylineMode>
      <wpml:finishAction>goHome</wpml:finishAction>
      <wpml:exitOnRCLost>executeLostAction</wpml:exitOnRCLost>
      <wpml:takeOffSecurityHeight>20</wpml:takeOffSecurityHeight>
      <wpml:globalTransitionalSpeed>{speed}</wpml:globalTransitionalSpeed>
      <wpml:globalRTHHeight>50</wpml:globalRTHHeight>
      <wpml:globalWaypointTurnMode>coordinateTurn</wpml:globalWaypointTurnMode>
    </wpml:missionConfig>
    <Folder>
      <wpml:templateType>waypoint</wpml:templateType>
      <wpml:templateId>0</wpml:templateId>
      <wpml:waylineCoordinateSysParam>
        <wpml:coordinateMode>WGS84</wpml:coordinateMode>
      </wpml:waylineCoordinateSysParam>
      <wpml:autoFlightSpeed>{speed}</wpml:autoFlightSpeed>
      <wpml:executeHeight>
        <wpml:waylineAltitudeMode>{altitude_mode}</wpml:waylineAltitudeMode>
        <wpml:waylineAltitude>{altitude}</wpml:waylineAltitude>
      </wpml:executeHeight>
      <wpml:gimbalPitchAngle>{gimbal_pitch}</wpml:gimbalPitchAngle>
{chr(10).join(wpml_entries)}
    </Folder>
  </Document>
</kml>'''

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("wpmz/template.kml", template_kml)
        zf.writestr("wpmz/waylines.wpml", waylines_wpml)
    LOG.info(f"[WRT] DJI-WPMZ: {len(waypoints)} waypoints")


def write_huace_kml(gdf, path, **kwargs):
    from xml.etree.ElementTree import Element, SubElement, tostring
    wgdf = gdf.copy().to_crs(WGS84_EPSG)
    name_field = kwargs.get("name_field", "name")
    desc_field = kwargs.get("description_field")
    kml_root = Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2"})
    doc_el = SubElement(kml_root, "Document")
    SubElement(doc_el, "name").text = "Huace GNSS Export"
    style = SubElement(doc_el, "Style", {"id": "huace_default"})
    icon_st = SubElement(style, "IconStyle")
    SubElement(icon_st, "scale").text = "1.0"
    SubElement(SubElement(icon_st, "Icon"), "href").text = (
        "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"
    )
    for idx, row in wgdf.iterrows():
        g = row.geometry
        if g is None or g.is_empty:
            continue
        pm = SubElement(doc_el, "Placemark")
        SubElement(pm, "name").text = str(row.get(name_field, f"Pt_{idx}"))
        desc = str(row.get(desc_field, "")) if desc_field else ""
        if desc:
            SubElement(pm, "description").text = desc
        SubElement(pm, "styleUrl").text = "#huace_default"
        if g.geom_type == "Point":
            SubElement(SubElement(pm, "Point"), "coordinates").text = f"{g.x},{g.y}"
        elif g.geom_type == "LineString":
            cs = " ".join(f"{c[0]},{c[1]}" for c in g.coords)
            SubElement(SubElement(pm, "LineString"), "coordinates").text = cs
        elif g.geom_type == "Polygon":
            outer = SubElement(SubElement(pm, "Polygon"), "outerBoundaryIs")
            cs = " ".join(f"{c[0]},{c[1]}" for c in g.exterior.coords)
            SubElement(SubElement(outer, "LinearRing"), "coordinates").text = cs
        else:
            SubElement(SubElement(pm, "Point"), "coordinates").text = f"{g.centroid.x},{g.centroid.y}"
    with open(path, "wb") as f:
        f.write(tostring(kml_root, encoding="utf-8", xml_declaration=True))
    LOG.info(f"[WRT] Huace-KML: {len(gdf)} features")


def write_gpkg(gdf, path, **kwargs):
    wgdf = gdf.copy()
    target_crs = kwargs.get("target_crs")
    if target_crs:
        wgdf = wgdf.to_crs(target_crs)
    wgdf.to_file(path, driver="GPKG", layer=kwargs.get("layer_name", "layer"))
    LOG.info(f"[WRT] GeoPackage: {len(gdf)} features")


def write_parquet(gdf, path, **kwargs):
    gdf.to_parquet(path, index=False)
    LOG.info(f"[WRT] GeoParquet: {len(gdf)} features")


def write_ovjsn(gdf, path, **kwargs):
    wgdf = gdf.copy().to_crs(WGS84_EPSG)
    wgdf["geometry"] = wgdf["geometry"].apply(_apply_wgs84_to_gcj02)
    name_field = kwargs.get("name_field", "name")
    objitems = []
    base_id = int(datetime.now().timestamp() * 1000) % 2147483647
    for idx, row in wgdf.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            continue
        name = str(row.get(name_field, f"Feature_{idx}"))
        detail = {"Gcj02": 1}
        if geom.geom_type == "Point":
            detail["Lat"] = round(geom.y, 7)
            detail["Lng"] = round(geom.x, 7)
            obj_type = 7
        elif geom.geom_type == "LineString":
            detail["PointList"] = [{"Lat": round(c[1], 7), "Lng": round(c[0], 7)} for c in geom.coords]
            obj_type = 9
        elif geom.geom_type in ("Polygon", "MultiPolygon"):
            polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
            all_c = []
            for poly in polys:
                all_c.extend([{"Lat": round(c[1], 7), "Lng": round(c[0], 7)} for c in poly.exterior.coords])
            detail["PointList"] = all_c; obj_type = 10
        else:
            detail["Lat"] = round(geom.centroid.y, 7); detail["Lng"] = round(geom.centroid.x, 7)
            obj_type = 7
        objitems.append({
            "Type": obj_type, "ObjID": base_id + idx,
            "Object": {"Name": name, "Type": obj_type, "ObjectDetail": detail},
        })
    data = {"Version": "V9.7.1", "ObjItems": objitems}
    with open(path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    LOG.info(f"[WRT] OVJSN: {len(objitems)} features (GCJ-02 offset applied)")


# ═══════════════════════════════════════════════════════════════
#  LAYER 3: Smart Converter Engine
# ═══════════════════════════════════════════════════════════════

EXT_READ_MAP = {
    "shp": "shp", "geojson": "geojson", "json": "geojson",
    "kml": "kml", "kmz": "kmz", "dxf": "dxf", "dwg": "dxf",
    "ovkml": "ovkml", "ovjsn": "ovjsn",
    "gpkg": "gpkg", "parquet": "parquet",
}

EXT_WRITE_MAP = {
    "shp": "shp", "geojson": "geojson", "json": "geojson",
    "kml": "kml", "kmz": "kml", "dxf": "dxf",
    "ovkml": "ovkml", "wpmz": "wpmz", "wpml": "wpmz",
    "huacekml": "huacekml",
    "gpkg": "gpkg", "parquet": "parquet",
    "ovjsn": "ovjsn",
}

READERS: Dict[str, Callable] = {
    "shp": read_shp, "geojson": read_geojson,
    "kml": read_kml, "kmz": read_kmz,
    "dxf": read_dxf, "ovkml": read_ovkml, "ovjsn": read_ovjsn,
    "gpkg": read_gpkg, "parquet": read_parquet,
}

WRITERS: Dict[str, Callable] = {
    "shp": write_shp, "geojson": write_geojson,
    "kml": write_kml, "ovkml": write_ovkml,
    "dxf": write_dxf, "wpmz": write_dji_wpmz,
    "huacekml": write_huace_kml,
    "gpkg": write_gpkg, "parquet": write_parquet,
    "ovjsn": write_ovjsn,
}


def convert(input_path, output_path,
            source_crs=None, target_crs=None,
            source_gcj02=False, auto_correct_gcj02=True,
            encoding="utf-8",
            **writer_kwargs):
    """Universal GIS format conversion with smart pre-flight checks.

    Parameters (User-Adjustable):
      source_crs:    Override auto-detected input CRS
      target_crs:    Force output CRS (for SHP/DXF output)
      source_gcj02:  Force GCJ-02 correction on input
      auto_correct_gcj02: Auto-detect and correct GCJ-02 (Ovital formats)
      encoding:      File encoding for SHP

    DJI-WPMZ (via **writer_kwargs):
      drone_model, payload_model, altitude, speed, gimbal_pitch,
      action_type, heading_mode, altitude_mode
    """
    inp_ext = Path(input_path).suffix.lower().lstrip(".")
    out_ext = Path(output_path).suffix.lower().lstrip(".")
    inp_key = EXT_READ_MAP.get(inp_ext, inp_ext)
    out_key = EXT_WRITE_MAP.get(out_ext, out_ext)

    LOG.info(f"=== KML/SHP/CAD Converter === 坤图_GIS ===")
    LOG.info(f"    Input:  {Path(input_path).name} [{inp_key}]")
    LOG.info(f"    Output: {Path(output_path).name} [{out_key}]")

    # ── AUTO STEP 0: DWG -> DXF ──
    if inp_ext == "dwg":
        dxf_temp = auto_convert_dwg(input_path)
        input_path = dxf_temp
        inp_ext = "dxf"
        inp_key = "dxf"

    # ── AUTO STEP 0.5: CRS auto-detection for DXF/DWG ──
    if inp_key == "dxf" and source_crs is None:
        try:
            epsg, desc, confidence = detect_dxf_crs(input_path)
            if epsg and confidence <= _CONFIDENCE_HIGH:
                source_crs = epsg
                LOG.info(f"    CRS auto-detected: {desc} (confidence: HIGH)")
            elif epsg and confidence <= _CONFIDENCE_MEDIUM:
                source_crs = epsg
                LOG.warning(f"    CRS auto-detected: {desc} (confidence: MEDIUM, verify recommended)")
            elif epsg:
                # Low confidence — ask user in interactive mode
                source_crs = _ask_user_confirm(epsg, desc, confidence)
                LOG.info(f"    CRS confirmed: {source_crs}")
            else:
                LOG.warning(f"    CRS could not be auto-detected. Defaulting to WGS84.")
                LOG.warning(f"    Use --source-crs to specify manually.")
        except Exception as e:
            LOG.warning(f"    CRS detection failed: {e}. Defaulting to WGS84.")

    # STEP 1: Read
    reader = READERS.get(inp_key)
    if not reader:
        raise ValueError(f"Unsupported input format: .{inp_ext}. Supported: {list(READERS.keys())}")
    read_kwargs = {"source_crs": source_crs}
    if inp_key in ("ovkml", "ovjsn"):
        read_kwargs["auto_correct_gcj02"] = auto_correct_gcj02
    try:
        gdf = reader(input_path, **read_kwargs)
    except Exception as e:
        LOG.error(f"Read failed [{inp_key}]: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Failed to read {Path(input_path).name}: {e}") from e

    if len(gdf) == 0:
        LOG.warning("Input contains 0 features — output will be empty")

    # CRS diagnostic for legacy systems
    crs_str = str(gdf.crs).upper() if gdf.crs else ""
    for legacy_epsg, info in LEGACY_CRS_DIAGNOSTIC.items():
        if legacy_epsg.upper() in crs_str:
            LOG.warning(
                f"    [CRS WARNING] {info['name']} ({info['status']}) detected.\n"
                f"    Expected WGS84 offset: {info['offset']}.\n"
                f"    pyproj default transform may not use correct datum shift.\n"
                f"    For precise conversion, provide a 7-parameter pipeline or grid shift file."
            )
            break

    # Manual GCJ-02 correction
    if source_gcj02:
        gdf["geometry"] = gdf["geometry"].apply(_apply_gcj02_to_wgs84)
        LOG.info("    Applied manual GCJ-02 correction")

    # Ensure WGS84 intermediate
    gdf = _gdf_to_wgs84(gdf)

    # STEP 2: Summary statistics
    geom_types = gdf.geometry.geom_type.value_counts().to_dict()
    LOG.info(f"    Features: {len(gdf)} | Types: {geom_types}")

    # STEP 3: Write
    writer = WRITERS.get(out_key)
    if not writer:
        raise ValueError(f"Unsupported output format: .{out_ext}. Supported: {list(WRITERS.keys())}")
    write_kwargs = {}
    if out_key == "shp":
        write_kwargs = {"target_crs": target_crs, "encoding": encoding}
    elif out_key == "dxf":
        write_kwargs = {"target_crs": target_crs}
    elif out_key in ("kml", "huacekml"):
        write_kwargs = {"name_field": writer_kwargs.get("name_field", "name"),
                        "description_field": writer_kwargs.get("description_field")}
    elif out_key == "wpmz":
        write_kwargs = writer_kwargs

    try:
        writer(gdf, output_path, **write_kwargs)
    except Exception as e:
        LOG.error(f"Write failed [{out_key}]: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Failed to write {Path(output_path).name}: {e}") from e

    stats = f"  Input  : {Path(input_path).name} ({len(gdf)} features, {len(geom_types)} types)"
    if source_crs:
        stats += f"\n  CRS    : {source_crs}"
    stats += f"\n  Output : {Path(output_path).name}"
    LOG.info(f"=== Conversion complete ===")
    LOG.info(stats)
    return output_path


# ═══════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    ap = argparse.ArgumentParser(
        prog="gis_converter",
        description="KML/SHP/CAD Format Converter V1.0 — 坤图_GIS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s drawing.dwg output.kml               # DWG->KML, auto CRS
  %(prog)s drawing.dwg output.shp               # DWG->SHP, auto CRS
  %(prog)s data.shp output.kml                  # SHP->KML
  %(prog)s boundary.geojson mission.wpmz --drone "M350 RTK"
  %(prog)s drawing.dxf output.shp --source-crs EPSG:3857
""")
    ap.add_argument("input", help="Input file path (.dwg/.dxf/.shp/.kml/.geojson/.gpkg/.parquet/.ovkml/.ovjsn)")
    ap.add_argument("output", help="Output file path")
    ap.add_argument("--source-crs", help="Override auto-detected input CRS (e.g. EPSG:4490)")
    ap.add_argument("--target-crs", help="Force output CRS for SHP/DXF")
    ap.add_argument("--source-gcj02", action="store_true", help="Force GCJ-02 correction on input")
    ap.add_argument("--no-gcj02-correct", action="store_true", help="Disable Ovital auto-correction")
    ap.add_argument("--encoding", default="utf-8", help="SHP encoding (default: utf-8, try gbk if garbled)")
    ap.add_argument("--name-field", default="name", help="KML name field")
    ap.add_argument("--desc-field", default=None, help="KML description field")
    ap.add_argument("--drone", default="M350 RTK", help="DJI drone model")
    ap.add_argument("--payload", default="Zenmuse H20", help="DJI payload model")
    ap.add_argument("--altitude", type=float, default=50.0, help="Flight altitude (m)")
    ap.add_argument("--speed", type=float, default=8.0, help="Flight speed (m/s)")
    ap.add_argument("--gimbal-pitch", type=float, default=-90, help="Gimbal pitch angle (deg)")
    ap.add_argument("--action", default="takePhoto", help="Waypoint action")
    ap.add_argument("--heading-mode", default="followWayline", help="Heading mode")
    ap.add_argument("--altitude-mode", default="relativeToGround", help="Altitude reference mode")
    ap.add_argument("--log-dir", default=None, help="Custom log directory")
    args = ap.parse_args()

    _setup_logging(args.log_dir)
    writer_kwargs = {}
    out_suffix = Path(args.output).suffix.lower()
    if out_suffix in (".wpmz", ".wpml"):
        writer_kwargs = {
            "drone_model": args.drone, "payload_model": args.payload,
            "altitude": args.altitude, "speed": args.speed,
            "gimbal_pitch": args.gimbal_pitch, "action_type": args.action,
            "heading_mode": args.heading_mode, "altitude_mode": args.altitude_mode,
        }
    else:
        writer_kwargs = {"name_field": args.name_field, "description_field": args.desc_field}

    result = convert(
        input_path=args.input, output_path=args.output,
        source_crs=args.source_crs, target_crs=args.target_crs,
        source_gcj02=args.source_gcj02,
        auto_correct_gcj02=not args.no_gcj02_correct,
        encoding=args.encoding,
        **writer_kwargs,
    )
    print(f"\n  Conversion SUCCESS")
    print(f"  Input:  {args.input}")
    print(f"  Output: {result}")
    if LOG_FILE:
        print(f"  Log:    {LOG_FILE}")


if __name__ == "__main__":
    main()
