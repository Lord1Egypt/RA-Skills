/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * Skill2：MVP精益设计（原型期）
 * 
 * 核心能力：
 * - MVP极简裁剪：砍非核心，保留可变现最小功能
 * - 三层产品体系：引流款/利润款/被动产品
 * - 单人交付成本测算：时间/工具/试错成本
 * - 首单冷交付方案、小样标准、报价逻辑
 */

import {
  StageEnum,
  type SkillMeta,
  type Skill2Input,
  type SkillResult,
  type PrerequisiteCheckResult,
} from '../../src/core/types';
import { skill2OutputSchema } from '../../src/core/output-schema';

/** Skill2元数据 */
export const skill2Meta: SkillMeta = {
  id: 'skill2-mvp-design',
  name: 'MVP精益设计',
  description: '基于已验证的需求，设计最小可行产品（MVP），构建三层产品体系，测算交付成本，规划首单冷交付方案',
  applicableStage: StageEnum.MVP,
  version: '1.0.0',
  inputs: [
    { name: 'projectInfo', type: 'object', required: true, description: '项目基本信息' },
    { name: 'validatedDemand', type: 'string', required: true, description: '已验证的需求（来自Skill1输出）' },
    { name: 'coreFeatures', type: 'array', required: true, description: '核心功能列表' },
    { name: 'expectedPricing', type: 'string', required: false, description: '预期定价' },
    { name: 'deliveryMethod', type: 'string', required: false, description: '交付方式' },
  ],
  outputSchema: skill2OutputSchema,
  prerequisites: [
    '需求已通过可行性验证（Skill1输出feasibility≥feasible）',
    '核心功能列表已明确',
    '有明确的交付方式设想',
  ],
};

/**
 * 前置条件检查
 */
export function checkPrerequisites(input: Skill2Input): PrerequisiteCheckResult {
  const failedConditions: string[] = [];
  const suggestions: string[] = [];

  if (!input.projectInfo.projectName) {
    failedConditions.push('项目名称不能为空');
    suggestions.push('请提供项目名称');
  }

  if (!input.validatedDemand || input.validatedDemand.length < 10) {
    failedConditions.push('已验证需求描述不充分');
    suggestions.push('请先完成Skill1可行性研判，并提供已验证的需求描述');
  }

  if (!input.coreFeatures || input.coreFeatures.length === 0) {
    failedConditions.push('核心功能列表为空');
    suggestions.push('请列出你设想的核心功能，至少1个');
  }

  return {
    passed: failedConditions.length === 0,
    failedConditions,
    suggestedStage: StageEnum.MVP,
    suggestions,
  };
}

/**
 * 构建Skill2的Prompt
 */
export function buildPrompt(input: Skill2Input): string {
  return `# OPC智脑 - Skill2：MVP精益设计

## 智能体人设
你是一位专注服务于"一人创业者"（OPC）的精益产品设计师。你深谙"少即是多"的哲学，擅长用最小成本验证产品假设，帮助创业者避免过度设计。

## 阶段上下文
当前创业者处于【原型期】（五阶段模型第2阶段），核心目标是设计MVP、确定三层产品体系、测算交付成本、完成首单冷交付。

## 任务指令
请基于以下已验证的需求，设计精益MVP方案。

### 项目信息
- **项目名称**：${input.projectInfo.projectName}
- **项目描述**：${input.projectInfo.description}
- **所属行业**：${input.projectInfo.industry}
- **目标用户**：${input.projectInfo.targetUsers}

### 已验证需求
${input.validatedDemand}

### 设想的核心功能
${input.coreFeatures.map((f, i) => `${i + 1}. ${f}`).join('\n')}

${input.expectedPricing ? `### 预期定价\n${input.expectedPricing}` : ''}
${input.deliveryMethod ? `### 交付方式\n${input.deliveryMethod}` : ''}

### 创业者资源
- **创始人背景**：${input.projectInfo.founderBackground}
- **可用预算**：${input.projectInfo.budget ?? '未提供'}元
- **可投入时间**：${input.projectInfo.availableTime ?? '未提供'}小时/周

## 分析框架

### 1. MVP极简裁剪
请对设想的功能进行裁剪决策：
- **保留功能**（核心功能，可变现的最小集合）：
  - 功能名称与描述
  - 是否为核心功能
  - 预估开发时间（小时）
  - 优先级（1最高）
  
- **裁剪功能**（非核心，MVP阶段砍掉）：
  - 功能名称
  - 裁剪理由
  - 恢复条件（什么情况下可以加回来）

裁剪原则：
1. 只保留能直接产生价值的功能
2. 砍掉所有"有了更好"但非必须的功能
3. 砍掉所有需要外部依赖的功能（除非零成本获取）
4. 单人可在2周内完成开发

### 2. 三层产品体系
为一人创业者设计三层产品结构：

- **引流款**（低价/免费，获取用户信任）：
  - 产品名称与描述
  - 定价策略
  - 引流目的

- **利润款**（核心收入来源）：
  - 产品名称与描述
  - 定价策略
  - 利润率说明

- **被动产品**（可自动化交付，边际成本趋零）：
  - 产品名称与描述
  - 定价策略
  - 自动化程度

### 3. 单人交付成本测算
从三个维度测算交付成本：
- **时间成本**：每次交付需要多少时间
- **工具成本**：需要哪些工具/平台，费用多少
- **试错成本**：前3次交付可能的额外成本
- **总成本估算**
- **成本控制建议**

### 4. 首单冷交付方案
- 冷交付方式（如何在没案例的情况下交付第一单）
- 小样标准（什么算合格的交付成果）
- 报价逻辑（首单如何定价，既不亏本又不过高）
- 交付时间线

## 输出格式要求
请严格按照以下JSON Schema输出结构化结果：
\`\`\`json
${JSON.stringify(skill2OutputSchema, null, 2)}
\`\`\`

## 约束规则
1. MVP功能数不超过3个核心功能
2. 所有成本测算必须基于单人交付，不假设有团队
3. 首单定价可以低于正常价，但不能亏本
4. 三层产品体系必须有一层可自动化交付
5. 交付时间线必须具体到天
6. 所有建议必须可执行、可量化`;
}

/**
 * 执行Skill2
 */
export function executeSkill2(input: Skill2Input): SkillResult {
  const prereqCheck = checkPrerequisites(input);
  if (!prereqCheck.passed) {
    return {
      skillId: skill2Meta.id,
      success: false,
      data: {},
      prompt: '',
      error: `前置条件未满足：${prereqCheck.failedConditions.join('；')}`,
    };
  }

  const prompt = buildPrompt(input);

  return {
    skillId: skill2Meta.id,
    success: true,
    data: {
      projectName: input.projectInfo.projectName,
      stage: StageEnum.MVP,
      stageLabel: '原型期',
    },
    prompt,
  };
}