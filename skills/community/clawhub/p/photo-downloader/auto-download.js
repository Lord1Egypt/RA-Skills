#!/usr/bin/env node
/**
 * photo-downloader - 自动下载版本
 * 使用无头浏览器（Playwright）自动完成：
 *  1. 搜索内容获取ID
 *  2. 打开剧照/海报页面（继承已登录的会话状态，或连接到已有浏览器）
 *  3. 自动提取所有图片ID
 *  4. 分批下载
 */

const fs = require('fs');
const path = require('path');
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

// 下载单个图片（Node.js 直接下载，带正确Referer）
async function downloadImage(imageId, refererUrl, outputPath) {
  return new Promise((resolve, reject) => {
    const https = require('https');
    const url = require('url');
    
    // 豆瓣图片URL
    const imageUrl = `https://img9.doubanio.com/view/photo/l/public/p${imageId}.webp`;
    const parsedUrl = url.parse(imageUrl);
    
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.path,
      method: 'GET',
      headers: {
        'Referer': refererUrl,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
      }
    };

    const req = https.get(options, (response) => {
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        reject(new Error(`Redirect ${response.statusCode}`));
        return;
      }
      
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }

      const chunks = [];
      response.on('data', chunk => chunks.push(chunk));
      response.on('end', () => {
        const buffer = Buffer.concat(chunks);
        fs.writeFileSync(outputPath, buffer);
        resolve({ size: buffer.length });
      });
    });

    req.on('error', reject);
  });
}

