/**
 * 按需注入引擎 v1.1.0
 * 根据当前对话动态加载相关记忆
 */

class ContextInjectionEngine {
  constructor(options = {}) {
    this.maxMemoriesToInject = options.maxMemories || 5;
    this.minImportance = options.minImportance || 50;
    this.vectorEngine = options.vectorEngine;
    this.compressionEngine = options.compressionEngine;
  }

  /**
   * 分析当前对话，确定需要注入的记忆类型
   */
  analyzeContext(currentMessage, conversationHistory = []) {
    const analysis = {
      topic: this.detectTopic(currentMessage),
      urgency: this.detectUrgency(currentMessage),
      memoryTypes: [],
      suggestedCount: this.maxMemoriesToInject
    };

    // 检测话题类型
    const topicKeywords = {
      project: ['项目', '开发', '代码', '功能', '需求', '产品'],
      preference: ['喜欢', '偏好', '习惯', '常用', '爱用'],
      task: ['任务', '待办', '计划', '安排', '会议', '日程'],
      contact: ['联系', '电话', '邮箱', '微信', '地址'],
      decision: ['决定', '选择', '方案', '确定'],
      learning: ['学习', '教程', '文档', '知识', '技能']
    };

    const text = currentMessage + ' ' + conversationHistory.slice(-3).join(' ');

    Object.entries(topicKeywords).forEach(([type, keywords]) => {
      if (keywords.some(kw => text.includes(kw))) {
        analysis.memoryTypes.push(type);
      }
    });

    // 如果没有明确话题，使用通用策略
    if (analysis.memoryTypes.length === 0) {
      analysis.memoryTypes = ['preference', 'contact', 'decision'];
    }

    return analysis;
  }

  /**
   * 检测话题类型
   */
  detectTopic(text) {
    const topics = {
      work: ['工作', '项目', '开发', '代码', '需求'],
      life: ['生活', '家庭', '朋友', '娱乐', '旅行'],
      study: ['学习', '考试', '课程', '培训'],
      health: ['健康', '运动', '医疗', '饮食'],
      finance: ['投资', '理财', '股票', '基金']
    };

    for (const [topic, keywords] of Object.entries(topics)) {
      if (keywords.some(kw => text.includes(kw))) {
        return topic;
      }
    }

    return 'general';
  }

  /**
   * 检测紧急程度
   */
  detectUrgency(text) {
    const urgentKeywords = ['紧急', '马上', '立刻', '快点', '急', '今天', '现在'];
    const hasUrgent = urgentKeywords.some(kw => text.includes(kw));
    
    return hasUrgent ? 'high' : 'normal';
  }

  /**
   * 智能选择要注入的记忆
   * @param {string} currentMessage - 当前用户消息
   * @param {Array} allMemories - 所有可用记忆
   * @returns {Array} 要注入的记忆列表
   */
  async selectMemoriesToInject(currentMessage, allMemories) {
    if (allMemories.length === 0) {
      return [];
    }

    // 1. 分析当前上下文
    const context = this.analyzeContext(currentMessage);

    // 2. 过滤最低重要性
    let candidates = allMemories.filter(m => m.importance >= this.minImportance);

    // 3. 如果有向量引擎，使用语义搜索
    if (this.vectorEngine && candidates.some(m => m.embedding)) {
      try {
        const vectorResults = await this.vectorEngine.search(
          currentMessage,
          candidates,
          this.maxMemoriesToInject * 2  // 先取 2 倍，再筛选
        );

        // 按相似度和重要性综合排序
        const scored = vectorResults.map(memory => ({
          ...memory,
          combinedScore: memory.similarity * 0.6 + (memory.importance / 100) * 0.4
        }));

        scored.sort((a, b) => b.combinedScore - a.combinedScore);
        candidates = scored.slice(0, this.maxMemoriesToInject);
      } catch (error) {
        console.warn('⚠️  向量搜索失败，使用备用方案:', error.message);
        // 降级到关键词匹配
        candidates = this.keywordMatch(currentMessage, candidates);
      }
    } else {
      // 降级到关键词匹配
      candidates = this.keywordMatch(currentMessage, candidates);
    }

    // 4. 确保包含高重要性记忆（≥85 分）
    const highImportance = allMemories.filter(m => m.importance >= 85);
    const existingIds = new Set(candidates.map(m => m.id));
    
    highImportance.forEach(memory => {
      if (!existingIds.has(memory.id) && candidates.length < this.maxMemoriesToInject) {
        candidates.push(memory);
      }
    });

    // 5. 限制最终数量
    return candidates.slice(0, this.maxMemoriesToInject);
  }

