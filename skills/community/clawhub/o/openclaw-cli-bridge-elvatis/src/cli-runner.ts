/**
 * cli-runner.ts
 *
 * Spawns CLI subprocesses (gemini, claude, codex, opencode, pi) and captures their output.
 * Input: OpenAI-format messages → formatted prompt string → CLI stdin (or CLI arg).
 *
 * Prompt delivery:
 *   - Gemini/Claude/Codex receive the prompt via stdin to avoid E2BIG and agentic mode.
 *   - OpenCode receives the prompt as a CLI argument (`opencode run "prompt"`).
 *   - Pi receives the prompt via `-p "prompt"` flag.
 *
 * Workdir isolation:
 *   - Gemini: defaults to tmpdir() (prevents agentic workspace scanning).
 *   - Claude/Codex: defaults to homedir().
 *   - OpenCode/Pi: defaults to homedir().
 *   - All runners accept an explicit `workdir` override via RouteOptions.
 */

import { spawn, execSync } from "node:child_process";
import { tmpdir, homedir } from "node:os";
import { existsSync, writeFileSync, unlinkSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { randomBytes } from "node:crypto";
import { ensureClaudeToken, refreshClaudeToken } from "./claude-auth.js";
import {
  type ToolDefinition,
  type CliToolResult,
  buildToolPromptBlock,
  parseToolCallResponse,
} from "./tool-protocol.js";
import {
  MAX_MESSAGES,
  MAX_MSG_CHARS,
  DEFAULT_CLI_TIMEOUT_MS,
  TIMEOUT_GRACE_MS,
  MEDIA_TMP_DIR,
} from "./config.js";

// ──────────────────────────────────────────────────────────────────────────────
// Message formatting
// ──────────────────────────────────────────────────────────────────────────────

export interface ContentPart {
  type: string;
  text?: string;
}

export interface ChatMessage {
  role: "system" | "user" | "assistant" | "tool";
  /** Plain string or OpenAI-style content array (multimodal / structured). */
  content: string | ContentPart[] | unknown;
  /** Tool calls made by the assistant (OpenAI tool calling protocol). */
  tool_calls?: Array<{ id: string; type: string; function: { name: string; arguments: string } }>;
  /** ID linking a tool result to the assistant's tool_call. */
  tool_call_id?: string;
  /** Function name for tool result messages. */
  name?: string;
}

// Re-export tool-protocol types for convenience
export type { ToolDefinition, CliToolResult } from "./tool-protocol.js";

/**
 * Convert OpenAI messages to a single flat prompt string.
 * Truncates to MAX_MESSAGES (keeping the most recent) and MAX_MSG_CHARS per
 * message to avoid oversized payloads.
 *
 * Handles tool-calling messages:
 *   - role "tool": formatted as [Tool Result: name]
 *   - role "assistant" with tool_calls: formatted as [Assistant Tool Call: name(args)]
 */
export function formatPrompt(messages: ChatMessage[]): string {
  if (messages.length === 0) return "";

  // Keep system message (if any) + last N non-system messages
  const system = messages.find((m) => m.role === "system");
  const nonSystem = messages.filter((m) => m.role !== "system");
  const recent = nonSystem.slice(-MAX_MESSAGES);
  const truncated = system ? [system, ...recent] : recent;

  // Single short user message — send bare (no wrapping needed)
  if (truncated.length === 1 && truncated[0].role === "user") {
    return truncateContent(truncated[0].content);
  }

  return truncated
    .map((m) => {
      // Assistant message with tool_calls (no text content)
      if (m.role === "assistant" && m.tool_calls?.length) {
        const calls = m.tool_calls.map((tc) =>
          `[Assistant Tool Call: ${tc.function.name}(${tc.function.arguments})]\n`
        ).join("");
        const content = m.content ? truncateContent(m.content) : "";
        return content ? `${calls}\n${content}` : calls.trimEnd();
      }

      // Tool result message
      if (m.role === "tool") {
        const name = m.name ?? "unknown";
        const content = truncateContent(m.content);
        return `[Tool Result: ${name}]\n${content}`;
      }

      const content = truncateContent(m.content);
      switch (m.role) {
        case "system":    return `[System]\n${content}`;
        case "assistant": return `[Assistant]\n${content}`;
        case "user":
        default:          return `[User]\n${content}`;
      }
    })
    .join("\n\n");
}

/**
 * Coerce any message content value to a plain string.
 *
 * Handles:
 *  - string          → as-is
 *  - ContentPart[]   → join text parts + describe non-text parts (multimodal)
 *  - other object    → JSON.stringify (prevents "[object Object]" from reaching the CLI)
 *  - null/undefined  → ""
 */
function contentToString(content: unknown): string {
  if (typeof content === "string") return content;
  if (content === null || content === undefined) return "";
  if (Array.isArray(content)) {
    return (content as Record<string, unknown>[])
      .map((c) => {
        if (c?.type === "text" && typeof c.text === "string") return c.text;
        if (c?.type === "image_url") return "[Attached image — see saved media file]";
        if (c?.type === "input_audio") return "[Attached audio — see saved media file]";
        return null;
      })
      .filter(Boolean)
      .join("\n");
  }
  if (typeof content === "object") return JSON.stringify(content);
  return String(content);
}

function truncateContent(raw: unknown): string {
  const s = contentToString(raw);
  if (s.length <= MAX_MSG_CHARS) return s;
  return s.slice(0, MAX_MSG_CHARS) + `\n...[truncated ${s.length - MAX_MSG_CHARS} chars]`;
}

// ──────────────────────────────────────────────────────────────────────────────
// Multimodal content extraction
// ──────────────────────────────────────────────────────────────────────────────

export interface MediaFile {
  path: string;
  mimeType: string;
}

// MEDIA_TMP_DIR imported from config.ts

/**
 * Extract non-text content parts (images, audio) from messages.
 * Saves base64 data to temp files and replaces media parts with file references.
 * Returns cleaned messages + list of saved media files for CLI -i flags.
 */
export function extractMultimodalParts(messages: ChatMessage[]): {
  cleanMessages: ChatMessage[];
  mediaFiles: MediaFile[];
} {
  const mediaFiles: MediaFile[] = [];
  const cleanMessages = messages.map((m) => {
    if (!Array.isArray(m.content)) return m;

    const parts = m.content as Record<string, unknown>[];
    const newParts: Record<string, unknown>[] = [];

    for (const part of parts) {
      if (part?.type === "image_url") {
        const imageUrl = (part as { image_url?: { url?: string } }).image_url;
        const url = imageUrl?.url ?? "";
        if (url.startsWith("data:")) {
          // data:image/png;base64,iVBOR...
          const match = url.match(/^data:(image\/\w+);base64,(.+)$/);
          if (match) {
            const ext = match[1].split("/")[1] || "png";
            const filePath = saveBase64ToTemp(match[2], ext);
            mediaFiles.push({ path: filePath, mimeType: match[1] });
            newParts.push({ type: "text", text: `[Attached image: ${filePath}]` });
            continue;
          }
        }
        // URL-based image — include URL reference in text
        newParts.push({ type: "text", text: `[Image URL: ${url}]` });
        continue;
      }

      if (part?.type === "input_audio") {
        const audioData = (part as { input_audio?: { data?: string; format?: string } }).input_audio;
        if (audioData?.data) {
          const ext = audioData.format || "wav";
          const filePath = saveBase64ToTemp(audioData.data, ext);
          mediaFiles.push({ path: filePath, mimeType: `audio/${ext}` });
          newParts.push({ type: "text", text: `[Attached audio: ${filePath}]` });
          continue;
        }
      }

      // Keep text parts and anything else as-is
      newParts.push(part);
    }

    return { ...m, content: newParts };
  });

  return { cleanMessages, mediaFiles };
}

function saveBase64ToTemp(base64Data: string, ext: string): string {
  mkdirSync(MEDIA_TMP_DIR, { recursive: true });
  const fileName = `media-${randomBytes(8).toString("hex")}.${ext}`;
  const filePath = join(MEDIA_TMP_DIR, fileName);
  writeFileSync(filePath, Buffer.from(base64Data, "base64"));
  return filePath;
}

/** Schedule deletion of temp media files after a delay. */
export function cleanupMediaFiles(files: MediaFile[], delayMs = 60_000): void {
  if (files.length === 0) return;
  setTimeout(() => {
    for (const f of files) {
      try { unlinkSync(f.path); } catch { /* already deleted */ }
    }
  }, delayMs);
}

// ──────────────────────────────────────────────────────────────────────────────
// Minimal environment for spawned subprocesses
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Build a minimal, safe environment for spawning CLI subprocesses.
 *
 * WHY: The OpenClaw gateway modifies process.env at runtime (OPENCLAW_* vars,
 * session context, etc.). Spreading the full process.env into spawn() can push
 * argv+envp over ARG_MAX (~2 MB on Linux) → "spawn E2BIG". Only passing what
 * the CLI tools actually need keeps us well under the limit regardless of
 * gateway runtime state.
 */
function buildMinimalEnv(): Record<string, string> {
  const pick = (key: string) => process.env[key];
  const env: Record<string, string> = { NO_COLOR: "1", TERM: "dumb" };

  for (const key of ["HOME", "PATH", "USER", "LOGNAME", "SHELL", "TMPDIR", "TMP", "TEMP"]) {
    const v = pick(key);
    if (v) env[key] = v;
  }
  for (const key of [
    "GOOGLE_APPLICATION_CREDENTIALS",
    "ANTHROPIC_API_KEY",
    "CLAUDE_API_KEY",
    "CODEX_API_KEY",
    "OPENAI_API_KEY",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_CACHE_HOME",
    // Required for Claude Code OAuth (Gnome Keyring / libsecret access)
    "XDG_RUNTIME_DIR",
    "DBUS_SESSION_BUS_ADDRESS",
  ]) {
    const v = pick(key);
    if (v) env[key] = v;
  }

  return env;
}

// ──────────────────────────────────────────────────────────────────────────────
// Core subprocess runner
// ──────────────────────────────────────────────────────────────────────────────

export interface CliRunResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  /** True when the process was killed due to a timeout (exit 143 = SIGTERM). */
  timedOut: boolean;
}

