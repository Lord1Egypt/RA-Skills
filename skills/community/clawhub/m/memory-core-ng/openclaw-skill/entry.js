const { createMemoryCore, quickStart } = require('./index');

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
        verbose: this.config.verbose || false
      });
      
      this.initialized = true;
      console.log(`✅ ${this.name} 技能初始化成功`);
      return this.memoryCore;
    } catch (error) {
      console.error(`❌ ${this.name} 技能初始化失败:`, error.message);
      throw error;
    }
  }
  
  async execute(context, args = {}) {
    if (!this.initialized) await this.initialize();
    
    const command = args.command || 'help';
    
    switch (command) {
      case 'search': return await this.handleSearch(args);
      case 'add': return await this.handleAdd(args);
      case 'stats': return await this.handleStats(args);
      case 'import-flomo': return await this.handleImportFlomo(args);
      case 'help': default: return await this.handleHelp(args);
    }
  }
  
  async handleSearch(args) {
    const { query, topK = 3, useReranker = true } = args;
    
    if (!query) {
      return {
        success: false,
        error: '请提供搜索查询内容',
        usage: '/memory search <query> [--topK=3] [--useReranker=true]'
      };
    }
    
    try {
      const startTime = Date.now();
      const result = await this.memoryCore.search(query, {
        topKFinal: parseInt(topK),
        useReranker: useReranker !== 'false'
      });
      const searchTime = Date.now() - startTime;
      
      if (result.success) {
        return {
          success: true,
          query,
          results: result.results,
          stats: { searchTime, resultsCount: result.results.length }
        };
      } else {
        return { success: false, query, error: result.error };
      }
    } catch (error) {
      return { success: false, query, error: error.message };
    }
  }
  
  async handleAdd(args) {
    const { content, category, tags } = args;
    
    if (!content) {
      return {
        success: false,
        error: '请提供记忆内容',
        usage: '/memory add <content> [--category=分类] [--tags=标签1,标签2]'
      };
    }
    
    try {
      const metadata = {};
      if (category) metadata.category = category;
      if (tags) metadata.tags = tags.split(',');
      
      const memory = await this.memoryCore.addMemory(content, metadata);
      
      return {
        success: true,
        memory: {
          id: memory.id,
          content: memory.content.substring(0, 100) + (memory.content.length > 100 ? '...' : ''),
          category: memory.metadata?.category,
          tags: memory.metadata?.tags
        },
        message: '记忆添加成功'
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  async handleStats(args) {
    try {
      const info = this.memoryCore.getInfo();
      const memoryStats = this.memoryCore.memoryService.getStats();
      
      return {
        success: true,
        stats: {
          system: {
            initialized: info.initialized,
            services: Object.keys(info.services)
          },
          memory: memoryStats
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  async handleImportFlomo(args) {
    const { filePath, batchSize = 10 } = args;
    
    if (!filePath) {
      return {
        success: false,
        error: '请提供 Flomo 导出文件路径',
        usage: '/memory import-flomo <filePath> [--batchSize=10]'
      };
    }
    
    try {
      const flomoAdapter = this.memoryCore.createFlomoAdapter({ verbose: true });
      
      const parseResult = await flomoAdapter.parseFromFile(filePath);
      
      if (!parseResult.success) {
        return { success: false, error: `Flomo 解析失败: ${parseResult.error}` };
      }
      
      const importResult = await flomoAdapter.importToMemory(
        parseResult.notes,
        this.memoryCore.memoryService,
        { batchSize: parseInt(batchSize) }
      );
      
      return {
        success: true,
        import: {
          totalNotes: parseResult.stats.totalNotes,
          imported: importResult.successful,
          failed: importResult.failed
        },
        message: `Flomo 导入完成: ${importResult.successful}/${parseResult.notes.length} 条笔记`
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  async handleHelp(args) {
    return {
      success: true,
      commands: {
        search: '搜索记忆 - /memory search <查询>',
        add: '添加记忆 - /memory add <内容>',
        stats: '查看统计 - /memory stats',
        'import-flomo': '导入 Flomo - /memory import-flomo <文件路径>',
        help: '显示帮助 - /memory help'
      },
      examples: [
        '/memory search "AI 身份验证" --topK=5',
        '/memory add "重要信息" --category=知识 --tags=学习,笔记',
        '/memory stats',
        '/memory import-flomo ~/flomo-export.html --batchSize=20'
      ]
    };
  }
  
  getInfo() {
    return {
      name: this.name,
      description: this.description,
      version: this.version,
      initialized: this.initialized,
      config: this.config
    };
  }
}

module.exports = MemoryCoreSkill;
