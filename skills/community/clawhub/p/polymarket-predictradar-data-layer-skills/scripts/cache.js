/**
 * cache.js — File-level cache shared by polymarket-data-layer and other skills
 *
 * Cache files are stored in scripts/cache/ directory, JSON format,
 * filenames are derived from hashed keys.
 *
 * Usage:
 *   const cache = require('../../polymarket-data-layer/scripts/cache');
 *   const data  = cache.get('positions:0xabc', { ttl: 3600 });
 *   cache.set('positions:0xabc', rows);
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const CACHE_DIR = path.join(__dirname, 'cache');

if (!fs.existsSync(CACHE_DIR)) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
}

// key → safe filename (only preserve alphanumeric and -_:., replace others with _)
function keyToFilename(key) {
  return key.replace(/[^a-zA-Z0-9\-_:.]/g, '_').slice(0, 200) + '.json';
}

function filePath(key) {
  return path.join(CACHE_DIR, keyToFilename(key));
}

/**
 * Read cache.
 * @param {string} key
 * @param {{ ttl?: number }} opts  ttl in seconds, default 3600
 * @returns {any|null}  Returns data if cache is valid, null otherwise
 */
function get(key, { ttl = 3600 } = {}) {
  const fp = filePath(key);
  if (!fs.existsSync(fp)) return null;
  try {
    const { _cachedAt, data } = JSON.parse(fs.readFileSync(fp, 'utf-8'));
    const ageSeconds = (Date.now() - _cachedAt) / 1000;
    if (ageSeconds > ttl) return null;
    return data;
  } catch (_) {
    return null;
  }
}

/**
 * Write cache.
 * @param {string} key
 * @param {any} data
 */
function set(key, data) {
  const fp = filePath(key);
  fs.writeFileSync(fp, JSON.stringify({ _cachedAt: Date.now(), data }));
}

/**
 * Delete a single cache entry.
 */
function invalidate(key) {
  const fp = filePath(key);
  if (fs.existsSync(fp)) fs.unlinkSync(fp);
}

/**
 * Clear cache by prefix (clears all if prefix is empty).
 * @param {string} prefix
 */
function clear(prefix = '') {
  const safePrefix = prefix.replace(/[^a-zA-Z0-9\-_:.]/g, '_');
  const files = fs.readdirSync(CACHE_DIR).filter(f => f.endsWith('.json'));
  for (const f of files) {
    if (!safePrefix || f.startsWith(safePrefix)) {
      fs.unlinkSync(path.join(CACHE_DIR, f));
    }
  }
}

/**
 * Remove cache files older than maxAgeSeconds.
 * Recommended to call once at the start of long-running processes to prevent unbounded cache growth.
 * @param {number} maxAgeSeconds  Default 7 days
 */
function cleanup(maxAgeSeconds = 7 * 86400) {
  const now   = Date.now();
  const files = fs.readdirSync(CACHE_DIR).filter(f => f.endsWith('.json'));
  let removed = 0;
  for (const f of files) {
    const fp = path.join(CACHE_DIR, f);
    try {
      const { _cachedAt } = JSON.parse(fs.readFileSync(fp, 'utf-8'));
      if ((now - _cachedAt) / 1000 > maxAgeSeconds) {
        fs.unlinkSync(fp);
        removed++;
      }
    } catch (_) {
      fs.unlinkSync(fp); // Delete corrupted cache directly
      removed++;
    }
  }
  return removed;
}

/**
 * Returns remaining valid seconds for a cache entry (< 0 means expired or not exists).
 */
function ttlRemaining(key, ttl = 3600) {
  const fp = filePath(key);
  if (!fs.existsSync(fp)) return -1;
  try {
    const { _cachedAt } = JSON.parse(fs.readFileSync(fp, 'utf-8'));
    return ttl - (Date.now() - _cachedAt) / 1000;
  } catch (_) {
    return -1;
  }
}

module.exports = { get, set, invalidate, clear, cleanup, ttlRemaining };
