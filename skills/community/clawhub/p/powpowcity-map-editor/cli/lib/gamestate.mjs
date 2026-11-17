// IsoCity CLI - game state model.
// Constants mirror src/lib/shareState.ts, src/lib/simulation.ts and
// src/games/isocity/types/buildings.ts - keep in sync with those files.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export const BUILDING_TYPES = [
  'empty', 'grass', 'water', 'road', 'bridge', 'rail', 'tree',
  'house_small', 'house_medium', 'mansion', 'apartment_low', 'apartment_high',
  'shop_small', 'shop_medium', 'office_low', 'office_high', 'mall',
  'factory_small', 'factory_medium', 'factory_large', 'warehouse',
  'police_station', 'fire_station', 'hospital', 'school', 'university',
  'park', 'park_large', 'tennis', 'power_plant', 'water_tower', 'subway_station',
  'rail_station', 'stadium', 'museum', 'airport', 'space_program', 'city_hall', 'amusement_park',
  'basketball_courts', 'playground_small', 'playground_large', 'baseball_field_small',
  'soccer_field_small', 'football_field', 'baseball_stadium', 'community_center',
  'office_building_small', 'swimming_pool', 'skate_park', 'mini_golf_course',
  'bleachers_field', 'go_kart_track', 'amphitheater', 'greenhouse_garden',
  'animal_pens_farm', 'cabin_house', 'campground', 'marina_docks_small', 'pier_large',
  'roller_coaster_small', 'community_garden', 'pond_park', 'park_gate',
  'mountain_lodge', 'mountain_trailhead',
];

export const ZONE_TYPES = ['none', 'residential', 'commercial', 'industrial'];

export const TERRAIN_TYPES = ['empty', 'grass', 'water', 'road', 'bridge', 'rail', 'tree'];

export const GROWABLE_TYPES = [
  'house_small', 'house_medium', 'mansion', 'apartment_low', 'apartment_high',
  'shop_small', 'shop_medium', 'office_low', 'office_high', 'mall',
  'factory_small', 'factory_medium', 'factory_large', 'warehouse',
];

export const PARK_TYPES = [
  'park', 'park_large', 'tennis', 'basketball_courts', 'playground_small', 'playground_large',
  'baseball_field_small', 'soccer_field_small', 'football_field', 'baseball_stadium',
  'community_center', 'swimming_pool', 'skate_park', 'mini_golf_course', 'bleachers_field',
  'go_kart_track', 'amphitheater', 'greenhouse_garden', 'animal_pens_farm', 'cabin_house',
  'campground', 'community_garden', 'pond_park', 'park_gate', 'mountain_lodge', 'mountain_trailhead',
];

// width x height footprint per building (simulation.ts BUILDING_SIZES)
export const BUILDING_SIZES = {
  power_plant: { width: 2, height: 2 },
  hospital: { width: 2, height: 2 },
  school: { width: 2, height: 2 },
  stadium: { width: 3, height: 3 },
  museum: { width: 3, height: 3 },
  university: { width: 3, height: 3 },
  airport: { width: 4, height: 4 },
  space_program: { width: 3, height: 3 },
  park_large: { width: 3, height: 3 },
  mansion: { width: 2, height: 2 },
  apartment_low: { width: 2, height: 2 },
  apartment_high: { width: 2, height: 2 },
  office_low: { width: 2, height: 2 },
  office_high: { width: 2, height: 2 },
  mall: { width: 3, height: 3 },
  factory_medium: { width: 2, height: 2 },
  factory_large: { width: 3, height: 3 },
  warehouse: { width: 2, height: 2 },
  city_hall: { width: 2, height: 2 },
  amusement_park: { width: 4, height: 4 },
  playground_large: { width: 2, height: 2 },
  baseball_field_small: { width: 2, height: 2 },
  football_field: { width: 2, height: 2 },
  baseball_stadium: { width: 3, height: 3 },
  mini_golf_course: { width: 2, height: 2 },
  go_kart_track: { width: 2, height: 2 },
  amphitheater: { width: 2, height: 2 },
  greenhouse_garden: { width: 2, height: 2 },
  marina_docks_small: { width: 2, height: 2 },
  roller_coaster_small: { width: 2, height: 2 },
  mountain_lodge: { width: 2, height: 2 },
  mountain_trailhead: { width: 3, height: 3 },
  rail_station: { width: 2, height: 2 },
};

