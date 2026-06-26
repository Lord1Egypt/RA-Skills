import Database from "better-sqlite3";
import path from "path";
import os from "os";
import fs from "fs";
import type { OrchardConfig } from "../config.js";

export function resolveDbPath(configPath?: string): string {
  const raw = configPath ?? "~/.openclaw/orchard/orchard.db";
  if (raw.startsWith("~")) {
    return path.join(os.homedir(), raw.slice(1));
  }
  return raw;
}

export function openDb(dbPath: string): Database.Database {
  const dir = path.dirname(dbPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const db = new Database(dbPath);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");
  return db;
}

export function initSchema(db: Database.Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS projects (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      goal TEXT NOT NULL,
      status TEXT DEFAULT 'active',
      completion_score REAL DEFAULT 0,
      completion_temperature REAL DEFAULT 0.7,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id TEXT NOT NULL,
      parent_task_id INTEGER,
      title TEXT NOT NULL,
      description TEXT,
      acceptance_criteria TEXT,
      priority TEXT DEFAULT 'medium',
      status TEXT DEFAULT 'pending',
      assigned_role TEXT DEFAULT 'executor',
      model_override TEXT,
      blocker_reason TEXT,
      retry_count INTEGER DEFAULT 0,
      next_attempt_at DATETIME,
      created_by TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (project_id) REFERENCES projects(id),
      FOREIGN KEY (parent_task_id) REFERENCES tasks(id)
    );

    CREATE TABLE IF NOT EXISTS task_runs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id INTEGER NOT NULL,
      role TEXT NOT NULL,
      model TEXT,
      session_key TEXT,
      status TEXT DEFAULT 'running',
      owner_token TEXT,
      timeout_at DATETIME,
      timeout_reason TEXT,
      input TEXT,
      output TEXT,
      qa_verdict TEXT,
      qa_notes TEXT,
      started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      ended_at DATETIME,
      FOREIGN KEY (task_id) REFERENCES tasks(id)
    );

    CREATE TABLE IF NOT EXISTS task_blockers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id INTEGER NOT NULL,
      blocked_by_task_id INTEGER,
      reason TEXT,
      resolved_at DATETIME,
      FOREIGN KEY (task_id) REFERENCES tasks(id)
    );

    CREATE TABLE IF NOT EXISTS task_comments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id INTEGER NOT NULL,
      author TEXT,
      content TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (task_id) REFERENCES tasks(id)
    );

    CREATE TABLE IF NOT EXISTS project_knowledge (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id TEXT NOT NULL,
      content TEXT NOT NULL,
      embedding TEXT,
      source TEXT,
      task_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS config_safety_profiles (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      enabled INTEGER DEFAULT 1,
      doc_urls TEXT DEFAULT '[]',
      knowledge_sources TEXT DEFAULT '[]',
      watchdog_inject INTEGER DEFAULT 1,
      custom_rules TEXT DEFAULT '',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS circuit_breakers (
      scope TEXT PRIMARY KEY,
      failure_count INTEGER DEFAULT 0,
      last_failure_at DATETIME,
      open_until DATETIME,
      last_error TEXT,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);

  try {
    db.exec(`ALTER TABLE tasks ADD COLUMN next_attempt_at DATETIME`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN owner_token TEXT`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN timeout_at DATETIME`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN timeout_reason TEXT`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN subagent_run_id TEXT`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN child_session_keys TEXT`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN last_activity_at DATETIME`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN cleanup_status TEXT`);
  } catch {}
  try {
    db.exec(`ALTER TABLE task_runs ADD COLUMN stall_reason TEXT`);
  } catch {}
}

export function seedSettings(db: Database.Database, cfg: OrchardConfig): void {
  const defaults: Record<string, unknown> = {
    'executor.model': cfg.roles?.executor?.model ?? 'openai/gpt-4o',
    'executor.timeoutSeconds': cfg.roles?.executor?.timeoutSeconds ?? 1800,
    'executor.retryLimit': cfg.roles?.executor?.retryLimit ?? 3,
    'architect.enabled': cfg.roles?.architect?.enabled ?? false,
    'architect.model': cfg.roles?.architect?.model ?? 'openai/gpt-4o',
    'architect.wakeEvery': cfg.roles?.architect?.wakeEvery ?? '6h',
    'qa.enabled': cfg.roles?.qa?.enabled ?? false,
    'qa.model': cfg.roles?.qa?.model ?? 'openai/gpt-4o',
    'qa.autoApproveThreshold': cfg.roles?.qa?.autoApproveThreshold ?? 0.85,
    'reporter.enabled': cfg.roles?.reporter?.enabled ?? false,
    'reporter.channel': cfg.roles?.reporter?.channel ?? '',
    'reporter.channelId': cfg.roles?.reporter?.channelId ?? '',
    'debug.enabled': cfg.debug?.enabled ?? false,
    'debug.verbose': cfg.debug?.verbose ?? false,
    'debug.logOnly': cfg.debug?.logOnly ?? false,
    'debug.dryRun': cfg.debug?.dryRun ?? false,
    'debug.disableAllSpawns': cfg.debug?.disableAllSpawns ?? false,
    'debug.disableExecutorSpawns': cfg.debug?.disableExecutorSpawns ?? false,
    'debug.disableQaSpawns': cfg.debug?.disableQaSpawns ?? false,
    'debug.disableArchitectSpawns': cfg.debug?.disableArchitectSpawns ?? false,
    'debug.preserveSessions': cfg.debug?.preserveSessions ?? false,
    'debug.circuitBreaker.enabled': true,
    'debug.circuitBreaker.failureThreshold': 3,
    'debug.circuitBreaker.cooldownMs': 300000,
    'limits.enabled': cfg.limits?.enabled ?? true,
    'limits.maxConcurrentExecutors': cfg.limits?.maxConcurrentExecutors ?? 2,
    'limits.maxTasksPerHour': cfg.limits?.maxTasksPerHour ?? 10,
    'limits.maxSubagentsPerProject': cfg.limits?.maxSubagentsPerProject ?? 3,
    'limits.cooldownOnFailureMs': cfg.limits?.cooldownOnFailureMs ?? 60000,
    'limits.stalledSessionIdleMs': cfg.limits?.stalledSessionIdleMs ?? 900000,
    'limits.orphanedSessionGraceMs': cfg.limits?.orphanedSessionGraceMs ?? 120000,
    'queue.intervalMs': cfg.queueIntervalMs ?? 300000,
  };
  const upsert = db.prepare(`INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)`);
  for (const [k, v] of Object.entries(defaults)) {
    upsert.run(k, JSON.stringify(v));
  }

  // Seed default config-safety profile
  db.prepare(`
    INSERT OR IGNORE INTO config_safety_profiles (id, name, enabled, doc_urls, knowledge_sources, watchdog_inject, custom_rules)
    VALUES ('default', 'Default Safety Profile', 1, '["https://docs.openclaw.ai/llms.txt"]', '[]', 1, '')
  `).run();
}
