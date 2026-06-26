/**
 * IntentRouter - P0-2 路由算法升级
 * 从关键词匹配 → 意图置信度计算
 * 
 * 核心改进：
 * 1. 关键词权重（TF-IDF风格）
 * 2. 多词命中加权
 * 3. 负向权重（排除词）
 * 4. 置信度归一化
 */

class IntentRouter {
  constructor() {
    // 意图配置：关键词 + 权重 + 排除词
    this.intents = {
      novel_creation: {
        keywords: [
          { word: '小说', weight: 1.0 },
          { word: '网文', weight: 1.0 },
          { word: '章节', weight: 0.8 },
          { word: '草稿', weight: 0.7 },
          { word: '世界观', weight: 0.9 },
          { word: '大纲', weight: 0.8 },
          { word: '角色设定', weight: 0.9 },
          { word: 'novel', weight: 1.0 },
          { word: 'story bible', weight: 1.0 },
          { word: 'publish', weight: 0.6 },
          { word: '发布包', weight: 0.8 }
        ],
        exclude: ['小红书', '知乎', '公众号'],
        baseScore: 0.1
      },
      operations: {
        keywords: [
          { word: '部署', weight: 1.0 },
          { word: '备份', weight: 0.9 },
          { word: '重启', weight: 1.0 },
          { word: '监控', weight: 0.8 },
          { word: '运维', weight: 1.0 },
          { word: 'gateway', weight: 0.9 },
          { word: '进程', weight: 0.7 },
          { word: '健康检查', weight: 0.8 }
        ],
        exclude: [],
        baseScore: 0.2
      },
      content_creation: {
        keywords: [
          { word: '小红书', weight: 1.0 },
          { word: '笔记', weight: 0.6 },
          { word: '内容', weight: 0.4 },
          { word: '发布', weight: 0.5 },
          { word: '帖子', weight: 0.7 },
          { word: '文章', weight: 0.5 },
          { word: '视频', weight: 0.5 },
          { word: '封面', weight: 0.6 },
          { word: '标题', weight: 0.5 },
          { word: '知乎', weight: 1.0 },
          { word: '公众号', weight: 1.0 },
          { word: '抖音', weight: 0.9 },
          { word: '文案', weight: 0.7 },
          { word: '选题', weight: 0.8 },
          { word: '种草', weight: 0.9 },
          { word: '涨粉', weight: 0.8 }
        ],
        exclude: ['代码', '开发', '架构'],
        baseScore: 0.15
      },
      product_management: {
        keywords: [
          { word: '产品', weight: 1.0 },
          { word: '功能', weight: 0.7 },
          { word: '迭代', weight: 0.8 },
          { word: 'roadmap', weight: 1.0 },
          { word: 'pmf', weight: 1.0 },
          { word: 'mvp', weight: 1.0 },
          { word: '需求', weight: 0.6 },
          { word: '优先级', weight: 0.7 },
          { word: '用户研究', weight: 0.9 },
          { word: '数据分析', weight: 0.6 }
        ],
        exclude: [],
        baseScore: 0.1
      },
      technical: {
        keywords: [
          { word: '代码', weight: 1.0 },
          { word: '开发', weight: 0.8 },
          { word: 'skill', weight: 0.9 },
          { word: '系统', weight: 0.5 },
          { word: '架构', weight: 0.9 },
          { word: 'python', weight: 1.0 },
          { word: 'javascript', weight: 1.0 },
          { word: 'api', weight: 0.7 },
          { word: '自动化', weight: 0.6 },
          { word: '脚本', weight: 0.8 },
          { word: 'bug', weight: 0.9 },
          { word: '修复', weight: 0.7 }
        ],
        exclude: [],
        baseScore: 0.1
      },
      strategy: {
        keywords: [
          { word: '战略', weight: 1.0 },
          { word: '商业', weight: 0.9 },
          { word: '财富', weight: 1.0 },
          { word: '机会', weight: 0.7 },
          { word: '风险', weight: 0.7 },
          { word: '市场', weight: 0.6 },
          { word: '分析', weight: 0.4 },
          { word: '投资', weight: 0.8 },
          { word: '盈利', weight: 0.8 },
          { word: '商业模式', weight: 1.0 }
        ],
        exclude: [],
        baseScore: 0.1
      },
      hr_recruitment: {
        keywords: [
          { word: '招聘', weight: 1.0 },
          { word: '简历', weight: 1.0 },
          { word: '面试', weight: 0.9 },
          { word: '候选人', weight: 1.0 },
          { word: '人才', weight: 0.8 },
          { word: '岗位', weight: 0.7 },
          { word: 'JD', weight: 0.9 }
        ],
        exclude: [],
        baseScore: 0.2
      },
      reporting: {
        keywords: [
          { word: '汇报', weight: 1.0 },
          { word: '同步', weight: 0.8 },
          { word: '总结', weight: 0.7 },
          { word: '进度', weight: 0.6 },
          { word: '进展', weight: 0.7 },
          { word: '状态', weight: 0.4 }
        ],
        exclude: [],
        baseScore: 0.25
      }
    };

    // 意图 → Agent 映射
    this.intentToAgent = {
      novel_creation: 'RD',
      operations: 'RD',
      content_creation: 'Marketing',
      product_management: 'Product',
      technical: 'RD',
      strategy: 'Strategy',
      hr_recruitment: 'CEO',
      reporting: 'CEO'
    };

    // Agent 置信度基数
    this.agentBase = {
      Marketing: 0.85,
      RD: 0.85,
      CEO: 0.8,
      Strategy: 0.85,
      Product: 0.85
    };
  }

