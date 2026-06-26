import type Database from "better-sqlite3";
import type { OrchardConfig } from "../config.js";
import { isLogOnlyMode, getArchitectModel, shouldSpawnArchitect } from "../config.js";
import { updateProjectRuntimeState } from "../queue/runtime-state.js";

const architectInFlight = new Set<string>();
const recentArchitectWakeAt = new Map<string, number>();

function parseDuration(s: string): number {
  const m = s.match(/^(\d+)(h|m|s)$/);
  if (!m) return 6 * 60 * 60 * 1000;
  const n = parseInt(m[1], 10);
  if (m[2] === "h") return n * 60 * 60 * 1000;
  if (m[2] === "m") return n * 60 * 1000;
  return n * 1000;
}

export async function wakeArchitectForProject(
  project: any,
  db: Database.Database,
  cfg: OrchardConfig,
  runtime: any,
  logger: any
): Promise<void> {
  // Count tasks by status
  const done = (db.prepare(`SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status = 'done'`).get(project.id) as any).n;
  const total = (db.prepare(`SELECT COUNT(*) as n FROM tasks WHERE project_id = ?`).get(project.id) as any).n;
  const ready = (db.prepare(`SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status = 'ready'`).get(project.id) as any).n;

  const completionTemp = project.completion_temperature ?? 0.7;
  const score = project.completion_score ?? 0;

  // Simple heuristic: if score >= (1 - completionTemp), don't generate more work
  if (score >= (1 - completionTemp) && score >= 0.9) {
    updateProjectRuntimeState(db, project.id, {
      lastArchitectDecisionAt: new Date().toISOString(),
      lastArchitectSkipReason: `completion-threshold:${score}`,
    });
    logger.info(`[orchard] architect skip — project ${project.id} completion score ${score} at threshold`);
    return;
  }

  if (architectInFlight.has(project.id)) {
    updateProjectRuntimeState(db, project.id, {
      lastArchitectDecisionAt: new Date().toISOString(),
      lastArchitectSkipReason: `already-in-flight`,
    });
    logger.info(`[orchard] architect scheduler skip — project ${project.id} already in flight`);
    return;
  }
  const recentWake = recentArchitectWakeAt.get(project.id) ?? 0;
  if (Date.now() - recentWake < 5 * 60 * 1000) {
    updateProjectRuntimeState(db, project.id, {
      lastArchitectDecisionAt: new Date().toISOString(),
      lastArchitectSkipReason: `recently-woke`,
    });
    logger.info(`[orchard] architect scheduler skip — project ${project.id} woke recently`);
    return;
  }

  recentArchitectWakeAt.set(project.id, Date.now());
  updateProjectRuntimeState(db, project.id, {
    lastArchitectDecisionAt: new Date().toISOString(),
    lastArchitectWakeAt: new Date().toISOString(),
    lastArchitectSkipReason: null,
  });
  logger.info(`[orchard][debug] architect scheduler evaluated project ${project.id}`);

  const message = `You are the architect for OrchardOS project "${project.name}".

Goal: ${project.goal}
Completion score: ${score}
Tasks: ${done} done, ${ready} ready, ${total} total

Review progress and add any new tasks needed to move the project closer to completion.
Use orchard_task_add to add tasks, orchard_task_list to review current work.
If the goal is fully achieved, call orchard_project_status to confirm.`;

  architectInFlight.add(project.id);

  try {
    if (!shouldSpawnArchitect(cfg)) {
      logger.warn(`[orchard][safety] architect spawn disabled; skipping project ${project.id}`);
      return;
    }

    const sessionKey = `orchard-arch-${project.id}`;
    logger.info(`[orchard] waking architect for project ${project.id} (session ${sessionKey})`);

    const { runId: subagentRunId } = await (runtime as any).subagent.run({
      sessionKey,
      message,
      model: getArchitectModel(cfg),
      lane: "orchard",
      idempotencyKey: `arch-${project.id}-${Date.now()}`,
    });

    const waitResult = await (runtime as any).subagent.waitForRun({
      runId: subagentRunId,
      timeoutMs: 10 * 60 * 1000,
    });

    if (waitResult.status === "ok") {
      logger.info(`[orchard] architect completed for project ${project.id}`);
      updateProjectRuntimeState(db, project.id, {
        lastArchitectDecisionAt: new Date().toISOString(),
        lastArchitectSkipReason: null,
      });
    } else {
      logger.warn(`[orchard] architect session ended with status ${waitResult.status} for project ${project.id}: ${waitResult.error ?? ""}`);
      updateProjectRuntimeState(db, project.id, {
        lastArchitectDecisionAt: new Date().toISOString(),
        lastArchitectSkipReason: `session:${waitResult.status}`,
      });
    }

    await (runtime as any).subagent.deleteSession({ sessionKey }).catch(() => {});
  } catch (err: any) {
    updateProjectRuntimeState(db, project.id, {
      lastArchitectDecisionAt: new Date().toISOString(),
      lastArchitectSkipReason: `error:${err?.message ?? "unknown"}`,
    });
    logger.error(`[orchard] architect periodic wake error: ${err?.message}`);
  } finally {
    architectInFlight.delete(project.id);
  }
}

export function scheduleArchitect(
  getDb: () => Database.Database,
  cfg: OrchardConfig,
  runtime: any,
  logger: any
): ReturnType<typeof setInterval> | null {
  const architectCfg = cfg.roles?.architect;
  if (!architectCfg?.enabled || !architectCfg?.wakeEvery) return null;
  if (isLogOnlyMode(cfg)) {
    logger.warn(`[orchard] architect scheduler disabled in log-only mode`);
    return null;
  }

  const interval = parseDuration(architectCfg.wakeEvery);
  logger.info(`[orchard] architect scheduled every ${architectCfg.wakeEvery} (${interval}ms)`);

  return setInterval(async () => {
    try {
      const db = getDb();
      const projects = db.prepare(`SELECT * FROM projects WHERE status = 'active'`).all() as any[];
      for (const project of projects) {
        await wakeArchitectForProject(project, db, cfg, runtime, logger);
      }
    } catch (err: any) {
      logger.error(`[orchard] architect scheduler error: ${err?.message}`);
    }
  }, interval);
}
