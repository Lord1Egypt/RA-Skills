#!/usr/bin/env node
/**
 * LLM 客户端 - 安全的模型调用工具
 * 
 * 配置来源（按优先级）：
 * 1. 环境变量（OPENCLAW_*, LLM_*, ANTHROPIC_*）- 云环境首选，最高优先级
 * 2. OpenClaw 运行时 API（云环境动态获取）- 云环境标准方式
 * 3. 内存缓存（进程内缓存解密后的明文配置）
 * 4. 技能缓存（references/settings.json 中的 llmCache 字段，加密存储）
 * 5. OpenClaw 配置（~/.openclaw/openclaw.json 中的 models.providers）- 本地环境回退
 * 
 * 安全机制：
 * - settings.json 中存储加密后的配置（密文）
 * - 环境变量存储明文（进程内可用）
 * - 内存缓存明文配置，避免重复解密
 * - 使用 Node.js 内置 crypto 模块进行 AES-256-CBC 加密
 * - 云环境通过运行时 API 动态获取配置，无需本地文件
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 加密密钥（使用环境变量或默认密钥，生产环境应使用环境变量）
const ENCRYPTION_KEY = process.env.LLM_ENCRYPTION_KEY || 'license-pre-audit-default-key-32bytes!';
const IV_LENGTH = 16; // AES block size
const ALGORITHM = 'aes-256-cbc';

// 配置文件路径
const SETTINGS_FILE = path.join(__dirname, '..', '..', 'references', 'settings.json');

// 内存缓存（进程内缓存明文配置）
let memoryCache = null;
let configSource = '未知';
let configInitialized = false;

/**
 * 加密数据
 * @param {string} text - 明文
 * @returns {string} 加密后的字符串 (iv:ciphertext)
 */
function encrypt(text) {
  try {
    const key = Buffer.from(ENCRYPTION_KEY.padEnd(32, ' ').substring(0, 32));
    const iv = crypto.randomBytes(IV_LENGTH);
    const cipher = crypto.createCipheriv(ALGORITHM, key, iv);

    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    return iv.toString('hex') + ':' + encrypted;
  } catch (error) {
    console.error('✗ 加密失败:', error.message);
    return text; // 加密失败时返回原文
  }
}

/**
 * 解密数据
 * @param {string} encryptedText - 加密字符串 (iv:ciphertext)
 * @returns {string} 明文
 */
function decrypt(encryptedText) {
  try {
    if (!encryptedText || !encryptedText.includes(':')) {
      return encryptedText; // 不是加密格式，返回原文
    }

    const parts = encryptedText.split(':');
    const iv = Buffer.from(parts[0], 'hex');
    const encrypted = parts[1];

    const key = Buffer.from(ENCRYPTION_KEY.padEnd(32, ' ').substring(0, 32));
    const decipher = crypto.createDecipheriv(ALGORITHM, key, iv);

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  } catch (error) {
    console.error('✗ 解密失败:', error.message);
    return encryptedText; // 解密失败时返回原文
  }
}

/**
 * 读取缓存的配置（从 settings.json 的 llmCache 字段，解密后返回）
 * @returns {Object|null} 解密后的配置或 null
 */
function readCache() {
  if (!fs.existsSync(SETTINGS_FILE)) {
    return null;
  }

  try {
    const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
    const cacheData = settings.llmCache;

    if (!cacheData || !cacheData.encryptedConfig) {
      return null;
    }

    // 检查缓存是否有效（24 小时有效）
    const now = Date.now();
    const cacheAge = now - (cacheData.timestamp || 0);
    const maxAge = 24 * 60 * 60 * 1000; // 24 小时

    if (cacheAge > maxAge) {
      // 缓存过期，删除
      delete settings.llmCache;
      fs.writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2), 'utf8');
      return null;
    }

    // 解密配置
    const decryptedJson = decrypt(cacheData.encryptedConfig);
    return JSON.parse(decryptedJson);
  } catch (error) {
    return null;
  }
}

/**
 * 写入缓存的配置（加密后存储到 settings.json 的 llmCache 字段）
 * @param {Object} config - 明文配置对象
 */
