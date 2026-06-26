/**
 * Memory-Master v3.0.0 - 查询分类器
 * 实现 5 种检索类型：流程、时间、关系、偏好、事实
 */

const fs = require('fs');

// 查询类型定义
const QueryTypes = {
  FLOW: 'flow',           // 流程/步骤查询
  TEMPORAL: 'temporal',   // 时间相关查询
  RELATIONAL: 'relational', // 关系/关联查询
  PREFERENCE: 'preference', // 偏好查询
  FACTUAL: 'factual'      // 事实查询
};

// 查询类型配置
const QueryTypeConfig = {
  [QueryTypes.FLOW]: {
    name: '流程查询',
    description: '查询步骤、方法、操作流程',
    memoryTypes: ['procedural'],
    searchStrategy: 'step-match',
    responseTemplate: '步骤导向'
  },
  [QueryTypes.TEMPORAL]: {
    name: '时间查询',
    description: '查询时间相关的事件和经历',
    memoryTypes: ['episodic'],
    searchStrategy: 'time-range',
    responseTemplate: '时间线导向'
  },
  [QueryTypes.RELATIONAL]: {
    name: '关系查询',
    description: '查询关联、联系、相关事物',
    memoryTypes: ['episodic', 'semantic', 'procedural', 'persona'],
    searchStrategy: 'relation-match',
    responseTemplate: '关联导向'
  },
  [QueryTypes.PREFERENCE]: {
    name: '偏好查询',
    description: '查询用户偏好、习惯、风格',
    memoryTypes: ['persona'],
    searchStrategy: 'preference-match',
    responseTemplate: '偏好导向'
  },
  [QueryTypes.FACTUAL]: {
    name: '事实查询',
    description: '查询事实、定义、知识',
    memoryTypes: ['semantic'],
    searchStrategy: 'fact-match',
    responseTemplate: '知识导向'
  }
};

// 查询关键词
const QueryKeywords = {
  [QueryTypes.FLOW]: {
    keywords: [
      '怎么', '如何', '怎样', '步骤', '流程', '方法',
      '怎么做', '如何做', '怎么办', '流程', '顺序',
      '第一步', '然后', '接着', '最后', '操作', '指南'
    ],
    patterns: [
      /怎么 [做办]|如何 [做办]/,
      /步骤 \d+|第 \d+ 步/,
      /首先.*然后.*最后/,
      /1\.|2\.|3\./,
      /流程 | 方法 | 指南 | 教程/
    ]
  },
  [QueryTypes.TEMPORAL]: {
    keywords: [
      '今天', '昨天', '明天', '本周', '上周', '下周',
      '这个月', '上个月', '最近', '什么时候', '时间',
      '何时', '哪天', '几号', '日期', '时候'
    ],
    patterns: [
      /今天 | 昨天 | 明天 | 本周 | 上周/,
      /这个月 | 上个月 | 最近/,
      /什么时候 | 何时 | 哪天/,
      /\d{4}[-/]\d{1,2}[-/]\d{1,2}/
    ]
  },
  [QueryTypes.RELATIONAL]: {
    keywords: [
      '和', '与', '及', '关联', '相关', '联系',
      '关于', '涉及', '关系', '连接', '影响'
    ],
    patterns: [
      /和.*有关 | 与.*相关/,
      /关联 | 关系 | 联系/,
      /.*和.*|.*与.*/,
      /涉及 | 影响 | 关于/
    ]
  },
  [QueryTypes.PREFERENCE]: {
    keywords: [
      '喜欢', '讨厌', '偏好', '习惯', '风格',
      '倾向', '爱好', '喜好', '不爱', '反感'
    ],
    patterns: [
      /喜欢 | 讨厌 | 偏好/,
      /习惯 | 风格 | 倾向/,
      /我通常 | 我总是/,
      /爱.*|不爱.*/
    ]
  },
  [QueryTypes.FACTUAL]: {
    keywords: [
      '什么', '什么是', '定义', '原理', '为什么',
      '哪个', '哪些', '哪里', '何处', '概念',
      '意思', '含义', '解释', '说明'
    ],
    patterns: [
      /什么 (是 | 叫 | 意思)/,
      /定义 (是 | 为)|原理/,
      /为什么 | 为何/,
      /哪个 | 哪些 | 哪里/
    ]
  }
};

class QueryClassifier {
  constructor(config = null) {
    this.config = config || QueryTypeConfig;
    this.stats = {
      total: 0,
      byType: {}
    };
    
    // 初始化统计
    Object.values(QueryTypes).forEach(type => {
      this.stats.byType[type] = 0;
    });
  }

