import type { Edict, EdictInput, EdictFileSchema, HistoryEntry } from './types.js';
import { EdictValidationError } from './errors.js';
import { parseDuration } from './duration.js';

const VALID_CONFIDENCE = new Set(['verified', 'inferred', 'user']);
const VALID_TTL = new Set(['ephemeral', 'event', 'durable', 'permanent']);

export function validateEdictInput(input: EdictInput): void {
  if (!input.text || input.text.trim().length === 0) {
    throw new EdictValidationError('Edict text is required and cannot be empty');
  }

  if (!input.category || input.category.trim().length === 0) {
    throw new EdictValidationError('Edict category is required and cannot be empty');
  }

  if (input.confidence !== undefined && !VALID_CONFIDENCE.has(input.confidence)) {
    throw new EdictValidationError(
      `Invalid confidence "${input.confidence}". Must be: ${[...VALID_CONFIDENCE].join(', ')}`
    );
  }

  if (input.ttl !== undefined && !VALID_TTL.has(input.ttl)) {
    throw new EdictValidationError(
      `Invalid ttl "${input.ttl}". Must be: ${[...VALID_TTL].join(', ')}`
    );
  }

  if (input.expiresAt !== undefined) {
    const parsed = new Date(input.expiresAt);
    if (isNaN(parsed.getTime())) {
      throw new EdictValidationError(
        `Invalid expiresAt "${input.expiresAt}". Must be a valid ISO 8601 date.`
      );
    }
  }

  if (input.expiresIn !== undefined && input.expiresAt !== undefined) {
    throw new EdictValidationError(
      'Cannot specify both expiresAt and expiresIn. Use one or the other.'
    );
  }

  if (input.expiresIn !== undefined) {
    try {
      parseDuration(input.expiresIn);
    } catch (error) {
      throw new EdictValidationError(
        error instanceof Error ? error.message : 'Invalid expiresIn value.'
      );
    }
  }
}

export function validateFileSchema(schema: EdictFileSchema): string[] {
  const warnings: string[] = [];

  if (!schema.version) {
    throw new EdictValidationError('Missing required field: version');
  }

  if (schema.version !== 1) {
    throw new EdictValidationError(`Unsupported schema version: ${schema.version}`);
  }

  if (!schema.config) {
    warnings.push('Missing config section, using defaults');
  }

  if (!Array.isArray(schema.edicts)) {
    throw new EdictValidationError('edicts must be an array');
  }

  if (!Array.isArray(schema.history)) {
    warnings.push('Missing history array, initializing empty');
  }

  for (const edict of schema.edicts) {
    if (!edict.id) warnings.push('Edict missing id, will be regenerated');
    if (!edict.text) warnings.push(`Edict ${edict.id ?? '(unknown)'} missing text`);
    if (!edict.created) warnings.push(`Edict ${edict.id ?? '(unknown)'} missing created timestamp`);
  }

  return warnings;
}

export function pruneExpired(
  edicts: Edict[],
  now: Date = new Date()
): { active: Edict[]; expired: HistoryEntry[] } {
  const active: Edict[] = [];
  const expired: HistoryEntry[] = [];

  for (const edict of edicts) {
    if (edict.expiresAt && new Date(edict.expiresAt) < now) {
      expired.push({
        id: `${edict.id}__${now.toISOString().slice(0, 10).replace(/-/g, '')}`,
        text: edict.text,
        supersededBy: 'expired',
        archivedAt: now.toISOString(),
      });
    } else {
      active.push(edict);
    }
  }

  return { active, expired };
}
