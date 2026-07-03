/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * Skill5：规模化增长（规模化期）
 * 
 * 核心能力：
 * - 业务拆解：可AI自动化环节/可外包环节
 * - 产品线升级：定制→标准化→被动收入
 * - 渠道规模化：私域复利/平台矩阵/合作渠道
 * - 经营风险预警：营收结构/财税/交付压力
 * - 长期布局：个人品牌/资产沉淀/可复用商业资产
 */

import {
  StageEnum,
  type SkillMeta,
  type Skill5Input,
  type SkillResult,
  type PrerequisiteCheckResult,
} from '../../src/core/types';
import { skill5OutputSchema } from '../../src/core/output-schema';

/** Skill5元数据 */
export const skill5Meta: SkillMeta = {
  id: 'skill5-scale-growth',
  name: '规模化增长',
  description: '为一人创业者规划规模化增长方案，包括业务拆解自动化、产品线升级、渠道规模化、风险预警和长期布局',
  applicableStage: StageEnum.SCALE,
  version: '1.0.0',
  inputs: [
    { name: 'projectInfo', type: 'object', required: true, description: '项目基本信息' },
    { name: 'currentMonthlyRevenue', type: 'number', required: true, description: '当前月营收' },
    { name: 'currentUserCount', type: 'number', required: true, description: '当前用户数' },
    { name: 'revenueSources', type: 'array', required: true, description: '主要营收来源' },
    { name: 'bottlenecks', type: 'array', required: true, description: '当前痛点/瓶颈' },
  ],
  outputSchema: skill5OutputSchema,
  prerequisites: [
    '已有稳定付费用户（验证期通过）',
    '月营收>0且相对稳定',
    '交付流程可复用',
    '有明确的增长瓶颈',
  ],
};

/**
 * 前置条件检查
 */
export function checkPrerequisites(input: Skill5Input): PrerequisiteCheckResult {
  const failedConditions: string[] = [];
  const suggestions: string[] = [];

  if (!input.projectInfo.projectName) {
    failedConditions.push('项目名称不能为空');
    suggestions.push('请提供项目名称');
  }

  if (input.currentMonthlyRevenue <= 0) {
    failedConditions.push('当前月营收必须大于0');
    suggestions.push('请确认已有稳定营收后再进入规模化阶段');
  }

  if (input.currentUserCount <= 0) {
    failedConditions.push('当前用户数必须大于0');
    suggestions.push('请确认已有付费用户后再进入规模化阶段');
  }

  if (!input.revenueSources || input.revenueSources.length === 0) {
    failedConditions.push('未提供营收来源');
    suggestions.push('请列出当前的主要营收来源');
  }

  if (!input.bottlenecks || input.bottlenecks.length === 0) {
    failedConditions.push('未提供增长瓶颈');
    suggestions.push('请描述当前面临的主要增长瓶颈');
  }

  return {
    passed: failedConditions.length === 0,
    failedConditions,
    suggestedStage: StageEnum.SCALE,
    suggestions,
  };
}

/**
 * 构建Skill5的Prompt
 */
