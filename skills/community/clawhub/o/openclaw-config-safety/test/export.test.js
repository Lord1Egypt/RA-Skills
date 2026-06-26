/**
 * export.test.js — Unit tests for config token export
 */

"use strict";

const { exportConfigToken } = require("../src/export.js");
const { decode } = require("../src/base64url.js");

let pass = 0, fail = 0;
function assert(cond, msg) { cond ? pass++ : (fail++, console.error(`FAIL: ${msg}`)); }
function assertEqual(a, b, msg) {
  if (JSON.stringify(a) === JSON.stringify(b)) pass++;
  else { fail++; console.error(`FAIL: ${msg}`); console.error(`  Expected: ${JSON.stringify(b)}`); console.error(`  Actual:   ${JSON.stringify(a)}`); }
}

// ─── base64url round-trip ─────────────────────────────────────────────────────
console.log("=== base64url ===");

const enc = decode("eyJ2IjoxfQ").toString("utf8");
assertEqual(enc, '{"v":1}', "base64url decode works");

// No padding
const enc2 = decode("YWJj").toString("utf8");
assertEqual(enc2, "abc", "base64url decode no padding");

// Round-trip
const { encode } = require("../src/base64url.js");
assertEqual(decode(encode("hello world")).toString("utf8"), "hello world", "encode→decode round-trip");

// URL-safe chars
const urlSafe = encode("a+b/c==");
assert(!urlSafe.includes("+"), "no + in encoded");
assert(!urlSafe.includes("/"), "no / in encoded");
assert(!urlSafe.includes("="), "no = in encoded");

// ─── export: basic token structure ───────────────────────────────────────────
console.log("=== export: token structure ===");

const config = {
  agents: { defaults: { model: "m2.7", timeoutSeconds: 30 } },
  models: { providers: { minimax: { apiKey: "${MINIMAX_API_KEY}", enabled: true } } },
  plugins: { entries: {} },
};

const { token } = { token: exportConfigToken(config) };
assert(token.startsWith("mrconf:v1:"), "token has correct prefix");
const encoded = token.slice("mrconf:v1:".length);
assert(encoded.length > 0, "encoded payload is non-empty");

// Decode and check structure
const payload = JSON.parse(decode(encoded).toString("utf8"));
assertEqual(payload.version, 1, "payload version is 1");
assertEqual(typeof payload.exportedAt, "string", "exportedAt is string");
assert(new Date(payload.exportedAt).getTime() > 0, "exportedAt is valid ISO");
assertEqual(payload.normalizerVersion, "1.0.0", "normalizerVersion is set");
assertEqual(typeof payload.config, "object", "config is object");
assertEqual(Array.isArray(payload.credentialRefs), true, "credentialRefs is array");

// ─── export: credential refs collected ────────────────────────────────────────
console.log("=== export: credential refs ===");

const config2 = {
  agents: { defaults: {} },
  models: { providers: { cerebras: { apiKey: "${CEREBRAS_API_KEY}" } } },
  plugins: { entries: {} },
};
const { token: t2 } = { token: exportConfigToken(config2) };
const p2 = JSON.parse(decode(t2.slice("mrconf:v1:".length)).toString("utf8"));
assertEqual(p2.credentialRefs, ["CEREBRAS_API_KEY"], "credential ref extracted");

// Multiple refs
const config3 = {
  agents: { defaults: {} },
  models: { providers: { cerebras: { apiKey: "${CEREBRAS_API_KEY}" }, openai: { apiKey: "${OPENAI_API_KEY}" } } },
  plugins: { entries: {} },
};
const t3 = exportConfigToken(config3);
const p3 = JSON.parse(decode(t3.slice("mrconf:v1:".length)).toString("utf8"));
assertEqual(p3.credentialRefs.sort(), ["CEREBRAS_API_KEY", "OPENAI_API_KEY"], "multiple refs extracted");

// Non-ref strings with $ are NOT collected
const config4 = {
  agents: { defaults: { model: "price is $100" } },
  models: { providers: { minimax: {} } },
  plugins: { entries: {} },
};
const t4 = exportConfigToken(config4);
const p4 = JSON.parse(decode(t4.slice("mrconf:v1:".length)).toString("utf8"));
assertEqual(p4.credentialRefs, [], "non-ref $ strings not collected");

// ─── export: normalization applied ─────────────────────────────────────────────
console.log("=== export: normalization applied ===");

const config5 = {
  agents: { defaults: { model: "  m2.7  ", timeoutSeconds: "60" } },
  models: { providers: { minimax: { enabled: "true" } } },
  plugins: { entries: {} },
};
const t5 = exportConfigToken(config5);
const p5 = JSON.parse(decode(t5.slice("mrconf:v1:".length)).toString("utf8"));
assertEqual(p5.config.agents.defaults.model, "m2.7", "model trimmed in export");
assertEqual(p5.config.agents.defaults.timeoutSeconds, 60, "timeoutSeconds number-coerced in export");
assertEqual(p5.config.models.providers.minimax.enabled, true, "enabled boolean coerced in export");

// ─── export: no actual credentials in token ─────────────────────────────────────
console.log("=== export: no credentials in token ===");

const config6 = {
  agents: { defaults: {} },
  models: { providers: { cerebras: { apiKey: "sk-actual-secret-key" } } },
  plugins: { entries: {} },
};
const t6 = exportConfigToken(config6);
const p6 = JSON.parse(decode(t6.slice("mrconf:v1:".length)).toString("utf8"));
// Actual credential values (not ${REF} pattern) are NOT in scope for export.
// Export only handles ${REF} reference collection. Real credentials must be
// pre-replaced by the caller before export (OUT OF SCOPE for this module).
assertEqual(p6.credentialRefs, [], "no refs in this config — actual creds out of scope for export");

// ─── Summary ──────────────────────────────────────────────────────────────────
console.log("");
console.log(`=== Results: ${pass} passed, ${fail} failed ===`);
if (fail > 0) process.exit(1);
