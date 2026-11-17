import { Ga4Error } from "./errors.js";
/**
 * Date range parsing.
 *
 * A GA4 property reports in *its own* timezone, which is frequently not the
 * timezone of the machine running OpenClaw. Computing "yesterday" locally and
 * sending an absolute date is how integrations end up quietly off by one day.
 *
 * The API accepts relative tokens (`today`, `yesterday`, `NdaysAgo`) and
 * resolves them in the property's timezone. So the rule here is: emit a
 * relative token whenever the request is relative, and fall back to absolute
 * dates only for calendar boundaries ("last month") that have no token form.
 * Those carry an explicit note about which timezone was used.
 */
export type Ga4DateRange = {
    /** `YYYY-MM-DD`, `NdaysAgo`, `yesterday`, or `today`. */
    startDate: string;
    endDate: string;
    /** Human label for the rendered report header. */
    label: string;
    /** Set when boundaries were computed locally rather than resolved by Google. */
    timezoneNote?: string;
};
/**
 * A date range this module could not read, or read as impossible.
 *
 * Extends Ga4Error, rather than a plain Error, for the same reason
 * Ga4RequestError in src/ga4/limits.ts does (read the comment there; this is
 * the same defect, found again in a second class that was not brought along
 * with the first). A plain Error falls through diagnose() into the generic
 * "UNEXPECTED" bucket, which carries the fix "Run doctor to check the setup"
 * and the exit code for "Google refused". Parsing happens entirely on this
 * machine and never touches a socket, so a mistyped range was being reported
 * to somebody as Google turning them down, with a fix that could not help.
 *
 * INVALID_REQUEST, so it exits 2: name the value that was rejected and the
 * forms that are accepted, and do not retry with a different guess.
 */
export declare class DateRangeError extends Ga4Error {
    constructor(input: string, message?: string);
}
/**
 * Parse a human date-range expression into GA4 request fields.
 *
 * @param today Reference date. Injected so tests do not depend on the clock.
 */
export declare function parseDateRange(input: string, today?: Date): Ga4DateRange;
/**
 * Build the immediately preceding range of equal length, for period comparison.
 *
 * Resolves relative tokens to absolute dates first, because "the 7 days before
 * the last 7 days" has no relative-token spelling.
 */
export declare function precedingRange(range: Ga4DateRange, today?: Date): Ga4DateRange;
/** Turn any accepted GA4 date expression into a concrete UTC date. */
export declare function resolveToDate(value: string, today?: Date): Date;
