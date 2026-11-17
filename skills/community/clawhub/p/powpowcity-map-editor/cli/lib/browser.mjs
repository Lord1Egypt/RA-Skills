// IsoCity CLI - Playwright automation against the running game (local dev or deployed).
// Uses the #s= share-hash to load state and the window.__isocity bridge for control.
import { createShareUrl } from './share.mjs';

async function loadChromium() {
  try {
    const pw = await import('playwright');
    return pw.chromium;
  } catch {
    throw new Error(
      'playwright is not installed. Run:\n' +
      '  npm install\n' +
      '  npx playwright install chromium'
    );
  }
}

async function launchBrowser(chromium) {
  try {
    return await chromium.launch();
  } catch {
    // Headless shell may be missing - fall back to the full chromium build
    return await chromium.launch({ channel: 'chromium' });
  }
}

function cleanBase(url) {
  return url.split('#')[0].replace(/\/+$/, '');
}

async function openGamePage({ state, url, width = 1600, height = 900 }) {
  const chromium = await loadChromium();
  const browser = await launchBrowser(chromium);
  const context = await browser.newContext({ viewport: { width, height } });
  // Disable tutorial tip toasts before any page script runs (locale-independent)
  await context.addInitScript(() => {
    try { localStorage.setItem('isocity-tips-disabled', 'true'); } catch { /* ignore */ }
  });
  const page = await context.newPage();
  const target = createShareUrl(state, `${cleanBase(url)}/`);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await page.waitForFunction(() => typeof window.__isocity !== 'undefined', null, { timeout: 60000 });
  const stateJson = JSON.stringify(state);
  const ok = await page.evaluate((json) => window.__isocity.loadState(json), stateJson);
  if (!ok) {
    await browser.close();
    throw new Error('The game rejected the state file (loadState returned false)');
  }
  return { browser, page };
}

function largestCanvasIndex(page) {
  return page.locator('canvas').evaluateAll((canvases) => {
    let bestIndex = 0;
    let bestArea = -1;
    canvases.forEach((c, i) => {
      const area = c.width * c.height;
      if (area > bestArea) { bestArea = area; bestIndex = i; }
    });
    return bestIndex;
  });
}

export async function screenshotState({ state, url, out, width, height, waitMs = 5000, zoomOut = 0 }) {
  const { browser, page } = await openGamePage({ state, url, width, height });
  try {
    const canvasCount = await page.locator('canvas').count();
    if (canvasCount === 0) throw new Error('No canvas element found on the game page');
    const bestIndex = await largestCanvasIndex(page);
    const canvas = page.locator('canvas').nth(bestIndex);
    if (zoomOut > 0) {
      const box = await canvas.boundingBox();
      if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        for (let i = 0; i < zoomOut; i++) await page.mouse.wheel(0, 240);
      }
    }
    if (waitMs > 0) await page.waitForTimeout(waitMs);
    await canvas.screenshot({ path: out });
    return { out };
  } finally {
    await browser.close();
  }
}

export async function simulateTicks({ state, url, ticks, width, height }) {
  const { browser, page } = await openGamePage({ state, url, width, height });
  try {
    await page.evaluate(() => window.__isocity.setSpeed(0));
    const resultJson = await page.evaluate((n) => window.__isocity.runTicks(n), ticks);
    const result = JSON.parse(resultJson);
    return result;
  } finally {
    await browser.close();
  }
}
