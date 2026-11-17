// IsoCity CLI - Baidu Maps provider: geocoding + China coordinate system conversion.
// Systems: WGS-84 (true GPS, what OSM/Overpass uses), GCJ-02 (China standard offset,
// Amap/Tencent), BD-09 (Baidu offset). WGS-84<->GCJ-02 uses the well-known offline
// approximation (~1m accurate); BD-09<->GCJ-02 uses Baidu's published formula pair.

import { pathToFileURL } from 'node:url';

const GEOCODE_URL = 'https://api.map.baidu.com/geocoding/v3/';

const PI = Math.PI;
const X_PI = (PI * 3000.0) / 180.0;
const A = 6378245.0;
const EE = 0.00669342162296594323;

function transformLat(x, y) {
  let ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x));
  ret += ((20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0) / 3.0;
  ret += ((20.0 * Math.sin(y * PI) + 40.0 * Math.sin((y / 3.0) * PI)) * 2.0) / 3.0;
  ret += ((160.0 * Math.sin((y / 12.0) * PI) + 320.0 * Math.sin((y * PI) / 30.0)) * 2.0) / 3.0;
  return ret;
}

function transformLon(x, y) {
  let ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x));
  ret += ((20.0 * Math.sin(6.0 * x * PI) + 20.0 * Math.sin(2.0 * x * PI)) * 2.0) / 3.0;
  ret += ((20.0 * Math.sin(x * PI) + 40.0 * Math.sin((x / 3.0) * PI)) * 2.0) / 3.0;
  ret += ((150.0 * Math.sin((x / 12.0) * PI) + 300.0 * Math.sin((x / 30.0) * PI)) * 2.0) / 3.0;
  return ret;
}

export function outOfChina(lat, lon) {
  return lon < 72.004 || lon > 137.8347 || lat < 0.8293 || lat > 55.8271;
}

export function wgs84ToGcj02(lat, lon) {
  if (outOfChina(lat, lon)) return { lat, lon };
  const dLat = transformLat(lon - 105.0, lat - 35.0);
  const dLon = transformLon(lon - 105.0, lat - 35.0);
  const radLat = (lat / 180.0) * PI;
  let magic = Math.sin(radLat);
  magic = 1 - EE * magic * magic;
  const sqrtMagic = Math.sqrt(magic);
  const dLatAdj = (dLat * 180.0) / (((A * (1 - EE)) / (magic * sqrtMagic)) * PI);
  const dLonAdj = (dLon * 180.0) / ((A / sqrtMagic) * Math.cos(radLat) * PI);
  return { lat: lat + dLatAdj, lon: lon + dLonAdj };
}

export function gcj02ToWgs84(lat, lon) {
  if (outOfChina(lat, lon)) return { lat, lon };
  let wgsLat = lat;
  let wgsLon = lon;
  for (let i = 0; i < 4; i++) {
    const g = wgs84ToGcj02(wgsLat, wgsLon);
    wgsLat += lat - g.lat;
    wgsLon += lon - g.lon;
  }
  return { lat: wgsLat, lon: wgsLon };
}

export function gcj02ToBd09(lat, lon) {
  const z = Math.sqrt(lon * lon + lat * lat) + 0.00002 * Math.sin(lat * X_PI);
  const theta = Math.atan2(lat, lon) + 0.000003 * Math.cos(lon * X_PI);
  return { lat: z * Math.sin(theta) + 0.006, lon: z * Math.cos(theta) + 0.0065 };
}

export function bd09ToGcj02(lat, lon) {
  const x = lon - 0.0065;
  const y = lat - 0.006;
  const z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * X_PI);
  const theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * X_PI);
  return { lat: z * Math.sin(theta), lon: z * Math.cos(theta) };
}

export function bd09ToWgs84(lat, lon) {
  const g = bd09ToGcj02(lat, lon);
  return gcj02ToWgs84(g.lat, g.lon);
}

export function wgs84ToBd09(lat, lon) {
  const g = wgs84ToGcj02(lat, lon);
  return gcj02ToBd09(g.lat, g.lon);
}

export function toWgs84(lat, lon, from = 'wgs84') {
  if (from === 'wgs84') return { lat, lon };
  if (from === 'gcj02') return gcj02ToWgs84(lat, lon);
  if (from === 'bd09') return bd09ToWgs84(lat, lon);
  throw new Error(`Unknown coordinate system "${from}" (expected wgs84, gcj02 or bd09)`);
}

export function haversineMeters(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const dLat = ((lat2 - lat1) * PI) / 180;
  const dLon = ((lon2 - lon1) * PI) / 180;
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * PI) / 180) * Math.cos((lat2 * PI) / 180) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

const BAIDU_ERRORS = {
  1: 'server internal error',
  2: 'invalid request parameters',
  3: 'verification failed',
  4: 'daily quota exhausted',
  5: 'AK does not exist or is illegal',
  101: 'AK does not exist',
  102: 'AK signature (SN) check failed',
  201: 'blocked by AK whitelist',
  202: 'request rejected (quota or permission)',
  210: 'IP verification failed - check the AK IP whitelist (leave it empty for CLI use)',
  211: 'AK has no permission for this API - the app type must be "服务端" (server-side), not browser-side',
  240: 'AK does not exist or is wrong',
  241: 'AK service is blocked',
  252: 'request rate exceeded, retry later',
};

