#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let chromium;
try { chromium = require('playwright').chromium; }
catch (_) {
  try { chromium = require('playwright-chromium').chromium; }
  catch (err) {
    console.error('Missing renderer dependency. Install one of: npm install playwright OR npm install playwright-chromium');
    process.exit(2);
  }
}

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('usage: render_issue.mjs <issue.html> <out-dir> [basename]');
  process.exit(2);
}

const input = path.resolve(args[0]);
const outDir = path.resolve(args[1]);
const base = args[2] || path.basename(input, path.extname(input));
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
await page.goto('file://' + input, { waitUntil: 'networkidle' });

const pdfPath = path.join(outDir, `${base}.pdf`);
await page.pdf({ path: pdfPath, width: '794px', height: '1123px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });

const pages = await page.locator('.page').count();
for (let i = 0; i < pages; i++) {
  await page.locator('.page').nth(i).screenshot({ path: path.join(outDir, `${base}-page-${i + 1}.png`) });
}

await browser.close();
console.log(JSON.stringify({ pdf: pdfPath, previews: pages }, null, 2));
