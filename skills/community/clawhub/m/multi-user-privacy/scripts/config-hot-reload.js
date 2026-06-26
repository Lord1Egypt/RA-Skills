#!/usr/bin/env node

/**
 * 配置热更新监听器
 * 
 * 功能：
 * 1. 监听配置文件变化
 * 2. 自动重新加载配置
 * 3. 无需重启 OpenClaw
 * 
 * 用法：
 * node scripts/config-hot-reload.js
 */

const fs = require('fs');
const path = require('path');

const CONFIG_FILES = [
  path.join(process.env.HOME, '.openclaw/workspace/.privacy-config.json'),
  path.join(process.env.HOME, '.openclaw/workspace/.projects-config.json')
];

let configCache = {};
let watchers = [];

/**
 * 加载配置
 */
function loadConfig(configPath) {
  try {
    const content = fs.readFileSync(configPath, 'utf-8');
    const config = JSON.parse(content);
    configCache[configPath] = config;
    console.log(`[ConfigReload] ✅ 配置已加载：${path.basename(configPath)}`);
    return config;
  } catch (e) {
    console.error(`[ConfigReload] ❌ 加载配置失败：${path.basename(configPath)}`, e.message);
    return null;
  }
}

/**
 * 重新加载所有配置
 */
function reloadAllConfigs() {
  console.log('\n[ConfigReload] 🔄 重新加载所有配置...\n');
  
  CONFIG_FILES.forEach(configPath => {
    if (fs.existsSync(configPath)) {
      loadConfig(configPath);
    }
  });
  
  // 通知所有监听器
  watchers.forEach(callback => {
    try {
      callback(configCache);
    } catch (e) {
      console.error('[ConfigReload] 监听器回调错误:', e.message);
    }
  });
}

/**
 * 监听配置变化
 */
function watchConfigs() {
  console.log('[ConfigReload] 👁️  开始监听配置文件变化...\n');
  
  CONFIG_FILES.forEach(configPath => {
    if (!fs.existsSync(configPath)) {
      console.warn(`[ConfigReload] ⚠️  配置文件不存在：${path.basename(configPath)}`);
      return;
    }
    
    // 加载初始配置
    loadConfig(configPath);
    
    // 使用 fs.watch 监听变化
    const watcher = fs.watch(configPath, (eventType) => {
      if (eventType === 'change') {
        console.log(`\n[ConfigReload] 📝 检测到配置变化：${path.basename(configPath)}`);
        
        // 延迟 100ms 再加载（避免文件写入未完成）
        setTimeout(() => {
          reloadAllConfigs();
        }, 100);
      }
    });
    
    watcher.on('error', (err) => {
      console.error(`[ConfigReload] ❌ 监听错误：`, err.message);
    });
    
    console.log(`[ConfigReload] ✅ 已监听：${path.basename(configPath)}`);
  });
  
  console.log('\n[ConfigReload] ✅ 配置热更新已启动');
  console.log('[ConfigReload] 💡 修改配置文件后会自动重新加载，无需重启\n');
}

/**
 * 添加配置变化监听器
 */
function onConfigChange(callback) {
  watchers.push(callback);
}

/**
 * 获取配置
 */
function getConfig(configType) {
  if (configType === 'privacy') {
    return configCache[CONFIG_FILES[0]];
  } else if (configType === 'projects') {
    return configCache[CONFIG_FILES[1]];
  }
  return configCache;
}

// 导出
module.exports = {
  watchConfigs,
  onConfigChange,
  getConfig,
  reloadAllConfigs
};

// CLI 入口
if (require.main === module) {
  watchConfigs();
  
  // 保持进程运行
  process.on('SIGINT', () => {
    console.log('\n[ConfigReload] 👋 配置热更新已停止\n');
    process.exit(0);
  });
}
