import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: false }); // visible so we can see what's blocking
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  viewport: { width: 1280, height: 900 },
});
const page = await context.newPage();

console.log('Loading SoFIFA...');
try {
  await page.goto('https://sofifa.com/teams?type=international&col=oa&sort=desc', {
    waitUntil: 'commit',
    timeout: 30000,
  });
} catch(e) {
  console.log('goto error:', e.message);
}

// Wait a bit for JS to run
await page.waitForTimeout(8000);

const title = await page.title().catch(() => '?');
console.log('Title:', title);

await page.screenshot({ path: '/tmp/sofifa_debug.png', fullPage: false });
console.log('Screenshot at /tmp/sofifa_debug.png');

const bodyText = await page.evaluate(() => document.body?.innerText?.slice(0, 2000) || 'no body').catch(() => 'error');
console.log('Body sample:\n', bodyText);

const selectors = await page.evaluate(() => {
  const tags = ['table', 'tbody', '.bp3-html-table', '.table', 'article', '.team-row', '.col-name'];
  return tags.map(s => `${s}: ${document.querySelectorAll(s).length}`);
}).catch(() => ['eval error']);
console.log('Selectors:', selectors);

await browser.close();
