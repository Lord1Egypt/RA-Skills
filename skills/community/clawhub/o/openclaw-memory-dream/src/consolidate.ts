import { readFile, writeFile, readdir } from "fs/promises";
import { join } from "path";
import { homedir } from "os";
import { acquireLock, releaseLock } from "./lock.js";
import { loadState, saveState } from "./state.js";
import { DreamConfig } from "./scheduler.js";
import { readRecentTranscripts } from "./transcript.js";
import { STAGING_FILE } from "./capture.js";

async function readMemoryFile(workspaceDir: string, filename: string): Promise<string | null> {
  try {
    return await readFile(join(workspaceDir, filename), "utf-8");
  } catch {
    return null;
  }
}

async function readLcmSummaries(agentDir: string): Promise<string> {
  const lcmDir = join(agentDir, "lossless-claw");
  try {
    const entries = await readdir(lcmDir);
    const summaryFiles = entries
      .filter((f) => f.endsWith(".md") || f.endsWith(".txt") || f.endsWith(".json"))
      .sort()
      .slice(-10); // last 10 summaries

    const contents: string[] = [];
    for (const file of summaryFiles) {
      try {
        const content = await readFile(join(lcmDir, file), "utf-8");
        contents.push(`--- ${file} ---\n${content.slice(0, 2000)}`);
      } catch {
        // skip unreadable files
      }
    }

    return contents.length > 0
      ? contents.join("\n\n")
      : "(no recent session history available)";
  } catch {
    return "(no recent session history available)";
  }
}

function buildConsolidationPrompt(
  filename: string,
  content: string,
  lcmSummaries: string,
  transcripts: string,
  staging: string
): string {
  const currentDate = new Date().toISOString().split("T")[0];

  const stagingSection = staging.trim()
    ? `\nIn-session captured signals (new, not yet integrated):\n${staging}\n`
    : "";

  return `You are consolidating an AI agent's memory files. Your job is to make them more useful, not smaller — keep everything important.

Current date: ${currentDate}

Rules:
- Replace vague references like "today", "yesterday", "last week" with actual dates based on context
- Remove entries that are clearly stale or superseded by newer information
- Resolve contradictions — keep the most recent/accurate version
- Preserve relationship history, decisions, and learned preferences
- Integrate any new signals from the captured staging section below
- Do NOT summarize away specific details that might matter later
- Return ONLY the updated file content, no commentary

Current content of ${filename}:
${content}

Recent session history (LCM summaries, for context on what's still relevant):
${lcmSummaries}

Recent high-value transcript moments:
${transcripts}
${stagingSection}
Return the consolidated content for ${filename}. Keep the same format and headers.`;
}

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";

async function callLlm(
  prompt: string,
  config: DreamConfig,
  api: OpenClawPluginApi,
  agentId: string
): Promise<string> {
  // Session key is scoped to the actual agentId — never hard-coded
  const sessionKey = `agent:${agentId}:subagent:memory-dream-consolidation`;

  const { runId } = await api.runtime.subagent.run({
    sessionKey,
    message: prompt,
    ...(config.model ? { model: config.model } : {}),
    deliver: false,
  });

  const result = await api.runtime.subagent.waitForRun({ runId, timeoutMs: 120_000 });
  if (result.status !== "ok") {
    throw new Error(`Subagent consolidation failed with status: ${result.status}`);
  }

  // Extract text from the last assistant message
  const messages = await api.runtime.subagent.getSessionMessages({ sessionKey });
  const lastAssistant = [...(messages.messages as unknown[])].reverse().find(
    (m): m is { role: string; content: unknown } =>
      typeof m === "object" && m !== null && (m as { role?: string }).role === "assistant"
  );
  if (!lastAssistant) throw new Error("No assistant message in consolidation result");

  const text = Array.isArray(lastAssistant.content)
    ? (lastAssistant.content as Array<{ type?: string; text?: string }>)
        .filter((c) => c.type === "text")
        .map((c) => c.text ?? "")
        .join("")
    : String(lastAssistant.content);

  return text;
}

