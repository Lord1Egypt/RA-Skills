/**
 * SQLite 辅助工具 — 结构化记忆存储
 *
 * 所有表都包含 agent_id 列以支持动态 Agent 隔离。
 * 每个 WeCom 用户/群组对应一个独立的 agentId，数据完全隔离。
 */
import type Database from "better-sqlite3";
import { join } from "node:path";
import { existsSync, mkdirSync } from "node:fs";
import { ensureSqlite } from "./ensure-sqlite.js";
import { migrateV5ToV6 } from "./hook-profile-db.js";
import { migrateV6ToV7, migrateV7ToV8 } from "./ctx-usage-db.js";
import type {
  MemoryEntry,
  MemoryCategory,
  FlamePet,
  FlameColor,
  FlameStats,
  Notification,
  NotificationLevel,
  NotificationSource,
  TodoEntry,
  TodoStatus,
  ChapterMark,
} from "../types.js";

const SCHEMA_V2 = `
CREATE TABLE IF NOT EXISTS memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  agent_id TEXT NOT NULL DEFAULT 'main',
  category TEXT NOT NULL CHECK(category IN ('user','project','feedback','reference','decision')),
  content TEXT NOT NULL,
  tags TEXT DEFAULT '',
  importance INTEGER DEFAULT 5 CHECK(importance BETWEEN 1 AND 10),
  session_id TEXT DEFAULT '',
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id);
CREATE INDEX IF NOT EXISTS idx_memories_agent_category ON memories(agent_id, category);
CREATE INDEX IF NOT EXISTS idx_memories_agent_created ON memories(agent_id, created_at DESC);

CREATE TABLE IF NOT EXISTS safety_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  agent_id TEXT NOT NULL DEFAULT 'main',
  tool TEXT NOT NULL,
  params TEXT,
  action TEXT NOT NULL,
  rule TEXT,
  reason TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_safety_agent ON safety_log(agent_id);
CREATE INDEX IF NOT EXISTS idx_safety_agent_created ON safety_log(agent_id, created_at DESC);
`;

/**
 * v1 → v2 迁移：为已有表添加 agent_id 列
 */
function migrateV1ToV2(db: Database.Database): void {
  const memoryCols = db.prepare("PRAGMA table_info(memories)").all() as Array<{ name: string }>;
  if (memoryCols.length > 0 && !memoryCols.some((c) => c.name === "agent_id")) {
    db.exec("ALTER TABLE memories ADD COLUMN agent_id TEXT NOT NULL DEFAULT 'main'");
    db.exec("CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id)");
    db.exec("CREATE INDEX IF NOT EXISTS idx_memories_agent_category ON memories(agent_id, category)");
    db.exec("CREATE INDEX IF NOT EXISTS idx_memories_agent_created ON memories(agent_id, created_at DESC)");
  }

  const safetyCols = db.prepare("PRAGMA table_info(safety_log)").all() as Array<{ name: string }>;
  if (safetyCols.length > 0 && !safetyCols.some((c) => c.name === "agent_id")) {
    db.exec("ALTER TABLE safety_log ADD COLUMN agent_id TEXT NOT NULL DEFAULT 'main'");
    db.exec("CREATE INDEX IF NOT EXISTS idx_safety_agent ON safety_log(agent_id)");
    db.exec("CREATE INDEX IF NOT EXISTS idx_safety_agent_created ON safety_log(agent_id, created_at DESC)");
  }
}

/**
 * v2 → v3 迁移：新增 flame_pets 和 notifications 表
 */
function migrateV2ToV3(db: Database.Database): void {
  const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>;
  const tableNames = new Set(tables.map((t) => t.name));

  if (!tableNames.has("flame_pets")) {
    db.exec(`
      CREATE TABLE flame_pets (
        agent_id TEXT PRIMARY KEY,
        name TEXT NOT NULL DEFAULT '小火苗',
        color TEXT NOT NULL DEFAULT 'orange',
        level INTEGER NOT NULL DEFAULT 1,
        xp INTEGER NOT NULL DEFAULT 0,
        total_xp INTEGER NOT NULL DEFAULT 0,
        stat_warmth INTEGER NOT NULL DEFAULT 10,
        stat_brightness INTEGER NOT NULL DEFAULT 10,
        stat_stability INTEGER NOT NULL DEFAULT 10,
        stat_spark INTEGER NOT NULL DEFAULT 10,
        stat_endurance INTEGER NOT NULL DEFAULT 10,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
      );
    `);
  }

  if (!tableNames.has("notifications")) {
    db.exec(`
      CREATE TABLE notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL DEFAULT 'main',
        level TEXT NOT NULL DEFAULT 'info',
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        detail TEXT DEFAULT '',
        read INTEGER NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now'))
      );
      CREATE INDEX idx_notif_agent ON notifications(agent_id);
      CREATE INDEX idx_notif_created ON notifications(created_at DESC);
    `);
  }
}

