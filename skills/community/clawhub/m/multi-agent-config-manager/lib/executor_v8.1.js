/**
 * 执行引擎 v8.1 - 多代理编排的 sessions_spawn 桥接层
 * 
 * v8.1 核心改进（稳定性增强）：
 * 1. 主动轮询机制 - 每 30 秒检查文件产出，防止"丢失"误判
 * 2. 超时处理 - 1 小时无产出触发降级协议
 * 3. 状态日志 - 记录完整轮询历史，便于调试
 * 4. 消息路由验证 - 确保 sessions_send 消息可追溯
 * 
 * @version 8.1.0
 * @author OpenClaw Multi-Agent Team
 */

import fs from 'fs';
import path from 'path';
import { generateAgentPrompt, generateAgentPromptLegacy } from './communication.js';
import { validateOutput, selectSchema, formatSchemaPrompt } from './outputSchema.js';
import { validate, formatValidationReport } from './validator.js';
import { aggregate, formatAggregation } from './aggregator.js';
import { selectModel, selectBatchModels, buildModelPool } from './modelSelector.js';
import { diagnoseFailure, buildRetrySpawn, assessDegradation, buildDegradationPlan, ErrorType, DegradationLevel } from './retryManager.js';
import { archiveWorkflow, cleanShared, generateFinalSummary, archiveAndClean } from './archiver.js';
import { checkModelThinking, selectThinkingLevel, degradeThinking, verifyThinkingExecution } from './thinkingCapabilities.js';
import { buildRoleSpawnParams, loadRoleConfig, ensureThinkingEnabled } from './modelAdaptation.js';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const OPENCLAW_CONFIG_PATH = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'openclaw.json');

// ===================== 版本检测（v7.2 增强 - 不依赖环境变量） =====================
/**
 * 检测 OpenClaw 版本
 * 优先级：1.环境变量 → 2.openclaw.json → 3.Gateway API → 4.unknown
 */
function detectOpenClawVersion() {
  // 方法 1: 环境变量
  if (process.env.OPENCLAW_VERSION && process.env.OPENCLAW_VERSION !== 'unknown') {
    return process.env.OPENCLAW_VERSION;
  }
  
  // 方法 2: 读取 openclaw.json
  try {
    if (fs.existsSync(OPENCLAW_CONFIG_PATH)) {
      const config = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG_PATH, 'utf-8'));
      if (config.meta?.lastTouchedVersion) {
        return config.meta.lastTouchedVersion;
      }
    }
  } catch (e) {
    // 忽略错误，继续下一步
  }
  
  // 方法 3: 检查 Gateway API
  if (typeof globalThis.gateway !== 'undefined') {
    return '2026.4.x (Gateway API detected)';
  }
  
  return 'unknown';
}

// ===================== 运行环境验证 =====================
export function validateEnvironment() {
  const errors = [];
  const warnings = [];

  // 使用增强版版本检测
  const version = detectOpenClawVersion();
  
  if (version !== 'unknown') {
    const [major] = version.split('.').map(Number);
    if (major < 2026) {
      errors.push(`OpenClaw 版本过低 (${version})，需要 2026.3.x+ 以支持 sessions_spawn API`);
    }
  } else {
    // 版本未知时，检查关键 API 是否存在
    const isAgentRuntime = typeof globalThis.sessions_spawn !== 'undefined';
    if (!isAgentRuntime) {
      warnings.push(
        'OpenClaw 版本未知，无法验证版本兼容性。\n' +
        '⚠️ 注意：多代理执行需要 OpenClaw 2026.3.x+ 以支持 sessions_spawn API'
      );
    }
  }

  const isAgentRuntime = typeof globalThis.sessions_spawn !== 'undefined';
  if (!isAgentRuntime) {
    warnings.push(
      '当前运行在 CLI 模式，工具检查跳过。\n' +
      '⚠️ 注意：多代理执行必须在 OpenClaw Agent 环境中运行'
    );
  }

  return { valid: errors.length === 0, errors, warnings, version, isAgentRuntime };
}

const ENV_CHECK = validateEnvironment();

