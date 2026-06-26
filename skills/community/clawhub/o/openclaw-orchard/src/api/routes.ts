import type Database from "better-sqlite3";
import crypto from "crypto";
import http from "http";
import https from "https";
import path from "path";
import type { IncomingMessage, ServerResponse } from "http";
import { addKnowledge, searchKnowledge } from "../kb/knowledge.js";
import { getAllSettings, getSetting, setSetting } from "../db/settings.js";
import type { OrchardConfig } from "../config.js";
import { getWakeCallback, getQueueDebugState, runQueueTick, reapStalledRunsManual } from "../queue/runner.js";
import { closeCircuit, openCircuit, isQueuePaused, setQueuePaused } from "../queue/control.js";
import { DASHBOARD_HTML } from "../ui/dashboard.generated.js";

// ── helpers ──────────────────────────────────────────────────────────────────

function jsonOk(res: ServerResponse, data: unknown, status = 200): void {
  const body = JSON.stringify(data);
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(body);
}

function jsonErr(res: ServerResponse, status: number, message: string): void {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: message }));
}

const MAX_BODY_BYTES = 512 * 1024; // 512 KB

function readBody(req: IncomingMessage): Promise<any> {
  return new Promise((resolve) => {
    const chunks: Buffer[] = [];
    let totalBytes = 0;
    req.on("data", (c: Buffer) => {
      totalBytes += c.length;
      if (totalBytes > MAX_BODY_BYTES) { req.destroy(); return resolve({}); }
      chunks.push(c);
    });
    req.on("end", () => {
      try { resolve(JSON.parse(Buffer.concat(chunks).toString())); } catch { resolve({}); }
    });
    req.on("error", () => resolve({}));
  });
}

/** Split URL path into parts, ignoring query string. e.g. /orchard/projects/foo → ["orchard","projects","foo"] */
function urlParts(req: IncomingMessage): string[] {
  return (req.url ?? "").split("?")[0].split("/").filter(Boolean);
}

/** Fetch a URL and return up to maxChars of text content. */
function isPrivateHost(hostname: string): boolean {
  // Block loopback, link-local, and RFC-1918 private ranges
  if (hostname === "localhost") return true;
  const v4 = hostname.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
  if (v4) {
    const [, a, b] = v4.map(Number);
    if (a === 127 || a === 10) return true;
    if (a === 172 && b >= 16 && b <= 31) return true;
    if (a === 192 && b === 168) return true;
    if (a === 169 && b === 254) return true; // link-local
    if (a === 0) return true;
  }
  if (hostname === "::1" || hostname.startsWith("fc") || hostname.startsWith("fd")) return true;
  return false;
}

