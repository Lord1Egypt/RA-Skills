/**
 * Multi-Path Recall - 多路召回融合
 * 
 * 结合三种检索方式：
 * 1. 语义检索（向量相似度）
 * 2. 关键词检索（BM25）
 * 3. 图检索（知识图谱遍历）
 * 
 * 使用 RRF/Borda/加权融合进行结果融合
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import * as fs from 'fs';
import * as path from 'path';

// ============ 检索结果 ============

export interface RecallResult {
  memoryId: string;
  score: number;
  source: 'semantic' | 'keyword' | 'graph';
  memory: any;
}

export interface FusedResult {
  memoryId: string;
  fusedScore: number;
  sources: Array<{
    source: 'semantic' | 'keyword' | 'graph';
    score: number;
    rank: number;
  }>;
  memory: any;
}

// ============ BM25 关键词检索 ============

export interface BM25Config {
  k1?: number;       // 词频饱和度参数（默认 1.2）
  b?: number;        // 长度归一化参数（默认 0.75）
}

export class BM25Index {
  private config: Required<BM25Config>;
  private documents: Map<string, string>;  // id -> content
  private termFreq: Map<string, Map<string, number>>;  // id -> {term: freq}
  private docFreq: Map<string, number>;  // term -> doc count
  private avgDocLength: number;

  constructor(config: BM25Config = {}) {
    this.config = {
      k1: config.k1 ?? 1.2,
      b: config.b ?? 0.75,
    };
    this.documents = new Map();
    this.termFreq = new Map();
    this.docFreq = new Map();
    this.avgDocLength = 0;
  }

  /**
   * 添加文档
   */
  addDocument(id: string, content: string): void {
    this.documents.set(id, content);

    // 分词（简单中文分词）
    const terms = this.tokenize(content);
    
    // 计算词频
    const tf = new Map<string, number>();
    for (const term of terms) {
      tf.set(term, (tf.get(term) || 0) + 1);
    }
    this.termFreq.set(id, tf);

    // 更新文档频率
    for (const term of tf.keys()) {
      this.docFreq.set(term, (this.docFreq.get(term) || 0) + 1);
    }

    // 更新平均长度
    const totalLength = Array.from(this.documents.values())
      .reduce((sum, doc) => sum + this.tokenize(doc).length, 0);
    this.avgDocLength = totalLength / this.documents.size;
  }

  /**
   * 批量添加文档
   */
  addDocuments(docs: Array<{ id: string; content: string }>): void {
    for (const doc of docs) {
      this.addDocument(doc.id, doc.content);
    }
  }

  /**
   * 检索
   */
  search(query: string, topK: number = 20): Array<{ id: string; score: number }> {
    const queryTerms = this.tokenize(query);
    const scores = new Map<string, number>();

    // BM25 评分
    for (const [docId, content] of this.documents.entries()) {
      const docLength = this.tokenize(content).length;
      let score = 0;

      for (const term of queryTerms) {
        const tf = this.termFreq.get(docId)?.get(term) || 0;
        const df = this.docFreq.get(term) || 0;
        
        if (tf > 0 && df > 0) {
          // IDF
          const idf = Math.log((this.documents.size - df + 0.5) / (df + 0.5) + 1);
          
          // 词频部分
          const numerator = tf * (this.config.k1 + 1);
          const denominator = tf + this.config.k1 * (
            1 - this.config.b + this.config.b * (docLength / this.avgDocLength)
          );
          
          score += idf * (numerator / denominator);
        }
      }

      if (score > 0) {
        scores.set(docId, score);
      }
    }

    // 排序
    const results = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, topK);

    return results.map(([id, score]) => ({ id, score }));
  }

  /**
   * 简单中文分词（按字符）
   * TODO: 集成 jieba 分词
   */
  private tokenize(text: string): string[] {
    // 移除标点，保留中文、英文、数字
    const cleaned = text.replace(/[^\w\u4e00-\u9fa5]/g, ' ');
    
    // 简单分词：中文按字，英文按词
    const terms: string[] = [];
    let currentWord = '';
    
    for (const char of cleaned) {
      if (/[\u4e00-\u9fa5]/.test(char)) {
        // 中文字符：单独成词
        if (currentWord) {
          terms.push(currentWord);
          currentWord = '';
        }
        terms.push(char);
      } else if (/\w/.test(char)) {
        // 英文/数字：累积成词
        currentWord += char;
      } else {
        // 空格/标点：分隔
        if (currentWord) {
          terms.push(currentWord);
          currentWord = '';
        }
      }
    }
    
    if (currentWord) {
      terms.push(currentWord);
    }
    
    return terms.filter(t => t.length > 0);
  }

  /**
   * 删除文档
   */
  removeDocument(id: string): void {
    const content = this.documents.get(id);
    if (!content) return;

    // 更新文档频率
    const tf = this.termFreq.get(id);
    if (tf) {
      for (const term of tf.keys()) {
        const df = this.docFreq.get(term) || 0;
        if (df > 0) {
          this.docFreq.set(term, df - 1);
        }
      }
    }

    this.documents.delete(id);
    this.termFreq.delete(id);

    // 重新计算平均长度
    if (this.documents.size > 0) {
      const totalLength = Array.from(this.documents.values())
        .reduce((sum, doc) => sum + this.tokenize(doc).length, 0);
      this.avgDocLength = totalLength / this.documents.size;
    }
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalDocuments: number;
    totalTerms: number;
    avgDocLength: number;
  } {
    const totalTerms = Array.from(this.docFreq.keys()).length;
    
    return {
      totalDocuments: this.documents.size,
      totalTerms,
      avgDocLength: this.avgDocLength,
    };
  }
}

