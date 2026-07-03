/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * Skill4：种子用户冷启动（验证期）
 * 
 * 核心能力：
 * - 低成本获客渠道方案（单人可落地）
 * - 种子用户招募策略：试用规则/小单体系/破冰方案
 * - 用户反馈拆解：产品问题/服务短板/优化优先级
 * - 定价诊断与调价方案
 * - 最小商业闭环验证
 */

import {
  StageEnum,
  type SkillMeta,
  type Skill4Input,
  type SkillResult,
  type PrerequisiteCheckResult,
} from '../../src/core/types';
import { skill4OutputSchema } from '../../src/core/output-schema';

/** Skill4元数据 */
export const skill4Meta: SkillMeta = {
  id: 'skill4-seed-coldstart',
  name: '种子用户冷启动',
  description: '为一人创业者规划种子用户冷启动方案，包括低成本获客渠道、招募策略、反馈拆解、定价诊断和最小商业闭环验证',
  applicableStage: StageEnum.VALIDATION,
  version: '1.0.0',
  inputs: [
    { name: 'projectInfo', type: 'object', required: true, description: '项目基本信息' },
    { name: 'productDescription', type: 'string', required: true, description: '产品/MVP描述' },
    { name: 'currentPricing', type: 'string', required: true, description: '当前定价' },
    { name: 'existingUsers', type: 'number', required: false, description: '已有用户数', defaultValue: 0 },
    { name: 'channelPreference', type: 'array', required: false, description: '获客渠道偏好' },
  ],
  outputSchema: skill4OutputSchema,
  prerequisites: [
    'MVP已可交付',
    '合规主体已就绪（或至少在办理中）',
    '产品定价已有初步方案',
  ],
};

/**
 * 前置条件检查
 */
export function checkPrerequisites(input: Skill4Input): PrerequisiteCheckResult {
  const failedConditions: string[] = [];
  const suggestions: string[] = [];

  if (!input.projectInfo.projectName) {
    failedConditions.push('项目名称不能为空');
    suggestions.push('请提供项目名称');
  }

  if (!input.productDescription || input.productDescription.length < 10) {
    failedConditions.push('产品描述不充分');
    suggestions.push('请详细描述你的MVP/产品，包括核心功能和交付形态');
  }

  if (!input.currentPricing) {
    failedConditions.push('未提供当前定价');
    suggestions.push('请提供产品的当前定价方案');
  }

  return {
    passed: failedConditions.length === 0,
    failedConditions,
    suggestedStage: StageEnum.VALIDATION,
    suggestions,
  };
}

/**
 * 构建Skill4的Prompt
 */
export function buildPrompt(input: Skill4Input): string {
  return `# OPC智脑 - Skill4：种子用户冷启动

## 智能体人设
你是一位专注服务于"一人创业者"（OPC）的增长黑客。你擅长用极低成本获取种子用户，深谙"先有10个愿意付费的用户，胜过1000个免费用户"的真理。

## 阶段上下文
当前创业者处于【验证期】（五阶段模型第4阶段），核心目标是获取种子用户、验证付费意愿、跑通最小商业闭环。这是最关键的阶段——证明有人愿意为你的产品付费。

## 任务指令
请为以下一人创业项目规划种子用户冷启动方案。

### 项目信息
- **项目名称**：${input.projectInfo.projectName}
- **项目描述**：${input.projectInfo.description}
- **所属行业**：${input.projectInfo.industry}
- **目标用户**：${input.projectInfo.targetUsers}

### 产品/MVP描述
${input.productDescription}

### 当前定价
${input.currentPricing}

${input.existingUsers ? `### 已有用户数\n${input.existingUsers}人` : '### 已有用户数\n0人（从零冷启动）'}

${input.channelPreference?.length ? `### 获客渠道偏好\n${input.channelPreference.join('、')}` : ''}

### 创业者资源
- **创始人背景**：${input.projectInfo.founderBackground}
- **可用预算**：${input.projectInfo.budget ?? '未提供'}元

## 分析框架

### 1. 低成本获客渠道方案
请推荐至少5个单人可落地的低成本获客渠道，每个包含：
- 渠道名称与类型
- 预计成本（必须量化）
- 预计效果（用户数/转化率）
- 操作难度（1-5分）
- 具体操作步骤（分步骤，可直接执行）

渠道类型参考：
- 内容获客：公众号/小红书/知乎/视频号
- 社区获客：行业社群/豆瓣/即刻
- 搜索获客：SEO/长尾词
- 推荐获客：转介绍/裂变
- 平台获客：闲鱼/淘宝/猪八戒
- 线下获客：行业活动/地推

### 2. 种子用户招募策略
- **试用规则**：如何设计试用机制（免费试用/低价体验/部分功能开放）
- **小单体系**：如何设计低门槛的首单产品（价格/内容/交付方式）
- **破冰方案**：如何让用户从"知道你"到"愿意试一下"
- **目标种子用户数**：建议招募多少种子用户

### 3. 用户反馈拆解框架
设计反馈收集与分析框架：
- **产品问题**：可能的产品层面问题（功能/体验/稳定性）
- **服务短板**：可能的服务层面问题（响应/交付/售后）
- **优化优先级**：基于影响程度排序的优化方向

### 4. 定价诊断与调价方案
- **当前定价问题诊断**：当前定价是否合理
- **建议定价**：基于成本、竞品、用户价值的定价建议
- **定价逻辑**：定价背后的逻辑说明
- **调价方案**：如何从当前定价过渡到建议定价

### 5. 最小商业闭环验证
设计最小商业闭环：
- **闭环步骤**：从获客到付费到交付到复购的完整步骤
- **验证指标**：每个步骤的核心验证指标
- **通过标准**：什么算跑通了商业闭环

关键标准：
- 至少10个种子用户
- 至少1个付费用户
- 付费用户有正面反馈
- 交付流程可复用

## 输出格式要求
请严格按照以下JSON Schema输出结构化结果：
\`\`\`json
${JSON.stringify(skill4OutputSchema, null, 2)}
\`\`\`

## 约束规则
1. 所有获客渠道必须是一人可落地的，不假设有团队
2. 获客成本必须量化，不写"低成本"这种模糊描述
3. 种子用户数宁精勿多，10个高质量用户胜过100个低质量用户
4. 定价建议必须基于数据（成本/竞品/价值），不是拍脑袋
5. 商业闭环必须可验证，有明确的通过/不通过标准
6. 所有方案必须可立即执行，不需要额外资源`;
}

/**
 * 执行Skill4
 */
export function executeSkill4(input: Skill4Input): SkillResult {
  const prereqCheck = checkPrerequisites(input);
  if (!prereqCheck.passed) {
    return {
      skillId: skill4Meta.id,
      success: false,
      data: {},
      prompt: '',
      error: `前置条件未满足：${prereqCheck.failedConditions.join('；')}`,
    };
  }

  const prompt = buildPrompt(input);

  return {
    skillId: skill4Meta.id,
    success: true,
    data: {
      projectName: input.projectInfo.projectName,
      stage: StageEnum.VALIDATION,
      stageLabel: '验证期',
    },
    prompt,
  };
}