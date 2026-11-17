import { configFromEnv } from "../config.js";
import { diagnose } from "../ga4/errors.js";
import { FILTER_OPERATORS } from "../ga4/filters.js";
import { redactText } from "../privacy/redact.js";
import { createRuntime } from "../runtime.js";
import { setupStateFrom } from "../setup/state.js";
import { runCompare, runQuery, runRealtime, runReport } from "../tools/reports.js";
import { runDiagnose, runFields, runProperties } from "../tools/discovery.js";
import { parseArgs, UsageError } from "./args.js";
import { EXIT, exitCodeFor } from "./exit.js";
/**
 * A string literal, not a read of package.json at runtime: package.json is
 * not shipped inside the skill bundle, so a runtime read would work in this
 * checkout and fail after install. src/cli/main.test.ts asserts this equals
 * package.json's version, so the two cannot silently drift apart.
 */
export const VERSION = "0.2.1";
const USAGE = `open-ga4: read-only Google Analytics 4 answers.

Usage: node <skill-dir>/lib/cli.js <command> [options]

Commands:
  doctor [--json]            Check setup and report the one thing to fix next
  report <preset>            One ready-made report
  compare <preset>           The same report across two periods
  live [breakdown]           Active users in roughly the last 30 minutes
  query                      Explicit dimensions, metrics, filters and sort
  fields <search>            Search the property's live field catalog
  properties                 List the properties this credential can read

query's --filter is one condition, field:operator:value (for example
country:exact:US). The split is found by locating the operator, not by
counting colons, so both sides of it may contain colons of their own: a value
may be a full URL (pageLocation and pageReferrer are URLs), and a field may be
a custom dimension, which always has a colon in its name (customUser:<name>,
customEvent:<name>, customItem:<name>). Operators: ${FILTER_OPERATORS.join(", ")}.

Run a command with --help for its options.
Settings live in the environment; see SKILL.md.
`;
export async function main(argv, env, streams) {
    let parsed;
    try {
        parsed = parseArgs(argv);
    }
    catch (error) {
        // redactText here too, not only on the paths below. A parse failure quotes
        // the argv token it could not read, and argv is the one place a person
        // pastes things: `--property <a key they had on the clipboard>` prints
        // that value back out. redactText is unconditional by design: every one of
        // the four writes in this function goes through it, the success path on
        // stdout included, so there is no path out of this process that skips it.
        streams.err(`error: ${redactText(error instanceof Error ? error.message : String(error))}\n`);
        return EXIT.BAD_INPUT;
    }
    if (parsed.kind === "help") {
        streams.out(USAGE);
        return EXIT.OK;
    }
    if (parsed.kind === "version") {
        streams.out(`${VERSION}\n`);
        return EXIT.OK;
    }
    const warnings = [];
    const config = configFromEnv(env, (m) => warnings.push(m));
    const runtime = createRuntime({ config, env, onWarning: (m) => warnings.push(m) });
    /**
     * Warnings go out on both paths, and through redactText like everything
     * else this process prints.
     *
     * Both halves of that were wrong. They were printed only when the command
     * succeeded, which is backwards: a warning says a setting was ignored, and
     * suppressing it exactly when the command then fails hides the explanation
     * at the moment it is needed (an ignored GA4_PROPERTY_ALLOWLIST entry is
     * why the property was refused, and only the warning says so). And they were
     * printed raw, although they quote values a person typed:
     * configFromEnv echoes the allowlist entry it rejected, and the audit-log
     * warning carries a path.
     */
    const flushWarnings = () => {
        for (const warning of warnings)
            streams.err(`warning: ${redactText(warning)}\n`);
        warnings.length = 0;
    };
    try {
        const result = await dispatch(runtime, parsed);
        flushWarnings();
        // The success path too, which is what makes "no path out of this process
        // skips redactText" above a statement about the code rather than about the
        // error paths. It was not true when written: this line printed `result`
        // raw. Nothing was leaking, because what reaches here is rows redaction
        // already cleaned plus prose this skill wrote, and doctor's checks redact
        // at construction. But an invariant that holds by coincidence of what the
        // callers happen to pass is not an invariant, and the next writer of a
        // message on this path would have had no way to know it was the one path
        // without a net. redactText is idempotent (a second pass over
        // "[redacted]" matches nothing), so the paths that already redact are
        // unaffected, and it only ever removes a private key block, a secret JSON
        // field or a bearer token, none of which belongs in a report.
        streams.out(redactText(result.endsWith("\n") ? result : `${result}\n`));
        return EXIT.OK;
    }
    catch (error) {
        flushWarnings();
        if (error instanceof UsageError) {
            // A UsageError raised while converting flags in dispatch (a missing
            // positional, a --limit that is not a number) is the same kind of
            // problem as one from parseArgs: bad input, entirely local, nothing to
            // do with Google. It gets the same exit code, so the agent does not go
            // looking for a machine-readable reason from Google that was never
            // asked for.
            streams.err(`error: ${redactText(error.message)}\n`);
            return EXIT.BAD_INPUT;
        }
        // Never let a traceback reach the user: it names the wrong problem. The
        // taxonomy already maps every known failure to a sentence with a fix, and
        // redactText keeps a credential out of the message on every path.
        const named = diagnose(error, { principal: runtime.principal() });
        streams.err(`error: ${redactText(named.toString())}\n`);
        return exitCodeFor(named);
    }
}
/** A flag's raw value, or undefined if it was not given. Every flag this CLI
 * defines takes a value, so one given bare (`--property` with nothing after
 * it) is a mistake worth naming rather than silently coercing. */
