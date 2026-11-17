// IsoCity CLI - short-link sharing via Supabase REST (feature: shortlink-gallery).
//
// Stores an immutable city snapshot server-side and returns a /city/<code>
// short URL (<=50 chars) that loads the city on first visit. Zero npm
// dependencies: Node >= 18 global fetch only.
//
// The Supabase publishable (anon) key is public by design - it ships in the
// production web bundle anyway - so baking it in as a default is safe. Only
// the public REST surface is used (insert + count RPC); no secret keys here.
//
// Env overrides:
//   POWPOWCITY_API_BASE   - Supabase REST base (defaults to the production project)
//   POWPOWCITY_ANON_KEY   - Supabase publishable key
// Table setup: run supabase/shared_cities.sql in the Supabase SQL editor once.

import { compressGameState } from './share.mjs';

// Public-by-design constants (extracted from the production JS bundle).
export const DEFAULT_API_BASE = 'https://xhahsqbaohraqrdhtvay.supabase.co/rest/v1';
export const DEFAULT_ANON_KEY = 'sb_publishable_v7BW5kO4AUKJoRu5fVb-Ag_XL-_byGA';
export const DEFAULT_WEB_BASE = 'https://powpowcity.powpow.online';

// 1 MiB hard cap on the compressed payload (mirrors the DB CHECK constraint).
export const MAX_SNAPSHOT_CHARS = 1048576;

// 5-char code over a 32-char alphabet without confusables (I/O/0/1),
// same charset as coop room codes: 32^5 = 33.5M codes.
const SHARE_CODE_CHARSET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const SHARE_CODE_LENGTH = 5;
const MAX_CODE_RETRIES = 5;

// ---------------------------------------------------------------------------
// Typed errors - callers can branch on .code to decide fallback behavior.
// ---------------------------------------------------------------------------
export class ShortlinkError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'ShortlinkError';
    this.code = code;
  }
}

/** Supabase endpoint/key missing or unusable. */
export class ShortlinkConfigError extends ShortlinkError {
  constructor(message) {
    super(message, 'SHORTLINK_CONFIG');
    this.name = 'ShortlinkConfigError';
  }
}

/** Compressed city exceeds MAX_SNAPSHOT_CHARS (FR-011) - use file exchange. */
export class SnapshotTooLargeError extends ShortlinkError {
  constructor(sizeChars) {
    super(
      `City snapshot is too large for a short link (${sizeChars} chars, limit ${MAX_SNAPSHOT_CHARS}). ` +
      'Share the .isocity.json file instead (Settings > Import from File).',
      'SNAPSHOT_TOO_LARGE'
    );
    this.name = 'SnapshotTooLargeError';
    this.sizeChars = sizeChars;
  }
}

/** Network-level failure: DNS, offline, timeout, connection refused. */
export class ShortlinkNetworkError extends ShortlinkError {
  constructor(cause) {
    super(
      `Cannot reach the short-link server (${cause?.message || cause}). ` +
      'Check your network connection, or override with --api-base / POWPOWCITY_API_BASE.',
      'SHORTLINK_NETWORK'
    );
    this.name = 'ShortlinkNetworkError';
    this.cause = cause;
  }
}

/** Server responded with a non-retryable HTTP error. */
export class ShortlinkHttpError extends ShortlinkError {
  constructor(status, bodyMessage) {
    super(
      `Short-link server rejected the request (HTTP ${status})${bodyMessage ? `: ${bodyMessage}` : ''}`,
      'SHORTLINK_HTTP'
    );
    this.name = 'ShortlinkHttpError';
    this.status = status;
  }
}

// ---------------------------------------------------------------------------
// Core
// ---------------------------------------------------------------------------

/** Generate a random 5-char share code (charset excludes I/O/0/1). */
export function generateShareCode() {
  let code = '';
  for (let i = 0; i < SHARE_CODE_LENGTH; i++) {
    code += SHARE_CODE_CHARSET[Math.floor(Math.random() * SHARE_CODE_CHARSET.length)];
  }
  return code;
}

