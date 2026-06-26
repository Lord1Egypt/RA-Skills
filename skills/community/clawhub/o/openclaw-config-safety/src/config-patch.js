/**
 * config-patch.js — Safe config merge for import
 *
 * Merges an imported token config into openclaw.json.
 * Preserves top-level keys not present in the token (plugins.entries, etc.)
 * Replaces only keys present in the token.
 */

"use strict";

/**
 * Merge token config into existing config.
 * Keeps existing keys not present in token.
 * @param {object} existing — current openclaw.json
 * @param {object} imported — token config
 * @returns {object} merged config
 */
function mergeConfig(existing, imported) {
  const result = JSON.parse(JSON.stringify(existing));

  for (const [key, value] of Object.entries(imported)) {
    if (value === null) {
      delete result[key];
    } else if (typeof value === "object" && !Array.isArray(value)) {
      result[key] = _deepMerge(result[key] || {}, value);
    } else {
      result[key] = JSON.parse(JSON.stringify(value));
    }
  }

  return result;
}

/**
 * Deep merge two objects.
 * If target is undefined, returns a deep clone of source.
 * Arrays are replaced (not concatenated).
 */
function _deepMerge(target, source) {
  if (target === undefined) {
    return JSON.parse(JSON.stringify(source));
  }
  const result = Array.isArray(target) ? [] : { ...target };
  for (const [key, value] of Object.entries(source)) {
    if (value === null) {
      delete result[key];
    } else if (
      typeof value === "object" &&
      !Array.isArray(value) &&
      typeof result[key] === "object" &&
      result[key] !== null &&
      !Array.isArray(result[key])
    ) {
      result[key] = _deepMerge(result[key], value);
    } else {
      result[key] = JSON.parse(JSON.stringify(value));
    }
  }
  return result;
}

module.exports = { mergeConfig };
