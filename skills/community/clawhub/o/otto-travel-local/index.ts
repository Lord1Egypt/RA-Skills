/**
 * OpenClaw plugin for Otto Travel.
 *
 * Connects to Otto's MCP endpoint via Streamable HTTP, discovers tools
 * dynamically, and registers each as a native OpenClaw agent tool.
 * Authenticates via OAuth 2.1 Device Authorization Grant (RFC 8628).
 */

import { OttoAuth } from "./src/auth.js";
import { OttoMcpClient } from "./src/mcp-client.js";

const DEFAULT_SERVER_URL = "https://api.ottotheagent.com/mcp";

export default function register(api: any) {
  const config = (api.pluginConfig ?? {}) as { serverUrl?: string };
  const serverUrl = config.serverUrl?.trim() || DEFAULT_SERVER_URL;

  const auth = new OttoAuth(serverUrl, api.logger);
  const mcp = new OttoMcpClient(serverUrl, auth, api.logger);

  api.registerService({
    id: "openclaw-otto-travel",

    async start() {
      try {
        api.logger.info(`[otto] Connecting to ${serverUrl}...`);
        await mcp.connect();

        const tools = await mcp.listTools();
        api.logger.info(`[otto] Discovered ${tools.length} tools`);

        for (const tool of tools) {
          api.registerTool({
            name: tool.name,
            description: tool.description ?? `Otto Travel tool: ${tool.name}`,
            parameters: tool.inputSchema ?? { type: "object", properties: {} },
            async execute(_id: string, params: unknown) {
              const result = await mcp.callTool(tool.name, params as Record<string, unknown>);
              const content = result.content as Array<{ text?: string; data?: string }> | undefined;
              const text = content?.map((c) => c.text ?? c.data ?? "").join("\n") ?? "";
              return {
                content: [{ type: "text", text }],
                isError: result.isError,
              };
            },
          });
          api.logger.info(`[otto] Registered tool: ${tool.name}`);
        }
      } catch (err) {
        api.logger.error("[otto] Failed to connect:", err);
      }
    },

    async stop() {
      api.logger.info("[otto] Disconnecting...");
      await mcp.disconnect();
    },
  });

  api.logger.info("[otto] Plugin registered");
}
