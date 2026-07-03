/**
 * @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08
 * 
 * LangChain集成示例
 * 
 * 演示如何将opc-skills与LangChain集成，
 * 使用StructuredOutputParser实现结构化输出。
 * 
 * 运行方式：npx tsx examples/langchain-example.ts
 * 
 * 需要安装：npm install langchain @langchain/openai zod
 */

import {
  classifyStage,
  executeSkill1,
  skill1OutputSchema,
  getStageInfo,
  getAllStageInfo,
  StageEnum,
  type Skill1Input,
  type BusinessDimensions,
} from '../src/index';

// ============================================================
// 示例1：使用opc-skills进行阶段判定
// ============================================================

function demoLangChainStageClassification() {
  console.log('=== LangChain集成示例1：阶段判定 ===\n');

  // 模拟用户输入的五维度信息
  const userDimensions: BusinessDimensions = {
    demandValidation: 30,
    solutionMaturity: 20,
    complianceReadiness: 10,
    userAcquisition: 5,
    scalabilityLevel: 0,
  };

  // 使用opc-skills进行判定
  const result = classifyStage(userDimensions);

  console.log('阶段判定结果：');
  console.log(`  阶段：${result.stageLabel}（${result.stage}）`);
  console.log(`  置信度：${result.confidence}`);
  console.log(`  推荐Skill：${result.recommendedSkill}`);
  console.log(`  是否有矛盾：${result.hasContradiction ? '是' : '否'}`);

  // 输出所有阶段信息
  console.log('\n所有阶段信息：');
  const allStages = getAllStageInfo();
  for (const stage of allStages) {
    console.log(`  ${stage.order}. ${stage.label}：${stage.goal}`);
  }
}

// ============================================================
// 示例2：LangChain集成伪代码
// ============================================================

function demoLangChainIntegration() {
  console.log('\n=== LangChain集成示例2：完整集成伪代码 ===\n');

  console.log(`
import { ChatOpenAI } from '@langchain/openai';
import { StructuredOutputParser } from 'langchain/output_parsers';
import { z } from 'zod';
import { ChatPromptTemplate } from 'langchain/prompts';
import {
  classifyStage,
  executeSkill1,
  skill1OutputSchema,
} from 'opc-skills';

// Step 1: 定义输出Schema（Zod格式）
const feasibilityReportSchema = z.object({
  reportTitle: z.string().describe('报告标题'),
  projectName: z.string().describe('项目名称'),
  demandValidation: z.object({
    demandType: z.enum(['rigid', 'improvement', 'fake']),
    demandTypeLabel: z.enum(['刚需', '改善型', '伪需求']),
    reasoning: z.string(),
  }),
  personalMatch: z.object({
    skillMatch: z.number().min(0).max(100),
    timeMatch: z.number().min(0).max(100),
    budgetMatch: z.number().min(0).max(100),
    overallMatch: z.number().min(0).max(100),
  }),
  feasibilityLevel: z.enum(['highly_feasible', 'feasible', 'challenging', 'not_feasible']),
  feasibilityLabel: z.enum(['高度可行', '可行', '有挑战', '不可行']),
  summary: z.string(),
  nextStep: z.string(),
});

// Step 2: 创建输出解析器
const parser = StructuredOutputParser.fromZodSchema(feasibilityReportSchema);

// Step 3: 创建LLM实例
const llm = new ChatOpenAI({
  modelName: 'gpt-4o',
  temperature: 0,
});

// Step 4: 判定阶段并生成Prompt
const dimensions = {
  demandValidation: 30,
  solutionMaturity: 20,
  complianceReadiness: 10,
  userAcquisition: 5,
  scalabilityLevel: 0,
};
const stageResult = classifyStage(dimensions);

// Step 5: 执行对应Skill
const skillInput = {
  projectInfo: {
    projectName: '示例项目',
    description: '示例描述',
    industry: 'SaaS',
    targetUsers: '微团队',
    valueProposition: '极简工具',
    founderBackground: '产品经理',
  },
  demandDescription: '微团队需要极简工具',
  personalSkills: ['产品经理'],
  budget: 10000,
  availableTime: 30,
};
const skillResult = executeSkill1(skillInput);

// Step 6: 创建Prompt模板
const prompt = ChatPromptTemplate.fromMessages([
  ['system', skillResult.prompt],
  ['human', '{question}'],
]);

// Step 7: 构建Chain
const chain = prompt.pipe(llm).pipe(parser);

// Step 8: 执行Chain
const report = await chain.invoke({
  question: '请对这个Idea进行可行性研判',
  format_instructions: parser.getFormatInstructions(),
});

console.log(report.feasibilityLabel);  // '可行'
console.log(report.summary);           // 可行性总结
console.log(report.nextStep);          // 下一步建议
  `);
}

// ============================================================
// 示例3：使用RunnableSequence构建多阶段Chain
// ============================================================

function demoMultiStageChain() {
  console.log('\n=== LangChain集成示例3：多阶段Chain伪代码 ===\n');

  console.log(`
import { RunnableSequence } from 'langchain/schema/runnable';

// 构建多阶段诊断Chain
const diagnosisChain = RunnableSequence.from([
  // Step 1: 阶段判定
  (input: UserInput) => {
    const dimensions = mapUserInputToDimensions(input);
    return classifyStage(dimensions);
  },
  
  // Step 2: 根据阶段选择Skill
  (stageResult: StageResult) => {
    switch (stageResult.stage) {
      case 'IDEA': return executeSkill1;
      case 'MVP': return executeSkill2;
      case 'ENTITY': return executeSkill3;
      case 'VALIDATION': return executeSkill4;
      case 'SCALE': return executeSkill5;
    }
  },
  
  // Step 3: 执行Skill获取Prompt
  (executeSkill: Function) => executeSkill(skillInput),
  
  // Step 4: 发送给LLM
  (skillResult: SkillResult) => llm.invoke(skillResult.prompt),
  
  // Step 5: 解析结构化输出
  (llmResult: any) => parser.parse(llmResult.content),
]);

// 执行多阶段诊断
const finalReport = await diagnosisChain.invoke(userInput);
  `);
}

// ============================================================
// 运行示例
// ============================================================

demoLangChainStageClassification();
demoLangChainIntegration();
demoMultiStageChain();