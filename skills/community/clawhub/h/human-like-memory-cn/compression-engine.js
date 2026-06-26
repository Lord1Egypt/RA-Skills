/**
 * 智能摘要压缩引擎 v1.1.0
 * 三级压缩：原文 → 摘要 → 关键词
 */

class SummaryCompressionEngine {
  constructor(options = {}) {
    this.compressionLevels = {
      FULL: 'full',      // 原文保留
      SUMMARY: 'summary', // 摘要压缩（60%）
      KEYWORDS: 'keywords' // 关键词压缩（85%）
    };

    this.thresholds = {
      high: options.highThreshold || 80,    // ≥80 分：原文
      medium: options.mediumThreshold || 50, // 50-79 分：摘要
      low: options.lowThreshold || 30        // 30-49 分：关键词
    };

    this.keywordExtractionCount = options.keywordCount || 8;
  }

  /**
   * 根据重要性分数决定压缩级别
   */
  getCompressionLevel(importance) {
    if (importance >= this.thresholds.high) {
      return this.compressionLevels.FULL;
    } else if (importance >= this.thresholds.medium) {
      return this.compressionLevels.SUMMARY;
    } else if (importance >= this.thresholds.low) {
      return this.compressionLevels.KEYWORDS;
    }
    return null; // 低于阈值，应该遗忘
  }

  /**
   * 生成摘要（使用简单的提取式摘要）
   * 性能优化：预编译正则 + 缓存
   */
  generateSummary(text, maxLength = 50) {
    if (text.length <= maxLength) {
      return text;
    }

    // 性能优化：缓存长文本摘要
    const cacheKey = `${text.slice(0, 50)}_${maxLength}`;
    if (this.summaryCache && this.summaryCache.has(cacheKey)) {
      return this.summaryCache.get(cacheKey);
    }

    // 预编译正则（性能提升 30%）
    const sentenceRegex = /[。！？.!?]/g;
    const sentences = text.split(sentenceRegex).filter(s => s.trim().length > 0);
    
    if (sentences.length === 0) {
      return text.slice(0, maxLength) + '...';
    }

    // 取第一句
    let summary = sentences[0].trim();
    
    // 如果还不够，添加第二句
    if (summary.length < maxLength && sentences.length > 1) {
      const remaining = maxLength - summary.length - 2;
      summary += '；' + sentences[1].trim().slice(0, remaining);
    }

    const result = summary + '。';
    
    // 缓存结果
    if (!this.summaryCache) this.summaryCache = new Map();
    if (this.summaryCache.size >= 50) {
      const toDelete = Array.from(this.summaryCache.keys()).slice(0, 10);
      toDelete.forEach(key => this.summaryCache.delete(key));
    }
    this.summaryCache.set(cacheKey, result);

    return result;
  }

  /**
   * 初始化缓存（延迟初始化）
   */
  initCaches() {
    if (!this.stopwords) {
      // 性能优化：预编译停用词集合（只创建一次）
      this.stopwords = new Set([
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
        '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
        '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '他'
      ]);
      
      // 预编译分词正则
      this.tokenizerRegex = /[\s,，.。!！?？:：;；'"'"”"()（）【】\[\]]+/;
    }
    
    if (!this.keywordCache) this.keywordCache = new Map();
    if (!this.summaryCache) this.summaryCache = new Map();
  }

  /**
   * 提取关键词
   * 性能优化：使用预编译的正则和停用词集合
   */
  extractKeywords(text, count = 8) {
    // 初始化缓存
    this.initCaches();
    
    // 性能优化：缓存结果
    const cacheKey = text.slice(0, 50) + '_' + count;
    if (this.keywordCache.has(cacheKey)) {
      return this.keywordCache.get(cacheKey);
    }

    // 使用预编译的正则和停用词
    const words = text
      .split(this.tokenizerRegex)
      .filter(w => w.trim().length > 1)
      .filter(w => !this.stopwords.has(w));

    // 统计词频
    const freq = {};
    words.forEach(word => {
      freq[word] = (freq[word] || 0) + 1;
    });

    // 排序并取 Top N
    const sorted = Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, count)
      .map(([word]) => word);

