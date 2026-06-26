#!/usr/bin/env node

/**
 * Pinterest Browser Publisher - Login Script
 * Opens browser for manual login, saves cookies for future automated runs.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'pinterest');
const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');

async function login() {
  console.log('📌 Pinterest Login Helper\n');
  console.log('A browser window will open. Please:');
  console.log('1. Log in to your Pinterest account');
  console.log('2. Wait until you see your home feed');
  console.log('3. Close the browser window\n');

  // Ensure config directory exists
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--window-size=1280,800']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();

  console.log('Opening Pinterest login page...');
  await page.goto('https://www.pinterest.com/login/', { waitUntil: 'domcontentloaded', timeout: 60000 });

  // Wait for user to log in and navigate to home
  console.log('\nWaiting for login... (check the browser window)');
  
  // Wait for home feed indicator (pinned items grid)
  try {
    await page.waitForSelector('[data-grid-item="true"]', { timeout: 300000 });
    console.log('✓ Login detected!');
  } catch (e) {
    console.log('⚠ Timeout waiting for login. Proceeding anyway...');
  }

  // Save cookies
  const cookies = await context.cookies();
  fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2));
  console.log(`✓ Cookies saved to ${COOKIES_FILE}`);

  await browser.close();
  console.log('\n✓ Login complete! You can now use publish.js to auto-publish pins.');
}

login().catch(console.error);
