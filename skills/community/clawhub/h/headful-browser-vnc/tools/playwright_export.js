#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

function options(argv) {
  const [command, ...rest] = argv;
  if (!['capture', 'navigate-and-capture', 'cookies', 'storage-state'].includes(command)) {
    throw new Error('Expected capture, navigate-and-capture, cookies, or storage-state');
  }
  const opts = { command };
  const allowed = new Set(['--port', '--out', '--session', '--target', '--url']);
  for (let i = 0; i < rest.length; i++) {
    const key = rest[i];
    if (allowed.has(key) && rest[i + 1] && !rest[i + 1].startsWith('--')) {
      if (Object.hasOwn(opts, key.slice(2))) throw new Error('Duplicate option: ' + key);
      opts[key.slice(2)] = rest[++i];
    } else {
      throw new Error('Unknown option or missing value: ' + key);
    }
  }
  if (!/^\d+$/.test(opts.port || '') || Number(opts.port) < 1024 || Number(opts.port) > 65535) {
    throw new Error('A local --port between 1024 and 65535 is required');
  }
  if (!opts.out) throw new Error('--out is required');
  if (command !== 'cookies' && !opts.target) throw new Error('--target is required; select a targetId from pages');
  if (command === 'navigate-and-capture' || command === 'cookies') {
    const url = new URL(opts.url);
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) {
      throw new Error('--url must be an http(s) URL without embedded credentials');
    }
  }
  return opts;
}

function prepareDirectory(directory) {
  const info = fs.lstatSync(directory);
  if (!info.isDirectory() || (process.getuid && info.uid !== process.getuid())) {
    throw new Error('Output must be an owned directory, not a symlink');
  }
  fs.chmodSync(directory, 0o700);
}

function writePrivate(directory, name, content) {
  fs.writeFileSync(path.join(directory, name), content, { flag: 'wx', mode: 0o600 });
}

async function selectPage(browser, targetId) {
  for (const context of browser.contexts()) {
    for (const page of context.pages()) {
      const session = await context.newCDPSession(page);
      try {
        const { targetInfo } = await session.send('Target.getTargetInfo');
        if (targetInfo.targetId === targetId) return page;
      } finally {
        await session.detach();
      }
    }
  }
  throw new Error('Target ' + targetId + ' does not exist; refresh pages and select again');
}

async function performExport(opts, browser) {
  const result = {
    success: false, command: opts.command, sessionId: opts.session || null,
    targetId: opts.target || null, capturedAt: new Date().toISOString(),
    outputDir: path.resolve(opts.out), artifacts: {},
  };
  const artifact = async (name, filename, produce) => {
    try {
      const value = await produce();
      writePrivate(opts.out, filename, value);
      result.artifacts[name] = { success: true, path: path.join(result.outputDir, filename) };
    } catch (error) {
      result.artifacts[name] = { success: false, error: error.message };
    }
  };
  try {
    if (opts.command === 'cookies') {
      const context = browser.contexts()[0];
      if (!context) throw new Error('Existing browser context not found');
      result.url = opts.url;
      await artifact('cookies', 'cookies.json', async () => JSON.stringify(await context.cookies([opts.url]), null, 2));
    } else {
      const page = await selectPage(browser, opts.target);
      page.setDefaultTimeout(15000);
      if (opts.command === 'navigate-and-capture') {
        const response = await page.goto(opts.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        if (response && response.status() >= 400) throw new Error('Navigation returned HTTP ' + response.status());
      }
      result.url = page.url();
      if (opts.command === 'storage-state') {
        result.scope = 'Selected page origin; cookies scoped to its URL';
        result.omitted = ['IndexedDB', 'sessionStorage', 'service workers', 'device-bound credentials'];
        await artifact('storageState', 'storage-state.json', async () => {
          // Existing CDP contexts may not track origins visited before attachment.
          // Read the selected page directly; never navigate a helper tab.
          const url = new URL(page.url());
          if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Storage export requires an http(s) page');
          const storage = await page.evaluate(() => ({
            origin: location.origin,
            localStorage: Object.keys(localStorage).map(name => ({ name, value: localStorage.getItem(name) })),
          }));
          if (storage.origin !== url.origin) throw new Error('Page navigated during storage export');
          return JSON.stringify({ cookies: await page.context().cookies([url.href]), origins: [storage] }, null, 2);
        });
      } else {
        await artifact('html', 'page.html', () => page.content());
        await artifact('screenshot', 'page.png', () => page.screenshot({ fullPage: true, timeout: 15000 }));
      }
      if (page.url() !== result.url) throw new Error('Page navigated during capture; artifacts may reflect different states');
    }
    result.success = Object.keys(result.artifacts).length > 0 && Object.values(result.artifacts).every(a => a.success);
  } catch (error) {
    result.error = error.message;
  }
  writePrivate(opts.out, 'manifest.json', JSON.stringify(result, null, 2));
  return result;
}

async function main(argv = process.argv.slice(2), dependencies = {}) {
  process.umask(0o077);
  let browser;
  try {
    const opts = options(argv);
    prepareDirectory(opts.out);
    const chromium = dependencies.chromium || require('playwright').chromium;
    browser = await chromium.connectOverCDP('http://127.0.0.1:' + opts.port, { timeout: 15000, noDefaults: true });
    const result = await performExport(opts, browser);
    return { result, code: result.success ? 0 : 1 };
  } catch (error) {
    return { result: { success: false, error: error.message }, code: 1 };
  } finally {
    // Disconnect attached client. Never create/close operator pages or contexts.
    if (browser) await browser.close();
  }
}

module.exports = { options, selectPage, performExport, main };
if (require.main === module) {
  main().then(({ result, code }) => {
    console.log(JSON.stringify(result));
    process.exitCode = code;
  }).catch(error => {
    console.log(JSON.stringify({ success: false, error: error.message }));
    process.exitCode = 1;
  });
}
