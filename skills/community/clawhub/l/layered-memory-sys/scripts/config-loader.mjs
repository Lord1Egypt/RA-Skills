// config-loader.mjs - 路径配置化加载器
// 支持环境变量覆盖 + 默认值

import path from 'path';
import fs from 'fs';

const WORKSPACE = process.env.MEMORY_WORKSPACE || path.resolve(import.meta.dirname, '..');
const HOME = process.env.HOME || '/root';

function resolveEnvVars(str) {
  return str
    .replace(/\$\{WORKSPACE\}/g, WORKSPACE)
    .replace(/\$\{HOME\}/g, HOME)
    .replace(/\$\{MEMORY_DIR\}/g, process.env.MEMORY_DIR || path.join(WORKSPACE, 'memory'))
    .replace(/\$\{SESSION_DIR\}/g, process.env.SESSION_DIR || path.join(HOME, '.openclaw/agents/main/sessions'));
}

function loadConfig(configPath) {
  const cfgPath = configPath || path.join(WORKSPACE, 'memory', 'config.json');
  
  if (!fs.existsSync(cfgPath)) {
    console.warn(`⚠️ 配置文件不存在: ${cfgPath}，使用默认配置`);
    return getDefaultConfig();
  }
  
  const raw = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
  
  // 解析路径中的环境变量
  if (raw.paths) {
    for (const [key, val] of Object.entries(raw.paths)) {
      raw.paths[key] = resolveEnvVars(val);
    }
  }
  
  return raw;
}

function getDefaultConfig() {
  return {
    version: '1.1.0',
    paths: {
      memoryDir: path.join(WORKSPACE, 'memory'),
      sessionDir: path.join(HOME, '.openclaw/agents/main/sessions'),
      indexFile: 'index.json',
      dreamLog: 'dream-log.md',
      archiveFile: 'archive.md',
      statsDir: 'stats',
    },
    embedding: {
      provider: 'local',
      model: 'all-MiniLM-L6-v2',
      fallback: 'tfidf',
    },
    autoWrite: {
      enabled: true,
      rules: {
        turnsThreshold: 10,
        rememberKeywords: ['记住', '记住这个', '别忘了', '记下来'],
        longReplyThreshold: 2000,
        taskCompletePatterns: ['完成了', '搞定了', '已经', '成功'],
      },
    },
    stats: {
      enabled: true,
      outputFormat: 'html',
    },
  };
}

// 快捷获取路径
export function getPath(name, config) {
  const cfg = config || loadConfig();
  const paths = cfg.paths;
  
  switch (name) {
    case 'memoryDir': return paths.memoryDir;
    case 'sessionDir': return paths.sessionDir;
    case 'indexFile': return path.join(paths.memoryDir, paths.indexFile);
    case 'dreamLog': return path.join(paths.memoryDir, paths.dreamLog);
    case 'archiveFile': return path.join(paths.memoryDir, paths.archiveFile);
    case 'statsDir': return path.join(paths.memoryDir, paths.statsDir);
    case 'vectorIndex': return path.join(paths.memoryDir, '.vector');
    default: return paths[name];
  }
}

export { loadConfig, resolveEnvVars };
