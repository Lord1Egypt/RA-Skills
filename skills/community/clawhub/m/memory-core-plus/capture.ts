import { randomUUID } from "node:crypto";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/memory-core-plus";
import type { MemoryCorePlusConfig } from "./config.js";
import { extractMessagesOfRole, isCapturableMessage, stripRecallMarkers } from "./safety.js";

const CAPTURE_SYSTEM_PROMPT = [
  "You are a memory extraction assistant.",
  "Your ONLY task is to extract durable facts, preferences, decisions, and entities from the conversation below.",
  "Write them to the specified memory file in the workspace.",
  "If the file does not exist, create it with appropriate headings.",
  "If the file already exists, APPEND new content only — do not overwrite existing entries.",
  "Do NOT create timestamped variant files.",
  "Each fact should be a concise bullet point under a relevant heading.",
  "Skip ephemeral details (greetings, acknowledgments, transient requests).",
  "If nothing is worth remembering, do not write anything.",
].join(" ");

function buildCapturePrompt(conversation: string, dateStr: string): string {
  return [
    `Extract durable memories from the following conversation and append to memory/${dateStr}.md.`,
    "",
    "--- Conversation ---",
    conversation,
    "--- End ---",
    "",
    'If nothing is worth remembering, reply with "[SILENT]".',
  ].join("\n");
}

function formatDateStamp(): string {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date());
  const year = parts.find((p) => p.type === "year")?.value;
  const month = parts.find((p) => p.type === "month")?.value;
  const day = parts.find((p) => p.type === "day")?.value;
  if (year && month && day) return `${year}-${month}-${day}`;
  // fallback to local date
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
}

async function captureLLM(
  api: OpenClawPluginApi,
  messages: unknown[],
  cfg: MemoryCorePlusConfig,
  ctx: { agentId?: string },
): Promise<void> {
  // Pre-filter: skip LLM call if no user message contains memory triggers
  const userMessages = extractMessagesOfRole(messages, ["user"], cfg.autoCaptureMaxMessages);
  const cleanedUser = userMessages.map((m) => stripRecallMarkers(m.text));
  if (!cleanedUser.some(isCapturableMessage)) {
    api.logger.info(
      `memory-core-plus: capture skipped (no capturable user messages out of ${cleanedUser.length})`,
    );
    return;
  }

  // Proceed with full conversation extraction (user + assistant)
  const recent = extractMessagesOfRole(messages, ["user", "assistant"], cfg.autoCaptureMaxMessages);
  if (recent.length === 0) return;

  const cleaned = recent.map((m) => `${m.role}: ${stripRecallMarkers(m.text)}`);
  const conversationBlock = cleaned.join("\n\n");
  if (conversationBlock.length < 20) {
    api.logger.info("memory-core-plus: capture skipped (conversation too short)");
    return;
  }

  const dateStr = formatDateStamp();
  const sessionKey = `:memory-capture:${ctx.agentId ?? "default"}`;

  const captureStart = Date.now();
  try {
    const result = await api.runtime.subagent.run({
      sessionKey,
      message: buildCapturePrompt(conversationBlock, dateStr),
      extraSystemPrompt: CAPTURE_SYSTEM_PROMPT,
      idempotencyKey: randomUUID(),
    });

    await api.runtime.subagent.waitForRun({
      runId: result.runId,
      timeoutMs: 30_000,
    });

    const elapsed = Date.now() - captureStart;
    api.logger.info(`memory-core-plus: auto-capture completed via LLM extraction (${elapsed}ms)`);
  } catch (err) {
    const msg = String(err);
    if (msg.includes("only available during a gateway request")) {
      api.logger.info("memory-core-plus: LLM capture unavailable (non-gateway), skipping");
      return;
    }
    api.logger.warn(`memory-core-plus: LLM capture failed: ${msg}`);
  }
}

export function createCaptureHook(api: OpenClawPluginApi, cfg: MemoryCorePlusConfig) {
  return async (
    event: { messages: unknown[]; success: boolean; error?: string; durationMs?: number },
    ctx: { agentId?: string; sessionKey?: string; trigger?: string },
  ) => {
    if (!event.success || !event.messages || event.messages.length === 0) {
      api.logger.info(
        `memory-core-plus: capture skipped (success=${event.success}, messages=${event.messages?.length ?? 0})`,
      );
      return;
    }

    if (ctx.trigger === "memory" || ctx.sessionKey?.includes(":memory-capture:")) {
      api.logger.info("memory-core-plus: capture skipped (inside memory-capture subagent, avoiding recursion)");
      return;
    }

    try {
      await captureLLM(api, event.messages, cfg, ctx);
    } catch (err) {
      api.logger.warn(`memory-core-plus: capture failed: ${String(err)}`);
    }
  };
}
