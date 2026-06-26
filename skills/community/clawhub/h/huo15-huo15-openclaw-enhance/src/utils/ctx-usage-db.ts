/**
 * v6.5.6: context-watchdog 持久化层
 *
 * 一张表（schema migration v6 → v7）：
 *  - ctx_usage: 会话级 token 累加状态。session_key 主键（跨重启不丢）。
 *
 * 设计约束：
 *  - 启动期不全量加载，按 getOrCreate 按需 lazy hydrate
 *  - 节流 flush：dirty 标记 + 每 10s 批量写，避免每个 llm_output 都 IO
 *  - LRU eviction 不删 sqlite row（保留作历史画像，跟 peak_percent 为 P2-12 铺路）
 *  - 写失败一律静默（不能影响 LLM 主流程）
 */
import type { Database } from "better-sqlite3";

export function migrateV6ToV7(db: Database): void {
  const tables = db
    .prepare("SELECT name FROM sqlite_master WHERE type='table'")
    .all() as Array<{ name: string }>;
  const tableNames = new Set(tables.map((t) => t.name));

  if (!tableNames.has("ctx_usage")) {
    db.exec(`
      CREATE TABLE ctx_usage (
        session_key TEXT PRIMARY KEY,
        agent_id TEXT NOT NULL DEFAULT 'main',
        total_tokens INTEGER NOT NULL DEFAULT 0,
        last_model TEXT,
        last_model_ctx_max INTEGER NOT NULL DEFAULT 128000,
        original_model TEXT,
        last_warned_threshold REAL NOT NULL DEFAULT 0,
        peak_percent REAL NOT NULL DEFAULT 0,
        estimated_cost_usd REAL NOT NULL DEFAULT 0,
        last_updated_at INTEGER NOT NULL,
        created_at INTEGER NOT NULL
      );
      CREATE INDEX idx_ctx_usage_agent ON ctx_usage(agent_id);
      CREATE INDEX idx_ctx_usage_updated ON ctx_usage(last_updated_at DESC);
    `);
  }
}

/**
 * v6.6.0: 给从 v6.5.6 升级来的用户补加 estimated_cost_usd 列
 * （初次装 v6.6.0 的用户 CREATE TABLE 已含此列；本函数只对存在 ctx_usage 但缺该列的库 ALTER）
 */
export function migrateV7ToV8(db: Database): void {
  try {
    const tables = db
      .prepare("SELECT name FROM sqlite_master WHERE type='table'")
      .all() as Array<{ name: string }>;
    if (!tables.some((t) => t.name === "ctx_usage")) return;

    const cols = db
      .prepare("PRAGMA table_info(ctx_usage)")
      .all() as Array<{ name: string }>;
    if (!cols.some((c) => c.name === "estimated_cost_usd")) {
      db.exec("ALTER TABLE ctx_usage ADD COLUMN estimated_cost_usd REAL NOT NULL DEFAULT 0");
    }
  } catch {
    /* silent */
  }
}

// ─────────── 行类型 + CRUD ───────────
export interface CtxUsageRow {
  session_key: string;
  agent_id: string;
  total_tokens: number;
  last_model: string | null;
  last_model_ctx_max: number;
  original_model: string | null;
  last_warned_threshold: number;
  peak_percent: number;
  /** v6.6.0：会话累计估算成本（USD），按 model.costInPerM/costOutPerM 在 llm_output 时累加 */
  estimated_cost_usd: number;
  last_updated_at: number;
  created_at: number;
}

export function loadCtxUsage(db: Database, sessionKey: string): CtxUsageRow | null {
  try {
    const row = db
      .prepare(`SELECT * FROM ctx_usage WHERE session_key = ?`)
      .get(sessionKey) as CtxUsageRow | undefined;
    return row ?? null;
  } catch {
    return null;
  }
}

