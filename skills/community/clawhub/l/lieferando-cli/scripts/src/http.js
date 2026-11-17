// Polite HTTP layer.
// - Enforces a minimum interval between requests per host (politeness).
// - Honors Retry-After on 429 with a single bounded retry.
// - Never persists or logs cookies, tokens, or personal data.
// - Verbose traces go to stderr with location-identifying query values redacted.

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { CliError, CODES } from './errors.js';

const MIN_INTERVAL_MS = 1200;
const MAX_RETRY_AFTER_MS = 15000;
const REDACTED_PARAMS = new Set(['postalcode', 'lat', 'lng', 'lon', 'latitude', 'longitude', 'q', 'street', 'address']);

const lastRequestAt = new Map(); // host -> epoch ms (in-process)

// Cross-process pacing: each CLI invocation is a fresh process, so the
// in-memory map alone would let rapid sequential invocations hammer a host.
// Persist per-host timestamps to a small state file (best effort only).
function pacingPath() {
  const dir = process.env.LIEFERANDO_CLI_STATE_DIR || join(homedir(), '.local', 'state', 'lieferando-cli');
  return join(dir, 'pacing.json');
}

function readPacing() {
  try {
    return JSON.parse(readFileSync(pacingPath(), 'utf8'));
  } catch {
    return {};
  }
}

function writePacing(host, ts) {
  try {
    const all = readPacing();
    all[host] = ts;
    mkdirSync(join(pacingPath(), '..'), { recursive: true });
    writeFileSync(pacingPath(), JSON.stringify(all));
  } catch {
    // pacing persistence is best effort
  }
}

function redactUrl(url) {
  try {
    const u = new URL(url);
    for (const key of [...u.searchParams.keys()]) {
      if (REDACTED_PARAMS.has(key.toLowerCase())) u.searchParams.set(key, '…');
    }
    // Location can also live in path segments, e.g. /bypostcode/10115.
    u.pathname = u.pathname.replace(/(\/bypostcode\/)[^/]+/i, '$1…');
    return u.toString();
  } catch {
    return '<unparseable-url>';
  }
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

/**
 * Create an HTTP client. fetchImpl is injectable for tests.
 * @param {{fetchImpl?: typeof fetch, verbose?: boolean, userAgent?: string, provider?: string, minIntervalMs?: number, sleepImpl?: (ms:number)=>Promise<void>}} opts
 */
export function createHttpClient({
  fetchImpl = fetch,
  verbose = false,
  userAgent = 'lieferando-cli/0.2.4 (+https://clawhub.ai/skills/lieferando-cli; read-only discovery)',
  provider = 'lieferando',
  minIntervalMs = MIN_INTERVAL_MS,
  sleepImpl = sleep,
} = {}) {
  function trace(msg) {
    if (verbose) process.stderr.write(`[trace] ${msg}\n`);
  }

  async function politeWait(host) {
    const last = Math.max(lastRequestAt.get(host) ?? 0, minIntervalMs > 0 ? readPacing()[host] ?? 0 : 0);
    const wait = last + minIntervalMs - Date.now();
    if (wait > 0) {
      trace(`politeness wait ${wait}ms for ${host}`);
      await sleepImpl(wait);
    }
    const now = Date.now();
    lastRequestAt.set(host, now);
    if (minIntervalMs > 0) writePacing(host, now);
  }

  /**
   * GET a JSON document. Throws CliError on failure.
   * @param {string} url
   * @param {{headers?: object}} [opts]
   */
  async function getJson(url, { headers = {} } = {}) {
    return requestJson('GET', url, { headers });
  }

  /**
   * POST a JSON query and read a JSON document back. Some upstreams (Uber
   * Eats) shape read-only queries as POST; this carries a query body only and
   * uses the exact same pacing and error mapping as getJson. It must never be
   * pointed at a mutating endpoint.
   * @param {string} url
   * @param {{headers?: object, body?: object}} [opts]
   */
  async function postJson(url, { headers = {}, body = {} } = {}) {
    return requestJson('POST', url, { headers, body });
  }

  async function requestJson(method, url, { headers = {}, body = undefined } = {}) {
    const host = new URL(url).host;
    let attempt = 0;
    // At most one retry, and only for 429 with a small Retry-After.
    for (;;) {
      attempt += 1;
      await politeWait(host);
      trace(`${method} ${redactUrl(url)} (attempt ${attempt})`);
      let res;
      try {
        res = await fetchImpl(url, {
          method,
          headers: {
            accept: 'application/json',
            'user-agent': userAgent,
            ...(body !== undefined ? { 'content-type': 'application/json' } : {}),
            ...headers,
          },
          ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
          redirect: 'follow',
        });
      } catch (cause) {
        throw new CliError(CODES.NETWORK_ERROR, `Network error talking to ${host}: ${cause?.message ?? 'request failed'}`, {
          provider,
          retryable: true,
        });
      }
      trace(`-> HTTP ${res.status}`);

      if (res.status === 429) {
        const retryAfterSec = Number(res.headers.get('retry-after'));
        const waitMs = Number.isFinite(retryAfterSec) ? retryAfterSec * 1000 : NaN;
        if (attempt === 1 && Number.isFinite(waitMs) && waitMs <= MAX_RETRY_AFTER_MS) {
          trace(`429, honoring Retry-After ${retryAfterSec}s`);
          await sleepImpl(waitMs);
          continue;
        }
        throw new CliError(CODES.RATE_LIMITED, `${host} rate-limited the request. Back off and retry later.`, {
          provider,
          retryable: true,
          details: { status: 429 },
        });
      }
      if (res.status === 403) {
        throw new CliError(
          CODES.BLOCKED,
          `${host} refused the request (403). This tool does not bypass bot protection; stop and retry much later.`,
          { provider, retryable: false, details: { status: 403 } }
        );
      }
      if (res.status === 404) {
        throw new CliError(CODES.NOT_FOUND, 'Upstream resource not found.', {
          provider,
          retryable: false,
          details: { status: 404 },
        });
      }
      if (!res.ok) {
        throw new CliError(CODES.UPSTREAM_ERROR, `Upstream error from ${host} (HTTP ${res.status}).`, {
          provider,
          retryable: res.status >= 500,
          details: { status: res.status },
        });
      }
      try {
        return await res.json();
      } catch {
        throw new CliError(CODES.PARSE_ERROR, `Upstream returned non-JSON payload from ${host}.`, {
          provider,
          retryable: false,
        });
      }
    }
  }

  return { getJson, postJson };
}
