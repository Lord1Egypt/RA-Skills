# Mapbox Patterns

Load this file when the task needs concrete Mapbox implementation details.

## Baseline GL JS Setup

Use the smallest valid setup first:

```ts
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken = process.env.MAPBOX_ACCESS_TOKEN ?? "";

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/streets-v12",
  center: [116.397, 39.908],
  zoom: 10,
});
```

Checklist:

- Container element exists before constructing the map.
- Container has non-zero width and height.
- Token is present and valid for the requested APIs.

## React Pattern

Use a ref for the DOM node and clean up on unmount:

```ts
import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

export function MapView() {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;

    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: "mapbox://styles/mapbox/light-v11",
      center: [-74.006, 40.7128],
      zoom: 11,
    });

    return () => map.remove();
  }, []);

  return <div ref={containerRef} style={{ width: "100%", height: "100%" }} />;
}
```

If the map appears only after window resize, the container sizing is wrong.

## GeoJSON Source And Layer

Prefer data-driven styling over many DOM markers:

```ts
map.on("load", () => {
  map.addSource("places", {
    type: "geojson",
    data: placesGeoJson,
  });

  map.addLayer({
    id: "places-circle",
    type: "circle",
    source: "places",
    paint: {
      "circle-radius": 6,
      "circle-color": "#0f766e",
      "circle-stroke-width": 1.5,
      "circle-stroke-color": "#ffffff",
    },
  });
});
```

Use DOM markers only for small counts or highly custom HTML.

## Fitting Bounds

For multiple features, prefer `fitBounds` over guessing a zoom:

```ts
const bounds = new mapboxgl.LngLatBounds();
for (const feature of features) {
  bounds.extend(feature.geometry.coordinates as [number, number]);
}
map.fitBounds(bounds, { padding: 40, maxZoom: 14 });
```

## Layer Ordering

Mapbox draws later-added layers on top of earlier ones.

- Add fill/line layers before symbol layers when labels should stay above geometry.
- Use the optional second argument to `addLayer(layer, beforeId)` when precise ordering matters.
- If symbols disappear, check collision behavior and `icon-allow-overlap` or `text-allow-overlap` only after verifying layer order.

## Expressions

Mapbox style expressions are strict JSON-like arrays. Common patterns:

```ts
"circle-color": [
  "match",
  ["get", "status"],
  "open", "#16a34a",
  "closed", "#dc2626",
  "#64748b"
]
```

```ts
"circle-radius": [
  "interpolate",
  ["linear"],
  ["zoom"],
  5, 4,
  12, 10
]
```

Check expression shape carefully; many styling bugs are invalid expression arrays rather than bad data.

## Geocoding And Directions

- Geocoding: use forward geocoding for search boxes and reverse geocoding for dropped pins or picked coordinates.
- Directions: confirm profile (`driving`, `walking`, `cycling`) and whether the UI needs route geometry, step-by-step instructions, or both.
- For client apps, avoid firing an API request on every keystroke; debounce search input.

## Token Safety

- Treat public web tokens as configurable but still scoped.
- Restrict tokens by allowed URLs when possible.
- Keep secret tokens on the server side only.
- If the user pastes a real token into chat, avoid reprinting it.

## Migration Notes

When upgrading or fixing an existing app, check:

- `mapbox-gl` version and framework compatibility.
- Whether the code expects legacy style URLs or older plugin APIs.
- Whether CSS import was lost during bundler migration.
- Whether the project should stay on Mapbox or move to a MapLibre-compatible path.
