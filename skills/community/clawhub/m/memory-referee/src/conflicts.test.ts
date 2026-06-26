import { describe, it, expect } from 'vitest';
import { detectConflicts } from './conflicts';
import type { MemoryRecord, RecordId } from './types';

function id(s: string): RecordId {
  return s as RecordId;
}

function rec(
  rid: string,
  entity: string,
  content: string,
  extra: Partial<MemoryRecord> = {},
): MemoryRecord {
  return {
    id: id(rid),
    kind: 'fact',
    entity,
    content,
    timestamp: '2024-01-01T00:00:00.000Z',
    provenance: [{ sourceId: rid, sourceLabel: 'test', capturedAt: '2024-01-01T00:00:00.000Z' }],
    ...extra,
  };
}

describe('detectConflicts', () => {
  it('direct contradiction: same subject+predicate, differing value → exactly one ConflictPair', () => {
    // Negation proximity: "not" in B fires near shared noun "active" (and others).
    const a = rec('r1', 'project-alpha', 'project alpha status is active');
    const b = rec('r2', 'project-alpha', 'project alpha status is not active');
    const result = detectConflicts([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].a).toBe(a);
    expect(result[0].b).toBe(b);
    expect(result[0].reason).toMatch(/negation proximity/);
  });

  it('partial overlap: same subject, different predicates → empty array', () => {
    // Same entity, but content domains are disjoint — no shared nouns trigger negation,
    // and neither record contains a number.
    const a = rec('r3', 'api-gateway', 'api gateway uses oauth2 for authentication');
    const b = rec('r4', 'api-gateway', 'api gateway deployed in kubernetes');
    expect(detectConflicts([a, b])).toHaveLength(0);
  });

  it('same-subject no conflict: identical subject+predicate+value (exact duplicate) → empty array', () => {
    // Identical content has no negation and equal numbers; no signal fires.
    const a = rec('r5', 'cache', 'cache status is active');
    const b = rec('r6', 'cache', 'cache status is active');
    expect(detectConflicts([a, b])).toHaveLength(0);
  });

  it('multi-record chain: [0]↔[1] conflict, [1]↔[2] no conflict → exactly one ConflictPair for [0] and [1]', () => {
    // Numeric divergence: A=2 vs B=50 fires (96% apart).
    // B=50 vs C (no number) does not fire — numeric signal requires exactly one number per record.
    // A=2 vs C (no number) does not fire for the same reason.
    const a = rec('r7', 'replica', 'replica count is 2');
    const b = rec('r8', 'replica', 'replica count is 50');
    const c = rec('r9', 'replica', 'replica pool is scaling horizontally');
    const result = detectConflicts([a, b, c]);
    expect(result).toHaveLength(1);
    expect(result[0].a).toBe(a);
    expect(result[0].b).toBe(b);
  });

  it('resolved conflict excluded: record with resolvedAt is silently dropped from output', () => {
    // Without resolution marker, 3 vs 90 differs by 96% → would produce a ConflictPair.
    // With resolvedAt on b, detectConflicts must exclude b before pairing and return [].
    const a = rec('r10', 'deployment', 'deployment replica count is 3');
    const b = rec('r11', 'deployment', 'deployment replica count is 90', {
      resolvedAt: '2024-06-01T00:00:00.000Z',
    });
    expect(detectConflicts([a, b])).toHaveLength(0);
  });

  it('empty set: detectConflicts([]) returns [] without throwing', () => {
    expect(detectConflicts([])).toEqual([]);
  });
});
