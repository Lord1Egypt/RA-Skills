/**
 * 🎯 Memory Core 集成模块
 * 将新的 Memory Core 架构集成到现有的 Smart Memory 系统
 */

const path = require('path');

class MemoryCoreIntegration {
  constructor(smartMemorySystem, config = {}) {
    this.smartMemorySystem = smartMemorySystem;
    this.config = config;
    this.memoryCore = null;
    this.integrated = false;
    
    this.stats = {
      integrationAttempts: 0,
      successfulIntegrations: 0,
      failedIntegrations: 0,
      searchesDelegated: 0,
      memoriesMigrated: 0
    };
  }
  
  /**
   * 集成 Memory Core
   */
  async integrate() {
    if (this.integrated) {
      console.log('✅ Memory Core 已集成');
      return this.memoryCore;
    }
    
    this.stats.integrationAttempts++;
    console.log('🔗 开始集成 Memory Core...');
    
    try {
      // 尝试加载 Memory Core
      let memoryCoreModule;
      
      try {
        // 尝试从 workspace 加载
        memoryCoreModule = require('../../../workspace/memory-core');
        console.log('📦 从 workspace 加载 Memory Core');
      } catch (error) {
        // 尝试从 node_modules 加载
        try {
          memoryCoreModule = require('@openclaw/memory-core');
          console.log('📦 从 node_modules 加载 Memory Core');
        } catch (npmError) {
          // 尝试从当前目录加载
          try {
            const localPath = path.join(__dirname, '../../memory-core');
            memoryCoreModule = require(localPath);
            console.log('📦 从本地目录加载 Memory Core');
          } catch (localError) {
            throw new Error('无法加载 Memory Core 模块。请确保已安装或配置正确。');
          }
        }
      }
      
      // 初始化 Memory Core
      const { createMemoryCore } = memoryCoreModule;
      
      this.memoryCore = createMemoryCore({
        ...this.config,
        verbose: this.config.verbose || true,
        // 从 Smart Memory 配置继承
        apiKey: this.config.apiKey || this.smartMemorySystem.config?.apiKey,
        baseUrl: this.config.baseUrl || 'https://api.edgefn.net/v1'
      });
      
      await this.memoryCore.initialize();
      
      // 迁移现有记忆（如果存在）
      await this.migrateExistingMemories();
      
      this.integrated = true;
      this.stats.successfulIntegrations++;
      
      console.log('✅ Memory Core 集成成功');
      console.log('📊 集成统计:', this.getStats());
      
      return this.memoryCore;
      
    } catch (error) {
      this.stats.failedIntegrations++;
      console.error('❌ Memory Core 集成失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 迁移现有记忆到 Memory Core
   */
  async migrateExistingMemories() {
    console.log('🔄 检查现有记忆迁移...');
    
    // 检查 Smart Memory 是否有记忆数据
    if (!this.smartMemorySystem.memories || 
        typeof this.smartMemorySystem.memories.getAll !== 'function') {
      console.log('   ℹ️  没有找到可迁移的记忆数据');
      return { migrated: 0, skipped: 0 };
    }
    
    try {
      const existingMemories = this.smartMemorySystem.memories.getAll();
      
      if (!existingMemories || existingMemories.length === 0) {
        console.log('   ℹ️  没有现有记忆需要迁移');
        return { migrated: 0, skipped: 0 };
      }
      
      console.log(`   📋 找到 ${existingMemories.length} 条现有记忆`);
      
      let migrated = 0;
      let skipped = 0;
      
      // 分批迁移以避免内存问题
      const batchSize = 10;
      for (let i = 0; i < existingMemories.length; i += batchSize) {
        const batch = existingMemories.slice(i, i + batchSize);
        
        const migrationPromises = batch.map(async (memory, index) => {
          try {
            // 迁移记忆到 Memory Core
            await this.memoryCore.addMemory(memory.content, {
              ...memory.metadata,
              migrated: true,
              originalId: memory.id,
              migrationDate: new Date().toISOString()
            });
            
            migrated++;
            
            if ((migrated + skipped) % 10 === 0) {
              console.log(`   🔄 迁移进度: ${migrated + skipped}/${existingMemories.length}`);
            }
            
            return { success: true, memory };
          } catch (error) {
            console.log(`   ⚠️  迁移失败 ${memory.id}: ${error.message}`);
            skipped++;
            return { success: false, memory, error };
          }
        });
        
        await Promise.all(migrationPromises);
      }
      
      this.stats.memoriesMigrated = migrated;
      
      console.log(`   ✅ 记忆迁移完成: ${migrated} 条迁移, ${skipped} 条跳过`);
      
      return { migrated, skipped };
      
    } catch (error) {
      console.log(`   ❌ 记忆迁移失败: ${error.message}`);
      return { migrated: 0, skipped: 0, error: error.message };
    }
  }
  
  /**
   * 集成搜索功能
   */
  async integratedSearch(query, options = {}) {
    if (!this.integrated) {
      await this.integrate();
    }
    
    this.stats.searchesDelegated++;
    
    console.log(`🔍 集成搜索: "${query}" (委托给 Memory Core)`);
    
    // 使用 Memory Core 进行搜索
    const memoryCoreResult = await this.memoryCore.search(query, {
      ...options,
      useReranker: options.useReranker !== false
    });
    
    // 如果 Memory Core 搜索失败，回退到原系统
    if (!memoryCoreResult.success) {
      console.log('   ⚠️  Memory Core 搜索失败，回退到原系统');
      
      if (typeof this.smartMemorySystem.search === 'function') {
        return await this.smartMemorySystem.search(query, options);
      } else {
        return {
          success: false,
          query,
          error: 'Memory Core 搜索失败且无回退方案',
          results: []
        };
      }
    }
    
    // 转换结果为 Smart Memory 格式
    const convertedResults = memoryCoreResult.results.map(result => ({
      id: result.id,
      content: result.content,
      score: result.score,
      metadata: result.metadata || {},
      preview: result.preview,
      // 添加集成标记
      source: 'memory-core',
      embeddingScore: result.embeddingScore,
      rerankerScore: result.rerankerScore
    }));
    
    return {
      success: true,
      query,
      results: convertedResults,
      stats: {
        ...memoryCoreResult.stats,
        integrated: true,
        searchesDelegated: this.stats.searchesDelegated
      }
    };
  }
  
  /**
   * 集成添加功能
   */
  async integratedAdd(content, metadata = {}) {
    if (!this.integrated) {
      await this.integrate();
    }
    
    console.log(`📝 集成添加记忆: "${content.substring(0, 50)}..."`);
    
    // 同时添加到两个系统
    const promises = [];
    
    // 添加到 Memory Core
    promises.push(
      this.memoryCore.addMemory(content, {
        ...metadata,
        integrated: true,
        addedVia: 'smart-memory-integration'
      })
    );
    
    // 添加到原系统（如果支持）
    if (typeof this.smartMemorySystem.add === 'function') {
      promises.push(
        this.smartMemorySystem.add(content, metadata).catch(error => {
          console.log('   ⚠️  原系统添加失败:', error.message);
          return null;
        })
      );
    }
    
    const results = await Promise.all(promises);
    const memoryCoreResult = results[0];
    
    return {
      success: true,
      memory: memoryCoreResult,
      integrated: true,
      addedToBoth: results[1] !== null
    };
  }
  
  /**
   * 获取集成状态
   */
  getIntegrationStatus() {
    return {
      integrated: this.integrated,
      memoryCoreAvailable: !!this.memoryCore,
      stats: this.getStats(),
      config: {
        ...this.config,
        apiKey: this.config.apiKey ? '***' + this.config.apiKey.slice(-4) : '未设置'
      }
    };
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    const memoryCoreStats = this.memoryCore ? this.memoryCore.getInfo() : null;
    const memoryServiceStats = this.memoryCore?.memoryService?.getStats?.() || null;
    
    return {
      ...this.stats,
      memoryCore: memoryCoreStats ? {
        initialized: memoryCoreStats.initialized,
        services: Object.keys(memoryCoreStats.services || {}),
        providers: Object.keys(memoryCoreStats.providers || {})
      } : null,
      memoryService: memoryServiceStats ? {
        totalMemories: memoryServiceStats.totalMemories,
        totalSearches: memoryServiceStats.totalSearches
      } : null
    };
  }
  
  /**
   * 清理和重置
   */
  async cleanup() {
    console.log('🧹 清理集成资源...');
    
    if (this.memoryCore && typeof this.memoryCore.clearCache === 'function') {
      this.memoryCore.clearCache();
    }
    
    this.integrated = false;
    this.memoryCore = null;
    
    console.log('✅ 集成资源已清理');
  }
}

module.exports = MemoryCoreIntegration;
