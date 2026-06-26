/**
 * 🎯 服务容器
 * 依赖注入容器，管理所有服务生命周期
 */

const EdgefnEmbeddingProvider = require('../providers/embeddings/EdgefnEmbeddingProvider');
const EdgefnRerankProvider = require('../providers/rerank/EdgefnRerankProvider');
const EmbeddingService = require('../services/EmbeddingService');
const CoreMemoryService = require('../services/MemoryService');
const { IntelligentCache } = require('../utils/cache');

class ServiceContainer {
  constructor(config = {}) {
    this.config = {
      // Provider 配置
      providers: {
        embedding: {
          type: 'edgefn',
          apiKey: config.apiKey || process.env.EDGEFN_API_KEY,
          baseUrl: config.baseUrl || 'https://api.edgefn.net/v1',
          verbose: config.verbose || false,
          ...config.embeddingProvider
        },
        rerank: {
          type: 'edgefn',
          apiKey: config.apiKey || process.env.EDGEFN_API_KEY,
          baseUrl: config.baseUrl || 'https://api.edgefn.net/v1',
          verbose: config.verbose || false,
          ...config.rerankProvider
        }
      },
      
      // 服务配置
      services: {
        embedding: {
          defaultProvider: 'edgefn',
          cacheEnabled: true,
          verbose: config.verbose || false,
          ...config.embeddingService
        },
        memory: {
          autoEmbed: true,
          verbose: config.verbose || false,
          defaultSearchOptions: {
            useReranker: true,
            topKInitial: 15,
            topKFinal: 5,
            embeddingWeight: 0.4,
            rerankerWeight: 0.6,
            minScore: 0.1
          },
          ...config.memoryService
        }
      },
      
      // 存储配置
      storage: config.storage || new Map(),
      
      // 其他
      verbose: config.verbose || false,
      ...config
    };
    
    this.services = new Map();
    this.providers = new Map();
    this.initialized = false;
    
    this.log('🚀 ServiceContainer created');
  }
  
  /**
   * 初始化所有服务
   */
  async initialize() {
    if (this.initialized) {
      this.log('⚠️  Already initialized');
      return;
    }
    
    this.log('🎯 Initializing services...');
    
    try {
      // 1. 初始化 Provider
      await this._initializeProviders();
      
      // 2. 初始化服务
      await this._initializeServices();
      
      // 3. 连接依赖
      this._connectDependencies();
      
      this.initialized = true;
      this.log('✅ All services initialized successfully');
      
    } catch (error) {
      this.log(`❌ Initialization failed: ${error.message}`);
      throw error;
    }
  }
  
  /**
   * 初始化 Provider
   */
  async _initializeProviders() {
    this.log('🔧 Initializing providers...');
    
    // Embedding Provider
    const embeddingConfig = this.config.providers.embedding;
    if (embeddingConfig.type === 'edgefn') {
      const provider = new EdgefnEmbeddingProvider(embeddingConfig);
      this.providers.set('embedding', provider);
      this.log(`✅ Embedding provider: ${provider.getName()}`);
    } else {
      throw new Error(`Unsupported embedding provider type: ${embeddingConfig.type}`);
    }
    
    // Rerank Provider
    const rerankConfig = this.config.providers.rerank;
    if (rerankConfig.type === 'edgefn') {
      const provider = new EdgefnRerankProvider(rerankConfig);
      this.providers.set('rerank', provider);
      this.log(`✅ Rerank provider: ${provider.getName()}`);
    } else {
      this.log(`⚠️  Rerank provider not configured, searches will use embeddings only`);
    }
  }
  
  /**
   * 初始化服务
   */
  async _initializeServices() {
    this.log('🔧 Initializing services...');
    
    // Embedding Service
    const embeddingService = new EmbeddingService(this.config.services.embedding);
    embeddingService.registerProvider('edgefn', this.providers.get('embedding'));
    this.services.set('embedding', embeddingService);
    this.log('✅ EmbeddingService initialized');
    
    // Memory Service
    const memoryService = new CoreMemoryService({
      ...this.config.services.memory,
      embeddingService,
      rerankProvider: this.providers.get('rerank'),
      storage: this.config.storage
    });
    this.services.set('memory', memoryService);
    this.log('✅ MemoryService initialized');
  }
  
  /**
   * 连接服务依赖
   */
  _connectDependencies() {
    // 目前依赖已经在初始化时设置好
    this.log('🔗 Service dependencies connected');
  }
  
  /**
   * 获取服务
   */
  getService(name) {
    if (!this.initialized) {
      throw new Error('ServiceContainer not initialized. Call initialize() first.');
    }
    
    const service = this.services.get(name);
    if (!service) {
      throw new Error(`Service not found: ${name}. Available: ${Array.from(this.services.keys()).join(', ')}`);
    }
    
    return service;
  }
  
  /**
   * 获取 Provider
   */
  getProvider(name) {
    if (!this.initialized) {
      throw new Error('ServiceContainer not initialized. Call initialize() first.');
    }
    
    const provider = this.providers.get(name);
    if (!provider) {
      throw new Error(`Provider not found: ${name}. Available: ${Array.from(this.providers.keys()).join(', ')}`);
    }
    
    return provider;
  }
  
  /**
   * 获取所有服务信息
   */
  getServicesInfo() {
    const info = {
      initialized: this.initialized,
      services: {},
      providers: {},
      stats: {}
    };
    
    // 服务信息
    for (const [name, service] of this.services.entries()) {
      info.services[name] = {
        type: service.constructor.name,
        stats: service.getStats ? service.getStats() : {}
      };
    }
    
    // Provider 信息
    for (const [name, provider] of this.providers.entries()) {
      info.providers[name] = {
        name: provider.getName(),
        type: provider.constructor.name,
        stats: provider.getStats ? provider.getStats() : {}
      };
    }
    
    // 容器统计
    info.stats = {
      totalServices: this.services.size,
      totalProviders: this.providers.size,
      config: {
        verbose: this.config.verbose,
        embeddingProvider: this.config.providers.embedding.type,
        rerankProvider: this.config.providers.rerank.type
      }
    };
    
    return info;
  }
  
  /**
   * 清空所有缓存
   */
  clearAllCaches() {
    for (const [name, service] of this.services.entries()) {
      if (service.clearCache) {
        service.clearCache();
        this.log(`🗑️  Cleared cache for ${name}`);
      }
    }
    
    this.log('✅ All caches cleared');
  }
  
  /**
   * 重置所有服务
   */
  async reset() {
    this.log('🔄 Resetting all services...');
    
    this.services.clear();
    this.providers.clear();
    this.initialized = false;
    
    await this.initialize();
    
    this.log('✅ All services reset');
  }
  
  log(...args) {
    if (this.config.verbose) {
      console.log('[ServiceContainer]', ...args);
    }
  }
}

module.exports = ServiceContainer;
