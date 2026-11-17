/**
 * Forward geocoding: place name -> WGS-84 coordinates.
 *
 * Queries the platform's place-text search endpoint
 * (GET /api/amap/place/text, returns GCJ-02) and converts every candidate to
 * WGS-84 locally (lib/coord-transform.js) so the coordinates match the web
 * editor's coordinate system (its LocationPicker stores Nominatim/WGS-84).
 * The platform's provider is used because its Chinese POI coverage is far
 * better than open alternatives.
 *
 * The user must confirm a candidate before it enters a draft — same-name
 * places are common (e.g. "潮白河大桥" returns 90 hits).
 *
 * NEUTRAL NAMING RULE: this script's stdout may be paraphrased to the end
 * user. Never print the underlying map provider's brand name; say
 * 「地图数据库」/ "map database" instead. The endpoint path is the platform's
 * own and is not user-visible.
 *
 * Usage:
 *   node geocode.js "<place name>" [--city <city>] [--limit N] [--json]
 */
const { api, SessionExpiredError } = require('./lib/api-client');
const { gcj02ToWgs84 } = require('./lib/coord-transform');

async function main() {
  const args = process.argv.slice(2);
  const asJson = args.includes('--json');
  const cityIdx = args.indexOf('--city');
  const city = cityIdx !== -1 ? args[cityIdx + 1] : '全国';
  const limitIdx = args.indexOf('--limit');
  const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) || 5 : 5;
  const query = args.find(a => !a.startsWith('--') && a !== city && a !== String(limit));

  if (!query) {
    console.error('Usage: node geocode.js "<place name>" [--city <city>] [--limit N] [--json]');
    process.exit(1);
  }

  try {
    const path = `/api/amap/place/text?keywords=${encodeURIComponent(query)}`
      + `&city=${encodeURIComponent(city)}&offset=${limit}`;
    const body = await api('GET', path);
    const pois = (body.pois || []).filter(p => p.location && p.location.includes(','));

    if (pois.length === 0) {
      console.error(`❌ No place found for "${query}".`);
      console.error('   Try a different wording, add --city <城市>, or fall back to publishing without a location.');
      process.exitCode = 1;
      return;
    }

    const candidates = pois.map((p, i) => {
      const [gcjLng, gcjLat] = p.location.split(',').map(Number);
      const [lng, lat] = gcj02ToWgs84(gcjLng, gcjLat);
      return {
        index: i + 1,
        name: p.name,
        district: [p.pname, p.cityname, p.adname].filter(Boolean)
          .filter((s, i, arr) => s !== arr[i - 1]).join(''),
        address: p.address || '',
        lng: Number(lng.toFixed(6)),
        lat: Number(lat.toFixed(6)),
      };
    });

    if (asJson) {
      console.log(JSON.stringify(candidates, null, 2));
      return;
    }

    console.log(`Top ${candidates.length} candidates for "${query}" (地图数据库匹配，坐标已转换为平台坐标系):\n`);
    candidates.forEach(c => {
      console.log(`${c.index}. ${c.name}`);
      console.log(`   ${c.district} | ${c.lng}, ${c.lat} (WGS-84)`);
      if (c.address) console.log(`   ${c.address}`);
      console.log('');
    });
    console.log('Present these to the user to pick. If none fit, in this order:');
    console.log('  1) retry with different wording or --city <城市>;');
    console.log('  2) widen --limit and help the user recognise one from its district/address;');
    console.log('  3) publish without a location. Never ask the user for coordinates.');
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    console.error(`❌ Geocode failed: ${err.message}`);
    process.exitCode = 1;
  }
}

main();
