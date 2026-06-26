#!/usr/bin/env node
/**
 * Memory Decay & Promotion Engine - 衰减和晋升引擎
 *
 * 核心机制：
 * 1. Weibull 衰减模型：重要记忆衰减更慢
 * 2. 三层晋升机制：Peripheral ↔ Working ↔ Core
 * 3. 访问强化：频繁访问的记忆获得强化（类似间隔重复）
 *
 * 衰减公式：
 * score = base_score × decay_factor × (1 + importance × 0.5)
 * decay_factor = exp(-days_since_last_access / half_life)
 * half_life = 30 天（普通记忆）或 90 天（重要记忆）
 *
 * 晋升规则：
 * - Peripheral → Working: access_count >= 3 或 importance >= 0.6
 * - Working → Core: access_count >= 10 或 importance >= 0.8
 * - Core → Working: 90 天未访问且 importance < 0.7
 * - Working → Peripheral: 60 天未访问且 importance < 0.5
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const MEMORY_INDEX = path.join(WORKSPACE, 'memory/metadata/memory-index.json');

/**
 * 计算衰减因子
 */
function calculateDecayFactor(lastAccess, halfLife) {
  const now = new Date();
  const lastAccessDate = new Date(lastAccess);
  const daysSinceAccess = (now - lastAccessDate) / (1000 * 60 * 60 * 24);

  // Weibull 衰减：exp(-days / half_life)
  return Math.exp(-daysSinceAccess / halfLife);
}

/**
 * 计算记忆得分
 */
function calculateMemoryScore(memory) {
  const { importance, last_access, decay_half_life } = memory;

  // 基础分数 = 重要性
  const baseScore = importance;

  // 衰减因子
  const decayFactor = calculateDecayFactor(last_access, decay_half_life);

  // 最终得分 = 基础分数 × 衰减因子 × (1 + 重要性加成)
  const score = baseScore * decayFactor * (1 + importance * 0.5);

  return {
    score,
    baseScore,
    decayFactor,
    daysSinceAccess: (new Date() - new Date(last_access)) / (1000 * 60 * 60 * 24)
  };
}

/**
 * 判断是否应该晋升
 */
function shouldPromote(memory, currentTier) {
  const { access_count, importance } = memory;
  const daysSinceAccess = (new Date() - new Date(memory.last_access)) / (1000 * 60 * 60 * 24);

  switch (currentTier) {
    case 'peripheral':
      // Peripheral → Working
      return access_count >= 3 || importance >= 0.6;

    case 'working':
      // Working → Core
      return access_count >= 10 || importance >= 0.8;

    case 'core':
      // Core 不再晋升
      return false;

    default:
      return false;
  }
}

/**
 * 判断是否应该降级
 */
function shouldDemote(memory, currentTier) {
  const { importance } = memory;
  const daysSinceAccess = (new Date() - new Date(memory.last_access)) / (1000 * 60 * 60 * 24);

  switch (currentTier) {
    case 'core':
      // Core → Working: 90 天未访问且重要性 < 0.7
      return daysSinceAccess >= 90 && importance < 0.7;

    case 'working':
      // Working → Peripheral: 60 天未访问且重要性 < 0.5
      return daysSinceAccess >= 60 && importance < 0.5;

    case 'peripheral':
      // Peripheral 不再降级（可以考虑归档或删除）
      return false;

    default:
      return false;
  }
}

/**
 * 更新记忆层级
 */
function updateMemoryTier(memory) {
  const currentTier = memory.tier;
  let newTier = currentTier;
  let action = 'KEEP';

  if (shouldPromote(memory, currentTier)) {
    // 晋升
    if (currentTier === 'peripheral') {
      newTier = 'working';
      action = 'PROMOTE';
    } else if (currentTier === 'working') {
      newTier = 'core';
      action = 'PROMOTE';
    }
  } else if (shouldDemote(memory, currentTier)) {
    // 降级
    if (currentTier === 'core') {
      newTier = 'working';
      action = 'DEMOTE';
    } else if (currentTier === 'working') {
      newTier = 'peripheral';
      action = 'DEMOTE';
    }
  }

  return { newTier, action };
}

/**
 * 记录访问（强化记忆）
 */
function recordAccess(memoryId) {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memory = index.memories[memoryId];

  if (!memory) {
    console.error(`记忆 ${memoryId} 不存在`);
    return null;
  }

  // 更新访问计数和时间
  memory.access_count = (memory.access_count || 0) + 1;
  memory.last_access = new Date().toISOString();

  // 计算新得分
  const scoreInfo = calculateMemoryScore(memory);
  memory.current_score = scoreInfo.score;

  // 检查是否需要晋升
  const { newTier, action } = updateMemoryTier(memory);

  if (action === 'PROMOTE') {
    console.log(`✓ 记忆 ${memoryId} 晋升: ${memory.tier} → ${newTier}`);
    memory.tier = newTier;
    memory.promoted_at = new Date().toISOString();
  }

  // 更新索引
  index.memories[memoryId] = memory;
  fs.writeFileSync(MEMORY_INDEX, JSON.stringify(index, null, 2));

  return memory;
}

/**
 * 批量更新所有记忆的衰减状态
 */
