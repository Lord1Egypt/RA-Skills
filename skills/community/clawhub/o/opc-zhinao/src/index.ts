/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-10
 * 
 * OPC智脑五阶段创业诊断 - 统一导出入口
 * 
 * 本文件是opc-skills包的主入口，导出所有核心API、类型和Skill。
 * 
 * 使用方式：
 * ```typescript
 * import { classifyStage, executeSkill1, StageEnum } from 'opc-skills';
 * ```
 */

// ============================================================
// 核心类型导出
// ============================================================

export {
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
  type SkillMeta,
  type SkillInput,
  type SkillResult,
  type PrerequisiteCheckResult,
  type ProjectInfo,
  type Skill1Input,
  type Skill2Input,
  type Skill3Input,
  type Skill4Input,
  type Skill5Input,
  type FeasibilityLevel,
  type DemandType,
  type DemandValidationResult,
  type PersonalMatchResult,
  type CompetitorAnalysisResult,
  type MVPFeature,
  type ComplianceItem,
  type AcquisitionChannel,
  type RiskItem,
} from './core/types';

// ============================================================
// 核心API导出
// ============================================================

export {
  classifyStage,
  detectContradiction,
  getStageInfo,
  getAllStageInfo,
  getDimensionWeights,
  getDimensionLabels,
} from './core/stage-classifier';

// ============================================================
// 输出Schema导出
// ============================================================

export {
  skill1OutputSchema,
  skill2OutputSchema,
  skill3OutputSchema,
  skill4OutputSchema,
  skill5OutputSchema,
  ALL_OUTPUT_SCHEMAS,
  getOutputSchema,
  getSemanticRules,
  runSemanticValidation,
  type SemanticRule,
} from './core/output-schema';

export {
  validateAIOutput,
  getUnderstandingTraps,
  checkUnderstanding,
  type ValidationIssue,
  type ValidationResult,
  type UnderstandingCheck,
} from './core/ai-output-validator';

// ============================================================
// Skill1：Idea可行性研判
// ============================================================

export {
  skill1Meta,
  checkPrerequisites as checkSkill1Prerequisites,
  buildPrompt as buildSkill1Prompt,
  executeSkill1,
} from '../skills/skill1-idea-feasibility';

// ============================================================
// Skill2：MVP精益设计
// ============================================================

export {
  skill2Meta,
  checkPrerequisites as checkSkill2Prerequisites,
  buildPrompt as buildSkill2Prompt,
  executeSkill2,
} from '../skills/skill2-mvp-design';

// ============================================================
// Skill3：OPC合规落地
// ============================================================

export {
  skill3Meta,
  checkPrerequisites as checkSkill3Prerequisites,
  buildPrompt as buildSkill3Prompt,
  executeSkill3,
} from '../skills/skill3-opc-compliance';

// ============================================================
// Skill4：种子用户冷启动
// ============================================================

export {
  skill4Meta,
  checkPrerequisites as checkSkill4Prerequisites,
  buildPrompt as buildSkill4Prompt,
  executeSkill4,
} from '../skills/skill4-seed-coldstart';

// ============================================================
// Skill5：规模化增长
// ============================================================

export {
  skill5Meta,
  checkPrerequisites as checkSkill5Prerequisites,
  buildPrompt as buildSkill5Prompt,
  executeSkill5,
} from '../skills/skill5-scale-growth';

// ============================================================
// 便捷API：根据阶段自动执行对应Skill
// ============================================================

import { type BusinessDimensions } from './core/types';
import { classifyStage } from './core/stage-classifier';
import { skill1Meta } from '../skills/skill1-idea-feasibility';
import { skill2Meta } from '../skills/skill2-mvp-design';
import { skill3Meta } from '../skills/skill3-opc-compliance';
import { skill4Meta } from '../skills/skill4-seed-coldstart';
import { skill5Meta } from '../skills/skill5-scale-growth';

/**
 * 获取所有Skill的元数据列表
 */
export function getAllSkillMetas() {
  return [skill1Meta, skill2Meta, skill3Meta, skill4Meta, skill5Meta];
}

/**
 * 根据五维度评分自动判定阶段并获取推荐的Skill ID
 * 
 * @param dimensions 五维度业务评分
 * @returns 推荐的Skill ID
 */
export function getRecommendedSkillId(dimensions: BusinessDimensions): string {
  const result = classifyStage(dimensions);
  return result.recommendedSkill;
}
