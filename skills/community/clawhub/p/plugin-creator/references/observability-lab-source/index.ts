import { definePluginEntry, type OpenClawPluginApi } from "./api.js";
import {
  runObserveCommand,
  runObserveHelpCommand,
  runObserveTailCommand,
} from "./commands/observe.js";
import { registerObservabilityHooks } from "./hooks/telemetry.js";
import { OBSERVABILITY_LAB_PLUGIN_ID } from "./src/observability.js";
import { createObserveDemoEchoTool } from "./tools/observe-demo-echo.js";

function registerCommands(api: OpenClawPluginApi): void {
  // 把 slash 命令注册集中到这里，后续新增命令模块时只需要做一次装配。
  api.registerCommand({
    name: "observe",
    description: "Enable, disable, or inspect Observability Lab telemetry.",
    acceptsArgs: true,
    handler: async (ctx) => runObserveCommand(api, ctx),
  });

  api.registerCommand({
    name: "observe_help",
    description: "Explain what this plugin observes and how to verify it.",
    handler: async () => runObserveHelpCommand(),
  });

  api.registerCommand({
    name: "observe_tail",
    description: "Show the latest telemetry events recorded by the plugin.",
    handler: async () => runObserveTailCommand(api),
  });
}

export default definePluginEntry({
  id: OBSERVABILITY_LAB_PLUGIN_ID,
  name: "Observability Lab",
  description: "Experimental native plugin for skills, hooks, and slash commands",
  register(api: OpenClawPluginApi) {
    // tool、command、hook 分目录放置，这样这个插件本身就可以作为后续开发脚手架。
    api.registerTool(createObserveDemoEchoTool());
    registerCommands(api);
    registerObservabilityHooks(api);
  },
});
