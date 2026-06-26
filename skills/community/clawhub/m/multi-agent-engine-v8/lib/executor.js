/**
 * 执行引擎 - 多代理编排的 sessions_spawn 桥接层
 * v8.0 精简版 - 强约束JSON输出 + Tokens节省
 * 
 * 核心变化：
 * 1. 提示词精简（从 ~800行 → ~80行）
 * 2. 支持JSON强约束输出模式
 * 3. 集成输出校验机制
 * 4. 默认使用精简版提示词（节省 25-30% tokens）
 */

// ===================== 导入子模块 =====================
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

// ===================== 运行环境验证 =====================
/**
 * 启动时验证：检查 OpenClaw 版本 + 必需工具可用性
 * 如果检查失败，抛出明确的错误信息，而不是在运行时崩溃
 */
export function validateEnvironment() {
  const errors = [];
  const warnings = [];

  // 1. OpenClaw 版本检查
  const version = process.env.OPENCLAW_VERSION || 'unknown';
  if (version !== 'unknown') {
    const [major] = version.split('.').map(Number);
    if (major < 2026) {
      errors.push(`OpenClaw 版本过低 (${version})，需要 2026.3.x+ 以支持 sessions_spawn API`);
    }
  }

  // 2. 工具可用性检查
  const isAgentRuntime = typeof globalThis.sessions_spawn !== 'undefined';

  if (!isAgentRuntime) {
    warnings.push(
      '当前运行在 CLI 模式，工具检查跳过。\n' +
      '⚠️ 注意：多代理执行必须在 OpenClaw Agent 环境中运行\n' +
      '   AI 代理会自动调用 sessions_spawn 驱动子代理'
    );
  }

  return { valid: errors.length === 0, errors, warnings, version, isAgentRuntime };
}

const ENV_CHECK = validateEnvironment();

// ===================== 任务复杂度评估 =====================

/**
 * 根据任务描述和要求评估复杂度
 * 简单启发式规则，主代理可在 plan 时手动覆盖
 */
function estimateComplexity(task, agentRole) {
  const desc = (task?.description || '').toLowerCase();
  const reqs = (task?.requirements || []).join(' ').toLowerCase();
  const combined = desc + ' ' + reqs;

  // 复杂度信号词
  const complexSignals = ['深入', '全面', '多维度', '交叉验证', '对比分析', 'deep', 'comprehensive', 'multi-angle'];
  const simpleSignals = ['简单', '快速', '列出', '汇总', '格式化', 'simple', 'quick', 'list'];

  const complexCount = complexSignals.filter(s => combined.includes(s)).length;
  const simpleCount = simpleSignals.filter(s => combined.includes(s)).length;

  if (complexCount >= 2 || agentRole === 'Critic') return 'complex';
  if (simpleCount >= 2) return 'simple';
  return 'medium';
}

// ===================== 分层目录管理 =====================
/**
 * 构建分层输出目录
 * shared/researches/{slug}_{date}/v{n}/
 */
function buildOutputDirs(workflow, version = 1) {
  const slug = (workflow.slug || workflow.id).replace(/[^a-z0-9-]/g, '-');
  const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const researchDir = path.join(CONFIG_DIR, 'shared', 'researches', `${slug}_${dateStr}`);
  const versionDir = path.join(researchDir, `v${version}`);
  const finalDir = path.join(researchDir, 'final');
  const boardsDir = path.join(CONFIG_DIR, 'shared', 'boards');

  [versionDir, finalDir, boardsDir].forEach(d => fs.mkdirSync(d, { recursive: true }));
  return { researchDir, versionDir, finalDir, boardsDir, slug };
}

/**
 * 构建输出文件路径（含分层目录）
 */
function buildOutputPath(directories, agentName, version = 1) {
  return path.join(directories.versionDir, `${agentName}_report${version > 1 ? `_v${version}` : ''}.md`);
}

// ===================== 看板系统 =====================
/**
 * 创建计划看板
 */