/**
 * v4 → v5 迁移：memories 表新增 why / how_to_apply 结构化正文字段
 * （对齐 Claude Code feedback/project 记忆的 Why + How-to-apply 两段式）
 */
function migrateV4ToV5(db: Database.Database): void {
  const memoryCols = db.prepare("PRAGMA table_info(memories)").all() as Array<{ name: string }>;
  const hasCol = (n: string) => memoryCols.some((c) => c.name === n);
  if (memoryCols.length > 0 && !hasCol("why")) {
    db.exec("ALTER TABLE memories ADD COLUMN why TEXT DEFAULT NULL");
  }
  if (memoryCols.length > 0 && !hasCol("how_to_apply")) {
    db.exec("ALTER TABLE memories ADD COLUMN how_to_apply TEXT DEFAULT NULL");
  }
}

/**
 * v3 → v4 迁移：todos / chapters / scheduled_task_bindings
 */
function migrateV3ToV4(db: Database.Database): void {
  const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>;
  const tableNames = new Set(tables.map((t) => t.name));

  if (!tableNames.has("todos")) {
    db.exec(`
      CREATE TABLE todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL DEFAULT 'main',
        session_id TEXT NOT NULL DEFAULT '',
        content TEXT NOT NULL,
        active_form TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','in_progress','completed')),
        position INTEGER NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
      );
      CREATE INDEX idx_todos_agent_session ON todos(agent_id, session_id);
      CREATE INDEX idx_todos_agent_status ON todos(agent_id, status);
    `);
  }

  if (!tableNames.has("chapters")) {
    db.exec(`
      CREATE TABLE chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL DEFAULT 'main',
        session_id TEXT NOT NULL DEFAULT '',
        title TEXT NOT NULL,
        summary TEXT DEFAULT '',
        created_at TEXT DEFAULT (datetime('now'))
      );
      CREATE INDEX idx_chapters_agent_session ON chapters(agent_id, session_id, created_at DESC);
    `);
  }

  if (!tableNames.has("scheduled_task_bindings")) {
    db.exec(`
      CREATE TABLE scheduled_task_bindings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL DEFAULT 'main',
        name TEXT NOT NULL,
        cron_ref TEXT NOT NULL,
        instructions TEXT NOT NULL DEFAULT '',
        enabled INTEGER NOT NULL DEFAULT 1,
        last_fired_at TEXT,
        created_at TEXT DEFAULT (datetime('now'))
      );
      CREATE INDEX idx_scheduled_agent ON scheduled_task_bindings(agent_id);
    `);
  }
}

let _db: Database.Database | null = null;
let _dbInitError: string | null = null;

export type { Database };

/**
 * 同步初始化数据库连接（仅在插件启动时由 index.ts 调用一次）。
 * v5.7.17: sync 化以适配 openclaw plugin loader 对 register() 同步返回的硬约束。
 * 用 createRequire 加载 better-sqlite3，失败可以被 try/catch 截获。
 */