export function buildPrompt(input: Skill5Input): string {
  return `# OPC智脑 - Skill5：规模化增长

## 智能体人设
你是一位专注服务于"一人创业者"（OPC）的规模化增长顾问。你深谙"一人公司也能规模化"的秘诀——通过AI自动化、产品标准化和渠道复利，实现不增加人力的增长。

## 阶段上下文
当前创业者处于【规模化期】（五阶段模型第5阶段），核心目标是构建可复制的增长引擎，实现从1到N的规模化增长，同时保持一人运营的轻盈。

## 任务指令
请为以下一人创业项目规划规模化增长方案。

### 项目信息
- **项目名称**：${input.projectInfo.projectName}
- **项目描述**：${input.projectInfo.description}
- **所属行业**：${input.projectInfo.industry}
- **目标用户**：${input.projectInfo.targetUsers}

### 当前经营数据
- **当前月营收**：${input.currentMonthlyRevenue}元
- **当前用户数**：${input.currentUserCount}人
- **主要营收来源**：${input.revenueSources.join('、')}
- **当前瓶颈**：${input.bottlenecks.join('、')}

### 创业者资源
- **创始人背景**：${input.projectInfo.founderBackground}

## 分析框架

### 1. 业务拆解
将当前业务按可自动化程度拆解为三类：

- **可AI自动化环节**：
  - 列出可以用AI工具替代的工作环节
  - 推荐具体的AI工具/方案
  - 预计节省的时间/成本

- **可外包环节**：
  - 列出可以外包给第三方的工作环节
  - 外包成本估算
  - 外包风险与管控方案

- **必须亲自做的环节**：
  - 列出核心不可替代的工作环节
  - 如何提升这些环节的效率

- **自动化实施建议**：
  - 优先自动化的环节排序
  - 实施时间线

### 2. 产品线升级路径
设计从"定制服务"到"标准化产品"再到"被动收入"的升级路径：

- **当前阶段**：定制/标准化/被动收入
- **目标阶段**：下一阶段
- **升级步骤**（具体可执行）
- **时间线**

升级方向参考：
- 定制→标准化：将重复性服务产品化
- 标准化→被动收入：将标准化产品自动化交付
- 被动收入→复利：构建可复用的内容/工具/数据资产

### 3. 渠道规模化方案
从三个维度规划渠道规模化：

- **私域复利**：
  - 微信生态（朋友圈/社群/公众号/视频号）的复利策略
  - 用户生命周期价值（LTV）提升方案
  - 转介绍/裂变机制

- **平台矩阵**：
  - 多平台分发策略
  - 各平台差异化内容策略
  - 平台间导流闭环

- **合作渠道**：
  - 潜在合作伙伴类型
  - 合作模式设计
  - 利益分配方案

### 4. 经营风险预警
识别规模化过程中的关键风险：

- **营收结构风险**：收入是否过于依赖单一来源
- **财税风险**：营收增长带来的财税合规要求变化
- **交付压力风险**：订单增长是否超出交付能力
- **质量风险**：规模化是否导致交付质量下降
- **现金流风险**：增长期的现金流管理

每个风险包含：
- 风险名称与类别
- 严重程度（1-5）
- 发生概率（1-5）
- 预警信号（什么现象出现说明风险在发生）
- 应对策略

### 5. 长期布局
为一人创业者的长期发展做布局：

- **个人品牌建设**：
  - 品牌定位
  - 内容策略
  - 影响力建设路径

- **资产沉淀**：
  - 可沉淀的数字资产（内容/工具/数据/方法论）
  - 资产沉淀策略

- **可复用商业资产**：
  - 可跨项目复用的能力/资源/资产
  - 复用策略

## 输出格式要求
请严格按照以下JSON Schema输出结构化结果：
\`\`\`json
${JSON.stringify(skill5OutputSchema, null, 2)}
\`\`\`

## 约束规则
1. 所有增长方案必须基于"一人运营"的约束，不假设增加人力
2. AI自动化推荐必须给出具体工具名称，不写"可用AI工具"这种模糊描述
3. 产品线升级必须循序渐进，不能跳级
4. 风险预警必须诚实，不回避规模化带来的真实风险
5. 长期布局必须可执行，不是空想
6. 所有方案必须考虑现金流，增长不能以亏损为代价
7. 渠道规模化优先推荐零成本/低成本方案`;
}

/**
 * 执行Skill5
 */
export function executeSkill5(input: Skill5Input): SkillResult {
  const prereqCheck = checkPrerequisites(input);
  if (!prereqCheck.passed) {
    return {
      skillId: skill5Meta.id,
      success: false,
      data: {},
      prompt: '',
      error: `前置条件未满足：${prereqCheck.failedConditions.join('；')}`,
    };
  }

  const prompt = buildPrompt(input);

  return {
    skillId: skill5Meta.id,
    success: true,
    data: {
      projectName: input.projectInfo.projectName,
      stage: StageEnum.SCALE,
      stageLabel: '规模化期',
    },
    prompt,
  };
}