function writeCache(config) {
  try {
    let settings = {};

    if (fs.existsSync(SETTINGS_FILE)) {
      settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
    }

    // 将配置转换为 JSON 字符串并加密
    const configJson = JSON.stringify(config);
    const encryptedConfig = encrypt(configJson);

    settings.llmCache = {
      timestamp: Date.now(),
      encryptedConfig: encryptedConfig
    };

    fs.writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2), 'utf8');
  } catch (error) {
    console.error('⚠ 写入缓存失败:', error.message);
  }
}

/**
 * 从 OpenClaw 运行时 API 动态获取模型配置（云环境）
 * @returns {Promise<Object|null>} { apiBase, apiKey, model } 或 null
 */
async function getRuntimeModelConfig() {
  // 检查是否在 OpenClaw 运行时环境中
  const runtimeToken = process.env.OPENCLAW_RUNTIME_TOKEN || 
                       process.env.OPENCLAW_API_TOKEN ||
                       process.env.CLAUDIA_RUNTIME_TOKEN;
  
  const runtimeApiBase = process.env.OPENCLAW_RUNTIME_API ||
                         'http://localhost:3000/api'; // 默认运行时 API 地址
  
  if (!runtimeToken) {
    return null; // 没有运行时令牌，跳过
  }
  
  try {
    console.error('🌐 尝试从 OpenClaw 运行时 API 获取配置...');
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 秒超时
    
    const response = await fetch(`${runtimeApiBase}/config/models`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${runtimeToken}`,
        'Content-Type': 'application/json'
      },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      console.error('✗ 运行时 API 返回错误:', response.status, response.statusText);
      return null;
    }
    
    const data = await response.json();
    
    // 解析配置
    if (data.models && data.models.providers) {
      const providers = data.models.providers;
      const providerNames = Object.keys(providers);
      
      if (providerNames.length === 0) {
        return null;
      }
      
      // 使用第一个可用的 provider 或指定模型
      const preferredModel = process.env.OPENCLAW_MODEL || 
                            process.env.LLM_MODEL ||
                            process.env.ANTHROPIC_MODEL;
      
      let providerName = providerNames[0];
      let modelId = providers[providerName].models?.[0]?.id;
      
      if (preferredModel) {
        // 查找包含指定模型的 provider
        for (const [name, provider] of Object.entries(providers)) {
          if (provider.models && provider.models.some(m => m.id === preferredModel)) {
            providerName = name;
            modelId = preferredModel;
            break;
          }
        }
      }
      
      const provider = providers[providerName];
      
      console.error('✅ 从运行时 API 获取配置成功');
      console.error(`   模型：${modelId}`);
      console.error(`   地址：${provider.baseUrl || provider.apiBase}`);
      
      return {
        apiBase: provider.baseUrl || provider.apiBase,
        apiKey: provider.apiKey,
        model: modelId
      };
    }
    
    return null;
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('✗ 运行时 API 请求超时');
    } else {
      console.error('✗ 从运行时 API 获取配置失败:', error.message);
    }
    return null;
  }
}

/**
 * 从 OpenClaw 配置中读取模型配置（本地环境回退）
 * @param {string} modelName - 模型名称（可选，默认为第一个可用模型）
 * @returns {Object|null} { apiBase, apiKey, model } 或 null
 */
function getOpenClawModelConfig(modelName) {
  const openclawConfigPath = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'openclaw.json');

  if (!fs.existsSync(openclawConfigPath)) {
    return null;
  }

  try {
    const config = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf8'));
    const providers = config.models?.providers;

    if (!providers || Object.keys(providers).length === 0) {
      return null;
    }

    // 查找指定的模型或第一个可用模型
    let providerName = null;
    let modelId = modelName;

    if (modelName) {
      // 查找包含该模型的 provider
      for (const [name, provider] of Object.entries(providers)) {
        if (provider.models && provider.models.some(m => m.id === modelName)) {
          providerName = name;
          break;
        }
      }
    } else {
      // 使用第一个 provider
      providerName = Object.keys(providers)[0];
      if (providerName && providers[providerName].models && providers[providerName].models.length > 0) {
        modelId = providers[providerName].models[0].id;
      }
    }

    if (!providerName) {
      return null;
    }

    const provider = providers[providerName];

    return {
      apiBase: provider.baseUrl,
      apiKey: provider.apiKey,
      model: modelId || provider.models?.[0]?.id
    };
  } catch (error) {
    console.error('✗ 读取 OpenClaw 配置失败:', error.message);
    return null;
  }
}

/**
 * 初始化配置（异步）
 * 按优先级加载配置：环境变量 > 运行时 API > 内存缓存 > 加密缓存 > openclaw.json
 */
async function initConfig() {
  if (configInitialized) {
    return;
  }
  
  configInitialized = true;
  
  // 优先级 1: 环境变量（最高优先级）
  if (process.env.LLM_API_KEY || process.env.OPENCLAW_API_KEY || process.env.ANTHROPIC_API_KEY) {
    // 标准化环境变量
    process.env.LLM_API_BASE = process.env.LLM_API_BASE || 
                               process.env.OPENCLAW_BASE_URL ||
                               process.env.ANTHROPIC_BASE_URL;
    process.env.LLM_API_KEY = process.env.LLM_API_KEY || 
                              process.env.OPENCLAW_API_KEY ||
                              process.env.ANTHROPIC_API_KEY;
    process.env.LLM_MODEL = process.env.LLM_MODEL || 
                            process.env.OPENCLAW_MODEL ||
                            process.env.ANTHROPIC_MODEL;
    configSource = '环境变量';
    return;
  }
  
  // 优先级 2: 内存缓存
  if (memoryCache) {
    process.env.LLM_API_BASE = memoryCache.apiBase;
    process.env.LLM_API_KEY = memoryCache.apiKey;
    process.env.LLM_MODEL = memoryCache.model;
    configSource = '内存缓存';
    return;
  }
  
  // 优先级 3: 加密缓存
  const encryptedCache = readCache();
  if (encryptedCache) {
    process.env.LLM_API_BASE = encryptedCache.apiBase;
    process.env.LLM_API_KEY = encryptedCache.apiKey;
    process.env.LLM_MODEL = encryptedCache.model;
    memoryCache = encryptedCache;
    configSource = '加密缓存 (已解密)';
    return;
  }
  
  // 优先级 4: OpenClaw 运行时 API（云环境）
  const runtimeConfig = await getRuntimeModelConfig();
  if (runtimeConfig) {
    writeCache(runtimeConfig);
    process.env.LLM_API_BASE = runtimeConfig.apiBase;
    process.env.LLM_API_KEY = runtimeConfig.apiKey;
    process.env.LLM_MODEL = runtimeConfig.model;
    memoryCache = runtimeConfig;
    configSource = '运行时 API (已加密缓存)';
    return;
  }
  
  // 优先级 5: OpenClaw 配置（本地环境回退）
  const openClawConfig = getOpenClawModelConfig(process.env.LLM_MODEL);
  if (openClawConfig) {
    writeCache(openClawConfig);
    process.env.LLM_API_BASE = openClawConfig.apiBase;
    process.env.LLM_API_KEY = openClawConfig.apiKey;
    process.env.LLM_MODEL = openClawConfig.model;
    memoryCache = openClawConfig;
    configSource = 'OpenClaw 配置 (已加密缓存)';
    return;
  }
  
  // 所有来源都失败
  console.error('⚠  未找到 LLM 配置，请检查：');
  console.error('  1. 环境变量：OPENCLAW_API_KEY, LLM_API_KEY, ANTHROPIC_API_KEY');
  console.error('  2. 云环境运行时令牌：OPENCLAW_RUNTIME_TOKEN');
  console.error('  3. 本地配置：~/.openclaw/openclaw.json');
}

// 同步初始化配置（用于向后兼容）
function initConfigSync() {
  // 尝试从环境变量读取
  if (process.env.LLM_API_KEY || process.env.OPENCLAW_API_KEY || process.env.ANTHROPIC_API_KEY) {
    process.env.LLM_API_BASE = process.env.LLM_API_BASE || 
                               process.env.OPENCLAW_BASE_URL ||
                               process.env.ANTHROPIC_BASE_URL;
    process.env.LLM_API_KEY = process.env.LLM_API_KEY || 
                              process.env.OPENCLAW_API_KEY ||
                              process.env.ANTHROPIC_API_KEY;
    process.env.LLM_MODEL = process.env.LLM_MODEL || 
                            process.env.OPENCLAW_MODEL ||
                            process.env.ANTHROPIC_MODEL;
    configSource = '环境变量';
    configInitialized = true;
    return;
  }
  
  // 尝试从缓存读取
  if (memoryCache) {
    process.env.LLM_API_BASE = memoryCache.apiBase;
    process.env.LLM_API_KEY = memoryCache.apiKey;
    process.env.LLM_MODEL = memoryCache.model;
    configSource = '内存缓存';
    configInitialized = true;
    return;
  }
  
  const encryptedCache = readCache();
  if (encryptedCache) {
    process.env.LLM_API_BASE = encryptedCache.apiBase;
    process.env.LLM_API_KEY = encryptedCache.apiKey;
    process.env.LLM_MODEL = encryptedCache.model;
    memoryCache = encryptedCache;
    configSource = '加密缓存 (已解密)';
    configInitialized = true;
    return;
  }
  
  // 尝试从 openclaw.json 读取
  const openClawConfig = getOpenClawModelConfig(process.env.LLM_MODEL);
  if (openClawConfig) {
    writeCache(openClawConfig);
    process.env.LLM_API_BASE = openClawConfig.apiBase;
    process.env.LLM_API_KEY = openClawConfig.apiKey;
    process.env.LLM_MODEL = openClawConfig.model;
    memoryCache = openClawConfig;
    configSource = 'OpenClaw 配置 (已加密缓存)';
    configInitialized = true;
    return;
  }
}

// 初始化配置（同步优先，异步作为补充）
initConfigSync();

const config = {
  apiBase: process.env.LLM_API_BASE,
  apiKey: process.env.LLM_API_KEY,
  model: process.env.LLM_MODEL,
  temperature: parseFloat(process.env.LLM_TEMPERATURE) || 0.1,
  maxTokens: parseInt(process.env.LLM_MAX_TOKENS) || 8192
};

/**
 * 检查配置是否完整
 * @returns {Object} { valid: boolean, missing: string[], source: string }
 */
function checkConfig() {
  const missing = [];

  if (!config.apiKey) {
    missing.push('LLM_API_KEY');
  }
  if (!config.apiBase) {
    missing.push('LLM_API_BASE');
  }
  if (!config.model) {
    missing.push('LLM_MODEL');
  }

  return {
    valid: missing.length === 0,
    missing,
    source: configSource
  };
}

/**
 * 调用 LLM 进行文本分析（异步，先尝试初始化配置）
 * @param {string} systemPrompt - 系统提示词
 * @param {string} userPrompt - 用户提示词
 * @param {Object} options - 额外选项
 * @returns {Promise<Object|null>} 解析后的 JSON 结果
 */
async function callLLM(systemPrompt, userPrompt, options = {}) {
  const { maxTextLength = 8000 } = options;
  
  // 如果配置未初始化，尝试异步初始化（云环境）
  if (!configInitialized) {
    await initConfig();
  }
  
  // 如果仍然没有 API_KEY，尝试运行时 API
  if (!process.env.LLM_API_KEY && !configInitialized) {
    const runtimeConfig = await getRuntimeModelConfig();
    if (runtimeConfig) {
      writeCache(runtimeConfig);
      process.env.LLM_API_BASE = runtimeConfig.apiBase;
      process.env.LLM_API_KEY = runtimeConfig.apiKey;
      process.env.LLM_MODEL = runtimeConfig.model;
      memoryCache = runtimeConfig;
      configSource = '运行时 API (已加密缓存)';
    }
  }

  // 检查配置
  const configCheck = checkConfig();
  if (!configCheck.valid) {
    console.error('✗ LLM 配置缺失:', configCheck.missing.join(', '));
    console.error('配置来源:', configCheck.source);
    console.error('请通过以下方式之一配置：');
    console.error('  1. 设置环境变量：export OPENCLAW_API_KEY=<你的 Key>');
    console.error('  2. 在云环境中配置运行时 API 令牌');
    console.error('  3. 在 ~/.openclaw/openclaw.json 中配置 models.providers');
    return null;
  }

  // 截断过长的文本
  const textToProcess = userPrompt.length > maxTextLength
    ? userPrompt.substring(0, maxTextLength) + '\n...（已截断）'
    : userPrompt;

  const payload = {
    model: config.model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: textToProcess }
    ],
    temperature: config.temperature,
    max_tokens: config.maxTokens
  };

  try {
    const result = spawnSync('curl', [
      '-s', '-X', 'POST',
      `${config.apiBase}/chat/completions`,
      '-H', 'Content-Type: application/json',
      '-H', `Authorization: Bearer ${config.apiKey}`,
      '-d', JSON.stringify(payload)
    ], { encoding: 'utf8' });

    if (result.status === 0) {
      const response = JSON.parse(result.stdout);
      const content = response.choices?.[0]?.message?.content;

      if (!content) {
        console.error('✗ LLM 返回空内容');
        return null;
      }

      // 提取 JSON 内容
      let jsonStr = content.trim()
        .replace(/```json\s*/g, '')
        .replace(/```\s*/g, '')
        .trim();

      const startIdx = jsonStr.indexOf('{');
      const endIdx = jsonStr.lastIndexOf('}');
      if (startIdx >= 0 && endIdx > startIdx) {
        jsonStr = jsonStr.substring(startIdx, endIdx + 1);
      }

      // 修复常见的 JSON 错误
      jsonStr = jsonStr
        .replace(/,\s*}/g, '}')
        .replace(/:\s*,/g, ': null,')
        .replace(/,\s*]/g, ']');

      return JSON.parse(jsonStr);
    } else {
      console.error('✗ LLM 调用失败:', result.stderr || result.stdout);
      return null;
    }
  } catch (error) {
    console.error('✗ LLM 调用异常:', error.message);
    return null;
  }
}

/**
 * 测试 LLM 连接
 * @returns {Promise<boolean>} 是否成功
 */
async function testConnection() {
  console.log('🧪 测试 LLM 连接...');
  
  // 尝试初始化配置
  if (!configInitialized) {
    await initConfig();
  }

  const result = await callLLM(
    '你是一个测试助手。',
    '请回复：OK',
    { maxTextLength: 100 }
  );

  if (result) {
    console.log('✓ LLM 连接成功');
    return true;
  } else {
    console.log('✗ LLM 连接失败');
    return false;
  }
}

module.exports = {
  callLLM,
  checkConfig,
  testConnection,
  config,
  readCache,
  writeCache,
  encrypt,
  decrypt,
  initConfig,
  getRuntimeModelConfig
};

// 测试模式
if (require.main === module) {
  (async () => {
    await testConnection();

    // 显示缓存信息
    console.log('\n📦 缓存信息:');
    console.log('  配置文件:', SETTINGS_FILE);

    if (fs.existsSync(SETTINGS_FILE)) {
      const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
      if (settings.llmCache) {
        const age = Date.now() - settings.llmCache.timestamp;
        const hours = Math.floor(age / (1000 * 60 * 60));
        console.log('  缓存存在：是');
        console.log('  创建时间:', new Date(settings.llmCache.timestamp).toLocaleString());
        console.log('  已存在:', hours, '小时');
        console.log('  剩余有效时间:', Math.max(0, 24 - hours), '小时');
        console.log('  加密状态:', settings.llmCache.encryptedConfig ? '加密' : '未加密');
      } else {
        console.log('  缓存存在：否');
      }
    } else {
      console.log('  配置文件不存在');
    }
    
    console.log('\n📊 当前配置:');
    console.log('  来源:', configSource);
    console.log('  模型:', config.model || '未设置');
    console.log('  API 地址:', config.apiBase || '未设置');
    console.log('  API Key:', config.apiKey ? '已设置' : '未设置');
  })();
}
