/**
 * config.ts
 *
 * Central configuration defaults for the CLI bridge plugin.
 * All magic numbers, timeouts, paths, and constants live here.
 * Import from this module instead of scattering literals across the codebase.
 *
 * Values can be overridden at runtime via openclaw.plugin.json configSchema
 * or via the CliPluginConfig interface in index.ts.
 */

import { homedir, tmpdir } from "node:os";
import { join } from "node:path";

// ──────────────────────────────────────────────────────────────────────────────
// Proxy server
// ──────────────────────────────────────────────────────────────────────────────

/** Default port for the local OpenAI-compatible proxy server. */
export const DEFAULT_PROXY_PORT = 31337;

/** Default API key between OpenClaw vllm provider and the proxy. */
export const DEFAULT_PROXY_API_KEY = "cli-bridge";

/** Default base timeout for CLI subprocess responses (ms). Scales dynamically. */
export const DEFAULT_PROXY_TIMEOUT_MS = 300_000; // 5 min

/** Maximum effective timeout after dynamic scaling (ms). */
export const MAX_EFFECTIVE_TIMEOUT_MS = 900_000; // 15 min

/** Extra timeout per message beyond 10 in the conversation (ms). */
export const TIMEOUT_PER_EXTRA_MSG_MS = 2_000;

/** Extra timeout per tool definition in the request (ms). */
export const TIMEOUT_PER_TOOL_MS = 7_000;

/** SSE keepalive interval — prevents OpenClaw read-timeout during long CLI runs (ms). */
export const SSE_KEEPALIVE_INTERVAL_MS = 15_000;

// ──────────────────────────────────────────────────────────────────────────────
// CLI subprocess
// ──────────────────────────────────────────────────────────────────────────────

/** Default timeout for individual CLI subprocess invocations (ms). */
export const DEFAULT_CLI_TIMEOUT_MS = 120_000; // 2 min

/** Grace period between SIGTERM and SIGKILL when a timeout fires (ms). */
export const TIMEOUT_GRACE_MS = 5_000;

/** Max messages to include in the prompt sent to CLI subprocesses. */
export const MAX_MESSAGES = 20;

/** Max characters per message content before truncation. */
export const MAX_MSG_CHARS = 4_000;

// ──────────────────────────────────────────────────────────────────────────────
// Session manager (long-running sessions)
// ──────────────────────────────────────────────────────────────────────────────

/** Auto-cleanup threshold: sessions older than this are killed and removed (ms). */
export const SESSION_TTL_MS = 30 * 60 * 1_000; // 30 min

/** Interval for the session cleanup sweep (ms). */
export const CLEANUP_INTERVAL_MS = 5 * 60 * 1_000; // 5 min

/** Grace period between SIGTERM and SIGKILL for session termination (ms). */
export const SESSION_KILL_GRACE_MS = 5_000;

// ──────────────────────────────────────────────────────────────────────────────
// Provider sessions (persistent session registry)
// ──────────────────────────────────────────────────────────────────────────────

/** Default TTL for provider sessions before they're considered stale (ms). */
export const PROVIDER_SESSION_TTL_MS = 2 * 60 * 60 * 1_000; // 2 hours

/** Sweep interval for stale provider sessions (ms). */
export const PROVIDER_SESSION_SWEEP_MS = 10 * 60 * 1_000; // 10 min

// ──────────────────────────────────────────────────────────────────────────────
// Per-model timeout defaults (ms)
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Default per-model timeout overrides.
 * These are applied as the base timeout before dynamic scaling.
 * Override via `modelTimeouts` in plugin config.
 *
 * Strategy:
 *   - Heavy/agentic models (Opus, GPT-5.4): 5 min — need time for tool use
 *   - Standard interactive (Sonnet, Pro, GPT-5.3): 3 min
 *   - Fast/lightweight (Haiku, Flash, Mini): 90s
 */
export const DEFAULT_MODEL_TIMEOUTS: Record<string, number> = {
  "cli-claude/claude-opus-4-6":        300_000,  // 5 min
  "cli-claude/claude-sonnet-4-6":      300_000,  // 5 min — match idleTimeoutSeconds
  "cli-claude/claude-haiku-4-5":        90_000,  // 90s
  "cli-gemini/gemini-2.5-pro":         300_000,  // 5 min — image generation needs more time
  "cli-gemini/gemini-2.5-flash":       180_000,  // 3 min
  "cli-gemini/gemini-3-pro-preview":   300_000,  // 5 min — image generation needs more time
  "cli-gemini/gemini-3-flash-preview": 180_000,  // 3 min
  "openai-codex/gpt-5.4":             300_000,
  "openai-codex/gpt-5.3-codex":       180_000,
  "openai-codex/gpt-5.1-codex-mini":   90_000,
  "gemini-api/gemini-2.5-pro":        300_000,  // 5 min — image generation needs time
  "gemini-api/gemini-2.5-flash":      180_000,  // 3 min
};

// ──────────────────────────────────────────────────────────────────────────────
// Model fallback chain
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Default fallback chain: when a primary model fails (timeout, error),
 * retry once with the lighter variant.
 */
