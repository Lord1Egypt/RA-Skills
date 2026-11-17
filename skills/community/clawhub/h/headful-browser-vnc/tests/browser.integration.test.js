'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');
const net = require('node:net');
const { chromium } = require('playwright');
const { main } = require('../tools/playwright_export');

async function freePort() {
  const server = net.createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  await new Promise(resolve => server.close(resolve));
  return port;
}

test('real CDP capture preserves an operator tab, cookies scope, and live browser', { timeout: 60000 }, async t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'headful-real-browser-'));
  let context;
  let visits = 0;
  const server = http.createServer((req, res) => {
    if (req.url === '/favicon.ico') { res.writeHead(204).end(); return; }
    visits++;
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<html><body><h1 id="state">initial</h1><input id="draft"></body></html>');
  });
  t.after(async () => {
    if (context) await context.close();
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(root, { recursive: true, force: true });
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const url = 'http://127.0.0.1:' + server.address().port + '/';
  const port = await freePort();
  const executablePath = process.env.TEST_CHROME_BIN || (process.platform === 'darwin'
    ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : undefined);
  context = await chromium.launchPersistentContext(path.join(root, 'profile'), {
    headless: true, executablePath, chromiumSandbox: true,
    args: ['--remote-debugging-port=' + port, '--remote-debugging-address=127.0.0.1'],
  });
  const page = context.pages()[0];
  await page.goto(url);
  await page.locator('#draft').fill('unsaved operator input');
  await page.evaluate(() => {
    document.querySelector('#state').textContent = 'operator finished MFA';
    sessionStorage.setItem('handoff', 'same-tab-only');
    localStorage.setItem('auth-test', 'local-state');
  });
  await context.addCookies([
    { name: 'local', value: 'test-value', url },
    { name: 'unrelated', value: 'must-not-export', url: 'https://unrelated.example/' },
  ]);
  const cdp = await context.newCDPSession(page);
  const { targetInfo } = await cdp.send('Target.getTargetInfo');
  await cdp.detach();
  const before = context.pages().length;
  const run = async (command, extra = []) => {
    const output = fs.mkdtempSync(path.join(root, 'capture-'));
    const args = [command, '--port', String(port), '--out', output,
      ...(command === 'cookies' ? [] : ['--target', targetInfo.targetId]), ...extra];
    return { ...(await main(args)), output };
  };
  const capture = await run('capture');
  assert.equal(capture.code, 0, JSON.stringify(capture.result));
  assert.match(fs.readFileSync(path.join(capture.output, 'page.html'), 'utf8'), /operator finished MFA/);
  assert.ok(fs.statSync(path.join(capture.output, 'page.png')).size > 100);
  assert.equal(context.pages().length, before);
  assert.equal(visits, 1, 'capture must not reload or open another page');
  assert.equal(await page.locator('#draft').inputValue(), 'unsaved operator input');
  assert.equal(await page.evaluate(() => sessionStorage.getItem('handoff')), 'same-tab-only');
  assert.equal(fs.existsSync(path.join(capture.output, 'cookies.json')), false);

  const cookies = await run('cookies', ['--url', url]);
  assert.equal(cookies.code, 0);
  assert.deepEqual(JSON.parse(fs.readFileSync(path.join(cookies.output, 'cookies.json'))).map(c => c.name), ['local']);

  const storage = await run('storage-state');
  assert.equal(storage.code, 0, JSON.stringify(storage.result));
  const state = JSON.parse(fs.readFileSync(path.join(storage.output, 'storage-state.json')));
  assert.ok(state.origins.some(o => o.localStorage.some(v => v.name === 'auth-test')));

  const missing = fs.mkdtempSync(path.join(root, 'missing-'));
  const stale = await main(['capture', '--port', String(port), '--out', missing, '--target', 'nonexistent']);
  assert.equal(stale.code, 1);
  assert.match(stale.result.error, /does not exist/);
  assert.equal(context.pages().length, before);
  assert.equal(page.isClosed(), false, 'export must disconnect without closing operator page');
});
