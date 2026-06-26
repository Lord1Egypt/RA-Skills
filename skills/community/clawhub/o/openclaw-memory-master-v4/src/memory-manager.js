/**
 * Memory-Master v4.2.0 - 统一记忆管理器
 * 整合 4 类记忆模型、时间树结构、5 种检索类型、迭代压缩
 * 
 * @version 4.2.0
 * @date 2026-04-11
 * @features:
 *   - 迭代压缩 (Hermes Agent 启发)
 *   - Lineage 谱系追踪
 *   - 结构化摘要模板
 */

const fs = require('fs');
const path = require('path');

const { MemoryTypes, MemoryTypeClassifier } = require('./memory-classifier');
const { TimeTree } = require('./time-tree');
const { QueryTypes, QueryClassifier } = require('./query-classifier');
const { AAAKIterativeCompressor } = require('./compressors/aaak-iterative-compressor');

class MemoryManager {
  constructor(config = {}) {
    this.config = {
      baseDir: config.baseDir || path.join(process.cwd(), 'memory'),
      autoIndex: config.autoIndex !== false,
      compression: config.compression || false
    };

    // 初始化子模块
    this.typeClassifier = new MemoryTypeClassifier();
    this.timeTree = new TimeTree(path.join(this.config.baseDir, 'time-tree'));
    this.queryClassifier = new QueryClassifier();
    
    // 初始化迭代压缩器 (v4.2.0 新增)
    this.compressor = new AAAKIterativeCompressor({
      maxLength: config.compressionMaxLength || 2000,
      targetCompressionRatio: config.compressionRatio || 0.6,
    });

    // 确保目录结构
    this.ensureDirectoryStructure();

    // 缓存
    this.cache = {
      memories: new Map(),
      indexes: new Map()
    };

    // 统计
    this.stats = {
      totalMemories: 0,
      byType: {},
      queries: 0
    };
  }

