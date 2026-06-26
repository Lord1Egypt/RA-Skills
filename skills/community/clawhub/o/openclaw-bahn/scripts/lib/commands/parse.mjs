import * as data from '../data.mjs';
import { getLegHistoricalStats } from '../stats.mjs';
import {
  makeEnvelope,
  mergeMessages,
  extractRemarks,
  computeTransfers,
  computeAssessment,
  loadConnection,
} from '../helpers.mjs';

/**
 * --parse [file|stdin]  [--stats] [--predict] [--json]
 * Parses a DB Navigator connection share text (stdin) or loads a JSON file.
 * Enriches with vendo disruption remarks, optional historical stats, and
 * optional predict-model assessment.
 * Returns an Envelope with the parsed connection.
 */
export default async function parse({ flags, positional }) {
  const file = typeof flags.parse === 'string' ? flags.parse : positional[0] || null;
  const wantPredict = !!flags.predict;
  const wantStats = !!flags.stats;
  const envelope = makeEnvelope('parse');

  let conn, saved;
  try {
    ({ conn, saved } = loadConnection(file));
  } catch (err) {
    envelope.errors.push(`Failed to load connection: ${err.message}`);
    return envelope;
  }

  if (saved) {
    envelope.warnings.push('Parsed plaintext → saved to connections/active.json');
  }

  const { date, from, to, legs } = conn;

  // Look up the journey via vendo to get disruption remarks per leg
  let vendoRemarks = new Map(); // leg index → remarks[]
  try {
    const firstDep = legs[0]?.dep;
    const result = await data.getJourneys(from, to, date, firstDep, { results: 3 });
    mergeMessages(envelope, result);
    const journeys = Array.isArray(result.data) ? result.data : [];

    // Match the vendo journey to our parsed legs by comparing train names
    for (const journey of journeys) {
      const vendoLegs = (journey.legs || []).filter(l => !l.walking);
      if (vendoLegs.length !== legs.length) continue;

      let matched = true;
      for (let i = 0; i < legs.length; i++) {
        const vName = vendoLegs[i].line?.name || '';
        const pTrain = legs[i].train || '';
        // Match if vendo name appears in parsed train or parsed category+number starts with vendo name
        if (!pTrain.includes(vName) && !vName.includes(pTrain.split(' ')[0])) {
          matched = false;
          break;
        }
      }

      if (matched) {
        for (let i = 0; i < vendoLegs.length; i++) {
          const remarks = extractRemarks(vendoLegs[i]);
          if (remarks.length) vendoRemarks.set(i, remarks);
        }
        break;
      }
    }
  } catch {
    // vendo disruption lookup is best-effort
  }

  // Enrich legs with disruption remarks from vendo
  const enrichedLegs = [];
  for (let i = 0; i < legs.length; i++) {
    const leg = legs[i];
    const remarks = vendoRemarks.get(i) || [];
    const enriched = { ...leg, remarks };

    // --stats: fetch historical bahn.expert data per leg
    if (wantStats) {
      const hist = await getLegHistoricalStats(leg, data);
      if (hist) enriched.historicalStats = hist;
    }

    enrichedLegs.push(enriched);
  }

  const transfers = computeTransfers(legs, wantPredict);

  // --predict: connection-level assessment at the end
  const assessment = wantPredict ? computeAssessment(legs, transfers) : null;

  envelope.connection = { date, from, to, legs: enrichedLegs, transfers };
  envelope.assessment = assessment;
  return envelope;
}
