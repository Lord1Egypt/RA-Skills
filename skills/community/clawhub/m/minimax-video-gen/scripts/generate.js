#!/usr/bin/env node
/**
 * MiniMax 视频生成脚本
 * 支持首尾帧模式(fl2v)和文生视频模式(t2v)
 * 
 * 用法:
 *   node generate.js --mode fl2v --first-frame <url> --last-frame <url> --prompt <text> [--model MiniMax-Hailuo-02] [--duration 6] [--resolution 1080P]
 *   node generate.js --mode t2v --prompt <text> [--model MiniMax-Hailuo-2.3] [--duration 6] [--resolution 1080P]
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
    mode: 'fl2v', // 默认首尾帧模式
    prompt: '',
    firstFrame: '',
    lastFrame: '',
    model: 'MiniMax-Hailuo-02',
    duration: 6,
    resolution: '1080P'
  };

  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    switch (argv[i]) {
      case '--mode':
        args.mode = argv[++i];
        break;
      case '--first-frame':
        args.firstFrame = argv[++i];
        break;
      case '--last-frame':
        args.lastFrame = argv[++i];
        break;
      case '--prompt':
        args.prompt = argv[++i];
        break;
      case '--model':
        args.model = argv[++i];
        break;
      case '--duration':
        args.duration = parseInt(argv[++i]) || 6;
        break;
      case '--resolution':
        args.resolution = argv[++i];
        break;
    }
  }
  return args;
}

// 发送 POST 请求
function httpPost(url, payload, apiKey) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
    req.write(JSON.stringify(payload));
    req.end();
  });
}

// 生成视频
async function generateVideo(args) {
  const apiKey = getApiKey();
  const url = 'https://api.minimaxi.com/v1/video_generation';
  
  const payload = {
    prompt: args.prompt,
    model: args.model,
    duration: args.duration,
    resolution: args.resolution
  };

  // 首尾帧模式
  if (args.mode === 'fl2v') {
    payload.first_frame_image = args.firstFrame;
    payload.last_frame_image = args.lastFrame;
  }

  console.log('📹 开始生成视频...');
  console.log('参数:', JSON.stringify(payload, null, 2));

  const result = await httpPost(url, payload, apiKey);
  
  if (result.task_id) {
    console.log('✅ 任务创建成功!');
    console.log('Task ID:', result.task_id);
    console.log('\n查询命令:');
    console.log(`  node scripts/query.js --task-id ${result.task_id}`);
    return result.task_id;
  } else {
    console.error('❌ 任务创建失败:', result);
    process.exit(1);
  }
}

// 主函数
async function main() {
  const args = parseArgs();
  
  if (!args.prompt) {
    console.error('❌ 请提供 --prompt 参数');
    process.exit(1);
  }
  
  if (args.mode === 'fl2v' && (!args.firstFrame || !args.lastFrame)) {
    console.error('❌ 首尾帧模式需要提供 --first-frame 和 --last-frame 参数');
    process.exit(1);
  }

  await generateVideo(args);
}

main().catch(console.error);
