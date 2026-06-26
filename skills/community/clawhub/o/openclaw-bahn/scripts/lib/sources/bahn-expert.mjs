import { stringify, parse } from 'devalue';

const BASE_URL = 'https://bahn.expert/rpc';

/**
 * Generic tRPC caller for bahn.expert (devalue serialization).
 */
export async function callBahnExpert(procedure, input) {
  const serialized = stringify(input);
  const batchInput = JSON.stringify({ 0: serialized });
  const url = `${BASE_URL}/${procedure}?batch=1&input=${encodeURIComponent(batchInput)}`;
  const res = await fetch(url, { signal: AbortSignal.timeout(10_000) });
  if (!res.ok) throw new Error(`bahn.expert HTTP ${res.status} for ${procedure}`);
  const json = JSON.parse(await res.text());
  if (json[0]?.error) throw new Error(`bahn.expert tRPC error: ${JSON.stringify(json[0].error)}`);
  return parse(json[0].result.data);
}

// ---------------------------------------------------------------------------
// Departures (unified format)
// ---------------------------------------------------------------------------

function normalizeDeparture(d) {
  return {
    train: d.train?.name ?? null,
    trainNumber: d.train?.journeyNumber ?? null,
    category: d.train?.category ?? null,
    from: {
      name: d.station?.name ?? null,
      eva: d.station?.evaNumber ?? null,
    },
    to: {
      name: d.destination ?? null,
      eva: null,
    },
    scheduledDep: d.departure?.scheduledTime?.toISOString?.() ?? null,
    actualDep: d.departure?.time?.toISOString?.() ?? null,
    depDelay: d.departure?.delay ?? null,
    scheduledArr: d.arrival?.scheduledTime?.toISOString?.() ?? null,
    actualArr: d.arrival?.time?.toISOString?.() ?? null,
    arrDelay: d.arrival?.delay ?? null,
    platform: d.departure?.platform ?? null,
    scheduledPlatform: d.departure?.scheduledPlatform ?? null,
    cancelled: d.cancelled ?? false,
    route: d.route ?? [],
    replacement: d.substitute
      ? {
        train: d.ref?.train?.name ?? null,
        number: d.ref?.train?.journeyNumber ?? null,
        source: 'bahn-expert',
      }
      : null,
    delayReasons: (d.messages?.delay ?? []).map((m) => ({ code: null, text: m.text })),
    disruptions: (d.messages?.him ?? []).map((m) => ({
      category: 'Störung',
      source: 'bahn.expert',
      text: m.text,
      priority: m.priority ?? 1,
    })),
    source: 'bahn-expert',
  };
}

export async function getAbfahrten(evaNumber, { lookahead = 0, lookbehind = 0 } = {}) {
  const data = await callBahnExpert('iris.abfahrten', { evaNumber, lookahead, lookbehind });
  const departures = [
    ...(Array.isArray(data.departures) ? data.departures : []),
    ...(Array.isArray(data.lookbehind) ? data.lookbehind : []),
  ];
  return departures.map(normalizeDeparture);
}

// ---------------------------------------------------------------------------
// Station search
// ---------------------------------------------------------------------------

export async function searchStation(searchTerm, { filterForIris = false } = {}) {
  const stations = await callBahnExpert('stopPlace.byName', { searchTerm, filterForIris });
  return (stations || []).map((s) => ({
    eva: s.evaNumber,
    name: s.name,
    products: s.availableTransports ?? [],
  }));
}

// ---------------------------------------------------------------------------
// Journey lookup
// ---------------------------------------------------------------------------

export async function findJourney(journeyNumber, { initialDepartureDate, category } = {}) {
  const parsedNumber = typeof journeyNumber === 'string'
    ? parseInt(journeyNumber, 10)
    : journeyNumber;
  if (!Number.isFinite(parsedNumber)) throw new Error('journeyNumber must be a number');
  const input = { journeyNumber: parsedNumber };
  if (initialDepartureDate) {
    input.initialDepartureDate = initialDepartureDate instanceof Date
      ? initialDepartureDate
      : new Date(initialDepartureDate);
  }
  if (category) input.category = category;
  return callBahnExpert('journeys.find', input);
}

export async function getJourneyDetails(journeyId) {
  return callBahnExpert('journeys.detailsByJourneyId', journeyId);
}

// ---------------------------------------------------------------------------
// Train history & aggregate stats
// ---------------------------------------------------------------------------

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const percentile = (sorted, p) => {
  if (!sorted.length) return null;
  const idx = Math.ceil((p / 100) * sorted.length) - 1;
  return sorted[Math.min(Math.max(idx, 0), sorted.length - 1)];
};

const mean = (values) => (values.length
  ? values.reduce((sum, v) => sum + v, 0) / values.length
  : null);

const median = (values) => {
  if (!values.length) return null;
  const mid = Math.floor(values.length / 2);
  return values.length % 2 === 0
    ? (values[mid - 1] + values[mid]) / 2
    : values[mid];
};

export async function getTrainHistory(trainNumber, category, date) {
  const journeys = await findJourney(trainNumber, {
    category,
    initialDepartureDate: new Date(date),
  });
  if (!journeys?.length) throw new Error(`No journey found for ${category || ''} ${trainNumber}`.trim());
  const details = await getJourneyDetails(journeys[0].journeyId);
  return {
    train: details.train,
    date,
    stops: details.stops.map((s) => ({
      name: s.stopPlace.name,
      evaNumber: s.stopPlace.evaNumber,
      arrDelay: s.arrival?.delay ?? null,
      depDelay: s.departure?.delay ?? null,
      isRealTime: s.arrival?.isRealTime ?? s.departure?.isRealTime ?? false,
    })),
  };
}

export async function aggregateStats(trainNumber, category, days) {
  const stopStats = new Map();
  const today = new Date();

  for (let i = 1; i <= days; i += 1) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateString = date.toISOString().slice(0, 10);

    try {
      const history = await getTrainHistory(trainNumber, category, dateString);
      for (const stop of history.stops) {
        const delay = stop.arrDelay ?? stop.depDelay ?? null;
        if (delay === null) continue;
        if (!stopStats.has(stop.name)) stopStats.set(stop.name, []);
        stopStats.get(stop.name).push(delay);
      }
    } catch {
      // skip missing days
    }

    if (i < days) {
      await sleep(500);
    }
  }

  const stops = Array.from(stopStats.entries()).map(([name, delays]) => {
    const sorted = [...delays].sort((a, b) => a - b);
    const meanValue = mean(delays);
    const medianValue = median(sorted);
    const p95Value = percentile(sorted, 95);
    const onTimeRate = delays.length
      ? delays.filter((d) => d <= 5).length / delays.length
      : null;
    const zugbindungRate = delays.length
      ? delays.filter((d) => d >= 20).length / delays.length
      : null;

    return {
      name,
      mean: meanValue,
      median: medianValue,
      p95: p95Value,
      onTimeRate,
      zugbindungRate,
      samples: delays.length,
    };
  });

  return {
    trainNumber,
    category,
    days,
    stops,
  };
}
