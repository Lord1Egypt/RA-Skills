#!/usr/bin/env node

/**
 * Pinterest Japan Publisher v2
 * Click the "+" button to create pins
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
    'board': { type: 'string', default: '' },
    'link': { type: 'string', default: '' }
  }
});

async function publishJPv2() {
  console.log('📌 Pinterest Japan Publisher v2\n');
  
  if (!values.images || !values.title) {
    console.log('Usage:');
    console.log('node scripts/publish-jp-v2.js --images "./pin.png" --title "タイトル" --description "説明"\n');
    process.exit(1);
  }

  const images = values.images.split(',').map(p => p.trim());
  const title = values.title;
  const description = values.description || '';
  const board = values.board;

  console.log(`Title: ${title}`);
  console.log(`Images: ${images.length}`);
  if (board) console.log(`Board: ${board}`);
  console.log('');

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

    // Check login
    const profileBtn = await page.$('a[href="/profile/"], button[aria-label="Profile"]');
    if (!profileBtn) {
      console.log('⚠ Not logged in. Please log in manually...\n');
      await page.waitForTimeout(120000); // Wait 2 min for manual login
    }
    
    // Save cookies
    const newCookies = await context.cookies();
    fs.writeFileSync(COOKIES_FILE, JSON.stringify(newCookies, null, 2));
    console.log('✓ Cookies saved\n');

    // Method 1: Try direct URL
    console.log('Trying direct URL to create pin...');
    await page.goto('https://jp.pinterest.com/pin/create/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(8000);
    
    await page.screenshot({ path: '/tmp/pinterest-create-attempt1.png' });
    console.log('Screenshot 1: /tmp/pinterest-create-attempt1.png\n');

    // Check if we're on create page by looking for upload area
    let uploadFound = await page.$('input[type="file"]');
    
    if (!uploadFound) {
      // Method 2: Click the "+" button in sidebar
      console.log('Looking for create button (+)...');
      
      // Try various selectors for the create button
      const createBtn = await page.$('a[href="/pin/create/"], button:has-text("作成"), [data-test-id="create-pin"], .create-pin-button');
      
      if (createBtn) {
        console.log('Found create button, clicking...');
        await createBtn.click();
        await page.waitForTimeout(5000);
        await page.screenshot({ path: '/tmp/pinterest-create-attempt2.png' });
      } else {
        console.log('Create button not found. Trying keyboard shortcut...');
        // Pinterest uses 'C' for create
        await page.keyboard.press('c');
        await page.waitForTimeout(3000);
      }
    }

    // Upload images
    console.log('\nUploading images...');
    const absolutePaths = images.map(img => path.resolve(img));
    
    let fileInput = await page.$('input[type="file"]');
    
    if (fileInput) {
      await fileInput.setInputFiles(absolutePaths);
      await page.waitForTimeout(10000);
      console.log('✓ Images uploaded\n');
      
      await page.screenshot({ path: '/tmp/pinterest-after-upload.png' });
    } else {
      console.log('⚠ Upload input not found.');
      console.log('👉 Please drag & drop images or click to upload.\n');
      console.log('   Waiting 60 seconds for manual upload...\n');
      await page.waitForTimeout(60000);
    }

    // Enter title
    if (title) {
      console.log('Entering title...');
      const inputs = await page.$$('input:not([type="hidden"]), input[type="text"]');
      for (const input of inputs) {
        const visible = await input.isVisible();
        if (!visible) continue;
        
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
        const visible = await textarea.isVisible();
        if (!visible) continue;
        
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

    // Select board
    if (board) {
      console.log(`Selecting board: ${board}...`);
      const boardBtn = await page.$('button:has-text("ボード"), button:has-text("Board")');
      if (boardBtn) {
        await boardBtn.click();
        await page.waitForTimeout(2000);
        
        const boardOption = await page.$(`text="${board}"`);
        if (boardOption) {
          await boardOption.click();
          console.log('✓ Board selected\n');
        }
      }
    }

    // Final state
    console.log('✅ Pin setup complete!\n');
    console.log('👉 Please click "保存" (Save) or "公開" (Publish) to publish.\n');
    console.log('   Browser will close in 90 seconds...\n');

    await page.screenshot({ path: '/tmp/pinterest-final.png' });
    await page.waitForTimeout(90000);

  } catch (error) {
    console.log(`\n❌ Error: ${error.message}\n`);
    await page.screenshot({ path: '/Users/dhr/.config/pinterest/error-' + Date.now() + '.png' });
  } finally {
    await browser.close();
    console.log('✓ Done!\n');
  }
}

publishJPv2().catch(console.error);
