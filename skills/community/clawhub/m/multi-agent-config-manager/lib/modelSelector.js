/**
 * 异构模型选择器 v2 (Heterogeneous Model Selector)
 *
 * 设计变更 v2：从 OpenClaw 系统配置动态读取可用模型池
 * 不再硬编码模型 ID，系统配置变更后自动适配
 *
 * 职责：
 * 1. 读取系统 config 中的 providers + fallbacks → 构建动态模型池
 * 2. 按代理角色、任务类型、复杂度匹配最优模型
 * 3. 同一批次确保模型不重复（异构博弈）
 * 4. 支持自定义规则覆盖（可选的 rules 文件）
 */

import fs from 'fs';
import path from 'path';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const OPENCLAW_CONFIG = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'openclaw.json');
const RULES_FILE = path.join(CONFIG_DIR, '.model-selector-rules.json');

// ===================== 角色 → 能力标签映射 =====================

const ROLE_TRAITS = {
  Research_Analyst:     { prefer: ['research', 'analysis', 'general'], avoid: [] },
  Technical_Specialist: { prefer: ['coding', 'analysis', 'general'],   avoid: [] },
  Strategy_Analyst:     { prefer: ['analysis', 'general', 'research'], avoid: [] },
  Critic:               { prefer: ['analysis', 'general'],             avoid: [] },
};

// ===================== 已知无效模型黑名单（基于历史故障） =====================
/**
 * 已知无效或低效的模型ID
 * 这些模型在历史执行中表现不佳（高频超时/空输出/API错误）
 * 将在模型选择时自动过滤，除非明确允许
 */
const INEFFECTIVE_MODEL_BLACKLIST = new Set([
  // OpenRouter free 层无效模型（高频 402/429）
  'openrouter/free',
  // 其他已知无效免费模型
  'openrouter/auto',
  // 历史记录中零产出的模型（基于 2026-04-04 审计）
  'openrouter/nvidia/nemotron-3-super-120b-a12b:free',
  'openrouter/stepfun/step-3.5-flash:free',
  'openrouter/minimax/minimax-m2.5:free',
]);

/**
 * 检查模型是否在有效范围内
 * 排除黑名单中的模型，除非明确允许使用
 */
function isModelEffective(modelId, allowBlacklisted = false) {
  if (allowBlacklisted) return true;
  return !INEFFECTIVE_MODEL_BLACKLIST.has(modelId);
}

// ===================== 模型能力标签（启发式） =====================

/**
 * 启发式模型特征推断
 * 支持自定义规则覆盖：在 .model-selector-rules.json 中定义 traits 映射
 */
function inferTraits(modelId, modelName, provider) {
  const id = (modelId + ' ' + (modelName || '')).toLowerCase();

  // 1. 优先检查自定义规则覆盖
  const rules = loadRules();
  if (rules?.traits?.[modelId]) {
    return [...new Set([...rules.traits[modelId]])];
  }

  const traits = ['general'];  // 所有模型都有通用能力

  if (id.includes('deepseek') && (id.includes('coder') || id.includes('code'))) {
    traits.push('coding');
  }
  if (id.includes('qwen') && id.includes('coder')) {
    traits.push('coding');
  }
  if (id.includes('deepseek') && id.includes('r1')) {
    traits.push('analysis', 'coding');
  }
  if (id.includes('glm-5') || id.includes('glm-4.7')) {
    traits.push('analysis');
  }
  if (id.includes('kimi') || id.includes('moonshot')) {
    traits.push('research', 'analysis');
  }
  if (id.includes('qwen3.5') || id.includes('qwen3-')) {
    traits.push('analysis', 'research');
  }
  if (id.includes('mimo')) {
    traits.push('research', 'analysis');
  }
  if (id.includes('deepseek') && id.includes('v3')) {
    traits.push('analysis', 'research', 'coding');
  }
  if (id.includes('nemotron') || id.includes('step-')) {
    traits.push('general');
  }

  // 2. 检查 provider 级别的排除规则
  if (rules?.exclude?.[provider]?.includes(modelId)) {
    return ['general'];  // 排除该模型的特殊trait，降级为通用
  }

  // 去重
  return [...new Set(traits)];
}

