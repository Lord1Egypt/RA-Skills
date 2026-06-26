const { chromium } = require('playwright');
const fs = require('fs');

const PLAYWRIGHT_WS = process.env.PLAYWRIGHT_WS || 'ws://localhost:3000';

async function generatePDF(url, outputPath, options = {}) {
  const {
    format = 'A4',
    landscape = false,
    margin = { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
    printBackground = true,
    waitForSelector = null,
    delay = 0
  } = options;

  let browser;
  try {
    // Connect to remote Playwright server via WebSocket
    browser = await chromium.connect(PLAYWRIGHT_WS);
    
    const context = await browser.newContext();
    const page = await context.newPage();
    
    await page.goto(url, { waitUntil: 'networkidle' });
    
    if (waitForSelector) {
      await page.waitForSelector(waitForSelector, { timeout: 10000 });
    }
    
    if (delay > 0) {
      await page.waitForTimeout(delay);
    }
    
    await page.pdf({
      path: outputPath,
      format,
      landscape,
      margin,
      printBackground
    });
    
    console.log(`PDF saved: ${outputPath}`);
  } finally {
    if (browser) await browser.close();
  }
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const url = args[0];
  const outputPath = args[1] || 'output.pdf';
  
  if (!url) {
    console.log('Usage: node pdf-export.js <url> [output-path] [options]');
    console.log('Options: --format=A4|Letter|Legal, --landscape, --wait-for=selector, --delay=ms');
    console.log('');
    console.log('Environment:');
    console.log('  PLAYWRIGHT_WS=ws://your-server:3000  WebSocket URL of Playwright server');
    process.exit(1);
  }
  
  const options = {
    format: args.find(a => a.startsWith('--format='))?.split('=')[1] || 'A4',
    landscape: args.includes('--landscape'),
    waitForSelector: args.find(a => a.startsWith('--wait-for='))?.split('=')[1],
    delay: parseInt(args.find(a => a.startsWith('--delay='))?.split('=')[1] || '0')
  };
  
  generatePDF(url, outputPath, options).catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}

module.exports = { generatePDF };