// ============ 融合排序 ============

export type FusionMethod = 'rrf' | 'borda' | 'weighted' | 'reciprocal';

export interface FusionConfig {
  method?: FusionMethod;
  weights?: {
    semantic?: number;
    keyword?: number;
    graph?: number;
  };
  rrfK?: number;  // RRF 常数（默认 60）
}

export class FusionRanker {
  private config: Required<FusionConfig>;

  constructor(config: FusionConfig = {}) {
    this.config = {
      method: config.method ?? 'rrf',
      weights: {
        semantic: config.weights?.semantic ?? 0.4,
        keyword: config.weights?.keyword ?? 0.3,
        graph: config.weights?.graph ?? 0.3,
      },
      rrfK: config.rrfK ?? 60,
    };
  }

  /**
   * 融合多路检索结果
   */
  fuse(
    semantic: RecallResult[],
    keyword: RecallResult[],
    graph: RecallResult[]
  ): FusedResult[] {
    switch (this.config.method) {
      case 'rrf':
        return this.rrfFusion(semantic, keyword, graph);
      case 'borda':
        return this.bordaFusion(semantic, keyword, graph);
      case 'weighted':
        return this.weightedFusion(semantic, keyword, graph);
      case 'reciprocal':
        return this.reciprocalFusion(semantic, keyword, graph);
      default:
        return this.rrfFusion(semantic, keyword, graph);
    }
  }

  /**
   * RRF (Reciprocal Rank Fusion) - 倒排排名融合
   * 
   * 公式：RRF(d) = Σ 1/(k + rank_i(d))
   * k 是常数（通常 60）
   */
  private rrfFusion(
    semantic: RecallResult[],
    keyword: RecallResult[],
    graph: RecallResult[]
  ): FusedResult[] {
    const fused = new Map<string, FusedResult>();
    const k = this.config.rrfK;

    // 合并所有结果
    const allResults = [
      { source: 'semantic' as const, results: semantic },
      { source: 'keyword' as const, results: keyword },
      { source: 'graph' as const, results: graph },
    ];

    for (const { source, results } of allResults) {
      for (let rank = 0; rank < results.length; rank++) {
        const result = results[rank];
        
        if (!fused.has(result.memoryId)) {
          fused.set(result.memoryId, {
            memoryId: result.memoryId,
            fusedScore: 0,
            sources: [],
            memory: result.memory,
          });
        }

        const fusedResult = fused.get(result.memoryId)!;
        
        // RRF 评分
        const rrfScore = 1 / (k + rank + 1);
        fusedResult.fusedScore += rrfScore;

        // 记录来源
        fusedResult.sources.push({
          source,
          score: result.score,
          rank: rank + 1,
        });
      }
    }

    // 按融合评分排序
    return Array.from(fused.values())
      .sort((a, b) => b.fusedScore - a.fusedScore);
  }

