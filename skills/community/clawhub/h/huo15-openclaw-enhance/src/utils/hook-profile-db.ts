/**
 * v5.8.0: hook-profiler 数据存储
 *
 * 两张表（schema migration v5 → v6）：
 *  - prep_stage_metrics: 端到端 turn 准备阶段耗时（来自 gateway.err.log
 *    [trace:embedded-run] prep stages 行解析）。每行一次 turn。
 *  - hook_profile: 单 hook handler 调用记录（来自 wrap + log-timeout/log-error 解析）。
 *    source='wrap' 是 enhance 自家 hook 精确测时；'log-timeout'/'log-error' 是
 *    其它 plugin 通过日志间接抓到的异常事件。
 *
 * 设计约束：
 *  - 不写其它 plugin 成功 handler 的耗时（openclaw 不暴露这个事件，无从下手）
 *  - 不替用户改 openclaw.json（红线 #5"诊断不修复"）
 *  - 写入失败一律静默（profiler 不能影响主流程）
 */
import type { Database } from "better-sqlite3";

export function migrateV5ToV6(db: Database): void {
  const tables = db
    .prepare("SELECT name FROM sqlite_master WHERE type='table'")
    .all() as Array<{ name: string }>;
  const tableNames = new Set(tables.map((t) => t.name));

  if (!tableNames.has("prep_stage_metrics")) {
    db.exec(`
      CREATE TABLE prep_stage_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER NOT NULL,
        run_id TEXT,
        session_id TEXT,
        total_ms INTEGER,
        workspace_sandbox_ms INTEGER,
        skills_ms INTEGER,
        core_plugin_tools_ms INTEGER,
        bootstrap_context_ms INTEGER,
        bundle_tools_ms INTEGER,
        system_prompt_ms INTEGER,
        session_resource_loader_ms INTEGER,
        agent_session_ms INTEGER,
        stream_setup_ms INTEGER,
        raw_line TEXT
      );
      CREATE INDEX idx_prep_ts ON prep_stage_metrics(ts DESC);
    `);
  }

  if (!tableNames.has("hook_profile")) {
    db.exec(`
      CREATE TABLE hook_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER NOT NULL,
        source TEXT NOT NULL CHECK(source IN ('wrap','log-timeout','log-error')),
        hook_event TEXT NOT NULL,
        plugin_id TEXT NOT NULL,
        module TEXT,
        duration_ms INTEGER,
        status TEXT NOT NULL CHECK(status IN ('ok','timeout','error')),
        err_msg TEXT
      );
      CREATE INDEX idx_hook_event_ts ON hook_profile(hook_event, ts DESC);
      CREATE INDEX idx_hook_plugin_ts ON hook_profile(plugin_id, ts DESC);
    `);
  }
}

// ─────────── prep_stage_metrics 行 ───────────
export interface PrepStageRow {
  ts: number;
  run_id: string | null;
  session_id: string | null;
  total_ms: number;
  workspace_sandbox_ms: number;
  skills_ms: number;
  core_plugin_tools_ms: number;
  bootstrap_context_ms: number;
  bundle_tools_ms: number;
  system_prompt_ms: number;
  session_resource_loader_ms: number;
  agent_session_ms: number;
  stream_setup_ms: number;
  raw_line: string;
}