export interface RunCliOptions {
  /**
   * Working directory for the subprocess.
   * Defaults to homedir() — a neutral dir that won't trigger agentic context scanning.
   */
  cwd?: string;
  timeoutMs?: number;
  /** Optional logger for timeout events. */
  log?: (msg: string) => void;
}

// TIMEOUT_GRACE_MS imported from config.ts

/**
 * Spawn a CLI and deliver the prompt via stdin.
 *
 * Timeout handling (replaces Node's spawn({ timeout }) for better control):
 *   1. After `timeoutMs`, send SIGTERM and log a clear message.
 *   2. If the process doesn't exit within TIMEOUT_GRACE_MS (5s), send SIGKILL.
 *   3. The result's `timedOut` flag is set so callers can distinguish
 *      supervisor timeouts from real CLI errors.
 *
 * cwd defaults to homedir() so CLIs that scan the working directory for
 * project context (like Gemini) don't accidentally enter agentic mode.
 */
export function runCli(
  cmd: string,
  args: string[],
  prompt: string,
  timeoutMs = DEFAULT_CLI_TIMEOUT_MS,
  opts: RunCliOptions = {}
): Promise<CliRunResult> {
  const cwd = opts.cwd ?? homedir();
  const log = opts.log ?? (() => {});

  return new Promise((resolve, reject) => {
    // Do NOT pass timeout to spawn() — we manage it ourselves for graceful shutdown.
    const proc = spawn(cmd, args, {
      env: buildMinimalEnv(),
      cwd,
    });

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    let killTimer: ReturnType<typeof setTimeout> | null = null;
    let timeoutTimer: ReturnType<typeof setTimeout> | null = null;

    const clearTimers = () => {
      if (timeoutTimer) { clearTimeout(timeoutTimer); timeoutTimer = null; }
      if (killTimer) { clearTimeout(killTimer); killTimer = null; }
    };

    // ── Timeout sequence: SIGTERM → grace → SIGKILL ──────────────────────
    timeoutTimer = setTimeout(() => {
      timedOut = true;
      const elapsed = Math.round(timeoutMs / 1000);
      log(`[cli-bridge] timeout after ${elapsed}s for ${cmd}, sending SIGTERM`);
      proc.kill("SIGTERM");

      killTimer = setTimeout(() => {
        if (!proc.killed) {
          log(`[cli-bridge] ${cmd} still running after ${TIMEOUT_GRACE_MS / 1000}s grace, sending SIGKILL`);
          proc.kill("SIGKILL");
        }
      }, TIMEOUT_GRACE_MS);
    }, timeoutMs);

    proc.stdin.write(prompt, "utf8", () => {
      proc.stdin.end();
    });

    proc.stdout.on("data", (d: Buffer) => { stdout += d.toString(); });
    proc.stderr.on("data", (d: Buffer) => { stderr += d.toString(); });

    proc.on("close", (code) => {
      clearTimers();
      resolve({ stdout: stdout.trim(), stderr: stderr.trim(), exitCode: code ?? 0, timedOut });
    });

    proc.on("error", (err) => {
      clearTimers();
      reject(new Error(`Failed to spawn '${cmd}': ${err.message}`));
    });
  });
}

