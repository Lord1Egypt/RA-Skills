#!/usr/bin/env node
/**
 * MIA Planner - 智能规划器
 * 职责：生成 Search Plan，支持参考历史轨迹优化
 * 支持模式：local（本地部署）/ api（OpenAI协议兼容）
 */

import fetch from 'node-fetch';

// 读取配置
const MODE = process.env.MIA_PLANNER_MODE || 'local';
const CUSTOM_URL = process.env.MIA_PLANNER_URL;
const MODEL = process.env.MIA_PLANNER_MODEL;
const API_KEY = process.env.MIA_PLANNER_API_KEY;

// 模式校验
if (!['local', 'api'].includes(MODE)) {
  console.error(`Error: Invalid MIA_PLANNER_MODE="${MODE}". Must be "local" or "api"`);
  process.exit(1);
}

// API 模式必需参数检查
if (MODE === 'api' && !API_KEY) {
  console.error('Error: MIA_PLANNER_API_KEY is required when MIA_PLANNER_MODE=api');
  process.exit(1);
}

// 构建 URL
let PLANNER_URL;
if (CUSTOM_URL) {
  PLANNER_URL = CUSTOM_URL;
} else if (MODE === 'api') {
  PLANNER_URL = 'https://api.openai.com/v1/chat/completions';
} else {
  PLANNER_URL = 'http://localhost:8000/v1/chat/completions';
}

// 确定模型
const PLANNER_MODEL = MODEL || (MODE === 'api' ? 'gpt-4' : 'Qwen3-8B');

// 基础 Prompt
const BASE_PROMPT = `你是一名规划助手，为OpenClaw提供战略指导。该OpenClaw可以使用以下Skill：
- \`tavily-search\`：进行基于文本的网络查询以获取外部信息。

### 你的任务：
- 分析**问题**。 
- 建议一个**清晰、通用的工作计划或行动策略**，直接针对当前情况并为Agent提供每一步的中间目标。

### 输出应：
1. 表述要清晰简洁——字数不超过 300 个字，并以分步计划的形式呈现你的回答。
2. 该计划中的每一项步骤都必须是独立且可执行的，要明确指定一个单一的操作，比如调用一个工具（例如，执行带有精确查询意图的"搜索"操作）。
3. 不要直接给出答案，而要给出一个方案。
4. 禁止生成与计划无关的内容。
5. 你的回复不得包含任何事实性信息。你的输出仅应包含指导原则，不得添加任何解释。

**[问题]**（全局目标）：{问题}`;

// 参考历史轨迹的 Prompt
const REFERENCE_PROMPT = `你是一名规划助手。之前解决过类似问题，以下是参考方案：

### 历史方案
{历史Plan}

### 你的任务
请基于以上参考，为当前问题生成优化后的 Plan：
1. 可以借鉴历史方案的结构和策略
2. 根据当前问题的具体情况调整
3. 生成更高效、更精准的 Plan
4. 不要直接给出答案，只提供执行计划

**[当前问题]**（全局目标）：{问题}`;

async function generatePlan(question, referencePlan = null) {
  const prompt = referencePlan !== null
    ? REFERENCE_PROMPT.replace('{历史Plan}', referencePlan).replace('{问题}', question)
    : BASE_PROMPT.replace('{问题}', question);
  
  try {
    // 构建请求头
    const headers = { 'Content-Type': 'application/json' };
    if (MODE === 'api') {
      headers['Authorization'] = `Bearer ${API_KEY}`;
    }
    
    // 构建请求体
    const body = {
      model: PLANNER_MODEL,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7,
      max_tokens: 2048
    };
    
    // 本地模式添加特殊参数（兼容Qwen）
    if (MODE === 'local') {
      body.chat_template_kwargs = { enable_thinking: false };
    }
    
    // 发送请求（带30秒超时）
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    
    const response = await fetch(PLANNER_URL, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: controller.signal
    });
    
    clearTimeout(timeout);
    
    // 处理HTTP错误
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      const errorMsg = data.error?.message || `HTTP ${response.status}`;
      throw new Error(`API Error: ${errorMsg}`);
    }
    
    const data = await response.json();
    
    // 验证响应格式
    if (!data.choices || !data.choices[0]?.message?.content) {
      throw new Error('Invalid response format');
    }
    
    let plan = data.choices[0].message.content;
    
    // 清理输出（移除think标签）
    plan = plan.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
    
    return { plan, reference_used: referencePlan !== null, raw: data };
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Request timeout (30s)');
    }
    throw new Error(`Plan generation failed: ${error.message}`);
  }
}

function parseSteps(plan) {
  const lines = plan.split('\n').filter(line => line.trim());
  const steps = [];
  
  for (const line of lines) {
    const match = line.match(/^\s*(?:\d+[.、)）]|[-•*])\s*(.+)$/);
    if (match) {
      steps.push(match[1].trim());
    }
  }
  
  return steps;
}

// 主函数
async function main() {
  const question = process.argv[2];
  const referenceFlag = process.argv[3];
  const referencePlan = process.argv[4];
  
  if (!question) {
    console.error('Usage: mia-planner.mjs "your question" [--reference "historical plan"]');
    console.error('');
    console.error('Environment variables:');
    console.error('  MIA_PLANNER_MODE=local|api       # 运行模式（默认: local）');
    console.error('  MIA_PLANNER_URL=<url>            # 自定义端点（可选）');
    console.error('  MIA_PLANNER_MODEL=<model>        # 模型名称（可选）');
    console.error('  MIA_PLANNER_API_KEY=<key>        # API密钥（api模式必需）');
    process.exit(1);
  }
  
  try {
    const refPlan = (referenceFlag === '--reference' && referencePlan) ? referencePlan : null;
    const result = await generatePlan(question, refPlan);
    const steps = parseSteps(result.plan);
    
    // 输出 JSON 格式结果
    console.log(JSON.stringify({
      question,
      plan: result.plan,
      steps,
      reference_used: result.reference_used,
      model: PLANNER_MODEL,
      mode: MODE,
      timestamp: new Date().toISOString()
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ error: error.message }));
    process.exit(1);
  }
}

main();