  /**
   * 计算输入对各意图的置信度
   */
  calculateIntentScores(input) {
    const text = input.toLowerCase();
    const scores = {};

    for (const [intentName, config] of Object.entries(this.intents)) {
      let score = config.baseScore;

      // 检查排除词
      const hasExclude = config.exclude.some(word => text.includes(word.toLowerCase()));
      if (hasExclude) {
        scores[intentName] = 0;
        continue;
      }

      // 计算关键词匹配得分
      let matchCount = 0;
      let weightedSum = 0;

      for (const { word, weight } of config.keywords) {
        const regex = new RegExp(word.toLowerCase(), 'gi');
        const matches = text.match(regex);
        if (matches) {
          matchCount += matches.length;
          weightedSum += weight * matches.length;
        }
      }

      // TF-IDF 风格得分
      if (matchCount > 0) {
        // 得分 = 基础分 + 加权命中数 / (1 + log(文本长度))
        const lenNorm = 1 + Math.log(Math.max(text.length, 1) / 10);
        score = config.baseScore + (weightedSum / lenNorm);
        
        // 多词命中加成
        if (matchCount >= 3) score *= 1.2;
        else if (matchCount >= 2) score *= 1.1;
      }

      scores[intentName] = Math.min(score, 1.0); // 上限1.0
    }

    return scores;
  }

  /**
   * 归一化置信度
   */
  normalizeScores(scores) {
    const maxScore = Math.max(...Object.values(scores));
    const minScore = Math.min(...Object.values(scores));
    const range = maxScore - minScore || 1;

    const normalized = {};
    for (const [intent, score] of Object.entries(scores)) {
      normalized[intent] = (score - minScore) / range;
    }

    return normalized;
  }

  /**
   * 检测显式Agent指定
   */
  detectExplicitAgent(input) {
    const text = input.toLowerCase();
    
    const patterns = [
      { regex: /@marketing|@内容/gi, agent: 'Marketing' },
      { regex: /@rd|@研发|@novel|@小说/gi, agent: 'RD' },
      { regex: /@strategy|@战略/gi, agent: 'Strategy' },
      { regex: /@product|@产品/gi, agent: 'Product' },
      { regex: /@ceo|@森森/gi, agent: 'CEO' }
    ];

    for (const { regex, agent } of patterns) {
      if (regex.test(text)) {
        return { agent, confidence: 1.0, explicit: true };
      }
    }

    return null;
  }

  /**
   * 主路由方法
   */
  route(input) {
    const text = input.toLowerCase();

    // 1. 检查显式指定
    const explicit = this.detectExplicitAgent(input);
    if (explicit) {
      return {
        intent: explicit.agent === 'CEO' ? 'coordination' : 'explicit',
        agent: explicit.agent,
        confidence: 1.0,
        reasoning: `显式指定 @${explicit.agent}`,
        scores: {}
      };
    }

    // 2. 计算各意图置信度
    const rawScores = this.calculateIntentScores(input);
    const normalizedScores = this.normalizeScores(rawScores);

    // 3. 找最高置信度意图
    let bestIntent = 'coordination';
    let bestScore = 0;

    for (const [intent, score] of Object.entries(normalizedScores)) {
      if (score > bestScore) {
        bestScore = score;
        bestIntent = intent;
      }
    }

    // 4. 确定目标Agent
    const agent = this.intentToAgent[bestIntent] || 'CEO';
    const agentMultiplier = this.agentBase[agent] || 0.8;
    const finalConfidence = Math.min(bestScore * agentMultiplier, 1.0);

    return {
      intent: bestIntent,
      agent,
      confidence: Math.round(finalConfidence * 100) / 100,
      reasoning: this._buildReasoning(bestIntent, rawScores[bestIntent], normalizedScores[bestIntent]),
      scores: rawScores
    };
  }

  /**
   * 构建推理说明
   */
  _buildReasoning(intent, rawScore, normalizedScore) {
    const intentLabels = {
      novel_creation: '小说创作',
      operations: '运维',
      content_creation: '内容创作',
      product_management: '产品管理',
      technical: '技术开发',
      strategy: '战略',
      hr_recruitment: 'HR招聘',
      reporting: '汇报同步',
      coordination: '综合协调'
    };

    const label = intentLabels[intent] || intent;
    return `意图[${label}] 置信度=${Math.round(normalizedScore * 100)}%`;
  }

  /**
   * 获取所有可能的路由（带置信度排序）
   */
  routeWithRanking(input, topN = 3) {
    const result = this.route(input);
    const scores = result.scores;

    // 按得分排序
    const ranking = Object.entries(scores)
      .map(([intent, score]) => ({
        intent,
        agent: this.intentToAgent[intent],
        confidence: Math.round(score * 100) / 100
      }))
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, topN);

    return { primary: result, ranking };
  }
}

// 导出
module.exports = { IntentRouter };
