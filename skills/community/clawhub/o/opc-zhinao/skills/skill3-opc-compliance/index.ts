/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * Skill3：OPC合规落地规划（实体期）
 * 
 * 核心能力：
 * - 主体选型：个体户 vs 一人有限公司优劣
 * - 经营范围精准推荐
 * - 2024新公司法OPC合规要点
 * - 初创财税规划：小规模纳税人/零申报/成本票
 * - 商用模板：合同/报价单/保密协议/服务说明书
 * - 前期筹备清单：对公户/开票/印章/知识产权
 */

import {
  StageEnum,
  type SkillMeta,
  type Skill3Input,
  type SkillResult,
  type PrerequisiteCheckResult,
} from '../../src/core/types';
import { skill3OutputSchema } from '../../src/core/output-schema';

/** Skill3元数据 */
export const skill3Meta: SkillMeta = {
  id: 'skill3-opc-compliance',
  name: 'OPC合规落地规划',
  description: '为一人创业者规划合规落地方案，包括主体选型、经营范围、新公司法合规要点、财税规划、商用模板和筹备清单',
  applicableStage: StageEnum.ENTITY,
  version: '1.0.0',
  inputs: [
    { name: 'projectInfo', type: 'object', required: true, description: '项目基本信息' },
    { name: 'businessType', type: 'string', required: true, description: '业务类型（service/product/hybrid）' },
    { name: 'expectedMonthlyRevenue', type: 'number', required: false, description: '预计月营收' },
    { name: 'hasEmployees', type: 'boolean', required: false, description: '是否有员工', defaultValue: false },
    { name: 'city', type: 'string', required: false, description: '所在城市' },
  ],
  outputSchema: skill3OutputSchema,
  prerequisites: [
    'MVP已设计完成（Skill2输出）',
    '业务类型已明确（服务/产品/混合）',
    '有明确的营收预期',
  ],
};

/**
 * 前置条件检查
 */
export function checkPrerequisites(input: Skill3Input): PrerequisiteCheckResult {
  const failedConditions: string[] = [];
  const suggestions: string[] = [];

  if (!input.projectInfo.projectName) {
    failedConditions.push('项目名称不能为空');
    suggestions.push('请提供项目名称');
  }

  if (!['service', 'product', 'hybrid'].includes(input.businessType)) {
    failedConditions.push('业务类型必须是 service/product/hybrid 之一');
    suggestions.push('请明确业务类型：service=纯服务, product=纯产品, hybrid=混合');
  }

  return {
    passed: failedConditions.length === 0,
    failedConditions,
    suggestedStage: StageEnum.ENTITY,
    suggestions,
  };
}

/**
 * 构建Skill3的Prompt
 */
export function buildPrompt(input: Skill3Input): string {
  const businessTypeLabel = {
    service: '纯服务型',
    product: '纯产品型',
    hybrid: '服务+产品混合型',
  }[input.businessType];

  return `# OPC智脑 - Skill3：OPC合规落地规划

## 智能体人设
你是一位专注服务于"一人创业者"（OPC）的合规落地顾问。你深谙中国商事法规和新公司法，擅长用最低成本帮助创业者完成合规化运营，避免过度注册和过度合规。

## 阶段上下文
当前创业者处于【实体期】（五阶段模型第3阶段），核心目标是完成主体注册、财税规划、商用模板准备、前期筹备，实现低成本合规落地。

## 任务指令
请为以下一人创业项目规划合规落地方案。

### 项目信息
- **项目名称**：${input.projectInfo.projectName}
- **项目描述**：${input.projectInfo.description}
- **所属行业**：${input.projectInfo.industry}
- **主营业务**：${input.projectInfo.valueProposition}
- **业务类型**：${businessTypeLabel}
${input.expectedMonthlyRevenue ? `- **预计月营收**：${input.expectedMonthlyRevenue}元` : ''}
${input.hasEmployees !== undefined ? `- **是否有员工**：${input.hasEmployees ? '是' : '否'}` : ''}
${input.city ? `- **所在城市**：${input.city}` : ''}

## 分析框架

### 1. 主体选型建议
请对比分析两种主体类型的优劣，给出推荐：

**个体工商户**：
- 优势：注册简单、维护成本低、无企业所得税、个税核定征收
- 劣势：无限连带责任、无法融资、品牌形象受限

**一人有限公司**：
- 优势：有限责任、品牌形象好、可融资、可开专票
- 劣势：需记账报税、有企业所得税、需年度审计、新公司法要求更严

请给出：
- 推荐类型及理由
- 优势列表
- 劣势列表
- 选择建议（基于项目特点）

### 2. 经营范围精准推荐
- **主营范围**（必须包含，与核心业务直接相关）
- **扩围范围**（建议包含，为未来业务拓展留空间）
- 经营范围说明（为什么这样选）

### 3. 2024新公司法OPC合规要点
请重点关注2024年7月1日施行的新公司法对一人有限公司的影响：
- 关键合规要点（至少5条）
- 风险预警（可能踩的坑）
- 行动清单（必须做的事项）

### 4. 初创财税规划
- **纳税人类型建议**：小规模纳税人 vs 一般纳税人
- **零申报指南**：创业初期如何合规零申报
- **成本票策略**：如何获取和管理成本票
- **月度财税例行事项**：每月必做的财税动作

### 5. 商用模板清单
列出创业必备的商用文档模板：
- 合同模板
- 报价单模板
- 保密协议模板
- 服务说明书模板
- 其他必要模板
每个模板标注优先级和获取方式。

### 6. 前期筹备清单
按优先级排序的筹备事项：
- 对公账户开户
- 发票申领
- 印章刻制
- 知识产权保护（商标/软著等）
- 其他必要事项

每个事项标注：是否必须、预估费用、预估时间、优先级。

## 输出格式要求
请严格按照以下JSON Schema输出结构化结果：
\`\`\`json
${JSON.stringify(skill3OutputSchema, null, 2)}
\`\`\`

## 约束规则
1. 合规建议必须基于2024年新公司法的最新规定
2. 所有费用估算必须保守，留出20%余量
3. 优先推荐最低成本的合规路径
4. 个体户和一人有限公司的对比必须客观，不偏袒
5. 经营范围不能过于宽泛，避免被重点监管
6. 财税规划必须合法合规，不推荐任何灰色操作
7. 筹备清单必须按优先级排序，标注哪些可以延后`;
}

/**
 * 执行Skill3
 */
export function executeSkill3(input: Skill3Input): SkillResult {
  const prereqCheck = checkPrerequisites(input);
  if (!prereqCheck.passed) {
    return {
      skillId: skill3Meta.id,
      success: false,
      data: {},
      prompt: '',
      error: `前置条件未满足：${prereqCheck.failedConditions.join('；')}`,
    };
  }

  const prompt = buildPrompt(input);

  return {
    skillId: skill3Meta.id,
    success: true,
    data: {
      projectName: input.projectInfo.projectName,
      stage: StageEnum.ENTITY,
      stageLabel: '实体期',
    },
    prompt,
  };
}