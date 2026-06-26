#!/usr/bin/env node

/**
 * Parallel Responder - Time Estimator
 * 
 * 执行时间预估器，基于多维度分析
 */

class TimeEstimator {
  constructor(config = {}) {
    this.config = {
      // 基础时间（秒）
      baseTime: {
        simple: 3,
        medium: 10,
        complex: 30
      },
      
      // 复杂度系数
      complexityFactors: {
        // 文件操作
        readFile: 1.2,
        writeFile: 1.3,
        multipleFiles: 1.5,
        
        // 网络操作
        webSearch: 1.5,
        apiCall: 1.3,
        download: 1.8,
        
        // AI 操作
        generateText: 2.0,
        analyzeContent: 1.8,
        summarize: 1.5,
        
        // 系统操作
        install: 1.5,
        configure: 1.3,
        restart: 1.2
      },
      
      // 数据量系数
      dataVolumeFactors: {
        small: 1.0,    // < 10 条记录
        medium: 1.3,   // 10-100 条
        large: 1.8,    // 100-1000 条
        xlarge: 2.5    // > 1000 条
      },
      
      ...config
    };

    // 历史记录
    this.history = [];
  }

  /**
   * 预估执行时间
   * @param {string} taskType - 任务类型
   * @param {string} message - 用户消息
   * @param {Object} context - 上下文信息
   * @returns {Object} 预估结果
   */
  estimate(taskType, message, context = {}) {
    // 1. 基础时间
    let baseTime = this.config.baseTime[taskType] || 10;

    // 2. 复杂度系数
    let complexityFactor = this.analyzeComplexity(message);

    // 3. 数据量系数
    let volumeFactor = this.analyzeDataVolume(message, context);

    // 4. 计算预估时间
    const estimatedTime = baseTime * complexityFactor * volumeFactor;

    // 5. 生成范围（±50%）
    const min = Math.floor(estimatedTime * 0.5);
    const max = Math.floor(estimatedTime * 1.5);

    return {
      min,
      max,
      range: `${min}-${max}秒`,
      average: Math.floor(estimatedTime),
      confidence: this.calculateConfidence(taskType, message),
      factors: {
        baseTime,
        complexityFactor,
        volumeFactor
      },
      breakdown: this.getBreakdown(taskType, message)
    };
  }

  /**
   * 分析复杂度
   */
  analyzeComplexity(message) {
    let factor = 1.0;
    const lowerMessage = message.toLowerCase();

    // 检查复杂度关键词
    Object.entries(this.config.complexityFactors).forEach(([key, value]) => {
      if (lowerMessage.includes(key.toLowerCase())) {
        factor = Math.max(factor, value);
      }
    });

    // 长消息更复杂
    if (message.length > 100) factor += 0.2;
    if (message.length > 200) factor += 0.3;

    // 多个动作更复杂
    const actionCount = (message.match(/(然后 | 接着 | 再 | 并 | 且)/g) || []).length;
    factor += actionCount * 0.1;

    return Math.min(factor, 3.0); // 上限 3.0
  }

  /**
   * 分析数据量
   */
  analyzeDataVolume(message, context) {
    // 从上下文获取数据量信息
    if (context.fileCount) {
      if (context.fileCount > 100) return this.config.dataVolumeFactors.xlarge;
      if (context.fileCount > 10) return this.config.dataVolumeFactors.large;
      if (context.fileCount > 1) return this.config.dataVolumeFactors.medium;
    }

    // 从消息中推断
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('所有') || lowerMessage.includes('全部')) {
      return this.config.dataVolumeFactors.large;
    }
    
    if (lowerMessage.includes('批量')) {
      return this.config.dataVolumeFactors.large;
    }

    return this.config.dataVolumeFactors.small;
  }

  /**
   * 计算置信度
   */
  calculateConfidence(taskType, message) {
    let confidence = 0.7; // 基础置信度

    // 有关键词匹配，置信度更高
    if (message.length > 20) confidence += 0.1;
    
    // 有上下文信息，置信度更高
    confidence += 0.1;

    // 历史准确率
    if (this.history.length > 10) {
      const recentAccuracy = this.getRecentAccuracy(taskType);
      confidence = (confidence + recentAccuracy) / 2;
    }

    return Math.min(confidence, 0.95);
  }

  /**
   * 获取最近准确率
   */
  getRecentAccuracy(taskType) {
    const recent = this.history
      .filter(r => r.taskType === taskType)
      .slice(-10);

    if (recent.length === 0) return 0.7;

    const accurate = recent.filter(r => {
      const error = Math.abs(r.estimated - r.actual) / r.actual;
      return error < 0.5; // 误差 < 50% 算准确
    }).length;

    return accurate / recent.length;
  }

  /**
   * 获取时间分解
   */
  getBreakdown(taskType, message) {
    const breakdown = [];

    // 根据任务类型添加分解
    if (taskType === 'complex') {
      breakdown.push({ step: '启动子 agent', time: '2 秒' });
      breakdown.push({ step: '任务执行', time: '主要时间' });
      breakdown.push({ step: '进度汇报', time: '每 10 秒' });
      breakdown.push({ step: '结果汇总', time: '3 秒' });
    }

    if (message.includes('搜索') || message.includes('找')) {
      breakdown.push({ step: '网络搜索', time: '5-10 秒' });
    }

    if (message.includes('写') || message.includes('生成')) {
      breakdown.push({ step: '内容生成', time: '10-30 秒' });
    }

    return breakdown;
  }

  /**
   * 记录实际执行时间
   */
  recordActual(taskType, estimated, actual) {
    this.history.push({
      taskType,
      estimated,
      actual,
      error: Math.abs(estimated - actual) / actual,
      timestamp: Date.now()
    });

    // 保持历史记录大小
    if (this.history.length > 100) {
      this.history.shift();
    }
  }

  /**
   * 获取预估统计
   */
  getStats() {
    if (this.history.length === 0) {
      return {
        totalEstimates: 0,
        averageError: 0,
        accuracy: 0
      };
    }

    const avgError = this.history.reduce((sum, r) => sum + r.error, 0) / this.history.length;
    const accurate = this.history.filter(r => r.error < 0.5).length;

    return {
      totalEstimates: this.history.length,
      averageError: avgError.toFixed(2),
      accuracy: (accurate / this.history.length * 100).toFixed(1) + '%'
    };
  }
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TimeEstimator;
}

// CLI usage
if (require.main === module) {
  const estimator = new TimeEstimator();
  
  const taskType = process.argv[2] || 'complex';
  const message = process.argv.slice(3).join(' ');
  
  if (!message) {
    console.log('Usage: node time-estimator.js <taskType> <message>');
    console.log('Example: node time-estimator.js complex "帮我整理记忆"');
    process.exit(1);
  }

  const result = estimator.estimate(taskType, message);
  
  console.log('⏱️ 时间预估结果:');
  console.log(JSON.stringify(result, null, 2));
}
