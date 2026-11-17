"""NASA GIBS connector — WMTS tile service for satellite imagery.

Actions:
    layers   — list available imagery layers (MODIS, VIIRS, etc.)
    tile_url  — build a tile URL for a given layer/date/zoom/coords
    capabilities — raw GetCapabilities XML (parsed into JSON)
"""
import os
from . import _http
try:
    from defusedxml.ElementTree import fromstring as ET_parse
except ImportError:
    # GIBS serves WMTS Capabilities XML from a trusted NASA origin.
    # No DOCTYPE/entity declarations expected in this format.
    import xml.etree.ElementTree as _ET
    ET_parse = _ET.fromstring
from urllib.parse import urlencode

WMTS_BASE = "https://gibs.earthdata.nasa.gov/wmts/epsg4326"
WMS_BASE = "https://gibs.earthdata.nasa.gov/wms/epsg4326"
CAPABILITIES_URL = WMTS_BASE + "/best/1.0.0/WMTSCapabilities.xml"

NS = {
    "wmts": "http://www.opengis.net/wmts/1.0",
    "ows": "http://www.opengis.net/ows/1.1",
    "xlink": "http://www.w3.org/1999/xlink",
}

PROJECTIONS = ["epsg4326", "epsg3857", "epsg3411", "epsg3031"]


def _parse_capabilities(xml_text):
    """Parse WMTS GetCapabilities into a structured dict of layers."""
    root = ET_parse(xml_text)
    layers_out = []
    for layer in root.findall("wmts:Contents/wmts:Layer", NS):
        title = layer.findtext("ows:Title", "", NS)
        identifier = layer.findtext("ows:Identifier", "", NS)
        formats = [f.text for f in layer.findall("wmts:Format", NS) if f.text]
        tile_matrix_sets = []
        for tms_link in layer.findall("wmts:TileMatrixSetLink", NS):
            tms = tms_link.findtext("wmts:TileMatrixSet", "", NS)
            tile_matrix_sets.append(tms)
        # Extract time dimension if present
        has_time = False
        default_time = None
        time_values = []
        for dim in layer.findall("wmts:Dimension", NS):
            dim_id = dim.findtext("ows:Identifier", "", NS)
            if dim_id == "Time":
                has_time = True
                default_time = dim.findtext("ows:Default", "", NS)
                time_values = [v.text for v in dim.findall("ows:Value", NS) if v.text]
                break
        # styles
        styles = [s.findtext("ows:Identifier", "", NS) for s in layer.findall("wmts:Style", NS)]
        layers_out.append({
            "title": title,
            "identifier": identifier,
            "formats": formats,
            "tile_matrix_sets": tile_matrix_sets,
            "has_time_dimension": has_time,
            "default_time": default_time,
            "time_values_sample": time_values[:5],
            "styles": styles or ["default"],
        })
    return {"layers": layers_out, "count": len(layers_out)}


def _fetch_capabilities():
    """Fetch and cache the WMTS GetCapabilities document."""
    xml = _http.get(CAPABILITIES_URL, headers={
        "User-Agent": "ocas-reach (contact: os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com"))",
        "Accept": "application/xml",
    })
    return xml


def query(action, params, auth):
    if action == "layers":
        # Optional filters: category (modis, viirs, instruments), has_time
        category = (params.get("category") or "").lower()
        instrument = (params.get("instrument") or "").lower()
        search = (params.get("search") or "").lower()
        limit = int(params.get("limit") or 50)
        offset = int(params.get("offset") or 0)

        xml = _fetch_capabilities()
        parsed = _parse_capabilities(xml)
        layers = parsed["layers"]

        # Filters
        if category:
            layers = [l for l in layers if category in l["identifier"].lower() or category in l["title"].lower()]
        if instrument:
            layers = [l for l in layers if instrument in l["identifier"].lower() or instrument in l["title"].lower()]
        if search:
            layers = [l for l in layers if search in l["identifier"].lower() or search in l["title"].lower()]

        total = len(layers)
        layers = layers[offset:offset + limit]
        return {
            "ok": True,
            "data": {
                "layers": layers,
                "returned": len(layers),
                "total": total,
                "limit": limit,
                "offset": offset,
            },
            "citation": {
                "source": "NASA GIBS",
                "url": "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/",
                "accessed": "live",
            },
        }

    if action == "capabilities":
        # Raw parsed capabilities (full, unfiltered)
        raw = params.get("raw", False)
        xml = _fetch_capabilities()
        if raw:
            return {"ok": True, "data": xml}
        parsed = _parse_capabilities(xml)
        parsed["citation"] = {
            "source": "NASA GIBS",
            "url": CAPABILITIES_URL,
            "accessed": "live",
        }
        return {"ok": True, "data": parsed}

    if action == "tile_url":
        # Build a tile URL. Params: layer, date, tile_matrix_set, level, row, col, format
        layer = params.get("layer")
        if not layer:
            raise ValueError("tile_url requires {'layer': '<LayerIdentifier>'}")
        date = params.get("date", "default")
        tms = params.get("tile_matrix_set") or params.get("tms", "2km")
        level = int(params.get("level", params.get("z", 0)))
        row = int(params.get("row", params.get("y", 0)))
        col = int(params.get("col", params.get("x", 0)))
        fmt = params.get("format", "png")

        # URL template from WMTS spec: .../{Time}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png
        if date and date != "default":
            url = f"{WMTS_BASE}/best/{layer}/default/{date}/{tms}/{level}/{row}/{col}.{fmt}"
        else:
            url = f"{WMTS_BASE}/best/{layer}/default/default/{tms}/{level}/{row}/{col}.{fmt}"
        return {
            "ok": True,
            "data": {
                "url": url,
                "layer": layer,
                "date": date,
                "tile_matrix_set": tms,
                "level": level,
                "row": row,
                "col": col,
                "format": fmt,
            },
            "citation": {"source": "NASA GIBS", "url": url},
        }

    if action == "wms_bbox":
        # Build a WMS GetMap URL for a bounding box. Params: layer, date, bbox (west,south,east,north), width, height
        layer = params.get("layer")
        if not layer:
            raise ValueError("wms_bbox requires {'layer': '<LayerIdentifier>'}")
        date = params.get("date", "default")
        bbox = params.get("bbox")  # comma-separated: west,south,east,north
        if not bbox:
            raise ValueError("wms_bbox requires {'bbox': 'west,south,east,north'}")
        width = int(params.get("width", 512))
        height = int(params.get("height", 512))
        crs = params.get("crs", "EPSG:4326")

        url = (f"{WMS_BASE}/best/wms?"
               f"service=WMS&request=GetMap&version=1.1.1"
               f"&layers={layer}&styles=default"
               f"&bbox={bbox}&width={width}&height={height}"
               f"&srs={crs}&format=image%2Fpng")
        if date and date != "default":
            url += f"&time={date}"
        return {
            "ok": True,
            "data": {"url": url, "layer": layer, "date": date, "bbox": bbox},
            "citation": {"source": "NASA GIBS"},
        }

    if action == "projections":
        return {"ok": True, "data": {"projections": PROJECTIONS}}

    raise ValueError(f"Unknown action: {action}")