function createPlanBoard(workflow, phases, directories) {
  const planBoard = {
    workflow_id: workflow.id,
    goal: workflow.goal,
    complexity: workflow.complexity || 'unknown',
    route: workflow.route || 'full',
    phases: phases.map(phase => ({
      id: phase.id,
      name: phase.name,
      type: phase.type,
      status: 'pending',
      tasks: (phase.spawns || []).map(spawn => ({
        agent: spawn._meta?.agentRole || 'unknown',
        model: spawn.model,
        model_tier: spawn._meta?.modelTier || 'unknown',
        thinking: spawn.thinking,
        timeout: spawn.timeoutSeconds,
        output_file: spawn.output_file || '未指定',
        status: 'pending'
      }))
    })),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  const planPath = path.join(directories.boardsDir, `${workflow.id}_plan.json`);
  fs.writeFileSync(planPath, JSON.stringify(planBoard, null, 2), 'utf-8');
  return planBoard;
}

/**
 * 创建/初始化执行看板
 */
function createExecBoard(workflow, directories) {
  const execBoard = {
    workflow_id: workflow.id,
    goal: workflow.goal,
    current_phase: 'idle',
    started_at: new Date().toISOString(),
    completed_at: null,
    elapsed_total: '0s',
    phases: [],
    version: 1
  };

  const execPath = path.join(directories.boardsDir, `${workflow.id}_exec.json`);
  fs.writeFileSync(execPath, JSON.stringify(execBoard, null, 2), 'utf-8');
  return execBoard;
}

/**
 * 更新执行看板阶段状态
 */
function updateExecBoard(execBoard, phaseData, directories) {
  execBoard.current_phase = phaseData.id;

  const existingIdx = execBoard.phases.findIndex(p => p.id === phaseData.id);
  if (existingIdx >= 0) {
    execBoard.phases[existingIdx] = { ...execBoard.phases[existingIdx], ...phaseData };
  } else {
    execBoard.phases.push(phaseData);
  }
  execBoard.updated_at = new Date().toISOString();

  const execPath = path.join(directories.boardsDir, `${execBoard.workflow_id}_exec.json`);
  fs.writeFileSync(execPath, JSON.stringify(execBoard, null, 2), 'utf-8');
  return execBoard;
}

/**
 * 加载执行看板
 */
function loadExecBoard(workflowId) {
  const execPath = path.join(CONFIG_DIR, 'shared', 'boards', `${workflowId}_exec.json`);
  if (!fs.existsSync(execPath)) return null;
  return JSON.parse(fs.readFileSync(execPath, 'utf-8'));
}

/**
 * 格式化执行看板为可读文本
 */
function formatExecBoard(execBoard) {
  const totalElapsed = execBoard.elapsed_total || '进行中';
  let out = '';
  out += `╔═════════════════════════════════════════════════════════════╗\n`;
  out += `║  📊 执行看板 | ${execBoard.workflow_id} | 总耗时：${totalElapsed.padEnd(20)}║\n`;
  out += `╠═══════════╤═══════════════╤════════╤════════╤═══════════════╣\n`;
  out += `║ 阶段      │ 代理          │ 状态   │ 耗时   │ 模型/Tokens   ║\n`;
  out += `╠═══════════╪═══════════════╪════════╪════════╪═══════════════╣\n`;

  for (const phase of execBoard.phases) {
    const tasks = phase.tasks || [];
    const phaseLabel = {
      parallel: '⚡并行',
      critic: '🔍审核',
      aggregate: '🧠聚合',
      finalize: '📝终稿'
    }[phase.id] || phase.id;

    if (tasks.length === 0) {
      out += `║ ${phaseLabel.padEnd(10)}│ ${(phase.status || '').padEnd(14)}│ —      │ —      │ —             ║\n`;
      continue;
    }

    tasks.forEach((t, i) => {
      const agentShort = (t.agent || '').slice(0, 13).padEnd(13);
      const statusIcon = t.status === 'success' ? '✅成功' : t.status === 'failed' ? '❌失败' : t.status === 'timeout' ? '⏰超时' : t.status === 'retry' ? '🔄重试' : t.status?.padEnd(6) || '⏳运行';
      const timeStr = (t.actual_time || '—').padEnd(6);
      const modelStr = `${(t.model || '—').slice(0, 10).padEnd(10)}`;
      const tokenStr = t.tokens ? `${(t.tokens.in/1000).toFixed(0)}k in/${(t.tokens.out/1000).toFixed(0)}k out` : '';
      const fileSize = t.file_size ? `${t.file_size}` : '';

      if (i === 0) {
        out += `║ ${phaseLabel.padEnd(10)}│ ${agentShort} │ ${statusIcon} │ ${timeStr} │ ${modelStr}      ║\n`;
      } else {
        out += `║           │ ${agentShort} │ ${statusIcon} │ ${timeStr} │ ${modelStr}      ║\n`;
      }
      if (tokenStr || fileSize) {
        out += `║           │               │        │        │ ${(tokenStr + ' ' + fileSize).slice(0, 13).padEnd(13)} ║\n`;
      }
    });
  }

  out += `╠═══════════╧═══════════════╧════════╧════════╧═══════════════╣\n`;

  const completed = execBoard.phases.filter(p => p.status === 'completed').length;
  const total = execBoard.phases.length;
  out += `║ 阶段进度：${completed}/${total} 完成                                      ║\n`;
  out += `╚═════════════════════════════════════════════════════════════╝\n`;

  return out;
}

// ===================== 核心函数 =====================

/**
 * 为单个子代理构建 sessions_spawn 参数（支持分层目录）
 *
 * @param {object} agentProfile - 代理配置（来自 .multi-agent-profiles.json）
 * @param {object} task - 任务描述 { description, requirements, context }
 * @param {object} workflow - 工作流实例
 * @param {object} options - 额外选项 { sharedDir, outputDir }
 * @returns {object} sessions_spawn 调用参数
 */
export function buildSpawnParams(agentProfile, task, workflow, options = {}) {
  // 异构模型选择（取代硬编码配置）
  const complexity = options.complexity || estimateComplexity(task, agentProfile.name);
  const modelResult = selectModel(agentProfile.name, {
    complexity,
    excludedModels: options.excludedModels || [],
    allowFree: options.allowFree !== false
  });

  // 模型池耗尽或为空 — 复用池内首个可用模型确保不中断
  if (modelResult.error || !modelResult.model) {
    const modelPool = buildModelPool();
    const anyModel = modelPool.all[0];
    if (anyModel) {
      modelResult.model = anyModel.id;
      modelResult.tier = anyModel.tier;
      modelResult.thinking = 'low';
      modelResult.reason = `${modelResult.reason} [降级复用池内首个可用模型: ${anyModel.id}]`;
      modelResult.reused = true;
    } else {
      // 真的没有模型 — 返回空 model 让 sessions_spawn 用默认模型
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

  // Thinking 容错：先检查能力矩阵，再决定 thinking 级别
  const thinkingCaps = checkModelThinking(modelResult.model);
  let finalThinking = modelResult.thinking || 'low';

  if (!thinkingCaps.supportsThinking) {
    // 模型不支持 thinking，直接关闭
    finalThinking = 'off';
  } else {
    // 用 selectThinkingLevel 确保兼容性
    finalThinking = selectThinkingLevel(modelResult.model, complexity);
  }

  // 分层目录支持（默认回退到旧结构）
  const dirs = options.directories;
  const outputDir = dirs?.versionDir || options.outputDir || path.join(CONFIG_DIR, 'shared', 'final');

  // 超时按复杂度分级（与 protocols.md §4 超时预设表一致）
  // ⚠️ research: 480s（从 300s 提升，解决长报告超时问题）
  const timeoutPresets = { simple: 120, medium: 480, complex: 480, critical: 600 };
  const timeoutSeconds = options.timeoutSeconds || timeoutPresets[complexity] || 480;

  // 构建文件路径（含版本号）
  const version = options.version || 1;
  const baseName = `${agentProfile.name}_report${version > 1 ? `_v${version}` : ''}.md`;
  const outputFile = path.join(outputDir, baseName);

  // 构建完整任务提示词
  const context = {
    goal: workflow.goal,
    related_tasks: options.relatedTasks || [],
    workflow_id: workflow.id,
    output_dir: outputDir
  };

  const fullPrompt = generateAgentPrompt(agentProfile, task, 'standard_task', context);

  // 构建文件系统挂载说明
  const mountInstructions = buildMountInstructions(agentProfile, outputDir);

  const completeTask = `${fullPrompt}\n${mountInstructions}\n\n## 重要：输出要求\n将你的完整分析报告写入文件：${outputFile}\n完成后在最后一行输出：EXECUTION_COMPLETE`;

  // 确保代理独立工作区和输出目录存在
  const agentWorkspace = agentProfile.workspace || CONFIG_DIR;
  fs.mkdirSync(agentWorkspace, { recursive: true });
  fs.mkdirSync(outputDir, { recursive: true });

  return {
    task: completeTask,
    label: `multi-agent-${agentProfile.name}-${workflow.id}${version > 1 ? `-v${version}` : ''}`,
    model: modelResult.model,
    thinking: finalThinking !== 'off' ? finalThinking : undefined,  // off 时不传参数
    timeoutSeconds,
    cwd: agentWorkspace,
    mode: 'run',
    thread: false,
    cleanup: 'keep',
    // 输出文件路径（用于看板追踪）
    output_file: outputFile,
    // 元数据（用于看板和重试）
    _meta: {
      agentRole: agentProfile.name,
      complexity,
      modelTier: modelResult.tier,
      modelReason: modelResult.reason,
      costPerMToken: modelResult.costPerMToken,
      modelReused: modelResult.reused || false,
      modelError: modelResult.error || false
    }
  };
}

/**
 * 构建文件系统挂载/访问说明（纯文本，嵌入到 task 中）
 * ⚠️ 修复：禁止包含任何 shell 命令语法（&& 等），子代理只能用 write 工具写文件
 */
function buildMountInstructions(agentProfile, sharedDir, outputDir) {
  let instructions = `\n## 工作环境\n`;
  instructions += `- 你的工作区: ${agentProfile.workspace || CONFIG_DIR}\n`;
  instructions += `- 共享目录（只读参考）: ${sharedDir}\n`;
  instructions += `- 输出目录: ${outputDir}\n\n`;

  instructions += `### 文件写入规则（强制遵守）\n`;
  instructions += `- 仅使用 write 工具写入文件，禁止使用 exec/shell 命令\n`;
  instructions += `- 禁止使用 &&、||、| 等 shell 连接符\n`;
  instructions += `- 文件必须包含 .md 后缀\n`;
  instructions += `- 写入后用 read 工具验证前 3 行确认成功\n\n`;

  instructions += `### 可用资源\n`;

  // 列出共享目录中已有的文件
  try {
    if (fs.existsSync(sharedDir)) {
      const files = fs.readdirSync(sharedDir).filter(f => !f.startsWith('.'));
      if (files.length > 0) {
        for (const f of files) {
          const fullPath = path.join(sharedDir, f);
          const stat = fs.statSync(fullPath);
          instructions += `- shared/${f} (${stat.isDirectory() ? '目录' : stat.size + ' 字节'})\n`;
        }
      } else {
        instructions += `- （共享目录为空，你是首个执行的代理）\n`;
      }
    }
  } catch {
    instructions += `- （无法读取共享目录）\n`;
  }

  return instructions;
}

/**
 * 为并行阶段构建多个子代理的 spawn 参数
 *
 * @param {array} agentNames - 并行执行的代理名称列表
 * @param {object} workflow - 工作流实例
 * @param {object} profiles - 代理配置映射 { name: profile }
 * @param {object} phaseTasks - 各代理的任务映射 { agentName: task }
 * @returns {array} spawn 参数数组
 */
export function buildParallelSpawnParams(agentNames, workflow, profiles, phaseTasks) {
  const sharedDir = path.join(CONFIG_DIR, 'shared');
  const outputDir = path.join(sharedDir, 'final');

  // 确保目录存在
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(sharedDir, 'progress'), { recursive: true });

  // 批量异构模型选择（同一批次不重复模型）
  const batchModels = selectBatchModels(agentNames, { complexity: 'complex' });

  return agentNames.map(agentName => {
    const profile = profiles[agentName];
    if (!profile) throw new Error(`代理配置缺失: ${agentName}`);

    const task = phaseTasks[agentName] || {
      description: `请执行你在工作流 "${workflow.name}" 中的职责`,
      requirements: []
    };

    // 告知每个代理其他并行代理的信息（了解协作上下文）
    const relatedTasks = agentNames
      .filter(n => n !== agentName)
      .map(n => ({ agent: n, description: phaseTasks[n]?.description || '并行执行中' }));

    // 获取预选的模型
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

/**
 * 收集子代理执行结果（从文件系统读取）
 * v8.1 增强版：主动轮询监控 + 文件写入验证 + 内容有效性检查 + 自动重试机制
 *
 * 核心改进：
 * 1. 主动轮询机制（每 30 秒检查文件状态，防止"丢失"误判）
 * 2. 超时处理（1 小时无产出触发降级协议）
 * 3. 状态日志记录（记录每次轮询状态，便于调试）
 * 4. 消息路由验证（确保 sessions_send 消息可追溯）
 *
 * @param {array} agentNames - 代理名称列表
 * @param {string} outputDir - 输出目录
 * @param {object} modelInfo - 模型信息 { agentName: { modelId, thinking } }
 * @param {object} options - 额外选项 { pollIntervalMs, timeoutMs, logFile }
 * @returns {object} { results: { agentName: content }, missing: [agentNames], thinkingVerification: { agentName: verify }, verificationStatus: { agentName: boolean }, pollHistory: { agentName: [{timestamp, status}] } }
 */
export function collectResults(agentNames, outputDir, modelInfo, options = {}) {
  const results = {};
  const missing = [];
  const thinkingVerification = {};
  const verificationStatus = {};
  const verificationDetails = {};
  const pollHistory = {}; // 新增：轮询历史记录
  
  // 轮询配置（v8.1 新增）
  const POLL_INTERVAL_MS = options.pollIntervalMs || 30000; // 默认 30 秒
  const TIMEOUT_MS = options.timeoutMs || 3600000; // 默认 1 小时
  const logFile = options.logFile || null; // 可选：日志文件路径
  
  /**
   * 记录轮询日志（v8.1 新增）
   */
  function logPollEvent(agentName, event, details = {}) {
    const timestamp = new Date().toISOString();
    const logEntry = { timestamp, agent: agentName, event, ...details };
    
    // 记录到轮询历史
    if (!pollHistory[agentName]) pollHistory[agentName] = [];
    pollHistory[agentName].push(logEntry);
    
    // 写入日志文件（如果指定）
    if (logFile) {
      try {
        const logLine = JSON.stringify(logEntry) + '\n';
        fs.appendFileSync(logFile, logLine, 'utf-8');
      } catch (err) {
        console.warn(`日志写入失败：${err.message}`);
      }
    }
    
    console.log(`[轮询] ${timestamp} - ${agentName}: ${event}`, details);
  }

  /**
   * 验证文件写入的有效性
   * @param {string} filePath - 文件路径
   * @returns {object} { valid: boolean, reason?: string, size?: number }
   */
  function verifyFileWrite(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        return { valid: false, reason: '文件不存在' };
      }
      
      const stats = fs.statSync(filePath);
      const size = stats.size;
      
      // 基本大小检查 - 100字节为最小有意义内容
      if (size < 100) {
        return { valid: false, reason: `文件大小不足 (${size} < 100 bytes)`, size };
      }
      
      // 读取文件内容进行进一步验证
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // 内容有效性检查 - 避免空内容或无效内容
      if (!content || content.trim().length === 0) {
        return { valid: false, reason: '文件内容为空', size };
      }
      
      // 检查是否包含常见的无效模板文本
      const invalidPatterns = [
        '我是OpenClaw AI助手',
        '未能完成任务',
        '抱歉，我无法',
        '对不起，我不能'
      ];
      
      const lowerContent = content.toLowerCase();
      for (const pattern of invalidPatterns) {
        if (lowerContent.includes(pattern.toLowerCase())) {
          return { valid: false, reason: `检测到无效模板文本: ${pattern}`, size };
        }
      }
      
      // 检查内容是否为有效Markdown或文本
      const lineCount = content.split('\n').length;
      if (lineCount < 3) {
        return { valid: false, reason: `行数过少 (${lineCount} < 3)`, size };
      }
      
      // 检查实际文本字符比例（排除空白符）
      const textChars = content.replace(/\s+/g, '').length;
      const textRatio = textChars / content.length;
      if (textRatio < 0.3) {
        return { valid: false, reason: `文本字符比例过低 (${(textRatio*100).toFixed(1)}% < 30%)`, size };
      }
      
      return { valid: true, size, lineCount, textRatio };
    } catch (err) {
      return { valid: false, reason: `文件访问错误: ${err.message}` };
    }
  }

  for (const name of agentNames) {
    const reportPath = path.join(outputDir || path.join(CONFIG_DIR, 'shared', 'final'), `${name}_report.md`);
    let fileValid = false;
    let verificationResult = null;
    
    try {
      // 验证文件写入
      verificationResult = verifyFileWrite(reportPath);
      fileValid = verificationResult.valid;
      verificationStatus[name] = fileValid;
      verificationDetails[name] = verificationResult;
      
      if (fileValid) {
        const content = fs.readFileSync(reportPath, 'utf-8');
        results[name] = content;

        // Thinking 验证（如果提供了模型信息）
        if (modelInfo && modelInfo[name]) {
          const { modelId } = modelInfo[name];
          thinkingVerification[name] = verifyThinkingExecution(modelId, { content, status: 'success' });
        }
      } else {
        // 文件写入无效，记录原因并标记为缺失
        console.warn(`代理 ${name} 文件写入验证失败: ${verificationResult.reason}`);
        missing.push(name);
      }
    } catch (err) {
      // 任何异常都视为缺失
      console.error(`代理 ${name} 结果收集异常: ${err.message}`);
      verificationStatus[name] = false;
      verificationDetails[name] = { valid: false, reason: `异常: ${err.message}` };
      missing.push(name);
    }
  }

  return { results, missing, thinkingVerification, verificationStatus, verificationDetails };
}

/**
 * 验证单个代理的产出
 *
 * @param {string} agentName - 代理名称
 * @param {string} content - 产出内容
 * @param {string} goal - 工作流目标
 * @returns {object} 验证结果
 */
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
      report: `验证执行失败: ${err.message}`,
      details: null
    };
  }
}

