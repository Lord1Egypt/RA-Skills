import { test } from 'node:test';
import assert from 'node:assert/strict';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const scriptPath = resolve(__dirname, '../scripts/kalshi-trades.mjs');

function runCli(args) {
  const res = spawnSync(process.execPath, [scriptPath, ...args], {
    encoding: 'utf8',
  });
  return {
    code: res.status ?? 1,
    stdout: res.stdout ?? '',
    stderr: res.stderr ?? '',
  };
}

test('help prints usage and exits 0', () => {
  const out = runCli(['help']);
  assert.equal(out.code, 0, `Expected success. stderr:\n${out.stderr}`);
  assert.match(out.stdout, /Usage:/);
  assert.match(out.stdout, /kalshi-trades\.mjs/);
});

test('status returns JSON with exchange fields', () => {
  const out = runCli(['status']);
  assert.equal(out.code, 0, `Expected success. stderr:\n${out.stderr}\nstdout:\n${out.stdout}`);

  const payload = JSON.parse(out.stdout.trim());
  assert.equal(typeof payload.endpoint, 'string');
  assert.equal(typeof payload.data, 'object');
  assert.equal(typeof payload.data.exchange_active, 'boolean');
  assert.equal(typeof payload.data.trading_active, 'boolean');
});

test('unknown command exits non-zero with JSON error payload', () => {
  const out = runCli(['definitely-not-a-command']);
  assert.notEqual(out.code, 0, `Expected failure. stdout:\n${out.stdout}`);

  const payload = JSON.parse(out.stdout.trim());
  assert.equal(typeof payload.error, 'string');
  assert.match(payload.error, /unknown command/i);
});