export function getBuildingSize(buildingType) {
  return BUILDING_SIZES[buildingType] || { width: 1, height: 1 };
}

// Placement costs (game.ts TOOL_INFO). Zoned growable buildings grow for free.
export const PLACE_COSTS = {
  road: 25,
  rail: 40,
  tree: 15,
  police_station: 500,
  fire_station: 500,
  hospital: 1000,
  school: 400,
  university: 2000,
  park: 150,
  park_large: 600,
  tennis: 200,
  power_plant: 3000,
  water_tower: 1000,
  subway_station: 750,
  rail_station: 1000,
  stadium: 5000,
  museum: 4000,
  airport: 10000,
  space_program: 15000,
  city_hall: 6000,
  amusement_park: 12000,
  basketball_courts: 250,
  playground_small: 200,
  playground_large: 350,
  baseball_field_small: 800,
  soccer_field_small: 400,
  football_field: 1200,
  baseball_stadium: 6000,
  community_center: 500,
  office_building_small: 600,
  swimming_pool: 450,
  skate_park: 300,
  mini_golf_course: 700,
  bleachers_field: 350,
  go_kart_track: 1000,
  amphitheater: 1500,
  greenhouse_garden: 800,
  animal_pens_farm: 400,
  cabin_house: 300,
  campground: 250,
  marina_docks_small: 1200,
  pier_large: 600,
  roller_coaster_small: 3000,
  community_garden: 200,
  pond_park: 350,
  park_gate: 150,
  mountain_lodge: 1500,
  mountain_trailhead: 400,
};

export const BULLDOZE_COST = 10;
export const ZONE_COST = 50;
export const TERRAFORM_COST = 50000;
export const WATERFRONT_BUILDINGS = ['marina_docks_small', 'pier_large'];

const NO_CONSTRUCTION_TYPES = new Set(['grass', 'empty', 'water', 'road', 'bridge', 'tree']);

export function uuid() {
  return crypto.randomUUID();
}

export function createBuilding(type) {
  return {
    type,
    level: type === 'grass' || type === 'empty' || type === 'water' ? 0 : 1,
    population: 0,
    jobs: 0,
    powered: false,
    watered: false,
    onFire: false,
    fireProgress: 0,
    age: 0,
    constructionProgress: NO_CONSTRUCTION_TYPES.has(type) ? 100 : 0,
    abandoned: false,
  };
}

export function createTile(x, y, type = 'grass', landValue = 50) {
  return {
    x,
    y,
    zone: 'none',
    building: createBuilding(type),
    landValue,
    pollution: 0,
    crime: 0,
    traffic: 0,
    hasSubway: false,
  };
}

export function blankGrid(size) {
  const grid = [];
  for (let y = 0; y < size; y++) {
    const row = [];
    for (let x = 0; x < size; x++) row.push(createTile(x, y));
    grid.push(row);
  }
  return grid;
}

function numGrid(size) {
  return Array.from({ length: size }, () => new Array(size).fill(0));
}

function boolGrid(size) {
  return Array.from({ length: size }, () => new Array(size).fill(false));
}

export function createStateShell({ grid, gridSize, cityName, money = 100000, waterBodies = [] }) {
  return {
    id: uuid(),
    grid,
    gridSize,
    cityName,
    year: 2024, month: 1, day: 1, hour: 12, tick: 0,
    speed: 1,
    selectedTool: 'select',
    taxRate: 9,
    effectiveTaxRate: 9,
    stats: {
      population: 0, jobs: 0, money, income: 0, expenses: 0,
      happiness: 50, health: 50, education: 50, safety: 50, environment: 75,
      demand: { residential: 50, commercial: 30, industrial: 40 },
    },
    budget: {
      police: { name: 'Police', funding: 100, cost: 0 },
      fire: { name: 'Fire', funding: 100, cost: 0 },
      health: { name: 'Health', funding: 100, cost: 0 },
      education: { name: 'Education', funding: 100, cost: 0 },
      transportation: { name: 'Transportation', funding: 100, cost: 0 },
      parks: { name: 'Parks', funding: 100, cost: 0 },
      power: { name: 'Power', funding: 100, cost: 0 },
      water: { name: 'Water', funding: 100, cost: 0 },
    },
    services: { police: numGrid(gridSize), fire: numGrid(gridSize), health: numGrid(gridSize), education: numGrid(gridSize), power: boolGrid(gridSize), water: boolGrid(gridSize) },
    notifications: [],
    advisorMessages: [],
    history: [],
    activePanel: 'none',
    disastersEnabled: true,
    adjacentCities: [],
    waterBodies,
    gameVersion: 0,
    cities: [{
      id: uuid(),
      name: cityName,
      bounds: { minX: 0, minY: 0, maxX: gridSize - 1, maxY: gridSize - 1 },
      economy: { population: 0, jobs: 0, income: 0, expenses: 0, happiness: 50, lastCalculated: 0 },
      color: '#3b82f6',
    }],
  };
}