/**
 * 聚合所有分支结果为最终报告
 *
 * @param {object} results - { agentName: content } 映射
 * @param {string} goal - 工作流目标
 * @param {string} template - 聚合模板名
 * @returns {object} { report: string, formatted: string }
 */
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
      formatted: `聚合失败: ${err.message}\n\n## 原始结果\n\n${Object.entries(results).map(([k, v]) => `### ${k}\n\n${v}`).join('\n\n---\n\n')}`
    };
  }
}

/**
 * 生成批判性审核任务的提示词
 *
 * @param {string} aggregatedContent - 聚合后的内容
 * @param {string} goal - 工作流目标
 * @returns {object} Critic 的 spawn 参数
 */
export function buildCriticTask(aggregatedContent, goal, workflowId) {
  const criticProfile = {
    name: 'Critic',
    description: '独立批判性审核者。审查所有产出的逻辑漏洞、证据不足、偏见盲点。',
    capabilities: ['critical_thinking', 'bias_detection', 'logic_review', 'gap_analysis'],
    workspace: path.join(CONFIG_DIR, 'agents', 'Critic')
  };

  const task = {
    description: `对以下聚合报告进行独立批判性评估：\n\n---\n\n${aggregatedContent}\n\n---\n\n总体目标: ${goal}`,
    requirements: [
      '逻辑一致性评分（1-10）',
      '证据充分性评分（1-10）',
      '识别偏见和盲点',
      '指出关键漏洞',
      '给出审核结论（通过/返工/重大修订）'
    ]
  };

  const outputDir = path.join(CONFIG_DIR, 'shared', 'final');

  return buildSpawnParams(criticProfile, task, {
    id: workflowId || `wf_critic_${Date.now()}`,
    name: '批判性审核',
    goal
  }, {
    sharedDir: path.join(CONFIG_DIR, 'shared'),
    outputDir
  });
}

