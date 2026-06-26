const { createMemoryCore, quickStart } = require('./index');

/**
 * OpenClaw Skill Entry Point for Memory Core
 * 符合 OpenClaw skill 格式的入口文件
 */
class MemoryCoreSkill {
  constructor(config = {}) {
    this.config = config;
    this.name = 'memory-core';
    this.description = '智能记忆核心系统';
    this.version = '1.0.0';
    this.memoryCore = null;
    this.initialized = false;
  }
  
  async initialize() {
    if (this.initialized) return this.memoryCore;
    
    console.log(`🚀 初始化 ${this.name} 技能 v${this.version}...`);
    
    try {
      this.memoryCore = await quickStart({
        ...this.config,
        silent: true // 静默模式，不输出过多日志
      });
      
      this.initialized = true;
      console.log(`✅ ${this.name} 技能初始化完成`);
      return this.memoryCore;
    } catch (error) {
      console.error(`❌ ${this.name} 技能初始化失败:`, error.message);
      throw error;
    }
  }
  
  async search(query, options = {}) {
    await this.ensureInitialized();
    return this.memoryCore.search(query, options);
  }
  
  async add(content, metadata = {}) {
    await this.ensureInitialized();
    return this.memoryCore.addMemory(content, metadata);
  }
  
  async importFlomo(filePath) {
    await this.ensureInitialized();
    return this.memoryCore.importFromFlomo(filePath);
  }
  
  async getStats() {
    await this.ensureInitialized();
    return this.memoryCore.getStats();
  }
  
  async ensureInitialized() {
    if (!this.initialized) {
      await this.initialize();
    }
  }
  
  // OpenClaw skill 标准方法
  getCommands() {
    return [
      {
        name: 'search',
        description: '搜索记忆',
        usage: '/memory search <查询>'
      },
      {
        name: 'add',
        description: '添加记忆',
        usage: '/memory add <内容>'
      },
      {
        name: 'stats',
        description: '查看统计',
        usage: '/memory stats'
      },
      {
        name: 'import-flomo',
        description: '导入 Flomo 笔记',
        usage: '/memory import-flomo <文件路径>'
      }
    ];
  }
  
  getConfigTemplate() {
    return {
      apiKey: {
        type: 'string',
        description: 'Edgefn API Key',
        required: true
      },
      flomoPath: {
        type: 'string',
        description: 'Flomo 导出文件路径 (可选)',
        required: false
      }
    };
  }
}

module.exports = MemoryCoreSkill;