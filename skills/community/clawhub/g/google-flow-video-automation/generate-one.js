#!/usr/bin/env node
/**
 * generate-one.js v6 - 可靠版
 * 
 * 核心改进：
 * ✅ 检测当前 URL，自动判断页面状态
 * ✅ 项目列表页 → 点 "New project"
 * ✅ 项目页 → 点 "New session"（如需要）
 * ✅ Save 后等面板关闭再填提示词
 * ✅ 生成确认对话框自动点 "Yes"
 * ✅ 下载视频（多种方式尝试）
 * 
 * 使用：node generate-one.js --prompt "提示词" --output ./videos
 */

const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const cfg = { prompt: null, outputDir: '/tmp/flow-videos' };
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' && args[i+1]) { cfg.prompt = args[i+1]; i++; }
    if (args[i] === '--output' && args[i+1]) { cfg.outputDir = args[i+1]; i++; }
  }
  return cfg;
}
const cfg = parseArgs();
if (!cfg.prompt) { console.error('❌ 用法: node generate-one.js --prompt "提示词"'); process.exit(1); }

console.log('\n╔══════════════════════════════════════╗');
console.log('║   🎬 Google Flow 单条视频生成 v6    ║');
console.log('╚══════════════════════════════════════╝\n');
console.log(`📝 提示词  : ${cfg.prompt.substring(0,55)}...`);
console.log(`📁 输出目录: ${cfg.outputDir}\n`);

async function shot(page, label) {
  try { await page.screenshot({ path: `/tmp/v6-${label}.png`, fullPage: false }); } catch(e) {}
}

async function clickIt(page, findFn) {
  return await page.evaluate((fnStr) => {
    try { return new Function('return ' + fnStr)()(); } catch(e) { return false; }
  }, findFn.toString());
}

function waitForEnter() {
  return new Promise(resolve => {
    process.stdin.resume();
    process.stdin.once('data', () => { process.stdin.pause(); resolve(); });
  });
}