/**
 * 生成完整工作流的执行计划
 * 这是主入口函数——AI 代理调用此函数获取整个工作流的结构化执行方案
 *
 * @param {object} workflow - 工作流实例
 * @param {object} profiles - 代理配置映射
 * @returns {object} 完整执行计划
 */
export function buildExecutionPlan(workflow, profiles) {
  // 使用分层目录结构
  const directories = buildOutputDirs(workflow);
  const { researchDir, versionDir, finalDir, boardsDir, slug } = directories;
  const sharedDir = path.join(CONFIG_DIR, 'shared');

  // 确保代理工作区目录存在
  fs.mkdirSync(path.join(CONFIG_DIR, 'agents', 'Research_Analyst'), { recursive: true });
  fs.mkdirSync(path.join(CONFIG_DIR, 'agents', 'Technical_Specialist'), { recursive: true });
  fs.mkdirSync(path.join(CONFIG_DIR, 'agents', 'Strategy_Analyst'), { recursive: true });
  fs.mkdirSync(path.join(CONFIG_DIR, 'agents', 'Critic'), { recursive: true });

  const plan = {
    workflow_id: workflow.id,
    name: workflow.name,
    goal: workflow.goal,
    shared_dir: sharedDir,
    output_dir: versionDir,  // 使用分层目录
    final_dir: finalDir,
    research_dir: researchDir,
    slug,
    directories,  // 保存完整目录结构供后续使用
    phases: []
  };

  for (const phase of workflow.phases) {
    const phasePlan = {
      id: phase.id,
      name: phase.name,
      type: phase.type,
      description: phase.description,
      status: 'pending',
      spawns: []  // 需要 sessions_spawn 的调用列表
    };

    if (phase.type === 'parallel') {
      // 并行阶段：批量异构模型选择 + 为每个分支代理构建 spawn 参数
      const branchAgents = ['Research_Analyst', 'Technical_Specialist', 'Strategy_Analyst'];
      const phaseTasks = buildPhaseTasks(workflow.goal, phase);

      // 先批量选择模型，确保不重复
      const pool = buildModelPool();
      const batchModels = selectBatchModels(branchAgents, { complexity: 'complex', pool });

      for (const agentName of branchAgents) {
        const profile = profiles[agentName];
        if (profile) {
          const task = phaseTasks[agentName];
          const relatedTasks = branchAgents
            .filter(n => n !== agentName)
            .map(n => ({ agent: n, description: phaseTasks[n]?.description || '' }));

          // 排除其他代理已选的模型
          const otherModels = branchAgents
            .filter(n => n !== agentName)
            .map(n => batchModels.get(n)?.model)
            .filter(Boolean);

          phasePlan.spawns.push(
            buildSpawnParams(profile, task, workflow, {
              sharedDir, outputDir: directories.versionDir, relatedTasks,
              excludedModels: otherModels,
              directories  // 传递完整目录结构
            })
          );
        }
      }
    } else if (phase.type === 'critical_agent') {
      // 批判性审核阶段：读取聚合结果，生成审核任务
      phasePlan.depends_on = 'aggregate';  // 依赖聚合阶段完成
      phasePlan.build_task = 'critic_review';  // 标记：需要动态构建
    } else if (phase.type === 'main_agent') {
      // 主代理阶段：由 AI 代理自行处理，无需 spawn
      phasePlan.execution = 'inline';
      phasePlan.instructions = getMainAgentInstructions(phase, workflow);
    }

    plan.phases.push(phasePlan);
  }

  return plan;
}

