import Database from 'better-sqlite3';
import { randomUUID } from 'crypto';
import { homedir } from 'os';
import { mkdirSync, existsSync } from 'fs';
import { dirname, resolve } from 'path';
import { Type } from '@sinclair/typebox';

// ============================================================================
// 工具函数
// ============================================================================

function expandPath(p) {
  return resolve(p.replace(/^~/, homedir()));
}

// ============================================================================
// 配置
// ============================================================================

const DEFAULT_CONFIG = {
  embedding: {
    apiKey: '',
    baseUrl: 'http://your-api-server:3000/v1',
    model: 'm3e-large'
  },
  dbPath: '~/.openclaw/data/memory-m3e.db',
  autoCapture: false,
  autoRecall: false,
  indexInterval: 600000
};

// ============================================================================
// Embedding API
// ============================================================================

async function getEmbedding(text, config) {
  const response = await fetch(`${config.embedding.baseUrl}/embeddings`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${config.embedding.apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: config.embedding.model,
      input: [text]  // array 格式
    })
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Embedding API error: ${response.status} ${errText}`);
  }

  const data = await response.json();
  return data.data[0].embedding;
}

// ============================================================================
// 数据库
// ============================================================================

function initDB(dbPath) {
  const resolved = expandPath(dbPath);
  const dir = dirname(resolved);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  const db = new Database(resolved);
  db.exec(`
    CREATE TABLE IF NOT EXISTS memories (
      id TEXT PRIMARY KEY,
      text TEXT NOT NULL,
      vector TEXT NOT NULL,
      category TEXT DEFAULT 'other',
      importance REAL DEFAULT 0.5,
      createdAt INTEGER NOT NULL
    )
  `);
  return db;
}

// ============================================================================
// 余弦相似度搜索
// ============================================================================

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

function searchMemories(db, queryVector, limit = 5) {
  const rows = db.prepare('SELECT * FROM memories').all();
  const scored = rows.map(row => {
    const vec = JSON.parse(row.vector);
    return { ...row, score: cosineSimilarity(queryVector, vec) };
  });
  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(({ vector, ...rest }) => rest);
}

// ============================================================================
// 定时索引刷新
// ============================================================================

function startIndexUpdater(db, intervalMs, logger) {
  setInterval(() => {
    const { count } = db.prepare('SELECT COUNT(*) as count FROM memories').get();
    logger.info(`[memory-m3e] Index refresh: ${count} memories in db`);
  }, intervalMs);
}

// ============================================================================
// 插件注册
// ============================================================================

export default {
  id: 'memory-m3e',
  kind: 'memory',

  register(api) {
    const config = {
      ...DEFAULT_CONFIG,
      ...(api.pluginConfig ?? {}),
      embedding: {
        ...DEFAULT_CONFIG.embedding,
        ...((api.pluginConfig ?? {}).embedding ?? {})
      }
    };

    const db = initDB(config.dbPath);
    api.logger.info(`[memory-m3e] Initialized (db: ${expandPath(config.dbPath)})`);
    startIndexUpdater(db, config.indexInterval, api.logger);

    // ------------------------------------------------------------------
    // memory_store
    // ------------------------------------------------------------------
    api.registerTool({
      name: 'memory_store',
      description: 'Store information in long-term memory',
      parameters: Type.Object({
        text: Type.String({ description: 'Information to remember' }),
        category: Type.Optional(Type.Union([
          Type.Literal('preference'),
          Type.Literal('fact'),
          Type.Literal('decision'),
          Type.Literal('entity'),
          Type.Literal('other')
        ])),
        importance: Type.Optional(Type.Number({ minimum: 0, maximum: 1 }))
      }),
      async execute(_toolCallId, params) {
        const { text, category = 'other', importance = 0.5 } = params;
        const vector = await getEmbedding(text, config);
        const id = randomUUID();

        db.prepare(`
          INSERT INTO memories (id, text, vector, category, importance, createdAt)
          VALUES (?, ?, ?, ?, ?, ?)
        `).run(id, text, JSON.stringify(vector), category, importance, Date.now());

        return {
          content: [{ type: 'text', text: `Memory stored (id: ${id})` }],
          details: { id, text, category, importance }
        };
      }
    });

    // ------------------------------------------------------------------
    // memory_recall
    // ------------------------------------------------------------------
    api.registerTool({
      name: 'memory_recall',
      description: 'Search long-term memory using semantic search',
      parameters: Type.Object({
        query: Type.String({ description: 'Search query' }),
        limit: Type.Optional(Type.Number({ description: 'Max results (default: 5)' }))
      }),
      async execute(_toolCallId, params) {
        const { query, limit = 5 } = params;
        const queryVector = await getEmbedding(query, config);
        const results = searchMemories(db, queryVector, limit);

        if (results.length === 0) {
          return {
            content: [{ type: 'text', text: 'No relevant memories found.' }],
            details: { count: 0, results: [] }
          };
        }

        const summary = results.map((r, i) =>
          `${i + 1}. [${r.category}] (score: ${r.score.toFixed(3)}) ${r.text}`
        ).join('\n');

        return {
          content: [{ type: 'text', text: summary }],
          details: { count: results.length, results }
        };
      }
    });

    // ------------------------------------------------------------------
    // memory_forget
    // ------------------------------------------------------------------
    api.registerTool({
      name: 'memory_forget',
      description: 'Delete memories by id or search query',
      parameters: Type.Object({
        memoryId: Type.Optional(Type.String({ description: 'Delete by exact id' })),
        query: Type.Optional(Type.String({ description: 'Delete by similarity search' }))
      }),
      async execute(_toolCallId, params) {
        const { memoryId, query } = params;

        if (memoryId) {
          const result = db.prepare('DELETE FROM memories WHERE id = ?').run(memoryId);
          return {
            content: [{ type: 'text', text: `Deleted ${result.changes} memory` }],
            details: { deleted: result.changes }
          };
        }

        if (query) {
          const queryVector = await getEmbedding(query, config);
          const matches = searchMemories(db, queryVector, 1);
          if (matches.length > 0) {
            db.prepare('DELETE FROM memories WHERE id = ?').run(matches[0].id);
            return {
              content: [{ type: 'text', text: `Deleted: ${matches[0].text.slice(0, 60)}` }],
              details: { deleted: 1, deletedText: matches[0].text }
            };
          }
        }

        return {
          content: [{ type: 'text', text: 'Nothing deleted' }],
          details: { deleted: 0 }
        };
      }
    });
  }
};
