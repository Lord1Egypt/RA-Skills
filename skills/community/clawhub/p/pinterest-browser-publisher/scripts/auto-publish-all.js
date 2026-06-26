#!/usr/bin/env node

/**
 * Auto Publish All Pins
 * Fully automated: upload → fill → publish
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const COOKIES_FILE = path.join(process.env.HOME, '.config', 'pinterest', 'cookies.json');

const pins = [
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin01.png',
    title: '✨轻奢×中古ミックス✨大人の部屋作りアイデア',
    description: '高級感とヴィンテージの絶妙なバランス🏠 轻奢風と中古风を組み合わせることで、洗練された大人の空間が完成します。#轻奢风 #中古风 #房间布置 #家居灵感 #日式收纳 #东京生活 #室内设计 #软装搭配',
    board: 'ホームデコ'
  },
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin02.png',
    title: '🌿北欧風の定番🌿シンプルで心地いい暮らし',
    description: '白×木×緑の黄金比率🤍 北欧風は、どんなお部屋にも合いやすい定番スタイル。飽きがこなくて、毎日心地よく過ごせます。#北欧风 #简约风 #日式家居 #收纳技巧 #植物生活 #东京公寓 #软装设计',
    board: '北欧スタイル'
  },
  {
    image: '/Users/dhr/.openclaw/workspace-growth-agents/agents/jp-girl-agent/pins/pin03.png',
    title: '🥐フレンチ×クリーム色🥐優しさあふれるお部屋',
    description: 'クリーム色の壁とフレンチ雑貨で🧁 まるでパリのカフェのような、優しい雰囲気の空間。女子力が上がる、憧れのインテリアです。#法式风 #奶油风 #温柔风 #女生房间 #巴黎风 #软装灵感 #家居美学',
    board: 'フレンチスタイル'
  }
];

async function autoPublish() {
  console.log('📌 Pinterest Auto Publisher\n');
  console.log(`Total pins to publish: ${pins.length}\n`);

  if (!fs.existsSync(COOKIES_FILE)) {
    console.log('❌ No cookies. Run force-login.js first.\n');
    process.exit(1);
  }

  const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf-8'));

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--window-size=1280,800']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);

  for (let i = 0; i < pins.length; i++) {
    const pin = pins[i];
    console.log(`\n${'='.repeat(50)}`);
    console.log(`Publishing Pin ${i + 1}/${pins.length}`);
    console.log(`${'='.repeat(50)}`);
    console.log(`Title: ${pin.title}`);
    console.log(`Image: ${path.basename(pin.image)}\n`);

    const page = await context.newPage();

    try {
      // Go to creation tool
      console.log('Opening pin creation tool...');
      await page.goto('https://jp.pinterest.com/pin-creation-tool/', { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(8000);

      // Screenshot
      await page.screenshot({ path: `/tmp/pin${i+1}-start.png` });

      // Check login
      const profileBtn = await page.$('a[href="/profile/"]');
      if (!profileBtn) {
        console.log('⚠ Not logged in, waiting 30s...');
        await page.waitForTimeout(30000);
      }

      // Upload image
      console.log('Uploading image...');
      let fileInput = await page.$('input[type="file"]');
      
      if (!fileInput) {
        // Try clicking upload area
        const uploadArea = await page.$('div[role="button"], button:has-text("アップロード"), button:has-text("Upload")');
        if (uploadArea) {
          await uploadArea.click();
          await page.waitForTimeout(2000);
          fileInput = await page.$('input[type="file"]');
        }
      }

      if (fileInput) {
        await fileInput.setInputFiles([pin.image]);
        await page.waitForTimeout(10000);
        console.log('✓ Image uploaded\n');
      } else {
        console.log('⚠ Upload not found, trying drag-drop area click...\n');
        // Click center of page to trigger file dialog
        await page.mouse.click(640, 400);
        await page.waitForTimeout(5000);
      }

      await page.screenshot({ path: `/tmp/pin${i+1}-uploaded.png` });

      // Enter title
      console.log('Entering title...');
      const allInputs = await page.$$('input[type="text"], input:not([type])');
      for (const input of allInputs) {
        if (!await input.isVisible()) continue;
        const placeholder = await input.getAttribute('placeholder') || '';
        const ariaLabel = await input.getAttribute('aria-label') || '';
        
        if (placeholder.includes('タイトル') || placeholder.toLowerCase().includes('title') ||
            ariaLabel.includes('タイトル') || ariaLabel.toLowerCase().includes('title')) {
          await input.click();
          await input.fill(pin.title);
          console.log('✓ Title entered\n');
          break;
        }
      }

      // Enter description
      console.log('Entering description...');
      const allTextareas = await page.$$('textarea, div[contenteditable="true"]');
      for (const ta of allTextareas) {
        if (!await ta.isVisible()) continue;
        const placeholder = await ta.getAttribute('placeholder') || '';
        const ariaLabel = await ta.getAttribute('aria-label') || '';
        
        if (placeholder.includes('説明') || placeholder.toLowerCase().includes('description') ||
            ariaLabel.includes('説明') || ariaLabel.toLowerCase().includes('description')) {
          await ta.click();
          await ta.fill(pin.description);
          console.log('✓ Description entered\n');
          break;
        }
      }

      await page.screenshot({ path: `/tmp/pin${i+1}-filled.png` });

      // Select board
      if (pin.board) {
        console.log(`Selecting board: ${pin.board}...`);
        const boardBtn = await page.$('button:has-text("ボード"), button:has-text("Board")');
        if (boardBtn) {
          await boardBtn.click();
          await page.waitForTimeout(2000);
          
          const boardOption = await page.$(`text="${pin.board}"`);
          if (boardOption) {
            await boardOption.click();
            console.log('✓ Board selected\n');
          }
        }
      }

      // Find and click publish button
      console.log('Publishing...');
      const publishBtn = await page.$('button:has-text("保存"), button:has-text("公開"), button:has-text("Publish")');
      
      if (publishBtn) {
        await publishBtn.click();
        await page.waitForTimeout(5000);
        console.log('✓ Publish button clicked!\n');
      } else {
        console.log('⚠ Publish button not found. May need manual click.\n');
      }

      await page.screenshot({ path: `/tmp/pin${i+1}-done.png` });

      // Wait for publish to complete
      console.log('Waiting for publish to complete...');
      await page.waitForTimeout(10000);

      console.log(`✅ Pin ${i + 1} done!\n`);

    } catch (error) {
      console.log(`❌ Error: ${error.message}\n`);
      await page.screenshot({ path: `/tmp/pin${i+1}-error.png` });
    } finally {
      await page.close();
    }

    // Delay between pins
    if (i < pins.length - 1) {
      console.log('Waiting 30 seconds before next pin...\n');
      await page.waitForTimeout(30000);
    }
  }

  await browser.close();
  console.log('\n🎉 All pins published!\n');
}

autoPublish().catch(console.error);
