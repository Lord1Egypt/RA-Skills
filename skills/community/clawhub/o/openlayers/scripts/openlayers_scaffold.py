#!/usr/bin/env python3
"""Generate minimal OpenLayers HTML scaffolds for local debugging."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


MINIMAL_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>OpenLayers Minimal Map</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@latest/ol.css" />
    <style>
      html, body {{
        margin: 0;
        height: 100%;
      }}
      #map {{
        width: 100%;
        height: 100%;
      }}
      .panel {{
        position: absolute;
        top: 12px;
        left: 12px;
        z-index: 10;
        padding: 10px 12px;
        background: rgba(255, 255, 255, 0.92);
        border-radius: 8px;
        font: 13px/1.4 sans-serif;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
      }}
    </style>
  </head>
  <body>
    <div class="panel">OpenLayers minimal map</div>
    <div id="map"></div>
    <script type="module">
      import Map from "https://cdn.jsdelivr.net/npm/ol@latest/Map.js";
      import View from "https://cdn.jsdelivr.net/npm/ol@latest/View.js";
      import TileLayer from "https://cdn.jsdelivr.net/npm/ol@latest/layer/Tile.js";
      import OSM from "https://cdn.jsdelivr.net/npm/ol@latest/source/OSM.js";
      import {{ fromLonLat }} from "https://cdn.jsdelivr.net/npm/ol@latest/proj.js";

      const map = new Map({{
        target: "map",
        layers: [
          new TileLayer({{
            source: new OSM(),
          }}),
        ],
        view: new View({{
          center: fromLonLat([{lng}, {lat}]),
          zoom: {zoom},
        }}),
      }});

      window.map = map;
    </script>
  </body>
</html>
"""


GEOJSON_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>OpenLayers GeoJSON Map</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@latest/ol.css" />
    <style>
      html, body {{
        margin: 0;
        height: 100%;
        font-family: sans-serif;
      }}
      #map {{
        width: 100%;
        height: 100%;
      }}
      .panel {{
        position: absolute;
        top: 12px;
        left: 12px;
        z-index: 10;
        max-width: 320px;
        padding: 10px 12px;
        background: rgba(255, 255, 255, 0.94);
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
        font-size: 13px;
      }}
      .code {{
        margin-top: 6px;
        color: #444;
        word-break: break-all;
      }}
    </style>
  </head>
  <body>
    <div class="panel">
      <div>OpenLayers GeoJSON demo</div>
      <div class="code">GeoJSON: {geojson_label}</div>
    </div>
    <div id="map"></div>
    <script type="module">
      import Map from "https://cdn.jsdelivr.net/npm/ol@latest/Map.js";
      import View from "https://cdn.jsdelivr.net/npm/ol@latest/View.js";
      import TileLayer from "https://cdn.jsdelivr.net/npm/ol@latest/layer/Tile.js";
      import VectorLayer from "https://cdn.jsdelivr.net/npm/ol@latest/layer/Vector.js";
      import OSM from "https://cdn.jsdelivr.net/npm/ol@latest/source/OSM.js";
      import VectorSource from "https://cdn.jsdelivr.net/npm/ol@latest/source/Vector.js";
      import GeoJSON from "https://cdn.jsdelivr.net/npm/ol@latest/format/GeoJSON.js";
      import Fill from "https://cdn.jsdelivr.net/npm/ol@latest/style/Fill.js";
      import Stroke from "https://cdn.jsdelivr.net/npm/ol@latest/style/Stroke.js";
      import Style from "https://cdn.jsdelivr.net/npm/ol@latest/style/Style.js";
      import CircleStyle from "https://cdn.jsdelivr.net/npm/ol@latest/style/Circle.js";
      import {{ fromLonLat }} from "https://cdn.jsdelivr.net/npm/ol@latest/proj.js";

      const geojsonObject = {geojson_payload};
      const vectorSource = new VectorSource({{
        features: new GeoJSON().readFeatures(geojsonObject, {{
          dataProjection: "EPSG:4326",
          featureProjection: "EPSG:3857",
        }}),
      }});

      const vectorLayer = new VectorLayer({{
        source: vectorSource,
        style: new Style({{
          image: new CircleStyle({{
            radius: 6,
            fill: new Fill({{ color: "#d9480f" }}),
            stroke: new Stroke({{ color: "#ffffff", width: 2 }}),
          }}),
          stroke: new Stroke({{
            color: "#0b7285",
            width: 3,
          }}),
          fill: new Fill({{
            color: "rgba(11, 114, 133, 0.18)",
          }}),
        }}),
      }});

      const map = new Map({{
        target: "map",
        layers: [
          new TileLayer({{ source: new OSM() }}),
          vectorLayer,
        ],
        view: new View({{
          center: fromLonLat([{lng}, {lat}]),
          zoom: {zoom},
        }}),
      }});

      const extent = vectorSource.getExtent();
      if (extent.every(Number.isFinite)) {{
        map.getView().fit(extent, {{ padding: [40, 40, 40, 40], maxZoom: 15 }});
      }}

      map.on("singleclick", (event) => {{
        const feature = map.forEachFeatureAtPixel(event.pixel, (candidate) => candidate);
        if (!feature) return;
        console.log("Picked feature properties:", feature.getProperties());
      }});

      window.map = map;
    </script>
  </body>
</html>
"""


def write_text(path_text: str, content: str) -> None:
    path = Path(path_text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def cmd_minimal(args: argparse.Namespace) -> int:
    html_text = MINIMAL_TEMPLATE.format(lng=args.lng, lat=args.lat, zoom=args.zoom)
    write_text(args.out, html_text)
    print(json.dumps({"written": args.out, "template": "minimal"}, ensure_ascii=True, indent=2))
    return 0


def cmd_geojson(args: argparse.Namespace) -> int:
    geojson_path = Path(args.geojson)
    geojson_obj = json.loads(geojson_path.read_text(encoding="utf-8"))
    html_text = GEOJSON_TEMPLATE.format(
        geojson_label=html.escape(args.geojson),
        geojson_payload=json.dumps(geojson_obj, ensure_ascii=True, indent=2),
        lng=args.lng,
        lat=args.lat,
        zoom=args.zoom,
    )
    write_text(args.out, html_text)
    print(
        json.dumps(
            {"written": args.out, "template": "geojson", "geojson": args.geojson},
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenLayers HTML scaffold generator.")
    sub = parser.add_subparsers(dest="command", required=True)

    minimal = sub.add_parser("minimal", help="Write a minimal OpenLayers page.")
    minimal.add_argument("--out", required=True)
    minimal.add_argument("--lng", type=float, default=116.397)
    minimal.add_argument("--lat", type=float, default=39.908)
    minimal.add_argument("--zoom", type=int, default=11)
    minimal.set_defaults(func=cmd_minimal)

    geojson = sub.add_parser("geojson", help="Write an OpenLayers page with inline GeoJSON.")
    geojson.add_argument("--out", required=True)
    geojson.add_argument("--geojson", required=True)
    geojson.add_argument("--lng", type=float, default=116.397)
    geojson.add_argument("--lat", type=float, default=39.908)
    geojson.add_argument("--zoom", type=int, default=11)
    geojson.set_defaults(func=cmd_geojson)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
