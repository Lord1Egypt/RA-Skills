/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-13
 * 
 * OPC智脑 - AI输出校验引擎
 * 
 * 三层校验 + 理解纠偏机制，解决"AI输出无校验"和"AI理解偏差无法纠正"问题。
 * 
 * L1 格式校验：JSON Schema结构验证（复用output-schema.ts）
 * L2 逻辑校验：交叉检查结论是否自洽
 * L3 事实校验：关键数字的合理性检查
 * L4 理解校验：用户意图→AI理解的偏差检测
 */

import { getOutputSchema } from './output-schema';
import {
  type StageEnum,
  StageEnum as StageEnumVal,
} from './types';

// ============================================================
// 校验结果类型
// ============================================================

export interface ValidationIssue {
  layer: 'L1' | 'L2' | 'L3' | 'L4';
  severity: 'error' | 'warning' | 'info';
  code: string;
  message: string;
  detail?: string;
  suggestion?: string;
}

export interface ValidationResult {
  isValid: boolean;
  issues: ValidationIssue[];
  score: number;
  summary: string;
}

export interface UnderstandingCheck {
  userIntent: string;
  aiUnderstanding: string;
  deviation: 'none' | 'minor' | 'major' | 'critical';
  clarification?: string;
}

// ============================================================
// L1：格式校验（基于JSON Schema）
// ============================================================

function validateL1Format(skillId: string, output: Record<string, unknown>): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  const schema = getOutputSchema(skillId);

  if (!schema) {
    issues.push({
      layer: 'L1',
      severity: 'warning',
      code: 'L1_NO_SCHEMA',
      message: `未找到Skill ${skillId}的输出Schema，跳过格式校验`,
    });
    return issues;
  }

  const required = (schema as any).required as string[] | undefined;
  if (required) {
    for (const field of required) {
      if (output[field] === undefined || output[field] === null) {
        issues.push({
          layer: 'L1',
          severity: 'error',
          code: 'L1_MISSING_REQUIRED',
          message: `缺少必填字段：${field}`,
          suggestion: `请确保输出包含 ${field} 字段`,
        });
      }
    }
  }

  const properties = (schema as any).properties as Record<string, any> | undefined;
  if (properties) {
    for (const [key, propSchema] of Object.entries(properties)) {
      if (output[key] !== undefined && propSchema.type) {
        const actualType = Array.isArray(output[key]) ? 'array' : typeof output[key];
        const expectedType = propSchema.type as string;
        if (actualType !== expectedType) {
          issues.push({
            layer: 'L1',
            severity: 'error',
            code: 'L1_TYPE_MISMATCH',
            message: `字段 ${key} 类型错误：期望 ${expectedType}，实际 ${actualType}`,
          });
        }
      }
      if (output[key] !== undefined && propSchema.enum) {
        if (!(propSchema.enum as any[]).includes(output[key])) {
          issues.push({
            layer: 'L1',
            severity: 'error',
            code: 'L1_ENUM_VIOLATION',
            message: `字段 ${key} 值 "${output[key]}" 不在允许范围 [${(propSchema.enum as any[]).join(', ')}]`,
          });
        }
      }
      if (typeof output[key] === 'number') {
        if (propSchema.minimum !== undefined && (output[key] as number) < propSchema.minimum) {
          issues.push({
            layer: 'L1',
            severity: 'error',
            code: 'L1_BELOW_MIN',
            message: `字段 ${key} 值 ${output[key]} 低于最小值 ${propSchema.minimum}`,
          });
        }
        if (propSchema.maximum !== undefined && (output[key] as number) > propSchema.maximum) {
          issues.push({
            layer: 'L1',
            severity: 'error',
            code: 'L1_ABOVE_MAX',
            message: `字段 ${key} 值 ${output[key]} 超过最大值 ${propSchema.maximum}`,
          });
        }
      }
    }
  }

  return issues;
}

// ============================================================
// L2：逻辑校验（交叉检查结论自洽性）
// ============================================================