/**
 * Normalize an API base: accept either the Supabase project URL
 * (https://<ref>.supabase.co) or the full REST base (.../rest/v1).
 */
function normalizeApiBase(apiBase) {
  const trimmed = String(apiBase).replace(/\/+$/, '');
  return trimmed.endsWith('/rest/v1') ? trimmed : `${trimmed}/rest/v1`;
}

/** Truncate a city name to 80 code points (emoji-safe), matching createShareUrl. */
function truncateCityName(name) {
  return Array.from(String(name || 'Shared City').trim()).slice(0, 80).join('') || 'Shared City';
}

function restHeaders(anonKey) {
  return {
    apikey: anonKey,
    Authorization: `Bearer ${anonKey}`,
    'Content-Type': 'application/json',
  };
}

/**
 * Create a server-side snapshot of the state and return a short URL.
 *
 * @param {object} options
 * @param {object} options.state        Full GameState (.isocity.json content).
 * @param {boolean} [options.isPublic]  Opt-in to the homepage hot-maps gallery.
 * @param {string} [options.apiBase]    Supabase REST base (env POWPOWCITY_API_BASE overrides default).
 * @param {string} [options.anonKey]    Supabase publishable key (env POWPOWCITY_ANON_KEY overrides default).
 * @param {string} [options.webBase]    Web base used to build the /city/<code> URL.
 * @returns {Promise<{code: string, url: string}>}
 * @throws {ShortlinkConfigError|SnapshotTooLargeError|ShortlinkNetworkError|ShortlinkHttpError}
 */
export async function createShortLink({ state, isPublic = false, apiBase, anonKey, webBase }) {
  const base = apiBase || process.env.POWPOWCITY_API_BASE || DEFAULT_API_BASE;
  const key = anonKey || process.env.POWPOWCITY_ANON_KEY || DEFAULT_ANON_KEY;
  const site = (webBase || DEFAULT_WEB_BASE).replace(/\/+$/, '');
  if (!base || !key) {
    throw new ShortlinkConfigError(
      'Short-link server is not configured. Pass --api-base/--anon-key or set POWPOWCITY_API_BASE/POWPOWCITY_ANON_KEY.'
    );
  }
  const restBase = normalizeApiBase(base);

  const compressed = compressGameState(state);
  if (compressed.length > MAX_SNAPSHOT_CHARS) {
    throw new SnapshotTooLargeError(compressed.length);
  }

  const body = {
    city_name: truncateCityName(state.cityName),
    game_state: compressed,
    population: state.stats?.population ?? 0,
    grid_size: state.gridSize ?? 64,
    is_public: Boolean(isPublic),
  };

  let lastError = null;
  for (let attempt = 0; attempt <= MAX_CODE_RETRIES; attempt++) {
    const code = generateShareCode();
    let res;
    try {
      res = await fetch(`${restBase}/shared_cities`, {
        method: 'POST',
        headers: { ...restHeaders(key), Prefer: 'return=minimal' },
        body: JSON.stringify({ ...body, share_code: code }),
      });
    } catch (e) {
      // fetch itself failed: offline / DNS / timeout - no point retrying.
      throw new ShortlinkNetworkError(e);
    }

    if (res.ok) {
      return { code, url: `${site}/city/${code}` };
    }

    // Duplicate share code (PG 23505, PostgREST maps it to HTTP 409):
    // regenerate a fresh code and retry.
    let errCode = '';
    let errMsg = '';
    try {
      const err = await res.json();
      errCode = String(err?.code || '');
      errMsg = String(err?.message || '');
    } catch {
      // non-JSON error body
    }
    if (errCode === '23505' || res.status === 409) {
      lastError = new ShortlinkError('Share code collision after retry', 'SHORTLINK_CONFLICT');
      continue;
    }
    throw new ShortlinkHttpError(res.status, errMsg);
  }

  throw lastError || new ShortlinkError('Failed to create short link', 'SHORTLINK_UNKNOWN');
}
