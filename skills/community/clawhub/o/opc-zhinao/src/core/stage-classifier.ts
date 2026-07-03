/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * OPC智脑五阶段创业诊断 - 五阶段判定引擎
 * 
 * 纯TypeScript逻辑，零外部依赖。
 * 基于五维度评分模型，判定创业者当前所处阶段。
 * 
 * 核心API：
 * - classifyStage(input) → StageResult       五维度判定
 * - detectContradiction(input) → ContradictionResult  维度矛盾检测
 * - getStageInfo(stage) → StageInfo           阶段信息查询
 */

import {
  StageEnum,
  STAGE_LABELS,
  type StageInfo,
  type BusinessDimensions,
  type DimensionScore,
  type DimensionDetail,
  type StageResult,
  type ContradictionResult,
  type Contradiction,
  ContradictionType,
} from './types';

// ============================================================
// 阶段信息常量表
// ============================================================

const STAGE_INFO_MAP: Record<StageEnum, StageInfo> = {
  [StageEnum.IDEA]: {
    stage: StageEnum.IDEA,
    label: '构思期',
    order: 1,
    description: '从0到1的想法验证阶段，核心是判断Idea是否值得做',
    goal: '验证需求真伪，确认个人匹配度，完成可行性研判',
    risk: '伪需求陷阱、过度投入未验证想法、赛道选择错误',
    skillName: 'skill1-idea-feasibility',
    graduationCriteria: '需求验证通过 + 个人匹配度≥60 + 存在可行赛道',
  },
  [StageEnum.MVP]: {
    stage: StageEnum.MVP,
    label: '原型期',
    order: 2,
    description: '最小可行产品设计与交付，核心是用最小成本验证产品假设',
    goal: '设计MVP、确定三层产品体系、测算交付成本、完成首单冷交付',
    risk: '功能过度膨胀、交付成本失控、首单无法冷启动',
    skillName: 'skill2-mvp-design',
    graduationCriteria: 'MVP可交付 + 首单冷交付成功 + 交付成本可控',
  },
  [StageEnum.ENTITY]: {
    stage: StageEnum.ENTITY,
    label: '实体期',
    order: 3,
    description: '合规化运营主体搭建，核心是低成本合规落地',
    goal: '完成主体注册、财税规划、商用模板准备、前期筹备',
    risk: '合规风险、财税踩坑、过度注册/过度合规',
    skillName: 'skill3-opc-compliance',
    graduationCriteria: '主体注册完成 + 财税规划落地 + 商用模板齐备',
  },
  [StageEnum.VALIDATION]: {
    stage: StageEnum.VALIDATION,
    label: '验证期',
    order: 4,
    description: '种子用户获取与商业闭环验证，核心是证明有人愿意付费',
    goal: '获取种子用户、验证付费意愿、跑通最小商业闭环',
    risk: '获客成本过高、无付费意愿、产品市场不匹配',
    skillName: 'skill4-seed-coldstart',
    graduationCriteria: '种子用户≥10 + 付费用户≥1 + 商业闭环跑通',
  },
  [StageEnum.SCALE]: {
    stage: StageEnum.SCALE,
    label: '规模化期',
    order: 5,
    description: '从1到N的规模化增长，核心是构建可复制的增长引擎',
    goal: '业务拆解自动化、产品线升级、渠道规模化、风险预警',
    risk: '规模化失控、交付质量下降、现金流断裂、过度扩张',
    skillName: 'skill5-scale-growth',
    graduationCriteria: '月营收稳定增长 + 交付可规模化 + 增长引擎运转',
  },
};

// ============================================================
// 维度权重与区间定义
// ============================================================

/**
 * 各维度判定权重
 * 权重之和 = 1.0
 */
const DIMENSION_WEIGHTS: Record<keyof BusinessDimensions, number> = {
  demandValidation: 0.30,   // 需求验证度权重最高
  solutionMaturity: 0.25,   // 方案成熟度次之
  complianceReadiness: 0.15, // 合规完备度
  userAcquisition: 0.15,    // 用户获取度
  scalabilityLevel: 0.15,   // 规模化度
};

