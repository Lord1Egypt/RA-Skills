import { describe, it, expect } from 'vitest';
import { classifyRecords } from './classify';
import type { MemoryRecord, RecordId } from './types';

function id(s: string): RecordId {
  return s as RecordId;
}

function makeRecord(
  overrides: Partial<MemoryRecord> & { id: RecordId; content: string },
): MemoryRecord {
  return {
    id: overrides.id,
    kind: overrides.kind ?? 'fact',
    entity: overrides.entity ?? 'test-entity',
    content: overrides.content,
    timestamp: overrides.timestamp ?? '2024-01-01T00:00:00Z',
    provenance: overrides.provenance ?? [
      { sourceId: overrides.id, sourceLabel: 'test', capturedAt: '2024-01-01T00:00:00Z' },
    ],
  };
}

describe('classifyRecords', () => {
  it('clear-fact: confirmed+verified body classifies as fact with positive confidence', () => {
    const rec = makeRecord({
      id: id('t1'),
      content: 'The results were confirmed and verified by the team',
    });
    const [result] = classifyRecords([rec]);
    expect(result.kind).toBe('fact');
    expect(result.confidence).toBeGreaterThan(0);
  });

  it('clear-goal: intend+must+objective body classifies as goal with positive confidence', () => {
    const rec = makeRecord({
      id: id('t2'),
      content: 'We intend to achieve the objective and must complete the deployment',
    });
    const [result] = classifyRecords([rec]);
    expect(result.kind).toBe('goal');
    expect(result.confidence).toBeGreaterThan(0);
  });

  it('clear-speculation: might+possibly body classifies as speculation with positive confidence', () => {
    const rec = makeRecord({
      id: id('t3'),
      content: 'The server might be overloaded possibly due to high traffic',
    });
    const [result] = classifyRecords([rec]);
    expect(result.kind).toBe('speculation');
    expect(result.confidence).toBeGreaterThan(0);
  });

  it('ambiguous-fallback: body with no classification markers returns fact with confidence 0', () => {
    // No tokens from any keyword list — maxScore stays below MIN_THRESHOLD
    const rec = makeRecord({
      id: id('t4'),
      content: 'the data was processed and stored on the remote server',
    });
    const [result] = classifyRecords([rec]);
    expect(result.kind).toBe('fact');
    expect(result.confidence).toBe(0);
  });

  it('mixed-signal: fact markers dominate goal markers; outcome is the same on two calls', () => {
    // factScore: confirmed(2.0) + verified(2.0) = 4.0 over 10 tokens = 0.4
    // goalScore: intend(2.0) = 2.0 over 10 tokens = 0.2 — fact wins
    const rec = makeRecord({
      id: id('t5'),
      content: 'The experiment confirmed and verified the approach intend to extend',
    });
    const [first] = classifyRecords([rec]);
    const [second] = classifyRecords([rec]);
    expect(first.kind).toBe('fact');
    expect(second.kind).toBe(first.kind);
    expect(second.confidence).toBe(first.confidence);
  });

  it('empty-body: record with body === "" returns fact with confidence 0 without throwing', () => {
    const rec = makeRecord({ id: id('t6'), content: '' });
    expect(() => classifyRecords([rec])).not.toThrow();
    const [result] = classifyRecords([rec]);
    expect(result.kind).toBe('fact');
    expect(result.confidence).toBe(0);
  });
});