// ===================== 模型档次推断 =====================

/**
 * 启导式模型档次推断
 * 支持自定义规则覆盖：在 .model-selector-rules.json 中定义 tier 映射
 */
function inferTier(modelId, cost) {
  const rules = loadRules();
  if (rules?.tiers?.[modelId]) return rules.tiers[modelId];

  // 免费模型
  if (modelId.includes(':free') || modelId === 'openrouter/free') return 'free';

  // 本地模型
  if (modelId.startsWith('local/')) return 'local';

  // ModelScope / BigModel 等平台：cost=0 表示包月，不算 free
  if (modelId.startsWith('custom-api-inference-modelscope') ||
      modelId.startsWith('custom-open-bigmodel-cn')) {
    return 'standard';
  }

  // 按上下文窗口粗估能力
  return 'standard';
}

// ===================== 从系统配置构建模型池 =====================

/**
 * 读取 OpenClaw 系统配置，构建动态模型池
 * 每次调用都重新读取（配置可能随时变更）
 */
export function buildModelPool() {
  const pool = {
    all: [],       // 所有可用模型
    byProvider: {}, // 按 provider 分组
    byTier: {      // 按档次分组
      free: [],
      local: [],
      standard: [],
    }
  };

  try {
    // 1. 读取 providers 配置
    const configRaw = fs.readFileSync(OPENCLAW_CONFIG, 'utf-8');

    // openclaw.json 可能是 JSON5（含注释、无引号键），用多种方式解析
    let config;
    try {
      // 先尝试标准 JSON（strip BOM）
      config = JSON.parse(configRaw.replace(/^\uFEFF/, ''));
    } catch (e1) {
      try {
        // JSON5 fallback：移除注释、尾逗号
        const cleaned = configRaw.replace(/^\uFEFF/, '')
          .replace(/\/\/[^\n]*/g, '')
          .replace(/\/\*[\s\S]*?\*\//g, '')
          .replace(/,\s*([}\]])/g, '$1');
        config = JSON.parse(cleaned);
      } catch (e2) {
        try {
          // 最后尝试 eval (信任本地文件)
          config = JSON.parse((0, eval)('(' + configRaw.replace(/^\uFEFF/, '') + ')'));
        } catch (e3) {
          console.error(`⚠️ openclaw.json 解析失败: ${e3.message}`);
          return pool;
        }
      }
    }

    const providers = config?.models?.providers || {};

    for (const [providerName, providerConfig] of Object.entries(providers)) {
      const models = providerConfig.models || [];
      pool.byProvider[providerName] = [];

      for (const m of models) {
        const fullId = `${providerName}/${m.id}`;
        const cost = m.cost || { input: 0, output: 0 };
        const tier = inferTier(fullId, cost);
        const traits = inferTraits(m.id, m.name, providerName);

        const entry = {
          id: fullId,
          shortId: m.id,
          name: m.name || m.id,
          provider: providerName,
          tier,
          traits,
          contextWindow: m.contextWindow || 0,
          maxTokens: m.maxTokens || 4096,
          costPerMToken: (cost.input || 0) * 1_000_000,
          reasoning: m.reasoning || false,
        };

        pool.all.push(entry);
        pool.byProvider[providerName].push(entry);
        if (pool.byTier[tier]) pool.byTier[tier].push(entry);
        else pool.byTier[tier] = [entry];
      }
    }

    // 2. 从 fallbacks 补充 openrouter/xxx:free 模型（这些可能不在 providers 里显式定义）
    const fallbacks = config?.agents?.defaults?.model?.fallbacks || [];
    const existingIds = new Set(pool.all.map(m => m.id));

    for (const fbId of fallbacks) {
      if (!existingIds.has(fbId)) {
        const tier = inferTier(fbId, null);
        const traits = inferTraits(fbId, fbId, 'openrouter');
        const entry = {
          id: fbId,
          shortId: fbId.replace('openrouter/', ''),
          name: fbId,
          provider: fbId.split('/')[0],
          tier,
          traits,
          contextWindow: 0,
          maxTokens: 4096,
          costPerMToken: 0,
          reasoning: false,
        };
        pool.all.push(entry);
        if (pool.byTier[tier]) pool.byTier[tier].push(entry);
        else pool.byTier[tier] = [entry];
      }
    }

  } catch (err) {
    console.error('⚠️ 读取系统配置失败，使用空模型池:', err.message);
  }

  return pool;
}

