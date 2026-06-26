#!/usr/bin/env node
/**
 * MiniMax 视频生成任务状态查询脚本
 * 
 * 用法:
 *   node query.js --task-id <task_id>
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
  const args = {};
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--task-id') {
      args.taskId = argv[++i];
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

// 查询任务状态
async function queryTask(taskId) {
  const apiKey = getApiKey();
  const url = `https://api.minimaxi.com/v1/query/video_generation?task_id=${taskId}`;

  console.log(`🔍 查询任务状态: ${taskId}`);
  
  const result = await httpGet(url, apiKey);
  
  if (result.base_resp?.status_code === 0 || result.status) {
    const status = result.status;
    const statusEmoji = {
      'Preparing': '⏳',
      'Queueing': '⏳',
      'Processing': '🔄',
      'Success': '✅',
      'Fail': '❌'
    };
    
    console.log(`\n状态: ${statusEmoji[status] || '❓'} ${status}`);
    
    if (status === 'Success') {
      console.log(`📁 文件ID: ${result.file_id}`);
      console.log(`📐 分辨率: ${result.video_width}x${result.video_height}`);
      console.log(`\n下载命令:`);
      console.log(`  node scripts/download.js --file-id ${result.file_id} --output ./output.mp4`);
    } else if (status === 'Fail') {
      console.error('❌ 任务失败:', result.base_resp?.status_msg);
    }
    
    return result;
  } else {
    console.error('❌ 查询失败:', result);
    process.exit(1);
  }
}

// 主函数
async function main() {
  const args = parseArgs();
  
  if (!args.taskId) {
    console.error('❌ 请提供 --task-id 参数');
    console.error('用法: node query.js --task-id <task_id>');
    process.exit(1);
  }

  await queryTask(args.taskId);
}

main().catch(console.error);