export function initDb(
  openclawDir: string,
  extDir?: string,
  log?: { warn: (msg: string) => void; info?: (msg: string) => void },
): Database.Database {
  if (_db) return _db;

  const resolvedExtDir = extDir ?? join(openclawDir, "extensions", "enhance");
  const result = ensureSqlite(openclawDir, resolvedExtDir, log ?? { warn: console.warn });
  if (!result.ok) {
    _dbInitError = result.error;
    throw new Error(`better-sqlite3 原生绑定不可用：${result.error}\n修复命令：${result.repairCmd}`);
  }

  const memoryDir = join(openclawDir, "memory");
  if (!existsSync(memoryDir)) mkdirSync(memoryDir, { recursive: true });

  const dbPath = join(memoryDir, "enhance-memory.sqlite");
  _db = new result.Database(dbPath);
  _db.pragma("journal_mode = WAL");

  // 检测是否需要迁移 v1 表
  const tables = _db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all() as Array<{ name: string }>;
  if (tables.some((t) => t.name === "memories")) {
    migrateV1ToV2(_db);
  } else {
    _db.exec(SCHEMA_V2);
  }

  // v2 → v3: 新增宠物和通知表
  migrateV2ToV3(_db);
  // v3 → v4: todos / chapters / scheduled_task_bindings
  migrateV3ToV4(_db);
  // v4 → v5: memories 加 why / how_to_apply
  migrateV4ToV5(_db);
  // v5 → v6 (v5.8.0): hook-profiler 两张表 prep_stage_metrics / hook_profile
  migrateV5ToV6(_db);
  // v6 → v7 (v6.5.6): context-watchdog ctx_usage 表（会话级 token 累加跨重启持久化）
  migrateV6ToV7(_db);
  // v7 → v8 (v6.6.0): ctx_usage 加 estimated_cost_usd 列（cost-aware 切换）
  migrateV7ToV8(_db);

  // v5.7.2: 启动期清理 safety_log / notifications 90 天前的旧记录，避免无限增长
  // 异步 fire-and-forget，不阻塞插件加载
  try {
    _db.exec(`
      DELETE FROM safety_log WHERE created_at < datetime('now', '-90 days');
      DELETE FROM notifications WHERE created_at < datetime('now', '-90 days');
    `);
  } catch {
    // 静默失败 — 旧表不存在或权限错误不影响插件正常工作
  }

  return _db;
}

/**
 * 同步获取已初始化的数据库实例。
 * 必须在 initDb() 成功后调用；否则抛出明确的错误。
 * 供各模块在注册期使用（此时 DB 已由 index.ts 初始化完毕）。
 */
export function getDb(): Database.Database {
  if (_db) return _db;
  if (_dbInitError) {
    throw new Error(`better-sqlite3 未初始化：${_dbInitError}`);
  }
  throw new Error("better-sqlite3 未初始化：initDb() 尚未调用或已失败");
}

/** v5.7.2: 暴露给运维 / enhance_memory_purge 调用的清理函数 */
export function purgeOldSafetyLogs(db: Database.Database, retentionDays: number = 90): { deleted: number } {
  const result = db
    .prepare(`DELETE FROM safety_log WHERE created_at < datetime('now', ?)`)
    .run(`-${retentionDays} days`);
  return { deleted: result.changes };
}

// ── 记忆操作（全部按 agentId 隔离）──