/**
 * Spawn a CLI with the prompt delivered as a CLI argument (not stdin).
 * Used by OpenCode which expects `opencode run "prompt"`.
 * Uses the same graceful SIGTERM→SIGKILL timeout sequence as runCli.
 */
export function runCliWithArg(
  cmd: string,
  args: string[],
  timeoutMs = DEFAULT_CLI_TIMEOUT_MS,
  opts: RunCliOptions = {}
): Promise<CliRunResult> {
  const cwd = opts.cwd ?? homedir();
  const log = opts.log ?? (() => {});

  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, {
      env: buildMinimalEnv(),
      cwd,
    });

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    let killTimer: ReturnType<typeof setTimeout> | null = null;
    let timeoutTimer: ReturnType<typeof setTimeout> | null = null;

    const clearTimers = () => {
      if (timeoutTimer) { clearTimeout(timeoutTimer); timeoutTimer = null; }
      if (killTimer) { clearTimeout(killTimer); killTimer = null; }
    };

    timeoutTimer = setTimeout(() => {
      timedOut = true;
      const elapsed = Math.round(timeoutMs / 1000);
      log(`[cli-bridge] timeout after ${elapsed}s for ${cmd}, sending SIGTERM`);
      proc.kill("SIGTERM");

      killTimer = setTimeout(() => {
        if (!proc.killed) {
          log(`[cli-bridge] ${cmd} still running after ${TIMEOUT_GRACE_MS / 1000}s grace, sending SIGKILL`);
          proc.kill("SIGKILL");
        }
      }, TIMEOUT_GRACE_MS);
    }, timeoutMs);

    proc.stdout.on("data", (d: Buffer) => { stdout += d.toString(); });
    proc.stderr.on("data", (d: Buffer) => { stderr += d.toString(); });

    proc.on("close", (code) => {
      clearTimers();
      resolve({ stdout: stdout.trim(), stderr: stderr.trim(), exitCode: code ?? 0, timedOut });
    });

    proc.on("error", (err) => {
      clearTimers();
      reject(new Error(`Failed to spawn '${cmd}': ${err.message}`));
    });
  });
}