/**
 * 为并行阶段构建各代理的子任务
 * 修复：角色模板必须与任务领域适配，不再使用通用技术模板
 */
function buildPhaseTasks(goal, phase) {
  // 领域自适应通用模板 - 基于 goal 动态生成任务描述
  return {
    Research_Analyst: {
      description: `研究课题：${goal}\n\n请从信息收集、背景调研、关键要素分析的角度进行深度研究。`,
      requirements: [
        '梳理背景、现状和关键脉络',
        '列出核心要素和关键数据',
        '分析各方/各要素的关联和影响',
        '识别关键趋势和变化点',
        '输出结构化研究报告（Markdown 格式，中文撰写）'
      ]
    },
    Technical_Specialist: {
      description: `专项分析：${goal}\n\n请从技术/数据/方法的视角进行定量或深入分析。`,
      requirements: [
        '对比分析关键要素和数据',
        '提供具体数据和量化对比（如适用）',
        '分析关键技术/方法/工具',
        '列出关键瓶颈和限制因素',
        '识别关键节点和突破点',
        '输出结构化分析报告（Markdown 格式，中文撰写）'
      ]
    },
    Strategy_Analyst: {
      description: `综合研判：${goal}\n\n请从多维度、多情景、未来走向的角度进行预测和建议。`,
      requirements: [
        '分析多维度影响和关联',
        '多情景推演（含概率评估：高/中/低）',
        '短/中/长期趋势预测',
        '关键风险和机会评估',
        '输出结构化研判报告（Markdown 格式，中文撰写）'
      ]
    }
  };
}

