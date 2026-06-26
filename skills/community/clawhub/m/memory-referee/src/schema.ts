import type { MemoryRecord, RecordKind } from './types.js';

export interface FieldError {
  field: string;
  message: string;
}

export interface ValidationResult {
  id: string;
  valid: boolean;
  errors: FieldError[];
}

const allowedKinds: readonly RecordKind[] = ['fact', 'goal', 'speculation'];

/**
 * Validate an array of MemoryRecords against required field constraints.
 *
 * Returns one ValidationResult per input element. All field errors for a
 * record are collected before advancing — never aborts on first violation.
 * Input records are not mutated.
 */
export function validateRecords(records: MemoryRecord[]): ValidationResult[] {
  return (records as unknown[]).map(validateOne);
}

function validateOne(raw: unknown): ValidationResult {
  if (raw === null || Array.isArray(raw) || typeof raw !== 'object') {
    const received =
      raw === null ? 'null' : Array.isArray(raw) ? 'array' : typeof raw;
    return {
      id: '',
      valid: false,
      errors: [
        {
          field: 'record',
          message: `expected a plain object, got ${received}`,
        },
      ],
    };
  }

  const r = raw as Record<string, unknown>;
  const errors: FieldError[] = [];

  const id = r['id'];
  if (typeof id !== 'string' || id === '') {
    const got =
      id === undefined
        ? 'undefined'
        : typeof id === 'string'
          ? 'empty string'
          : typeof id;
    errors.push({ field: 'id', message: `id: expected a non-empty string, got ${got}` });
  }

  const entity = r['entity'];
  if (typeof entity !== 'string' || entity === '') {
    const got =
      entity === undefined
        ? 'undefined'
        : typeof entity === 'string'
          ? 'empty string'
          : typeof entity;
    errors.push({
      field: 'entity',
      message: `entity: expected a non-empty string, got ${got}`,
    });
  }

  const content = r['content'];
  if (typeof content !== 'string' || content === '') {
    const got =
      content === undefined
        ? 'undefined'
        : typeof content === 'string'
          ? 'empty string'
          : typeof content;
    errors.push({
      field: 'content',
      message: `content: expected a non-empty string, got ${got}`,
    });
  }

  const kind = r['kind'];
  if (!(allowedKinds as readonly unknown[]).includes(kind)) {
    const got = kind === undefined ? 'undefined' : JSON.stringify(kind);
    errors.push({
      field: 'kind',
      message: `kind: expected one of ${allowedKinds.join(', ')}, got ${got}`,
    });
  }

  const ts = r['timestamp'];
  let tsValid = false;
  if (typeof ts === 'number') {
    tsValid = Number.isFinite(ts);
  } else if (typeof ts === 'string') {
    tsValid = !Number.isNaN(Date.parse(ts));
  }
  if (!tsValid) {
    const got =
      ts === undefined
        ? 'undefined'
        : typeof ts === 'number'
          ? String(ts)
          : JSON.stringify(ts);
    errors.push({
      field: 'timestamp',
      message: `timestamp: expected a finite number or parseable date string, got ${got}`,
    });
  }

  const confidence = r['confidence'];
  if (confidence !== undefined) {
    if (
      typeof confidence !== 'number' ||
      !Number.isFinite(confidence) ||
      confidence < 0 ||
      confidence > 1
    ) {
      const got =
        typeof confidence === 'number'
          ? String(confidence)
          : typeof confidence;
      errors.push({
        field: 'confidence',
        message: `confidence: expected number in [0,1], got ${got}`,
      });
    }
  }

  return {
    id: typeof id === 'string' ? id : '',
    valid: errors.length === 0,
    errors,
  };
}
