/**
 * data.mjs — Central source router.
 * Picks the right data source based on date context, handles fallbacks.
 * Every exported function returns { data, warnings, errors }.
 */

import * as bahnExpert from './sources/bahn-expert.mjs';
import * as vendo from './sources/vendo.mjs';
import * as iris from './sources/iris.mjs';

// ---------------------------------------------------------------------------
// Date classification helpers (Europe/Berlin timezone)
// ---------------------------------------------------------------------------

function berlinDateStr(dateStr) {
  const d = dateStr instanceof Date ? dateStr : new Date(dateStr + (dateStr.includes('T') ? '' : 'T12:00:00'));
  return d.toLocaleDateString('sv-SE', { timeZone: 'Europe/Berlin' });
}

function todayBerlin() {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Europe/Berlin' });
}

export function isToday(dateStr) {
  return berlinDateStr(dateStr) === todayBerlin();
}

export function isPast(dateStr) {
  return berlinDateStr(dateStr) < todayBerlin();
}

export function isFuture(dateStr) {
  return berlinDateStr(dateStr) > todayBerlin();
}

// ---------------------------------------------------------------------------
// searchStations — bahn-expert first, fallback vendo
// ---------------------------------------------------------------------------

export async function searchStations(query) {
  const warnings = [];
  const errors = [];

  try {
    const data = await bahnExpert.searchStation(query);
    return { data, warnings, errors };
  } catch (err) {
    warnings.push(`bahn.expert station search failed: ${err.message} — falling back to vendo`);
  }

  try {
    const data = await vendo.searchStations(query);
    return { data, warnings, errors };
  } catch (err) {
    errors.push(`vendo station search also failed: ${err.message}`);
    return { data: [], warnings, errors };
  }
}

// ---------------------------------------------------------------------------
// getStationDepartures — past→bahnExpert, today→IRIS, future→vendo
// ---------------------------------------------------------------------------

export async function getStationDepartures(eva, date) {
  const warnings = [];
  const errors = [];

  if (isPast(date)) {
    // Past: bahn.expert (has historical IRIS data)
    try {
      const data = await bahnExpert.getAbfahrten(eva, { lookbehind: 480 });
      return { data, warnings, errors };
    } catch (err) {
      errors.push(`bahn.expert departures failed for past date: ${err.message}`);
      return { data: [], warnings, errors };
    }
  }

  if (isToday(date)) {
    // Today: IRIS primary, bahn.expert fallback
    try {
      const now = new Date();
      const currentHour = parseInt(now.toLocaleString('en-US', { timeZone: 'Europe/Berlin', hour: 'numeric', hour12: false }), 10);
      const hours = [currentHour];
      if (currentHour > 0) hours.unshift(currentHour - 1);
      if (currentHour < 23) hours.push(currentHour + 1);

      const data = await iris.getPlanAndFchg(eva, { date, hours });
      return { data, warnings, errors };
    } catch (irisErr) {
      warnings.push(`IRIS departures failed: ${irisErr.message} — falling back to bahn.expert`);
      try {
        const data = await bahnExpert.getAbfahrten(eva, { lookahead: 120, lookbehind: 30 });
        return { data, warnings, errors };
      } catch (beErr) {
        errors.push(`bahn.expert fallback also failed: ${beErr.message}`);
        return { data: [], warnings, errors };
      }
    }
  }

  // Future: vendo
  try {
    const data = await vendo.getDepartures(eva);
    return { data, warnings, errors };
  } catch (err) {
    errors.push(`vendo departures failed for future date: ${err.message}`);
    return { data: [], warnings, errors };
  }
}

// ---------------------------------------------------------------------------
// getTrainDelay — past→bahnExpert (hard error), today→IRIS
// ---------------------------------------------------------------------------

export async function getTrainDelay(eva, trainNumber, date, hour) {
  const warnings = [];
  const errors = [];

  if (isPast(date)) {
    // Past: bahn.expert only, no fallback
    try {
      const abfahrten = await bahnExpert.getAbfahrten(eva, { lookbehind: 480 });
      const match = abfahrten.find(d =>
        String(d.trainNumber) === String(trainNumber) || d.train?.includes(String(trainNumber))
      );
      if (!match) {
        errors.push(`Train ${trainNumber} not found in bahn.expert historical data for ${eva}`);
        return { data: null, warnings, errors };
      }
      return {
        data: {
          arrDelay: match.arrDelay,
          depDelay: match.depDelay,
          cancelled: match.cancelled,
          delayReasons: match.delayReasons,
          source: 'bahn-expert',
        },
        warnings,
        errors,
      };
    } catch (err) {
      errors.push(`bahn.expert unavailable — no fallback for past delay data: ${err.message}`);
      return { data: null, warnings, errors };
    }
  }

  // Today (or future treated as today): IRIS
  try {
    const result = await iris.getDelay(eva, trainNumber, date, hour);
    return {
      data: {
        arrDelay: result.arrDelayMin,
        depDelay: result.depDelayMin,
        cancelled: result.cancelled,
        found: result.found,
        delayReasons: result.delayReasons,
        source: 'iris',
      },
      warnings,
      errors,
    };
  } catch (err) {
    errors.push(`IRIS delay fetch failed: ${err.message}`);
    return { data: null, warnings, errors };
  }
}

// ---------------------------------------------------------------------------
// getJourneys — always vendo
// ---------------------------------------------------------------------------

export async function getJourneys(from, to, date, time, opts = {}) {
  const warnings = [];
  const errors = [];

  try {
    const data = await vendo.getJourneys(from, to, { date, time, ...opts });
    return { data, warnings, errors };
  } catch (err) {
    errors.push(`vendo journeys failed: ${err.message}`);
    return { data: [], warnings, errors };
  }
}

// ---------------------------------------------------------------------------
// getHistoricalStats — always bahnExpert.aggregateStats, hard error if down
// ---------------------------------------------------------------------------

export async function getHistoricalStats(trainNumber, category, days) {
  const warnings = [];
  const errors = [];

  try {
    const data = await bahnExpert.aggregateStats(trainNumber, category, days);
    return { data, warnings, errors };
  } catch (err) {
    errors.push(`bahn.expert unavailable — no fallback for historical data`);
    return { data: null, warnings, errors };
  }
}