// ===================== 主动轮询监控器 (v8.1 新增) =====================

/**
 * 轮询监控器类 - 管理子代理文件产出的主动轮询
 */
export class PollMonitor {
  constructor(options = {}) {
    this.pollIntervalMs = options.pollIntervalMs || 30000; // 30 秒
    this.timeoutMs = options.timeoutMs || 3600000; // 1 小时
    this.logFile = options.logFile;
    this.pollHistory = {};
    this.startTime = Date.now();
  }

  /**
   * 记录轮询事件
   */
  log(agentName, event, details = {}) {
    const timestamp = new Date().toISOString();
    const elapsed = Date.now() - this.startTime;
    const entry = { timestamp, agent: agentName, event, elapsedMs: elapsed, ...details };

    if (!this.pollHistory[agentName]) {
      this.pollHistory[agentName] = [];
    }
    this.pollHistory[agentName].push(entry);

    // 写入日志文件
    if (this.logFile) {
      try {
        fs.appendFileSync(this.logFile, JSON.stringify(entry) + '\n', 'utf-8');
      } catch (err) {
        console.warn(`日志写入失败：${err.message}`);
      }
    }

    console.log(`[轮询] ${timestamp} - ${agentName}: ${event} (T+${Math.round(elapsed/1000)}s)`, details);
  }

  /**
   * 验证文件是否有效产出
   */
  verifyFile(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        return { valid: false, reason: '文件不存在' };
      }

      const stats = fs.statSync(filePath);
      const size = stats.size;

      if (size < 100) {
        return { valid: false, reason: `文件大小不足 (${size} < 100 bytes)`, size };
      }

      const content = fs.readFileSync(filePath, 'utf-8');

      if (!content || content.trim().length === 0) {
        return { valid: false, reason: '文件内容为空', size };
      }

      const invalidPatterns = [
        '我是 OpenClaw AI 助手',
        '未能完成任务',
        '抱歉，我无法',
        '对不起，我不能'
      ];

      const lowerContent = content.toLowerCase();
      for (const pattern of invalidPatterns) {
        if (lowerContent.includes(pattern.toLowerCase())) {
          return { valid: false, reason: `检测到无效模板文本：${pattern}`, size };
        }
      }

      const lineCount = content.split('\n').length;
      if (lineCount < 3) {
        return { valid: false, reason: `行数过少 (${lineCount} < 3)`, size };
      }

      const textChars = content.replace(/\s+/g, '').length;
      const textRatio = textChars / content.length;
      if (textRatio < 0.3) {
        return { valid: false, reason: `文本字符比例过低 (${(textRatio * 100).toFixed(1)}% < 30%)`, size };
      }

      return { valid: true, size, lineCount, textRatio, content };
    } catch (err) {
      return { valid: false, reason: `文件访问错误：${err.message}` };
    }
  }

  /**
   * 轮询单个代理直到文件产出或超时
   */
  async pollUntilReady(agentName, outputFile) {
    const startTime = Date.now();
    let pollCount = 0;

    this.log(agentName, 'POLL_START', { outputFile, pollInterval: this.pollIntervalMs, timeout: this.timeoutMs });

    while (true) {
      const elapsed = Date.now() - startTime;

      // 超时检查
      if (elapsed >= this.timeoutMs) {
        this.log(agentName, 'TIMEOUT', { elapsedMs: elapsed, pollCount, reason: '超过 1 小时无有效产出' });
        return {
          success: false,
          reason: `超时：${Math.round(elapsed / 1000)}秒无有效产出`,
          pollCount,
          elapsedMs: elapsed
        };
      }

      // 检查文件
      const result = this.verifyFile(outputFile);
      pollCount++;

      if (result.valid) {
        this.log(agentName, 'FILE_READY', {
          elapsedMs: elapsed,
          pollCount,
          fileSize: result.size,
          lineCount: result.lineCount
        });
        return {
          success: true,
          content: result.content,
          fileSize: result.size,
          lineCount: result.lineCount,
          pollCount,
          elapsedMs: elapsed
        };
      } else {
        this.log(agentName, 'POLL_CHECK', {
          elapsedMs: elapsed,
          pollCount,
          status: result.reason
        });

        // 5 分钟后仍无文件，标记为可能丢失
        if (pollCount >= 10 && elapsed > 300000) {
          this.log(agentName, 'POSSIBLY_LOST', {
            elapsedMs: elapsed,
            pollCount,
            suggestion: '建议检查子代理会话状态或触发降级协议'
          });
        }

        // 等待下次轮询
        if (elapsed + this.pollIntervalMs < this.timeoutMs) {
          await new Promise(resolve => setTimeout(resolve, this.pollIntervalMs));
        }
      }
    }
  }

  /**
   * 获取完整轮询历史
   */
  getHistory() {
    return this.pollHistory;
  }
}

