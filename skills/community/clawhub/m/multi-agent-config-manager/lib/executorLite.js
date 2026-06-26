/**
 * 执行引擎精简版 - v8.0 Tokens优化版本
 * 
 * 核心变化：
 * 1. 默认使用JSON强约束输出（节省 25-30% tokens）
 * 2. 提示词精简（从 ~800行 → ~80行）
 * 3. 集成输出校验机制
 * 4. 失败边界机制（skip/fallback/partial）
 * 
 * 使用方式：
 * - 简单任务：直接使用 buildLiteSpawnParams
 * - 复杂任务：使用 buildSpawnParams（完整版）
 */

import fs from 'fs';
import path from 'path';
import { generateAgentPrompt } from './communication.js';
import { validateOutput, selectSchema, formatSchemaPrompt } from './outputSchema.js';
import { selectModel, buildModelPool } from './modelSelector.js';
import { checkModelThinking, selectThinkingLevel } from './thinkingCapabilities.js';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');

// ===== 失败策略定义 =====
export const FAILURE_STRATEGY = {
  skip: { name: '跳过', action: '跳过该代理，继续执行其他代理' },
  fallback: { name: '兜底', action: '使用预设模板结果' },
  partial: { name: '部分', action: '部分成功，继续聚合' },
  retry: { name: '重试', action: '重新调用该代理（最多2次）' }
};

// ===== 复杂度评估（简化版） =====
function estimateComplexityLite(task) {
  const desc = (task?.description || '').toLowerCase();
  
  // 简单任务信号词
  const simpleSignals = ['列出', '汇总', '格式化', '简单', '快速', 'list', 'quick'];
  if (simpleSignals.some(s => desc.includes(s))) return 'simple';
  
  // 复杂任务信号词
  const complexSignals = ['深入', '全面', '多维度', '分析', 'deep', 'comprehensive'];
  if (complexSignals.some(s => desc.includes(s))) return 'complex';
  
  return 'medium';
}

// ===== 核心函数：精简版Spawn参数构建 =====

/**
 * 构建精简版子代理Spawn参数
 * 
 * @param {object} agentProfile - 代理配置
 * @param {object} task - 任务描述 { description, requirements }
 * @param {object} workflow - 工作流实例
 * @param {object} options - 额外选项
 * @returns {object} sessions_spawn 调用参数
 */
export function buildLiteSpawnParams(agentProfile, task, workflow, options = {}) {
  // ===== 输出模式（默认JSON） =====
  const outputMode = options.outputMode || 'json';
  
  // ===== 复杂度评估 =====
  const complexity = options.complexity || estimateComplexityLite(task);
  
  // ===== 模型选择 =====
  const modelResult = selectModel(agentProfile.name, {
    complexity,
    allowFree: options.allowFree !== false
  });
  
  // 模型池耗尽降级
  if (modelResult.error || !modelResult.model) {
    const modelPool = buildModelPool();
    const fallbackModel = modelPool.all[0];
    if (fallbackModel) {
      modelResult.model = fallbackModel.id;
      modelResult.tier = fallbackModel.tier;
      modelResult.reason = `[降级] 复用池内首个模型: ${fallbackModel.id}`;
    }
  }
  
  // ===== Thinking配置 =====
  const thinkingCaps = checkModelThinking(modelResult.model);
  const finalThinking = thinkingCaps.supportsThinking 
    ? selectThinkingLevel(modelResult.model, complexity) 
    : 'off';
  
  // ===== 超时预设 =====
  const timeoutPresets = { simple: 120, medium: 300, complex: 480 };
  const timeoutSeconds = options.timeoutSeconds || timeoutPresets[complexity] || 300;
  
  // ===== 输出文件路径 =====
  const outputDir = options.outputDir || path.join(CONFIG_DIR, 'shared', 'final');
  const ext = outputMode === 'json' ? '.json' : '.md';
  const outputFile = path.join(outputDir, `${agentProfile.name}_report${ext}`);
  
  // ===== 精简提示词（v8.0核心） =====
  const context = {
    goal: workflow.goal,
    output_dir: outputDir
  };
  
  const prompt = generateAgentPrompt(agentProfile, task, 'standard_task', context);
  const outputInstruction = `输出文件: ${outputFile}\n完成后输出: EXECUTION_COMPLETE`;
  const completeTask = `${prompt}\n\n${outputInstruction}`;
  
  // ===== 创建目录 =====
  fs.mkdirSync(outputDir, { recursive: true });
  
  // ===== 返回Spawn参数 =====
  return {
    task: completeTask,
    label: `lite-${agentProfile.name}-${workflow.id}`,
    model: modelResult.model,
    thinking: finalThinking !== 'off' ? finalThinking : undefined,
    timeoutSeconds,
    cwd: CONFIG_DIR,
    mode: 'run',
    thread: false,
    cleanup: 'keep',
    output_file: outputFile,
    output_mode: outputMode,
    schema: outputMode === 'json' ? selectSchema(agentProfile.name) : null,
    failure_strategy: FAILURE_STRATEGY[options.failureStrategy || 'retry'],
    _meta: {
      agentRole: agentProfile.name,
      complexity,
      modelTier: modelResult.tier || 'unknown',
      tokensSavedEstimate: outputMode === 'json' ? '25-30%' : '0%',
      version: 'v8.0-lite'
    }
  };
}

