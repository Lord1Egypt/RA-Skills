#!/usr/bin/env node
/**
 * Memory Deduplication - 智能去重器
 * 两阶段去重：
 * 1. 向量相似度预过滤（≥0.7）
 * 2. LLM 语义决策（CREATE/MERGE/SKIP）
 *
 * 合并策略：
 * - profiles: 总是合并
 * - preferences: 总是合并
 * - events/cases: 仅追加时间线
 * - entities: 更新属性
 * - patterns: 合并并提炼
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const MEMORY_INDEX = path.join(WORKSPACE, 'memory/metadata/memory-index.json');

/**
 * 计算向量相似度（使用 openclaw memory search）
 */
async function findSimilarMemories(content, threshold = 0.7) {
  try {
    // 使用 openclaw 的向量搜索
    const result = execSync(
      `openclaw memory search "${content.replace(/"/g, '\\"')}" --limit 10 --format json`,
      { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 }
    );

    const results = JSON.parse(result);
    return results.filter(r => r.similarity >= threshold);
  } catch (error) {
    console.error('向量搜索失败:', error.message);
    return [];
  }
}

/**
 * LLM 语义决策：CREATE / MERGE / SKIP
 */
async function decideMergeStrategy(newMemory, existingMemory) {
  const prompt = `你是记忆去重专家。请判断两条记忆是否应该合并。

新记忆：
${JSON.stringify(newMemory, null, 2)}

已有记忆：
${JSON.stringify(existingMemory, null, 2)}

请以 JSON 格式返回决策：
{
  "action": "CREATE | MERGE | SKIP",
  "reasoning": "决策理由",
  "merge_strategy": "REPLACE | APPEND | UPDATE | SYNTHESIZE",
  "merged_content": "如果选择 MERGE，这里是合并后的内容"
}

决策规则：
- CREATE: 两条记忆内容不同，应该独立保存
- MERGE: 两条记忆内容相似或互补，应该合并
- SKIP: 新记忆是重复或噪音，应该丢弃

合并策略：
- REPLACE: 新记忆完全替代旧记忆（用于更正错误）
- APPEND: 追加到时间线（用于 events/cases）
- UPDATE: 更新部分字段（用于 entities）
- SYNTHESIZE: 提炼综合（用于 profiles/preferences/patterns）

只返回 JSON，不要其他内容。`;

  try {
    const result = execSync(
      `echo ${JSON.stringify(prompt)} | openclaw chat --model sonnet --format json`,
      { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 }
    );

    return JSON.parse(result.trim());
  } catch (error) {
    console.error('LLM 决策失败:', error.message);
    // Fallback: 基于类别的默认策略
    return fallbackDecision(newMemory, existingMemory);
  }
}

/**
 * Fallback 决策器
 */
function fallbackDecision(newMemory, existingMemory) {
  const category = newMemory.category;

  // 基于类别的默认策略
  const strategies = {
    profiles: { action: 'MERGE', merge_strategy: 'SYNTHESIZE' },
    preferences: { action: 'MERGE', merge_strategy: 'SYNTHESIZE' },
    entities: { action: 'MERGE', merge_strategy: 'UPDATE' },
    events: { action: 'MERGE', merge_strategy: 'APPEND' },
    cases: { action: 'MERGE', merge_strategy: 'APPEND' },
    patterns: { action: 'MERGE', merge_strategy: 'SYNTHESIZE' }
  };

  const strategy = strategies[category] || { action: 'CREATE', merge_strategy: null };

  return {
    action: strategy.action,
    reasoning: `Fallback: ${category} 类型默认使用 ${strategy.action} 策略`,
    merge_strategy: strategy.merge_strategy,
    merged_content: null
  };
}

/**
 * 执行合并
 */
function executeMerge(newMemory, existingMemory, decision) {
  const { merge_strategy, merged_content } = decision;

  switch (merge_strategy) {
    case 'REPLACE':
      // 完全替换
      return {
        ...newMemory,
        id: existingMemory.id, // 保留原 ID
        created_at: existingMemory.created_at,
        access_count: existingMemory.access_count,
        replaced_at: new Date().toISOString()
      };

    case 'APPEND':
      // 追加时间线
      return {
        ...existingMemory,
        content: `${existingMemory.content}\n\n[${newMemory.timestamp}] ${newMemory.content}`,
        last_updated: new Date().toISOString(),
        timeline: [
          ...(existingMemory.timeline || []),
          { timestamp: newMemory.timestamp, content: newMemory.content }
        ]
      };

    case 'UPDATE':
      // 更新字段
      return {
        ...existingMemory,
        ...newMemory,
        id: existingMemory.id,
        created_at: existingMemory.created_at,
        access_count: existingMemory.access_count,
        entities: [...new Set([...existingMemory.entities, ...newMemory.entities])],
        tags: [...new Set([...existingMemory.tags, ...newMemory.tags])],
        last_updated: new Date().toISOString()
      };

    case 'SYNTHESIZE':
      // 提炼综合（使用 LLM 生成的 merged_content）
      return {
        ...existingMemory,
        content: merged_content || `${existingMemory.content}\n${newMemory.content}`,
        importance: Math.max(existingMemory.importance, newMemory.importance),
        entities: [...new Set([...existingMemory.entities, ...newMemory.entities])],
        tags: [...new Set([...existingMemory.tags, ...newMemory.tags])],
        last_updated: new Date().toISOString(),
        synthesized_from: [
          ...(existingMemory.synthesized_from || [existingMemory.id]),
          newMemory.id
        ]
      };

    default:
      return existingMemory;
  }
}

