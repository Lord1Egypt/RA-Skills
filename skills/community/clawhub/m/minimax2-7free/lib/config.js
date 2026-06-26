/**
 * singularity-freemodels/lib/config.js
 * 凭证加载模块
 * 
 * 按以下顺序读取凭证：
 * 1. 环境变量
 * 2. Windows: %APPDATA%\singularity\credentials.json
 * 3. Linux/macOS: ~/.config/singularity/credentials.json
 */

const fs = require('fs');
const path = require('path');

const CONFIG_DIR = process.env.APPDATA
  ? path.join(process.env.APPDATA, 'singularity')
  : path.join(process.env.HOME || '/root', '.config', 'singularity');

const CONFIG_FILE = path.join(CONFIG_DIR, 'credentials.json');

function loadConfigFromFile() {
  if (!fs.existsSync(CONFIG_FILE)) {
    return {};
  }
  try {
    const content = fs.readFileSync(CONFIG_FILE, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    console.error(`[config] Failed to read ${CONFIG_FILE}: ${e.message}`);
    return {};
  }
}

function loadCredentials() {
  const envConfig = {
    apiKey: process.env.SINGULARITY_API_KEY,
    agentId: process.env.SINGULARITY_AGENT_ID,
    nodeSecret: process.env.SINGULARITY_NODE_SECRET,
    agentName: process.env.SINGULARITY_AGENT_NAME,
    apiBaseUrl: process.env.SINGULARITY_API_URL || 'https://www.singularity.mba',
    hubBaseUrl: process.env.SINGULARITY_HUB_BASE_URL || 'https://www.singularity.mba',
  };

  const fileConfig = loadConfigFromFile();

  // 文件配置支持 camelCase 和 snake_case
  const merged = {
    apiKey:        envConfig.apiKey        || fileConfig.apiKey        || fileConfig.api_key,
    agentId:       envConfig.agentId       || fileConfig.agentId       || fileConfig.agent_id,
    nodeSecret:    envConfig.nodeSecret    || fileConfig.nodeSecret    || fileConfig.node_secret,
    agentName:     envConfig.agentName     || fileConfig.agentName     || fileConfig.agent_name,
    apiBaseUrl:    envConfig.apiBaseUrl    || fileConfig.apiBaseUrl    || fileConfig.api_base_url || 'https://www.singularity.mba',
    hubBaseUrl:    envConfig.hubBaseUrl    || fileConfig.hubBaseUrl    || fileConfig.hub_base_url || 'https://www.singularity.mba',
    configPath:    CONFIG_FILE,
  };

  return merged;
}

function maskSecret(key) {
  if (!key) return '(not set)';
  if (key.length < 8) return '***';
  return key.slice(0, 6) + '...' + key.slice(-4);
}

module.exports = { loadCredentials, maskSecret, CONFIG_FILE };
