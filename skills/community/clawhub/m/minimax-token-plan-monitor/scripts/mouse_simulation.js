#!/usr/bin/env node
/**
 * MiniMax Token Plan Scraper - Real Mouse Simulation
 */

const { chromium } = require('playwright');

async function scrapeTokenPlan() {
  const browser = await chromium.launch({ 
    headless: true,
    executablePath: '/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome'
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  
  const page = await context.newPage();
  
  console.error('Step 1: Login...');
  await page.goto('https://platform.minimaxi.com/login', { 
    waitUntil: 'networkidle',
    timeout: 30000 
  });
  
  await page.fill('input[placeholder*="手机号"], input[placeholder*="邮箱"]', 'your_account_here');
  await page.fill('input[type="password"]', 'sym,1998');
  
  const checkbox = await page.$('input[type="checkbox"]');
  if (checkbox && !(await checkbox.isChecked())) {
    await checkbox.click();
  }
  
  await page.click('button:has-text("立即登录"), button[type="submit"]');
  await page.waitForURL('**/user-center/**', { timeout: 15000 }).catch(() => {});
  console.error('Logged in, URL:', page.url());
  await page.waitForTimeout(3000);
  
  console.error('Step 2: Find and click Token Plan...');
  
  // Get the Token Plan element position
  const tokenPlanBox = await page.evaluate(() => {
    // Find all elements that contain "Token Plan" text
    const allElements = document.querySelectorAll('*');
    for (const el of allElements) {
      if (el.childNodes.length === 1 && el.textContent.trim() === 'Token Plan') {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          return { 
            x: rect.x + rect.width / 2, 
            y: rect.y + rect.height / 2,
            width: rect.width,
            height: rect.height
          };
        }
      }
    }
    return null;
  });
  
  if (tokenPlanBox) {
    console.error('Token Plan found at:', tokenPlanBox);
    
    // Move mouse to the element like a real user would
    await page.mouse.move(0, 0);
    await page.waitForTimeout(100);
    await page.mouse.move(tokenPlanBox.x - 50, tokenPlanBox.y - 50);
    await page.waitForTimeout(100);
    await page.mouse.move(tokenPlanBox.x, tokenPlanBox.y);
    await page.waitForTimeout(100);
    
    // Click
    await page.mouse.click(tokenPlanBox.x, tokenPlanBox.y);
    
    // Wait for potential navigation
    await page.waitForTimeout(5000);
    
    console.error('URL after mouse simulation:', page.url());
  } else {
    console.error('Token Plan element not found');
  }
  
  const text = await page.evaluate(() => document.body.innerText);
  console.log('Page text:', text.substring(0, 5000));
  
  // Try to extract usage
  const usageMatch = text.match(/已用\s*(\d+)\s*次/);
  const remainingMatch = text.match(/剩余\s*(\d+)\s*次/);
  const expiryMatch = text.match(/\d{4}-\d{2}-\d{2}/);
  const planMatch = text.match(/(?:Starter|Plus|Max)/);
  
  console.log(JSON.stringify({
    url: page.url(),
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
