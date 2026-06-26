import type Database from "better-sqlite3";
import type { OrchardConfig } from "../config.js";
import {
  getMaxConcurrent,
  getExecutorModel,
  isDebugEnabled,
  isVerboseDebug,
  isLogOnlyMode,
  shouldSpawnExecutors,
  shouldSpawnQa,
} from "../config.js";
import { addKnowledge, searchKnowledge } from "../kb/knowledge.js";
import { isCircuitOpen, recordCircuitFailure, recordCircuitSuccess } from "./circuit-breaker.js";
import { isQueuePaused } from "./control.js";
import { getRuntimeState, updateProjectRuntimeState, updateRuntimeState } from "./runtime-state.js";
import { wakeArchitectForProject } from "../roles/architect.js";

interface RunningTask {
  taskId: number;
  projectId: string;
  startedAt: number;
}

interface FinalizeTaskRunParams {
  db: Database.Database;
  runtime?: any;
  cfg: OrchardConfig;
  logger: any;
  taskId: number;
  runId: number;
  projectId?: string | null;
  runStatus: "done" | "failed";
  taskStatus: "done" | "ready" | "failed" | "blocked";
  output: string;
  retryCount?: number;
  nextAttemptAt?: string | null;
  timeoutReason?: string | null;
  stallReason?: string | null;
  cleanupStatus?: string | null;
  blockerReason?: string | null;
  cleanupDescendants?: boolean;
}

const runningTasks = new Map<number, RunningTask>();
const dispatchTimes: number[] = [];

function parseSessionKeyList(raw: unknown): string[] {
  if (typeof raw !== "string" || !raw.trim()) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter((v): v is string => typeof v === "string" && v.trim().length > 0) : [];
  } catch {
    return [];
  }
}

function getDescendantTaskIds(db: Database.Database, rootTaskId: number): number[] {
  const descendants: number[] = [];
  const queue = [rootTaskId];
  const seen = new Set<number>(queue);
  const stmt = db.prepare(`SELECT id FROM tasks WHERE parent_task_id = ?`);
  while (queue.length > 0) {
    const current = queue.shift()!;
    const children = stmt.all(current) as Array<{ id: number }>;
    for (const child of children) {
      if (seen.has(child.id)) continue;
      seen.add(child.id);
      descendants.push(child.id);
      queue.push(child.id);
    }
  }
  return descendants;
}

function cleanupDescendantTasks(db: Database.Database, taskId: number, reason: string): number {
  const descendantIds = getDescendantTaskIds(db, taskId);
  if (descendantIds.length === 0) return 0;
  const placeholders = descendantIds.map(() => "?").join(", ");
  const activeStatuses = ["pending", "ready", "assigned", "running"];
  const result = db.prepare(`
    UPDATE tasks
    SET status = 'blocked', blocker_reason = COALESCE(blocker_reason, ?), next_attempt_at = NULL, updated_at = CURRENT_TIMESTAMP
    WHERE id IN (${placeholders}) AND status IN (${activeStatuses.map(() => "?").join(", ")})
  `).run(reason, ...descendantIds, ...activeStatuses);
  return Number(result.changes ?? 0);
}

async function cleanupRunSessions(runtime: any, logger: any, sessionKeys: string[]): Promise<number> {
  if (!runtime?.subagent?.deleteSession) return 0;
  let cleaned = 0;
  for (const sessionKey of [...new Set(sessionKeys.filter(Boolean))]) {
    try {
      await runtime.subagent.deleteSession({ sessionKey, deleteTranscript: false });
      cleaned++;
    } catch (err: any) {
      logger?.debug?.(`[orchard] session cleanup skipped for ${sessionKey}: ${err?.message ?? String(err)}`);
    }
  }
  return cleaned;
}

export async function finalizeTaskRun(params: FinalizeTaskRunParams): Promise<{ cleanedSessions: number; cleanedDescendants: number }> {
  const {
    db,
    runtime,
    cfg: _cfg,
    logger,
    taskId,
    runId,
    projectId,
    runStatus,
    taskStatus,
    output,
    retryCount,
    nextAttemptAt,
    timeoutReason,
    stallReason,
    cleanupStatus,
    blockerReason,
    cleanupDescendants = runStatus === "failed",
  } = params;

  const run = db.prepare(`SELECT session_key, child_session_keys FROM task_runs WHERE id = ?`).get(runId) as any;
  db.prepare(`
    UPDATE task_runs
    SET status = ?, output = ?, timeout_reason = ?, stall_reason = ?, cleanup_status = ?, ended_at = CURRENT_TIMESTAMP
    WHERE id = ?
  `).run(
    runStatus,
    output,
    timeoutReason ?? null,
    stallReason ?? null,
    cleanupStatus ?? null,
    runId,
  );

  const taskFields = ["status = ?", "updated_at = CURRENT_TIMESTAMP"];
  const taskValues: any[] = [taskStatus];
  if (blockerReason !== undefined) {
    taskFields.push("blocker_reason = ?");
    taskValues.push(blockerReason);
  }
  if (nextAttemptAt !== undefined) {
    taskFields.push("next_attempt_at = ?");
    taskValues.push(nextAttemptAt);
  }
  if (retryCount !== undefined) {
    taskFields.push("retry_count = ?");
    taskValues.push(retryCount);
  }
  taskValues.push(taskId);
  db.prepare(`UPDATE tasks SET ${taskFields.join(", ")} WHERE id = ?`).run(...taskValues);

  const sessionKeys = [run?.session_key, ...parseSessionKeyList(run?.child_session_keys)].filter((v): v is string => Boolean(v));
  const cleanedSessions = await cleanupRunSessions(runtime, logger, sessionKeys);

  let cleanedDescendants = 0;
  if (cleanupDescendants) {
    cleanedDescendants = cleanupDescendantTasks(db, taskId, blockerReason ?? output);
  }

  runningTasks.delete(taskId);
  if (projectId) {
    updateProjectRuntimeState(db, String(projectId), {
      lastQueueTickAt: new Date().toISOString(),
      lastQueueSkipReason: cleanupStatus ? `${cleanupStatus}:task-${taskId}` : null,
    });
  }

  return { cleanedSessions, cleanedDescendants };
}
// Per-slot pacing state. Keeps last N dispatch timestamps where N = maxConcurrent.
// slotDispatchTimes[0] is always the oldest ("least recently used slot").
const slotDispatchTimes: number[] = [];
let tickInFlight = false;
let tickRerunRequested = false;
let lastTickSummary: Record<string, unknown> = {
  startedAt: null,
  finishedAt: null,
  projectsScanned: 0,
  readyTasksSeen: 0,
  dispatched: 0,
  skipped: [],
  projectDetails: [],
};