function str(flags, name) {
    const value = flags[name];
    if (value === undefined)
        return undefined;
    if (typeof value !== "string") {
        throw new UsageError(`--${name} needs a value.`);
    }
    return value;
}
/** A flag's value as a number. Number(true) is 1, so a bare boolean flag must
 * be rejected explicitly rather than silently read as a limit of 1. */
function num(flags, name) {
    const raw = str(flags, name);
    if (raw === undefined)
        return undefined;
    const value = Number(raw);
    if (!Number.isFinite(value)) {
        throw new UsageError(`--${name} must be a number; ${JSON.stringify(raw)} is not one.`);
    }
    return value;
}
/** A flag's value split on commas, trimmed, empty entries dropped. */
function csv(flags, name) {
    const raw = str(flags, name);
    if (raw === undefined)
        return undefined;
    return raw.split(",").map((entry) => entry.trim()).filter((entry) => entry.length > 0);
}
const FIELD_KINDS = ["any", "dimension", "metric"];
function kindFlag(flags) {
    const raw = str(flags, "kind");
    if (raw === undefined)
        return undefined;
    if (!FIELD_KINDS.includes(raw)) {
        throw new UsageError(`--kind must be one of ${FIELD_KINDS.join(", ")}; got ${JSON.stringify(raw)}.`);
    }
    return raw;
}
/**
 * Locates the `field:operator:value` split in a raw --filter expression by
 * finding the operator, not by counting colons.
 *
 * An earlier version split on the first two colons, so the value could carry
 * its own colons (a URL's scheme separator, for pageLocation and
 * pageReferrer). That was correct as far as it went, but it assumed a field
 * name never contains a colon, and GA4 custom dimensions all do:
 * `customUser:<name>`, `customEvent:<name>`, `customItem:<name>`. Counting
 * colons split `customEvent:plan_tier:exact:pro` into field `customEvent`,
 * operator `plan_tier`, which is not a real operator, so no custom dimension
 * could be filtered at all, and `customUser:` filters (which the privacy
 * policy in src/privacy/policy.ts refuses) were rejected as malformed input
 * before that check ever ran.
 *
 * Splitting on the operator's identity fixes both: try each colon-delimited
 * segment as the candidate operator, keep only the ones that are a real
 * FILTER_OPERATORS name with a non-empty field before it and a non-empty
 * value after it, and use the rightmost one that qualifies. Rightmost, to
 * make the one genuinely ambiguous shape deterministic: a field whose own
 * text happens to equal an operator name, such as
 * `customEvent:exact:exact:pro`, could split at either "exact". A field name
 * is a fixed GA4 identifier and the value is arbitrary text the caller typed,
 * so the reading that keeps more of the leading text in the field (here,
 * field `customEvent:exact`, not `customEvent`) is the one more often meant,
 * and it is the same reading that already handles the ordinary
 * `customEvent:plan_tier:exact:pro` case correctly. Trying candidates from
 * the right is what makes that the first (and so the chosen) match.
 *
 * A value's own colons still survive intact: this only ever treats one
 * segment as the operator, so anything after it, colons included, rejoins
 * into the value untouched.
 *
 * An unknown operator, an empty field, an empty value and a missing
 * separator all fall out of this the same way, as "no segment qualifies",
 * and are reported with one message that echoes the input and lists the
 * valid operators, exactly as before.
 */
function splitFilterExpression(raw) {
    const segments = raw.split(":");
    // i is the candidate operator's index. It needs at least one segment
    // before it (the field) and at least one after it (the value), so it
    // ranges from 1 to segments.length - 2; trying the largest first is what
    // makes the rightmost qualifying split the one returned.
    for (let i = segments.length - 2; i >= 1; i -= 1) {
        const op = segments[i];
        if (!FILTER_OPERATORS.includes(op))
            continue;
        const field = segments.slice(0, i).join(":");
        const value = segments.slice(i + 1).join(":");
        if (field === "" || value === "")
            continue;
        return { field, op: op, value };
    }
    return undefined;
}
/**
 * query's --filter is one condition, `field:operator:value` (for example
 * `country:exact:US`, or `customEvent:plan_tier:exact:pro` where the field
 * itself contains a colon). See splitFilterExpression above for how the
 * split is found.
 */
