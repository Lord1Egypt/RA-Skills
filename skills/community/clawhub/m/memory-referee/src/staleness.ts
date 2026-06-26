import type { MemoryRecord } from './types';

export interface ArchiveCandidate {
  record: MemoryRecord;
  ageMs: number;
  reason: string;
}

export interface StalenessResult {
  fresh: MemoryRecord[];
  archiveCandidates: ArchiveCandidate[];
}

/**
 * Parse a raw timestamp value into a Unix-ms number.
 *
 * Accepts a numeric epoch (ms) or an ISO-8601 string. Returns NaN for
 * anything missing, non-finite, or unparseable. Never throws.
 */
function parseTimestamp(value: unknown): number {
  if (value === undefined || value === null) {
    return NaN;
  }
  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : NaN;
  }
  if (typeof value === 'string' && value !== '') {
    const parsed = Date.parse(value);
    return Number.isFinite(parsed) ? parsed : NaN;
  }
  return NaN;
}

/** Default TTL for memory records: 7 days in milliseconds. */
export const DEFAULT_TTL = 7 * 24 * 60 * 60 * 1000;

/**
 * Partition records into fresh vs. archive candidates based on age.
 *
 * A record is stale when its age in ms is strictly greater than ttlMs.
 * A record at exactly (Date.now() - ttlMs) is considered fresh.
 *
 * Records with missing or unparseable timestamps are always placed in
 * archiveCandidates with ageMs = -1 and reason = 'invalid-timestamp'.
 *
 * Input records are never mutated.
 *
 * @param records - Records to evaluate.
 * @param ttlMs   - Time-to-live in milliseconds (non-negative integer).
 */
export function checkStaleness(records: MemoryRecord[], ttlMs: number): StalenessResult {
  if (records.length === 0) {
    return { fresh: [], archiveCandidates: [] };
  }

  const now = Date.now();
  const fresh: MemoryRecord[] = [];
  const archiveCandidates: ArchiveCandidate[] = [];

  for (const record of records) {
    // Access the field as unknown to handle runtime numeric values despite the
    // TypeScript type declaring timestamp as string.
    const rawTs: unknown = (record as unknown as Record<string, unknown>)['timestamp'];
    const ts = parseTimestamp(rawTs);

    if (!Number.isFinite(ts)) {
      archiveCandidates.push({ record, ageMs: -1, reason: 'invalid-timestamp' });
      continue;
    }

    const ageMs = now - ts;
    if (ageMs > ttlMs) {
      archiveCandidates.push({ record, ageMs, reason: 'ttl-exceeded' });
    } else {
      fresh.push(record);
    }
  }

  return { fresh, archiveCandidates };
}
