/**
 * Words that naturally end in 's' — do not strip.
 * Covers common cases. Not exhaustive, but handles the 90%.
 */
const NATURAL_S_ENDINGS = new Set([
  'chaos',
]);

/** Minimum length to consider stripping trailing 's' */
const MIN_STRIP_LENGTH = 4;

/**
 * Normalize a single category or tag string:
 * - Trim whitespace
 * - Lowercase
 * - Strip trailing 's' for simple plurals (unless word naturally ends in s)
 */
export function normalizeCategory(raw: string): string {
  let value = raw.trim().toLowerCase();

  if (value.length >= MIN_STRIP_LENGTH && value.endsWith('ies')) {
    return `${value.slice(0, -3)}y`;
  }

  if (value.length >= MIN_STRIP_LENGTH && /(ches|shes|xes|zes|sses)$/.test(value)) {
    return value.slice(0, -2);
  }

  if (
    value.length >= MIN_STRIP_LENGTH &&
    value.endsWith('s') &&
    !value.endsWith('ss') &&
    !value.endsWith('us') &&
    !value.endsWith('is') &&
    !value.endsWith('as') &&
    !value.endsWith('es') &&
    !NATURAL_S_ENDINGS.has(value)
  ) {
    value = value.slice(0, -1);
  }

  return value;
}

/**
 * Normalize an array of tags: normalize each, deduplicate.
 */
export function normalizeTags(tags: string[]): string[] {
  const seen = new Set<string>();
  const result: string[] = [];

  for (const tag of tags) {
    const normalized = normalizeCategory(tag);
    if (!seen.has(normalized)) {
      seen.add(normalized);
      result.push(normalized);
    }
  }

  return result;
}
