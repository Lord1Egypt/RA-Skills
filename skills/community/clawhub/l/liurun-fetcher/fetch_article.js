/**
 * 刘润公众号每日文章自动抓取
 * 策略：搜狗微信搜索 → 提取文章链接 → 获取全文
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// 搜索配置
const CONFIG = {
  searchUrl: 'https://wx.sogou.com/weixin',
  query: '刘润每日商业新闻',
  date: new Date().toISOString().split('T')[0].replace(/-/g, '月') + '号',
  // date: '4月20号', // 今天
  outputDir: path.join(__dirname, 'articles'),
  maxRetries: 2,
  timeout: 15000
};

// 确保输出目录存在
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

/**
 * 发送HTTP请求
 */
function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || 80,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://wx.sogou.com/',
        ...headers
      },
      timeout: CONFIG.timeout
    };

    const req = http.request(options, (res) => {
      // 处理重定向
      if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
        resolve(httpGet(res.headers.location, headers));
        return;
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data, headers: res.headers }));
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.end();
  });
}

/**
 * 搜索刘润今日文章
 */
async function searchTodayArticle() {
  console.log(`🔍 搜索日期: ${CONFIG.date}`);
  console.log(`📡 目标: ${CONFIG.searchUrl}?type=2&query=${encodeURIComponent(CONFIG.query + CONFIG.date)}`);

  try {
    const { status, data } = await httpGet(
      `${CONFIG.searchUrl}?type=2&query=${encodeURIComponent(CONFIG.query + ' ' + CONFIG.date)}`
    );

    console.log(`✅ 搜索完成，状态: ${status}, 数据大小: ${data.length} bytes`);

    // 提取文章链接
    // 搜狗微信格式: /link?url=xxx&type=2&query=xxx&token=xxx
    const linkPattern = /href="(\/link\?url=[^"&]+)"/g;
    const links = [];
    let match;

    while ((match = linkPattern.exec(data)) !== null) {
      links.push(match[1]);
    }

    console.log(`📰 找到 ${links.length} 个文章链接`);

    if (links.length === 0) {
      // 尝试备选搜索词
      console.log('🔄 尝试备选搜索词...');
      const altQuery = `刘润 ${CONFIG.date}`;
      const altData = await httpGet(
        `${CONFIG.searchUrl}?type=2&query=${encodeURIComponent(altQuery)}`
      );
      const altPattern = /href="(\/link\?url=[^"&]+)"/g;
      while ((match = altPattern.exec(altData.data)) !== null) {
        links.push(match[1]);
      }
    }

    return links;
  } catch (error) {
    console.error('❌ 搜索失败:', error.message);
    return [];
  }
}

/**
 * 获取文章全文
 */
async function fetchArticle(linkUrl) {
  console.log(`📖 尝试获取文章: ${linkUrl.substring(0, 80)}...`);

  try {
    // 完整URL
    const fullUrl = linkUrl.startsWith('http') ? linkUrl : `https://wx.sogou.com${linkUrl}`;
    const { status, data, headers } = await httpGet(fullUrl);

    console.log(`   状态: ${status}, 大小: ${data.length} bytes`);

    // 检查是否成功获取到微信文章
    if (data.includes('var clickurl') || data.includes('window.__RENDER_DATA__') || data.includes('js_content')) {
      // 提取文章内容 - 微信文章通常包含这些特征
      const titleMatch = data.match(/<h1[^>]*>([^<]+)<\/h1>/) || data.match(/"title"\s*:\s*"([^"]+)"/);
      const contentMatch = data.match(/id="js_content"[^>]*>([\s\S]*?)<\/section>/) ||
                          data.match(/"content"\s*:\s*"([^"]+)"/);

      const title = titleMatch ? titleMatch[1] : '未知标题';
      const content = contentMatch ? contentMatch[1] : data.substring(0, 5000);

      return { success: true, title, content: content.substring(0, 10000), data };
    }

    // 如果是搜狗的中间页，尝试从meta或script中提取真实URL
    const realUrlMatch = data.match(/url\s*=\s*["']([^"']+)["']/);
    if (realUrlMatch) {
      const realUrl = decodeURIComponent(realUrlMatch[1]);
      console.log(`   发现真实链接: ${realUrl.substring(0, 100)}...`);
      return { success: true, redirectUrl: realUrl, data };
    }

    return { success: false, data: data.substring(0, 2000) };
  } catch (error) {
    console.error('   ❌ 获取失败:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 提取纯文本内容
 */
function extractText(html) {
  return html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, '\n')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/\n\s*\n/g, '\n\n')
    .trim();
}

