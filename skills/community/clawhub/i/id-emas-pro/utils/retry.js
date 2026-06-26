// ============================================
// utils/retry.js — Exponential backoff retry
// ============================================

/**
 * Retry dengan exponential backoff
 *
 * @param {Function} fn         - async function to retry
 * @param {object}   opts
 * @param {number}   opts.maxAttempts  - max percobaan (default: 3)
 * @param {number}   opts.baseDelayMs  - delay awal ms (default: 500)
 * @param {number}   opts.maxDelayMs   - delay maksimum ms (default: 10000)
 * @param {Function} opts.shouldRetry  - (err) => bool, default: selalu retry
 * @param {string}   opts.label        - label untuk logging
 */
export async function withRetry(fn, opts = {}) {
  const {
    maxAttempts = 3,
    baseDelayMs = 500,
    maxDelayMs = 10_000,
    shouldRetry = () => true,
    label = "operation",
  } = opts;

  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;

      const isLast = attempt === maxAttempts;
      const willRetry = !isLast && shouldRetry(err);

      if (!willRetry) break;

      // Exponential backoff: 500ms, 1000ms, 2000ms, ... capped at maxDelayMs
      const delay = Math.min(baseDelayMs * 2 ** (attempt - 1), maxDelayMs);
      // Add jitter ±20% agar tidak semua request retry bersamaan
      const jitter = delay * 0.2 * (Math.random() * 2 - 1);
      const actualDelay = Math.round(delay + jitter);

      console.error(
        `⏳ ${label} gagal (attempt ${attempt}/${maxAttempts}), retry dalam ${actualDelay}ms: ${err.message}`
      );

      await sleep(actualDelay);
    }
  }

  throw lastError;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Tentukan apakah error layak di-retry
 * Tidak retry: 4xx client errors (kecuali 429 rate limit)
 */
export function isRetryableError(err) {
  const msg = err.message ?? "";

  // Jangan retry kalau kena 4xx (kecuali 429)
  if (msg.includes("HTTP 400")) return false;
  if (msg.includes("HTTP 401")) return false;
  if (msg.includes("HTTP 403")) return false;
  if (msg.includes("HTTP 404")) return false;

  // Retry kalau: timeout, 429, 5xx, network error
  return true;
}