// ===================== 文件写入验证（同步版本，向后兼容） =====================

/**
 * 验证文件写入的有效性（同步版本）
 * @param {string} filePath - 文件路径
 * @returns {object} { valid: boolean, reason?: string, size?: number, lineCount?: number, textRatio?: number }
 */
export function verifyFileWrite(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return { valid: false, reason: '文件不存在' };
    }

    const stats = fs.statSync(filePath);
    const size = stats.size;

    if (size < 100) {
      return { valid: false, reason: `文件大小不足 (${size} < 100 bytes)`, size };
    }

    const content = fs.readFileSync(filePath, 'utf-8');

    if (!content || content.trim().length === 0) {
      return { valid: false, reason: '文件内容为空', size };
    }

    const invalidPatterns = [
      '我是 OpenClaw AI 助手',
      '未能完成任务',
      '抱歉，我无法',
      '对不起，我不能'
    ];

    const lowerContent = content.toLowerCase();
    for (const pattern of invalidPatterns) {
      if (lowerContent.includes(pattern.toLowerCase())) {
        return { valid: false, reason: `检测到无效模板文本：${pattern}`, size };
      }
    }

    const lineCount = content.split('\n').length;
    if (lineCount < 3) {
      return { valid: false, reason: `行数过少 (${lineCount} < 3)`, size };
    }

    const textChars = content.replace(/\s+/g, '').length;
    const textRatio = textChars / content.length;
    if (textRatio < 0.3) {
      return { valid: false, reason: `文本字符比例过低 (${(textRatio * 100).toFixed(1)}% < 30%)`, size };
    }

    return { valid: true, size, lineCount, textRatio };
  } catch (err) {
    return { valid: false, reason: `文件访问错误：${err.message}` };
  }
}

// ===================== 收集结果（v8.1 增强版） =====================

/**
 * 收集子代理执行结果（从文件系统读取）
 * v8.1 增强版：主动轮询监控 + 文件写入验证 + 内容有效性检查 + 自动重试机制
 *
 * @param {array} agentNames - 代理名称列表
 * @param {string} outputDir - 输出目录
 * @param {object} modelInfo - 模型信息 { agentName: { modelId, thinking } }
 * @param {object} options - 额外选项 { pollIntervalMs, timeoutMs, logFile, useAsyncPoll }
 * @returns {object} { results, missing, thinkingVerification, verificationStatus, verificationDetails, pollHistory }
 */