/**
 * 维度中文名称映射
 */
const DIMENSION_LABELS: Record<keyof BusinessDimensions, string> = {
  demandValidation: '需求验证度',
  solutionMaturity: '方案成熟度',
  complianceReadiness: '合规完备度',
  userAcquisition: '用户获取度',
  scalabilityLevel: '规模化度',
};

/**
 * 维度得分区间说明
 */
function getScoreLevel(score: DimensionScore): string {
  if (score <= 20) return '极低 - 几乎未启动';
  if (score <= 40) return '较低 - 仅有初步进展';
  if (score <= 60) return '中等 - 已有基础但不够扎实';
  if (score <= 80) return '较高 - 基本到位，有优化空间';
  return '很高 - 已充分完备';
}

// ============================================================
// 阶段判定规则
// ============================================================

/**
 * 五阶段判定阈值
 * 基于加权总分判定所处阶段
 * 
 * 判定逻辑：
 * - 总分 0-20:  构思期（IDEA）
 * - 总分 21-40: 原型期（MVP）
 * - 总分 41-60: 实体期（ENTITY）
 * - 总分 61-80: 验证期（VALIDATION）
 * - 总分 81-100: 规模化期（SCALE）
 * 
 * 同时参考关键维度的硬性条件进行微调
 */
const STAGE_THRESHOLDS = [
  { stage: StageEnum.IDEA, min: 0, max: 20 },
  { stage: StageEnum.MVP, min: 21, max: 40 },
  { stage: StageEnum.ENTITY, min: 41, max: 60 },
  { stage: StageEnum.VALIDATION, min: 61, max: 80 },
  { stage: StageEnum.SCALE, min: 81, max: 100 },
];

/**
 * 关键维度硬性条件（用于微调判定结果）
 * 如果关键维度不满足，即使总分够了也不能进入后续阶段
 */
const HARD_CONDITIONS: Record<StageEnum, (input: BusinessDimensions) => boolean> = {
  [StageEnum.IDEA]: () => true, // 构思期无前置条件
  [StageEnum.MVP]: (input) => input.demandValidation >= 40, // 需求至少经过初步验证
  [StageEnum.ENTITY]: (input) => input.demandValidation >= 50 && input.solutionMaturity >= 40, // 需求已验证+方案已成型
  [StageEnum.VALIDATION]: (input) => input.demandValidation >= 60 && input.solutionMaturity >= 50 && input.complianceReadiness >= 40, // 需求强验证+方案成熟+合规基础
  [StageEnum.SCALE]: (input) => input.demandValidation >= 70 && input.solutionMaturity >= 60 && input.complianceReadiness >= 50 && input.userAcquisition >= 50, // 全面达标
};

// ============================================================
// 核心API实现
// ============================================================

/**
 * 计算加权总分
 */
function calculateWeightedScore(input: BusinessDimensions): number {
  let totalScore = 0;
  const keys = Object.keys(DIMENSION_WEIGHTS) as (keyof BusinessDimensions)[];
  for (const key of keys) {
    // 确保得分在0-100范围内
    const clampedScore = Math.max(0, Math.min(100, input[key]));
    totalScore += clampedScore * DIMENSION_WEIGHTS[key];
  }
  return Math.round(totalScore * 100) / 100; // 保留两位小数
}

/**
 * 构建维度详细信息
 */
function buildDimensionDetails(input: BusinessDimensions): DimensionDetail[] {
  const keys = Object.keys(DIMENSION_WEIGHTS) as (keyof BusinessDimensions)[];
  return keys.map((key) => ({
    name: DIMENSION_LABELS[key],
    key,
    score: Math.max(0, Math.min(100, input[key])),
    level: getScoreLevel(input[key]),
    weight: DIMENSION_WEIGHTS[key],
  }));
}

