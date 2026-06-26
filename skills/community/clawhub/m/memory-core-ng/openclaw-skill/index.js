/**
 * 🎯 Memory Core 主入口
 * 提供简化的使用接口
 */

const ServiceContainer = require('./src/managers/ServiceContainer');
const SimpleFlomoAdapter = require('./src/adapters/SimpleFlomoAdapter');

/**
 * 创建 Memory Core 实例
 */
function createMemoryCore(config = {}) {
  const container = new ServiceContainer(config);
  
  return {
    /**
     * 初始化所有服务
     */
    async initialize() {
      return container.initialize();
    },
    
    /**
     * 获取记忆服务
     */
    get memoryService() {
      return container.getService('memory');
    },
    
    /**
     * 获取 embedding 服务
     */
    get embeddingService() {
      return container.getService('embedding');
    },
    
    /**
     * 获取服务容器
     */
    get container() {
      return container;
    },
    
    /**
     * 创建 Flomo 适配器
     */
    createFlomoAdapter(flomoConfig = {}) {
      return new SimpleFlomoAdapter({
        ...config.flomo,
        ...flomoConfig
      });
    },
    
    /**
     * 快速搜索记忆
     */
    async search(query, options = {}) {
      const service = container.getService('memory');
      return service.search(query, options);
    },
    
    /**
     * 快速添加记忆
     */
    async addMemory(content, metadata = {}) {
      const service = container.getService('memory');
      return service.add(content, metadata);
    },
    
    /**
     * 获取系统信息
     */
    getInfo() {
      return container.getServicesInfo();
    },
    
    /**
     * 清空缓存
     */
    clearCache() {
      container.clearAllCaches();
    },
    
    /**
     * 重置系统
     */
    async reset() {
      return container.reset();
    }
  };
}

/**
 * 快速启动函数
 */
async function quickStart(config = {}) {
  const memoryCore = createMemoryCore(config);
  
  try {
    console.log('🚀 Memory Core 快速启动...');
    await memoryCore.initialize();
    
    console.log('✅ Memory Core 初始化成功');
    console.log('📊 系统信息:', JSON.stringify(memoryCore.getInfo(), null, 2));
    
    return memoryCore;
  } catch (error) {
    console.error('❌ Memory Core 启动失败:', error.message);
    throw error;
  }
}

module.exports = {
  createMemoryCore,
  quickStart,
  ServiceContainer,
  FlomoAdapter: SimpleFlomoAdapter,
  
  // 组件导出（高级用户使用）
  components: {
    // Providers
    EdgefnEmbeddingProvider: require('./src/providers/embeddings/EdgefnEmbeddingProvider'),
    EdgefnRerankProvider: require('./src/providers/rerank/EdgefnRerankProvider'),
    
    // Services
    EmbeddingService: require('./src/services/EmbeddingService'),
    MemoryService: require('./src/services/MemoryService'),
    
    // Utilities
    SimilarityCalculator: require('./src/utils/similarity').SimilarityCalculator,
    IntelligentCache: require('./src/utils/cache').IntelligentCache,
    ResilientService: require('./src/utils/resilience').ResilientService,
    SimpleIdGenerator: require('./src/utils/id').SimpleIdGenerator
  }
};