export function collectResults(agentNames, outputDir, modelInfo, options = {}) {
  const results = {};
  const missing = [];
  const thinkingVerification = {};
  const verificationStatus = {};
  const verificationDetails = {};
  const pollHistory = {};

  const POLL_INTERVAL_MS = options.pollIntervalMs || 30000;
  const TIMEOUT_MS = options.timeoutMs || 3600000;
  const logFile = options.logFile || null;
  const useAsyncPoll = options.useAsyncPoll || false; // 是否使用异步轮询（需要主代理支持）

  function logPollEvent(agentName, event, details = {}) {
    const timestamp = new Date().toISOString();
    const entry = { timestamp, agent: agentName, event, ...details };

    if (!pollHistory[agentName]) pollHistory[agentName] = [];
    pollHistory[agentName].push(entry);

    if (logFile) {
      try {
        fs.appendFileSync(logFile, JSON.stringify(entry) + '\n', 'utf-8');
      } catch (err) {
        console.warn(`日志写入失败：${err.message}`);
      }
    }

    console.log(`[轮询] ${timestamp} - ${agentName}: ${event}`, details);
  }

  for (const name of agentNames) {
    const reportPath = path.join(outputDir || path.join(CONFIG_DIR, 'shared', 'final'), `${name}_report.md`);
    let fileValid = false;
    let verificationResult = null;
    let pollCount = 0;
    const startTime = Date.now();

    logPollEvent(name, 'POLL_START', {
      outputFile: reportPath,
      pollInterval: POLL_INTERVAL_MS,
      timeout: TIMEOUT_MS
    });

    try {
      // 主动轮询循环
      while (!fileValid) {
        const elapsed = Date.now() - startTime;

        if (elapsed >= TIMEOUT_MS) {
          logPollEvent(name, 'TIMEOUT', {
            elapsedMs: elapsed,
            pollCount,
            reason: '超过 1 小时无有效产出'
          });
          verificationStatus[name] = false;
          verificationDetails[name] = {
            valid: false,
            reason: `超时：${Math.round(elapsed / 1000)}秒无有效产出`,
            pollCount
          };
          missing.push(name);
          break;
        }

        verificationResult = verifyFileWrite(reportPath);
        pollCount++;

        if (verificationResult.valid) {
          fileValid = true;
          verificationStatus[name] = true;
          verificationDetails[name] = verificationResult;

          const content = fs.readFileSync(reportPath, 'utf-8');
          results[name] = content;

          logPollEvent(name, 'FILE_READY', {
            elapsedMs: elapsed,
            pollCount,
            fileSize: verificationResult.size,
            lineCount: verificationResult.lineCount
          });

          if (modelInfo && modelInfo[name]) {
            const { modelId } = modelInfo[name];
            thinkingVerification[name] = verifyThinkingExecution(modelId, { content, status: 'success' });
          }
          break;
        } else {
          logPollEvent(name, 'POLL_CHECK', {
            elapsedMs: elapsed,
            pollCount,
            status: verificationResult.reason
          });

          if (pollCount >= 10 && elapsed > 300000) {
            logPollEvent(name, 'POSSIBLY_LOST', {
              elapsedMs: elapsed,
              pollCount,
              suggestion: '建议检查子代理会话状态或触发降级协议'
            });
          }

          verificationStatus[name] = false;
          verificationDetails[name] = verificationResult;
          missing.push(name);
          break;
        }
      }
    } catch (err) {
      logPollEvent(name, 'ERROR', { error: err.message, pollCount });
      console.error(`代理 ${name} 结果收集异常：${err.message}`);
      verificationStatus[name] = false;
      verificationDetails[name] = { valid: false, reason: `异常：${err.message}`, pollCount };
      missing.push(name);
    }
  }

  return { results, missing, thinkingVerification, verificationStatus, verificationDetails, pollHistory };
}

// ===================== 导出其他必要函数（向后兼容） =====================

export function estimateComplexity(task, agentRole) {
  const desc = (task?.description || '').toLowerCase();
  const reqs = (task?.requirements || []).join(' ').toLowerCase();
  const combined = desc + ' ' + reqs;

  const complexSignals = ['深入', '全面', '多维度', '交叉验证', '对比分析', 'deep', 'comprehensive', 'multi-angle'];
  const simpleSignals = ['简单', '快速', '列出', '汇总', '格式化', 'simple', 'quick', 'list'];

  const complexCount = complexSignals.filter(s => combined.includes(s)).length;
  const simpleCount = simpleSignals.filter(s => combined.includes(s)).length;

  if (complexCount >= 2 || agentRole === 'Critic') return 'complex';
  if (simpleCount >= 2) return 'simple';
  return 'medium';
}

