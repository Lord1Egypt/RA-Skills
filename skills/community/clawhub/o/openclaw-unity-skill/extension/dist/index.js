// extension/index.ts
var sessions = /* @__PURE__ */ new Map();
function generateId() {
  return `unity_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}
function cleanupStaleSessions() {
  const now = Date.now();
  const staleThreshold = 12e4;
  for (const [id, session] of sessions) {
    if (now - session.lastHeartbeat > staleThreshold) {
      sessions.delete(id);
    }
  }
}
var ENGINE_LABEL = "Unity";
var ALLOW_DESTRUCTIVE_ENV_VARS = [
  "OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE",
  "OPENCLAW_UNITY_ALLOW_DESTRUCTIVE"
];
var READ_ONLY_VERB = /^(get|list|find|search|read|inspect|describe|query|exists|has|count|status|state|info|tree|hierarchy|screenshot|capture)/i;
var NON_MUTATING_TOOLS = /* @__PURE__ */ new Set([
  "debug.log",
  // writes one line to the Editor console
  "editor.focuswindow",
  // moves Editor UI focus
  "editor.listwindows",
  "scriptableobject.load"
  // loads an existing asset for inspection only
]);
var HIGH_RISK_NAME = /(execute|eval|delete|destroy|remove|install|uninstall|build|import|deploy|publish|reset|\brun\b)/i;
var BATCH_TOOLS = /* @__PURE__ */ new Set(["batch.execute"]);
var MAX_BATCH_DEPTH = 4;
function currentEnv() {
  return globalThis?.process?.env ?? {};
}
function isTruthyFlag(value) {
  if (value === true) return true;
  if (typeof value === "string") return /^(1|true|yes|on)$/i.test(value.trim());
  return false;
}
function batchCommands(parameters) {
  const commands = parameters?.commands ?? parameters?.calls;
  return Array.isArray(commands) ? commands : null;
}
function classifyTool(tool, parameters, depth = 0) {
  const name = typeof tool === "string" ? tool.trim() : "";
  if (!name) return "project-changing";
  const key = name.toLowerCase();
  if (BATCH_TOOLS.has(key)) {
    if (depth >= MAX_BATCH_DEPTH) return "project-changing";
    const commands = batchCommands(parameters);
    if (!commands || commands.length === 0) return "project-changing";
    for (const command of commands) {
      if (!command || typeof command !== "object") return "project-changing";
      const sub = classifyTool(
        command.tool,
        command.params ?? command.parameters,
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
function projectChangingTools(tool, parameters, depth = 0) {
  const name = typeof tool === "string" && tool.trim() ? tool.trim() : "(unnamed tool)";
  const key = name.toLowerCase();
  if (BATCH_TOOLS.has(key) && depth < MAX_BATCH_DEPTH) {
    const commands = batchCommands(parameters);
    if (!commands || commands.length === 0) return [name];
    const found = [];
    for (const command of commands) {
      if (!command || typeof command !== "object") {
        found.push(`${name} (malformed command)`);
        continue;
      }
      found.push(
        ...projectChangingTools(
          command.tool,
          command.params ?? command.parameters,
          depth + 1
        )
      );
    }
    return found;
  }
  return classifyTool(name, parameters, depth) === "project-changing" ? [name] : [];
}
function destructiveOperationsEnabled(env = currentEnv()) {
  return ALLOW_DESTRUCTIVE_ENV_VARS.some((name) => isTruthyFlag(env[name]));
}
function evaluateDestructiveGate(input) {
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
      message: `Refused: ${listed} would change this ${ENGINE_LABEL} project, and this gateway was not started with project-changing operations enabled. Ask the user to confirm the change, restart the gateway with ${ALLOW_DESTRUCTIVE_ENV_VARS[0]}=1 (or ${ALLOW_DESTRUCTIVE_ENV_VARS[1]}=1), then repeat the call with confirm: true. Read-only tools are unaffected; pass dryRun: true to preview a call without sending it.`
    };
  }
  if (!isTruthyFlag(input.confirm)) {
    return {
      allowed: false,
      risk,
      tools,
      reason: "confirmation-missing",
      message: `Refused: ${listed} would change this ${ENGINE_LABEL} project. Confirm the change with the user, then repeat this call with confirm: true. Pass dryRun: true to preview it first.`
    };
  }
  return { allowed: true, risk, tools, reason: "confirmed" };
}
async function readJsonBody(req, maxBytes = 1024 * 1024) {
  const chunks = [];
  let total = 0;
  return new Promise((resolve, reject) => {
    req.on("data", (chunk) => {
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
        const repaired = raw.replace(/(:\s*-?\d+),(\d+\s*[,}\]])/g, "$1.$2");
        if (repaired !== raw) {
          try {
            resolve(JSON.parse(repaired));
            return;
          } catch {
          }
        }
        reject(err);
      }
    });
    req.on("error", reject);
  });
}
function sendJson(res, status, data) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.end(JSON.stringify(data));
}
async function handleUnityHttpRequest(req, res) {
  const url = new URL(req.url ?? "/", "http://localhost");
  const path = url.pathname;
  if (!path.startsWith("/unity/")) {
    return false;
  }
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
        const session = {
          sessionId,
          registeredAt: Date.now(),
          lastHeartbeat: Date.now(),
          projectName: project || "Unknown",
          unityVersion: version || "Unknown",
          platform: platform || "UnityEditor",
          toolCount: tools || 0,
          pendingCommands: [],
          results: /* @__PURE__ */ new Map()
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
        if (session.pendingCommands.length > 0) {
          const command = session.pendingCommands.shift();
          sendJson(res, 200, command);
        } else {
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
        const activeSessions = Array.from(sessions.values()).map((s) => ({
          sessionId: s.sessionId,
          project: s.projectName,
          version: s.unityVersion,
          platform: s.platform,
          connectedAt: new Date(s.registeredAt).toISOString(),
          lastSeen: new Date(s.lastHeartbeat).toISOString(),
          pendingCommands: s.pendingCommands.length
        }));
        sendJson(res, 200, {
          enabled: true,
          destructiveOperations: destructiveOperationsEnabled() ? "enabled" : "blocked",
          sessions: activeSessions,
          sessionCount: activeSessions.length
        });
        return true;
      }
      default:
        sendJson(res, 404, { error: "Unknown endpoint" });
        return true;
    }
  } catch (err) {
    console.error("[Unity] HTTP error:", err);
    sendJson(res, 500, { error: err.message });
    return true;
  }
}
var plugin = {
  id: "unity",
  name: "Unity Plugin",
  description: "Connect Unity Editor to OpenClaw AI assistant",
  register(api) {
    const logger = api.logger;
    setInterval(cleanupStaleSessions, 3e4);
    const httpApi = api;
    if (typeof httpApi.registerHttpRoute === "function") {
      httpApi.registerHttpRoute({
        path: "/unity",
        auth: "plugin",
        match: "prefix",
        handler: handleUnityHttpRequest
      });
    } else {
      httpApi.registerHttpHandler(handleUnityHttpRequest);
    }
    api.registerTool({
      name: "unity_execute",
      description: "Execute a tool in the connected Unity Editor. Available tools: console.getLogs, scene.getData, gameobject.find, gameobject.create, gameobject.delete, gameobject.setActive, transform.setPosition, transform.setRotation, transform.setScale, component.get, component.add, debug.hierarchy, debug.screenshot, app.getState, app.play, app.stop, input.simulateKey, input.simulateMouse, and more. Read-only tools (get*/list/find/read/debug.hierarchy/debug.screenshot) run directly. Project-changing tools are refused unless the gateway was started with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 and the call passes confirm: true after the user approved the change; dryRun: true previews any call without sending it.",
      parameters: {
        type: "object",
        properties: {
          tool: { type: "string", description: "The Unity tool to execute (e.g., 'debug.hierarchy', 'gameobject.find')" },
          parameters: { type: "object", description: "Parameters for the tool (varies by tool)" },
          sessionId: { type: "string", description: "Optional: specific Unity session ID" },
          confirm: {
            type: "boolean",
            description: "Required for project-changing tools (create/delete/save/set*, package.add, script.execute, input.*, editor.play). Set it only after the user has approved that specific change. Read-only tools ignore it."
          },
          dryRun: {
            type: "boolean",
            description: "Preview only: report how the call is classified and what would be sent to the Editor, without sending it."
          }
        },
        required: ["tool"]
      },
      execute: async (toolCallId, args) => {
        const jsonResult = (payload) => ({
          content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
          details: payload
        });
        const tool = args?.tool;
        const parameters = args?.parameters;
        const sessionId = args?.sessionId;
        if (!tool) {
          return jsonResult({
            success: false,
            error: "Missing 'tool' parameter. Specify which Unity tool to execute (e.g., 'debug.hierarchy', 'gameobject.find')."
          });
        }
        const gate = evaluateDestructiveGate({
          tool,
          parameters,
          confirm: args?.confirm
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
            gate: { reason: gate.reason, message: gate.message }
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
              tools: gate.tools
            }
          });
        }
        let session;
        if (sessionId) {
          session = sessions.get(sessionId);
        } else {
          const firstSession = sessions.values().next();
          session = firstSession.done ? void 0 : firstSession.value;
        }
        if (!session) {
          return jsonResult({
            success: false,
            error: "No Unity session connected. Make sure Unity Editor is running with OpenClaw plugin enabled."
          });
        }
        const requestId = generateId();
        session.pendingCommands.push({
          toolCallId: requestId,
          tool,
          arguments: parameters || {},
          createdAt: Date.now()
        });
        logger.info(`[Unity] Queued command: ${tool} (request: ${requestId})`);
        const timeout = 6e4;
        const startTime = Date.now();
        while (Date.now() - startTime < timeout) {
          if (session.results.has(requestId)) {
            const result = session.results.get(requestId);
            session.results.delete(requestId);
            return jsonResult({
              success: true,
              result
            });
          }
          await new Promise((resolve) => setTimeout(resolve, 100));
        }
        return jsonResult({
          success: false,
          error: "Timeout waiting for Unity response. Make sure the OpenClaw plugin is enabled in Unity Editor."
        });
      }
    });
    api.registerTool({
      name: "unity_sessions",
      description: "List all connected Unity Editor sessions",
      parameters: {
        type: "object",
        properties: {
          _dummy: { type: "string", description: "Unused parameter" }
        },
        required: []
      },
      execute: async (_toolCallId, _args) => {
        const activeSessions = Array.from(sessions.values()).map((s) => ({
          sessionId: s.sessionId,
          project: s.projectName,
          version: s.unityVersion,
          platform: s.platform,
          tools: s.toolCount
        }));
        const payload = {
          success: true,
          sessions: activeSessions,
          count: activeSessions.length
        };
        return {
          content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
          details: payload
        };
      }
    });
    api.registerCli(
      ({ program }) => {
        const unityCmd = program.command("unity").description("Unity Plugin commands");
        unityCmd.command("status").description("Show Unity connection status").action(() => {
          console.log("\n\u{1F3AE} Unity Plugin Status\n");
          console.log(
            destructiveOperationsEnabled() ? "  Project-changing tools: ENABLED (confirm: true still required per call)\n" : "  Project-changing tools: BLOCKED (start the gateway with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 to enable)\n"
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
            const age = Math.round((Date.now() - session.registeredAt) / 1e3);
            const lastSeen = Math.round((Date.now() - session.lastHeartbeat) / 1e3);
            console.log(`  \u2705 ${session.projectName}`);
            console.log(`     Version: Unity ${session.unityVersion}`);
            console.log(`     Platform: ${session.platform}`);
            console.log(`     Session: ${id}`);
            console.log(`     Connected: ${age}s ago`);
            console.log(`     Last seen: ${lastSeen}s ago`);
            console.log(`     Pending: ${session.pendingCommands.length} commands
`);
          }
        });
      },
      { commands: ["unity"] }
    );
    logger.info("[Unity] Plugin loaded - HTTP endpoints at /unity/*");
  }
};
var extension_default = plugin;
export {
  classifyTool,
  extension_default as default,
  destructiveOperationsEnabled,
  evaluateDestructiveGate,
  projectChangingTools
};
