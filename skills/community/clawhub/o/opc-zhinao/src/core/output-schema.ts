/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * OPC智脑五阶段创业诊断 - 结构化输出Schema
 * 
 * 定义每个Skill的结构化输出JSON Schema，
 * 确保无论在哪个AI平台使用，输出格式都一致。
 * 
 * 所有Schema遵循JSON Schema Draft-07规范，
 * 可直接用于OpenAI Function Calling、
 * Dify输出变量、LangChain Output Parser等。
 */

// ============================================================
// 通用Schema片段
// ============================================================

/** 通用字符串项 */
const stringItem = {
  type: 'string',
  description: '条目说明',
};

/** 通用字符串数组 */
const stringArray = {
  type: 'array',
  items: { type: 'string' },
  description: '字符串列表',
};

// ============================================================
// Skill1：Idea可行性研判 输出Schema
// ============================================================

export const skill1OutputSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  title: 'OPC项目可行性分析报告',
  description: 'Skill1 - Idea可行性研判的结构化输出',
  type: 'object',
  properties: {
    reportTitle: {
      type: 'string',
      description: '报告标题',
    },
    projectName: {
      type: 'string',
      description: '项目名称',
    },
    demandValidation: {
      type: 'object',
      description: '需求真伪校验结果',
      properties: {
        demandType: {
          type: 'string',
          enum: ['rigid', 'improvement', 'fake'],
          description: '需求类型：rigid=刚需, improvement=改善型, fake=伪需求',
        },
        demandTypeLabel: {
          type: 'string',
          enum: ['刚需', '改善型', '伪需求'],
          description: '需求类型中文标签',
        },
        reasoning: {
          type: 'string',
          description: '判定理由',
        },
        validationSuggestion: {
          type: 'string',
          description: '需求验证建议',
        },
        evidenceForRigid: stringArray,
        evidenceAgainstRigid: stringArray,
      },
      required: ['demandType', 'demandTypeLabel', 'reasoning'],
    },
    personalMatch: {
      type: 'object',
      description: '个人匹配度测评',
      properties: {
        skillMatch: { type: 'number', minimum: 0, maximum: 100, description: '技能匹配度' },
        timeMatch: { type: 'number', minimum: 0, maximum: 100, description: '时间匹配度' },
        budgetMatch: { type: 'number', minimum: 0, maximum: 100, description: '预算匹配度' },
        overallMatch: { type: 'number', minimum: 0, maximum: 100, description: '综合匹配度' },
        gaps: stringArray,
        suggestions: stringArray,
      },
      required: ['skillMatch', 'timeMatch', 'budgetMatch', 'overallMatch'],
    },
    competitorAnalysis: {
      type: 'array',
      description: '竞品格局分析',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '竞品名称' },
          approach: { type: 'string', description: '竞品打法' },
          pricing: { type: 'string', description: '定价策略' },
          strengths: stringArray,
          weaknesses: stringArray,
          counterStrategy: { type: 'string', description: '单人创业者应对策略' },
        },
        required: ['name', 'approach', 'pricing'],
      },
    },
    feasibilityLevel: {
      type: 'string',
      enum: ['highly_feasible', 'feasible', 'challenging', 'not_feasible'],
      description: '可行性等级',
    },
    feasibilityLabel: {
      type: 'string',
      enum: ['高度可行', '可行', '有挑战', '不可行'],
      description: '可行性中文标签',
    },
    summary: {
      type: 'string',
      description: '可行性研判总结',
    },
    alternativeTracks: {
      type: 'array',
      description: '替代赛道建议（不可行时提供）',
      items: {
        type: 'object',
        properties: {
          trackName: { type: 'string', description: '替代赛道名称' },
          reason: { type: 'string', description: '推荐理由' },
          entryBarrier: { type: 'string', description: '进入门槛' },
        },
      },
    },
    nextStep: {
      type: 'string',
      description: '下一步行动建议',
    },
  },
  required: ['reportTitle', 'projectName', 'demandValidation', 'personalMatch', 'feasibilityLevel', 'feasibilityLabel', 'summary'],
} as const;

