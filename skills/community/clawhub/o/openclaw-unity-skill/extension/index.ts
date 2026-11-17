/**
 * OpenClaw Unity Plugin
 * Connects Unity Editor to OpenClaw AI assistant via HTTP
 */

import type { IncomingMessage, ServerResponse } from "node:http";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";

interface UnitySession {
  sessionId: string;
  registeredAt: number;
  lastHeartbeat: number;
  projectName: string;
  unityVersion: string;
  platform: string;
  toolCount: number;
  pendingCommands: Array<{
    toolCallId: string;
    tool: string;
    arguments: Record<string, any>;
    createdAt: number;
  }>;
  results: Map<string, any>;
}

// Store active Unity sessions
const sessions = new Map<string, UnitySession>();

// Generate unique ID
function generateId(): string {
  return `unity_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}

// Clean up stale sessions (no heartbeat for 2 minutes)
function cleanupStaleSessions() {
  const now = Date.now();
  const staleThreshold = 120000; // 2 minutes
  
  for (const [id, session] of sessions) {
    if (now - session.lastHeartbeat > staleThreshold) {
      sessions.delete(id);
    }
  }
}

// ===== Safety gate: runtime confirmation for project-changing operations =====
//
// Read-only tools (get*/list/find/read/hierarchy/screenshot/...) behave exactly
// as before. Anything that can change the project — creating or deleting
// GameObjects and assets, saving scenes, installing packages, running C# via
// script.execute, simulating input, entering Play mode — is refused by default
// and needs two independent opt-ins:
//
//   1. the operator starts the gateway with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1
//      (or OPENCLAW_UNITY_ALLOW_DESTRUCTIVE=1), and
//   2. the caller passes confirm: true on that individual call, after asking
//      the user about that specific change.
//
// Unknown tool names — including project-registered custom tools — count as
// project-changing unless their verb is clearly read-only: the gate fails
// closed, never open. Pass dryRun: true to preview any call without sending it.

const ENGINE_LABEL = "Unity";

/** Environment variables that let the operator enable project-changing calls. */
const ALLOW_DESTRUCTIVE_ENV_VARS = [
  "OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE",
  "OPENCLAW_UNITY_ALLOW_DESTRUCTIVE",
];

export type ToolRisk = "read-only" | "project-changing";

/** Verbs that only read Editor/project state. */
const READ_ONLY_VERB =
  /^(get|list|find|search|read|inspect|describe|query|exists|has|count|status|state|info|tree|hierarchy|screenshot|capture)/i;

/** Tools that write something, but never the project or its assets. */
const NON_MUTATING_TOOLS = new Set([
  "debug.log",              // writes one line to the Editor console
  "editor.focuswindow",     // moves Editor UI focus
  "editor.listwindows",
  "scriptableobject.load",  // loads an existing asset for inspection only
]);

/** Names that are project-changing even when the verb reads like a query. */
const HIGH_RISK_NAME =
  /(execute|eval|delete|destroy|remove|install|uninstall|build|import|deploy|publish|reset|\brun\b)/i;

/** Tools whose real risk is the risk of the commands they carry. */
const BATCH_TOOLS = new Set(["batch.execute"]);
const MAX_BATCH_DEPTH = 4;

function currentEnv(): Record<string, string | undefined> {
  return (globalThis as any)?.process?.env ?? {};
}

function isTruthyFlag(value: unknown): boolean {
  if (value === true) return true;
  if (typeof value === "string") return /^(1|true|yes|on)$/i.test(value.trim());
  return false;
}

function batchCommands(parameters: any): any[] | null {
  const commands = parameters?.commands ?? parameters?.calls;
  return Array.isArray(commands) ? commands : null;
}

/**
 * Classify one tool call. Fails closed: anything unrecognised, unnamed or
 * malformed counts as project-changing.
 */
export function classifyTool(
  tool: unknown,
  parameters?: Record<string, any>,
  depth = 0
): ToolRisk {
  const name = typeof tool === "string" ? tool.trim() : "";
  if (!name) return "project-changing";
  const key = name.toLowerCase();

  // A batch is exactly as risky as the riskiest command inside it.
  if (BATCH_TOOLS.has(key)) {
    if (depth >= MAX_BATCH_DEPTH) return "project-changing";
    const commands = batchCommands(parameters);
    if (!commands || commands.length === 0) return "project-changing";
    for (const command of commands) {
      if (!command || typeof command !== "object") return "project-changing";
      const sub = classifyTool(
        (command as any).tool,
        (command as any).params ?? (command as any).parameters,
        depth + 1
      );
      if (sub === "project-changing") return "project-changing";
    }
    return "read-only";
  }

  if (NON_MUTATING_TOOLS.has(key)) return "read-only";
  if (HIGH_RISK_NAME.test(key)) return "project-changing";

  const verb = key.includes(".") ? key.slice(key.lastIndexOf(".") + 1) : key;
  return READ_ONLY_VERB.test(verb) ? "read-only" : "project-changing";
}

/** The project-changing tool names a call would run (flattens batches). */
export function projectChangingTools(
  tool: unknown,
  parameters?: Record<string, any>,
  depth = 0
): string[] {
  const name =
    typeof tool === "string" && tool.trim() ? tool.trim() : "(unnamed tool)";
  const key = name.toLowerCase();

  if (BATCH_TOOLS.has(key) && depth < MAX_BATCH_DEPTH) {
    const commands = batchCommands(parameters);
    if (!commands || commands.length === 0) return [name];
    const found: string[] = [];
    for (const command of commands) {
      if (!command || typeof command !== "object") {
        found.push(`${name} (malformed command)`);
        continue;
      }
      found.push(
        ...projectChangingTools(
          (command as any).tool,
          (command as any).params ?? (command as any).parameters,
          depth + 1
        )
      );
    }
    return found;
  }

  return classifyTool(name, parameters, depth) === "project-changing"
    ? [name]
    : [];
}

/** True when the operator started the gateway with project changes enabled. */
export function destructiveOperationsEnabled(
  env: Record<string, string | undefined> = currentEnv()
): boolean {
  return ALLOW_DESTRUCTIVE_ENV_VARS.some((name) => isTruthyFlag(env[name]));
}

export interface GateDecision {
  allowed: boolean;
  risk: ToolRisk;
  /** Project-changing tools this call would run. */
  tools: string[];
  reason:
    | "read-only"
    | "confirmed"
    | "operator-opt-in-missing"
    | "confirmation-missing";
  message?: string;
}

/**
 * The runtime confirmation control. Read-only calls pass through untouched;
 * project-changing calls require operator opt-in AND per-call confirm: true.
 */
export function evaluateDestructiveGate(input: {
  tool: unknown;
  parameters?: Record<string, any>;
  confirm?: unknown;
  env?: Record<string, string | undefined>;
}): GateDecision {
  const env = input.env ?? currentEnv();
  const risk = classifyTool(input.tool, input.parameters);

  if (risk === "read-only") {
    return { allowed: true, risk, tools: [], reason: "read-only" };
  }

  const tools = projectChangingTools(input.tool, input.parameters);
  const listed = tools.length > 0 ? tools.join(", ") : "this call";

  if (!destructiveOperationsEnabled(env)) {
    return {
      allowed: false,
      risk,
      tools,
      reason: "operator-opt-in-missing",
      message:
        `Refused: ${listed} would change this ${ENGINE_LABEL} project, and this gateway was ` +
        `not started with project-changing operations enabled. Ask the user to confirm the ` +
        `change, restart the gateway with ${ALLOW_DESTRUCTIVE_ENV_VARS[0]}=1 (or ` +
        `${ALLOW_DESTRUCTIVE_ENV_VARS[1]}=1), then repeat the call with confirm: true. ` +
        `Read-only tools are unaffected; pass dryRun: true to preview a call without sending it.`,
    };
  }

  if (!isTruthyFlag(input.confirm)) {
    return {
      allowed: false,
      risk,
      tools,
      reason: "confirmation-missing",
      message:
        `Refused: ${listed} would change this ${ENGINE_LABEL} project. Confirm the change with ` +
        `the user, then repeat this call with confirm: true. Pass dryRun: true to preview it first.`,
    };
  }

  return { allowed: true, risk, tools, reason: "confirmed" };
}

// Read JSON body from request
async function readJsonBody(req: IncomingMessage, maxBytes = 1024 * 1024): Promise<any> {
  const chunks: Buffer[] = [];
  let total = 0;
  
  return new Promise((resolve, reject) => {
    req.on("data", (chunk: Buffer) => {
      total += chunk.length;
      if (total > maxBytes) {
        reject(new Error("Payload too large"));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    
    req.on("end", () => {
      const raw = Buffer.concat(chunks).toString("utf8");
      if (!raw.trim()) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(raw));
      } catch (err) {
        // Older Unity plugins on comma-decimal locales (e.g. pl-PL) emit
        // "time":323,60 — repair bare-number commas and retry before failing.
        const repaired = raw.replace(/(:\s*-?\d+),(\d+\s*[,}\]])/g, "$1.$2");
        if (repaired !== raw) {
          try {
            resolve(JSON.parse(repaired));
            return;
          } catch {
            // fall through to reject with the original error
          }
        }
        reject(err);
      }
    });
    
    req.on("error", reject);
  });
}

// Send JSON response
function sendJson(res: ServerResponse, status: number, data: any) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.end(JSON.stringify(data));
}

// HTTP Handler for Unity endpoints
async function handleUnityHttpRequest(
  req: IncomingMessage,
  res: ServerResponse
): Promise<boolean> {
  const url = new URL(req.url ?? "/", "http://localhost");
  const path = url.pathname;
  
  // Only handle /unity/* paths
  if (!path.startsWith("/unity/")) {
    return false;
  }
  
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
    res.statusCode = 204;
    res.end();
    return true;
  }
  
  const endpoint = path.replace("/unity/", "");
  
  try {
    switch (endpoint) {
      case "register": {
        if (req.method !== "POST") {
          sendJson(res, 405, { error: "Method not allowed" });
          return true;
        }
        
        const body = await readJsonBody(req);
        const { project, version, platform, tools } = body;
        
        const sessionId = generateId();
        const session: UnitySession = {
          sessionId,
          registeredAt: Date.now(),
          lastHeartbeat: Date.now(),
          projectName: project || "Unknown",
          unityVersion: version || "Unknown",
          platform: platform || "UnityEditor",
          toolCount: tools || 0,
          pendingCommands: [],
          results: new Map(),
        };
        
        sessions.set(sessionId, session);
        console.log(`[Unity] Registered: ${project} (${version}) - Session: ${sessionId}`);
        
        sendJson(res, 200, { sessionId, status: "connected" });
        return true;
      }
      
      case "heartbeat": {
        if (req.method !== "POST") {
          sendJson(res, 405, { error: "Method not allowed" });
          return true;
        }
        
        const body = await readJsonBody(req);
        const { sessionId } = body;
        
        const session = sessions.get(sessionId);
        if (!session) {
          sendJson(res, 404, { error: "Session not found" });
          return true;
        }
        
        session.lastHeartbeat = Date.now();
        sendJson(res, 200, { ok: true });
        return true;
      }
      
      case "poll": {
        const sessionId = url.searchParams.get("sessionId");
        
        const session = sessions.get(sessionId || "");
        if (!session) {
          sendJson(res, 404, { error: "Session not found" });
          return true;
        }
        
        session.lastHeartbeat = Date.now();
        
        // Return next pending command if any
        if (session.pendingCommands.length > 0) {
          const command = session.pendingCommands.shift()!;
          sendJson(res, 200, command);
        } else {
          // No content
          res.statusCode = 204;
          res.end();
        }
        return true;
      }
      
      case "result": {
        if (req.method !== "POST") {
          sendJson(res, 405, { error: "Method not allowed" });
          return true;
        }
        
        const body = await readJsonBody(req);
        const { sessionId, toolCallId, result } = body;
        
        const session = sessions.get(sessionId);
        if (!session) {
          sendJson(res, 404, { error: "Session not found" });
          return true;
        }
        
        session.results.set(toolCallId, result);
        console.log(`[Unity] Tool result received for: ${toolCallId}`);
        
        sendJson(res, 200, { ok: true });
        return true;
      }
      
      case "status": {
        const activeSessions = Array.from(sessions.values()).map(s => ({
          sessionId: s.sessionId,
          project: s.projectName,
          version: s.unityVersion,
          platform: s.platform,
          connectedAt: new Date(s.registeredAt).toISOString(),
          lastSeen: new Date(s.lastHeartbeat).toISOString(),
          pendingCommands: s.pendingCommands.length,
        }));
        
        sendJson(res, 200, {
          enabled: true,
          destructiveOperations: destructiveOperationsEnabled() ? "enabled" : "blocked",
          sessions: activeSessions,
          sessionCount: activeSessions.length,
        });
        return true;
      }
      
      default:
        sendJson(res, 404, { error: "Unknown endpoint" });
        return true;
    }
  } catch (err: any) {
    console.error("[Unity] HTTP error:", err);
    sendJson(res, 500, { error: err.message });
    return true;
  }
}

const plugin = {
  id: "unity",
  name: "Unity Plugin",
  description: "Connect Unity Editor to OpenClaw AI assistant",
  
  register(api: OpenClawPluginApi) {
    const logger = api.logger;
    
    // Cleanup timer
    setInterval(cleanupStaleSessions, 30000);
    
    // Register HTTP handler.
    // OpenClaw ≥2026.3 removed registerHttpHandler in favor of registerHttpRoute —
    // support both so the plugin loads on old and new gateways (issue #1).
    const httpApi = api as any;
    if (typeof httpApi.registerHttpRoute === "function") {
      httpApi.registerHttpRoute({
        path: "/unity",
        auth: "plugin",
        match: "prefix",
        handler: handleUnityHttpRequest,
      });
    } else {
      httpApi.registerHttpHandler(handleUnityHttpRequest);
    }
    
    // ===== Agent Tools =====
    
    // Tool: Execute a Unity command
    api.registerTool({
      name: "unity_execute",
      description: "Execute a tool in the connected Unity Editor. Available tools: console.getLogs, scene.getData, gameobject.find, gameobject.create, gameobject.delete, gameobject.setActive, transform.setPosition, transform.setRotation, transform.setScale, component.get, component.add, debug.hierarchy, debug.screenshot, app.getState, app.play, app.stop, input.simulateKey, input.simulateMouse, and more. Read-only tools (get*/list/find/read/debug.hierarchy/debug.screenshot) run directly. Project-changing tools are refused unless the gateway was started with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 and the call passes confirm: true after the user approved the change; dryRun: true previews any call without sending it.",
      parameters: {
        type: "object" as const,
        properties: {
          tool: { type: "string" as const, description: "The Unity tool to execute (e.g., 'debug.hierarchy', 'gameobject.find')" },
          parameters: { type: "object" as const, description: "Parameters for the tool (varies by tool)" },
          sessionId: { type: "string" as const, description: "Optional: specific Unity session ID" },
          confirm: {
            type: "boolean" as const,
            description:
              "Required for project-changing tools (create/delete/save/set*, package.add, script.execute, input.*, editor.play). Set it only after the user has approved that specific change. Read-only tools ignore it.",
          },
          dryRun: {
            type: "boolean" as const,
            description:
              "Preview only: report how the call is classified and what would be sent to the Editor, without sending it.",
          },
        },
        required: ["tool"] as const,
      },
      execute: async (toolCallId: string, args: any) => {
        // Helper to format result for OpenClaw
        const jsonResult = (payload: any) => ({
          content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
          details: payload,
        });
        
        // Extract parameters
        const tool = args?.tool;
        const parameters = args?.parameters;
        const sessionId = args?.sessionId;
        
        if (!tool) {
          return jsonResult({
            success: false,
            error: "Missing 'tool' parameter. Specify which Unity tool to execute (e.g., 'debug.hierarchy', 'gameobject.find').",
          });
        }
        
        // Safety gate (see "Safety gate" above): read-only calls pass straight
        // through, project-changing calls need operator opt-in + confirm: true.
        const gate = evaluateDestructiveGate({
          tool,
          parameters,
          confirm: args?.confirm,
        });

        if (isTruthyFlag(args?.dryRun)) {
          return jsonResult({
            success: true,
            dryRun: true,
            executed: false,
            tool,
            parameters: parameters || {},
            risk: gate.risk,
            projectChangingTools: gate.tools,
            requiresConfirmation: gate.risk === "project-changing",
            destructiveOperationsEnabled: destructiveOperationsEnabled(),
            wouldRun: gate.allowed,
            gate: { reason: gate.reason, message: gate.message },
          });
        }

        if (!gate.allowed) {
          logger.info(
            `[Unity] Refused ${gate.risk} call: ${gate.tools.join(", ") || tool} (${gate.reason})`
          );
          return jsonResult({
            success: false,
            error: gate.message,
            gate: {
              allowed: false,
              risk: gate.risk,
              reason: gate.reason,
              tools: gate.tools,
            },
          });
        }

        // Find session
        let session: UnitySession | undefined;
        
        if (sessionId) {
          session = sessions.get(sessionId);
        } else {
          // Use first active session
          const firstSession = sessions.values().next();
          session = firstSession.done ? undefined : firstSession.value;
        }
        
        if (!session) {
          return jsonResult({
            success: false,
            error: "No Unity session connected. Make sure Unity Editor is running with OpenClaw plugin enabled.",
          });
        }
        
        // Create command
        const requestId = generateId();
        session.pendingCommands.push({
          toolCallId: requestId,
          tool,
          arguments: parameters || {},
          createdAt: Date.now(),
        });
        
        logger.info(`[Unity] Queued command: ${tool} (request: ${requestId})`);
        
        // Wait for result (with timeout)
        const timeout = 60000; // 60 seconds
        const startTime = Date.now();
        
        while (Date.now() - startTime < timeout) {
          if (session.results.has(requestId)) {
            const result = session.results.get(requestId);
            session.results.delete(requestId);
            
            return jsonResult({
              success: true,
              result,
            });
          }
          
          await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        return jsonResult({
          success: false,
          error: "Timeout waiting for Unity response. Make sure the OpenClaw plugin is enabled in Unity Editor.",
        });
      },
    });
    
    // Tool: List Unity sessions
    api.registerTool({
      name: "unity_sessions",
      description: "List all connected Unity Editor sessions",
      parameters: {
        type: "object" as const,
        properties: {
          _dummy: { type: "string" as const, description: "Unused parameter" },
        },
        required: [] as const,
      },
      execute: async (_toolCallId: string, _args: any) => {
        const activeSessions = Array.from(sessions.values()).map(s => ({
          sessionId: s.sessionId,
          project: s.projectName,
          version: s.unityVersion,
          platform: s.platform,
          tools: s.toolCount,
        }));
        
        const payload = {
          success: true,
          sessions: activeSessions,
          count: activeSessions.length,
        };
        
        return {
          content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
          details: payload,
        };
      },
    });
    
    // ===== CLI Commands =====
    
    api.registerCli(
      ({ program }) => {
        const unityCmd = program
          .command("unity")
          .description("Unity Plugin commands");
        
        unityCmd
          .command("status")
          .description("Show Unity connection status")
          .action(() => {
            console.log("\n🎮 Unity Plugin Status\n");
            console.log(
              destructiveOperationsEnabled()
                ? "  Project-changing tools: ENABLED (confirm: true still required per call)\n"
                : "  Project-changing tools: BLOCKED (start the gateway with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 to enable)\n"
            );
            
            if (sessions.size === 0) {
              console.log("  No Unity sessions connected.\n");
              console.log("  To connect Unity:");
              console.log("  1. Install OpenClaw Unity Plugin package");
              console.log("  2. Configure Gateway URL: http://localhost:18789");
              console.log("  3. Enable plugin in Window > OpenClaw");
              console.log("  4. Check connection status\n");
              return;
            }
            
            for (const [id, session] of sessions) {
              const age = Math.round((Date.now() - session.registeredAt) / 1000);
              const lastSeen = Math.round((Date.now() - session.lastHeartbeat) / 1000);
              
              console.log(`  ✅ ${session.projectName}`);
              console.log(`     Version: Unity ${session.unityVersion}`);
              console.log(`     Platform: ${session.platform}`);
              console.log(`     Session: ${id}`);
              console.log(`     Connected: ${age}s ago`);
              console.log(`     Last seen: ${lastSeen}s ago`);
              console.log(`     Pending: ${session.pendingCommands.length} commands\n`);
            }
          });
      },
      { commands: ["unity"] }
    );
    
    logger.info("[Unity] Plugin loaded - HTTP endpoints at /unity/*");
  },
};

export default plugin;
