/**
 * In the Cards — Social Card Renderer
 * Renders 1080×1440 social card HTML to individual PNGs using Puppeteer.
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { chromiumArgs } = require('./chromium-args');

(async () => {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node render-social-cards.js <html-file> [output-prefix]');
    process.exit(1);
  }

  const htmlPath = path.resolve(args[0]);
  if (!fs.existsSync(htmlPath)) {
    console.error(`HTML not found: ${htmlPath}`);
    process.exit(1);
  }

  const outputPrefix = args[1] || htmlPath.replace(/\.html?$/i, '');

  const browser = await puppeteer.launch({
    headless: true,
    args: chromiumArgs(['--disable-dev-shm-usage'])
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1080, height: 1440, deviceScaleFactor: 2 });

    await page.goto('file://' + htmlPath, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // Wait for web fonts to fully load (Chiron Sung HK from CDN)
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 2000));

    const posters = await page.$$('.poster.xhs');
    console.log(`Found ${posters.length} poster(s)`);

    for (let i = 0; i < posters.length; i++) {
      const filePath = `${outputPrefix}-${String(i + 1).padStart(2, '0')}.png`;
      await posters[i].screenshot({ path: filePath });
      console.log(`  [${i + 1}/${posters.length}] ${path.basename(filePath)}`);
    }

    console.log(`\nDone. ${posters.length} PNG(s) generated.`);
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
