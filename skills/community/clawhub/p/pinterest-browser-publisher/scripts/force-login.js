#!/usr/bin/env node

/**
 * Force Login and Save Cookies
 * Opens browser, user logs in, cookies are saved immediately.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.env.HOME, '.config', 'pinterest');
const COOKIES_FILE = path.join(CONFIG_DIR, 'cookies.json');

async function forceLogin() {
  console.log('📌 Pinterest Force Login\n');
  console.log('A browser window will open.\n');
  console.log('Please:');
  console.log('1. Log in to https://jp.pinterest.com/');
  console.log('2. Wait until you see your home feed');
  console.log('3. The browser will close automatically and cookies will be saved\n');

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
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();

  console.log('Opening Pinterest Japan...');
  await page.goto('https://jp.pinterest.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });

  console.log('\n👉 Please log in now...\n');
  console.log('Waiting for login (max 5 minutes)...\n');

  // Wait for login - check for profile button
  const maxWait = 5 * 60 * 1000;
  const startTime = Date.now();
  let loggedIn = false;

  while (!loggedIn && (Date.now() - startTime) < maxWait) {
    await page.waitForTimeout(2000);
    
    // Check for profile button or home feed
    const profileBtn = await page.$('a[href="/profile/"], button[aria-label="Profile"], button[data-test-id="profile"]');
    const homeFeed = await page.$('[data-grid-item="true"], [data-test-id="home-feed"]');
    
    if (profileBtn || homeFeed) {
      loggedIn = true;
      console.log('✓ Login detected!\n');
    }
  }

  // Save cookies
  const cookies = await context.cookies();
  fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2));
  console.log(`✓ Cookies saved to: ${COOKIES_FILE}\n`);
  
  // Verify cookies
  console.log(`Saved ${cookies.length} cookies:`);
  const importantCookies = cookies.filter(c => 
    c.name.includes('sess') || c.name.includes('token') || c.name.includes('auth')
  );
  importantCookies.forEach(c => {
    console.log(`  - ${c.name}: ${c.value.slice(0, 50)}...`);
  });

  await browser.close();
  
  console.log('\n✅ Login complete!\n');
  console.log('You can now use publish scripts to auto-publish pins.\n');
}

forceLogin().catch(console.error);
