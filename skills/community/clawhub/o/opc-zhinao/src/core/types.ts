/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * OPC智脑五阶段创业诊断 - 核心类型定义
 * 
 * 本文件定义了五阶段模型的所有核心类型，包括：
 * - 五阶段枚举及阶段信息
 * - 业务维度输入（五维度判定模型）
 * - 判定结果与矛盾检测结果
 * - Skill元数据与输入输出定义
 * - 结构化输出Schema类型
 */

// ============================================================
// 五阶段枚举
// ============================================================

/**
 * 创业五阶段枚举
 * - IDEA: 构思期 - Idea可行性研判
 * - MVP: 原型期 - MVP精益设计
 * - ENTITY: 实体期 - OPC合规落地
 * - VALIDATION: 验证期 - 种子用户冷启动
 * - SCALE: 规模化期 - 规模化增长
 */
export enum StageEnum {
  IDEA = 'IDEA',
  MVP = 'MVP',
  ENTITY = 'ENTITY',
  VALIDATION = 'VALIDATION',
  SCALE = 'SCALE',
}

/**
 * 阶段中文名称映射
 */
export const STAGE_LABELS: Record<StageEnum, string> = {
  [StageEnum.IDEA]: '构思期',
  [StageEnum.MVP]: '原型期',
  [StageEnum.ENTITY]: '实体期',
  [StageEnum.VALIDATION]: '验证期',
  [StageEnum.SCALE]: '规模化期',
};

/**
 * 阶段完整信息
 */
export interface StageInfo {
  /** 阶段枚举值 */
  stage: StageEnum;
  /** 阶段中文名 */
  label: string;
  /** 阶段序号（1-5） */
  order: number;
  /** 阶段描述 */
  description: string;
  /** 该阶段核心目标 */
  goal: string;
  /** 该阶段关键风险 */
  risk: string;
  /** 该阶段对应的Skill名称 */
  skillName: string;
  /** 进入下一阶段的条件 */
  graduationCriteria: string;
}

// ============================================================
// 五维度判定模型
// ============================================================

/**
 * 需求验证程度（0-100分）
 * - 0-20: 仅有模糊想法
 * - 21-40: 有初步需求假设
 * - 41-60: 已做需求验证
 * - 61-80: 需求已验证且有付费意愿
 * - 81-100: 需求强验证，有预付款/意向金
 */
export type DimensionScore = number;

/**
 * 五维度业务输入
 * 每个维度0-100分，用于判定当前所处阶段
 */
export interface BusinessDimensions {
  /** 需求验证度：需求是否经过真实验证 */
  demandValidation: DimensionScore;
  /** 方案成熟度：解决方案/MVP是否已成型 */
  solutionMaturity: DimensionScore;
  /** 合规完备度：法律实体/财税/合同等合规程度 */
  complianceReadiness: DimensionScore;
  /** 用户获取度：是否有种子用户/付费用户 */
  userAcquisition: DimensionScore;
  /** 规模化度：业务是否可规模化/自动化 */
  scalabilityLevel: DimensionScore;
}

/**
 * 单个维度的详细信息
 */
export interface DimensionDetail {
  /** 维度名称 */
  name: string;
  /** 维度字段名 */
  key: keyof BusinessDimensions;
  /** 得分（0-100） */
  score: DimensionScore;
  /** 得分区间说明 */
  level: string;
  /** 该维度的判定权重 */
  weight: number;
}

// ============================================================
// 判定结果
// ============================================================

/**
 * 五阶段判定结果
 */
export interface StageResult {
  /** 判定所处的阶段 */
  stage: StageEnum;
  /** 阶段中文名 */
  stageLabel: string;
  /** 判定置信度（0-1） */
  confidence: number;
  /** 各维度详细信息 */
  dimensions: DimensionDetail[];
  /** 判定理由说明 */
  reasoning: string;
  /** 建议使用的Skill */
  recommendedSkill: string;
  /** 是否存在维度矛盾 */
  hasContradiction: boolean;
}

/**
 * 维度矛盾类型
 */
export enum ContradictionType {
  /** 跳跃矛盾：某维度远超当前阶段应有水平 */
  SKIP = 'SKIP',
  /** 倒挂矛盾：后续维度得分高于前序维度 */
  REVERSE = 'REVERSE',
  /** 缺失矛盾：关键维度得分过低，与其他维度不匹配 */
  MISSING = 'MISSING',
}

