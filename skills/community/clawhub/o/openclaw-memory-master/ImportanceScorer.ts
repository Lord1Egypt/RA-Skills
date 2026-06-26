/**
 * Auto Classifier - 自动分类器
 * 
 * 混合分类器：规则匹配 + LLM 精细分类
 * 支持多类别分类和置信度评分
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.3.0
 * @module smart
 */

import { ClassifierConfig } from './SmartMemoryCurator';

// ============ 类型定义 ============

export interface ClassificationResult {
  category: string;
  confidence: number;
  subcategory?: string;
  explanation?: string;
  ruleMatches?: string[];
  llmUsed: boolean;
}

export interface ClassificationRule {
  category: string;
  patterns: string[];           // 关键词/正则表达式
  weight: number;              // 规则权重
  description: string;         // 规则描述
}

export interface LLMClassificationRequest {
  content: string;
  categories: string[];
  context?: string;
}

export interface LLMClassificationResponse {
  category: string;
  confidence: number;
  reasoning: string;
  alternativeCategories?: Array<{ category: string; confidence: number }>;
}

// ============ 规则定义 ============

/**
 * 预定义分类规则
 * 基于关键词匹配的快速分类
 */
export const DEFAULT_CLASSIFICATION_RULES: ClassificationRule[] = [
  // 技术类
  {
    category: 'technical',
    patterns: [
      '代码', '编程', '算法', 'API', '数据库', '服务器', '前端', '后端',
      'JavaScript', 'TypeScript', 'Python', 'Node.js', 'React', 'Vue',
      'git', 'GitHub', '部署', '调试', 'bug', '错误', '异常',
      '内存', '性能', '优化', '架构', '设计模式', '测试',
      '命令行', '终端', 'shell', 'docker', '容器', '云',
      '人工智能', 'AI', '机器学习', '深度学习', '神经网络',
      'OpenClaw', '技能', '插件', '扩展', '配置',
    ],
    weight: 1.0,
    description: '技术开发相关',
  },
  
  // 项目类
  {
    category: 'project',
    patterns: [
      '项目', '任务', '里程碑', '进度', '计划', '时间表',
      '需求', '功能', '特性', '用户故事', '产品', '原型',
      '团队', '协作', '会议', '讨论', '评审', '反馈',
      '交付', '发布', '版本', '迭代', '冲刺', '敏捷',
      '文档', '说明', '指南', '教程', '手册',
      '预算', '资源', '人力', '时间', '成本',
      '风险', '问题', '障碍', '解决方案',
    ],
    weight: 1.0,
    description: '项目管理相关',
  },
  
  // 学习类
  {
    category: 'learning',
    patterns: [
      '学习', '教程', '课程', '教育', '培训', '读书',
      '研究', '探索', '实验', '尝试', '实践', '练习',
      '知识', '概念', '理论', '原理', '方法', '技巧',
      '进步', '提高', '成长', '发展', '技能', '能力',
      '学校', '课堂', '作业', '考试', '成绩', '学位',
      '在线课程', 'MOOC', '视频教程', '电子书', '文档',
    ],
    weight: 1.0,
    description: '学习教育相关',
  },
  
  // 生活类
  {
    category: 'life',
    patterns: [
      '生活', '日常', '家庭', '朋友', '家人', '亲戚',
      '健康', '饮食', '运动', '健身', '休息', '睡眠',
      '购物', '消费', '购买', '商品', '服务', '交易',
      '旅行', '旅游', '假期', '度假', '景点', '酒店',
      '娱乐', '游戏', '电影', '音乐', '书籍', '艺术',
      '兴趣', '爱好', '收藏', '手工艺', '创作',
      '情感', '心情', '感受', '思考', '反思', '感悟',
    ],
    weight: 1.0,
    description: '日常生活相关',
  },
  
  // 工作类
  {
    category: 'work',
    patterns: [
      '工作', '职业', '职场', '公司', '企业', '组织',
      '同事', '上司', '下属', '客户', '合作伙伴',
      '职位', '岗位', '职责', '责任', '目标', 'KPI',
      '工资', '薪资', '福利', '待遇', '奖金', '晋升',
      '面试', '招聘', '应聘', '简历', '求职', '离职',
      '加班', '压力', '平衡', '职业发展', '职业生涯',
    ],
    weight: 1.0,
    description: '工作职业相关',
  },
  
  // 健康类
  {
    category: 'health',
    patterns: [
      '健康', '医疗', '医生', '医院', '诊所', '药品',
      '疾病', '症状', '诊断', '治疗', '康复', '恢复',
      '体检', '检查', '化验', '报告', '指标',
      '心理', '心理健康', '压力管理', '焦虑', '抑郁',
      '营养', '维生素', '矿物质', '蛋白质', '碳水',
      '运动', '锻炼', '健身', '瑜伽', '跑步', '游泳',
      '睡眠', '失眠', '休息', '放松', '冥想',
      '预防', '保健', '养生', '长寿', '生活质量',
    ],
    weight: 1.0,
    description: '健康医疗相关',
  },
  
  // 财务类
  {
    category: 'finance',
    patterns: [
      '财务', '金钱', '资金', '资产', '财富', '收入',
      '支出', '花费', '消费', '预算', '记账', '账目',
      '投资', '股票', '基金', '债券', '证券', '理财',
      '银行', '账户', '存款', '取款', '转账', '支付',
      '信用卡', '贷款', '债务', '利息', '还款',
      '税务', '税收', '报税', '发票', '收据',
      '保险', '保障', '风险', '赔偿', '理赔',
      '经济', '市场', '价格', '价值', '成本', '效益',
    ],
    weight: 1.0,
    description: '财务金融相关',
  },
  
  // 社交类
  {
    category: 'social',
    patterns: [
      '社交', '社交网络', '朋友圈', '人际关系', '人脉',
      '微信', 'QQ', '微博', '小红书', '抖音', '社交媒体',
      '聊天', '对话', '沟通', '交流', '互动', '联系',
      '朋友', '好友', '伙伴', '同伴', '搭档', '团队',
      '聚会', '聚餐', '活动', '事件', '庆典', '节日',
      '社区', '群体', '组织', '协会', '俱乐部',
      '帮助', '支持', '关心', '关爱', '友谊', '感情',
    ],
    weight: 1.0,
    description: '社交人际关系相关',
  },
];

