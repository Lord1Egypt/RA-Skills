/**
 * 🎯 Memory Service
 * 智能记忆管理核心服务
 */

const { SimpleIdGenerator } = require('../utils/id');
const { MemoryService: BaseMemoryService, SearchOptions, SearchResult, Memory } = require('../interfaces');
const { SimilarityCalculator } = require('../utils/similarity');
const { IntelligentCache } = require('../utils/cache');

class CoreMemoryService extends BaseMemoryService {
  constructor(config = {}) {
    super();
    
    this.config = {
      // 服务配置
      embeddingService: config.embeddingService,
      rerankProvider: config.rerankProvider,
      
      // 搜索配置
      defaultSearchOptions: {
        useReranker: true,
        topKInitial: 15,
        topKFinal: 5,
        embeddingWeight: 0.4,
        rerankerWeight: 0.6,
        minScore: 0.1,
        includeMetadata: false,
        ...config.defaultSearchOptions
      },
      
      // 存储配置
      storage: config.storage || new Map(), // 默认内存存储
      autoEmbed: config.autoEmbed !== false,
      
      // 其他配置
      verbose: config.verbose || false,
      ...config
    };
    
    if (!this.config.embeddingService) {
      throw new Error('EmbeddingService is required');
    }
    
    // 初始化
    this.memories = this.config.storage; // Map 或兼容接口
    this.cache = new IntelligentCache({
      defaultTTLs: {
        search: 300000,  // 5分钟
        embeddings: 3600000  // 1小时
      }
    });
    
    this.stats = {
      totalMemories: 0,
      totalSearches: 0,
      successfulSearches: 0,
      failedSearches: 0,
      embeddingsGenerated: 0,
      rerankerCalls: 0
    };
    
    // 如果 storage 是 Map，计算初始数量
    if (this.memories instanceof Map) {
      this.stats.totalMemories = this.memories.size;
    }
    
    this.log('🚀 CoreMemoryService initialized');
  }
  
  async add(content, metadata = {}) {
    if (!content || typeof content !== 'string') {
      throw new Error('Content must be a non-empty string');
    }
    
    const id = SimpleIdGenerator.generate();
    const now = new Date();
    
    const memory = new Memory({
      id,
      content,
      metadata: {
        ...metadata,
        length: content.length,
        createdAt: now,
        updatedAt: now
      },
      createdAt: now,
      updatedAt: now
    });
    
    // 自动生成 embedding
    if (this.config.autoEmbed) {
      try {
        const [embedding] = await this.config.embeddingService.embed([content]);
        memory.embedding = embedding;
        this.stats.embeddingsGenerated++;
        this.log(`✅ Generated embedding for memory ${id}`);
      } catch (error) {
        this.log(`⚠️  Failed to generate embedding for memory ${id}: ${error.message}`);
        // 继续，embedding 是可选的
      }
    }
    
    // 存储记忆
    this.memories.set(id, memory);
    this.stats.totalMemories++;
    
    // 清理相关缓存
    this.cache.delete('search', 'recent');
    
    this.log(`✅ Added memory ${id} (${content.length} chars)`);
    
    return memory;
  }
  