// ============================================================
// Skill2：MVP精益设计 输出Schema
// ============================================================

export const skill2OutputSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  title: 'OPC精益MVP设计方案',
  description: 'Skill2 - MVP精益设计的结构化输出',
  type: 'object',
  properties: {
    reportTitle: { type: 'string', description: '报告标题' },
    projectName: { type: 'string', description: '项目名称' },
    mvpScope: {
      type: 'object',
      description: 'MVP极简裁剪方案',
      properties: {
        coreFeatures: {
          type: 'array',
          description: '核心功能列表（保留）',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string', description: '功能名称' },
              description: { type: 'string', description: '功能描述' },
              isCore: { type: 'boolean', description: '是否为核心功能' },
              estimatedHours: { type: 'number', description: '预估开发时间（小时）' },
              priority: { type: 'number', description: '优先级（1最高）' },
            },
            required: ['name', 'description', 'isCore', 'priority'],
          },
        },
        cutFeatures: {
          type: 'array',
          description: '裁剪功能列表（砍掉）',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string', description: '功能名称' },
              cutReason: { type: 'string', description: '裁剪理由' },
              resumeCondition: { type: 'string', description: '恢复条件' },
            },
            required: ['name', 'cutReason'],
          },
        },
      },
      required: ['coreFeatures', 'cutFeatures'],
    },
    productLayers: {
      type: 'object',
      description: '三层产品体系',
      properties: {
        trafficProduct: {
          type: 'object',
          description: '引流款',
          properties: {
            name: { type: 'string', description: '产品名称' },
            description: { type: 'string', description: '产品描述' },
            pricing: { type: 'string', description: '定价' },
            purpose: { type: 'string', description: '引流目的' },
          },
          required: ['name', 'description', 'pricing'],
        },
        profitProduct: {
          type: 'object',
          description: '利润款',
          properties: {
            name: { type: 'string', description: '产品名称' },
            description: { type: 'string', description: '产品描述' },
            pricing: { type: 'string', description: '定价' },
            margin: { type: 'string', description: '利润率说明' },
          },
          required: ['name', 'description', 'pricing'],
        },
        passiveProduct: {
          type: 'object',
          description: '被动产品',
          properties: {
            name: { type: 'string', description: '产品名称' },
            description: { type: 'string', description: '产品描述' },
            pricing: { type: 'string', description: '定价' },
            automationLevel: { type: 'string', description: '自动化程度' },
          },
          required: ['name', 'description', 'pricing'],
        },
      },
      required: ['trafficProduct', 'profitProduct'],
    },
    deliveryCost: {
      type: 'object',
      description: '单人交付成本测算',
      properties: {
        timeCost: { type: 'string', description: '时间成本' },
        toolCost: { type: 'string', description: '工具成本' },
        trialCost: { type: 'string', description: '试错成本' },
        totalCost: { type: 'string', description: '总成本估算' },
        costControlTips: stringArray,
      },
      required: ['timeCost', 'toolCost', 'totalCost'],
    },
    firstOrderPlan: {
      type: 'object',
      description: '首单冷交付方案',
      properties: {
        approach: { type: 'string', description: '冷交付方式' },
        sampleStandard: { type: 'string', description: '小样标准' },
        pricingLogic: { type: 'string', description: '报价逻辑' },
        timeline: { type: 'string', description: '交付时间线' },
      },
      required: ['approach', 'sampleStandard', 'pricingLogic'],
    },
    summary: { type: 'string', description: 'MVP设计总结' },
    nextStep: { type: 'string', description: '下一步行动建议' },
  },
  required: ['reportTitle', 'projectName', 'mvpScope', 'productLayers', 'deliveryCost', 'summary'],
} as const;

// ============================================================
// Skill3：OPC合规落地 输出Schema
// ============================================================

