/**
 * 情感成长 (Emotional Growth) v1.0.0
 *
 * 情感经历的学习和成长
 */

class EmotionalGrowth {
  constructor(options = {}) {
    this.growthHistory = [];
    this.patterns = new Map();
    this.maxHistory = options.maxHistory || 200;
    this.learningRate = options.learningRate || 0.1;
  }

  /**
   * 记录情感经历
   */
  recordExperience(experience) {
    const record = {
      id: `exp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      emotion: experience.emotion,
      trigger: experience.trigger,
      response: experience.response,
      outcome: experience.outcome,
      context: experience.context || {},
      timestamp: Date.now(),
      learned: false
    };

    this.growthHistory.push(record);

    // 清理旧记录
    if (this.growthHistory.length > this.maxHistory) {
      this.growthHistory = this.growthHistory.slice(-this.maxHistory);
    }

    // 学习
    this._learnFromExperience(record);

    return record;
  }

  /**
   * 从经历中学习
   */
  _learnFromExperience(experience) {
    // 分析结果
    if (!experience.outcome) return;

    const isPositive = experience.outcome.positive !== false;
    const key = `${experience.emotion}_${experience.trigger}`;

    // 获取或创建模式
    let pattern = this.patterns.get(key);
    if (!pattern) {
      pattern = {
        emotion: experience.emotion,
        trigger: experience.trigger,
        occurrences: 0,
        positiveOutcomes: 0,
        negativeOutcomes: 0,
        lastOccurrence: null,
        adaptations: []
      };
      this.patterns.set(key, pattern);
    }

    // 更新模式
    pattern.occurrences++;
    pattern.lastOccurrence = Date.now();
    if (isPositive) {
      pattern.positiveOutcomes++;
    } else {
      pattern.negativeOutcomes++;
    }

    // 生成适应建议
    if (pattern.occurrences >= 3) {
      const successRate = pattern.positiveOutcomes / pattern.occurrences;

      if (successRate < 0.4) {
        // 需要适应：消极结果过多
        const adaptation = this._generateAdaptation(experience, pattern);
        pattern.adaptations.push({
          ...adaptation,
          timestamp: Date.now()
        });
      }
    }

    experience.learned = true;
  }

  /**
   * 生成适应建议
   */
  _generateAdaptation(experience, pattern) {
    const suggestions = [];

    // 根据情感类型生成建议
    if (experience.emotion === 'anger') {
      suggestions.push({
        type: 'response_change',
        suggestion: '下次遇到类似触发时，尝试冷静处理',
        confidence: 0.7
      });
    }

    if (experience.emotion === 'fear') {
      suggestions.push({
        type: 'exposure',
        suggestion: '渐进式面对恐惧源头',
        confidence: 0.6
      });
    }

    if (experience.emotion === 'sadness') {
      suggestions.push({
        type: 'action',
        suggestion: '悲伤时尝试做一些积极的事情',
        confidence: 0.5
      });
    }

    // 选择最佳建议
    const best = suggestions.sort((a, b) => b.confidence - a.confidence)[0];

    return best || {
      type: 'observe',
      suggestion: '继续观察这个模式',
      confidence: 0.3
    };
  }

  /**
   * 获取学习模式
   */
  getPatterns(emotion = null) {
    const patterns = [...this.patterns.values()];

    if (emotion) {
      return patterns.filter(p => p.emotion === emotion);
    }

    return patterns.sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 获取需要适应的模式
   */
  getAdaptationNeeded() {
    return this.getPatterns()
      .filter(p => p.occurrences >= 3)
      .map(p => ({
        ...p,
        successRate: p.positiveOutcomes / p.occurrences
      }))
      .filter(p => p.successRate < 0.4)
      .sort((a, b) => a.successRate - b.successRate);
  }

  /**
   * 获取成长摘要
   */
  getGrowthSummary() {
    const patterns = [...this.patterns.values()];

    const totalExperiences = this.growthHistory.length;
    const learnedExperiences = this.growthHistory.filter(e => e.learned).length;
    const uniquePatterns = patterns.length;
    const adaptationsNeeded = this.getAdaptationNeeded().length;

    // 计算情感分布
    const emotionDistribution = {};
    for (const exp of this.growthHistory) {
      emotionDistribution[exp.emotion] = (emotionDistribution[exp.emotion] || 0) + 1;
    }

    return {
      totalExperiences,
      learnedExperiences,
      uniquePatterns,
      adaptationsNeeded,
      emotionDistribution,
      recentPatterns: patterns.slice(-5)
    };
  }

  /**
   * 获取历史
   */
  getHistory(limit = 20) {
    return this.growthHistory.slice(-limit);
  }

  /**
   * 重置学习记录
   */
  reset() {
    this.growthHistory = [];
    this.patterns = new Map();
  }
}

module.exports = { EmotionalGrowth };
