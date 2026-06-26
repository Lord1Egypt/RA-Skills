import { describe, it, expect } from 'vitest';
import { checkStaleness, DEFAULT_TTL } from './staleness';
import type { MemoryRecord, RecordId } from './types';

const RECORDED_AT = 1_700_000_000_000; // 2023-11-14T22:13:20.000Z

function rec(ts: string): MemoryRecord {
  return {
    id: 'r1' as RecordId,
    kind: 'fact',
    entity: 'test-entity',
    content: 'test content',
    timestamp: ts,
    provenance: [{ sourceId: 'r1', sourceLabel: 'test', capturedAt: ts }],
  };
}

describe('checkStaleness', () => {
  it('archives records older than the TTL', () => {
    const { fresh, archiveCandidates } = checkStaleness([rec(new Date(RECORDED_AT).toISOString())], DEFAULT_TTL);
    expect(fresh).toHaveLength(0);
    expect(archiveCandidates).toHaveLength(1);
    expect(archiveCandidates[0].reason).toBe('ttl-exceeded');
  });

  it('keeps records younger than the TTL as fresh', () => {
    // A future timestamp is guaranteed within any reasonable TTL
    const { fresh, archiveCandidates } = checkStaleness([rec(new Date(Date.now() + 1000).toISOString())], DEFAULT_TTL);
    expect(fresh).toHaveLength(1);
    expect(archiveCandidates).toHaveLength(0);
  });

  it('archives records with unparseable timestamps under reason invalid-timestamp', () => {
    const { archiveCandidates } = checkStaleness([rec('not-a-date')], DEFAULT_TTL);
    expect(archiveCandidates[0].ageMs).toBe(-1);
    expect(archiveCandidates[0].reason).toBe('invalid-timestamp');
  });
});
