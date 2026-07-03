#!/usr/bin/env node
/**
 * Google Flow 自动化 - 优化版（减少 Token 消耗）
 * 
 * 优化点：
 * 1. 使用缓存的 selectors（避免反复探索）
 * 2. 减少截图（只在失败时截图）
 * 3. 批量操作（一次连接，生成多条视频）
 * 4. 高效的 JS 执行（减少 evaluate 调用）
 * 
 * 使用方法：
 *   node google-flow-fast.js --prompts prompts.txt
 */

const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

// 加载配置
const CONFIG = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf-8'));

// 加载缓存的 selectors
let SELECTORS = {};
const selectorsPath = path.join(__dirname, CONFIG.selectorsFile || 'selectors.json');
if (fs.existsSync(selectorsPath)) {
  SELECTORS = JSON.parse(fs.readFileSync(selectorsPath, 'utf-8'));
}

/**
 * 保存 selectors 到缓存
 */
function saveSelectors() {
  SELECTORS.lastUpdated = new Date().toISOString();
  fs.writeFileSync(selectorsPath, JSON.stringify(SELECTORS, null, 2));
  console.log('💾 Selectors cached');
}

/**
 * 连接到 Chrome CDP（复用现有连接）
 */
async function connectToChrome() {
  const browser = await chromium.connectOverCDP(`http://${CONFIG.cdpHost}:${CONFIG.cdpPort}`);
  const context = browser.contexts()[0];
  let page = context.pages().find(p => p.url().includes('google'));
  
  if (!page) {
    page = await context.newPage();
    await page.goto(CONFIG.googleFlowUrl, { waitUntil: 'networkidle', timeout: 30000 });
  } else {
    await page.bringToFront();
  }
  
  return { browser, page };
}

/**
 * 智能点击（使用缓存的 selector，失败时自动探索）
 */
async function smartClick(page, actionName, fallbackSelectors) {
  const cachedSelector = SELECTORS[actionName];
  
  // 尝试使用缓存的 selector
  if (cachedSelector) {
    try {
      await page.waitForSelector(cachedSelector, { timeout: 3000 });
      await page.click(cachedSelector);
      console.log(`✅ [Cached] ${actionName}: ${cachedSelector}`);
      return cachedSelector;
    } catch (e) {
      console.log(`⚠️  Cached selector failed, exploring...`);
    }
  }
  
  // 探索并缓存新的 selector
  for (const selector of fallbackSelectors) {
    try {
      await page.waitForSelector(selector, { timeout: 2000 });
      await page.click(selector);
      SELECTORS[actionName] = selector;
      saveSelectors();
      console.log(`✅ [Explored] ${actionName}: ${selector}`);
      return selector;
    } catch (e) {
      continue;
    }
  }
  
  throw new Error(`Failed to find element for action: ${actionName}`);
}

/**
 * 填写提示词（优化版：一次性完成）
 */
async function fillPromptFast(page, promptText) {
  console.log(`📝 Prompt: ${promptText.substring(0, 50)}...`);
  
  const result = await page.evaluate((text) => {
    // 查找所有可编辑元素
    const editableElements = [
      ...document.querySelectorAll('[contenteditable="true"]'),
      ...document.querySelectorAll('div[role="textbox"]'),
      ...document.querySelectorAll('textarea')
    ];
    
    // 找到可见的那个
    for (const el of editableElements) {
      if (el.offsetParent !== null) {  // 可见
        el.focus();
        el.innerText = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        return { success: true, tag: el.tagName, className: el.className };
      }
    }
    
    return { success: false };
  }, promptText);
  
  if (!result.success) {
    throw new Error('Prompt input not found');
  }
  
  console.log(`✅ Prompt filled (${result.tag})`);
}

/**
 * 配置设置（优化版：使用智能点击）
 */
async function configureSettingsFast(page) {
  console.log('⚙️  Configuring settings...');
  
  // 点击 Settings 按钮
  await smartClick(page, 'settingsButton', [
    'button[aria-label*="Settings"]',
    'button:has(svg[data-icon="tune"])',
    'button:has-text("Settings")'
  ]);
  
  await page.waitForTimeout(800);
  
  // 选择比例
  await page.click(`text=${CONFIG.defaultRatio}`);
  await page.waitForTimeout(300);
  
  // 选择时长
  await page.click(`text=${CONFIG.defaultDuration}`);
  await page.waitForTimeout(300);
  
  // 保存
  await smartClick(page, 'saveButton', ['button:has-text("Save")']);
  await page.waitForTimeout(800);
  
  console.log('✅ Settings configured');
}

/**
 * 开始生成（优化版）
 */
async function startGenerationFast(page) {
  console.log('🎬 Starting generation...');
  
  // 点击 Create
  await smartClick(page, 'createButton', [
    'button:has-text("Create")',
    'button[aria-label*="Create"]'
  ]);
  
  await page.waitForTimeout(1500);
  
  // 检查是否需要确认
  const needConfirm = await page.evaluate(() => {
    return document.body.innerText.toLowerCase().includes('credit');
  });
  
  if (needConfirm) {
    console.log('💰 Confirming credits...');
    await smartClick(page, 'confirmYesButton', ['button:has-text("Yes")']);
    await page.waitForTimeout(1000);
  }
  
  console.log('✅ Generation started');
}

/**
 * 等待完成（优化版：减少轮询）
 */
