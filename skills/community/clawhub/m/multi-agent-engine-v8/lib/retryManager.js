/**
 * 重试管理器 (Retry Manager)
 *
 * 职责：
 * 1. 区分错误类型（超时/API错误/空输出/文件缺失/质量不合格）
 * 2. 根据错误类型选择不同重试策略
 * 3. API 错误自动换模型，超时自动加时限
 * 4. 记录重试历史，避免无限循环
 */

import fs from 'fs';
import path from 'path';
import { selectModel } from './modelSelector.js';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');

// ===================== 错误类型 =====================

export const ErrorType = {
  TIMEOUT:      'timeout',       // 超时
  API_ERROR:    'api_error',     // 402/429/500
  EMPTY_OUTPUT: 'empty_output',  // 0 tokens 输出
  FILE_MISSING: 'file_missing',  // 输出文件不存在
  QUALITY_FAIL: 'quality_fail',  // 质量验证不通过
  CRASH:        'crash',         // 子代理崩溃（异常退出）
  THINKING_FAIL: 'thinking_fail', // Thinking 未生效
  QPS_RATE_LIMIT: 'qps_rate_limit', // Free 层 QPS 限流（非正常退出，<30s 超时）
  UNKNOWN:      'unknown'
};

// ===================== 重试策略 =====================

const RETRY_STRATEGY = {
  [ErrorType.TIMEOUT]: {
    maxRetries: 1,
    timeoutMultiplier: 1.5,
    switchModel: false,
    description: '超时：增加 1.5x 时限重试'
  },
  [ErrorType.API_ERROR]: {
    maxRetries: 2,
    timeoutMultiplier: 1.0,
    switchModel: true,
    description: 'API 错误：换模型重试'
  },
  [ErrorType.EMPTY_OUTPUT]: {
    maxRetries: 1,
    timeoutMultiplier: 1.5,
    switchModel: true,
    description: '空输出：换模型 + 增加时限'
  },
  [ErrorType.FILE_MISSING]: {
    maxRetries: 1,
    timeoutMultiplier: 1.5,
    switchModel: false,
    description: '文件缺失：增加时限重试'
  },
  [ErrorType.QUALITY_FAIL]: {
    maxRetries: 2,
    timeoutMultiplier: 1.0,
    switchModel: false,
    description: '质量不合格：同模型重试（加强提示）'
  },
  [ErrorType.CRASH]: {
    maxRetries: 1,
    timeoutMultiplier: 1.5,
    switchModel: true,
    description: '崩溃：换模型 + 增加时限'
  },
  [ErrorType.THINKING_FAIL]: {
    maxRetries: 2,
    timeoutMultiplier: 1.0,
    switchModel: true,
    description: 'Thinking 未生效：第一次降级为 off，第二次换模型'
  },
  [ErrorType.QPS_RATE_LIMIT]: {
    maxRetries: 2,
    timeoutMultiplier: 1.2,
    switchModel: true,
    description: 'Free 层 QPS 限流：强制换到 standard 层重试'
  }
};

// ===================== 降级级别 =====================

export const DegradationLevel = {
  NONE:    0,  // 全部成功
  LIGHT:   1,  // 成功率 >= 60%：主代理补做缺失
  MODERATE: 2,  // 成功率 >= 30%：重试缺失代理
  HEAVY:   3   // 成功率 < 30%：主代理全面接管
};

// ===================== 核心函数 =====================

/**
 * 分析子代理失败原因，归类错误类型
 *
 * @param {object} agentResult - 子代理执行结果
 * @param {string} agentResult.sessionKey - session key
 * @param {string} agentResult.outputFile - 预期输出文件路径
 * @param {number} agentResult.tokensUsed - 使用的 token 数
 * @param {string} agentResult.error - 错误信息
 * @param {string} agentResult.status - 状态
 * @returns {object} { errorType, detail, strategy }
 */
