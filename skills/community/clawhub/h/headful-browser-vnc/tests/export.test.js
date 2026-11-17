'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { main, options } = require('../tools/playwright_export');

function fixture(t, overrides = {}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'headful-export-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const calls = { goto: 0, disconnect: 0, detached: 0 };
  const context = {
    pages: () => [page],
    newCDPSession: async () => ({
      send: async () => ({ targetInfo: { targetId: 'operator-tab' } }),
      detach: async () => { calls.detached++; },
    }),
    cookies: async urls => { calls.cookieURLs = urls; return [{ name: 'auth', value: 'secret' }]; },
    storageState: async opts => { calls.storageOptions = opts; return { cookies: [], origins: [] }; },
  };
  const page = {
    setDefaultTimeout() {},
    goto: async () => { calls.goto++; return { status: () => 200 }; },
    content: async () => '<div>operator edited state</div>',
    screenshot: async () => Buffer.from('png'),
    url: () => 'https://example.test/in-progress',
    context: () => context,
    evaluate: async () => ({ origin: 'https://example.test', localStorage: [{ name: 'auth-test', value: 'state' }] }),
    ...overrides,
  };
  const browser = { contexts: () => [context], close: async () => { calls.disconnect++; } };
  const dependencies = { chromium: { connectOverCDP: async endpoint => {
    assert.equal(endpoint, 'http://127.0.0.1:9222');
    return browser;
  } } };
  const run = (command, extra = []) => main([command, '--port', '9222', '--out', directory,
    ...(command === 'cookies' ? [] : ['--target', 'operator-tab']), ...extra], dependencies);
  return { directory, calls, run };
}

test('capture preserves existing operator tab and emits private artifacts without cookies', async t => {
  const { directory, calls, run } = fixture(t);
  const { result, code } = await run('capture');
  assert.equal(code, 0);
  assert.equal(result.success, true);
  assert.equal(calls.goto, 0);
  assert.equal(calls.disconnect, 1);
  assert.equal(calls.detached, 1);
  assert.equal(fs.readFileSync(path.join(directory, 'page.html'), 'utf8'), '<div>operator edited state</div>');
  assert.deepEqual(fs.readdirSync(directory).sort(), ['manifest.json', 'page.html', 'page.png']);
  assert.equal(fs.statSync(directory).mode & 0o777, 0o700);
  for (const file of fs.readdirSync(directory)) assert.equal(fs.statSync(path.join(directory, file)).mode & 0o777, 0o600);
});

test('partial screenshot failure propagates and retains successful HTML plus manifest', async t => {
  const { directory, run } = fixture(t, { screenshot: async () => { throw new Error('Page closed'); } });
  const { result, code } = await run('capture');
  assert.equal(code, 1);
  assert.equal(result.artifacts.html.success, true);
  assert.equal(result.artifacts.screenshot.success, false);
  assert.equal(JSON.parse(fs.readFileSync(path.join(directory, 'manifest.json'))).success, false);
});

test('duplicate targets are rejected before connecting', async t => {
  const { run, calls } = fixture(t);
  const { code, result } = await run('capture', ['--target', 'missing']);
  // Duplicate targets are rejected before connecting.
  assert.equal(code, 1);
  assert.match(result.error, /Duplicate/);
  assert.equal(calls.goto, 0);
});

test('cookies require URL scope and are explicit', async t => {
  const { run, calls } = fixture(t);
  const { result, code } = await run('cookies', ['--url', 'https://example.test/account']);
  assert.equal(code, 0);
  assert.deepEqual(calls.cookieURLs, ['https://example.test/account']);
  assert.deepEqual(Object.keys(result.artifacts), ['cookies']);
});

test('navigation is an explicit separate operation', async t => {
  const { run, calls } = fixture(t);
  assert.equal((await run('navigate-and-capture', ['--url', 'https://example.test/next'])).code, 0);
  assert.equal(calls.goto, 1);
});

test('HTTP error cannot be reported as a successful navigation capture', async t => {
  const { run } = fixture(t, { goto: async () => ({ status: () => 503 }) });
  const { result, code } = await run('navigate-and-capture', ['--url', 'https://example.test/next']);
  assert.equal(code, 1);
  assert.match(result.error, /503/);
});

test('storage export reads current origin and declares omissions without navigating', async t => {
  const { run, calls } = fixture(t);
  const { code, result } = await run('storage-state');
  assert.equal(code, 0);
  assert.equal(calls.storageOptions, undefined);
  assert.ok(result.omitted.includes('IndexedDB'));
  assert.deepEqual(calls.cookieURLs, ['https://example.test/in-progress']);
  assert.equal(calls.goto, 0);
});

test('unsafe URL, invalid port, unknown flags and missing target fail validation', () => {
  const base = ['--out', '/tmp/artifacts', '--port', '9222'];
  assert.throws(() => options(['capture', ...base]), /target/);
  assert.throws(() => options(['cookies', ...base, '--url', 'file:///etc/passwd']), /http/);
  assert.throws(() => options(['cookies', ...base, '--url', 'https://user:secret@example.test']), /credentials/);
  assert.throws(() => options(['capture', '--port', '80']), /port/);
  assert.throws(() => options(['capture', ...base, '--wat']), /Unknown/);
});

test('pre-existing output symlink is never overwritten', async t => {
  const { directory, run } = fixture(t);
  const victim = path.join(directory, 'victim');
  fs.writeFileSync(victim, 'keep');
  fs.symlinkSync(victim, path.join(directory, 'page.html'));
  assert.equal((await run('capture')).code, 1);
  assert.equal(fs.readFileSync(victim, 'utf8'), 'keep');
});