// 批量下载
async function batchDownload(photoIds, subjectId, title, type, limit = CONFIG.defaultLimit) {
  const safeTitle = title.replace(/[<>:"/\\|?*]+/g, '_');
  const downloadDir = path.join(CONFIG.downloadDir, safeTitle, type === 'S' ? '剧照' : '海报');
  fs.mkdirSync(downloadDir, { recursive: true });
  
  // 读取已下载列表
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
      alreadyDownloaded: existingPhotos.size,
      directory: downloadDir
    };
  }
  
  console.log(`⬇️ Downloading ${toDownload.length} photos...\n`);
  
  let success = 0;
  let failed = 0;
  // 豆瓣剧照页面URL
  const refererUrl = `https://movie.douban.com/subject/${subjectId}/photos?type=${type}`;
  
  for (let i = 0; i < toDownload.length; i++) {
    const photoId = toDownload[i];
    const ext = '.webp';
    const filename = `${photoId}${ext}`;
    const outputPath = path.join(downloadDir, filename);
    
    process.stdout.write(`  [${i+1}/${toDownload.length}] ${photoId}... `);
    
    try {
      const result = await downloadImage(photoId, refererUrl, outputPath);
      console.log(`✅ ${(result.size / 1024).toFixed(0)}KB`);
      success++;
    } catch (error) {
      console.log(`❌ ${error.message}`);
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
  
  const remaining = photoIds.length - existingPhotos.size - success;
  if (remaining > 0) {
    console.log(`\n💡 There are ${remaining} more photos remaining.`);
    console.log(`   To download more, run: node auto-download.js ${subjectId} ${type} ${remaining}`);
  }
  
  return {
    success,
    failed,
    total: toDownload.length,
    alreadyDownloaded: existingPhotos.size,
    directory: downloadDir
  };
}

// 从浏览器HTML提取photo ids
function extractPhotoIds(html) {
  const regex = /https:\/\/[^\s"']+\/view\/photo\/l\/public\/p(\d+)\.webp/g;
  const photoIds = [];
  let match;
  
  while ((match = regex.exec(html)) !== null) {
    if (!photoIds.includes(match[1])) {
      photoIds.push(match[1]);
    }
  }
  
  return photoIds;
}

// 使用Playwright无头浏览器自动提取
async function extractPhotoIdsWithPlaywright(subjectId, type, isPerson = false) {
  // 启动无头浏览器，不需要连接已有浏览器（隐私安全考虑）
  const { chromium } = require('playwright');
  
  console.log('🔌 Starting headless browser...');
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  let photosUrl;
  if (isPerson) {
    // 影人照片页面
    photosUrl = `https://movie.douban.com/celebrity/${subjectId}/photos/`;
  } else {
    // 电影/剧集照片页面
    photosUrl = `https://movie.douban.com/subject/${subjectId}/photos?type=${type}`;
  }
  
  console.log(`📖 Loading photos page: ${photosUrl}`);
  await page.goto(photosUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
  // 等待页面加载完成（处理重定向）
  await page.waitForTimeout(3000);
  
  // 滚动加载更多图片 - 影人页面需要滚动才能加载更多照片
  console.log('🖱️ Scrolling to load more photos...');
  for (let i = 0; i < 12; i++) {
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(2000); // 给AJAX加载时间
  }
  // 最后再等一下，让最后一批图片加载完
  await page.waitForTimeout(3000);
  
  // 提取所有photo ids - 豆瓣图片本身就在img src里
  const photoIds = await page.evaluate(() => {
    if (!document) return [];
    const ids = [];
    console.log('Looking for photos...');
    // 1. 从所有图片的src提取
    const imgs = document.querySelectorAll('img');
    console.log('Found ' + imgs.length + ' images');
    for (let img of imgs) {
      // 匹配多种格式: /p1234567890.webp /p1234567890.jpg /p1234567890.jpeg
      const match = img.src.match(/\/p(\d+)\./);
      if (match && !ids.includes(match[1]) && match[1].length > 6) {
        ids.push(match[1]);
      }
    }
    console.log('Extracted ' + ids.length + ' IDs from img');
    // 2. 总是从链接再提取一遍，保证不丢
    const photoLinks = document.querySelectorAll('a[href*="/photo/"]');
    console.log('Found ' + photoLinks.length + ' photo links');
    for (let link of photoLinks) {
      const match = link.getAttribute('href').match(/\/photo\/(\d+)\//);
      if (match && !ids.includes(match[1]) && match[1].length > 6) {
        ids.push(match[1]);
      }
    }
    console.log('After links: ' + ids.length + ' IDs total');
    console.log('First 10 IDs: ' + ids.slice(0, 10).join(', '));
    return ids;
  });
  
  console.log('Extracted photo IDs: ' + photoIds.slice(0, 10).join(', ') + (photoIds.length > 10 ? '...' : ''));
  
  await browser.close();
  return photoIds;
}

// 搜索电影获取subject id - 使用Playwright因为有反爬
async function searchMovieWithPlaywright(movieName) {
  const { chromium } = require('playwright');
  
  // 启动无头浏览器，不需要连接已有浏览器（隐私安全考虑）
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  // 豆瓣电影搜索URL - 正确搜索电影需要去电影搜索页
  const searchUrl = `https://search.douban.com/movie/subject_search?search_text=${encodeURIComponent(movieName)}`;
  
  console.log(`🔍 Searching for "${movieName}"...`);
  console.log(`📍 Connecting to content platform...`);
  
  await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  
  // 提取第一个结果 - 数据已经在 window.__DATA__
  const result = await page.evaluate(() => {
    // 豆瓣已经把数据放在 window.__DATA__.items 里了！
    if (!window.__DATA__ || !window.__DATA__.items || window.__DATA__.items.length === 0) {
      return null;
    }
    // 遍历找第一个真正的内容（跳过 search_more 等占位类型）
    for (const item of window.__DATA__.items) {
      // 跳过"查看更多"这种占位项
      if (item.tpl_name === 'search_more') {
        continue;
      }
      // 判断类型：影人 vs 内容
      if (item.url && item.url.includes('/celebrity/')) {
        // 影人类型
        const match = item.url.match(/celebrity\/(\d+)/);
        const id = match ? match[1] : item.id + '';
        return {
          id: id,
          title: item.title,
          rating: item.rating ? item.rating.value : 0,
          isPerson: true
        };
      }
      // 普通电影/剧集 - 找到第一个就返回
      return {
        id: item.id + '',
        title: item.title,
        rating: item.rating ? item.rating.value : 0,
        isPerson: false
      };
    }
    // 没找到
    return null;
  });
  
  await browser.close();
  return result;
}

// 主函数
async function main() {
  let query = process.argv[2];
  let type = process.argv[3] || 'S';
  let limit = process.argv[4] ? parseInt(process.argv[4], 10) : CONFIG.defaultLimit;
  
  let subjectId = null;
  let movieTitle = null;
  
  // 判断是否直接传入subject id
  if (query && /^\d+$/.test(query)) {
    subjectId = query;
    movieTitle = `movie-${query}`;
  }
  
  console.log('========================================');
  console.log('🎬 剧照与海报批量下载 (自动无头浏览器版本)');
  if (subjectId) {
    console.log(`🆔 Content ID: ${subjectId}`);
  } else {
    console.log(`🎬 内容: ${query}`);
  }
  console.log(`📸 类型: ${type === 'S' ? '剧照' : '海报'}`);
  console.log(`📊 批次数量: ${limit}`);
  console.log('========================================\n');
  
  try {
    // 检查playwright是否安装
    try {
      require.resolve('playwright');
    } catch (e) {
      console.log('📦 Installing playwright...');
      const { execSync } = require('child_process');
      execSync('npm install playwright', { stdio: 'inherit' });
    }
    
    let movie;
    if (!subjectId) {
      // 搜索
      movie = await searchMovieWithPlaywright(query);
      if (!movie) {
        console.log('❌ No search results found');
        process.exit(1);
      }
      subjectId = movie.id;
      movieTitle = movie.title;
      console.log(`✅ Found: "${movieTitle}" (id: ${subjectId}) rating: ${movie.rating}`);
      console.log('');
    }
    
    // 提取photo ids
    console.log('🔍 Extracting photo ids from page...');
    const photoIds = await extractPhotoIdsWithPlaywright(subjectId, type, movie && movie.isPerson);
    
    if (photoIds.length === 0) {
      console.log('❌ No photos found');
      process.exit(1);
    }
    
    console.log(`✅ Found ${photoIds.length} photos`);
    console.log('');
    
    // 批量下载
    await batchDownload(photoIds, subjectId, movieTitle, type, limit);
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

// 如果直接运行
if (require.main === module) {
  main();
}

module.exports = {
  searchMovieWithPlaywright,
  extractPhotoIdsWithPlaywright,
  batchDownload,
  downloadImage,
  CONFIG
};