/**
 * Annotate an error message when exit code 143 (SIGTERM) is detected.
 * Makes it clear in logs that this was a supervisor timeout, not a model error.
 */
export function annotateExitError(exitCode: number, stderr: string, timedOut: boolean, model: string): string {
  const base = stderr || "(no output)";
  if (timedOut || exitCode === 143) {
    return `timeout: ${model} killed by supervisor (exit ${exitCode}, likely timeout) — ${base}`;
  }
  return base;
}

// ──────────────────────────────────────────────────────────────────────────────
// Gemini CLI
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Run Gemini CLI in headless mode with prompt delivered via stdin.
 *
 * WHY stdin (not @file):
 *   The @file syntax (`gemini -p @/tmp/xxx.txt`) triggers Gemini's agentic
 *   mode — it scans the current working directory for project context and
 *   interprets the prompt as a task instruction, not a Q&A. This causes hangs,
 *   wrong answers, and "directory does not exist" errors when run from a
 *   project workspace.
 *
 * Gemini CLI: -p "" triggers headless mode; stdin content is the actual prompt
 * (per Gemini docs: "prompt is appended to input on stdin (if any)").
 *
 * cwd = tmpdir() by default — neutral empty-ish dir, prevents workspace context scanning.
 * Override with explicit workdir.
 */
