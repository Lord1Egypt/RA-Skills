import type { OpenClawPluginApi } from "openclaw/plugin-sdk/memory-core-plus";
import { createCaptureHook } from "./capture.js";
import { memoryCoreConfigSchema, parseConfig } from "./config.js";
import { createRecallHook } from "./recall.js";

const memoryCorePlusPlugin = {
  id: "memory-core-plus",
  name: "Memory Core Plus",
  description: "Enhanced workspace memory with auto-recall and auto-capture",
  kind: "memory" as const,
  configSchema: memoryCoreConfigSchema,

  register(api: OpenClawPluginApi) {
    // ── Inherit memory-core tool registration ──
    api.registerTool(
      (ctx) => {
        const memorySearchTool = api.runtime.tools.createMemorySearchTool({
          config: ctx.config,
          agentSessionKey: ctx.sessionKey,
        });
        const memoryGetTool = api.runtime.tools.createMemoryGetTool({
          config: ctx.config,
          agentSessionKey: ctx.sessionKey,
        });
        if (!memorySearchTool || !memoryGetTool) {
          return null;
        }
        return [memorySearchTool, memoryGetTool];
      },
      { names: ["memory_search", "memory_get"] },
    );

    api.registerCli(
      ({ program }) => {
        api.runtime.tools.registerMemoryCli(program);
      },
      { commands: ["memory"] },
    );

    // ── Auto-Recall + Auto-Capture hooks ──
    const cfg = parseConfig(api.pluginConfig);

    if (cfg.autoRecall) {
      api.on("before_prompt_build", createRecallHook(api, cfg));
    }

    if (cfg.autoCapture) {
      api.on("agent_end", createCaptureHook(api, cfg));
    }

    const hooks = [cfg.autoRecall && "auto-recall", cfg.autoCapture && "auto-capture"].filter(
      Boolean,
    );
    if (hooks.length > 0) {
      api.logger.info(`memory-core-plus: registered hooks: ${hooks.join(", ")}`);
    } else {
      api.logger.info(
        "memory-core-plus: no hooks registered (autoRecall and autoCapture both disabled)",
      );
    }
  },
};

export default memoryCorePlusPlugin;
