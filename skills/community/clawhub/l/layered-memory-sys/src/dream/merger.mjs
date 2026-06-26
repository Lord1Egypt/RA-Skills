// merger.mjs - 合并逻辑 (v2.0)
// 语义相似度阈值 + 来源追溯

import { getDb, saveDatabase } from '../db/database.mjs';
import { embedText, cosineSimilarity } from '../search/embedder.mjs';
import { logEvent } from '../db/repository.mjs';

// 判断是否应该合并
export async function shouldMerge(memA, memB, config) {
  // 1. 带提醒时间的记忆不合并
  if (memA.remind_at || memB.remind_at) return false;

  // 2. 标签重叠检查（初步筛选）
  const tagOverlap = memA.tags.filter(t => memB.tags.includes(t));
  if (tagOverlap.length < 2) return false;  // 降到2个标签即可候选

  // 3. 语义相似度检查（主要判断）
  try {
    const vecA = await embedText(memA.title + ' ' + memA.summary);
    const vecB = await embedText(memB.title + ' ' + memB.summary);

    if (vecA && vecB) {
      const sim = cosineSimilarity(vecA, vecB);
      // 高置信度直接合并
      if (sim >= 0.85) return true;
      // 中等置信度 + 标签确认
      if (sim >= 0.70 && tagOverlap.length >= 3) return true;
      // 低置信度 + 更多标签
      if (sim >= 0.55 && tagOverlap.length >= 5) return true;
    }
  } catch {}

  // 4. 无 embedding 时用标题关键词匹配
  const wordsA = memA.title.toLowerCase().split(/\s+/);
  const wordsB = memB.title.toLowerCase().split(/\s+/);
  const wordOverlap = wordsA.filter(w => wordsB.includes(w) && w.length > 3);
  if (wordOverlap.length >= 2 && tagOverlap.length >= 3) return true;

  return false;
}

// 执行合并
export async function mergeMemories(memA, memB, config) {
  const db = getDb();

  // 合并策略：
  // - title: 保留较长的或较具体的
  // - summary: 合并两条
  // - recallCount: 相加（带时间衰减）
  // - tags: 去重合并
  // - source: 保留追溯信息

  const mergedTitle = memA.title.length > memB.title.length ? memA.title : memB.title;
  const mergedSummary = `${memA.summary || ''} | ${memB.summary || ''}`;
  const mergedRecallCount = memA.recall_count + memB.recall_count;
  const mergedRecallDays = [...new Set([...(memA.recall_days || []), ...(memB.recall_days || [])])];
  const mergedTags = [...new Set([...(memA.tags || []), ...(memB.tags || [])])];
  const mergedTTL = Math.max(memA.ttl, memB.ttl);
  const mergedLayer = ['attention', 'settled'].includes(memA.layer) ? memA.layer : memB.layer;

  // 来源追溯
  const sourceInfo = {
    primary: memA.id,
    merged: [
      {
        id: memB.id,
        title: memB.title,
        mergedAt: new Date().toISOString(),
        recallCount: memB.recall_count,
        tags: memB.tags,
      },
    ],
    mergedCount: 1,
    history: memA.source ? JSON.parse(memA.source) : null,
  };

  // 合并后的记忆
  db.run(
    `UPDATE memories SET
     title = ?, summary = ?, layer = ?, ttl = ?, recall_count = ?, recall_days = ?
     WHERE id = ?`,
    [mergedTitle, mergedSummary, mergedLayer, mergedTTL, mergedRecallCount, JSON.stringify(mergedRecallDays), memA.id]
  );

  // 更新标签
  db.run('DELETE FROM memory_tags WHERE memory_id = ?', [memA.id]);
  for (const tag of mergedTags) {
    db.run('INSERT OR IGNORE INTO memory_tags (memory_id, tag) VALUES (?, ?)', [memA.id, tag]);
  }

  // 删除被合并的记忆
  db.run('DELETE FROM memory_tags WHERE memory_id = ?', [memB.id]);
  db.run('DELETE FROM memories WHERE id = ?', [memB.id]);

  // 事件记录
  logEvent('merged', memA.id, {
    target: memA.id,
    source: memB.id,
    sourceTitle: memB.title,
    tags: mergedTags,
    recallCount: mergedRecallCount,
  });

  saveDatabase();

  return {
    id: memA.id,
    title: mergedTitle,
    mergedFrom: memB.id,
    mergedTitle: memB.title,
  };
}

// 执行所有合并检查
export async function runMergeChecks(config) {
  const db = getDb();
  const rows = db.exec(
    "SELECT * FROM memories WHERE status = 'active' AND remind_at IS NULL ORDER BY recall_count DESC"
  );

  if (!rows.length || !rows[0].values.length) return [];

  const memories = rows[0].values.map(row => ({
    id: row[0], title: row[1], summary: row[2], content: row[3],
    layer: row[4], ttl: row[5], status: row[6], created_at: row[7],
    last_active: row[8], recall_count: row[9], recall_days: JSON.parse(row[10] || '[]'),
    remind_at: row[11], tags: [],
  }));

  // 加载标签
  for (const mem of memories) {
    const tagRows = db.exec('SELECT tag FROM memory_tags WHERE memory_id = ?', [mem.id]);
    if (tagRows.length) {
      mem.tags = tagRows[0].values.map(v => v[0]);
    }
  }

  const merges = [];

  // 检查所有记忆对的相似性
  for (let i = 0; i < memories.length && merges.length < 3; i++) {
    for (let j = i + 1; j < memories.length && merges.length < 3; j++) {
      const memA = memories[i];
      const memB = memories[j];

      // 已被合并的记忆跳过
      if (merges.some(m => m.mergedFrom === memA.id || m.mergedFrom === memB.id)) continue;

      if (await shouldMerge(memA, memB, config)) {
        const merged = await mergeMemories(memA, memB, config);
        merges.push(merged);
      }
    }
  }

  return merges;
}