export const skill3OutputSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  title: 'OPC合规落地规划方案',
  description: 'Skill3 - OPC合规落地规划的结构化输出',
  type: 'object',
  properties: {
    reportTitle: { type: 'string', description: '报告标题' },
    projectName: { type: 'string', description: '项目名称' },
    entityRecommendation: {
      type: 'object',
      description: '主体选型建议',
      properties: {
        recommendedType: {
          type: 'string',
          enum: ['individual_business', 'one_person_company'],
          description: '推荐类型：individual_business=个体户, one_person_company=一人有限公司',
        },
        typeLabel: { type: 'string', description: '类型中文标签' },
        reasoning: { type: 'string', description: '选型理由' },
        pros: stringArray,
        cons: stringArray,
      },
      required: ['recommendedType', 'typeLabel', 'reasoning'],
    },
    businessScope: {
      type: 'object',
      description: '经营范围推荐',
      properties: {
        primaryScopes: stringArray,
        extendedScopes: stringArray,
        scopeExplanation: { type: 'string', description: '经营范围说明' },
      },
      required: ['primaryScopes'],
    },
    compliancePoints: {
      type: 'object',
      description: '2024新公司法OPC合规要点',
      properties: {
        keyPoints: stringArray,
        riskAlerts: stringArray,
        actionItems: stringArray,
      },
      required: ['keyPoints'],
    },
    taxPlanning: {
      type: 'object',
      description: '初创财税规划',
      properties: {
        taxpayerType: { type: 'string', description: '纳税人类型建议' },
        zeroFilingGuide: { type: 'string', description: '零申报指南' },
        costInvoiceStrategy: { type: 'string', description: '成本票策略' },
        monthlyRoutine: stringArray,
      },
      required: ['taxpayerType'],
    },
    templates: {
      type: 'array',
      description: '商用模板清单',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '模板名称' },
          category: { type: 'string', description: '分类' },
          description: { type: 'string', description: '模板说明' },
          priority: { type: 'number', description: '优先级' },
        },
        required: ['name', 'category'],
      },
    },
    preparationChecklist: {
      type: 'array',
      description: '前期筹备清单',
      items: {
        type: 'object',
        properties: {
          item: { type: 'string', description: '事项名称' },
          category: { type: 'string', description: '分类' },
          required: { type: 'boolean', description: '是否必须' },
          estimatedCost: { type: 'string', description: '预估费用' },
          estimatedDays: { type: 'number', description: '预估天数' },
          priority: { type: 'number', description: '优先级' },
        },
        required: ['item', 'category', 'required', 'priority'],
      },
    },
    summary: { type: 'string', description: '合规规划总结' },
    nextStep: { type: 'string', description: '下一步行动建议' },
  },
  required: ['reportTitle', 'projectName', 'entityRecommendation', 'summary'],
} as const;

// ============================================================
// Skill4：种子用户冷启动 输出Schema
// ============================================================

export const skill4OutputSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  title: 'OPC种子用户冷启动方案',
  description: 'Skill4 - 种子用户冷启动的结构化输出',
  type: 'object',
  properties: {
    reportTitle: { type: 'string', description: '报告标题' },
    projectName: { type: 'string', description: '项目名称' },
    acquisitionChannels: {
      type: 'array',
      description: '低成本获客渠道方案',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '渠道名称' },
          type: { type: 'string', description: '渠道类型' },
          estimatedCost: { type: 'string', description: '预计成本' },
          expectedEffect: { type: 'string', description: '预计效果' },
          difficulty: { type: 'number', minimum: 1, maximum: 5, description: '操作难度（1-5）' },
          steps: stringArray,
        },
        required: ['name', 'type', 'estimatedCost', 'expectedEffect', 'difficulty'],
      },
    },
    seedUserStrategy: {
      type: 'object',
      description: '种子用户招募策略',
      properties: {
        trialRules: { type: 'string', description: '试用规则' },
        smallOrderSystem: { type: 'string', description: '小单体系' },
        iceBreakPlan: { type: 'string', description: '破冰方案' },
        targetSeedCount: { type: 'number', description: '目标种子用户数' },
      },
      required: ['trialRules', 'smallOrderSystem', 'iceBreakPlan'],
    },
    feedbackFramework: {
      type: 'object',
      description: '用户反馈拆解框架',
      properties: {
        productIssues: stringArray,
        serviceGaps: stringArray,
        optimizationPriority: stringArray,
      },
      required: ['productIssues', 'serviceGaps', 'optimizationPriority'],
    },
    pricingDiagnosis: {
      type: 'object',
      description: '定价诊断与调价方案',
      properties: {
        currentPricingIssue: { type: 'string', description: '当前定价问题' },
        suggestedPricing: { type: 'string', description: '建议定价' },
        pricingLogic: { type: 'string', description: '定价逻辑' },
        adjustmentPlan: { type: 'string', description: '调价方案' },
      },
      required: ['currentPricingIssue', 'suggestedPricing'],
    },
    businessLoop: {
      type: 'object',
      description: '最小商业闭环验证',
      properties: {
        loopSteps: stringArray,
        validationMetrics: stringArray,
        passCriteria: { type: 'string', description: '闭环通过标准' },
      },
      required: ['loopSteps', 'validationMetrics', 'passCriteria'],
    },
    summary: { type: 'string', description: '冷启动方案总结' },
    nextStep: { type: 'string', description: '下一步行动建议' },
  },
  required: ['reportTitle', 'projectName', 'acquisitionChannels', 'seedUserStrategy', 'businessLoop', 'summary'],
} as const;