  /**
   * Borda Count - 波达计数法
   * 
   * 公式：Borda(d) = Σ (N - rank_i(d))
   * N 是候选集大小
   */
  private bordaFusion(
    semantic: RecallResult[],
    keyword: RecallResult[],
    graph: RecallResult[]
  ): FusedResult[] {
    const fused = new Map<string, FusedResult>();
    const allResults = [
      { source: 'semantic' as const, results: semantic },
      { source: 'keyword' as const, results: keyword },
      { source: 'graph' as const, results: graph },
    ];

    for (const { source, results } of allResults) {
      const n = results.length;
      
      for (let rank = 0; rank < results.length; rank++) {
        const result = results[rank];
        
        if (!fused.has(result.memoryId)) {
          fused.set(result.memoryId, {
            memoryId: result.memoryId,
            fusedScore: 0,
            sources: [],
            memory: result.memory,
          });
        }

        const fusedResult = fused.get(result.memoryId)!;
        
        // Borda 评分
        const bordaScore = n - rank;
        fusedResult.fusedScore += bordaScore;

        fusedResult.sources.push({
          source,
          score: result.score,
          rank: rank + 1,
        });
      }
    }

    return Array.from(fused.values())
      .sort((a, b) => b.fusedScore - a.fusedScore);
  }

  /**
   * 加权融合
   * 
   * 公式：Score(d) = w1*semantic + w2*keyword + w3*graph
   */
  private weightedFusion(
    semantic: RecallResult[],
    keyword: RecallResult[],
    graph: RecallResult[]
  ): FusedResult[] {
    const fused = new Map<string, FusedResult>();
    const weights = this.config.weights;

    const allResults = [
      { source: 'semantic' as const, results: semantic, weight: weights.semantic },
      { source: 'keyword' as const, results: keyword, weight: weights.keyword },
      { source: 'graph' as const, results: graph, weight: weights.graph },
    ];

    for (const { source, results, weight } of allResults) {
      for (let rank = 0; rank < results.length; rank++) {
        const result = results[rank];
        
        if (!fused.has(result.memoryId)) {
          fused.set(result.memoryId, {
            memoryId: result.memoryId,
            fusedScore: 0,
            sources: [],
            memory: result.memory,
          });
        }

        const fusedResult = fused.get(result.memoryId)!;
        
        // 加权评分
        const weightedScore = result.score * (weight ?? 0.33);
        fusedResult.fusedScore += weightedScore;

        fusedResult.sources.push({
          source,
          score: result.score,
          rank: rank + 1,
        });
      }
    }

    return Array.from(fused.values())
      .sort((a, b) => b.fusedScore - a.fusedScore);
  }

  /**
   * 倒数融合（简化版 RRF）
   */
  private reciprocalFusion(
    semantic: RecallResult[],
    keyword: RecallResult[],
    graph: RecallResult[]
  ): FusedResult[] {
    const fused = new Map<string, FusedResult>();
    const allResults = [
      { source: 'semantic' as const, results: semantic },
      { source: 'keyword' as const, results: keyword },
      { source: 'graph' as const, results: graph },
    ];

    for (const { source, results } of allResults) {
      for (let rank = 0; rank < results.length; rank++) {
        const result = results[rank];
        
        if (!fused.has(result.memoryId)) {
          fused.set(result.memoryId, {
            memoryId: result.memoryId,
            fusedScore: 0,
            sources: [],
            memory: result.memory,
          });
        }

        const fusedResult = fused.get(result.memoryId)!;
        
        // 倒数评分
        const reciprocalScore = 1 / (rank + 1);
        fusedResult.fusedScore += reciprocalScore;

        fusedResult.sources.push({
          source,
          score: result.score,
          rank: rank + 1,
        });
      }
    }

    return Array.from(fused.values())
      .sort((a, b) => b.fusedScore - a.fusedScore);
  }

  /**
   * 更新权重
   */
  updateWeights(weights: { semantic?: number; keyword?: number; graph?: number }): void {
    if (weights.semantic !== undefined) {
      this.config.weights.semantic = weights.semantic;
    }
    if (weights.keyword !== undefined) {
      this.config.weights.keyword = weights.keyword;
    }
    if (weights.graph !== undefined) {
      this.config.weights.graph = weights.graph;
    }

    // 归一化
    const total = (this.config.weights.semantic ?? 0.33) + 
                  (this.config.weights.keyword ?? 0.33) + 
                  (this.config.weights.graph ?? 0.34);
    
    if (total > 0) {
      this.config.weights.semantic = (this.config.weights.semantic ?? 0.33) / total;
      this.config.weights.keyword = (this.config.weights.keyword ?? 0.33) / total;
      this.config.weights.graph = (this.config.weights.graph ?? 0.34) / total;
    }
  }
}