/**
 * 处理单条记忆的去重
 */
async function deduplicateMemory(newMemory) {
  console.log(`\n检查记忆去重: ${newMemory.id}`);

  // 1. 向量相似度预过滤
  const similarMemories = await findSimilarMemories(newMemory.content, 0.7);

  if (similarMemories.length === 0) {
    console.log('  ✓ 无相似记忆，创建新记忆');
    return { action: 'CREATE', memory: newMemory };
  }

  console.log(`  发现 ${similarMemories.length} 条相似记忆`);

  // 2. 逐条进行 LLM 语义决策
  for (const similar of similarMemories) {
    // 加载完整的已有记忆
    const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
    const existingMemory = index.memories[similar.id];

    if (!existingMemory) continue;

    console.log(`  对比记忆 ${similar.id} (相似度: ${similar.similarity.toFixed(2)})`);

    const decision = await decideMergeStrategy(newMemory, existingMemory);
    console.log(`  决策: ${decision.action} (${decision.reasoning})`);

    if (decision.action === 'MERGE') {
      const merged = executeMerge(newMemory, existingMemory, decision);
      console.log(`  ✓ 合并完成，策略: ${decision.merge_strategy}`);
      return { action: 'MERGE', memory: merged, original_id: existingMemory.id };
    } else if (decision.action === 'SKIP') {
      console.log('  ✓ 跳过重复记忆');
      return { action: 'SKIP', memory: null };
    }
  }

  // 3. 如果所有相似记忆都不需要合并，创建新记忆
  console.log('  ✓ 创建新记忆');
  return { action: 'CREATE', memory: newMemory };
}

/**
 * 批量去重
 */
async function batchDeduplicate(memories) {
  const results = {
    created: [],
    merged: [],
    skipped: []
  };

  for (const memory of memories) {
    try {
      const result = await deduplicateMemory(memory);

      switch (result.action) {
        case 'CREATE':
          results.created.push(result.memory);
          break;
        case 'MERGE':
          results.merged.push(result.memory);
          break;
        case 'SKIP':
          results.skipped.push(memory.id);
          break;
      }
    } catch (error) {
      console.error(`处理记忆 ${memory.id} 失败:`, error.message);
    }
  }

  return results;
}

/**
 * 更新记忆索引
 */
function updateMemoryIndex(results) {
  let index = { memories: {}, tiers: { core: [], working: [], peripheral: [] }, categories: {} };

  if (fs.existsSync(MEMORY_INDEX)) {
    index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  }

  // 添加新创建的记忆
  results.created.forEach(mem => {
    index.memories[mem.id] = mem;
  });

  // 更新合并的记忆
  results.merged.forEach(mem => {
    index.memories[mem.id] = mem;
  });

  // 重建索引
  index.tiers = { core: [], working: [], peripheral: [] };
  index.categories = {};

  Object.values(index.memories).forEach(mem => {
    // 更新层级索引
    if (!index.tiers[mem.tier].includes(mem.id)) {
      index.tiers[mem.tier].push(mem.id);
    }

    // 更新分类索引
    if (!index.categories[mem.category]) {
      index.categories[mem.category] = [];
    }
    if (!index.categories[mem.category].includes(mem.id)) {
      index.categories[mem.category].push(mem.id);
    }
  });

  index.total_memories = Object.keys(index.memories).length;
  index.last_updated = new Date().toISOString();

  fs.writeFileSync(MEMORY_INDEX, JSON.stringify(index, null, 2));

  console.log('\n=== 去重统计 ===');
  console.log(`创建: ${results.created.length} 条`);
  console.log(`合并: ${results.merged.length} 条`);
  console.log(`跳过: ${results.skipped.length} 条`);
  console.log(`总计: ${index.total_memories} 条记忆`);
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法: node memory-dedup.js <记忆文件路径>');
    console.log('或者: node memory-dedup.js --check-all  # 检查所有记忆');
    process.exit(1);
  }

  (async () => {
    if (args[0] === '--check-all') {
      // 检查所有记忆
      const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
      const memories = Object.values(index.memories);

      console.log(`开始检查 ${memories.length} 条记忆...`);

      const results = await batchDeduplicate(memories);
      updateMemoryIndex(results);

      console.log('\n✓ 去重完成！');
    } else {
      // 从文件读取
      const filePath = args[0];
      if (!fs.existsSync(filePath)) {
        console.error(`文件不存在: ${filePath}`);
        process.exit(1);
      }

      const content = fs.readFileSync(filePath, 'utf-8');
      const memories = JSON.parse(content);

      const results = await batchDeduplicate(memories);
      updateMemoryIndex(results);

      console.log('\n✓ 去重完成！');
    }
  })();
}

module.exports = { deduplicateMemory, batchDeduplicate, updateMemoryIndex };