  /**
   * 关键词匹配（备用方案）
   */
  keywordMatch(query, memories) {
    const queryWords = query.toLowerCase().split(/[\s,，.。]+/).filter(w => w.length > 1);
    
    const scored = memories.map(memory => {
      const content = (memory.content + ' ' + (memory.tags || []).join(' ')).toLowerCase();
      let score = 0;

      queryWords.forEach(word => {
        if (content.includes(word)) {
          score += 1;
        }
      });

      // 加上重要性分数
      score += memory.importance / 100;

      return { ...memory, score };
    });

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, this.maxMemoriesToInject);
  }

  /**
   * 格式化注入的记忆为提示词
   */
  formatMemoriesForPrompt(memories, options = {}) {
    const format = options.format || 'concise';  // concise | detailed | json

    if (memories.length === 0) {
      return '';
    }

    switch (format) {
      case 'concise':
        return this.formatConcise(memories);
      case 'detailed':
        return this.formatDetailed(memories);
      case 'json':
        return JSON.stringify(memories, null, 2);
      default:
        return this.formatConcise(memories);
    }
  }

  /**
   * 简洁格式（推荐，节省 token）
   */
  formatConcise(memories) {
    const lines = memories.map(memory => {
      const content = memory.compressedContent || memory.content;
      const tags = memory.tags ? `[${memory.tags.slice(0, 3).join(', ')}]` : '';
      const importance = this.importanceIcon(memory.importance);
      
      return `${importance} ${content} ${tags}`;
    });

    return `\n📚 相关记忆:\n${lines.join('\n')}`;
  }

  /**
   * 详细格式（包含更多信息）
   */
  formatDetailed(memories) {
    const lines = memories.map(memory => {
      const content = memory.originalContent || memory.content;
      const meta = [
        `重要性：${memory.importance}`,
        `分类：${memory.category}`,
        `时间：${new Date(memory.timestamp).toLocaleDateString('zh-CN')}`
      ].join(', ');

      return `• ${content}\n  (${meta})`;
    });

    return `\n📚 相关记忆:\n${lines.join('\n\n')}`;
  }

  /**
   * 重要性图标
   */
  importanceIcon(importance) {
    if (importance >= 85) return '🔴';
    if (importance >= 70) return '🟡';
    return '🟢';
  }

  /**
   * 获取注入统计
   */
  getStats(injectionHistory) {
    if (!injectionHistory || injectionHistory.length === 0) {
      return {
        totalInjections: 0,
        avgMemoriesPerInjection: 0,
        tokenSavings: 'N/A'
      };
    }

    const totalMemories = injectionHistory.reduce(
      (sum, record) => sum + record.memoriesInjected,
      0
    );

    return {
      totalInjections: injectionHistory.length,
      avgMemoriesPerInjection: (totalMemories / injectionHistory.length).toFixed(1),
      estimatedTokenSavings: `${((1 - 5 / 20) * 100).toFixed(0)}%`,  // 相比全量加载
      lastInjection: injectionHistory[injectionHistory.length - 1]?.timestamp || 'N/A'
    };
  }
}

module.exports = ContextInjectionEngine;
