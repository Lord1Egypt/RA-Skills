import { makeEnvelope } from '../helpers.mjs';
import { findJourney, getJourneyDetails } from '../sources/bahn-expert.mjs';

/**
 * --track --train <NUM> --category <CAT> [--date YYYY-MM-DD] [--json]
 * Looks up a specific train and returns per-stop delay data.
 * Reports Zugbindung triggered when max observed delay ≥ 20 minutes.
 */
export default async function track({ flags }) {
  const trainNumber = flags.train;
  const category = flags.category;
  const date = flags.date || null;
  const envelope = makeEnvelope('track');

  if (!trainNumber || !category) {
    envelope.errors.push('Missing required flags. Usage: --track --train <NUM> --category <CAT> [--date YYYY-MM-DD] [--json]');
    return envelope;
  }

  let journeys;
  try {
    journeys = await findJourney(trainNumber, {
      category,
      initialDepartureDate: date ? new Date(date) : undefined,
    });
  } catch (err) {
    envelope.errors.push(`Journey lookup failed: ${err.message}`);
    return envelope;
  }

  if (!journeys?.length) {
    envelope.errors.push('Train not found');
    return envelope;
  }

  let details;
  try {
    details = await getJourneyDetails(journeys[0].journeyId);
  } catch (err) {
    envelope.errors.push(`Journey details failed: ${err.message}`);
    return envelope;
  }

  const stops = details.stops || [];
  const trainName = details.train?.name || `${category} ${trainNumber}`;
  const firstStop = stops[0]?.stopPlace?.name || '?';
  const lastStop = stops.at(-1)?.stopPlace?.name || '?';

  const perStop = stops.map(stop => ({
    name: stop.stopPlace?.name,
    arrDelay: stop.arrival?.delay ?? null,
    depDelay: stop.departure?.delay ?? null,
    isRealTime: stop.arrival?.isRealTime || stop.departure?.isRealTime || false,
  }));

  let maxDelay = 0;
  for (const stop of perStop) {
    for (const d of [stop.arrDelay, stop.depDelay]) {
      if (d !== null && d !== undefined && !Number.isNaN(d) && d > maxDelay) {
        maxDelay = d;
      }
    }
  }

  const zugbindungStatus = maxDelay >= 20 ? 'triggered' : 'not_triggered';

  envelope.trackStatus = {
    train: trainName,
    from: firstStop,
    to: lastStop,
    stops: perStop,
    maxDelay,
    zugbindungStatus,
    delayReasons: details.currentStop?.irisMessages || [],
  };

  return envelope;
}
