import { readFile, writeFile, mkdir } from "fs/promises";
import { join } from "path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import { DreamConfig } from "./scheduler.js";

export const STAGING_FILE = "memory-staging.md";

function buildCapturePrompt(conversationText: string): string {
  return `You are scanning a conversation exchange for memory-worthy signals to capture for an AI agent's persistent memory.

Look for:
- User corrections ("actually, do it this way", "no, that's wrong", "don't do X")
- Stated preferences ("I prefer X", "always use Y", "I like Z style")
- Key decisions made that should be remembered
- Important facts or constraints discovered
- Patterns the agent should apply in future sessions

Do NOT capture:
- Trivial exchanges or small talk
- Task completions that have no future relevance
- Routine questions and answers
- Things that are obvious from the code itself

Conversation to analyze:
${conversationText}

If there are NO memory-worthy signals, respond with exactly: NOTHING

If there ARE signals, respond with a bullet list (one item per line, each starting with "- "):
- <concise description of the signal>
- <another signal if present>

Be brief and specific. Do NOT include commentary, headers, or explanations outside the bullet list.`;
}

async function callCaptureLlm(
  prompt: string,
  config: DreamConfig,
  api: OpenClawPluginApi,
  agentId: string
): Promise<string> {
  const sessionKey = `agent:${agentId}:subagent:memory-dream-capture-${Date.now()}`;
  const model = config.captureModel ?? "claude-haiku-4-5-20251001";

  const { runId } = await api.runtime.subagent.run({
    sessionKey,
    message: prompt,
    model,
    deliver: false,
  });

  const result = await api.runtime.subagent.waitForRun({ runId, timeoutMs: 30_000 });
  if (result.status !== "ok") {
    throw new Error(`Capture subagent failed: ${result.status}`);
  }

  const messages = await api.runtime.subagent.getSessionMessages({ sessionKey });
  const lastAssistant = [...(messages.messages as unknown[])].reverse().find(
    (m): m is { role: string; content: unknown } =>
      typeof m === "object" && m !== null && (m as { role?: string }).role === "assistant"
  );
  if (!lastAssistant) throw new Error("No assistant message in capture result");

  const text = Array.isArray(lastAssistant.content)
    ? (lastAssistant.content as Array<{ type?: string; text?: string }>)
        .filter((c) => c.type === "text")
        .map((c) => c.text ?? "")
        .join("")
    : String(lastAssistant.content);

  return text;
}

export async function captureFromTurn(
  stateDir: string,
  workspaceDir: string,
  conversationText: string,
  config: DreamConfig,
  api: OpenClawPluginApi,
  agentId: string
): Promise<boolean> {
  if (!config.enableCapture) return false;
  if (!conversationText || conversationText.trim().length < 50) return false;

  try {
    const prompt = buildCapturePrompt(conversationText);
    const result = await callCaptureLlm(prompt, config, api, agentId);

    const trimmed = result.trim();
    if (!trimmed || trimmed === "NOTHING" || !trimmed.startsWith("-")) {
      return false;
    }

    const date = new Date().toISOString().split("T")[0];
    const entry = `\n## [${date}] Captured\n${trimmed}\n`;
    const stagingPath = join(workspaceDir, STAGING_FILE);

    await mkdir(workspaceDir, { recursive: true });
    let existing = "";
    try {
      existing = await readFile(stagingPath, "utf-8");
    } catch {
      // File doesn't exist yet — start fresh
    }
    await writeFile(stagingPath, existing + entry, "utf-8");

    api.logger.info(`[memory-dream] Captured memory signal to ${STAGING_FILE}`);
    return true;
  } catch (err) {
    // Fail silently — never block a turn
    api.logger.warn(`[memory-dream] Capture failed (non-blocking): ${String(err)}`);
    return false;
  }
}