/**
 * 基于总分判定基础阶段
 */
function classifyByScore(weightedScore: number): StageEnum {
  for (const threshold of STAGE_THRESHOLDS) {
    if (weightedScore >= threshold.min && weightedScore <= threshold.max) {
      return threshold.stage;
    }
  }
  // 兜底：超过100分归入规模化期
  return StageEnum.SCALE;
}

/**
 * 应用硬性条件修正
 * 如果硬性条件不满足，回退到满足条件的最高阶段
 */
function applyHardConditions(
  baseStage: StageEnum,
  input: BusinessDimensions
): StageEnum {
  const stageOrder = [StageEnum.IDEA, StageEnum.MVP, StageEnum.ENTITY, StageEnum.VALIDATION, StageEnum.SCALE];
  const baseIndex = stageOrder.indexOf(baseStage);

  // 从当前阶段开始，逐级检查硬性条件
  for (let i = baseIndex; i >= 0; i--) {
    if (HARD_CONDITIONS[stageOrder[i]](input)) {
      return stageOrder[i];
    }
  }

  // 兜底返回构思期
  return StageEnum.IDEA;
}

/**
 * 计算判定置信度
 * 基于总分与阶段边界的距离
 */
function calculateConfidence(weightedScore: number, stage: StageEnum): number {
  const threshold = STAGE_THRESHOLDS.find((t) => t.stage === stage);
  if (!threshold) return 0.5;

  const range = threshold.max - threshold.min;
  const midpoint = (threshold.min + threshold.max) / 2;
  const distance = Math.abs(weightedScore - midpoint);
  
  // 距中心越近置信度越高，最高0.95，最低0.5
  const maxDistance = range / 2;
  const confidence = 0.95 - (distance / maxDistance) * 0.45;
  return Math.round(confidence * 100) / 100;
}

/**
 * 生成判定理由
 */
function generateReasoning(
  stage: StageEnum,
  weightedScore: number,
  dimensions: DimensionDetail[],
  wasAdjusted: boolean
): string {
  const stageLabel = STAGE_LABELS[stage];
  const topDimensions = dimensions
    .sort((a, b) => b.score - a.score)
    .slice(0, 2);
  const bottomDimensions = dimensions
    .sort((a, b) => a.score - b.score)
    .slice(0, 2);

  let reasoning = `基于五维度加权评分（总分${weightedScore}），判定当前处于【${stageLabel}】。\n`;
  reasoning += `优势维度：${topDimensions.map((d) => `${d.name}(${d.score}分)`).join('、')}；`;
  reasoning += `短板维度：${bottomDimensions.map((d) => `${d.name}(${d.score}分)`).join('、')}。`;

  if (wasAdjusted) {
    reasoning += `\n注意：由于关键维度硬性条件未满足，已从更高阶段回退至当前阶段。建议优先补齐短板维度。`;
  }

  return reasoning;
}

// ============================================================
// 公开API
// ============================================================

/**
 * 五维度判定 - 核心API
 * 
 * 基于五维度评分，判定创业者当前所处的创业阶段。
 * 
 * @param input 五维度业务评分输入
 * @returns 阶段判定结果
 * 
 * @example
 * ```typescript
 * import { classifyStage } from 'opc-skills';
 * 
 * const result = classifyStage({
 *   demandValidation: 30,
 *   solutionMaturity: 20,
 *   complianceReadiness: 10,
 *   userAcquisition: 5,
 *   scalabilityLevel: 0,
 * });
 * 
 * console.log(result.stage);       // 'IDEA'
 * console.log(result.stageLabel);  // '构思期'
 * console.log(result.confidence);  // 0.72
 * ```
 */
