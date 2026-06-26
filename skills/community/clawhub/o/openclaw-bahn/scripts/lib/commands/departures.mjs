import { makeEnvelope, mergeMessages, todayDateStr } from '../helpers.mjs';
import { searchStations, getStationDepartures } from '../data.mjs';
import { fmtTime } from '../format.mjs';

/**
 * --departures <station> [--results N]
 * Resolves station EVA, fetches live departures.
 * Returns an Envelope with departure entries.
 */
export default async function departures({ flags, positional }) {
  const stationArg = typeof flags.departures === 'string' ? flags.departures : positional.join(' ');
  const maxResults = parseInt(flags.results || '15', 10);
  const envelope = makeEnvelope('departures');

  if (!stationArg) {
    envelope.errors.push('Missing station. Usage: --departures <station> [--results N]');
    return envelope;
  }

  // Resolve EVA — numeric strings are treated as EVA codes directly
  let eva = stationArg;
  let stationName = stationArg;

  if (!/^\d{6,}$/.test(stationArg)) {
    const searchResult = await searchStations(stationArg);
    mergeMessages(envelope, searchResult);

    const stations = searchResult.data;

    if (!stations.length) {
      envelope.errors.push(`Station not found: '${stationArg}'`);
      return envelope;
    }

    // Fuzzy resolution: check for exact match (case-insensitive)
    const exactMatch = stations.some(s => s.name.toLowerCase() === stationArg.toLowerCase());
    if (!exactMatch) {
      envelope.warnings.push(`No exact match for '${stationArg}', using '${stations[0].name}'`);
    }

    eva = stations[0].eva;
    stationName = stations[0].name;
  }

  const depResult = await getStationDepartures(eva, todayDateStr());
  mergeMessages(envelope, depResult);

  // Normalize entries: { time, delay, train, destination, platform, cancelled }
  const raw = Array.isArray(depResult.data) ? depResult.data : [];
  const entries = raw.slice(0, maxResults).map(d => ({
    time: fmtTime(d.scheduledDep),
    delay: d.depDelay ?? 0,
    train: d.train ?? '?',
    destination: d.to?.name || (d.route?.length ? d.route[d.route.length - 1] : '?'),
    platform: d.platform ?? null,
    cancelled: d.cancelled ?? false,
  }));

  envelope.departures = { station: stationName, entries };
  return envelope;
}