export function validateState(state, sourceLabel = 'state') {
  const fail = (msg) => {
    throw new Error(`Invalid ${sourceLabel}: ${msg}`);
  };
  if (!state || typeof state !== 'object') fail('not a JSON object');
  if (!Array.isArray(state.grid)) fail('missing grid array');
  if (typeof state.gridSize !== 'number') fail('missing gridSize number');
  if (state.grid.length !== state.gridSize) fail(`grid rows (${state.grid.length}) != gridSize (${state.gridSize})`);
  for (let y = 0; y < state.grid.length; y++) {
    const row = state.grid[y];
    if (!Array.isArray(row)) fail(`grid row ${y} is not an array`);
    if (row.length !== state.gridSize) fail(`grid row ${y} length ${row.length} != gridSize ${state.gridSize}`);
    for (let x = 0; x < row.length; x++) {
      const t = row[x];
      if (!t || typeof t !== 'object') fail(`tile ${x},${y} is not an object`);
      if (!t.building || typeof t.building.type !== 'string') fail(`tile ${x},${y} missing building.type`);
      if (!BUILDING_TYPES.includes(t.building.type)) fail(`tile ${x},${y} has unknown building type "${t.building.type}"`);
      if (t.zone && !ZONE_TYPES.includes(t.zone)) fail(`tile ${x},${y} has unknown zone "${t.zone}"`);
    }
  }
  if (!state.stats || typeof state.stats.money !== 'number') fail('missing stats.money');
  return true;
}

// Mirrors the migrations in GameContext.loadState so older saves stay loadable
export function migrateState(state) {
  if (!state.adjacentCities) state.adjacentCities = [];
  for (const city of state.adjacentCities) {
    if (city.discovered === undefined) city.discovered = true;
  }
  if (!state.waterBodies) state.waterBodies = [];
  if (!state.cities) {
    state.cities = [{
      id: state.id || 'default-city',
      name: state.cityName || 'City',
      bounds: { minX: 0, minY: 0, maxX: (state.gridSize || 50) - 1, maxY: (state.gridSize || 50) - 1 },
      economy: { population: state.stats?.population || 0, jobs: state.stats?.jobs || 0, income: 0, expenses: 0, happiness: 50, lastCalculated: 0 },
      color: '#3b82f6',
    }];
  }
  if (state.effectiveTaxRate === undefined) state.effectiveTaxRate = state.taxRate ?? 9;
  for (let y = 0; y < state.grid.length; y++) {
    for (let x = 0; x < state.grid[y].length; x++) {
      const b = state.grid[y][x]?.building;
      if (b) {
        if (b.constructionProgress === undefined) b.constructionProgress = 100;
        if (b.abandoned === undefined) b.abandoned = false;
      }
    }
  }
  return state;
}

export function loadStateFile(file) {
  if (!fs.existsSync(file)) {
    throw new Error(`File not found: ${file}`);
  }
  let state;
  try {
    state = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    throw new Error(`${file} is not valid JSON: ${e.message}`);
  }
  validateState(state, file);
  migrateState(state);
  return state;
}

export function saveStateFile(file, state, { backup = true } = {}) {
  const dir = path.dirname(file);
  if (dir && !fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  if (backup && fs.existsSync(file)) {
    fs.copyFileSync(file, `${file}.bak`);
  }
  fs.writeFileSync(file, JSON.stringify(state));
}

// Deep-copy the grid once per command run; rules.mjs mutates this copy in place
export function cloneGrid(grid) {
  return grid.map((row) => row.map((t) => ({ ...t, building: { ...t.building } })));
}

export function inBounds(state, x, y) {
  return Number.isInteger(x) && Number.isInteger(y) && x >= 0 && y >= 0 && x < state.gridSize && y < state.gridSize;
}
