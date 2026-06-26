/**
 * vault-client.js — Locker Secrets Manager Client for OpenClaw Agents
 *
 * Zero-dependency Node.js wrapper around the Locker CLI with:
 * - In-memory TTL cache (per-key expiry)
 * - Permission gate (ro/rw modes)
 * - Vault reference resolver (vault://KEY → actual value)
 * - Cache statistics for monitoring
 *
 * Usage:
 *   const vault = require('./vault-client');
 *   await vault.init({ mode: 'ro', cacheTTL: 300 });
 *   const apiKey = await vault.get('MY_API_KEY');
 */

'use strict';

const { execFile } = require('child_process');
const { promisify } = require('util');

const execFileAsync = promisify(execFile);

// ─── State ──────────────────────────────────────────────────────────────────

const _cache = new Map();        // key → { value, expiry }
let _listCache = null;           // { keys, expiry }
let _config = {
  mode: 'ro',                    // 'ro' | 'rw'
  cacheTTL: 300,                 // seconds, default 5 min
  listCacheTTL: 60,              // seconds, default 1 min
  cliPath: 'locker',             // path to locker binary
  cliTimeout: 10000,             // ms, max wait for CLI response
  strict: false,                 // throw on errors vs return null
};
let _stats = { hits: 0, misses: 0 };
let _initialized = false;

// ─── Internal Helpers ───────────────────────────────────────────────────────

function _now() {
  return Math.floor(Date.now() / 1000);
}

function _cacheGet(key) {
  const entry = _cache.get(key);
  if (!entry) return undefined;
  if (_now() > entry.expiry) {
    _cache.delete(key);
    return undefined;
  }
  _stats.hits++;
  return entry.value;
}

function _cacheSet(key, value, ttl) {
  const effectiveTTL = ttl || _config.cacheTTL;
  _cache.set(key, {
    value,
    expiry: _now() + effectiveTTL,
  });
}

function _cacheEvict(key) {
  _cache.delete(key);
}

function _assertWritable(operation) {
  if (_config.mode !== 'rw') {
    const err = new Error(
      `VAULT_PERMISSION_DENIED: Operation "${operation}" requires mode "rw", ` +
      `but agent is configured as "${_config.mode}". ` +
      `Change VAULT_MODE to "rw" if this agent needs write access.`
    );
    err.code = 'VAULT_PERMISSION_DENIED';
    throw err;
  }
}

async function _exec(args) {
  try {
    const { stdout } = await execFileAsync(_config.cliPath, args, {
      timeout: _config.cliTimeout,
      env: {
        ...process.env,
        // Ensure Locker CLI uses non-interactive mode
        LOCKER_NON_INTERACTIVE: '1',
      },
    });
    return stdout.trim();
  } catch (err) {
    if (err.code === 'ENOENT') {
      const error = new Error(
        `VAULT_CLI_NOT_FOUND: The "${_config.cliPath}" binary was not found. ` +
        `Install Locker CLI: curl -fsSL https://locker.io/secrets/install.sh | bash`
      );
      error.code = 'VAULT_CLI_NOT_FOUND';
      throw error;
    }
    if (err.killed) {
      const error = new Error(
        `VAULT_TIMEOUT: CLI call timed out after ${_config.cliTimeout}ms. ` +
        `Check network connectivity and Locker API status.`
      );
      error.code = 'VAULT_TIMEOUT';
      throw error;
    }
    if (err.stderr && err.stderr.includes('auth')) {
      const error = new Error(
        `VAULT_AUTH_FAILED: Authentication failed. ` +
        `Check LOCKER_ACCESS_KEY_ID and LOCKER_SECRET_ACCESS_KEY.`
      );
      error.code = 'VAULT_AUTH_FAILED';
      throw error;
    }
    const error = new Error(
      `VAULT_CLI_ERROR: ${err.stderr || err.message}`
    );
    error.code = 'VAULT_CLI_ERROR';
    throw error;
  }
}

function _handleError(err, options = {}) {
  const strict = options.strict !== undefined ? options.strict : _config.strict;
  if (strict) throw err;
  console.error(`[vault-client] ${err.message}`);
  return null;
}

// ─── Public API ─────────────────────────────────────────────────────────────

