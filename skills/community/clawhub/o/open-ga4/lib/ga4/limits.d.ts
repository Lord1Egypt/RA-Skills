import { type AccessPolicy } from "../privacy/policy.js";
import { Ga4Error } from "./errors.js";
/**
 * Request limits and the metric renames, enforced before a socket is opened.
 *
 * Failing locally matters more than it looks: Google counts client errors
 * against a budget of 10,000 per 15 minutes per project-and-property pair, and
 * exhausting it blocks that pair entirely. A request we know is invalid must
 * never be sent.
 */
export declare const LIMITS: {
    /** Google's documented per-request ceilings. */
    readonly MAX_DIMENSIONS: 9;
    readonly MAX_METRICS: 10;
    readonly MAX_DATE_RANGES: 4;
    readonly MAX_MINUTE_RANGES: 2;
    readonly ROW_LIMIT_MAX: 250000;
    readonly ROW_LIMIT_DEFAULT: 10000;
    readonly MINUTES_AGO_MAX: 29;
    /** Our own, tighter ceilings, so a report stays readable and cheap in tokens. */
    readonly DEFAULT_ROWS: 25;
    readonly MAX_ROWS: 1000;
};
/**
 * Names Google retired, mapped to their replacements.
 *
 * Models were trained on years of documentation using the old names, so
 * `conversions` is what they reach for. Rewriting silently is kinder than a
 * 400, and the rewrite is reported in the result so nobody is misled about
 * which metric was actually read.
 */
export declare const RENAMED_FIELDS: Readonly<Record<string, string>>;
export type FieldRewrite = {
    from: string;
    to: string;
};
/** Apply the rename table, reporting what changed. */
export declare function applyRenames(names: readonly string[]): {
    names: string[];
    rewrites: FieldRewrite[];
};
/**
 * A request the client can already tell Google would reject: too many
 * dimensions, an empty request, a filter value that will not parse, and so on.
 *
 * Extends Ga4Error, rather than a plain Error, so it carries the same exit
 * code as every other bad-input failure: `code` is fixed at INVALID_REQUEST,
 * which exitCodeFor already maps to exit 2. Before this, a plain Error here
 * fell through diagnose()'s generic "UNEXPECTED" bucket and read as a refusal
 * from Google that was never asked for; nothing here ever reaches a network
 * call. `reason` keeps the specific check that failed (EMPTY_REQUEST,
 * TOO_MANY_DIMENSIONS, BAD_FILTER_VALUE, ...) for anyone who wants more detail
 * than "invalid request"; it does not affect the exit code.
 */
export declare class Ga4RequestError extends Ga4Error {
    readonly reason: string;
    constructor(reason: string, message: string);
}
export type ReportShape = {
    dimensions: readonly string[];
    metrics: readonly string[];
    dateRangeCount?: number;
    limit?: number;
};
/** Reject a request Google would reject, with a message that says what to do. */
export declare function assertWithinLimits(shape: ReportShape): void;
/**
 * Realtime accepts a small, fixed subset of fields. Rejecting locally turns an
 * opaque 400 into a sentence naming what realtime can actually do.
 */
export declare const REALTIME_DIMENSIONS: ReadonlySet<string>;
export declare const REALTIME_METRICS: ReadonlySet<string>;
/**
 * Everything realtime refuses locally: fields it does not have, and fields it
 * has but that this skill will not ask for by default.
 *
 * The policy check is here rather than at the call site for the reason
 * buildFilters holds its own: the caller that skips it is the defect, and a
 * required argument is what stops one being written. runRealtime was that
 * caller. Nothing could exploit it, because `live` takes only a preset id and
 * every realtime preset's dimensions are constants, but the check was missing
 * from the one command that has a permissive `customUser:` rule of its own,
 * which is the worst place for it to be missing from.
 */
export declare function assertRealtimeFields(dimensions: readonly string[], metrics: readonly string[], policy: AccessPolicy, propertyIdentifying?: ReadonlySet<string>): void;
