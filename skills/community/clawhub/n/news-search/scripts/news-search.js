#!/usr/bin/env node

const { chromium } = require('playwright-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');

// 注册 Stealth 插件以绕过反爬虫检测
chromium.use(stealthPlugin());

const NEWS_ENGINES = {
  'google': {
    name: 'Google News',
    url: 'https://news.google.com/search?q={keyword}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans',
    selectors: ['article', '.M1VMeb'],
    titleSel: 'h3, .J7Y63c, .W8vS3b',
    linkSel: 'a',
    sourceSel: '.vr1PYe, .mg59ee'
  },
  'baidu': {
    name: '百度新闻',
    url: 'https://www.baidu.com/s?tn=news&word={keyword}',
    selectors: ['.result-op', '.result', '.c-container', 'div[class*="result"]', 'div[class*="container"]'],
    titleSel: 'h3, a.t, .c-title a, .news-title_1YDR3 a',
    linkSel: 'a',
    sourceSel: '.c-color-gray, .c-author, .source'
  },
  'bing': {
    name: 'Bing News',
    url: 'https://www.bing.com/news/search?q={keyword}',
    selectors: ['.news-card', '.card-with-cluster', '.article-card', 'div[class*="card"]'],
    titleSel: '.title, h2 a, h3 a, a[class*="title"]',
    linkSel: 'a',
    sourceSel: '.source, .attribution'
  },
  'toutiao': {
    name: '今日头条新闻',
    url: 'https://so.toutiao.com/search?keyword={keyword}&pd=news',
    selectors: ['.article-item', '.result-item', '.news-item', 'div[class*="article"]', 'div[class*="result"]'],
    titleSel: '.title, h3, .article-title, a[class*="title"]',
    linkSel: 'a',
    sourceSel: '.source, .author'
  },
  'sina': {
    name: '新浪新闻',
    url: 'https://search.sina.com.cn/?q={keyword}&c=news',
    selectors: ['.box-result', '.r-info'],
    titleSel: 'h2 a',
    linkSel: 'a',
    sourceSel: '.fgray_time'
  }
};

async function fetchNews(engineKey, keyword, maxResults = 10) {
  const engine = NEWS_ENGINES[engineKey];
  if (!engine) {
    throw new Error(`未知的搜索引擎: ${engineKey}`);
  }

  const url = engine.url.replace('{keyword}', encodeURIComponent(keyword));
  
  console.error(`🔍 [${engine.name}] 正在搜索: ${keyword}`);
  
  let browser;
  try {
    browser = await chromium.launch({ 
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    
    const page = await context.newPage();
    page.setDefaultTimeout(30000);
    
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000); // 等待异步内容加载
    
    // 滚动一下以触发懒加载
    await page.evaluate(() => window.scrollTo(0, 500));
    await page.waitForTimeout(1000);

    const results = await page.evaluate((config) => {
      const items = [];
      const seenLinks = new Set();
      
      for (const sel of config.selectors) {
        const elements = document.querySelectorAll(sel);
        
        elements.forEach((el) => {
          if (items.length >= 20) return;
          
          let title = '';
          let link = '';
          let source = '';
          let time = '';
          
          // 提取标题
          const titleEl = el.querySelector(config.titleSel);
          if (titleEl) {
            title = titleEl.textContent.trim();
            // 提取链接
            const linkEl = titleEl.tagName === 'A' ? titleEl : titleEl.closest('a') || el.querySelector('a');
            if (linkEl && linkEl.href) {
              link = linkEl.href;
            }
          }
          
          if (!title) {
            const hEl = el.querySelector('h1, h2, h3, h4');
            if (hEl) title = hEl.textContent.trim();
          }
          
          // 提取来源和时间
          const sourceEl = el.querySelector(config.sourceSel);
          if (sourceEl) {
            const sourceText = sourceEl.textContent.trim();
            // 简单的分割来源和时间，通常格式是 "来源 时间" 或 "来源 | 时间"
            const parts = sourceText.split(/[\s|]+/).filter(p => p.length > 0);
            if (parts.length > 0) source = parts[0];
            if (parts.length > 1) time = parts.slice(1).join(' ');
          }
          
          if (title && link && !link.includes('javascript') && !seenLinks.has(link)) {
            items.push({ title, link, source, time });
            seenLinks.add(link);
          }
        });
      }
      
      return items;
    }, engine);

    return results.slice(0, maxResults);
    
  } catch (error) {
    console.error(`❌ [${engine.name}] 搜索出错: ${error.message}`);
    return [];
  } finally {
    if (browser) await browser.close();
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('📖 用法: node news-search.js <keyword> [options]');
    console.log('\n参数:');
    console.log('  keyword          搜索关键词');
    console.log('\n选项:');
    console.log('  --engine=NAME    指定引擎 (google, baidu, bing, toutiao, sina, all)');
    console.log('  --max=N          最大结果数 (默认 10)');
    console.log('  --format=md|json 输出格式 (默认 md)');
    console.log('\n示例:');
    console.log('  node news-search.js "人工智能最新进展"');
    console.log('  node news-search.js "特斯拉财报" --engine=baidu');
    console.log('  node news-search.js "A股收盘" --engine=all --max=5');
    process.exit(1);
  }

  let keyword = '';
  let engineKey = 'all';
  let maxResults = 10;
  let format = 'md';

  // 解析参数
  const filteredArgs = [];
  for (const arg of args) {
    if (arg.startsWith('--engine=')) {
      engineKey = arg.split('=')[1];
    } else if (arg.startsWith('--max=')) {
      maxResults = parseInt(arg.split('=')[1]);
    } else if (arg.startsWith('--format=')) {
      format = arg.split('=')[1];
    } else {
      filteredArgs.push(arg);
    }
  }
  keyword = filteredArgs.join(' ');

  const enginesToUse = engineKey === 'all' 
    ? Object.keys(NEWS_ENGINES) 
    : [engineKey];

  const allResults = [];
  
  for (const key of enginesToUse) {
    if (!NEWS_ENGINES[key]) {
      console.error(`警告: 跳过未知引擎 ${key}`);
      continue;
    }
    const results = await fetchNews(key, keyword, maxResults);
    results.forEach(r => {
      allResults.push({ ...r, engine: NEWS_ENGINES[key].name });
    });
  }

  // 去重 (根据链接)
  const uniqueResults = [];
  const seenLinks = new Set();
  for (const r of allResults) {
    if (!seenLinks.has(r.link)) {
      uniqueResults.push(r);
      seenLinks.add(r.link);
    } else {
      // 如果已经有了，更新一下来源，显示多个来源
      const existing = uniqueResults.find(x => x.link === r.link);
      if (existing && !existing.engine.includes(r.engine)) {
        existing.engine += ` + ${r.engine}`;
      }
    }
  }

  // 输出结果
  if (format === 'json') {
    console.log(JSON.stringify(uniqueResults, null, 2));
  } else {
    console.log(`\n============================================================`);
    console.log(`🔍 "${keyword}" 新闻搜索结果（共 ${uniqueResults.length} 条）`);
    console.log(`============================================================\n`);

    if (uniqueResults.length === 0) {
      console.log('未找到相关新闻。');
    } else {
      uniqueResults.forEach((r, i) => {
        console.log(`${i + 1}. ${r.title}`);
        console.log(`   🔗 ${r.link}`);
        console.log(`   📌 来源: ${r.source || '未知'} | 渠道: ${r.engine}${r.time ? ` | 时间: ${r.time}` : ''}`);
        console.log('');
      });
    }
  }
}

main();