export async function consolidate(
  stateDir: string,
  workspaceDir: string,
  config: DreamConfig,
  api: OpenClawPluginApi,
  agentId = "main"
): Promise<void> {
  const logger = api.logger;
  // Step 1: Acquire lock
  const locked = await acquireLock(stateDir);
  if (!locked) {
    logger.warn("[memory-dream] Could not acquire lock — consolidation already running");
    return;
  }

  try {
    // Step 2: Mark as running
    const state = await loadState(stateDir);
    state.lastRunStatus = "running";
    await saveState(stateDir, state);

    logger.info("[memory-dream] Starting memory consolidation");

    // Step 3: Gather context — LCM summaries, transcripts, and staging
    const lcmSummaries = await readLcmSummaries(stateDir);

    const agentBaseDir = join(homedir(), ".openclaw", agentId);
    const transcripts = await readRecentTranscripts(agentBaseDir);

    const stagingPath = join(workspaceDir, STAGING_FILE);
    let stagingContent = "";
    try {
      stagingContent = await readFile(stagingPath, "utf-8");
    } catch {
      // No staging file — that's fine
    }

    const updatedFiles: string[] = [];
    const skippedFiles: string[] = [];

    // Step 4: Process each memory file
    for (const filename of config.memoryFiles) {
      const content = await readMemoryFile(workspaceDir, filename);
      if (content === null) {
        skippedFiles.push(filename);
        logger.warn(`[memory-dream] Skipping ${filename} — file not found`);
        continue;
      }

      logger.info(`[memory-dream] Consolidating ${filename}`);

      try {
        const prompt = buildConsolidationPrompt(filename, content, lcmSummaries, transcripts, stagingContent);
        const consolidated = await callLlm(prompt, config, api, agentId);

        if (consolidated && consolidated.trim().length > 0) {
          const originalLines = content.split("\n").length;
          const newLines = consolidated.trim().split("\n").length;
          const delta = newLines - originalLines;
          const deltaStr = delta <= 0 ? `${Math.abs(delta)} lines removed` : `${delta} lines added`;
          logger.info(`[memory-dream] Writing ${filename}: ${originalLines} → ${newLines} lines (${deltaStr})`);
          await writeFile(join(workspaceDir, filename), consolidated.trim() + "\n", "utf-8");
          updatedFiles.push(filename);
        } else {
          logger.warn(`[memory-dream] LLM returned empty content for ${filename}, skipping write`);
          skippedFiles.push(filename);
        }
      } catch (err) {
        logger.error(`[memory-dream] Failed to consolidate ${filename}: ${err}`);
        skippedFiles.push(filename);
      }
    }

    // Step 5: Clear staging file — its content has been absorbed into memory files
    if (stagingContent.trim()) {
      try {
        await writeFile(stagingPath, "", "utf-8");
        logger.info("[memory-dream] Cleared memory-staging.md (absorbed into consolidation)");
      } catch {
        // Best-effort — don't fail consolidation over this
      }
    }

    // Step 6: Update state — success
    const summary = buildSummary(updatedFiles, skippedFiles);
    const finalState = await loadState(stateDir);
    finalState.sessionCount = 0;
    finalState.lastRunAt = new Date().toISOString();
    finalState.lastRunStatus = "success";
    finalState.lastRunSummary = summary;
    await saveState(stateDir, finalState);

    logger.info(`[memory-dream] Consolidation complete. ${summary}`);
  } catch (err) {
    logger.error(`[memory-dream] Consolidation failed: ${err}`);

    try {
      const state = await loadState(stateDir);
      state.lastRunStatus = "failed";
      await saveState(stateDir, state);
    } catch {
      // best-effort
    }
  } finally {
    // Step 6: Release lock
    await releaseLock(stateDir);
  }
}

function buildSummary(updated: string[], skipped: string[]): string {
  const parts: string[] = [];
  if (updated.length > 0) parts.push(`updated: ${updated.join(", ")}`);
  if (skipped.length > 0) parts.push(`skipped: ${skipped.join(", ")}`);
  return parts.join("; ") || "nothing to do";
}