export async function geocodeBaidu(address, ak, { city } = {}) {
  if (!ak) throw new Error('Baidu geocoding needs an AK: pass --ak <AK> or set BAIDU_MAP_AK');
  const params = new URLSearchParams({ address, output: 'json', ak });
  if (city) params.set('city', city);
  let res;
  try {
    res = await fetch(`${GEOCODE_URL}?${params}`, { signal: AbortSignal.timeout(30000) });
  } catch (e) {
    throw new Error(`Baidu Maps API unreachable (${e.cause?.code || e.message})`);
  }
  if (!res.ok) throw new Error(`Baidu geocoding failed: HTTP ${res.status}`);
  const data = await res.json();
  const status = Number(data?.status ?? -1);
  if (status !== 0) {
    const desc = BAIDU_ERRORS[status] || data?.message || 'unknown error';
    throw new Error(`Baidu geocoding failed (status ${status}: ${desc})`);
  }
  const loc = data?.result?.location;
  if (!loc || typeof loc.lat !== 'number' || typeof loc.lng !== 'number') {
    throw new Error(`Baidu geocoding returned no location for "${address}"`);
  }
  const wgs = bd09ToWgs84(loc.lat, loc.lng);
  const level = data.result.level || 'unknown';
  const precise = Number(data.result.precise ?? 0) === 1;
  return {
    lat: wgs.lat,
    lon: wgs.lon,
    bd09Lat: loc.lat,
    bd09Lon: loc.lng,
    level,
    precise,
    confidence: data.result.confidence,
    displayName: `${address} [Baidu geocode, level=${level}${precise ? ', precise' : ', approximate'}]`,
  };
}

async function selfTest() {
  const argv = process.argv.slice(2);
  const akIdx = argv.indexOf('--ak');
  const ak = akIdx >= 0 ? argv[akIdx + 1] : process.env.BAIDU_MAP_AK || '';
  const placeIdx = argv.indexOf('--place');
  const place = placeIdx >= 0 ? argv[placeIdx + 1] : '北京大学';

  console.log('== Offline coordinate conversion self-test ==');
  const POINTS = [
    { name: 'Beijing (Tiananmen)', lat: 39.90734, lon: 116.39134 },
    { name: 'Shanghai (the Bund)', lat: 31.2397, lon: 121.4869 },
    { name: 'Shenzhen', lat: 22.546, lon: 114.0579 },
    { name: 'Chengdu', lat: 30.6602, lon: 104.0799 },
    { name: 'New York (outside China)', lat: 40.7128, lon: -74.006 },
  ];
  let failures = 0;
  for (const p of POINTS) {
    const gcj = wgs84ToGcj02(p.lat, p.lon);
    const bd = gcj02ToBd09(gcj.lat, gcj.lon);
    const back = bd09ToWgs84(bd.lat, bd.lon);
    const rtErr = haversineMeters(p.lat, p.lon, back.lat, back.lon);
    const gcjOff = haversineMeters(p.lat, p.lon, gcj.lat, gcj.lon);
    const inChina = !outOfChina(p.lat, p.lon);
    const okRt = rtErr < 2;
    const okOff = inChina ? gcjOff > 100 && gcjOff < 2000 : gcjOff < 0.01;
    const ok = okRt && okOff;
    if (!ok) failures++;
    console.log(
      `${ok ? 'PASS' : 'FAIL'} ${p.name}: wgs=(${p.lat.toFixed(5)},${p.lon.toFixed(5)}) ` +
      `gcj=(${gcj.lat.toFixed(5)},${gcj.lon.toFixed(5)}) bd09=(${bd.lat.toFixed(5)},${bd.lon.toFixed(5)}) ` +
      `gcj-offset=${gcjOff.toFixed(0)}m roundtrip-err=${rtErr.toFixed(2)}m`
    );
  }
  try {
    toWgs84(39.9, 116.3, 'bogus');
    console.log('FAIL toWgs84 should reject unknown coordinate system');
    failures++;
  } catch {
    console.log('PASS toWgs84 rejects unknown coordinate system');
  }

  if (ak) {
    console.log(`\n== Live Baidu geocoding test: "${place}" ==`);
    try {
      const r = await geocodeBaidu(place, ak);
      const off = haversineMeters(r.bd09Lat, r.bd09Lon, r.lat, r.lon);
      console.log(`PASS geocoded via Baidu`);
      console.log(`  BD-09:    ${r.bd09Lat.toFixed(6)}, ${r.bd09Lon.toFixed(6)}`);
      console.log(`  WGS-84:   ${r.lat.toFixed(6)}, ${r.lon.toFixed(6)} (for OSM)`);
      console.log(`  correction offset: ${Math.round(off)}m, level=${r.level}, precise=${r.precise}`);
    } catch (e) {
      console.log(`FAIL live geocoding: ${e.message}`);
      failures++;
    }
  } else {
    console.log('\n(live geocoding skipped: pass --ak <AK> or set BAIDU_MAP_AK to test)');
  }
  process.exitCode = failures > 0 ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  selfTest().catch((e) => {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  });
}