/**
 * 单个矛盾详情
 */
export interface Contradiction {
  /** 矛盾类型 */
  type: ContradictionType;
  /** 涉及的维度 */
  dimensions: string[];
  /** 矛盾描述 */
  description: string;
  /** 修复建议 */
  suggestion: string;
  /** 严重程度（1-5，5最严重） */
  severity: number;
}

/**
 * 矛盾检测结果
 */
export interface ContradictionResult {
  /** 是否存在矛盾 */
  hasContradiction: boolean;
  /** 矛盾列表 */
  contradictions: Contradiction[];
  /** 整体健康度（0-100） */
  healthScore: number;
  /** 综合建议 */
  overallSuggestion: string;
}

// ============================================================
// Skill元数据与定义
// ============================================================

/**
 * Skill元数据
 */
export interface SkillMeta {
  /** Skill唯一标识 */
  id: string;
  /** Skill名称 */
  name: string;
  /** Skill中文描述 */
  description: string;
  /** 适用的阶段 */
  applicableStage: StageEnum;
  /** Skill版本 */
  version: string;
  /** 输入参数定义 */
  inputs: SkillInput[];
  /** 输出Schema定义 */
  outputSchema: Record<string, unknown>;
  /** 前置条件 */
  prerequisites: string[];
}

/**
 * Skill输入参数定义
 */
export interface SkillInput {
  /** 参数名 */
  name: string;
  /** 参数类型 */
  type: 'string' | 'number' | 'boolean' | 'object' | 'array';
  /** 是否必填 */
  required: boolean;
  /** 参数说明 */
  description: string;
  /** 默认值 */
  defaultValue?: unknown;
}

/**
 * Skill执行结果
 */
export interface SkillResult {
  /** 执行的Skill ID */
  skillId: string;
  /** 执行是否成功 */
  success: boolean;
  /** 结果数据 */
  data: Record<string, unknown>;
  /** Prompt文本（可直接传给大模型） */
  prompt: string;
  /** 错误信息（如果失败） */
  error?: string;
}

/**
 * 前置条件检查结果
 */
export interface PrerequisiteCheckResult {
  /** 是否通过 */
  passed: boolean;
  /** 未通过的条件 */
  failedConditions: string[];
  /** 当前建议阶段 */
  suggestedStage: StageEnum;
  /** 修复建议 */
  suggestions: string[];
}

// ============================================================
// 业务输入（Skill通用输入）
// ============================================================

/**
 * 创业项目基本信息
 */
export interface ProjectInfo {
  /** 项目/业务名称 */
  projectName: string;
  /** 项目描述 */
  description: string;
  /** 所属行业 */
  industry: string;
  /** 目标用户群体 */
  targetUsers: string;
  /** 核心价值主张 */
  valueProposition: string;
  /** 创业者背景/技能 */
  founderBackground: string;
  /** 可用预算（元） */
  budget?: number;
  /** 可投入时间（小时/周） */
  availableTime?: number;
}

/**
 * Skill1专用输入：Idea可行性研判
 */
export interface Skill1Input {
  /** 项目信息 */
  projectInfo: ProjectInfo;
  /** 需求描述 */
  demandDescription: string;
  /** 竞品信息（可选） */
  competitorInfo?: string;
  /** 个人技能清单 */
  personalSkills: string[];
  /** 可用预算 */
  budget: number;
  /** 可投入时间（小时/周） */
  availableTime: number;
}

/**
 * Skill2专用输入：MVP精益设计
 */
export interface Skill2Input {
  /** 项目信息 */
  projectInfo: ProjectInfo;
  /** 已验证的需求（来自Skill1输出） */
  validatedDemand: string;
  /** 核心功能列表 */
  coreFeatures: string[];
  /** 预期定价 */
  expectedPricing?: string;
  /** 交付方式 */
  deliveryMethod?: string;
}

/**
 * Skill3专用输入：OPC合规落地
 */
