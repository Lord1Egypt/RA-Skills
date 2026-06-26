/**
 * Thinking 能力检测与容错管理器
 *
 * 职责：
 * 1. 维护每个模型的 thinking 支持能力矩阵
 * 2. 执行前：查询能力矩阵，自动降级不支持的模型
 * 3. 执行后：通过响应分析更新能力状态（学习机制）
 * 4. 容错：thinking 异常时自动降级到 safe 模式
 *
 * 数据持久化：.thinking-capabilities.json
 */

import fs from 'fs';
import path from 'path';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const CAPABILITIES_FILE = path.join(CONFIG_DIR, '.thinking-capabilities.json');

// ===================== 已知模型能力预设 =====================

/**
 * 已知模型的 thinking 支持预设表
 * 基于模型特性手动维护的首批数据
 * 运行后会根据实际执行结果不断更新
 */
const KNOWN_CAPABILITIES = {
  // ── OpenRouter ──
  'openrouter/qwen/qwen3.6-plus:free': {
    supportsThinking: true,
    thinkingModes: ['low', 'medium', 'high'],
    defaultMode: 'medium',
    confidence: 0.9,
    source: 'preset'
  },
  'openrouter/nvidia/nemotron-3-super-120b-a12b:free': {
    supportsThinking: true,
    thinkingModes: ['low', 'medium'],
    defaultMode: 'low',
    confidence: 0.7,
    source: 'preset'
  },
  'openrouter/stepfun/step-3.5-flash:free': {
    supportsThinking: true,
    thinkingModes: ['low'],
    defaultMode: 'low',
    confidence: 0.6,
    source: 'preset'
  },

  // ── ModelScope ──
  'custom-api-inference-modelscope-cn/deepseek-ai/DeepSeek-V3.2': {
    supportsThinking: true,
    thinkingModes: ['medium', 'high'],
    defaultMode: 'high',
    confidence: 0.95,
    source: 'preset'
  },
  'custom-api-inference-modelscope-cn/ZhipuAI/GLM-5': {
    supportsThinking: true,
    thinkingModes: ['medium', 'high'],
    defaultMode: 'medium',
    confidence: 0.85,
    source: 'preset'
  },
  'custom-api-inference-modelscope-cn/Qwen/Qwen3.5-397B-A17B': {
    supportsThinking: true,
    thinkingModes: ['low', 'medium'],
    defaultMode: 'medium',
    confidence: 0.85,
    source: 'preset'
  },
  'custom-api-inference-modelscope-cn/moonshotai/Kimi-K2.5': {
    supportsThinking: true,
    thinkingModes: ['low', 'medium'],
    defaultMode: 'medium',
    confidence: 0.7,
    source: 'preset'
  },

  // ── BigModel (GLM) ──
  'custom-open-bigmodel-cn/GLM-4.7-Flash': {
    supportsThinking: true,
    thinkingModes: ['low', 'medium'],
    defaultMode: 'low',
    confidence: 0.8,
    source: 'preset'
  },

  // ── Local ──
  'local/zai-org/glm-4.7-flash': {
    supportsThinking: true,
    thinkingModes: ['low', 'medium'],
    defaultMode: 'low',
    confidence: 0.7,
    source: 'preset'
  },

  // ── 盲盒（不建议用，但作为 fallback） ──
  'openrouter/free': {
    supportsThinking: false,
    thinkingModes: [],
    defaultMode: 'off',
    confidence: 1.0,
    source: 'preset',
    reason: '盲盒模型，无法保证 thinking 支持'
  }
};

// ===================== 能力矩阵读写 =====================

/**
 * 加载 thinking 能力矩阵
 * 合并方式：用户实际验证结果 > 预设数据
 */
export function loadCapabilities() {
  let userOverrides = {};
  try {
    if (fs.existsSync(CAPABILITIES_FILE)) {
      const raw = fs.readFileSync(CAPABILITIES_FILE, 'utf-8');
      userOverrides = JSON.parse(raw);
    }
  } catch (err) {
    console.error(`⚠️ 读取 thinking 能力矩阵失败: ${err.message}`);
  }

  // 深合并：用户数据覆盖预设
  const merged = { ...KNOWN_CAPABILITIES };
  for (const [modelId, caps] of Object.entries(userOverrides)) {
    if (merged[modelId]) {
      merged[modelId] = { ...merged[modelId], ...caps };
      if (caps.source) merged[modelId].source = caps.source;
    } else {
      merged[modelId] = { ...caps };
    }
  }

  return merged;
}

/**
 * 保存 thinking 能力矩阵
 */