function filterFlag(flags) {
    const raw = str(flags, "filter");
    if (raw === undefined)
        return undefined;
    const parsed = splitFilterExpression(raw);
    if (!parsed) {
        throw new UsageError(`--filter must look like field:operator:value (got ${JSON.stringify(raw)}). Operators: ` +
            `${FILTER_OPERATORS.join(", ")}.`);
    }
    return [parsed];
}
/** The first positional argument, or a UsageError pointing at a worked example. */
function requirePositional(positional, example) {
    const value = positional[0];
    if (!value) {
        throw new UsageError(`Missing argument. For example: ${example}`);
    }
    return value;
}
/** Every operation returns `{ markdown, details }`; `--json` selects `details` over `markdown`. */
function output(result, json) {
    return json ? JSON.stringify(result.details, null, 2) : result.markdown;
}
/**
 * A fresh property listing for `no_property_selected`: the one state where
 * the agent must list the options and ask, rather than guess which property
 * the user meant (a confident answer about the wrong website is the worst
 * outcome available here). Fetched again rather than reused from
 * runDiagnose's own check, because that check may have found nothing for a
 * reason that has since cleared.
 *
 * Failing to enumerate is not itself a setup blocker: that already happened,
 * one way or another, before setupStateFrom ever produced
 * "no_property_selected". So a failure here degrades to an empty list
 * rather than throwing or changing `blocked_on`.
 */
async function propertiesToOffer(runtime) {
    try {
        const { details } = await runProperties(runtime, {});
        const { properties } = details;
        return properties.map((property) => ({ id: property.id, name: property.name }));
    }
    catch {
        return [];
    }
}
/**
 * `--json`'s value as the boolean it is: true for a bare `--json` (parseArgs
 * hands that back as the literal boolean `true`) or an explicit truthy
 * spelling, false when the flag was not given at all or was explicitly
 * turned off. `--json=false` must select markdown, not JSON: a value merely
 * being *present* is not the same question as what it says. Same true/false
 * spellings src/config.ts's isTrue/isFalse already use, for one convention
 * across the codebase.
 */
function jsonFlag(flags) {
    const value = flags.json;
    if (value === undefined)
        return false;
    if (typeof value === "boolean")
        return value;
    return !["0", "false", "no", "off"].includes(value.trim().toLowerCase());
}
/**
 * Converts each command's flags into the operation's own parameter object and
 * returns its markdown, or with `--json`, its structured details instead.
 * Kept in this file, not split out: this mapping is what a reviewer most
 * needs to see in one place.
 */
export async function dispatch(runtime, parsed) {
    const { command, positional, flags } = parsed;
    // Read unconditionally, before the switch, so every command's flags object
    // is touched regardless of which branch runs below (src/cli/main.test.ts's
    // "every KNOWN_FLAGS entry reaches a real field" suite checks that every
    // declared flag is actually read).
    const json = jsonFlag(flags);
    switch (command) {
        case "doctor": {
            const result = await runDiagnose(runtime, {});
            if (json) {
                // doctor's own `details` is the raw Check[] the markdown checklist
                // renders from: useful for a person, but still a wall of everything
                // that was checked. setupStateFrom reduces that to the one blocking
                // step, which is what --json is for on this command specifically.
                const { checks } = result.details;
                const state = setupStateFrom(checks, runtime.principal());
                if (state.blocked_on === "no_property_selected") {
                    state.properties = await propertiesToOffer(runtime);
                }
                return JSON.stringify(state, null, 2);
            }
            return result.markdown;
        }
        case "report":
            return output(await runReport(runtime, {
                report: requirePositional(positional, "report overview"),
                property_id: str(flags, "property"),
                date_range: str(flags, "range"),
                start_date: str(flags, "start"),
                end_date: str(flags, "end"),
                limit: num(flags, "limit"),
                filter_contains: str(flags, "filter"),
            }), json);
        case "compare":
            return output(await runCompare(runtime, {
                report: requirePositional(positional, "compare overview"),
                property_id: str(flags, "property"),
                date_range: str(flags, "range"),
                limit: num(flags, "limit"),
            }), json);
        case "live":
            return output(await runRealtime(runtime, {
                breakdown: positional[0],
                property_id: str(flags, "property"),
                limit: num(flags, "limit"),
            }), json);
        case "query":
            return output(await runQuery(runtime, {
                metrics: csv(flags, "metrics") ?? [],
                dimensions: csv(flags, "dimensions"),
                property_id: str(flags, "property"),
                date_range: str(flags, "range"),
                start_date: str(flags, "start"),
                end_date: str(flags, "end"),
                filters: filterFlag(flags),
                order_by: str(flags, "sort"),
                limit: num(flags, "limit"),
            }), json);
        case "fields":
            return output(await runFields(runtime, {
                query: requirePositional(positional, "fields sessions"),
                kind: kindFlag(flags),
                property_id: str(flags, "property"),
            }), json);
        case "properties":
            return output(await runProperties(runtime, {}), json);
        default:
            // Unreachable: parseArgs validates command against COMMANDS before
            // returning a "command" result. Kept so the switch satisfies the
            // compiler's control-flow analysis rather than assuming it.
            throw new Error(`internal error: unhandled command ${JSON.stringify(command)}`);
    }
}
