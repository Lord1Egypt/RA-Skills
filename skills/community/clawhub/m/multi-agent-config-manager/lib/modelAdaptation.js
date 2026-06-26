/**
 * 模型池动态适配器 (Model Pool Adapter)
 *
 * 职责：
 * 1. 首次运行时检测用户模型库，引导配置
 * 2. 持续监控模型池变更，自动适配或通知用户
 * 3. 变更检测：增量（自动适配）vs 大幅变化（需用户确认）
 * 4. 为 Coordinator 和 Critic 推荐最佳模型
 *
 * 数据持久化：
 * - .model-pool-snapshot.json — 上次快照
 * - .model-role-config.json — 用户确认后的角色-模型映射
 */

import fs from 'fs';
import path from 'path';
import { buildModelPool } from './modelSelector.js';
import { checkModelThinking, selectThinkingLevel } from './thinkingCapabilities.js';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const SNAPSHOT_FILE = path.join(CONFIG_DIR, '.model-pool-snapshot.json');
const ROLE_CONFIG_FILE = path.join(CONFIG_DIR, '.model-role-config.json');

// ===================== 阈值配置 =====================

const CHANGE_THRESHOLDS = {
  minorChange: 0.15,    // ≤15% 变更：自动适配
  significantChange: 0.30,  // >30% 变更：提示用户确认
};

// ===================== 快照管理 =====================

/**
 * 获取当前模型池快照（简化版）
 */
function getCurrentPoolSnapshot() {
  const pool = buildModelPool();
  return {
    modelIds: pool.all.map(m => m.id).sort(),
    providerCount: Object.keys(pool.byProvider).length,
    tierCounts: {
      free: pool.byTier.free?.length || 0,
      standard: pool.byTier.standard?.length || 0,
      local: pool.byTier.local?.length || 0,
    },
    snapshotTakenAt: new Date().toISOString()
  };
}

/**
 * 加载上次快照
 */
function loadSnapshot() {
  try {
    if (fs.existsSync(SNAPSHOT_FILE)) {
      return JSON.parse(fs.readFileSync(SNAPSHOT_FILE, 'utf-8'));
    }
  } catch (err) {
    console.error(`⚠️ 读取模型池快照失败: ${err.message}`);
  }
  return null;
}

/**
 * 保存当前快照
 */
function saveSnapshot(snapshot) {
  try {
    fs.writeFileSync(SNAPSHOT_FILE, JSON.stringify(snapshot, null, 2), 'utf-8');
  } catch (err) {
    console.error(`⚠️ 保存模型池快照失败: ${err.message}`);
  }
}

// ===================== 变更检测 =====================

/**
 * 对比两个快照，计算变更比例
 *
 * @param {object} oldSnapshot - 旧快照
 * @param {object} newSnapshot - 新快照
 * @returns {object} { changeRatio, added, removed, isSignificant, summary }
 */
export function detectPoolChanges(oldSnapshot, newSnapshot) {
  if (!oldSnapshot) {
    return {
      changeRatio: 1.0,
      added: newSnapshot.modelIds,
      removed: [],
      isSignificant: true,
      isFirstRun: true,
      summary: `首次检测到 ${newSnapshot.modelIds.length} 个模型`
    };
  }

  const oldSet = new Set(oldSnapshot.modelIds);
  const newSet = new Set(newSnapshot.modelIds);

  const added = newSnapshot.modelIds.filter(id => !oldSet.has(id));
  const removed = oldSnapshot.modelIds.filter(id => !newSet.has(id));

  const maxLen = Math.max(oldSet.size, newSet.size, 1);
  const changeRatio = (added.length + removed.length) / maxLen;

  const isSignificant = changeRatio > CHANGE_THRESHOLDS.significantChange;
  const isMinor = changeRatio <= CHANGE_THRESHOLDS.minorChange;

  let summary;
  if (added.length === 0 && removed.length === 0) {
    summary = '模型池无变化';
  } else {
    summary = `变更 +${added.length}/-${removed.length}（${(changeRatio * 100).toFixed(0)}%）`;
    if (added.length > 0) summary += `\n  新增: ${added.join(', ')}`;
    if (removed.length > 0) summary += `\n  移除: ${removed.join(', ')}`;
  }

  return {
    changeRatio,
    added,
    removed,
    isSignificant,
    isMinor,
    isFirstRun: false,
    summary
  };
}

// ===================== 角色推荐算法 =====================

/**
 * 模型评分权重（针对角色）
 */
