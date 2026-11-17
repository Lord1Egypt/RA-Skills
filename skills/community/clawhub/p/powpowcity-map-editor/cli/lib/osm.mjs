// IsoCity CLI - OSM data rasterizer, generalized from mapgen/generate-map.mjs
import { createTile } from './gamestate.mjs';

export function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function pointInPolygon(px, py, ring) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if (((yi > py) !== (yj > py)) && (px < ((xj - xi) * (py - yi)) / (yj - yi) + xi)) inside = !inside;
  }
  return inside;
}

const ROAD_TYPES = new Set([
  'trunk', 'primary', 'secondary', 'tertiary', 'residential', 'unclassified',
  'service', 'living_street', 'pedestrian',
  'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link',
]);

const GREEN_LANDUSE = new Set(['grass', 'forest', 'meadow', 'recreation_ground']);

const COMMERCIAL_TAGS = new Set(['office', 'commercial', 'retail', 'hotel', 'service']);

function classifyBuilding(buildingTag, size) {
  if (COMMERCIAL_TAGS.has(buildingTag)) return size <= 3 ? 'shop_small' : 'office_low';
  if (size <= 1) return 'house_small';
  if (size <= 3) return 'house_medium';
  return 'apartment_low';
}

function sportTypeOf(tags) {
  const sport = tags.sport || '';
  if (tags.leisure === 'track' || sport.includes('running') || sport.includes('athletics')) return 'football_field';
  if (sport.includes('tennis')) return 'tennis';
  if (sport.includes('basketball')) return 'basketball_courts';
  if (sport.includes('soccer') || sport.includes('football')) return 'soccer_field_small';
  if (sport.includes('baseball')) return 'baseball_field_small';
  if (sport.includes('swimming')) return 'swimming_pool';
  return 'playground_small';
}

/**
 * Rasterize OSM elements (Overpass JSON) into an IsoCity grid.
 * region: { polygons: [[lon,lat],...][] } - features limited to inside these rings
 * bbox: fetch bbox { minLat, minLon, maxLat, maxLon } - scale is anchored to this
 *       area (way nodes outside it are drawn but excluded from the bounds).
 */