export interface Skill3Input {
  /** 项目信息 */
  projectInfo: ProjectInfo;
  /** 业务类型（服务/产品/混合） */
  businessType: 'service' | 'product' | 'hybrid';
  /** 预计月营收 */
  expectedMonthlyRevenue?: number;
  /** 是否有员工 */
  hasEmployees?: boolean;
  /** 所在城市 */
  city?: string;
}

/**
 * Skill4专用输入：种子用户冷启动
 */
export interface Skill4Input {
  /** 项目信息 */
  projectInfo: ProjectInfo;
  /** 产品/MVP描述 */
  productDescription: string;
  /** 当前定价 */
  currentPricing: string;
  /** 已有用户数 */
  existingUsers?: number;
  /** 获客渠道偏好 */
  channelPreference?: string[];
}

/**
 * Skill5专用输入：规模化增长
 */
export interface Skill5Input {
  /** 项目信息 */
  projectInfo: ProjectInfo;
  /** 当前月营收 */
  currentMonthlyRevenue: number;
  /** 当前用户数 */
  currentUserCount: number;
  /** 主要营收来源 */
  revenueSources: string[];
  /** 当前痛点/瓶颈 */
  bottlenecks: string[];
}

// ============================================================
// 结构化输出类型
// ============================================================

/**
 * 可行性判定结果
 */
export type FeasibilityLevel = 'highly_feasible' | 'feasible' | 'challenging' | 'not_feasible';

/**
 * 需求类型判定
 */
export type DemandType = 'rigid' | 'improvement' | 'fake';

/**
 * 需求真伪校验结果
 */
export interface DemandValidationResult {
  /** 需求类型 */
  demandType: DemandType;
  /** 需求类型中文说明 */
  demandTypeLabel: string;
  /** 判定理由 */
  reasoning: string;
  /** 验证建议 */
  validationSuggestion: string;
}

/**
 * 个人匹配度评估结果
 */
export interface PersonalMatchResult {
  /** 技能匹配度（0-100） */
  skillMatch: number;
  /** 时间匹配度（0-100） */
  timeMatch: number;
  /** 预算匹配度（0-100） */
  budgetMatch: number;
  /** 综合匹配度（0-100） */
  overallMatch: number;
  /** 短板分析 */
  gaps: string[];
  /** 提升建议 */
  suggestions: string[];
}

/**
 * 竞品分析结果
 */
export interface CompetitorAnalysisResult {
  /** 竞品名称 */
  name: string;
  /** 竞品打法 */
  approach: string;
  /** 定价策略 */
  pricing: string;
  /** 优势 */
  strengths: string[];
  /** 劣势 */
  weaknesses: string[];
  /** 单人创业者应对策略 */
  counterStrategy: string;
}

/**
 * MVP功能项
 */
export interface MVPFeature {
  /** 功能名称 */
  name: string;
  /** 功能描述 */
  description: string;
  /** 是否为核心功能 */
  isCore: boolean;
  /** 所属产品层（引流款/利润款/被动产品） */
  productLayer: 'traffic' | 'profit' | 'passive';
  /** 预估开发时间（小时） */
  estimatedHours: number;
  /** 优先级（1最高） */
  priority: number;
}

/**
 * 合规事项
 */
export interface ComplianceItem {
  /** 事项名称 */
  name: string;
  /** 事项分类 */
  category: string;
  /** 是否必须 */
  required: boolean;
  /** 办理说明 */
  instruction: string;
  /** 预估费用 */
  estimatedCost?: number;
  /** 预估时间（天） */
  estimatedDays?: number;
  /** 优先级 */
  priority: number;
}

/**
 * 获客渠道
 */
export interface AcquisitionChannel {
  /** 渠道名称 */
  name: string;
  /** 渠道类型 */
  type: string;
  /** 预计成本 */
  estimatedCost: string;
  /** 预计效果 */
  expectedEffect: string;
  /** 操作难度（1-5） */
  difficulty: number;
  /** 具体操作步骤 */
  steps: string[];
}

/**
 * 风险项
 */
export interface RiskItem {
  /** 风险名称 */
  name: string;
  /** 风险类别 */
  category: string;
  /** 严重程度（1-5） */
  severity: number;
  /** 发生概率（1-5） */
  probability: number;
  /** 预警信号 */
  warningSigns: string[];
  /** 应对策略 */
  mitigationStrategy: string;
}