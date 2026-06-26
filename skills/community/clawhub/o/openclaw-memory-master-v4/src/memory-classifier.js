/**
 * Memory-Master v3.0.0 - 记忆类型分类器
 * 实现 4 类记忆模型：情景记忆、语义记忆、程序记忆、人设记忆
 */

const fs = require('fs');
const path = require('path');

// 记忆类型定义
const MemoryTypes = {
  EPISODIC: 'episodic',      // 情景记忆
  SEMANTIC: 'semantic',      // 语义记忆
  PROCEDURAL: 'procedural',  // 程序记忆
  PERSONA: 'persona'         // 人设记忆
};

// 记忆类型配置
const MemoryTypeConfig = {
  [MemoryTypes.EPISODIC]: {
    name: '情景记忆',
    description: '个人经历、事件和情境',
    fields: ['event', 'time', 'location', 'participants', 'emotion'],
    retention: 'long-term',
    defaultQueryType: 'temporal'
  },
  [MemoryTypes.SEMANTIC]: {
    name: '语义记忆',
    description: '事实、概念和通用知识',
    fields: ['concept', 'definition', 'category', 'relations'],
    retention: 'permanent',
    defaultQueryType: 'factual'
  },
  [MemoryTypes.PROCEDURAL]: {
    name: '程序记忆',
    description: '技能、步骤和操作流程',
    fields: ['skill_name', 'steps', 'conditions', 'examples'],
    retention: 'permanent',
    defaultQueryType: 'flow'
  },
  [MemoryTypes.PERSONA]: {
    name: '人设记忆',
    description: '用户偏好、习惯和个人设定',
    fields: ['preference', 'category', 'priority', 'context'],
    retention: 'long-term',
    defaultQueryType: 'preference'
  }
};

// 分类关键词
const ClassificationKeywords = {
  [MemoryTypes.EPISODIC]: {
    keywords: [
      '完成', '实现', '发布', '部署', '修复', '更新', 
      '会议', '讨论', '决定', '今天', '昨天', '明天',
      '开始', '结束', '经历', '事件'
    ],
    patterns: [
      /\[\d{4}-\d{2}-\d{2}\]/,  // 日期标记
      /## \[.*\].*$/,           // 标题标记
      /今天 | 昨天 | 明天 | 本周 | 上周/
    ]
  },
  [MemoryTypes.SEMANTIC]: {
    keywords: [
      '定义', '原理', '概念', '知识', '文档', 
      '规范', '标准', '解释', '说明', '术语'
    ],
    patterns: [
      /## \[知识\]/,
      /什么是/,
      /定义是/,
      /指的是/
    ]
  },
  [MemoryTypes.PROCEDURAL]: {
    keywords: [
      '步骤', '流程', '如何', '怎么', '方法', 
      '技能', '操作', '教程', '指南', '手册'
    ],
    patterns: [
      /步骤 \d+|第 \d+ 步/,
      /1\.|2\.|3\./,
      /首先 | 然后 | 接着 | 最后/
    ]
  },
  [MemoryTypes.PERSONA]: {
    keywords: [
      '喜欢', '讨厌', '偏好', '习惯', '风格', 
      '人设', '个性', '性格', '倾向', '爱好'
    ],
    patterns: [
      /## \[偏好\]/,
      /我喜欢 | 我讨厌/,
      /我总是 | 我通常/
    ]
  }
};

class MemoryTypeClassifier {
  constructor(configPath = null) {
    this.config = this.loadConfig(configPath);
    this.stats = {
      total: 0,
      byType: {
        [MemoryTypes.EPISODIC]: 0,
        [MemoryTypes.SEMANTIC]: 0,
        [MemoryTypes.PROCEDURAL]: 0,
        [MemoryTypes.PERSONA]: 0
      }
    };
  }

  /**
   * 加载配置文件
   */
  loadConfig(configPath) {
    if (configPath && fs.existsSync(configPath)) {
      const yaml = require('js-yaml');
      return yaml.load(fs.readFileSync(configPath, 'utf8'));
    }
    return MemoryTypeConfig;
  }

  /**
   * 分类单条记忆
   * @param {string} content - 记忆内容
   * @param {object} context - 上下文信息（可选）
   * @returns {object} 分类结果
   */
  classify(content, context = {}) {
    this.stats.total++;
    
    const scores = {
      [MemoryTypes.EPISODIC]: 0,
      [MemoryTypes.SEMANTIC]: 0,
      [MemoryTypes.PROCEDURAL]: 0,
      [MemoryTypes.PERSONA]: 0
    };

    // 1. 关键词评分
    this.scoreByKeywords(content, scores);

    // 2. 模式匹配评分
    this.scoreByPatterns(content, scores);

    // 3. 上下文评分
    if (context) {
      this.scoreByContext(content, context, scores);
    }

    // 4. 结构评分
    this.scoreByStructure(content, scores);

    // 5. 归一化并确定类型
    const result = this.normalizeAndSelect(scores);

    // 更新统计
    this.stats.byType[result.type]++;

    return result;
  }

  /**
   * 关键词评分
   */
  scoreByKeywords(content, scores) {
    const lowerContent = content.toLowerCase();
    
    for (const [type, config] of Object.entries(ClassificationKeywords)) {
      for (const keyword of config.keywords) {
        if (lowerContent.includes(keyword.toLowerCase())) {
          scores[type] += 1.0;
        }
      }
    }
  }

