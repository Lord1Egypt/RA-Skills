const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function arg(name) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
}
function has(name) { return process.argv.includes(name); }
function args(name) {
  const out = [];
  for (let i = 0; i < process.argv.length; i++) if (process.argv[i] === name && process.argv[i + 1]) out.push(process.argv[i + 1]);
  return out;
}
(async () => {
  const url = arg('--url');
  if (!url) throw new Error('Usage: node index.js --url <url> [--screenshot <path>] [--title] [--extract <selector>] [--click <selector>] [--fill <selector=value>] [--save-session <path>] [--load-session <path>]');
  const headless = !has('--headed');
  const browser = await chromium.launch({ headless });
  const contextOpts = {};
  const loadSession = arg('--load-session');
  if (loadSession && fs.existsSync(path.resolve(loadSession))) contextOpts.storageState = path.resolve(loadSession);
  const context = await browser.newContext(contextOpts);
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  const result = { ok: true, url, title: null, extracted: [], screenshot: null, clicked: [], filled: [], sessionSaved: null };
  if (has('--title')) result.title = await page.title();
  for (const selector of args('--click')) {
    await page.locator(selector).first().click();
    result.clicked.push(selector);
  }
  for (const pair of args('--fill')) {
    const idx = pair.indexOf('=');
    if (idx <= 0) continue;
    const selector = pair.slice(0, idx);
    const value = pair.slice(idx + 1);
    await page.locator(selector).first().fill(value);
    result.filled.push({ selector, value });
  }
  for (const selector of args('--extract')) {
    const text = await page.locator(selector).first().textContent();
    result.extracted.push({ selector, text });
  }
  const screenshot = arg('--screenshot');
  if (screenshot) {
    const out = path.resolve(screenshot);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out, fullPage: true });
    result.screenshot = out;
  }
  const saveSession = arg('--save-session');
  if (saveSession) {
    const out = path.resolve(saveSession);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await context.storageState({ path: out });
    result.sessionSaved = out;
  }
  await context.close();
  await browser.close();
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
})().catch(err => {
  process.stderr.write(String(err && err.stack || err) + '\n');
  process.exit(1);
});
