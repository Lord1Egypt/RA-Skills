#!/usr/bin/env node
/**
 * MiniMax Token Plan Check + QQ Notification
 */

const { chromium } = require('playwright');
const https = require('https');
const http = require('http');

async function sendQQMessage(userId, message) {
  // Use OpenClaw's /tools/invoke API to send message
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      tool: 'message',
      action: 'send',
      args: {
        channel: 'qqbot',
        target: userId,
        message: message
      }
    });
    
    const options = {
      hostname: 'localhost',
      port: 37701,
      path: '/tools/invoke',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Authorization': 'Bearer 8d9c37620f26ffb66ec81daba1547ac537b6dee5aa0cc8fd'
      }
    };
    
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.error('[Notify] Response:', res.statusCode, data);
        resolve({ success: res.statusCode === 200, response: data });
      });
    });
    
    req.on('error', (e) => {
      console.error('[Notify] Error:', e.message);
      resolve({ success: false, error: e.message });
    });
    
    req.write(postData);
    req.end();
  });
}

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
  
  const result = { success: false, data: null, error: null };

  try {
    await page.goto('https://platform.minimaxi.com/login', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForSelector('input[placeholder*="手机号"], input[placeholder*="邮箱"]', { timeout: 10000 });
    await page.fill('input[placeholder*="手机号"], input[placeholder*="邮箱"]', phone);
    await page.fill('input[type="password"]', password);
    
    const checkbox = await page.$('input[type="checkbox"]');
    if (checkbox && !(await checkbox.isChecked())) await checkbox.click();
    
    await page.click('button:has-text("立即登录"), button[type="submit"]');
    await page.waitForURL('**/user-center/**', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(3000);
    
    // Find Token Plan position
    const tokenPlanBox = await page.evaluate(() => {
      const allElements = document.querySelectorAll('*');
      for (const el of allElements) {
        if (el.childNodes.length === 1 && el.textContent.trim() === 'Token Plan') {
          const rect = el.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0 && rect.x < 200) {
            return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
          }
        }
      }
      return null;
    });
    
    if (!tokenPlanBox) throw new Error('Token Plan element not found');
    
    // Click with mouse movement
    await page.mouse.move(0, 0);
    await page.waitForTimeout(100);
    await page.mouse.move(tokenPlanBox.x - 50, tokenPlanBox.y - 50);
    await page.waitForTimeout(100);
    await page.mouse.move(tokenPlanBox.x, tokenPlanBox.y);
    await page.waitForTimeout(100);
    await page.mouse.click(tokenPlanBox.x, tokenPlanBox.y);
    await page.waitForTimeout(5000);
    
    const text1 = await page.evaluate(() => document.body.innerText);
    const planMatch = text1.match(/(Starter|Plus|Max|Ultra)/);
    const usageSection1 = text1.match(/当前使用[\s\S]*?(?=©|$)/);
    const usageText1 = usageSection1 ? usageSection1[0] : '';
    const used1Match = usageText1.match(/(\d+)\/600/);
    const percent1Match = usageText1.match(/(\d+)%\s*已使用/);
    
    // Click 本周 tab
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
      await page.mouse.move(0, 0);
      await page.waitForTimeout(100);
      await page.mouse.move(weekTabPos.x - 30, weekTabPos.y);
      await page.waitForTimeout(100);
      await page.mouse.move(weekTabPos.x, weekTabPos.y);
      await page.waitForTimeout(100);
      await page.mouse.click(weekTabPos.x, weekTabPos.y);
      await page.waitForTimeout(3000);
    }
    
    const text2 = await page.evaluate(() => document.body.innerText);
    const usageSection2 = text2.match(/当前使用[\s\S]*?(?=©|$)/);
    const usageText2 = usageSection2 ? usageSection2[0] : '';
    const used2Match = usageText2.match(/(\d+)\/600/);
    const percent2Match = usageText2.match(/(\d+)%\s*已使用/);
    const resetTimeMatch = usageText2.match(/重置时间:\s*(.+?)(?:\n|$)/);
    
    result.success = true;
    result.data = {
      plan: planMatch ? planMatch[1] : null,
      fiveHour: {
        used: used1Match ? parseInt(used1Match[1]) : null,
        limit: 600,
        usedPercent: percent1Match ? parseInt(percent1Match[1]) : null
      },
      week: {
        used: used2Match ? parseInt(used2Match[1]) : null,
        limit: 6000,
        usedPercent: percent2Match ? parseInt(percent2Match[1]) : null
      },
      resetTime: resetTimeMatch ? resetTimeMatch[1].trim() : null
    };

  } catch (error) {
    result.error = error.message;
  } finally {
    await browser.close();
  }
  
  return result;
}

async function main() {
  const phone = 'your_account_here';
  const password = 'sym,1998';
  const userId = '9BB108CD680D558F5BB78A066DF4FB37';
  
  console.error('[MiniMax] Starting check...');
  const result = await scrapeTokenPlanUsage(phone, password);
  
  if (result.success && result.data) {
    const d = result.data;
    const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    
    const message = `📊 MiniMax Token Plan 用量报告

⏰ ${now}

🏷️ 套餐: ${d.plan}

📌 5小时窗口: ${d.fiveHour.used} / ${d.fiveHour.limit} (${d.fiveHour.usedPercent}%)

📌 本周: ${d.week.used} / ${d.week.limit} (${d.week.usedPercent}%)

🔄 ${d.resetTime}`;
    
    console.error('[MiniMax] Sending notification...');
    
    // Try to send via local API
    await sendQQMessage(userId, message);
    
    console.log(message);
  } else {
    console.error('[MiniMax] Error:', result.error);
    console.log(JSON.stringify(result, null, 2));
  }
  
  // Also save to log
  const fs = require('fs');
  const logPath = '/root/.openclaw/workspace/bb/skills/minimax-token-plan/daily_usage.log';
  const logLine = `[${new Date().toISOString()}] 套餐:${result.data?.plan || 'N/A'} | 5小时:${result.data?.fiveHour?.used || 'N/A'}/600(${result.data?.fiveHour?.usedPercent || 'N/A'}%) | 本周:${result.data?.week?.used || 'N/A'}/6000(${result.data?.week?.usedPercent || 'N/A'}%) | 重置:${result.data?.resetTime || 'N/A'}\n`;
  fs.appendFileSync(logPath, logLine);
}

main().catch(err => {
  console.error('[MiniMax] Fatal error:', err);
  process.exit(1);
});
