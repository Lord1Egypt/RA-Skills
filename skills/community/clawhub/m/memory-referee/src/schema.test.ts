import { describe, it, expect } from 'vitest';
import { validateRecords } from './schema';
import type { MemoryRecord, RecordId } from './types';

const VALID: MemoryRecord = {
  id: 'r1' as RecordId,
  kind: 'fact',
  entity: 'test-entity',
  content: 'some content',
  timestamp: '2024-06-01T00:00:00.000Z',
  provenance: [{ sourceId: 'r1', sourceLabel: 'test', capturedAt: '2024-06-01T00:00:00.000Z' }],
};

describe('validateRecords — valid record', () => {
  it('returns valid:true with no errors for a fully-populated valid record', () => {
    const [result] = validateRecords([VALID]);
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });
});

describe('validateRecords — missing required field', () => {
  it('returns valid:false with an error that identifies the missing field by name', () => {
    const fixture = { ...VALID } as Record<string, unknown>;
    delete fixture['id'];

    const [result] = validateRecords([fixture as unknown as MemoryRecord]);

    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
    expect(result.errors.find(e => e.field === 'id')).toBeDefined();
  });
});
