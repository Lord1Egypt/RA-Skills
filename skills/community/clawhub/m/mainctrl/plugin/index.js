import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { homedir } from "node:os";

const STATE_FILE = resolve(homedir(), ".openclaw/workspace/skills/mainctrl/scripts/state.json");

const DEFAULT_BLOCKED_TOOLS = ["write", "edit", "exec", "process", "apply_patch"];
const DEFAULT_CONTROLLED_AGENTS = ["main"];

const DEFAULT_EXEC_ALLOW_EXCEPT = {
  find:  ["-exec", "-ok", "-delete", "-fprint", "|", "$(", ">", ">>"],
  ls:    [">", ">>", "|"],
  pwd:   [">", ">>", "|"],
  sed:   [">", ">>", "|", ".java", ".py", ".js", ".html", ".css"],
  cat:   [">", ">>", "|"],
};

/**
 * Read current control state from the skill's state file.
 * Gracefully handles missing files and corrupted JSON by falling
 * back to safe defaults: enabled=false so all tools pass through
 * (blockedTools is populated but never reached — the enabled check
 *  short-circuits before any tool is inspected).
 */
function readState() {
  try {
    if (!existsSync(STATE_FILE)) {
      return {
        enabled: false,
        controlledAgents: DEFAULT_CONTROLLED_AGENTS,
        blockedTools: DEFAULT_BLOCKED_TOOLS,
        execAllowExcept: DEFAULT_EXEC_ALLOW_EXCEPT,
      };
    }
    const raw = readFileSync(STATE_FILE, "utf-8");
    const state = JSON.parse(raw);
    return {
      enabled: state.enabled !== false,
      controlledAgents: Array.isArray(state.controlledAgents) && state.controlledAgents.length > 0
        ? state.controlledAgents
        : DEFAULT_CONTROLLED_AGENTS,
      blockedTools: Array.isArray(state.blockedTools)
        ? state.blockedTools
        : DEFAULT_BLOCKED_TOOLS,
      execAllowExcept: state.execAllowExcept && typeof state.execAllowExcept === "object" && !Array.isArray(state.execAllowExcept)
        ? state.execAllowExcept
        : DEFAULT_EXEC_ALLOW_EXCEPT,
    };
  } catch {
    return {
      enabled: false,
      controlledAgents: DEFAULT_CONTROLLED_AGENTS,
      blockedTools: DEFAULT_BLOCKED_TOOLS,
      execAllowExcept: DEFAULT_EXEC_ALLOW_EXCEPT,
    };
  }
}

const plugin = {
  id: "mainctrl",
  name: "mainctrl",
  description: "Runtime tool-access guard for OpenClaw agents. Intercepts destructive tool calls (write, edit, exec, process, apply_patch) before they execute, redirecting controlled agents to delegate via sub-agents. Configured via a companion skill (mainctrl.sh) — no agent config changes needed, no restart required for toggles.",

  register(e) {
    e.on?.("before_tool_call", (event, ctx) => {
      const state = readState();

      // When the safety is off (enabled=false), allow everything
      if (!state.enabled) return;

      // Only intercept for controlled agents
      if (!state.controlledAgents.includes(ctx.agentId || "")) return;

      // exec allow-except: allow safe read-only commands with allow-except checks
      if (event.toolName === "exec" && state.blockedTools.includes("exec")) {
        const cmd = event.params?.command || "";
        const firstWord = cmd.trim().split(/\s/)[0];
        const allowExcept = state.execAllowExcept[firstWord];
        if (allowExcept) {
          // Command is allowlisted — check allow-except patterns
          const blocked = allowExcept.find(p => cmd.includes(p));
          if (blocked) {
            return {
              block: true,
              blockReason: `exec blocked: "${firstWord}" matched allow-except pattern "${blocked}". Delegate this work to a sub-agent instead.`,
            };
          }
          return; // allowed
        }
        // Not in allow-except map → falls through to generic block below
      }

      // Block if the requested tool is on the blocked list
      if (state.blockedTools.includes(event.toolName)) {
        return {
          block: true,
          blockReason: "Delegate this work to a sub-agent instead. Use sessions_spawn to dispatch to coder, tester, auditor, or publicist.",
        };
      }
    });
  },
};

export default plugin;
