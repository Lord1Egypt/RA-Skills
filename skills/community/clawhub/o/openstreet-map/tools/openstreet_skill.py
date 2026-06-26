#!/usr/bin/env python3
"""OpenStreetMap geocoding and annotated map renderer.

Capabilities:
1) Query location information for a single place.
2) Render an annotated map image for multiple places.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import sys
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

import requests
from PIL import Image, ImageDraw, ImageFont

DEFAULT_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
DEFAULT_TILE_URL_TEMPLATE = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
USER_AGENT = "openclaw-openstreet-skill/1.0"
DEFAULT_TIMEOUT = 20
DEFAULT_TILE_SIZE = 256
DEFAULT_VIEW_PADDING_RATIO = 0.01
MARKER_RADIUS_PX = 11
MIN_EDGE_PADDING_PX = 10

# ----- Font configuration -----
BUNDLED_FONT_DIR = Path(__file__).parent / "fonts"

_SYSTEM_CJK_FONT_PATHS = [
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode MS.ttf",
    # Linux common
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    # Windows
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]


def _find_cjk_font() -> Path | None:
    """Return path to first usable CJK font: bundled dir first, then system."""
    if BUNDLED_FONT_DIR.is_dir():
        for ext in ("*.otf", "*.ttf", "*.ttc"):
            matches = list(BUNDLED_FONT_DIR.glob(ext))
            if matches:
                return matches[0]
    for path_str in _SYSTEM_CJK_FONT_PATHS:
        p = Path(path_str)
        if p.exists():
            return p
    return None


def _load_cjk_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a CJK-capable TrueType font; warn and fall back to PIL default on failure."""
    font_path = _find_cjk_font()
    if font_path is None:
        print(
            "Warning: No CJK font found. Run 'setup-fonts' to download AlibabaPuHuiTi.",
            file=sys.stderr,
        )
        return ImageFont.load_default()
    try:
        return ImageFont.truetype(str(font_path), size=size)
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: Could not load font {font_path}: {exc}", file=sys.stderr)
        return ImageFont.load_default()


def _resolve_service_endpoints() -> tuple[str, str]:
    """Resolve endpoints from environment variable override."""
    host = os.getenv("OPENSTREET_MAP_HOST")
    if not host:
        return DEFAULT_NOMINATIM_URL, DEFAULT_TILE_URL_TEMPLATE

    normalized = host.strip()
    parsed = urlsplit(
        normalized if "://" in normalized else f"https://{normalized}"
    )
    replacement_host = parsed.netloc or parsed.path
    replacement_host = replacement_host.strip("/")
    if not replacement_host:
        return DEFAULT_NOMINATIM_URL, DEFAULT_TILE_URL_TEMPLATE

    return (
        DEFAULT_NOMINATIM_URL.replace("openstreetmap.de", replacement_host),
        DEFAULT_TILE_URL_TEMPLATE.replace(
            "openstreetmap.de", replacement_host
        ),
    )


NOMINATIM_URL, TILE_URL_TEMPLATE = _resolve_service_endpoints()


@dataclass
class Place:
    name: str
    lat: float
    lon: float


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def geocode_place(query: str, limit: int = 1) -> list[dict[str, Any]]:
    """Geocode text query with Nominatim."""
    params = {
        "q": query,
        "format": "jsonv2",
        "addressdetails": 1,
        "limit": limit,
    }
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=DEFAULT_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def latlon_to_world_px(lat: float, lon: float, zoom: int, tile_size: int) -> tuple[float, float]:
    """Convert lat/lon to world pixel coordinates in Web Mercator."""
    lat = clamp(lat, -85.05112878, 85.05112878)
    n = 2.0 ** zoom
    world_px = tile_size * n
    x = (lon + 180.0) / 360.0 * world_px
    lat_rad = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * world_px
    return x, y


