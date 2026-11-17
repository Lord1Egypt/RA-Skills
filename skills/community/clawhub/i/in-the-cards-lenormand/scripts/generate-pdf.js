/**
 * In the Cards — HTML to PDF Converter
 *
 * Usage:
 *   node generate-pdf.js <input.html> [output.pdf]
 *
 * If output path is omitted, replaces .html with .pdf.
 *
 * Dependencies: puppeteer (npm install puppeteer)
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { chromiumArgs } = require('./chromium-args');

(async () => {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node generate-pdf.js <input.html> [output.pdf]');
    process.exit(1);
  }

  const htmlPath = path.resolve(args[0]);
  const pdfPath = args[1]
    ? path.resolve(args[1])
    : htmlPath.replace(/\.html?$/i, '.pdf');

  // Verify HTML exists
  if (!fs.existsSync(htmlPath)) {
    console.error(`Error: HTML file not found: ${htmlPath}`);
    process.exit(1);
  }

  console.log(`HTML: ${htmlPath}`);
  console.log(`PDF:  ${pdfPath}`);

  const browser = await puppeteer.launch({
    headless: true,
    args: chromiumArgs(['--disable-dev-shm-usage'])
  });

  try {
    const page = await browser.newPage();

    // Load HTML with network idle to ensure fonts load
    await page.goto('file://' + htmlPath, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // Allow font rendering to settle
    await new Promise(r => setTimeout(r, 1500));

    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '20mm', right: '22mm', bottom: '22mm', left: '22mm' }
    });

    console.log(`✅ PDF generated: ${pdfPath}`);
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
