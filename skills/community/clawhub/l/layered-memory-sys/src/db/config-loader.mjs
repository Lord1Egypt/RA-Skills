// config-loader.mjs - 配置加载器 (v2.0)
// 支持环境变量 + 配置文件 + 默认值

import fs from 'fs';
import path from 'path';

const DEFAULT_CONFIG = {
  memoryDir: '~/.openclaw/workspace/memory',
  indexFile: '~/.openclaw/workspace/memory/index.json',
  archiveFile: '~/.openclaw/workspace/memory/archive.md',
  sessionDir: '~/.openclaw/agents/main/sessions',
  dreamLogFile: '~/.openclaw/workspace/memory/dream-log.md',
  dbFile: '~/.openclaw/workspace/memory/memory.db',
  embedding: {
    mode: 'auto',  // auto/local/api
    localModel: 'Xenova/paraphrase-multilingual-MiniLM-L12-v2',
    apiProvider: 'doubao',
    apiKey: '',    // 或从环境变量 DOUBAO_API_KEY 读取
  },
  tokenizer: {
    mode: 'auto',  // auto/jieba/ngram
    ngramSize: 3,
  },
  scheduler: {
    enabled: true,
    jobs: [
      { id: 'dream-cycle', cron: '0 3 * * *', handler: 'dreamCycle' },
      { id: 'remind-check', cron: '* * * * *', handler: 'checkReminders' },
    ],
  },
  layers: {
    flash: { ttl: 3 },
    active: { ttl: 7 },
    attention: { ttl: 30 },
    settled: { ttl: 90 },
  },
};

let _config = null;

export function loadConfig(customPath) {
  if (_config) return _config;

  const config = { ...DEFAULT_CONFIG };

  // 1. 从文件加载
  const configPaths = [
    customPath,
    path.join(getWorkspaceDir(), 'memory', 'config.json'),
    path.join(getWorkspaceDir(), 'skills', 'layered-memory-sys', 'assets', 'config.json'),
  ].filter(Boolean);

  for (const p of configPaths) {
    if (fs.existsSync(p)) {
      try {
        const fileConfig = JSON.parse(fs.readFileSync(p, 'utf-8'));
        deepMerge(config, fileConfig);
        break;
      } catch (e) {
        console.warn(`配置加载失败 (${p}): ${e.message}，使用默认值`);
      }
    }
  }

  // 2. 环境变量覆盖
  config.embedding.apiKey = process.env.DOUBAO_API_KEY || config.embedding.apiKey;
  config.embedding.apiKey = process.env.DASHSCOPE_API_KEY || config.embedding.apiKey;
  if (process.env.MEMORY_DIR) config.memoryDir = process.env.MEMORY_DIR;
  if (process.env.SESSION_DIR) config.sessionDir = process.env.SESSION_DIR;

  _config = config;
  return config;
}

// 获取路径（支持 ~ 展开）
export function getPath(key, config) {
  config = config || loadConfig();
  const raw = config[key] || DEFAULT_CONFIG[key];
  if (!raw) return null;
  return raw.replace(/^~/, process.env.HOME || '/root');
}

// 深度合并
function deepMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      target[key] = target[key] || {};
      deepMerge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
}

function getWorkspaceDir() {
  return process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || '/root', '.openclaw', 'workspace');
}

export function getDefaultConfig() {
  return { ...DEFAULT_CONFIG };
}