/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * Skill1：Idea可行性研判（构思期）
 * 
 * 核心能力：
 * - 需求真伪校验：刚需/改善型/伪需求判定框架
 * - 个人匹配度测评：技能/时间/预算三维评估
 * - 竞品格局分析：单人创业者打法/定价/优缺点
 * - 输出《OPC项目可行性分析报告》
 * - 不可行则给出轻量化替代赛道建议
 */

import {
  StageEnum,
  type SkillMeta,
  type Skill1Input,
  type SkillResult,
  type PrerequisiteCheckResult,
  type BusinessDimensions,
} from '../../src/core/types';
import { skill1OutputSchema } from '../../src/core/output-schema';

/** Skill1元数据 */
export const skill1Meta: SkillMeta = {
  id: 'skill1-idea-feasibility',
  name: 'Idea可行性研判',
  description: '对创业Idea进行全方位可行性研判，包括需求真伪校验、个人匹配度测评、竞品格局分析，输出《OPC项目可行性分析报告》',
  applicableStage: StageEnum.IDEA,
  version: '1.0.0',
  inputs: [
    { name: 'projectInfo', type: 'object', required: true, description: '项目基本信息' },
    { name: 'demandDescription', type: 'string', required: true, description: '需求描述' },
    { name: 'competitorInfo', type: 'string', required: false, description: '竞品信息' },
    { name: 'personalSkills', type: 'array', required: true, description: '个人技能清单' },
    { name: 'budget', type: 'number', required: true, description: '可用预算（元）' },
    { name: 'availableTime', type: 'number', required: true, description: '可投入时间（小时/周）' },
  ],
  outputSchema: skill1OutputSchema,
  prerequisites: [
    '有明确的创业Idea描述',
    '需求描述清晰，能说明目标用户和痛点',
    '已了解自身技能和可用资源',
  ],
};

/**
 * 前置条件检查
 * 验证用户是否处于构思期（IDEA阶段）
 */
export function checkPrerequisites(input: Skill1Input): PrerequisiteCheckResult {
  const failedConditions: string[] = [];
  const suggestions: string[] = [];

  // 检查1：项目信息是否完整
  if (!input.projectInfo.projectName || !input.projectInfo.description) {
    failedConditions.push('项目名称和描述不能为空');
    suggestions.push('请先明确你的创业Idea，包括项目名称和核心描述');
  }

  // 检查2：需求描述是否充分
  if (!input.demandDescription || input.demandDescription.length < 10) {
    failedConditions.push('需求描述过于简略，至少需要10个字符');
    suggestions.push('请详细描述你要解决的需求，包括目标用户、痛点场景、现有解决方案的不足');
  }

  // 检查3：个人技能是否已列出
  if (!input.personalSkills || input.personalSkills.length === 0) {
    failedConditions.push('未提供个人技能清单');
    suggestions.push('请列出你的核心技能，用于评估个人匹配度');
  }

  // 检查4：预算和时间是否合理
  if (input.budget < 0) {
    failedConditions.push('预算不能为负数');
    suggestions.push('请输入正确的可用预算');
  }
  if (input.availableTime <= 0) {
    failedConditions.push('可投入时间必须大于0');
    suggestions.push('请输入每周可投入的时间（小时）');
  }

  return {
    passed: failedConditions.length === 0,
    failedConditions,
    suggestedStage: StageEnum.IDEA,
    suggestions,
  };
}

/**
 * 构建Skill1的Prompt
 * 将用户输入嵌入到完整的Prompt模板中
 */
