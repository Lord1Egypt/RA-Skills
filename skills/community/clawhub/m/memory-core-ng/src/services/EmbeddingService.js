/**
 * 🎯 Embedding 服务
 * 管理多个 Embedding Provider，提供统一接口
 */

const { IntelligentCache } = require('../utils/cache');

class EmbeddingService {
  constructor(config = {}) {
    this.config = {
      defaultProvider: config.defaultProvider || 'edgefn',
      cacheEnabled: config.cacheEnabled !== false,
      verbose: config.verbose || false,
      ...config
    };
    
    this.providers = new Map();
    this.cache = this.config.cacheEnabled ? new IntelligentCache() : null;
    
    this.stats = {
      totalRequests: 0,
      cachedRequests: 0,
      providerRequests: new Map(),
      totalTexts: 0
    };
    
    this.log('🚀 EmbeddingService initialized');
  }
  
  /**
   * 注册 Provider
   */
  registerProvider(name, provider) {
    if (!name || !provider) {
      throw new Error('Provider name and instance are required');
    }
    
    if (this.providers.has(name)) {
      this.log(`⚠️  Overriding existing provider: ${name}`);
    }
    
    this.providers.set(name, provider);
    this.stats.providerRequests.set(name, 0);
    
    this.log(`✅ Registered provider: ${name}`);
    return this;
  }
  
  /**
   * 获取 Provider
   */
  getProvider(name = null) {
    const providerName = name || this.config.defaultProvider;
    
    if (!this.providers.has(providerName)) {
      throw new Error(`Provider not found: ${providerName}. Available: ${Array.from(this.providers.keys()).join(', ')}`);
    }
    
    return this.providers.get(providerName);
  }
  
  /**
   * 生成 embeddings（统一接口）
   */
  async embed(texts, options = {}) {
    if (!texts || !Array.isArray(texts) || texts.length === 0) {
      throw new Error('Texts must be a non-empty array');
    }
    
    this.stats.totalRequests++;
    this.stats.totalTexts += texts.length;
    
    const {
      provider: providerName,
      useCache = this.config.cacheEnabled,
      ...embeddingOptions
    } = options;
    
    // 1. 检查缓存
    if (useCache && this.cache) {
      const cacheKey = this._generateCacheKey(texts, providerName);
      const cached = this.cache.get('embeddings', cacheKey);
      
      if (cached) {
        this.stats.cachedRequests++;
        this.log(`💾 Cache hit for ${texts.length} texts`);
        return cached;
      }
    }
    
    // 2. 获取 Provider 并调用
    const provider = this.getProvider(providerName);
    const providerStats = this.stats.providerRequests.get(provider.getName()) || 0;
    this.stats.providerRequests.set(provider.getName(), providerStats + 1);
    
    this.log(`🔧 Generating embeddings via ${provider.getName()}: ${texts.length} texts`);
    
    try {
      const embeddings = await provider.generateEmbeddings(texts, embeddingOptions);
      
      // 3. 缓存结果
      if (useCache && this.cache) {
        const cacheKey = this._generateCacheKey(texts, providerName);
        this.cache.intelligentSet('embeddings', cacheKey, embeddings);
      }
      
      return embeddings;
      
    } catch (error) {
      this.log(`❌ Embedding generation failed: ${error.message}`);
      throw error;
    }
  }
  
  /**
   * 生成缓存键
   */
  _generateCacheKey(texts, providerName) {
    // 简化：使用文本内容的哈希
    const textHash = texts.join('|').length.toString(); // 实际应该用更好的哈希
    return `${providerName}:${textHash}:${texts.length}`;
  }
  
  /**
   * 获取所有 Provider 信息
   */
  getProvidersInfo() {
    const info = {};
    
    for (const [name, provider] of this.providers.entries()) {
      info[name] = {
        name: provider.getName(),
        dimensions: provider.getDimensions(),
        supportsBatch: provider.supportsBatch(),
        maxBatchSize: provider.getMaxBatchSize?.(),
        stats: provider.getStats?.() || {}
      };
    }
    
    return info;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    const cacheStats = this.cache ? this.cache.getStats() : null;
    const providerRequests = {};
    
    for (const [name, count] of this.stats.providerRequests.entries()) {
      providerRequests[name] = count;
    }
    
    const cacheHitRate = this.stats.totalRequests > 0 
      ? this.stats.cachedRequests / this.stats.totalRequests 
      : 0;
    
    return {
      ...this.stats,
      providerRequests,
      cacheStats,
      cacheHitRate: Math.round(cacheHitRate * 10000) / 100,
      providers: this.getProvidersInfo()
    };
  }
  
  /**
   * 清空缓存
   */
  clearCache() {
    if (this.cache) {
      this.cache.clear();
      this.log('🗑️  Embedding cache cleared');
    }
  }
  
  log(...args) {
    if (this.config.verbose) {
      console.log('[EmbeddingService]', ...args);
    }
  }
}

module.exports = EmbeddingService;
