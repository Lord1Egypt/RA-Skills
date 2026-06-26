import { normalizeLowercaseStringOrEmpty } from "openclaw/plugin-sdk/text-runtime";

const STREAM_TOPIC_SEP = "#";

/**
 * Parse a "stream#topic" string into its parts.
 * The stream portion is required; topic is optional.
 */
export function parseStreamTopic(target: string): { stream: string; topic?: string } | undefined {
  const trimmed = target.trim();
  if (!trimmed) {
    return undefined;
  }
  const idx = trimmed.indexOf(STREAM_TOPIC_SEP);
  if (idx < 0) {
    // No separator — treat as stream-only if it doesn't look like a numeric user id
    return undefined;
  }
  const stream = trimmed.slice(0, idx).trim();
  if (!stream) {
    return undefined;
  }
  const topic = trimmed.slice(idx + 1).trim() || undefined;
  return { stream, topic };
}

/** Format a stream and optional topic into the canonical "stream#topic" form. */
export function formatStreamTopic(stream: string, topic?: string): string {
  if (topic) {
    return `${stream}${STREAM_TOPIC_SEP}${topic}`;
  }
  return stream;
}

/** Returns true if the target string contains a stream#topic separator. */
export function isStreamTarget(target: string): boolean {
  return target.includes(STREAM_TOPIC_SEP);
}

/**
 * Normalize a raw messaging target string into a canonical Zulip target.
 *
 * Accepted forms:
 * - Full qualified: "zulip:<account>:group:<stream>#<topic>"
 * - Full qualified DM: "zulip:<account>:direct:<user_id>"
 * - Medium: "group:<stream>#<topic>" or "direct:<user_id>"
 * - Short: "stream#topic" or "user_id"
 *
 * Returns undefined for empty or unparseable input.
 */
export function normalizeZulipMessagingTarget(raw: string): string | undefined {
  const trimmed = raw.trim();
  if (!trimmed) {
    return undefined;
  }
  let target = trimmed;
  const lowered = normalizeLowercaseStringOrEmpty(target);

  // Strip "zulip:" prefix (and optional account segment)
  if (lowered.startsWith("zulip:")) {
    target = target.slice("zulip:".length).trim();
    // Strip account segment: everything up to next ":" if followed by group:/direct:
    const nextColon = target.indexOf(":");
    if (nextColon > 0) {
      const afterAccount = normalizeLowercaseStringOrEmpty(target.slice(nextColon + 1));
      if (afterAccount.startsWith("group:") || afterAccount.startsWith("direct:")) {
        target = target.slice(nextColon + 1).trim();
      }
    }
  }

  const targetLower = normalizeLowercaseStringOrEmpty(target);

  // Handle "group:<stream>#<topic>"
  if (targetLower.startsWith("group:")) {
    target = target.slice("group:".length).trim();
    if (!target) {
      return undefined;
    }
    return target;
  }

  // Handle "direct:<user_id>"
  if (targetLower.startsWith("direct:")) {
    target = target.slice("direct:".length).trim();
    if (!target) {
      return undefined;
    }
    return target;
  }

  // Short form — return as-is if non-empty
  return target || undefined;
}

/** Normalize a single allowlist entry, stripping prefixes and lowercasing. */
export function normalizeZulipAllowEntry(raw: string): string {
  let value = normalizeLowercaseStringOrEmpty(raw);
  if (!value) {
    return "";
  }
  if (value.startsWith("zulip:")) {
    value = value.slice("zulip:".length);
  }
  if (value.startsWith("direct:")) {
    value = value.slice("direct:".length);
  }
  if (value.startsWith("group:")) {
    value = value.slice("group:".length);
  }
  return value.trim();
}

/** Normalize an entire allowlist array. */
export function normalizeZulipAllowlist(entries?: Array<string | number>): string[] {
  return (entries ?? []).map((entry) => normalizeZulipAllowEntry(String(entry))).filter(Boolean);
}