// ============================================================
// Skill5：规模化增长 输出Schema
// ============================================================

export const skill5OutputSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  title: 'OPC规模化增长方案',
  description: 'Skill5 - 规模化增长的结构化输出',
  type: 'object',
  properties: {
    reportTitle: { type: 'string', description: '报告标题' },
    projectName: { type: 'string', description: '项目名称' },
    businessDecomposition: {
      type: 'object',
      description: '业务拆解',
      properties: {
        aiAutomatable: stringArray,
        outsourceable: stringArray,
        mustDoYourself: stringArray,
        automationSuggestions: stringArray,
      },
      required: ['aiAutomatable', 'outsourceable', 'mustDoYourself'],
    },
    productLineUpgrade: {
      type: 'object',
      description: '产品线升级路径',
      properties: {
        currentStage: { type: 'string', description: '当前阶段（定制/标准化/被动收入）' },
        targetStage: { type: 'string', description: '目标阶段' },
        upgradeSteps: stringArray,
        timeline: { type: 'string', description: '升级时间线' },
      },
      required: ['currentStage', 'targetStage', 'upgradeSteps'],
    },
    channelScale: {
      type: 'object',
      description: '渠道规模化方案',
      properties: {
        privateDomain: stringArray,
        platformMatrix: stringArray,
        partnerChannels: stringArray,
      },
      required: ['privateDomain', 'platformMatrix'],
    },
    riskWarning: {
      type: 'array',
      description: '经营风险预警',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '风险名称' },
          category: { type: 'string', description: '风险类别' },
          severity: { type: 'number', minimum: 1, maximum: 5, description: '严重程度' },
          probability: { type: 'number', minimum: 1, maximum: 5, description: '发生概率' },
          warningSigns: stringArray,
          mitigationStrategy: { type: 'string', description: '应对策略' },
        },
        required: ['name', 'category', 'severity', 'warningSigns', 'mitigationStrategy'],
      },
    },
    longTermLayout: {
      type: 'object',
      description: '长期布局',
      properties: {
        personalBrand: stringArray,
        assetAccumulation: stringArray,
        reusableAssets: stringArray,
      },
      required: ['personalBrand', 'assetAccumulation', 'reusableAssets'],
    },
    summary: { type: 'string', description: '规模化增长总结' },
    nextStep: { type: 'string', description: '下一步行动建议' },
  },
  required: ['reportTitle', 'projectName', 'businessDecomposition', 'productLineUpgrade', 'summary'],
} as const;

// ============================================================
// Schema汇总导出
// ============================================================

/**
 * 所有Skill的输出Schema汇总
 * key为Skill ID，value为对应的JSON Schema
 */
export const ALL_OUTPUT_SCHEMAS = {
  'skill1-idea-feasibility': skill1OutputSchema,
  'skill2-mvp-design': skill2OutputSchema,
  'skill3-opc-compliance': skill3OutputSchema,
  'skill4-seed-coldstart': skill4OutputSchema,
  'skill5-scale-growth': skill5OutputSchema,
} as const;