export async function runGemini(
  prompt: string,
  modelId: string,
  timeoutMs: number,
  workdir?: string,
  opts?: { tools?: ToolDefinition[]; log?: (msg: string) => void }
): Promise<string> {
  const model = stripPrefix(modelId);
  // -p "" = headless mode trigger; actual prompt arrives via stdin
  // --approval-mode yolo: auto-approve all tool executions, never ask questions
  const args = ["-m", model, "-p", "", "--approval-mode", "yolo"];
  const cwd = workdir ?? tmpdir();

  // When tools are present, prepend tool instructions to prompt
  const effectivePrompt = opts?.tools?.length
    ? buildToolPromptBlock(opts.tools) + "\n\n" + prompt
    : prompt;

  const result = await runCli("gemini", args, effectivePrompt, timeoutMs, { cwd, log: opts?.log });

  // Filter out [WARN] lines from stderr (Gemini emits noisy permission warnings)
  const cleanStderr = result.stderr
    .split("\n")
    .filter((l) => !l.startsWith("[WARN]") && !l.startsWith("Loaded cached"))
    .join("\n")
    .trim();

  if (result.exitCode !== 0 && result.stdout.length === 0) {
    throw new Error(`gemini exited ${result.exitCode}: ${annotateExitError(result.exitCode, cleanStderr, result.timedOut, modelId)}`);
  }

  return result.stdout || cleanStderr;
}

// ──────────────────────────────────────────────────────────────────────────────
// Claude Code CLI
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Run Claude Code CLI in headless mode with prompt delivered via stdin.
 * Strips the model prefix ("cli-claude/claude-opus-4-6" → "claude-opus-4-6").
 * cwd = homedir() by default. Override with explicit workdir.
 */
