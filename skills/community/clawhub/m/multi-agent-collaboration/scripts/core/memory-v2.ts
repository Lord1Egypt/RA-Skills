/**
 * 统一记忆系统 V2 - 改进版
 * 
 * 改进点：
 * 1. 场景化改造 - 每个场景有自己的记忆空间和规则
 * 2. 元数据化 - 增加来源可信度、上下文指纹、结果追踪
 * 3. 双向验证 - 实现反馈闭环
 */

import * as fs from 'fs';
import * as path from 'path';

// ==================== 类型定义 ====================

type MemoryLevel = 'L0' | 'L1' | 'L2' | 'L3' | 'L4';
type MemoryCategory = 'task' | 'rule' | 'insight' | 'pattern' | 'methodology' | 'worldview' | 'goal' | 'value' | 'wisdom';
type SystemType = 'signal' | 'workflow' | 'goal' | 'shared';

// 场景类型
type ScenarioType = 'duty' | 'sentiment' | 'workflow' | 'goal' | 'general';

// 🆕 记忆元数据
interface MemoryMetadata {
  // 来源信息
  source: SystemType;                    // 来源系统
  sourceCredibility: number;             // 来源可信度 0-1
  
  // 上下文指纹
  contextFingerprint: {
    timestamp: string;                   // 时间戳
    scenario: ScenarioType;              // 场景类型
    environment?: Record<string, any>;   // 环境参数
  };
  
  // 结果追踪
  resultTracking: Array<{
    usedAt: string;                      // 使用时间
    scenario: ScenarioType;              // 使用场景
    effect: 'success' | 'failure' | 'neutral';  // 效果
    feedback?: string;                   // 反馈说明
  }>;
  
  // 统计信息
  stats: {
    accessCount: number;                 // 访问次数
    successRate: number;                 // 成功率
    lastUsedAt: string;                  // 最后使用时间
  };
}

// 🆕 改进后的记忆条目
interface MemoryEntryV2 {
  id: string;
  level: MemoryLevel;
  category: MemoryCategory;
  key: string;
  value: string | object;
  tags: string[];
  importance: number;
  
  // 🆕 元数据
  metadata: MemoryMetadata;
  
  createdAt: string;
  accessedAt: string;
}

// 🆕 场景配置
interface ScenarioConfig {
  name: ScenarioType;
  description: string;
  
  // 记忆压缩规则
  compressionRules: {
    // 什么信息需要压缩到中期记忆
    shouldCompress: (entry: MemoryEntryV2) => boolean;
    // 压缩时保留哪些信息
    preserveFields: string[];
  };
  
  // 模式提炼规则
  extractionRules: {
    // 什么信息需要提炼为长期记忆
    shouldExtract: (entries: MemoryEntryV2[]) => boolean;
    // 如何提炼模式
    extractPattern: (entries: MemoryEntryV2[]) => object;
  };
  
  // 领域约束（用于语义检索）
  domainConstraints: {
    // 相关性判断
    isRelevant: (query: string, entry: MemoryEntryV2) => boolean;
    // 优先级调整
    adjustPriority: (entry: MemoryEntryV2, context: any) => number;
  };
}

// 🆕 记忆配置
interface MemoryConfigV2 {
  // 基础配置
  L0_MAX_ITEMS: number;
  L1_MAX_LINES: number;
  L2_MAX_ENTRIES: number;
  L3_MAX_ENTRIES: number;
  
  // 🆕 场景配置
  scenarios: Record<ScenarioType, ScenarioConfig>;
  
  // 🆕 遗忘机制
  forgetting: {
    // 遗忘阈值
    threshold: number;
    // 时间衰减系数
    decayRate: number;
    // 清理周期（毫秒）
    cleanupInterval: number;
  };
  
  // 🆕 反馈机制
  feedback: {
    // 成功时增加的重要性
    successBonus: number;
    // 失败时减少的重要性
    failurePenalty: number;
    // 最小重要性
    minImportance: number;
  };
}

// ==================== 默认场景配置 ====================