/**
 * Manual reap — callable from debug control endpoint.
 * Uses zero idle cutoff so it catches ALL stalled runs regardless of idleMs config.
 */
export async function reapStalledRunsManual(
  db: Database.Database,
  runtime: any,
  cfg: OrchardConfig,
  logger: any,
  taskId?: number
): Promise<{ reaped: number; cleanedSessions: number; cleanedDescendants: number }> {
  const retryLimit = cfg.roles?.executor?.retryLimit ?? 3;
  const baseCooldownMs = cfg.limits?.cooldownOnFailureMs ?? 60000;

  const query = taskId
    ? db.prepare(`SELECT tr.id, tr.task_id, tr.session_key, t.retry_count, t.project_id FROM task_runs tr JOIN tasks t ON t.id = tr.task_id WHERE tr.status = 'running' AND tr.task_id = ?`).all(taskId)
    : db.prepare(`SELECT tr.id, tr.task_id, tr.session_key, t.retry_count, t.project_id FROM task_runs tr JOIN tasks t ON t.id = tr.task_id WHERE tr.status = 'running'`).all();

  let cleanedSessions = 0;
  let cleanedDescendants = 0;
  for (const run of query as any[]) {
    const reason = `[orchard][reap] manual operator reap${taskId ? ` task=${taskId}` : ''}`;
    const retryCount = Number(run.retry_count ?? 0) + 1;
    const nextAttemptAt = retryCount <= retryLimit
      ? new Date(Date.now() + Math.min(baseCooldownMs * Math.pow(2, retryCount - 1), 30 * 60 * 1000)).toISOString()
      : null;
    const result = await finalizeTaskRun({
      db,
      runtime,
      cfg,
      logger,
      taskId: run.task_id,
      runId: run.id,
      projectId: run.project_id,
      runStatus: 'failed',
      taskStatus: retryCount <= retryLimit ? 'ready' : 'failed',
      output: reason,
      retryCount,
      nextAttemptAt,
      stallReason: reason,
      cleanupStatus: 'reaped',
      blockerReason: reason,
      cleanupDescendants: retryCount > retryLimit,
    });
    cleanedSessions += result.cleanedSessions;
    cleanedDescendants += result.cleanedDescendants;
    logger.warn(`[orchard] manual reap: task=${run.task_id} run=${run.id}`);
  }
  return { reaped: (query as any[]).length, cleanedSessions, cleanedDescendants };
}

// Exported so routes/tools can trigger a wake
let wakeCallback: (() => Promise<void>) | null = null;
export function setWakeCallback(cb: () => Promise<void>): void { wakeCallback = cb; }
export function getWakeCallback(): (() => Promise<void>) | null { return wakeCallback; }
export function getQueueDebugState(db?: Database.Database, cfg?: OrchardConfig): Record<string, unknown> {
  const globalCircuit = db ? isCircuitOpen(db, "global") : { open: false, state: null };
  const paused = db ? isQueuePaused(db) : false;
  const projectCircuits = db
    ? (db.prepare(`SELECT scope, failure_count, last_failure_at, open_until, last_error, updated_at FROM circuit_breakers WHERE scope LIKE 'project:%' ORDER BY scope`).all() as any[])
    : [];
  const timeoutRuns = db
    ? (db.prepare(`SELECT task_id, role, status, timeout_at, timeout_reason, started_at FROM task_runs WHERE timeout_at IS NOT NULL ORDER BY id DESC LIMIT 20`).all() as any[])
    : [];
  const runtimeState = db ? getRuntimeState(db) : { queue: {}, projects: {} };
  const projectSkipReasons = db
    ? (db.prepare(`
        SELECT
          p.id,
          p.name,
          (SELECT COUNT(*) FROM tasks t WHERE t.project_id = p.id AND t.status IN ('ready','assigned','running','blocked')) AS active_task_count,
          (SELECT COUNT(*) FROM tasks t WHERE t.project_id = p.id AND t.status = 'ready' AND t.next_attempt_at IS NOT NULL AND t.next_attempt_at > CURRENT_TIMESTAMP) AS cooling_down_count
        FROM projects p
        WHERE p.status = 'active'
        ORDER BY p.id
      `).all() as any[]).map((project: any) => ({
        ...project,
        runtime: runtimeState.projects?.[project.id] ?? {},
      }))
    : [];
  const spreadIntervalMs = cfg ? getSpreadIntervalMs(cfg) : null;
  return {
    runningTasks: Array.from(runningTasks.values()),
    runningCount: runningTasks.size,
    dispatchesLastHour: getTasksDispatchedLastHour(),
    wakeRegistered: Boolean(wakeCallback),
    queuePaused: paused,
    lastTickSummary,
    debug: cfg?.debug ?? {},
    pacing: {
      spreadTasksOverPeriod: cfg?.limits?.spreadTasksOverPeriod ?? false,
      minNextDelayMs: cfg?.limits?.minNextDelayMs ?? 0,
      spreadIntervalMs,
      slotDispatchTimes: [...slotDispatchTimes],
      nextSlotAvailableMs: cfg ? getNextSlotAvailableMs(cfg) : null,
    },
    runtimeState,
    timeouts: timeoutRuns,
    projects: projectSkipReasons,
    circuitBreaker: {
      global: globalCircuit,
      projects: projectCircuits,
    },
  };
}

function countRunningForProject(projectId: string): number {
  let count = 0;
  for (const t of runningTasks.values()) {
    if (t.projectId === projectId) count++;
  }
  return count;
}

function getTasksDispatchedLastHour(): number {
  const cutoff = Date.now() - 60 * 60 * 1000;
  while (dispatchTimes.length > 0 && dispatchTimes[0] < cutoff) dispatchTimes.shift();
  return dispatchTimes.length;
}

