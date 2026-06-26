import { describe, it, expect } from 'vitest';
import { main } from './index.js';

const FRESH_TS = new Date().toISOString();
const STALE_TS = '2020-01-01T00:00:00.000Z';

function makeRecord(overrides: Record<string, unknown> = {}) {
  return {
    id: 'r1',
    kind: 'fact',
    entity: 'TestEntity',
    content: 'observed a confirmed result',
    timestamp: FRESH_TS,
    provenance: { sourceId: 'src1', sourceLabel: 'Source 1', capturedAt: FRESH_TS },
    ...overrides,
  };
}

describe('main', () => {
  it('returns exactly { markdown, json, report } keys', () => {
    const result = main('');
    expect(Object.keys(result).sort()).toEqual(['json', 'markdown', 'report']);
  });

  it('empty string → no throw, all array fields empty, input_count 0', () => {
    const { report } = main('');
    expect(report.input_count).toBe(0);
    expect(report.deduped_count).toBe(0);
    expect(report.conflicts).toHaveLength(0);
    expect(report.archived).toHaveLength(0);
    expect(report.schema_violations).toHaveLength(0);
    expect(report.provenance_chain).toHaveLength(0);
  });

  it('non-array JSON → empty report (no throw)', () => {
    const { report } = main(JSON.stringify({ not: 'an array' }));
    expect(report.input_count).toBe(0);
  });

  it('invalid JSON → empty report (no throw)', () => {
    const { report } = main('{ bad json }}');
    expect(report.input_count).toBe(0);
  });

  it('idempotent: identical input produces structurally identical output', () => {
    const input = JSON.stringify([makeRecord()]);
    const a = main(input);
    const b = main(input);
    expect(a.json).toBe(b.json);
    expect(a.markdown).toBe(b.markdown);
    expect(a.report.input_count).toBe(b.report.input_count);
    expect(a.report.deduped_count).toBe(b.report.deduped_count);
  });

  it('markdown is a non-empty string containing the report header', () => {
    const { markdown } = main(JSON.stringify([makeRecord()]));
    expect(typeof markdown).toBe('string');
    expect(markdown).toContain('# Memory Adjudication Report');
  });

  it('json round-trips to the report object', () => {
    const input = JSON.stringify([makeRecord()]);
    const { json, report } = main(input);
    expect(JSON.parse(json)).toEqual(report);
  });

  it('input_count reflects parsed records count', () => {
    const records = [makeRecord({ id: 'a' }), makeRecord({ id: 'b' })];
    const { report } = main(JSON.stringify(records));
    expect(report.input_count).toBe(2);
  });

  it('deduped_count ≤ input_count', () => {
    const records = [
      makeRecord({ id: 'a' }),
      makeRecord({ id: 'b' }), // same kind+entity → deduped
    ];
    const { report } = main(JSON.stringify(records));
    expect(report.deduped_count).toBeLessThanOrEqual(report.input_count);
  });

  it('deduplication reduces count when kind+entity match', () => {
    const records = [
      makeRecord({ id: 'a', timestamp: '2024-01-01T00:00:00Z' }),
      makeRecord({ id: 'b', timestamp: '2024-01-02T00:00:00Z' }),
    ];
    const { report } = main(JSON.stringify(records));
    expect(report.input_count).toBe(2);
    expect(report.deduped_count).toBe(1);
  });

  it('classified sums equal deduped_count', () => {
    const records = [
      makeRecord({ id: 'a', content: 'observed confirmed result' }),
      makeRecord({ id: 'b', kind: 'goal', entity: 'Goal1', content: 'intend to achieve target' }),
    ];
    const { report } = main(JSON.stringify(records));
    const total = report.classified['fact'] + report.classified['goal'] + report.classified['speculation'];
    expect(total).toBe(report.deduped_count);
  });

  it('stale records appear in archived', () => {
    const records = [makeRecord({ id: 'stale', timestamp: STALE_TS })];
    const { report } = main(JSON.stringify(records));
    expect(report.archived.length).toBeGreaterThan(0);
    expect(report.archived[0].id).toBe('stale');
  });

  it('fresh records do not appear in archived', () => {
    const records = [makeRecord({ id: 'fresh', timestamp: FRESH_TS })];
    const { report } = main(JSON.stringify(records));
    expect(report.archived).toHaveLength(0);
  });

  it('provenance_chain contains unique sourceIds', () => {
    const records = [
      makeRecord({ id: 'a', provenance: { sourceId: 'src1', sourceLabel: 'S1', capturedAt: FRESH_TS } }),
      makeRecord({ id: 'b', entity: 'Other', provenance: { sourceId: 'src1', sourceLabel: 'S1', capturedAt: FRESH_TS } }),
    ];
    const { report } = main(JSON.stringify(records));
    const ids = report.provenance_chain.map(p => p.sourceId);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('conflicts detected for contradicting records on same entity', () => {
    // Different kinds prevent deduplication; same entity causes conflict detection
    const records = [
      makeRecord({ id: 'p', kind: 'fact', entity: 'Server', content: 'The server has 100 connections' }),
      makeRecord({ id: 'q', kind: 'speculation', entity: 'Server', content: 'The server has 200 connections' }),
    ];
    const { report } = main(JSON.stringify(records));
    // numeric divergence: 100 vs 200 is > 10% apart
    expect(report.conflicts.length).toBeGreaterThan(0);
  });
});
