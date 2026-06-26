#!/usr/bin/env node
/**
 * MiniMax Token Plan Scraper - Stealth Mode
 */

const puppeteer = require('puppeteer-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth')();

puppeteer.use(stealthPlugin);

async function scrapeTokenPlan() {
  const browser = await puppeteer.launch({ 
    headless: true,
    executablePath: '/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome'
  });
  
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });
  
  // Set realistic viewport and user agent
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
  
  console.error('Navigating to login...');
  await page.goto('https://platform.minimaxi.com/login', { 
    waitUntil: 'networkidle',
    timeout: 30000 
  });
  
  console.error('Filling login form...');
  await page.waitForSelector('input[placeholder*="手机号"], input[placeholder*="邮箱"]', { timeout: 10000 });
  await page.fill('input[placeholder*="手机号"], input[placeholder*="邮箱"]', 'your_account_here');
  await page.fill('input[type="password"]', 'sym,1998');
  
  const checkbox = await page.$('input[type="checkbox"]');
  if (checkbox && !(await checkbox.isChecked())) {
    await checkbox.click();
  }
  
  console.error('Clicking login button...');
  await page.click('button:has-text("立即登录"), button[type="submit"]');
  await page.waitForURL('**/user-center/**', { timeout: 15000 }).catch(() => {});
  
  console.error('Logged in, waiting for page...');
  await page.waitForTimeout(3000);
  
  // Try to click on Token Plan in sidebar using mouse
  console.error('Looking for Token Plan in sidebar...');
  
  // First expand 套餐管理 if needed
  const packageManager = await page.$('text="套餐管理"');
  if (packageManager) {
    console.error('Expanding 套餐管理...');
    await packageManager.click({ delay: 100 });
    await page.waitForTimeout(500);
  }
  
  // Try clicking using mouse coordinates
  const tokenPlanElement = await page.$('text="Token Plan"');
  if (tokenPlanElement) {
    const box = await tokenPlanElement.boundingBox();
    if (box) {
      console.error('Found Token Plan, clicking at', box.x + box.width/2, box.y + box.height/2);
      await page.mouse.click(box.x + box.width/2, box.y + box.height/2);
      await page.waitForTimeout(5000);
    }
  }
  
  console.error('Current URL:', page.url());
  
  const text = await page.evaluate(() => document.body.innerText);
  
  // Extract usage info
  const usageMatch = text.match(/已用\s*(\d+)\s*次/);
  const remainingMatch = text.match(/剩余\s*(\d+)\s*次/);
  const expiryMatch = text.match(/\d{4}-\d{2}-\d{2}/);
  const planMatch = text.match(/(?:Starter|Plus|Max)/);
  
  console.log(JSON.stringify({
    url: page.url(),
    text: text.substring(0, 5000),
    usage: usageMatch ? usageMatch[1] : null,
    remaining: remainingMatch ? remainingMatch[1] : null,
    expiry: expiryMatch ? expiryMatch[0] : null,
    plan: planMatch ? planMatch[0] : null
  }, null, 2));
  
  await browser.close();
}

scrapeTokenPlan().catch(err => {
  console.error('Error:', err.message);
  console.log(JSON.stringify({ error: err.message }));
  process.exit(1);
});
