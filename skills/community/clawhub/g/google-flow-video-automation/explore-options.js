#!/usr/bin/env node
/**
 * explore-options.js - 首次使用引导：探索 Google Flow 可用选项
 * 
 * 功能：
 * 1. 检查 Chrome CDP 连接
 * 2. 引导用户登录（如果未登录）
 * 3. 打开 Agent Settings 面板
 * 4. 探索所有可用选项（模型、比例、时长）
 * 5. 截图保存，生成配置文件
 * 
 * 使用场景：第一次使用 Google Flow 自动化前必须运行
 */

const { chromium } = require('/opt/homebrew/lib/node_modules/playwright-core');
const fs = require('fs');
const path = require('path');

console.log('🚀 欢迎使用 Google Flow 自动化 — 首次设置引导！\n');
console.log('📋 此脚本会帮你：');
console.log('   1. 检查 Chrome 连接状态');
console.log('   2. 引导你登录 Google Flow（如果还没登录）');
console.log('   3. 探索所有可用的模型、比例、时长选项');
console.log('   4. 保存配置，方便以后使用\n');
console.log('💡 预计耗时：3-5 分钟（主要是登录时间）\n');
console.log('=' .repeat(60) + '\n');

// 截图工具
async function screenshot(page, name) {
  const p = `/tmp/explore-${name}-${Date.now()}.png`;
  await page.screenshot({ path: p, fullPage: false });
  console.log(`   📸 截图已保存: ${p}`);
  return p;
}

