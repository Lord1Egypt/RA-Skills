// embedder.mjs - Embedding 接入 (v2.0)
// 优先级：本地模型 > 免费 API > TF-IDF fallback

import { getDb, saveDatabase } from '../db/database.mjs';

let _embedder = null;
let _model = null;
let _dimensions = 0;

// 初始化 Embedding 模型
export async function initEmbedder(config) {
  const mode = config?.embedding?.mode || 'auto';

  // 1. 本地模型（推荐）
  if (mode === 'local' || mode === 'auto') {
    try {
      const { pipeline } = await import('@xenova/transformers');
      _embedder = await pipeline('feature-extraction',
        config?.embedding?.localModel || 'Xenova/paraphrase-multilingual-MiniLM-L12-v2');
      _model = 'local-transformers';
      _dimensions = 384;
      console.log('✅ Embedding: 本地模型已加载');
      return true;
    } catch (e) {
      console.log('ℹ️ 本地模型不可用:', e.message);
      if (mode === 'local') return false;
    }
  }

  // 2. 免费 API（豆包/通义）
  if (mode === 'api' || mode === 'auto') {
    try {
      const provider = config?.embedding?.apiProvider || 'doubao';
      const apiKey = config?.embedding?.apiKey || process.env.DOUBAO_API_KEY;
      if (apiKey) {
        _embedder = async (text) => await callEmbeddingAPI(provider, apiKey, text);
        _model = provider;
        _dimensions = 1024;
        console.log(`✅ Embedding: API (${provider}) 已配置`);
        return true;
      }
    } catch (e) {
      console.log('ℹ️ API Embedding 不可用:', e.message);
    }
  }

  // 3. TF-IDF fallback
  console.log('⚠️ Embedding: 使用 TF-IDF fallback');
  _model = 'tfidf-fallback';
  _dimensions = 0;
  return false;
}

// 本地模型 embedding
export async function embedText(text) {
  if (!_embedder) return null;

  try {
    if (_model === 'local-transformers') {
      const result = await _embedder(text, { pooling: 'mean', normalize: true });
      return Array.from(result.data);
    } else {
      return await _embedder(text);
    }
  } catch (e) {
    console.error('Embedding 失败:', e.message);
    return null;
  }
}

// 批量 embedding
export async function embedBatch(texts) {
  const vectors = [];
  for (const text of texts) {
    const vec = await embedText(text);
    vectors.push(vec);
  }
  return vectors;
}

// 存储向量到数据库
export function storeEmbedding(memoryId, vector) {
  const db = getDb();
  const buffer = new Float32Array(vector).buffer;
  const blob = Buffer.from(buffer);

  db.run(
    'INSERT INTO embeddings (memory_id, model, dimensions, vector) VALUES (?, ?, ?, ?)',
    [memoryId, _model, vector.length, blob]
  );

  const rows = db.exec('SELECT last_insert_rowid()');
  const embeddingId = rows[0].values[0][0];

  db.run('UPDATE memories SET embedding_id = ? WHERE id = ?', [embeddingId, memoryId]);
  saveDatabase();

  return embeddingId;
}

// 获取记忆的向量
export function getEmbedding(memoryId) {
  const db = getDb();
  const rows = db.exec('SELECT vector, dimensions FROM embeddings WHERE memory_id = ?', [memoryId]);
  if (!rows.length || !rows[0].values.length) return null;

  const blob = rows[0].values[0][0];
  const dims = rows[0].values[0][1];
  const float32 = new Float32Array(blob.buffer || blob);
  return Array.from(float32);
}

// 计算余弦相似度
export function cosineSimilarity(vecA, vecB) {
  if (!vecA || !vecB || vecA.length !== vecB.length) return 0;

  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }

  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

// ============= API Embedding =============

async function callEmbeddingAPI(provider, apiKey, text) {
  const endpoints = {
    doubao: 'https://ark.cn-beijing.volces.com/api/v3/embeddings',
    dashscope: 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding',
  };

  const url = endpoints[provider] || endpoints.doubao;

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'text-embedding',
      input: text,
    }),
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);

  const data = await res.json();
  return data.data?.[0]?.embedding || data.embeddings?.[0] || null;
}

// 获取当前状态
export function getStatus() {
  return { model: _model, dimensions: _dimensions, available: !!_embedder };
}