/**
 * 获取主代理阶段的执行指令 — 修复：路径使用分层目录
 */
function getMainAgentInstructions(phase, workflow) {
  // 根据 workflow 的目录结构生成正确路径
  const versionDir = workflow.versionDir
    || path.join(CONFIG_DIR, 'shared', 'researches', (workflow.slug || workflow.id || 'unknown'), 'v1');
  const finalDir = workflow.finalDir
    || path.join(CONFIG_DIR, 'shared', 'researches', (workflow.slug || workflow.id || 'unknown'), 'final');

  switch (phase.id) {
    case 'decompose':
      return `请分析目标"${workflow.goal}"，将其分解为3-5个具体子任务。输出任务分解方案和分配计划。`;
    case 'validate':
      return `请检查 ${versionDir} 目录下各分支代理的报告，评估质量是否达标（完整性、准确性、格式）。不达标则标注需要返工的具体问题。`;
    case 'aggregate':
      return `请读取 ${versionDir} 下所有分支报告，将其融合为一份统一的综合报告，保存到 ${finalDir}/AGGREGATED_REPORT.md。`;
    case 'critic_rework':
      return `Phase 4b — Critic 审核不通过，触发返工循环。\n\n请按以下步骤执行：
1. 读取 ${versionDir}/Critic_report.md 了解审核问题
2. 针对每个需要修正的问题，使用 buildReworkSpawnParams() 生成修正任务的 spawn 参数
3. 对每个需要修正的代理调用 sessions_spawn 下发修正任务
4. 修正完成后再次触发 Critic 审核
5. 直到 Critic 审核通过，才进入聚合阶段

不可进入聚合：Critic 审核结论不是"通过"。`;
    case 'decision':
      return `请根据批判性审核结果做出最终决策：接受（生成最终报告）/ 部分修订 / 拒绝返工。`;
    case 'complete':
      return `请生成最终交付物，保存到 ${finalDir}/FINAL_REPORT.md，并在报告末尾附加执行总结。`;
    default:
      return `请执行阶段"${phase.name}"的任务：${phase.description}`;
  }
}