// ============ 多路召回管理器 ============

export interface MultiPathRecallConfig {
  basePath?: string;
  fusionMethod?: FusionMethod;
  weights?: {
    semantic?: number;
    keyword?: number;
    graph?: number;
  };
}

export class MultiPathRecallManager {
  private config: MultiPathRecallConfig & {
    basePath: string;
    fusionMethod: FusionMethod;
    weights: {
      semantic: number;
      keyword: number;
      graph: number;
    };
  };
  private bm25Index: BM25Index;
  private fusionRanker: FusionRanker;
  private memoryStore: Map<string, any>;  // 临时存储，实际应该用 LayeredMemoryManager

  constructor(config: MultiPathRecallConfig = {}) {
    this.config = {
      basePath: config.basePath ?? 'memory/multi-path-recall',
      fusionMethod: config.fusionMethod ?? 'rrf',
      weights: {
        semantic: config.weights?.semantic ?? 0.4,
        keyword: config.weights?.keyword ?? 0.3,
        graph: config.weights?.graph ?? 0.3,
      },
    };

    this.bm25Index = new BM25Index();
    this.fusionRanker = new FusionRanker({
      method: this.config.fusionMethod,
      weights: {
        semantic: this.config.weights.semantic ?? 0.4,
        keyword: this.config.weights.keyword ?? 0.3,
        graph: this.config.weights.graph ?? 0.3,
      },
    });
    this.memoryStore = new Map();

    // 确保目录存在
    if (!fs.existsSync(this.config.basePath)) {
      fs.mkdirSync(this.config.basePath, { recursive: true });
    }
  }

  /**
   * 添加记忆
   */
  async addMemory(id: string, content: string, memory: any): Promise<void> {
    this.memoryStore.set(id, memory);
    this.bm25Index.addDocument(id, content);
  }

  /**
   * 批量添加记忆
   */
  async addMemories(memories: Array<{ id: string; content: string; memory: any }>): Promise<void> {
    for (const m of memories) {
      await this.addMemory(m.id, m.content, m.memory);
    }
  }

  /**
   * 多路召回
   */
  async recall(
    query: string,
    options: {
      topK?: number;
      useSemantic?: boolean;
      useKeyword?: boolean;
      useGraph?: boolean;
    } = {}
  ): Promise<FusedResult[]> {
    const {
      topK = 20,
      useSemantic = true,
      useKeyword = true,
      useGraph = true,
    } = options;

    const results: {
      semantic: RecallResult[];
      keyword: RecallResult[];
      graph: RecallResult[];
    } = {
      semantic: [],
      keyword: [],
      graph: [],
    };

    // 1. 关键词检索（BM25）
    if (useKeyword) {
      const bm25Results = this.bm25Index.search(query, topK * 2);
      results.keyword = bm25Results.map(r => ({
        memoryId: r.id,
        score: r.score,
        source: 'keyword' as const,
        memory: this.memoryStore.get(r.id),
      }));
    }

    // 2. 语义检索（TODO: 向量检索）
    if (useSemantic) {
      // 暂时用 BM25 模拟语义检索
      // 实际应该用向量相似度
      results.semantic = results.keyword.slice(0, topK);
    }

    // 3. 图检索（TODO: 知识图谱）
    if (useGraph) {
      // 暂时返回空结果
      // 实际应该用 KnowledgeGraph 检索
      results.graph = [];
    }

    // 4. 融合排序
    const fused = this.fusionRanker.fuse(
      results.semantic,
      results.keyword,
      results.graph
    );

    // 5. 返回 Top-K
    return fused.slice(0, topK);
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalMemories: number;
    bm25Stats: {
      totalDocuments: number;
      totalTerms: number;
      avgDocLength: number;
    };
    fusionMethod: FusionMethod;
    weights: {
      semantic: number;
      keyword: number;
      graph: number;
    };
  } {
    return {
      totalMemories: this.memoryStore.size,
      bm25Stats: this.bm25Index.getStats(),
      fusionMethod: this.config.fusionMethod,
      weights: this.config.weights,
    };
  }

  /**
   * 更新融合权重
   */
  updateWeights(weights: { semantic?: number; keyword?: number; graph?: number }): void {
    this.fusionRanker.updateWeights(weights);
  }
}
