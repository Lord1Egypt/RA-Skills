/**
 * human-type browser player v2
 * Handles all event types: type, delete, pause, arrow, select-back, select-replace.
 */

const DEFAULT_CDP_URL = 'http://127.0.0.1:18800';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function hasPlaywright() {
  try {
    require.resolve('playwright-core');
    return true;
  } catch (_) {}
  return false;
}

function getFirstPage(browser) {
  for (const context of browser.contexts()) {
    const page = context.pages()[0];
    if (page) return page;
  }
  return null;
}

// ─── Playwright player ────────────────────────────────────────────────────────

async function playWithPlaywright(events, opts = {}) {
  const { chromium } = require('playwright-core');
  const { cdpUrl = DEFAULT_CDP_URL, selector, delayStart = 500 } = opts;

  let browser, page;

  try {
    browser = await chromium.connectOverCDP(cdpUrl);
  } catch (_) {
    throw new Error(
      `Could not connect to a Chromium browser at ${cdpUrl}.\n` +
      'Start the OpenClaw browser first with: openclaw browser start\n' +
      'Then open a page with: openclaw browser open <url>\n' +
      'Or pass --cdp-url to point at a different browser.'
    );
  }

  page = getFirstPage(browser);
  if (!page) throw new Error('Could not get a page handle from the browser.');

  if (selector) {
    await page.click(selector);
    await sleep(150);
  }

  await page.bringToFront();

  if (delayStart > 0) await sleep(delayStart);

  const startTime = Date.now();

  for (const ev of events) {
    const elapsed = Date.now() - startTime;
    const waitFor = ev.time - elapsed;
    if (waitFor > 0) await sleep(waitFor);

    switch (ev.type) {
      case 'type':
        await page.keyboard.type(ev.ch, { delay: 0 });
        break;

      case 'delete':
        await page.keyboard.press('Backspace');
        break;

      case 'pause':
        // Timing gap already handled above — no key action
        break;

      case 'arrow':
        // Press arrow key ev.n times
        for (let i = 0; i < ev.n; i++) {
          await page.keyboard.press(`Arrow${ev.dir}`);
        }
        break;

      case 'select-back':
        // Shift+Left × n  (selects n chars behind cursor)
        for (let i = 0; i < ev.n; i++) {
          await page.keyboard.press('Shift+ArrowLeft');
        }
        break;

      case 'select-replace':
        // Type the correct char — replaces the selection
        await page.keyboard.type(ev.ch, { delay: 0 });
        break;
    }
  }
}

// ─── Public ───────────────────────────────────────────────────────────────────

async function playScript(events, opts = {}) {
  if (!hasPlaywright()) {
    throw new Error(
      'Missing dependency: playwright-core. Reinstall the package or run `npm install`.'
    );
  }
  await playWithPlaywright(events, opts);
}

module.exports = { playScript, hasPlaywright, DEFAULT_CDP_URL };
