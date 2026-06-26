import { Type } from "@sinclair/typebox";
import type Database from "better-sqlite3";
import { finalizeTaskRun, getWakeCallback, runQueueTick } from "../queue/runner.js";

type ToolResult = { content: Array<{ type: "text"; text: string }> };

function ok(data: unknown): ToolResult { return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] }; }
function err(msg: string): ToolResult { return { content: [{ type: "text", text: `Error: ${msg}` }] }; }

function getOwnedActiveRun(db: Database.Database, taskId: number, ownerToken?: string, sessionKey?: string): any {
  const activeRun = db.prepare(
    `SELECT * FROM task_runs WHERE task_id = ? AND status = 'running' ORDER BY id DESC LIMIT 1`
  ).get(taskId) as any;
  if (!activeRun) return null;

  if (!ownerToken && !sessionKey) {
    return { error: "owner_token or session_key is required to finalize an active task run" };
  }

  if (ownerToken && activeRun.owner_token === ownerToken) return activeRun;
  if (sessionKey && activeRun.session_key === sessionKey) return activeRun;

  return { error: `active run ownership mismatch for task ${taskId}` };
}

export function registerTaskTools(
  api: any,
  getDb: () => Database.Database,
  getCfg?: () => any
): void {
  api.registerTool({
    name: "orchard_task_add",
    description: "Add a task to an OrchardOS project",
    parameters: Type.Object({
      project_id: Type.String({ description: "Project ID" }),
      title: Type.String({ description: "Task title" }),
      description: Type.Optional(Type.String({ description: "Detailed task description" })),
      acceptance_criteria: Type.Optional(Type.String({ description: "Criteria for task completion" })),
      priority: Type.Optional(
        Type.Union([
          Type.Literal("critical"),
          Type.Literal("high"),
          Type.Literal("medium"),
          Type.Literal("low"),
        ], { description: "Task priority" })
      ),
      model_override: Type.Optional(Type.String({ description: "Override the executor model for this task" })),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const project = db.prepare(`SELECT id FROM projects WHERE id = ?`).get(params.project_id);
      if (!project) return err(`Project ${params.project_id} not found`);

      const result = db.prepare(`
        INSERT INTO tasks (project_id, title, description, acceptance_criteria, priority, model_override, status)
        VALUES (?, ?, ?, ?, ?, ?, 'ready')
      `).run(
        params.project_id,
        params.title,
        params.description ?? null,
        params.acceptance_criteria ?? null,
        params.priority ?? "medium",
        params.model_override ?? null,
      );
      return ok({ id: result.lastInsertRowid, title: params.title, status: "ready" });
    },
  });

  api.registerTool({
    name: "orchard_task_list",
    description: "List tasks, optionally filtered by project and/or status",
    parameters: Type.Object({
      project_id: Type.Optional(Type.String({ description: "Filter by project ID" })),
      status: Type.Optional(Type.String({ description: "Filter by status (e.g. ready, running, done)" })),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      let query = `SELECT * FROM tasks WHERE 1=1`;
      const args: any[] = [];
      if (params.project_id) {
        query += ` AND project_id = ?`;
        args.push(params.project_id);
      }
      if (params.status) {
        query += ` AND status = ?`;
        args.push(params.status);
      }
      query += ` ORDER BY created_at DESC`;
      const rows = db.prepare(query).all(...args);
      return ok(rows);
    },
  });

  api.registerTool({
    name: "orchard_task_done",
    description: "Mark a task as done with a completion summary",
    parameters: Type.Object({
      task_id: Type.Number({ description: "Task ID" }),
      summary: Type.String({ description: "Summary of what was done" }),
      owner_token: Type.Optional(Type.String({ description: "Owner token for the active executor run" })),
      session_key: Type.Optional(Type.String({ description: "Session key for the active executor run" })),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const task = db.prepare(`SELECT * FROM tasks WHERE id = ?`).get(params.task_id) as any;
      if (!task) return err(`Task ${params.task_id} not found`);
      const activeRun = getOwnedActiveRun(db, params.task_id, params.owner_token, params.session_key);
      if (activeRun?.error) return err(activeRun.error);
      if (!activeRun && task.status !== 'running' && task.status !== 'assigned') return err(`Task ${params.task_id} is not actively running`);

      db.prepare(`INSERT INTO task_comments (task_id, author, content) VALUES (?, 'executor', ?)`).run(
        params.task_id,
        `Completed: ${params.summary}`
      );
      await finalizeTaskRun({
        db,
        runtime: api.runtime,
        cfg: getCfg ? getCfg() : {},
        logger: api.logger,
        taskId: params.task_id,
        runId: activeRun.id,
        runStatus: 'done',
        taskStatus: 'done',
        output: params.summary,
        nextAttemptAt: null,
        blockerReason: null,
        cleanupStatus: 'completed',
        cleanupDescendants: false,
      });

      return ok({ task_id: params.task_id, status: "done", run_id: activeRun.id });
    },
  });

  api.registerTool({
    name: "orchard_task_block",
    description: "Mark a task as blocked with a reason",
    parameters: Type.Object({
      task_id: Type.Number({ description: "Task ID" }),
      reason: Type.String({ description: "Reason the task is blocked" }),
      owner_token: Type.Optional(Type.String({ description: "Owner token for the active executor run" })),
      session_key: Type.Optional(Type.String({ description: "Session key for the active executor run" })),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const task = db.prepare(`SELECT * FROM tasks WHERE id = ?`).get(params.task_id) as any;
      if (!task) return err(`Task ${params.task_id} not found`);
      const activeRun = getOwnedActiveRun(db, params.task_id, params.owner_token, params.session_key);
      if (activeRun?.error) return err(activeRun.error);
      if (!activeRun && task.status !== 'running' && task.status !== 'assigned') return err(`Task ${params.task_id} is not actively running`);

      db.prepare(`INSERT INTO task_blockers (task_id, reason) VALUES (?, ?)`).run(params.task_id, params.reason);
      await finalizeTaskRun({
        db,
        runtime: api.runtime,
        cfg: getCfg ? getCfg() : {},
        logger: api.logger,
        taskId: params.task_id,
        runId: activeRun.id,
        runStatus: 'failed',
        taskStatus: 'blocked',
        output: `[orchard] blocked: ${params.reason}`,
        nextAttemptAt: null,
        blockerReason: params.reason,
        cleanupStatus: 'blocked',
        cleanupDescendants: true,
      });

      return ok({ task_id: params.task_id, status: "blocked", reason: params.reason, run_id: activeRun.id });
    },
  });

  api.registerTool({
    name: "orchard_task_comment",
    description: "Add a comment to a task",
    parameters: Type.Object({
      task_id: Type.Number({ description: "Task ID" }),
      content: Type.String({ description: "Comment content" }),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const task = db.prepare(`SELECT id FROM tasks WHERE id = ?`).get(params.task_id);
      if (!task) return err(`Task ${params.task_id} not found`);

      const result = db.prepare(`INSERT INTO task_comments (task_id, content) VALUES (?, ?)`).run(
        params.task_id,
        params.content
      );
      return ok({ id: result.lastInsertRowid, task_id: params.task_id, content: params.content });
    },
  });

  api.registerTool({
    name: "orchard_wake",
    description: "Manually trigger the OrchardOS queue runner for all projects or a specific project",
    parameters: Type.Object({
      project_id: Type.Optional(Type.String({ description: "Project ID to target (or all if omitted)" })),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const cfg = getCfg ? getCfg() : {};
      if (params?.project_id) {
        const project = db.prepare(`SELECT id FROM projects WHERE id = ?`).get(params.project_id);
        if (!project) return err(`Project ${params.project_id} not found`);
        await runQueueTick(db, cfg, api.runtime, api.logger, params.project_id);
        return ok({ triggered: true, project_id: params.project_id, note: "Queue tick triggered for requested project" });
      }
      const cb = getWakeCallback();
      if (cb) {
        cb().catch(() => {});
        return ok({ triggered: true, message: "Queue runner triggered" });
      }
      return ok({ triggered: false, message: "Queue runner not yet initialized" });
    },
  });
}
