const puppeteer = require('puppeteer');
const fs = require('fs');

const tasks = [
  // 训练集 T2-T15
  ['T2', 'test-data/training/T2-images.html'],
  ['T3', 'test-data/training/T3-longpage.html'],
  ['T4', 'test-data/training/T4-tables.html'],
  ['T5', 'test-data/training/T5-multicolumn.html'],
  ['T6', 'test-data/training/T6-backdrop-filter.html'],
  ['T7', 'test-data/training/T7-fixed.html'],
  ['T8', 'test-data/training/T8-transform.html'],
  ['T9', 'test-data/training/T9-opacity.html'],
  ['T10', 'test-data/training/T10-mixed-css.html'],
  ['T11', 'test-data/training/T11-js-dynamic.html'],
  ['T12', 'test-data/training/T12-lazy-load.html'],
  ['T13', 'test-data/training/T13-external-url.html'],
  ['T14', 'test-data/training/T14-mobile.html'],
  ['T15', 'test-data/training/T15-full-report.html'],
  // 验证集 V1-V10
  ['V1', 'test-data/validation/V1-simple.html'],
  ['V2', 'test-data/validation/V2-longpage.html'],
  ['V3', 'test-data/validation/V3-complex-table.html'],
  ['V4', 'test-data/validation/V4-nested-position.html'],
  ['V5', 'test-data/validation/V5-gradient-shadow.html'],
  ['V6', 'test-data/validation/V6-external-font.html'],
  ['V7', 'test-data/validation/V7-media-embed.html'],
  ['V8', 'test-data/validation/V8-dark-theme.html'],
  ['V9', 'test-data/validation/V9-responsive.html'],
  ['V10', 'test-data/validation/V10-zhihu-style.html'],
];

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    channel: 'chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });

  for (const [task, htmlFile] of tasks) {
    process.stdout.write(`  ⏳ ${task} ... `);
    try {
      const html = fs.readFileSync(htmlFile, 'utf8');
      const page = await browser.newPage();
      await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 2 });
      await page.setContent(html, { waitUntil: 'load', timeout: 30000 });

      const dims = await page.evaluate(() => ({
        width: Math.ceil(document.body.scrollWidth),
        height: Math.ceil(document.body.scrollHeight),
      }));

      await page.setViewport({ width: dims.width, height: dims.height, deviceScaleFactor: 2 });
      await page.evaluate(() => window.stop());

      const screenshot = await page.screenshot({ type: 'png', fullPage: true });
      const outputPath = `test-data/output/${task}.png`;
      fs.writeFileSync(outputPath, screenshot);

      const kb = Math.round(screenshot.length / 1024);
      console.log(`✅ ${dims.width}x${dims.height} (${kb}KB)`);

      await page.close();
    } catch (e) {
      console.log(`❌ ${e.message}`);
    }
  }

  await browser.close();
  console.log('\n✅ Baseline 完成');
})();