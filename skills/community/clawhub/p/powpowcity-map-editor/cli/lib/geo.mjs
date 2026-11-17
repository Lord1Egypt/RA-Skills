// IsoCity CLI - geospatial data providers (Baidu/Nominatim geocoding + Overpass OSM data)

import { geocodeBaidu, haversineMeters } from './baidu.mjs';

const USER_AGENT = 'isocity-cli/1.0 (https://powpowcity.powpow.online/)';

const OVERPASS_ENDPOINTS = [
  'https://overpass-api.de/api/interpreter',
  'https://overpass.kumi.systems/api/interpreter',
  'https://overpass.private.coffee/api/interpreter',
];

export async function geocodePlace(query, { ak = '', radius = 800 } = {}) {
  if (ak) {
    try {
      const b = await geocodeBaidu(query, ak);
      const offset = haversineMeters(b.bd09Lat, b.bd09Lon, b.lat, b.lon);
      return {
        lat: b.lat,
        lon: b.lon,
        displayName: b.displayName,
        bbox: bboxFromCenter(b.lat, b.lon, radius),
        polygons: [],
        coordNote: `Baidu BD-09 (${b.bd09Lat.toFixed(6)},${b.bd09Lon.toFixed(6)}) -> WGS-84 ` +
          `(${b.lat.toFixed(6)},${b.lon.toFixed(6)}) for OSM, corrected ~${Math.round(offset)}m`,
      };
    } catch (e) {
      process.stderr.write(`Baidu geocoding failed: ${e.message}\nFalling back to Nominatim...\n`);
    }
  }
  const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=jsonv2&limit=1&polygon_geojson=1`;
  let res;
  try {
    res = await fetch(url, {
      headers: { 'User-Agent': USER_AGENT, 'Accept-Language': 'en' },
      signal: AbortSignal.timeout(30000),
    });
  } catch (e) {
    throw new Error(
      `Geocoding "${query}" failed (${e.cause?.code || e.message}). ` +
      'Nominatim may be unreachable from this network. ' +
      'Fallback: use --lat and --lon with --radius instead.'
    );
  }
  if (!res.ok) throw new Error(`Nominatim geocoding failed: HTTP ${res.status}`);
  const results = await res.json();
  if (!Array.isArray(results) || results.length === 0) {
    throw new Error(`No geocoding result for "${query}"`);
  }
  const r = results[0];
  // boundingbox: [south, north, west, east] (strings)
  const [south, north, west, east] = r.boundingbox.map(Number);
  const polygons = [];
  if (r.geojson) {
    if (r.geojson.type === 'Polygon') {
      polygons.push(r.geojson.coordinates[0]);
    } else if (r.geojson.type === 'MultiPolygon') {
      for (const poly of r.geojson.coordinates) polygons.push(poly[0]);
    }
  }
  return {
    lat: Number(r.lat),
    lon: Number(r.lon),
    displayName: r.display_name,
    bbox: { minLat: south, minLon: west, maxLat: north, maxLon: east },
    polygons,
  };
}

export function bboxFromCenter(lat, lon, radiusMeters) {
  const dLat = radiusMeters / 110540;
  const dLon = radiusMeters / (111320 * Math.cos((lat * Math.PI) / 180));
  return {
    minLat: lat - dLat, maxLat: lat + dLat,
    minLon: lon - dLon, maxLon: lon + dLon,
  };
}

function overpassQuery(bbox) {
  const { minLat, minLon, maxLat, maxLon } = bbox;
  const bb = `(${minLat},${minLon},${maxLat},${maxLon})`;
  return `[out:json][timeout:90];
(
  way["building"]${bb};
  relation["building"]${bb};
  way["highway"]${bb};
  way["natural"="water"]${bb};
  way["waterway"="riverbank"]${bb};
  relation["natural"="water"]${bb};
  way["leisure"~"^(park|garden|pitch|track|playground)$"]${bb};
  way["landuse"~"^(grass|forest|meadow|recreation_ground)$"]${bb};
  relation["leisure"~"^(park|garden)$"]${bb};
  relation["landuse"~"^(forest|meadow|recreation_ground)$"]${bb};
);
(._;>;);
out body;`;
}

export async function fetchOverpass(bbox) {
  const query = overpassQuery(bbox);
  const errors = [];
  for (const endpoint of OVERPASS_ENDPOINTS) {
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'User-Agent': USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `data=${encodeURIComponent(query)}`,
        signal: AbortSignal.timeout(120000),
      });
      if (res.status === 429) {
        errors.push(`${endpoint}: rate limited`);
        continue;
      }
      if (!res.ok) {
        errors.push(`${endpoint}: HTTP ${res.status}`);
        continue;
      }
      return await res.json();
    } catch (e) {
      errors.push(`${endpoint}: ${e.message}`);
    }
  }
  throw new Error(`All Overpass endpoints failed:\n  ${errors.join('\n  ')}`);
}
