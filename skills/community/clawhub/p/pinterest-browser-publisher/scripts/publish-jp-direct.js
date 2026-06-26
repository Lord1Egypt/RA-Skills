#!/usr/bin/env node

/**
 * Pinterest Japan Direct Publisher
 * Uses https://jp.pinterest.com/pin-creation-tool/
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

async function publishDirect() {
  console.log('📌 Pinterest Japan Direct Publisher\n');
  
  if (!values.images || !values.title) {
    console.log('Usage: node scripts/publish-jp-direct.js --images "./pin.png" --title "Title"\n');
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
    console.log('⚠ No cookies found. Will wait for manual login.\n');
  }

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--window-size=1280,800']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });

  // Load cookies if exist
  if (fs.existsSync(COOKIES_FILE)) {
    const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));
    await context.addCookies(cookies);
    console.log('✓ Cookies loaded\n');
  }

  const page = await context.newPage();

  try {
    // Go directly to pin creation tool
    console.log('Opening pin creation tool...');
    await page.goto('https://jp.pinterest.com/pin-creation-tool/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(8000);

    // Take screenshot
    await page.screenshot({ path: '/tmp/pinterest-creation-tool.png' });
    console.log('Screenshot: /tmp/pinterest-creation-tool.png\n');

    // Check if logged in
    const profileBtn = await page.$('a[href="/profile/"], button[aria-label="Profile"]');
    if (!profileBtn) {
      console.log('⚠ Not logged in. Please log in manually in the browser.\n');
      console.log('Waiting 2 minutes for login...\n');
      await page.waitForTimeout(120000);
      
      // Save new cookies
      const newCookies = await context.cookies();
      fs.writeFileSync(COOKIES_FILE, JSON.stringify(newCookies, null, 2));
      console.log('✓ Cookies saved\n');
    }

    // Upload images
    console.log('Uploading images...');
    const absolutePaths = images.map(img => path.resolve(img));
    
    let fileInput = await page.$('input[type="file"]');
    
    if (fileInput) {
      await fileInput.setInputFiles(absolutePaths);
      await page.waitForTimeout(10000);
      console.log('✓ Images uploaded\n');
    } else {
      console.log('⚠ Upload input not found.');
      console.log('👉 Please upload images manually.\n');
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
    console.log('👉 Please click "保存" to publish.\n');
    console.log('   Browser will close in 120 seconds...\n');

    await page.screenshot({ path: '/tmp/pinterest-ready.png' });
    await page.waitForTimeout(120000);

  } catch (error) {
    console.log(`\n❌ Error: ${error.message}\n`);
    await page.screenshot({ path: '/Users/dhr/.config/pinterest/error-' + Date.now() + '.png' });
  } finally {
    await browser.close();
    console.log('✓ Done!\n');
  }
}

publishDirect().catch(console.error);