/**
 * 保存文章
 */
function saveArticle(article, filename) {
  const filepath = path.join(CONFIG.outputDir, filename);
  fs.writeFileSync(filepath, article, 'utf8');
  console.log(`💾 已保存: ${filepath}`);
  return filepath;
}

/**
 * 主流程
 */
async function main() {
  console.log('═══════════════════════════════════════════════');
  console.log('📰 刘润公众号每日文章抓取工具');
  console.log(`📅 执行时间: ${new Date().toLocaleString('zh-CN')}`);
  console.log('═══════════════════════════════════════════════\n');

  // 1. 搜索今日文章
  const links = await searchTodayArticle();

  if (links.length === 0) {
    console.log('\n❌ 未找到文章，尝试备选方案...');

    // 备选：直接访问刘润商业频道最近文章
    // 这个频道ID可能需要从搜索结果中获取
    console.log('📡 尝试直接访问刘润商业频道...');

    // 刘润商业频道的__biz可能是 MzA5NjUyNzYxOQ== (需要确认)
    // 直接尝试获取最近文章列表
    const bizChannels = [
      'MzA5NjUyNzYxOQ==', // 商业洞察
      // 可能的其他频道
    ];

    for (const biz of bizChannels) {
      console.log(`\n🔍 尝试频道: ${biz}`);
      // 微信文章列表API
      const listUrl = `https://mp.weixin.qq.com/profile?src=3&ver=1&token=123&lang=zh_CN&scene=123&__biz=${biz}`;
      const result = await httpGet(listUrl);
      console.log(`   状态: ${result.status}`);
    }
  }

  // 2. 尝试获取每个链接的文章
  console.log('\n═══════════════════════════════════════════════');
  console.log('📖 尝试获取文章全文...');
  console.log('═══════════════════════════════════════════════\n');

  let successCount = 0;

  for (let i = 0; i < Math.min(links.length, 3); i++) {
    console.log(`\n--- 文章 ${i + 1}/${Math.min(links.length, 3)} ---`);
    const result = await fetchArticle(links[i]);

    if (result.success) {
      successCount++;
      if (result.title) {
        const text = extractText(result.content || result.data);
        const article = `【${result.title}】\n\n${text}\n\n---原始数据长度: ${(result.data || '').length} bytes---`;
        const filename = `article_${new Date().toISOString().split('T')[0]}_${i + 1}.txt`;
        saveArticle(article, filename);
      }
    } else {
      console.log('   ⚠️ 获取文章内容失败');
      // 保存原始数据用于调试
      if (result.data) {
        const debugFile = `debug_${Date.now()}.html`;
        fs.writeFileSync(path.join(CONFIG.outputDir, debugFile), result.data.substring(0, 10000), 'utf8');
        console.log(`   🔍 已保存调试文件: ${debugFile}`);
      }
    }
  }

  // 3. 总结
  console.log('\n═══════════════════════════════════════════════');
  console.log('📊 抓取结果汇总');
  console.log('═══════════════════════════════════════════════');
  console.log(`✅ 成功: ${successCount}/${Math.min(links.length, 3)}`);
  console.log(`📁 文章保存目录: ${CONFIG.outputDir}`);

  // 列出保存的文件
  const files = fs.readdirSync(CONFIG.outputDir).filter(f => f.startsWith('article_'));
  console.log(`📄 已保存文章: ${files.length} 篇`);
  files.forEach(f => console.log(`   - ${f}`));

  return successCount > 0;
}

// 执行
main()
  .then(success => {
    console.log(`\n${success ? '🎉 抓取成功!' : '😢 抓取失败，请检查网络或API变化'}`);
    process.exit(success ? 0 : 1);
  })
  .catch(err => {
    console.error('\n💥 程序异常:', err);
    process.exit(1);
  });
