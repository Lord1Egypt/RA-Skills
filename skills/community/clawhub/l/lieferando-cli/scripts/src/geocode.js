// Address -> {lat, lng, postcode} via OSM Nominatim.
// Nominatim usage policy: identify the app, max 1 req/s. The shared http
// client already enforces polite pacing per host.
// Results are cached on disk so repeated runs don't re-hit Nominatim.

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { CliError, CODES } from './errors.js';

const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';

function cacheDir() {
  return process.env.LIEFERANDO_CLI_CACHE_DIR || join(homedir(), '.cache', 'lieferando-cli');
}

function loadCache() {
  try {
    return JSON.parse(readFileSync(join(cacheDir(), 'geocode.json'), 'utf8'));
  } catch {
    return {};
  }
}

function saveCache(cache) {
  try {
    mkdirSync(cacheDir(), { recursive: true });
    writeFileSync(join(cacheDir(), 'geocode.json'), JSON.stringify(cache, null, 2));
  } catch {
    // Cache is best-effort; never fail the command over it.
  }
}

/**
 * @param {string} address free-text address, e.g. "Torstraße 1, 10119 Berlin"
 * @param {{http: {getJson: Function}, countryCodes?: string}} deps
 * @returns {Promise<{lat: number, lng: number, postcode: string|null, display_name: string}>}
 */
export async function geocodeAddress(address, { http, countryCodes = 'de' }) {
  const key = `${countryCodes}:${address.trim().toLowerCase()}`;
  const cache = loadCache();
  if (cache[key]) return cache[key];

  const url = new URL(NOMINATIM_URL);
  url.searchParams.set('q', address);
  url.searchParams.set('format', 'jsonv2');
  url.searchParams.set('addressdetails', '1');
  url.searchParams.set('limit', '1');
  url.searchParams.set('countrycodes', countryCodes);

  let results;
  try {
    results = await http.getJson(url.toString());
  } catch (err) {
    if (err instanceof CliError) {
      throw new CliError(CODES.GEOCODE_ERROR, `Could not geocode the address (${err.code}).`, {
        provider: 'nominatim',
        retryable: err.retryable,
      });
    }
    throw err;
  }
  if (!Array.isArray(results) || results.length === 0) {
    throw new CliError(CODES.GEOCODE_ERROR, 'Address could not be resolved. Try adding a postcode and city.', {
      provider: 'nominatim',
      retryable: false,
    });
  }
  const hit = results[0];
  const resolved = {
    lat: Number(hit.lat),
    lng: Number(hit.lon),
    postcode: hit.address?.postcode ?? null,
    display_name: hit.display_name ?? null,
  };
  if (!Number.isFinite(resolved.lat) || !Number.isFinite(resolved.lng)) {
    throw new CliError(CODES.GEOCODE_ERROR, 'Geocoder returned unusable coordinates.', {
      provider: 'nominatim',
      retryable: false,
    });
  }
  cache[key] = resolved;
  saveCache(cache);
  return resolved;
}

/**
 * Resolve location from CLI flags: either --address, or --postcode (+ optional --lat/--lng).
 * @returns {Promise<{lat: number|null, lng: number|null, postcode: string|null, source: string}>}
 */
export async function resolveLocation({ address, postcode, lat, lng }, deps) {
  if (address && (postcode || lat || lng)) {
    throw new CliError(CODES.INVALID_ARGUMENT, 'Use either --address or --postcode/--lat/--lng, not both.', { exitCode: 2 });
  }
  if (address) {
    const g = await geocodeAddress(address, deps);
    if (!g.postcode) {
      throw new CliError(CODES.GEOCODE_ERROR, 'Address resolved without a postcode; pass --postcode explicitly.', {
        provider: 'nominatim',
        retryable: false,
      });
    }
    return { lat: g.lat, lng: g.lng, postcode: g.postcode, source: 'geocoded' };
  }
  if (postcode) {
    if (!/^\d{5}$/.test(String(postcode))) {
      throw new CliError(CODES.INVALID_ARGUMENT, '--postcode must be a 5-digit German postcode.', { exitCode: 2 });
    }
    return {
      lat: lat != null ? Number(lat) : null,
      lng: lng != null ? Number(lng) : null,
      postcode: String(postcode),
      source: 'flags',
    };
  }
  throw new CliError(CODES.INVALID_ARGUMENT, 'A location is required: pass --address "…" or --postcode NNNNN.', { exitCode: 2 });
}