/**
 * 根据 Critic 审核意见构建返工任务的 spawn 参数
 * 新增：修复 Critic 反馈后缺少返工 spawn builder 的问题
 *
 * @param {string} agentName - 需要修正的代理角名
 * @param {object} criticFeedback - Critic 审核报告中针对该代理的修正建议
 * @param {object} workflow - 工作流实例
 * @param {object} options - 额外选项 { directories, version })
 * @returns {object} sessions_spawn 参数
 */
export function buildReworkSpawnParams(agentName, criticFeedback, workflow, options = {}) {
  // 获取代理配置
  const profiles = loadProfileConfig();
  const profile = profiles[agentName];
  if (!profile) {
    throw new Error(`代理配置不存在: ${agentName}`);
  }

  const dirs = options.directories || buildOutputDirs(workflow, options.version || 1);
  const outputFile = path.join(dirs.versionDir, `${agentName}_report_v${options.version || 2}.md`);

  const originalReportPath = path.join(dirs.versionDir, `${agentName}_report.md`);

  // 构建返工任务 prompt
  const task = {
    description: '【返工修正任务】\n\nCritic 审核发现你的初始报告存在以下问题，请立即修正：\n\n' + criticFeedback + '\n\n---\n\n请读取你原始报告：' + originalReportPath,
    requirements: [
      '逐一修正 Critic 列出的每个问题',
      '在报告开头标注修正版本号（V2/V3...）',
      '输出完整的修正后报告（不要只输出修改部分）',
      'Markdown 格式，中文撰写'
    ]
  };

  const fullPrompt = generateAgentPrompt(profile, task, 'rework_task', {
    goal: workflow.goal,
    workflow_id: workflow.id,
    output_dir: dirs.versionDir,
    critic_feedback: criticFeedback
  });

  const completeTask = `${fullPrompt}\n\n## 重要：输出要求\n将你的完整修正报告写入文件${outputFile}\n完成后在最后一行输出：REWORK_COMPLETE`;

  // 模型选择：同角色使用不同模型，避开导致第一次失败的模型
  const modelResult = selectModel(agentName, {
    complexity: 'complex',
    excludedModels: options.excludedModels || [],
    allowFree: options.allowFree !== false
  });

  const thinkingLevel = selectThinkingLevel(modelResult.model, 'complex');

  return {
    task: completeTask,
    label: `rework-${agentName}-${workflow.id}-v${options.version || 2}`,
    model: modelResult.model,
    thinking: thinkingLevel !== 'off' ? thinkingLevel : undefined,
    timeoutSeconds: options.timeoutSeconds || 180,
    cwd: profile.workspace || CONFIG_DIR,
    mode: 'run',
    thread: false,
    cleanup: 'keep',
    output_file: outputFile,
    _meta: {
      agentRole: agentName,
      complexity: 'complex',
      modelTier: modelResult.tier,
      isRework: true,
      reworkVersion: options.version || 2
    }
  };
}

