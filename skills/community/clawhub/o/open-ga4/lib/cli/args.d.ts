export declare class UsageError extends Error {
    constructor(message: string);
}
export declare const COMMANDS: readonly ["doctor", "report", "compare", "live", "query", "fields", "properties"];
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
export declare const FORBIDDEN_FLAGS: readonly ["redact", "no-redact", "redaction", "no-redaction", "allow-user-dimensions", "allow-user-identifying-dimensions", "property-allowlist", "property-allow-list", "audit-log", "audit-log-path"];
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
export declare const KNOWN_FLAGS: Record<string, readonly string[]>;
export type ParsedArgs = {
    kind: "help";
    command?: string;
} | {
    kind: "version";
} | {
    kind: "command";
    command: string;
    positional: string[];
    flags: Record<string, string | boolean>;
};
export declare function parseArgs(argv: string[]): ParsedArgs;
