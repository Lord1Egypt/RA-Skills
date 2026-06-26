import type { OpenClawPluginApi } from "openclaw/plugin-sdk/memory-core-plus";
import type { MemoryCorePlusConfig } from "./config.js";
import { extractUserQuery, formatRelevantMemoriesContext } from "./safety.js";

export function createRecallHook(api: OpenClawPluginApi, cfg: MemoryCorePlusConfig) {
  return async (
    event: { prompt: string; messages: unknown[] },
    ctx: { agentId?: string; sessionKey?: string; trigger?: string },
  ) => {
    if (!event.prompt || event.prompt.length < cfg.autoRecallMinPromptLength) {
      api.logger.info(
        `memory-core-plus: recall skipped (prompt too short: ${event.prompt?.length ?? 0} < ${cfg.autoRecallMinPromptLength})`,
      );
      return;
    }

    if (ctx.trigger === "memory" || ctx.sessionKey?.includes(":memory-capture:")) {
      api.logger.info("memory-core-plus: recall skipped (inside memory-capture subagent, no recall needed)");
      return;
    }

    const agentId = ctx.agentId ?? "default";
    let manager;
    try {
      const result = await api.runtime.tools.getMemorySearchManager({
        cfg: api.config,
        agentId,
      });
      manager = result.manager;
      if (!manager) {
        if (result.error) {
          api.logger.warn(
            `memory-core-plus: recall skipped, search manager unavailable: ${result.error}`,
          );
        }
        return;
      }
    } catch (err) {
      api.logger.warn(`memory-core-plus: recall init failed: ${String(err)}`);
      return;
    }

    try {
      const searchQuery = extractUserQuery(event.prompt);
      const searchStart = Date.now();
      const results = await manager.search(searchQuery, {
        maxResults: cfg.autoRecallMaxResults,
        sessionKey: ctx.sessionKey,
      });
      const searchMs = Date.now() - searchStart;

      if (results.length === 0) {
        api.logger.info(
          `memory-core-plus: recall search returned 0 results (${searchMs}ms, query: "${truncate(searchQuery, 80)}")`,
        );
        return;
      }

      const summary = results.map((r) => `${r.path}(${(r.score * 100).toFixed(0)}%)`).join(", ");
      api.logger.info(
        `memory-core-plus: injecting ${results.length} memories into context (${searchMs}ms) [${summary}]`,
      );
      return {
        prependContext: formatRelevantMemoriesContext(results),
      };
    } catch (err) {
      api.logger.warn(`memory-core-plus: recall search failed: ${String(err)}`);
    }
  };
}

function truncate(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  return `${text.slice(0, maxLen)}…`;
}
