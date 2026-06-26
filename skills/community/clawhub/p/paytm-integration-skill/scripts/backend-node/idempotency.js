// Minimal in-process idempotency cache for the reference create endpoints.
//
// PRODUCTION NOTE: this is in-memory and per-process - fine for the demo, NOT
// fine for a real merchant deployment. Replace with Redis / DynamoDB / a DB
// table keyed on (idempotencyKey -> { status, body, createdAt }) before going
// live. The interface here is deliberately small so the swap is straightforward.

const TTL_MS = 24 * 60 * 60 * 1000;          // 24h
const MAX_ENTRIES = 10_000;
const cache = new Map();                       // key -> { status, body, createdAt }

function pruneIfNeeded() {
  if (cache.size <= MAX_ENTRIES) return;
  const cutoff = Date.now() - TTL_MS;
  for (const [k, v] of cache) {
    if (v.createdAt < cutoff) cache.delete(k);
    if (cache.size <= MAX_ENTRIES) break;
  }
}

export function getCached(key) {
  if (!key) return null;
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.createdAt > TTL_MS) {
    cache.delete(key);
    return null;
  }
  return entry;
}

export function setCached(key, status, body) {
  if (!key) return;
  pruneIfNeeded();
  cache.set(key, { status, body, createdAt: Date.now() });
}

/**
 * Read the idempotency key from headers OR body.
 * Header `Idempotency-Key` is the recommended convention; some clients pass
 * `idempotencyKey` in the JSON body - accept both for ergonomics.
 */
export function readKey(req) {
  const fromHeader = req.headers["idempotency-key"];
  if (typeof fromHeader === "string" && fromHeader.trim()) return fromHeader.trim();
  const fromBody = req.body?.idempotencyKey;
  if (typeof fromBody === "string" && fromBody.trim()) return fromBody.trim();
  return null;
}
