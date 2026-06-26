/**
 * resolve-refs.js — Credential reference resolution
 *
 * Resolves ${REF} style references from environment variables or `pass`.
 * NEVER exposes the resolved value in error messages.
 *
 * Reference regex: /^\$\{([A-Z_][A-Z0-9_]*)\}$/
 */

"use strict";

const { execSync } = require("child_process");
const { CredentialMissingError } = require("./token-errors.js");

/** Reference regex — strict ENV_VAR style names only */
const REF_REGEX = /^\$\{([A-Z_][A-Z0-9_]*)\}$/;

/**
 * Extract all credential references from a normalized config.
 * Walks all string values; matches ${REF} pattern.
 * @param {object} config
 * @returns {{ refs: string[], credMap: Map<string, string> }}
 *   refs: ordered list of unique ref names (e.g., "CEREBRAS_API_KEY")
 *   credMap: ref → resolved value (from env or pass)
 */
function extractAndResolveRefs(config) {
  const refs = new Set();
  _walkStrings(config, (path, value) => {
    const match = value.match(REF_REGEX);
    if (match) {
      refs.add(match[1]);
    }
  });

  const credMap = new Map();
  for (const ref of refs) {
    const resolved = _resolveOne(ref);
    credMap.set(ref, resolved);
  }

  return { refs: Array.from(refs), credMap };
}

/**
 * Substitute ${REF} placeholders in a config with resolved values.
 * @param {object} config
 * @param {Map<string,string>} credMap — ref → resolved value
 * @returns {object} — new config (does not mutate input)
 */
function substituteRefs(config, credMap) {
  const result = JSON.parse(JSON.stringify(config)); // deep clone
  _walkStrings(result, (path, value) => {
    const match = value.match(REF_REGEX);
    if (match) {
      const refName = match[1];
      const resolved = credMap.get(refName);
      if (resolved === undefined) {
        throw new CredentialMissingError(value); // value = "${REF_NAME}"
      }
      return resolved;
    }
    return value;
  });
  return result;
}

// ─── Internal ─────────────────────────────────────────────────────────────────

/**
 * Resolve a single ref name from env var first, then pass.
 * @param {string} refName — e.g., "CEREBRAS_API_KEY"
 * @returns {string} resolved value
 * @throws {CredentialMissingError} if not found
 */
function _resolveOne(refName) {
  // Try env var first
  const envVal = process.env[refName];
  if (envVal !== undefined) return envVal;

  // Try pass: key = refName converted to path
  // e.g., CEREBRAS_API_KEY → cerebras/apikey (kebab-case lower)
  const passKey = _envToPassKey(refName);
  const passVal = _passShow(passKey);
  if (passVal !== undefined) return passVal;

  // Not found anywhere
  throw new CredentialMissingError(`\${${refName}}`);
}

/**
 * Convert ENV_VAR_NAME → category/name format for pass
 * CEREBRAS_API_KEY → cerebras/api_key → cerebras/apikey
 * OPENCLAW_GATEWAY_TOKEN → openclaw/gateway_token → openclaw/gateway
 */
function _envToPassKey(refName) {
  // Strip _API_KEY suffix if present
  let key = refName
    .replace(/_API_KEY$/, "")
    .replace(/_KEY$/, "")
    .replace(/_TOKEN$/, "")
    .toLowerCase();

  // Convert UNDER_SCORE → /slash
  key = key.replace(/_/g, "/");

  // Common mappings
  const MAPPINGS = {
    "cerebras": "cerebras/apikey",
    "openclaw/gateway": "openclaw/gateway-token",
    "openclaw": "openclaw/gateway-token",
    "agentmail": "agentmail/apikey",
    "alchemy": "alchemy/apikey",
    "morpheus": "morpheus/apikey",
  };

  if (MAPPINGS[key]) return MAPPINGS[key];
  return key;
}

/**
 * Call `pass show <key>` and return stdout, or undefined on failure.
 * @param {string} key
 * @returns {string|undefined}
 */
function _passShow(key) {
  try {
    const out = execSync(`pass show ${key} 2>/dev/null`, {
      encoding: "utf8",
      timeout: 5000,
      stdio: ["ignore", "pipe", "ignore"],
    });
    // pass show outputs the password followed by a newline
    return out.trim();
  } catch {
    return undefined;
  }
}

/**
 * Walk all string values in an object (recursive), calling visitor(path, value).
 * visitor can return a replacement value.
 */
function _walkStrings(obj, visitor, path = "") {
  if (obj === null || typeof obj !== "object" || Array.isArray(obj)) return;
  for (const [key, val] of Object.entries(obj)) {
    const childPath = path ? `${path}.${key}` : key;
    if (typeof val === "string") {
      const replacement = visitor(childPath, val);
      if (replacement !== undefined && replacement !== val) {
        obj[key] = replacement;
      }
    } else if (Array.isArray(val)) {
      val.forEach((item, i) => {
        if (typeof item === "string") {
          const replacement = visitor(`${childPath}[${i}]`, item);
          if (replacement !== undefined && replacement !== item) {
            val[i] = replacement;
          }
        } else if (item !== null && typeof item === "object") {
          _walkStrings(item, visitor, `${childPath}[${i}]`);
        }
      });
    } else if (val !== null && typeof val === "object") {
      _walkStrings(val, visitor, childPath);
    }
  }
}

module.exports = {
  extractAndResolveRefs,
  substituteRefs,
  REF_REGEX,
  _envToPassKey, // exported for testing
};
