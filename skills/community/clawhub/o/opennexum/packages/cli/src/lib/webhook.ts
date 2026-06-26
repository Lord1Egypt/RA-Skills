import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";

import { loadConfig, type NexumConfig } from "@nexum/core";

const DEFAULT_WEBHOOK_GATEWAY_URL = "http://127.0.0.1:18789";
const WEBHOOK_AGENT_PATH = "hooks/agent";

export async function resolveWebhookToken(
  config: Pick<NexumConfig, "webhook">
): Promise<string | undefined> {
  const envToken = process.env.OPENCLAW_HOOKS_TOKEN?.trim();
  if (envToken) {
    return envToken;
  }

  const configToken = config.webhook?.token?.trim();
  if (configToken) {
    return configToken;
  }

  return readOpenClawHooksToken();
}

export function resolveWebhookAgentEndpoint(
  config: Pick<NexumConfig, "webhook">
): string {
  return new URL(
    WEBHOOK_AGENT_PATH,
    withTrailingSlash(config.webhook?.gatewayUrl?.trim() || DEFAULT_WEBHOOK_GATEWAY_URL)
  ).toString();
}

export function summarizeResponse(body: string): string {
  const normalized = body.trim().replace(/\s+/g, " ");
  if (!normalized) {
    return "";
  }

  return normalized.length > 200 ? `${normalized.slice(0, 197)}...` : normalized;
}

export async function dispatchAgentWebhook(
  taskId: string,
  role: "generator" | "evaluator",
  projectDir: string,
  sessionName: string
): Promise<boolean> {
  return postWebhookMessage({
    projectDir,
    message: `nexum-dispatch: ${taskId} ${role} ${projectDir}`,
    sessionName,
    source: "callback"
  });
}

export async function postWebhookMessage(options: {
  projectDir: string;
  message: string;
  sessionName?: string;
  source: "callback" | "health" | "watch";
}): Promise<boolean> {
  try {
    const config = await loadConfig(options.projectDir).catch(
      () => ({ webhook: undefined } as NexumConfig)
    );
    const token = await resolveWebhookToken(config);

    if (!token) {
      console.warn(`[${options.source}] webhook skipped for ${options.projectDir}: no hooks token configured`);
      return false;
    }

    const endpoint = resolveWebhookAgentEndpoint(config);
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: options.message,
        name: "OpenNexum",
        agentId: config.webhook?.agentId?.trim() || "orchestrator",
        deliver: false,
        ...(options.sessionName ? { sessionName: options.sessionName } : {})
      })
    });

    if (!response.ok) {
      const details = summarizeResponse(await response.text().catch(() => ""));
      console.warn(
        `[${options.source}] webhook failed for ${options.projectDir}: ${response.status} ${response.statusText}${details ? ` - ${details}` : ""}`
      );
      return false;
    }

    return true;
  } catch (error) {
    console.warn(
      `[${options.source}] webhook failed for ${options.projectDir}: ${error instanceof Error ? error.message : error}`
    );
    return false;
  }
}

async function readOpenClawHooksToken(): Promise<string | undefined> {
  const openClawConfigPath = path.join(homedir(), ".openclaw", "openclaw.json");

  try {
    const contents = await readFile(openClawConfigPath, "utf8");
    const parsed = JSON.parse(contents) as { hooks?: { token?: unknown } };
    const token = parsed.hooks?.token;
    return typeof token === "string" && token.trim() ? token.trim() : undefined;
  } catch {
    return undefined;
  }
}

function withTrailingSlash(url: string): string {
  return url.endsWith("/") ? url : `${url}/`;
}
