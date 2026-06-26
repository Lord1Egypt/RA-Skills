/**
 * login.js — 启动有头浏览器，让用户手动登录 x.com，然后保存 session
 * 用法: node login.js
 */

const { chromium } = require('playwright');
const path = require('path');

const SESSION_DIR = path.join(__dirname, '..', 'session');

(async () => {
  console.log('🐾 Starting browser, please log in to x.com in the opened window...');
  console.log('📂 Session will be saved to:', SESSION_DIR);
  console.log('');
  console.log('✅ After logging in, press Enter in the terminal to save the session and close the browser.');
  console.log('');

  const context = await chromium.launchPersistentContext(SESSION_DIR, {
    headless: false,
    channel: 'chromium',
    viewport: { width: 1280, height: 900 },
    args: ['--disable-blink-features=AutomationControlled'],
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://x.com/i/grok');

  // 等待用户按 Enter
  await new Promise((resolve) => {
    process.stdin.setRawMode?.(false);
    process.stdin.resume();
    process.stdin.once('data', resolve);
  });

  console.log('💾 Saving session...');
  await context.close();
  console.log('✅ Session saved! You can now run npm run scrape to test meow~');
  process.exit(0);
})();