def choose_zoom(
    points: Iterable[Place],
    width: int,
    height: int,
    tile_size: int,
    max_zoom: int = 19,
    min_zoom: int = 1,
    padding_ratio: float = DEFAULT_VIEW_PADDING_RATIO,
    marker_radius_px: int = MARKER_RADIUS_PX,
    min_edge_padding_px: int = MIN_EDGE_PADDING_PX,
) -> int:
    """Pick the highest zoom that fits all points inside target viewport."""
    pts = list(points)
    if not pts:
        raise ValueError("points must not be empty")

    # Keep a small but explicit edge margin so marker circles remain fully visible.
    pad_x = max(width * padding_ratio, float(min_edge_padding_px + marker_radius_px))
    pad_y = max(height * padding_ratio, float(min_edge_padding_px + marker_radius_px))
    avail_w = max(1.0, width - pad_x * 2.0)
    avail_h = max(1.0, height - pad_y * 2.0)

    for zoom in range(max_zoom, min_zoom - 1, -1):
        coords = [latlon_to_world_px(p.lat, p.lon, zoom, tile_size) for p in pts]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        span_x = max(xs) - min(xs)
        span_y = max(ys) - min(ys)
        if span_x <= avail_w and span_y <= avail_h:
            return zoom

    return min_zoom


def fetch_tile(z: int, x: int, y: int, session: requests.Session) -> Image.Image:
    """Download one OSM tile image."""
    max_tile = (2**z) - 1
    if y < 0 or y > max_tile:
        return Image.new("RGB", (DEFAULT_TILE_SIZE, DEFAULT_TILE_SIZE), color=(245, 245, 245))

    x_wrapped = x % (2**z)
    url = TILE_URL_TEMPLATE.format(z=z, x=x_wrapped, y=y)
    resp = session.get(url, timeout=DEFAULT_TIMEOUT)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert("RGB")


def build_base_map(
    points: list[Place],
    width: int,
    height: int,
    tile_size: int,
    zoom: int,
) -> tuple[Image.Image, list[tuple[float, float]]]:
    """Build cropped base map and return point pixel coordinates on it."""
    world_coords = [latlon_to_world_px(p.lat, p.lon, zoom, tile_size) for p in points]
    xs = [c[0] for c in world_coords]
    ys = [c[1] for c in world_coords]

    center_x = (min(xs) + max(xs)) / 2.0
    center_y = (min(ys) + max(ys)) / 2.0

    left = center_x - width / 2.0
    top = center_y - height / 2.0
    right = left + width
    bottom = top + height

    tile_x_min = math.floor(left / tile_size)
    tile_x_max = math.floor((right - 1) / tile_size)
    tile_y_min = math.floor(top / tile_size)
    tile_y_max = math.floor((bottom - 1) / tile_size)

    canvas_w = (tile_x_max - tile_x_min + 1) * tile_size
    canvas_h = (tile_y_max - tile_y_min + 1) * tile_size
    tile_canvas = Image.new("RGB", (canvas_w, canvas_h), color=(245, 245, 245))

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    for ty in range(tile_y_min, tile_y_max + 1):
        for tx in range(tile_x_min, tile_x_max + 1):
            tile_img = fetch_tile(zoom, tx, ty, session)
            ox = (tx - tile_x_min) * tile_size
            oy = (ty - tile_y_min) * tile_size
            tile_canvas.paste(tile_img, (ox, oy))

    crop_left = int(round(left - tile_x_min * tile_size))
    crop_top = int(round(top - tile_y_min * tile_size))
    crop_right = crop_left + width
    crop_bottom = crop_top + height
    map_img = tile_canvas.crop((crop_left, crop_top, crop_right, crop_bottom))

    point_pixels = [(x - left, y - top) for (x, y) in world_coords]
    return map_img, point_pixels


def draw_markers(map_img: Image.Image, point_pixels: list[tuple[float, float]]) -> Image.Image:
    """Draw numbered markers on map image."""
    out = map_img.copy()
    draw = ImageDraw.Draw(out)

    font = _load_cjk_font(12)

    for idx, (x, y) in enumerate(point_pixels, start=1):
        r = MARKER_RADIUS_PX
        cx = int(round(x))
        cy = int(round(y))

        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(211, 47, 47), outline=(255, 255, 255), width=2)

        label = str(idx)
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw / 2, cy - th / 2), label, font=font, fill=(255, 255, 255))

    return out