export function saveCtxUsage(db: Database, row: CtxUsageRow): void {
  try {
    db.prepare(
      `INSERT INTO ctx_usage
        (session_key, agent_id, total_tokens, last_model, last_model_ctx_max,
         original_model, last_warned_threshold, peak_percent, estimated_cost_usd,
         last_updated_at, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ON CONFLICT(session_key) DO UPDATE SET
         agent_id = excluded.agent_id,
         total_tokens = excluded.total_tokens,
         last_model = excluded.last_model,
         last_model_ctx_max = excluded.last_model_ctx_max,
         original_model = excluded.original_model,
         last_warned_threshold = excluded.last_warned_threshold,
         peak_percent = MAX(ctx_usage.peak_percent, excluded.peak_percent),
         estimated_cost_usd = excluded.estimated_cost_usd,
         last_updated_at = excluded.last_updated_at`,
    ).run(
      row.session_key,
      row.agent_id,
      row.total_tokens,
      row.last_model,
      row.last_model_ctx_max,
      row.original_model,
      row.last_warned_threshold,
      row.peak_percent,
      row.estimated_cost_usd,
      row.last_updated_at,
      row.created_at,
    );
  } catch {
    /* silent */
  }
}

/** 批量持久化（dirty session 一次性写盘）*/
export function batchSaveCtxUsage(db: Database, rows: CtxUsageRow[]): void {
  if (rows.length === 0) return;
  try {
    const tx = db.transaction((items: CtxUsageRow[]) => {
      for (const r of items) saveCtxUsage(db, r);
    });
    tx(rows);
  } catch {
    /* silent */
  }
}

/** v6.5.6: 清理 N 天前没活动的 session（默认 30 天）*/
export function purgeOldCtxUsage(db: Database, retentionDays: number = 30): { deleted: number } {
  try {
    const cutoff = Date.now() - retentionDays * 86_400_000;
    const result = db
      .prepare(`DELETE FROM ctx_usage WHERE last_updated_at < ?`)
      .run(cutoff);
    return { deleted: result.changes };
  } catch {
    return { deleted: 0 };
  }
}

/** 取 agent 历史峰值画像（为 P2-12 用，本期暴露给 enhance_ctx_status 工具）*/
export function getAgentCtxProfile(
  db: Database,
  agentId: string,
): { sessions: number; avgPeak: number; maxPeak: number; totalCostUSD: number } {
  try {
    const row = db
      .prepare(
        `SELECT COUNT(*) AS n,
                AVG(peak_percent) AS avg_peak,
                MAX(peak_percent) AS max_peak,
                SUM(estimated_cost_usd) AS total_cost
         FROM ctx_usage WHERE agent_id = ?`,
      )
      .get(agentId) as { n: number; avg_peak: number | null; max_peak: number | null; total_cost: number | null };
    return {
      sessions: row.n ?? 0,
      avgPeak: row.avg_peak ?? 0,
      maxPeak: row.max_peak ?? 0,
      totalCostUSD: row.total_cost ?? 0,
    };
  } catch {
    return { sessions: 0, avgPeak: 0, maxPeak: 0, totalCostUSD: 0 };
  }
}

/** v6.6.0: 月度成本估算（按 agentId 或全部）— 不强制预算，仅观察 */
export function getMonthlyCostEstimate(
  db: Database,
  agentId?: string,
): { sessions: number; totalCostUSD: number } {
  try {
    const cutoff = Date.now() - 30 * 86_400_000;
    const sql = agentId
      ? `SELECT COUNT(*) AS n, SUM(estimated_cost_usd) AS total
         FROM ctx_usage WHERE agent_id = ? AND last_updated_at >= ?`
      : `SELECT COUNT(*) AS n, SUM(estimated_cost_usd) AS total
         FROM ctx_usage WHERE last_updated_at >= ?`;
    const row = (agentId
      ? db.prepare(sql).get(agentId, cutoff)
      : db.prepare(sql).get(cutoff)) as { n: number; total: number | null };
    return { sessions: row.n ?? 0, totalCostUSD: row.total ?? 0 };
  } catch {
    return { sessions: 0, totalCostUSD: 0 };
  }
}