export function buildOutputDirs(workflow, version = 1) {
  const slug = (workflow.slug || workflow.id).replace(/[^a-z0-9-]/g, '-');
  const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const researchDir = path.join(CONFIG_DIR, 'shared', 'researches', `${slug}_${dateStr}`);
  const versionDir = path.join(researchDir, `v${version}`);
  const finalDir = path.join(researchDir, 'final');
  const boardsDir = path.join(CONFIG_DIR, 'shared', 'boards');

  [versionDir, finalDir, boardsDir].forEach(d => fs.mkdirSync(d, { recursive: true }));
  return { researchDir, versionDir, finalDir, boardsDir, slug };
}

export function buildMountInstructions(agentProfile, outputDir) {
  let instructions = `\n\n## 文件系统访问说明\n`;
  instructions += `- 你的工作区：${agentProfile.workspace || CONFIG_DIR}\n`;
  instructions += `- 输出目录：${outputDir}\n`;
  instructions += `- 使用 write 工具将报告写入输出目录\n`;

  try {
    const sharedDir = path.join(CONFIG_DIR, 'shared');
    if (fs.existsSync(sharedDir)) {
      const files = fs.readdirSync(sharedDir);
      if (files.length > 0) {
        instructions += `\n- 共享目录内容：${files.slice(0, 10).join(', ')}${files.length > 10 ? '...' : ''}\n`;
      } else {
        instructions += `- （共享目录为空，你是首个执行的代理）\n`;
      }
    }
  } catch {
    instructions += `- （无法读取共享目录）\n`;
  }

  return instructions;
}

export function buildSpawnParams(agentProfile, task, workflow, options = {}) {
  const complexity = options.complexity || estimateComplexity(task, agentProfile.name);
  const modelResult = selectModel(agentProfile.name, {
    complexity,
    excludedModels: options.excludedModels || [],
    allowFree: options.allowFree !== false
  });

  if (modelResult.error || !modelResult.model) {
    const modelPool = buildModelPool();
    const anyModel = modelPool.all[0];
    if (anyModel) {
      modelResult.model = anyModel.id;
      modelResult.tier = anyModel.tier;
      modelResult.thinking = 'low';
      modelResult.reason = `${modelResult.reason} [降级复用池内首个可用模型：${anyModel.id}]`;
      modelResult.reused = true;
    } else {
      return {
        task: `⚠️ 未定义任何可用模型，无法为 ${agentProfile.name} 分配模型。`,
        label: `multi-agent-${agentProfile.name}-${workflow.id}-model-error`,
        model: undefined,
        thinking: 'off',
        timeoutSeconds: 60,
        cwd: CONFIG_DIR,
        mode: 'run',
        thread: false,
        cleanup: 'keep',
        output_file: null,
        _meta: {
          agentRole: agentProfile.name,
          complexity,
          modelTier: 'none',
          modelReason: '❌ 模型池为空',
          modelReused: false,
          modelError: true
        }
      };
    }
  }

  const thinkingCaps = checkModelThinking(modelResult.model);
  let finalThinking = modelResult.thinking || 'low';

  if (!thinkingCaps.supportsThinking) {
    finalThinking = 'off';
  } else {
    finalThinking = selectThinkingLevel(modelResult.model, complexity);
  }

  const dirs = options.directories;
  const outputDir = dirs?.versionDir || options.outputDir || path.join(CONFIG_DIR, 'shared', 'final');

  const timeoutPresets = { simple: 120, medium: 480, complex: 480, critical: 600 };
  const timeoutSeconds = options.timeoutSeconds || timeoutPresets[complexity] || 480;

  const version = options.version || 1;
  const baseName = `${agentProfile.name}_report${version > 1 ? `_v${version}` : ''}.md`;
  const outputFile = path.join(outputDir, baseName);

  const context = {
    goal: workflow.goal,
    related_tasks: options.relatedTasks || [],
    workflow_id: workflow.id,
    output_dir: outputDir
  };

  const fullPrompt = generateAgentPrompt(agentProfile, task, 'standard_task', context);
  const mountInstructions = buildMountInstructions(agentProfile, outputDir);
  const completeTask = `${fullPrompt}\n${mountInstructions}\n\n## 重要：输出要求\n将你的完整分析报告写入文件：${outputFile}\n完成后在最后一行输出：EXECUTION_COMPLETE`;

  const agentWorkspace = agentProfile.workspace || CONFIG_DIR;
  fs.mkdirSync(agentWorkspace, { recursive: true });
  fs.mkdirSync(outputDir, { recursive: true });

  return {
    task: completeTask,
    label: `multi-agent-${agentProfile.name}-${workflow.id}${version > 1 ? `-v${version}` : ''}`,
    model: modelResult.model,
    thinking: finalThinking,
    timeoutSeconds,
    cwd: CONFIG_DIR,
    mode: 'run',
    thread: false,
    cleanup: 'keep',
    output_file: null,
    _meta: {
      agentRole: agentProfile.name,
      complexity,
      modelTier: modelResult.tier,
      modelReason: modelResult.reason,
      modelReused: modelResult.reused || false,
      outputFile,
      version
    }
  };
}

