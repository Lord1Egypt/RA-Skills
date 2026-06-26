#!/usr/bin/env node

/**
 * Pinterest Browser Publisher - Interactive Publish
 * Opens browser, user logs in manually, then publishes pins in the same session.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function interactivePublish() {
  console.log('📌 Pinterest Interactive Publisher\n');
  console.log('This will:');
  console.log('1. Open a browser window');
  console.log('2. You log in manually');
  console.log('3. Upload and publish pins\n');

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

  // Step 1: Login
  console.log('Opening Pinterest...');
  await page.goto('https://www.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  
  console.log('\n👉 Please log in to your Pinterest account in the browser window.');
  console.log('   When you see your home feed, press Enter here to continue...\n');
  await ask('   Press Enter when logged in: ');

  // Save cookies
  const CONFIG_DIR = path.join(process.env.HOME, '.config', 'pinterest');
  const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
  const cookies = await context.cookies();
  fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2));
  console.log('✓ Cookies saved\n');

  // Step 2: Get pin details
  const imagePath = await ask('   Image path: ');
  const title = await ask('   Title: ');
  const description = await ask('   Description: ');
  const board = await ask('   Board name: ');

  console.log('\n📌 Publishing...\n');

  // Navigate to create pin
  await page.goto('https://www.pinterest.com/pin/create/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(5000);

  // Upload image
  console.log('Uploading image...');
  const fileInput = await page.$('input[type="file"]');
  if (fileInput) {
    await fileInput.setInputFiles(path.resolve(imagePath));
    await page.waitForTimeout(5000);
    console.log('✓ Image uploaded\n');
  } else {
    console.log('❌ Could not find upload button. You may need to click it manually.\n');
  }

  // Enter title
  console.log('Entering title...');
  const titleInput = await page.$('input[aria-label*="title" i], input[placeholder*="title" i], input:not([type])');
  if (titleInput) {
    await titleInput.click();
    await page.keyboard.type(title, { delay: 50 });
    console.log('✓ Title entered\n');
  }

  // Enter description
  console.log('Entering description...');
  const descInput = await page.$('textarea[aria-label*="description" i], textarea[placeholder*="description" i], div[contenteditable="true"]');
  if (descInput) {
    await descInput.click();
    await page.keyboard.type(description, { delay: 30 });
    console.log('✓ Description entered\n');
  }

  // Select board
  console.log('Selecting board...');
  const boardButton = await page.$('button:has-text("Choose board"), button:has-text("Select board"), button[aria-label*="board" i]');
  if (boardButton) {
    await boardButton.click();
    await page.waitForTimeout(2000);
    
    const boardOption = await page.$(`text="${board}"`);
    if (boardOption) {
      await boardOption.click();
      console.log('✓ Board selected\n');
    }
  }

  console.log('👉 Please review and click "Publish" manually in the browser.\n');
  console.log('   The browser will stay open for 60 seconds...\n');

  await page.waitForTimeout(60000);
  await browser.close();
  rl.close();
  
  console.log('✓ Done!\n');
}

interactivePublish().catch(console.error);