// ============ 自动分类器 ============

/**
 * 自动分类器
 * 
 * 实现规则匹配和LLM分类的混合策略
 */
export class AutoClassifier {
  private config: ClassifierConfig;
  private rules: ClassificationRule[];
  private ruleCache: Map<string, ClassificationResult>;
  
  constructor(config: ClassifierConfig) {
    this.config = config;
    this.rules = DEFAULT_CLASSIFICATION_RULES.filter(rule => 
      config.categories.includes(rule.category)
    );
    this.ruleCache = new Map();
    
    console.log(`[AutoClassifier] 初始化完成，使用 ${this.rules.length} 条分类规则`);
  }

  /**
   * 分类主方法
   */
  async classify(content: string): Promise<ClassificationResult> {
    const cacheKey = this.generateCacheKey(content);
    
    // 检查缓存
    const cached = this.ruleCache.get(cacheKey);
    if (cached) {
      console.log(`[AutoClassifier] 缓存命中: ${cached.category} (${cached.confidence.toFixed(2)})`);
      return cached;
    }
    
    try {
      // 1. 规则分类
      const ruleResult = await this.ruleBasedClassify(content);
      
      // 2. 判断是否需要LLM分类
      let finalResult: ClassificationResult;
      
      if (this.shouldUseLLM(ruleResult)) {
        console.log(`[AutoClassifier] 规则分类置信度低(${ruleResult.confidence.toFixed(2)})，启用LLM分类`);
        const llmResult = await this.llmClassify(content, ruleResult);
        finalResult = llmResult;
      } else {
        finalResult = ruleResult;
      }
      
      // 3. 缓存结果
      this.ruleCache.set(cacheKey, finalResult);
      this.cleanCache();
      
      console.log(`[AutoClassifier] 分类完成: ${finalResult.category} (${finalResult.confidence.toFixed(2)}, ${finalResult.llmUsed ? 'LLM' : '规则'})`);
      return finalResult;
      
    } catch (error) {
      console.error('[AutoClassifier] 分类失败:', error);
      
      // 返回降级结果
      const fallbackResult: ClassificationResult = {
        category: 'other',
        confidence: 0.5,
        explanation: `分类失败: ${error}`,
        llmUsed: false,
      };
      
      return fallbackResult;
    }
  }