  async search(query, options = {}) {
    if (!query || typeof query !== 'string') {
      throw new Error('Query must be a non-empty string');
    }
    
    this.stats.totalSearches++;
    
    const searchOptions = new SearchOptions({
      ...this.config.defaultSearchOptions,
      ...options
    });
    
    this.log(`🔍 Searching: "${query.substring(0, 50)}${query.length > 50 ? '...' : ''}"`);
    this.log(`   Options: reranker=${searchOptions.useReranker}, topK=${searchOptions.topKFinal}`);
    
    try {
      // 1. 检查缓存
      const cacheKey = this._generateSearchCacheKey(query, searchOptions);
      const cached = this.cache.get('search', cacheKey);
      
      if (cached) {
        this.log(`💾 Search cache hit for query`);
        this.stats.successfulSearches++;
        return cached;
      }
      
      // 2. 获取所有记忆
      const memories = Array.from(this.memories.values());
      if (memories.length === 0) {
        const emptyResult = {
          success: true,
          query,
          results: [],
          stats: { memoriesProcessed: 0 }
        };
        
        this.cache.set('search', cacheKey, emptyResult, 60000); // 短暂缓存空结果
        this.stats.successfulSearches++;
        return emptyResult;
      }
      
      // 3. 生成查询的 embedding
      const [queryEmbedding] = await this.config.embeddingService.embed([query]);
      
      // 4. 收集有 embedding 的记忆
      const memoriesWithEmbeddings = [];
      const memoriesWithoutEmbeddings = [];
      
      for (const memory of memories) {
        if (memory.embedding && memory.embedding.length > 0) {
          memoriesWithEmbeddings.push(memory);
        } else {
          memoriesWithoutEmbeddings.push(memory);
        }
      }
      
      this.log(`   Memories: ${memoriesWithEmbeddings.length} with embeddings, ${memoriesWithoutEmbeddings.length} without`);
      
      // 5. 计算相似度
      const embeddings = memoriesWithEmbeddings.map(m => m.embedding);
      const similarities = SimilarityCalculator.batchSimilarity(queryEmbedding, embeddings);
      
      // 6. 初始排序（仅基于 embeddings）
      const initialResults = [];
      
      for (let i = 0; i < memoriesWithEmbeddings.length; i++) {
        const similarity = similarities[i];
        if (similarity >= searchOptions.minScore) {
          initialResults.push({
            memory: memoriesWithEmbeddings[i],
            embeddingScore: similarity
          });
        }
      }
      
      // 添加没有 embedding 的记忆（低分）
      for (const memory of memoriesWithoutEmbeddings) {
        initialResults.push({
          memory,
          embeddingScore: 0.01 // 最低分
        });
      }
      
      // 按 embedding 分数排序
      initialResults.sort((a, b) => b.embeddingScore - a.embeddingScore);
      const topInitial = initialResults.slice(0, searchOptions.topKInitial);
      
      this.log(`   Initial candidates: ${topInitial.length}/${initialResults.length}, top score: ${topInitial[0]?.embeddingScore?.toFixed(4) || 0}`);
      
      // 7. 使用 reranker 优化（如果启用）
      let finalResults = topInitial;
      
      if (searchOptions.useReranker && this.config.rerankProvider && topInitial.length > 0) {
        try {
          const documents = topInitial.map(r => r.memory.content);
          const rerankResults = await this.config.rerankProvider.rerank(query, documents);
          this.stats.rerankerCalls++;
          
          // 合并分数
          finalResults = topInitial.map((result, i) => {
            const rerankerScore = rerankResults[i]?.relevanceScore || 0;
            const combinedScore = (result.embeddingScore * searchOptions.embeddingWeight) + 
                                  (rerankerScore * searchOptions.rerankerWeight);
            
            return {
              ...result,
              rerankerScore,
              combinedScore
            };
          });
          
          // 按综合分数排序
          finalResults.sort((a, b) => (b.combinedScore || 0) - (a.combinedScore || 0));
          this.log(`   Reranked top score: ${finalResults[0]?.combinedScore?.toFixed(4) || 0}`);
          
        } catch (rerankError) {
          this.log(`⚠️  Reranker failed: ${rerankError.message}, using embeddings only`);
          // 继续使用 embeddings 分数
        }
      }
      
      // 8. 格式化最终结果
      const formattedResults = finalResults
        .slice(0, searchOptions.topKFinal)
        .map((result, index) => {
          const memory = result.memory;
          const score = result.combinedScore !== undefined ? result.combinedScore : result.embeddingScore;
          
          return new SearchResult({
            id: memory.id,
            content: memory.content,
            score,
            embeddingScore: result.embeddingScore,
            rerankerScore: result.rerankerScore,
            metadata: searchOptions.includeMetadata ? memory.metadata : {},
            preview: memory.content.substring(0, 100) + (memory.content.length > 100 ? '...' : '')
          });
        });
      
      // 9. 构建返回结果
      const searchResult = {
        success: true,
        query,
        results: formattedResults,
        stats: {
          memoriesProcessed: memories.length,
          withEmbeddings: memoriesWithEmbeddings.length,
          withoutEmbeddings: memoriesWithoutEmbeddings.length,
          initialCandidates: topInitial.length,
          finalResults: formattedResults.length,
          usedReranker: searchOptions.useReranker && this.config.rerankProvider
        }
      };
      
      // 10. 缓存结果
      this.cache.intelligentSet('search', cacheKey, searchResult);
      
      this.stats.successfulSearches++;
      this.log(`✅ Search completed: ${formattedResults.length} results`);
      
      return searchResult;
      
    } catch (error) {
      this.stats.failedSearches++;
      this.log(`❌ Search failed: ${error.message}`);
      
      return {
        success: false,
        query,
        error: error.message,
        results: []
      };
    }
  }
  
