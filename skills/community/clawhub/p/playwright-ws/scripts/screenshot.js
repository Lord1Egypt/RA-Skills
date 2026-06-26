const { chromium } = require('playwright');
const fs = require('fs');

const PLAYWRIGHT_WS = process.env.PLAYWRIGHT_WS || 'ws://localhost:3000';

async function takeScreenshot(url, outputPath, options = {}) {
  const {
    fullPage = false,
    viewport = { width: 1280, height: 720 },
    waitForSelector = null,
    delay = 0,
    type = 'png'
  } = options;

  let browser;
  try {
    // Connect to remote Playwright server via WebSocket
    browser = await chromium.connect(PLAYWRIGHT_WS);
    
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    
    await page.goto(url, { waitUntil: 'networkidle' });
    
    if (waitForSelector) {
      await page.waitForSelector(waitForSelector, { timeout: 10000 });
    }
    
    if (delay > 0) {
      await page.waitForTimeout(delay);
    }
    
    await page.screenshot({ 
      path: outputPath, 
      fullPage,
      type
    });
    
    console.log(`Screenshot saved: ${outputPath}`);
  } finally {
    if (browser) await browser.close();
  }
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const url = args[0];
  const outputPath = args[1] || 'screenshot.png';
  
  if (!url) {
    console.log('Usage: node screenshot.js <url> [output-path] [options]');
    console.log('Options: --full-page, --wait-for=selector, --delay=ms');
    console.log('');
    console.log('Environment:');
    console.log('  PLAYWRIGHT_WS=ws://your-server:3000  WebSocket URL of Playwright server');
    process.exit(1);
  }
  
  const options = {
    fullPage: args.includes('--full-page'),
    waitForSelector: args.find(a => a.startsWith('--wait-for='))?.split('=')[1],
    delay: parseInt(args.find(a => a.startsWith('--delay='))?.split('=')[1] || '0')
  };
  
  takeScreenshot(url, outputPath, options).catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}

module.exports = { takeScreenshot };