  /**
   * 批量分类
   */
  async batchClassify(contents: string[]): Promise<ClassificationResult[]> {
    const results: ClassificationResult[] = [];
    
    for (let i = 0; i < contents.length; i++) {
      console.log(`[AutoClassifier] 批量分类: ${i + 1}/${contents.length}`);
      const result = await this.classify(contents[i]);
      results.push(result);
      
      // 避免过载
      if (i % 10 === 9) {
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }
    
    return results;
  }

  /**
   * 添加自定义分类规则
   */
  addRule(rule: ClassificationRule): void {
    this.rules.push(rule);
    console.log(`[AutoClassifier] 添加分类规则: ${rule.category} (${rule.patterns.length} 个模式)`);
  }

  /**
   * 获取规则统计
   */
  getRuleStats(): Record<string, number> {
    const stats: Record<string, number> = {};
    
    for (const rule of this.rules) {
      stats[rule.category] = (stats[rule.category] || 0) + rule.patterns.length;
    }
    
    return stats;
  }

  /**
   * 清除缓存
   */
  clearCache(): void {
    this.ruleCache.clear();
    console.log('[AutoClassifier] 规则缓存已清除');
  }

  // ============ 私有方法 ============

  /**
   * 规则分类
   */
  private async ruleBasedClassify(content: string): Promise<ClassificationResult> {
    const startTime = Date.now();
    
    // 转换为小写方便匹配
    const contentLower = content.toLowerCase();
    
    // 计算每个类别的得分
    const scores: Record<string, number> = {};
    const ruleMatches: Record<string, string[]> = {};
    
    for (const rule of this.rules) {
      let categoryScore = 0;
      const matches: string[] = [];
      
      for (const pattern of rule.patterns) {
        const patternLower = pattern.toLowerCase();
        
        // 简单关键词匹配
        if (contentLower.includes(patternLower)) {
          categoryScore += rule.weight;
          matches.push(pattern);
        }
        
        // 简单的边界匹配（避免部分匹配）
        const wordPattern = new RegExp(`\\b${patternLower}\\b`, 'gi');
        const wordMatches = content.match(wordPattern);
        if (wordMatches && wordMatches.length > 0) {
          categoryScore += rule.weight * wordMatches.length;
          matches.push(...wordMatches);
        }
      }
      
      if (categoryScore > 0) {
        scores[rule.category] = (scores[rule.category] || 0) + categoryScore;
        ruleMatches[rule.category] = (ruleMatches[rule.category] || []).concat(matches);
      }
    }
    
    // 找到最高分
    let bestCategory = 'other';
    let bestScore = 0;
    
    for (const [category, score] of Object.entries(scores)) {
      if (score > bestScore) {
        bestScore = score;
        bestCategory = category;
      }
    }
    
    // 计算置信度（基于分数归一化）
    const maxPossibleScore = this.calculateMaxPossibleScore(content);
    const confidence = maxPossibleScore > 0 ? Math.min(bestScore / maxPossibleScore, 1.0) : 0;
    
    // 归一化置信度
    const normalizedConfidence = this.normalizeConfidence(confidence, content.length);
    
    const processingTime = Date.now() - startTime;
    
    return {
      category: bestCategory,
      confidence: normalizedConfidence,
      ruleMatches: ruleMatches[bestCategory] || [],
      explanation: `规则匹配: ${bestScore.toFixed(1)} 分, 处理时间: ${processingTime}ms`,
      llmUsed: false,
    };
  }

  /**
   * LLM分类
   */
  private async llmClassify(content: string, ruleResult: ClassificationResult): Promise<ClassificationResult> {
    const startTime = Date.now();
    
    try {
      // 构建LLM请求
      const request: LLMClassificationRequest = {
        content: content.length > 1000 ? content.substring(0, 1000) + '...' : content,
        categories: this.config.categories,
        context: `规则分类结果: ${ruleResult.category} (置信度: ${ruleResult.confidence.toFixed(2)})`,
      };
      
      // 调用LLM（这里需要集成OpenClaw的LLM调用）
      const llmResponse = await this.callLLMForClassification(request);
      
      const processingTime = Date.now() - startTime;
      
      return {
        category: llmResponse.category,
        confidence: llmResponse.confidence,
        subcategory: llmResponse.category.includes('/') ? llmResponse.category.split('/')[1] : undefined,
        explanation: `LLM分类: ${llmResponse.reasoning} (处理时间: ${processingTime}ms)`,
        llmUsed: true,
      };
      
    } catch (error) {
      console.error('[AutoClassifier] LLM分类失败:', error);
      
      // LLM失败时返回规则分类结果，但降低置信度
      return {
        ...ruleResult,
        confidence: ruleResult.confidence * 0.7, // 降低置信度
        explanation: `LLM分类失败，使用规则分类结果: ${ruleResult.explanation}`,
        llmUsed: false,
      };
    }
  }

  /**
   * 判断是否需要LLM分类
   */
  private shouldUseLLM(ruleResult: ClassificationResult): boolean {
    if (!this.config.useLLM) {
      return false;
    }
    
    // 置信度低于阈值时使用LLM
    if (ruleResult.confidence < this.config.llmThreshold) {
      return true;
    }
    
    // 分类为'other'时使用LLM
    if (ruleResult.category === 'other' && this.config.ruleBasedFallback) {
      return true;
    }
    
    return false;
  }

  /**
   * 调用LLM进行分类（占位实现）
   */
  private async callLLMForClassification(request: LLMClassificationRequest): Promise<LLMClassificationResponse> {
    // 这里需要集成OpenClaw的LLM调用
    // 暂时返回模拟结果
    
    console.log('[AutoClassifier] 调用LLM进行分类（模拟）');
    
    // 模拟LLM处理延迟
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // 基于内容的简单模拟
    const content = request.content.toLowerCase();
    let simulatedCategory = 'other';
    let simulatedConfidence = 0.5;
    
    // 简单的模拟逻辑
    if (content.includes('代码') || content.includes('编程')) {
      simulatedCategory = 'technical';
      simulatedConfidence = 0.85;
    } else if (content.includes('项目') || content.includes('任务')) {
      simulatedCategory = 'project';
      simulatedConfidence = 0.8;
    } else if (content.includes('学习') || content.includes('教程')) {
      simulatedCategory = 'learning';
      simulatedConfidence = 0.75;
    } else if (content.includes('生活') || content.includes('日常')) {
      simulatedCategory = 'life';
      simulatedConfidence = 0.7;
    }
    
    return {
      category: simulatedCategory,
      confidence: simulatedConfidence,
      reasoning: `基于内容关键词分析，判断为${simulatedCategory}类别`,
      alternativeCategories: [
        { category: simulatedCategory, confidence: simulatedConfidence },
        { category: 'other', confidence: 1 - simulatedConfidence },
      ],
    };
  }

  /**
   * 计算最大可能得分
   */
  private calculateMaxPossibleScore(content: string): number {
    // 简单实现：基于内容长度和规则数量
    const wordCount = content.split(/\s+/).length;
    const avgRulesPerCategory = this.rules.reduce((sum, rule) => sum + rule.patterns.length, 0) / this.rules.length;
    
    return Math.min(wordCount * 0.5, avgRulesPerCategory * 2);
  }

  /**
   * 归一化置信度
   */
  private normalizeConfidence(rawConfidence: number, contentLength: number): number {
    // 考虑内容长度的置信度调整
    let adjusted = rawConfidence;
    
    // 短内容置信度降低
    if (contentLength < 50) {
      adjusted *= 0.7;
    }
    
    // 长内容置信度提高
    if (contentLength > 500) {
      adjusted = Math.min(adjusted * 1.2, 1.0);
    }
    
    // 应用平滑
    return this.smoothConfidence(adjusted);
  }

  /**
   * 置信度平滑
   */
  private smoothConfidence(confidence: number): number {
    // 将置信度映射到更合理的范围
    if (confidence < 0.3) {
      return confidence * 0.8; // 低置信度更保守
    } else if (confidence > 0.7) {
      return 0.7 + (confidence - 0.7) * 1.5; // 高置信度更激进
    } else {
      return confidence;
    }
  }

  /**
   * 生成缓存键
   */
  private generateCacheKey(content: string): string {
    // 简单的内容哈希
    const hash = this.simpleHash(content.substring(0, 100));
    const lengthCategory = content.length < 100 ? 'short' : content.length < 500 ? 'medium' : 'long';
    
    return `${hash}_${lengthCategory}`;
  }

  /**
   * 简单哈希函数
   */
  private simpleHash(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转换为32位整数
    }
    return Math.abs(hash).toString(36).substring(0, 8);
  }

  /**
   * 清理缓存
   */
  private cleanCache(): void {
    const maxCacheSize = 1000;
    
    if (this.ruleCache.size > maxCacheSize) {
      // 移除最旧的条目
      const keysToRemove = Array.from(this.ruleCache.keys()).slice(0, this.ruleCache.size - maxCacheSize);
      for (const key of keysToRemove) {
        this.ruleCache.delete(key);
      }
      
      console.log(`[AutoClassifier] 清理缓存: 移除了 ${keysToRemove.length} 个条目`);
    }
  }
}

/**
 * 导出工具函数
 */
export function createClassifier(config?: Partial<ClassifierConfig>): AutoClassifier {
  const fullConfig: ClassifierConfig = {
    useLLM: true,
    llmThreshold: 0.7,
    ruleBasedFallback: true,
    categories: [
      'technical', 'project', 'learning', 'life', 
      'work', 'health', 'finance', 'social', 'other'
    ],
    ...config,
  };
  
  return new AutoClassifier(fullConfig);
}

/**
 * 快速分类函数
 */
export async function quickClassify(content: string, config?: Partial<ClassifierConfig>): Promise<ClassificationResult> {
  const classifier = createClassifier(config);
  return classifier.classify(content);
}