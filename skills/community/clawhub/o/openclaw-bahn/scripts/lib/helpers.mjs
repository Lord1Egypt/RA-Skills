import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import * as predict from './predict.mjs';
import { transferRisk } from './format.mjs';
import { parseConnection } from './parse.mjs';

// ── envelope factory ────────────────────────────────
export function makeEnvelope(mode) {
  return {
    mode,
    timestamp: new Date().toISOString(),
    connection: null,
    journeyOptions: null,
    departures: null,
    stations: null,
    liveStatus: null,
    trackStatus: null,
    assessment: null,
    errors: [],
    warnings: [],
  };
}

// ── helpers ──────────────────────────────────────────
export function toMinutes(hhmm) {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
}

export function todayDateStr() {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Europe/Berlin' });
}

export function mergeMessages(envelope, result) {
  if (result.warnings?.length) envelope.warnings.push(...result.warnings);
  if (result.errors?.length) envelope.errors.push(...result.errors);
}

/** Extract disruption/warning remarks from vendo leg, filtering junk */
export function extractRemarks(vendoLeg) {
  return (vendoLeg.remarks || [])
    .filter(r => {
      if (r.type !== 'status' && r.type !== 'warning') return false;
      // Filter internal codes and placeholder text
      const txt = (r.text || r.summary || '').trim();
      if (!txt || txt.startsWith('"') || txt.length < 5) return false;
      return true;
    })
    .map(r => {
      // Prefer full text over terse summary when summary is just a label
      const text = r.text || r.summary || '';
      const summary = r.summary || '';
      const useText = text.length > summary.length && summary.length < 60;
      return { type: r.type, text: useText ? text : summary };
    });
}

export function computeTransfers(legs, wantPredict) {
  const transfers = [];
  for (let i = 0; i < legs.length - 1; i++) {
    const arr = legs[i];
    const dep = legs[i + 1];

    let scheduledMinutes = toMinutes(dep.dep) - toMinutes(arr.arr);
    if (scheduledMinutes < 0) scheduledMinutes += 1440;

    const risk = transferRisk(scheduledMinutes).label;
    const platformFrom = arr.arrPlatform || null;
    const platformTo = dep.depPlatform || null;
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

    // Only compute catch probability when --predict is active
    if (wantPredict) {
      transfer.catchProb = predict.transferProb(scheduledMinutes, arr.category, dep.category);
    }

    transfers.push(transfer);
  }
  return transfers;
}

export function computeAssessment(legs, transfers) {
  const zugProb = predict.zugbindungProb(legs);

  let maxZbProb = 0;
  let mostLikelyLeg = null;
  for (const leg of legs) {
    const p = predict.zugbindungProbPerLeg(leg.category);
    if (p > maxZbProb) {
      maxZbProb = p;
      mostLikelyLeg = leg.train;
    }
  }

  const pAllTransfers = transfers.reduce((p, t) => p * (t.catchProb ?? 1), 1);
  const pNoCancellations = legs.reduce((p, l) => p * predict.legNotCancelledProb(l.category), 1);
  const pReaching = pAllTransfers * pNoCancellations;

  let verdict;
  if (zugProb > 0.90) {
    verdict = 'Zugbindung release highly likely (>90%).';
  } else if (zugProb > 0.70) {
    verdict = 'Zugbindung release probable (>70%).';
  } else if (zugProb > 0.50) {
    verdict = 'Zugbindung release unlikely (<50%).';
  } else {
    verdict = 'Zugbindung release very unlikely (<50%).';
  }

  return {
    zugbindung: { prob: zugProb, mostLikelyLeg },
    reach: { pAllTransfers, pNoCancellations, pReaching },
    verdict,
  };
}

function readStdin() {
  return readFileSync(0, 'utf8');
}

export function loadConnection(file) {
  let raw;
  if (file && file !== '-') {
    raw = readFileSync(file, 'utf8');
  } else {
    raw = readStdin();
  }

  const trimmed = raw.trim();

  // Auto-detect: if it starts with { it's JSON, otherwise plaintext
  if (trimmed.startsWith('{')) {
    return { conn: JSON.parse(trimmed), saved: false };
  }

  // Plaintext → parse and save to connections/active.json
  const conn = parseConnection(trimmed);
  mkdirSync('connections', { recursive: true });
  writeFileSync('connections/active.json', JSON.stringify(conn, null, 2) + '\n');
  return { conn, saved: true };
}
