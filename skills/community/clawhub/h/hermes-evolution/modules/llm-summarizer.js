/**
 * LLMSummarizer - P2-2 LLM自动摘要
 * 检索后摘要再注入，减少Token开销
 * 
 * 核心思路：
 * 1. 大量检索结果 → LLM摘要
 * 2. 摘要注入上下文，而非完整内容
 * 3. 支持多种摘要策略
 */

const fs = require('fs');
const path = require('path');

/**
 * 摘要策略
 */
const SummaryStrategy = {
  EXTRACTIVE: 'extractive',     // 抽取式：提取关键句子
  ABSTRACTIVE: 'abstractive',   // 生成式：理解后生成
  STRUCTURED: 'structured',     // 结构化：提取关键字段
  HYBRID: 'hybrid'              // 混合：抽取+生成
};

/**
 * 摘要配置
 */
const DEFAULT_CONFIG = {
  strategy: SummaryStrategy.HYBRID,
  maxLength: 500,        // 最大Token数
  maxSentences: 5,       // 最大句子数
  includeKeywords: true,  // 包含关键词
  includeEntities: true,  // 包含实体
  confidenceThreshold: 0.7  // 置信度阈值
};

/**
 * LLM 摘要器
 */
class LLMSummarizer {
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    this.summaryCache = new Map();  // contentHash → summary
    this.stats = {
      totalSummaries: 0,
      cachedHits: 0,
      avgReduction: 0  // 平均压缩比
    };
  }

  /**
   * 生成摘要
   * @param {string} content - 原始内容
   * @param {Object} context - 上下文信息（用于提示）
   * @returns {Object} 摘要结果
   */
  async summarize(content, context = {}) {
    if (!content || content.length < 100) {
      return {
        original: content,
        summary: content,
        reduced: false,
        tokenReduction: 0
      };
    }

    // 检查缓存
    const contentHash = this.hashContent(content);
    if (this.summaryCache.has(contentHash)) {
      this.stats.cachedHits++;
      const cached = this.summaryCache.get(contentHash);
      return { ...cached, fromCache: true };
    }

    // 根据策略生成摘要
    let summary;
    switch (this.config.strategy) {
      case SummaryStrategy.EXTRACTIVE:
        summary = this.extractiveSummary(content);
        break;
      case SummaryStrategy.ABSTRACTIVE:
        summary = await this.abstractiveSummary(content, context);
        break;
      case SummaryStrategy.STRUCTURED:
        summary = this.structuredSummary(content, context);
        break;
      case SummaryStrategy.HYBRID:
      default:
        summary = this.hybridSummary(content, context);
    }

    // 计算压缩比
    const originalTokens = this.estimateTokens(content);
    const summaryTokens = this.estimateTokens(summary.text);
    const reduction = (1 - summaryTokens / originalTokens) * 100;

    const result = {
      original: content.substring(0, 200) + (content.length > 200 ? '...' : ''),
      summary: summary.text,
      reduced: reduction > 20,
      tokenReduction: Math.round(reduction),
      originalTokens,
      summaryTokens,
      strategy: this.config.strategy,
      keywords: summary.keywords || [],
      entities: summary.entities || [],
      fromCache: false,
      timestamp: new Date().toISOString()
    };

    // 缓存
    this.summaryCache.set(contentHash, {
      summary: result.summary,
      reduced: result.reduced,
      tokenReduction: result.tokenReduction,
      originalTokens: result.originalTokens,
      summaryTokens: result.summaryTokens
    });
    this.stats.totalSummaries++;
    this.updateAvgReduction(reduction);

    return result;
  }

  /**
   * 抽取式摘要
   */
  extractiveSummary(content) {
    // 简单实现：提取关键句子
    const sentences = this.splitSentences(content);
    
    // 按句子位置和长度打分
    const scored = sentences.map((s, i) => ({
      text: s,
      score: (1 / (i + 1)) * 0.5 + (s.length / 100) * 0.3 + (i === 0 ? 0.2 : 0)
    }));

    // 选择高分句子
    scored.sort((a, b) => b.score - a.score);
    const selected = scored.slice(0, this.config.maxSentences)
      .sort((a, b) => a.text.localeCompare(b.text))
      .map(s => s.text);

    return {
      text: selected.join('。'),
      keywords: this.extractKeywords(selected.join(''))
    };
  }

  /**
   * 生成式摘要（模拟，需要LLM API）
   */
  async abstractiveSummary(content, context = {}) {
    // 这里是模拟实现，实际需要调用 LLM API
    // 真实实现会调用如 OpenAI GPT, Claude 等
    
    // 模拟：生成简短总结
    const sentences = this.splitSentences(content);
    const firstSentence = sentences[0] || '';
    const lastSentence = sentences[sentences.length - 1] || '';
    
    return {
      text: `概述：${firstSentence}。${lastSentence}`,
      keywords: this.extractKeywords(content)
    };
  }

  /**
   * 结构化摘要
   */
  structuredSummary(content, context) {
    const keywords = this.extractKeywords(content);
    const entities = this.extractEntities(content);
    const stats = this.computeStats(content);
    
    return {
      text: `主题：${context.topic || '未知'}\n关键词：${keywords.slice(0, 5).join(', ')}\n实体：${entities.slice(0, 3).join(', ')}\n统计：字数${stats.charCount}，句子${stats.sentenceCount}`,
      keywords,
      entities
    };
  }

  /**
   * 混合摘要
   */
  hybridSummary(content, context = {}) {
    // 1. 提取关键词和实体
    const keywords = this.extractKeywords(content);
    const entities = this.extractEntities(content);
    
    // 2. 抽取关键句子
    const extractive = this.extractiveSummary(content);
    
    // 3. 如果太长，进一步压缩
    let text = extractive.text;
    if (this.estimateTokens(text) > this.config.maxLength) {
      // 截断到最大长度
      text = this.truncateToToken(text, this.config.maxLength);
    }
    
    // 4. 添加结构化信息
    if (this.config.includeKeywords && keywords.length > 0) {
      text += `\n\n关键词: ${keywords.slice(0, 5).join(', ')}`;
    }
    
    if (this.config.includeEntities && entities.length > 0) {
      text += `\n关键实体: ${entities.slice(0, 3).join(', ')}`;
    }
    
    return {
      text: text || '',
      keywords: keywords || [],
      entities: entities || []
    };
  }

  /**
   * 提取关键词
   */
  extractKeywords(content) {
    // 简单实现：词频统计
    const words = content.split(/[\s，。、！？；：""''【】（）：,.!?;:'"()[\]]+/);
    const freq = new Map();
    
    for (const word of words) {
      if (word.length >= 2) {
        freq.set(word, (freq.get(word) || 0) + 1);
      }
    }
    
    // 排序并返回前10
    return Array.from(freq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([w]) => w);
  }

  /**
   * 提取实体（简单实现）
   */
  extractEntities(content) {
    // 简单实现：识别特定模式
    const entities = [];
    
    // 识别 @提及
    const mentions = content.match(/@[a-zA-Z]+/g);
    if (mentions) entities.push(...mentions);
    
    // 识别话题标签
    const hashtags = content.match(/#[\u4e00-\u9fa5a-zA-Z0-9]+/g);
    if (hashtags) entities.push(...hashtags);
    
    // 识别 URL
    const urls = content.match(/https?:\/\/[^\s]+/g);
    if (urls) entities.push(...urls);
    
    return [...new Set(entities)];
  }

  /**
   * 计算统计信息
   */
  computeStats(content) {
    const sentences = this.splitSentences(content);
    return {
      charCount: content.length,
      sentenceCount: sentences.length,
      avgSentenceLength: Math.round(content.length / sentences.length)
    };
  }

  /**
   * 分割句子
   */
  splitSentences(content) {
    return content.split(/[。！？.!?]+/).filter(s => s.trim().length > 0);
  }

  /**
   * 截断到指定Token数
   */
  truncateToToken(text, maxTokens) {
    const tokens = this.estimateTokens(text);
    if (tokens <= maxTokens) return text;
    
    // 简单截断
    const charsPerToken = 2;  // 估算
    const maxChars = maxTokens * charsPerToken;
    return text.substring(0, maxChars) + '...';
  }

  /**
   * 估算Token数
   */
  estimateTokens(text) {
    if (!text) return 0;
    const chinese = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const english = (text.match(/[a-zA-Z]/g) || []).length;
    return chinese + Math.ceil(english / 4);
  }

  /**
   * 内容哈希
   */
  hashContent(content) {
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }

  /**
   * 更新平均压缩比
   */
  updateAvgReduction(reduction) {
    const n = this.stats.totalSummaries;
    this.stats.avgReduction = (this.stats.avgReduction * (n - 1) + reduction) / n;
  }

  /**
   * 批量摘要
   */
  async summarizeBatch(contents, context = {}) {
    const results = [];
    
    for (const content of contents) {
      const result = await this.summarize(content, context);
      results.push(result);
    }
    
    return results;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      cacheSize: this.summaryCache.size
    };
  }

  /**
   * 打印统计
   */
  printStats() {
    const s = this.stats;
    console.log('\n📊 LLMSummarizer 统计');
    console.log('═'.repeat(40));
    console.log(`总摘要数: ${s.totalSummaries}`);
    console.log(`缓存命中: ${s.cachedHits}`);
    console.log(`平均压缩比: ${s.avgReduction.toFixed(1)}%`);
    console.log(`缓存大小: ${s.cacheSize}`);
    console.log('═'.repeat(40));
  }
}

// 导出
module.exports = {
  LLMSummarizer,
  SummaryStrategy,
  DEFAULT_CONFIG
};
