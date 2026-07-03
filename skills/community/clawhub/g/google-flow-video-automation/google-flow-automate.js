#!/usr/bin/env node
/**
 * Google Flow 批量视频生成自动化脚本
 * 
 * 功能：
 * 1. 通过 Chrome CDP 连接已登录的 Chrome
 * 2. 批量生成视频（支持自定义提示词、时长、比例）
 * 3. 自动下载生成的视频到本地
 * 
 * 使用方法：
 *   node google-flow-automate.js --prompts prompts.txt --output ./videos
 */

const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================
const CONFIG = {
  cdpPort: 9222,
  cdpHost: '127.0.0.1',
  googleFlowUrl: 'https://labs.google/fx/tools/flow',
  defaultRatio: '16:9',
  defaultDuration: 'x2',  // x1=5s, x2=10s, x3=15s, x4=20s
  outputDir: './videos',
  pollInterval: 3000,
  maxWaitTime: 600000,  // 10分钟
  screenshotDir: './screenshots',
  selectorsFile: path.join(__dirname, 'selectors.json')
};

// ==================== 工具函数 ====================

/**
 * 连接到 Chrome CDP
 */
async function connectToChrome() {
  console.log('🔗 Connecting to Chrome via CDP...');
  const browser = await chromium.connectOverCDP(`http://${CONFIG.cdpHost}:${CONFIG.cdpPort}`);
  console.log('✅ Connected to Chrome');
  
  const contexts = browser.contexts();
  if (contexts.length === 0) {
    throw new Error('No browser contexts found. Please ensure Chrome is running with remote debugging.');
  }
  
  const context = contexts[0];
  let page = context.pages().find(p => p.url().includes('google.com')) || null;
  
  if (!page) {
    console.log('📄 No existing Google page found, creating new tab...');
    page = await context.newPage();
    await page.goto(CONFIG.googleFlowUrl, { waitUntil: 'networkidle', timeout: 30000 });
  } else {
    console.log('✅ Found existing Google page:', page.url());
    await page.bringToFront();
  }
  
  return { browser, page };
}

/**
 * 截图（只在关键步骤使用）
 */
async function takeScreenshot(page, name) {
  const dir = CONFIG.screenshotDir;
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  
  const filePath = path.join(dir, `${name}-${Date.now()}.png`);
  await page.screenshot({ path: filePath, fullPage: false });
  console.log(`📸 Screenshot saved: ${filePath}`);
  return filePath;
}

/**
 * 等待并点击（带重试）
 */
async function waitAndClick(page, selector, options = {}) {
  const { timeout = 10000, fallbackSelectors = [] } = options;
  
  try {
    await page.waitForSelector(selector, { timeout });
    await page.click(selector);
    console.log(`✅ Clicked: ${selector}`);
    return true;
  } catch (e) {
    console.log(`⚠️  Primary selector failed: ${selector}`);
    
    // 尝试 fallback selectors
    for (const fallback of fallbackSelectors) {
      try {
        await page.waitForSelector(fallback, { timeout: 2000 });
        await page.click(fallback);
        console.log(`✅ Clicked (fallback): ${fallback}`);
        return true;
      } catch (e2) {
        continue;
      }
    }
    
    throw new Error(`Failed to click any selector. Primary: ${selector}`);
  }
}

/**
 * 填写提示词（Google Flow 使用 contenteditable div）
 */
async function fillPrompt(page, promptText) {
  console.log('📝 Filling prompt:', promptText.substring(0, 50) + '...');
  
  const result = await page.evaluate((text) => {
    // 查找 contenteditable div（提示词输入框）
    const selectors = [
      '[contenteditable="true"]',
      'div[role="textbox"]',
      'textarea[aria-label*="prompt"]',
      'textarea[placeholder*="create"]'
    ];
    
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el) {
        el.focus();
        el.innerText = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return { success: true, selector: sel };
      }
    }
    
    return { success: false, error: 'No prompt input found' };
  }, promptText);
  
  if (!result.success) {
    throw new Error('Failed to fill prompt: ' + result.error);
  }
  
  console.log(`✅ Prompt filled using: ${result.selector}`);
  return result.selector;
}

/**
 * 打开设置面板并配置视频参数
 */
