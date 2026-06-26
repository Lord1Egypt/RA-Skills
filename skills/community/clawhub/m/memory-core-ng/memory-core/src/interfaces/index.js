/**
 * 🎯 核心接口定义
 * 遵循依赖倒置原则：高层模块依赖抽象，不依赖具体实现
 */

/**
 * Embedding Provider 接口
 */
class EmbeddingProvider {
  /**
   * 获取 Provider 名称
   */
  getName() {
    throw new Error('必须实现 getName() 方法');
  }
  
  /**
   * 生成文本的 embeddings
   * @param {string[]} texts - 文本数组
   * @returns {Promise<number[][]>} embeddings 数组
   */
  async generateEmbeddings(texts) {
    throw new Error('必须实现 generateEmbeddings() 方法');
  }
  
  /**
   * 获取 embedding 维度
   */
  getDimensions() {
    throw new Error('必须实现 getDimensions() 方法');
  }
  
  /**
   * 是否支持批量处理
   */
  supportsBatch() {
    return true;
  }
  
  /**
   * 获取最大批量大小
   */
  getMaxBatchSize() {
    return 100;
  }
}

/**
 * Rerank Provider 接口
 */
class RerankProvider {
  /**
   * 获取 Provider 名称
   */
  getName() {
    throw new Error('必须实现 getName() 方法');
  }
  
  /**
   * 对文档进行重排序
   * @param {string} query - 查询文本
   * @param {string[]} documents - 文档数组
   * @returns {Promise<RerankResult[]>} 重排序结果
   */
  async rerank(query, documents) {
    throw new Error('必须实现 rerank() 方法');
  }
  
  /**
   * 获取最大文档数量
   */
  getMaxDocuments() {
    return 100;
  }
}

/**
 * Rerank 结果
 */
class RerankResult {
  constructor(index, relevanceScore) {
    this.index = index;
    this.relevanceScore = relevanceScore;
  }
}

/**
 * 记忆服务接口
 */
class MemoryService {
  /**
   * 添加记忆
   * @param {string} content - 记忆内容
   * @param {object} metadata - 元数据
   * @returns {Promise<Memory>} 创建的记忆
   */
  async add(content, metadata = {}) {
    throw new Error('必须实现 add() 方法');
  }
  
  /**
   * 搜索记忆
   * @param {string} query - 搜索查询
   * @param {SearchOptions} options - 搜索选项
   * @returns {Promise<SearchResult[]>} 搜索结果
   */
  async search(query, options = {}) {
    throw new Error('必须实现 search() 方法');
  }
  
  /**
   * 更新记忆
   * @param {string} id - 记忆 ID
   * @param {object} updates - 更新内容
   */
  async update(id, updates) {
    throw new Error('必须实现 update() 方法');
  }
  
  /**
   * 删除记忆
   * @param {string} id - 记忆 ID
   */
  async delete(id) {
    throw new Error('必须实现 delete() 方法');
  }
  
  /**
   * 获取记忆统计
   */
  getStats() {
    throw new Error('必须实现 getStats() 方法');
  }
}

/**
 * 搜索选项
 */
class SearchOptions {
  constructor({
    useReranker = true,
    topKInitial = 10,
    topKFinal = 5,
    embeddingWeight = 0.4,
    rerankerWeight = 0.6,
    minScore = 0.1,
    includeMetadata = false
  } = {}) {
    this.useReranker = useReranker;
    this.topKInitial = topKInitial;
    this.topKFinal = topKFinal;
    this.embeddingWeight = embeddingWeight;
    this.rerankerWeight = rerankerWeight;
    this.minScore = minScore;
    this.includeMetadata = includeMetadata;
  }
}

/**
 * 搜索结果
 */
class SearchResult {
  constructor({
    id,
    content,
    score,
    embeddingScore,
    rerankerScore,
    metadata = {},
    preview
  }) {
    this.id = id;
    this.content = content;
    this.score = score;
    this.embeddingScore = embeddingScore;
    this.rerankerScore = rerankerScore;
    this.metadata = metadata;
    this.preview = preview || content.substring(0, 100) + '...';
  }
}

/**
 * 记忆对象
 */
class Memory {
  constructor({
    id,
    content,
    embedding = null,
    metadata = {},
    createdAt = new Date(),
    updatedAt = new Date()
  }) {
    this.id = id;
    this.content = content;
    this.embedding = embedding;
    this.metadata = metadata;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }
}

module.exports = {
  EmbeddingProvider,
  RerankProvider,
  RerankResult,
  MemoryService,
  SearchOptions,
  SearchResult,
  Memory
};