function fetchUrl(url: string, maxChars = 2000, _redirectDepth = 0): Promise<string> {
  return new Promise((resolve, reject) => {
    if (_redirectDepth > 3) return reject(new Error("Too many redirects"));
    let parsed: URL;
    try { parsed = new URL(url); } catch { return reject(new Error("Invalid URL")); }
    if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
      return reject(new Error("Only http/https URLs are allowed"));
    }
    if (isPrivateHost(parsed.hostname)) {
      return reject(new Error("Requests to private/internal addresses are not allowed"));
    }
    const lib = url.startsWith("https") ? https : http;
    const req = lib.get(url, { timeout: 10000, headers: { "User-Agent": "OrchardOS/1.0" } }, (res) => {
      // Follow redirects up to depth limit
      if (res.statusCode && res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return fetchUrl(res.headers.location, maxChars, _redirectDepth + 1).then(resolve).catch(reject);
      }
      if (res.statusCode && res.statusCode >= 400) {
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode}`));
      }
      let data = "";
      res.setEncoding("utf-8");
      res.on("data", (chunk: string) => {
        data += chunk;
        if (data.length > maxChars * 3) { res.destroy(); resolve(data.slice(0, maxChars)); return; }
      });
      res.on("end", () => {
        // Strip HTML tags if looks like HTML
        let text = data;
        if (text.includes("<html") || text.includes("<!DOCTYPE")) {
          text = text.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
                     .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
                     .replace(/<[^>]+>/g, " ")
                     .replace(/\s{2,}/g, " ")
                     .trim();
        }
        resolve(text.slice(0, maxChars));
      });
      res.on("error", reject);
    });
    req.on("error", reject);
    req.on("timeout", () => { req.destroy(); reject(new Error("timeout")); });
  });
}

// ── standalone UI proxy server ────────────────────────────────────────────────

function getDashboardHtml(stripLegacyAuth = false): string {
  return stripLegacyAuth ? DASHBOARD_HTML.replace(/const AUTH = '[^']*'/, "const AUTH = ''") : DASHBOARD_HTML;
}

export function startStandaloneUiServer(
  _uiHtmlPath: string,
  gatewayUrl: string,
  port = 18790,
  bindAddress = "127.0.0.1",
  allowUnsafeBind = false,
  logger?: { warn?: (message: string) => void; info?: (message: string) => void; }
): http.Server {
  const normalizedBindAddress = bindAddress || "127.0.0.1";
  const isLoopbackOnly = normalizedBindAddress === "127.0.0.1" || normalizedBindAddress === "::1" || normalizedBindAddress === "localhost";
  if (!isLoopbackOnly) {
    if (!allowUnsafeBind) {
      throw new Error(`[orchard] refusing to start standalone UI on non-loopback bindAddress=${normalizedBindAddress}; set uiServer.allowUnsafeBind=true only if you intentionally want LAN exposure for the auth-forwarding proxy`);
    }
    logger?.warn?.(`[orchard] standalone UI bindAddress=${normalizedBindAddress} exposes a local auth-forwarding proxy beyond loopback; uiServer.allowUnsafeBind=true was set explicitly`);
  }
  const standaloneHtml = getDashboardHtml(true);
  // The proxy forwards the browser's Authorization header directly to the
  // gateway. No token is stored or injected server-side — the gateway itself
  // validates auth. Only same-host requests are proxied (CORS restricted).
  const server = http.createServer((req, res) => {
    const origin = req.headers.origin ?? "";
    const host = req.headers.host ?? "";
    // Exact hostname match to prevent substring-based bypass (e.g. attacker-localhost.com)
    let sameHost = !origin;
    if (origin) {
      try {
        sameHost = new URL(origin).hostname === host.split(":")[0];
      } catch { sameHost = false; }
    }
    if (!sameHost) {
      res.writeHead(403);
      res.end(JSON.stringify({ error: "forbidden" }));
      return;
    }
    if (origin) res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Authorization, Content-Type");
    res.setHeader("Vary", "Origin");

    if (req.method === "OPTIONS") {
      res.writeHead(204);
      res.end();
      return;
    }

    if (req.url?.startsWith("/orchard")) {
      // Pass the browser's Authorization header straight through.
      // The gateway rejects invalid/missing tokens — no need to re-check here.
      const target = new URL(req.url, gatewayUrl);
      // Whitelist only the headers the gateway needs — never forward cookies, host, etc.
      const proxyHeaders: Record<string, string | string[] | undefined> = {
        host: target.host,
        ...(req.headers.authorization ? { authorization: req.headers.authorization } : {}),
        ...(req.headers["content-type"] ? { "content-type": req.headers["content-type"] } : {}),
        ...(req.headers["content-length"] ? { "content-length": req.headers["content-length"] } : {}),
        ...(req.headers.accept ? { accept: req.headers.accept } : {}),
      };
      const proxyReq = http.request(
        {
          hostname: target.hostname,
          port: target.port,
          path: target.pathname + target.search,
          method: req.method,
          headers: proxyHeaders,
        },
        (proxyRes) => {
          res.writeHead(proxyRes.statusCode ?? 200, proxyRes.headers);
          proxyRes.pipe(res);
        }
      );
      proxyReq.on("error", () => {
        res.writeHead(502);
        res.end(JSON.stringify({ error: "gateway unavailable" }));
      });
      req.pipe(proxyReq);
      return;
    }

    // Serve dashboard HTML with no token embedded — browser handles auth via localStorage
    try {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" });
      res.end(standaloneHtml);
    } catch {
      res.writeHead(500);
      res.end("<h1>OrchardOS UI not found</h1>");
    }
  });

  server.on("error", (err) => {
    console.error(`[orchard] standalone UI server error: ${err.message}`);
  });
  server.listen(port, normalizedBindAddress, () => {
    console.log(`[orchard] UI available at http://${normalizedBindAddress}:${port}`);
  });
  return server;
}

// ── route registration ────────────────────────────────────────────────────────
// NOTE: OpenClaw plugin SDK registerHttpRoute does NOT support per-method routing —
// there is no `method` field in OpenClawPluginHttpRouteParams.
// Each registered path handles ALL HTTP methods; we branch on req.method internally.
// Paths with URL params (e.g. /orchard/projects/:id) must use match:"prefix" and
// parse params from req.url manually.

export function registerRoutes(
  api: any,
  getDb: () => Database.Database,
  getCfg?: () => OrchardConfig
): void {

  // ── /orchard/projects  (GET list | POST create) ───────────────────────────
  api.registerHttpRoute({
    path: "/orchard/projects",
    auth: "gateway",
    match: "exact",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      if (req.method === "GET") {
        const projects = db.prepare(`SELECT * FROM projects ORDER BY created_at DESC`).all();
        return jsonOk(res, projects);
      }
      if (req.method === "POST") {
        const body = await readBody(req);
        const { id, name, goal, completion_temperature } = body ?? {};
        if (!id || !name || !goal) return jsonErr(res, 400, "id, name, goal required");
        db.prepare(
          `INSERT INTO projects (id, name, goal, completion_temperature) VALUES (?, ?, ?, ?)`
        ).run(id, name, goal, completion_temperature ?? 0.7);
        const project = db.prepare(`SELECT * FROM projects WHERE id = ?`).get(id);
        return jsonOk(res, project, 200);
      }
      jsonErr(res, 405, "Method not allowed");
    },
  });

  // ── /orchard/wake  (POST) ─────────────────────────────────────────────────
  api.registerHttpRoute({
    path: "/orchard/wake",
    auth: "gateway",
    match: "exact",
    handler: async (_req: IncomingMessage, res: ServerResponse) => {
      const cb = getWakeCallback();
      if (cb) {
        cb().catch(() => {});
        return jsonOk(res, { triggered: true });
      }
      jsonOk(res, { triggered: false, message: "Queue runner not yet initialized" });
    },
  });

  // ── /orchard/debug/state  (GET) ───────────────────────────────────────────
  api.registerHttpRoute({
    path: "/orchard/debug/state",
    auth: "gateway",
    match: "exact",
    handler: async (_req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      const cfg = getCfg ? getCfg() : ({} as OrchardConfig);
      return jsonOk(res, getQueueDebugState(db, cfg));
    },
  });

  // ── /orchard/debug/control  (POST) ────────────────────────────────────────
  api.registerHttpRoute({
    path: "/orchard/debug/control",
    auth: "gateway",
    match: "exact",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      if (req.method !== "POST") return jsonErr(res, 405, "Method not allowed");
      const db = getDb();
      const cfg = getCfg ? getCfg() : ({} as OrchardConfig);
      const body = await readBody(req);
      const action = body?.action;
      const scope = body?.scope || "global";
      const cooldownMs = Math.max(0, Math.min(24 * 3600000, Number(body?.cooldownMs ?? cfg.debug?.circuitBreaker?.cooldownMs ?? 300000) || 300000));
      const reason = String(body?.reason || "manual operator action");
      const projectId = body?.projectId ? String(body.projectId) : null;

      if (action === "pauseQueue") {
        setQueuePaused(db, true);
        return jsonOk(res, { ok: true, queuePaused: true });
      }
      if (action === "resumeQueue") {
        setQueuePaused(db, false);
        return jsonOk(res, { ok: true, queuePaused: false });
      }
      if (action === "openCircuit") {
        openCircuit(db, scope, reason, cooldownMs);
        return jsonOk(res, { ok: true, scope, status: "open" });
      }
      if (action === "closeCircuit" || action === "resetCircuit") {
        closeCircuit(db, scope);
        return jsonOk(res, { ok: true, scope, status: "closed" });
      }
      if (action === "tickProject") {
        if (!projectId) return jsonErr(res, 400, "projectId required");
        const original = db.prepare(`SELECT status FROM projects WHERE id = ?`).get(projectId) as any;
        if (!original) return jsonErr(res, 404, "Project not found");
        await runQueueTick(db, cfg, api.runtime, api.logger, projectId);
        return jsonOk(res, { ok: true, projectId, note: "Triggered queue tick for the requested project" });
      }
      if (action === "cleanupSessions") {
        const rawPrefix = body?.prefix ? String(body.prefix) : "orchard-";
        // Escape LIKE special chars to prevent wildcard injection
        const prefix = rawPrefix.replace(/[%_\\]/g, "\\$&");
        const sessionRows = db.prepare(`
          SELECT DISTINCT session_key FROM task_runs
          WHERE status = 'running' AND session_key IS NOT NULL AND session_key LIKE ? ESCAPE '\\'
        `).all(`${prefix}%`) as any[];
        let deletedSessions = 0;
        for (const row of sessionRows) {
          try {
            await (api.runtime as any).subagent.deleteSession({ sessionKey: row.session_key, deleteTranscript: false });
            deletedSessions++;
          } catch { /* ignore — session may already be gone */ }
        }
        const result = db.prepare(`
          UPDATE task_runs
          SET status = 'failed', output = COALESCE(output, '[orchard][cleanup] stale session cleanup'), ended_at = CURRENT_TIMESTAMP
          WHERE status = 'running' AND (session_key IS NULL OR session_key LIKE ? ESCAPE '\\')
        `).run(`${prefix}%`);
        return jsonOk(res, { ok: true, cleanedRuns: result.changes ?? 0, deletedSessions, prefix });
      }

      if (action === "reapStalledRuns") {
        const taskId = body?.taskId ? parseInt(String(body.taskId), 10) : undefined;
        if (taskId !== undefined && (!Number.isFinite(taskId) || taskId <= 0)) return jsonErr(res, 400, "Invalid taskId");
        const result = await reapStalledRunsManual(db, api.runtime, cfg, api.logger, taskId);
        return jsonOk(res, { ok: true, ...result });
      }

      return jsonErr(res, 400, "Unknown debug control action");
    },
  });

  // ── /orchard/tasks/:id/runs  (GET) ───────────────────────────────────────
  // Must be registered before /orchard/tasks/:id to win on prefix match ordering.
  api.registerHttpRoute({
    path: "/orchard/tasks/",
    auth: "gateway",
    match: "prefix",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      const parts = urlParts(req); // ["orchard","tasks",<id>,"runs"|"comments"]
      const taskId = parseInt(parts[2] ?? "", 10);
      const sub = parts[3]; // "runs" | "comments" | undefined

      if (!Number.isFinite(taskId) || taskId <= 0) return jsonErr(res, 400, "Invalid task id");

      // GET /orchard/tasks/:id/runs
      if (sub === "runs" && req.method === "GET") {
        const runs = db
          .prepare(`SELECT * FROM task_runs WHERE task_id = ? ORDER BY started_at DESC`)
          .all(taskId);
        return jsonOk(res, runs);
      }

      // GET|POST /orchard/tasks/:id/comments
      if (sub === "comments") {
        if (req.method === "GET") {
          const comments = db
            .prepare(`SELECT * FROM task_comments WHERE task_id = ? ORDER BY created_at ASC`)
            .all(taskId);
          return jsonOk(res, comments);
        }
        if (req.method === "POST") {
          const existing = db.prepare(`SELECT id FROM tasks WHERE id = ?`).get(taskId);
          if (!existing) return jsonErr(res, 404, "Task not found");
          const body = await readBody(req);
          const { content, author } = body ?? {};
          if (!content) return jsonErr(res, 400, "content required");
          if (typeof content === "string" && content.length > 100_000) return jsonErr(res, 400, "content too large");
          const result = db
            .prepare(`INSERT INTO task_comments (task_id, author, content) VALUES (?, ?, ?)`)
            .run(taskId, author ?? "user", content);
          return jsonOk(res, { id: result.lastInsertRowid }, 200);
        }
      }

      // GET|PUT /orchard/tasks/:id  (no sub-resource)
      if (!sub) {
        if (req.method === "GET") {
          const task = db.prepare(`SELECT * FROM tasks WHERE id = ?`).get(taskId);
          if (!task) return jsonErr(res, 404, "Task not found");
          return jsonOk(res, task);
        }
        if (req.method === "PUT") {
          const existing = db.prepare(`SELECT id FROM tasks WHERE id = ?`).get(taskId);
          if (!existing) return jsonErr(res, 404, "Task not found");
          const activeRun = db.prepare(`SELECT id FROM task_runs WHERE task_id = ? AND status = 'running' ORDER BY id DESC LIMIT 1`).get(taskId);
          if (activeRun) return jsonErr(res, 409, "Task is currently running; mutation rejected");
          const body = await readBody(req);
          const { status, priority, description, acceptance_criteria } = body ?? {};
          const validStatuses = new Set(["pending","ready","assigned","running","done","failed","blocked","cancelled"]);
          const validPriorities = new Set(["critical","high","medium","low"]);
          if (status !== undefined && !validStatuses.has(status)) return jsonErr(res, 400, "Invalid status");
          if (priority !== undefined && !validPriorities.has(priority)) return jsonErr(res, 400, "Invalid priority");
          const fields: string[] = [];
          const vals: any[] = [];
          if (status !== undefined)               { fields.push("status = ?");               vals.push(status); }
          if (priority !== undefined)             { fields.push("priority = ?");             vals.push(priority); }
          if (description !== undefined)          { fields.push("description = ?");          vals.push(description); }
          if (acceptance_criteria !== undefined)  { fields.push("acceptance_criteria = ?");  vals.push(acceptance_criteria); }
          if (fields.length === 0) return jsonErr(res, 400, "No fields to update");
          fields.push("updated_at = CURRENT_TIMESTAMP");
          vals.push(taskId);
          db.prepare(`UPDATE tasks SET ${fields.join(", ")} WHERE id = ?`).run(...vals);
          return jsonOk(res, db.prepare(`SELECT * FROM tasks WHERE id = ?`).get(taskId));
        }

        if (req.method === 'DELETE') {
          const existing = db.prepare('SELECT id FROM tasks WHERE id = ?').get(taskId);
          if (!existing) return jsonErr(res, 404, 'Task not found');
          const activeRun = db.prepare(`SELECT id FROM task_runs WHERE task_id = ? AND status = 'running' ORDER BY id DESC LIMIT 1`).get(taskId);
          if (activeRun) return jsonErr(res, 409, 'Task is currently running; delete rejected');
          db.prepare('DELETE FROM tasks WHERE id = ?').run(taskId);
          return jsonOk(res, { deleted: true, id: taskId });
        }
      }

      jsonErr(res, 405, "Method not allowed");
    },
  });

  // ── /orchard/projects/:id/...  (prefix handler for all project sub-routes) ─
  api.registerHttpRoute({
    path: "/orchard/projects/",
    auth: "gateway",
    match: "prefix",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      const parts = urlParts(req); // ["orchard","projects",<id>,"tasks"|"knowledge"|undefined]
      const projectId = parts[2];
      const sub = parts[3]; // "tasks" | "knowledge" | undefined

      if (!projectId) return jsonErr(res, 400, "Invalid project id");

      // GET|POST /orchard/projects/:id/tasks
      if (sub === "tasks") {
        if (req.method === "GET") {
          const tasks = db
            .prepare(`SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at DESC`)
            .all(projectId);
          return jsonOk(res, tasks);
        }
        if (req.method === "POST") {
          const project = db.prepare(`SELECT id FROM projects WHERE id = ?`).get(projectId);
          if (!project) return jsonErr(res, 404, "Project not found");
          const body = await readBody(req);
          const { title, description, acceptance_criteria, priority, model_override } = body ?? {};
          if (!title) return jsonErr(res, 400, "title required");
          const validPrioritiesCreate = new Set(["critical","high","medium","low"]);
          if (priority !== undefined && !validPrioritiesCreate.has(priority)) return jsonErr(res, 400, "Invalid priority");
          const result = db
            .prepare(
              `INSERT INTO tasks (project_id, title, description, acceptance_criteria, priority, model_override, status)
               VALUES (?, ?, ?, ?, ?, ?, 'ready')`
            )
            .run(projectId, title, description ?? null, acceptance_criteria ?? null, priority ?? "medium", model_override ?? null);
          return jsonOk(res, { id: result.lastInsertRowid, status: "ready" }, 201);
        }
      }

      // GET|POST /orchard/projects/:id/knowledge
      if (sub === "knowledge") {
        if (req.method === "GET") {
          const rows = db
            .prepare(
              `SELECT id, project_id, content, source, task_id, created_at
               FROM project_knowledge WHERE project_id = ? ORDER BY created_at DESC`
            )
            .all(projectId);
          return jsonOk(res, rows);
        }
        if (req.method === "POST") {
          const project = db.prepare(`SELECT id FROM projects WHERE id = ?`).get(projectId);
          if (!project) return jsonErr(res, 404, "Project not found");
          const body = await readBody(req);
          const { content } = body ?? {};
          if (!content) return jsonErr(res, 400, "content required");
          const cfg = getCfg ? getCfg() : ({} as OrchardConfig);
          await addKnowledge(db, cfg, projectId, content, "user");
          return jsonOk(res, { stored: true });
        }
      }

      // GET /orchard/projects/:id  (no sub-resource)
      if (!sub) {
        if (req.method === "GET") {
          const project = db.prepare(`SELECT * FROM projects WHERE id = ?`).get(projectId);
          if (!project) return jsonErr(res, 404, "Project not found");
          return jsonOk(res, project);
        }
      }

      jsonErr(res, 405, "Method not allowed");
    },
  });

  // ── /orchard/settings  (GET all | PUT one) ──────────────────────────────
  api.registerHttpRoute({
    path: "/orchard/settings",
    auth: "gateway",
    match: "exact",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      if (req.method === "GET") {
        return jsonOk(res, getAllSettings(db));
      }
      if (req.method === "PUT") {
        const body = await readBody(req);
        const { key, value } = body ?? {};
        if (!key) return jsonErr(res, 400, "key required");
        setSetting(db, key, value);
        return jsonOk(res, { ok: true });
      }
      jsonErr(res, 405, "Method not allowed");
    },
  });

  // ── /orchard/activity  (GET live task activity) ───────────────────────────
  api.registerHttpRoute({
    path: "/orchard/activity",
    auth: "gateway",
    match: "exact",
    handler: async (_req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      const running = db.prepare(`
        SELECT t.id as taskId, t.title, t.project_id as projectId,
               tr.model, tr.session_key as sessionKey, tr.timeout_at as timeoutAt,
               tr.id as runId, tr.input as inputJson,
               COALESCE(tr.started_at, t.updated_at) as startedAt
        FROM tasks t
        LEFT JOIN task_runs tr ON tr.id = (SELECT id FROM task_runs WHERE task_id = t.id ORDER BY id DESC LIMIT 1)
        WHERE t.status IN ('running', 'assigned')
        ORDER BY t.updated_at DESC LIMIT 20
      `).all();
      const recent = db.prepare(`
        SELECT t.id as taskId, t.title, t.project_id as projectId,
               tr.status, tr.output, tr.model, tr.session_key as sessionKey,
               tr.ended_at as endedAt
        FROM task_runs tr JOIN tasks t ON t.id = tr.task_id
        WHERE tr.status IN ('done', 'failed') AND tr.ended_at > datetime('now', '-30 minutes')
        ORDER BY tr.ended_at DESC LIMIT 20
      `).all();
      const totalRow = db.prepare(`SELECT COUNT(*) as n FROM tasks`).get() as { n: number };
      // Truncate output to last 200 chars
      const recentClean = (recent as any[]).map((r: any) => ({
        ...r,
        output: r.output ? String(r.output).slice(-200).replace(/\n/g, ' ').trim() : '',
      }));

      // Capacity / limits snapshot
      const g = (key: string, fallback: unknown) => {
        try { return getSetting(db, key) ?? fallback; } catch { return fallback; }
      };
      const maxConcurrent = (g('limits.maxConcurrentExecutors', 2) as number);
      const maxPerHour = (g('limits.maxTasksPerHour', 10) as number);
      const maxPerProject = (g('limits.maxSubagentsPerProject', 3) as number);
      const limitsEnabled = g('limits.enabled', true) as boolean;
      const logOnly = g('debug.logOnly', false) as boolean;
      const disableAll = g('debug.disableAllSpawns', false) as boolean;
      const disableExecutors = g('debug.disableExecutorSpawns', false) as boolean;
      const queuePaused = isQueuePaused(db);
      const spawnsEnabled = !logOnly && !disableAll && !disableExecutors && !queuePaused;
      const spreadTasksOverPeriod = g('limits.spreadTasksOverPeriod', false) as boolean;
      const minNextDelayMs = (g('limits.minNextDelayMs', 0) as number);

      // Compute spread interval for display: (3600000 / maxPerHour) * maxConcurrent
      const spreadIntervalMs = spreadTasksOverPeriod
        ? Math.floor(3600000 / maxPerHour) * maxConcurrent
        : (minNextDelayMs > 0 ? minNextDelayMs : null);

      return jsonOk(res, {
        running,
        recent: recentClean,
        counts: { running: (running as any[]).length, total: totalRow?.n ?? 0 },
        capacity: {
          maxConcurrent,
          maxPerHour,
          maxPerProject,
          limitsEnabled,
          spawnsEnabled,
          queuePaused,
          logOnly,
          disableAllSpawns: disableAll,
          disableExecutorSpawns: disableExecutors,
          spreadTasksOverPeriod,
          minNextDelayMs,
          spreadIntervalMs,
        },
      });
    },
  });

  // ── /orchard/config  (GET current plugin config) ─────────────────────────
  api.registerHttpRoute({
    path: "/orchard/config",
    auth: "gateway",
    match: "exact",
    handler: async (_req: IncomingMessage, res: ServerResponse) => {
      const cfg = getCfg ? getCfg() : ({} as OrchardConfig);
      const allowModelOverride = cfg.allowModelOverride === true;
      return jsonOk(res, { ...cfg, allowModelOverride });
    },
  });

  // ── /orchard/models  (GET available models from openclaw.json) ────────────
  api.registerHttpRoute({
    path: "/orchard/models",
    auth: "gateway",
    match: "exact",
    handler: async (_req: IncomingMessage, res: ServerResponse) => {
      const models: { id: string; name: string; provider: string }[] = [];
      const providers: Record<string, { models?: { id: string; name?: string }[] }> =
        (api.config as any)?.models?.providers ?? {};
      for (const [providerId, p] of Object.entries(providers)) {
        for (const m of (p as any).models ?? []) {
          models.push({ id: `${providerId}/${m.id}`, name: m.name ?? m.id, provider: providerId });
        }
      }
      return jsonOk(res, models);
    },
  });

  // ── /orchard/config-safety/:id/inject  (GET) ─────────────────────────────
  api.registerHttpRoute({
    path: "/orchard/config-safety/",
    auth: "gateway",
    match: "prefix",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      const cfg = getCfg ? getCfg() : ({} as OrchardConfig);
      const parts = urlParts(req); // ["orchard","config-safety",<id>,"inject"]
      const profileId = parts[2];
      const sub = parts[3];

      // GET /orchard/config-safety (list all)
      if (!profileId && req.method === "GET") {
        const profiles = db.prepare(`SELECT * FROM config_safety_profiles ORDER BY id`).all();
        return jsonOk(res, profiles);
      }

      // POST /orchard/config-safety (create)
      if (!profileId && req.method === "POST") {
        const body = await readBody(req);
        let data: any = {};
        try { data = JSON.parse(body); } catch { return jsonErr(res, 400, "Invalid JSON"); }
        const { name, enabled = 1, doc_urls = "[]", knowledge_sources = "[]", watchdog_inject = 0, custom_rules = "" } = data;
        if (!name) return jsonErr(res, 400, "name required");
        const result = db.prepare(
          `INSERT INTO config_safety_profiles (name, enabled, doc_urls, knowledge_sources, watchdog_inject, custom_rules) VALUES (?, ?, ?, ?, ?, ?)`
        ).run(name, enabled ? 1 : 0, typeof doc_urls === "string" ? doc_urls : JSON.stringify(doc_urls),
          typeof knowledge_sources === "string" ? knowledge_sources : JSON.stringify(knowledge_sources),
          watchdog_inject ? 1 : 0, custom_rules);
        const created = db.prepare(`SELECT * FROM config_safety_profiles WHERE id = ?`).get(result.lastInsertRowid);
        return jsonOk(res, created);
      }

      if (!profileId) return jsonErr(res, 400, "Profile id required");

      // GET /orchard/config-safety/:id/inject
      if (sub === "inject" && req.method === "GET") {
        const profile = db.prepare(`SELECT * FROM config_safety_profiles WHERE id = ?`).get(profileId) as any;
        if (!profile) return jsonErr(res, 404, `Config safety profile '${profileId}' not found`);

        const sections: string[] = [];
        const sources: string[] = [];

        // ── 1. Config-change rules preamble ───────────────────────────────
        const preamble = [
          "## ⛔ Config Change Safety Rules",
          "",
          "Before making ANY configuration change:",
          "1. Read the relevant documentation first — no exceptions",
          "2. Back up the current config before editing",
          "3. Leave a note in `~/.openclaw/watchdog-notes.md` describing the change",
          "4. Verify the change after applying it",
          "5. If unsure, ask before proceeding",
          "",
          "**Key config facts:**",
          "- `google` provider is built-in — auth via `env.GEMINI_API_KEY`, no `models.providers` entry needed",
          "- Agent auth is per-agent: `~/.openclaw/agents/<id>/agent/auth-profiles.json`",
          "- Model fallbacks: `agents.list[].model.fallbacks` in openclaw.json",
          "- Use `thinkingDefault: \"off\"` per-agent to disable reasoning",
          "- `maxChildrenPerAgent` controls subagent concurrency (not `maxConcurrent`)",
        ].join("\n");
        sections.push(preamble);
        sources.push("preamble:config-change-rules");

        // ── 2. Doc URLs ────────────────────────────────────────────────────
        let docUrls: string[] = [];
        try { docUrls = JSON.parse(profile.doc_urls ?? "[]"); } catch {}
        for (const url of docUrls) {
          try {
            const content = await fetchUrl(url, 2000);
            const heading = `## 📄 Doc: ${url}`;
            sections.push(`${heading}\n\n${content}`);
            sources.push(`doc_url:${url}`);
          } catch (e: any) {
            sections.push(`## 📄 Doc: ${url}\n\n_(fetch failed: ${e?.message ?? "unknown error"})_`);
            sources.push(`doc_url:${url}:error`);
          }
        }

        // ── 3. Knowledge sources ───────────────────────────────────────────
        let knowledgeSources: string[] = [];
        try { knowledgeSources = JSON.parse(profile.knowledge_sources ?? "[]"); } catch {}
        for (const projectId of knowledgeSources) {
          try {
            const entries = await searchKnowledge(db, cfg, projectId, "config change safety rules watchdog", 5, 0.0);
            if (entries.length > 0) {
              const kbText = entries.map(e => `- ${e.content.slice(0, 400)}`).join("\n");
              sections.push(`## 🧠 Knowledge: ${projectId}\n\n${kbText}`);
              sources.push(`knowledge:${projectId}`);
            }
          } catch (e: any) {
            sources.push(`knowledge:${projectId}:error`);
          }
        }

        // ── 4. Watchdog rules ─────────────────────────────────────────────
        if (profile.watchdog_inject) {
          const watchdogSection = [
            "## 🐕 Watchdog Safety Rules",
            "",
            "**Backup paths:**",
            "- Configs: `~/.backup/openclaw-configs/`",
            "- Script: `~/.openclaw/workspace/scripts/watchdog.sh`",
            "",
            "**Notes file:** `~/.openclaw/watchdog-notes.md`",
            "Always append a note here before changing any config.",
            "",
            "**Recovery steps:**",
            "1. Identify broken config file",
            "2. Restore from `~/.backup/openclaw-configs/` (most recent backup)",
            "3. Restart the service: `openclaw gateway restart`",
            "4. Verify: `openclaw gateway status`",
            "5. If still broken: check `journalctl --user -u openclaw -n 50 --no-pager`",
            "",
            "**On 3 consecutive failures:** Watchdog quarantines bad config and restores last known good.",
          ].join("\n");
          sections.push(watchdogSection);
          sources.push("watchdog:rules");
        }

        // ── 5. Custom rules ───────────────────────────────────────────────
        if (profile.custom_rules?.trim()) {
          sections.push(`## 📝 Custom Rules\n\n${profile.custom_rules.trim()}`);
          sources.push("custom_rules");
        }

        const injection_text = sections.join("\n\n---\n\n");
        return jsonOk(res, { injection_text, sources });
      }

      // GET /orchard/config-safety/:id  (profile detail)
      if (!sub && req.method === "GET") {
        const profile = db.prepare(`SELECT * FROM config_safety_profiles WHERE id = ?`).get(profileId);
        if (!profile) return jsonErr(res, 404, `Profile '${profileId}' not found`);
        return jsonOk(res, profile);
      }

      // PUT /orchard/config-safety/:id (update)
      if (!sub && req.method === "PUT") {
        const existing = db.prepare(`SELECT * FROM config_safety_profiles WHERE id = ?`).get(profileId) as any;
        if (!existing) return jsonErr(res, 404, `Profile '${profileId}' not found`);
        const body = await readBody(req);
        let data: any = {};
        try { data = JSON.parse(body); } catch { return jsonErr(res, 400, "Invalid JSON"); }
        const name = data.name ?? existing.name;
        const enabled = data.enabled !== undefined ? (data.enabled ? 1 : 0) : existing.enabled;
        const doc_urls = data.doc_urls !== undefined
          ? (typeof data.doc_urls === "string" ? data.doc_urls : JSON.stringify(data.doc_urls))
          : existing.doc_urls;
        const knowledge_sources = data.knowledge_sources !== undefined
          ? (typeof data.knowledge_sources === "string" ? data.knowledge_sources : JSON.stringify(data.knowledge_sources))
          : existing.knowledge_sources;
        const watchdog_inject = data.watchdog_inject !== undefined ? (data.watchdog_inject ? 1 : 0) : existing.watchdog_inject;
        const custom_rules = data.custom_rules !== undefined ? data.custom_rules : existing.custom_rules;
        db.prepare(
          `UPDATE config_safety_profiles SET name=?, enabled=?, doc_urls=?, knowledge_sources=?, watchdog_inject=?, custom_rules=? WHERE id=?`
        ).run(name, enabled, doc_urls, knowledge_sources, watchdog_inject, custom_rules, profileId);
        const updated = db.prepare(`SELECT * FROM config_safety_profiles WHERE id = ?`).get(profileId);
        return jsonOk(res, updated);
      }

      // DELETE /orchard/config-safety/:id
      if (!sub && req.method === "DELETE") {
        const existing = db.prepare(`SELECT * FROM config_safety_profiles WHERE id = ?`).get(profileId);
        if (!existing) return jsonErr(res, 404, `Profile '${profileId}' not found`);
        db.prepare(`DELETE FROM config_safety_profiles WHERE id = ?`).run(profileId);
        return jsonOk(res, { deleted: true, id: profileId });
      }

      jsonErr(res, 405, "Method not allowed");
    },
  });

  // ── /orchard/knowledge/:id  (DELETE) ────────────────────────────────────
  api.registerHttpRoute({
    path: "/orchard/knowledge/",
    auth: "gateway",
    match: "prefix",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      const db = getDb();
      const parts = urlParts(req); // ["orchard","knowledge",<id>]
      const entryId = Number(parts[2]);
      if (!entryId) return jsonErr(res, 400, "Invalid entry id");
      if (req.method === "DELETE") {
        const existing = db.prepare(`SELECT id FROM project_knowledge WHERE id = ?`).get(entryId);
        if (!existing) return jsonErr(res, 404, "Knowledge entry not found");
        db.prepare(`DELETE FROM project_knowledge WHERE id = ?`).run(entryId);
        return jsonOk(res, { deleted: true, id: entryId });
      }
      jsonErr(res, 405, "Method not allowed");
    },
  });

  // ── /orchard/ui  (serve dashboard HTML) ──────────────────────────────────
  const uiHtml = getDashboardHtml();
  const serveUi = async (_req: IncomingMessage, res: ServerResponse) => {
    try {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" });
      res.end(uiHtml);
    } catch {
      res.writeHead(500, { "Content-Type": "text/html" });
      res.end("<h1>OrchardOS UI not found</h1>");
    }
  };
  api.registerHttpRoute({ path: "/orchard/ui", auth: "gateway", match: "prefix", handler: serveUi });
}