async function waitForCompletionFast(page) {
  console.log('⏳ Waiting for completion...');
  
  const startTime = Date.now();
  let lastProgress = 0;
  
  while (Date.now() - startTime < CONFIG.maxWaitTime) {
    const status = await page.evaluate(() => {
      // 检查是否有视频元素
      const videos = document.querySelectorAll('video[src]');
      if (videos.length > 0) {
        return { done: true, url: videos[0].src };
      }
      
      // 检查是否有"Generation complete"消息
      if (document.body.innerText.includes('complete') || 
          document.body.innerText.includes('Download')) {
        const downloadButtons = document.querySelectorAll('button[aria-label*="Download"]');
        if (downloadButtons.length > 0) {
          return { done: true, downloadReady: true };
        }
      }
      
      // 返回进度（如果有进度条）
      const progressBar = document.querySelector('[role="progressbar"]');
      if (progressBar) {
        return { done: false, progress: progressBar.getAttribute('aria-valuenow') };
      }
      
      return { done: false };
    });
    
    if (status.done) {
      console.log('✅ Video generation complete!');
      return status;
    }
    
    // 每5秒输出一次进度
    if (status.progress && status.progress !== lastProgress) {
      console.log(`  Progress: ${status.progress}%`);
      lastProgress = status.progress;
    } else if (Date.now() - startTime > 30000 && (Date.now() - startTime) % 10000 < 500) {
      console.log(`  Still waiting... (${(Date.now() - startTime) / 1000}s)`);
    }
    
    await page.waitForTimeout(CONFIG.pollInterval);
  }
  
  throw new Error('Timeout waiting for video generation');
}

/**
 * 下载视频（优化版）
 */
async function downloadVideoFast(page, videoInfo, outputPath) {
  console.log('💾 Downloading video...');
  
  if (videoInfo.url) {
    // 方法1: 直接下载
    const response = await page.evaluate(async (url) => {
      const res = await fetch(url);
      return await res.arrayBuffer();
    }, videoInfo.url);
    
    fs.writeFileSync(outputPath, Buffer.from(response));
  } else if (videoInfo.downloadReady) {
    // 方法2: 点击下载按钮
    await smartClick(page, 'downloadButton', ['button[aria-label*="Download"]']);
    await page.waitForTimeout(3000);
  }
  
  console.log(`✅ Video saved: ${outputPath}`);
}

/**
 * 生成单条视频（完整流程）
 */
async function generateVideoFast(page, promptText, outputPath) {
  console.log('\n' + '='.repeat(50));
  
  try {
    // 1. 填写提示词
    await fillPromptFast(page, promptText);
    await page.waitForTimeout(500);
    
    // 2. 配置设置（如果首次运行）
    if (!SELECTORS.settingsButton) {
      await configureSettingsFast(page);
    } else {
      console.log('⚙️  Settings already configured (skipping)');
    }
    
    // 3. 开始生成
    await startGenerationFast(page);
    
    // 4. 等待完成
    const videoInfo = await waitForCompletionFast(page);
    
    // 5. 下载
    await downloadVideoFast(page, videoInfo, outputPath);
    
    return { success: true, output: outputPath };
  } catch (e) {
    console.error(`❌ Error: ${e.message}`);
    
    // 失败时截图
    if (CONFIG.screenshotOnError) {
      await page.screenshot({ path: `error-${Date.now()}.png` });
    }
    
    return { success: false, error: e.message };
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 Google Flow Automation (Optimized)');
  
  // 解析参数
  const args = process.argv.slice(2);
  const params = {};
  for (let i = 0; i < args.length; i += 2) {
    params[args[i].replace('--', '')] = args[i + 1];
  }
  
  // 读取提示词
  const prompts = params.prompts 
    ? fs.readFileSync(params.prompts, 'utf-8').split('\n').filter(l => l.trim())
    : [params.prompt];
  
  if (!prompts || prompts.length === 0) {
    console.error('❌ No prompts provided');
    process.exit(1);
  }
  
  const outputDir = params.output || CONFIG.outputDir;
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  console.log(`📝 ${prompts.length} video(s) to generate`);
  console.log(`📁 Output: ${outputDir}`);
  console.log(`🔧 Cached selectors: ${Object.keys(SELECTORS).length > 0 ? 'Yes' : 'No (will explore)'}`);
  
  // 连接 Chrome
  const { browser, page } = await connectToChrome();
  
  try {
    const results = [];
    
    for (let i = 0; i < prompts.length; i++) {
      const outputPath = path.join(outputDir, `video-${i + 1}-${Date.now()}.mp4`);
      console.log(`\n[${i + 1}/${prompts.length}] Generating...`);
      
      const result = await generateVideoFast(page, prompts[i], outputPath);
      results.push({ index: i + 1, ...result });
      
      // 视频之间稍微等待
      if (i < prompts.length - 1) {
        await page.waitForTimeout(2000);
      }
    }
    
    // 输出结果
    console.log('\n' + '='.repeat(50));
    console.log('📊 Results:');
    results.forEach(r => {
      if (r.success) {
        console.log(`  ✅ [${r.index}] ${path.basename(r.output)}`);
      } else {
        console.log(`  ❌ [${r.index}] ${r.error}`);
      }
    });
    
  } finally {
    await browser.close();
    console.log('\n✅ Done!');
  }
}

// 入口
if (require.main === module) {
  main().catch(e => {
    console.error('Fatal error:', e);
    process.exit(1);
  });
}

module.exports = { connectToChrome, fillPromptFast, smartClick };
