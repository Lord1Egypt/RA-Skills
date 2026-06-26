#!/usr/bin/env node

/**
 * Pinterest Login & Publish in one session
 * User logs in, then immediately publishes without relying on saved cookies.
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
    'board': { type: 'string', default: 'Home Decor' },
    'link': { type: 'string', default: '' }
  }
});

async function loginAndPublish() {
  console.log('📌 Pinterest Login & Publisher\n');
  
  if (!values.images || !values.title) {
    console.log('Usage:');
    console.log('node scripts/login-and-publish.js --images "./pin.png" --title "My Pin" --description "Desc" --board "My Board"\n');
    process.exit(1);
  }

  const images = values.images.split(',').map(p => p.trim());
  const title = values.title;
  const description = values.description || '';
  const board = values.board;
  const link = values.link;

  console.log(`Title: ${title}`);
  console.log(`Images: ${images.length}`);
  console.log(`Board: ${board}\n`);

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--window-size=1280,800']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();

  try {
    // Step 1: Go to Pinterest and let user log in
    console.log('Opening Pinterest...');
    await page.goto('https://www.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);

    console.log('\n👉 Please log in to Pinterest in the browser window.');
    console.log('   Waiting for you to log in (max 5 minutes)...\n');

    // Wait for user to log in - check for profile button
    let isLoggedIn = false;
    const maxWait = 5 * 60 * 1000; // 5 minutes
    const startTime = Date.now();

    while (!isLoggedIn && (Date.now() - startTime) < maxWait) {
      await page.waitForTimeout(2000);
      const profileBtn = await page.$('a[href="/profile/"], button[aria-label="Profile"], button[data-test-id="profile"]');
      if (profileBtn) {
        isLoggedIn = true;
        console.log('✓ Login detected!\n');
      }
    }

    if (!isLoggedIn) {
      throw new Error('Login timeout. Please try again.');
    }

    // Save cookies for future use
    const CONFIG_DIR = path.join(process.env.HOME, '.config', 'pinterest');
    const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');
    if (!fs.existsSync(CONFIG_DIR)) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true });
    }
    const cookies = await context.cookies();
    fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2));
    console.log('✓ Cookies saved\n');

    // Step 2: Navigate to create pin
    console.log('Navigating to create pin page...');
    await page.goto('https://www.pinterest.com/pin/create/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(5000);

    // Step 3: Upload images
    console.log('Uploading images...');
    const absolutePaths = images.map(img => path.resolve(img));
    
    // Try multiple selectors for file input
    let fileInput = await page.$('input[type="file"]');
    
    if (!fileInput) {
      // Try clicking the upload area first
      const uploadBtn = await page.$('button:has-text("Upload"), button:has-text("upload"), [role="button"]:has-text("image")');
      if (uploadBtn) {
        await uploadBtn.click();
        await page.waitForTimeout(2000);
        fileInput = await page.$('input[type="file"]');
      }
    }

    if (fileInput) {
      await fileInput.setInputFiles(absolutePaths);
      await page.waitForTimeout(8000);
      console.log('✓ Images uploaded\n');
    } else {
      console.log('⚠ Could not find upload input automatically.');
      console.log('👉 Please click the upload button and select images manually.\n');
      await page.waitForTimeout(30000); // Give user time to upload manually
    }

    // Step 4: Enter title
    if (title) {
      console.log('Entering title...');
      const titleInputs = await page.$$('input:not([type="hidden"]), input[type="text"]');
      for (const input of titleInputs) {
        const ariaLabel = await input.getAttribute('aria-label');
        const placeholder = await input.getAttribute('placeholder');
        if ((ariaLabel && ariaLabel.toLowerCase().includes('title')) || 
            (placeholder && placeholder.toLowerCase().includes('title'))) {
          await input.click();
          await input.fill('');
          await input.type(title, { delay: 50 });
          console.log('✓ Title entered\n');
          break;
        }
      }
    }

    // Step 5: Enter description
    if (description) {
      console.log('Entering description...');
      const descInputs = await page.$$('textarea, div[contenteditable="true"]');
      for (const input of descInputs) {
        const ariaLabel = await input.getAttribute('aria-label');
        const placeholder = await input.getAttribute('placeholder');
        if ((ariaLabel && ariaLabel.toLowerCase().includes('description')) || 
            (placeholder && placeholder.toLowerCase().includes('description'))) {
          await input.click();
          await input.fill('');
          await input.type(description, { delay: 30 });
          console.log('✓ Description entered\n');
          break;
        }
      }
    }

    // Step 6: Select board
    if (board) {
      console.log(`Selecting board: ${board}...`);
      const boardBtn = await page.$('button:has-text("Choose board"), button:has-text("Select board"), button:has-text("Board")');
      if (boardBtn) {
        await boardBtn.click();
        await page.waitForTimeout(2000);
        
        const boardOption = await page.$(`text="${board}"`);
        if (boardOption) {
          await boardOption.click();
          console.log('✓ Board selected\n');
        } else {
          console.log(`⚠ Board "${board}" not found. Will use default.\n`);
        }
      }
    }

    // Step 7: Ready to publish
    console.log('✅ Pin is ready to publish!\n');
    console.log('👉 Please review and click "Publish" manually in the browser.\n');
    console.log('   Browser will close in 90 seconds...\n');

    await page.waitForTimeout(90000);

  } catch (error) {
    console.log(`\n❌ Error: ${error.message}\n`);
    await page.screenshot({ path: '/Users/dhr/.config/pinterest/error-' + Date.now() + '.png' });
    console.log('Screenshot saved.\n');
  } finally {
    await browser.close();
    console.log('✓ Done!\n');
  }
}

loginAndPublish().catch(console.error);
