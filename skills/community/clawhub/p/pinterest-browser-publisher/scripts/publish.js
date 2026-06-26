#!/usr/bin/env node

/**
 * Pinterest Browser Publisher - Publish Pin
 * Automates pin creation via browser automation.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { parseArgs } = require('node:util');

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'pinterest');
const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');

// Human-like delay between 2-5 seconds
const randomDelay = () => Math.floor(Math.random() * 3000) + 2000;

// Bezier curve mouse movement simulation
async function humanMove(page, startX, startY, endX, endY, duration = 500) {
  const steps = 10;
  const cp1x = startX + (endX - startX) * 0.3;
  const cp1y = startY + (endY - startY) * 0.8;
  const cp2x = startX + (endX - startX) * 0.7;
  const cp2y = startY + (endY - startY) * 0.2;
  
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const t1 = 1 - t;
    const x = t1*t1*t1*startX + 3*t1*t1*t*cp1x + 3*t1*t*t*cp2x + t*t*t*endX;
    const y = t1*t1*t1*startY + 3*t1*t1*t*cp1y + 3*t1*t*t*cp2y + t*t*t*endY;
    await page.mouse.move(x, y);
    await page.waitForTimeout(duration / steps);
  }
}

async function publishPin(options) {
  const { images, title, description, board, link } = options;

  console.log('📌 Pinterest Pin Publisher\n');
  console.log(`Title: ${title}`);
  console.log(`Images: ${images.length}`);
  console.log(`Board: ${board}`);
  console.log('');

  // Check cookies exist
  if (!fs.existsSync(COOKIES_FILE)) {
    console.log('❌ No saved session found. Run "node scripts/login.js" first.');
    process.exit(1);
  }

  const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    // Navigate to create pin page - use home page first, then navigate
    console.log('Opening Pinterest home...');
    await page.goto('https://www.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);
    
    // Check if logged in by looking for profile icon
    const isLoggedIn = await page.$('a[href="/profile/"], button[aria-label="Profile"]');
    if (!isLoggedIn) {
      console.log('⚠ Not logged in. Redirecting to login...');
      await page.goto('https://www.pinterest.com/login/', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(5000);
      throw new Error('Not logged in. Please run "node scripts/login.js" first.');
    }
    
    console.log('✓ Logged in. Navigating to create pin...');
    await page.goto('https://www.pinterest.com/pin/create/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(randomDelay());

    // Upload images
    console.log('Uploading images...');
    const fileInput = await page.$('input[type="file"]');
    if (!fileInput) {
      throw new Error('Could not find file upload input. Pinterest UI may have changed.');
    }
    
    // Convert to absolute paths
    const absolutePaths = images.map(img => path.resolve(img));
    await fileInput.setInputFiles(absolutePaths);
    
    // Wait for upload to complete
    await page.waitForTimeout(5000);
    console.log(`✓ Uploaded ${images.length} image(s)`);

    // Wait for image preview to appear
    await page.waitForTimeout(randomDelay());

    // Enter title
    console.log('Entering title...');
    const titleInput = await page.$('input[aria-label*="title" i], input[placeholder*="title" i]');
    if (titleInput) {
      await titleInput.click();
      await page.keyboard.type(title, { delay: 50 });
      console.log(`✓ Title entered`);
    } else {
      console.log('⚠ Could not find title input');
    }

    await page.waitForTimeout(randomDelay());

    // Enter description
    console.log('Entering description...');
    const descInput = await page.$('textarea[aria-label*="description" i], textarea[placeholder*="description" i], div[contenteditable="true"]');
    if (descInput) {
      await descInput.click();
      await page.keyboard.type(description, { delay: 30 });
      console.log(`✓ Description entered`);
    } else {
      console.log('⚠ Could not find description input');
    }

    await page.waitForTimeout(randomDelay());

    // Enter link (optional)
    if (link) {
      console.log('Entering link...');
      const linkInput = await page.$('input[type="url"], input[placeholder*="website" i]');
      if (linkInput) {
        await linkInput.click();
        await page.keyboard.type(link, { delay: 30 });
        console.log(`✓ Link entered`);
      }
      await page.waitForTimeout(randomDelay());
    }

    // Select board
    console.log(`Selecting board: ${board}...`);
    const boardDropdown = await page.$('button[aria-label*="board" i], button:has-text("Choose board")');
    if (boardDropdown) {
      await boardDropdown.click();
      await page.waitForTimeout(1000);
      
      // Find and click the board
      const boardOption = await page.$(`text="${board}"`);
      if (boardOption) {
        await boardOption.click();
        console.log(`✓ Board selected`);
      } else {
        console.log(`⚠ Board "${board}" not found. Pin will be saved to default board.`);
      }
    }

    await page.waitForTimeout(randomDelay());

    // Publish
    console.log('Publishing pin...');
    const publishButton = await page.$('button[type="submit"], button:has-text("Publish"), button:has-text("Save")');
    if (publishButton) {
      await publishButton.click();
      console.log('✓ Publish button clicked');
      
      // Wait for confirmation
      await page.waitForTimeout(3000);
      
      // Check if we're still on create page (publish may have failed)
      const currentUrl = page.url();
      if (currentUrl.includes('/pin/create/')) {
        console.log('⚠ Still on create page - pin may not have published');
      } else {
        console.log(`✓ Pin published! URL: ${currentUrl}`);
      }
    } else {
      console.log('⚠ Could not find publish button');
    }

  } catch (error) {
    console.error('❌ Error:', error.message);
    
    // Take screenshot for debugging
    const screenshotPath = path.join(CONFIG_DIR, `error-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    console.log(`Screenshot saved: ${screenshotPath}`);
    
  } finally {
    await browser.close();
    console.log('\n✓ Done!');
  }
}

// Parse command line arguments
const { values: args } = parseArgs({
  options: {
    images: { type: 'string', short: 'i' },
    title: { type: 'string', short: 't' },
    description: { type: 'string', short: 'd' },
    board: { type: 'string', short: 'b' },
    link: { type: 'string', short: 'l' }
  }
});

if (!args.images || !args.title) {
  console.log('Usage: node publish.js --images "img1.png,img2.png" --title "Title" --description "Desc" --board "Board" --link "https://..."');
  process.exit(1);
}

publishPin({
  images: args.images.split(','),
  title: args.title,
  description: args.description || '',
  board: args.board || '',
  link: args.link || ''
}).catch(console.error);
