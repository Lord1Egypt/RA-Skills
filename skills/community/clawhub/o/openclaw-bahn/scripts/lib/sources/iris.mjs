import { XMLParser } from 'fast-xml-parser';
import { lookup } from '../messageLookup.mjs';

const IRIS_BASE = 'https://iris.noncd.db.de/iris-tts/timetable';

const parser = new XMLParser({
  ignoreAttributes: false,
  attributeNamePrefix: '',
  isArray: (name) => name === 's' || name === 'm',
});

function parseIrisTime(ts) {
  if (!ts || ts.length < 10) return null;
  const hh = parseInt(ts.slice(6, 8), 10);
  const mm = parseInt(ts.slice(8, 10), 10);
  return hh * 60 + mm;
}

function delayMinutes(ctStr, ptStr) {
  if (!ctStr) return 0;
  const ct = parseIrisTime(ctStr);
  const pt = parseIrisTime(ptStr);
  if (ct === null || pt === null) return 0;
  let diff = ct - pt;
  if (diff < -720) diff += 1440;
  return diff;
}

function toYYMMDD(date) {
  if (typeof date === 'string') {
    const parts = date.split('-');
    return parts[0].slice(2) + parts[1] + parts[2];
  }
  const yy = String(date.getFullYear()).slice(2);
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return yy + mm + dd;
}

// Parse IRIS timestamp YYMMDDHHMM → ISO string in Europe/Berlin
function irisTimeToISO(ts, dateStr) {
  if (!ts || ts.length < 10) return null;
  // ts format: YYMMDDHHMM, dateStr: YYYY-MM-DD
  const year = '20' + ts.slice(0, 2);
  const month = ts.slice(2, 4);
  const day = ts.slice(4, 6);
  const hh = ts.slice(6, 8);
  const mm = ts.slice(8, 10);
  // Build ISO string with Berlin offset (approximate — IRIS times are local)
  return `${year}-${month}-${day}T${hh}:${mm}:00+01:00`;
}

function extractDelayReasons(stop) {
  const messages = stop?.m ?? [];
  const arr = Array.isArray(messages) ? messages : [messages];
  return arr
    .filter(m => m && String(m.t) === 'd' && m.c != null)
    .map(m => {
      const code = parseInt(String(m.c), 10);
      return { code, text: lookup(code) };
    });
}

async function fetchXml(url) {
  const res = await fetch(url, { signal: AbortSignal.timeout(15_000) });
  if (!res.ok) throw new Error(`IRIS HTTP ${res.status} for ${url}`);
  const text = await res.text();
  return parser.parse(text);
}

/**
 * Fetch real-time delay for a train at a station.
 * @returns {{ arrDelayMin, depDelayMin, cancelled, found, delayReasons }}
 */
export async function getDelay(evaId, trainNumber, date, hour) {
  const yymmdd = toYYMMDD(date);
  const hh = String(hour).padStart(2, '0');
  const trainNum = String(trainNumber);

  const [planData, fchgData] = await Promise.all([
    fetchXml(`${IRIS_BASE}/plan/${evaId}/${yymmdd}/${hh}`),
    fetchXml(`${IRIS_BASE}/fchg/${evaId}`),
  ]);

  const planStops = planData?.timetable?.s || [];
  const fchgStops = fchgData?.timetable?.s || [];

  const planStop = planStops.find(s => String(s.tl?.n) === trainNum);
  if (!planStop) {
    return { arrDelayMin: null, depDelayMin: null, cancelled: false, found: false, delayReasons: [] };
  }

  const stopId = planStop.id;
  const fchgStop = fchgStops.find(s => s.id === stopId);

  const cancelled = fchgStop?.ar?.cs === 'c' || fchgStop?.dp?.cs === 'c' || false;

  let arrDelayMin = null;
  if (planStop.ar) {
    arrDelayMin = delayMinutes(fchgStop?.ar?.ct, planStop.ar.pt);
  }

  let depDelayMin = null;
  if (planStop.dp) {
    depDelayMin = delayMinutes(fchgStop?.dp?.ct, planStop.dp.pt);
  }

  const delayReasons = fchgStop ? extractDelayReasons(fchgStop) : [];

  return { arrDelayMin, depDelayMin, cancelled, found: true, delayReasons };
}

/**
 * Fetch plan + fchg for a station and return normalized departures in unified format.
 * @param {string} evaId
 * @param {{ date?: string, hours?: number[] }} opts
 * @returns {Promise<Array>}
 */
export async function getPlanAndFchg(evaId, { date, hours } = {}) {
  const now = new Date();
  const dateStr = date || now.toISOString().slice(0, 10);
  const hoursArr = hours || [now.getHours()];
  const yymmdd = toYYMMDD(dateStr);

  // Fetch plan for each hour + fchg in parallel
  const planFetches = hoursArr.map(h =>
    fetchXml(`${IRIS_BASE}/plan/${evaId}/${yymmdd}/${String(h).padStart(2, '0')}`)
      .catch(() => null)
  );
  const [fchgData, ...planResults] = await Promise.all([
    fetchXml(`${IRIS_BASE}/fchg/${evaId}`).catch(() => ({ timetable: { s: [] } })),
    ...planFetches,
  ]);

  const fchgStops = fchgData?.timetable?.s || [];
  const fchgById = Object.fromEntries(fchgStops.map(s => [s.id, s]));

  const allPlanStops = planResults.flatMap(r => r?.timetable?.s || []);

  return allPlanStops.map(s => {
    const fchg = fchgById[s.id] ?? {};
    const tl = s.tl ?? {};
    const dp = s.dp ?? {};
    const ar = s.ar ?? {};
    const fdp = fchg.dp ?? {};
    const far = fchg.ar ?? {};

    const scheduledDep = dp.pt ? irisTimeToISO(dp.pt, dateStr) : null;
    const actualDep = fdp.ct ? irisTimeToISO(fdp.ct, dateStr) : null;
    const depDelay = dp.pt ? delayMinutes(fdp.ct, dp.pt) : null;

    const scheduledArr = ar.pt ? irisTimeToISO(ar.pt, dateStr) : null;
    const actualArr = far.ct ? irisTimeToISO(far.ct, dateStr) : null;
    const arrDelay = ar.pt ? delayMinutes(far.ct, ar.pt) : null;

    const route = dp.ppth ? String(dp.ppth).split('|') : [];
    const cancelled = far.cs === 'c' || fdp.cs === 'c';
    const delayReasons = extractDelayReasons(fchg);

    return {
      train: `${tl.c ?? ''} ${tl.n ?? ''}`.trim(),
      trainNumber: String(tl.n ?? ''),
      category: String(tl.c ?? ''),
      from: { name: null, eva: evaId },
      to: { name: null, eva: null },
      scheduledDep,
      actualDep,
      depDelay,
      scheduledArr,
      actualArr,
      arrDelay,
      platform: fdp.cp ?? dp.pp ?? null,
      scheduledPlatform: dp.pp ?? null,
      cancelled,
      route,
      replacement: null,
      delayReasons,
      disruptions: [],
      source: 'iris',
    };
  });
}