/**
 * 根据Skill ID获取对应的输出Schema
 */
export function getOutputSchema(skillId: string): Record<string, unknown> | undefined {
  return ALL_OUTPUT_SCHEMAS[skillId as keyof typeof ALL_OUTPUT_SCHEMAS];
}

// ============================================================
// 语义校验规则（L2/L3层，供ai-output-validator.ts使用）
// ============================================================

export interface SemanticRule {
  id: string;
  layer: 'L2' | 'L3';
  description: string;
  check: (output: Record<string, unknown>) => boolean;
  errorMessage: string;
  suggestion: string;
}

const SEMANTIC_RULES: Record<string, SemanticRule[]> = {
  'skill1-idea-feasibility': [
    {
      id: 'S1_001',
      layer: 'L2',
      description: '伪需求不可判定为可行',
      check: (o) => {
        const dv = o.demandValidation as any;
        const fl = o.feasibilityLevel as string;
        return !(dv?.demandType === 'fake' && (fl === 'highly_feasible' || fl === 'feasible'));
      },
      errorMessage: '需求判定为"伪需求"但可行性为"可行"，逻辑矛盾',
      suggestion: '伪需求应判定为"有挑战"或"不可行"',
    },
    {
      id: 'S1_002',
      layer: 'L3',
      description: '个人匹配度各子项应在0-100范围',
      check: (o) => {
        const pm = o.personalMatch as any;
        if (!pm) return true;
        return [pm.skillMatch, pm.timeMatch, pm.budgetMatch, pm.overallMatch]
          .filter((v) => v !== undefined)
          .every((v) => v >= 0 && v <= 100);
      },
      errorMessage: '个人匹配度子项超出0-100范围',
      suggestion: '所有匹配度评分必须在0-100之间',
    },
  ],
  'skill2-mvp-design': [
    {
      id: 'S2_001',
      layer: 'L2',
      description: 'MVP核心功能不超过3个',
      check: (o) => {
        const core = (o.mvpScope as any)?.coreFeatures;
        if (!core) return true;
        return core.length <= 3;
      },
      errorMessage: 'MVP核心功能超过3个上限',
      suggestion: '按一人创业者MVP铁律裁剪至3个以内',
    },
    {
      id: 'S2_002',
      layer: 'L3',
      description: 'MVP总开发时间不超过2周(80小时)',
      check: (o) => {
        const core = (o.mvpScope as any)?.coreFeatures;
        if (!core) return true;
        const total = core.reduce((s: number, f: any) => s + (f.estimatedHours || 0), 0);
        return total <= 80;
      },
      errorMessage: 'MVP总开发时间超过80小时',
      suggestion: '裁剪功能或延长交付时间，并标注风险',
    },
  ],
  'skill3-opc-compliance': [
    {
      id: 'S3_001',
      layer: 'L2',
      description: '主体选型必须给出理由',
      check: (o) => {
        const entity = o.entityRecommendation as any;
        if (!entity) return true;
        return !!entity.reasoning;
      },
      errorMessage: '主体选型缺少选型理由',
      suggestion: '必须给出推荐该主体类型的具体理由',
    },
  ],
  'skill4-seed-coldstart': [
    {
      id: 'S4_001',
      layer: 'L2',
      description: '目标种子用户数不低于10',
      check: (o) => {
        const target = (o.seedUserStrategy as any)?.targetSeedCount;
        if (target === undefined) return true;
        return target >= 10;
      },
      errorMessage: '目标种子用户数低于毕业条件(≥10人)',
      suggestion: '调整目标种子用户数至10人以上',
    },
  ],
  'skill5-scale-growth': [],
};

export function getSemanticRules(skillId: string): SemanticRule[] {
  return SEMANTIC_RULES[skillId] || [];
}

export function runSemanticValidation(skillId: string, output: Record<string, unknown>): { passed: boolean; failures: SemanticRule[] } {
  const rules = getSemanticRules(skillId);
  const failures = rules.filter((r) => !r.check(output));
  return { passed: failures.length === 0, failures };
}