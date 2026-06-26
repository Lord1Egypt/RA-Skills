#!/usr/bin/env node

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const COOKIES_FILE = path.join(process.env.HOME, '.config', 'pinterest', 'cookies.json');
const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));

const pins = [
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin01.png',
    title: '✨轻奢×中古ミックス✨大人の部屋作りアイデア',
    description: '高級感とヴィンテージの絶妙なバランス🏠 轻奢風と中古风を組み合わせることで、洗練された大人の空間が完成します。#轻奢风 #中古风 #房间布置 #家居灵感 #日式收纳 #东京生活 #室内设计 #软装搭配'
  },
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin02.png',
    title: '🌿北欧風の定番🌿シンプルで心地いい暮らし',
    description: '白×木×緑の黄金比率🤍 北欧風は、どんなお部屋にも合いやすい定番スタイル。飽きがこなくて、毎日心地よく過ごせます。#北欧风 #简约风 #日式家居 #收纳技巧 #植物生活 #东京公寓 #软装设计'
  },
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin03.png',
    title: '🥐フレンチ×クリーム色🥐優しさあふれるお部屋',
    description: 'クリーム色の壁とフレンチ雑貨で🧁 まるでパリのカフェのような、優しい雰囲気の空間。女子力が上がる、憧れのインテリアです。#法式风 #奶油风 #温柔风 #女生房间 #巴黎风 #软装灵感 #家居美学'
  }
];

(async () => {
  console.log('📌 Pinterest Fix Publisher\n');

  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });
  await context.addCookies(cookies);

  for (let i = 0; i < pins.length; i++) {
    const pin = pins[i];
    const page = await context.newPage();
    
    console.log(`\n[${i+1}/3] ${pin.title}`);
    
    try {
      // Go to creation tool
      await page.goto('https://jp.pinterest.com/pin-creation-tool/', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(8000);
      
      // Upload image
      console.log('  Uploading...');
      const fileInput = await page.$('input[type="file"]');
      if (fileInput) {
        await fileInput.setInputFiles([pin.image]);
        await page.waitForTimeout(10000);
        console.log('  ✓ Uploaded');
      } else {
        console.log('  ⚠ No upload found');
        await page.waitForTimeout(5000);
      }
      
      await page.screenshot({ path: `/tmp/fix${i+1}-upload.png` });
      
      // Find title input by placeholder "添加标题" or "タイトル"
      console.log('  Entering title...');
      const titleInput = await page.$('input[placeholder*="标题"], input[placeholder*="タイトル"], input[aria-label*="标题"]');
      if (titleInput) {
        await titleInput.click();
        await page.keyboard.type(pin.title, { delay: 30 });
        console.log('  ✓ Title done');
      } else {
        // Try clicking the input area and typing
        await page.click('text=添加标题');
        await page.keyboard.type(pin.title, { delay: 30 });
        console.log('  ✓ Title done (fallback)');
      }
      
      // Find description textarea
      console.log('  Entering description...');
      const descTextarea = await page.$('textarea[placeholder*="说明"], textarea[placeholder*="説明"], div[contenteditable="true"]');
      if (descTextarea) {
        await descTextarea.click();
        await page.keyboard.type(pin.description, { delay: 20 });
        console.log('  ✓ Description done');
      } else {
        console.log('  ⚠ No description field found');
      }
      
      await page.screenshot({ path: `/tmp/fix${i+1}-filled.png` });
      
      // Wait a bit for auto-save
      await page.waitForTimeout(3000);
      
      // Click publish button (red button with "发布" or "保存")
      console.log('  Publishing...');
      const publishBtn = await page.$('button:has-text("发布"), button:has-text("保存"), button:has-text("公開")');
      if (publishBtn) {
        await publishBtn.click();
        await page.waitForTimeout(5000);
        console.log('  ✓ Published!');
      } else {
        console.log('  ⚠ Publish button not found');
      }
      
      await page.screenshot({ path: `/tmp/fix${i+1}-done.png` });
      
      // Wait between pins
      if (i < pins.length - 1) {
        console.log('  Waiting 20s...');
        await page.waitForTimeout(20000);
      }
      
    } catch (err) {
      console.log(`  ❌ ${err.message}`);
      await page.screenshot({ path: `/tmp/fix${i+1}-error.png` });
    }
    
    await page.close();
  }
  
  await browser.close();
  console.log('\n✅ All done!\n');
})();
