/** Default constants for the Zulip adapter. */

export const DEFAULT_STREAM = "general";
export const DEFAULT_TOPIC = "general";
export const DEFAULT_TIMEOUT_MS = 90_000;

/** Topic prefix conventions (Phase 1 — no DB, convention-based). */
export const TOPIC_PREFIX = {
  RESOLVED: "✔ ",
  BLOCKED: "🔴 ",
  PINNED: "📌 ",
} as const;
