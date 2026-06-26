import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { dirname } from "path";

/**
 * Shared on-disk state for recipe scripts. One schema per skill:
 * { lastStreamEpoch, lastEmittedBlock, emittedFingerprints: string[] }
 */
export function loadState(file) {
  if (!existsSync(file)) {
    return {
      lastStreamEpoch: null,
      lastEmittedBlock: 0,
      emittedFingerprints: [],
    };
  }
  try {
    const j = JSON.parse(readFileSync(file, "utf8"));
    return {
      lastStreamEpoch: j.lastStreamEpoch ?? null,
      lastEmittedBlock: j.lastEmittedBlock ?? 0,
      emittedFingerprints: Array.isArray(j.emittedFingerprints)
        ? j.emittedFingerprints
        : [],
    };
  } catch {
    return {
      lastStreamEpoch: null,
      lastEmittedBlock: 0,
      emittedFingerprints: [],
    };
  }
}

export function saveState(file, state) {
  const dir = dirname(file);
  try {
    mkdirSync(dir, { recursive: true });
  } catch {
    /* exists */
  }
  writeFileSync(file, JSON.stringify(state, null, 2));
}

export function fingerprintTrade(t) {
  const tx = t.log?.transactionHash || t.transactionHash || "";
  const bn = t.log?.blockNumber ?? t.blockNumber ?? "";
  return `${tx}:${bn}`;
}

export function rememberFingerprint(state, fp, max = 500) {
  const next = [...state.emittedFingerprints, fp];
  while (next.length > max) next.shift();
  state.emittedFingerprints = next;
}

export function wasEmitted(state, fp) {
  return state.emittedFingerprints.includes(fp);
}
