// IsoCity CLI - share URL generation.
// Port of src/lib/shareState.ts compressGameState (MinState v1 format).
// lz-string is vendored (MIT, pieroxy) so the CLI runs without node_modules.
import LZString from './vendor/lz-string.js';

const ZONE_MAP = { none: 0, residential: 1, commercial: 2, industrial: 3 };

const BUILDING_TYPES = [
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

const BUILDING_MAP = new Map(BUILDING_TYPES.map((t, i) => [t, i]));

function minifyTile(tile) {
  return [
    ZONE_MAP[tile.zone] ?? 0,
    BUILDING_MAP.get(tile.building.type) ?? 1,
    tile.building.level,
    tile.building.population,
    tile.building.jobs,
    tile.building.powered ? 1 : 0,
    tile.building.watered ? 1 : 0,
    tile.landValue,
    tile.hasSubway ? 1 : 0,
    tile.building.constructionProgress ?? 100,
    tile.building.abandoned ? 1 : 0,
    tile.building.flipped ? 1 : 0,
    tile.hasRailOverlay ? 1 : 0,
  ];
}

export function compressGameState(state) {
  const min = {
    v: 1,
    n: state.cityName,
    s: state.gridSize,
    y: state.year,
    m: state.month,
    d: state.day,
    h: state.hour,
    t: state.taxRate,
    $: state.stats.money,
    g: state.grid.map((row) => row.map(minifyTile)),
  };
  if (state.adjacentCities && state.adjacentCities.length > 0) {
    min.ac = state.adjacentCities.map((city) => ({
      id: city.id,
      n: city.name,
      dir: city.direction[0],
      c: city.connected,
      d: city.discovered,
    }));
  }
  return LZString.compressToEncodedURIComponent(JSON.stringify(min));
}

export function createShareUrl(state, baseUrl = 'https://powpowcity.powpow.online/') {
  const compressed = compressGameState(state);
  const base = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;
  const rawName = String(state.cityName || 'Shared City').trim();
  const name = encodeURIComponent(Array.from(rawName).slice(0, 80).join('') || 'Shared City');
  // /c/<name> path gives chat-app link previews (WeChat cards) the city name;
  // the state itself lives in the #s= fragment which servers never see.
  return `${base}c/${name}#s=${compressed}`;
}