  async update(id, updates) {
    if (!this.memories.has(id)) {
      throw new Error(`Memory not found: ${id}`);
    }
    
    const memory = this.memories.get(id);
    const now = new Date();
    
    // 应用更新
    if (updates.content !== undefined) {
      memory.content = updates.content;
      
      // 如果内容更新，重新生成 embedding
      if (this.config.autoEmbed) {
        try {
          const [embedding] = await this.config.embeddingService.embed([updates.content]);
          memory.embedding = embedding;
          this.stats.embeddingsGenerated++;
        } catch (error) {
          this.log(`⚠️  Failed to regenerate embedding for memory ${id}: ${error.message}`);
        }
      }
    }
    
    if (updates.metadata !== undefined) {
      memory.metadata = { ...memory.metadata, ...updates.metadata };
    }
    
    memory.updatedAt = now;
    memory.metadata.updatedAt = now;
    
    this.memories.set(id, memory);
    
    // 清理缓存
    this.cache.delete('search', 'recent');
    
    this.log(`✅ Updated memory ${id}`);
    
    return memory;
  }
  
  async delete(id) {
    if (!this.memories.has(id)) {
      throw new Error(`Memory not found: ${id}`);
    }
    
    const deleted = this.memories.delete(id);
    
    if (deleted) {
      this.stats.totalMemories--;
      
      // 清理缓存
      this.cache.delete('search', 'recent');
      
      this.log(`✅ Deleted memory ${id}`);
    }
    
    return deleted;
  }
  
  getStats() {
    const searchSuccessRate = this.stats.totalSearches > 0 
      ? this.stats.successfulSearches / this.stats.totalSearches 
      : 0;
    
    const cacheStats = this.cache.getStats();
    
    return {
      ...this.stats,
      searchSuccessRate: Math.round(searchSuccessRate * 10000) / 100,
      cacheStats
    };
  }
  
  /**
   * 批量添加记忆
   */
  async batchAdd(contents, metadataArray = []) {
    const results = [];
    
    for (let i = 0; i < contents.length; i++) {
      try {
        const content = contents[i];
        const metadata = metadataArray[i] || {};
        
        const memory = await this.add(content, metadata);
        results.push({ success: true, memory });
        
      } catch (error) {
        results.push({ success: false, error: error.message });
      }
    }
    
    return results;
  }
  
  /**
   * 批量搜索
   */
  async batchSearch(queries, optionsArray = []) {
    const results = [];
    
    for (let i = 0; i < queries.length; i++) {
      try {
        const query = queries[i];
        const options = optionsArray[i] || {};
        
        const result = await this.search(query, options);
        results.push(result);
        
      } catch (error) {
        results.push({
          success: false,
          query: queries[i],
          error: error.message
        });
      }
    }
    
    return results;
  }
  
  /**
   * 获取所有记忆（分页）
   */
  getAllMemories(limit = 100, offset = 0) {
    const memories = Array.from(this.memories.values())
      .sort((a, b) => b.createdAt - a.createdAt)
      .slice(offset, offset + limit);
    
    return {
      memories,
      total: this.stats.totalMemories,
      limit,
      offset
    };
  }
  
  /**
   * 清空所有缓存
   */
  clearCache() {
    this.cache.clear();
    this.log('🗑️  All caches cleared');
  }
  
  /**
   * 生成搜索缓存键
   */
  _generateSearchCacheKey(query, options) {
    const optionsStr = JSON.stringify({
      useReranker: options.useReranker,
      topKFinal: options.topKFinal,
      minScore: options.minScore
    });
    
    return `${query}:${optionsStr}:${this.stats.totalMemories}`;
  }
  
  log(...args) {
    if (this.config.verbose) {
      console.log('[MemoryService]', ...args);
    }
  }
}

module.exports = CoreMemoryService;
