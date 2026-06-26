import { readFileSync } from 'node:fs';
import { makeEnvelope, toMinutes, mergeMessages } from '../helpers.mjs';
import { searchStations, getTrainDelay } from '../data.mjs';
import { transferRisk } from '../format.mjs';
import * as predict from '../predict.mjs';

const MIN_WALK_TIME = 2;

function transferTime(arrTime, depTime) {
  let diff = toMinutes(depTime) - toMinutes(arrTime);
  if (diff < 0) diff += 1440; // midnight crossing
  return diff;
}

/**
 * --live <file.json> --current-leg N [--delay M] [--predict] [--json]
 * Fetches live delay data for the current leg and computes transfer feasibility.
 * Returns an Envelope with liveStatus.
 */
export default async function live({ flags, positional }) {
  const file = typeof flags.live === 'string' ? flags.live : positional[0];
  const wantPredict = !!flags.predict;
  const envelope = makeEnvelope('live');

  if (!file) {
    envelope.errors.push('Missing connection file. Usage: --live [file.json] --current-leg N [--delay M] [--json]');
    return envelope;
  }

  if (flags['current-leg'] === undefined) {
    envelope.errors.push('Missing --current-leg N');
    return envelope;
  }

  let connection;
  try {
    connection = JSON.parse(readFileSync(file, 'utf8'));
  } catch (err) {
    envelope.errors.push(`Failed to load connection file: ${err.message}`);
    return envelope;
  }

  const legs = connection.legs;
  const legIdx = parseInt(flags['current-leg'], 10);

  if (isNaN(legIdx) || legIdx < 0 || legIdx >= legs.length - 1) {
    envelope.errors.push(`--current-leg ${flags['current-leg']} out of range (valid: 0-${legs.length - 2})`);
    return envelope;
  }

  const current = legs[legIdx];
  const next = legs[legIdx + 1];
  const tMin = transferTime(current.arr, next.dep);
  const buffer = tMin - MIN_WALK_TIME;

  let delay = 0;
  let cancelled = false;
  let delayReasons = [];
  let zugbindungStatus = 'not_triggered';

  if (flags.delay !== undefined) {
    // ── Mode B: known delay ──
    delay = parseInt(flags.delay, 10);
    if (isNaN(delay)) delay = 0;
  } else {
    // ── Mode C: fetch live delay from IRIS ──
    let eva = null;
    const stationResult = await searchStations(current.to);
    mergeMessages(envelope, stationResult);

    if (stationResult.data?.length) {
      eva = stationResult.data[0].eva;
    }

    if (!eva) {
      delay = Math.round(predict.getProfile(current.category).mean);
      envelope.warnings.push(`Could not resolve station "${current.to}" — using model estimate (+${delay}min)`);
    } else {
      const hour = parseInt(current.arr.split(':')[0], 10);
      const result = await getTrainDelay(eva, current.number, connection.date, hour);
      mergeMessages(envelope, result);

      if (result.errors?.length || !result.data) {
        delay = Math.round(predict.getProfile(current.category).mean);
        envelope.warnings.push(`Live delay unavailable for ${current.train} — using model estimate (+${delay}min)`);
      } else if (result.data.cancelled) {
        cancelled = true;
        delay = 0;
        delayReasons = result.data.delayReasons || [];
      } else {
        delay = result.data.depDelay ?? result.data.arrDelay ?? 0;
        delayReasons = result.data.delayReasons || [];
      }
    }
  }

  // ── Zugbindung status ──
  if (cancelled) {
    zugbindungStatus = 'triggered_cancellation';
  } else if (delay >= 20) {
    zugbindungStatus = 'triggered_delay';
  }

  // ── Next transfer probability ──
  const effectiveMin = Math.max(0, tMin - delay);
  const nextRisk = transferRisk(effectiveMin).label;
  const catchProb = wantPredict
    ? (cancelled ? 0 : predict.transferProbWithKnownDelay(delay, next.category, buffer))
    : null;

  // ── Recommendation ──
  let recommendation;
  if (zugbindungStatus !== 'not_triggered') {
    recommendation = 'Ticket binding lifted — you may take any train.';
  } else if (effectiveMin >= 8) {
    recommendation = `Transfer is safe. ${effectiveMin}min effective buffer at ${current.to}.`;
  } else if (effectiveMin >= 4) {
    recommendation = 'Transfer is tight. Monitor delays.';
  } else if (effectiveMin >= 1) {
    recommendation = `Transfer at risk. Consider alternatives.`;
  } else {
    recommendation = 'Transfer very likely missed. Switch to alternative route.';
  }

  // ── Remaining transfers ──
  const remainingTransfers = [];
  for (let i = legIdx + 1; i < legs.length - 1; i++) {
    const rMin = transferTime(legs[i].arr, legs[i + 1].dep);
    const rRisk = transferRisk(rMin).label;
    const rt = { at: legs[i].to, minutes: rMin, risk: rRisk };
    if (wantPredict) {
      rt.catchProb = predict.transferProb(rMin, legs[i].category, legs[i + 1].category);
    }
    remainingTransfers.push(rt);
  }

  // ── Build envelope ──
  envelope.connection = connection;
  envelope.liveStatus = {
    currentLeg: {
      train: current.train,
      station: current.to,
      delay,
      cancelled,
      delayReasons,
    },
    nextTransfer: {
      nextTrain: next.train,
      at: current.to,
      scheduledMinutes: tMin,
      effectiveMinutes: effectiveMin,
      catchProb,
      risk: nextRisk,
    },
    zugbindungStatus,
    recommendation,
    remainingTransfers,
  };

  return envelope;
}