/**
 * Initialize the vault client.
 * Call once per session before any other operation.
 *
 * @param {Object} options
 * @param {string} options.mode       - 'ro' (read-only) or 'rw' (read-write)
 * @param {number} options.cacheTTL   - Cache TTL in seconds (default: 300)
 * @param {number} options.listCacheTTL - List cache TTL in seconds (default: 60)
 * @param {string} options.cliPath    - Path to locker binary (default: 'locker')
 * @param {number} options.cliTimeout - CLI timeout in ms (default: 10000)
 * @param {boolean} options.strict    - Throw on errors (default: false)
 */
async function init(options = {}) {
  _config = { ..._config, ...options };

  // Validate mode
  if (!['ro', 'rw'].includes(_config.mode)) {
    throw new Error(
      `VAULT_CONFIG_ERROR: Invalid mode "${_config.mode}". Use "ro" or "rw".`
    );
  }

  // Validate CLI is available
  try {
    await _exec(['--version']);
  } catch (err) {
    if (err.code === 'VAULT_CLI_NOT_FOUND') throw err;
    // Version check might not exist in all CLI versions, that's OK
  }

  _initialized = true;
  console.log(
    `[vault-client] Initialized in "${_config.mode}" mode ` +
    `(cache TTL: ${_config.cacheTTL}s, list TTL: ${_config.listCacheTTL}s)`
  );
}

/**
 * Get a secret value by key.
 * Returns cached value if available and not expired.
 *
 * @param {string} key - The secret key name
 * @param {Object} options
 * @param {number}  options.ttl       - Override TTL for this key
 * @param {boolean} options.skipCache - Bypass cache, force CLI call
 * @param {boolean} options.strict    - Throw on error for this call
 * @returns {string|null} The secret value, or null on error (non-strict mode)
 */
async function get(key, options = {}) {
  if (!_initialized) await init();

  // Check cache first (unless skipCache)
  if (!options.skipCache) {
    const cached = _cacheGet(key);
    if (cached !== undefined) return cached;
  }

  _stats.misses++;

  try {
    const value = await _exec(['secret', 'get', `--name=${key}`]);

    if (!value) {
      const err = new Error(
        `VAULT_KEY_NOT_FOUND: Secret "${key}" not found in vault. ` +
        `Use list() to see available keys.`
      );
      err.code = 'VAULT_KEY_NOT_FOUND';
      throw err;
    }

    _cacheSet(key, value, options.ttl);
    return value;
  } catch (err) {
    return _handleError(err, options);
  }
}

/**
 * List all available secret key names.
 * Returns cached list if available and not expired.
 *
 * @param {Object} options
 * @param {boolean} options.skipCache - Bypass cache
 * @returns {string[]} Array of key names
 */
async function list(options = {}) {
  if (!_initialized) await init();

  // Check list cache
  if (!options.skipCache && _listCache && _now() <= _listCache.expiry) {
    _stats.hits++;
    return _listCache.keys;
  }

  _stats.misses++;

  try {
    const output = await _exec(['secret', 'list']);
    const keys = output
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);

    _listCache = {
      keys,
      expiry: _now() + _config.listCacheTTL,
    };

    return keys;
  } catch (err) {
    return _handleError(err, options) || [];
  }
}

/**
 * Check if a secret exists in the vault.
 *
 * @param {string} key - The secret key name
 * @returns {boolean}
 */
async function exists(key) {
  const keys = await list();
  return keys.includes(key);
}

/**
 * Create a new secret in the vault.
 * Requires mode: 'rw'.
 *
 * @param {string} key   - The secret key name
 * @param {string} value - The secret value
 * @param {Object} options
 * @param {boolean} options.strict - Throw on error
 * @returns {boolean} true on success
 */
async function create(key, value, options = {}) {
  _assertWritable('create');
  if (!_initialized) await init();

  try {
    await _exec(['secret', 'create', `--key=${key}`, `--value=${value}`]);
    // Update cache with new value
    _cacheSet(key, value);
    // Invalidate list cache (new key added)
    _listCache = null;
    return true;
  } catch (err) {
    return _handleError(err, options) || false;
  }
}

