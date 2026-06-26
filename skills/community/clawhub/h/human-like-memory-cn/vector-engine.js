/**
 * 向量化记忆引擎 v1.1.0
 * 使用本地 Embedding 模型，无需 API Key
 * 模型：bge-m3 (ONNX 版本)
 */

const { pipeline } = require('@xenova/transformers');
const fs = require('fs');
const path = require('path');

class VectorMemoryEngine {
  constructor(options = {}) {
    this.embeddingPipeline = null;
    this.modelName = options.modelName || 'Xenova/bge-m3';
    this.cacheDir = options.cacheDir || path.join(__dirname, '.cache');
    this.similarityThreshold = options.threshold || 0.7;
    
    // 确保缓存目录存在
    if (!fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
  }

  /**
   * 初始化 Embedding 模型（首次使用会自动下载）
   * 性能优化：单例模式 + 懒加载 + 缓存
   */
  async initialize() {
    if (this.embeddingPipeline) {
      return this.embeddingPipeline;
    }

    console.log('🧠 初始化向量化引擎...');
    console.log('📥 首次使用会自动下载模型（约 200MB，仅需一次）');
    
    try {
      // 性能优化：使用量化版本 + 禁用不必要功能
      this.embeddingPipeline = await pipeline('feature-extraction', this.modelName, {
        cache_dir: this.cacheDir,
        quantized: true,           // 量化模型，减小 75% 体积
        device: 'cpu',             // 强制使用 CPU（兼容性更好）
        progress_callback: null,   // 禁用进度回调（减少开销）
      });
      
      console.log('✅ 向量化引擎初始化完成');
      console.log('💡 提示：模型已缓存，下次启动无需下载');
      return this.embeddingPipeline;
    } catch (error) {
      console.error('❌ 向量化引擎初始化失败:', error.message);
      console.log('⚠️  将使用备用方案（关键词检索）');
      throw error;
    }
  }

  /**
   * 生成文本的 embedding 向量
   * 性能优化：缓存短文本结果
   */
  async embed(text) {
    // 性能优化：缓存常见短文本
    const cacheKey = text.slice(0, 100);
    if (this.embedCache && this.embedCache.has(cacheKey)) {
      return this.embedCache.get(cacheKey);
    }

    if (!this.embeddingPipeline) {
      await this.initialize();
    }

    const startTime = Date.now();
    const output = await this.embeddingPipeline(text, {
      pooling: 'mean',
      normalize: true,
    });

    // 转换为数组
    const embedding = Array.from(output.data);
    
    // 性能监控
    const duration = Date.now() - startTime;
    if (duration > 200) {
      console.warn(`⚠️  Embedding 生成较慢：${duration}ms (文本长度：${text.length})`);
    }

    // 缓存结果（最多 100 条）
    if (!this.embedCache) this.embedCache = new Map();
    if (this.embedCache.size >= 100) {
      // 删除最旧的 20%
      const toDelete = Array.from(this.embedCache.keys()).slice(0, 20);
      toDelete.forEach(key => this.embedCache.delete(key));
    }
    this.embedCache.set(cacheKey, embedding);

    return embedding;
  }

  /**
   * 批量生成 embedding
   * 性能优化：并行处理 + 分批
   */
  async embedBatch(texts, batchSize = 10) {
    if (!this.embeddingPipeline) {
      await this.initialize();
    }

    const embeddings = [];
    const startTime = Date.now();

    // 分批处理（避免内存溢出）
    for (let i = 0; i < texts.length; i += batchSize) {
      const batch = texts.slice(i, i + batchSize);
      const batchEmbeddings = await Promise.all(
        batch.map(text => this.embed(text))
      );
      embeddings.push(...batchEmbeddings);
      
      // 进度日志（仅大数据量时）
      if (texts.length > 50) {
        const progress = Math.min(100, Math.round(((i + batchSize) / texts.length) * 100));
        console.log(`📊 Embedding 进度：${progress}% (${i + batchSize}/${texts.length})`);
      }
    }

    const duration = Date.now() - startTime;
    console.log(`✅ 批量处理完成：${texts.length}条，耗时${duration}ms，平均${(duration/texts.length).toFixed(1)}ms/条`);

    return embeddings;
  }

  /**
   * 计算两个向量的余弦相似度
   */
  cosineSimilarity(vecA, vecB) {
    if (vecA.length !== vecB.length) {
      throw new Error('向量维度不匹配');
    }

    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < vecA.length; i++) {
      dotProduct += vecA[i] * vecB[i];
      normA += vecA[i] * vecA[i];
      normB += vecB[i] * vecB[i];
    }

    if (normA === 0 || normB === 0) {
      return 0;
    }

    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  /**
   * 向量搜索：找到与查询最相关的记忆
   * @param {string} query - 查询文本
   * @param {Array} memories - 记忆数组（每条记忆需包含 embedding 字段）
   * @param {number} topK - 返回结果数量
   * @returns {Array} 排序后的相关记忆（带相似度分数）
   */
  async search(query, memories, topK = 5) {
    if (memories.length === 0) {
      return [];
    }

    // 生成查询的 embedding
    const queryEmbedding = await this.embed(query);

    // 计算与每条记忆的相似度
    const results = memories.map(memory => {
      if (!memory.embedding || !Array.isArray(memory.embedding)) {
        return { ...memory, similarity: 0, warning: '无向量数据' };
      }

      const similarity = this.cosineSimilarity(queryEmbedding, memory.embedding);
      return { ...memory, similarity };
    });

    // 过滤低相似度结果
    const filtered = results.filter(r => r.similarity >= this.similarityThreshold);

    // 按相似度排序
    filtered.sort((a, b) => b.similarity - a.similarity);

    // 返回 Top K
    return filtered.slice(0, topK);
  }

  /**
   * 为记忆批量添加 embedding
   */
  async addEmbeddings(memories) {
    const texts = memories.map(m => m.content);
    const embeddings = await this.embedBatch(texts);

    return memories.map((memory, index) => ({
      ...memory,
      embedding: embeddings[index],
      embeddingModel: this.modelName,
      embeddingCreatedAt: new Date().toISOString(),
    }));
  }

  /**
   * 检查记忆是否需要更新 embedding
   */
  needsEmbeddingUpdate(memory) {
    if (!memory.embedding) return true;
    if (memory.embeddingModel !== this.modelName) return true;
    if (!memory.embeddingCreatedAt) return true;
    
    // 超过 30 天未更新，重新生成
    const lastUpdate = new Date(memory.embeddingCreatedAt);
    const daysOld = (Date.now() - lastUpdate.getTime()) / (1000 * 60 * 60 * 24);
    return daysOld > 30;
  }

  /**
   * 获取向量统计信息
   */
  getStats(memories) {
    const withEmbedding = memories.filter(m => m.embedding).length;
    const total = memories.length;

    return {
      totalMemories: total,
      vectorizedMemories: withEmbedding,
      vectorizationRate: ((withEmbedding / total) * 100).toFixed(1) + '%',
      modelUsed: this.modelName,
      cacheDir: this.cacheDir,
    };
  }
}

module.exports = VectorMemoryEngine;
