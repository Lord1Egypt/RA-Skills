export class UsageError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "UsageError";
  }
}

export const COMMANDS = ["doctor", "report", "compare", "live", "query", "fields", "properties"] as const;

/**
 * Names that must never become flags.
 *
 * These four settings weaken the privacy defaults. A flag can be set by the
 * model, and dimension values are authored by site visitors, so a page title is
 * a channel for talking an agent into passing one. They are environment
 * variables so that a person sets them.
 *
 * Each setting is listed under both spellings a model could plausibly reach
 * for: the environment variable name lowercased (GA4_REDACT -> redact,
 * GA4_ALLOW_USER_DIMENSIONS -> allow-user-dimensions, GA4_PROPERTY_ALLOWLIST
 * -> property-allowlist, GA4_AUDIT_LOG -> audit-log) and the internal config
 * field name it fills (redaction -> redaction, auditLogPath ->
 * audit-log-path). property-allow-list covers the common alternative
 * hyphenation of "allowlist". Extra names here only ever improve the error
 * message, so err toward including one too many.
 */
export const FORBIDDEN_FLAGS = [
  "redact", "no-redact", "redaction", "no-redaction",
  "allow-user-dimensions", "allow-user-identifying-dimensions",
  "property-allowlist", "property-allow-list",
  "audit-log", "audit-log-path",
] as const;

/**
 * report, compare and live all take a preset id as their positional
 * (ReportParams.report, CompareParams.report and RealtimeParams.breakdown in
 * src/tools/reports.ts). Every other command's positional is free text passed
 * straight to Google or matched literally (FieldsParams.query in
 * src/tools/discovery.ts, for one), so rewriting its hyphens would silently
 * change what the user asked for.
 */
const NORMALIZE_ID_COMMANDS = new Set(["report", "compare", "live"]);

/**
 * The flags each command accepts. Every name here must reach a real field on
 * the operation's parameter type in src/tools/reports.ts or
 * src/tools/discovery.ts (checked by src/cli/main.test.ts's "every KNOWN_FLAGS
 * entry reaches a real field" suite), with one deliberate exception: "json"
 * selects markdown vs JSON output in dispatch itself (src/cli/main.ts), not a
 * field on any parameter type, so it never becomes one. Every operation here
 * returns structured `details` alongside its markdown, so every command that
 * declares "json" can produce it; none needed to drop the flag instead.
 * A name listed here that dispatch never reads is exactly the defect
 * README.md calls out in a competing tool: a parameter that parses
 * successfully and is then silently dropped, rather than raising or doing
 * what it says.
 *
 * compare previously listed "against" and "filter" here. Neither has ever had
 * a field on CompareParams to land in (no way to choose the comparison period,
 * and no filtering capability on compare at all), so both parsed successfully
 * and vanished. Removed; the existing unknown-option error now names them
 * correctly, and adding either back is new feature work on CompareParams and
 * runCompare, not an args.ts change.
 */
export const KNOWN_FLAGS: Record<string, readonly string[]> = {
  doctor: ["json"],
  report: ["property", "range", "start", "end", "limit", "filter", "json"],
  compare: ["property", "range", "limit", "json"],
  live: ["property", "limit", "json"],
  query: ["property", "dimensions", "metrics", "range", "start", "end", "limit", "filter", "sort", "json"],
  fields: ["property", "kind", "json"],
  properties: ["json"],
};

export type ParsedArgs =
  | { kind: "help"; command?: string }
  | { kind: "version" }
  | { kind: "command"; command: string; positional: string[]; flags: Record<string, string | boolean> };

export function parseArgs(argv: string[]): ParsedArgs {
  if (argv.length === 0 || argv[0] === "--help" || argv[0] === "-h") return { kind: "help" };
  if (argv[0] === "--version" || argv[0] === "-V") return { kind: "version" };

  const command = argv[0]!;
  if (!(COMMANDS as readonly string[]).includes(command)) {
    throw new UsageError(
      `unknown command ${JSON.stringify(command)}. Valid commands are: ${COMMANDS.join(", ")}.`,
    );
  }

  const positional: string[] = [];
  const flags: Record<string, string | boolean> = {};
  const allowed = KNOWN_FLAGS[command]!;
  let literal = false;

  for (let i = 1; i < argv.length; i += 1) {
    const token = argv[i]!;

    if (literal) { positional.push(token); continue; }
    if (token === "--") { literal = true; continue; }
    if (token === "--help" || token === "-h") return { kind: "help", command };

    if (!token.startsWith("--")) {
      positional.push(NORMALIZE_ID_COMMANDS.has(command) ? normalizeId(token) : token);
      continue;
    }

    const body = token.slice(2);
    const eq = body.indexOf("=");
    const name = eq === -1 ? body : body.slice(0, eq);

    if ((FORBIDDEN_FLAGS as readonly string[]).includes(name)) {
      throw new UsageError(
        `--${name} is not a flag. It changes a privacy default, so it is set by a person ` +
          `through an environment variable, not by an agent on a command line. ` +
          `See the Privacy section of SKILL.md.`,
      );
    }
    if (!allowed.includes(name)) {
      throw new UsageError(
        `unknown option --${name} for ${command}. Valid options are: ` +
          `${allowed.map((f) => `--${f}`).join(", ")}.`,
      );
    }

    if (eq !== -1) { flags[name] = body.slice(eq + 1); continue; }
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) { flags[name] = true; continue; }
    flags[name] = next;
    i += 1;
  }

  return { kind: "command", command, positional, flags };
}

/** Preset ids are snake_case; a model writes hyphens more often than underscores. */
function normalizeId(value: string): string {
  return /^[a-z0-9]+(-[a-z0-9]+)+$/.test(value) ? value.replaceAll("-", "_") : value;
}
