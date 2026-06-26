export interface RetryOptions {
  maxAttempts?: number;
  baseDelayMs?: number;
  onRetry?: (err: Error, attempt: number) => void;
  /** Return false to abort retries early (e.g. for 4xx errors). */
  shouldRetry?: (err: Error) => boolean;
}

const DEFAULT_MAX_ATTEMPTS = 3;
const DEFAULT_BASE_DELAY_MS = 1000;

export async function withRetry<T>(
  fn: () => Promise<T>,
  opts?: RetryOptions,
): Promise<T> {
  const maxAttempts = opts?.maxAttempts ?? DEFAULT_MAX_ATTEMPTS;
  const baseDelay = opts?.baseDelayMs ?? DEFAULT_BASE_DELAY_MS;

  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e instanceof Error ? e : new Error(String(e));

      if (attempt === maxAttempts) break;
      if (opts?.shouldRetry && !opts.shouldRetry(lastError)) break;

      opts?.onRetry?.(lastError, attempt);

      const delay = baseDelay * 2 ** (attempt - 1) + Math.random() * baseDelay;
      await new Promise((r) => setTimeout(r, delay));
    }
  }

  throw lastError;
}

/**
 * Returns true for errors that are typically transient and worth retrying:
 * network failures, timeouts, and 5xx server errors.
 */
export function isRetryableError(err: Error): boolean {
  const msg = err.message.toLowerCase();
  if (
    msg.includes("fetch failed") ||
    msg.includes("econnreset") ||
    msg.includes("econnrefused") ||
    msg.includes("etimedout") ||
    msg.includes("socket hang up") ||
    msg.includes("network") ||
    msg.includes("timeout")
  ) {
    return true;
  }
  const httpMatch = msg.match(/http\s*(\d{3})/);
  if (httpMatch) {
    const status = parseInt(httpMatch[1], 10);
    return status >= 500;
  }
  return false;
}