/**
 * Returns the per-slot spread interval in ms, or null if pacing is disabled.
 *
 * "Spread" mode: interval = (3600000 / maxPerHour) * maxConcurrent
 *   e.g. concurrent=1, perHour=10 → 6 min per slot
 *        concurrent=2, perHour=10 → 12 min per slot  (still 10/hr total)
 * "Min next delay" mode: a fixed ms floor, applied per slot.
 * Both can coexist — the larger value wins.
 */
function getSpreadIntervalMs(cfg: OrchardConfig): number | null {
  const maxConcurrent = getMaxConcurrent(cfg);
  const maxPerHour = cfg.limits?.maxTasksPerHour ?? 10;
  let intervalMs = 0;
  if (cfg.limits?.spreadTasksOverPeriod) {
    intervalMs = Math.max(intervalMs, Math.floor(3600000 / maxPerHour) * maxConcurrent);
  }
  const minDelay = cfg.limits?.minNextDelayMs ?? 0;
  if (minDelay > 0) {
    intervalMs = Math.max(intervalMs, minDelay);
  }
  return intervalMs > 0 ? intervalMs : null;
}

/**
 * Returns how many slots are ready to dispatch right now under pacing rules.
 * With no pacing configured always returns the full concurrent capacity.
 */
function availableSpreadSlots(cfg: OrchardConfig, capacityAvailable: number): number {
  const intervalMs = getSpreadIntervalMs(cfg);
  if (!intervalMs) return capacityAvailable;
  const maxConcurrent = getMaxConcurrent(cfg);
  const now = Date.now();
  let ready = 0;
  for (let i = 0; i < maxConcurrent; i++) {
    const lastTime = slotDispatchTimes[i] ?? 0;
    if (now - lastTime >= intervalMs) ready++;
  }
  return Math.min(ready, capacityAvailable);
}

/** Record a dispatch against a slot. Keeps slotDispatchTimes sorted oldest-first. */
function recordSlotDispatch(cfg: OrchardConfig): void {
  const maxConcurrent = getMaxConcurrent(cfg);
  // Replace the oldest slot time (index 0) with now, then re-sort so oldest is still [0]
  if (slotDispatchTimes.length < maxConcurrent) {
    slotDispatchTimes.push(Date.now());
  } else {
    slotDispatchTimes[0] = Date.now();
  }
  slotDispatchTimes.sort((a, b) => a - b);
}

/** Returns ms until the next slot becomes available (for debug/UI). */
export function getNextSlotAvailableMs(cfg: OrchardConfig): number | null {
  const intervalMs = getSpreadIntervalMs(cfg);
  if (!intervalMs) return null;
  if (slotDispatchTimes.length === 0) return 0;
  const maxConcurrent = getMaxConcurrent(cfg);
  const oldest = slotDispatchTimes[Math.min(maxConcurrent - 1, slotDispatchTimes.length - 1)];
  const wait = intervalMs - (Date.now() - oldest);
  return wait > 0 ? wait : 0;
}

async function enforceOverdueRuns(
  db: Database.Database,
  runtime: any,
  cfg: OrchardConfig,
  logger: any
): Promise<number> {
  const retryLimit = cfg.roles?.executor?.retryLimit ?? 3;
  const baseCooldownMs = cfg.limits?.cooldownOnFailureMs ?? 60000;
  const overdueRuns = db.prepare(`
    SELECT tr.id, tr.task_id, tr.timeout_at, tr.status, t.retry_count, t.project_id
    FROM task_runs tr
    JOIN tasks t ON t.id = tr.task_id
    WHERE tr.status = 'running'
      AND tr.timeout_at IS NOT NULL
      AND tr.timeout_at <= CURRENT_TIMESTAMP
  `).all() as any[];

  for (const run of overdueRuns) {
    const retryCount = Number(run.retry_count ?? 0) + 1;
    const backoffMs = Math.min(baseCooldownMs * Math.pow(2, retryCount - 1), 30 * 60 * 1000);
    const nextAttemptAt = retryCount <= retryLimit ? new Date(Date.now() + backoffMs).toISOString() : null;
    const timeoutReason = `[orchard][timeout] executor run overdue at ${run.timeout_at}`;

    await finalizeTaskRun({
      db,
      runtime,
      cfg,
      logger,
      taskId: run.task_id,
      runId: run.id,
      projectId: run.project_id,
      runStatus: 'failed',
      taskStatus: retryCount <= retryLimit ? 'ready' : 'failed',
      output: timeoutReason,
      retryCount,
      nextAttemptAt,
      timeoutReason,
      cleanupStatus: 'timed_out',
      blockerReason: timeoutReason,
      cleanupDescendants: retryCount > retryLimit,
    });
    logger.warn(`[orchard] timed out overdue executor run task=${run.task_id} run=${run.id} retry=${retryCount}/${retryLimit}`);
  }

  return overdueRuns.length;
}

/** Append a child session key to a run's child_session_keys JSON array. */
function appendChildSessionKey(db: Database.Database, runId: number, sessionKey: string): void {
  if (!sessionKey || sessionKey.length > 256) return;
  const row = db.prepare(`SELECT child_session_keys FROM task_runs WHERE id = ?`).get(runId) as any;
  let keys: string[] = [];
  try { keys = JSON.parse(row?.child_session_keys || '[]'); } catch {}
  if (keys.length >= 20) return; // cap to prevent unbounded growth
  if (!keys.includes(sessionKey)) {
    keys.push(sessionKey);
    db.prepare(`UPDATE task_runs SET child_session_keys = ? WHERE id = ?`).run(JSON.stringify(keys), runId);
  }
}

/** Touch last_activity_at for a run whenever new output is seen. */
function touchRunActivity(db: Database.Database, runId: number): void {
  db.prepare(`UPDATE task_runs SET last_activity_at = CURRENT_TIMESTAMP WHERE id = ?`).run(runId);
}

/**
 * Detect stalled runs: running but no activity for stalledSessionIdleMs.
 * Fails them and schedules retry like a timeout.
 */
