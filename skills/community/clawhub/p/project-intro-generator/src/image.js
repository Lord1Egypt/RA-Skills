const path = require('path');

async function exportLongImage(htmlPath, imagePath, options = {}) {
  let playwright;
  try {
    playwright = require('playwright');
  } catch (err) {
    throw new Error('未安装 playwright，请运行 npm install playwright 后再试。');
  }

  const browser = await playwright.chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: options.width || 700, height: options.height || 1200 },
    deviceScaleFactor: options.deviceScaleFactor || 2
  });
  const url = htmlPath.startsWith('http') ? htmlPath : `file://${path.resolve(htmlPath)}`;
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => {
    document.body.classList.add('export-mode');
  });
  await page.waitForTimeout(options.waitFor || 300);
  await page.screenshot({ path: imagePath, fullPage: true });
  await browser.close();
}

module.exports = {
  exportLongImage
};
