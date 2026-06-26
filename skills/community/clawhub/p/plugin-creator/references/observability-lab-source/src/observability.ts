import fs from "node:fs/promises";
import path from "node:path";
import type { OpenClawConfig } from "../api.js";

export const OBSERVABILITY_LAB_PLUGIN_ID = "observability-lab";
export const DEFAULT_TRANSCRIPT_PREFIX = "[obs] ";
export const OBSERVABILITY_LAB_MESSAGE_MARKER = "【可观测实验室】";

export type ObservabilityLabConfig = {
  captureEnabled: boolean;
  rewriteEnabled: boolean;
  transcriptPrefix: string;
};

export type TelemetryEventRecord = {
  type:
    | "session_start"
    | "message_received"
    | "llm_input"
    | "llm_output"
    | "before_tool_call"
    | "after_tool_call"
    | "before_message_write"
    | "session_end";
  at: string;
  event: Record<string, unknown>;
  context: Record<string, unknown>;
};

const activeSessionKeys = new Set<string>();
const activeConversationKeys = new Set<string>();

export function readObservabilityLabConfig(config: OpenClawConfig): ObservabilityLabConfig {
  const raw = config.plugins?.entries?.[OBSERVABILITY_LAB_PLUGIN_ID]?.config;
  const captureEnabled = raw?.captureEnabled === true;
  const rewriteEnabled = raw?.rewriteEnabled === true;
  const transcriptPrefix =
    typeof raw?.transcriptPrefix === "string" && raw.transcriptPrefix.length > 0
      ? raw.transcriptPrefix
      : DEFAULT_TRANSCRIPT_PREFIX;
  return { captureEnabled, rewriteEnabled, transcriptPrefix };
}

export function activateSessionCapture(sessionKey: string | undefined): boolean {
  const normalized = sessionKey?.trim();
  if (!normalized) {
    return false;
  }
  activeSessionKeys.add(normalized);
  return true;
}

function buildConversationCaptureKey(params: {
  channelId?: string;
  accountId?: string;
  conversationId?: string;
}): string {
  const channelId = params.channelId?.trim() || "";
  const accountId = params.accountId?.trim() || "";
  const conversationId = params.conversationId?.trim() || "";
  return [channelId, accountId, conversationId].join("::");
}

export function activateConversationCapture(params: {
  channelId?: string;
  accountId?: string;
  conversationId?: string;
}): boolean {
  const key = buildConversationCaptureKey(params);
  if (!key.replaceAll(":", "")) {
    return false;
  }
  activeConversationKeys.add(key);
  return true;
}

export function deactivateConversationCapture(params: {
  channelId?: string;
  accountId?: string;
  conversationId?: string;
}): boolean {
  const key = buildConversationCaptureKey(params);
  if (!key.replaceAll(":", "")) {
    return false;
  }
  return activeConversationKeys.delete(key);
}

export function isConversationCaptureActive(params: {
  channelId?: string;
  accountId?: string;
  conversationId?: string;
}): boolean {
  const key = buildConversationCaptureKey(params);
  if (!key.replaceAll(":", "")) {
    return false;
  }
  return activeConversationKeys.has(key);
}

export function deactivateSessionCapture(sessionKey: string | undefined): boolean {
  const normalized = sessionKey?.trim();
  if (!normalized) {
    return false;
  }
  return activeSessionKeys.delete(normalized);
}

export function isSessionCaptureActive(sessionKey: string | undefined): boolean {
  const normalized = sessionKey?.trim();
  if (!normalized) {
    return false;
  }
  return activeSessionKeys.has(normalized);
}

export function resetObservabilityLabRuntimeState(): void {
  activeSessionKeys.clear();
  activeConversationKeys.clear();
}

export function updateObservabilityLabConfig(
  config: OpenClawConfig,
  nextConfig: Partial<ObservabilityLabConfig>,
): OpenClawConfig {
  const current = readObservabilityLabConfig(config);
  const merged: Record<string, unknown> = {
    captureEnabled: nextConfig.captureEnabled ?? current.captureEnabled,
    rewriteEnabled: nextConfig.rewriteEnabled ?? current.rewriteEnabled,
    transcriptPrefix: nextConfig.transcriptPrefix ?? current.transcriptPrefix,
  };
  return {
    ...config,
    plugins: {
      ...config.plugins,
      entries: {
        ...config.plugins?.entries,
        [OBSERVABILITY_LAB_PLUGIN_ID]: {
          ...config.plugins?.entries?.[OBSERVABILITY_LAB_PLUGIN_ID],
          enabled: true,
          config: merged,
        },
      },
    },
  };
}

export function resolveObservabilityLabDir(stateDir: string): string {
  return path.join(stateDir, "plugins", OBSERVABILITY_LAB_PLUGIN_ID);
}

export function resolveTelemetryLogPath(stateDir: string): string {
  return path.join(resolveObservabilityLabDir(stateDir), "telemetry.jsonl");
}

type TelemetryQueue = {
  pendingLines: string[];
  flushPromise: Promise<void> | null;
};

const telemetryQueues = new Map<string, TelemetryQueue>();

function getTelemetryQueue(logPath: string): TelemetryQueue {
  let queue = telemetryQueues.get(logPath);
  if (!queue) {
    queue = {
      pendingLines: [],
      flushPromise: null,
    };
    telemetryQueues.set(logPath, queue);
  }
  return queue;
}

function startTelemetryFlush(logPath: string, queue: TelemetryQueue): void {
  if (queue.flushPromise) {
    return;
  }
  queue.flushPromise = Promise.resolve()
    .then(async () => {
      await fs.mkdir(path.dirname(logPath), { recursive: true });
      // Drain in batches so a burst of hook events still collapses into a small number of writes.
      while (queue.pendingLines.length > 0) {
        const lines = queue.pendingLines.splice(0, queue.pendingLines.length);
        await fs.appendFile(logPath, lines.join(""), "utf8");
      }
    })
    .finally(() => {
      queue.flushPromise = null;
      if (queue.pendingLines.length > 0) {
        startTelemetryFlush(logPath, queue);
        return;
      }
      if (telemetryQueues.get(logPath) === queue) {
        telemetryQueues.delete(logPath);
      }
    });
}

export function enqueueTelemetryEvent(params: {
  stateDir: string;
  record: TelemetryEventRecord;
}): void {
  const logPath = resolveTelemetryLogPath(params.stateDir);
  const queue = getTelemetryQueue(logPath);
  queue.pendingLines.push(`${JSON.stringify(params.record)}\n`);
  // Writing is intentionally decoupled from hooks so capture stays cheap on the hot path.
  startTelemetryFlush(logPath, queue);
}

export async function flushTelemetryEvents(params: { stateDir: string }): Promise<void> {
  const logPath = resolveTelemetryLogPath(params.stateDir);
  const queue = telemetryQueues.get(logPath);
  if (!queue) {
    return;
  }
  startTelemetryFlush(logPath, queue);
  while (queue.flushPromise) {
    await queue.flushPromise;
  }
}

export async function readTelemetryTail(params: {
  stateDir: string;
  limit: number;
}): Promise<TelemetryEventRecord[]> {
  const logPath = resolveTelemetryLogPath(params.stateDir);
  // Tail is used for operator-facing inspection, so prefer freshness over avoiding one flush.
  await flushTelemetryEvents({ stateDir: params.stateDir });
  let content = "";
  try {
    content = await fs.readFile(logPath, "utf8");
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === "ENOENT") {
      return [];
    }
    throw error;
  }
  return content
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(-Math.max(1, params.limit))
    .map((line) => JSON.parse(line) as TelemetryEventRecord);
}
