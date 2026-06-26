/**
 * export.js — Config token export
 *
 * exportConfigToken(config) → "mrconf:v1:..." token string
 */

"use strict";

const { normalizeOpenClawConfig } = require("./normalize.js");
const { encode } = require("./base64url.js");
const { REF_REGEX } = require("./resolve-refs.js");

const NORMALIZER_VERSION = "1.0.0";

/**
 * Export a config as a shareable token.
 *
 * @param {object} config — raw openclaw.json config
 * @returns {{ token: string, credentialRefs: string[] }}
 */
function exportConfigToken(config) {
  // 1. Normalize
  const { normalized } = normalizeOpenClawConfig(config);

  // 2. Extract credential references from normalized config
  // (Note: actual credentials in the config are already replaced with ${REF}
  // by the caller before export — we just collect the ${REF} patterns)
  const credentialRefs = _collectRefs(normalized);

  // 3. Build token payload
  const payload = {
    version: 1,
    exportedAt: new Date().toISOString(),
    normalizerVersion: NORMALIZER_VERSION,
    config: normalized,
    credentialRefs,
  };

  // 4. Encode
  const jsonStr = JSON.stringify(payload);
  const encoded = encode(jsonStr);

  // 5. Prepend prefix
  return `mrconf:v1:${encoded}`;
}

/**
 * Collect all unique ${REF} references from a config object.
 * @param {object} obj
 * @returns {string[]} unique ref names (without ${} wrapper)
 */
function _collectRefs(obj) {
  const refs = new Set();
  _walkStrings(obj, (path, value) => {
    const match = value.match(REF_REGEX);
    if (match) {
      refs.add(match[1]); // capture group: ref name
    }
  });
  return Array.from(refs).sort();
}

/**
 * Walk all string values in an object, calling visitor.
 */
function _walkStrings(obj, visitor) {
  if (obj === null || typeof obj !== "object" || Array.isArray(obj)) return;
  for (const [key, val] of Object.entries(obj)) {
    if (typeof val === "string") {
      visitor(key, val);
    } else if (Array.isArray(val)) {
      val.forEach((item) => {
        if (typeof item === "string") visitor(null, item);
        else if (item !== null && typeof item === "object") _walkStrings(item, visitor);
      });
    } else if (val !== null && typeof val === "object") {
      _walkStrings(val, visitor);
    }
  }
}

module.exports = { exportConfigToken };