function updateAllMemories() {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  const stats = {
    total: memories.length,
    promoted: 0,
    demoted: 0,
    kept: 0,
    byTier: { core: 0, working: 0, peripheral: 0 }
  };

  console.log(`开始更新 ${memories.length} 条记忆的衰减状态...\n`);

  memories.forEach(memory => {
    // 计算得分
    const scoreInfo = calculateMemoryScore(memory);
    memory.current_score = scoreInfo.score;
    memory.decay_factor = scoreInfo.decayFactor;

    // 更新层级
    const { newTier, action } = updateMemoryTier(memory);

    if (action === 'PROMOTE') {
      console.log(`↑ ${memory.id}: ${memory.tier} → ${newTier} (访问${memory.access_count}次, 重要性${memory.importance.toFixed(2)})`);
      memory.tier = newTier;
      memory.promoted_at = new Date().toISOString();
      stats.promoted++;
    } else if (action === 'DEMOTE') {
      console.log(`↓ ${memory.id}: ${memory.tier} → ${newTier} (${scoreInfo.daysSinceAccess.toFixed(0)}天未访问)`);
      memory.tier = newTier;
      memory.demoted_at = new Date().toISOString();
      stats.demoted++;
    } else {
      stats.kept++;
    }

    stats.byTier[memory.tier]++;

    // 更新索引
    index.memories[memory.id] = memory;
  });

  // 重建层级索引
  index.tiers = { core: [], working: [], peripheral: [] };
  Object.values(index.memories).forEach(mem => {
    index.tiers[mem.tier].push(mem.id);
  });

  index.last_decay_update = new Date().toISOString();
  fs.writeFileSync(MEMORY_INDEX, JSON.stringify(index, null, 2));

  console.log('\n=== 衰减更新统计 ===');
  console.log(`总计: ${stats.total} 条`);
  console.log(`晋升: ${stats.promoted} 条`);
  console.log(`降级: ${stats.demoted} 条`);
  console.log(`保持: ${stats.kept} 条`);
  console.log('\n=== 层级分布 ===');
  console.log(`Core: ${stats.byTier.core} 条`);
  console.log(`Working: ${stats.byTier.working} 条`);
  console.log(`Peripheral: ${stats.byTier.peripheral} 条`);

  return stats;
}

/**
 * 获取应该加载的记忆（按层级和得分排序）
 */
function getMemoriesToLoad(tier = 'all', limit = 10) {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  let memories = Object.values(index.memories);

  // 过滤层级
  if (tier !== 'all') {
    memories = memories.filter(m => m.tier === tier);
  }

  // 按得分排序
  memories.sort((a, b) => {
    const scoreA = calculateMemoryScore(a).score;
    const scoreB = calculateMemoryScore(b).score;
    return scoreB - scoreA;
  });

  return memories.slice(0, limit);
}

/**
 * 归档长期未访问的 Peripheral 记忆
 */
function archiveOldMemories(daysThreshold = 180) {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  const toArchive = memories.filter(mem => {
    const daysSinceAccess = (new Date() - new Date(mem.last_access)) / (1000 * 60 * 60 * 24);
    return mem.tier === 'peripheral' && daysSinceAccess >= daysThreshold;
  });

  if (toArchive.length === 0) {
    console.log('没有需要归档的记忆');
    return;
  }

  console.log(`发现 ${toArchive.length} 条长期未访问的记忆，准备归档...`);

  // 创建归档文件
  const archiveDir = path.join(WORKSPACE, 'memory/archive');
  if (!fs.existsSync(archiveDir)) {
    fs.mkdirSync(archiveDir, { recursive: true });
  }

  const archiveFile = path.join(archiveDir, `archive-${new Date().toISOString().split('T')[0]}.json`);
  fs.writeFileSync(archiveFile, JSON.stringify(toArchive, null, 2));

  // 从索引中移除
  toArchive.forEach(mem => {
    delete index.memories[mem.id];
  });

  // 重建索引
  index.tiers = { core: [], working: [], peripheral: [] };
  Object.values(index.memories).forEach(mem => {
    index.tiers[mem.tier].push(mem.id);
  });

  index.total_memories = Object.keys(index.memories).length;
  fs.writeFileSync(MEMORY_INDEX, JSON.stringify(index, null, 2));

  console.log(`✓ 已归档 ${toArchive.length} 条记忆到 ${archiveFile}`);
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0] || 'update';

  switch (command) {
    case 'update':
      // 更新所有记忆的衰减状态
      updateAllMemories();
      break;

    case 'access':
      // 记录访问
      if (args.length < 2) {
        console.error('用法: node memory-decay.js access <记忆ID>');
        process.exit(1);
      }
      recordAccess(args[1]);
      break;

    case 'load':
      // 获取应该加载的记忆
      const tier = args[1] || 'all';
      const limit = parseInt(args[2]) || 10;
      const memories = getMemoriesToLoad(tier, limit);
      console.log(JSON.stringify(memories, null, 2));
      break;

    case 'archive':
      // 归档旧记忆
      const daysThreshold = parseInt(args[1]) || 180;
      archiveOldMemories(daysThreshold);
      break;

    default:
      console.log('用法:');
      console.log('  node memory-decay.js update              # 更新所有记忆的衰减状态');
      console.log('  node memory-decay.js access <记忆ID>      # 记录访问（强化记忆）');
      console.log('  node memory-decay.js load [tier] [limit] # 获取应该加载的记忆');
      console.log('  node memory-decay.js archive [days]      # 归档长期未访问的记忆');
      process.exit(1);
  }
}

module.exports = {
  calculateMemoryScore,
  updateMemoryTier,
  recordAccess,
  updateAllMemories,
  getMemoriesToLoad,
  archiveOldMemories
};