const ROLE_WEIGHTS = {
  coordinator: {
    contextWindow: 0.35,   // 大窗口最重要
    maxTokens: 0.25,       // 大输出
    thinkingQuality: 0.2,  // 推理质量
    stability: 0.2         // API 稳定性
  },
  critic: {
    contextWindow: 0.2,
    maxTokens: 0.2,
    thinkingQuality: 0.4,  // 推理最重要
    stability: 0.2
  },
  worker: {
    contextWindow: 0.15,
    maxTokens: 0.25,
    thinkingQuality: 0.25,
    stability: 0.35        // 稳定性最重要
  }
};

/**
 * 为指定角色推荐最佳模型
 *
 * @param {string} role - coordinator | critic | worker
 * @param {object} pool - 模型池
 * @param {string[]} excludedModels - 排除的模型
 * @returns {object} { model, config }
 */
function recommendModelForRole(role, pool, excludedModels = []) {
  const weights = ROLE_WEIGHTS[role];
  if (!weights) return null;

  const candidates = pool.all.filter(m => !excludedModels.includes(m.id));
  if (candidates.length === 0) return null;

  // 计算每个候选的加权得分
  const scored = candidates.map(candidate => {
    // 上下文窗口评分（标准化 0-100）
    const windowScore = Math.min(100, (candidate.contextWindow / 128000) * 100);

    // 最大输出评分（标准化 0-100）
    const outputScore = Math.min(100, (candidate.maxTokens / 16384) * 100);

    // Thinking 质量评分
    const thinkingCaps = checkModelThinking(candidate.id);
    let thinkingScore = 0;
    if (thinkingCaps.supportsThinking) {
      const modeIdx = ['low', 'medium', 'high'].indexOf(thinkingCaps.defaultMode);
      thinkingScore = (modeIdx + 1) / 3 * 100;  // 1/3, 2/3, 1.0
      thinkingScore *= thinkingCaps.confidence;
    }

    // 稳定性评分（云端/本地）
    const isProvider = candidate.provider && !candidate.provider.startsWith('openrouter/free');
    const stabilityScore = thinkingCaps.supportsThinking ? 90 : 70;

    const totalScore =
      windowScore * weights.contextWindow +
      outputScore * weights.maxTokens +
      thinkingScore * weights.thinkingQuality +
      stabilityScore * weights.stability;

    return {
      candidate,
      score: totalScore,
      breakdown: {
        windowScore: windowScore.toFixed(0),
        outputScore: outputScore.toFixed(0),
        thinkingScore: thinkingScore.toFixed(0),
        stabilityScore: stabilityScore.toFixed(0)
      }
    };
  });

  scored.sort((a, b) => b.score - a.score);

  const winner = scored[0];
  return {
    model: winner.candidate.id,
    shortId: winner.candidate.shortId,
    contextWindow: winner.candidate.contextWindow,
    maxTokens: winner.candidate.maxTokens,
    thinking: selectThinkingLevel(winner.candidate.id, 'complex'),
    score: winner.score.toFixed(0),
    breakdown: winner.breakdown,
    allCandidates: scored.slice(0, 3).map(s => ({
      id: s.candidate.id,
      score: s.score.toFixed(0)
    }))
  };
}

/**
 * 为三个角色推荐完整配置
 */
export function recommendRoleConfig() {
  const pool = buildModelPool();
  const available = pool.all.length;

  if (available === 0) {
    return {
      available: 0,
      message: '⚠️ 未检测到可用模型，请先配置模型提供商',
      config: null
    };
  }

  // Coordinator 推荐（需要大窗口）
  const coordinator = recommendModelForRole('coordinator', pool);

  // Critic 推荐（排除 coordinator 已选）
  const critic = coordinator
    ? recommendModelForRole('critic', pool, [coordinator.model])
    : null;

  // Worker 推荐（排除前两个已选）
  const excludedSoFar = [coordinator?.model, critic?.model].filter(Boolean);
  const worker = recommendModelForRole('worker', pool, excludedSoFar);

  // 计算 fallback 链（每个角色从剩余模型中选 2-3 个）
  const allUsed = new Set([coordinator?.model, critic?.model, worker?.model].filter(Boolean));

  const fallbacks = pool.all
    .filter(m => !allUsed.has(m.id) && m.contextWindow >= 64000)
    .slice(0, 3)
    .map(m => m.id);

  const config = {
    coordinator: {
      primary: coordinator?.model || null,
      fallbackChain: fallbacks.slice(0, 2),
      thinking: coordinator?.thinking || 'medium'
    },
    critic: {
      primary: critic?.model || coordinator?.model || null,
      fallbackChain: fallbacks.slice(0, 2),
      thinking: critic?.thinking || 'high'
    },
    worker: {
      primary: worker?.model || coordinator?.model || null,
      fallbackChain: fallbacks.slice(0, 2),
      thinking: worker?.thinking || 'medium'
    }
  };

  return {
    available,
    providerCount: Object.keys(pool.byProvider).length,
    coordinator,
    critic,
    worker,
    config,
    recommendedAt: new Date().toISOString()
  };
}