const LOGIC_RULES: Record<string, ((output: Record<string, unknown>) => ValidationIssue[])[]> = {
  'skill1-idea-feasibility': [
    (output) => {
      const issues: ValidationIssue[] = [];
      const dv = output.demandValidation as Record<string, unknown> | undefined;
      const fl = output.feasibilityLevel as string | undefined;
      if (dv && fl) {
        const demandType = dv.demandType as string;
        if (demandType === 'fake' && (fl === 'highly_feasible' || fl === 'feasible')) {
          issues.push({
            layer: 'L2',
            severity: 'error',
            code: 'L2_CONTRADICT_DEMAND_FEASIBILITY',
            message: '逻辑矛盾：需求判定为"伪需求"，但可行性等级为"可行"或"高度可行"',
            detail: '伪需求不应给出可行结论，应判定为"有挑战"或"不可行"',
            suggestion: '请检查需求判定和可行性等级是否一致',
          });
        }
        if (demandType === 'rigid' && fl === 'not_feasible') {
          issues.push({
            layer: 'L2',
            severity: 'warning',
            code: 'L2_RIGID_BUT_NOT_FEASIBLE',
            message: '逻辑存疑：需求判定为"刚需"，但可行性等级为"不可行"',
            detail: '刚需但不可行，通常是个人匹配度极低或竞争极度红海，需在报告中明确说明原因',
            suggestion: '请在报告中补充不可行的具体原因',
          });
        }
      }
      return issues;
    },
    (output) => {
      const issues: ValidationIssue[] = [];
      const pm = output.personalMatch as Record<string, unknown> | undefined;
      if (pm) {
        const overall = pm.overallMatch as number | undefined;
        const skill = pm.skillMatch as number | undefined;
        const time = pm.timeMatch as number | undefined;
        const budget = pm.budgetMatch as number | undefined;
        if (overall !== undefined && skill !== undefined && time !== undefined && budget !== undefined) {
          const expectedOverall = Math.round(skill * 0.4 + time * 0.3 + budget * 0.3);
          if (Math.abs(overall - expectedOverall) > 5) {
            issues.push({
              layer: 'L2',
              severity: 'warning',
              code: 'L2_MATCH_SCORE_MISMATCH',
              message: `综合匹配度${overall}与子维度计算值${expectedOverall}偏差>5分`,
              suggestion: '请核实综合匹配度计算是否正确',
            });
          }
        }
      }
      return issues;
    },
  ],
  'skill2-mvp-design': [
    (output) => {
      const issues: ValidationIssue[] = [];
      const mvp = output.mvpScope as Record<string, unknown> | undefined;
      if (mvp) {
        const coreFeatures = mvp.coreFeatures as any[] | undefined;
        if (coreFeatures && coreFeatures.length > 3) {
          issues.push({
            layer: 'L2',
            severity: 'error',
            code: 'L2_MVP_CORE_EXCEED',
            message: `MVP核心功能${coreFeatures.length}个，超过上限3个`,
            suggestion: '一人创业者MVP铁律：核心功能不超过3个，请裁剪',
          });
        }
        const totalHours = coreFeatures?.reduce((sum: number, f: any) => sum + (f.estimatedHours || 0), 0) || 0;
        if (totalHours > 80) {
          issues.push({
            layer: 'L2',
            severity: 'warning',
            code: 'L2_MVP_TIME_EXCEED',
            message: `MVP总开发时间${totalHours}小时，超过2周上限(80小时)`,
            suggestion: '建议裁剪功能或延长交付时间，并明确告知用户风险',
          });
        }
      }
      return issues;
    },
  ],
  'skill3-opc-compliance': [
    (output) => {
      const issues: ValidationIssue[] = [];
      const entity = output.entityRecommendation as Record<string, unknown> | undefined;
      if (entity) {
        const type = entity.recommendedType as string | undefined;
        const reasoning = entity.reasoning as string | undefined;
        if (type && !reasoning) {
          issues.push({
            layer: 'L2',
            severity: 'warning',
            code: 'L2_NO_ENTITY_REASONING',
            message: '主体选型缺少选型理由',
            suggestion: '必须给出为什么推荐该主体类型的具体理由',
          });
        }
      }
      return issues;
    },
  ],
  'skill4-seed-coldstart': [
    (output) => {
      const issues: ValidationIssue[] = [];
      const strategy = output.seedUserStrategy as Record<string, unknown> | undefined;
      if (strategy) {
        const target = strategy.targetSeedCount as number | undefined;
        if (target !== undefined && target < 10) {
          issues.push({
            layer: 'L2',
            severity: 'warning',
            code: 'L2_SEED_COUNT_LOW',
            message: `目标种子用户数${target}人，低于毕业条件(≥10人)`,
            suggestion: '毕业条件要求种子用户≥10人，建议调整目标',
          });
        }
      }
      return issues;
    },
  ],
  'skill5-scale-growth': [],
};