export function diagnoseFailure(agentResult) {
  const { outputFile, tokensUsed, error, status } = agentResult;

  // 1. 检查错误信息（最可靠）
  if (error) {
    const errLower = error.toLowerCase();

    // API 错误
    if (errLower.includes('402') || errLower.includes('429') ||
        errLower.includes('500') || errLower.includes('502') ||
        errLower.includes('503') || errLower.includes('rate limit') ||
        errLower.includes('insufficient') || errLower.includes('quota')) {
      return {
        errorType: ErrorType.API_ERROR,
        detail: `API 错误: ${error.slice(0, 200)}`,
        strategy: RETRY_STRATEGY[ErrorType.API_ERROR]
      };
    }

    // 超时
    if (errLower.includes('timeout') || errLower.includes('timed out') ||
        status === 'timeout') {
      // 区分正常超时和 QPS 限流引起的快速超时（<30s）
      if (agentResult.actualRuntimeMs && agentResult.actualRuntimeMs < 30000) {
        return {
          errorType: ErrorType.QPS_RATE_LIMIT,
          detail: `QPS 限流：子代理在 ${agentResult.actualRuntimeMs}ms 内非正常退出（模型：${agentResult.model}）`,
          strategy: RETRY_STRATEGY[ErrorType.QPS_RATE_LIMIT]
        };
      }
      return {
        errorType: ErrorType.TIMEOUT,
        detail: `执行超时`,
        strategy: RETRY_STRATEGY[ErrorType.TIMEOUT]
      };
    }

    // 崩溃
    if (errLower.includes('crash') || errLower.includes('fatal') ||
        errLower.includes('exception') || errLower.includes('error')) {
      return {
        errorType: ErrorType.CRASH,
        detail: `子代理异常: ${error.slice(0, 200)}`,
        strategy: RETRY_STRATEGY[ErrorType.CRASH]
      };
    }
  }

  // 2. 状态检查
  if (status === 'timeout') {
    return {
      errorType: ErrorType.TIMEOUT,
      detail: '子代理超时退出',
      strategy: RETRY_STRATEGY[ErrorType.TIMEOUT]
    };
  }

  // 3. 检查文件是否存在
  if (outputFile && !fs.existsSync(outputFile)) {
    if (tokensUsed && tokensUsed > 0) {
      return {
        errorType: ErrorType.FILE_MISSING,
        detail: `子代理消耗了 ${tokensUsed} tokens 但未写入输出文件`,
        strategy: RETRY_STRATEGY[ErrorType.FILE_MISSING]
      };
    }
    return {
      errorType: ErrorType.EMPTY_OUTPUT,
      detail: '子代理未产生任何输出（0 tokens，文件缺失）',
      strategy: RETRY_STRATEGY[ErrorType.EMPTY_OUTPUT]
    };
  }

  // 4. 空输出（无 token 消耗）
  if (!tokensUsed || tokensUsed === 0) {
    return {
      errorType: ErrorType.EMPTY_OUTPUT,
      detail: '子代理未产生任何输出（0 tokens）',
      strategy: RETRY_STRATEGY[ErrorType.EMPTY_OUTPUT]
    };
  }

  // 5. 未知错误
  return {
    errorType: ErrorType.UNKNOWN,
    detail: '无法归类的失败原因',
    strategy: { maxRetries: 1, timeoutMultiplier: 1.5, switchModel: false, description: '未知错误：保守重试' }
  };
}

/**
 * 根据诊断结果生成重试的 spawn 参数
 *
 * @param {object} originalSpawn - 原始 spawn 参数
 * @param {object} diagnosis - diagnoseFailure 的返回结果
 * @param {number} retryCount - 当前重试次数（从 0 开始）
 * @returns {object|null} 新的 spawn 参数，或 null 表示不应重试
 */