// ===================== 角色配置读写 =====================

/**
 * 加载已确认的角色配置
 */
export function loadRoleConfig() {
  try {
    if (fs.existsSync(ROLE_CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(ROLE_CONFIG_FILE, 'utf-8'));
    }
  } catch (err) {
    console.error(`⚠️ 读取角色配置失败: ${err.message}`);
  }
  return null;
}

/**
 * 保存角色配置（用户确认后）
 */
export function saveRoleConfig(config) {
  try {
    config.confirmedAt = new Date().toISOString();
    config.version = (config.version || 0) + 1;
    fs.writeFileSync(ROLE_CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');

    // 同时保存当前快照
    saveSnapshot(getCurrentPoolSnapshot());

    return true;
  } catch (err) {
    console.error(`⚠️ 保存角色配置失败: ${err.message}`);
    return false;
  }
}

/**
 * 更新角色配置（修改单个角色）
 */
export function patchRoleConfig(role, modelId) {
  const config = loadRoleConfig() || { coordinator: {}, critic: {}, worker: {} };
  const thinkingCaps = checkModelThinking(modelId);
  
  config[role] = {
    ...config[role],
    primary: modelId,
    thinking: selectThinkingLevel(modelId, 'complex'),
    updatedAt: new Date().toISOString()
  };

  return saveRoleConfig(config);
}

// ===================== 首次引导 =====================

/**
 * 检查是否需要首次引导
 *
 * @returns {boolean}
 */
export function needsSetup() {
  const existingConfig = loadRoleConfig();
  return !existingConfig;
}

/**
 * 生成首次引导提示
 *
 * @returns {object} { isFirstRun: bool, recommendation, userPrompt }
 */
export function generateSetupPrompt() {
  const needsSetup = !fs.existsSync(ROLE_CONFIG_FILE);
  if (!needsSetup) {
    return { isFirstRun: false };
  }

  const recommendation = recommendRoleConfig();

  if (!recommendation.config) {
    return {
      isFirstRun: true,
      availableModels: recommendation.available,
      message: recommendation.message,
      userPrompt: null
    };
  }

  const { coordinator, critic, worker } = recommendation;

  const prompt = {
    type: 'model_setup_required',
    title: '🎯 检测到首次使用 — 请确认角色模型分配',
    description: `检测到 ${recommendation.available} 个可用模型，已自动推荐最佳配置：`,
    recommendations: {
      coordinator: {
        role: '🧠 Coordinator（协调器）',
        model: coordinator.shortId,
        fallbackChain: recommendation.config.coordinator.fallbackChain.map(id => id.split('/').pop()).join(' → '),
        thinking: coordinator.thinking,
        reason: `大窗口 ${coordinator.contextWindow} tokens，适合复杂任务分解`
      },
      critic: {
        role: '👁️ Critic（审核器）',
        model: critic.shortId,
        fallbackChain: recommendation.config.critic.fallbackChain.map(id => id.split('/').pop()).join(' → '),
        thinking: critic.thinking,
        reason: `强推理能力，适合深度审查`
      },
      worker: {
        role: '👷 Worker（执行器）',
        model: worker.shortId,
        fallbackChain: recommendation.config.worker.fallbackChain.map(id => id.split('/').pop()).join(' → '),
        thinking: worker.thinking,
        reason: `速度与质量平衡，适合批量任务`
      }
    },
    actions: [
      { id: 'confirm', label: '✅ 确认使用推荐配置', description: '直接采用上述配置' },
      { id: 'customize', label: '✏️ 手动调整', description: '自定义各角色模型' },
      { id: 'auto', label: '🤖 自动配置', description: '以后自动适配，不提示' }
    ]
  };

  return {
    isFirstRun: true,
    availableModels: recommendation.available,
    recommendation,
    userPrompt: prompt
  };
}

// ===================== 变更检测入口 =====================

/**
 * 主动检测模型池变更
 *
 * @returns {object} { action: 'none' | 'auto_adapt' | 'notify_user', recommendation, change }
 */
export function checkForModelChanges() {
  const oldSnapshot = loadSnapshot();
  const newSnapshot = getCurrentPoolSnapshot();
  const change = detectPoolChanges(oldSnapshot, newSnapshot);

  // 无变更
  if (change.changeRatio === 0) {
    return {
      action: 'none',
      change
    };
  }

  // 首次运行 → 生成引导
  if (change.isFirstRun) {
    const prompt = generateSetupPrompt();
    return {
      action: 'setup_required',
      change,
      setupPrompt: prompt.userPrompt
    };
  }

  // 小变更 → 自动适配
  if (change.isMinor) {
    // 检查是否需要重新推荐
    const currentConfig = loadRoleConfig();
    let needReconfigure = false;

    if (currentConfig) {
      // 检查当前使用的模型是否被移除
      const roles = ['coordinator', 'critic', 'worker'];
      for (const role of roles) {
        const primary = currentConfig[role]?.primary;
        if (primary && change.removed.includes(primary)) {
          needReconfigure = true;
          break;
        }
      }
    }

    if (needReconfigure) {
      const recommendation = recommendRoleConfig();
      return {
        action: 'auto_adapt',
        change,
        recommendation,
        log: '检测到已用模型被移除，自动重新配置'
      };
    }

    return {
      action: 'auto_adapt',
      change,
      log: '小幅变更，自动适配（无需用户介入）'
    };
  }

  // 大变更 → 通知用户确认
  if (change.isSignificant) {
    const recommendation = recommendRoleConfig();
    return {
      action: 'notify_user',
      change,
      recommendation,
      log: `模型池大幅变更（+${change.added.length}/-${change.removed.length}），建议重新配置`
    };
  }

  return {
    action: 'none',
    change
  };
}

// ===================== 格式化展示 =====================

/**
 * 格式化为可读推荐报告
 */
export function formatRecommendationReport(recommendation) {
  if (!recommendation || !recommendation.config) {
    return '❌ 无可用模型进行推荐';
  }

  const bar = '-'.repeat(58);
  let report = '';
  report += bar + '\n';
  report += '  Role Model Recommendation Report\n';
  report += bar + '\n';

  // Coordinator
  const c = recommendation.coordinator;
  report += '  Coordinator: ' + c.shortId + '\n';
  report += '    Context Window: ' + (c.contextWindow / 1024).toFixed(0) + 'K tokens, Max Output: ' + c.maxTokens + ' tokens\n';
  report += '    Thinking: ' + c.thinking + ', Score: ' + c.score + '\n';

  // Critic
  const cr = recommendation.critic;
  report += '  Critic: ' + cr.shortId + '\n';
  report += '    Context Window: ' + (cr.contextWindow / 1024).toFixed(0) + 'K tokens, Max Output: ' + cr.maxTokens + ' tokens\n';
  report += '    Thinking: ' + cr.thinking + ', Score: ' + cr.score + '\n';

  // Worker
  const w = recommendation.worker;
  report += '  Worker: ' + w.shortId + '\n';
  report += '    Context Window: ' + (w.contextWindow / 1024).toFixed(0) + 'K tokens, Max Output: ' + w.maxTokens + ' tokens\n';
  report += '    Thinking: ' + w.thinking + ', Score: ' + w.score + '\n';

  // Fallbacks
  report += bar + '\n';
  report += '  Fallback Chain:';
  const fallbacks = recommendation.config.coordinator.fallbackChain;
  fallbacks.forEach((fb, i) => {
    const shortName = fb.split('/').pop();
    report += '\n    ' + (i + 1) + '. ' + shortName;
  });

  report += '\n' + bar;

  return report;
}

/**
 * 格式化变更通知
 */
export function formatChangeNotification(change) {
  let notification = '';
  notification += 'Model Pool Change Detection\n';
  notification += '---' + '\n';
  notification += '  ' + change.summary + '\n';
  notification += '  Change Ratio: ' + (change.changeRatio * 100).toFixed(0) + '%' + '\n';

  if (change.added.length > 0) {
    notification += '\n  Added Models:\n';
    change.added.forEach(m => {
      notification += '    - ' + m + '\n';
    });
  }

  if (change.removed.length > 0) {
    notification += '\n  Removed Models:\n';
    change.removed.forEach(m => {
      notification += '    - ' + m + '\n';
    });
  }

  if (change.isSignificant) {
    notification += '\n  Significant change! Recommend running model setup to reconfigure.';
  }

  return notification;
}

// ===================== 角色模型分配（供 executor 调用）=====================

/**
 * 根据角色配置生成 spawn 参数
 * 覆盖 modelSelector 的自动选择，使用用户确认的角色-模型映射
 *
 * @param {string} agentRole - 代理角色名
 * @param {object} options - 选项
 * @param {boolean} options.forceRoleConfig - 是否强制使用角色配置
 * @param {object} options.pool - 可选的模型池
 * @returns {object|null} { model, thinking, fallbackChain, source }
 */
export function buildRoleSpawnParams(agentRole, options = {}) {
  const roleConfig = loadRoleConfig();
  if (!roleConfig || !options.forceRoleConfig) {
    // 没有用户配置或不强制使用 → 回退到自动
    return null;
  }

  // 映射代理角色名到配置角色
  const roleMapping = {
    'Research_Analyst': 'worker',
    'Technical_Specialist': 'worker',
    'Strategy_Analyst': 'worker',
    'Critic': 'critic',
    'Coordinator': 'coordinator'
  };

  const configRole = roleMapping[agentRole] || agentRole.toLowerCase();
  const roleConf = roleConfig[configRole];
  if (!roleConf?.primary) return null;

  const modelId = roleConf.primary;
  const thinking = roleConf.thinking || selectThinkingLevel(modelId, 'medium');

  // Thinking 容错检查
  const caps = checkModelThinking(modelId);
  if (!caps.supportsThinking) {
    // 模型不支持 thinking，尝试 fallback
    const fbChain = roleConf.fallbackChain || [];
    for (const fbId of fbChain) {
      const fbCaps = checkModelThinking(fbId);
      if (fbCaps.supportsThinking) {
        return {
          model: fbId,
          thinking: fbCaps.defaultMode,
          fallbackChain: fbChain,
          source: 'role_config_with_thinking_fallback',
          reason: `${modelId} 不支持 thinking，使用 ${fbId}`
        };
      }
    }
    return {
      model: modelId,
      thinking: null, // thinking: off
      fallbackChain: fbChain,
      source: 'role_config_thinking_off',
      reason: `${modelId} 不支持 thinking，已关闭`
    };
  }

  return {
    model: modelId,
    thinking,
    fallbackChain: roleConf.fallbackChain || [],
    source: 'role_config',
    reason: `使用用户配置的角色-模型映射`
  };
}

/**
 * 确保 Coordinator 和 Critic 的 thinking 被正确启用
 * 在流程启动时调用，返回修正后的 spawn 参数
 *
 * @param {array} spawns - 原始 spawn 参数数组
 * @returns {array} 修正后的 spawn 参数
 */
export function ensureThinkingEnabled(spawns) {
  return spawns.map(spawn => {
    const label = spawn.label || '';
    const isCoordinator = label.toLowerCase().includes('coordinator');
    const isCritic = label.toLowerCase().includes('critic');

    if (!isCoordinator && !isCritic) return spawn; // 只在 coordinator 和 critic 上开启 thinking

    const modelId = spawn.model;
    const defaultThinking = isCritic ? 'high' : 'medium';

    // 使用 thinking capabilities 进行安全选择
    const caps = checkModelThinking(modelId);
    if (!caps.supportsThinking) {
      // 找支持 thinking 的 fallback
      const pool = buildModelPool();
      const candidate = pool.all.find(m => {
        const mCaps = checkModelThinking(m.id);
        return mCaps.supportsThinking && m.contextWindow >= 64000;
      });

      if (candidate) {
        const cCaps = checkModelThinking(candidate.id);
        console.log(`⚠️ ${modelId} 不支持 thinking，切换到 ${candidate.id}`);
        return {
          ...spawn,
          model: candidate.id,
          thinking: cCaps.defaultMode || defaultThinking
        };
      }

      console.log(`⚠️ ${modelId} 不支持 thinking，尝试关闭后执行`);
      return {
        ...spawn,
        thinking: undefined
      };
    }

    // 模型支持 thinking，选择最佳级别
    const safeThinking = selectThinkingLevel(modelId, isCritic ? 'critical' : 'complex');

    return {
      ...spawn,
      thinking: safeThinking || defaultThinking
    };
  });
}

// ===================== 导出 =====================

export default {
  detectPoolChanges,
  recommendRoleConfig,
  loadRoleConfig,
  saveRoleConfig,
  patchRoleConfig,
  needsSetup,
  generateSetupPrompt,
  checkForModelChanges,
  formatRecommendationReport,
  formatChangeNotification,
  buildRoleSpawnParams,
  ensureThinkingEnabled,
  getCurrentPoolSnapshot,
  loadSnapshot,
  saveSnapshot
};