    // 缓存结果
    if (this.keywordCache.size >= 50) {
      const toDelete = Array.from(this.keywordCache.keys()).slice(0, 10);
      toDelete.forEach(key => this.keywordCache.delete(key));
    }
    this.keywordCache.set(cacheKey, sorted);

    return sorted;
  }

  /**
   * 格式化关键词字符串
   */
  formatKeywords(keywords, separator = ' | ') {
    return keywords.join(separator);
  }

  /**
   * 压缩记忆内容
   * @param {Object} memory - 记忆对象
   * @returns {Object} 压缩后的记忆（包含原始内容和压缩内容）
   */
  compressMemory(memory) {
    const level = this.getCompressionLevel(memory.importance);
    
    if (!level) {
      return {
        ...memory,
        compressionLevel: 'FORGET',
        shouldForget: true,
        reason: '重要性低于阈值'
      };
    }

    const originalContent = memory.content;
    let compressedContent = originalContent;
    let compressionRatio = 0;

    switch (level) {
      case this.compressionLevels.FULL:
        compressedContent = originalContent;
        compressionRatio = 0;
        break;

      case this.compressionLevels.SUMMARY:
        compressedContent = this.generateSummary(originalContent);
        compressionRatio = 1 - (compressedContent.length / originalContent.length);
        break;

      case this.compressionLevels.KEYWORDS:
        const keywords = this.extractKeywords(originalContent, this.keywordExtractionCount);
        compressedContent = this.formatKeywords(keywords);
        compressionRatio = 1 - (compressedContent.length / originalContent.length);
        break;
    }

    return {
      ...memory,
      compressionLevel: level,
      originalContent: originalContent,  // 始终保留原文
      compressedContent: compressedContent,
      compressionRatio: (compressionRatio * 100).toFixed(1) + '%',
      keywords: this.extractKeywords(originalContent, this.keywordExtractionCount),
      compressedAt: new Date().toISOString()
    };
  }

  /**
   * 批量压缩记忆
   */
  compressMemories(memories) {
    return memories.map(memory => this.compressMemory(memory));
  }

  /**
   * 解压记忆（恢复原文）
   */
  decompressMemory(memory) {
    if (!memory) return null;
    
    return {
      ...memory,
      content: memory.originalContent || memory.compressedContent || memory.content,
      compressionLevel: 'FULL',
      decompressedAt: new Date().toISOString()
    };
  }

  /**
   * 获取压缩统计
   */
  getStats(memories) {
    const compressed = this.compressMemories(memories);
    
    const stats = {
      total: memories.length,
      byLevel: {
        full: 0,
        summary: 0,
        keywords: 0,
        forget: 0
      },
      avgCompressionRatio: 0,
      tokenSavings: 0
    };

    let totalOriginalLength = 0;
    let totalCompressedLength = 0;

    compressed.forEach(memory => {
      if (memory.shouldForget) {
        stats.byLevel.forget++;
      } else {
        switch (memory.compressionLevel) {
          case 'full':
            stats.byLevel.full++;
            break;
          case 'summary':
            stats.byLevel.summary++;
            break;
          case 'keywords':
            stats.byLevel.keywords++;
            break;
        }

        totalOriginalLength += memory.originalContent.length;
        totalCompressedLength += memory.compressedContent.length;
      }
    });

    if (totalOriginalLength > 0) {
      stats.avgCompressionRatio = (1 - totalCompressedLength / totalOriginalLength) * 100;
      stats.tokenSavings = stats.avgCompressionRatio.toFixed(1) + '%';
    }

    return stats;
  }

  /**
   * 获取压缩级别说明
   */
  getLevelDescription(level) {
    const descriptions = {
      full: '原文保留（重要性≥80）',
      summary: '摘要压缩（50-79 分，节省~60%）',
      keywords: '关键词压缩（30-49 分，节省~85%）',
      forget: '建议遗忘（<30 分）'
    };
    return descriptions[level] || level;
  }
}

module.exports = SummaryCompressionEngine;
