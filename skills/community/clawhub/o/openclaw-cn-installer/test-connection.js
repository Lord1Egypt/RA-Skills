#!/usr/bin/env node
/**
 * OpenClaw CN Installer - Connection Tester
 * 测试 AI 模型 API 连接是否正常
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

const openclawDir = path.join(os.homedir(), '.openclaw');
const envFile = path.join(openclawDir, '.env');

const API_ENDPOINTS = {
  DEEPSEEK_API_KEY: {
    name: 'DeepSeek',
    url: 'api.deepseek.com',
    path: '/v1/chat/completions',
    model: 'deepseek-chat',
  },
  ZHIPU_API_KEY: {
    name: '智谱 GLM',
    url: 'open.bigmodel.cn',
    path: '/api/paas/v4/chat/completions',
    model: 'glm-4-flash',
  },
  DASHSCOPE_API_KEY: {
    name: '通义千问',
    url: 'dashscope.aliyuncs.com',
    path: '/compatible-mode/v1/chat/completions',
    model: 'qwen-turbo',
  },
};

function loadEnv() {
  if (!fs.existsSync(envFile)) {
    return {};
  }
  const content = fs.readFileSync(envFile, 'utf-8');
  const env = {};
  content.split('\n').forEach(line => {
    const [key, ...rest] = line.split('=');
    if (key && rest.length) {
      env[key.trim()] = rest.join('=').trim();
    }
  });
  return env;
}

function testAPI(name, apiKey, config) {
  return new Promise((resolve) => {
    const startTime = Date.now();

    const data = JSON.stringify({
      model: config.model,
      messages: [{ role: 'user', content: 'Hi' }],
      max_tokens: 5,
    });

    const options = {
      hostname: config.url,
      port: 443,
      path: config.path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(data),
      },
      timeout: 10000,
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        const latency = Date.now() - startTime;
        if (res.statusCode === 200) {
          console.log(`${GREEN}✅ ${name} API: 连接成功 (${latency}ms)${RESET}`);
          resolve(true);
        } else if (res.statusCode === 401) {
          console.log(`${RED}❌ ${name} API: API Key 无效${RESET}`);
          resolve(false);
        } else if (res.statusCode === 429) {
          console.log(`${YELLOW}⚠️  ${name} API: 请求频率限制 (但连接正常)${RESET}`);
          resolve(true);
        } else {
          console.log(`${RED}❌ ${name} API: HTTP ${res.statusCode}${RESET}`);
          resolve(false);
        }
      });
    });

    req.on('error', (e) => {
      console.log(`${RED}❌ ${name} API: ${e.message}${RESET}`);
      resolve(false);
    });

    req.on('timeout', () => {
      req.destroy();
      console.log(`${RED}❌ ${name} API: 超时${RESET}`);
      resolve(false);
    });

    req.write(data);
    req.end();
  });
}

async function main() {
  console.log('\n🔌 测试 AI 模型连接\n');
  console.log('─'.repeat(50));

  const env = loadEnv();

  if (Object.keys(env).length === 0) {
    console.log(`${YELLOW}⚠️  未找到配置文件${RESET}`);
    console.log('请先运行: node setup-ai.js deepseek\n');
    return;
  }

  const results = [];

  for (const [key, config] of Object.entries(API_ENDPOINTS)) {
    const apiKey = env[key];
    if (apiKey) {
      const success = await testAPI(config.name, apiKey, config);
      results.push({ name: config.name, success });
    }
  }

  if (results.length === 0) {
    console.log(`${YELLOW}⚠️  未配置任何 AI 模型${RESET}`);
    console.log('请运行: node setup-ai.js <model>\n');
    return;
  }

  console.log('─'.repeat(50));

  const passCount = results.filter(r => r.success).length;
  console.log(`\n📊 测试结果: ${passCount}/${results.length} 连接成功\n`);

  if (passCount === results.length) {
    console.log(`${GREEN}✨ 所有模型连接正常，可以开始使用！${RESET}`);
    console.log('启动 OpenClaw: openclaw run\n');
  }
}

main().catch(console.error);