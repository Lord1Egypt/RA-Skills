/**
 * render-long-image.js
 *
 * Renders a full-page PNG screenshot of a completed web page HTML.
 * Usage:
 *   node scripts/render-long-image.js output/lenormand-web-每日運勢-2026-06-22.html
 *
 * Output: same path but with .png extension.
 *
 * Prerequisites: Puppeteer in NODE_PATH workspace.
 *   NODE_PATH=/Users/1mether/.workbuddy/binaries/node/workspace/node_modules \
 *   /Users/1mether/.workbuddy/binaries/node/versions/22.22.2/bin/node \
 *   scripts/render-long-image.js <html-path>
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { chromiumArgs } = require('./chromium-args');

const htmlPath = path.resolve(process.argv[2]);
if (!htmlPath || !fs.existsSync(htmlPath)) {
  console.error('Usage: node render-long-image.js <path-to-web.html>');
  console.error('       The input must be a valid HTML file from Phase 3b.');
  process.exit(1);
}

const ext = path.extname(htmlPath).toLowerCase();
if (ext !== '.html' && ext !== '.htm') {
  console.error('Error: input must be an HTML file (.html / .htm)');
  process.exit(1);
}

const outPath = htmlPath.replace(/\.html?$/i, '.png');
console.log(`Rendering: ${htmlPath}`);
console.log(`Output:    ${outPath}`);

const html = fs.readFileSync(htmlPath, 'utf8');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: chromiumArgs(),
  });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: outPath, fullPage: true });

  const stats = fs.statSync(outPath);
  console.log(`Done: ${(stats.size / 1024).toFixed(1)} KB`);

  await browser.close();
})().catch(err => {
  console.error('Screenshot failed:', err.message);
  process.exit(1);
});
