import { createClient } from 'db-vendo-client';
import { profile as dbnavProfile } from 'db-vendo-client/p/dbnav/index.js';

const client = createClient(dbnavProfile, 'openclaw-db-skill/1.0');

const PRODUCT_CATEGORY = {
  nationalExpress: 'ICE',
  national: 'IC',
  regionalExpress: 'RE',
  regional: 'RB',
  suburban: 'S',
  bus: 'Bus',
};

export async function searchStations(query) {
  const results = await client.locations(query, {
    results: 10,
    poi: false,
    addresses: false,
  });
  return results.map(r => ({
    eva: r.id,
    name: r.name,
    products: Object.keys(r.products || {})
      .filter(k => r.products[k])
      .map(k => k.toUpperCase()),
  }));
}

export async function getDepartures(evaOrQuery, { results = 10 } = {}) {
  let eva = evaOrQuery;
  if (!/^\d+$/.test(evaOrQuery)) {
    const stations = await searchStations(evaOrQuery);
    if (!stations.length) throw new Error(`Station not found: ${evaOrQuery}`);
    eva = stations[0].eva;
  }

  const data = await client.departures(eva, { results, stopovers: false });
  const departures = data.departures ?? data;

  return departures.map(d => ({
    train: d.line?.name ?? d.direction ?? '?',
    trainNumber: d.line?.fahrtNr ?? null,
    category: PRODUCT_CATEGORY[d.line?.product] ?? d.line?.product ?? '?',
    from: { name: d.stop?.name ?? null, eva: d.stop?.id ?? null },
    to: { name: d.destination?.name ?? null, eva: d.destination?.id ?? null },
    scheduledDep: d.plannedWhen ?? null,
    actualDep: d.when ?? null,
    depDelay: d.delay != null ? Math.round(d.delay / 60) : null,
    scheduledArr: null,
    actualArr: null,
    arrDelay: null,
    platform: d.platform ?? null,
    scheduledPlatform: d.plannedPlatform ?? null,
    cancelled: d.cancelled ?? false,
    route: [],
    replacement: null,
    delayReasons: [],
    disruptions: [],
    source: 'vendo',
  }));
}

export async function getJourneys(fromQuery, toQuery, { date, time, results = 3 } = {}) {
  const [fromStations, toStations] = await Promise.all([
    searchStations(fromQuery),
    searchStations(toQuery),
  ]);
  if (!fromStations.length) throw new Error(`Station not found: ${fromQuery}`);
  if (!toStations.length) throw new Error(`Station not found: ${toQuery}`);

  const fromEva = fromStations[0].eva;
  const toEva = toStations[0].eva;

  const journeyOpts = { results, stopovers: true };
  if (date || time) {
    const d = date || new Date().toISOString().slice(0, 10);
    const t = time || '08:00';
    journeyOpts.departure = new Date(`${d}T${t}`);
  }

  const data = await client.journeys(fromEva, toEva, journeyOpts);
  return data.journeys ?? [];
}
