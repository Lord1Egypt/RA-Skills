#!/usr/bin/env node
// IsoCity CLI - map editing tool for AI agents.
// Full documentation: see AGENTS.md in the repo root.
import fs from 'node:fs';
import path from 'node:path';
import {
  BUILDING_TYPES, ZONE_TYPES, PLACE_COSTS, BULLDOZE_COST, ZONE_COST, TERRAFORM_COST,
  GROWABLE_TYPES, getBuildingSize, createStateShell, blankGrid, loadStateFile, saveStateFile,
  cloneGrid, inBounds,
} from './lib/gamestate.mjs';
import * as rules from './lib/rules.mjs';
import { asciiMap, infoText, tileDetailText } from './lib/mapview.mjs';
import { createShareUrl } from './lib/share.mjs';
import { createShortLink, SnapshotTooLargeError } from './lib/shortlink.mjs';
import { generateRandomTerrain } from './lib/random.mjs';
import { geocodePlace, bboxFromCenter, fetchOverpass } from './lib/geo.mjs';
import { toWgs84, haversineMeters } from './lib/baidu.mjs';
import { rasterizeOsm } from './lib/osm.mjs';
import { screenshotState, simulateTicks } from './lib/browser.mjs';

const DEFAULT_GAME_URL = 'http://localhost:3000';
const ONLINE_GAME_URL = 'https://powpowcity.powpow.online';

