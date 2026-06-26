import { describe, it, expect } from 'vitest';
import { deduplicateRecords } from './dedupe';
import type { MemoryRecord, RecordId } from './types';

function id(s: string): RecordId {
  return s as RecordId;
}

function rec(
  rid: string,
  entity: string,
  kind: MemoryRecord['kind'],
  provSourceId: string,
): MemoryRecord {
  return {
    id: id(rid),
    kind,
    entity,
    content: 'content',
    timestamp: '2024-01-01T00:00:00Z',
    provenance: [{ sourceId: provSourceId, sourceLabel: 'test', capturedAt: '2024-01-01T00:00:00Z' }],
  };
}

describe('deduplicateRecords', () => {
  it('exact-duplicate: two records with same entity and kind produce one output record', () => {
    const a = rec('r1', 'Alice', 'fact', 's1');
    const b = rec('r2', 'Alice', 'fact', 's2');
    const { deduped, merged } = deduplicateRecords([a, b]);
    expect(deduped).toHaveLength(1);
    expect(merged).toHaveLength(1);
    expect(merged[0].strategy).toBe('name+type');
  });

  it('case-normalised-duplicate: names differing only by case merge into one record', () => {
    const a = rec('r1', 'Alice', 'fact', 's1');
    const b = rec('r2', 'alice', 'fact', 's2');
    const { deduped, merged } = deduplicateRecords([a, b]);
    expect(deduped).toHaveLength(1);
    expect(merged).toHaveLength(1);
  });

  it('type-mismatch-non-merge: same entity name but different kinds preserves both records', () => {
    const a = rec('r1', 'Alice', 'fact', 's1');
    const b = rec('r2', 'Alice', 'goal', 's2');
    const { deduped, merged } = deduplicateRecords([a, b]);
    expect(deduped).toHaveLength(2);
    expect(merged).toHaveLength(0);
  });

  it('provenance-preserved: merged record contains both distinct provenance entries', () => {
    const a = rec('r1', 'Alice', 'fact', 'src-a');
    const b = rec('r2', 'alice', 'fact', 'src-b');
    const { deduped } = deduplicateRecords([a, b]);
    expect(deduped).toHaveLength(1);
    const provSourceIds = deduped[0].provenance.map(p => p.sourceId);
    expect(provSourceIds).toHaveLength(2);
    expect(provSourceIds).toContain('src-a');
    expect(provSourceIds).toContain('src-b');
  });

  it('triple-merge: three duplicates produce one record with three provenance entries and deduping the output is idempotent', () => {
    const a = rec('r1', 'Bob', 'fact', 'src-1');
    const b = rec('r2', 'bob', 'fact', 'src-2');
    const c = rec('r3', 'BOB', 'fact', 'src-3');
    const { deduped } = deduplicateRecords([a, b, c]);
    expect(deduped).toHaveLength(1);
    expect(deduped[0].provenance).toHaveLength(3);

    const { deduped: deduped2, merged: merged2 } = deduplicateRecords(deduped);
    expect(deduped2).toHaveLength(1);
    expect(merged2).toHaveLength(0);
  });

  it('empty-input: returns empty arrays without error', () => {
    const { deduped, merged } = deduplicateRecords([]);
    expect(deduped).toEqual([]);
    expect(merged).toEqual([]);
  });
});