function validateL2Logic(skillId: string, output: Record<string, unknown>): ValidationIssue[] {
  const rules = LOGIC_RULES[skillId] || [];
  const issues: ValidationIssue[] = [];
  for (const rule of rules) {
    issues.push(...rule(output));
  }
  return issues;
}

// ============================================================
// L3：事实校验（关键数字合理性）
// ============================================================

const FACT_RULES: ((skillId: string, output: Record<string, unknown>) => ValidationIssue[])[] = [
  (skillId, output) => {
    const issues: ValidationIssue[] = [];
    if (skillId === 'skill3-opc-compliance') {
      const checklist = output.preparationChecklist as any[] | undefined;
      if (checklist) {
        for (const item of checklist) {
          if (item.estimatedDays !== undefined && item.estimatedDays > 90) {
            issues.push({
              layer: 'L3',
              severity: 'warning',
              code: 'L3_PREP_TIME_LONG',
              message: `筹备事项"${item.item}"预估${item.estimatedDays}天，超过90天`,
              suggestion: '一人创业者筹备周期应尽量短，超过90天的事项建议标注为可延后',
            });
          }
        }
      }
    }
    return issues;
  },
  (skillId, output) => {
    const issues: ValidationIssue[] = [];
    if (skillId === 'skill4-seed-coldstart') {
      const channels = output.acquisitionChannels as any[] | undefined;
      if (channels) {
        for (const ch of channels) {
          if (ch.difficulty !== undefined && (ch.difficulty < 1 || ch.difficulty > 5)) {
            issues.push({
              layer: 'L3',
              severity: 'error',
              code: 'L3_DIFFICULTY_OUT_OF_RANGE',
              message: `渠道"${ch.name}"难度${ch.difficulty}不在1-5范围内`,
            });
          }
        }
      }
    }
    return issues;
  },
  (skillId, output) => {
    const issues: ValidationIssue[] = [];
    if (skillId === 'skill5-scale-growth') {
      const risks = output.riskWarning as any[] | undefined;
      if (risks) {
        for (const r of risks) {
          if (r.severity !== undefined && (r.severity < 1 || r.severity > 5)) {
            issues.push({
              layer: 'L3',
              severity: 'error',
              code: 'L3_SEVERITY_OUT_OF_RANGE',
              message: `风险"${r.name}"严重程度${r.severity}不在1-5范围内`,
            });
          }
        }
      }
    }
    return issues;
  },
];

function validateL3Fact(skillId: string, output: Record<string, unknown>): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  for (const rule of FACT_RULES) {
    issues.push(...rule(skillId, output));
  }
  return issues;
}

// ============================================================
// L4：理解校验（用户意图→AI理解的偏差检测）
// ============================================================

const UNDERSTANDING_TRAPS: Record<string, { scenario: string; trap: string; correction: string }[]> = {
  'skill1-idea-feasibility': [
    { scenario: '用户说"我想做XX"', trap: 'AI直接判定为具体Idea开始可行性分析', correction: '应先确认：用户是已有明确Idea，还是只有一个模糊方向？模糊方向应先做赛道扫描' },
    { scenario: '用户说"帮我看看这个方向行不行"', trap: 'AI直接给出"可行/不可行"的结论', correction: '应先拆解需求要素（目标用户、痛点场景、现有方案），再逐步判定' },
    { scenario: '用户描述了一个技术方案而非用户需求', trap: 'AI把技术方案当作需求来分析', correction: '应追问"这个方案解决什么用户痛点？"，区分需求和技术实现' },
  ],
  'skill2-mvp-design': [
    { scenario: '用户列出很多功能想全部保留', trap: 'AI默认保留大部分功能只裁剪少量', correction: '必须严格执行四问裁剪法，核心功能≤3个，2周开发上限' },
    { scenario: '用户说"我先把所有功能做完再上线"', trap: 'AI不指出这种做法的风险', correction: '必须强调精益原则：先验证1个核心功能，再逐步增加' },
  ],
  'skill3-opc-compliance': [
    { scenario: '用户问"我应该注册多少钱的注册资本"', trap: 'AI建议写一个很高的注册资本(如500万)', correction: '新公司法5年实缴，注册资本应按实际需要(建议10-50万)，不能虚高' },
    { scenario: '用户对财税完全不懂', trap: 'AI给出复杂的专业财税术语和方案', correction: '应使用大白话解释，强烈推荐代账公司，给出"绝对不能做的3件事"' },
  ],
  'skill4-seed-coldstart': [
    { scenario: '用户说"我要先做100个用户再说"', trap: 'AI给出大规模获客方案', correction: '验证期种子用户宁精勿多，目标10-30人，1个付费用户>10个免费用户' },
    { scenario: '用户说"我的产品定价9.9元"', trap: 'AI不质疑定价合理性', correction: '必须执行定价三要素校验(成本/竞品/价值)，9.9元是否覆盖成本×1.5？' },
  ],
  'skill5-scale-growth': [
    { scenario: '用户说"我每天工作16小时"', trap: 'AI继续给出更多增长方案', correction: '必须先预警精力耗尽风险，推荐时间审计和自动化方案，每周工作≤60小时' },
    { scenario: '用户想通过大量广告投放获客', trap: 'AI给出广告投放方案', correction: '一人创业者不推荐广告投放>5000元/月，应优先内容获客和私域复利' },
  ],
};