  /**
   * 分类查询
   * @param {string} query - 用户查询
   * @param {object} context - 上下文信息
   * @returns {object} 分类结果
   */
  classify(query, context = {}) {
    this.stats.total++;
    
    const scores = {};
    Object.values(QueryTypes).forEach(type => {
      scores[type] = 0;
    });

    // 1. 关键词评分
    this.scoreByKeywords(query, scores);

    // 2. 模式匹配评分
    this.scoreByPatterns(query, scores);

    // 3. 上下文评分
    if (context) {
      this.scoreByContext(query, context, scores);
    }

    // 4. 语义分析评分（简化版）
    this.scoreBySemantics(query, scores);

    // 5. 归一化并确定类型
    const result = this.normalizeAndSelect(scores);

    // 更新统计
    if (result.type) {
      this.stats.byType[result.type]++;
    }

    return result;
  }

  /**
   * 关键词评分
   */
  scoreByKeywords(query, scores) {
    const lowerQuery = query.toLowerCase();
    
    for (const [type, config] of Object.entries(QueryKeywords)) {
      for (const keyword of config.keywords) {
        if (lowerQuery.includes(keyword.toLowerCase())) {
          // 流程和时间查询给予更高权重
          const boost = (type === QueryTypes.FLOW || type === QueryTypes.TEMPORAL) ? 2.5 : 1.5;
          scores[type] += boost;
        }
      }
    }
  }

  /**
   * 模式匹配评分
   */
  scoreByPatterns(query, scores) {
    for (const [type, config] of Object.entries(QueryKeywords)) {
      for (const pattern of config.patterns) {
        if (pattern.test(query)) {
          scores[type] += 2.5;  // 模式匹配权重更高
        }
      }
    }
  }

  /**
   * 上下文评分
   */
  scoreByContext(query, context, scores) {
    // 如果上下文中指定了查询类型
    if (context.suggestedQueryType) {
      scores[context.suggestedQueryType] += 4.0;
    }

    // 如果之前有相关查询，增加连续性
    if (context.previousQueryType) {
      scores[context.previousQueryType] += 1.0;
    }

    // 如果当前对话聚焦于特定主题
    if (context.currentTopic) {
      // 根据主题调整权重
      const topicBoosts = {
        'technical': QueryTypes.FLOW,
        'schedule': QueryTypes.TEMPORAL,
        'relationship': QueryTypes.RELATIONAL,
        'personal': QueryTypes.PREFERENCE,
        'knowledge': QueryTypes.FACTUAL
      };
      
      const boost = topicBoosts[context.currentTopic];
      if (boost) {
        scores[boost] += 2.0;
      }
    }

    // 用户明确指定
    if (context.userSpecified) {
      scores[context.userSpecified] += 5.0;
    }
  }

  /**
   * 语义分析评分（简化版）
   */
  scoreBySemantics(query, scores) {
    // 问句类型分析
    const isHowQuestion = /怎么 | 如何 | 怎样/.test(query);
    const isWhenQuestion = /什么时候 | 何时 | 哪天/.test(query);
    const isWhatQuestion = /(什么 | 哪些 | 哪个)/.test(query) && !/(喜欢 | 讨厌 | 偏好)/.test(query);
    const isWhyQuestion = /为什么 | 为何/.test(query);
    const isPreferenceQuestion = /喜欢 | 讨厌 | 偏好/.test(query);
    const isStepQuestion = /步骤 | 流程 | 方法/.test(query);

    if (isHowQuestion || isStepQuestion) {
      scores[QueryTypes.FLOW] += 4.0;
    }
    if (isWhenQuestion) {
      scores[QueryTypes.TEMPORAL] += 4.0;
    }
    if (isWhatQuestion) {
      scores[QueryTypes.FACTUAL] += 2.0;
    }
    if (isWhyQuestion) {
      scores[QueryTypes.FACTUAL] += 1.5;
      scores[QueryTypes.RELATIONAL] += 1.0;
    }
    if (isPreferenceQuestion) {
      scores[QueryTypes.PREFERENCE] += 4.0;
    }

    // 查询长度分析
    const queryLength = query.length;
    if (queryLength < 10) {
      // 短查询更可能是事实或偏好
      scores[QueryTypes.FACTUAL] += 0.5;
      scores[QueryTypes.PREFERENCE] += 0.5;
    } else if (queryLength > 30) {
      // 长查询更可能是流程或关系
      scores[QueryTypes.FLOW] += 0.5;
      scores[QueryTypes.RELATIONAL] += 0.5;
    }
  }

  /**
   * 归一化并选择最佳类型
   */
  normalizeAndSelect(scores) {
    const total = Object.values(scores).reduce((sum, score) => sum + score, 0);
    
    // 计算置信度
    const confidences = {};
    for (const [type, score] of Object.entries(scores)) {
      confidences[type] = total > 0 ? score / total : 0.2;
    }

    // 选择最高分的类型
    let bestType = null;
    let bestScore = -1;
    
    for (const [type, score] of Object.entries(scores)) {
      if (score > bestScore) {
        bestScore = score;
        bestType = type;
      }
    }

    // 如果没有明确的类型，返回默认
    if (bestScore < 2.0) {
      bestType = QueryTypes.FACTUAL;  // 默认为事实查询
    }

    // 计算置信度差距
    const sortedScores = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    const confidenceGap = sortedScores.length > 1 
      ? (sortedScores[0][1] - sortedScores[1][1]) / Math.max(sortedScores[0][1], 1)
      : 1.0;

    return {
      type: bestType,
      typeName: QueryTypeConfig[bestType]?.name || '未知',
      confidence: confidences[bestType] || 0,
      confidenceGap: confidenceGap,
      allScores: scores,
      allConfidences: confidences,
      isCertain: confidenceGap > 0.3,  // 置信度差距>30% 认为确定
      searchStrategy: QueryTypeConfig[bestType]?.searchStrategy || 'default',
      memoryTypes: QueryTypeConfig[bestType]?.memoryTypes || []
    };
  }

