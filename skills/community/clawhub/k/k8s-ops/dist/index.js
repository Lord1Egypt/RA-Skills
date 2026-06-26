import { emptyPluginConfigSchema } from "openclaw/plugin-sdk";
import { Type } from "@sinclair/typebox";
import { skillRegistry } from "@k8s-ops/core";
const plugin = {
    id: "k8s",
    name: "Kubernetes",
    description: "Kubernetes operations plugin - 32 tools for K8s management",
    configSchema: emptyPluginConfigSchema(),
    register(api) {
        const pluginConfig = api.pluginConfig ?? undefined;
        for (const skill of skillRegistry) {
            api.registerTool({
                name: skill.name,
                label: skill.name,
                description: skill.description,
                parameters: Type.Any(),
                async execute(_toolCallId, params) {
                    const result = await skill.handler(params, pluginConfig);
                    const text = typeof result === "string" ? result : JSON.stringify(result, null, 2);
                    return {
                        content: [{ type: "text", text }],
                        details: result,
                    };
                },
            });
        }
        api.logger?.info?.(`K8s plugin loaded successfully - ${skillRegistry.length} skills registered`);
    },
};
export default plugin;
