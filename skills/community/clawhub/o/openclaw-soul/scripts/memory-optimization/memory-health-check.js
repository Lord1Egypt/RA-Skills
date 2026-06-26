#!/usr/bin/env node
/**
 * Memory Health Check - 记忆系统健康检查
 *
 * 检查项：
 * 1. 记忆质量：分类准确性、重要性分布
 * 2. 去重率：重复记忆比例
 * 3. 衰减状态：各层级分布、衰减因子
 * 4. 索引完整性：L0/L1/L2 索引是否存在且最新
 * 5. 访问模式：热门记忆、冷门记忆
 * 6. 存储效率：Token 使用情况
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const MEMORY_INDEX = path.join(WORKSPACE, 'memory/metadata/memory-index.json');
const L0_INDEX = path.join(WORKSPACE, 'memory/metadata/L0-index.md');
const L1_INDEX = path.join(WORKSPACE, 'memory/metadata/L1-index.md');
const L2_INDEX = path.join(WORKSPACE, 'memory/metadata/L2-index.md');

/**
 * 检查记忆质量
 */
function checkMemoryQuality() {
  console.log('\n=== 1. 记忆质量检查 ===\n');

  if (!fs.existsSync(MEMORY_INDEX)) {
    console.log('❌ 记忆索引不存在');
    return { status: 'error', score: 0 };
  }

  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  if (memories.length === 0) {
    console.log('⚠️  暂无记忆');
    return { status: 'empty', score: 0 };
  }

  // 分类分布
  const categoryDist = {};
  memories.forEach(mem => {
    categoryDist[mem.category] = (categoryDist[mem.category] || 0) + 1;
  });

  console.log('分类分布:');
  Object.entries(categoryDist).forEach(([cat, count]) => {
    const percentage = (count / memories.length * 100).toFixed(1);
    console.log(`  ${cat}: ${count} 条 (${percentage}%)`);
  });

  // 重要性分布
  const importanceDist = {
    high: memories.filter(m => m.importance >= 0.8).length,
    medium: memories.filter(m => m.importance >= 0.5 && m.importance < 0.8).length,
    low: memories.filter(m => m.importance < 0.5).length
  };

  console.log('\n重要性分布:');
  console.log(`  高 (≥0.8): ${importanceDist.high} 条`);
  console.log(`  中 (0.5-0.8): ${importanceDist.medium} 条`);
  console.log(`  低 (<0.5): ${importanceDist.low} 条`);

  // 质量评分
  const qualityScore = (
    (importanceDist.high * 1.0 + importanceDist.medium * 0.6 + importanceDist.low * 0.3) / memories.length
  );

  console.log(`\n质量评分: ${(qualityScore * 100).toFixed(1)}/100`);

  return {
    status: 'ok',
    score: qualityScore,
    total: memories.length,
    categoryDist,
    importanceDist
  };
}

/**
 * 检查去重率
 */
function checkDeduplication() {
  console.log('\n=== 2. 去重率检查 ===\n');

  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  // 统计合并记忆
  const merged = memories.filter(m => m.synthesized_from || m.timeline);
  const mergedCount = merged.length;
  const totalCount = memories.length;

  const dedupRate = totalCount > 0 ? (mergedCount / totalCount * 100).toFixed(1) : 0;

  console.log(`总记忆数: ${totalCount}`);
  console.log(`合并记忆: ${mergedCount}`);
  console.log(`去重率: ${dedupRate}%`);

  if (dedupRate < 10) {
    console.log('⚠️  去重率较低，可能存在重复记忆');
  } else {
    console.log('✓ 去重率正常');
  }

  return {
    status: 'ok',
    dedupRate: parseFloat(dedupRate),
    mergedCount,
    totalCount
  };
}

/**
 * 检查衰减状态
 */
function checkDecayStatus() {
  console.log('\n=== 3. 衰减状态检查 ===\n');

  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  // 层级分布
  const tierDist = {
    core: index.tiers.core.length,
    working: index.tiers.working.length,
    peripheral: index.tiers.peripheral.length
  };

  console.log('层级分布:');
  console.log(`  Core: ${tierDist.core} 条`);
  console.log(`  Working: ${tierDist.working} 条`);
  console.log(`  Peripheral: ${tierDist.peripheral} 条`);

  // 平均衰减因子
  const avgDecayFactor = memories.reduce((sum, m) => sum + (m.decay_factor || 1), 0) / memories.length;
  console.log(`\n平均衰减因子: ${avgDecayFactor.toFixed(3)}`);

  // 长期未访问的记忆
  const now = new Date();
  const staleMemories = memories.filter(m => {
    const daysSince = (now - new Date(m.last_access)) / (1000 * 60 * 60 * 24);
    return daysSince > 90;
  });

  console.log(`长期未访问 (>90天): ${staleMemories.length} 条`);

  if (staleMemories.length > memories.length * 0.3) {
    console.log('⚠️  超过 30% 的记忆长期未访问，建议归档');
  }

  return {
    status: 'ok',
    tierDist,
    avgDecayFactor,
    staleCount: staleMemories.length
  };
}

/**
 * 检查索引完整性
 */