async function configureSettings(page, ratio = CONFIG.defaultRatio, duration = CONFIG.defaultDuration) {
  console.log(`⚙️  Configuring settings: ratio=${ratio}, duration=${duration}`);
  
  // 点击 Settings 按钮
  await waitAndClick(page, 'button[aria-label*="Settings"]', {
    fallbackSelectors: [
      'button:has(svg[data-icon="tune"])',
      'button:has-text("Settings")',
      '[role="button"]:has(svg[icon*="tune"])'
    ]
  });
  
  await page.waitForTimeout(1000);
  
  // 等待设置面板打开
  await page.waitForSelector('text*=Agent Settings', { timeout: 5000 });
  
  // 选择视频比例
  console.log(`  - Setting ratio: ${ratio}`);
  await page.click(`text=${ratio}`);
  await page.waitForTimeout(500);
  
  // 选择时长
  console.log(`  - Setting duration: ${duration}`);
  await page.click(`text=${duration}`);
  await page.waitForTimeout(500);
  
  // 保存设置
  await waitAndClick(page, 'button:has-text("Save")', {
    fallbackSelectors: ['button:has-text("Save")', 'button[aria-label*="Save"]']
  });
  
  console.log('✅ Settings saved');
  await page.waitForTimeout(1000);
}

/**
 * 点击 Create 并确认
 */
async function startGeneration(page) {
  console.log('🎬 Starting video generation...');
  
  // 点击 Create 按钮
  await waitAndClick(page, 'button:has-text("Create")', {
    fallbackSelectors: [
      'button[aria-label*="Create"]',
      'button:has(svg[data-icon="arrow_forward"])',
      '[role="button"]:has-text("Create")'
    ]
  });
  
  await page.waitForTimeout(2000);
  
  // 检查是否需要确认 credits
  const needConfirmation = await page.evaluate(() => {
    return document.body.innerText.includes('credits');
  });
  
  if (needConfirmation) {
    console.log('💰 Confirmation dialog detected, clicking "Yes"...');
    await waitAndClick(page, 'text*=Yes', {
      fallbackSelectors: ['button:has-text("Yes")', 'button:has-text("Confirm")']
    });
    await page.waitForTimeout(1000);
  }
}

/**
 * 轮询等待视频生成完成
 */
async function waitForVideoCompletion(page) {
  console.log('⏳ Waiting for video generation to complete...');
  
  const startTime = Date.now();
  let lastLogTime = 0;
  
  while (Date.now() - startTime < CONFIG.maxWaitTime) {
    const result = await page.evaluate(() => {
      // 查找视频元素或下载链接
      const videos = Array.from(document.querySelectorAll('video'));
      for (const video of videos) {
        if (video.src && video.src.includes('.mp4')) {
          return { done: true, url: video.src };
        }
      }
      
      // 查找已生成的视频缩略图（表示完成）
      const thumbnails = Array.from(document.querySelectorAll('img[src*="thumbnail"], img[src*="preview"]'));
      if (thumbnails.length > 0) {
        // 检查是否有下载按钮
        const downloadButtons = Array.from(document.querySelectorAll('button[aria-label*="Download"], a[download]'));
        if (downloadButtons.length > 0) {
          return { done: true, downloadUrl: downloadButtons[0].href || downloadButtons[0].src };
        }
      }
      
      return { done: false };
    });
    
    if (result.done) {
      console.log('✅ Video generation complete!');
      return result;
    }
    
    // 每10秒输出一次进度
    if (Date.now() - lastLogTime > 10000) {
      console.log(`  Still waiting... (${(Date.now() - startTime) / 1000}s elapsed)`);
      lastLogTime = Date.now();
    }
    
    await page.waitForTimeout(CONFIG.pollInterval);
  }
  
  throw new Error('Timeout: Video generation took too long');
}

/**
 * 下载视频
 */
