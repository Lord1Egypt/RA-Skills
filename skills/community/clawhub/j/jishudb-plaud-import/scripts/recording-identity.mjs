import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const identityDomain = 'jishudb-plaud-import/v1';
const uuidNamespace = Buffer.from('6ba7b8119dad11d180b400c04fd430c8', 'hex');
const maxInputBytes = 8 * 1024;
const representations = new Set(['audio', 'transcript', 'summary']);
const allowedFields = new Set(['accountScope', 'recordingId', 'kbId', 'representation', 'contentSha256']);

class IdentityInputError extends Error {}

function requiredString(input, field, maxBytes = 512) {
  const value = input[field];
  if (typeof value !== 'string' || value === '' || value !== value.trim() ||
      Buffer.byteLength(value, 'utf8') > maxBytes || /[\u0000-\u001f\u007f]/.test(value)) {
    throw new IdentityInputError(`${field} must be a bounded, non-empty identifier without surrounding whitespace or control characters`);
  }
  return value;
}

function digest(parts) {
  return createHash('sha256').update(JSON.stringify(parts), 'utf8').digest('hex');
}

function namespacedNoteId(parts) {
  const bytes = createHash('sha1').update(uuidNamespace).update(JSON.stringify(parts), 'utf8').digest().subarray(0, 16);
  bytes[6] = (bytes[6] & 0x0f) | 0x50;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = bytes.toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

/**
 * Derive stable, non-secret recording associations and optional transfer keys.
 * This computes identifiers only; it does not authenticate, transfer, or save data.
 * @param {Record<string, unknown>} input Source/account/KB identity and optional exact content revision.
 * @returns {{externalAssetId: string, manifestNoteId: string, idempotencyKey?: string}}
 */
export function recordingIdentity(input) {
  if (input === null || typeof input !== 'object' || Array.isArray(input) ||
      Object.keys(input).some((field) => !allowedFields.has(field))) {
    throw new IdentityInputError('stdin must be an identity object containing only the documented fields');
  }
  const accountScope = requiredString(input, 'accountScope');
  const recordingId = requiredString(input, 'recordingId');
  const kbId = requiredString(input, 'kbId', 256);
  const externalAssetId = `plaud:${digest([identityDomain, accountScope, recordingId])}`;
  const result = {
    externalAssetId,
    manifestNoteId: namespacedNoteId([identityDomain, 'manifest', externalAssetId, kbId]),
  };
  const hasRepresentation = Object.hasOwn(input, 'representation');
  const hasContent = Object.hasOwn(input, 'contentSha256');
  if (hasRepresentation !== hasContent) {
    throw new IdentityInputError('representation and contentSha256 must be supplied together');
  }
  if (hasRepresentation) {
    const representation = requiredString(input, 'representation');
    const contentSha256 = requiredString(input, 'contentSha256', 64);
    if (!representations.has(representation) || !/^[0-9a-f]{64}$/.test(contentSha256)) {
      throw new IdentityInputError('use audio, transcript, or summary and an actual lowercase SHA-256 digest');
    }
    return {
      ...result,
      idempotencyKey: `plaud-${digest([identityDomain, externalAssetId, kbId, representation, contentSha256])}`,
    };
  }
  return result;
}

async function readInput() {
  const chunks = [];
  let size = 0;
  for await (const chunk of process.stdin) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += bytes.length;
    if (size > maxInputBytes) {
      throw new IdentityInputError('identity input exceeds 8192 bytes');
    }
    chunks.push(bytes);
  }
  let text;
  try {
    text = new TextDecoder('utf-8', { fatal: true }).decode(Buffer.concat(chunks));
  } catch (error) {
    if (!(error instanceof TypeError)) throw error;
    throw new IdentityInputError('identity input must be valid UTF-8');
  }
  try {
    return JSON.parse(text);
  } catch (error) {
    if (!(error instanceof SyntaxError)) throw error;
    throw new IdentityInputError('stdin must contain one JSON identity object');
  }
}

async function main() {
  if (process.argv.length === 3 && process.argv[2] === '--help') {
    process.stdout.write('Usage: node recording-identity.mjs < identity-input.json\n');
    return;
  }
  if (process.argv.length !== 2) {
    throw new IdentityInputError('pass identity JSON through stdin, not command-line arguments');
  }
  process.stdout.write(`${JSON.stringify(recordingIdentity(await readInput()))}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  main().catch((error) => {
    if (!(error instanceof IdentityInputError)) throw error;
    process.stderr.write(`Invalid recording identity: ${error.message}\n`);
    process.exitCode = 2;
  });
}
