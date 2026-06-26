/**
 * audit.js — Config summary generator
 *
 * Produces a human-readable audit of an openclaw.json config.
 * Read-only — never modifies config.
 */

"use strict";

const { normalizeOpenClawConfig } = require("./normalize.js");

/**
 * @param {object} config — raw openclaw.json
 * @returns {{ summary: string, warnings: string[], credentialRefs: string[] }}
 */
function generateAudit(config) {
  const warnings = [];
  const credentialRefs = [];

  // Normalize and get warnings
  let normalized;
  try {
    const result = normalizeOpenClawConfig(config);
    normalized = result.normalized;
    warnings.push(...result.warnings);
  } catch {
    normalized = config;
  }

  // Extract credential refs from original config
  _walkStrings(config, (path, value) => {
    const match = value.match(/^\$\{([A-Z_][A-Z0-9_]*)\}$/);
    if (match) credentialRefs.push(match[1]);
  });

  const lines = [];

  // Gateway
  const gateway = config.gateway || {};
  const bind = gateway.bind || "localhost:18789";
  const port = gateway.port || 18789;
  lines.push(`Gateway:      ${bind}`);
  if (typeof port === "number") {
    lines.push(`Port:         ${port}`);
  }

  // Plugins
  const plugins = config.plugins || {};
  const pluginEntries = plugins.entries || {};
  const pluginCount = Object.keys(pluginEntries).length;
  const loaded = Object.entries(pluginEntries)
    .filter(([, v]) => v && v.enabled !== false)
    .map(([k]) => k)
    .sort();
  lines.push(`Plugins:      ${pluginCount} configured (${loaded.join(", ") || "none"})`);

  // Models
  const models = config.models || {};
  const providers = models.providers || {};
  const providerNames = Object.keys(providers).sort();
  lines.push(`Providers:    ${providerNames.length} (${providerNames.join(", ") || "none"})`);

  // Default model
  const rawDefault = config.agents?.defaults?.model;
  let defaultModel = "not set";
  if (typeof rawDefault === "string") {
    defaultModel = rawDefault;
  } else if (typeof rawDefault === "object" && rawDefault !== null) {
    // Object form: { "provider/model": { ... } } — show provider/model key
    defaultModel = Object.keys(rawDefault)[0] || "not set";
  }
  lines.push(`Default:      ${defaultModel}`);

  // Compaction
  const compaction = config.agents?.defaults?.compaction || {};
  if (compaction.enabled !== undefined) {
    lines.push(`Compaction:   ${compaction.enabled ? "enabled" : "disabled"} (threshold: ${compaction.threshold || "default"})`);
  }

  // Credential refs
  if (credentialRefs.length > 0) {
    const unique = [...new Set(credentialRefs)];
    lines.push(`Credentials:  ${unique.length} reference(s): ${unique.join(", ")}`);
  }

  // Warnings from normalization
  const normWarnings = warnings.filter((w) => !credentialRefs.some((c) => w.includes(`\${${c}}`)));
  if (normWarnings.length > 0) {
    // Skip — these will be surfaced separately
  }

  const summary = lines.join("\n");
  return { summary, warnings: normWarnings, credentialRefs: [...new Set(credentialRefs)] };
}

/**
 * @param {object} obj
 * @param {(path: string, value: string) => void} visitor
 */
function _walkStrings(obj, visitor, path = "") {
  if (obj === null || typeof obj !== "object" || Array.isArray(obj)) return;
  for (const [key, val] of Object.entries(obj)) {
    const childPath = path ? `${path}.${key}` : key;
    if (typeof val === "string") {
      visitor(childPath, val);
    } else if (Array.isArray(val)) {
      val.forEach((item, i) => {
        if (typeof item === "string") visitor(`${childPath}[${i}]`, item);
        else if (item !== null && typeof item === "object") _walkStrings(item, visitor, `${childPath}[${i}]`);
      });
    } else if (val !== null && typeof val === "object") {
      _walkStrings(val, visitor, childPath);
    }
  }
}

module.exports = { generateAudit };
