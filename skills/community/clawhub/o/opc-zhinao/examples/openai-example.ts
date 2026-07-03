/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * OpenAI Function Calling 集成示例
 * 
 * 演示如何将opc-skills与OpenAI API集成，
 * 使用Function Calling实现结构化输出。
 * 
 * 运行方式：npx tsx examples/openai-example.ts
 */

import {
  classifyStage,
  executeSkill1,
  skill1OutputSchema,
  getStageInfo,
  StageEnum,
  type Skill1Input,
  type BusinessDimensions,
} from '../src/index';

// ============================================================
// 示例1：五阶段判定 + 自动调度Skill
// ============================================================

function demoStageClassification() {
  console.log('=== 示例1：五阶段判定 ===\n');

  // 模拟一个处于构思期的创业者
  const dimensions: BusinessDimensions = {
    demandValidation: 25,   // 有初步想法，但未验证
    solutionMaturity: 10,   // 没有产品
    complianceReadiness: 5, // 未注册
    userAcquisition: 0,     // 无用户
    scalabilityLevel: 0,    // 无规模化
  };

  const result = classifyStage(dimensions);

  console.log(`阶段判定：${result.stageLabel}（${result.stage}）`);
  console.log(`置信度：${result.confidence}`);
  console.log(`推荐Skill：${result.recommendedSkill}`);
  console.log(`判定理由：${result.reasoning}`);
  console.log(`是否存在矛盾：${result.hasContradiction ? '是' : '否'}`);
  console.log('');

  // 获取阶段详细信息
  const stageInfo = getStageInfo(result.stage);
  console.log(`阶段目标：${stageInfo.goal}`);
  console.log(`关键风险：${stageInfo.risk}`);
  console.log(`毕业条件：${stageInfo.graduationCriteria}`);
}

// ============================================================
// 示例2：执行Skill1并生成Prompt
// ============================================================

function demoSkill1Execution() {
  console.log('\n=== 示例2：执行Skill1 - Idea可行性研判 ===\n');

  const input: Skill1Input = {
    projectInfo: {
      projectName: '微团队CRM',
      description: '专为3-5人微团队设计的轻量CRM，解决小团队用不起大CRM、用Excel又太乱的痛点',
      industry: 'SaaS工具',
      targetUsers: '3-5人微团队的创始人/负责人',
      valueProposition: '用大CRM1/10的价格，解决微团队客户管理核心需求',
      founderBackground: '5年SaaS产品经理，熟悉CRM领域，有技术基础',
      budget: 10000,
      availableTime: 30,
    },
    demandDescription: '3-5人微团队目前只能用Excel管理客户，或被迫使用为中小企业设计的CRM（功能臃肿、价格高）。他们需要一个极简的、只关注核心流程的CRM。',
    personalSkills: ['产品经理', '需求分析', '基础编程', 'CRM领域知识'],
    budget: 10000,
    availableTime: 30,
  };

  const result = executeSkill1(input);

  if (result.success) {
    console.log(`Skill执行成功：${result.skillId}`);
    console.log(`项目名称：${result.data.projectName}`);
    console.log(`当前阶段：${result.data.stageLabel}`);
    console.log(`Prompt长度：${result.prompt.length} 字符`);
    console.log('\n--- Prompt前500字符预览 ---');
    console.log(result.prompt.substring(0, 500) + '...');
  } else {
    console.log(`Skill执行失败：${result.error}`);
  }
}

// ============================================================
// 示例3：与OpenAI API集成（伪代码，需要API Key）
// ============================================================

/**
 * 将opc-skills生成的Prompt发送给OpenAI API
 * 
 * 实际使用时需要安装openai包：npm install openai
 */
async function demoOpenAIIntegration() {
  console.log('\n=== 示例3：OpenAI API集成（伪代码） ===\n');

  // Step 1: 判定阶段
  const dimensions: BusinessDimensions = {
    demandValidation: 25,
    solutionMaturity: 10,
    complianceReadiness: 5,
    userAcquisition: 0,
    scalabilityLevel: 0,
  };
  const stageResult = classifyStage(dimensions);

  // Step 2: 执行对应Skill，生成Prompt
  const skill1Input: Skill1Input = {
    projectInfo: {
      projectName: '示例项目',
      description: '示例描述',
      industry: 'SaaS',
      targetUsers: '微团队创始人',
      valueProposition: '极简CRM',
      founderBackground: '产品经理',
    },
    demandDescription: '微团队需要极简CRM',
    personalSkills: ['产品经理'],
    budget: 10000,
    availableTime: 30,
  };
  const skillResult = executeSkill1(skill1Input);

  if (!skillResult.success) {
    console.log('Skill执行失败，跳过API调用');
    return;
  }

  // Step 3: 发送给OpenAI（伪代码）
  console.log('以下为与OpenAI API集成的伪代码：\n');
  console.log(`
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: 'your-api-key' });

// 方式1：直接使用Prompt
const response1 = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: '你是一位OPC创业诊断专家' },
    { role: 'user', content: skillResult.prompt },
  ],
});

// 方式2：使用Function Calling实现结构化输出
const response2 = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: '你是一位OPC创业诊断专家' },
    { role: 'user', content: skillResult.prompt },
  ],
  functions: [{
    name: 'feasibility_report',
    description: '输出OPC项目可行性分析报告',
    parameters: ${JSON.stringify(skill1OutputSchema, null, 2)},
  }],
  function_call: { name: 'feasibility_report' },
});

// 解析结构化输出
const report = JSON.parse(response2.choices[0].message.function_call.arguments);
console.log(report.feasibilityLevel);  // 'feasible'
console.log(report.summary);           // 可行性研判总结
  `);
}

// ============================================================
// 运行示例
// ============================================================

demoStageClassification();
demoSkill1Execution();
demoOpenAIIntegration();