  /**
   * 确保目录结构存在
   */
  ensureDirectoryStructure() {
    const dirs = [
      this.config.baseDir,
      path.join(this.config.baseDir, 'daily'),
      path.join(this.config.baseDir, 'knowledge'),
      path.join(this.config.baseDir, 'time-tree'),
      path.join(this.config.baseDir, 'indexes')
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  /**
   * 存储记忆
   * @param {string} content - 记忆内容
   * @param {object} options - 选项
   * @returns {object} 存储结果
   */
  store(content, options = {}) {
    const timestamp = options.timestamp || Date.now();
    const memoryId = options.id || this.generateId();
    const memoryDate = new Date(timestamp);

    // 1. 分类记忆类型
    const classification = this.typeClassifier.classify(content, options.context);

    // 2. 提取时间信息
    const timeRange = this.timeTree.extractTimeRange(content, memoryDate);

    // 3. 创建记忆对象
    const memory = {
      id: memoryId,
      content,
      type: classification.type,
      typeName: classification.typeName,
      confidence: classification.confidence,
      timestamp,
      date: memoryDate.toISOString(),
      timeRange: timeRange,
      metadata: {
        wordCount: content.length,
        lineCount: content.split('\n').length,
        tags: options.tags || [],
        source: options.source || 'manual'
      }
    };

    // 4. 存储到文件
    const filePath = this.getMemoryFilePath(memory, memoryDate);
    this.writeMemoryToFile(filePath, memory);

    // 5. 更新索引
    if (this.config.autoIndex) {
      this.updateIndexes(memory, filePath);
    }

    // 6. 存储到时间树
    this.timeTree.storeMemory(memoryId, memory, memoryDate);

    // 7. 更新缓存
    this.cache.memories.set(memoryId, memory);

    // 8. 更新统计
    this.stats.totalMemories++;
    this.stats.byType[classification.type] = (this.stats.byType[classification.type] || 0) + 1;

    return {
      success: true,
      memoryId,
      type: classification.type,
      typeName: classification.typeName,
      filePath,
      confidence: classification.confidence
    };
  }

  /**
   * 生成记忆 ID
   */
  generateId() {
    return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 获取记忆文件路径
   */
  getMemoryFilePath(memory, memoryDate) {
    const dateStr = memoryDate.toISOString().split('T')[0];
    const typePrefix = {
      [MemoryTypes.EPISODIC]: 'episodic',
      [MemoryTypes.SEMANTIC]: 'semantic',
      [MemoryTypes.PROCEDURAL]: 'procedural',
      [MemoryTypes.PERSONA]: 'persona'
    }[memory.type] || 'daily';

    return path.join(this.config.baseDir, 'daily', `${dateStr}_${typePrefix}_${memory.id.substring(4, 12)}.md`);
  }

  /**
   * 写入记忆到文件
   */
  writeMemoryToFile(filePath, memory) {
    const content = `---
id: ${memory.id}
type: ${memory.type}
typeName: ${memory.typeName}
timestamp: ${memory.timestamp}
date: ${memory.date}
confidence: ${memory.confidence.toFixed(3)}
---

${memory.content}
`;

    fs.writeFileSync(filePath, content, 'utf8');
  }

  /**
   * 更新索引
   */
  updateIndexes(memory, filePath) {
    const indexPath = path.join(this.config.baseDir, 'indexes', 'master-index.json');
    let index = { memories: [], lastUpdated: Date.now() };

    if (fs.existsSync(indexPath)) {
      index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
    }

    // 添加新记忆到索引
    index.memories.push({
      id: memory.id,
      type: memory.type,
      date: memory.date,
      filePath,
      preview: memory.content.substring(0, 100)
    });

    fs.writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf8');
  }

  /**
   * 压缩记忆 (v4.2.0 新增)
   * @param {string} memoryId - 记忆 ID
   * @param {object} options - 选项
   * @returns {object} 压缩结果
   */
  async compressMemory(memoryId, options = {}) {
    const memory = this.cache.memories.get(memoryId);
    if (!memory) {
      throw new Error(`Memory ${memoryId} not found`);
    }

    // 检查是否需要压缩
    if (memory.content.length < (options.minLength || 1000)) {
      return {
        success: false,
        reason: 'Content too short',
        memoryId
      };
    }

    // 查找父记忆的摘要 (用于迭代压缩)
    const parentSummary = options.parentMemoryId
      ? await this.getMemorySummary(options.parentMemoryId)
      : null;

    // 执行压缩
    const compressionResult = await this.compressor.compress(
      memory.content,
      parentSummary,
      options.parentMemoryId
    );

    // 更新记忆对象
    memory.summary = compressionResult.summary;
    memory.compressionRatio = compressionResult.compressionRatio;
    memory.isIterativeCompression = compressionResult.isIterative;
    memory.compressionChain = compressionResult.lineageChain;
    memory.lastCompressedSummary = parentSummary;
    memory.compressionTemplate = compressionResult.metadata.template;

    // 更新缓存
    this.cache.memories.set(memoryId, memory);

    // 更新文件
    const filePath = this.getMemoryFilePath(memory, new Date(memory.timestamp));
    this.writeMemoryToFile(filePath, memory);

    return {
      success: true,
      memoryId,
      summary: compressionResult.summary,
      compressionRatio: compressionResult.compressionRatio,
      isIterative: compressionResult.isIterative,
      lineageChain: compressionResult.lineageChain,
      metadata: compressionResult.metadata
    };
  }

  /**
   * 批量压缩 (v4.2.0 新增)
   * @param {array} memoryIds - 记忆 ID 列表
   * @param {object} options - 选项
   * @returns {array} 压缩结果
   */
  async compressMemoriesBatch(memoryIds, options = {}) {
    const results = [];

    for (const memoryId of memoryIds) {
      try {
        const result = await this.compressMemory(memoryId, options);
        results.push(result);
        
        // 延迟避免速率限制
        if (options.delayMs) {
          await new Promise(resolve => setTimeout(resolve, options.delayMs));
        }
      } catch (error) {
        results.push({
          success: false,
          memoryId,
          error: error.message
        });
      }
    }

    return {
      total: memoryIds.length,
      success: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      results
    };
  }

  /**
   * 获取记忆摘要 (v4.2.0 新增)
   */
  async getMemorySummary(memoryId) {
    const memory = this.cache.memories.get(memoryId);
    if (!memory) {
      return null;
    }
    
    // 如果已经有摘要，直接返回
    if (memory.summary) {
      return memory.summary;
    }

    // 否则实时压缩
    const result = await this.compressMemory(memoryId);
    return result.success ? result.summary : null;
  }

  /**
   * 查询记忆
   * @param {string} query - 查询文本
   * @param {object} options - 选项
   * @returns {array} 查询结果
   */
  query(query, options = {}) {
    this.stats.queries++;

    // 1. 分类查询类型
    const queryClassification = this.queryClassifier.classify(query, options.context);

    // 2. 提取时间范围（如果有）
    const timeRange = this.timeTree.extractTimeRange(query);

    // 3. 根据查询类型选择搜索策略
    const results = this.executeSearch(query, queryClassification, timeRange, options);

    // 4. 格式化结果
    const formattedResults = this.queryClassifier.formatResults(results, queryClassification.type);

    return {
      query,
      queryType: queryClassification.type,
      queryTypeName: queryClassification.typeName,
      timeRange,
      results: formattedResults,
      count: formattedResults.length,
      confidence: queryClassification.confidence
    };
  }

  /**
   * 执行搜索
   */
  executeSearch(query, queryClassification, timeRange, options) {
    const results = [];
    const memoryTypes = queryClassification.memoryTypes;

    // 读取索引文件
    const indexPath = path.join(this.config.baseDir, 'indexes', 'master-index.json');
    if (!fs.existsSync(indexPath)) {
      return [];
    }

    const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));

    // 过滤和评分
    for (const memIndex of index.memories) {
      // 类型过滤
      if (memoryTypes.length > 0 && !memoryTypes.includes(memIndex.type)) {
        continue;
      }

      // 时间过滤
      if (timeRange) {
        const memDate = new Date(memIndex.date);
        if (memDate < timeRange.start || memDate > timeRange.end) {
          continue;
        }
      }

      // 内容匹配评分
      const score = this.scoreMemoryMatch(query, memIndex, queryClassification);
      
      if (score > 0) {
        results.push({
          ...memIndex,
          score,
          matchType: this.getMatchType(query, memIndex)
        });
      }
    }

    // 按分数排序
    results.sort((a, b) => b.score - a.score);

    // 限制结果数量
    const limit = options.limit || 10;
    return results.slice(0, limit);
  }

  /**
   * 评分记忆匹配度
   */
  scoreMemoryMatch(query, memory, queryClassification) {
    let score = 0;

    // 读取记忆内容
    try {
      const content = fs.readFileSync(memory.filePath, 'utf8');
      
      // 关键词匹配
      const queryWords = query.toLowerCase().split(/\s+/);
      for (const word of queryWords) {
        if (word.length > 1 && content.toLowerCase().includes(word)) {
          score += 1.0;
        }
      }

      // 查询类型特定评分
      switch (queryClassification.type) {
        case QueryTypes.FLOW:
          if (/步骤 | 流程 | 方法/.test(content)) {
            score += 2.0;
          }
          break;
        case QueryTypes.TEMPORAL:
          if (/\d{4}-\d{2}-\d{2}/.test(content)) {
            score += 1.5;
          }
          break;
        case QueryTypes.RELATIONAL:
          if (/关联 | 关系 | 相关/.test(content)) {
            score += 1.5;
          }
          break;
        case QueryTypes.PREFERENCE:
          if (/喜欢 | 偏好 | 习惯/.test(content)) {
            score += 2.0;
          }
          break;
        case QueryTypes.FACTUAL:
          if (/定义 | 是 | 指/.test(content)) {
            score += 1.5;
          }
          break;
      }
    } catch (err) {
      return 0;
    }

    return score;
  }

  /**
   * 获取匹配类型
   */
  getMatchType(query, memory) {
    const queryLower = query.toLowerCase();
    const previewLower = memory.preview.toLowerCase();

    if (queryLower.split(' ').some(w => previewLower.includes(w))) {
      return 'keyword';
    }
    return 'semantic';
  }

  /**
   * 批量存储
   */
  storeBatch(memories) {
    return memories.map(memory => this.store(memory.content, memory.options));
  }

  /**
   * 批量查询
   */
  queryBatch(queries) {
    return queries.map(query => this.query(query));
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      typeClassifier: this.typeClassifier.getStats(),
      queryClassifier: this.queryClassifier.getStats(),
      cacheSize: this.cache.memories.size
    };
  }

