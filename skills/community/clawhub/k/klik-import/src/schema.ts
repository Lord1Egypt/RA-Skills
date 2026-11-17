import type { ImportPayload } from './types.ts';

const MAX_ITEMS = 5000;
const MAX_BYTES = 10 * 1024 * 1024;

export function validatePayload(payload: unknown): asserts payload is ImportPayload {
  if (!payload || typeof payload !== 'object') {
    throw new Error('payload must be an object');
  }
  const p = payload as Record<string, unknown>;

  if (!p.schema_version) throw new Error('missing schema_version');
  if (p.schema_version !== '1.0') throw new Error(`unsupported schema_version: ${p.schema_version}`);
  if (!p.client || typeof p.client !== 'object') throw new Error('missing client');
  if (!p.redaction || typeof p.redaction !== 'object') throw new Error('missing redaction');
  if (!Array.isArray(p.collectors)) throw new Error('collectors must be an array');

  let totalItems = 0;
  for (const c of p.collectors as unknown[]) {
    if (!c || typeof c !== 'object') throw new Error('each collector must be an object');
    const col = c as Record<string, unknown>;
    if (!col.name || typeof col.name !== 'string') throw new Error('collector missing name');
    if (!Array.isArray(col.items)) throw new Error(`collector ${col.name} missing items array`);
    totalItems += col.items.length;
  }

  if (totalItems > MAX_ITEMS) {
    throw new Error(`total items ${totalItems} exceeds limit ${MAX_ITEMS}`);
  }

  const bytes = Buffer.byteLength(JSON.stringify(p), 'utf8');
  if (bytes > MAX_BYTES) {
    throw new Error(`payload ${bytes} bytes exceeds 10 MB limit`);
  }
}
