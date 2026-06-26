/**
 * predict.mjs — Pure exponential delay model.
 * Opt-in via --predict. No historical data, no network calls.
 * Returns connection-level assessment: transfer catch probs, zugbindung prob, verdict.
 * thx bahn-vorhersage!
*/

const PROFILES = {
  ICE:  { mean: 5.0,  cancel: 0.055 },
  IC:   { mean: 4.0,  cancel: 0.04 },
  EC:   { mean: 4.0,  cancel: 0.04 },
  ECE:  { mean: 5.0,  cancel: 0.05 },
  TGV:  { mean: 3.5,  cancel: 0.03 },
  EN:   { mean: 7.0,  cancel: 0.06 },
  NJ:   { mean: 7.0,  cancel: 0.06 },
  FLX:  { mean: 4.5,  cancel: 0.04 },
  RJ:   { mean: 4.0,  cancel: 0.03 },
  IRE:  { mean: 2.5,  cancel: 0.02 },
  RE:   { mean: 2.5,  cancel: 0.02 },
  RB:   { mean: 2.0,  cancel: 0.015 },
  S:    { mean: 1.5,  cancel: 0.01 },
  STR:  { mean: 2.0,  cancel: 0.01 },
  Bus:  { mean: 3.0,  cancel: 0.02 },
};
const DEFAULT_PROFILE = { mean: 3.5, cancel: 0.03 };

const MIN_WALK_TIME = 2;

export function getProfile(lineName) {
  if (!lineName) return DEFAULT_PROFILE;
  const cat = lineName.match(/^(ICE|IC|EC|ECE|TGV|EN|NJ|FLX|RJ|IRE|RE|RB|STR|S|Bus)/i)?.[1];
  if (!cat) return DEFAULT_PROFILE;
  return PROFILES[cat.toUpperCase()] || PROFILES[cat.charAt(0).toUpperCase() + cat.slice(1)] || DEFAULT_PROFILE;
}

/**
 * P(catching transfer) given scheduled buffer and two train categories.
 * Closed-form convolution of two independent exponentials.
 */
export function transferProb(scheduledTransferMin, arrLine, depLine) {
  const arr = getProfile(arrLine);
  const dep = getProfile(depLine);
  const la = 1 / arr.mean;
  const ld = 1 / dep.mean;
  const buffer = scheduledTransferMin - MIN_WALK_TIME;

  if (buffer >= 0) {
    return 1 - Math.exp(-la * buffer) * ld / (la + ld);
  }
  return la / (la + ld) * Math.exp(ld * buffer);
}

/**
 * P(catching transfer) when arriving train's delay is already known.
 */
export function transferProbWithKnownDelay(knownArrDelayMin, depLineName, bufferMin) {
  const ld = 1 / getProfile(depLineName).mean;
  return Math.exp(-ld * Math.max(0, knownArrDelayMin - bufferMin));
}

export function legNotCancelledProb(lineName) {
  return 1 - getProfile(lineName).cancel;
}

export function zugbindungProbPerLeg(category) {
  const mean = getProfile(category).mean;
  return Math.exp(-20 / mean);
}

export function zugbindungProb(legs) {
  return 1 - legs.reduce((prod, leg) => prod * (1 - zugbindungProbPerLeg(leg.category)), 1);
}