// 主函数
async function main() {
  let browser;
  
  try {
    // 步骤 1：连接 Chrome
    console.log('📶 步骤 1/5：连接 Chrome...');
    browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
    console.log('   ✅ 连接成功！\n');
    
    let page = browser.contexts()[0].pages()[0];
    if (!page) {
      page = await browser.contexts()[0].newPage();
    }
    
    // 步骤 2：检查登录状态
    console.log('🔑 步骤 2/5：检查 Google Flow 登录状态...');
    const currentUrl = page.url();
    console.log(`   当前 URL: ${currentUrl}`);
    
    if (!currentUrl.includes('google') || currentUrl.includes('accounts.google.com')) {
      console.log('   ⚠️  未登录或不在 Google Flow 页面\n');
      console.log('   💡 请按以下步骤操作：');
      console.log('      1. 在 Chrome 窗口中，访问 https://labs.google/fx/tools/flow');
      console.log('      2. 点击 "Create with Google Flow" 按钮');
      console.log('      3. 输入账号：你的 Google 账号');
      console.log('      4. 输入密码：你的 Google 密码');
      console.log('      5. 完成登录后，回到这里按 Enter 继续\n');
      
      await waitForEnter();
      
      // 重新检查
      await page.reload({ waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(3000);
    }
    
    console.log('   ✅ 已登录 Google Flow！\n');
    
    // 步骤 3：导航到项目页面
    console.log('📂 步骤 3/5：准备探索设置选项...');
    
    // 点击 "New session" 或确保进入创作界面
    const hasSession = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const newSessionBtn = btns.find(b => (b.innerText || '').includes('New session'));
      if (newSessionBtn && newSessionBtn.offsetParent !== null) {
        newSessionBtn.click();
        return true;
      }
      return false;
    });
    
    if (hasSession) {
      console.log('   ✅ 已点击 "New session"');
      await page.waitForTimeout(2000);
    }
    
    await screenshot(page, 'ready');
    console.log('');
    
    // 步骤 4：打开 Agent Settings 面板
    console.log('⚙️  步骤 4/5：打开 Agent Settings 面板，探索可用选项...');
    
    const settingsOpened = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const tuneBtn = btns.find(b => {
        const t = b.innerText || '';
        return t.includes('tune') && t.includes('Settings');
      });
      
      if (tuneBtn && tuneBtn.offsetParent !== null) {
        tuneBtn.click();
        return true;
      }
      return false;
    });
    
    if (!settingsOpened) {
      console.log('   ⚠️  找不到 Agent Settings 按钮，可能需要先填写提示词');
      console.log('   💡 请在 Chrome 窗口中手动点击 "New session"，然后按 Enter 继续');
      await waitForEnter();
    } else {
      console.log('   ✅ Agent Settings 面板已打开');
      await page.waitForTimeout(1500);
    }
    
    await screenshot(page, 'settings-panel');
    
    // 步骤 5：探索所有选项
    console.log('');
    console.log('🔍 步骤 5/5：探索可用选项...');
    
    const options = await page.evaluate(() => {
      const result = {
        videoGeneration: { models: [], aspectRatios: [], durations: [] },
        imageGeneration: { models: [], aspectRatios: [], durations: [] },
        creditsInfo: {}
      };
      
      // 查找所有按钮
      const allButtons = Array.from(document.querySelectorAll('button'));
      
      // 分类收集选项
      allButtons.forEach(btn => {
        const text = (btn.innerText || '').trim();
        
        // 视频比例
        if (['16:9', '9:16', '4:3', '1:1', '3:4'].includes(text)) {
          if (!result.videoGeneration.aspectRatios.includes(text)) {
            result.videoGeneration.aspectRatios.push(text);
          }
        }
        
        // 时长
        if (['1x', 'x2', 'x3', 'x4'].some(d => text.includes(d))) {
          const duration = text.trim();
          if (!result.videoGeneration.durations.includes(duration)) {
            result.videoGeneration.durations.push(duration);
          }
        }
        
        // 模型（通过父元素文本判断是视频还是图片）
        const parentText = btn.closest('div')?.innerText || '';
        if (text.includes('Flash') || text.includes('Pro') || text.includes('Veo')) {
          const modelInfo = { name: text, type: parentText.includes('Video') ? 'video' : 'image' };
          
          if (modelInfo.type === 'video' && !result.videoGeneration.models.find(m => m.name === text)) {
            result.videoGeneration.models.push(modelInfo);
          } else if (modelInfo.type === 'image' && !result.imageGeneration.models.find(m => m.name === text)) {
            result.imageGeneration.models.push(modelInfo);
          }
        }
      });
      
      return result;
    });
    
    console.log('   ✅ 探索完成！\n');
    console.log('   📊 发现以下选项：');
    console.log(`      视频模型: ${options.videoGeneration.models.map(m => m.name).join(', ') || '未找到'}`);
    console.log(`      视频比例: ${options.videoGeneration.aspectRatios.join(', ') || '未找到'}`);
    console.log(`      视频时长: ${options.videoGeneration.durations.join(', ') || '未找到'}`);
    console.log('');
    
    // 保存配置
    const configPath = path.join(__dirname, 'available-options.json');
    const config = {
      exploredAt: new Date().toISOString(),
      account: 'YOUR_GOOGLE_EMAIL',
      ...options
    };
    
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`   💾 配置已保存到: ${configPath}\n`);
    
    await screenshot(page, 'options-explored');
    
    // 完成提示
    console.log('=' .repeat(60));
    console.log('🎉 首次设置完成！\n');
    console.log('📋 接下来的步骤：');
    console.log('   1. 查看上面的截图，确认选项是否正确');
    console.log('   2. 运行生成脚本：');
    console.log('      node generate-one.js --prompt "你的提示词" --output ./videos\n');
    console.log('💡 提示：');
    console.log('   - 以后使用不需要再运行此脚本');
    console.log('   - 如果发现新选项（Google 更新），可以再运行此脚本更新配置\n');
    
  } catch (err) {
    console.error('❌ 错误：', err.message);
    console.log('');
    console.log('💡 请检查：');
    console.log('   1. Chrome 是否已启动（带 --remote-debugging-port=9222 参数）');
    console.log('   2. 是否已手动登录 Google Flow');
    console.log('   3. 页面是否正常加载（截图在 /tmp/explore-*.png）');
  } finally {
    if (browser) await browser.close();
  }
}

// 等待用户按 Enter
function waitForEnter() {
  return new Promise(resolve => {
    process.stdin.once('data', () => resolve());
  });
}

main();