// ===================== 自定义规则（可选覆盖） =====================

function loadRules() {
  try {
    if (fs.existsSync(RULES_FILE)) {
      return JSON.parse(fs.readFileSync(RULES_FILE, 'utf-8'));
    }
  } catch { /* 忽略 */ }
  return null;
}

// ===================== 核心选择逻辑 =====================

/**
 * 为指定代理角色选择最优模型
 *
 * @param {string} agentRole - 代理角色名
 * @param {object} options
 * @param {string} options.complexity - simple/medium/complex/critical
 * @param {string[]} options.excludedModels - 已选中的模型 ID
 * @param {boolean} options.allowFree - 是否允许免费模型
 * @param {object} options.pool - 可选：预构建的模型池（避免重复读取）
 * @returns {object} { model, thinking, reason, tier, traits }
 */
export function selectModel(agentRole, options = {}) {
  const {
    complexity = 'medium',
    excludedModels = [],
    allowFree = true,
    pool = null,
  } = options;

  // 1. 加载自定义规则
  const rules = loadRules();

  // 2. 获取模型池
  const modelPool = pool || buildModelPool();

  // 3. 确定角色偏好 traits
  const roleTraits = rules?.roleTraits?.[agentRole] || ROLE_TRAITS[agentRole]?.prefer || ['general'];

  // 4. 过滤候选
  let candidates = modelPool.all.filter(m => {
    if (excludedModels.includes(m.id)) return false;
    if (!allowFree && m.tier === 'free') return false;
    // 排除已知无效模型（除非明确允许）
    if (!isModelEffective(m.id, options.allowBlacklisted)) return false;
    return true;
  });

  // 5. 打分排序（trait 匹配 + 档次偏好）
  const tierScores = {
    critical: { free: 10, local: 20, standard: 90 },
    complex:  { free: 30, local: 40, standard: 80 },
    medium:   { free: 70, local: 60, standard: 80 },
    simple:   { free: 90, local: 80, standard: 60 },
  };
  const scores = tierScores[complexity] || tierScores.medium;

  candidates.forEach(m => {
    m._score = (scores[m.tier] || 50);

    // trait 匹配加分
    for (const trait of roleTraits) {
      if (m.traits.includes(trait)) m._score += 15;
    }

    // 黑名单模型大幅减分（优先级最低）
    if (!isModelEffective(m.id, options.allowBlacklisted)) {
      m._score -= 1000; // 几乎确保不被选中
    }

    // 自定义规则覆盖
    if (rules?.boost?.[m.id]) m._score += rules.boost[m.id];
    if (rules?.penalty?.[m.id]) m._score -= rules.penalty[m.id];
  });

  candidates.sort((a, b) => b._score - a._score);

  const selected = candidates[0];

  if (!selected) {
    // 无排除条件时的最佳模型（回退到最后可用）
    const fallback = modelPool.all.filter(m => {
      if (!allowFree && m.tier === 'free') return false;
      // 排除黑名单模型（即使是fallback也避免使用）
      if (!isModelEffective(m.id, options.allowBlacklisted)) return false;
      return m.contextWindow > 0 || m.tier !== 'free'; // 至少要有基本能力
    }).sort((a, b) => {
      // 优先 standard > local > free
      const tierOrder = { standard: 3, local: 2, free: 1 };
      return (tierOrder[b.tier] || 1) - (tierOrder[a.tier] || 1);
    })[0];

    if (fallback) {
      return {
        model: fallback.id,
        thinking: 'low',
        reason: `无足够异构模型（可用${modelPool.all.length}个），复用 ${fallback.id} — ⚠️ 建议扩充模型池`,
        tier: fallback.tier,
        traits: fallback.traits,
        reused: true // 标记复用，供调用方决策
      };
    }

    // 极端情况：模型池完全为空
    return {
      model: null,
      thinking: 'off',
      reason: `⚠️ 模型池为空，无法分配模型 — 请检查 providers 配置`,
      tier: 'none',
      traits: [],
      error: true
    };
  }

  const thinkingLevel = complexity === 'critical' ? 'high'
    : complexity === 'complex' ? 'medium'
    : 'low';

  return {
    model: selected.id,
    thinking: thinkingLevel,
    reason: `角色=${agentRole} 偏好=${roleTraits.join(',')} 复杂度=${complexity} 得分=${selected._score} traits=${selected.traits.join(',')}`,
    tier: selected.tier,
    traits: selected.traits
  };
}

