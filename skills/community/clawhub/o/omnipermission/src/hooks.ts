import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { getSavedKey, getInterceptedTools } from "./storage.ts";
import { formatKey, requestMobileApproval } from "./utils.ts";

export const registerOmniHooks = (api: OpenClawPluginApi) => {
  api.on("before_tool_call", async (event) => {
    // 1. Blacklist Check
    const interceptedTools = await getInterceptedTools(api);
    if (!interceptedTools.includes(event.toolName)) {
      return;
    }

    // 2. Key Validation
    const rawKey = await getSavedKey(api);
    if (!rawKey) {
      api.logger.warn(`[omnipermission] 🛑 Action blocked: Public key is missing.`);
      return {
        block: true,
        blockReason: "Missing public key. Run: openclaw omnipermission set-key",
      };
    }

    const key = formatKey(rawKey);
    api.logger.info(`[omnipermission] 🎯 Intercepting tool: ${event.toolName}`);

    // 3. Hand off to Utils for API/Polling
    const result = await requestMobileApproval(api, event.toolName, key);

    if (!result.approved) {
      return {
        block: true,
        blockReason: result.reason || "Action rejected.",
      };
    }

    // If approved, we return nothing to let the tool execute
    return;
  });
};