def build_legend(places: list[Place], width: int, cols: int = 3) -> Image.Image:
    """Create legend panel for place indices (names only, no coordinates), multi-column."""
    padding = 14
    line_height = 26
    title_height = 30
    rows = math.ceil(len(places) / cols)
    legend_height = title_height + padding * 2 + line_height * rows

    panel = Image.new("RGB", (width, legend_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(panel)
    title_font = _load_cjk_font(16)
    font = _load_cjk_font(14)

    draw.text((padding, 8), "图例 / Legend", fill=(0, 0, 0), font=title_font)

    col_width = (width - padding * 2) // cols
    for idx, place in enumerate(places, start=1):
        col = (idx - 1) % cols
        row = (idx - 1) // cols
        x = padding + col * col_width
        y = title_height + padding + row * line_height
        draw.text((x, y), f"{idx}. {place.name}", fill=(20, 20, 20), font=font)

    return panel


def render_annotated_map(
    places: list[Place],
    output_path: Path | None,
    width: int = 1600,
    height: int = 800,
    tile_size: int = DEFAULT_TILE_SIZE,
    return_base64: bool = False,
) -> dict[str, Any]:
    if not places:
        raise ValueError("No places to render")

    zoom = choose_zoom(
        places,
        width,
        height,
        tile_size,
        padding_ratio=DEFAULT_VIEW_PADDING_RATIO,
        marker_radius_px=MARKER_RADIUS_PX,
        min_edge_padding_px=MIN_EDGE_PADDING_PX,
    )
    map_img, point_pixels = build_base_map(places, width, height, tile_size, zoom)
    annotated = draw_markers(map_img, point_pixels)
    legend = build_legend(places, width)

    final_img = Image.new("RGB", (width, height + legend.height), color=(255, 255, 255))
    final_img.paste(annotated, (0, 0))
    final_img.paste(legend, (0, height))

    result: dict[str, Any] = {
        "zoom": zoom,
        "size": {"width": width, "height": height + legend.height},
        "places": [
            {"index": i + 1, "name": p.name, "lat": p.lat, "lon": p.lon}
            for i, p in enumerate(places)
        ],
    }

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_img.save(output_path)
        result["output"] = str(output_path)

    if return_base64:
        buf = BytesIO()
        final_img.save(buf, format="PNG")
        result["image_base64"] = base64.b64encode(buf.getvalue()).decode("ascii")

    return result


def normalize_places(raw: list[dict[str, Any]]) -> list[Place]:
    """Normalize mixed input entries: supports explicit lat/lon or query."""
    places: list[Place] = []

    for item in raw:
        name = item.get("name")
        if not name:
            raise ValueError("Each place must include a 'name'")

        if "lat" in item and "lon" in item:
            places.append(Place(name=name, lat=float(item["lat"]), lon=float(item["lon"])))
            continue

        query = item.get("query") or name
        candidates = geocode_place(query, limit=1)
        if not candidates:
            raise ValueError(f"No geocode result for place: {name}")

        best = candidates[0]
        places.append(Place(name=name, lat=float(best["lat"]), lon=float(best["lon"])))

    return places


def cmd_locate(args: argparse.Namespace) -> int:
    results = geocode_place(args.query, limit=args.limit)
    output = [
        {
            "display_name": r.get("display_name"),
            "lat": float(r["lat"]),
            "lon": float(r["lon"]),
            "type": r.get("type"),
            "class": r.get("class"),
        }
        for r in results
    ]
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    if args.points_base64:
        decoded = base64.b64decode(args.points_base64).decode("utf-8")
        data = json.loads(decoded)
    elif args.points_file:
        data = json.loads(Path(args.points_file).read_text(encoding="utf-8"))
    else:
        raise ValueError("One of --points-file or --points-base64 is required")

    if not isinstance(data, list):
        raise ValueError("Input points must be a JSON array")

    output_path = Path(args.output) if args.output else None
    if output_path is None and not args.base64:
        raise ValueError("At least one of --output or --base64 is required")

    places = normalize_places(data)
    result = render_annotated_map(
        places=places,
        output_path=output_path,
        width=args.width,
        height=args.height,
        return_base64=args.base64,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenStreetMap skill helper")
    sub = parser.add_subparsers(dest="command", required=True)

    locate = sub.add_parser("locate", help="Query one place location info")
    locate.add_argument("--query", required=True, help="Place name / address")
    locate.add_argument("--limit", type=int, default=1, help="Number of matches")
    locate.set_defaults(func=cmd_locate)

    render = sub.add_parser("render", help="Render annotated map image")
    points_input = render.add_mutually_exclusive_group(required=True)
    points_input.add_argument("--points-file", help="JSON array file for places")
    points_input.add_argument("--points-base64", help="Base64 encoded JSON array for places")
    render.add_argument("--output", default=None, help="Output image path (PNG)")
    render.add_argument("--base64", action="store_true", help="Include base64-encoded PNG in JSON output")
    render.add_argument("--width", type=int, default=1600, help="Map width")
    render.add_argument("--height", type=int, default=800, help="Map height")
    render.set_defaults(func=cmd_render)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return args.func(args)
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