export function buildRetrySpawn(originalSpawn, diagnosis, retryCount = 0) {
  const { strategy } = diagnosis;

  // 检查重试次数限制
  if (retryCount >= strategy.maxRetries) {
    return null;  // 超过最大重试次数，放弃
  }

  const retrySpawn = { ...originalSpawn };

  // 调整超时
  if (strategy.timeoutMultiplier !== 1.0) {
    retrySpawn.timeoutSeconds = Math.ceil(originalSpawn.timeoutSeconds * strategy.timeoutMultiplier);
  }

  // 换模型
  if (strategy.switchModel) {
    const meta = originalSpawn._meta || {};
    const newModel = selectModel(meta.agentRole || 'unknown', {
      complexity: meta.complexity || 'medium',
      excludedModels: [originalSpawn.model],
      allowFree: true
    });
    retrySpawn.model = newModel.model;
    retrySpawn.thinking = newModel.thinking;

    // 更新元数据
    retrySpawn._meta = {
      ...meta,
      modelReason: `重试#${retryCount + 1}: 换模型 ${originalSpawn.model} → ${newModel.model}`,
      retryCount: retryCount + 1
    };
  } else {
    retrySpawn._meta = {
      ...(originalSpawn._meta || {}),
      modelReason: `重试#${retryCount + 1}: 同模型 ${originalSpawn.model}, 超时 ${originalSpawn.timeoutSeconds}s → ${retrySpawn.timeoutSeconds}s`,
      retryCount: retryCount + 1
    };
  }

  // 更新 label（避免冲突）
  retrySpawn.label = `${originalSpawn.label}-retry${retryCount + 1}`;

  return retrySpawn;
}

/**
 * 评估整体降级级别
 *
 * @param {object} results - { agentName: { status, outputFile, ... } }
 * @returns {object} { level, successRate, failedAgents, recommendation }
 */
export function assessDegradation(results) {
  const total = Object.keys(results).length;
  if (total === 0) {
    return { level: DegradationLevel.HEAVY, successRate: 0, failedAgents: [], recommendation: '无代理结果，主代理全面接管' };
  }

  const succeeded = [];
  const failed = [];

  for (const [name, result] of Object.entries(results)) {
    const exists = result.outputFile && fs.existsSync(result.outputFile);
    if (exists || result.status === 'completed') {
      succeeded.push(name);
    } else {
      failed.push(name);
    }
  }

  const successRate = succeeded.length / total;

  let level, recommendation;
  if (successRate >= 1.0) {
    level = DegradationLevel.NONE;
    recommendation = '全部成功，进入 Critic 审核阶段';
  } else if (successRate >= 0.6) {
    level = DegradationLevel.LIGHT;
    recommendation = `${failed.join(', ')} 缺失，主代理补做缺失分支`;
  } else if (successRate >= 0.3) {
    level = DegradationLevel.MODERATE;
    recommendation = `成功率仅 ${Math.round(successRate * 100)}%，对缺失代理重试（超时 × 1.5）`;
  } else {
    level = DegradationLevel.HEAVY;
    recommendation = `成功率仅 ${Math.round(successRate * 100)}%，放弃多代理模式，主代理全面接管`;
  }

  return { level, successRate, failedAgents: failed, succeededAgents: succeeded, recommendation };
}

/**
 * 生成降级执行方案
 *
 * @param {object} degradation - assessDegradation 返回结果
 * @param {object} originalSpawns - 原始 spawn 参数映射
 * @returns {object} { action, spawns?, instruction? }
 */
export function buildDegradationPlan(degradation, originalSpawns) {
  const { level, failedAgents } = degradation;

  switch (level) {
    case DegradationLevel.NONE:
      return { action: 'proceed', instruction: '所有代理成功完成，进入下一阶段' };

    case DegradationLevel.LIGHT:
      return {
        action: 'fill_missing',
        instruction: `主代理自行补做以下缺失分支：${failedAgents.join(', ')}`,
        missingAgents: failedAgents
      };

    case DegradationLevel.MODERATE: {
      // 对缺失代理构建重试 spawn
      const retrySpawns = [];
      for (const agentName of failedAgents) {
        const original = originalSpawns.find(s => s.label?.includes(agentName));
        if (original) {
          const diagnosis = diagnoseFailure({ outputFile: null, tokensUsed: 0, error: 'file_missing', status: 'failed' });
          const retry = buildRetrySpawn(original, diagnosis, 0);
          if (retry) retrySpawns.push(retry);
        }
      }
      return {
        action: 'retry',
        spawns: retrySpawns,
        instruction: `重试 ${failedAgents.join(', ')}（超时 × 1.5）`
      };
    }

    case DegradationLevel.HEAVY:
      return {
        action: 'full_fallback',
        instruction: `因多代理执行失败，由主代理独立完成所有研究。缺失代理：${failedAgents.join(', ')}`
      };

    default:
      return { action: 'proceed', instruction: '未知降级级别，继续执行' };
  }
}

export { RETRY_STRATEGY };