  /**
   * 批量分类
   */
  classifyBatch(queries) {
    return queries.map(query => ({
      query,
      classification: this.classify(query)
    }));
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const total = this.stats.total;
    return {
      total,
      byType: this.stats.byType,
      percentages: Object.fromEntries(
        Object.entries(this.stats.byType).map(([type, count]) => [
          type,
          total > 0 ? ((count / total) * 100).toFixed(1) + '%' : '0%'
        ])
      )
    };
  }

  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      total: 0,
      byType: {}
    };
    
    Object.values(QueryTypes).forEach(type => {
      this.stats.byType[type] = 0;
    });
  }

  /**
   * 获取查询类型的搜索策略
   */
  getSearchStrategy(queryType) {
    return QueryTypeConfig[queryType]?.searchStrategy || 'default';
  }

  /**
   * 获取查询类型的记忆类型偏好
   */
  getMemoryTypePreferences(queryType) {
    return QueryTypeConfig[queryType]?.memoryTypes || [];
  }

  /**
   * 格式化查询结果
   */
  formatResults(results, queryType) {
    const config = QueryTypeConfig[queryType];
    if (!config) {
      return results;
    }

    switch (config.searchStrategy) {
      case 'step-match':
        return this.formatAsSteps(results);
      case 'time-range':
        return this.formatAsTimeline(results);
      case 'relation-match':
        return this.formatAsRelations(results);
      case 'preference-match':
        return this.formatAsPreferences(results);
      case 'fact-match':
        return this.formatAsFacts(results);
      default:
        return results;
    }
  }

  /**
   * 格式化为步骤
   */
  formatAsSteps(results) {
    return results.map(r => ({
      ...r,
      format: 'steps',
      highlight: 'ordered_list'
    }));
  }

  /**
   * 格式化为时间线
   */
  formatAsTimeline(results) {
    return results.map(r => ({
      ...r,
      format: 'timeline',
      highlight: 'time_expression'
    }));
  }

  /**
   * 格式化为关系
   */
  formatAsRelations(results) {
    return results.map(r => ({
      ...r,
      format: 'relations',
      highlight: 'connections'
    }));
  }

  /**
   * 格式化为偏好
   */
  formatAsPreferences(results) {
    return results.map(r => ({
      ...r,
      format: 'preferences',
      highlight: 'user_preference'
    }));
  }

  /**
   * 格式化为事实
   */
  formatAsFacts(results) {
    return results.map(r => ({
      ...r,
      format: 'facts',
      highlight: 'key_information'
    }));
  }
}

// 导出
module.exports = {
  QueryTypes,
  QueryTypeConfig,
  QueryKeywords,
  QueryClassifier
};

// CLI 测试
if (require.main === module) {
  const classifier = new QueryClassifier();
  
  console.log('🔍 Query Classifier Test\n');
  console.log('='.repeat(50));

  const testQueries = [
    // 流程查询
    '怎么发布 Skill 到 ClawHub？',
    '如何配置 Memory-Master？',
    '部署的步骤是什么？',
    
    // 时间查询
    '今天完成了什么？',
    '上周我们讨论了什么？',
    '这个月有什么计划？',
    
    // 关系查询
    'Memory-Master 和 OpenViking 有什么关系？',
    '这个功能和哪个模块相关？',
    
    // 偏好查询
    '我喜欢什么样的写作风格？',
    '有什么偏好的配置方式？',
    
    // 事实查询
    '什么是 AAAK 压缩？',
    'Memory-Master 的定义是什么？',
    '为什么需要记忆系统？'
  ];

  testQueries.forEach((query, index) => {
    const result = classifier.classify(query);
    console.log(`\n查询 ${index + 1}: ${query}`);
    console.log(`  类型：${result.typeName}`);
    console.log(`  置信度：${(result.confidence * 100).toFixed(1)}%`);
    console.log(`  搜索策略：${result.searchStrategy}`);
    console.log(`  记忆类型：${result.memoryTypes.join(', ') || '全部'}`);
    console.log(`  确定性：${result.isCertain ? '✓ 确定' : '⚠ 不确定'}`);
  });

  console.log('\n' + '='.repeat(50));
  console.log('\n统计信息:');
  console.log(JSON.stringify(classifier.getStats(), null, 2));
}
