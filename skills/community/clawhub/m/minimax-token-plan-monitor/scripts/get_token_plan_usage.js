#!/usr/bin/env node
/**
 * MiniMax Token Plan Usage Scraper
 * 
 * Uses Playwright to login and scrape Token Plan usage data.
 * Key: Use realistic mouse movements to trigger Next.js SPA routing.
 * Gets data from BOTH tabs: "5小时窗口" and "本周"
 */

const { chromium } = require('playwright');

async function scrapeTokenPlanUsage(phone, password) {
  const browser = await chromium.launch({ 
    headless: true,
    executablePath: '/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome'
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  
  const page = await context.newPage();
  
  const result = {
    success: false,
    data: null,
    error: null
  };

  try {
    console.error('[MiniMax] Step 1: Login...');
    await page.goto('https://platform.minimaxi.com/login', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });

    await page.waitForSelector('input[placeholder*="手机号"], input[placeholder*="邮箱"]', { timeout: 10000 });
    await page.fill('input[placeholder*="手机号"], input[placeholder*="邮箱"]', phone);
    await page.fill('input[type="password"]', password);
    
    const checkbox = await page.$('input[type="checkbox"]');
    if (checkbox && !(await checkbox.isChecked())) {
      await checkbox.click();
    }
    
    await page.click('button:has-text("立即登录"), button[type="submit"]');
    await page.waitForURL('**/user-center/**', { timeout: 15000 }).catch(() => {});
    console.error('[MiniMax] Logged in');
    await page.waitForTimeout(3000);
    
    console.error('[MiniMax] Step 2: Navigate to Token Plan page...');
    
    // Find the Token Plan element position in sidebar
    const tokenPlanBox = await page.evaluate(() => {
      const allElements = document.querySelectorAll('*');
      for (const el of allElements) {
        if (el.childNodes.length === 1 && el.textContent.trim() === 'Token Plan') {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0 && rect.x < 200) {
            return { 
              x: rect.x + rect.width / 2, 
              y: rect.y + rect.height / 2
            };
          }
        }
      }
      return null;
    });
    
    if (!tokenPlanBox) {
      throw new Error('Token Plan element not found');
    }
    
    console.error('[MiniMax] Token Plan found at:', tokenPlanBox);
    
    // Use realistic mouse movements to trigger the click
    await page.mouse.move(0, 0);
    await page.waitForTimeout(100);
    await page.mouse.move(tokenPlanBox.x - 50, tokenPlanBox.y - 50);
    await page.waitForTimeout(100);
    await page.mouse.move(tokenPlanBox.x, tokenPlanBox.y);
    await page.waitForTimeout(100);
    await page.mouse.click(tokenPlanBox.x, tokenPlanBox.y);
    
    // Wait for page navigation
    await page.waitForTimeout(5000);
    
    console.error('[MiniMax] URL after click:', page.url());
    
    // Get page content - default shows "5小时" tab data
    const text1 = await page.evaluate(() => document.body.innerText);
    
    // Find the usage section for first tab
    const planMatch = text1.match(/(Starter|Plus|Max|Ultra)/);
    
    // Extract data from first tab (5小时窗口)
    const usageSection1 = text1.match(/当前使用[\s\S]*?(?=©|$)/);
    const usageText1 = usageSection1 ? usageSection1[0] : '';
    const used1Match = usageText1.match(/(\d+)\/600/);
    const percent1Match = usageText1.match(/(\d+)%\s*已使用/);
    
    // Click on "本周" tab to get second data
    console.error('[MiniMax] Step 3: Click on 本周 tab...');
    
    const weekTabPos = await page.evaluate(() => {
      const allElements = document.querySelectorAll('*');
      for (const el of allElements) {
        if (el.childNodes.length === 1 && el.textContent.trim() === '本周') {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
          }
        }
      }
      return null;
    });
    
    if (weekTabPos) {
      console.error('[MiniMax] 本周 tab found at:', weekTabPos);
      
      // Click on 本周 tab
      await page.mouse.move(0, 0);
      await page.waitForTimeout(100);
      await page.mouse.move(weekTabPos.x - 30, weekTabPos.y);
      await page.waitForTimeout(100);
      await page.mouse.move(weekTabPos.x, weekTabPos.y);
      await page.waitForTimeout(100);
      await page.mouse.click(weekTabPos.x, weekTabPos.y);
      
      // Wait for data to update
      await page.waitForTimeout(3000);
      
      console.error('[MiniMax] URL after tab click:', page.url());
    } else {
      console.error('[MiniMax] 本周 tab not found');
    }
    
    // Get page content after tab click
    const text2 = await page.evaluate(() => document.body.innerText);
    
    // Extract data from second tab (本周)
    const usageSection2 = text2.match(/当前使用[\s\S]*?(?=©|$)/);
    const usageText2 = usageSection2 ? usageSection2[0] : '';
    const used2Match = usageText2.match(/(\d+)\/600/);
    const percent2Match = usageText2.match(/(\d+)%\s*已使用/);
    
    // Reset time (usually the same)
    const resetTimeMatch = usageText2.match(/重置时间:\s*(.+?)(?:\n|$)/);
    
    result.success = true;
    result.data = {
      url: page.url(),
      plan: planMatch ? planMatch[1] : null,
      // 5小时窗口数据
      fiveHour: {
        used: used1Match ? parseInt(used1Match[1]) : null,
        limit: 600,
        usedPercent: percent1Match ? parseInt(percent1Match[1]) : null
      },
      // 本周数据
      week: {
        used: used2Match ? parseInt(used2Match[1]) : null,
        limit: 600,
        usedPercent: percent2Match ? parseInt(percent2Match[1]) : null
      },
      resetTime: resetTimeMatch ? resetTimeMatch[1].trim() : null,
      rawText: text2.substring(0, 5000)
    };
    
    console.error('[MiniMax] Success! 5小时:', result.data.fiveHour.used + '/600, 本周:', result.data.week.used + '/600');

  } catch (error) {
    console.error('[MiniMax] Error:', error.message);
    result.success = false;
    result.error = error.message;
  } finally {
    await browser.close();
  }
  
  return result;
}

// CLI entry point
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('Usage: node get_token_plan_usage.js <phone> <password>');
    console.error('Example: node get_token_plan_usage.js your_account yourpassword');
    process.exit(1);
  }
  
  const [phone, password] = args;
  
  console.error('[MiniMax] Starting Token Plan scraper...');
  const result = await scrapeTokenPlanUsage(phone, password);
  
  console.log(JSON.stringify(result, null, 2));
}

main().catch(err => {
  console.error('[MiniMax] Fatal error:', err);
  console.log(JSON.stringify({ success: false, error: err.message }));
  process.exit(1);
});
