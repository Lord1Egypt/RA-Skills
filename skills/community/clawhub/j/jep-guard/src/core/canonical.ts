import stringify from 'fast-json-stable-stringify';

/**
 * JSON Canonicalization Scheme (JCS | RFC 8785)
 * Produces deterministic serialization for signing
 */
export function canonicalize(obj: unknown): string {
  return stringify(obj);
}