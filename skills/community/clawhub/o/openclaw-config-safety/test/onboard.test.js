/**
 * onboard.test.js — Unit tests for Phase 3 components
 *
 * Tests: audit, config-patch, restore-backup, export/import integration
 */

"use strict";

const fs = require("fs");

// ─── Setup ───────────────────────────────────────────────────────────────────

const TMP = `/tmp/onboard-test-${process.pid}`;
const HOME_ORIG = process.env.HOME;
try { fs.mkdirSync(TMP, { recursive: true }); } catch {}
process.env.HOME = TMP;
const TEST_CONFIG = `${TMP}/openclaw.json`;
process.env.OPENCLAW_CONFIG = TEST_CONFIG;

let pass = 0, fail = 0;
function assert(cond, msg) { cond ? pass++ : (fail++, console.error(`FAIL: ${msg}`)); }
function assertEqual(a, b, msg) {
  if (JSON.stringify(a) === JSON.stringify(b)) pass++;
  else { fail++; console.error(`FAIL: ${msg}`); console.error(`  Expected: ${JSON.stringify(b)}`); console.error(`  Actual:   ${JSON.stringify(a)}`); }
}

// ─── audit.js tests ───────────────────────────────────────────────────────────

console.log("=== audit.js ===");

const { generateAudit } = require("../src/audit.js");

const minimalConfig = {
  agents: { defaults: { model: "minimax/MiniMax-M2.7" } },
  models: { providers: {} },
  plugins: { entries: {} },
};

const fullConfig = {
  gateway: { bind: "0.0.0.0:18789", port: 18789 },
  agents: {
    defaults: {
      model: "minimax/MiniMax-M2.7",
      compaction: { enabled: true, threshold: 0.75 },
    },
  },
  models: { providers: { minimax: { enabled: true }, cerebras: { enabled: false } } },
  plugins: { entries: { telegram: { enabled: true }, "lossless-claw": { enabled: true } } },
};

assert(generateAudit(minimalConfig).summary.includes("Gateway:"), "minimal config audit includes gateway");
assert(generateAudit(minimalConfig).credentialRefs.length === 0, "no credential refs in empty config");

const fullAudit = generateAudit(fullConfig);
assert(fullAudit.summary.includes("Plugins:      2 configured"), "plugins counted correctly");
assert(fullAudit.summary.includes("Default:      minimax/MiniMax-M2.7"), "default model shown");
assert(fullAudit.summary.includes("Compaction:   enabled"), "compaction shown");

const credConfig = {
  agents: { defaults: {} },
  models: { providers: { cerebras: { apiKey: "${CEREBRAS_API_KEY}" } } },
  plugins: { entries: {} },
};
assert(generateAudit(credConfig).credentialRefs.includes("CEREBRAS_API_KEY"), "credential ref detected");

const dupConfig = {
  agents: { defaults: {} },
  models: {
    providers: {
      a: { apiKey: "${CEREBRAS_API_KEY}" },
      b: { apiKey: "${CEREBRAS_API_KEY}" },
    },
  },
  plugins: { entries: {} },
};
const dupAudit = generateAudit(dupConfig);
assert(dupAudit.credentialRefs.filter((r) => r === "CEREBRAS_API_KEY").length === 1, "duplicate refs deduplicated");

// ─── config-patch.js tests ────────────────────────────────────────────────────

console.log("=== config-patch.js ===");

const { mergeConfig } = require("../src/config-patch.js");

const base = { a: 1, b: 2 };
const import_ = { b: 3, c: 4 };
assertEqual(mergeConfig(base, import_), { a: 1, b: 3, c: 4 }, "basic merge replaces top-level keys");

const deepBase = { agents: { defaults: { model: "a", timeoutSeconds: 30 } } };
const deepImport = { agents: { defaults: { timeoutSeconds: 60 }, newField: true } };
const merged = mergeConfig(deepBase, deepImport);
assertEqual(merged.agents.defaults.model, "a", "deep merge keeps existing keys");
assertEqual(merged.agents.defaults.timeoutSeconds, 60, "deep merge replaces nested keys");
assertEqual(merged.agents.newField, true, "newField from import merged into agents");

assertEqual(mergeConfig({ a: 1, b: 2 }, { b: null }), { a: 1 }, "null value deletes key");

// ─── restore-backup.js tests ──────────────────────────────────────────────────

console.log("=== restore-backup.js ===");

const { createBackup, listBackups, CONFIG_PATH } = require("../src/restore-backup.js");

assert(CONFIG_PATH.endsWith("openclaw.json"), "config path ends with openclaw.json");

fs.writeFileSync(TEST_CONFIG, JSON.stringify({ test: true }));
const { backupPath, timestamp } = createBackup();
assert(fs.existsSync(backupPath), "backup file created");
assert(timestamp.length > 0, "timestamp returned");

const backups = listBackups();
assert(backups.length > 0, "listBackups returns entries");
assert(backups[0].timestamp === timestamp, "backup timestamp matches");

// ─── export/import integration ─────────────────────────────────────────────────

console.log("=== export/import integration ===");

const { exportConfigToken } = require("../src/export.js");
const { importConfigToken } = require("../src/import.js");

const roundConfig = {
  agents: { defaults: { model: "minimax/MiniMax-M2.7", timeoutSeconds: 30 } },
  models: { providers: { minimax: { enabled: true } } },
  plugins: { entries: {} },
};

const token = exportConfigToken(roundConfig);
assert(token.startsWith("mrconf:v1:"), "export produces valid token prefix");

// ─── normalize stability ─────────────────────────────────────────────────────

console.log("=== normalize stability ===");

const { normalizeOpenClawConfig } = require("../src/normalize.js");

const stableConfig = {
  agents: { defaults: { model: "  m2.7  ", timeoutSeconds: "30", compaction: { enabled: "true" } } },
  models: { providers: { minimax: { enabled: true } } },
  plugins: { entries: {} },
};
const { normalized, changed } = normalizeOpenClawConfig(stableConfig);
assert(changed === true, "normalize detects changes");
assertEqual(normalized.agents.defaults.model, "m2.7", "trim applied");
assertEqual(normalized.agents.defaults.timeoutSeconds, 30, "number coercion applied");
assertEqual(normalized.agents.defaults.compaction.enabled, true, "boolean coercion applied");

// ─── Error classes ────────────────────────────────────────────────────────────

console.log("=== error classes ===");

const tokenErrors = require("../src/token-errors.js");
const errors = require("../src/errors.js");

const te = new tokenErrors.TokenFormatError();
assertEqual(te.name, "TokenFormatError", "TokenFormatError name");
assert(te.message.includes("mrconf:v1"), "TokenFormatError message");

const ce = new tokenErrors.CredentialMissingError("${CEREBRAS_API_KEY}");
assertEqual(ce.ref, "${CEREBRAS_API_KEY}", "CredentialMissingError includes ref");
assert(!ce.message.includes("cerebras_api_key") && !ce.message.includes("sk-"), "error does not expose value");

const ne = new errors.NormalizationError("agents.defaults.model", "must be a string");
assertEqual(ne.field, "agents.defaults.model", "NormalizationError includes field path");

// ─── Summary ─────────────────────────────────────────────────────────────────

process.env.HOME = HOME_ORIG;
try { fs.rmSync(TMP, { recursive: true, force: true }); } catch {}

console.log("");
console.log(`=== Results: ${pass} passed, ${fail} failed ===`);
if (fail > 0) process.exit(1);
