/**
 * import.test.js — Unit tests for config token import
 */

"use strict";

const { importConfigToken } = require("../src/import.js");
const { exportConfigToken } = require("../src/export.js");
const { encode } = require("../src/base64url.js");
const {
  TokenFormatError,
  TokenDecodeError,
  TokenJSONError,
  TokenVersionError,
  CredentialMissingError,
} = require("../src/token-errors.js");

let pass = 0, fail = 0;
function assert(cond, msg) { cond ? pass++ : (fail++, console.error(`FAIL: ${msg}`)); }
function assertEqual(a, b, msg) {
  if (JSON.stringify(a) === JSON.stringify(b)) pass++;
  else { fail++; console.error("FAIL: " + msg); console.error("  Expected: " + JSON.stringify(b)); console.error("  Actual:   " + JSON.stringify(a)); }
}
function assertThrows(fn, cls, msg) {
  try { fn(); fail++; console.error(`FAIL: ${msg} — did not throw`); }
  catch (e) {
    if (cls && !(e instanceof cls)) { fail++; console.error(`FAIL: ${msg} — wrong error type: ${e.name}`); }
    else pass++;
  }
}

// ─── Import: happy path round-trip ────────────────────────────────────────────
console.log("=== import: round-trip ===");

// Build a token manually (no real creds)
function makeToken(config, version = 1, refs = []) {
  const payload = {
    version,
    exportedAt: new Date().toISOString(),
    normalizerVersion: "1.0.0",
    config,
    credentialRefs: refs,
  };
  return "mrconf:v1:" + encode(JSON.stringify(payload));
}

function makeTokenWithDate(exportedAt, config, version = 1, refs = []) {
  const payload = { version, exportedAt, normalizerVersion: "1.0.0", config, credentialRefs: refs };
  return "mrconf:v1:" + encode(JSON.stringify(payload));
}

// No refs → simple round-trip
const inputConfig = {
  agents: { defaults: { model: "minimax/MiniMax-M2.7", timeoutSeconds: 60 } },
  models: { providers: { minimax: { enabled: true } } },
  plugins: { entries: {} },
};
const t1 = makeToken(inputConfig);
const r1 = importConfigToken(t1);
assertEqual(r1.config.agents.defaults.model, "minimax/MiniMax-M2.7", "model preserved");
assertEqual(r1.config.agents.defaults.timeoutSeconds, 60, "timeoutSeconds preserved");
assertEqual(r1.config.models.providers.minimax.enabled, true, "enabled preserved");
assertEqual(r1.credentialRefs, [], "no credentialRefs");

// ─── Import: wrong prefix ──────────────────────────────────────────────────────
console.log("=== import: format errors ===");

assertThrows(() => importConfigToken(""), TokenFormatError, "empty string throws");
assertThrows(() => importConfigToken("mrconf:v2:abc"), TokenVersionError, "wrong version throws");
assertThrows(() => importConfigToken("not-a-token"), TokenFormatError, "random string throws");
assertThrows(() => importConfigToken("mrconf:v1:!!invalid-base64!!"), TokenDecodeError, "invalid base64 throws");
assertThrows(() => importConfigToken("mrconf:v1:YWJj"), TokenJSONError, "valid base64 but invalid JSON throws");

// ─── Import: payload validation ───────────────────────────────────────────────
console.log("=== import: payload validation ===");

// version not 1
const badVersion = makeToken({ config: {}, exportedAt: new Date().toISOString(), normalizerVersion: "1.0.0" }, 99);
assertThrows(() => importConfigToken(badVersion), TokenVersionError, "version != 1 throws");

// missing exportedAt
const badAt = makeTokenWithDate("not-a-date", {}, 1);
assertThrows(() => importConfigToken(badAt), TokenJSONError, "invalid exportedAt throws");

// missing config
const badPayload = { version: 1, exportedAt: new Date().toISOString(), normalizerVersion: "1.0.0", credentialRefs: [], config: null };
assertThrows(() => importConfigToken("mrconf:v1:" + encode(JSON.stringify(badPayload))), TokenJSONError, "null config throws");

// credentialRefs not array
const badRefs = { version: 1, exportedAt: new Date().toISOString(), normalizerVersion: "1.0.0", config: {}, credentialRefs: "not-an-array" };
assertThrows(() => importConfigToken("mrconf:v1:" + encode(JSON.stringify(badRefs))), TokenJSONError, "credentialRefs not array throws");

// ─── Import: credential resolution ────────────────────────────────────────────
console.log("=== import: credential resolution ===");

// Ref not found → CredentialMissingError
const missingRefPayload = {
  version: 1,
  exportedAt: new Date().toISOString(),
  normalizerVersion: "1.0.0",
  config: { models: { providers: { test: { apiKey: "${DOES_NOT_EXIST_12345}" } } } },
  credentialRefs: ["DOES_NOT_EXIST_12345"],
};
const missingRefToken = "mrconf:v1:" + encode(JSON.stringify(missingRefPayload));
assertThrows(() => importConfigToken(missingRefToken), CredentialMissingError, "missing env ref throws");

// Resolved from env
process.env.TEST_API_KEY = "env-secret-value";
const envRefPayload = {
  version: 1,
  exportedAt: new Date().toISOString(),
  normalizerVersion: "1.0.0",
  config: { models: { providers: { test: { apiKey: "${TEST_API_KEY}" } } } },
  credentialRefs: ["TEST_API_KEY"],
};
const envRefToken = "mrconf:v1:" + encode(JSON.stringify(envRefPayload));
const rEnv = importConfigToken(envRefToken);
assertEqual(rEnv.config.models.providers.test.apiKey, "env-secret-value", "env var resolved");
delete process.env.TEST_API_KEY;

// ─── Import: pass resolution ───────────────────────────────────────────────────
// Can't easily test pass without mocking — skip pass tests (integration tests only)

// ─── Summary ──────────────────────────────────────────────────────────────────
console.log("");
console.log(`=== Results: ${pass} passed, ${fail} failed ===`);
if (fail > 0) process.exit(1);