async function enforceStalledRuns(
  db: Database.Database,
  runtime: any,
  cfg: OrchardConfig,
  logger: any
): Promise<number> {
  const idleMs = cfg.limits?.stalledSessionIdleMs ?? 900000;
  const retryLimit = cfg.roles?.executor?.retryLimit ?? 3;
  const baseCooldownMs = cfg.limits?.cooldownOnFailureMs ?? 60000;
  const cutoff = new Date(Date.now() - idleMs).toISOString();

  const stalledRuns = db.prepare(`
    SELECT tr.id, tr.task_id, tr.session_key, t.retry_count, t.project_id
    FROM task_runs tr
    JOIN tasks t ON t.id = tr.task_id
    WHERE tr.status = 'running'
      AND (
        tr.timeout_at <= CURRENT_TIMESTAMP
        OR (tr.last_activity_at IS NOT NULL AND tr.last_activity_at < ?)
      )
  `).all(cutoff) as any[];

  for (const run of stalledRuns) {
    const isTimedOut = run.timeout_at && run.timeout_at <= new Date().toISOString();
    const stall = isTimedOut
      ? `[orchard][timeout] run exceeded timeout_at=${run.timeout_at}`
      : `[orchard][stall] no activity since ${run.last_activity_at ?? 'unknown'} (idleMs=${idleMs})`;
    const retryCount = Number(run.retry_count ?? 0) + 1;
    const nextAttemptAt = retryCount <= retryLimit
      ? new Date(Date.now() + Math.min(baseCooldownMs * Math.pow(2, retryCount - 1), 30 * 60 * 1000)).toISOString()
      : null;
    await finalizeTaskRun({
      db,
      runtime,
      cfg,
      logger,
      taskId: run.task_id,
      runId: run.id,
      projectId: run.project_id,
      runStatus: 'failed',
      taskStatus: retryCount <= retryLimit ? 'ready' : 'failed',
      output: stall,
      retryCount,
      nextAttemptAt,
      stallReason: stall,
      cleanupStatus: 'stalled',
      blockerReason: stall,
      cleanupDescendants: retryCount > retryLimit,
    });
    logger.warn(`[orchard] stalled run detected task=${run.task_id} run=${run.id} session=${run.session_key}`);
  }
  return stalledRuns.length;
}

function extractLastAssistantMessage(messages: unknown[]): string {
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i] as any;
    if (msg?.role === "assistant") {
      if (typeof msg.content === "string") return msg.content;
      if (Array.isArray(msg.content)) {
        return msg.content
          .filter((c: any) => c?.type === "text")
          .map((c: any) => c.text ?? "")
          .join("\n");
      }
    }
  }
  return "";
}

/**
 * Called on service startup. Finds any task_runs still marked 'running' from
 * a previous process, deletes their sessions, and marks them for retry.
 * This prevents runaway sessions after restarts.
 */
export async function seedRunningTasksFromDb(
  db: Database.Database,
  runtime: any,
  cfg: OrchardConfig,
  logger: any
): Promise<void> {
  const stuckRuns = db.prepare(`
    SELECT tr.id, tr.task_id, tr.session_key, t.project_id, t.retry_count
    FROM task_runs tr
    JOIN tasks t ON t.id = tr.task_id
    WHERE tr.status = 'running'
  `).all() as any[];

  if (stuckRuns.length === 0) return;

  logger.warn(`[orchard] startup: found ${stuckRuns.length} stuck running session(s); cleaning up`);

  const retryLimit = cfg.roles?.executor?.retryLimit ?? 3;
  const baseCooldownMs = cfg.limits?.cooldownOnFailureMs ?? 60000;

  for (const run of stuckRuns) {
    if (run.session_key) {
      logger.info(`[orchard] startup: cleaning stale session ${run.session_key}`);
    }

    const retryCount = Number(run.retry_count ?? 0) + 1;
    const nextAttemptAt = retryCount <= retryLimit
      ? new Date(Date.now() + Math.min(baseCooldownMs * Math.pow(2, retryCount - 1), 30 * 60 * 1000)).toISOString()
      : null;
    await finalizeTaskRun({
      db,
      runtime,
      cfg,
      logger,
      taskId: run.task_id,
      runId: run.id,
      projectId: run.project_id,
      runStatus: 'failed',
      taskStatus: retryCount <= retryLimit ? 'ready' : 'failed',
      output: '[orchard] process restart; session abandoned',
      retryCount,
      nextAttemptAt,
      timeoutReason: '[orchard] process restart; session abandoned',
      cleanupStatus: 'startup_reaped',
      blockerReason: '[orchard] process restart; session abandoned',
      cleanupDescendants: retryCount > retryLimit,
    });
  }

  logger.warn(`[orchard] startup: cleaned up ${stuckRuns.length} stuck session(s)`);

  // Orphan sweep: tasks stuck in running/assigned with no active run (e.g. process crashed
  // between run INSERT and finalizeTaskRun task-status update).
  const orphanedTasks = db.prepare(`
    SELECT t.id, t.retry_count, t.project_id
    FROM tasks t
    WHERE t.status IN ('running', 'assigned')
      AND NOT EXISTS (
        SELECT 1 FROM task_runs tr WHERE tr.task_id = t.id AND tr.status = 'running'
      )
  `).all() as any[];

  if (orphanedTasks.length > 0) {
    logger.warn(`[orchard] startup: found ${orphanedTasks.length} orphaned task(s) with no active run; resetting to ready`);
    for (const t of orphanedTasks) {
      db.prepare(`UPDATE tasks SET status = 'ready', updated_at = CURRENT_TIMESTAMP, next_attempt_at = NULL WHERE id = ?`).run(t.id);
      logger.warn(`[orchard] startup: reset orphaned task=${t.id} project=${t.project_id}`);
    }
  }
}

