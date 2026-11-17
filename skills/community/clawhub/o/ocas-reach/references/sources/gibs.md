# gibs — NASA Global Imagery Browse Services

## What this source has

GIBS is NASA's public tile service providing global satellite imagery from MODIS, VIIRS, and other instruments. It serves pre-rendered image tiles via OGC Web Map Tile Service (WMTS) and Web Map Service (WMS) protocols — no registration or API key required.

GIBS provides ~180+ imagery layers covering true-color composites, false-color scientific products, aerosol optical depth, sea surface temperature, vegetation indices, fire detections, and analytic overlays. Data spans from early MODIS era (2000+) through near-real-time (current day lagged ~6-8 hours). Layers are available at multiple resolutions (from 16km down to 15m per pixel) across four map projections (EPSG:4326, EPSG:3857, EPSG:3411, EPSG:3031).

Use GIBS for: satellite imagery at coordinates, any-location-from-orbit views, comparative date analysis, layered scientific products (aerosols, SST, vegetation). Does NOT provide raw swath data or new tasking — only visualizations processed from raw instrument data.

## Auth

| | |
|---|---|
| Required | none |
| Env var | — |
| Account | not needed |
| Plan tier | free, public access |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | no documented hard cap; throttle to <5 req/sec for polite sharing of NASA infrastructure |

## Endpoints

```bash
python3 scripts/reach.py query gibs <action> '<params_json>'
```

| Action | Purpose | Params |
|---|---|---|
| `layers` | List imagery layers with filters (MODIS, VIIRS, instruments, keywords) | `{"category": "modis", "search": "true color", "limit": 50}` |
| `capabilities` | Full WMTS capabilities, parsed to JSON or raw XML | `{"raw": false}` |
| `tile_url` | Build a WMTS tile URL for layer/zoom/coords/date | `{"layer": "...", "date": "2024-01-15", "level": 6, "row": 20, "col": 30}` |
| `wms_bbox` | Build a WMS GetMap URL for an arbitrary bounding box | `{"layer": "...", "bbox": "-122.5,37.5,-122.0,38.0", "width": 512}` |
| `projections` | List available map projections | `{}` |

## Worked examples

```bash
# List MODIS layers available
python3 scripts/reach.py query gibs layers '{"category": "modis", "limit": 20}'

# Search for vegetation / NDVI products
python3 scripts/reach.py query gibs layers '{"search": "NDVI", "limit": 10}'

# VIIRS near-real-time layers
python3 scripts/reach.py query gibs layers '{"instrument": "viirs", "limit": 15}'

# Build a tile URL for VIIRS_SNPP_DayNightBand_ENCC at zoom 5, specific coordinates
python3 scripts/reach.py query gibs tile_url '{
  "layer": "VIIRS_SNPP_DayNightBand_ENCC",
  "date": "2026-06-23",
  "level": 5,
  "row": 12,
  "col": 8,
  "format": "png"
}'

# WMS bbox for an area around San Francisco
python3 scripts/reach.py query gibs wms_bbox '{
  "layer": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
  "date": "2026-06-20",
  "bbox": "-123.0,37.0,-121.5,38.5",
  "width": 1024,
  "height": 512
}'

# Full capabilities parsed to JSON
python3 scripts/reach.py query gibs capabilities '{}'
```

## Response shape

**`layers`** (subset of fields):
```json
{
  "ok": true,
  "data": {
    "layers": [
      {
        "title": "Corrected Reflectance (True Color, VIIRS SNPP / VIIRS NOAA-20)",
        "identifier": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
        "formats": ["image/png", "image/jpeg"],
        "tile_matrix_sets": ["2km", "1km", "500m", "250m"],
        "has_time_dimension": true,
        "default_time": "2026-06-23",
        "time_values_sample": ["2024-12-01/2026-06-20/P1D"],
        "styles": ["default"]
      }
    ],
    "returned": 20,
    "total": 187,
    "limit": 20,
    "offset": 0
  },
  "citation": {
    "source": "NASA GIBS",
    "url": "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/",
    "accessed": "live"
  }
}
```

**`tile_url`**:
```json
{
  "ok": true,
  "data": {
    "url": "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/VIIRS_SNPP_CorrectedReflectance_TrueColor/default/2026-06-23/2km/5/12/8.png",
    "layer": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
    "date": "2026-06-23",
    "tile_matrix_set": "2km",
    "level": 5,
    "row": 12,
    "col": 8,
    "format": "png"
  }
}
```

**`wms_bbox`**:
```json
{
  "ok": true,
  "data": {
    "url": "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms?service=WMS&request=GetMap&version=1.1.1&layers=VIIRS_SNPP_CorrectedReflectance_TrueColor&styles=default&bbox=-123.0,37.0,-121.5,38.5&width=1024&height=512&srs=EPSG:4326&format=image%2Fpng&time=2026-06-20",
    "layer": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
    "date": "2026-06-20",
    "bbox": "-123.0,37.0,-121.5,38.5"
  }
}
```

**`projections`**:
```json
{
  "ok": true,
  "data": {
    "projections": ["epsg4326", "epsg3857", "epsg3411", "epsg3031"]
  }
}
```

## Pitfalls

- **No API key needed.** This is a public service. Don't overthink auth.
- **Layers default to "best" quality.** Replace `best` with `std` (standard-only) or `nrt` (near-real-time only) in the base URL if you need to filter recency vs. quality.
- **Time dimension is layer-specific.** Not all layers have time data (some are static, like climatologies). Check `has_time_dimension` before filtering by date.
- **Tile matrix sets vary by layer.** VIIRS DayNightBand only has coarse resolutions; VIIRS imagery goes down to 250m. Use `capabilities` to discover what a layer supports.
- **EPSG:4326 is the default.** Lat/lon coordinates are in WGS84 order (lon, lat for bbox since EPSG:4326 in WMS 1.1.1 swaps axis — be careful).
- **WMS bbox format is west,south,east,north.** Standard WMS ordering for SRS=EPSG:4326.
- **Tiles are PNG or JPEG.** True-color composites only — no raw data, no multi-band GeoTIFF.
- **Near-real-time = ~6-8 hour lag.** Not actual real-time. If you need "right now" imagery that doesn't exist in any public feed.
- **`layers` action fetches GetCapabilities on every call.** Results aren't cached locally. For bulk queries, use `capabilities` + parse client-side, or cache results yourself.
- **Coordinate-to-tile math is non-trivial.** If you need "what tile covers lat X lon Y at zoom Z," you need to compute tile row/col from the lat/lon → Web Mercator formula, or query WMS instead of WMTS.

## Source links

- GIBS documentation: https://nasa-gibs.github.io/gibs-api-docs/
- Available visualizations catalog: https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/
- GIBS tile viewer (for visual verification): https://gibs.earthdata.nasa.gov/image-gallery.html
- GIBS imagery in NASA Worldview: https://worldview.earthdata.nasa.gov/
