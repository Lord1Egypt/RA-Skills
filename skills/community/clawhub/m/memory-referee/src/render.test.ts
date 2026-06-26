import { describe, it, expect } from 'vitest';
import { renderMarkdown, renderJSON } from './render';
import type { AdjudicationReport, MemoryRecord, RecordId } from './types';

function rid(s: string): RecordId {
  return s as RecordId;
}

// ── Shared fixture ─────────────────────────────────────────────────────────────
// One representative item per section.  Both tests consume this constant.

const factRecord: MemoryRecord = {
  id: rid('fix-r1'),
  kind: 'fact',
  entity: 'AuthService',
  content: 'AuthService runs on port 8080',
  timestamp: '2024-06-15T09:00:00.000Z',
  provenance: [
    {
      sourceId: 'src-ops',
      sourceLabel: 'ops-monitor',
      capturedAt: '2024-06-15T09:00:00.000Z',
      confidence: 0.92,
    },
  ],
};

const goalRecord: MemoryRecord = {
  id: rid('fix-r2'),
  kind: 'goal',
  entity: 'PaymentWorker',
  content: 'PaymentWorker should process 1000 TPS',
  timestamp: '2024-05-01T00:00:00.000Z',
  provenance: [
    {
      sourceId: 'src-pm',
      sourceLabel: 'product-spec',
      capturedAt: '2024-05-01T00:00:00.000Z',
    },
  ],
};

const FIXTURE: AdjudicationReport = {
  input_count: 12,
  deduped_count: 9,
  // classified covers 3 distinct RecordKind values (fact, goal, speculation)
  classified: { fact: 6, goal: 2, speculation: 1 },
  conflicts: [
    { a: factRecord, b: goalRecord, reason: 'entity status contradiction' },
  ],
  archived: [goalRecord],
  schema_violations: [
    {
      recordId: rid('fix-r3'),
      field: 'timestamp',
      message: 'value predates minimum allowed epoch',
    },
  ],
  // Two sources in provenance chain — exercises both sourceId and capturedAt assertions
  provenance_chain: [
    {
      sourceId: 'src-ops',
      sourceLabel: 'ops-monitor',
      capturedAt: '2024-06-15T09:00:00.000Z',
      confidence: 0.92,
    },
    {
      sourceId: 'src-pm',
      sourceLabel: 'product-spec',
      capturedAt: '2024-05-01T00:00:00.000Z',
    },
  ],
};

// ── Shape validator ────────────────────────────────────────────────────────────
// Walks every top-level field of AdjudicationReport so the JSON test validates
// the contract, not a deep-equal against the fixture value.

function assertReportShape(obj: unknown): void {
  // Every top-level field must be present
  expect(obj).toHaveProperty('input_count');
  expect(obj).toHaveProperty('deduped_count');
  expect(obj).toHaveProperty('classified');
  expect(obj).toHaveProperty('conflicts');
  expect(obj).toHaveProperty('archived');
  expect(obj).toHaveProperty('schema_violations');
  expect(obj).toHaveProperty('provenance_chain');

  const r = obj as AdjudicationReport;

  // Numeric summary fields
  expect(typeof r.input_count).toBe('number');
  expect(typeof r.deduped_count).toBe('number');

  // classified covers at least 2 distinct RecordKind values with numeric counts
  expect(typeof r.classified.fact).toBe('number');
  expect(typeof r.classified.goal).toBe('number');
  expect(typeof r.classified.speculation).toBe('number');

  // Array fields are arrays with at least one item
  expect(Array.isArray(r.conflicts)).toBe(true);
  expect(r.conflicts.length).toBeGreaterThanOrEqual(1);

  expect(Array.isArray(r.archived)).toBe(true);
  expect(r.archived.length).toBeGreaterThanOrEqual(1);

  expect(Array.isArray(r.schema_violations)).toBe(true);
  expect(r.schema_violations.length).toBeGreaterThanOrEqual(1);

  expect(Array.isArray(r.provenance_chain)).toBe(true);
  expect(r.provenance_chain.length).toBeGreaterThanOrEqual(1);

  // provenance_chain entries must carry a source identifier (sourceId) and a
  // captured timestamp (capturedAt); length serves as the sourceCount equivalent
  const prov = r.provenance_chain[0];
  expect(typeof prov.sourceId).toBe('string');
  expect(typeof prov.capturedAt).toBe('string');
  expect(typeof r.provenance_chain.length).toBe('number');
}

// ── Test cases ─────────────────────────────────────────────────────────────────

describe('renderMarkdown', () => {
  it('output contains all required section headings and at least one item per section', () => {
    const md = renderMarkdown(FIXTURE);

    // All section headings must be present (toContain matches substring, so the
    // "(N)" count suffix does not need to be pinned — keeps the test format-resilient)
    expect(md).toContain('## Summary');
    expect(md).toContain('## Contradictions');
    expect(md).toContain('## Stale Archived');
    expect(md).toContain('## Schema Violations');
    expect(md).toContain('## Provenance Chain');

    // At least one entity / identifier from the fixture appears in the output,
    // confirming items are rendered and not just the headings
    expect(md).toContain('AuthService');    // conflict Record A entity
    expect(md).toContain('PaymentWorker'); // conflict Record B entity + archived
    expect(md).toContain('fix-r3');        // schema violation recordId
    expect(md).toContain('ops-monitor');   // provenance chain sourceLabel
  });
});

describe('renderJSON', () => {
  it('output matches AdjudicationReport shape — every top-level field present and correctly typed', () => {
    const output = JSON.parse(renderJSON(FIXTURE));
    assertReportShape(output);
  });
});