export async function runClaude(
  prompt: string,
  modelId: string,
  timeoutMs: number,
  workdir?: string,
  opts?: { tools?: ToolDefinition[]; log?: (msg: string) => void }
): Promise<string> {
  // Proactively refresh OAuth token if it's about to expire (< 5 min remaining).
  // No-op for API-key users.
  await ensureClaudeToken();

  const model = stripPrefix(modelId);
  // Always use bypassPermissions to ensure fully autonomous execution (never asks questions).
  // Use text output for all cases — JSON schema is unreliable with Claude Code's system prompt.
  const args: string[] = [
    "-p",
    "--output-format", "text",
    "--permission-mode", "bypassPermissions",
    "--dangerously-skip-permissions",
    "--model", model,
  ];

  // When tools are present, prepend tool instructions to prompt
  const effectivePrompt = opts?.tools?.length
    ? buildToolPromptBlock(opts.tools) + "\n\n" + prompt
    : prompt;

  const cwd = workdir ?? homedir();
  const result = await runCli("claude", args, effectivePrompt, timeoutMs, { cwd, log: opts?.log });

  // On 401: attempt one token refresh + retry before giving up.
  if (result.exitCode !== 0 && result.stdout.length === 0) {
    // If this was a timeout, don't bother with auth retry — it's a supervisor kill, not a 401.
    if (result.timedOut) {
      throw new Error(`claude exited ${result.exitCode}: ${annotateExitError(result.exitCode, result.stderr, true, modelId)}`);
    }
    const stderr = result.stderr || "(no output)";
    if (stderr.includes("401") || stderr.includes("Invalid authentication credentials") || stderr.includes("authentication_error")) {
      // Refresh and retry once
      await refreshClaudeToken();
      const retry = await runCli("claude", args, effectivePrompt, timeoutMs, { cwd, log: opts?.log });
      if (retry.exitCode !== 0 && retry.stdout.length === 0) {
        const retryStderr = retry.stderr || "(no output)";
        if (retryStderr.includes("401") || retryStderr.includes("authentication_error") || retryStderr.includes("Invalid authentication credentials")) {
          throw new Error(
            "Claude CLI OAuth token refresh failed. " +
            "Re-login required: run `claude auth logout && claude auth login` in a terminal."
          );
        }
        throw new Error(`claude exited ${retry.exitCode} (after token refresh): ${retryStderr}`);
      }
      return retry.stdout;
    }
    throw new Error(`claude exited ${result.exitCode}: ${annotateExitError(result.exitCode, stderr, false, modelId)}`);
  }

  return result.stdout;
}

// ──────────────────────────────────────────────────────────────────────────────
// Codex CLI
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Ensure the workdir is a git repository. Codex CLI requires a git repo.
 * If the directory exists but is not a git repo, run `git init`.
 */
function ensureGitRepo(dir: string): void {
  if (!existsSync(join(dir, ".git"))) {
    execSync("git init", { cwd: dir, stdio: "ignore" });
  }
}

/**
 * Run Codex CLI in non-interactive mode with prompt via stdin.
 * cwd = homedir() by default. Override with explicit workdir.
 * Auto-initializes git if workdir is not already a git repo.
 */
export async function runCodex(
  prompt: string,
  modelId: string,
  timeoutMs: number,
  workdir?: string,
  opts?: { tools?: ToolDefinition[]; mediaFiles?: MediaFile[]; log?: (msg: string) => void }
): Promise<string> {
  const model = stripPrefix(modelId);
  const args = ["exec", "--model", model, "--full-auto"];

  // Codex supports native image input via -i flag
  if (opts?.mediaFiles?.length) {
    for (const f of opts.mediaFiles) {
      if (f.mimeType.startsWith("image/")) {
        args.push("-i", f.path);
      }
    }
  }

  const cwd = workdir ?? homedir();

  // Codex requires a git repo in the working directory
  ensureGitRepo(cwd);

  // When tools are present, prepend tool instructions to prompt
  const effectivePrompt = opts?.tools?.length
    ? buildToolPromptBlock(opts.tools) + "\n\n" + prompt
    : prompt;

  const result = await runCli("codex", args, effectivePrompt, timeoutMs, { cwd, log: opts?.log });

  if (result.exitCode !== 0 && result.stdout.length === 0) {
    throw new Error(`codex exited ${result.exitCode}: ${annotateExitError(result.exitCode, result.stderr, result.timedOut, modelId)}`);
  }

  return result.stdout || result.stderr;
}

// ──────────────────────────────────────────────────────────────────────────────
// OpenCode CLI
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Run OpenCode CLI. Prompt is passed as a CLI argument: `opencode run "prompt"`.
 * cwd = homedir() by default. Override with explicit workdir.
 */
