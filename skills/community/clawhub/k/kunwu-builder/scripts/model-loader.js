#!/usr/bin/env node

/**
 * Kunwu Builder 批量模型加载工具
 * 
 * 使用统一的 /model/create + checkFromCloud:true 机制
 * 支持进度显示、自动重试、错误恢复
 * 
 * 用法：
 *   node scripts/model-loader.js models.json
 * 
 * models.json 格式：
 * [
 *   { "id": "M900iB_280L", "rename": "机器人_1", "position": [0, 0, 0] },
 *   { "id": "辊床_01", "position": [1000, 0, 0] }
 * ]
 */

import http from 'http';
import fs from 'fs';
import path from 'path';

// ============ 配置 ============

const BASE_URL = process.env.KUNWU_API_URL || 'http://192.168.30.9:16888';
const API_HOST = new URL(BASE_URL).hostname;
const API_PORT = parseInt(new URL(BASE_URL).port);
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 1000;

// ============ 工具函数 ============

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function log(msg, type = 'info') {
  const timestamp = new Date().toLocaleTimeString('zh-CN');
  const icons = { info: 'ℹ️', success: '✅', error: '❌', warn: '⚠️', progress: '📊' };
  console.log(`${icons[type] || 'ℹ️'} [${timestamp}] ${msg}`);
}

// ============ API 调用 ============

async function callAPI(endpoint, data) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, BASE_URL);
    const body = JSON.stringify(data);
    
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => { responseData += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(responseData);
          if (result.code === 200 || result.code === 202) {
            resolve(result);
          } else {
            reject(new Error(`API Error ${result.code}: ${result.msg}`));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`Connection error: ${e.message}`));
    });

    req.write(body);
    req.end();
  });
}

async function callAPIWithRetry(endpoint, data, retries = MAX_RETRIES) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      return await callAPI(endpoint, data);
    } catch (error) {
      if (attempt === retries) throw error;
      log(`API 调用失败 (${endpoint})，第${attempt}次重试...`, 'warn');
      await sleep(RETRY_DELAY_MS * attempt);
    }
  }
}

// ============ 核心功能 ============

/**
 * 加载单个模型（使用 /model/create + checkFromCloud:true）
 */
async function loadModel(modelConfig) {
  const { id, rename, position, eulerAngle } = modelConfig;
  
  log(`加载模型：${id}${rename ? ` → ${rename}` : ''}`, 'info');
  
  const result = await callAPIWithRetry('/model/create', {
    id,
    rename,
    position: position || [0, 0, 0],
    eulerAngle: eulerAngle || [0, 0, 0],
    checkFromCloud: true, // 关键：本地有则快，没有自动下载
  });
  
  log(`✓ ${id} 加载成功`, 'success');
  return { success: true, modelId: result.data?.modelId, config: modelConfig };
}

/**
 * 批量加载模型（带进度显示）
 */
async function loadModels(models) {
  const total = models.length;
  const results = [];
  const failures = [];
  
  log(`开始批量加载 ${total} 个模型...`, 'progress');
  console.log('━'.repeat(50));
  
  for (let i = 0; i < total; i++) {
    const model = models[i];
    const progress = `${i + 1}/${total}`;
    
    try {
      const result = await loadModel(model);
      results.push(result);
      log(`进度：${progress} - 成功`, 'progress');
    } catch (error) {
      const failure = { success: false, error: error.message, config: model };
      failures.push(failure);
      log(`进度：${progress} - 失败：${error.message}`, 'error');
    }
    
    // 每个模型之间延迟 500ms，避免 API 过载
    if (i < total - 1) {
      await sleep(500);
    }
  }
  
  console.log('━'.repeat(50));
  
  // 输出统计
  log(`加载完成：成功 ${results.length}/${total}, 失败 ${failures.length}/${total}`, results.length === total ? 'success' : 'warn');
  
  if (failures.length > 0) {
    log('失败列表:', 'warn');
    failures.forEach(f => log(`  - ${f.config.id}: ${f.error}`, 'error'));
  }
  
  return { results, failures, total };
}

/**
 * 从 JSON 文件加载模型列表
 */
function loadModelsFromFile(filePath) {
  const absolutePath = path.isAbsolute(filePath) ? filePath : path.join(process.cwd(), filePath);
  
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`文件不存在：${absolutePath}`);
  }
  
  const content = fs.readFileSync(absolutePath, 'utf-8');
  const models = JSON.parse(content);
  
  if (!Array.isArray(models)) {
    throw new Error('JSON 文件必须包含模型数组');
  }
  
  // 验证每个模型配置
  models.forEach((model, index) => {
    if (!model.id) {
      throw new Error(`模型 ${index} 缺少必需字段：id`);
    }
  });
  
  return models;
}

// ============ 命令行入口 ============

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
用法：node scripts/model-loader.js <models.json>

示例：
  node scripts/model-loader.js models.json
  node scripts/model-loader.js ./configs/robots.json

models.json 格式：
[
  { "id": "M900iB_280L", "rename": "机器人_1", "position": [0, 2500, 515] },
  { "id": "辊床_01", "position": [0, 0, 0] }
]

环境变量：
  KUNWU_API_URL - API 地址（默认：http://192.168.30.9:16888）
`);
    process.exit(1);
  }
  
  const filePath = args[0];
  
  try {
    log(`读取配置文件：${filePath}`, 'info');
    const models = loadModelsFromFile(filePath);
    log(`找到 ${models.length} 个模型`, 'info');
    
    const stats = await loadModels(models);
    
    // 如果有失败，退出码设为 1
    if (stats.failures.length > 0) {
      process.exit(1);
    }
  } catch (error) {
    log(`错误：${error.message}`, 'error');
    process.exit(1);
  }
}

// 导出供其他模块使用
export { loadModel, loadModels, loadModelsFromFile };

// 命令行执行
if (process.argv[1]?.includes('model-loader.js')) {
  main();
}
