#!/usr/bin/env node

/**
 * Config Loader for Layered Memory
 * 读取配置文件并合并 CLI 参数
 */

const fs = require('fs');
const path = require('path');

const DEFAULT_CONFIG = {
  defaultLayer: 'l1',
  autoMaintain: true,
  maintainInterval: 'daily', // 'hourly' | 'daily' | 'weekly'
  skipPatterns: ['.git', 'node_modules', '.clawhub', 'tmp', '.DS_Store'],
  maxConcurrent: 4,
  dryRun: false,
  verbose: false,
  l0: {
    maxTokens: 100,
    includeSections: 3
  },
  l1: {
    maxTokens: 1000,
    includeSubtasks: true,
    maxSubsections: 5
  },
  hooks: {
    onBootstrap: true,
    onSave: false,
    logLevel: 'info'
  }
};

class ConfigLoader {
  constructor(options = {}) {
    this.options = options;
    this.config = null;
  }

  /**
   * 加载配置（优先级：config file < defaults < CLI options）
   */
  load() {
    // 1. 从文件加载
    const fileConfig = this._loadFromFiles();
    
    // 2. 从环境变量加载
    const envConfig = this._loadFromEnv();
    
    // 3. 合并配置（CLI options > env > file > default）
    this.config = this._deepMerge(
      DEFAULT_CONFIG,
      fileConfig,
      envConfig,
      this.options
    );
    
    // 4. 验证
    this._validate();
    
    return this.config;
  }

  _loadFromFiles() {
    const searchPaths = [
      process.cwd(),
      process.env.HOME,
      path.join(process.env.HOME, 'clawd'),
      path.join(process.env.HOME, '.config', 'layered-memory'),
    ].filter(Boolean);

    for (const dir of searchPaths) {
      const filePath = path.join(dir, 'layered-memory.json');
      if (fs.existsSync(filePath)) {
        try {
          const content = fs.readFileSync(filePath, 'utf-8');
          return JSON.parse(content);
        } catch (e) {
          console.warn(`⚠️ 配置文件 ${filePath} 解析失败: ${e.message}`);
        }
      }
    }
    
    // 也支持项目根目录的 .layered-memory.json
    const projectConfig = path.join(process.cwd(), '.layered-memory.json');
    if (fs.existsSync(projectConfig)) {
      try {
        return JSON.parse(fs.readFileSync(projectConfig, 'utf-8'));
      } catch (e) {
        console.warn(`⚠️ 项目配置文件 ${projectConfig} 解析失败: ${e.message}`);
      }
    }
    
    return {};
  }

  _loadFromEnv() {
    const envConfig = {};
    const prefix = 'LAYERED_MEMORY_';
    
    for (const key in process.env) {
      if (key.startsWith(prefix)) {
        const subKey = key.slice(prefix.length).toLowerCase();
        const value = process.env[key];
        
        // 尝试解析布尔值或数字
        if (value === 'true') envConfig[subKey] = true;
        else if (value === 'false') envConfig[subKey] = false;
        else if (!isNaN(value) && value.trim() !== '') envConfig[subKey] = Number(value);
        else envConfig[subKey] = value;
      }
    }
    
    return envConfig;
  }

  _deepMerge(...objects) {
    const result = {};
    
    for (const obj of objects) {
      if (!obj) continue;
      for (const key in obj) {
        if (result[key] && typeof result[key] === 'object' && !Array.isArray(result[key])) {
          result[key] = this._deepMerge(result[key], obj[key]);
        } else {
          result[key] = obj[key];
        }
      }
    }
    
    return result;
  }

  _validate() {
    if (this.config.maxConcurrent < 1 || this.config.maxConcurrent > 16) {
      console.warn(`⚠️ maxConcurrent ${this.config.maxConcurrent} 不在推荐范围 [1-16]，自动调整为 4`);
      this.config.maxConcurrent = 4;
    }
    
    if (this.config.l0.maxTokens < 50) {
      console.warn(`⚠️ l0.maxTokens ${this.config.l0.maxTokens} 太小，可能影响质量，调整为 100`);
      this.config.l0.maxTokens = 100;
    }
  }

  get() {
    return this.config;
  }

  toString() {
    return JSON.stringify(this.config, null, 2);
  }
}

module.exports = ConfigLoader;
