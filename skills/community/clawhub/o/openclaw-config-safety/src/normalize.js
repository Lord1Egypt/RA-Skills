/**
 * normalize.js — Core config normalization
 *
 * Design philosophy: normalize only what is unambiguously correct.
 * Fail loudly on anything requiring judgment.
 *
 * Security: never expose field values in errors; paths only.
 */

"use strict";

const { NormalizationError, NormalizationWarning } = require("./errors.js");
const { resolveCanonical, isAlias } = require("./alias-map.js");

// ─── Field path definitions ───────────────────────────────────────────────────

/** Fields that should NOT be normalized (opaque secrets/tokens) */
const OPAQUE_FIELDS = new Set([
  "models.providers.<provider>.apiKey",
  "models.providers.<provider>.apiSecret",
  "models.providers.<provider>.authHeader",
]);

/** Fields trimmed (Category A) */
const TRIM_FIELDS = [
  "agents.defaults.model",
  "agents.defaults.workspace",
  "agents.defaults.models.<key>.alias",
  "models.providers.<provider>.baseURL",
  "gateway.bind",
  "gateway.remoteUrl",
  "plugins.entries.<key>",
];

/** Fields boolean-coerced (Category B) */
const BOOL_FIELDS = [
  "agents.defaults.compaction.enabled",
  "agents.defaults.memorySearch.enabled",
  "models.providers.<provider>.enabled",
  "plugins.entries.<key>.enabled",
];

/** Fields number-coerced (Category C) */
const NUMBER_FIELDS = [
  "agents.defaults.timeoutSeconds",
  "agents.defaults.compaction.threshold",
  "agents.defaults.bootstrapMaxChars",
  "gateway.port",
  "models.providers.<provider>.contextWindow",
];

// ─── Utility helpers ─────────────────────────────────────────────────────────

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isString(value) {
  return typeof value === "string";
}

function isBlankString(value) {
  return isString(value) && value.trim() === "";
}

function trimTrailingSlash(path) {
  return path.replace(/\/+$/, "");
}

// ─── Field matching ───────────────────────────────────────────────────────────

/**
 * Match a field path pattern against an actual path.
 * Supports: exact match, <provider>, <key> wildcards.
 */
function matchField(actualPath, pattern) {
  if (actualPath === pattern) return true;

  const patternParts = pattern.split(".");
  const actualParts = actualPath.split(".");

  if (patternParts.length !== actualParts.length) return false;

  for (let i = 0; i < patternParts.length; i++) {
    const p = patternParts[i];
    if (p === "<provider>" || p === "<key>") continue;
    if (p !== actualParts[i]) return false;
  }
  return true;
}

function matchesAnyPattern(actualPath, patterns) {
  return patterns.some((p) => matchField(actualPath, p));
}

// ─── Normalization rules ─────────────────────────────────────────────────────

function shouldOpaque(fieldPath) {
  // Check for API key / secret / auth header patterns
  if (fieldPath.endsWith(".apiKey")) return true;
  if (fieldPath.endsWith(".apiSecret")) return true;
  if (fieldPath.endsWith(".authHeader")) return true;
  if (fieldPath.match(/token|password|secret|key/i) && fieldPath.includes("env")) return true;
  return false;
}

function trimValue(fieldPath, value, warnings) {
  if (!isString(value)) return value;
  // workspace: trim trailing slashes only
  if (fieldPath === "agents.defaults.workspace") {
    return trimTrailingSlash(value);
  }
  // Generic trim for other fields
  const trimmed = value.trim();
  if (value !== trimmed) {
    warnings.push(new NormalizationWarning(fieldPath, `trimmed whitespace`));
  }
  return trimmed;
}

function coerceBoolean(fieldPath, value, warnings) {
  if (value === "true") {
    warnings.push(new NormalizationWarning(fieldPath, `coerced string "true" → boolean true`));
    return true;
  }
  if (value === "false") {
    warnings.push(new NormalizationWarning(fieldPath, `coerced string "false" → boolean false`));
    return false;
  }
  return value; // leave as-is
}

function coerceNumber(fieldPath, value, warnings) {
  if (!isString(value)) return value;
  if (value === "") return value; // empty string: pass through
  const n = Number(value);
  if (String(n) !== value) {
    // Not a valid numeric string — leave as-is (warning already surfaced by caller)
    return value;
  }
  if (!isFinite(n)) return value; // NaN, Infinity: pass through

  // Check safe integer range
  if (!Number.isSafeInteger(n)) {
    warnings.push(new NormalizationWarning(fieldPath, `number ${n} outside safe integer range`));
  }

  // Return as number type
  warnings.push(new NormalizationWarning(fieldPath, `coerced string "${value}" → number ${n}`));
  return n;
}

// ─── Recursive traversal ─────────────────────────────────────────────────────

/**
 * Recursively normalize an object.
 * Returns { normalized, aliasInfo, warnings, changed }
 */