function checkIndexIntegrity() {
  console.log('\n=== 4. 索引完整性检查 ===\n');

  const checks = {
    l0: fs.existsSync(L0_INDEX),
    l1: fs.existsSync(L1_INDEX),
    l2: fs.existsSync(L2_INDEX)
  };

  console.log(`L0 索引: ${checks.l0 ? '✓ 存在' : '❌ 缺失'}`);
  console.log(`L1 索引: ${checks.l1 ? '✓ 存在' : '❌ 缺失'}`);
  console.log(`L2 索引: ${checks.l2 ? '✓ 存在' : '❌ 缺失'}`);

  // 检查索引更新时间
  if (checks.l0) {
    const l0Stat = fs.statSync(L0_INDEX);
    const l0Age = (new Date() - l0Stat.mtime) / (1000 * 60 * 60);
    console.log(`\nL0 索引更新时间: ${l0Age.toFixed(1)} 小时前`);

    if (l0Age > 24) {
      console.log('⚠️  L0 索引超过 24 小时未更新，建议重建');
    }
  }

  const allExist = checks.l0 && checks.l1 && checks.l2;

  return {
    status: allExist ? 'ok' : 'incomplete',
    checks
  };
}

/**
 * 检查访问模式
 */
function checkAccessPatterns() {
  console.log('\n=== 5. 访问模式检查 ===\n');

  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  // 按访问次数排序
  const sorted = memories.sort((a, b) => b.access_count - a.access_count);

  // 热门记忆（访问次数 > 5）
  const hotMemories = sorted.filter(m => m.access_count > 5);
  console.log(`热门记忆 (访问>5次): ${hotMemories.length} 条`);

  if (hotMemories.length > 0) {
    console.log('\nTop 5 热门记忆:');
    hotMemories.slice(0, 5).forEach((m, i) => {
      const summary = m.content.substring(0, 50).replace(/\n/g, ' ');
      console.log(`  ${i + 1}. [${m.id}] ${summary}... (访问${m.access_count}次)`);
    });
  }

  // 冷门记忆（从未访问）
  const coldMemories = memories.filter(m => m.access_count === 0);
  console.log(`\n冷门记忆 (从未访问): ${coldMemories.length} 条`);

  return {
    status: 'ok',
    hotCount: hotMemories.length,
    coldCount: coldMemories.length
  };
}

/**
 * 检查存储效率
 */
function checkStorageEfficiency() {
  console.log('\n=== 6. 存储效率检查 ===\n');

  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memories = Object.values(index.memories);

  // 计算总 Token 数（粗略估算：字符数 / 4）
  const totalChars = memories.reduce((sum, m) => sum + m.content.length, 0);
  const totalTokens = Math.ceil(totalChars / 4);

  console.log(`总字符数: ${totalChars.toLocaleString()}`);
  console.log(`估算 Token 数: ${totalTokens.toLocaleString()}`);

  // L0 索引大小
  if (fs.existsSync(L0_INDEX)) {
    const l0Content = fs.readFileSync(L0_INDEX, 'utf-8');
    const l0Tokens = Math.ceil(l0Content.length / 4);
    console.log(`L0 索引: ${l0Tokens.toLocaleString()} tokens`);

    if (l0Tokens > 1000) {
      console.log('⚠️  L0 索引超过 1000 tokens，建议精简');
    }
  }

  // 平均每条记忆的大小
  const avgTokens = Math.ceil(totalTokens / memories.length);
  console.log(`\n平均每条记忆: ${avgTokens} tokens`);

  return {
    status: 'ok',
    totalTokens,
    avgTokens
  };
}

/**
 * 生成健康报告
 */
function generateHealthReport() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║   记忆系统健康检查                     ║');
  console.log('╚════════════════════════════════════════╝');
  console.log(`\n时间: ${new Date().toISOString()}\n`);

  const results = {
    quality: checkMemoryQuality(),
    dedup: checkDeduplication(),
    decay: checkDecayStatus(),
    index: checkIndexIntegrity(),
    access: checkAccessPatterns(),
    storage: checkStorageEfficiency()
  };

  // 总体评分
  console.log('\n╔════════════════════════════════════════╗');
  console.log('║   总体评分                             ║');
  console.log('╚════════════════════════════════════════╝\n');

  const scores = {
    quality: results.quality.score * 100,
    dedup: results.dedup.dedupRate,
    decay: results.decay.avgDecayFactor * 100,
    index: results.index.status === 'ok' ? 100 : 50,
    access: (results.access.hotCount / (results.quality.total || 1)) * 100,
    storage: results.storage.avgTokens < 200 ? 100 : 50
  };

  Object.entries(scores).forEach(([key, score]) => {
    const bar = '█'.repeat(Math.floor(score / 10)) + '░'.repeat(10 - Math.floor(score / 10));
    console.log(`${key.padEnd(10)}: ${bar} ${score.toFixed(1)}`);
  });

  const overallScore = Object.values(scores).reduce((sum, s) => sum + s, 0) / Object.keys(scores).length;
  console.log(`\n总分: ${overallScore.toFixed(1)}/100`);

  if (overallScore >= 80) {
    console.log('✓ 记忆系统健康状况良好');
  } else if (overallScore >= 60) {
    console.log('⚠️  记忆系统需要优化');
  } else {
    console.log('❌ 记忆系统存在严重问题');
  }

  // 建议
  console.log('\n╔════════════════════════════════════════╗');
  console.log('║   优化建议                             ║');
  console.log('╚════════════════════════════════════════╝\n');

  if (results.dedup.dedupRate < 10) {
    console.log('• 运行去重: node memory-dedup.js --check-all');
  }

  if (results.index.status !== 'ok') {
    console.log('• 重建索引: node memory-index-builder.js build');
  }

  if (results.decay.staleCount > results.quality.total * 0.3) {
    console.log('• 归档旧记忆: node memory-decay.js archive 90');
  }

  if (results.storage.avgTokens > 200) {
    console.log('• 精简记忆内容，提取关键信息');
  }

  console.log('\n');

  return results;
}

// CLI 入口
if (require.main === module) {
  try {
    generateHealthReport();
  } catch (error) {
    console.error('健康检查失败:', error.message);
    process.exit(1);
  }
}

module.exports = { generateHealthReport };
