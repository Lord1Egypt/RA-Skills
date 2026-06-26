#!/usr/bin/env node
/**
 * photo-downloader
 * 下载综艺/电影/电视剧剧照，处理防盗链机制
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

function downloadImage(imageUrl, refererUrl, outputPath) {
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
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site'
      }
    };

    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    
    const req = protocol.get(options, (response) => {
      console.log('Status:', response.statusCode);
      
      if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
        // 处理重定向
        console.log('Redirect to:', response.headers.location);
        resolve(downloadImage(response.headers.location, refererUrl, outputPath));
        return;
      }
      
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage}`));
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

async function main() {
  const pageUrl = process.argv[2];
  if (!pageUrl) {
    console.error('Usage: node download.js https://example.com/photos/photo/12345678/');
    process.exit(1);
  }

  // 提取 photoId 从 URL
  const match = pageUrl.match(/photo\/(\d+)/);
  if (!match) {
    console.error('Invalid URL, expected format: https://example.com/photos/photo/12345678/');
    process.exit(1);
  }
  
  const photoId = match[1];
  const downloadDir = path.join(require('os').homedir(), 'download', 'photos');
  fs.mkdirSync(downloadDir, { recursive: true });
  const outputPath = path.join(downloadDir, `${photoId}.jpg`);

  console.log(`Downloading photo ${photoId} from: ${pageUrl}`);
  console.log(`Saving to: ${outputPath}`);

  // 尝试多种图片格式
  // 可能的格式: xl/公开/p{photoId}.jpg 或 l/公开/p{photoId}.webp

  // 先尝试高清格式
  // 注意：实际的URL由目标网站的域名组成
  console.log('💡 请确保 pageUrl 来自支持的内容平台');
  
  // 通用的图片URL模式
  let imageUrl = `${pageUrl.split('/photos/')[0]}/photos/l/public/p${photoId}.webp`;
  
  try {
    const result = await downloadImage(imageUrl, pageUrl, outputPath);
    console.log('\n✅ 下载成功!');
    console.log(`   Photo ID: ${photoId}`);
    console.log(`   File: ${result.path}`);
    console.log(`   Size: ${(result.size / 1024 / 1024).toFixed(2)} MB`);
  } catch (error) {
    console.log('\n❌ 尝试备用格式...');
    const imageUrlAlt = `${pageUrl.split('/photos/')[0]}/photos/xl/public/p${photoId}.jpg`;
    const outputPathAlt = path.join(downloadDir, `${photoId}-alt.jpg`);
    try {
      const result = await downloadImage(imageUrlAlt, pageUrl, outputPathAlt);
      console.log('\n✅ 下载成功 (备用格式)!');
      console.log(`   Photo ID: ${photoId}`);
      console.log(`   File: ${result.path}`);
      console.log(`   Size: ${(result.size / 1024 / 1024).toFixed(2)} MB`);
    } catch (error2) {
      console.error('\n❌ 下载失败');
      console.error('Error (webp):', error.message);
      console.error('Error (jpg):', error2.message);
      console.error('\n💡 提示: 请检查URL是否正确，或页面是否需要登录验证');
      process.exit(1);
    }
  }
}

main();