export function classifyStage(input: BusinessDimensions): StageResult {
  // 1. 计算加权总分
  const weightedScore = calculateWeightedScore(input);

  // 2. 基于总分判定基础阶段
  const baseStage = classifyByScore(weightedScore);

  // 3. 应用硬性条件修正
  const adjustedStage = applyHardConditions(baseStage, input);
  const wasAdjusted = adjustedStage !== baseStage;

  // 4. 构建维度详细信息
  const dimensions = buildDimensionDetails(input);

  // 5. 计算置信度
  const confidence = calculateConfidence(weightedScore, adjustedStage);

  // 6. 检测是否存在矛盾（快速检测）
  const contradictionResult = detectContradiction(input);

  // 7. 生成判定理由
  const reasoning = generateReasoning(adjustedStage, weightedScore, dimensions, wasAdjusted);

  return {
    stage: adjustedStage,
    stageLabel: STAGE_LABELS[adjustedStage],
    confidence,
    dimensions,
    reasoning,
    recommendedSkill: STAGE_INFO_MAP[adjustedStage].skillName,
    hasContradiction: contradictionResult.hasContradiction,
  };
}

/**
 * 维度矛盾检测 - 核心API
 * 
 * 检测五维度评分中是否存在逻辑矛盾，如：
 * - 跳跃矛盾：某维度远超当前阶段应有水平
 * - 倒挂矛盾：后续维度得分高于前序维度
 * - 缺失矛盾：关键维度得分过低，与其他维度不匹配
 * 
 * @param input 五维度业务评分输入
 * @returns 矛盾检测结果
 * 
 * @example
 * ```typescript
 * import { detectContradiction } from 'opc-skills';
 * 
 * const result = detectContradiction({
 *   demandValidation: 80,
 *   solutionMaturity: 10,
 *   complianceReadiness: 5,
 *   userAcquisition: 0,
 *   scalabilityLevel: 0,
 * });
 * 
 * console.log(result.hasContradiction); // true
 * console.log(result.contradictions);    // 包含跳跃矛盾
 * ```
 */