export function storeMemory(
  db: Database.Database,
  agentId: string,
  category: MemoryCategory,
  content: string,
  tags: string = "",
  importance: number = 5,
  sessionId: string = "",
  extras: { why?: string; howToApply?: string } = {},
): MemoryEntry {
  const stmt = db.prepare(
    `INSERT INTO memories (agent_id, category, content, tags, importance, session_id, why, how_to_apply)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
  );
  const result = stmt.run(
    agentId,
    category,
    content,
    tags,
    Math.min(10, Math.max(1, importance)),
    sessionId,
    extras.why ?? null,
    extras.howToApply ?? null,
  );
  return db.prepare("SELECT * FROM memories WHERE id = ?").get(result.lastInsertRowid) as MemoryEntry;
}

export function searchMemories(
  db: Database.Database,
  agentId: string,
  opts: {
    category?: MemoryCategory;
    keyword?: string;
    limit?: number;
    since?: string;
  } = {},
): MemoryEntry[] {
  const conditions: string[] = ["agent_id = ?"];
  const params: unknown[] = [agentId];

  if (opts.category) {
    conditions.push("category = ?");
    params.push(opts.category);
  }
  if (opts.keyword) {
    conditions.push("(content LIKE ? OR tags LIKE ?)");
    params.push(`%${opts.keyword}%`, `%${opts.keyword}%`);
  }
  if (opts.since) {
    conditions.push("created_at >= ?");
    params.push(opts.since);
  }

  const where = `WHERE ${conditions.join(" AND ")}`;
  const limit = opts.limit ?? 20;

  return db
    .prepare(`SELECT * FROM memories ${where} ORDER BY importance DESC, created_at DESC, id DESC LIMIT ?`)
    .all(...params, limit) as MemoryEntry[];
}

export function getRecentMemories(db: Database.Database, agentId: string, limit: number = 5): MemoryEntry[] {
  return db
    .prepare("SELECT * FROM memories WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?")
    .all(agentId, limit) as MemoryEntry[];
}

export function deleteMemory(db: Database.Database, agentId: string, id: number): boolean {
  const result = db.prepare("DELETE FROM memories WHERE id = ? AND agent_id = ?").run(id, agentId);
  return result.changes > 0;
}

/**
 * 按 tag / category / contentLike 批量清理记忆（agentId 隔离）。
 * dry_run=true 时只 SELECT 不 DELETE，返回匹配条数（v5.7.1 hot-fix 用）。
 */
export function purgeMemories(
  db: Database.Database,
  agentId: string,
  opts: {
    tag?: string;
    category?: MemoryCategory;
    contentLike?: string;
    dryRun?: boolean;
  },
): { matched: number } {
  const conditions: string[] = ["agent_id = ?"];
  const params: unknown[] = [agentId];
  if (opts.tag) {
    conditions.push("tags LIKE ?");
    params.push(`%${opts.tag}%`);
  }
  if (opts.category) {
    conditions.push("category = ?");
    params.push(opts.category);
  }
  if (opts.contentLike) {
    conditions.push("content LIKE ?");
    params.push(`%${opts.contentLike}%`);
  }
  const where = `WHERE ${conditions.join(" AND ")}`;
  const matched = (db.prepare(`SELECT COUNT(*) AS c FROM memories ${where}`).get(...params) as {
    c: number;
  }).c;
  if (!opts.dryRun) {
    db.prepare(`DELETE FROM memories ${where}`).run(...params);
  }
  return { matched };
}

export function getMemoryStats(db: Database.Database, agentId?: string): Record<string, number> {
  const query = agentId
    ? "SELECT category, COUNT(*) as count FROM memories WHERE agent_id = ? GROUP BY category"
    : "SELECT category, COUNT(*) as count FROM memories GROUP BY category";
  const rows = (agentId
    ? db.prepare(query).all(agentId)
    : db.prepare(query).all()
  ) as Array<{ category: string; count: number }>;
  const stats: Record<string, number> = { total: 0 };
  for (const row of rows) {
    stats[row.category] = row.count;
    stats.total += row.count;
  }
  return stats;
}

/** 获取所有已知的 agentId 列表 */
export function getAllAgentIds(db: Database.Database): string[] {
  const rows = db
    .prepare("SELECT DISTINCT agent_id FROM memories UNION SELECT DISTINCT agent_id FROM safety_log")
    .all() as Array<{ agent_id: string }>;
  return rows.map((r) => r.agent_id);
}

// ── 安全日志操作（全部按 agentId 隔离）──

export function logSafetyEvent(
  db: Database.Database,
  agentId: string,
  tool: string,
  params: string,
  action: string,
  rule: string = "",
  reason: string = "",
): void {
  db.prepare(
    `INSERT INTO safety_log (agent_id, tool, params, action, rule, reason) VALUES (?, ?, ?, ?, ?, ?)`,
  ).run(agentId, tool, params, action, rule, reason);
}

export function getRecentSafetyEvents(
  db: Database.Database,
  agentId?: string,
  limit: number = 20,
): Array<{ id: number; agent_id: string; tool: string; params: string; action: string; rule: string; reason: string; created_at: string }> {
  if (agentId) {
    return db
      .prepare("SELECT * FROM safety_log WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?")
      .all(agentId, limit) as any[];
  }
  return db
    .prepare("SELECT * FROM safety_log ORDER BY created_at DESC LIMIT ?")
    .all(limit) as any[];
}

export function getSafetyStats(
  db: Database.Database,
  agentId?: string,
): { total: number; blocked: number; logged: number } {
  const where = agentId ? "WHERE agent_id = ?" : "";
  const row = (agentId
    ? db.prepare(
        `SELECT
           COUNT(*) as total,
           SUM(CASE WHEN action = 'block' THEN 1 ELSE 0 END) as blocked,
           SUM(CASE WHEN action = 'log' THEN 1 ELSE 0 END) as logged
         FROM safety_log ${where}`,
      ).get(agentId)
    : db.prepare(
        `SELECT
           COUNT(*) as total,
           SUM(CASE WHEN action = 'block' THEN 1 ELSE 0 END) as blocked,
           SUM(CASE WHEN action = 'log' THEN 1 ELSE 0 END) as logged
         FROM safety_log`,
      ).get()
  ) as any;
  return { total: row.total ?? 0, blocked: row.blocked ?? 0, logged: row.logged ?? 0 };
}

// ── 火苗宠物操作 ──

const XP_PER_LEVEL = (level: number) => 50 + level * 30;

const SIZE_FOR_LEVEL = (level: number): "tiny" | "small" | "medium" | "large" =>
  level <= 5 ? "tiny" : level <= 15 ? "small" : level <= 30 ? "medium" : "large";

const COLOR_FOR_STATS = (stats: FlameStats): FlameColor => {
  const entries: [keyof FlameStats, FlameColor][] = [
    ["warmth", "orange"], ["brightness", "white"], ["stability", "blue"],
    ["spark", "purple"], ["endurance", "green"],
  ];
  let max = 0; let color: FlameColor = "orange";
  for (const [key, c] of entries) {
    if (stats[key] > max) { max = stats[key]; color = c; }
  }
  return color;
};

const PERSONALITY_FOR_STATS = (stats: FlameStats): string => {
  const entries: [keyof FlameStats, string][] = [
    ["warmth", "温暖守护者"], ["brightness", "明亮引路人"], ["stability", "沉稳磐石"],
    ["spark", "灵感火花"], ["endurance", "不灭之焰"],
  ];
  let max = 0; let p = "温暖守护者";
  for (const [key, label] of entries) {
    if (stats[key] > max) { max = stats[key]; p = label; }
  }
  return p;
};

function rowToPet(row: any): FlamePet {
  const stats: FlameStats = {
    warmth: row.stat_warmth, brightness: row.stat_brightness,
    stability: row.stat_stability, spark: row.stat_spark, endurance: row.stat_endurance,
  };
  return {
    agent_id: row.agent_id, name: row.name, color: row.color as FlameColor,
    size: SIZE_FOR_LEVEL(row.level), level: row.level, xp: row.xp,
    total_xp: row.total_xp, mood: "idle", stats,
    personality: PERSONALITY_FOR_STATS(stats),
    created_at: row.created_at, updated_at: row.updated_at,
  };
}

export function getOrCreatePet(db: Database.Database, agentId: string, defaultName?: string, defaultColor?: FlameColor): FlamePet {
  let row = db.prepare("SELECT * FROM flame_pets WHERE agent_id = ?").get(agentId) as any;
  if (!row) {
    db.prepare("INSERT INTO flame_pets (agent_id, name, color) VALUES (?, ?, ?)").run(
      agentId, defaultName ?? "小火苗", defaultColor ?? "orange",
    );
    row = db.prepare("SELECT * FROM flame_pets WHERE agent_id = ?").get(agentId);
  }
  return rowToPet(row);
}

export function addPetXp(
  db: Database.Database, agentId: string,
  xpGain: number, statBoosts?: Partial<FlameStats>,
): { pet: FlamePet; leveledUp: boolean; oldLevel: number } {
  const pet = getOrCreatePet(db, agentId);
  const oldLevel = pet.level;
  let xp = pet.xp + xpGain;
  let level = pet.level;
  let totalXp = pet.total_xp + xpGain;

  // 升级循环
  while (xp >= XP_PER_LEVEL(level) && level < 50) {
    xp -= XP_PER_LEVEL(level);
    level++;
  }
  if (level >= 50) xp = Math.min(xp, XP_PER_LEVEL(50));

  // 属性加成
  const w = Math.min(100, pet.stats.warmth + (statBoosts?.warmth ?? 0));
  const b = Math.min(100, pet.stats.brightness + (statBoosts?.brightness ?? 0));
  const st = Math.min(100, pet.stats.stability + (statBoosts?.stability ?? 0));
  const sp = Math.min(100, pet.stats.spark + (statBoosts?.spark ?? 0));
  const e = Math.min(100, pet.stats.endurance + (statBoosts?.endurance ?? 0));

  // 升级时自动推导颜色
  const stats: FlameStats = { warmth: w, brightness: b, stability: st, spark: sp, endurance: e };
  const color = level !== oldLevel ? COLOR_FOR_STATS(stats) : pet.color;

  db.prepare(`
    UPDATE flame_pets SET level=?, xp=?, total_xp=?, color=?,
      stat_warmth=?, stat_brightness=?, stat_stability=?, stat_spark=?, stat_endurance=?,
      updated_at=datetime('now')
    WHERE agent_id=?
  `).run(level, xp, totalXp, color, w, b, st, sp, e, agentId);

  const updated = getOrCreatePet(db, agentId);
  return { pet: updated, leveledUp: level > oldLevel, oldLevel };
}

export function renamePet(db: Database.Database, agentId: string, name: string): void {
  getOrCreatePet(db, agentId);
  db.prepare("UPDATE flame_pets SET name=?, updated_at=datetime('now') WHERE agent_id=?").run(name, agentId);
}

export function setPetColor(db: Database.Database, agentId: string, color: FlameColor): void {
  getOrCreatePet(db, agentId);
  db.prepare("UPDATE flame_pets SET color=?, updated_at=datetime('now') WHERE agent_id=?").run(color, agentId);
}

// ── 通知操作 ──

export function emitNotification(
  db: Database.Database, agentId: string,
  level: NotificationLevel, source: NotificationSource,
  title: string, detail: string = "",
): void {
  db.prepare(
    "INSERT INTO notifications (agent_id, level, source, title, detail) VALUES (?, ?, ?, ?, ?)",
  ).run(agentId, level, source, title, detail);
}

export function getRecentNotifications(db: Database.Database, agentId?: string, limit: number = 20): Notification[] {
  if (agentId) {
    return db.prepare(
      "SELECT * FROM notifications WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?",
    ).all(agentId, limit) as any[];
  }
  return db.prepare(
    "SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?",
  ).all(limit) as any[];
}

export function getUnreadNotificationCount(db: Database.Database, agentId?: string): number {
  const row = agentId
    ? db.prepare("SELECT COUNT(*) as c FROM notifications WHERE agent_id=? AND read=0").get(agentId) as any
    : db.prepare("SELECT COUNT(*) as c FROM notifications WHERE read=0").get() as any;
  return row?.c ?? 0;
}

export function markNotificationRead(db: Database.Database, id: number): void {
  db.prepare("UPDATE notifications SET read=1 WHERE id=?").run(id);
}

export function pruneNotifications(db: Database.Database, maxRetained: number): void {
  const count = (db.prepare("SELECT COUNT(*) as c FROM notifications").get() as any)?.c ?? 0;
  if (count > maxRetained * 1.5) {
    db.prepare(`
      DELETE FROM notifications WHERE id NOT IN (
        SELECT id FROM notifications ORDER BY created_at DESC LIMIT ?
      )
    `).run(maxRetained);
  }
}

// ── Todo 操作 ──

export interface TodoInput {
  content: string;
  activeForm: string;
  status?: TodoStatus;
}

export function replaceTodos(
  db: Database.Database,
  agentId: string,
  sessionId: string,
  todos: TodoInput[],
): TodoEntry[] {
  const tx = db.transaction(() => {
    db.prepare("DELETE FROM todos WHERE agent_id = ? AND session_id = ?").run(agentId, sessionId);
    const insert = db.prepare(
      `INSERT INTO todos (agent_id, session_id, content, active_form, status, position)
       VALUES (?, ?, ?, ?, ?, ?)`,
    );
    todos.forEach((t, i) => {
      insert.run(agentId, sessionId, t.content, t.activeForm, t.status ?? "pending", i);
    });
  });
  tx();
  return listTodos(db, agentId, sessionId);
}

export function listTodos(db: Database.Database, agentId: string, sessionId?: string): TodoEntry[] {
  if (sessionId) {
    return db
      .prepare(
        `SELECT * FROM todos WHERE agent_id = ? AND session_id = ? ORDER BY position ASC, id ASC`,
      )
      .all(agentId, sessionId) as TodoEntry[];
  }
  return db
    .prepare(
      `SELECT * FROM todos WHERE agent_id = ? ORDER BY updated_at DESC, position ASC LIMIT 200`,
    )
    .all(agentId) as TodoEntry[];
}

export function updateTodoStatus(
  db: Database.Database,
  agentId: string,
  sessionId: string,
  position: number,
  status: TodoStatus,
): TodoEntry | null {
  db.prepare(
    `UPDATE todos SET status = ?, updated_at = datetime('now')
     WHERE agent_id = ? AND session_id = ? AND position = ?`,
  ).run(status, agentId, sessionId, position);
  return (
    (db
      .prepare(`SELECT * FROM todos WHERE agent_id = ? AND session_id = ? AND position = ?`)
      .get(agentId, sessionId, position) as TodoEntry | undefined) ?? null
  );
}

export function getLatestTodos(db: Database.Database, agentId: string): TodoEntry[] {
  const sessionRow = db
    .prepare(
      `SELECT session_id FROM todos WHERE agent_id = ? ORDER BY updated_at DESC LIMIT 1`,
    )
    .get(agentId) as { session_id?: string } | undefined;
  if (!sessionRow?.session_id) return [];
  return listTodos(db, agentId, sessionRow.session_id);
}

// ── Chapter 操作 ──

export function addChapter(
  db: Database.Database,
  agentId: string,
  sessionId: string,
  title: string,
  summary = "",
): ChapterMark {
  const r = db
    .prepare(
      `INSERT INTO chapters (agent_id, session_id, title, summary) VALUES (?, ?, ?, ?)`,
    )
    .run(agentId, sessionId, title, summary);
  return db
    .prepare(`SELECT * FROM chapters WHERE id = ?`)
    .get(r.lastInsertRowid) as ChapterMark;
}

export function listChapters(
  db: Database.Database,
  agentId: string,
  sessionId?: string,
  limit = 50,
): ChapterMark[] {
  if (sessionId) {
    return db
      .prepare(
        `SELECT * FROM chapters WHERE agent_id = ? AND session_id = ? ORDER BY created_at ASC LIMIT ?`,
      )
      .all(agentId, sessionId, limit) as ChapterMark[];
  }
  return db
    .prepare(
      `SELECT * FROM chapters WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?`,
    )
    .all(agentId, limit) as ChapterMark[];
}

// ── Scheduled task binding 操作 ──

export interface ScheduledTaskBinding {
  id: number;
  agent_id: string;
  name: string;
  cron_ref: string;
  instructions: string;
  enabled: number;
  last_fired_at: string | null;
  created_at: string;
}

export function upsertScheduledBinding(
  db: Database.Database,
  agentId: string,
  name: string,
  cronRef: string,
  instructions: string,
): ScheduledTaskBinding {
  const existing = db
    .prepare(`SELECT * FROM scheduled_task_bindings WHERE agent_id = ? AND name = ?`)
    .get(agentId, name) as ScheduledTaskBinding | undefined;
  if (existing) {
    db.prepare(
      `UPDATE scheduled_task_bindings SET cron_ref = ?, instructions = ?, enabled = 1 WHERE id = ?`,
    ).run(cronRef, instructions, existing.id);
    return {
      ...existing,
      cron_ref: cronRef,
      instructions,
      enabled: 1,
    };
  }
  const r = db
    .prepare(
      `INSERT INTO scheduled_task_bindings (agent_id, name, cron_ref, instructions) VALUES (?, ?, ?, ?)`,
    )
    .run(agentId, name, cronRef, instructions);
  return db
    .prepare(`SELECT * FROM scheduled_task_bindings WHERE id = ?`)
    .get(r.lastInsertRowid) as ScheduledTaskBinding;
}

export function listScheduledBindings(
  db: Database.Database,
  agentId?: string,
): ScheduledTaskBinding[] {
  if (agentId) {
    return db
      .prepare(
        `SELECT * FROM scheduled_task_bindings WHERE agent_id = ? ORDER BY created_at DESC`,
      )
      .all(agentId) as ScheduledTaskBinding[];
  }
  return db
    .prepare(`SELECT * FROM scheduled_task_bindings ORDER BY created_at DESC`)
    .all() as ScheduledTaskBinding[];
}

export function disableScheduledBinding(
  db: Database.Database,
  agentId: string,
  name: string,
): boolean {
  const r = db
    .prepare(
      `UPDATE scheduled_task_bindings SET enabled = 0 WHERE agent_id = ? AND name = ?`,
    )
    .run(agentId, name);
  return r.changes > 0;
}

export function touchScheduledBindingFired(
  db: Database.Database,
  id: number,
): void {
  db.prepare(
    `UPDATE scheduled_task_bindings SET last_fired_at = datetime('now') WHERE id = ?`,
  ).run(id);
}