  /**
   * 清除缓存
   */
  clearCache() {
    this.cache.memories.clear();
    this.cache.indexes.clear();
  }

  /**
   * 删除记忆
   */
  delete(memoryId) {
    const memory = this.cache.memories.get(memoryId);
    if (!memory) {
      return { success: false, error: 'Memory not found' };
    }

    try {
      // 删除文件
      if (fs.existsSync(memory.filePath)) {
        fs.unlinkSync(memory.filePath);
      }

      // 从缓存移除
      this.cache.memories.delete(memoryId);

      // 更新索引
      this.rebuildIndex();

      // 更新统计
      this.stats.totalMemories--;

      return { success: true, memoryId };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  /**
   * 重建索引
   */
  rebuildIndex() {
    const indexPath = path.join(this.config.baseDir, 'indexes', 'master-index.json');
    const dailyDir = path.join(this.config.baseDir, 'daily');

    const memories = [];
    
    if (fs.existsSync(dailyDir)) {
      const files = fs.readdirSync(dailyDir);
      
      for (const file of files) {
        if (file.endsWith('.md')) {
          const filePath = path.join(dailyDir, file);
          try {
            const content = fs.readFileSync(filePath, 'utf8');
            const match = content.match(/id: (.+)/);
            const idMatch = content.match(/type: (.+)/);
            const dateMatch = content.match(/date: (.+)/);
            const preview = content.substring(0, 100);

            if (match && idMatch) {
              memories.push({
                id: match[1].trim(),
                type: idMatch[1].trim(),
                date: dateMatch ? dateMatch[1].trim() : null,
                filePath,
                preview
              });
            }
          } catch (err) {
            // 跳过无法读取的文件
          }
        }
      }
    }

    const index = {
      memories,
      lastUpdated: Date.now()
    };

    fs.writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf8');
  }
}

// 导出
module.exports = {
  MemoryManager,
  MemoryTypes,
  QueryTypes,
  TimeTree,
  AAAKIterativeCompressor: require('./compressors/aaak-iterative-compressor').AAAKIterativeCompressor
};

// CLI 测试
if (require.main === module) {
  const manager = new MemoryManager({
    baseDir: path.join(process.cwd(), 'test-memory')
  });

  console.log('🧠 Memory Manager Test\n');
  console.log('='.repeat(50));

  // 测试存储
  const testMemories = [
    {
      content: '## [2026-04-09] 完成 Memory-Master v3.0.0 核心开发\n- 因：需要实现宣传的所有功能\n- 改：实现了 4 类记忆模型、时间树、5 种检索\n- 待：继续开发压缩和知识图谱',
      options: { tags: ['开发', '里程碑'] }
    },
    {
      content: '## [知识] AAAK 压缩算法\nAAAK = Auto-Adaptive-Abstractive-Knowledge\n是一种 5 阶段智能压缩算法',
      options: { tags: ['知识', '算法'] }
    },
    {
      content: '## [技能] 发布 Skill 的步骤\n1. 检查 SKILL.md 格式\n2. 运行 clawdhub publish\n3. 等待审核通过',
      options: { tags: ['技能', '流程'] }
    },
    {
      content: '## [偏好] 代码风格\n- 喜欢简洁、注释清晰的代码\n- 讨厌冗长、无注释的代码',
      options: { tags: ['偏好', '代码'] }
    }
  ];

  console.log('\n📝 存储记忆测试:\n');
  testMemories.forEach((test, index) => {
    const result = manager.store(test.content, test.options);
    console.log(`记忆 ${index + 1}:`);
    console.log(`  ID: ${result.memoryId.substring(0, 20)}...`);
    console.log(`  类型：${result.typeName}`);
    console.log(`  置信度：${(result.confidence * 100).toFixed(1)}%`);
    console.log();
  });

  // 测试查询
  const testQueries = [
    '今天完成了什么？',
    '什么是 AAAK 压缩？',
    '怎么发布 Skill？',
    '我喜欢什么样的代码风格？'
  ];

  console.log('\n🔍 查询测试:\n');
  testQueries.forEach(query => {
    const result = manager.query(query);
    console.log(`查询：${query}`);
    console.log(`  查询类型：${result.queryTypeName}`);
    console.log(`  结果数量：${result.count}`);
    if (result.results.length > 0) {
      console.log(`  最佳匹配：${result.results[0].preview.substring(0, 50)}...`);
    }
    console.log();
  });

  console.log('='.repeat(50));
  console.log('\n统计信息:');
  console.log(JSON.stringify(manager.getStats(), null, 2));
}
