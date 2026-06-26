/**
 * Tests for create_campaign.js, pay_fee.js, top_up.js
 * Run: node --test test/create_campaign.test.js
 */

import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { join, dirname } from 'path';
import test from 'node:test';
import assert from 'node:assert';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

function run(...args) {
  const r = spawnSync('node', [join(root, 'scripts', 'create_campaign.js'), ...args], {
    cwd: root,
    encoding: 'utf8',
  });
  return { ...r, stdout: r.stdout?.trim?.(), stderr: r.stderr?.trim?.() };
}

function runPayFee(...args) {
  const r = spawnSync('node', [join(root, 'scripts', 'pay_fee.js'), ...args], {
    cwd: root,
    encoding: 'utf8',
    env: { ...process.env, PRIVATE_KEY: '' },
  });
  return { ...r, stdout: r.stdout?.trim?.(), stderr: r.stderr?.trim?.() };
}

function runTopUp(args = [], env = {}) {
  const r = spawnSync('node', [join(root, 'scripts', 'top_up.js'), ...args], {
    cwd: root,
    encoding: 'utf8',
    env: { ...process.env, ...env },
  });
  return { ...r, stdout: r.stdout?.trim?.(), stderr: r.stderr?.trim?.() };
}

const VALID_PAYMENT_HASH = '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef';
const VALID_WALLET = '0x0000000000000000000000000000000000000001';

// ---------------------------------------------------------------------------
// create_campaign — dry-run (no network call)
// ---------------------------------------------------------------------------

test('create_campaign --dry-run: valid args succeeds', () => {
  const { status, stdout } = run(
    '--dry-run',
    '--cast-url', 'https://x.com/user/status/123',
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '10'
  );
  assert.strictEqual(status, 0);
  const out = JSON.parse(stdout);
  assert.strictEqual(out.dryRun, true);
  assert.ok(out.input.castHash.startsWith('0x'));
  assert.strictEqual(out.input.maxBudget, '10');
  assert.strictEqual(out.input.paymentHash, VALID_PAYMENT_HASH);
  assert.strictEqual(out.input.appType, 2, 'Agent-created campaigns use appType 2');
});

test('create_campaign --dry-run: Farcaster URL extracts cast hash from path', () => {
  const castHash = '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890';
  const { status, stdout } = run(
    '--dry-run',
    '--cast-url', `https://warpcast.com/~/casts/${castHash}`,
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '10'
  );
  assert.strictEqual(status, 0);
  const out = JSON.parse(stdout);
  assert.strictEqual(out.input.castHash, castHash);
});

test('create_campaign: missing required args fails', () => {
  const { status, stderr } = run();
  assert.strictEqual(status, 1);
  assert.match(stderr, /Required|GRAPHQL_URL/);
});

test('create_campaign: invalid payment-hash fails', () => {
  const { status, stderr } = run(
    '--dry-run',
    '--cast-url', 'https://x.com/user/1',
    '--payment-hash', '0x1234...cdef',
    '--creator-wallet', VALID_WALLET,
    '--budget', '10'
  );
  assert.strictEqual(status, 1);
  assert.match(stderr, /payment-hash must be a valid tx hash/);
});

test('create_campaign: budget < 5 fails', () => {
  const { status, stderr } = run(
    '--dry-run',
    '--cast-url', 'https://x.com/user/1',
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '1'
  );
  assert.strictEqual(status, 1);
  assert.match(stderr, /Minimum budget is 5 USDC/);
});

// ---------------------------------------------------------------------------
// create_campaign — GRAPHQL_URL security validation (no dry-run, no real call)
// The validator runs before fetch, so these fail fast without touching network.
// ---------------------------------------------------------------------------

test('create_campaign: untrusted GRAPHQL_URL host is rejected', () => {
  const { status, stderr } = run(
    '--cast-url', 'https://x.com/user/1',
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '10',
    '--graphql-url', 'https://evil.com/graphql'
  );
  assert.strictEqual(status, 1);
  assert.match(stderr, /Untrusted GRAPHQL_URL host/);
});

test('create_campaign: http (non-HTTPS) GRAPHQL_URL is rejected', () => {
  const { status, stderr } = run(
    '--cast-url', 'https://x.com/user/1',
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '10',
    '--graphql-url', 'http://boost.inflynce.com/api/graphql'
  );
  assert.strictEqual(status, 1);
  assert.match(stderr, /must use HTTPS/);
});

test('create_campaign: malformed GRAPHQL_URL is rejected', () => {
  const { status, stderr } = run(
    '--cast-url', 'https://x.com/user/1',
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '10',
    '--graphql-url', 'not-a-url'
  );
  assert.strictEqual(status, 1);
  assert.match(stderr, /Invalid GRAPHQL_URL/);
});

test('create_campaign: subdomain of trusted host is rejected', () => {
  const { status, stderr } = run(
    '--cast-url', 'https://x.com/user/1',
    '--payment-hash', VALID_PAYMENT_HASH,
    '--creator-wallet', VALID_WALLET,
    '--budget', '10',
    '--graphql-url', 'https://evil.boost.inflynce.com/api/graphql'
  );
  assert.strictEqual(status, 1);
  assert.match(stderr, /Untrusted GRAPHQL_URL host/);
});

// ---------------------------------------------------------------------------
// pay_fee
// ---------------------------------------------------------------------------

test('pay_fee: missing PRIVATE_KEY fails', () => {
  const { status, stderr } = runPayFee();
  assert.strictEqual(status, 1);
  assert.match(stderr, /Private key required/);
});

// ---------------------------------------------------------------------------
// top_up
// ---------------------------------------------------------------------------

test('top_up: amount < 5 fails', () => {
  const { status, stderr } = runTopUp(['--amount', '2'], { PRIVATE_KEY: '0x' + 'a'.repeat(64) });
  assert.strictEqual(status, 1);
  assert.match(stderr, /Amount must be at least 5 USDC/);
});

test('top_up: missing PRIVATE_KEY fails', () => {
  const { status, stderr } = runTopUp(['--amount', '10'], { PRIVATE_KEY: '' });
  assert.strictEqual(status, 1);
  assert.match(stderr, /Private key required/);
});