const DEFAULT_SCENARIO_CONFIGS: Record<ScenarioType, ScenarioConfig> = {
  // 值班场景
  duty: {
    name: 'duty',
    description: '节假日值班热点监测场景',
    
    compressionRules: {
      shouldCompress: (entry) => {
        // S级、A级热点需要压缩
        return entry.tags.includes('S级') || entry.tags.includes('A级');
      },
      preserveFields: ['title', 'level', 'score', 'source', 'action']
    },
    
    extractionRules: {
      shouldExtract: (entries) => {
        // 同类热点出现3次以上，提炼模式
        return entries.length >= 3;
      },
      extractPattern: (entries) => {
        return {
          pattern: '热点模式',
          frequency: entries.length,
          avgScore: entries.reduce((sum, e) => sum + (e.importance || 0), 0) / entries.length
        };
      }
    },
    
    domainConstraints: {
      isRelevant: (query, entry) => {
        // 值班场景：关注热点、舆情、事件
        const keywords = ['热点', '舆情', '事件', '异常', '报警'];
        return keywords.some(k => query.includes(k) || entry.key.includes(k));
      },
      adjustPriority: (entry, context) => {
        // 如果是当前值班时间，提高优先级
        if (context.isOnDuty) return entry.importance * 1.2;
        return entry.importance;
      }
    }
  },
  
  // 舆情场景
  sentiment: {
    name: 'sentiment',
    description: '舆情监测场景',
    
    compressionRules: {
      shouldCompress: (entry) => {
        // 负面舆情、高热度需要压缩
        return entry.tags.includes('负面') || entry.importance >= 4;
      },
      preserveFields: ['topic', 'sentiment', 'heat', 'source']
    },
    
    extractionRules: {
      shouldExtract: (entries) => entries.length >= 5,
      extractPattern: (entries) => ({
        pattern: '舆情模式',
        topics: [...new Set(entries.map(e => e.key))]
      })
    },
    
    domainConstraints: {
      isRelevant: (query, entry) => {
        const keywords = ['舆情', '负面', '正面', '热度', '传播'];
        return keywords.some(k => query.includes(k) || entry.key.includes(k));
      },
      adjustPriority: (entry, context) => entry.importance
    }
  },
  
  // 工作流场景
  workflow: {
    name: 'workflow',
    description: '工作流资产沉淀场景',
    
    compressionRules: {
      shouldCompress: (entry) => entry.category === 'insight' || entry.category === 'pattern',
      preserveFields: ['operation', 'experience', 'decision', 'value']
    },
    
    extractionRules: {
      shouldExtract: (entries) => entries.length >= 3,
      extractPattern: (entries) => ({
        pattern: '方法论',
        steps: entries.map(e => e.key)
      })
    },
    
    domainConstraints: {
      isRelevant: (query, entry) => {
        const keywords = ['方法', '流程', '经验', '技巧', '决策'];
        return keywords.some(k => query.includes(k) || entry.key.includes(k));
      },
      adjustPriority: (entry, context) => entry.importance
    }
  },
  
  // 目标场景
  goal: {
    name: 'goal',
    description: '个人目标追踪场景',
    
    compressionRules: {
      shouldCompress: (entry) => entry.category === 'goal' || entry.importance >= 4,
      preserveFields: ['goal', 'progress', 'deadline', 'motivation']
    },
    
    extractionRules: {
      shouldExtract: (entries) => entries.length >= 2,
      extractPattern: (entries) => ({
        pattern: '目标模式',
        goals: entries.map(e => e.key)
      })
    },
    
    domainConstraints: {
      isRelevant: (query, entry) => {
        const keywords = ['目标', '进度', '动机', '精力', '盲点'];
        return keywords.some(k => query.includes(k) || entry.key.includes(k));
      },
      adjustPriority: (entry, context) => entry.importance
    }
  },
  
  // 通用场景
  general: {
    name: 'general',
    description: '通用场景',
    
    compressionRules: {
      shouldCompress: (entry) => entry.importance >= 3,
      preserveFields: ['key', 'value', 'tags']
    },
    
    extractionRules: {
      shouldExtract: (entries) => entries.length >= 5,
      extractPattern: (entries) => ({ pattern: '通用模式', count: entries.length })
    },
    
    domainConstraints: {
      isRelevant: (query, entry) => true,
      adjustPriority: (entry, context) => entry.importance
    }
  }
};

// ==================== 默认配置 ====================

const DEFAULT_CONFIG_V2: MemoryConfigV2 = {
  L0_MAX_ITEMS: 10,
  L1_MAX_LINES: 50,
  L2_MAX_ENTRIES: 200,
  L3_MAX_ENTRIES: 1000,
  
  scenarios: DEFAULT_SCENARIO_CONFIGS,
  
  forgetting: {
    threshold: 0.3,
    decayRate: 0.1,
    cleanupInterval: 24 * 60 * 60 * 1000  // 24小时
  },
  
  feedback: {
    successBonus: 0.1,
    failurePenalty: 0.2,
    minImportance: 0.1
  }
};

