<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08 -->

# OPC智脑 - 集成指南

## 安装

```bash
npm install opc-skills
```

或从源码：

```bash
git clone https://gitee.com/zx_allen_li/opc_skills.git
cd opc-skills && npm install && npm run build
```

## 核心API

### 阶段判定

```typescript
import { classifyStage, type BusinessDimensions } from 'opc-skills';

const result = classifyStage({
  demandValidation: 30,    // 需求验证度 0-100
  solutionMaturity: 20,    // 方案成熟度 0-100
  complianceReadiness: 10, // 合规完备度 0-100
  userAcquisition: 5,      // 用户获取度 0-100
  scalabilityLevel: 0,     // 规模化度 0-100
});
// result.stage → 'IDEA'  result.stageLabel → '构思期'
// result.confidence → 0.72  result.recommendedSkill → 'skill1-idea-feasibility'
```

### 矛盾检测

```typescript
import { detectContradiction } from 'opc-skills';
const result = detectContradiction(dimensions);
// result.hasContradiction / result.contradictions / result.healthScore
```

### 执行Skill

```typescript
import { executeSkill1, type Skill1Input } from 'opc-skills';

const result = executeSkill1({
  projectInfo: {
    projectName: '微团队CRM',
    description: '专为3-5人微团队的轻量CRM',
    industry: 'SaaS工具',
    targetUsers: '3-5人微团队创始人',
    valueProposition: '极简CRM，1/10价格',
    founderBackground: '5年SaaS产品经理',
    budget: 10000,
    availableTime: 30,
  },
  demandDescription: '微团队需要极简CRM',
  personalSkills: ['产品经理', '基础编程'],
  budget: 10000,
  availableTime: 30,
});
// result.success → true  result.prompt → 完整Prompt文本
```

## 集成方式

### OpenAI Function Calling

```typescript
import OpenAI from 'openai';
import { executeSkill1, skill1OutputSchema } from 'opc-skills';

const openai = new OpenAI({ apiKey: 'your-key' });
const skillResult = executeSkill1(input);

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: '你是OPC智脑创业诊断专家' },
    { role: 'user', content: skillResult.prompt },
  ],
  functions: [{ name: 'feasibility_report', description: '输出可行性分析报告', parameters: skill1OutputSchema }],
  function_call: { name: 'feasibility_report' },
});
```

### LangChain

```typescript
import { executeSkill1 } from 'opc-skills';
const skillResult = executeSkill1(input);
// 将 skillResult.prompt 作为 System Prompt 传给 LangChain
```

### Coze / Dify

- **Coze**：将`system-persona.md`和`core-hub.md`粘贴到人设Prompt，创建5个工作流对应5个Skill
- **Dify**：创建Chatflow，添加问题分类器节点路由到对应Skill分支

详见 [examples/coze-example.md](../examples/coze-example.md) 和 [examples/dify-example.md](../examples/dify-example.md)

### 自定义集成

核心输出是**Prompt文本**，可发送给任何大模型：

```typescript
import { executeSkill1 } from 'opc-skills';
const result = executeSkill1(input);
if (result.success) {
  const aiResponse = await yourLLM.generate(result.prompt);
  const report = JSON.parse(aiResponse);
}
```

## Prompt文件

位于`src/prompts/`，纯Markdown格式，可直接复制到任何AI平台：

| 文件 | 用途 |
|------|------|
| system-persona.md | 智能体人设（System Prompt） |
| core-hub.md | 核心中枢调度（System Prompt一部分） |
| skill1-5.md | 对应5个Skill的完整Prompt |

## 输出Schema

```typescript
import { skill1OutputSchema, getOutputSchema } from 'opc-skills';
console.log(skill1OutputSchema);                    // Skill1的JSON Schema
const schema = getOutputSchema('skill1-idea-feasibility'); // 按ID获取
```

可用于OpenAI Function Calling、LangChain StructuredOutputParser、Dify/Coze输出变量配置。

## TypeScript类型

```typescript
import type {
  BusinessDimensions, StageResult, ContradictionResult,
  Skill1Input, Skill2Input, Skill3Input, Skill4Input, Skill5Input,
  SkillResult, ProjectInfo,
} from 'opc-skills';
```

## 常见问题

| 问题 | 回答 |
|------|------|
| 必须用TypeScript？ | 不是，编译后的JS可在Node.js直接使用，但推荐TS获得类型提示 |
| 依赖特定大模型？ | 不依赖，核心输出是Prompt文本，可发给任何大模型 |
| 可以在浏览器用？ | 可以，纯TS实现，无Node.js特有API |
| Prompt文件可单独用？ | 可以，纯Markdown，直接复制到Coze/Dify等平台 |
| 如何自定义Prompt？ | Fork项目修改`src/prompts/`下的md文件，或修改Skill的`buildPrompt`函数 |