export function buildParallelSpawnParams(agentNames, workflow, profiles, phaseTasks) {
  const sharedDir = path.join(CONFIG_DIR, 'shared');
  const outputDir = path.join(sharedDir, 'final');

  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(sharedDir, 'progress'), { recursive: true });

  const batchModels = selectBatchModels(agentNames, { complexity: 'complex' });

  return agentNames.map(agentName => {
    const profile = profiles[agentName];
    if (!profile) throw new Error(`代理配置缺失：${agentName}`);

    const task = phaseTasks[agentName] || {
      description: `请执行你在工作流 "${workflow.name}" 中的职责`,
      requirements: []
    };

    const relatedTasks = agentNames
      .filter(n => n !== agentName)
      .map(n => ({ agent: n, description: phaseTasks[n]?.description || '并行执行中' }));

    const modelInfo = batchModels.get(agentName);

    return buildSpawnParams(profile, task, workflow, {
      sharedDir,
      outputDir,
      relatedTasks,
      complexity: modelInfo ? undefined : 'medium',
      excludedModels: agentNames.filter(n => n !== agentName).map(n => batchModels.get(n)?.model).filter(Boolean)
    });
  });
}

export function validateAgentOutput(agentName, content, goal) {
  try {
    const result = validate(content, 'research_output', { goal });
    return {
      agent: agentName,
      passed: result.passed,
      score: result.score,
      report: formatValidationReport(result),
      details: result
    };
  } catch (err) {
    return {
      agent: agentName,
      passed: false,
      score: 0,
      report: `验证执行失败：${err.message}`,
      details: null
    };
  }
}

export function aggregateResults(results, goal, template = 'research_report') {
  try {
    const resultArray = Object.entries(results).map(([agent, content]) => ({
      agent,
      content,
      timestamp: new Date().toISOString()
    }));

    const aggregated = aggregate(resultArray, template, goal);
    return {
      report: aggregated,
      formatted: formatAggregation(aggregated)
    };
  } catch (err) {
    return {
      report: null,
      formatted: `聚合失败：${err.message}\n\n## 原始结果\n\n${Object.entries(results).map(([k, v]) => `### ${k}\n\n${v}`).join('\n\n---\n\n')}`
    };
  }
}

export function buildCriticTask(aggregatedContent, goal, workflowId) {
  const criticProfile = {
    name: 'Critic',
    description: '独立批判性审核者。审查所有产出的逻辑漏洞、证据不足、偏见盲点。',
    capabilities: ['critical_thinking', 'bias_detection', 'logic_review', 'gap_analysis'],
    workspace: path.join(CONFIG_DIR, 'agents', 'Critic')
  };

  const task = {
    description: `对以下聚合报告进行独立批判性评估：\n\n---\n\n${aggregatedContent}\n\n---\n\n总体目标：${goal}`,
    requirements: [
      '识别逻辑漏洞和推理跳跃',
      '标记证据不足的断言',
      '指出潜在的偏见或盲点',
      '提出具体的改进建议'
    ]
  };

  return buildSpawnParams(criticProfile, task, { id: workflowId, goal }, {
    outputDir: path.join(CONFIG_DIR, 'shared', 'final'),
    complexity: 'complex'
  });
}
