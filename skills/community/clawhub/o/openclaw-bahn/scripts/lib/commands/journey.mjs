import { getJourneys } from '../data.mjs';
import * as predict from '../predict.mjs';
import { fmtTime, transferRisk } from '../format.mjs';
import {
  makeEnvelope,
  toMinutes,
  todayDateStr,
  mergeMessages,
  extractRemarks,
  computeAssessment,
} from '../helpers.mjs';

/**
 * --journey <from> <to> [--date YYYY-MM-DD] [--time HH:MM] [--results N] [--days N] [--predict]
 * Searches for journey options between two stations.
 * Returns an Envelope with journey options including legs, transfers, and durations.
 */
export default async function journey({ flags, positional }) {
  const fromQ = typeof flags.journey === 'string' ? flags.journey : null;
  const toQ = positional[0] || null;
  const numResults = parseInt(flags.results || '3', 10);
  const numDays = flags.days ? parseInt(flags.days, 10) : 1;
  const baseDate = flags.date || todayDateStr();
  const time = flags.time || null;
  const wantPredict = !!flags.predict;
  const envelope = makeEnvelope('journey');

  if (!fromQ || !toQ) {
    envelope.errors.push('Missing stations. Usage: --journey <from> <to> [--date YYYY-MM-DD] [--time HH:MM] [--results N] [--days N]');
    return envelope;
  }

  const allOptions = [];

  for (let d = 0; d < numDays; d++) {
    const dateObj = new Date(baseDate + 'T12:00:00');
    dateObj.setDate(dateObj.getDate() + d);
    const dateStr = dateObj.toISOString().slice(0, 10);

    const result = await getJourneys(fromQ, toQ, dateStr, time, { results: numResults });
    mergeMessages(envelope, result);

    const journeys = Array.isArray(result.data) ? result.data : [];

    for (let j = 0; j < journeys.length; j++) {
      const journey = journeys[j];
      const rawLegs = journey.legs || [];

      // Normalize legs
      const normalizedLegs = rawLegs.map(leg => {
        if (leg.walking) {
          return {
            train: null,
            category: null,
            from: leg.origin?.name || null,
            to: leg.destination?.name || null,
            dep: fmtTime(leg.departure),
            arr: fmtTime(leg.arrival),
            depDelay: null,
            cancelled: false,
            platformDep: null,
            platformArr: null,
            walking: true,
            remarks: [],
          };
        }

        const remarks = extractRemarks(leg);

        return {
          train: leg.line?.name || null,
          category: leg.line?.product || leg.line?.productName || null,
          from: leg.origin?.name || null,
          to: leg.destination?.name || null,
          dep: fmtTime(leg.departure),
          arr: fmtTime(leg.arrival),
          depDelay: leg.departureDelay ? Math.round(leg.departureDelay / 60) : null,
          cancelled: leg.cancelled || false,
          platformDep: leg.departurePlatform || null,
          platformArr: leg.arrivalPlatform || null,
          walking: false,
          remarks,
        };
      });

      const trainLegs = normalizedLegs.filter(l => !l.walking && l.category);

      // Compute transfers between consecutive non-walking legs
      const transfers = [];
      for (let k = 0; k < trainLegs.length - 1; k++) {
        const arr = trainLegs[k];
        const dep = trainLegs[k + 1];

        // Skip transfer computation if either leg is cancelled (times are invalid)
        if (arr.cancelled || dep.cancelled || arr.arr === '??:??' || dep.dep === '??:??') {
          transfers.push({
            at: arr.to,
            scheduledMinutes: null,
            risk: 'CRITICAL',
            platformFrom: arr.platformArr || null,
            platformTo: dep.platformDep || null,
            platformChange: false,
            differentStation: arr.to !== dep.from,
            cancelled: true,
            ...(wantPredict ? { catchProb: 0 } : {}),
          });
          continue;
        }

        let scheduledMinutes = toMinutes(dep.dep) - toMinutes(arr.arr);
        if (scheduledMinutes < 0) scheduledMinutes += 1440;

        const risk = transferRisk(scheduledMinutes).label;
        const platformFrom = arr.platformArr || null;
        const platformTo = dep.platformDep || null;
        const platformChange = !!(platformFrom && platformTo && platformFrom !== platformTo);
        const differentStation = arr.to !== dep.from;

        const transfer = {
          at: arr.to,
          scheduledMinutes,
          risk,
          platformFrom,
          platformTo,
          platformChange,
          differentStation,
        };

        if (wantPredict) {
          transfer.catchProb = predict.transferProb(scheduledMinutes, arr.category, dep.category);
        }

        transfers.push(transfer);
      }

      const assessment = wantPredict ? computeAssessment(trainLegs, transfers) : null;

      const depTime = new Date(rawLegs[0]?.departure);
      const arrTime = new Date(rawLegs[rawLegs.length - 1]?.arrival);
      const durationMs = arrTime - depTime;
      const durationMinutes = Number.isFinite(durationMs) && durationMs > 0 ? Math.round(durationMs / 60000) : null;

      allOptions.push({
        index: allOptions.length + 1,
        ...(numDays > 1 ? { date: dateStr } : {}),
        from: normalizedLegs[0]?.from || fromQ,
        to: normalizedLegs[normalizedLegs.length - 1]?.to || toQ,
        departure: rawLegs[0]?.departure || null,
        arrival: rawLegs[rawLegs.length - 1]?.arrival || null,
        durationMinutes,
        numTransfers: Math.max(0, trainLegs.length - 1),
        legs: normalizedLegs,
        transfers,
        assessment,
      });
    }
  }

  envelope.journeyOptions = {
    from: fromQ,
    to: toQ,
    date: baseDate,
    options: allOptions,
  };
  return envelope;
}
