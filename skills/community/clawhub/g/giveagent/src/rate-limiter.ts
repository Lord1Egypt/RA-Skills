import { RateLimitStatus } from "./types.js";

// ---------------------------------------------------------------------------
// Limits
// ---------------------------------------------------------------------------

const REQUEST_LIMIT = 10;
const REQUEST_WINDOW_MS = 60 * 1000; // 1 minute

const POST_LIMIT = 1;
const POST_WINDOW_MS = 60 * 60 * 1000; // 1 hour

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Sliding-window in-memory rate limiter.
 *
 * Each action category maintains a list of timestamps for recent actions.
 * On every check/record call, expired timestamps are pruned so the window
 * truly slides rather than resets at a fixed boundary.
 */
export interface RateLimiter {
  canMakeRequest(): boolean;
  canPost(): boolean;
  recordRequest(): void;
  recordPost(): void;
  getStatus(): RateLimitStatus;
  reset(): void;
}

// ---------------------------------------------------------------------------
// Implementation
// ---------------------------------------------------------------------------

/**
 * Prune timestamps older than `windowMs` from `now`.
 */
function pruneOld(timestamps: number[], windowMs: number, now: number): number[] {
  const cutoff = now - windowMs;
  return timestamps.filter((t) => t > cutoff);
}

/**
 * Compute the timestamp at which the oldest record will expire.
 * Returns `now` if there are no records (all slots already open).
 */
function nextResetTime(timestamps: number[], windowMs: number): Date {
  if (timestamps.length === 0) {
    return new Date();
  }
  // The earliest timestamp is the next one to expire.
  const oldest = Math.min(...timestamps);
  return new Date(oldest + windowMs);
}

class SlidingWindowRateLimiter implements RateLimiter {
  private requests: number[] = [];
  private posts: number[] = [];

  private now(): number {
    return Date.now();
  }

  canMakeRequest(): boolean {
    this.requests = pruneOld(this.requests, REQUEST_WINDOW_MS, this.now());
    return this.requests.length < REQUEST_LIMIT;
  }

  canPost(): boolean {
    this.posts = pruneOld(this.posts, POST_WINDOW_MS, this.now());
    return this.posts.length < POST_LIMIT;
  }

  recordRequest(): void {
    this.requests.push(this.now());
  }

  recordPost(): void {
    this.posts.push(this.now());
  }

  getStatus(): RateLimitStatus {
    const now = this.now();

    const activeRequests = pruneOld(this.requests, REQUEST_WINDOW_MS, now);
    const activePosts = pruneOld(this.posts, POST_WINDOW_MS, now);

    // resetAt reflects when the most-constrained resource next opens a slot.
    // Use the longest window's oldest timestamp as the canonical reset time.
    const candidates: Date[] = [
      nextResetTime(activeRequests, REQUEST_WINDOW_MS),
      nextResetTime(activePosts, POST_WINDOW_MS),
    ];
    const resetAt = new Date(Math.max(...candidates.map((d) => d.getTime())));

    return {
      requestsRemaining: Math.max(0, REQUEST_LIMIT - activeRequests.length),
      postsRemaining: Math.max(0, POST_LIMIT - activePosts.length),
      resetAt,
    };
  }

  reset(): void {
    this.requests = [];
    this.posts = [];
  }
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

/**
 * Create a new in-memory sliding-window rate limiter.
 *
 * Limits:
 * - 10 requests / 1 minute
 * - 1 post / 1 hour
 */
export function createRateLimiter(): RateLimiter {
  return new SlidingWindowRateLimiter();
}