export async function runOpenCode(
  prompt: string,
  _modelId: string,
  timeoutMs: number,
  workdir?: string,
  opts?: { log?: (msg: string) => void }
): Promise<string> {
  const args = ["run", prompt];
  const cwd = workdir ?? homedir();
  const result = await runCliWithArg("opencode", args, timeoutMs, { cwd, log: opts?.log });

  if (result.exitCode !== 0 && result.stdout.length === 0) {
    throw new Error(`opencode exited ${result.exitCode}: ${annotateExitError(result.exitCode, result.stderr, result.timedOut, "opencode")}`);
  }

  return result.stdout || result.stderr;
}

// ──────────────────────────────────────────────────────────────────────────────
// Pi CLI
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Run Pi CLI in non-interactive mode: `pi -p "prompt"`.
 * cwd = homedir() by default. Override with explicit workdir.
 */
export async function runPi(
  prompt: string,
  _modelId: string,
  timeoutMs: number,
  workdir?: string,
  opts?: { log?: (msg: string) => void }
): Promise<string> {
  const args = ["-p", prompt];
  const cwd = workdir ?? homedir();
  const result = await runCliWithArg("pi", args, timeoutMs, { cwd, log: opts?.log });

  if (result.exitCode !== 0 && result.stdout.length === 0) {
    throw new Error(`pi exited ${result.exitCode}: ${annotateExitError(result.exitCode, result.stderr, result.timedOut, "pi")}`);
  }

  return result.stdout || result.stderr;
}

// ──────────────────────────────────────────────────────────────────────────────
// Model allowlist (T-103)
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Default set of permitted models for the CLI bridge.
 * Matches the models registered as slash commands in index.ts.
 * Expressed as normalized "cli-<type>/<model-id>" strings (vllm/ prefix already stripped).
 *
 * To extend: pass a custom set to routeToCliRunner via the `allowedModels` option.
 * To disable the check: pass `null` for `allowedModels`.
 */
export const DEFAULT_ALLOWED_CLI_MODELS: ReadonlySet<string> = new Set([
  // Claude Code CLI
  "cli-claude/claude-sonnet-4-6",
  "cli-claude/claude-opus-4-6",
  "cli-claude/claude-haiku-4-5",
  // Gemini CLI
  "cli-gemini/gemini-2.5-pro",
  "cli-gemini/gemini-2.5-flash",
  "cli-gemini/gemini-3-pro-preview",
  "cli-gemini/gemini-3-flash-preview",
  // Aliases (map to preview variants internally)
  "cli-gemini/gemini-3-pro",   // alias → gemini-3-pro-preview
  "cli-gemini/gemini-3-flash", // alias → gemini-3-flash-preview
  // Codex CLI
  "openai-codex/gpt-5.3-codex",
  "openai-codex/gpt-5.3-codex-spark",
  "openai-codex/gpt-5.2-codex",
  "openai-codex/gpt-5.4",
  "openai-codex/gpt-5.1-codex-mini",
  // OpenCode CLI
  "opencode/default",
  // Pi CLI
  "pi/default",
]);

/** Normalize model aliases to their canonical CLI model names. */
function normalizeModelAlias(normalized: string): string {
  const ALIASES: Record<string, string> = {
    "cli-gemini/gemini-3-pro":   "cli-gemini/gemini-3-pro-preview",
    "cli-gemini/gemini-3-flash": "cli-gemini/gemini-3-flash-preview",
  };
  return ALIASES[normalized] ?? normalized;
}

// ──────────────────────────────────────────────────────────────────────────────
// Router
// ──────────────────────────────────────────────────────────────────────────────