export function rasterizeOsm(osm, { gridSize, pad = 4, region = null, bbox = null, centerLat, centerLon, seed = 42, cityLabel = '' }) {
  const rng = mulberry32(seed);

  const nodeIdx = new Map();
  for (const el of osm.elements) {
    if (el.type === 'node') nodeIdx.set(el.id, [el.lon, el.lat]);
  }
  const wayCoords = (way) => (way.nodes || []).map((id) => nodeIdx.get(id)).filter(Boolean);
  const wayById = new Map(osm.elements.filter((e) => e.type === 'way').map((e) => [e.id, e]));

  const inRegion = (lon, lat) => {
    if (!region || region.polygons.length === 0) return true;
    for (const ring of region.polygons) {
      if (pointInPolygon(lon, lat, ring)) return true;
    }
    return false;
  };

  // Equirectangular projection around the region center
  const MX = 111320 * Math.cos((centerLat * Math.PI) / 180);
  const MY = 110540;
  const toMeter = ([lon, lat]) => [(lon - centerLon) * MX, (centerLat - lat) * MY];

  // Collect all features to compute bounds
  const features = { rings: [], roads: [] };
  const buildingWays = [];
  const buildingRelations = [];

  for (const el of osm.elements) {
    if (el.type === 'relation') {
      if (el.tags && el.tags.building) buildingRelations.push(el);
      continue;
    }
    if (el.type !== 'way' || !el.nodes) continue;
    const t = el.tags || {};
    const pts = wayCoords(el);
    if (pts.length < 2) continue;
    const isClosed = pts.length > 3 && el.nodes[0] === el.nodes[el.nodes.length - 1];
    const isWater = t.natural === 'water' || t.waterway === 'riverbank';
    const isGreen = t.leisure === 'park' || t.leisure === 'garden' || GREEN_LANDUSE.has(t.landuse);
    const isSport = t.leisure === 'pitch' || t.leisure === 'track' || t.leisure === 'playground';
    if (isClosed && (isWater || isGreen || isSport)) {
      features.rings.push({ id: el.id, name: t.name || '', isWater, isGreen, isSport, tags: t, lonLat: pts });
    } else if (t.highway && ROAD_TYPES.has(t.highway)) {
      features.roads.push({ id: el.id, name: t.name || '', lonLat: pts });
    }
    if (t.building && isClosed) {
      buildingWays.push({ id: el.id, name: t.name || '', tags: t, lonLat: pts });
    }
  }

  // Compute grid mapping from feature bounds.
  // Only nodes inside the fetch bbox anchor the scale - way nodes far outside
  // (returned by Overpass for ways that merely cross the bbox) would stretch it.
  const inBbox = (lonLat) => {
    if (!bbox) return true;
    const [lon, lat] = lonLat;
    return lon >= bbox.minLon && lon <= bbox.maxLon && lat >= bbox.minLat && lat <= bbox.maxLat;
  };
  const allMeters = [
    ...features.rings.flatMap((r) => r.lonLat.filter(inBbox).map(toMeter)),
    ...features.roads.flatMap((r) => r.lonLat.filter(inBbox).map(toMeter)),
    ...buildingWays.flatMap((b) => b.lonLat.filter(inBbox).map(toMeter)),
  ];
  if (allMeters.length === 0) {
    throw new Error('No usable features (roads/water/buildings) found in the OSM data for this area');
  }
  let b = { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity };
  for (const [mx, my] of allMeters) {
    if (mx < b.minX) b.minX = mx;
    if (mx > b.maxX) b.maxX = mx;
    if (my < b.minY) b.minY = my;
    if (my > b.maxY) b.maxY = my;
  }
  const usable = gridSize - pad * 2;
  const scale = usable / Math.max(b.maxX - b.minX, b.maxY - b.minY);
  const offX = pad + (usable - (b.maxX - b.minX) * scale) / 2 - b.minX * scale;
  const offY = pad + (usable - (b.maxY - b.minY) * scale) / 2 - b.minY * scale;
  const toGrid = (lonLat) => {
    const [mx, my] = toMeter(lonLat);
    return [mx * scale + offX, my * scale + offY];
  };
  const oneTileM = 1 / scale;

  const type = Array.from({ length: gridSize }, () => new Array(gridSize).fill('grass'));
  const zone = Array.from({ length: gridSize }, () => new Array(gridSize).fill('none'));
  const inside = Array.from({ length: gridSize }, () => new Array(gridSize).fill(false));

  const gridLonLat = (x, y) => {
    // inverse of toGrid for region tests (approximate: use cell center)
    const mx = (x + 0.5 - offX) / scale;
    const my = (y + 0.5 - offY) / scale;
    return [centerLon + mx / MX, centerLat - my / MY];
  };

  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      const [lon, lat] = gridLonLat(x, y);
      inside[y][x] = inRegion(lon, lat);
    }
  }

  const bounds = (pts) => pts.reduce((acc, [px, py]) => ({
    minX: Math.min(acc.minX, px), maxX: Math.max(acc.maxX, px),
    minY: Math.min(acc.minY, py), maxY: Math.max(acc.maxY, py),
  }), { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity });

  // Water
  const waterBodies = [];
  for (const ring of features.rings.filter((r) => r.isWater)) {
    const g = ring.lonLat.map(toGrid);
    const rb = bounds(g);
    const cells = [];
    for (let y = Math.max(0, Math.floor(rb.minY)); y <= Math.min(gridSize - 1, Math.ceil(rb.maxY)); y++) {
      for (let x = Math.max(0, Math.floor(rb.minX)); x <= Math.min(gridSize - 1, Math.ceil(rb.maxX)); x++) {
        if (inside[y][x] && pointInPolygon(x + 0.5, y + 0.5, g)) cells.push([x, y]);
      }
    }
    if (cells.length === 0) {
      const cx = Math.round((rb.minX + rb.maxX) / 2), cy = Math.round((rb.minY + rb.maxY) / 2);
      if (cx >= 0 && cx < gridSize && cy >= 0 && cy < gridSize && inside[cy][cx]) cells.push([cx, cy]);
    }
    if (cells.length === 0) continue;
    for (const [x, y] of cells) type[y][x] = 'water';
    if (cells.length >= 2) {
      waterBodies.push({
        id: `osm-water-${ring.id}`,
        name: ring.name || 'Water',
        type: 'lake',
        tiles: cells.map(([x, y]) => ({ x, y })),
        centerX: Math.round(cells.reduce((s, c) => s + c[0], 0) / cells.length),
        centerY: Math.round(cells.reduce((s, c) => s + c[1], 0) / cells.length),
      });
    }
  }

  // Roads (skip water)
  let roadCells = 0;
  for (const road of features.roads) {
    const pts = road.lonLat.map(toGrid);
    for (let i = 0; i < pts.length - 1; i++) {
      const [x1, y1] = pts[i], [x2, y2] = pts[i + 1];
      const len = Math.hypot(x2 - x1, y2 - y1);
      const steps = Math.max(1, Math.ceil(len / 0.25));
      for (let s = 0; s <= steps; s++) {
        const x = Math.floor(x1 + ((x2 - x1) * s) / steps);
        const y = Math.floor(y1 + ((y2 - y1) * s) / steps);
        if (x < 0 || x >= gridSize || y < 0 || y >= gridSize) continue;
        if (type[y][x] === 'water') continue;
        if (type[y][x] !== 'road') { type[y][x] = 'road'; roadCells++; }
      }
    }
  }

  // Buildings (ways)
  const markCell = (x, y, bt, bz) => { type[y][x] = bt; zone[y][x] = bz; };
  const findFreeNear = (cx, cy) => {
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const x = cx + dx, y = cy + dy;
        if (x < 0 || x >= gridSize || y < 0 || y >= gridSize) continue;
        if (!inside[y][x]) continue;
        if (type[y][x] === 'grass' || type[y][x] === 'tree') return [x, y];
      }
    }
    return null;
  };

  let buildingCount = 0, buildingCells = 0;
  const placeBuildingCells = (cells, tags) => {
    let free = cells.filter(([x, y]) => type[y][x] === 'grass' || type[y][x] === 'tree');
    if (free.length === 0) {
      if (cells.length === 0) return;
      const rb = bounds(cells);
      const c = findFreeNear(Math.floor((rb.minX + rb.maxX) / 2), Math.floor((rb.minY + rb.maxY) / 2));
      if (c) free = [c];
    }
    if (free.length === 0) return;
    const bt = classifyBuilding(tags.building || 'yes', free.length);
    const bz = COMMERCIAL_TAGS.has(tags.building) ? 'commercial' : 'residential';
    for (const [x, y] of free) markCell(x, y, bt, bz);
    buildingCount++;
    buildingCells += free.length;
  };

  for (const bw of buildingWays) {
    const g = bw.lonLat.map(toGrid);
    const rb = bounds(g);
    const cells = [];
    for (let y = Math.max(0, Math.floor(rb.minY)); y <= Math.min(gridSize - 1, Math.ceil(rb.maxY)); y++) {
      for (let x = Math.max(0, Math.floor(rb.minX)); x <= Math.min(gridSize - 1, Math.ceil(rb.maxX)); x++) {
        if (inside[y][x] && pointInPolygon(x + 0.5, y + 0.5, g)) cells.push([x, y]);
      }
    }
    placeBuildingCells(cells, bw.tags);
  }

  // Buildings (relations - multipolygons with inner courtyards)
  for (const rel of buildingRelations) {
    const outerRings = [], innerRings = [];
    for (const m of rel.members || []) {
      if (m.type !== 'way') continue;
      const w = wayById.get(m.ref);
      if (!w || !w.nodes) continue;
      const pts = wayCoords(w);
      if (pts.length < 4 || w.nodes[0] !== w.nodes[w.nodes.length - 1]) continue;
      (m.role === 'inner' ? innerRings : outerRings).push(pts.map(toGrid));
    }
    if (outerRings.length === 0) continue;
    const rb = bounds(outerRings.flat());
    const cells = [];
    for (let y = Math.max(0, Math.floor(rb.minY)); y <= Math.min(gridSize - 1, Math.ceil(rb.maxY)); y++) {
      for (let x = Math.max(0, Math.floor(rb.minX)); x <= Math.min(gridSize - 1, Math.ceil(rb.maxX)); x++) {
        if (!inside[y][x]) continue;
        if (!outerRings.some((r) => pointInPolygon(x + 0.5, y + 0.5, r))) continue;
        if (innerRings.some((r) => pointInPolygon(x + 0.5, y + 0.5, r))) continue;
        cells.push([x, y]);
      }
    }
    placeBuildingCells(cells, rel.tags || {});
  }

  // Sport pitches
  let sportCount = 0;
  for (const s of features.rings.filter((r) => r.isSport)) {
    const g = s.lonLat.map(toGrid);
    const rb = bounds(g);
    const cells = [];
    for (let y = Math.max(0, Math.floor(rb.minY)); y <= Math.min(gridSize - 1, Math.ceil(rb.maxY)); y++) {
      for (let x = Math.max(0, Math.floor(rb.minX)); x <= Math.min(gridSize - 1, Math.ceil(rb.maxX)); x++) {
        if (inside[y][x] && pointInPolygon(x + 0.5, y + 0.5, g) &&
            (type[y][x] === 'grass' || type[y][x] === 'tree')) cells.push([x, y]);
      }
    }
    if (cells.length === 0) continue;
    const st = sportTypeOf(s.tags || {});
    let place = cells;
    if (cells.length > 4) {
      const cx = cells.reduce((a, c) => a + c[0], 0) / cells.length;
      const cy = cells.reduce((a, c) => a + c[1], 0) / cells.length;
      place = [cells.reduce((best, c) => (Math.hypot(c[0] - cx, c[1] - cy) < Math.hypot(best[0] - cx, best[1] - cy) ? c : best), cells[0])];
    }
    for (const [x, y] of place) markCell(x, y, st, 'none');
    sportCount++;
  }

  // Trees on green areas
  const greenSets = features.rings.filter((r) => r.isGreen).map((r) => r.lonLat.map(toGrid));
  let treeCells = 0;
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      if (type[y][x] !== 'grass') continue;
      let p = inside[y][x] ? 0 : 0.05;
      if (inside[y][x]) {
        for (const g of greenSets) {
          if (pointInPolygon(x + 0.5, y + 0.5, g)) { p = 0.42; break; }
        }
      }
      if (p > 0 && rng() < p) { type[y][x] = 'tree'; treeCells++; }
    }
  }

  // Assemble grid
  const grid = [];
  let waterCells = 0;
  for (let y = 0; y < gridSize; y++) {
    const row = [];
    for (let x = 0; x < gridSize; x++) {
      const t = type[y][x];
      if (t === 'water') waterCells++;
      const tile = createTile(x, y, t, t === 'water' ? 60 : 50);
      if (tile.building.constructionProgress === 0) tile.building.constructionProgress = 100;
      tile.zone = zone[y][x];
      row.push(tile);
    }
    grid.push(row);
  }

  const stats = {
    waterCells, roadCells, treeCells, buildingCount, buildingCells, sportCount,
    waterBodies: waterBodies.length, oneTileM,
  };
  return { grid, waterBodies, stats };
}
