import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { getMode } from "./storage.ts";

/**
 * Formats the public key for headers/body
 */
export function formatKey(rawKey: string): string {
  return rawKey.replace(/\r?\n/g, "\\n");
}

/**
 * Gets the correct backend URL based on stored mode
 */
export async function getOmniBackendUrl(api: OpenClawPluginApi): Promise<string> {
  const mode = await getMode(api);
  return mode === "dev"
    ? "https://backend.dev.ecrop.de/ecrop-command/omnipermission/poas"
    : "https://backend.ecrop.de/ecrop-command/omnipermission/poas";
}

/**
 * Handles the POA creation and the polling loop until approved or rejected.
 */
export async function requestMobileApproval(
  api: OpenClawPluginApi,
  toolName: string,
  key: string
): Promise<{ approved: boolean; reason?: string }> {
  const baseUrl = await getOmniBackendUrl(api);
  const headers = {
    "Content-Type": "application/json",
    "X-OmniPermission-Secret-Key": key,
  };

  const requestBody = {
    contentToApprove: `OpenClaw wants to use this tool: ${toolName}. Do you approve this?`,
    extraData: `UNKNOWN`,
  };

  try {
    const response = await fetch(baseUrl, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(requestBody),
    });

    if (response.status !== 201) {
      const errorText = await response.text();
      api.logger.error(`[omnipermission] ❌ API Error (${response.status}): ${errorText}`);
      return { approved: false, reason: `POA creation failed (Status ${response.status})` };
    }

    const { id: poaId } = await response.json();
    api.logger.info(`[omnipermission] ✅ POA created (ID: ${poaId}). Waiting for OmniPersona approval...`);

    // Polling Loop
    while (true) {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const pollResponse = await fetch(`${baseUrl}/${poaId}`, {
        method: "GET",
        headers: headers,
      });

      if (!pollResponse.ok) continue;

      const pollData = await pollResponse.json();

      if (pollData.status === "APPROVED") {
        api.logger.info(`[omnipermission] 👍 Approved: ${toolName}`);
        return { approved: true };
      }

      if (pollData.status === "REJECTED") {
        api.logger.warn(`[omnipermission] 🛑 Rejected by user via OmniPersona.`);
        return { approved: false, reason: "User rejected the action on OmniPersona." };
      }
    }
  } catch (error) {
    api.logger.error(`[omnipermission] ❌ Network error: ${error}`);
    return { approved: false, reason: "OmniPermission backend unreachable." };
  }
}
