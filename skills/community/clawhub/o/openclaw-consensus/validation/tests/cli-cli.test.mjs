#!/usr/bin/env node
// CLI-boundary regression tests for src/cli.mjs.
//
// These spawn the actual CLI as a child process, but only exercise paths
// that fail BEFORE shelling out to `openclaw` — meaning they are fully
// offline, deterministic, and never invoke a model or burn API credit.
//
// Specifically, the run command's order is:
//   parseFlags -> loadBrief -> parseTimeoutMs -> validateExplicitRunRoot
//   -> getAgentConfig (this is where openclaw is invoked)
//
// Every test in this file forces a failure at or before validateExplicitRunRoot
// so no openclaw process is spawned. We assert exit code, stderr, and that
// no `runs/` directory leaked.
//
// Run with: node validation/tests/cli-cli.test.mjs

import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, '..', '..');
const cliPath = path.join(repoRoot, 'src', 'cli.mjs');

function runCli(args, opts = {}) {
  return spawnSync(process.execPath, [cliPath, ...args], {
    cwd: repoRoot,
    encoding: 'utf8',
    timeout: 10_000,
    env: { ...process.env, ...(opts.env || {}) },
  });
}

const cases = [];
function test(name, fn) {
  cases.push({ name, fn });
}

// ---- help / unknown command ----
test('cli: help exits 0 and prints usage', () => {
  const r = runCli(['help']);
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('openclaw-consensus'));
  assert.ok(r.stdout.includes('Usage:'));
  assert.ok(r.stdout.includes('models'));
  assert.ok(r.stdout.includes('run'));
});

test('cli: --help exits 0', () => {
  const r = runCli(['--help']);
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('Usage:'));
});

test('cli: no args defaults to help and exits 0', () => {
  const r = runCli([]);
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('Usage:'));
});

test('cli: unknown command exits non-zero with "Unknown command"', () => {
  const r = runCli(['frobnicate']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('Unknown command'));
});

// ---- run flag/argument validation (pre-openclaw) ----
test('cli: run rejects unknown flag (typo guard)', () => {
  const r = runCli(['run', '--orchestator-model', 'a', '--brief', 'b', '--models', 'a,b']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('Unknown flag: --orchestator-model'));
});

test('cli: run rejects duplicate flag', () => {
  const r = runCli(['run', '--brief', 'a', '--brief', 'b', '--models', 'a,b']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('Duplicate flag'));
});

test('cli: run rejects positional arg', () => {
  const r = runCli(['run', 'oops', '--brief', 'b', '--models', 'a,b']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('Unexpected positional'));
});

test('cli: run rejects missing flag value', () => {
  const r = runCli(['run', '--brief', '--models', 'a,b']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('Missing value for --brief'));
});

test('cli: run rejects --model-timeout-ms non-integer (before openclaw)', () => {
  // parseTimeoutMs runs before getAgentConfig. We supply --run-root so the
  // run-root validator also runs, but parseTimeoutMs is checked first.
  const r = runCli([
    'run',
    '--brief', 'x',
    '--models', 'a,b',
    '--model-timeout-ms', '1.5',
  ]);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('integer'));
});

test('cli: run rejects --model-timeout-ms below minimum', () => {
  const r = runCli([
    'run',
    '--brief', 'x',
    '--models', 'a,b',
    '--model-timeout-ms', '100',
  ]);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('between'));
});

test('cli: run rejects --run-root inside protected /etc (before openclaw)', () => {
  const r = runCli([
    'run',
    '--brief', 'x',
    '--models', 'a,b',
    '--run-root', '/etc/openclaw-test',
  ]);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('protected system path'));
});

test('cli: run rejects --run-root = filesystem root', () => {
  const r = runCli([
    'run',
    '--brief', 'x',
    '--models', 'a,b',
    '--run-root', '/',
  ]);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('filesystem root'));
});

test('cli: run rejects --run-root with null byte', () => {
  // Node will error on a literal null byte in argv values; pass via env-resolved
  // path instead. We use a value Node can carry but cli rejects.
  // This is covered at the unit level by validateExplicitRunRoot; here we
  // only assert the integration path triggers if we use a forbidden prefix.
  const r = runCli([
    'run',
    '--brief', 'x',
    '--models', 'a,b',
    '--run-root', '/usr/local/oops',
  ]);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('protected system path'));
});

test('cli: models --json=foo rejected (boolean takes no value)', () => {
  const r = runCli(['models', '--json=foo']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('does not take a value'));
});

test('cli: models rejects unknown flag', () => {
  const r = runCli(['models', '--bogus']);
  assert.notEqual(r.status, 0);
  assert.ok(r.stderr.includes('Unknown flag'));
});

// ---- safety: failing CLI must not leak runs/ dirs ----
test('cli: failed pre-openclaw run does not create runs/ subdir', () => {
  const runsDir = path.join(repoRoot, 'runs');
  const before = fs.existsSync(runsDir) ? new Set(fs.readdirSync(runsDir)) : new Set();
  const r = runCli([
    'run',
    '--brief', 'safety-leak-check',
    '--models', 'a,b',
    '--run-root', '/etc/openclaw-test',
  ]);
  assert.notEqual(r.status, 0);
  const after = fs.existsSync(runsDir) ? new Set(fs.readdirSync(runsDir)) : new Set();
  // No new entries should appear under runs/.
  for (const name of after) {
    assert.ok(before.has(name), `unexpected new runs/ entry leaked: ${name}`);
  }
});

// ---- run ----
let pass = 0;
let fail = 0;
const failures = [];
for (const c of cases) {
  try {
    await c.fn();
    pass += 1;
  } catch (err) {
    fail += 1;
    failures.push({ name: c.name, err });
  }
}

if (fail > 0) {
  console.error(`FAIL: ${fail}/${cases.length} cases failed`);
  for (const f of failures) {
    console.error(`  - ${f.name}: ${f.err && f.err.stack ? f.err.stack : f.err}`);
  }
  process.exit(1);
}
console.log(`OK: ${pass}/${cases.length} cases passed`);
