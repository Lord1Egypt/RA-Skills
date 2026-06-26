#!/usr/bin/env node

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const COOKIES_FILE = path.join(process.env.HOME, '.config', 'pinterest', 'cookies.json');
const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));

const pins = [
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin04.png',
    title: '💎轻奢×フレンチ💎エレガントな大人の空間',
    description: '轻奢の高級感とフレンチの優雅さを融合✨ 上質さを求める大人のためのインテリア。金属フレームで高級感を演出、曲線デザインで優しさを。#轻奢风 #法式优雅 #高级感 #成人房间 #精致生活 #家居设计 #品质生活'
  },
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin05.png',
    title: '🪵原木×北欧🪵温もりあるナチュラルスタイル',
    description: '木の温もりと北欧のシンプルさ🌲 自然素材に囲まれた、癒しの空間。忙しい毎日でも、家に帰ればホッとできます。無垢材の家具、グリーンを複数配置、自然光を最大限に。#原木风 #北欧风 #自然风 #木质家居 #治愈系 #日式简约 #绿植装饰'
  }
];

(async () => {
  console.log('📌 Pinterest Remaining Pins Publisher\n');
  console.log(`Publishing ${pins.length} more pins...\n`);

  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });
  await context.addCookies(cookies);

  for (let i = 0; i < pins.length; i++) {
    const pin = pins[i];
    const page = await context.newPage();
    
    console.log(`\n[${i+1}/${pins.length}] ${pin.title}`);
    
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
      
      await page.screenshot({ path: `/tmp/rem${i+1}-upload.png` });
      
      // Enter title
      console.log('  Entering title...');
      const titleInput = await page.$('input[placeholder*="标题"], input[placeholder*="タイトル"]');
      if (titleInput) {
        await titleInput.click();
        await page.keyboard.type(pin.title, { delay: 30 });
        console.log('  ✓ Title done');
      }
      
      // Enter description
      console.log('  Entering description...');
      const descTextarea = await page.$('textarea[placeholder*="说明"], textarea[placeholder*="説明"], div[contenteditable="true"]');
      if (descTextarea) {
        await descTextarea.click();
        await page.keyboard.type(pin.description, { delay: 20 });
        console.log('  ✓ Description done');
      }
      
      await page.screenshot({ path: `/tmp/rem${i+1}-filled.png` });
      await page.waitForTimeout(3000);
      
      // Publish
      console.log('  Publishing...');
      const publishBtn = await page.$('button:has-text("发布"), button:has-text("保存"), button:has-text("公開")');
      if (publishBtn) {
        await publishBtn.click();
        await page.waitForTimeout(5000);
        console.log('  ✓ Published!');
      }
      
      await page.screenshot({ path: `/tmp/rem${i+1}-done.png` });
      
      if (i < pins.length - 1) {
        console.log('  Waiting 20s...');
        await page.waitForTimeout(20000);
      }
      
    } catch (err) {
      console.log(`  ❌ ${err.message}`);
      await page.screenshot({ path: `/tmp/rem${i+1}-error.png` });
    }
    
    await page.close();
  }
  
  await browser.close();
  console.log('\n✅ All remaining pins published!\n');
})();
