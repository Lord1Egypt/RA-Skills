import type { MemoryRecord, RecordId, RecordKind, ProvenanceInfo } from './types';

export interface ParseError {
  index: number;
  field?: string;
  message: string;
}

const allowedKinds = new Set<string>(['fact', 'goal', 'speculation']);

function isProvenanceInfo(value: unknown): value is ProvenanceInfo {
  if (typeof value !== 'object' || value === null) return false;
  const v = value as Record<string, unknown>;
  return (
    typeof v['sourceId'] === 'string' &&
    typeof v['sourceLabel'] === 'string' &&
    typeof v['capturedAt'] === 'string'
  );
}

export function parseRecords(raw: unknown): { records: MemoryRecord[]; errors: ParseError[] } {
  if (!Array.isArray(raw)) {
    return {
      records: [],
      errors: [{ index: -1, message: 'Input is not an array' }],
    };
  }

  const records: MemoryRecord[] = [];
  const errors: ParseError[] = [];

  for (let i = 0; i < raw.length; i++) {
    const elem = raw[i];
    const elemErrors: ParseError[] = [];

    if (typeof elem !== 'object' || elem === null || Array.isArray(elem)) {
      errors.push({ index: i, message: 'Element is not an object' });
      continue;
    }

    const obj = elem as Record<string, unknown>;

    if (typeof obj['id'] !== 'string' || obj['id'] === '') {
      elemErrors.push({ index: i, field: 'id', message: 'Field "id" must be a non-empty string' });
    }

    if (typeof obj['kind'] !== 'string') {
      elemErrors.push({ index: i, field: 'kind', message: 'Field "kind" must be a string' });
    } else if (!allowedKinds.has(obj['kind'])) {
      elemErrors.push({
        index: i,
        field: 'kind',
        message: `Field "kind" has invalid value "${obj['kind']}"; allowed: fact, goal, speculation`,
      });
    }

    if (typeof obj['entity'] !== 'string' || obj['entity'] === '') {
      elemErrors.push({ index: i, field: 'entity', message: 'Field "entity" must be a non-empty string' });
    }

    if (typeof obj['content'] !== 'string') {
      elemErrors.push({ index: i, field: 'content', message: 'Field "content" must be a string' });
    }

    if (typeof obj['timestamp'] !== 'string' || obj['timestamp'] === '') {
      elemErrors.push({ index: i, field: 'timestamp', message: 'Field "timestamp" must be a non-empty string' });
    }

    if (!isProvenanceInfo(obj['provenance'])) {
      elemErrors.push({
        index: i,
        field: 'provenance',
        message: 'Field "provenance" must be an object with sourceId, sourceLabel, and capturedAt strings',
      });
    }

    if (elemErrors.length > 0) {
      errors.push(...elemErrors);
    } else {
      const record: MemoryRecord = {
        id: obj['id'] as RecordId,
        kind: obj['kind'] as RecordKind,
        entity: obj['entity'] as string,
        content: obj['content'] as string,
        timestamp: obj['timestamp'] as string,
        provenance: [obj['provenance'] as ProvenanceInfo],
      };
      if (Array.isArray(obj['tags'])) {
        record.tags = obj['tags'] as string[];
      }
      records.push(record);
    }
  }

  return { records, errors };
}