  /**
   * 模式匹配评分
   */
  scoreByPatterns(content, scores) {
    for (const [type, config] of Object.entries(ClassificationKeywords)) {
      for (const pattern of config.patterns) {
        if (pattern.test(content)) {
          scores[type] += 2.0;  // 模式匹配权重更高
        }
      }
    }
  }

  /**
   * 上下文评分
   */
  scoreByContext(content, context, scores) {
    // 如果上下文中指定了类型，增加权重
    if (context.suggestedType) {
      scores[context.suggestedType] += 3.0;
    }

    // 如果是对话中的响应，参考上一条消息的类型
    if (context.previousMemoryType) {
      scores[context.previousMemoryType] += 1.5;
    }

    // 时间上下文
    if (context.timeExpression) {
      scores[MemoryTypes.EPISODIC] += 2.0;
    }

    // 用户明确标记
    if (context.userMarked) {
      scores[context.userMarked] += 5.0;
    }
  }

  /**
   * 结构评分
   */
  scoreByStructure(content, scores) {
    const lines = content.split('\n');
    
    // 检查是否有步骤列表
    const hasSteps = lines.some(line => /^\s*[\d\-•*]\./.test(line));
    if (hasSteps) {
      scores[MemoryTypes.PROCEDURAL] += 2.0;
    }

    // 检查是否有日期标记
    const hasDate = /\d{4}-\d{2}-\d{2}/.test(content);
    if (hasDate) {
      scores[MemoryTypes.EPISODIC] += 1.5;
    }

    // 检查是否有定义格式
    const hasDefinition = /是 | 指的是 | 定义为/.test(content);
    if (hasDefinition) {
      scores[MemoryTypes.SEMANTIC] += 1.5;
    }

    // 检查是否有偏好表达
    const hasPreference = /喜欢 | 讨厌 | 偏好/.test(content);
    if (hasPreference) {
      scores[MemoryTypes.PERSONA] += 2.0;
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
      confidences[type] = total > 0 ? score / total : 0.25;
    }

    // 选择最高分的类型
    let bestType = MemoryTypes.EPISODIC;
    let bestScore = scores[MemoryTypes.EPISODIC];
    
    for (const [type, score] of Object.entries(scores)) {
      if (score > bestScore) {
        bestScore = score;
        bestType = type;
      }
    }

    // 计算置信度差距
    const sortedScores = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    const confidenceGap = sortedScores.length > 1 
      ? (sortedScores[0][1] - sortedScores[1][1]) / Math.max(sortedScores[0][1], 1)
      : 1.0;

    return {
      type: bestType,
      typeName: MemoryTypeConfig[bestType].name,
      confidence: confidences[bestType],
      confidenceGap: confidenceGap,
      allScores: scores,
      allConfidences: confidences,
      isCertain: confidenceGap > 0.3  // 置信度差距>30% 认为确定
    };
  }

  /**
   * 批量分类
   */
  classifyBatch(memories) {
    return memories.map(memory => ({
      ...memory,
      classification: this.classify(memory.content, memory.context)
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
      byType: {
        [MemoryTypes.EPISODIC]: 0,
        [MemoryTypes.SEMANTIC]: 0,
        [MemoryTypes.PROCEDURAL]: 0,
        [MemoryTypes.PERSONA]: 0
      }
    };
  }
}

// 导出
module.exports = {
  MemoryTypes,
  MemoryTypeConfig,
  ClassificationKeywords,
  MemoryTypeClassifier
};

// CLI 测试
if (require.main === module) {
  const classifier = new MemoryTypeClassifier();
  
  // 测试用例
  const testCases = [
    {
      content: '## [2026-04-09] 完成小说《觉醒之鬼》\n- 因：写作 3 个月\n- 改：今天最终定稿\n- 待：准备宣传',
      context: { timeExpression: true }
    },
    {
      content: '## [知识] OpenViking\n- 火山引擎开发的 AI Agent 上下文数据库\n- 采用 L0/L1/L2 分层存储',
      context: {}
    },
    {
      content: '## [技能] 发布 Skill 到 ClawHub\n步骤:\n1. 检查 SKILL.md 格式\n2. 运行 clawdhub publish\n3. 等待审核',
      context: {}
    },
    {
      content: '## [偏好] 写作风格\n- 用户喜欢简洁、有深度的文字\n- 讨厌冗长、空洞的内容',
      context: {}
    }
  ];

  console.log('🧠 Memory Type Classifier Test\n');
  console.log('='.repeat(50));

  testCases.forEach((test, index) => {
    const result = classifier.classify(test.content, test.context);
    console.log(`\n测试 ${index + 1}:`);
    console.log(`内容：${test.content.substring(0, 50)}...`);
    console.log(`类型：${result.typeName}`);
    console.log(`置信度：${(result.confidence * 100).toFixed(1)}%`);
    console.log(`确定性：${result.isCertain ? '✓ 确定' : '⚠ 不确定'}`);
  });

  console.log('\n' + '='.repeat(50));
  console.log('\n统计信息:');
  console.log(JSON.stringify(classifier.getStats(), null, 2));
}