async function downloadVideo(page, videoInfo, outputPath) {
  console.log('💾 Downloading video...');
  
  // 方法1: 直接通过 URL 下载
  if (videoInfo.url) {
    const response = await page.evaluate(async (url) => {
      const res = await fetch(url);
      const blob = await res.blob();
      return {
        data: await blob.arrayBuffer(),
        contentType: res.headers.get('content-type')
      };
    }, videoInfo.url);
    
    fs.writeFileSync(outputPath, Buffer.from(response.data));
    console.log(`✅ Video downloaded: ${outputPath} (${Buffer.from(response.data).length} bytes)`);
    return;
  }
  
  // 方法2: 点击下载按钮
  if (videoInfo.downloadUrl) {
    const response = await page.goto(videoInfo.downloadUrl);
    const buffer = await response.body();
    fs.writeFileSync(outputPath, buffer);
    console.log(`✅ Video downloaded: ${outputPath} (${buffer.length} bytes)`);
    return;
  }
  
  // 方法3: 查找并点击下载按钮
  console.log('  Trying to find download button...');
  await waitAndClick(page, 'button[aria-label*="Download"]', {
    fallbackSelectors: ['a[download]', 'button:has-text("Download")', 'svg[data-icon="download"]']
  });
  
  await page.waitForTimeout(3000);
  console.log('✅ Download triggered (check browser downloads)');
}

// ==================== 主流程 ====================

async function generateVideo(page, promptText, outputPath) {
  console.log('\n' + '='.repeat(60));
  console.log('🎬 Generating video:', promptText.substring(0, 60) + '...');
  console.log('='.repeat(60));
  
  // 1. 填写提示词
  await fillPrompt(page, promptText);
  await page.waitForTimeout(1000);
  
  // 2. 配置设置（如果还没配置过）
  // 注意：如果之前已经保存过 "don't ask again"，可以跳过这步
  try {
    await configureSettings(page);
  } catch (e) {
    console.log('⚠️  Settings configuration failed (might be already configured):', e.message);
  }
  
  // 3. 开始生成
  await startGeneration(page);
  
  // 4. 等待完成
  const videoInfo = await waitForVideoCompletion(page);
  
  // 5. 下载视频
  await downloadVideo(page, videoInfo, outputPath);
  
  console.log('✅ Video generation complete!');
  return outputPath;
}

async function main() {
  console.log('🚀 Google Flow Automation Starting...');
  
  // 解析命令行参数
  const args = process.argv.slice(2);
  const params = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    params[key] = value;
  }
  
  const prompts = params.prompts ? fs.readFileSync(params.prompts, 'utf-8').split('\n').filter(l => l.trim()) : [params.prompt];
  const outputDir = params.output || CONFIG.outputDir;
  
  if (!prompts || prompts.length === 0) {
    console.error('❌ Error: No prompts provided. Use --prompt or --prompts');
    process.exit(1);
  }
  
  // 创建输出目录
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  console.log(`📝 Prompts: ${prompts.length} video(s) to generate`);
  console.log(`📁 Output: ${outputDir}`);
  
  // 连接到 Chrome
  const { browser, page } = await connectToChrome();
  
  try {
    // 批量生成视频
    const results = [];
    for (let i = 0; i < prompts.length; i++) {
      const promptText = prompts[i];
      const outputPath = path.join(outputDir, `video-${i + 1}-${Date.now()}.mp4`);
      
      console.log(`\n[${i + 1}/${prompts.length}] Processing...`);
      
      try {
        const result = await generateVideo(page, promptText, outputPath);
        results.push({ prompt: promptText, output: result, success: true });
      } catch (e) {
        console.error(`❌ Failed to generate video ${i + 1}:`, e.message);
        results.push({ prompt: promptText, error: e.message, success: false });
      }
    }
    
    // 输出结果摘要
    console.log('\n' + '='.repeat(60));
    console.log('📊 Results Summary');
    console.log('='.repeat(60));
    results.forEach((r, i) => {
      if (r.success) {
        console.log(`✅ [${i + 1}] ${path.basename(r.output)}`);
      } else {
        console.log(`❌ [${i + 1}] Failed: ${r.error}`);
      }
    });
    
  } finally {
    await browser.close();
    console.log('\n✅ Automation complete!');
  }
}

// ==================== 入口 ====================

if (require.main === module) {
  main().catch(e => {
    console.error('❌ Fatal error:', e);
    process.exit(1);
  });
}

module.exports = { connectToChrome, fillPrompt, configureSettings, startGeneration, waitForVideoCompletion, downloadVideo };
