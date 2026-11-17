// IsoCity CLI - text rendering of game state (ASCII map, info summary, tile detail)
import { GROWABLE_TYPES, PARK_TYPES, getBuildingSize } from './gamestate.mjs';

const SERVICE_TYPES = new Set([
  'police_station', 'fire_station', 'hospital', 'school', 'university',
  'power_plant', 'water_tower', 'subway_station', 'rail_station',
  'stadium', 'museum', 'airport', 'space_program', 'city_hall', 'amusement_park',
  'marina_docks_small', 'pier_large', 'roller_coaster_small', 'office_building_small',
]);

const GROWABLE = new Set(GROWABLE_TYPES);
const PARKS = new Set(PARK_TYPES);

export function tileChar(tile) {
  const t = tile.building.type;
  switch (t) {
    case 'water': return '~';
    case 'road': return '#';
    case 'bridge': return '=';
    case 'rail': return 'x';
    case 'tree': return 'T';
    case 'grass':
    case 'empty': break;
    default:
      if (GROWABLE.has(t)) return 'B';
      if (PARKS.has(t)) return 'P';
      if (SERVICE_TYPES.has(t)) return 'S';
      return '?';
  }
  if (t === 'empty') return "'";
  if (tile.zone === 'residential') return 'r';
  if (tile.zone === 'commercial') return 'c';
  if (tile.zone === 'industrial') return 'i';
  return '.';
}

export function asciiMap(state, { legend = true } = {}) {
  const lines = [];
  if (legend) {
    lines.push('Legend: ~ water | # road | = bridge | x rail | T tree | . grass | \' multi-tile part');
    lines.push('        r/c/i zoned land | B growable bldg | P park/recreation | S service/special');
    lines.push(`Grid: ${state.gridSize}x${state.gridSize} (row = y from north, col = x from west)`);
    lines.push('');
  }
  const width = String(state.gridSize - 1).length;
  const header = ' '.repeat(width + 1) + Array.from({ length: state.gridSize }, (_, x) =>
    x % 10 === 0 ? '|' : (x % 5 === 0 ? '+' : ' ')).join('');
  lines.push(header);
  for (let y = 0; y < state.gridSize; y++) {
    let row = String(y).padStart(width, ' ') + ' ';
    for (let x = 0; x < state.gridSize; x++) {
      row += tileChar(state.grid[y][x]);
    }
    lines.push(row);
  }
  return lines.join('\n');
}

export function countBuildings(state) {
  const counts = new Map();
  let zoneCounts = { none: 0, residential: 0, commercial: 0, industrial: 0 };
  let water = 0, road = 0, rail = 0, tree = 0, grass = 0;
  let powered = 0, watered = 0, constructed = 0, totalBuildings = 0;

  for (const row of state.grid) {
    for (const tile of row) {
      const t = tile.building.type;
      zoneCounts[tile.zone] = (zoneCounts[tile.zone] || 0) + 1;
      if (t === 'water') water++;
      else if (t === 'road') road++;
      else if (t === 'bridge') road++;
      else if (t === 'rail') rail++;
      else if (t === 'tree') tree++;
      else if (t === 'grass' || t === 'empty') grass++;
      else {
        totalBuildings++;
        counts.set(t, (counts.get(t) || 0) + 1);
        if (tile.building.powered) powered++;
        if (tile.building.watered) watered++;
        if ((tile.building.constructionProgress ?? 100) >= 100) constructed++;
      }
    }
  }
  return { counts, zoneCounts, water, road, rail, tree, grass, powered, watered, constructed, totalBuildings };
}

function fmtMoney(n) {
  return `$${Math.round(n).toLocaleString('en-US')}`;
}

export function infoText(state) {
  const c = countBuildings(state);
  const lines = [];
  lines.push(`City:          ${state.cityName}`);
  lines.push(`Grid:          ${state.gridSize} x ${state.gridSize}`);
  lines.push(`Date:          ${state.year}-${String(state.month).padStart(2, '0')}-${String(state.day).padStart(2, '0')} ${String(state.hour).padStart(2, '0')}:00 (tick ${state.tick}, speed ${state.speed})`);
  lines.push(`Money:         ${fmtMoney(state.stats.money)}  (income ${fmtMoney(state.stats.income)} / expenses ${fmtMoney(state.stats.expenses)})`);
  lines.push(`Population:    ${state.stats.population.toLocaleString('en-US')}`);
  lines.push(`Jobs:          ${state.stats.jobs.toLocaleString('en-US')}`);
  lines.push(`Happiness:     ${state.stats.happiness}  health ${state.stats.health}  education ${state.stats.education}  safety ${state.stats.safety}  environment ${state.stats.environment}`);
  lines.push(`Tax rate:      ${state.taxRate}% (effective ${state.effectiveTaxRate ?? state.taxRate}%)`);
  lines.push(`Demand:        R ${state.stats.demand?.residential} / C ${state.stats.demand?.commercial} / I ${state.stats.demand?.industrial}`);
  lines.push('');
  lines.push(`Terrain:       water ${c.water} | road/bridge ${c.road} | rail ${c.rail} | tree ${c.tree} | open land ${c.grass}`);
  lines.push(`Zoned land:    residential ${c.zoneCounts.residential} | commercial ${c.zoneCounts.commercial} | industrial ${c.zoneCounts.industrial}`);
  lines.push(`Buildings:     ${c.totalBuildings} total (${c.constructed} complete, ${c.powered} powered, ${c.watered} watered)`);
  const sorted = [...c.counts.entries()].sort((a, b) => b[1] - a[1]);
  if (sorted.length > 0) {
    lines.push('');
    lines.push('Building breakdown:');
    for (const [type, count] of sorted) {
      const size = getBuildingSize(type);
      const dims = size.width > 1 || size.height > 1 ? ` [${size.width}x${size.height}]` : '';
      lines.push(`  ${type}${dims}: ${count}`);
    }
  }
  if (state.waterBodies?.length) {
    lines.push('');
    lines.push(`Water bodies:  ${state.waterBodies.map((w) => `${w.name || w.type}(${w.tiles.length})`).join(', ')}`);
  }
  if (state.cities?.length) {
    lines.push(`City zones:    ${state.cities.map((ct) => `${ct.name} [${ct.bounds.minX},${ct.bounds.minY}..${ct.bounds.maxX},${ct.bounds.maxY}]`).join(' | ')}`);
  }
  return lines.join('\n');
}

export function tileDetailText(state, x, y) {
  const tile = state.grid[y]?.[x];
  if (!tile) return `Tile (${x},${y}) is out of bounds (grid is ${state.gridSize}x${state.gridSize})`;
  const lines = [];
  lines.push(`Tile (${x},${y}):`);
  lines.push(JSON.stringify(tile, null, 2));
  const t = tile.building.type;
  const size = getBuildingSize(t);
  if (size.width > 1 || size.height > 1) {
    lines.push(`Note: "${t}" is a ${size.width}x${size.height} building anchored at this tile.`);
  }
  return lines.join('\n');
}