export function insertPrepStage(db: Database, row: PrepStageRow): void {
  db.prepare(
    `INSERT INTO prep_stage_metrics (
      ts, run_id, session_id, total_ms,
      workspace_sandbox_ms, skills_ms, core_plugin_tools_ms,
      bootstrap_context_ms, bundle_tools_ms, system_prompt_ms,
      session_resource_loader_ms, agent_session_ms, stream_setup_ms, raw_line
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    row.ts,
    row.run_id,
    row.session_id,
    row.total_ms,
    row.workspace_sandbox_ms,
    row.skills_ms,
    row.core_plugin_tools_ms,
    row.bootstrap_context_ms,
    row.bundle_tools_ms,
    row.system_prompt_ms,
    row.session_resource_loader_ms,
    row.agent_session_ms,
    row.stream_setup_ms,
    row.raw_line.slice(0, 4000),
  );
}

// ─────────── hook_profile 行 ───────────
export interface HookProfileRow {
  ts: number;
  source: "wrap" | "log-timeout" | "log-error";
  hook_event: string;
  plugin_id: string;
  module: string | null;
  duration_ms: number | null;
  status: "ok" | "timeout" | "error";
  err_msg: string | null;
}

export function insertHookProfile(db: Database, row: HookProfileRow): void {
  db.prepare(
    `INSERT INTO hook_profile (
      ts, source, hook_event, plugin_id, module, duration_ms, status, err_msg
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    row.ts,
    row.source,
    row.hook_event,
    row.plugin_id,
    row.module,
    row.duration_ms,
    row.status,
    row.err_msg ? row.err_msg.slice(0, 500) : null,
  );
}

// ─────────── 90 天 retention 清理 ───────────
export function purgeOldHookProfiles(
  db: Database,
  retentionDays = 30,
): { deleted: number } {
  const cutoff = Date.now() - retentionDays * 86400_000;
  const r1 = db.prepare(`DELETE FROM hook_profile WHERE ts < ?`).run(cutoff);
  const r2 = db.prepare(`DELETE FROM prep_stage_metrics WHERE ts < ?`).run(cutoff);
  return { deleted: r1.changes + r2.changes };
}

// ─────────── 查询 helpers ───────────
function percentile(sorted: number[], p: number): number {
  if (sorted.length === 0) return 0;
  const idx = Math.min(
    sorted.length - 1,
    Math.max(0, Math.floor(sorted.length * p)),
  );
  return sorted[idx];
}

export interface PrepStageStats {
  count: number;
  total_ms: { p50: number; p95: number; max: number };
  core_plugin_tools_ms: { p50: number; p95: number };
  system_prompt_ms: { p50: number; p95: number };
  bundle_tools_ms: { p50: number; p95: number };
  stream_setup_ms: { p50: number; p95: number };
  session_resource_loader_ms: { p50: number; p95: number };
  bootstrap_context_ms: { p50: number; p95: number };
}

export function getPrepStageStats(db: Database, sinceMs: number): PrepStageStats {
  const rows = db
    .prepare(`SELECT * FROM prep_stage_metrics WHERE ts >= ? ORDER BY ts DESC`)
    .all(sinceMs) as PrepStageRow[];

  const stat = (col: keyof PrepStageRow) => {
    const arr = rows
      .map((r) => r[col] as number)
      .filter((v) => typeof v === "number" && v >= 0)
      .sort((a, b) => a - b);
    return { p50: percentile(arr, 0.5), p95: percentile(arr, 0.95) };
  };
  const total = rows
    .map((r) => r.total_ms)
    .filter((v) => v >= 0)
    .sort((a, b) => a - b);

  return {
    count: rows.length,
    total_ms: {
      p50: percentile(total, 0.5),
      p95: percentile(total, 0.95),
      max: total.length > 0 ? total[total.length - 1] : 0,
    },
    core_plugin_tools_ms: stat("core_plugin_tools_ms"),
    system_prompt_ms: stat("system_prompt_ms"),
    bundle_tools_ms: stat("bundle_tools_ms"),
    stream_setup_ms: stat("stream_setup_ms"),
    session_resource_loader_ms: stat("session_resource_loader_ms"),
    bootstrap_context_ms: stat("bootstrap_context_ms"),
  };
}

export interface HookProfileStats {
  hook_event: string;
  plugin_id: string;
  module: string | null;
  count: number;
  ok_count: number;
  p50: number;
  p95: number;
  timeout_count: number;
  error_count: number;
}

export function getHookProfileStats(
  db: Database,
  hookEvent: string,
  sinceMs: number,
): HookProfileStats[] {
  const rows = db
    .prepare(
      `SELECT plugin_id, module, status, duration_ms
       FROM hook_profile WHERE hook_event = ? AND ts >= ?`,
    )
    .all(hookEvent, sinceMs) as Array<{
    plugin_id: string;
    module: string | null;
    status: string;
    duration_ms: number | null;
  }>;

  type Bucket = {
    plugin_id: string;
    module: string | null;
    durations: number[];
    timeouts: number;
    errors: number;
  };
  const buckets = new Map<string, Bucket>();
  for (const r of rows) {
    const key = `${r.plugin_id}::${r.module ?? ""}`;
    let b = buckets.get(key);
    if (!b) {
      b = {
        plugin_id: r.plugin_id,
        module: r.module,
        durations: [],
        timeouts: 0,
        errors: 0,
      };
      buckets.set(key, b);
    }
    if (r.status === "ok" && r.duration_ms != null) b.durations.push(r.duration_ms);
    else if (r.status === "timeout") b.timeouts++;
    else if (r.status === "error") b.errors++;
  }

  const result: HookProfileStats[] = [];
  for (const b of buckets.values()) {
    const sorted = b.durations.sort((a, b) => a - b);
    result.push({
      hook_event: hookEvent,
      plugin_id: b.plugin_id,
      module: b.module,
      count: b.durations.length + b.timeouts + b.errors,
      ok_count: b.durations.length,
      p50: percentile(sorted, 0.5),
      p95: percentile(sorted, 0.95),
      timeout_count: b.timeouts,
      error_count: b.errors,
    });
  }
  result.sort((a, b) => b.p95 - a.p95);
  return result;
}

export function listKnownHookEvents(db: Database, sinceMs: number): string[] {
  const rows = db
    .prepare(
      `SELECT DISTINCT hook_event FROM hook_profile WHERE ts >= ? ORDER BY hook_event`,
    )
    .all(sinceMs) as Array<{ hook_event: string }>;
  return rows.map((r) => r.hook_event);
}
