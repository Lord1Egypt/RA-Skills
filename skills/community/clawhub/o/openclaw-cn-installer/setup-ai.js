#!/usr/bin/env node
/**
 * OpenClaw CN Installer - AI Model Setup
 * 配置国产 AI 模型（DeepSeek/智谱/通义千问）
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const openclawDir = path.join(os.homedir(), '.openclaw');
const envFile = path.join(openclawDir, '.env');
const configFile = path.join(openclawDir, 'config.json');

const MODELS = {
  deepseek: {
    name: 'DeepSeek V3',
    envKey: 'DEEPSEEK_API_KEY',
    envUrl: 'https://api.deepseek.com',
    model: 'deepseek-chat',
    price: '¥0.27/M tokens (输入)',
    getUrl: 'https://platform.deepseek.com',
  },
  zhipu: {
    name: '智谱 GLM-4',
    envKey: 'ZHIPU_API_KEY',
    envUrl: 'https://open.bigmodel.cn/api/paas/v4',
    model: 'glm-4',
    price: '¥0.1/M tokens',
    getUrl: 'https://open.bigmodel.cn',
  },
  qwen: {
    name: '阿里通义千问',
    envKey: 'DASHSCOPE_API_KEY',
    envUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    model: 'qwen-plus',
    price: '¥0.3/M tokens',
    getUrl: 'https://dashscope.console.aliyun.com',
  },
};

function ensureDir() {
  if (!fs.existsSync(openclawDir)) {
    fs.mkdirSync(openclawDir, { recursive: true });
    console.log('📁 创建配置目录:', openclawDir);
  }
}

function loadEnv() {
  if (fs.existsSync(envFile)) {
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
  return {};
}

function saveEnv(env) {
  const content = Object.entries(env)
    .map(([k, v]) => `${k}=${v}`)
    .join('\n');
  fs.writeFileSync(envFile, content + '\n');
  console.log('💾 保存配置:', envFile);
}

function updateConfig(model, modelId) {
  const config = fs.existsSync(configFile)
    ? JSON.parse(fs.readFileSync(configFile, 'utf-8'))
    : {};

  config.model = config.model || {};
  config.model.provider = model;
  config.model.model = modelId;

  fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
  console.log('⚙️  更新主配置:', configFile);
}

async function prompt(rl, question) {
  return new Promise(resolve => {
    rl.question(question, answer => {
      resolve(answer.trim());
    });
  });
}

async function setupModel(modelKey) {
  const model = MODELS[modelKey];
  if (!model) {
    console.error('❌ 未知模型:', modelKey);
    console.log('支持的模型:', Object.keys(MODELS).join(', '));
    process.exit(1);
  }

  console.log(`\n🤖 配置 ${model.name}\n`);
  console.log(`   价格: ${model.price}`);
  console.log(`   获取 API Key: ${model.getUrl}\n`);

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  try {
    const apiKey = await prompt(rl, `请输入 ${model.envKey}: `);

    if (!apiKey) {
      console.log('⚠️  跳过配置（未输入 API Key）');
      return false;
    }

    // 保存到 .env
    const env = loadEnv();
    env[model.envKey] = apiKey;
    saveEnv(env);

    // 更新 config.json
    updateConfig(modelKey, model.model);

    console.log(`\n✅ ${model.name} 配置完成！\n`);
    return true;
  } finally {
    rl.close();
  }
}

async function main() {
  const args = process.argv.slice(2);
  const target = args[0] || 'help';

  ensureDir();

  if (target === 'help' || target === '--help' || target === '-h') {
    console.log(`
用法: node setup-ai.js <model>

支持的模型:
  deepseek  - DeepSeek V3 (推荐，性价比最高)
  zhipu     - 智谱 GLM-4 (中文能力强)
  qwen      - 阿里通义千问 (多模态)
  all       - 配置全部模型

示例:
  node setup-ai.js deepseek
  node setup-ai.js all
`);
    return;
  }

  if (target === 'all') {
    for (const key of Object.keys(MODELS)) {
      await setupModel(key);
    }
  } else {
    await setupModel(target);
  }

  console.log('📖 下一步:');
  console.log('   1. 运行 node test-connection.js 测试连接');
  console.log('   2. 运行 openclaw run 启动 OpenClaw\n');
}

main().catch(console.error);