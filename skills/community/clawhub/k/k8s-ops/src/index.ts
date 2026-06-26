import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { emptyPluginConfigSchema } from "openclaw/plugin-sdk";
import { Type } from "@sinclair/typebox";
import { skillRegistry, type PluginConfig } from "@k8s-ops/core";

const plugin = {
  id: "k8s",
  name: "Kubernetes",
  description: "Kubernetes operations plugin - 32 tools for K8s management",
  configSchema: emptyPluginConfigSchema(),

  register(api: OpenClawPluginApi) {
    const pluginConfig: PluginConfig | undefined = (api as any).pluginConfig ?? undefined;

    for (const skill of skillRegistry) {
      api.registerTool({
        name: skill.name,
        label: skill.name,
        description: skill.description,
        parameters: Type.Any(),
        async execute(_toolCallId: string, params: unknown) {
          const result = await skill.handler(params, pluginConfig);
          const text = typeof result === "string" ? result : JSON.stringify(result, null, 2);
          return {
            content: [{ type: "text" as const, text }],
            details: result,
          };
        },
      });
    }

    api.logger?.info?.(`K8s plugin loaded successfully - ${skillRegistry.length} skills registered`);
  },
};

export default plugin;