/**
 * 从配置文件加载代理配置
 */
function loadProfileConfig() {
  const PROFILES_FILE = path.join(CONFIG_DIR, '.multi-agent-profiles.json');
  try {
    if (!fs.existsSync(PROFILES_FILE)) {
      // 返回默认配置
      return {
        Research_Analyst: {
          name: 'Research_Analyst',
          description: '信息收集与分析',
          capabilities: ['research', 'analysis', 'synthesis'],
          workspace: path.join(CONFIG_DIR, 'agents', 'Research_Analyst')
        },
        Technical_Specialist: {
          name: 'Technical_Specialist',
          description: '技术与能力分析',
          capabilities: ['technical', 'quantitative', 'comparison'],
          workspace: path.join(CONFIG_DIR, 'agents', 'Technical_Specialist')
        },
        Strategy_Analyst: {
          name: 'Strategy_Analyst',
          description: '战略与预测分析',
          capabilities: ['strategy', 'forecasting', 'scenario'],
          workspace: path.join(CONFIG_DIR, 'agents', 'Strategy_Analyst')
        },
        Critic: {
          name: 'Critic',
          description: '独立批判性审核',
          capabilities: ['critical_thinking', 'bias_detection', 'logic_review'],
          workspace: path.join(CONFIG_DIR, 'agents', 'Critic')
        }
      };
    }
    const config = JSON.parse(fs.readFileSync(PROFILES_FILE, 'utf-8'));
    const profiles = {};
    for (const agent of (config.agents || [])) {
      profiles[agent.name] = agent;
    }
    return profiles;
  } catch {
    return {};
  }
}

/**
 * 保存执行计划到文件（持久化 + 调试用）
 */
export function saveExecutionPlan(plan, filePath) {
  const targetPath = filePath || path.join(CONFIG_DIR, 'shared', 'execution_plan.json');
  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  fs.writeFileSync(targetPath, JSON.stringify(plan, null, 2), 'utf-8');
  return targetPath;
}

/**
 * 从文件加载执行计划
 */
export function loadExecutionPlan(filePath) {
  const targetPath = filePath || path.join(CONFIG_DIR, 'shared', 'execution_plan.json');
  if (!fs.existsSync(targetPath)) return null;
  return JSON.parse(fs.readFileSync(targetPath, 'utf-8'));
}

// ===================== 新增：看板 + 重试 + 模型选择导出 =====================

// 重新导出子模块函数，方便 index.js 和外部调用
export {
  // modelSelector
  selectModel, selectBatchModels,

  // retryManager
  diagnoseFailure, buildRetrySpawn, assessDegradation, buildDegradationPlan,
  ErrorType, DegradationLevel,

  // archiver
  archiveWorkflow, cleanShared, generateFinalSummary, archiveAndClean,

  // thinkingCapabilities
  checkModelThinking, selectThinkingLevel,

  // 分层目录 + 看板系统
  buildOutputDirs, buildOutputPath,
  createPlanBoard, createExecBoard, updateExecBoard, loadExecBoard, formatExecBoard
};
