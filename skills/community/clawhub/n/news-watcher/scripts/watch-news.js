import { chromium } from 'playwright';
import { createHash } from 'crypto';
import fs from 'fs';
import path from 'path';
import os from 'os';
// execFileSync 仅用于调用 OpenClaw AI Agent（node openclaw.mjs），非任意 shell 命令
// 完整源码开源：https://github.com/vvxer/openclaw-news-watcher
import { execFileSync } from 'child_process';

// 必须设置 OPENCLAW_MJS 环境变量，指向 openclaw.mjs 路径
const OPENCLAW_MJS = process.env.OPENCLAW_MJS;
if (!OPENCLAW_MJS) {
  console.error('❌ 请设置环境变量 OPENCLAW_MJS，指向 openclaw.mjs 的完整路径');
  console.error('   例如: export OPENCLAW_MJS=/path/to/openclaw.mjs');
  process.exit(1);
}

function runOpenclaw(args) {
  return execFileSync('node', [OPENCLAW_MJS, ...args], { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
}

/**
 * News Watcher - 使用 Playwright 监听虚拟货币新闻
 * 通过哈希变化检测，新闻有更新时触发
 */

// ✅ 修复：使用正确的 Windows 缓存路径
const dataDir = process.env.USERPROFILE || os.homedir();
const cacheDir = path.join(dataDir, '.openclaw', 'cache');
const cacheFile = path.join(cacheDir, 'news-hash.json');

// 网站配置
const sites = {
  coindesk: {
    url: 'https://www.coindesk.com/zh',
    selector: 'a[href*="/zh/"]', // CoinDesk 用 link 标签
    getContent: () => document.querySelectorAll('a[href*="/zh/"]')
      .forEach((a, i) => console.log(`${i}: ${a.textContent?.slice(0, 50) || 'N/A'}`))
  },
  panews: {
    url: 'https://www.panewslab.com/zh',
    selector: '.news-item',
    getContent: () => document.querySelectorAll('.news-item')
      .forEach((a, i) => console.log(`${i}: ${a.textContent?.slice(0, 100) || 'N/A'}`))
  }
};

// 计算内容哈希
function hashContent(content) {
  return createHash('md5').update(content).digest('hex');
}

// 读取上次哈希
function getLastHash() {
  try {
    if (fs.existsSync(cacheFile)) {
      const data = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
      return data.hash || null;
    }
  } catch (e) {
    console.warn('无法读取缓存:', e.message);
  }
  return null;
}

// 保存当前哈希
function saveHash(hash) {
  try {
    // ✅ 确保缓存目录存在
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
    fs.writeFileSync(cacheFile, JSON.stringify({ 
      hash, 
      timestamp: Date.now() 
    }), 'utf8');
    console.log(`  💾 缓存已保存: ${cacheFile}`);
  } catch (e) {
    console.error('无法保存哈希:', e.message);
  }
}

// 发送首次连接测试信息（包含最新文章全文总结）
async function sendFirstConnectionTest(latest, fullContent, siteName) {
  try {
    const telegramId = process.env.TELEGRAM_USER_ID;
    if (!telegramId) {
      console.error('❌ 请设置环境变量 TELEGRAM_USER_ID（你的 Telegram Chat ID）');
      return false;
    }
    
    console.log('🤖 调用 OpenClaw Agent 进行首次总结...');
    const summary = await summarizeNews(latest.title, fullContent);
    
    const message = `✅ News Watcher 首次连接测试

📰 监听网站: ${siteName.toUpperCase()}
🔍 监听状态: 已启动

📌 最新文章总结:
${summary}

🔗 ${latest.url}

💡 之后有新文章发布时，会自动抓取全文总结并发送。
⏰ ${new Date().toLocaleString('zh-CN')}`;
    
    console.log('📨 发送首次连接测试到 Telegram...');
    try {
      runOpenclaw(['message', 'send', '--channel', 'telegram', '--target', telegramId, '--message', message]);
      console.log('✅ 测试消息发送成功\n');
      return true;
    } catch (execError) {
      console.error('📨 命令执行失败:', execError.message);
      console.error('  stdout:', execError.stdout || '(空)');
      console.error('  stderr:', execError.stderr || '(空)');
      throw execError;
    }
  } catch (error) {
    console.error('❌ 发送测试消息失败:', error.message);
    return false;
  }
}

// 调用 openclaw agent 总结新闻全文
async function summarizeNews(articleTitle, articleContent) {
  try {
    console.log('🤖 调用 OpenClaw Agent 进行总结...');
    
    const prompt = `以下是一篇来自 CoinDesk 的加密货币新闻全文，请用中文进行总结分析，不要访问任何网址：

标题：${articleTitle}

正文：
${articleContent.slice(0, 4000)}

请用中文回复，要求：
1. 核心事件是什么（2-3句话）
2. 对加密货币市场有何影响
3. 重要性评级（高/中/低）及理由
格式简洁，适合 Telegram 阅读，控制在400字以内`;

    // 调用 openclaw agent
    console.log('⏳ 等待总结结果...');
    const result = runOpenclaw(['agent', '--agent', 'main', '--message', prompt, '--thinking', 'off', '--timeout', '90']);
    
    console.log('✅ 总结完成');
    return result;
    
  } catch (error) {
    console.error('❌ 总结失败:', error.message);
    return `（总结失败）${articleTitle}`;
  }
}

// 发送新文章总结到 Telegram
async function sendToTelegram(latest, fullContent, siteName) {
  try {
    const telegramId = process.env.TELEGRAM_USER_ID;
    if (!telegramId) {
      console.error('❌ 请设置环境变量 TELEGRAM_USER_ID（你的 Telegram Chat ID）');
      return false;
    }
    
    const summary = await summarizeNews(latest.title, fullContent);
    
    const message = `🔔 ${siteName.toUpperCase()} 新文章

📰 ${latest.title}

${summary}

🔗 ${latest.url}
⏰ ${new Date().toLocaleString('zh-CN')}`;
    
    console.log('📨 发送到 Telegram...');
    try {
      runOpenclaw(['message', 'send', '--channel', 'telegram', '--target', telegramId, '--message', message]);
      console.log('✅ Telegram 发送成功\n');
      return true;
    } catch (execError) {
      console.error('📨 命令执行失败:', execError.message);
      console.error('  stdout:', execError.stdout || '(空)');
      console.error('  stderr:', execError.stderr || '(空)');
      throw execError;
    }
  } catch (error) {
    console.error('❌ 发送 Telegram 失败:', error.message);
    return false;
  }
}

// 提取主页最新一条文章的链接和标题
async function extractLatestArticle(page) {
  return await page.evaluate(() => {
    // 匹配新闻文章链接（排除价格、视频、作者等页面）
    const links = Array.from(document.querySelectorAll('a[href]'))
      .filter(a => a.href.match(/coindesk\.com\/zh\/(markets|policy|business|tech|finance|web3|daybook)\//));
    if (links.length === 0) return null;
    const el = links[0];
    const lines = (el.textContent || '').trim().split('\n').map(l => l.trim()).filter(l => l.length > 5);
    return {
      url: el.href,
      title: lines[0] || '（无标题）',
      subtitle: lines[1] || ''
    };
  });
}

// 进入文章页面提取全文
async function extractArticleContent(page, articleUrl, mainUrl) {
  console.log(`  📖 读取文章全文...`);
  await page.goto(articleUrl, { waitUntil: 'load', timeout: 30000 });
  
  const content = await page.evaluate(() => {
    const main = document.querySelector('main');
    if (!main) return '';
    const blocks = Array.from(main.querySelectorAll('h1, h2, h3, h4, p'))
      .map(el => el.textContent?.trim())
      .filter(t => t && t.length > 10)
      .join('\n\n');
    return blocks;
  });
  
  // 读完文章后回到主页，为下次检查做准备
  try {
    await page.goto(mainUrl, { waitUntil: 'load', timeout: 30000 });
  } catch (e) { /* 忽略 */ }
  
  console.log(`  📄 获取到全文 ${content.length} 字符`);
  return content;
}

// 主监听函数（优化版本）
async function watchNews(siteName = 'coindesk', checkInterval = 60) {
  const site = sites[siteName];
  if (!site) {
    throw new Error(`未知的网站: ${siteName}. 支持: ${Object.keys(sites).join(', ')}`);
  }

  console.log(`\n🚀 开始监听 ${siteName.toUpperCase()} 新闻...`);
  console.log(`📍 URL: ${site.url}`);
  console.log(`⏱️  检查间隔: ${checkInterval}秒`);
  console.log(`� 缓存位置: ${cacheFile}`);
  console.log(`�🚄 性能优化: 保持连接 + 快速加载\n`);

  // 使用本地 Chrome（跨平台自动检测，或通过 CHROME_PATH 环境变量指定）
  const chromeExePath = process.env.CHROME_PATH || (
    process.platform === 'win32'
      ? 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
      : process.platform === 'darwin'
        ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        : '/usr/bin/google-chrome'
  );
  
  // ⚡ 优化 1: 一次启动，保持连接
  const browser = await chromium.launch({
    executablePath: chromeExePath,
    headless: process.env.PLAYWRIGHT_HEADLESS !== 'false',
    args: ['--disable-blink-features=AutomationControlled'] // 隐藏自动化标志
  });

  const page = await browser.newPage({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  });

  // 第一次访问，建立连接
  try {
    console.log('📡 初始化连接...');
    await page.goto(site.url, { waitUntil: 'load', timeout: 30000 });
  } catch (e) {
    console.error('初始连接失败:', e.message);
    await browser.close();
    throw e;
  }

  let checkCount = 0;
  let lastHash = getLastHash();

  try {
    while (true) {
      checkCount++;
      const timestamp = new Date().toLocaleString('zh-CN');
      
      console.log(`[${timestamp}] 检查 #${checkCount}...`);
      const startTime = Date.now();

      try {
        // 用 reload 刷新主页
        await page.reload({ waitUntil: 'load', timeout: 15000 });
        
        // 提取最新一条文章
        const latest = await extractLatestArticle(page);
        
        if (!latest) {
          console.log(`  ⚠️ 未找到文章链接，跳过本次检查`);
        } else {
          console.log(`  📰 最新文章: ${latest.title.slice(0, 60)}`);
          console.log(`  🔗 链接: ${latest.url}`);
          
          // 用文章 URL 做哈希（URL 变了 = 有新文章置顶）
          const currentHash = hashContent(latest.url);
          const elapsed = Date.now() - startTime;
          
          console.log(`  🔐 当前哈希: ${currentHash.slice(0, 8)}...`);
          console.log(`  🔐 上次哈希: ${lastHash ? lastHash.slice(0, 8) + '...' : '(无 - 首次运行)'}`);

          if (lastHash && currentHash !== lastHash) {
            console.log(`\n✅ 检测到新文章！(${elapsed}ms)`);
            const fullContent = await extractArticleContent(page, latest.url, site.url);
            saveHash(currentHash);
            lastHash = currentHash;
            await sendToTelegram(latest, fullContent, siteName);
            
          } else if (!lastHash) {
            console.log(`  ✓ 首次检查完成 (${elapsed}ms)`);
            const fullContent = await extractArticleContent(page, latest.url, site.url);
            saveHash(currentHash);
            lastHash = currentHash;
            await sendFirstConnectionTest(latest, fullContent, siteName);
            
          } else {
            console.log(`  ℹ️  无新文章 (${elapsed}ms)`);
          }
        }

      } catch (error) {
        console.error(`  ❌ 错误: ${error.message}`);
        // 出错时尝试重新访问
        try {
          console.log('  🔄 尝试重新连接...');
          await page.goto(site.url, { waitUntil: 'load', timeout: 30000 });
        } catch (e) {
          console.error('  ❌ 重新连接失败');
        }
      }

      // 等待下一次检查
      console.log(`⏳ 等待 ${checkInterval}秒后下次检查...\n`);
      await new Promise(resolve => setTimeout(resolve, checkInterval * 1000));
    }

  } finally {
    await browser.close();
    console.log('🛑 监听已停止');
  }
}

// CLI 入口
async function main() {
  const args = process.argv.slice(2);
  let siteName = 'coindesk';
  let checkInterval = 60;

  // 解析参数
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--site' && args[i + 1]) {
      siteName = args[++i];
    }
    if (args[i] === '--interval' && args[i + 1]) {
      checkInterval = parseInt(args[++i], 10);
    }
  }

  try {
    await watchNews(siteName, checkInterval);
  } catch (error) {
    console.error('错误:', error);
    process.exit(1);
  }
}

main();
