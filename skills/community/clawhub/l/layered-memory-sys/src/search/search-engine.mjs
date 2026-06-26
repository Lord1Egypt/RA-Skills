// search-engine.mjs - 统一搜索引擎 (v2.0)
// Embedding 语义搜索 > TF-IDF fallback

import { embedText, cosineSimilarity, getEmbedding, storeEmbedding, getStatus as getEmbedderStatus } from './embedder.mjs';
import { searchTFIDF, tokenize, clearIDFCache } from './tokenizer.mjs';
import { getDb } from '../db/database.mjs';

// 统一搜索
export async function search(query, options = {}) {
  const { limit = 20, threshold = 0.01, config } = options;

  // 1. 优先用 Embedding 搜索
  const embeddingStatus = getEmbedderStatus();
  if (embeddingStatus.available) {
    return await searchEmbedding(query, { limit, threshold, config });
  }

  // 2. 降级到 TF-IDF
  return searchTFIDF(query, { limit, threshold, config });
}

// Embedding 搜索
async function searchEmbedding(query, { limit, threshold, config }) {
  const queryVector = await embedText(query);
  if (!queryVector) {
    return searchTFIDF(query, { limit, threshold: 0.1, config });
  }

  const db = getDb();
  const rows = db.exec(
    `SELECT id, title, summary, content, layer, recall_count, last_active_ts
     FROM memories WHERE status != 'archived'`
  );

  if (!rows.length) return [];

  const results = [];

  // 有 embedding 的记忆 → 余弦相似度
  const memNoEmbedding = [];

  for (const row of rows[0].values) {
    const [id, title, summary, content, layer, recallCount, lastActiveTs] = row;

    const storedVec = getEmbedding(id);
    if (storedVec) {
      const score = cosineSimilarity(queryVector, storedVec);
      if (score >= threshold) {
        results.push({
          id, title, summary, layer, recallCount, lastActiveTs,
          score, matchType: 'semantic',
        });
      }
    } else {
      memNoEmbedding.push({ id, title, summary, content, layer, recallCount, lastActiveTs });
    }
  }

  // 无 embedding 的记忆 → TF-IDF 补充
  if (memNoEmbedding.length > 0 && results.length < limit) {
    const tfidfResults = searchTFIDF(query, { limit: limit - results.length, threshold: 0.1, config });
    const existingIds = new Set(results.map(r => r.id));
    for (const r of tfidfResults) {
      if (!existingIds.has(r.id)) {
        results.push(r);
      }
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}

// 高亮关键词
export function highlightSnippet(text, query, maxLen = 150) {
  if (!text) return '';

  const keywords = tokenize(query);
  if (keywords.length === 0) return text.slice(0, maxLen);

  // 找到最佳匹配位置
  let bestPos = 0;
  let bestScore = 0;

  for (let i = 0; i < text.length; i++) {
    let score = 0;
    for (const kw of keywords) {
      if (text.substring(i, i + kw.length).includes(kw)) {
        score += kw.length;
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestPos = i;
    }
  }

  // 提取片段
  const start = Math.max(0, bestPos - 30);
  const end = Math.min(text.length, start + maxLen);
  let snippet = text.slice(start, end);
  if (start > 0) snippet = '...' + snippet;
  if (end < text.length) snippet += '...';

  // 高亮标记
  for (const kw of keywords) {
    snippet = snippet.replaceAll(kw, `<<<${kw}>>>`);
  }

  return snippet;
}

// 索引记忆（计算并存储 embedding）
export async function indexMemory(memoryId) {
  const db = getDb();
  const rows = db.exec('SELECT id, title, summary, content FROM memories WHERE id = ?', [memoryId]);
  if (!rows.length || !rows[0].values.length) return false;

  const [, title, summary, content] = rows[0].values[0];
  const text = `${title} ${summary} ${content}`;

  const vector = await embedText(text);
  if (vector) {
    storeEmbedding(memoryId, vector);
    clearIDFCache();
    return true;
  }

  return false;
}

// 批量索引
export async function indexAllMemories(config) {
  const db = getDb();
  const rows = db.exec("SELECT id FROM memories WHERE status != 'archived'");
  if (!rows.length) return { indexed: 0, failed: 0 };

  let indexed = 0, failed = 0;
  for (const row of rows[0].values) {
    try {
      const ok = await indexMemory(row[0]);
      if (ok) indexed++;
      else failed++;
    } catch {
      failed++;
    }
  }

  clearIDFCache();
  console.log(`📊 索引完成: ${indexed} 成功, ${failed} 失败`);
  return { indexed, failed };
}