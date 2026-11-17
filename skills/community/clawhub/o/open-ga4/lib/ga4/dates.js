import { Ga4Error } from "./errors.js";
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
export class DateRangeError extends Ga4Error {
    constructor(input, message = `Could not read "${input}" as a date range. Use a preset (today, yesterday, ` +
        `last 7 days, last 28 days, last 30 days, last 90 days, this week, last week, this month, ` +
        `last month, this year, last year), an explicit "YYYY-MM-DD..YYYY-MM-DD", or "N days".`) {
        super("INVALID_REQUEST", message, 
        // Names the accepted forms rather than pointing "above" at them: this
        // one fix line is printed after either message, and the second one
        // ("starts after it ends") lists nothing for "above" to refer to.
        "This was read on this machine, before any request reached Google. Correct the range and " +
            'try again: --range "last 28 days" and --range 2026-01-01..2026-01-31 are both accepted.');
        this.name = "DateRangeError";
    }
}
const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
const EXPLICIT_RANGE = /^(\d{4}-\d{2}-\d{2})\s*(?:\.\.|to|—|–|-)\s*(\d{4}-\d{2}-\d{2})$/i;
const N_DAYS = /^(?:last\s+)?(\d{1,3})\s*(?:d|days?)(?:\s+ago)?$/i;
function iso(date) {
    return date.toISOString().slice(0, 10);
}
/** Midnight UTC for the calendar date, so arithmetic never crosses a DST seam. */
function startOfUtcDay(date) {
    return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
}
function addDays(date, days) {
    const next = new Date(date);
    next.setUTCDate(next.getUTCDate() + days);
    return next;
}
const LOCAL_BOUNDARY_NOTE = "Calendar boundaries were computed from this machine's clock. If the property reports in a " +
    "different timezone the range may be shifted by a day.";
/**
 * Parse a human date-range expression into GA4 request fields.
 *
 * @param today Reference date. Injected so tests do not depend on the clock.
 */
export function parseDateRange(input, today = new Date()) {
    const text = input.trim().toLowerCase().replace(/\s+/g, " ");
    if (!text) {
        throw new DateRangeError(input);
    }
    const explicit = EXPLICIT_RANGE.exec(text);
    if (explicit) {
        const [, start, end] = explicit;
        if (start > end) {
            throw new DateRangeError(input, `Date range starts after it ends: ${start} .. ${end}.`);
        }
        return { startDate: start, endDate: end, label: `${start} to ${end}` };
    }
    if (ISO_DATE.test(text)) {
        return { startDate: text, endDate: text, label: text };
    }
    // Relative forms Google resolves in property time. Preferred whenever possible.
    if (text === "today") {
        return { startDate: "today", endDate: "today", label: "today (partial day)" };
    }
    if (text === "yesterday") {
        return { startDate: "yesterday", endDate: "yesterday", label: "yesterday" };
    }
    const days = N_DAYS.exec(text);
    if (days) {
        const count = Number(days[1]);
        if (count < 1) {
            throw new DateRangeError(input);
        }
        // Ends yesterday: today is always partial, and including it makes
        // period-over-period comparisons misleading.
        return {
            startDate: `${count}daysAgo`,
            endDate: "yesterday",
            label: `last ${count} day${count === 1 ? "" : "s"}`,
        };
    }
    const base = startOfUtcDay(today);
    switch (text) {
        case "this week": {
            // ISO weeks start Monday.
            const offset = (base.getUTCDay() + 6) % 7;
            return {
                startDate: iso(addDays(base, -offset)),
                endDate: "today",
                label: "this week so far",
                timezoneNote: LOCAL_BOUNDARY_NOTE,
            };
        }
        case "last week": {
            const offset = (base.getUTCDay() + 6) % 7;
            const monday = addDays(base, -offset - 7);
            return {
                startDate: iso(monday),
                endDate: iso(addDays(monday, 6)),
                label: "last week",
                timezoneNote: LOCAL_BOUNDARY_NOTE,
            };
        }
        case "this month": {
            const first = new Date(Date.UTC(base.getUTCFullYear(), base.getUTCMonth(), 1));
            return {
                startDate: iso(first),
                endDate: "today",
                label: "this month so far",
                timezoneNote: LOCAL_BOUNDARY_NOTE,
            };
        }
        case "last month": {
            const first = new Date(Date.UTC(base.getUTCFullYear(), base.getUTCMonth() - 1, 1));
            const last = new Date(Date.UTC(base.getUTCFullYear(), base.getUTCMonth(), 0));
            return {
                startDate: iso(first),
                endDate: iso(last),
                label: "last month",
                timezoneNote: LOCAL_BOUNDARY_NOTE,
            };
        }
        case "this year": {
            return {
                startDate: iso(new Date(Date.UTC(base.getUTCFullYear(), 0, 1))),
                endDate: "today",
                label: "this year so far",
                timezoneNote: LOCAL_BOUNDARY_NOTE,
            };
        }
        case "last year": {
            return {
                startDate: iso(new Date(Date.UTC(base.getUTCFullYear() - 1, 0, 1))),
                endDate: iso(new Date(Date.UTC(base.getUTCFullYear() - 1, 11, 31))),
                label: "last year",
                timezoneNote: LOCAL_BOUNDARY_NOTE,
            };
        }
        default:
            throw new DateRangeError(input);
    }
}
/**
 * Build the immediately preceding range of equal length, for period comparison.
 *
 * Resolves relative tokens to absolute dates first, because "the 7 days before
 * the last 7 days" has no relative-token spelling.
 */
export function precedingRange(range, today = new Date()) {
    const start = resolveToDate(range.startDate, today);
    const end = resolveToDate(range.endDate, today);
    const lengthDays = Math.round((end.getTime() - start.getTime()) / 86_400_000) + 1;
    const previousEnd = addDays(start, -1);
    const previousStart = addDays(previousEnd, -(lengthDays - 1));
    return {
        startDate: iso(previousStart),
        endDate: iso(previousEnd),
        label: `previous ${lengthDays} day${lengthDays === 1 ? "" : "s"}`,
        timezoneNote: range.timezoneNote,
    };
}
/** Turn any accepted GA4 date expression into a concrete UTC date. */
export function resolveToDate(value, today = new Date()) {
    const base = startOfUtcDay(today);
    if (value === "today") {
        return base;
    }
    if (value === "yesterday") {
        return addDays(base, -1);
    }
    const relative = /^(\d{1,3})daysAgo$/.exec(value);
    if (relative) {
        return addDays(base, -Number(relative[1]));
    }
    if (ISO_DATE.test(value)) {
        return new Date(`${value}T00:00:00Z`);
    }
    throw new DateRangeError(value);
}
