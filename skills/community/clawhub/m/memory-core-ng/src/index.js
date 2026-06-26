/**
 * Memory Core - 简化版核心模块
 * 整合原有复杂结构，便于 OpenClaw skill 集成
 */

const ServiceContainer = require('./managers/ServiceContainer');
const SimpleFlomoAdapter = require('./adapters/SimpleFlomoAdapter');

// 重新导出原有功能
module.exports = {
  // 核心类
  ServiceContainer,
  SimpleFlomoAdapter,
  
  // 工具函数
  cache: require('./utils/cache'),
  similarity: require('./utils/similarity'),
  id: require('./utils/id'),
  resilience: require('./utils/resilience'),
  
  // 服务
  EmbeddingService: require('./services/EmbeddingService'),
  MemoryService: require('./services/MemoryService'),
  
  // 提供商
  EdgefnEmbeddingProvider: require('./providers/embeddings/EdgefnEmbeddingProvider'),
  EdgefnRerankProvider: require('./providers/rerank/EdgefnRerankProvider'),
  
  // 快捷方法
  createMemoryCore: function(config = {}) {
    const container = new ServiceContainer(config);
    
    return {
      async initialize() {
        return container.initialize();
      },
      
      async search(query, options = {}) {
        const memoryService = container.getService('memory');
        return memoryService.search(query, options);
      },
      
      async addMemory(content, metadata = {}) {
        const memoryService = container.getService('memory');
        return memoryService.add(content, metadata);
      },
      
      async importFromFlomo(filePath) {
        const adapter = new SimpleFlomoAdapter(filePath);
        const memories = await adapter.import();
        
        const memoryService = container.getService('memory');
        for (const memory of memories) {
          await memoryService.add(memory.content, memory.metadata);
        }
        
        return memories.length;
      },
      
      async getStats() {
        const memoryService = container.getService('memory');
        return memoryService.getStats();
      }
    };
  },
  
  quickStart: async function(config = {}) {
    const memoryCore = module.exports.createMemoryCore(config);
    await memoryCore.initialize();
    return memoryCore;
  }
};