export async function runQueueTick(
  db: Database.Database,
  cfg: OrchardConfig,
  runtime: any,
  logger: any,
  targetProjectId?: string
): Promise<void> {
  if (tickInFlight) {
    tickRerunRequested = true;
    logger.warn(`[orchard] queue tick already in flight; rerun requested`);
    return;
  }

  tickInFlight = true;
  updateRuntimeState(db, (state) => {
    state.queue ||= {};
    state.queue.lastTickStartedAt = new Date().toISOString();
    state.queue.lastTickTargetProjectId = targetProjectId ?? null;
    state.queue.lastTickSkippedReason = null;
  });
  lastTickSummary = {
    startedAt: new Date().toISOString(),
    finishedAt: null,
    projectsScanned: 0,
    readyTasksSeen: 0,
    dispatched: 0,
    skipped: [],
    projectDetails: [],
  };

  const maxConcurrent = getMaxConcurrent(cfg);
  const maxPerHour = cfg.limits?.maxTasksPerHour ?? 10;
  const limitsEnabled = cfg.limits?.enabled !== false;
  const overdueRunsCleaned = await enforceOverdueRuns(db, runtime, cfg, logger);
  const stalledRunsCleaned = await enforceStalledRuns(db, runtime, cfg, logger);

  // Orphan sweep: reset tasks stuck in running/assigned with no active run.
  const orphanedTasks = db.prepare(`
    SELECT id FROM tasks
    WHERE status IN ('running', 'assigned')
      AND NOT EXISTS (SELECT 1 FROM task_runs tr WHERE tr.task_id = tasks.id AND tr.status = 'running')
  `).all() as any[];
  for (const t of orphanedTasks) {
    db.prepare(`UPDATE tasks SET status = 'ready', updated_at = CURRENT_TIMESTAMP, next_attempt_at = NULL WHERE id = ?`).run(t.id);
    logger.warn(`[orchard] orphan sweep: reset task=${t.id} to ready (no active run found)`);
  }

  if (isDebugEnabled(cfg) && isVerboseDebug(cfg)) {
    logger.info(`[orchard][debug] queue tick start: running=${runningTasks.size}, maxConcurrent=${maxConcurrent}, maxPerHour=${maxPerHour}, logOnly=${isLogOnlyMode(cfg)}`);
  }

  const breakerEnabled = cfg.debug?.circuitBreaker?.enabled !== false;
  const breakerThreshold = cfg.debug?.circuitBreaker?.failureThreshold ?? 3;
  const breakerCooldownMs = cfg.debug?.circuitBreaker?.cooldownMs ?? 5 * 60 * 1000;
  const globalCircuit = breakerEnabled ? isCircuitOpen(db, "global") : { open: false, state: null };

  if (isQueuePaused(db)) {
    const reason = `[orchard] queue paused by operator`;
    logger.warn(reason);
    updateRuntimeState(db, (state) => {
      state.queue ||= {};
      state.queue.lastTickFinishedAt = new Date().toISOString();
      state.queue.lastTickSkippedReason = reason;
    });
    (lastTickSummary.skipped as any[]).push(reason);
    lastTickSummary.finishedAt = new Date().toISOString();
    tickInFlight = false;
    return;
  }

  if (globalCircuit.open) {
    const reason = `[orchard] global circuit open until ${globalCircuit.state?.open_until ?? "unknown"}`;
    logger.warn(reason);
    updateRuntimeState(db, (state) => {
      state.queue ||= {};
      state.queue.lastTickFinishedAt = new Date().toISOString();
      state.queue.lastTickSkippedReason = reason;
    });
    (lastTickSummary.skipped as any[]).push(reason);
    lastTickSummary.finishedAt = new Date().toISOString();
    tickInFlight = false;
    return;
  }

  if (limitsEnabled && runningTasks.size >= maxConcurrent) {
    logger.debug(`[orchard] at concurrency cap (${runningTasks.size}/${maxConcurrent}), skipping tick`);
    updateRuntimeState(db, (state) => {
      state.queue ||= {};
      state.queue.lastTickFinishedAt = new Date().toISOString();
      state.queue.lastTickSkippedReason = `concurrency-cap:${runningTasks.size}/${maxConcurrent}`;
    });
    (lastTickSummary.skipped as any[]).push(`concurrency-cap:${runningTasks.size}/${maxConcurrent}`);
    lastTickSummary.finishedAt = new Date().toISOString();
    tickInFlight = false;
    return;
  }
  if (limitsEnabled && getTasksDispatchedLastHour() >= maxPerHour) {
    logger.warn(`[orchard] hourly dispatch cap reached (${maxPerHour}), skipping tick`);
    updateRuntimeState(db, (state) => {
      state.queue ||= {};
      state.queue.lastTickFinishedAt = new Date().toISOString();
      state.queue.lastTickSkippedReason = `hourly-cap:${maxPerHour}`;
    });
    (lastTickSummary.skipped as any[]).push(`hourly-cap:${maxPerHour}`);
    lastTickSummary.finishedAt = new Date().toISOString();
    tickInFlight = false;
    return;
  }

  const projects = targetProjectId
    ? (db.prepare(`SELECT * FROM projects WHERE status = 'active' AND id = ?`).all(targetProjectId) as any[])
    : (db.prepare(`SELECT * FROM projects WHERE status = 'active'`).all() as any[]);
  lastTickSummary.projectsScanned = projects.length;
  (lastTickSummary as any).limits = {
    enabled: limitsEnabled,
    maxConcurrent,
    maxPerHour,
    dispatchedLastHour: getTasksDispatchedLastHour(),
  };
  (lastTickSummary as any).overdueRunsCleaned = overdueRunsCleaned;
  (lastTickSummary as any).stalledRunsCleaned = stalledRunsCleaned;

  for (const project of projects) {
    const maxPerProject = cfg.limits?.maxSubagentsPerProject ?? 3;
    const runningForProject = countRunningForProject(project.id);
    const projectDetail: Record<string, unknown> = {
      id: project.id,
      name: project.name,
      runningForProject,
      maxPerProject,
      activeTaskCount: 0,
      coolingDownCount: 0,
      readyTasks: 0,
      skippedReason: null,
    };

    if (limitsEnabled && runningForProject >= maxPerProject) {
      logger.debug(`[orchard] project ${project.id} at per-project cap`);
      projectDetail.skippedReason = `project-cap:${runningForProject}/${maxPerProject}`;
      updateProjectRuntimeState(db, project.id, {
        lastQueueTickAt: new Date().toISOString(),
        lastQueueSkipReason: projectDetail.skippedReason as string,
      });
      (lastTickSummary.projectDetails as any[]).push(projectDetail);
      (lastTickSummary.skipped as any[]).push(`project-cap:${project.id}:${runningForProject}/${maxPerProject}`);
      continue;
    }

    const priorityOrder = `CASE priority WHEN 'critical' THEN 0 WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 ELSE 4 END`;
    const readyTasks = db.prepare(
      `SELECT * FROM tasks WHERE project_id = ? AND status = 'ready' AND (next_attempt_at IS NULL OR next_attempt_at <= CURRENT_TIMESTAMP) ORDER BY ${priorityOrder}, created_at ASC`
    ).all(project.id) as any[];
    const activeTaskCount = (db.prepare(
      `SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status IN ('ready','assigned','running','blocked')`
    ).get(project.id) as any).n;
    const coolingDownCount = (db.prepare(
      `SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status = 'ready' AND next_attempt_at IS NOT NULL AND next_attempt_at > CURRENT_TIMESTAMP`
    ).get(project.id) as any).n;
    projectDetail.activeTaskCount = Number(activeTaskCount || 0);
    projectDetail.coolingDownCount = Number(coolingDownCount || 0);
    projectDetail.readyTasks = readyTasks.length;

    lastTickSummary.readyTasksSeen = Number(lastTickSummary.readyTasksSeen || 0) + readyTasks.length;
    (lastTickSummary as any).skippedReadyDueToCooldown = Number((lastTickSummary as any).skippedReadyDueToCooldown || 0) + Number(coolingDownCount || 0);

    if (readyTasks.length === 0) {
      projectDetail.skippedReason = coolingDownCount > 0 ? 'cooldown-wait' : 'no-ready-tasks';
      updateProjectRuntimeState(db, project.id, {
        lastQueueTickAt: new Date().toISOString(),
        lastQueueSkipReason: projectDetail.skippedReason as string,
      });
      (lastTickSummary.projectDetails as any[]).push(projectDetail);
      await handleEmptyQueue(db, project, cfg, runtime, logger);
      continue;
    }

    const capacityAvailable = Math.min(
      maxConcurrent - runningTasks.size,
      maxPerProject - runningForProject,
      readyTasks.length
    );
    const slotsAvailable = limitsEnabled
      ? availableSpreadSlots(cfg, capacityAvailable)
      : capacityAvailable;
    const nextSlotMs = slotsAvailable === 0 && capacityAvailable > 0
      ? getNextSlotAvailableMs(cfg)
      : null;

    projectDetail.skippedReason = slotsAvailable > 0 ? null : (capacityAvailable === 0 ? 'no-available-slots' : 'spread-delay');
    if (nextSlotMs != null) (projectDetail as any).nextSlotAvailableMs = nextSlotMs;
    updateProjectRuntimeState(db, project.id, {
      lastQueueTickAt: new Date().toISOString(),
      lastQueueSkipReason: (projectDetail.skippedReason as string | null) ?? null,
    });
    (lastTickSummary.projectDetails as any[]).push(projectDetail);

    for (let i = 0; i < slotsAvailable; i++) {
      if (limitsEnabled && getTasksDispatchedLastHour() >= maxPerHour) break;
      recordSlotDispatch(cfg);
      lastTickSummary.dispatched = Number(lastTickSummary.dispatched || 0) + 1;
      void dispatchExecutor(db, readyTasks[i], project, cfg, runtime, logger).catch((err: any) => {
        const msg = err?.message ?? String(err);
        logger.error(`[orchard] async dispatch error for task ${readyTasks[i]?.id}: ${msg}`);
        if (breakerEnabled) {
          const state = recordCircuitFailure(db, "global", msg, breakerThreshold, breakerCooldownMs);
          logger.warn(`[orchard] global circuit failure count=${state.failure_count} open_until=${state.open_until ?? 'closed'}`);
        }
      });
    }
  }

  lastTickSummary.finishedAt = new Date().toISOString();
  updateRuntimeState(db, (state) => {
    state.queue ||= {};
    state.queue.lastTickFinishedAt = new Date().toISOString();
    state.queue.lastTickSkippedReason = null;
  });

  tickInFlight = false;
  if (tickRerunRequested) {
    tickRerunRequested = false;
    logger.info(`[orchard] running queued follow-up tick`);
    return runQueueTick(db, cfg, runtime, logger, targetProjectId);
  }
}