// ── 主流程 ──────────────────────────────────
(async () => {
  let browser;
  try {

    // ① 连接
    console.log('━━━ ①/9 ━━━ 连接 Chrome CDP ━━━');
    browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
    let page = browser.contexts()[0].pages()[0];
    const startUrl = page.url();
    console.log(`✅ 已连接 | ${startUrl.substring(0,70)}\n`);

    // ② 根据 URL 判断页面状态并导航
    console.log('━━━ ②/9 ━━━ 诊断 & 导航 ━━━');

    // 检查：是否在项目列表页（URL 不含 /project/）
    const isOnHomepage = !startUrl.includes('/project/');
    // 检查：设置面板是否开着
    const isSettingsOpen = await page.evaluate(() =>
      !!Array.from(document.querySelectorAll('button')).find(
        b => (b.innerText||'').trim() === 'Save' && b.offsetParent !== null
      )
    );
    // 检查：提示词框是否可见
    const hasInput = await page.evaluate(() =>
      Array.from(document.querySelectorAll('[contenteditable="true"]')).some(e => e.offsetParent !== null)
    );

    console.log(`   在项目列表页?  ${isOnHomepage ? '⚠️  是（需要新建项目）' : '✅ 否（已在项目内）'}`);
    console.log(`   设置面板开着?  ${isSettingsOpen ? '⚠️  是（需要先关闭）' : '✅ 否'}`);
    console.log(`   提示词框可见?  ${hasInput ? '✅ 是' : '⚠️  否'}\n`);

    // 关闭设置面板（如开着）
    if (isSettingsOpen) {
      console.log('   🔧 关闭设置面板...');
      await clickIt(page, () => {
        const btn = Array.from(document.querySelectorAll('button')).find(
          b => (b.innerText||'').includes('Back') || (b.innerText||'').includes('Close')
        );
        if (btn) { btn.click(); return true; }
        return false;
      });
      await page.waitForTimeout(1000);
    }

    // 在项目列表页 → 点 New project
    if (isOnHomepage) {
      console.log('   🔧 在项目列表页，点击 New project...');
      const npClicked = await clickIt(page, () => {
        const btn = Array.from(document.querySelectorAll('button')).find(
          b => (b.innerText||'').includes('New project')
        );
        if (btn) { btn.click(); return true; }
        return false;
      });
      if (!npClicked) throw new Error('无法找到 "New project" 按钮');
      console.log('   ✅ New project 已点击');
      await page.waitForTimeout(3000);
    }

    // 等待提示词框出现（最多 20 秒）
    console.log('   ⏳ 等待创作界面加载（提示词框出现）...');
    let inputReady = false;
    for (let i = 0; i < 20; i++) {
      inputReady = await page.evaluate(() =>
        Array.from(document.querySelectorAll('[contenteditable="true"]')).some(e => e.offsetParent !== null)
      );
      if (inputReady) break;
      await page.waitForTimeout(1000);
      process.stdout.write(`\r   ⏳ 等待创作界面加载... (${i+1}/20)`);
    }
    console.log(inputReady ? '\n   ✅ 创作界面已加载' : '\n   ❌ 创作界面加载超时');
    if (!inputReady) throw new Error('创作界面未加载（提示词框未出现）');
    console.log('');

    // ②.5 检查是否需要新建会话（避免提示词被当作聊天消息）
    console.log('   🔧 检查会话状态...');
    
    // ★ 关键：先切换到视频模式（点击 "Scenes" 标签）
    await page.evaluate(() => {
      const scenesTab = Array.from(document.querySelectorAll('*')).find(
        el => (el.innerText||'').includes('Scenes') && el.offsetParent !== null
      );
      if (scenesTab) {
        console.log('   切换到视频模式（Scenes 标签）');
        scenesTab.click();
      }
    });
    await page.waitForTimeout(2000);
    
    const needsNewSession = await page.evaluate(() => {
      return !!Array.from(document.querySelectorAll('button')).find(
        b => (b.innerText||'').includes('New session') && b.offsetParent !== null
      );
    });
    if (needsNewSession) {
      console.log('   🔧 点击 New session（开始新视频会话）...');
      await clickIt(page, () => {
        const btn = Array.from(document.querySelectorAll('button')).find(
          b => (b.innerText||'').includes('New session')
        );
        if (btn) { btn.click(); return true; }
        return false;
      });
      await page.waitForTimeout(3000);
      console.log('   ✅ 新视频会话已创建');
    } else {
      console.log('   ℹ️  无需新建会话');
    }
    console.log('');

    // ③ 填写提示词（关键：Slate.js编辑器必须用keyboard.type，不能用innerText）
    console.log('━━━ ③/9 ━━━ 填写提示词 ━━━');
    
    // ★ 关键：确保提示词以 "Video of" 开头，否则 Google Flow AI 会解析为图片生成
    let finalPrompt = cfg.prompt;
    const videoKeywords = ['video of', 'a video of', 'generate a video', 'create a video', 'animated video'];
    const lowerPrompt = cfg.prompt.toLowerCase().trim();
    const hasVideoKeyword = videoKeywords.some(kw => lowerPrompt.startsWith(kw));
    if (!hasVideoKeyword) {
      // 自动添加 "Video of " 前缀
      finalPrompt = 'Video of ' + cfg.prompt.replace(/^[^a-zA-Z]*/, '');
      console.log(`   ⚠️  提示词未以视频关键词开头，已自动添加前缀：`);
      console.log(`   📝 原提示词: ${cfg.prompt.substring(0,50)}...`);
      console.log(`   📝 修正后  : ${finalPrompt.substring(0,50)}...`);
    }
    
    const editorInfo = await page.evaluate(() => {
      // 优先找 Slate.js 编辑器
      const slate = document.querySelector('[data-slate-editor="true"]');
      if (slate && slate.offsetParent !== null) {
        slate.focus();
        const rect = slate.getBoundingClientRect();
        return { ok: true, x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
      }
      // 回退到普通 contenteditable
      const editors = Array.from(document.querySelectorAll('[contenteditable="true"]')).filter(
        e => e.offsetParent !== null
      );
      if (!editors.length) return { ok: false };
      editors[0].focus();
      const rect = editors[0].getBoundingClientRect();
      return { ok: true, x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
    });
    if (!editorInfo.ok) throw new Error('未找到提示词输入框');

    // 点击获取焦点，然后用 keyboard.type 输入（触发React状态更新）
    await page.mouse.click(editorInfo.x, editorInfo.y);
    await page.waitForTimeout(300);
    await page.keyboard.press('Control+a'); // 全选已有内容（如有）
    await page.waitForTimeout(100);
    await page.keyboard.press('Backspace');   // 清空
    await page.waitForTimeout(200);
    await page.keyboard.type(finalPrompt, { delay: 5 }); // ★ 关键：用type而非innerText，使用finalPrompt
    await page.waitForTimeout(500);
    console.log(`   ✅ 提示词已填写 (keyboard.type): "${finalPrompt.substring(0,60)}..."\n`);

    // ④ 打开 Agent Settings
    console.log('━━━ ④/9 ━━━ 打开 Agent Settings ━━━');
    await clickIt(page, () => {
      const btn = Array.from(document.querySelectorAll('button')).find(
        b => (b.innerText||'').includes('tune') && (b.innerText||'').includes('Settings')
      );
      if (btn) { btn.click(); return true; }
      return false;
    });
    await page.waitForTimeout(1200);
    await shot(page, 'settings');
    console.log('   ✅ 设置面板已打开\n');

    // ⑤ 配置参数：先选视频模型 → 16:9 + x2 + Save
    console.log('━━━ ⑤/9 ━━━ 配置参数（视频模型 + 16:9 + x2）→ Save ━━━');
    
    // ★ 关键：先点击当前模型按钮，打开模型选择菜单
    await page.evaluate(() => {
      // 查找当前模型按钮（显示模型名称，如 "Nano Banana 2" 或 "Omni Flash"）
      const allBtns = Array.from(document.querySelectorAll('button')).filter(b => b.offsetParent !== null);
      const modelBtn = allBtns.find(b => 
        (b.innerText||'').includes('Nano') || 
        (b.innerText||'').includes('Omni') || 
        (b.innerText||'').includes('Veo') ||
        (b.innerText||'').includes('Imagen')
      );
      
      if (modelBtn) {
        console.log('   检测到模型按钮:', (modelBtn.innerText||'').substring(0, 30));
        modelBtn.click();
        return true;
      }
      return false;
    });
    await page.waitForTimeout(1500);
    await shot(page, 'model-menu');
    console.log('   📸 已截图模型选择菜单：/tmp/v6-model-menu.png');
    
    // 在菜单中选择视频模型（Omni Flash 或 Veo）
    const modelSelected = await page.evaluate(() => {
      // 查找视频模型选项
      const videoModels = ['Omni Flash', 'Omni Pro', 'Veo'];
      for (const modelName of videoModels) {
        const el = Array.from(document.querySelectorAll('*')).find(
          e => (e.innerText||'').includes(modelName) && e.offsetParent !== null
        );
        if (el) {
          console.log('   选择视频模型:', modelName);
          el.click();
          return true;
        }
      }
      return false;
    });
    
    if (modelSelected) {
      console.log('   ✅ 已选择视频模型');
      await page.waitForTimeout(1000);
    } else {
      console.log('   ⚠️  未找到视频模型选项，可能已在视频模式');
    }
    
    // 然后配置比例和时长
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      btns.find(b => (b.innerText||'').trim() === '16:9' && b.offsetParent !== null)?.click();
      btns.find(b => (b.innerText||'').trim() === 'x2' && b.offsetParent !== null)?.click();
      btns.find(b => (b.innerText||'').trim() === 'Save' && b.offsetParent !== null)?.click();
    });
    console.log('   ✅ 已选择视频模型 + 16:9 + x2，已点 Save');

    // ★ 关键：Save 后等面板关闭，提示词框才重新出现
    console.log('   ⏳ 等待设置面板关闭...');
    await page.waitForTimeout(1500);
    console.log('');

    // ⑥ 点击 Create 提交生成（★ 用mouse.click确保触发React事件）
    console.log('━━━ ⑥/9 ━━━ 提交生成请求 ━━━');
    
    // ★ 关键：记录当前页面上的所有媒体 ID（避免检测到旧媒体）
    const oldMediaIds = await page.evaluate(() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      const ids = [];
      for (const img of imgs) {
        const src = img.src || '';
        if (src.includes('google')) {
          const m = src.match(/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/i);
          if (m) ids.push(m[1]);
        }
      }
      return ids;
    });
    console.log(`   📝 当前页面已有 ${oldMediaIds.length} 个媒体，将等待新媒体生成...`);
    
    const createBtn = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find(b =>
        b.offsetParent !== null &&
        (b.innerText||'').includes('arrow_forward') &&
        (b.innerText||'').includes('Create')
      );
      if (!target) return null;
      const r = target.getBoundingClientRect();
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
    });
    if (!createBtn) throw new Error('未找到 Create 提交按钮（arrow_forward）');
    await page.mouse.click(createBtn.x, createBtn.y);
    console.log('   ✅ Create 已点击，等待 AI 处理...');
    await page.waitForTimeout(3000);
    await shot(page, 'after-create');
    console.log('');

    // ⑦ 处理确认对话框（点 Yes）
    console.log('━━━ ⑦/9 ━━━ 处理确认对话框 ━━━');
    
    // ★ 关键：查找包含 "Yes" 的可点击元素（可能是复选框、div 等，不一定是 button）
    const clickYes = async () => {
      return await page.evaluate(() => {
        // 方法1：查找 button 包含 Yes
        let el = Array.from(document.querySelectorAll('button')).find(
          b => (b.innerText||'').includes('Yes') && b.offsetParent !== null
        );
        
        // 方法2：查找任何包含 Yes 的可点击元素
        if (!el) {
          el = Array.from(document.querySelectorAll('*')).find(
            e => (e.innerText||'').trim() === 'Yes' && e.offsetParent !== null
          );
        }
        
        // 方法3：查找包含 "Yes" 的父元素（可能是自定义组件）
        if (!el) {
          const allWithYes = Array.from(document.querySelectorAll('*')).filter(
            e => (e.innerText||'').includes('Yes') && e.offsetParent !== null
          );
          if (allWithYes.length > 0) {
            // 找最具体的那个（leaf node）
            el = allWithYes.find(e => e.children.length === 0) || allWithYes[0];
          }
        }
        
        if (el) {
          console.log('   找到 Yes 元素，点击:', (el.innerText||'').substring(0, 20));
          el.click();
          return true;
        }
        return false;
      });
    };
    
    let confirmed = false;
    for (let i = 0; i < 15; i++) {  // 增加检查次数（15次 × 800ms = 12秒）
      const needsConfirm = await page.evaluate(() => {
        const text = document.body.innerText.toLowerCase();
        return text.includes('credit') || text.includes('cost') || text.includes('would you like');
      });
      
      if (needsConfirm) {
        console.log('   💰 检测到积分确认对话框，点击 Yes...');
        const clicked = await clickYes();
        if (clicked) {
          console.log('   ✅ 已确认（点击 Yes）');
          confirmed = true;
          await page.waitForTimeout(2000);  // 等待确认生效
          break;
        }
      }
      await page.waitForTimeout(800);
    }
    
    if (!confirmed) {
      console.log('   ℹ️  无确认对话框（可能已勾选"不再询问"，或对话框文本未匹配）');
      // 再次检查（用更宽泛的匹配）
      const hasDialog = await page.evaluate(() => {
        return document.body.innerText.includes('Would you like') || 
               document.body.innerText.includes('kick off') ||
               document.body.innerText.includes('costing');
      });
      if (hasDialog) {
        console.log('   ⚠️  检测到未处理的确认对话框，尝试点击 Yes...');
        await clickYes();
        console.log('   ✅ 已补点 Yes');
        await page.waitForTimeout(2000);
      }
    }
    console.log('');

    // ⑧ 等待视频生成完成
    console.log('━━━ ⑧/9 ━━━ 等待视频生成完成 ━━━');
    console.log('   ⏳ 预计等待时间：1~3 分钟...\n');
    
    let videoId = null;
    const t0 = Date.now();
    const maxWait = 6 * 60 * 1000;

    while ((Date.now() - t0) < maxWait) {
      await page.waitForTimeout(5000);

      const result = await page.evaluate((oldIds) => {
        const imgs = Array.from(document.querySelectorAll('img'));
        for (const img of imgs) {
          const src = img.src || '';
          // 检测两种 URL 格式：
          // 1. /flow/ 格式（旧）
          // 2. media.getMediaUrlRedirect?name= 格式（新）
          if (img.offsetParent !== null && src.includes('google')) {
            let mediaId = null;
            
            // 格式 1: /flow/ URLs
            if (src.includes('/flow/')) {
              const m = src.match(/\/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/i);
              if (m) mediaId = m[1];
            }
            
            // 格式 2: media.getMediaUrlRedirect URLs（新格式）
            if (src.includes('media.getMediaUrlRedirect')) {
              const m = src.match(/name=([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/i);
              if (m) mediaId = m[1];
            }
            
            // ★ 关键：只返回新媒体（不在旧列表中）
            if (mediaId && !oldIds.includes(mediaId)) {
              return { found: true, id: mediaId };
            }
          }
        }
        return { found: false };
      }, oldMediaIds);

      if (result.found) {
        videoId = result.id;
        const elapsed = Math.floor((Date.now() - t0) / 1000);
        console.log(`\n   🎉 视频生成完成！ID: ${videoId}`);
        console.log(`   ⏱️  耗时: ${elapsed} 秒`);
        break;
      }

      const elapsed = Math.floor((Date.now() - t0) / 1000);
      process.stdout.write(`\r   ⏳ 已等待 ${elapsed}s... (最多等 6 分钟)  `);
    }
    console.log('');

    if (!videoId) throw new Error('视频生成超时（6分钟）');

    // ⑨ 下载视频
    console.log('\n━━━ ⑨/9 ━━━ 下载视频 ━━━');
    if (!fs.existsSync(cfg.outputDir)) fs.mkdirSync(cfg.outputDir, { recursive: true });

    const outPath = path.join(cfg.outputDir, `video-${Date.now()}.mp4`);
    console.log(`   📁 输出路径: ${outPath}`);

    // ★ 方法：通过 API 直接下载（最可靠）
    console.log(`   🌐 正在通过 API 下载媒体 ID: ${videoId}...`);
    
    try {
      // 步骤1：在浏览器上下文中获取媒体重定向 URL（带 cookies）
      const mediaRedirectUrl = await page.evaluate(async (mId) => {
        const apiUrl = `https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name=${mId}`;
        const resp = await fetch(apiUrl, { redirect: 'follow' });
        return resp.url;
      }, videoId);
      
      console.log(`   ✅ 获取到媒体 URL: ${mediaRedirectUrl.substring(0, 100)}...`);
      
      // 步骤2：下载媒体数据（使用 Node.js https 模块）
      const https = require('https');
      const http = require('http');
      
      await new Promise((resolve, reject) => {
        const protocol = mediaRedirectUrl.startsWith('https') ? https : http;
        
        protocol.get(mediaRedirectUrl, (resp) => {
          // 检查 Content-Type 判断是视频还是图片
          const contentType = resp.headers['content-type'] || '';
          const isVideo = contentType.includes('video');
          const finalPath = isVideo ? outPath : outPath.replace('.mp4', '.jpg');
          
          console.log(`   📝 媒体类型: ${contentType} (${isVideo ? '视频' : '图片'})`);
          console.log(`   💾 保存到: ${finalPath}`);
          
          const fileStream = fs.createWriteStream(finalPath);
          resp.pipe(fileStream);
          
          fileStream.on('finish', () => {
            fileStream.close();
            console.log(`   ✅ 下载完成！文件大小: ${fs.statSync(finalPath).size} bytes`);
            resolve();
          });
          
          fileStream.on('error', reject);
        }).on('error', reject);
      });
      
      console.log(`\n   🎉 视频已保存到: ${outPath}`);
      
    } catch (dlError) {
      console.log(`   ⚠️  API 下载失败: ${dlError.message}`);
      console.log(`   💡 请手动在 Chrome 中找到视频，右键 → 保存`);
    }

    // ── 完成 ──────────────────────────────────
    console.log('\n' + '='.repeat(50));
    console.log('🎉 视频生成流程完成！\n');
    console.log('📋 生成信息：');
    console.log(`   提示词  : ${finalPrompt.substring(0,40)}...`);
    console.log(`   视频 ID: ${videoId}`);
    console.log(`   输出    : ${cfg.outputDir}`);
    console.log('\n💡 提示：');
    console.log('   - 如需生成更多视频，请再次运行此脚本');
    console.log('   - 一次只生成一条，避免浪费积分 ✨\n');

  } catch (err) {
    console.error('\n❌ 错误：', err.message);
    console.log('\n💡 调试信息：');
    console.log('   - 截图已保存到 /tmp/v6-*.png');
    console.log('   - 请检查 Chrome 窗口状态\n');
  } finally {
    // CDP 连接无需显式断开，Node 进程退出会自动清理
    // 千万不要调用 browser.close()，否则会关闭用户的 Chrome！
    console.log('🔌 CDP 连接已释放（Chrome 保持运行）');
  }
})();
