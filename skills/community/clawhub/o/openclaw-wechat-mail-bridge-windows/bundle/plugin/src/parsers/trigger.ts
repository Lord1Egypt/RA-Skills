import { extractEmails } from "./email";

export type TriggerDecision =
  | { kind: "ignore"; reason: string }
  | { kind: "clarify"; reason: string; emails?: string[] }
  | { kind: "findLatest"; email: string }
  | { kind: "waitForNew"; email: string; timeoutSec: number };

export interface TriggerParseOptions {
  triggerPrefixes: string[];
  passiveSingleEmailMode: boolean;
  defaultWaitTimeoutSec: number;
}

function isWatchPrefix(prefix: string): boolean {
  const p = prefix.toLowerCase();
  return p.includes("watch") || p.includes("监控") || p.includes("mail-watch");
}

function parseTimeoutFromTail(rest: string, fallback: number): number {
  const tokens = rest.split(/\s+/).filter((item) => item.length > 0);
  if (tokens.length === 0) {
    return fallback;
  }

  const last = tokens[tokens.length - 1];
  if (!/^\d{1,5}$/.test(last)) {
    return fallback;
  }

  return Math.min(3600, Math.max(5, Number(last)));
}

function parseTriggeredCommand(
  rest: string,
  commandMode: "findLatest" | "waitForNew",
  options: TriggerParseOptions
): TriggerDecision {
  const emails = extractEmails(rest);
  if (emails.length === 0) {
    return { kind: "clarify", reason: "missing_email" };
  }
  if (emails.length > 1) {
    return { kind: "clarify", reason: "multiple_emails", emails };
  }

  if (commandMode === "waitForNew") {
    return {
      kind: "waitForNew",
      email: emails[0],
      timeoutSec: parseTimeoutFromTail(rest, options.defaultWaitTimeoutSec)
    };
  }
  return { kind: "findLatest", email: emails[0] };
}

export function parseTrigger(text: string, options: TriggerParseOptions): TriggerDecision {
  const content = text.trim();
  if (content.length === 0) {
    return { kind: "ignore", reason: "empty_message" };
  }

  const sortedPrefixes = [...options.triggerPrefixes].sort((a, b) => b.length - a.length);
  for (const prefix of sortedPrefixes) {
    if (!content.startsWith(prefix)) {
      continue;
    }

    const rest = content.slice(prefix.length).trim();
    const mode = isWatchPrefix(prefix) ? "waitForNew" : "findLatest";
    return parseTriggeredCommand(rest, mode, options);
  }

  if (!options.passiveSingleEmailMode) {
    return { kind: "ignore", reason: "not_triggered" };
  }

  const emails = extractEmails(content);
  if (emails.length === 0) {
    return { kind: "ignore", reason: "no_email_in_passive_mode" };
  }
  if (emails.length > 1) {
    return { kind: "clarify", reason: "multiple_emails", emails };
  }

  return { kind: "findLatest", email: emails[0] };
}
