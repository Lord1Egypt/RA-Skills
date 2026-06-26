import type { MetadataFilter, TopicMetadataUpdate, TopicPriority, TopicStatus } from "./types.ts";

const VALID_STATUSES = new Set<string>(["open", "wip", "blocked", "done", "archived"]);
const VALID_PRIORITIES = new Set<string>(["p0", "p1", "p2", "p3"]);
const SETTABLE_KEYS = new Set(["status", "priority", "assignee", "due_date"]);

export type CommandAction = "show" | "set" | "label" | "list" | "clear";

export type ParsedCommand =
  | { action: "show" }
  | { action: "set"; updates: TopicMetadataUpdate }
  | { action: "label"; op: "add" | "rm"; tag: string }
  | { action: "list"; filter: MetadataFilter }
  | { action: "clear" };

export interface ParseError {
  error: string;
}

export type ParseResult = ParsedCommand | ParseError;

export function isParseError(result: ParseResult): result is ParseError {
  return "error" in result;
}

export function parseMetaCommand(text: string): ParseResult {
  const trimmed = text.trim();
  const match = trimmed.match(/^\/meta(?:\s+(.*))?$/s);
  if (!match) {
    return { error: "Not a /meta command" };
  }

  const rest = (match[1] ?? "").trim();
  if (!rest) {
    return { action: "show" };
  }

  const parts = rest.split(/\s+/);
  const action = parts[0].toLowerCase();

  switch (action) {
    case "show":
      return { action: "show" };

    case "set":
      return parseSet(parts.slice(1));

    case "label":
      return parseLabel(parts.slice(1));

    case "list":
      return parseList(parts.slice(1));

    case "clear":
      return { action: "clear" };

    default:
      return { error: `Unknown action: ${action}` };
  }
}

function parseSet(args: string[]): ParseResult {
  if (args.length === 0) {
    return { error: "Usage: /meta set key=value [key=value ...]" };
  }

  const updates: TopicMetadataUpdate = {};

  for (const arg of args) {
    const eqIdx = arg.indexOf("=");
    if (eqIdx === -1) {
      return { error: `Invalid key=value pair: ${arg}` };
    }
    const key = arg.slice(0, eqIdx).toLowerCase();
    const value = arg.slice(eqIdx + 1);

    if (!SETTABLE_KEYS.has(key)) {
      return { error: `Unknown field: ${key}. Valid fields: ${[...SETTABLE_KEYS].join(", ")}` };
    }

    switch (key) {
      case "status":
        if (!VALID_STATUSES.has(value)) {
          return { error: `Invalid status: ${value}. Valid: ${[...VALID_STATUSES].join(", ")}` };
        }
        updates.status = value as TopicStatus;
        break;
      case "priority":
        if (!VALID_PRIORITIES.has(value)) {
          return {
            error: `Invalid priority: ${value}. Valid: ${[...VALID_PRIORITIES].join(", ")}`,
          };
        }
        updates.priority = value as TopicPriority;
        break;
      case "assignee":
        updates.assignee = value || null;
        break;
      case "due_date":
        updates.due_date = value || null;
        break;
    }
  }

  return { action: "set", updates };
}

function parseLabel(args: string[]): ParseResult {
  if (args.length < 2) {
    return { error: "Usage: /meta label add <tag> | /meta label rm <tag>" };
  }

  const op = args[0].toLowerCase();
  if (op !== "add" && op !== "rm") {
    return { error: `Invalid label operation: ${op}. Use 'add' or 'rm'` };
  }

  const tag = args.slice(1).join(" ");
  return { action: "label", op, tag };
}

function parseList(args: string[]): ParseResult {
  const filter: MetadataFilter = {};

  for (const arg of args) {
    const eqIdx = arg.indexOf("=");
    if (eqIdx === -1) {
      return { error: `Invalid filter: ${arg}. Use key=value format` };
    }
    const key = arg.slice(0, eqIdx).toLowerCase();
    const value = arg.slice(eqIdx + 1);

    switch (key) {
      case "status":
        if (!VALID_STATUSES.has(value)) {
          return { error: `Invalid status filter: ${value}` };
        }
        filter.status = value as TopicStatus;
        break;
      case "assignee":
        filter.assignee = value;
        break;
      case "label":
        filter.label = value;
        break;
      default:
        return { error: `Unknown filter: ${key}. Valid: status, assignee, label` };
    }
  }

  return { action: "list", filter };
}
