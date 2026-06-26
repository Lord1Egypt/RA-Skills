#!/usr/bin/env node

/**
 * Pinterest Japan Publisher
 * Uses jp.pinterest.com for Japanese market
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
    'board': { type: 'string', default: 'ホームデコ' },
    'link': { type: 'string', default: '' }
  }
});

async function publishJP() {
  console.log('📌 Pinterest Japan Publisher\n');
  
  if (!values.images || !values.title) {
    console.log('Usage:');
    console.log('node scripts/publish-jp.js --images "./pin.png" --title "タイトル" --description "説明" --board "ボード名"\n');
    process.exit(1);
  }

  const images = values.images.split(',').map(p => p.trim());
  const title = values.title;
  const description = values.description || '';
  const board = values.board;

  console.log(`Title: ${title}`);
  console.log(`Images: ${images.length}`);
  console.log(`Board: ${board}\n`);

  // Load cookies if exist
  const CONFIG_DIR = path.join(process.env.HOME, '.config', 'pinterest');
  const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');
  let cookies = null;
  
  if (fs.existsSync(COOKIES_FILE)) {
    cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));
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

  if (cookies) {
    await context.addCookies(cookies);
  }

  const page = await context.newPage();

  try {
    // Go to Pinterest Japan
    console.log('Opening Pinterest Japan...');
    await page.goto('https://jp.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(5000);

    // Check login status
    const profileBtn = await page.$('a[href="/profile/"], button[aria-label="Profile"], button[data-test-id="profile"]');
    
    if (!profileBtn) {
      console.log('⚠ Not logged in. Opening login page...\n');
      await page.goto('https://jp.pinterest.com/login/', { waitUntil: 'domcontentloaded', timeout: 60000 });
      console.log('👉 Please log in manually in the browser window.\n');
      console.log('   Waiting for login (max 3 minutes)...\n');
      
      // Wait for login
      const maxWait = 3 * 60 * 1000;
      const startTime = Date.now();
      let loggedIn = false;
      
      while (!loggedIn && (Date.now() - startTime) < maxWait) {
        await page.waitForTimeout(2000);
        const check = await page.$('a[href="/profile/"]');
        if (check) {
          loggedIn = true;
          console.log('✓ Login detected!\n');
        }
      }
      
      if (!loggedIn) {
        console.log('⚠ Login timeout. Continuing anyway...\n');
      }
      
      // Save cookies
      const newCookies = await context.cookies();
      fs.writeFileSync(COOKIES_FILE, JSON.stringify(newCookies, null, 2));
      console.log('✓ Cookies saved\n');
    } else {
      console.log('✓ Already logged in\n');
    }

    // Navigate to pin creation
    console.log('Navigating to pin creation...');
    await page.goto('https://jp.pinterest.com/pin/create/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(8000);

    // Take screenshot for debugging
    await page.screenshot({ path: '/tmp/pinterest-jp-create.png' });
    console.log('Screenshot: /tmp/pinterest-jp-create.png\n');

    // Upload images
    console.log('Uploading images...');
    const absolutePaths = images.map(img => path.resolve(img));
    
    // Try to find file input
    let fileInput = await page.$('input[type="file"]');
    
    if (!fileInput) {
      // Try clicking upload button
      console.log('Looking for upload button...');
      const uploadBtn = await page.$('button:has-text("アップロード"), button:has-text("Upload"), button:has-text("画像"), [role="button"]:has-text("image")');
      if (uploadBtn) {
        console.log('Clicking upload button...');
        await uploadBtn.click();
        await page.waitForTimeout(3000);
        fileInput = await page.$('input[type="file"]');
      }
    }

    if (fileInput) {
      await fileInput.setInputFiles(absolutePaths);
      await page.waitForTimeout(10000);
      console.log('✓ Images uploaded\n');
    } else {
      console.log('⚠ Could not find upload input.');
      console.log('👉 Please upload images manually.\n');
      await page.waitForTimeout(30000);
    }

    // Enter title
    if (title) {
      console.log('Entering title...');
      const inputs = await page.$$('input:not([type="hidden"]), input[type="text"]');
      for (const input of inputs) {
        const ariaLabel = await input.getAttribute('aria-label');
        const placeholder = await input.getAttribute('placeholder');
        if ((ariaLabel && ariaLabel.toLowerCase().includes('title')) || 
            (placeholder && placeholder.toLowerCase().includes('title')) ||
            (ariaLabel && ariaLabel.includes('タイトル')) ||
            (placeholder && placeholder.includes('タイトル'))) {
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
        const ariaLabel = await textarea.getAttribute('aria-label');
        const placeholder = await textarea.getAttribute('placeholder');
        if ((ariaLabel && ariaLabel.toLowerCase().includes('description')) || 
            (placeholder && placeholder.toLowerCase().includes('description')) ||
            (ariaLabel && ariaLabel.includes('説明')) ||
            (placeholder && placeholder.includes('説明'))) {
          await textarea.click();
          await textarea.fill('');
          await textarea.type(description, { delay: 30 });
          console.log('✓ Description entered\n');
          break;
        }
      }
    }

    // Select board
    if (board) {
      console.log(`Selecting board: ${board}...`);
      const boardBtn = await page.$('button:has-text("ボード"), button:has-text("Choose board"), button:has-text("Select board")');
      if (boardBtn) {
        await boardBtn.click();
        await page.waitForTimeout(2000);
        
        const boardOption = await page.$(`text="${board}"`);
        if (boardOption) {
          await boardOption.click();
          console.log('✓ Board selected\n');
        } else {
          console.log(`⚠ Board "${board}" not found.\n`);
        }
      }
    }

    // Ready to publish
    console.log('✅ Pin is ready to publish!\n');
    console.log('👉 Please review and click "保存" or "Publish" button manually.\n');
    console.log('   Browser will close in 90 seconds...\n');

    await page.waitForTimeout(90000);

  } catch (error) {
    console.log(`\n❌ Error: ${error.message}\n`);
    await page.screenshot({ path: '/Users/dhr/.config/pinterest/error-' + Date.now() + '.png' });
  } finally {
    await browser.close();
    console.log('✓ Done!\n');
  }
}

publishJP().catch(console.error);