/**
 * 为并行批次选择互不重复的模型集合
 *
 * 安全约束：
 * - 同一批次不允许模型重复
 * - free 层模型最多 1 个（防止 OpenRouter QPS 限流导致子代理非正常退出）
 * - 如果 free 层名额已被占，后续角色强制分配到 standard 层
 */
export function selectBatchModels(agentRoles, options = {}) {
  const pool = options.pool || buildModelPool();
  const selected = new Map();
  const usedModels = new Set(options.excludedModels || []);
  let freeTierUsed = false;
  const uniqueModels = new Set(); // 跟踪已分配的独立模型
  let reuseTriggered = false; // 是否已触发复用降级

  for (const role of agentRoles) {
    const result = selectModel(role, {
      ...options,
      excludedModels: [...usedModels],
      pool
    });

    // 模型池完全为空 — 无法运行
    if (result.error) {
      selected.set(role, result);
      continue;
    }

    // 模型复用降级 — 可用模型不足，复用已有模型
    if (result.reused) {
      reuseTriggered = true;
      selected.set(role, result);
      // 复用模型不加入 usedModels，后续代理也可以复用
      continue;
    }

    // free 层 QPS 保护：同批次只允许 1 个 free 模型
    if (result.tier === 'free' && freeTierUsed) {
      // 已经被占，强制分配到 standard 层
      const fbResult = selectModel(role, {
        ...options,
        excludedModels: [...usedModels],
        allowFree: false,
        pool
      });

      if (fbResult.reused || fbResult.error) {
        reuseTriggered = true;
        selected.set(role, fbResult);
        continue;
      }

      selected.set(role, { ...fbResult, reason: fbResult.reason + ' [free层已满，降级到standard]' });
      usedModels.add(fbResult.model);
    } else {
      if (result.tier === 'free') freeTierUsed = true;
      selected.set(role, result);
      usedModels.add(result.model);
      uniqueModels.add(result.model);
    }
  }

  // 附加元数据：供调用方判断是否降级运行
  selected._meta = {
    totalRoles: agentRoles.length,
    uniqueModels: uniqueModels.size,
    reused: reuseTriggered,
    fullyHeterogeneous: uniqueModels.size === agentRoles.length,
    warning: reuseTriggered ? `⚠️ 可用模型(${uniqueModels.size}个) < 代理数(${agentRoles.length}个)，部分代理复用同一模型，异构博弈降级` : null
  };

  return selected;
}

/**
 * 获取模型池信息（用于调试/展示）
 */
export function getModelPoolInfo() {
  const pool = buildModelPool();
  const info = {};
  for (const [tier, models] of Object.entries(pool.byTier)) {
    if (models.length === 0) continue;
    info[tier] = models.map(m => `${m.id} [${m.traits.join(',')}]`);
  }
  info._all = pool.all.map(m => `${m.id} (${m.tier}, ${m.traits.join(',')})`);
  return info;
}

export { ROLE_TRAITS, inferTraits, inferTier };
