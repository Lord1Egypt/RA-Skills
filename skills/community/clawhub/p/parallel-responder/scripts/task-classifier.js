#!/usr/bin/env node

/**
 * Parallel Responder - Task Classifier
 * 
 * 智能任务分类器，支持自适应学习
 */

class TaskClassifier {
  constructor(config = {}) {
    this.config = {
      simple: {
        maxTime: 5,
        keywords: ['状态', '怎么样', '在吗', '你好', '谁', '什么', '哪里', '何时'],
        strategy: 'direct'
      },
      medium: {
        maxTime: 15,
        keywords: ['检查', '安装', '生成', '创建', '删除', '修改', '配置', '重启'],
        strategy: 'execute-and-report'
      },
      complex: {
        maxTime: 30,
        keywords: ['整理', '分析', '写文章', '批量', '所有', '总结', '报告', '研究'],
        strategy: 'sub-agent'
      },
      ...config
    };

    // 历史记录，用于自适应学习
    this.history = [];
    this.maxHistorySize = 100;
  }

  /**
   * 分类任务
   * @param {string} message - 用户消息
   * @returns {Object} 分类结果
   */
  classify(message) {
    const lowerMessage = message.toLowerCase();
    
    // 计算每个类型的匹配分数
    const scores = {
      simple: this.calculateScore(lowerMessage, this.config.simple),
      medium: this.calculateScore(lowerMessage, this.config.medium),
      complex: this.calculateScore(lowerMessage, this.config.complex)
    };

    // 选择分数最高的类型
    const type = Object.keys(scores).reduce((a, b) => 
      scores[a] > scores[b] ? a : b
    );

    // 预估时间
    const estimatedTime = this.estimateTime(type, message);

    return {
      type,
      confidence: scores[type] / 10, // 归一化到 0-1
      estimatedTime,
      strategy: this.config[type].strategy,
      matchedKeywords: this.getMatchedKeywords(lowerMessage, this.config[type])
    };
  }

  /**
   * 计算匹配分数
   */
  calculateScore(message, config) {
    let score = 0;

    // 关键词匹配
    config.keywords.forEach(keyword => {
      if (message.includes(keyword.toLowerCase())) {
        score += 3;
      }
    });

    // 消息长度（长消息更可能是复杂任务）
    if (message.length > 50) score += 2;
    if (message.length > 100) score += 2;

    // 问号数量（多个问题可能更复杂）
    const questionMarks = (message.match(/\?/g) || []).length;
    score += questionMarks;

    return score;
  }

  /**
   * 获取匹配的关键词
   */
  getMatchedKeywords(message, config) {
    return config.keywords.filter(keyword => 
      message.includes(keyword.toLowerCase())
    );
  }

  /**
   * 预估时间
   */
  estimateTime(type, message) {
    const base = this.config[type].maxTime;
    
    // 复杂度系数
    let complexityFactor = 1.0;
    
    // 长消息更复杂
    if (message.length > 100) complexityFactor += 0.5;
    
    // 多个关键词更复杂
    const matchedCount = this.getMatchedKeywords(message.toLowerCase(), this.config[type]).length;
    if (matchedCount > 2) complexityFactor += 0.3;

    const min = Math.floor(base * 0.5 * complexityFactor);
    const max = Math.floor(base * 1.5 * complexityFactor);

    return {
      min,
      max,
      range: `${min}-${max}秒`,
      confidence: 0.7 // 初始置信度
    };
  }

  /**
   * 记录任务执行结果（用于学习）
   */
  recordResult(taskType, estimatedTime, actualTime) {
    this.history.push({
      taskType,
      estimatedTime,
      actualTime,
      timestamp: Date.now(),
      error: Math.abs(estimatedTime.max - actualTime) / actualTime
    });

    // 保持历史记录大小
    if (this.history.length > this.maxHistorySize) {
      this.history.shift();
    }

    // 自适应调整
    this.adaptThresholds();
  }

  /**
   * 自适应调整阈值
   */
  adaptThresholds() {
    if (this.history.length < 20) return; // 至少需要 20 条记录

    // 分析每种类型的平均误差
    const errors = {
      simple: this.getAverageError('simple'),
      medium: this.getAverageError('medium'),
      complex: this.getAverageError('complex')
    };

    // 如果某种类型的平均误差 > 50%，调整阈值
    Object.entries(errors).forEach(([type, error]) => {
      if (error > 0.5) {
        // 增加该类型的 maxTime
        this.config[type].maxTime = Math.floor(this.config[type].maxTime * 1.2);
        console.log(`📊 自适应调整：${type} 类型的 maxTime 调整为 ${this.config[type].maxTime}秒`);
      }
    });
  }

  /**
   * 获取某类型的平均误差
   */
  getAverageError(type) {
    const records = this.history.filter(r => r.taskType === type);
    if (records.length === 0) return 0;

    const totalError = records.reduce((sum, r) => sum + r.error, 0);
    return totalError / records.length;
  }

  /**
   * 获取分类统计
   */
  getStats() {
    return {
      totalTasks: this.history.length,
      byType: {
        simple: this.history.filter(r => r.taskType === 'simple').length,
        medium: this.history.filter(r => r.taskType === 'medium').length,
        complex: this.history.filter(r => r.taskType === 'complex').length
      },
      averageError: this.history.length > 0 
        ? (this.history.reduce((sum, r) => sum + r.error, 0) / this.history.length).toFixed(2)
        : 0
    };
  }
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TaskClassifier;
}

// CLI usage
if (require.main === module) {
  const classifier = new TaskClassifier();
  
  const message = process.argv.slice(2).join(' ');
  
  if (!message) {
    console.log('Usage: node task-classifier.js <message>');
    console.log('Example: node task-classifier.js "帮我整理记忆"');
    process.exit(1);
  }

  const result = classifier.classify(message);
  
  console.log('📊 任务分类结果:');
  console.log(JSON.stringify(result, null, 2));
}