// ==================== 记忆系统 V2 ====================

export class UnifiedMemorySystemV2 {
  private skillName: string;
  private baseDir: string;
  private config: MemoryConfigV2;
  
  // 🆕 当前场景
  private currentScenario: ScenarioType = 'general';
  
  // 🆕 场景记忆空间
  private scenarioMemories: Map<ScenarioType, {
    L0: Map<string, any>;
    L1: MemoryEntryV2[];
    L2: MemoryEntryV2[];
    L3: MemoryEntryV2[];
    L4: MemoryEntryV2[];
  }>;
  
  // L0 闪存
  private flashMemory: Map<string, any> = new Map();
  private context: string = '';
  
  // L1 工作记忆
  private workingMemory: MemoryEntryV2[] = [];
  
  // L2 经验记忆
  private experienceMemory: MemoryEntryV2[] = [];
  
  // L3 知识记忆
  private knowledgeMemory: {
    worldviews: MemoryEntryV2[];
    methodologies: MemoryEntryV2[];
    patterns: MemoryEntryV2[];
    goals: MemoryEntryV2[];
  } = { worldviews: [], methodologies: [], patterns: [], goals: [] };
  
  // L4 智慧记忆
  private wisdomMemory: {
    insights: MemoryEntryV2[];
    values: MemoryEntryV2[];
  } = { insights: [], values: [] };
  
  // 跨系统共享
  private sharedMemory: MemoryEntryV2[] = [];
  
  constructor(skillName: string = 'ai_system', baseDir: string = 'memory', config?: Partial<MemoryConfigV2>) {
    this.skillName = skillName;
    this.baseDir = baseDir;
    this.config = { ...DEFAULT_CONFIG_V2, ...config };
    
    // 🆕 初始化场景记忆空间
    this.scenarioMemories = new Map();
    Object.keys(this.config.scenarios).forEach(scenario => {
      this.scenarioMemories.set(scenario as ScenarioType, {
        L0: new Map(),
        L1: [],
        L2: [],
        L3: [],
        L4: []
      });
    });
    
    this.initializeDirectories();
    this.loadFromDisk();
    
    // 🆕 启动定期清理
    this.startPeriodicCleanup();
  }
  
  // ==================== 初始化 ====================
  
