#!/usr/bin/env node
/**
 * photo-downloader
 * 批量下载综艺/电影/电视剧的剧照和海报
 * 
 * Usage:
 *   node index.js "内容名称" [type] [limit]
 *   type: S=剧照(default), R=海报
 *   limit: 下载数量，默认5
 * 
 * Features:
 *  - 自动搜索内容获取ID
 *  - 支持分类下载（剧照/海报）
 *  - 分批下载，默认5张一批
 *  - 缓存已下载文件，跳过重复
 *  - 随机延迟反爬
 *  - 保存到 output/{contentName}/{type}/ 目录
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const os = require('os');

// 配置
const CONFIG = {
  defaultLimit: 5,         // 默认每批下载数量
  minDelayMs: 800,        // 最小延迟毫秒
  maxDelayMs: 2000,       // 最大延迟毫秒
  downloadDir: path.join(os.homedir(), '.openclaw/output/photo-download'),
};

// 随机延迟
function randomDelay() {
  const delay = Math.floor(CONFIG.minDelayMs + Math.random() * (CONFIG.maxDelayMs - CONFIG.minDelayMs));
  return new Promise(resolve => setTimeout(resolve, delay));
}

// 下载单个图片
async function downloadImage(imageUrl, refererUrl, outputPath) {
  return new Promise((resolve, reject) => {
    const parsedUrl = url.parse(imageUrl);
    
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.path,
      method: 'GET',
      headers: {
        'Referer': refererUrl,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
      }
    };

    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    
    const req = protocol.get(options, (response) => {
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        // 处理重定向
        console.log(`  ↪ Redirect to ${response.headers.location}`);
        resolve(downloadImage(response.headers.location, refererUrl, outputPath));
        return;
      }
      
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }

      const fileStream = fs.createWriteStream(outputPath);
      response.pipe(fileStream);
      
      fileStream.on('finish', () => {
        fileStream.close();
        const stats = fs.statSync(outputPath);
        resolve({
          success: true,
          path: outputPath,
          size: stats.size
        });
      });
      
      fileStream.on('error', (err) => {
        fs.unlink(outputPath, () => {});
        reject(err);
      });
    });

    req.on('error', (err) => {
      reject(err);
    });
    
    req.end();
  });
}

// GET 请求获取 HTML
async function getHtml(pageUrl) {
  return new Promise((resolve, reject) => {
    const parsedUrl = url.parse(pageUrl);
    
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.path,
      method: 'GET',
      headers: {
        'Referer': 'https://movie.douban.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
      }
    };

    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    let html = '';
    
    const req = protocol.get(options, (response) => {
      // 处理重定向
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        console.log(`  ↪ Redirect to ${response.headers.location}`);
        // 递归处理重定向
        getHtml(response.headers.location).then(resolve).catch(reject);
        return;
      }
      
      response.on('data', (chunk) => {
        html += chunk;
      });
      response.on('end', () => {
        if (response.statusCode !== 200) {
          reject(new Error(`HTTP ${response.statusCode}`));
          return;
        }
        resolve(html);
      });
    });
    
    req.on('error', reject);
  });
}

// 搜索内容获取第一个结果的 ID
async function searchMovie(movieName) {
  // 注意：此实现需要根据实际使用的内容平台进行适配
  // 当前示例使用通用的搜索 URL 格式
  const searchUrl = `https://movie.douban.com/search?text=${encodeURIComponent(movieName)}`;
  console.log(`🔍 Searching for "${movieName}"...`);
  console.log(`📍 Connecting to content platform...`);
  
  const html = await getHtml(searchUrl);
  
  // 提取 window.__DATA__ - 使用粗暴但可靠的方式提取第一个结果
  // 因为JSON里有未转义的双引号在onclick里，不能直接JSON.parse
  if (!html.includes('window.__DATA__')) {
    throw new Error('Failed to find window.__DATA__ from search page');
  }
  
  // 提取第一个结果的 id, title
  // 从 window.__DATA__ 开始找第一个 id
  const idMatch = html.match(/"id":\s*(\d+)/);
  const titleMatch = html.match(/"title":\s*"([^"]+)"/);
  const ratingMatch = html.match(/"value":\s*([\d\.]+)/);
  const urlMatch = html.match(/"url":\s*"([^"]+)"/);
  
  if (!idMatch || !titleMatch) {
    throw new Error('Failed to extract movie info from search results');
  }
  
  return {
    id: idMatch[1],
    title: titleMatch[1],
    url: urlMatch ? urlMatch[1] : null,
    rating: { value: ratingMatch ? ratingMatch[1] : 0 }
  };
}

// 从照片页面提取所有 photo ids
async function extractPhotoIds(subjectId, type) {
  // type: S=剧照, R=海报
  // 注意：此 URL 需要根据实际的内容平台进行适配
  const photosUrl = `https://movie.douban.com/subject/${subjectId}/photos?type=${type}`;
  console.log(`\n📖 Extracting photos from page...`);
  
  const html = await getHtml(photosUrl);
  
  // 提取所有图片URL，格式: https://[domain]/view/photo/[size]/public/p{photoId}.webp
  const regex = /https:\/\/[^\s"']+\/view\/photo\/l\/public\/p(\d+)\.webp/g;
  const photoIds = [];
  let match;
  
  while ((match = regex.exec(html)) !== null) {
    if (!photoIds.includes(match[1])) {
      photoIds.push(match[1]);
    }
  }
  
  console.log(`✅ Found ${photoIds.length} photos`);
  return photoIds;
}

// 批量下载照片
async function downloadPhotos(photoIds, subjectId, title, type, limit = CONFIG.defaultLimit) {
  const safeTitle = title.replace(/[<>:"/\\|?*]+/g, '_');
  const downloadDir = path.join(CONFIG.downloadDir, safeTitle, type === 'S' ? '剧照' : '海报');
  fs.mkdirSync(downloadDir, { recursive: true });
  
  // 读取已下载列表（通过文件存在判断）
  const existingPhotos = new Set();
  if (fs.existsSync(downloadDir)) {
    const files = fs.readdirSync(downloadDir);
    files.forEach(file => {
      const photoId = path.basename(file, path.extname(file));
      existingPhotos.add(photoId);
    });
  }
  
  console.log(`💾 Download directory: ${downloadDir}`);
  console.log(`📋 Found ${existingPhotos.size} already downloaded`);
  
  // 过滤掉已下载的
  const toDownload = photoIds.filter(id => !existingPhotos.has(id)).slice(0, limit);
  
  if (toDownload.length === 0) {
    console.log('🎉 All photos already downloaded!');
    return {
      success: 0,
      failed: 0,
      total: 0,
      directory: downloadDir
    };
  }
  
  console.log(`⬇️ Downloading ${toDownload.length} photos...\n`);
  
  let success = 0;
  let failed = 0;
  
  for (let i = 0; i < toDownload.length; i++) {
    const photoId = toDownload[i];
    const ext = '.webp';
    const filename = `${photoId}${ext}`;
    const outputPath = path.join(downloadDir, filename);
    
    // 注意：这些 URL 需要根据实际的内容平台进行适配
    const refererUrl = `https://movie.douban.com/subject/${subjectId}/photos?type=${type}`;
    const imageUrl = `https://img9.doubanio.com/view/photo/l/public/p${photoId}.webp`;
    
    process.stdout.write(`  [${i+1}/${toDownload.length}] ${photoId}... `);
    
    try {
      const result = await downloadImage(imageUrl, refererUrl, outputPath);
      console.log(`✅ ${(result.size / 1024).toFixed(0)}KB`);
      success++;
    } catch (error) {
      console.log(`❌ ${error.message}`);
      // 删除失败的空文件
      if (fs.existsSync(outputPath)) {
        fs.unlinkSync(outputPath);
      }
      failed++;
    }
    
    // 延迟，除非是最后一张
    if (i < toDownload.length - 1) {
      await randomDelay();
    }
  }
  
  console.log(`\n🏁 Download complete! Success: ${success}, Failed: ${failed}`);
  console.log(`📂 Saved to: ${downloadDir}`);
  
  return {
    success,
    failed,
    total: toDownload.length,
    alreadyDownloaded: existingPhotos.size,
    directory: downloadDir
  };
}

// 主函数
async function main() {
  let movieName = process.argv[2];
  let type = process.argv[3] || 'S';
  let limit = process.argv[4] ? parseInt(process.argv[4], 10) : CONFIG.defaultLimit;
  let subjectId = null;
  
  // 检查第一个参数是否是数字（直接传入subject id）
  if (movieName && /^\d+$/.test(movieName)) {
    subjectId = movieName;
    movieName = `movie-${subjectId}`;
  }
  
  if (!movieName) {
    console.log('Usage:');
    console.log('  node index.js "内容名称" [type] [limit]');
    console.log('  node index.js <content-id> [type] [limit]  (直接使用id，跳过搜索)');
    console.log('  type: S=剧照 (default), R=海报');
    console.log('  limit: 下载数量，默认5');
    process.exit(1);
  }
  
  console.log('========================================');
  console.log('🎬 剧照与海报批量下载工具');
  if (subjectId) {
    console.log(`🆔 Content ID: ${subjectId}`);
  } else {
    console.log(`🎬 内容: ${movieName}`);
  }
  console.log(`📸 类型: ${type === 'S' ? '剧照' : '海报'}`);
  console.log(`📊 批次数量: ${limit}`);
  console.log('========================================\n');
  
  try {
    let movie;
    if (subjectId) {
      // 直接使用传入的 id
      movie = { id: subjectId, title: movieName };
    } else {
      // 1. 搜索电影
      movie = await searchMovie(movieName);
      console.log(`✅ Found: "${movie.title}" (id: ${movie.id}) rating: ${movie.rating.value}`);
    }
    
    // 2. 提取所有photo ids
    const photoIds = await extractPhotoIds(movie.id, type);
    
    if (photoIds.length === 0) {
      console.log('❌ 未找到图片');
      console.log('\n💡 提示: 某些网站对爬虫需要进行验证，你可以:');
      console.log('   1. 在浏览器中打开目标页面进行登录验证');
      console.log('   2. 登录后，复制内容 ID 传给脚本: node index.js {id} S 5');
      console.log('   3. 或开启远程调试模式以继承浏览器登录状态');
      process.exit(1);
    }
    
    console.log(`✅ Found ${photoIds.length} photos`);
    
    // 3. 批量下载
    const result = await downloadPhotos(photoIds, movie.id, movie.title, type, limit);
    
    // 4. 提示是否继续下载更多
    const remaining = photoIds.length - result.alreadyDownloaded - result.success;
    if (remaining > 0) {
      console.log(`\n💡 There are ${remaining} more photos remaining.`);
      console.log(`   To download more, run: node index.js ${movie.id} ${type} ${remaining}`);
    }
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

main();