/**
 * Create a secret with a random value.
 * Requires mode: 'rw'.
 *
 * @param {string} key - The secret key name
 * @param {Object} options
 * @param {boolean} options.strict - Throw on error
 * @returns {string|null} The generated value
 */
async function createRandom(key, options = {}) {
  _assertWritable('createRandom');
  if (!_initialized) await init();

  try {
    const value = await _exec(['secret', 'create', `--key=${key}`, '--random-value']);
    _cacheSet(key, value);
    _listCache = null;
    return value;
  } catch (err) {
    return _handleError(err, options);
  }
}

/**
 * Update an existing secret.
 * Requires mode: 'rw'.
 *
 * @param {string} key   - The secret key name
 * @param {string} value - The new value
 * @param {Object} options
 * @returns {boolean} true on success
 */
async function update(key, value, options = {}) {
  _assertWritable('update');
  if (!_initialized) await init();

  try {
    // Locker CLI uses create --key with existing key to update
    await _exec(['secret', 'create', `--key=${key}`, `--value=${value}`]);
    _cacheSet(key, value);
    return true;
  } catch (err) {
    return _handleError(err, options) || false;
  }
}

/**
 * Delete a secret from the vault.
 * Requires mode: 'rw'. Use with caution.
 *
 * @param {string} key - The secret key name
 * @param {Object} options
 * @returns {boolean} true on success
 */
async function remove(key, options = {}) {
  _assertWritable('delete');
  if (!_initialized) await init();

  try {
    await _exec(['secret', 'delete', `--name=${key}`]);
    _cacheEvict(key);
    _listCache = null;
    return true;
  } catch (err) {
    return _handleError(err, options) || false;
  }
}

/**
 * Resolve all vault:// references in an object.
 * Recursively walks the object and replaces any string matching
 * vault://KEY_NAME with the actual secret value from the vault.
 *
 * @param {Object} obj - Object with potential vault:// references
 * @param {Object} options
 * @param {boolean} options.strict - Throw if any ref can't be resolved
 * @returns {Object} New object with resolved values
 */
async function resolveVaultRefs(obj, options = {}) {
  if (typeof obj === 'string') {
    const match = obj.match(/^vault:\/\/(.+)$/);
    if (match) {
      return await get(match[1], options);
    }
    return obj;
  }

  if (Array.isArray(obj)) {
    return Promise.all(obj.map(item => resolveVaultRefs(item, options)));
  }

  if (obj !== null && typeof obj === 'object') {
    const resolved = {};
    for (const [key, value] of Object.entries(obj)) {
      resolved[key] = await resolveVaultRefs(value, options);
    }
    return resolved;
  }

  return obj;
}

/**
 * Create a vault reference string.
 * Use this instead of storing the actual value.
 *
 * @param {string} key - The secret key name
 * @returns {string} vault://KEY_NAME
 */
function ref(key) {
  return `vault://${key}`;
}

/**
 * Clear the entire cache.
 * Useful after bulk credential rotation.
 */
function clearCache() {
  _cache.clear();
  _listCache = null;
  _stats = { hits: 0, misses: 0 };
  console.log('[vault-client] Cache cleared');
}

/**
 * Get cache statistics.
 *
 * @returns {Object} { size, hits, misses, hitRate }
 */
function cacheStats() {
  const total = _stats.hits + _stats.misses;
  return {
    size: _cache.size,
    hits: _stats.hits,
    misses: _stats.misses,
    hitRate: total > 0 ? `${(((_stats.hits / total) * 100).toFixed(1))}%` : '0%',
  };
}

/**
 * Get current configuration (without sensitive data).
 *
 * @returns {Object}
 */
function getConfig() {
  return {
    mode: _config.mode,
    cacheTTL: _config.cacheTTL,
    listCacheTTL: _config.listCacheTTL,
    cliPath: _config.cliPath,
    initialized: _initialized,
  };
}

// ─── Exports ────────────────────────────────────────────────────────────────

module.exports = {
  init,
  get,
  list,
  exists,
  create,
  createRandom,
  update,
  delete: remove,  // 'delete' is reserved word, alias to 'remove'
  remove,
  resolveVaultRefs,
  ref,
  clearCache,
  cacheStats,
  getConfig,
};
