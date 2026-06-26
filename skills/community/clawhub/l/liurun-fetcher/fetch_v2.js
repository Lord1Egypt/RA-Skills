/**
 * 刘润公众号文章抓取 - 精简版
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const OUT_DIR = path.join(__dirname, 'articles');
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

// 今天的日期格式化
const today = new Date();
const monthDay = `${today.getMonth() + 1}月${today.getDate()}号`;
console.log(`📅 今日日期: ${monthDay}`);

function fetch(url) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const req = http.request({
      hostname: urlObj.hostname,
      port: urlObj.port || 80,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://wx.sogou.com/'
      },
      timeout: 10000
    }, res => {
      if ([301,302,303].includes(res.statusCode) && res.headers.location) {
        resolve(fetch(res.headers.location));
        return;
      }
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve({ status: res.statusCode, data: d }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

async function main() {
  // Step 1: 搜狗微信搜索
  const searchQuery = `刘润 ${monthDay}`;
  const searchUrl = `https://wx.sogou.com/weixin?type=2&query=${encodeURIComponent(searchQuery)}`;
  console.log(`\n🔍 搜索: ${searchQuery}`);

  let result;
  try {
    result = await fetch(searchUrl);
  } catch (e) {
    console.error('❌ 搜索失败:', e.message);
    process.exit(1);
  }

  console.log(`✅ 搜索完成 (${result.status}), ${result.data.length} bytes`);

  // 提取文章链接
  const linkMatches = [...result.data.matchAll(/href="(\/link\?url=[^"&]+)"/g)];
  console.log(`📰 找到 ${linkMatches.length} 个链接`);

  if (linkMatches.length === 0) {
    // 保存原始数据用于调试
    fs.writeFileSync(path.join(OUT_DIR, `debug_${Date.now()}.html`), result.data.substring(0, 20000), 'utf8');
    console.log('❌ 未找到链接，已保存调试文件');
    process.exit(1);
  }

  // Step 2: 逐个尝试获取文章
  for (let i = 0; i < Math.min(linkMatches.length, 5); i++) {
    const link = linkMatches[i][1];
    const fullUrl = `https://wx.sogou.com${link}`;
    console.log(`\n📖 尝试链接 ${i + 1}: ${link.substring(0, 60)}...`);

    try {
      const articleResult = await fetch(fullUrl);
      console.log(`   状态: ${articleResult.status}, 大小: ${articleResult.data.length}`);

      // 提取标题
      const titleMatch = articleResult.data.match(/<title>([^<]+)<\/title>/);
      const title = titleMatch ? titleMatch[1].trim() : `未知_${i}`;

      // 检查是否是微信文章内容
      const isWechatArticle = articleResult.data.includes('js_content') ||
                             articleResult.data.includes('appmsgtitle') ||
                             articleResult.data.includes('rich_media_content');

      if (isWechatArticle) {
        console.log(`🎉 成功! 标题: ${title}`);
        // 提取正文
        const contentMatch = articleResult.data.match(/id="js_content"[^>]*>([\s\S]*?)<section[^>]*id="js_pc_pd_/);
        const rawContent = contentMatch ? contentMatch[1] : articleResult.data.substring(0, 50000);

        // 清理HTML
        const text = rawContent
          .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
          .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
          .replace(/<[^>]+>/g, '\n')
          .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
          .replace(/\n\s*\n/g, '\n\n').trim();

        // 保存
        const filename = `article_${today.toISOString().split('T')[0]}.txt`;
        const content = `【${title}】\n来源: 刘润公众号\n日期: ${monthDay}\n\n${text}\n\n---原始大小: ${articleResult.data.length} bytes---`;
        fs.writeFileSync(path.join(OUT_DIR, filename), content, 'utf8');
        console.log(`💾 已保存: articles/${filename}`);
        console.log(`\n${'='.repeat(60)}`);
        console.log('📋 文章摘要预览:');
        console.log(text.substring(0, 2000));
        console.log('...\n');
        return; // 成功就退出
      } else {
        // 可能是搜狗中间页，尝试提取重定向URL
        const redirectMatch = articleResult.data.match(/url\s*=\s*["']([^"']+)["']/);
        if (redirectMatch) {
          console.log(`   → 跳转到: ${redirectMatch[1].substring(0, 80)}...`);
        } else {
          console.log(`   ⚠️ 不是微信文章内容`);
        }
      }
    } catch (e) {
      console.error(`   ❌ 请求失败: ${e.message}`);
    }
  }

  console.log('\n❌ 所有链接都失败了');
  // 保存调试信息
  fs.writeFileSync(path.join(OUT_DIR, `debug_last.html`), result.data.substring(0, 50000), 'utf8');
  console.log('🔍 已保存搜索结果到 debug_last.html');
}

main();