function validateL4Understanding(
  skillId: string,
  userIntent: string,
  aiUnderstanding: string
): { issues: ValidationIssue[]; check: UnderstandingCheck } {
  const issues: ValidationIssue[] = [];
  const traps = UNDERSTANDING_TRAPS[skillId] || [];

  let deviation: UnderstandingCheck['deviation'] = 'none';
  let clarification: string | undefined;

  for (const trap of traps) {
    const scenarioKeywords = trap.scenario.replace(/[""""]/g, '').split('');
    const userLower = userIntent.toLowerCase();
    const aiLower = aiUnderstanding.toLowerCase();

    const scenarioCore = trap.scenario.replace(/[""""]/g, '').slice(0, 20);
    if (userLower.includes(scenarioCore.slice(0, 6)) || aiLower.includes(trap.trap.slice(0, 10))) {
      deviation = deviation === 'none' ? 'minor' : deviation;
      issues.push({
        layer: 'L4',
        severity: 'warning',
        code: 'L4_UNDERSTANDING_TRAP',
        message: `可能的AI理解偏差：${trap.scenario}`,
        detail: `常见陷阱：${trap.trap}`,
        suggestion: `纠偏策略：${trap.correction}`,
      });
      clarification = trap.correction;
    }
  }

  if (issues.length >= 2) {
    deviation = 'major';
  }
  if (issues.length >= 3) {
    deviation = 'critical';
  }

  const check: UnderstandingCheck = {
    userIntent,
    aiUnderstanding,
    deviation,
    clarification,
  };

  return { issues, check };
}

// ============================================================
// 核心API：全量校验
// ============================================================

export function validateAIOutput(
  skillId: string,
  output: Record<string, unknown>,
  userIntent?: string,
  aiUnderstanding?: string
): ValidationResult {
  const issues: ValidationIssue[] = [];

  issues.push(...validateL1Format(skillId, output));
  issues.push(...validateL2Logic(skillId, output));
  issues.push(...validateL3Fact(skillId, output));

  if (userIntent && aiUnderstanding) {
    const { issues: l4Issues } = validateL4Understanding(skillId, userIntent, aiUnderstanding);
    issues.push(...l4Issues);
  }

  const errorCount = issues.filter((i) => i.severity === 'error').length;
  const warningCount = issues.filter((i) => i.severity === 'warning').length;
  const isValid = errorCount === 0;
  const score = Math.max(0, 100 - errorCount * 25 - warningCount * 8);

  const summary = isValid
    ? `校验通过（${warningCount}个警告，${issues.filter((i) => i.severity === 'info').length}个提示）`
    : `校验未通过（${errorCount}个错误，${warningCount}个警告）`;

  return { isValid, issues, score, summary };
}

export function getUnderstandingTraps(skillId: string): { scenario: string; trap: string; correction: string }[] {
  return UNDERSTANDING_TRAPS[skillId] || [];
}

export function checkUnderstanding(
  skillId: string,
  userIntent: string,
  aiUnderstanding: string
): UnderstandingCheck {
  const { check } = validateL4Understanding(skillId, userIntent, aiUnderstanding);
  return check;
}