  private initializeDirectories(): void {
    const dirs = [
      'L0_flash', 'L1_working', 'L2_experience',
      'L3_knowledge', 'L4_wisdom', 'shared', 'logs'
    ];
    
    dirs.forEach(dir => {
      const fullPath = path.join(this.baseDir, this.skillName, dir);
      if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
      }
    });
  }
  
  private loadFromDisk(): void {
    // 加载逻辑（简化）
    console.log(`[MemoryV2] 加载记忆: ${this.skillName}`);
  }
  
  private saveToDisk(): void {
    // 保存逻辑（简化）
    console.log(`[MemoryV2] 保存记忆: ${this.skillName}`);
  }
  
  // ==================== 🆕 场景管理 ====================
  
  /**
   * 设置当前场景
   */
  setScenario(scenario: ScenarioType): void {
    if (!this.config.scenarios[scenario]) {
      console.warn(`[MemoryV2] 未知场景: ${scenario}，使用通用场景`);
      this.currentScenario = 'general';
    } else {
      this.currentScenario = scenario;
      console.log(`[MemoryV2] 切换场景: ${scenario}`);
    }
  }
  
  /**
   * 获取当前场景
   */
  getScenario(): ScenarioType {
    return this.currentScenario;
  }
  
  /**
   * 获取场景配置
   */
  getScenarioConfig(scenario?: ScenarioType): ScenarioConfig {
    return this.config.scenarios[scenario || this.currentScenario];
  }
  
  /**
   * 注册自定义场景
   */
  registerScenario(config: ScenarioConfig): void {
    this.config.scenarios[config.name] = config;
    this.scenarioMemories.set(config.name, {
      L0: new Map(),
      L1: [],
      L2: [],
      L3: [],
      L4: []
    });
    console.log(`[MemoryV2] 注册场景: ${config.name}`);
  }
  
  // ==================== 🆕 元数据管理 ====================
  
  /**
   * 创建记忆元数据
   */
  private createMetadata(source: SystemType = 'shared'): MemoryMetadata {
    return {
      source,
      sourceCredibility: this.getSourceCredibility(source),
      contextFingerprint: {
        timestamp: new Date().toISOString(),
        scenario: this.currentScenario,
        environment: {}
      },
      resultTracking: [],
      stats: {
        accessCount: 0,
        successRate: 1.0,
        lastUsedAt: new Date().toISOString()
      }
    };
  }
  
  /**
   * 获取来源可信度
   */
  private getSourceCredibility(source: SystemType): number {
    const credibility: Record<SystemType, number> = {
      'signal': 0.85,
      'workflow': 0.80,
      'goal': 0.75,
      'shared': 0.70
    };
    return credibility[source] || 0.70;
  }
  
  /**
   * 🆕 记录使用效果（双向验证）
   */
  recordUsage(entryId: string, effect: 'success' | 'failure' | 'neutral', feedback?: string): void {
    const entry = this.findEntryById(entryId);
    if (!entry) {
      console.warn(`[MemoryV2] 未找到记忆条目: ${entryId}`);
      return;
    }
    
    // 记录结果追踪
    entry.metadata.resultTracking.push({
      usedAt: new Date().toISOString(),
      scenario: this.currentScenario,
      effect,
      feedback
    });
    
    // 更新统计信息
    entry.metadata.stats.accessCount++;
    entry.metadata.stats.lastUsedAt = new Date().toISOString();
    
    // 根据效果调整重要性
    if (effect === 'success') {
      entry.importance = Math.min(5, entry.importance + this.config.feedback.successBonus);
      entry.metadata.stats.successRate = this.calculateSuccessRate(entry);
    } else if (effect === 'failure') {
      entry.importance = Math.max(
        this.config.feedback.minImportance,
        entry.importance - this.config.feedback.failurePenalty
      );
      entry.metadata.stats.successRate = this.calculateSuccessRate(entry);
    }
    
    console.log(`[MemoryV2] 记录使用效果: ${entryId} -> ${effect}, 重要性: ${entry.importance.toFixed(2)}`);
  }
  
  /**
   * 计算成功率
   */
  private calculateSuccessRate(entry: MemoryEntryV2): number {
    const tracking = entry.metadata.resultTracking;
    if (tracking.length === 0) return 1.0;
    
    const successCount = tracking.filter(t => t.effect === 'success').length;
    return successCount / tracking.length;
  }
  
  /**
   * 根据ID查找记忆条目
   */
  private findEntryById(id: string): MemoryEntryV2 | null {
    // 在各层记忆中查找
    const allEntries = [
      ...this.workingMemory,
      ...this.experienceMemory,
      ...this.knowledgeMemory.worldviews,
      ...this.knowledgeMemory.methodologies,
      ...this.knowledgeMemory.patterns,
      ...this.knowledgeMemory.goals,
      ...this.wisdomMemory.insights,
      ...this.wisdomMemory.values
    ];
    
    return allEntries.find(e => e.id === id) || null;
  }
  
  // ==================== 🆕 智能检索 ====================
  
  /**
   * 智能检索（语义相似度 + 领域约束）
   */
  smartQuery(query: string, options?: {
    scenario?: ScenarioType;
    minCredibility?: number;
    minSuccessRate?: number;
    maxAge?: number;
  }): MemoryEntryV2[] {
    const scenario = options?.scenario || this.currentScenario;
    const scenarioConfig = this.config.scenarios[scenario];
    
    // 获取所有相关记忆
    const allEntries = this.getAllEntries();
    
    // 过滤和排序
    let results = allEntries.filter(entry => {
      // 1. 领域约束
      if (!scenarioConfig.domainConstraints.isRelevant(query, entry)) {
        return false;
      }
      
      // 2. 可信度过滤
      if (options?.minCredibility && entry.metadata.sourceCredibility < options.minCredibility) {
        return false;
      }
      
      // 3. 成功率过滤
      if (options?.minSuccessRate && entry.metadata.stats.successRate < options.minSuccessRate) {
        return false;
      }
      
      // 4. 时间过滤
      if (options?.maxAge) {
        const age = (Date.now() - new Date(entry.createdAt).getTime()) / (24 * 60 * 60 * 1000);
        if (age > options.maxAge) return false;
      }
      
      return true;
    });
    
    // 排序：综合评分 = 重要性 × 可信度 × 成功率 × 时间衰减
    results.sort((a, b) => {
      const scoreA = this.calculateEntryScore(a, query, scenario);
      const scoreB = this.calculateEntryScore(b, query, scenario);
      return scoreB - scoreA;
    });
    
    return results;
  }
  
  /**
   * 计算记忆条目综合评分
   */
  private calculateEntryScore(entry: MemoryEntryV2, query: string, scenario: ScenarioType): number {
    const scenarioConfig = this.config.scenarios[scenario];
    
    // 基础分
    let score = entry.importance;
    
    // 可信度加权
    score *= entry.metadata.sourceCredibility;
    
    // 成功率加权
    score *= entry.metadata.stats.successRate;
    
    // 时间衰减
    const ageInDays = (Date.now() - new Date(entry.createdAt).getTime()) / (24 * 60 * 60 * 1000);
    const timeDecay = Math.exp(-this.config.forgetting.decayRate * ageInDays);
    score *= timeDecay;
    
    // 场景优先级调整
    score = scenarioConfig.domainConstraints.adjustPriority(entry, { query });
    
    return score;
  }
  
  /**
   * 获取所有记忆条目
   */
  private getAllEntries(): MemoryEntryV2[] {
    return [
      ...this.workingMemory,
      ...this.experienceMemory,
      ...this.knowledgeMemory.worldviews,
      ...this.knowledgeMemory.methodologies,
      ...this.knowledgeMemory.patterns,
      ...this.knowledgeMemory.goals,
      ...this.wisdomMemory.insights,
      ...this.wisdomMemory.values
    ];
  }
  
  // ==================== 🆕 记忆流动 ====================
  
  /**
   * 执行记忆压缩（短期 → 中期）
   */
  compress(): void {
    const scenarioConfig = this.config.scenarios[this.currentScenario];
    
    // 找出需要压缩的记忆
    const toCompress = this.workingMemory.filter(entry => 
      scenarioConfig.compressionRules.shouldCompress(entry)
    );
    
    // 压缩并移入中期记忆
    toCompress.forEach(entry => {
      // 创建压缩后的条目
      const compressed: MemoryEntryV2 = {
        ...entry,
        level: 'L2',
        value: this.compressValue(entry, scenarioConfig.compressionRules.preserveFields)
      };
      
      this.experienceMemory.push(compressed);
      
      // 从工作记忆中移除
      const index = this.workingMemory.indexOf(entry);
      if (index > -1) {
        this.workingMemory.splice(index, 1);
      }
    });
    
    console.log(`[MemoryV2] 压缩 ${toCompress.length} 条记忆到中期记忆`);
  }
  
  /**
   * 压缩记忆值
   */
  private compressValue(entry: MemoryEntryV2, preserveFields: string[]): any {
    if (typeof entry.value === 'string') {
      return entry.value;
    }
    
    const compressed: any = {};
    preserveFields.forEach(field => {
      if ((entry.value as any)[field] !== undefined) {
        compressed[field] = (entry.value as any)[field];
      }
    });
    
    return compressed;
  }
  
  /**
   * 执行模式提炼（中期 → 长期）
   */
  extract(): void {
    const scenarioConfig = this.config.scenarios[this.currentScenario];
    
    // 按类别分组
    const grouped = this.groupEntriesByKey(this.experienceMemory);
    
    // 对每组进行模式提炼
    Object.entries(grouped).forEach(([key, entries]) => {
      if (scenarioConfig.extractionRules.shouldExtract(entries)) {
        const pattern = scenarioConfig.extractionRules.extractPattern(entries);
        
        // 创建长期记忆条目
        const extracted: MemoryEntryV2 = {
          id: this.generateId(),
          level: 'L3',
          category: 'pattern',
          key: `模式_${key}`,
          value: pattern,
          tags: ['extracted', 'pattern'],
          importance: Math.max(...entries.map(e => e.importance)),
          metadata: this.createMetadata('shared'),
          createdAt: new Date().toISOString(),
          accessedAt: new Date().toISOString()
        };
        
        this.knowledgeMemory.patterns.push(extracted);
        console.log(`[MemoryV2] 提炼模式: ${key}`);
      }
    });
  }
  
  /**
   * 按键分组
   */
  private groupEntriesByKey(entries: MemoryEntryV2[]): Record<string, MemoryEntryV2[]> {
    const grouped: Record<string, MemoryEntryV2[]> = {};
    
    entries.forEach(entry => {
      const key = entry.key.split('_')[0]; // 取前缀作为分组键
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(entry);
    });
    
    return grouped;
  }
  
  // ==================== 🆕 遗忘机制 ====================
  
  /**
   * 启动定期清理
   */
  private startPeriodicCleanup(): void {
    setInterval(() => {
      this.cleanup();
    }, this.config.forgetting.cleanupInterval);
  }
  
  /**
   * 清理低价值记忆
   */
  cleanup(): void {
    const threshold = this.config.forgetting.threshold;
    
    // 清理经验记忆
    const beforeL2 = this.experienceMemory.length;
    this.experienceMemory = this.experienceMemory.filter(entry => {
      const score = this.calculateEntryScore(entry, '', this.currentScenario);
      return score >= threshold;
    });
    
    // 清理知识记忆
    const beforeL3 = this.knowledgeMemory.patterns.length;
    this.knowledgeMemory.patterns = this.knowledgeMemory.patterns.filter(entry => {
      const score = this.calculateEntryScore(entry, '', this.currentScenario);
      return score >= threshold;
    });
    
    console.log(`[MemoryV2] 清理: L2 ${beforeL2 - this.experienceMemory.length}条, L3 ${beforeL3 - this.knowledgeMemory.patterns.length}条`);
  }
  
  // ==================== 基础操作 ====================
  
  /**
   * 添加到L1工作记忆
   */
  addToL1(key: string, value: string, category: MemoryCategory, importance: number = 3, source: SystemType = 'shared'): void {
    const entry: MemoryEntryV2 = {
      id: this.generateId(),
      level: 'L1',
      category,
      key,
      value,
      tags: [],
      importance,
      metadata: this.createMetadata(source),
      createdAt: new Date().toISOString(),
      accessedAt: new Date().toISOString()
    };
    
    this.workingMemory.push(entry);
    
    // 检查是否需要压缩
    if (this.workingMemory.length >= this.config.L1_MAX_LINES) {
      this.compress();
    }
  }
  
  /**
   * 添加到L2经验记忆
   */
  addToL2(key: string, value: string | object, category: MemoryCategory, importance: number, tags: string[] = [], source: SystemType = 'shared'): void {
    const entry: MemoryEntryV2 = {
      id: this.generateId(),
      level: 'L2',
      category,
      key,
      value,
      tags,
      importance,
      metadata: this.createMetadata(source),
      createdAt: new Date().toISOString(),
      accessedAt: new Date().toISOString()
    };
    
    this.experienceMemory.push(entry);
    
    // 检查是否需要提炼
    if (this.experienceMemory.length >= this.config.L2_MAX_ENTRIES * 0.8) {
      this.extract();
    }
  }
  
  /**
   * 生成ID
   */
  private generateId(): string {
    return Math.random().toString(36).substring(2, 10);
  }
  
  // ==================== 其他方法 ====================
  
  setVariable(key: string, value: any): void {
    this.flashMemory.set(key, value);
  }
  
  getVariable(key: string): any {
    return this.flashMemory.get(key);
  }
  
  setContext(context: string): void {
    this.context = context;
  }
  
  getContext(): string {
    return this.context;
  }
  
  /**
   * 获取系统摘要
   */
  getSummary(): string {
    return `
=== 统一记忆系统 V2 摘要 ===
技能名称: ${this.skillName}
当前场景: ${this.currentScenario}
最后更新: ${new Date().toISOString()}

【L0闪存】变量数: ${this.flashMemory.size}/${this.config.L0_MAX_ITEMS}
【L1工作记忆】条目数: ${this.workingMemory.length}/${this.config.L1_MAX_LINES}
【L2经验记忆】条目数: ${this.experienceMemory.length}/${this.config.L2_MAX_ENTRIES}
【L3知识记忆】模式: ${this.knowledgeMemory.patterns.length}条
【L4智慧记忆】洞察: ${this.wisdomMemory.insights.length}条

场景配置: ${Object.keys(this.config.scenarios).join(', ')}
    `.trim();
  }
  
  /**
   * 健康检查
   */
  healthCheck(): any {
    return {
      status: 'OK',
      scenario: this.currentScenario,
      levels: {
        L0: { usage: `${this.flashMemory.size}/${this.config.L0_MAX_ITEMS}`, status: 'OK' },
        L1: { usage: `${this.workingMemory.length}/${this.config.L1_MAX_LINES}`, status: 'OK' },
        L2: { usage: `${this.experienceMemory.length}/${this.config.L2_MAX_ENTRIES}`, status: 'OK' },
        L3: { usage: `${this.knowledgeMemory.patterns.length}`, status: 'OK' },
        L4: { usage: `${this.wisdomMemory.insights.length}`, status: 'OK' }
      }
    };
  }
}

export default UnifiedMemorySystemV2;