async function dispatchExecutor(
  db: Database.Database,
  task: any,
  project: any,
  cfg: OrchardConfig,
  runtime: any,
  logger: any
): Promise<void> {
  const breakerEnabled = cfg.debug?.circuitBreaker?.enabled !== false;
  const breakerThreshold = cfg.debug?.circuitBreaker?.failureThreshold ?? 3;
  const breakerCooldownMs = cfg.debug?.circuitBreaker?.cooldownMs ?? 5 * 60 * 1000;
  const projectCircuitScope = `project:${project.id}`;
  const projectCircuit = breakerEnabled ? isCircuitOpen(db, projectCircuitScope) : { open: false, state: null };
  if (projectCircuit.open) {
    logger.warn(`[orchard] skipping task ${task.id}; project circuit open until ${projectCircuit.state?.open_until ?? 'unknown'}`);
    db.prepare(`UPDATE tasks SET status = 'ready', updated_at = CURRENT_TIMESTAMP WHERE id = ?`).run(task.id);
    return;
  }
  const model = task.model_override || getExecutorModel(cfg) || undefined;
  const timeoutSeconds = cfg.roles?.executor?.timeoutSeconds ?? 600;
  const ownerToken = `task-${task.id}-run-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;

  if (isLogOnlyMode(cfg)) {
    logger.info(`[orchard][debug] would dispatch executor for task ${task.id}: ${task.title}`);
  } else {
    logger.info(`[orchard] dispatching executor for task ${task.id}: ${task.title}`);
  }
  if (isDebugEnabled(cfg)) {
    logger.info(`[orchard][debug] executor dispatch config: model=${model ?? "default"}, timeoutSeconds=${timeoutSeconds}, logOnly=${isLogOnlyMode(cfg)}, spawnExecutors=${shouldSpawnExecutors(cfg)}`);
  }

  const inputObj = {
    task_id: task.id,
    title: task.title,
    description: task.description,
    acceptance_criteria: task.acceptance_criteria,
    project_goal: project.goal,
  };

  if (isLogOnlyMode(cfg)) {
    logger.warn(`[orchard][observe] task ${task.id} left unchanged; no claim/run/status mutation in observe-only mode`);
    dispatchTimes.push(Date.now());
    return;
  }

  const initialRunStatus = shouldSpawnExecutors(cfg) ? 'running' : 'done';
  const timeoutAt = new Date(Date.now() + timeoutSeconds * 1000).toISOString();
  const claimAndCreateRun = db.transaction(() => {
    const claim = db.prepare(`UPDATE tasks SET status = 'assigned', updated_at = CURRENT_TIMESTAMP WHERE id = ? AND status = 'ready'`).run(task.id);
    if ((claim.changes ?? 0) !== 1) return null;
    const runResult = db.prepare(`
      INSERT INTO task_runs (task_id, role, model, status, owner_token, timeout_at, input, started_at)
      VALUES (?, 'executor', ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    `).run(task.id, model, initialRunStatus, ownerToken, timeoutAt, JSON.stringify(inputObj));
    const runId = runResult.lastInsertRowid as number;
    db.prepare(`UPDATE tasks SET status = 'running', updated_at = CURRENT_TIMESTAMP WHERE id = ?`).run(task.id);
    return runId;
  });
  const runId = claimAndCreateRun();
  if (!runId) {
    logger.warn(`[orchard] task ${task.id} was not claimable; skipping dispatch`);
    return;
  }

  runningTasks.set(task.id, { taskId: task.id, projectId: project.id, startedAt: Date.now() });
  dispatchTimes.push(Date.now());

  // KB context injection
  let kbContext = "";
  try {
    const hits = await searchKnowledge(db, cfg, project.id, `${task.title} ${task.description ?? ""}`);
    if (hits.length > 0) {
      kbContext = "[Relevant context from past work on this project]\n" +
        hits.map((h) => h.content).join("\n---\n") +
        "\n[/Relevant context]\n\n";
    }
  } catch (kbErr: any) {
    logger.warn(`[orchard] KB search failed (non-fatal): ${kbErr?.message}`);
  }

  const prompt = kbContext + buildExecutorPrompt(task, project, ownerToken, runId);

  try {
    let output = "";
    let success = false;

    if (!shouldSpawnExecutors(cfg)) {
      output = `[orchard][safety] executor spawn disabled for task ${task.id}; task logged only`;
      success = true;
      logger.warn(output);
    } else {
      const sessionKey = `orchard-exec-${task.id}-${runId}`;
      try {
        logger.info(`[orchard] spawning executor session ${sessionKey} for task ${task.id}`);
        const { runId: subagentRunId } = await (runtime as any).subagent.run({
          sessionKey,
          message: prompt,
          model,
          lane: "orchard",
          idempotencyKey: ownerToken,
        });
        db.prepare(`UPDATE task_runs SET session_key = ?, subagent_run_id = ? WHERE id = ?`)
          .run(sessionKey, subagentRunId, runId);

        // Poll in 30s chunks so we can write interim output to the DB
        // while the session is still running (for live UI display).
        const pollIntervalMs = 15_000;
        const deadline = Date.now() + timeoutSeconds * 1000;
        let waitResult: any = null;
        while (Date.now() < deadline) {
          const remaining = deadline - Date.now();
          const chunk = Math.min(pollIntervalMs, remaining);
          waitResult = await (runtime as any).subagent.waitForRun({
            runId: subagentRunId,
            timeoutMs: chunk,
          });
          if (waitResult.status !== "timeout") break;
          // Still running — grab latest messages for live display
          try {
            const { messages: interimMsgs } = await (runtime as any).subagent.getSessionMessages({ sessionKey, limit: 5 });
            const interim = extractLastAssistantMessage(interimMsgs as unknown[]);
            if (interim) {
              db.prepare(`UPDATE task_runs SET output = ? WHERE id = ?`).run(interim, runId);
              touchRunActivity(db, runId);
            }
          } catch { /* non-fatal */ }
        }
        // If we exhausted the deadline without a terminal status, treat as timeout
        if (!waitResult || waitResult.status === "timeout") {
          waitResult = { status: "timeout" };
        }

        if (waitResult.status === "ok") {
          const { messages } = await (runtime as any).subagent.getSessionMessages({ sessionKey, limit: 20 });
          output = extractLastAssistantMessage(messages as unknown[]) || `[orchard] executor completed (no output)`;
          success = true;
        } else {
          output = waitResult.status === "timeout"
            ? `[orchard] executor session timed out after ${timeoutSeconds}s`
            : `[orchard] executor session failed: ${waitResult.error ?? "unknown"}`;
          success = false;
        }

      } catch (spawnErr: any) {
        output = `[orchard] executor spawn error: ${spawnErr?.message ?? String(spawnErr)}`;
        success = false;
      }
    }

    // QA role
    let finalStatus: "done" | "ready" | "failed" = success ? "done" : "failed";
    if (success && cfg.roles?.qa?.enabled) {
      finalStatus = await runQaReview(db, task, project, output, runId, cfg, runtime, logger);
    }

    if (!success) {
      if (breakerEnabled) {
        const globalState = recordCircuitFailure(db, "global", output, breakerThreshold, breakerCooldownMs);
        const projectState = recordCircuitFailure(db, projectCircuitScope, output, breakerThreshold, breakerCooldownMs);
        logger.warn(`[orchard] circuit failure recorded task=${task.id} global=${globalState.failure_count} project=${projectState.failure_count}`);
      }

      // Exponential backoff retry logic
      const retryLimit = cfg.roles?.executor?.retryLimit ?? 3;
      const retryCount = (task.retry_count ?? 0) + 1;
      const baseCooldownMs = cfg.limits?.cooldownOnFailureMs ?? 60000;
      const backoffMs = Math.min(baseCooldownMs * Math.pow(2, retryCount - 1), 30 * 60 * 1000); // cap at 30min

      if (retryCount <= retryLimit) {
        const nextAttemptAt = new Date(Date.now() + backoffMs).toISOString();
        logger.warn(`[orchard] task ${task.id} failed (attempt ${retryCount}/${retryLimit}), requeueing for ${nextAttemptAt}`);
        await finalizeTaskRun({
          db,
          runtime,
          cfg,
          logger,
          taskId: task.id,
          runId,
          projectId: project.id,
          runStatus: 'failed',
          taskStatus: 'ready',
          output,
          retryCount,
          nextAttemptAt,
          cleanupStatus: 'retry_scheduled',
          blockerReason: output,
          cleanupDescendants: false,
        });
      } else {
        logger.warn(`[orchard] task ${task.id} failed after ${retryLimit} retries, marking failed`);
        await finalizeTaskRun({
          db,
          runtime,
          cfg,
          logger,
          taskId: task.id,
          runId,
          projectId: project.id,
          runStatus: 'failed',
          taskStatus: 'failed',
          output,
          retryCount,
          nextAttemptAt: null,
          cleanupStatus: 'failed',
          blockerReason: output,
          cleanupDescendants: true,
        });
      }
    } else {
      if (breakerEnabled) {
        recordCircuitSuccess(db, "global");
        recordCircuitSuccess(db, projectCircuitScope);
      }
      await finalizeTaskRun({
        db,
        runtime,
        cfg,
        logger,
        taskId: task.id,
        runId,
        projectId: project.id,
        runStatus: 'done',
        taskStatus: finalStatus === 'ready' ? 'ready' : finalStatus,
        output,
        nextAttemptAt: null,
        blockerReason: null,
        cleanupStatus: finalStatus === 'ready' ? 'qa_retry' : 'completed',
        cleanupDescendants: false,
      });

      // Auto-extract to KB on success
      if (finalStatus === "done" && cfg.contextInjection?.autoExtract !== false && output) {
        addKnowledge(db, cfg, project.id, output, "executor_output", task.id).catch(() => {});
      }
    }
  } finally {
    runningTasks.delete(task.id);
  }
}

async function runQaReview(
  db: Database.Database,
  task: any,
  _project: any,
  executorOutput: string,
  executorRunId: number,
  cfg: OrchardConfig,
  runtime: any,
  logger: any
): Promise<"done" | "ready" | "failed"> {
  const qaCfg = cfg.roles!.qa!;
  const model = qaCfg.model ?? "openai/gpt-4o";
  const retryLimit = cfg.roles?.executor?.retryLimit ?? 2;

  if (isLogOnlyMode(cfg)) {
    logger.warn(`[orchard][observe] QA skipped for task ${task.id}; no QA run recorded in observe-only mode`);
    return "ready";
  }

  logger.info(`[orchard] running QA for task ${task.id}`);

  const qaPrompt = `You are a QA reviewer for OrchardOS.

Task: ${task.title}
Description: ${task.description ?? "(none)"}
Acceptance Criteria: ${task.acceptance_criteria ?? "(none)"}

Executor Output:
${executorOutput}

Review the output against the acceptance criteria. Respond with ONLY valid JSON:
{ "verdict": "approved" | "rejected" | "retry", "notes": "brief explanation" }`;

  let verdict = "approved";
  let notes = "Auto-approved (QA spawns disabled)";

  if (shouldSpawnQa(cfg)) {
    const sessionKey = `orchard-qa-${task.id}-${Date.now()}`;
    appendChildSessionKey(db, executorRunId, sessionKey);
    try {
      const { runId: subagentRunId } = await (runtime as any).subagent.run({
        sessionKey,
        message: qaPrompt,
        model,
        lane: "orchard",
        idempotencyKey: `qa-${task.id}-${Date.now()}`,
      });
      const waitResult = await (runtime as any).subagent.waitForRun({ runId: subagentRunId, timeoutMs: 3 * 60 * 1000 });
      if (waitResult.status === "ok") {
        const { messages } = await (runtime as any).subagent.getSessionMessages({ sessionKey, limit: 5 });
        const raw = extractLastAssistantMessage(messages as unknown[]);
        try {
          const parsed = JSON.parse(raw.match(/\{[\s\S]*\}/)?.[0] ?? "");
          verdict = parsed.verdict ?? "approved";
          notes = parsed.notes ?? "";
        } catch {
          verdict = "approved";
          notes = `[orchard] QA response parse failed; auto-approving`;
        }
      } else {
        verdict = "approved";
        notes = `[orchard] QA session ${waitResult.status}; auto-approving`;
      }
      // sessions.delete not available to plugins (requires operator.admin). Store GC handles cleanup.
    } catch (e: any) {
      verdict = "approved";
      notes = `[orchard] QA spawn error: ${e?.message ?? String(e)}; auto-approving`;
    }
  }

  // Record QA run
  db.prepare(`
    INSERT INTO task_runs (task_id, role, model, status, input, output, qa_verdict, qa_notes, started_at, ended_at)
    VALUES (?, 'qa', ?, 'done', ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
  `).run(task.id, model, qaPrompt, executorOutput, verdict, notes);

  if (verdict === "approved") {
    return "done";
  }

  // rejected or retry
  const retryCount = (task.retry_count ?? 0) + 1;
  db.prepare(`UPDATE tasks SET retry_count = ? WHERE id = ?`).run(retryCount, task.id);

  if (retryCount <= retryLimit) {
    logger.info(`[orchard] QA ${verdict} task ${task.id}, requeueing (retry ${retryCount}/${retryLimit})`);
    return "ready"; // re-queue
  }

  logger.warn(`[orchard] QA rejected task ${task.id} after ${retryCount} retries, marking failed`);
  return "failed";
}

async function handleEmptyQueue(
  db: Database.Database,
  project: any,
  cfg: OrchardConfig,
  runtime: any,
  logger: any
): Promise<void> {
  const architectCfg = cfg.roles?.architect;
  if (!architectCfg?.enabled || !architectCfg?.wakeOnEmptyQueue) return;
  if (project.completion_score >= 1.0) return;

  const activeTaskCount = (db.prepare(
    `SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status IN ('ready','assigned','running','blocked')`
  ).get(project.id) as any).n;
  if (Number(activeTaskCount || 0) > 0) {
    logger.info(`[orchard][debug] architect empty-queue check skipped for project ${project.id}; activeTaskCount=${activeTaskCount}`);
    return;
  }

  if (isLogOnlyMode(cfg)) {
    logger.warn(`[orchard][observe] project ${project.id} queue empty; architect evaluation skipped in observe-only mode`);
    return;
  }

  logger.info(`[orchard] project ${project.id} queue empty, waking architect`);
  await wakeArchitectForProject(project, db, cfg, runtime, logger);
}

function buildExecutorPrompt(task: any, project: any, ownerToken: string, runId: number): string {
  return `You are an executor agent for OrchardOS.

Project: ${project.name}
Project Goal: ${project.goal}

Task #${task.id}: ${task.title}
${task.description ? `\nDescription:\n${task.description}` : ""}
${task.acceptance_criteria ? `\nAcceptance Criteria:\n${task.acceptance_criteria}` : ""}

Complete this task. When finished, end your response with a clear summary of exactly what was done.
If you cannot proceed due to a blocker, end your response with "BLOCKED: <reason>".

Run identity for any orchard_task_done/orchard_task_block call:
- owner_token: ${ownerToken}
- session_key: orchard-exec-${task.id}-${runId}`;
}