export function saveCapabilities(capabilities) {
  try {
    // 只保存用户验证过的数据（source !== 'preset'）
    const userEntries = {};
    for (const [modelId, caps] of Object.entries(capabilities)) {
      if (caps.source === 'verified' || caps.source === 'failed' || caps.source === 'user_override') {
        userEntries[modelId] = {
          supportsThinking: caps.supportsThinking,
          thinkingModes: caps.thinkingModes,
          defaultMode: caps.defaultMode,
          source: caps.source,
          verifiedAt: caps.verifiedAt,
          reason: caps.reason
        };
      }
    }
    fs.writeFileSync(CAPABILITIES_FILE, JSON.stringify(userEntries, null, 2), 'utf-8');
  } catch (err) {
    console.error(`⚠️ 保存 thinking 能力矩阵失败: ${err.message}`);
  }
}

// ===================== 能力查询 =====================

/**
 * 检查模型是否支持 thinking
 *
 * @param {string} modelId - 完整模型 ID
 * @returns {object} { supportsThinking, thinkingModes, defaultMode, reason }
 */
export function checkModelThinking(modelId) {
  const capabilities = loadCapabilities();
  const caps = capabilities[modelId];

  if (caps) {
    return {
      supportsThinking: caps.supportsThinking,
      thinkingModes: caps.thinkingModes || [],
      defaultMode: caps.defaultMode || 'off',
      confidence: caps.confidence,
      reason: caps.reason || null
    };
  }

  // 未知模型 → 保守策略：假设支持 low 级别
  return {
    supportsThinking: true,
    thinkingModes: ['low'],
    defaultMode: 'low',
    confidence: 0.3,
    reason: '未知模型，使用保守假设'
  };
}

/**
 * 为代理角色选择最佳 thinking 级别
 *
 * @param {string} modelId - 模型 ID
 * @param {string} complexity - simple/medium/complex/critical
 * @returns {string} thinking 级别（low/medium/high 或 off）
 */
export function selectThinkingLevel(modelId, complexity) {
  const caps = checkModelThinking(modelId);

  if (!caps.supportsThinking) return 'off';

  // 复杂度 → 期望级别映射
  const desiredLevel = {
    simple: 'low',
    medium: 'medium',
    complex: 'high',
    critical: 'high'
  }[complexity] || 'medium';

  const desiredIdx = ['low', 'medium', 'high'].indexOf(desiredLevel);

  // 选择模型支持的最高级别（不超过期望级别）
  const supportedModes = caps.thinkingModes;
  let bestMode = caps.defaultMode;

  for (const mode of ['high', 'medium', 'low']) {
    if (supportedModes.includes(mode)) {
      const modeIdx = ['low', 'medium', 'high'].indexOf(mode);
      if (modeIdx <= desiredIdx) {
        bestMode = mode;
        break;
      }
    }
  }

  // 如果所有支持的级别都超过期望（极少），降级到最低支持级别
  if (!supportedModes.includes(bestMode)) {
    bestMode = supportedModes[0];
  }

  return bestMode;
}

// ===================== 安全模式降级 =====================

/**
 * thinking 降级策略
 *
 * @param {string} modelId - 当前模型
 * @param {string} currentThinking - 当前 thinking 级别
 * @param {string} fallbackModel - 兜底模型（可选）
 * @returns {object} { model, thinking, reason }
 */
export function degradeThinking(modelId, currentThinking, fallbackModel) {
  const caps = checkModelThinking(modelId);

  // 场景1：模型支持但当前级别过高
  if (caps.supportsThinking && !caps.thinkingModes.includes(currentThinking)) {
    const safeMode = caps.defaultMode;
    return {
      model: modelId,
      thinking: safeMode,
      reason: `降级：${modelId} 不支持 ${currentThinking} → ${safeMode}`
    };
  }

  // 场景2：模型不支持 thinking
  if (!caps.supportsThinking) {
    if (fallbackModel) {
      const fbCaps = checkModelThinking(fallbackModel);
      if (fbCaps.supportsThinking) {
        return {
          model: fallbackModel,
          thinking: fbCaps.defaultMode,
          reason: `切换：${modelId} 不支持 thinking → ${fallbackModel}`
        };
      }
    }
    return {
      model: modelId,
      thinking: 'off',
      reason: `关闭：${modelId} 不支持 thinking`
    };
  }

  // 场景3：一切正常
  return {
    model: modelId,
    thinking: currentThinking,
    reason: '无需降级'
  };
}

/**
 * 批量降级：为一批 spawn 参数检查并修正 thinking
 *
 * @param {array} spawnParams - sessions_spawn 参数数组
 * @returns {array} 修正后的 spawn 参数数组 + 降级日志
 */
export function batchDegradeThinking(spawnParams) {
  const log = [];
  const degraded = spawnParams.map(spawn => {
    const modelId = spawn.model;
    const thinking = spawn.thinking || 'low';

    const result = degradeThinking(modelId, thinking);
    if (result.reason !== '无需降级') {
      log.push({
        agent: spawn.label || 'unknown',
        original: { model: modelId, thinking },
        degraded: { model: result.model, thinking: result.thinking },
        reason: result.reason
      });
    }

    return {
      ...spawn,
      model: result.model,
      thinking: result.thinking
    };
  });

  return { spawns: degraded, log };
}

