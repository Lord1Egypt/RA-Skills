import { describe, it, expect } from 'vitest';
import { parseRecords } from './parse';

const validProvenance = {
  sourceId: 'src-1',
  sourceLabel: 'agent-log',
  capturedAt: '2024-01-01T00:00:00Z',
};

describe('parseRecords', () => {
  it('returns records with no errors when input is a valid array', () => {
    const input = [
      {
        id: 'r1',
        kind: 'fact',
        entity: 'Alice',
        content: 'Alice is a senior engineer.',
        timestamp: '2024-01-01T00:00:00Z',
        provenance: validProvenance,
      },
      {
        id: 'r2',
        kind: 'goal',
        entity: 'Bob',
        content: 'Bob wants to lead the platform team.',
        timestamp: '2024-01-02T00:00:00Z',
        provenance: validProvenance,
      },
    ];
    const { records, errors } = parseRecords(input);
    expect(errors).toHaveLength(0);
    expect(records).toHaveLength(2);
    expect(records[0].id).toBe('r1');
    expect(records[1].kind).toBe('goal');
  });

  it('returns error entry and skips element when a required field is missing', () => {
    const input = [
      {
        // missing 'id'
        kind: 'fact',
        entity: 'Bob',
        content: 'Bob is on the platform team.',
        timestamp: '2024-01-02T00:00:00Z',
        provenance: validProvenance,
      },
    ];
    const { records, errors } = parseRecords(input);
    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0].field).toBe('id');
    expect(records).toHaveLength(0);
  });

  it('collects errors for all invalid elements and still returns valid ones', () => {
    const input = [
      {
        id: 'r1',
        kind: 'fact',
        entity: 'Alice',
        content: 'Alice is a senior engineer.',
        timestamp: '2024-01-01T00:00:00Z',
        provenance: validProvenance,
      },
      {
        // missing 'id'
        kind: 'fact',
        entity: 'Bob',
        content: 'Bob is on the platform team.',
        timestamp: '2024-01-02T00:00:00Z',
        provenance: validProvenance,
      },
    ];
    const { records, errors } = parseRecords(input);
    expect(records).toHaveLength(1);
    expect(errors.length).toBeGreaterThan(0);
  });
});