function normalizeValue(fieldPath, value, aliasInfo, warnings) {
  // null → pass through
  if (value === null) return value;

  // undefined → remove from parent (will be handled by caller)
  if (value === undefined) return undefined;

  // Primitives
  if (!isObject(value)) {
    // String: check trim fields
    if (isString(value)) {
      if (shouldOpaque(fieldPath)) return value;

      if (matchesAnyPattern(fieldPath, TRIM_FIELDS)) {
        const trimmed = trimValue(fieldPath, value, warnings);
        return trimmed;
      }

      // workspace: trim trailing slashes
      if (fieldPath === "agents.defaults.workspace") {
        return trimValue(fieldPath, value, warnings);
      }
    }

    // Boolean coercion
    if (matchesAnyPattern(fieldPath, BOOL_FIELDS) && isString(value)) {
      return coerceBoolean(fieldPath, value, warnings);
    }

    // Number coercion
    if (matchesAnyPattern(fieldPath, NUMBER_FIELDS) && isString(value)) {
      const result = coerceNumber(fieldPath, value, warnings);
      return result;
    }

    return value;
  }

  // Array: pass through (Category D)
  if (Array.isArray(value)) {
    // Arrays of objects: recurse into each element if it looks like a config object
    return value.map((item, i) => {
      if (isObject(item)) {
        return normalizeValue(`${fieldPath}[${i}]`, item, aliasInfo, warnings);
      }
      return item;
    });
  }

  // Object: deep traversal (Category E)
  const result = {};
  let changed = false;

  for (const [key, val] of Object.entries(value)) {
    const childPath = fieldPath ? `${fieldPath}.${key}` : key;

    // Skip env subtrees (opaque)
    if (childPath.endsWith(".env") || childPath === "env") continue;

    // Skip secret:// refs (opaque) — preserve as-is, don't recurse
    if (isString(val) && val.startsWith("secret://")) {
      result[key] = val;
      continue;
    }

    // Skip status/note in per-model overrides (known-crash, validator handles)
    if (childPath.includes("agents.defaults.models.") && (key === "status" || key === "note")) {
      continue;
    }

    // Skip custom plugin config blobs (pass through untouched)
    // EXCEPT: always recurse into plugin configs to find enabled/alias fields
    if (childPath.startsWith("plugins.entries.") && isObject(val)) {
      result[key] = normalizeValue(childPath, val, aliasInfo, warnings);
      continue;
    }

    // env: skip (already handled above)
    // Skip if key is "env"
    if (key === "env") continue;

    const normalized = normalizeValue(childPath, val, aliasInfo, warnings);
    result[key] = normalized;
  }

  return result;
}

// ─── Alias detection pass ─────────────────────────────────────────────────────

function detectAliases(config, aliasInfo) {
  const modelFieldPaths = [
    { path: "agents.defaults.model", value: config.agents?.defaults?.model },
    { path: "agents.defaults.imageModel", value: config.agents?.defaults?.imageModel },
    { path: "agents.defaults.pdfModel", value: config.agents?.defaults?.pdfModel },
  ];

  // Traverse agents.defaults.models
  const models = config.agents?.defaults?.models || {};
  for (const [modelKey, override] of Object.entries(models)) {
    if (!isObject(override)) continue;
    const alias = override.alias;
    if (alias && isAlias(alias)) {
      const canonical = resolveCanonical(alias.trim());
      aliasInfo.push({
        field: `agents.defaults.models["${modelKey}"].alias`,
        alias: alias.trim(),
        canonical,
      });
    }
  }

  // Check model field paths
  for (const { path, value } of modelFieldPaths) {
    if (value && isAlias(value)) {
      const canonical = resolveCanonical(value.trim());
      aliasInfo.push({ field: path, alias: value.trim(), canonical });
    }
  }
}

// ─── Required fields check ────────────────────────────────────────────────────

function checkRequiredFields(config, errors) {
  const required = ["agents", "models", "plugins"];
  for (const field of required) {
    if (!(field in config)) {
      errors.push(new NormalizationError("top-level", `openclaw.json is missing required top-level field: ${field}`));
    } else if (config[field] === null || (isObject(config[field]) && Object.keys(config[field]).length === 0)) {
      // Empty but present — warn but don't fail
      // (let Zod handle it)
    }
  }
}

// ─── Main export ─────────────────────────────────────────────────────────────

/**
 * @param {object} config - raw openclaw.json config object
 * @returns {{ normalized: object, aliasInfo: object[], warnings: string[], changed: boolean }}
 */
function normalizeOpenClawConfig(config) {
  if (!isObject(config)) {
    throw new NormalizationError("top-level", "config must be an object");
  }

  const warnings = [];
  const aliasInfo = [];
  const errors = [];

  // Required fields check
  checkRequiredFields(config, errors);
  if (errors.length > 0) {
    const msg = errors.map((e) => e.message).join("; ");
    throw new Error(msg);
  }

  // Alias detection pass (informational, before normalization)
  detectAliases(config, aliasInfo);

  // Main normalization pass
  const normalized = normalizeValue("", config, aliasInfo, warnings);

  // Check if anything changed (deep comparison is expensive; use heuristics)
  const changed = warnings.length > 0 || aliasInfo.length > 0;

  return {
    normalized,
    aliasInfo,
    warnings: warnings.map((w) => w.toString()),
    changed,
  };
}

// ─── File-based normalization ─────────────────────────────────────────────────

const fs = require("fs");
const path = require("path");

async function normalizeFile(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const config = JSON.parse(raw);
  return normalizeOpenClawConfig(config);
}

module.exports = { normalizeOpenClawConfig, normalizeFile };
