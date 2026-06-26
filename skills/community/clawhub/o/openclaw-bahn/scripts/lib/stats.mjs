/**
 * stats.mjs — Historical delay statistics from bahn.expert.
 * Opt-in via --stats. Fetches 14-day aggregate data per train.
 * Returns per-leg historical stats: mean, median, p95, zugbindungRate, samples.
 */

/**
 * Fetch historical stats for a leg via data.getHistoricalStats().
 * @param {object} leg - { trainNumber, category, number }
 * @param {object} dataModule - data.mjs module (for getHistoricalStats)
 * @param {{ days?: number }} opts
 * @returns {Promise<object|null>} stats object or null if unavailable
 */
export async function getLegHistoricalStats(leg, dataModule, { days = 14 } = {}) {
  const trainNumber = leg.trainNumber || leg.number;
  if (!trainNumber || !leg.category || !dataModule) return null;

  try {
    const result = await dataModule.getHistoricalStats(trainNumber, leg.category, days);
    const data = result?.data;
    if (!data?.stops || !Array.isArray(data.stops)) return null;

    let stops = data.stops.filter(s => s.samples > 0);
    if (!stops.length) return null;

    // Filter to only stops between leg.from and leg.to (inclusive)
    if (leg.from || leg.to) {
      const fromIdx = leg.from ? stops.findIndex(s => normalize(s.name) === normalize(leg.from)) : 0;
      const toIdx = leg.to ? stops.findIndex(s => normalize(s.name) === normalize(leg.to)) : stops.length - 1;
      if (fromIdx !== -1 && toIdx !== -1 && fromIdx <= toIdx) {
        stops = stops.slice(fromIdx, toIdx + 1);
      }
    }

    if (!stops.length) return null;

    // Use only the arrival stop (leg.to) — that's the delay you actually experience
    const arrivalStop = stops[stops.length - 1];
    if (arrivalStop.samples < 3) return null;

    return {
      trainNumber,
      category: leg.category,
      days,
      samples: arrivalStop.samples,
      mean: round2(arrivalStop.mean),
      median: round2(arrivalStop.median),
      p95: round2(arrivalStop.p95),
      onTimeRate: round4(arrivalStop.onTimeRate),
      zugbindungRate: round4(arrivalStop.zugbindungRate),
    };
  } catch {
    return null;
  }
}

function round2(v) { return v != null ? Math.round(v * 100) / 100 : null; }
function round4(v) { return v != null ? Math.round(v * 10000) / 10000 : null; }

/** Normalize station name for fuzzy matching (strip Hbf, parens, lowercase). */
function normalize(name) {
  return (name || '')
    .replace(/\s*\(.*?\)\s*/g, ' ')  // replace (parens) with a space to avoid concatenation
    .replace(/\bHbf\b/gi, '')
    .replace(/\bhaupt(?:bahnhof)?\b/gi, '')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}
