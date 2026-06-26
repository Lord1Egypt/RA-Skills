import https from "https";
import type { OrchardConfig } from "../config.js";
import type Database from "better-sqlite3";

export interface KnowledgeEntry {
  id: number;
  project_id: string;
  content: string;
  embedding: string | null;
  source: string;
  task_id: number | null;
  created_at: string;
}

function getApiKey(cfg: OrchardConfig): string {
  return cfg.contextInjection?.apiKey || process.env.GEMINI_API_KEY || "";
}

function isEnabled(cfg: OrchardConfig): boolean {
  if (cfg.contextInjection?.enabled === false) return false;
  // Conservative default: only active if API key present
  return !!getApiKey(cfg);
}

export async function embedText(text: string, cfg: OrchardConfig): Promise<number[]> {
  const apiKey = getApiKey(cfg);
  if (!apiKey) return [];
  const model = cfg.contextInjection?.model ?? "gemini-embedding-001";
  const body = JSON.stringify({ content: { parts: [{ text }] } });

  return new Promise((resolve) => {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:embedContent?key=${apiKey}`;
    const req = https.request(url, { method: "POST", headers: { "Content-Type": "application/json" } }, (res) => {
      let data = "";
      res.on("data", (c: Buffer) => { data += c; });
      res.on("end", () => {
        try {
          const json = JSON.parse(data);
          const values = json?.embedding?.values;
          resolve(Array.isArray(values) ? values : []);
        } catch {
          resolve([]);
        }
      });
    });
    req.on("error", () => resolve([]));
    req.setTimeout(10000, () => { req.destroy(); resolve([]); });
    req.write(body);
    req.end();
  });
}

function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length || a.length === 0) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

export async function addKnowledge(
  db: Database.Database,
  cfg: OrchardConfig,
  projectId: string,
  content: string,
  source: string,
  taskId?: number
): Promise<void> {
  // Always store the text; try to embed if enabled
  let embeddingJson: string | null = null;
  if (isEnabled(cfg)) {
    try {
      const vec = await embedText(content, cfg);
      if (vec.length > 0) embeddingJson = JSON.stringify(vec);
    } catch {
      // non-blocking — store without embedding
    }
  }
  db.prepare(
    `INSERT INTO project_knowledge (project_id, content, embedding, source, task_id) VALUES (?, ?, ?, ?, ?)`
  ).run(projectId, content, embeddingJson, source, taskId ?? null);
}

export async function searchKnowledge(
  db: Database.Database,
  cfg: OrchardConfig,
  projectId: string,
  query: string,
  topK?: number,
  minScore?: number
): Promise<KnowledgeEntry[]> {
  const k = topK ?? cfg.contextInjection?.topK ?? 5;
  const threshold = minScore ?? cfg.contextInjection?.minScore ?? 0.7;

  const rows = db.prepare(
    `SELECT * FROM project_knowledge WHERE project_id = ? ORDER BY created_at DESC`
  ).all(projectId) as KnowledgeEntry[];

  if (rows.length === 0) return [];

  // If embeddings disabled or no API key, fall back to returning most recent k entries
  if (!isEnabled(cfg)) return rows.slice(0, k);

  let queryVec: number[] = [];
  try {
    queryVec = await embedText(query, cfg);
  } catch {
    // fallback to recency
  }

  if (queryVec.length === 0) return rows.slice(0, k);

  // Score entries that have embeddings; unembedded entries get score 0
  const scored = rows.map((row) => {
    let score = 0;
    if (row.embedding) {
      try {
        const vec = JSON.parse(row.embedding) as number[];
        score = cosineSimilarity(queryVec, vec);
      } catch {
        score = 0;
      }
    }
    return { row, score };
  });

  return scored
    .filter((s) => s.score >= threshold)
    .sort((a, b) => b.score - a.score)
    .slice(0, k)
    .map((s) => s.row);
}
