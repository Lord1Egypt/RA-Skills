#!/usr/bin/env node
/**
 * MiniMax 视频下载脚本
 * 
 * 用法:
 *   node download.js --file-id <file_id> --output <path>
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 读取 API Key
function getApiKey() {
  const configPath = path.join(process.env.HOME || '/Users/js', '.openclaw/openclaw.json');
  try {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    // 支持多种配置路径
    return config?.models?.providers?.['minimax-cn']?.apiKey
        || config['minimax-cn']?.apiKey 
        || config?.providers?.['minimax-cn']?.apiKey;
  } catch (e) {
    console.error('无法读取配置文件:', e.message);
    process.exit(1);
  }
}

// 解析命令行参数
function parseArgs() {
  const args = {
    fileId: '',
    output: './output.mp4'
  };
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--file-id') {
      args.fileId = argv[++i];
    } else if (argv[i] === '--output') {
      args.output = argv[++i];
    }
  }
  return args;
}

// 发送 GET 请求
function httpGet(url, apiKey) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

// 下载文件
function downloadFile(url, outputPath) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const file = fs.createWriteStream(outputPath);
    
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method: 'GET'
    };

    console.log(`📥 开始下载: ${outputPath}`);
    
    const req = https.request(options, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        // 重定向，递归下载
        file.close();
        downloadFile(res.headers.location, outputPath).then(resolve).catch(reject);
        return;
      }
      
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        const stats = fs.statSync(outputPath);
        console.log(`✅ 下载完成! 大小: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
        resolve();
      });
    });

    req.on('error', (e) => {
      file.close();
      fs.unlink(outputPath, () => {});
      reject(e);
    });

    req.end();
  });
}

// 获取下载链接并下载
async function downloadVideo(fileId, outputPath) {
  const apiKey = getApiKey();
  
  // 确保输出目录存在
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // 先获取下载链接
  console.log(`🔍 获取文件 ${fileId} 的下载链接...`);
  const url = `https://api.minimaxi.com/v1/files/retrieve?file_id=${fileId}`;
  const result = await httpGet(url, apiKey);
  
  if (result.file?.download_url) {
    console.log('📎 获取到下载链接，准备下载...');
    await downloadFile(result.file.download_url, outputPath);
    return result.file;
  } else {
    console.error('❌ 获取下载链接失败:', result);
    process.exit(1);
  }
}

// 主函数
async function main() {
  const args = parseArgs();
  
  if (!args.fileId) {
    console.error('❌ 请提供 --file-id 参数');
    console.error('用法: node download.js --file-id <file_id> --output <path>');
    process.exit(1);
  }

  await downloadVideo(args.fileId, args.output);
}

main().catch(console.error);
