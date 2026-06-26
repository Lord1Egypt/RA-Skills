#!/usr/bin/env node

/**
 * Pinterest Final Publisher
 * Uses saved cookies and clicks the + button to create pins
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { parseArgs } = require('node:util');

const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    'images': { type: 'string', default: '' },
    'title': { type: 'string', default: '' },
    'description': { type: 'string', default: '' },
    'board': { type: 'string', default: '' }
  }
});

async function publishFinal() {
  console.log('📌 Pinterest Final Publisher\n');
  
  if (!values.images || !values.title) {
    console.log('Usage: node scripts/publish-final.js --images "./pin.png" --title "Title"\n');
    process.exit(1);
  }

  const images = values.images.split(',').map(p => p.trim());
  const title = values.title;
  const description = values.description || '';

  console.log(`Title: ${title}`);
  console.log(`Images: ${images.length}\n`);

  const CONFIG_DIR = path.join(process.env.HOME, '.config', 'pinterest');
  const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');
  
  if (!fs.existsSync(COOKIES_FILE)) {
    console.log('❌ No cookies found. Run "node scripts/force-login.js" first.\n');
    process.exit(1);
  }

  const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--window-size=1280,800']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // Go to Pinterest home
    console.log('Opening Pinterest...');
    await page.goto('https://jp.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(5000);

    // Take screenshot
    await page.screenshot({ path: '/tmp/pinterest-home-before.png' });
    console.log('✓ Home page loaded\n');

    // Click the + button in sidebar
    console.log('Clicking + button to create pin...');
    
    // Try multiple selectors for the create button
    const createSelectors = [
      'a[href="/pin/create/"]',
      'a[href="/create/"]',
      '[data-test-id="create-pin"]',
      '.create-pin-button',
      'button[aria-label="作成"]',
      'button:has-text("作成")',
      'nav a:nth-child(3)',  // Usually 3rd item in sidebar
    ];

    let clicked = false;
    for (const selector of createSelectors) {
      const btn = await page.$(selector);
      if (btn) {
        console.log(`  Found with selector: ${selector}`);
        await btn.click();
        await page.waitForTimeout(5000);
        clicked = true;
        break;
      }
    }

    if (!clicked) {
      console.log('⚠ Create button not found automatically.');
      console.log('👉 Please click the + button in the left sidebar manually.\n');
      await page.waitForTimeout(10000);
    }

    // Take screenshot after clicking
    await page.screenshot({ path: '/tmp/pinterest-create-page.png' });
    console.log('Screenshot: /tmp/pinterest-create-page.png\n');

    // Upload images
    console.log('Uploading images...');
    const absolutePaths = images.map(img => path.resolve(img));
    
    let fileInput = await page.$('input[type="file"]');
    
    if (fileInput) {
      await fileInput.setInputFiles(absolutePaths);
      await page.waitForTimeout(10000);
      console.log('✓ Images uploaded\n');
      await page.screenshot({ path: '/tmp/pinterest-after-upload.png' });
    } else {
      console.log('⚠ Upload input not found.');
      console.log('👉 Please upload images manually (drag & drop or click).\n');
      await page.waitForTimeout(60000);
    }

    // Enter title
    if (title) {
      console.log('Entering title...');
      const inputs = await page.$$('input:not([type="hidden"]), input[type="text"]');
      for (const input of inputs) {
        if (!await input.isVisible()) continue;
        
        const ariaLabel = await input.getAttribute('aria-label');
        const placeholder = await input.getAttribute('placeholder');
        
        if ((ariaLabel && (ariaLabel.toLowerCase().includes('title') || ariaLabel.includes('タイトル'))) || 
            (placeholder && (placeholder.toLowerCase().includes('title') || placeholder.includes('タイトル')))) {
          await input.click();
          await input.fill('');
          await input.type(title, { delay: 50 });
          console.log('✓ Title entered\n');
          break;
        }
      }
    }

    // Enter description
    if (description) {
      console.log('Entering description...');
      const textareas = await page.$$('textarea, div[contenteditable="true"]');
      for (const textarea of textareas) {
        if (!await textarea.isVisible()) continue;
        
        const ariaLabel = await textarea.getAttribute('aria-label');
        const placeholder = await textarea.getAttribute('placeholder');
        
        if ((ariaLabel && (ariaLabel.toLowerCase().includes('description') || ariaLabel.includes('説明'))) || 
            (placeholder && (placeholder.toLowerCase().includes('description') || placeholder.includes('説明')))) {
          await textarea.click();
          await textarea.fill('');
          await textarea.type(description, { delay: 30 });
          console.log('✓ Description entered\n');
          break;
        }
      }
    }

    // Ready to publish
    console.log('✅ Pin setup complete!\n');
    console.log(' Next steps:');
    console.log('   1. Review the pin in the browser');
    console.log('   2. Select a board if needed');
    console.log('   3. Click "保存" or "公開" to publish\n');
    console.log('   Browser will close in 120 seconds...\n');

    await page.screenshot({ path: '/tmp/pinterest-ready-to-publish.png' });
    await page.waitForTimeout(120000);

  } catch (error) {
    console.log(`\n❌ Error: ${error.message}\n`);
    await page.screenshot({ path: '/Users/dhr/.config/pinterest/error-' + Date.now() + '.png' });
  } finally {
    await browser.close();
    console.log('✓ Done!\n');
  }
}

publishFinal().catch(console.error);
