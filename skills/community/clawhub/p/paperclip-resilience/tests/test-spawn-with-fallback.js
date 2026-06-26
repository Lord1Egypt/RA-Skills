#!/usr/bin/env node
/**
 * Tests for configurable spawn-with-fallback module.
 *
 * Validates: config loading, alias resolution, failure detection,
 * config override behavior, and backward compatibility.
 *
 * Run: node skills/paperclip-resilience/tests/test-spawn-with-fallback.js
 */

'use strict';

const path = require('path');
const fs = require('fs');

const {
  loadConfig,
  resolveModel,
  detectFailure,
  extractReason,
  DEFAULT_ALIASES,
  DEFAULT_FALLBACKS,
  DEFAULT_FAILURE_PATTERN_STRINGS,
  DEFAULT_FAILURE_STOP_REASONS,
} = require('../src/spawn-with-fallback');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    console.log(`  ✅ ${label}`);
    passed++;
  } else {
    console.error(`  ❌ FAIL: ${label}`);
    failed++;
  }
}

function assertEq(actual, expected, label) {
  if (actual === expected) {
    console.log(`  ✅ ${label}`);
    passed++;
  } else {
    console.error(`  ❌ FAIL: ${label} — expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
    failed++;
  }
}

// ── Test: defaults are populated ──
console.log('\n── defaults: built-in maps are populated ──');
assert(Object.keys(DEFAULT_ALIASES).length >= 8, 'DEFAULT_ALIASES has entries');
assert(Object.keys(DEFAULT_FALLBACKS).length >= 8, 'DEFAULT_FALLBACKS has entries');
assert(DEFAULT_FAILURE_PATTERN_STRINGS.length >= 10, 'DEFAULT_FAILURE_PATTERN_STRINGS has entries');
assert(DEFAULT_FAILURE_STOP_REASONS.length >= 3, 'DEFAULT_FAILURE_STOP_REASONS has entries');

// ── Test: loadConfig with no config file returns defaults ──
console.log('\n── loadConfig: no config file → defaults ──');
const defaultCfg = loadConfig();
assert(Object.keys(defaultCfg.aliases).length >= 8, 'aliases populated from defaults');
assert(Object.keys(defaultCfg.fallbacks).length >= 8, 'fallbacks populated from defaults');
assert(defaultCfg.failurePatterns.length >= 10, 'failurePatterns populated from defaults');
assert(defaultCfg.failureStopReasons instanceof Set, 'failureStopReasons is a Set');
assert(defaultCfg.failureStopReasons.has('error'), 'failureStopReasons contains "error"');

// ── Test: loadConfig with explicit config file ──
console.log('\n── loadConfig: explicit config file with overrides ──');

const tmpConfig = path.join(__dirname, '_test-config.json');
fs.writeFileSync(tmpConfig, JSON.stringify({
  aliases: {
    '$doc': 'test aliases',
    'myalias': 'custom/model-v1',
    'sonnet': 'custom/sonnet-override',
  },
  fallbacks: {
    '$doc': 'test fallbacks',
    'custom/model-v1': 'custom/fallback-v1',
  },
  failurePatterns: {
    patterns: ['custom_error', 'out_of_tokens'],
  },
  failureStopReasons: {
    reasons: ['custom_stop'],
  },
}));

try {
  const customCfg = loadConfig(tmpConfig);

  // Custom aliases overlay on defaults
  assertEq(customCfg.aliases['myalias'], 'custom/model-v1', 'custom alias added');
  assertEq(customCfg.aliases['sonnet'], 'custom/sonnet-override', 'default alias overridden');
  assertEq(customCfg.aliases['haiku'], 'anthropic/claude-haiku-4-5', 'non-overridden default alias preserved');

  // Custom fallback added; defaults also present
  assertEq(customCfg.fallbacks['custom/model-v1'], 'custom/fallback-v1', 'custom fallback added');
  assert('anthropic/claude-opus-4-6' in customCfg.fallbacks, 'default fallback preserved');

  // Custom failure patterns replace defaults entirely
  assertEq(customCfg.failurePatterns.length, 2, 'custom failurePatterns replaces default list');
  assert(customCfg.failurePatterns[0].test('custom_error'), 'custom pattern matches');

  // Custom stop reasons replace defaults
  assert(customCfg.failureStopReasons.has('custom_stop'), 'custom stop reason present');
  assert(!customCfg.failureStopReasons.has('error'), 'default stop reason NOT present when overridden');

} finally {
  fs.unlinkSync(tmpConfig);
}

// ── Test: loadConfig rejects missing explicit path ──
console.log('\n── loadConfig: missing explicit path → throws ──');
let threwOnMissing = false;
try {
  loadConfig('/nonexistent/path/config.json');
} catch (e) {
  threwOnMissing = e.message.includes('not found');
}
assert(threwOnMissing, 'throws on missing explicit config path');

// ── Test: $doc keys are stripped from config ──
console.log('\n── loadConfig: $doc keys stripped ──');
const docConfig = path.join(__dirname, '_test-doc-config.json');
fs.writeFileSync(docConfig, JSON.stringify({
  aliases: { '$doc': 'ignore me', 'test': 'val/model' },
  fallbacks: { '$doc': 'ignore me too', 'val/model': 'val/fallback' },
}));
try {
  const cfg = loadConfig(docConfig);
  assert(!('$doc' in cfg.aliases), '$doc stripped from aliases');
  assert(!('$doc' in cfg.fallbacks), '$doc stripped from fallbacks');
  assertEq(cfg.aliases['test'], 'val/model', 'non-$doc alias preserved');
} finally {
  fs.unlinkSync(docConfig);
}

// ── Test: resolveModel ──
console.log('\n── resolveModel: alias resolution ──');
const aliases = defaultCfg.aliases;
assertEq(resolveModel('sonnet', aliases), 'anthropic/claude-sonnet-4-6', 'resolves "sonnet"');
assertEq(resolveModel('SONNET', aliases), 'anthropic/claude-sonnet-4-6', 'case-insensitive');
assertEq(resolveModel('  haiku  ', aliases), 'anthropic/claude-haiku-4-5', 'trims whitespace');
assertEq(resolveModel('codex', aliases), 'openai-codex/gpt-5.3-codex', 'resolves "codex"');
assertEq(resolveModel('unknown/model', aliases), 'unknown/model', 'passes through unknown models');

let threwOnEmpty = false;
try { resolveModel('', aliases); } catch (e) { threwOnEmpty = true; }
assert(threwOnEmpty, 'throws on empty model');

let threwOnNull = false;
try { resolveModel(null, aliases); } catch (e) { threwOnNull = true; }
assert(threwOnNull, 'throws on null model');

// ── Test: detectFailure ──
console.log('\n── detectFailure: pattern matching ──');
const fp = defaultCfg.failurePatterns;
const fsr = defaultCfg.failureStopReasons;

// Non-zero exit with matching pattern
let r = detectFailure(1, 'Error: no credits remaining', fp, fsr);
assert(r.failed === true, 'detects "no credits" failure');
assertEq(r.reason, 'credits_exhausted', 'reason: credits_exhausted');

r = detectFailure(1, 'HTTP 402 Payment Required', fp, fsr);
assert(r.failed === true, 'detects 402 failure');
assertEq(r.reason, 'payment_required', 'reason: payment_required');

r = detectFailure(1, 'rate limit exceeded', fp, fsr);
assert(r.failed === true, 'detects rate limit');
assertEq(r.reason, 'rate_limit', 'reason: rate_limit');

r = detectFailure(1, 'provider error: backend unavailable', fp, fsr);
assert(r.failed === true, 'detects provider error');
assertEq(r.reason, 'provider_error', 'reason: provider_error');

// Non-zero exit with no matching pattern → spawn_error
r = detectFailure(1, 'some random error', fp, fsr);
assert(r.failed === true, 'non-zero exit without pattern still fails');
assertEq(r.reason, 'spawn_error', 'reason: spawn_error for unknown');

// Exit 0 with matching pattern in output (embedded error)
r = detectFailure(0, 'task completed but quota_exceeded in background', fp, fsr);
assert(r.failed === true, 'detects embedded quota_exceeded on exit 0');

// Exit 0 with stop_reason JSON
r = detectFailure(0, '{"stop_reason": "credits_exhausted"}', fp, fsr);
assert(r.failed === true, 'detects stop_reason credits_exhausted');

// Exit 0, clean output
r = detectFailure(0, 'All good, task completed successfully', fp, fsr);
assert(r.failed === false, 'clean output is not a failure');

// ── Test: extractReason priority ──
console.log('\n── extractReason: classification priority ──');
assertEq(extractReason('credits_exhausted'), 'credits_exhausted', 'credits_exhausted');
assertEq(extractReason('quota_exceeded'), 'quota_exceeded', 'quota_exceeded');
assertEq(extractReason('http 402'), 'payment_required', '402 → payment_required');
assertEq(extractReason('billing issue'), 'billing_error', 'billing → billing_error');
assertEq(extractReason('rate limited'), 'rate_limit', 'rate limited → rate_limit');
assertEq(extractReason('insufficient_quota'), 'quota_exceeded', 'insufficient_quota → quota_exceeded');
assertEq(extractReason('no credits'), 'credits_exhausted', 'no credits → credits_exhausted');
assertEq(extractReason('provider error'), 'provider_error', 'provider error');
assertEq(extractReason('unknown'), 'spawn_error', 'unknown → spawn_error');

// ── Test: backward compat — defaults match original hardcoded values ──
console.log('\n── backward compat: defaults match original hardcoded values ──');
assertEq(DEFAULT_ALIASES['sonnet'], 'anthropic/claude-sonnet-4-6', 'sonnet alias matches original');
assertEq(DEFAULT_ALIASES['opus'], 'anthropic/claude-opus-4-6', 'opus alias matches original');
assertEq(DEFAULT_ALIASES['codex'], 'openai-codex/gpt-5.3-codex', 'codex alias matches original');
assertEq(DEFAULT_FALLBACKS['anthropic/claude-sonnet-4-6'], 'openai-codex/gpt-5.3-codex', 'sonnet fallback matches original');
assertEq(DEFAULT_FALLBACKS['anthropic/claude-opus-4-6'], 'openai-codex/gpt-5.3-codex', 'opus fallback matches original');
assertEq(DEFAULT_FALLBACKS['openai-codex/gpt-5.3-codex'], 'anthropic/claude-sonnet-4-6', 'codex fallback matches original');

// ── Summary ──
console.log(`\n${'='.repeat(50)}`);
console.log(`Results: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