const USAGE = `IsoCity CLI - edit IsoCity maps from the command line

Usage: node cli/isocity.mjs <command> [args]

Create:
  new [--grid N] [--name NAME] [--money N] [--seed N] [--out FILE]
      Create a blank flat-grass city (default 60x60).
  new --random [options]
      Create a city with random terrain (noise lakes, coast, tree clusters).
  new --osm --place "Peking University" [--ak AK] [--radius M] [options]
      Create a city from real-world OSM data by place name. Geocoding uses
      Baidu Maps when --ak (or env BAIDU_MAP_AK) is set - recommended in
      China: coordinates are corrected BD-09 -> WGS-84 and the API is fast
      and reachable. Without an AK it falls back to Nominatim (often
      unreachable from mainland China).
  new --osm --lat 39.99 --lon 116.31 [--radius 800] [--coord-sys wgs84|gcj02|bd09] [options]
      Create a city from real-world OSM data by coordinates (radius in meters).
      --coord-sys declares the input coordinate system: values copied from
      Baidu Maps are bd09, from Amap/Tencent gcj02 - they are corrected to
      true GPS (WGS-84) before querying OSM. Default: wgs84.

Query:
  info <file>                          City summary (money, population, buildings)
  map <file> [--no-legend]             ASCII map preview
  get <file> <x> <y>                   Full detail of one tile
  buildings                            List all valid building types with size/cost

Edit (each write creates a .bak backup of the previous version):
  place <file> <buildingType> --at x,y [--free]
  place <file> <buildingType> --tiles x,y;x,y
  place <file> <buildingType> --rect x1,y1,x2,y2
  place <file> <buildingType> --line x1,y1,x2,y2
      Place a building. Costs money unless --free.
  bulldoze <file> (--at|--tiles|--rect|--line ...) [--free]
      Demolish tiles ($10/tile). Removes whole multi-tile buildings and bridges.
  zone <file> <residential|commercial|industrial|none> (--at|--tiles|--rect) [--free]
      Zone/unzone land ($50/tile, unzone is free). Only on grass/tree/road tiles.
  terraform <file> <water|land|tree> (--at|--tiles|--rect) [--free]
      water: land->water, clears buildings ($50000/tile)
      land:  water->grass ($50000/tile)
      tree:  plant trees on grass ($15/tile)
  tax <file> [rate]                    Show or set tax rate (0-100)
  budget <file> [key] [funding]        Show budget, or set funding (0-100).
                                      Keys: police fire health education
                                            transportation parks power water
  money <file> <amount>                Set money, or adjust with +N / -N

Share:
  share <file> [--url BASE]            Print a share URL that loads this city
                                       (default base: ${ONLINE_GAME_URL}/)
  share <file> --short [--gallery] [--url BASE] [--api-base URL] [--anon-key KEY]
                                       Upload an immutable snapshot to the
                                       server and print a short /city/<code>
                                       link (<=50 chars) that survives chat
                                       apps and LLM re-telling. --gallery also
                                       lists the map on the homepage hot maps
                                       (热门地图). If the server is unreachable,
                                       falls back to printing the long URL.
                                       Env overrides: POWPOWCITY_API_BASE /
                                       POWPOWCITY_ANON_KEY. One-time setup: run
                                       supabase/shared_cities.sql in the
                                       Supabase SQL editor.

Browser (need the game running; defaults to ${DEFAULT_GAME_URL}):
  screenshot <file> [-o out.png] [--url URL] [--wait MS] [--width W] [--height H] [--zoom-out N]
      Render the city in a headless browser and capture the canvas.
      --zoom-out N scrolls the mouse wheel N times first (default 10 = city
      overview; use 0 for the game's default close-up view).
  simulate <file> --ticks N [-o out.json] [--url URL]
      Run N simulation ticks in the real game engine, save the result.
      Requires: npm install && npx playwright install chromium
      Start the game first (npm run dev) or pass --url ${ONLINE_GAME_URL}

Examples:
  node cli/isocity.mjs new --random --grid 60 --name Lakeside --seed 7
  node cli/isocity.mjs new --osm --place "Peking University" --ak YOUR_BAIDU_AK
  node cli/isocity.mjs new --osm --lat 39.9962 --lon 116.3174 --coord-sys bd09
  node cli/isocity.mjs place city.json road --line 5,10 5,40
  node cli/isocity.mjs place city.json park --at 12,12
  node cli/isocity.mjs zone city.json residential --rect 8,8,20,20
  node cli/isocity.mjs screenshot city.json -o preview.png
  node cli/isocity.mjs share city.json
`;

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-o') {
      const next = argv[i + 1];
      if (next === undefined) throw new Error('-o requires a value');
      args.out = next;
      i++;
    } else if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith('--') && next !== '-o') {
        args[key] = next;
        i++;
        // --rect/--line accept "x1,y1,x2,y2" or "x1,y1 x2,y2"
        const after = argv[i + 1];
        if ((key === 'rect' || key === 'line') && after !== undefined &&
            /^-?\d+\s*,\s*-?\d+$/.test(next) && /^-?\d+\s*,\s*-?\d+$/.test(after)) {
          args[key] = `${next},${after}`;
          i++;
        }
      } else {
        args[key] = true;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

function parseIntArg(value, name, { min, max } = {}) {
  const n = parseInt(value, 10);
  if (Number.isNaN(n)) throw new Error(`Invalid --${name}: "${value}" is not an integer`);
  if (min !== undefined && n < min) throw new Error(`--${name} must be >= ${min}`);
  if (max !== undefined && n > max) throw new Error(`--${name} must be <= ${max}`);
  return n;
}

function parseCoordPair(s) {
  const parts = String(s).split(',').map((v) => v.trim());
  if (parts.length !== 2) throw new Error(`Invalid coordinate "${s}" - expected "x,y"`);
  const x = parseInt(parts[0], 10);
  const y = parseInt(parts[1], 10);
  if (Number.isNaN(x) || Number.isNaN(y)) throw new Error(`Invalid coordinate "${s}" - expected integer "x,y"`);
  return { x, y };
}

function bresenham(x0, y0, x1, y1) {
  const points = [];
  let dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
  const sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
  let err = dx - dy;
  let cx = x0, cy = y0;
  for (;;) {
    points.push({ x: cx, y: cy });
    if (cx === x1 && cy === y1) break;
    const e2 = 2 * err;
    if (e2 > -dy) { err -= dy; cx += sx; }
    if (e2 < dx) { err += dx; cy += sy; }
  }
  return points;
}

function parseTilesArg(args) {
  const tiles = [];
  if (args.at) tiles.push(parseCoordPair(args.at));
  if (args.tiles) {
    for (const part of String(args.tiles).split(';')) {
      const p = part.trim();
      if (p) tiles.push(parseCoordPair(p));
    }
  }
  if (args.rect) {
    const nums = String(args.rect).split(',').map((v) => v.trim());
    if (nums.length !== 4) throw new Error(`Invalid --rect "${args.rect}" - expected "x1,y1,x2,y2"`);
    const a = parseCoordPair(`${nums[0]},${nums[1]}`);
    const b = parseCoordPair(`${nums[2]},${nums[3]}`);
    const [x1, x2] = [Math.min(a.x, b.x), Math.max(a.x, b.x)];
    const [y1, y2] = [Math.min(a.y, b.y), Math.max(a.y, b.y)];
    for (let y = y1; y <= y2; y++) for (let x = x1; x <= x2; x++) tiles.push({ x, y });
  }
  if (args.line) {
    const nums = String(args.line).split(',').map((v) => v.trim());
    if (nums.length !== 4) throw new Error(`Invalid --line "${args.line}" - expected "x1,y1,x2,y2"`);
    const a = parseCoordPair(`${nums[0]},${nums[1]}`);
    const b = parseCoordPair(`${nums[2]},${nums[3]}`);
    tiles.push(...bresenham(a.x, a.y, b.x, b.y));
  }
  const seen = new Set();
  const deduped = [];
  for (const t of tiles) {
    const key = `${t.x},${t.y}`;
    if (!seen.has(key)) { seen.add(key); deduped.push(t); }
  }
  if (deduped.length === 0) {
    throw new Error('No tile selector given. Use --at x,y | --tiles x,y;x,y | --rect x1,y1,x2,y2 | --line x1,y1,x2,y2');
  }
  return deduped;
}

function slug(name) {
  return String(name).toLowerCase().replace(/[^\w\u4e00-\u9fa5]+/g, '-').replace(/^-+|-+$/g, '') || 'city';
}

function fmtMoney(n) {
  return `$${Math.round(n).toLocaleString('en-US')}`;
}

function applyTileOps(state, tiles, { cost = 0, free = false, op }) {
  const grid = cloneGrid(state.grid);
  let okCount = 0;
  let spent = 0;
  const failures = [];
  for (const { x, y } of tiles) {
    if (!inBounds(state, x, y)) {
      failures.push(`(${x},${y}) is out of bounds (grid is ${state.gridSize}x${state.gridSize})`);
      continue;
    }
    if (!free && cost > 0 && state.stats.money - spent < cost) {
      failures.push(`(${x},${y}) insufficient funds (${fmtMoney(state.stats.money - spent)} left, need ${fmtMoney(cost)})`);
      continue;
    }
    const r = op(grid, state.gridSize, x, y);
    if (!r.ok) {
      failures.push(r.reason);
      continue;
    }
    okCount++;
    if (!free && cost > 0) spent += cost;
  }
  state.grid = grid;
  state.stats.money -= spent;
  return { okCount, spent, failures };
}

function reportEdit(label, result, file, changed) {
  console.log(`${label}: ${result.okCount} tile(s) ok${result.spent > 0 ? `, spent ${fmtMoney(result.spent)}` : ''}`);
  if (result.failures.length > 0) {
    console.log(`Failures (${result.failures.length}):`);
    for (const f of result.failures) console.log(`  - ${f}`);
  }
  if (changed && result.okCount > 0) {
    saveStateFile(file, result.state);
    console.log(`Saved: ${file} (backup: ${file}.bak)`);
  }
}

// ---------------------------------------------------------------- commands

async function cmdNew(args) {
  const gridSize = args.grid !== undefined ? parseIntArg(args.grid, 'grid', { min: 20, max: 150 }) : 60;
  let name = String(args.name || 'New City');
  const money = args.money !== undefined ? Number(args.money) : 100000;
  if (Number.isNaN(money)) throw new Error(`Invalid --money: "${args.money}"`);
  const seed = args.seed !== undefined ? parseIntArg(args.seed, 'seed') : 42;

  const wantsOsm = Boolean(args.osm || args.place || (args.lat !== undefined && args.lon !== undefined));
  let grid, waterBodies = [], genInfo = 'blank flat grass';

  let baiduAk = '';
  if (args.ak !== undefined) {
    if (typeof args.ak !== 'string') {
      throw new Error('--ak requires a value: your Baidu server-side AK (or set BAIDU_MAP_AK)');
    }
    baiduAk = args.ak;
  } else if (process.env.BAIDU_MAP_AK) {
    baiduAk = process.env.BAIDU_MAP_AK;
  }

  if (wantsOsm) {
    const radius = args.radius !== undefined ? Number(args.radius) : 800;
    if (Number.isNaN(radius) || radius < 50 || radius > 10000) throw new Error('--radius must be 50-10000 meters');
    let geo;
    if (args.place) {
      const via = baiduAk ? 'Baidu Maps' : 'Nominatim (pass --ak or set BAIDU_MAP_AK for Baidu geocoding)';
      process.stderr.write(`Geocoding "${args.place}" via ${via}...\n`);
      geo = await geocodePlace(String(args.place), { ak: baiduAk, radius });
      process.stderr.write(`Found: ${geo.displayName}\n`);
      if (geo.coordNote) process.stderr.write(`${geo.coordNote}\n`);
      if (!args.name) name = String(args.place);
    } else {
      const lat = Number(args.lat), lon = Number(args.lon);
      if (Number.isNaN(lat) || Number.isNaN(lon)) throw new Error('--lat and --lon must be numbers');
      const coordSys = args['coord-sys'] !== undefined ? String(args['coord-sys']) : 'wgs84';
      const wgs = toWgs84(lat, lon, coordSys);
      if (coordSys !== 'wgs84') {
        const off = haversineMeters(lat, lon, wgs.lat, wgs.lon);
        process.stderr.write(
          `Input ${coordSys} (${lat},${lon}) -> WGS-84 (${wgs.lat.toFixed(6)},${wgs.lon.toFixed(6)}), corrected ~${Math.round(off)}m\n`
        );
      }
      geo = {
        lat: wgs.lat, lon: wgs.lon,
        displayName: `${lat}, ${lon}${coordSys !== 'wgs84' ? ` (${coordSys})` : ''}`,
        bbox: bboxFromCenter(wgs.lat, wgs.lon, radius),
        polygons: [],
      };
    }
    process.stderr.write(`Fetching OSM data (${geo.bbox.minLat.toFixed(4)},${geo.bbox.minLon.toFixed(4)} to ${geo.bbox.maxLat.toFixed(4)},${geo.bbox.maxLon.toFixed(4)})...\n`);
    const osm = await fetchOverpass(geo.bbox);
    const elementCount = osm.elements?.length || 0;
    process.stderr.write(`Got ${elementCount} OSM elements, rasterizing to ${gridSize}x${gridSize} grid...\n`);
    const r = rasterizeOsm(osm, {
      gridSize,
      region: { polygons: geo.polygons },
      bbox: geo.bbox,
      centerLat: geo.lat,
      centerLon: geo.lon,
      seed,
    });
    grid = r.grid;
    waterBodies = r.waterBodies;
    genInfo = `OSM (${geo.displayName}) - 1 tile ~ ${r.stats.oneTileM.toFixed(0)}m, ` +
      `water ${r.stats.waterCells}, road ${r.stats.roadCells}, buildings ${r.stats.buildingCount} (${r.stats.buildingCells} tiles), ` +
      `trees ${r.stats.treeCells}, sport ${r.stats.sportCount}`;
  } else if (args.random) {
    const r = generateRandomTerrain(gridSize, seed);
    grid = r.grid;
    waterBodies = r.waterBodies;
    genInfo = `random terrain (seed ${seed}) - water ${r.stats.waterCells}, trees ${r.stats.treeCells}, lakes ${r.stats.waterBodyCount}`;
  } else {
    grid = blankGrid(gridSize);
  }

  const state = createStateShell({ grid, gridSize, cityName: name, money, waterBodies });
  const finalOut = args.out || path.join('cities', `${slug(name)}.isocity.json`);
  saveStateFile(finalOut, state, { backup: false });
  console.log(`Created: ${finalOut}`);
  console.log(`City: ${name} | grid ${gridSize}x${gridSize} | money ${fmtMoney(money)}`);
  console.log(`Terrain: ${genInfo}`);
  console.log(`Next: node cli/isocity.mjs map ${finalOut}`);
}

function cmdInfo(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: info <file>');
  console.log(infoText(loadStateFile(file)));
}

function cmdMap(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: map <file>');
  console.log(asciiMap(loadStateFile(file), { legend: !args['no-legend'] }));
}

function cmdGet(args) {
  const file = args._[0];
  if (!file || args._.length < 3) throw new Error('Usage: get <file> <x> <y>');
  const x = parseInt(args._[1], 10), y = parseInt(args._[2], 10);
  if (Number.isNaN(x) || Number.isNaN(y)) throw new Error('x and y must be integers');
  console.log(tileDetailText(loadStateFile(file), x, y));
}

function cmdBuildings() {
  console.log('Building types (size, placement cost):');
  for (const type of BUILDING_TYPES) {
    if (type === 'empty') continue;
    const size = getBuildingSize(type);
    const dims = size.width > 1 || size.height > 1 ? `${size.width}x${size.height}` : '1x1';
    let costStr;
    if (PLACE_COSTS[type] !== undefined) costStr = fmtMoney(PLACE_COSTS[type]);
    else if (GROWABLE_TYPES.includes(type)) costStr = 'free (grows on zoned land)';
    else if (type === 'grass') costStr = 'terrain (bulldoze restores grass)';
    else if (type === 'water') costStr = 'terrain (use: terraform water)';
    else if (type === 'bridge') costStr = 'auto (road over water becomes bridge)';
    else costStr = '-';
    console.log(`  ${type.padEnd(24)} ${dims.padEnd(5)} ${costStr}`);
  }
}

function cmdPlace(args) {
  const file = args._[0];
  const type = args._[1];
  if (!file || !type) throw new Error('Usage: place <file> <buildingType> (--at|--tiles|--rect|--line ...)');
  if (!BUILDING_TYPES.includes(type) || type === 'empty') {
    throw new Error(`Unknown building type "${type}". Run "buildings" to list valid types.`);
  }
  const tiles = parseTilesArg(args);
  const state = loadStateFile(file);
  const cost = PLACE_COSTS[type] ?? 0;
  const result = applyTileOps(state, tiles, {
    cost,
    free: Boolean(args.free),
    op: (grid, size, x, y) => rules.tryPlace(grid, size, x, y, type, null),
  });
  reportEdit(`Placed ${type}`, { ...result, state }, file, result.okCount > 0);
}

function cmdBulldoze(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: bulldoze <file> (--at|--tiles|--rect|--line ...)');
  const tiles = parseTilesArg(args);
  const state = loadStateFile(file);
  const result = applyTileOps(state, tiles, {
    cost: BULLDOZE_COST,
    free: Boolean(args.free),
    op: (grid, size, x, y) => rules.tryBulldoze(grid, size, x, y),
  });
  reportEdit('Bulldozed', { ...result, state }, file, result.okCount > 0);
}

function cmdZone(args) {
  const file = args._[0];
  const zone = args._[1];
  if (!file || !zone) throw new Error('Usage: zone <file> <residential|commercial|industrial|none> (--at|--tiles|--rect)');
  if (!ZONE_TYPES.includes(zone)) throw new Error(`Unknown zone "${zone}" - use residential|commercial|industrial|none`);
  const tiles = parseTilesArg(args);
  const state = loadStateFile(file);
  const result = applyTileOps(state, tiles, {
    cost: zone === 'none' ? 0 : ZONE_COST,
    free: Boolean(args.free),
    op: (grid, size, x, y) => rules.tryPlace(grid, size, x, y, null, zone),
  });
  reportEdit(`Zoned ${zone}`, { ...result, state }, file, result.okCount > 0);
}

function cmdTerraform(args) {
  const file = args._[0];
  const kind = args._[1];
  if (!file || !kind) throw new Error('Usage: terraform <file> <water|land|tree> (--at|--tiles|--rect)');
  if (!['water', 'land', 'tree'].includes(kind)) throw new Error(`Unknown terraform kind "${kind}" - use water|land|tree`);
  const tiles = parseTilesArg(args);
  const state = loadStateFile(file);
  const ops = {
    water: { cost: TERRAFORM_COST, op: (g, s, x, y) => rules.tryTerraformWater(g, s, x, y) },
    land: { cost: TERRAFORM_COST, op: (g, s, x, y) => rules.tryTerraformLand(g, s, x, y) },
    tree: { cost: PLACE_COSTS.tree, op: (g, s, x, y) => rules.tryPlace(g, s, x, y, 'tree', null) },
  };
  const { cost, op } = ops[kind];
  const result = applyTileOps(state, tiles, { cost, free: Boolean(args.free), op });
  reportEdit(`Terraformed ${kind}`, { ...result, state }, file, result.okCount > 0);
}

function cmdTax(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: tax <file> [rate]');
  const state = loadStateFile(file);
  if (args._.length >= 2) {
    const rate = Number(args._[1]);
    if (Number.isNaN(rate) || rate < 0 || rate > 100) throw new Error('Tax rate must be a number 0-100');
    state.taxRate = rate;
    saveStateFile(file, state);
    console.log(`Tax rate set to ${rate}% (effective ${state.effectiveTaxRate}% - takes effect over time)`);
    console.log(`Saved: ${file} (backup: ${file}.bak)`);
  } else {
    console.log(`Tax rate: ${state.taxRate}% (effective ${state.effectiveTaxRate ?? state.taxRate}%)`);
  }
}

const BUDGET_KEYS = ['police', 'fire', 'health', 'education', 'transportation', 'parks', 'power', 'water'];

function cmdBudget(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: budget <file> [key] [funding]');
  const state = loadStateFile(file);
  if (args._.length >= 3) {
    const key = args._[1];
    const funding = Number(args._[2]);
    if (!BUDGET_KEYS.includes(key)) throw new Error(`Unknown budget key "${key}" - use: ${BUDGET_KEYS.join(' ')}`);
    if (Number.isNaN(funding) || funding < 0 || funding > 100) throw new Error('Funding must be 0-100');
    state.budget[key].funding = funding;
    saveStateFile(file, state);
    console.log(`Budget ${key} funding set to ${funding}%`);
    console.log(`Saved: ${file} (backup: ${file}.bak)`);
  } else {
    console.log('Budget (funding % / monthly cost):');
    for (const key of BUDGET_KEYS) {
      const b = state.budget[key];
      console.log(`  ${key.padEnd(16)} ${String(b.funding).padStart(3)}%  ${fmtMoney(b.cost)}`);
    }
    if (args._.length === 2) {
      const key = args._[1];
      if (!BUDGET_KEYS.includes(key)) throw new Error(`Unknown budget key "${key}" - use: ${BUDGET_KEYS.join(' ')}`);
    }
  }
}

function cmdMoney(args) {
  const file = args._[0];
  const amountStr = args._[1];
  if (!file || amountStr === undefined) throw new Error('Usage: money <file> <amount|+amount|-amount>');
  const state = loadStateFile(file);
  if (String(amountStr).startsWith('+') || String(amountStr).startsWith('-')) {
    const delta = Number(amountStr);
    if (Number.isNaN(delta)) throw new Error(`Invalid amount "${amountStr}"`);
    state.stats.money = Math.max(0, state.stats.money + delta);
    console.log(`Money: ${fmtMoney(state.stats.money)} (${delta >= 0 ? '+' : ''}${fmtMoney(delta)})`);
  } else {
    const amount = Number(amountStr);
    if (Number.isNaN(amount) || amount < 0) throw new Error('Amount must be a non-negative number');
    state.stats.money = amount;
    console.log(`Money set to ${fmtMoney(amount)}`);
  }
  saveStateFile(file, state);
  console.log(`Saved: ${file} (backup: ${file}.bak)`);
}

// Print the classic long share URL (/c/<name>#s=<data>) plus the truncation
// note for very large cities. Shared by the no-flag path (zero regression)
// and the --short failure fallback.
function printLongShareLink(state, baseUrl) {
  const url = createShareUrl(state, baseUrl);
  console.log(url);
  if (url.length > 30000) {
    console.log(`\nNote: this URL is ${url.length} characters long - some chat apps may truncate it.`);
    console.log('For very large cities, share the .isocity.json file instead (Settings > Import from File).');
  }
  return url;
}

async function cmdShare(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: share <file> [--url BASE] [--short] [--gallery] [--api-base URL] [--anon-key KEY]');
  const state = loadStateFile(file);
  const baseUrl = typeof args.url === 'string' ? args.url : `${ONLINE_GAME_URL}/`;

  // No flags: legacy long-link behavior, byte-identical output (FR-013).
  if (!args.short) {
    printLongShareLink(state, baseUrl);
    return;
  }

  // --short: upload an immutable snapshot, print a /city/<code> link.
  try {
    const { url } = await createShortLink({
      state,
      isPublic: Boolean(args.gallery),
      apiBase: typeof args['api-base'] === 'string' ? args['api-base'] : undefined,
      anonKey: typeof args['anon-key'] === 'string' ? args['anon-key'] : undefined,
      webBase: baseUrl,
    });
    console.log(url);
    console.log(args.gallery
      ? 'Gallery: publicly listed on the homepage hot maps (热门地图).'
      : 'Gallery: not listed - add --gallery to feature this map on the homepage hot maps.');
  } catch (e) {
    if (e instanceof SnapshotTooLargeError) {
      // Too large for any URL-based sharing - refuse with the file-exchange hint.
      console.error(`Error: ${e.message}`);
      process.exitCode = 1;
      return;
    }
    // Network/server failure: report clearly, then auto-fallback to the long
    // link so the command still hands the agent something usable.
    // (Set exitCode rather than process.exit(): hard-exiting while undici
    // sockets are still open crashes Node on Windows.)
    console.error(`Error: short-link sharing failed (${e.message})`);
    console.error('Falling back to the long share URL:');
    printLongShareLink(state, baseUrl);
    process.exitCode = 1;
  }
}

async function cmdScreenshot(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: screenshot <file> [-o out.png] [--url URL] [--wait MS] [--zoom-out N]');
  const state = loadStateFile(file);
  const out = args.out || `${file.replace(/\.json$/i, '')}.png`;
  const url = typeof args.url === 'string' ? args.url : DEFAULT_GAME_URL;
  const waitMs = args.wait !== undefined ? parseIntArg(args.wait, 'wait', { min: 0, max: 60000 }) : 5000;
  const width = args.width !== undefined ? parseIntArg(args.width, 'width', { min: 400, max: 3840 }) : 1600;
  const height = args.height !== undefined ? parseIntArg(args.height, 'height', { min: 300, max: 2160 }) : 900;
  const zoomOut = args['zoom-out'] !== undefined ? parseIntArg(args['zoom-out'], 'zoom-out', { min: 0, max: 40 }) : 10;
  process.stderr.write(`Opening ${url} in headless Chromium...\n`);
  await screenshotState({ state, url, out, width, height, waitMs, zoomOut });
  console.log(`Screenshot saved: ${out}`);
}

async function cmdSimulate(args) {
  const file = args._[0];
  if (!file) throw new Error('Usage: simulate <file> --ticks N [-o out.json] [--url URL]');
  const state = loadStateFile(file);
  const ticks = args.ticks !== undefined ? parseIntArg(args.ticks, 'ticks', { min: 1, max: 5000 }) : 100;
  const out = args.out || file;
  const url = typeof args.url === 'string' ? args.url : DEFAULT_GAME_URL;
  process.stderr.write(`Opening ${url} in headless Chromium, running ${ticks} tick(s)...\n`);
  const result = await simulateTicks({ state, url, ticks });
  saveStateFile(out, result);
  console.log(`Simulated ${ticks} tick(s): ${result.year}-${String(result.month).padStart(2, '0')}-${String(result.day).padStart(2, '0')}, ` +
    `population ${result.stats.population.toLocaleString('en-US')}, money ${fmtMoney(result.stats.money)}`);
  console.log(`Saved: ${out}${out === file ? ' (backup: ' + file + '.bak)' : ''}`);
}

// ---------------------------------------------------------------- main

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  if (!command || command === 'help' || command === '--help' || command === '-h') {
    console.log(USAGE);
    return;
  }
  const args = parseArgs(rest);
  switch (command) {
    case 'new': return cmdNew(args);
    case 'info': return cmdInfo(args);
    case 'map': return cmdMap(args);
    case 'get': return cmdGet(args);
    case 'buildings': return cmdBuildings();
    case 'place': return cmdPlace(args);
    case 'bulldoze': return cmdBulldoze(args);
    case 'zone': return cmdZone(args);
    case 'terraform': return cmdTerraform(args);
    case 'tax': return cmdTax(args);
    case 'budget': return cmdBudget(args);
    case 'money': return cmdMoney(args);
    case 'share': return cmdShare(args);
    case 'screenshot': return cmdScreenshot(args);
    case 'simulate': return cmdSimulate(args);
    default:
      throw new Error(`Unknown command "${command}". Run without arguments for usage.`);
  }
}

main().catch((e) => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