export function detectContradiction(input: BusinessDimensions): ContradictionResult {
  const contradictions: Contradiction[] = [];

  // 维度顺序（创业逻辑上的前序关系）
  const dimensionOrder: (keyof BusinessDimensions)[] = [
    'demandValidation',
    'solutionMaturity',
    'complianceReadiness',
    'userAcquisition',
    'scalabilityLevel',
  ];

  // ---- 检测倒挂矛盾 ----
  // 后序维度得分不应显著高于前序维度
  for (let i = 1; i < dimensionOrder.length; i++) {
    const prev = input[dimensionOrder[i - 1]];
    const curr = input[dimensionOrder[i]];
    // 如果后序维度比前序维度高30分以上，视为倒挂
    if (curr - prev > 30) {
      contradictions.push({
        type: ContradictionType.REVERSE,
        dimensions: [DIMENSION_LABELS[dimensionOrder[i - 1]], DIMENSION_LABELS[dimensionOrder[i]]],
        description: `${DIMENSION_LABELS[dimensionOrder[i]]}(${curr}分)显著高于${DIMENSION_LABELS[dimensionOrder[i - 1]]}(${prev}分)，存在逻辑倒挂`,
        suggestion: `建议先提升${DIMENSION_LABELS[dimensionOrder[i - 1]]}，创业阶段应按顺序推进`,
        severity: Math.min(5, Math.floor((curr - prev) / 10)),
      });
    }
  }

  // ---- 检测跳跃矛盾 ----
  // 如果某个维度得分极高(>70)但前序维度得分很低(<30)
  for (let i = 1; i < dimensionOrder.length; i++) {
    const curr = input[dimensionOrder[i]];
    if (curr > 70) {
      // 检查是否有前序维度过低
      const lowPredecessors = dimensionOrder
        .slice(0, i)
        .filter((key) => input[key] < 30);

      if (lowPredecessors.length > 0) {
        contradictions.push({
          type: ContradictionType.SKIP,
          dimensions: [
            ...lowPredecessors.map((k) => DIMENSION_LABELS[k]),
            DIMENSION_LABELS[dimensionOrder[i]],
          ],
          description: `${DIMENSION_LABELS[dimensionOrder[i]]}已达${curr}分，但前序维度${lowPredecessors.map((k) => DIMENSION_LABELS[k]).join('、')}过低，存在跳跃`,
          suggestion: `建议先补齐前序维度，避免基础不牢导致后续返工`,
          severity: 4,
        });
      }
    }
  }

  // ---- 检测缺失矛盾 ----
  // 计算平均分，如果某维度低于平均分40分以上
  const scores = dimensionOrder.map((key) => input[key]);
  const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;

  for (const key of dimensionOrder) {
    if (avgScore - input[key] > 40 && avgScore > 30) {
      contradictions.push({
        type: ContradictionType.MISSING,
        dimensions: [DIMENSION_LABELS[key]],
        description: `${DIMENSION_LABELS[key]}(${input[key]}分)远低于其他维度平均水平(${Math.round(avgScore)}分)，存在明显短板`,
        suggestion: `建议重点提升${DIMENSION_LABELS[key]}，短板维度可能成为整体瓶颈`,
        severity: 3,
      });
    }
  }

  // ---- 计算健康度 ----
  // 基于矛盾数量和严重程度
  const totalSeverity = contradictions.reduce((sum, c) => sum + c.severity, 0);
  const healthScore = Math.max(0, Math.round(100 - totalSeverity * 8));

  // ---- 生成综合建议 ----
  let overallSuggestion = '';
  if (contradictions.length === 0) {
    overallSuggestion = '五维度评分逻辑一致，无矛盾 detected。建议按当前阶段推进。';
  } else {
    const highSeverity = contradictions.filter((c) => c.severity >= 4);
    if (highSeverity.length > 0) {
      overallSuggestion = `检测到${contradictions.length}个维度矛盾，其中${highSeverity.length}个较为严重。建议优先处理严重矛盾，确保创业阶段推进的合理性。`;
    } else {
      overallSuggestion = `检测到${contradictions.length}个轻度维度矛盾。建议关注并逐步调整，确保各维度协调发展。`;
    }
  }

  return {
    hasContradiction: contradictions.length > 0,
    contradictions,
    healthScore,
    overallSuggestion,
  };
}

/**
 * 阶段信息查询 - 核心API
 * 
 * 获取指定阶段的完整信息，包括描述、目标、风险、毕业条件等。
 * 
 * @param stage 阶段枚举值
 * @returns 阶段完整信息
 * 
 * @example
 * ```typescript
 * import { getStageInfo, StageEnum } from 'opc-skills';
 * 
 * const info = getStageInfo(StageEnum.MVP);
 * console.log(info.label);               // '原型期'
 * console.log(info.goal);                // MVP阶段目标
 * console.log(info.graduationCriteria);  // 进入下一阶段的条件
 * ```
 */
export function getStageInfo(stage: StageEnum): StageInfo {
  return STAGE_INFO_MAP[stage];
}

/**
 * 获取所有阶段信息
 * 
 * @returns 所有阶段的完整信息列表
 */
export function getAllStageInfo(): StageInfo[] {
  return [
    STAGE_INFO_MAP[StageEnum.IDEA],
    STAGE_INFO_MAP[StageEnum.MVP],
    STAGE_INFO_MAP[StageEnum.ENTITY],
    STAGE_INFO_MAP[StageEnum.VALIDATION],
    STAGE_INFO_MAP[StageEnum.SCALE],
  ];
}

/**
 * 获取维度权重配置
 * 
 * @returns 各维度的权重值
 */
export function getDimensionWeights(): Record<keyof BusinessDimensions, number> {
  return { ...DIMENSION_WEIGHTS };
}

/**
 * 获取维度中文名称
 * 
 * @returns 各维度的中文名称
 */
export function getDimensionLabels(): Record<keyof BusinessDimensions, string> {
  return { ...DIMENSION_LABELS };
}