export interface RouteOptions {
  /**
   * Explicit model allowlist (normalized, vllm/ stripped).
   * Pass `null` to disable the allowlist check entirely.
   * Defaults to DEFAULT_ALLOWED_CLI_MODELS.
   */
  allowedModels?: ReadonlySet<string> | null;
  /**
   * Working directory for the CLI subprocess.
   * Overrides the per-runner default (tmpdir for gemini, homedir for others).
   */
  workdir?: string;
  /**
   * OpenAI tool definitions. When present, tool instructions are injected
   * into the prompt and structured tool_call responses are parsed.
   */
  tools?: ToolDefinition[];
  /**
   * Media files extracted from multimodal message content.
   * Passed to CLIs that support native media input (e.g. codex -i).
   */
  mediaFiles?: MediaFile[];
  /** Logger for timeout and lifecycle events. */
  log?: (msg: string) => void;
}

/**
 * Route a chat completion to the correct CLI based on model prefix.
 *   cli-gemini/<id>      → gemini CLI
 *   cli-claude/<id>      → claude CLI
 *   openai-codex/<id>    → codex CLI
 *   opencode/<id>        → opencode CLI
 *   pi/<id>              → pi CLI
 *
 * When `tools` are provided, tool instructions are injected into the prompt
 * and the response is parsed for structured tool_calls.
 *
 * Enforces DEFAULT_ALLOWED_CLI_MODELS by default (T-103).
 * Pass `allowedModels: null` to skip the allowlist check.
 */
export async function routeToCliRunner(
  model: string,
  messages: ChatMessage[],
  timeoutMs: number,
  opts: RouteOptions = {}
): Promise<CliToolResult> {
  const prompt = formatPrompt(messages);
  const hasTools = !!(opts.tools?.length);

  // Strip "vllm/" prefix if present — OpenClaw sends the full provider path
  // (e.g. "vllm/cli-claude/claude-sonnet-4-6") but the router only needs the
  // "cli-<type>/<model>" portion.
  const normalized = model.startsWith("vllm/") ? model.slice(5) : model;

  // T-103: enforce allowlist unless explicitly disabled
  const allowedModels = opts.allowedModels === undefined
    ? DEFAULT_ALLOWED_CLI_MODELS
    : opts.allowedModels;

  if (allowedModels !== null && !allowedModels.has(normalized)) {
    const known = [...(allowedModels)].join(", ");
    throw new Error(
      `CLI bridge model not allowed: "${model}". Allowed: ${known || "(none)"}.`
    );
  }

  // Resolve aliases (e.g. gemini-3-pro → gemini-3-pro-preview) after allowlist check
  const resolved = normalizeModelAlias(normalized);

  const log = opts.log;
  let rawText: string;
  if (resolved.startsWith("cli-gemini/"))        rawText = await runGemini(prompt, resolved, timeoutMs, opts.workdir, { tools: opts.tools, log });
  else if (resolved.startsWith("cli-claude/"))   rawText = await runClaude(prompt, resolved, timeoutMs, opts.workdir, { tools: opts.tools, log });
  else if (resolved.startsWith("openai-codex/")) rawText = await runCodex(prompt, resolved, timeoutMs, opts.workdir, { tools: opts.tools, mediaFiles: opts.mediaFiles, log });
  else if (resolved.startsWith("opencode/"))     rawText = await runOpenCode(prompt, resolved, timeoutMs, opts.workdir, { log });
  else if (resolved.startsWith("pi/"))           rawText = await runPi(prompt, resolved, timeoutMs, opts.workdir, { log });
  else throw new Error(
    `Unknown CLI bridge model: "${model}". Use "vllm/cli-gemini/<model>", "vllm/cli-claude/<model>", "openai-codex/<model>", "opencode/<model>", or "pi/<model>".`
  );

  // When tools were provided, try to parse structured tool_calls from the response
  if (hasTools) {
    return parseToolCallResponse(rawText);
  }

  // No tools — wrap plain text
  return { content: rawText };
}

// ──────────────────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────────────────

function stripPrefix(modelId: string): string {
  const slash = modelId.indexOf("/");
  return slash === -1 ? modelId : modelId.slice(slash + 1);
}