// ===== 输出校验函数 =====

/**
 * 校验子代理输出结果
 * 
 * @param {string} agentName - 代理名称
 * @param {string} outputDir - 输出目录
 * @returns {object} 校验结果 { valid, errors, parsed, action }
 */
export function validateLiteOutput(agentName, outputDir) {
  const schema = selectSchema(agentName);
  const ext = '.json'; // 精简版默认JSON
  const outputFile = path.join(outputDir, `${agentName}_report${ext}`);
  
  try {
    if (!fs.existsSync(outputFile)) {
      return {
        valid: false,
        errors: ['输出文件不存在'],
        parsed: null,
        action: 'retry',
        strategy: FAILURE_STRATEGY.retry
      };
    }
    
    const content = fs.readFileSync(outputFile, 'utf-8');
    return validateOutput(content, schema);
  } catch (error) {
    return {
      valid: false,
      errors: [`读取失败: ${error.message}`],
      parsed: null,
      action: 'fallback',
      strategy: FAILURE_STRATEGY.fallback
    };
  }
}

// ===== 失败处理函数 =====

/**
 * 根据校验结果选择失败策略
 */
export function handleLiteFailure(validationResult, agentName) {
  const strategy = validationResult.strategy || FAILURE_STRATEGY.retry;
  
  switch (strategy.name) {
    case '跳过':
      return {
        action: 'skip',
        message: `跳过 ${agentName}，继续其他代理`,
        result: null
      };
    
    case '兜底':
      return {
        action: 'fallback',
        message: `使用预设模板`,
        result: generateFallbackResult(agentName)
      };
    
    case '部分':
      return {
        action: 'partial',
        message: `部分结果，继续聚合`,
        result: validationResult.parsed || {}
      };
    
    case '重试':
      return {
        action: 'retry',
        message: `重新调用 ${agentName}`,
        maxRetries: 2,
        result: null
      };
    
    default:
      return {
        action: 'retry',
        message: `默认重试`,
        maxRetries: 2,
        result: null
      };
  }
}

// ===== 兜底结果生成 =====

function generateFallbackResult(agentName) {
  // 根据代理类型生成预设模板
  if (agentName.includes('Research')) {
    return {
      findings: ['[待补充] 数据不足，需人工复核'],
      analysis: '[兜底模式] 研究未完成',
      conclusion: '需进一步调研',
      sources: [],
      confidence: 'low'
    };
  }
  
  if (agentName.includes('Critic')) {
    return {
      issues: ['[兜底] 未完成审核'],
      strengths: [],
      improvements: ['需人工复核'],
      verdict: 'conditional',
      score: 50
    };
  }
  
  // 默认兜底
  return {
    findings: ['[兜底] 结果不完整'],
    analysis: '需人工复核',
    conclusion: '系统降级输出',
    sources: [],
    confidence: 'low'
  };
}

// ===== 批量Spawn参数构建 =====

/**
 * 为多个代理批量构建精简版Spawn参数
 */
export function buildBatchLiteSpawnParams(agentNames, workflow, profiles, options = {}) {
  const outputDir = options.outputDir || path.join(CONFIG_DIR, 'shared', 'final');
  fs.mkdirSync(outputDir, { recursive: true });
  
  return agentNames.map(agentName => {
    const profile = profiles[agentName];
    if (!profile) {
      return {
        error: `代理配置缺失: ${agentName}`,
        agentName,
        skip: true
      };
    }
    
    const task = {
      description: options.tasks?.[agentName] || `执行 ${agentName} 的研究任务`,
      requirements: options.requirements?.[agentName] || []
    };
    
    return buildLiteSpawnParams(profile, task, workflow, {
      ...options,
      outputDir
    });
  });
}

// ===== Tokens节省估算 =====

/**
 * 估算本次任务的Tokens节省
 */
export function estimateTokensSavings(spawnParams) {
  const baselineTokens = {
    promptOld: 800, // 原版提示词行数
    contextOld: 500, // 原版上下文传递
    totalOld: 1300
  };
  
  const optimizedTokens = {
    promptNew: spawnParams.output_mode === 'json' ? 80 : 400,
    contextNew: spawnParams.output_mode === 'json' ? 20 : 100,
    totalNew: spawnParams.output_mode === 'json' ? 100 : 500
  };
  
  const savedTokens = baselineTokens.totalOld - optimizedTokens.totalNew;
  const savedPercent = Math.round((savedTokens / baselineTokens.totalOld) * 100);
  
  return {
    baseline: baselineTokens,
    optimized: optimizedTokens,
    saved: {
      tokens: savedTokens,
      percent: savedPercent + '%'
    },
    mode: spawnParams.output_mode,
    version: spawnParams._meta?.version || 'v8.0-lite'
  };
}

// ===== 导出所有函数 =====

export default {
  buildLiteSpawnParams,
  validateLiteOutput,
  handleLiteFailure,
  buildBatchLiteSpawnParams,
  estimateTokensSavings,
  FAILURE_STRATEGY
};