// ===================== 执行后验证 =====================

/**
 * 分析子代理响应，验证 thinking 是否实际生效
 *
 * @param {string} modelId - 使用的模型
 * @param {object} response - 子代理响应对象
 * @param {string} response.content - 响应内容
 * @param {string} response.status - 执行状态
 * @returns {object} { thinkingConfirmed: bool, evidence: string }
 */
export function verifyThinkingExecution(modelId, response) {
  const content = response?.content || '';
  const status = response?.status || '';

  // 检查是否有 thinking 标签（Anthropic 风格）
  const hasThinkingTag = /<thinking>/.test(content);

  // 检查是否有内部推理痕迹（多种模式）
  const hasReasoning = /让我逐步分析|step[- ]by[- ]step|首先.*然后.*最后|thought process|reasoning/i.test(content);

  // 如果响应正常且有推理痕迹，认为 thinking 生效
  if (status === 'success' && (hasThinkingTag || hasReasoning)) {
    updateModelCapability(modelId, {
      supportsThinking: true,
      source: 'verified',
      verifiedAt: new Date().toISOString()
    });

    return {
      thinkingConfirmed: true,
      evidence: hasThinkingTag ? '检测到 <thinking> 标签' : '检测到推理痕迹'
    };
  }

  // 如果状态正常但完全没有推理痕迹（且复杂度不低），可能 thinking 未生效
  if (status === 'success' && !hasThinkingTag && !hasReasoning) {
    // 不立即标记为不支持（可能是简单任务不需要推理）
    return {
      thinkingConfirmed: false,
      evidence: '未检测到推理痕迹（可能任务过于简单）',
      inconclusive: true
    };
  }

  return {
    thinkingConfirmed: false,
    evidence: '任务未成功完成，无法验证',
    inconclusive: true
  };
}

/**
 * 更新模型能力（执行后学习）
 */
function updateModelCapability(modelId, update) {
  const capabilities = loadCapabilities();
  const existing = capabilities[modelId] || {
    supportsThinking: true,
    thinkingModes: ['low'],
    defaultMode: 'low',
    confidence: 0.3,
    source: 'inferred'
  };

  capabilities[modelId] = { ...existing, ...update };
  saveCapabilities(capabilities);
}

/**
 * 用户手动覆盖模型 thinking 能力
 *
 * @param {string} modelId - 模型 ID
 * @param {object} caps - 能力配置
 */
export function setUserOverride(modelId, caps) {
  const capabilities = loadCapabilities();

  capabilities[modelId] = {
    ...caps,
    source: 'user_override',
    verifiedAt: new Date().toISOString()
  };

  saveCapabilities(capabilities);
}

// ===================== 能力矩阵展示 =====================

/**
 * 获取能力矩阵摘要（用于用户展示）
 */
export function getCapabilitiesSummary() {
  const capabilities = loadCapabilities();
  const entries = [];

  for (const [modelId, caps] of Object.entries(capabilities)) {
    const status = caps.supportsThinking
      ? `✅ ${caps.thinkingModes.join('/')}`
      : '❌ 不支持';

    entries.push({
      modelId,
      shortId: modelId.split('/').pop(),
      status,
      confidence: caps.confidence,
      source: caps.source,
      reason: caps.reason
    });
  }

  return entries;
}

/**
 * 格式化为可读表格
 */
export function formatCapabilitiesTable() {
  const summary = getCapabilitiesSummary();
  let out = '';
  out += '┌────────────────────────────────────────┬───────────────┬────────────┬──────────┐\n';
  out += '│ 模型                                   │ Thinking 支持  │ 置信度    │ 来源     │\n';
  out += '├────────────────────────────────────────┼───────────────┼────────────┼──────────┤\n';

  for (const entry of summary) {
    const modelShort = entry.shortId.padEnd(38);
    const statusShort = entry.status.padEnd(13);
    const conf = `( ${(entry.confidence * 100).toFixed(0)}% )`.padEnd(10);
    const src = (entry.source || '-').padEnd(8);
    out += `│ ${modelShort} │ ${statusShort} │ ${conf} │ ${src} │\n`;
  }

  out += '└────────────────────────────────────────┴───────────────┴────────────┴──────────┘';
  return out;
}

// ===================== 导出 =====================

export { KNOWN_CAPABILITIES };
export default {
  loadCapabilities,
  saveCapabilities,
  checkModelThinking,
  selectThinkingLevel,
  degradeThinking,
  batchDegradeThinking,
  verifyThinkingExecution,
  setUserOverride,
  getCapabilitiesSummary,
  formatCapabilitiesTable
};
