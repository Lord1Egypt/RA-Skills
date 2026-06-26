import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import { homedir } from "os";
import { join } from "path";
import { loadState, detectAndCountSession, saveState } from "./src/state.js";
import { isLocked } from "./src/lock.js";
import { shouldTrigger, hoursUntilNextTrigger, mergeConfig } from "./src/scheduler.js";
import { consolidate } from "./src/consolidate.js";
import { captureFromTurn } from "./src/capture.js";

/** Stable per-agent state dir derived from agentId or a fallback */
function resolveStateDir(agentId?: string): string {
  const id = agentId ?? "main";
  return join(homedir(), ".openclaw", "memory-dream", id);
}

export default definePluginEntry({
  id: "memory-dream",
  name: "Memory Dream",
  description:
    "Auto-consolidates agent memory files after sessions — like REM sleep for AI agents",

  register(api: OpenClawPluginApi) {
    const pluginCfg = (api.pluginConfig ?? {}) as Record<string, unknown>;
    const cfg = mergeConfig(pluginCfg);

    // ── Hook: before each agent turn — time-based trigger check ────────────
    // session_start/session_end are gated on isNewSession which never fires in
    // persistent DM contexts. before_agent_start fires every turn; we check
    // whether enough time has passed since last consolidation and fire if so.
    api.on("before_agent_start", async (_event, ctx) => {
      if (!cfg.enabled) return;

      const agentId = (ctx as { agentId?: string }).agentId;
      const stateDir = resolveStateDir(agentId);

      try {
        // Detect session boundary (gap > 30 min = new session) and update counter
        const { state, newSessionDetected } = await detectAndCountSession(stateDir, 30);

        if (newSessionDetected) {
          api.logger.info(
            `[memory-dream] New session detected. Sessions since last consolidation: ${state.sessionCount}`
          );
        }

        // Surface last consolidation status in logs
        if (state.lastRunStatus === "success" && state.lastRunSummary) {
          const lastRun = state.lastRunAt
            ? new Date(state.lastRunAt).toLocaleString()
            : "unknown";
          api.logger.info(
            `[memory-dream] Last consolidation: ${lastRun} — ${state.lastRunSummary}`
          );
        } else if (state.lastRunStatus === "running") {
          const locked = await isLocked(stateDir);
          if (!locked) {
            api.logger.warn(
              "[memory-dream] Last consolidation interrupted (status=running, no lock) — marking failed"
            );
            await saveState(stateDir, { ...state, lastRunStatus: "failed" });
          }
        }

        // Capture phase: scan the last exchange for memory-worthy signals
        if (cfg.enableCapture) {
          const rawCtx = ctx as Record<string, unknown>;
          const lastUser = rawCtx.lastUserMessage ?? rawCtx.userMessage ?? rawCtx.message;
          const lastAssistant = rawCtx.lastAssistantMessage ?? rawCtx.assistantMessage;
          if (lastUser || lastAssistant) {
            const conversationText = [
              lastUser ? `User: ${String(lastUser)}` : null,
              lastAssistant ? `Assistant: ${String(lastAssistant)}` : null,
            ]
              .filter(Boolean)
              .join("\n");

            const workspaceDir = api.runtime.agent.resolveAgentWorkspaceDir(
              api.config,
              agentId ?? "main"
            );

            captureFromTurn(stateDir, workspaceDir, conversationText, cfg, api, agentId ?? "main").catch(
              (err: unknown) => {
                api.logger.warn(`[memory-dream] Capture error (non-blocking): ${String(err)}`);
              }
            );
          }
        }

        // Check trigger: N sessions AND 24h since last run
        const trigger = await shouldTrigger(state, cfg, stateDir);
        if (trigger) {
          api.logger.info(
            `[memory-dream] Trigger conditions met (${state.sessionCount} sessions, 24h elapsed) — starting background consolidation`
          );

          const workspaceDir = api.runtime.agent.resolveAgentWorkspaceDir(
            api.config,
            agentId ?? "main"
          );

          consolidate(stateDir, workspaceDir, cfg, api, agentId ?? "main").catch((err: unknown) => {
            api.logger.error(
              `[memory-dream] Background consolidation error: ${String(err)}`
            );
          });
        }
      } catch (err) {
        api.logger.error(`[memory-dream] before_agent_start error: ${String(err)}`);
      }
    });

    // ── Tool: memory_dream_status ──────────────────────────────────────────
    api.registerTool((ctx) => ({
      name: "memory_dream_status",
      label: "Memory Dream Status",
      description:
        "Returns the current memory-dream plugin state: session count since last consolidation, time since last run, next trigger estimate, and whether consolidation is currently running.",
      parameters: {
        type: "object" as const,
        properties: {},
        additionalProperties: false,
      } as const,
      async execute(_toolCallId, _params) {
        const stateDir = resolveStateDir(ctx.agentId);
        const state = await loadState(stateDir);
        const locked = await isLocked(stateDir);
        const hoursLeft = hoursUntilNextTrigger(state, cfg);

        const lastRunAt = state.lastRunAt
          ? new Date(state.lastRunAt).toLocaleString()
          : "never";

        const hoursSinceRun = state.lastRunAt
          ? (
              (Date.now() - new Date(state.lastRunAt).getTime()) /
              (1000 * 60 * 60)
            ).toFixed(1)
          : null;

        const sessionsNeeded = Math.max(0, cfg.minSessions - state.sessionCount);

        let nextTrigger: string;
        if (!cfg.enabled) {
          nextTrigger = "disabled";
        } else if (locked) {
          nextTrigger = "running now";
        } else if (sessionsNeeded > 0) {
          nextTrigger = `${sessionsNeeded} more session(s) needed`;
        } else if (hoursLeft !== null && hoursLeft > 0) {
          nextTrigger = `in ~${hoursLeft.toFixed(1)}h (time condition not met)`;
        } else {
          nextTrigger = "ready (will trigger on next session end)";
        }

        const details = {
          sessionCount: state.sessionCount,
          minSessions: cfg.minSessions,
          lastRunAt,
          hoursSinceLastRun: hoursSinceRun ? `${hoursSinceRun}h` : null,
          minHours: cfg.minHours,
          lastRunStatus: state.lastRunStatus,
          lastRunSummary: state.lastRunSummary,
          consolidationRunning: locked,
          nextTrigger,
          memoryFiles: cfg.memoryFiles,
          enabled: cfg.enabled,
        };

        return {
          content: [{ type: "text" as const, text: JSON.stringify(details, null, 2) }],
          details,
        };
      },
    }));
  },
});