export const DEFAULT_MODEL_FALLBACKS: Record<string, string> = {
  "cli-gemini/gemini-2.5-pro":        "cli-gemini/gemini-2.5-flash",
  "cli-gemini/gemini-3-pro-preview":  "cli-gemini/gemini-3-flash-preview",
  "cli-claude/claude-opus-4-6":       "cli-claude/claude-sonnet-4-6",
  "cli-claude/claude-sonnet-4-6":     "cli-claude/claude-haiku-4-5",
  "gemini-api/gemini-2.5-pro":       "gemini-api/gemini-2.5-flash",
};

// ──────────────────────────────────────────────────────────────────────────────
// Paths
// ──────────────────────────────────────────────────────────────────────────────

/** Base directory for all CLI bridge state files. */
export const OPENCLAW_DIR = join(homedir(), ".openclaw");

/** State file — persists the model active before the last /cli-* switch. */
export const STATE_FILE = join(OPENCLAW_DIR, "cli-bridge-state.json");

/** Pending switch file — stores a staged model switch not yet applied. */
export const PENDING_FILE = join(OPENCLAW_DIR, "cli-bridge-pending.json");

/** Provider session registry file. */
export const PROVIDER_SESSIONS_FILE = join(OPENCLAW_DIR, "cli-bridge", "sessions.json");

/** Persistent metrics file — survives gateway restarts. */
export const METRICS_FILE = join(OPENCLAW_DIR, "cli-bridge", "metrics.json");

/** Temporary directory for multimodal media files. */
export const MEDIA_TMP_DIR = join(tmpdir(), "cli-bridge-media");

/** Browser profile directories. */
export const PROFILE_DIRS = {
  grok:    join(OPENCLAW_DIR, "grok-profile"),
  gemini:  join(OPENCLAW_DIR, "gemini-profile"),
  claude:  join(OPENCLAW_DIR, "claude-profile"),
  chatgpt: join(OPENCLAW_DIR, "chatgpt-profile"),
} as const;

// ──────────────────────────────────────────────────────────────────────────────
// Browser automation
// ──────────────────────────────────────────────────────────────────────────────

/** Navigation timeout for Playwright page.goto (ms). */
export const BROWSER_NAV_TIMEOUT_MS = 15_000;

/** Delay after page load before interacting (ms). */
export const BROWSER_PAGE_LOAD_DELAY_MS = 2_000;

/** Delay after typing into input fields (ms). */
export const BROWSER_INPUT_DELAY_MS = 300;

/** Default timeout for browser-based completions (ms). */
export const BROWSER_COMPLETION_TIMEOUT_MS = 120_000;

/** Consecutive stable reads to confirm a streaming response is done. */
export const BROWSER_STABLE_CHECKS = 3;

/** Interval between stability checks (ms). */
export const BROWSER_STABLE_INTERVAL_MS = 500;

/** Gemini uses a longer stability interval due to slower streaming. */
export const GEMINI_STABLE_INTERVAL_MS = 600;

// ──────────────────────────────────────────────────────────────────────────────
// Claude auth
// ──────────────────────────────────────────────────────────────────────────────

/** Refresh OAuth token this many ms before expiry. */
export const CLAUDE_REFRESH_BEFORE_EXPIRY_MS = 30 * 60 * 1_000; // 30 min

/** Sync window for token refresh (ms). */
export const CLAUDE_REFRESH_SYNC_WINDOW_MS = 5 * 60 * 1_000; // 5 min

/** Max wait for a single token refresh attempt (ms). */
export const CLAUDE_REFRESH_TIMEOUT_MS = 30_000;

/** Polling interval for proactive token refresh (ms). */
export const CLAUDE_REFRESH_POLL_INTERVAL_MS = 10 * 60 * 1_000; // 10 min

// ──────────────────────────────────────────────────────────────────────────────
// Workdir isolation
// ──────────────────────────────────────────────────────────────────────────────

/** Prefix for temporary workdir directories. */
export const WORKDIR_PREFIX = "cli-bridge-";

/** Max age for orphaned workdirs before they are swept (ms). */
export const WORKDIR_ORPHAN_MAX_AGE_MS = 60 * 60 * 1_000; // 1 hour

// ──────────────────────────────────────────────────────────────────────────────
// BitNet
// ──────────────────────────────────────────────────────────────────────────────

/** Default URL for the local BitNet llama-server. */
export const DEFAULT_BITNET_SERVER_URL = "http://127.0.0.1:8082";

/** Max messages to send to BitNet (4096 token context limit). */
export const BITNET_MAX_MESSAGES = 6;

/** Minimal system prompt for BitNet to conserve tokens. */
export const BITNET_SYSTEM_PROMPT =
  "You are Akido, a concise AI assistant. Answer briefly and directly. Current user: Emre. Timezone: Europe/Berlin.";

// ──────────────────────────────────────────────────────────────────────────────
// Default model for /cli-test
// ──────────────────────────────────────────────────────────────────────────────

export const CLI_TEST_DEFAULT_MODEL = "cli-claude/claude-sonnet-4-6";