export function buildPrompt(input: Skill1Input): string {
  return `# OPC智脑 - Skill1：Idea可行性研判

## 智能体人设
你是一位专注服务于"一人创业者"（OPC, One Person Company）的创业诊断专家。你的核心能力是帮助创业者从0到1验证Idea的可行性，避免在伪需求上浪费时间。

## 阶段上下文
当前创业者处于【构思期】（五阶段模型第1阶段），核心目标是验证需求真伪、确认个人匹配度、完成可行性研判。

## 任务指令
请对以下创业Idea进行全方位可行性研判，输出《OPC项目可行性分析报告》。

### 待研判项目
- **项目名称**：${input.projectInfo.projectName}
- **项目描述**：${input.projectInfo.description}
- **所属行业**：${input.projectInfo.industry}
- **目标用户**：${input.projectInfo.targetUsers}
- **核心价值主张**：${input.projectInfo.valueProposition}

### 需求描述
${input.demandDescription}

${input.competitorInfo ? `### 竞品信息\n${input.competitorInfo}` : '### 竞品信息\n（未提供，请基于行业常识进行分析）'}

### 创业者画像
- **个人技能**：${input.personalSkills.join('、')}
- **创始人背景**：${input.projectInfo.founderBackground}
- **可用预算**：${input.budget}元
- **可投入时间**：${input.availableTime}小时/周

## 分析框架

### 1. 需求真伪校验
请严格按照以下框架判定需求类型：
- **刚需**：用户不解决就会产生严重损失或强烈痛苦，有明确付费意愿
- **改善型**：用户有更好选择但非必须，付费意愿取决于性价比
- **伪需求**：用户嘴上说需要但实际不会付费，或市场规模极小

请给出：
- 需求类型判定（刚需/改善型/伪需求）
- 判定理由（至少3条支撑证据）
- 支持刚需的证据列表
- 反对刚需的证据列表
- 需求验证建议（如何用最小成本验证）

### 2. 个人匹配度测评
从三个维度评估创业者与该Idea的匹配度：
- **技能匹配度**（0-100）：创业者现有技能与项目所需技能的重合度
- **时间匹配度**（0-100）：可投入时间是否足够支撑项目运转
- **预算匹配度**（0-100）：可用预算是否覆盖验证期所需
- **综合匹配度**：三项加权平均
- **短板分析**：最需要补齐的方面
- **提升建议**：如何提升匹配度

### 3. 竞品格局分析
分析至少3个竞品/替代方案，每个包含：
- 竞品名称与打法
- 定价策略
- 优势与劣势
- **单人创业者的应对策略**（重点：如何以一人之力差异化竞争）

### 4. 可行性综合判定
基于以上分析，给出可行性等级：
- **高度可行**：刚需+匹配度高+竞争有空间
- **可行**：改善型需求+匹配度中等+有差异化点
- **有挑战**：需求存疑或匹配度低或竞争激烈
- **不可行**：伪需求或严重不匹配或红海无空间

### 5. 替代赛道建议（仅当不可行时）
如果判定不可行，请提供2-3个轻量化替代赛道：
- 替代赛道名称
- 推荐理由
- 进入门槛

## 输出格式要求
请严格按照以下JSON Schema输出结构化结果：
\`\`\`json
${JSON.stringify(skill1OutputSchema, null, 2)}
\`\`\`

## 约束规则
1. 所有分析必须基于事实和逻辑，不做无依据的乐观预测
2. 竞品分析必须考虑"单人创业者"的约束，不假设有团队
3. 需求判定宁可偏保守，也不要鼓励在伪需求上投入
4. 预算和时间评估要留出安全余量（建议预留30%）
5. 替代赛道必须是同一创业者能力范围内可落地的
6. 所有建议必须可执行、可量化、有明确下一步`;
}

/**
 * 执行Skill1
 * 
 * @param input Skill1输入
 * @returns Skill执行结果（包含完整Prompt，可直接传给大模型）
 */
export function executeSkill1(input: Skill1Input): SkillResult {
  // 1. 前置条件检查
  const prereqCheck = checkPrerequisites(input);
  if (!prereqCheck.passed) {
    return {
      skillId: skill1Meta.id,
      success: false,
      data: {},
      prompt: '',
      error: `前置条件未满足：${prereqCheck.failedConditions.join('；')}。建议：${prereqCheck.suggestions.join('；')}`,
    };
  }

  // 2. 构建Prompt
  const prompt = buildPrompt(input);

  // 3. 返回结果
  return {
    skillId: skill1Meta.id,
    success: true,
    data: {
      projectName: input.projectInfo.projectName,
      stage: StageEnum.IDEA,
      stageLabel: '构思期',
    },
    prompt,
  };
}