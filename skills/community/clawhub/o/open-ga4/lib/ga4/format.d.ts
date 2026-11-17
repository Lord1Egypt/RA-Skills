import { type RedactionOptions } from "../privacy/redact.js";
import type { ResponseMetaData, RunReportResponse } from "./client.js";
/**
 * Rendering a report for a model to read.
 *
 * Three jobs, in order of how much they matter:
 *
 * 1. Redact. Every dimension value passes through redaction on the way out.
 *    This is the last point at which a stray email in a URL can be stopped.
 * 2. Frame the data as data. Dimension values are visitor-authored (anyone
 *    can put text in `pagePath` by visiting a URL), so rows go inside a fenced
 *    block introduced as untrusted, never interpolated into prose, and the
 *    same framing travels with the structured `rows` field below: a value
 *    with no personal-data pattern in it redacts to nothing, so an
 *    injection attempt reaches a model with no warning at all unless the
 *    warning is attached to the data itself, on every channel it travels.
 * 3. Say what the numbers do not mean. Thresholding, sampling and `(other)`
 *    rollups all make totals wrong in ways that are invisible unless stated.
 */
export type FormatOptions = {
    title: string;
    dateRangeLabel?: string;
    redaction: RedactionOptions;
    /** Extra caveats from the caller (timezone notes, renamed fields, quota). */
    notes?: string[];
    maxRows?: number;
};
export type FormattedReport = {
    markdown: string;
    rowsShown: number;
    rowsAvailable: number;
    redactions: number;
    caveats: string[];
    /**
     * The same formatted, redacted values the markdown table shows, addressed
     * by field name instead of column position, so `--json` has an answer that
     * is not "re-parse a markdown table". Redaction and metric formatting both
     * already happened before this is built: this is not a second, separate
     * path back to a raw cell. Newlines are flattened for the same reason the
     * markdown table's cells are (see flattenNewlines below), which happens
     * upstream of both, in `body` and `headers`, so the two cannot drift apart.
     * Every cell and every key, dimensions, metrics and headers alike.
     */
    rows: Array<Record<string, string>>;
    /**
     * The same untrusted-input sentence the markdown table's lead-in gives,
     * carried as its own field rather than folded into `caveats` (a list about
     * data quality, not about trust) or left implicit. A dedicated field next
     * to `rows` makes it hard to consume the data without also seeing this.
     */
    rowsWarning: string;
};
/**
 * Collapses runs of `\r` and `\n` into a single space.
 *
 * In the markdown table this keeps a value from forging a new table row (a
 * bare newline would otherwise start a line of its own, read as a fresh
 * `| ... |` row). The same flattening matters just as much for the JSON
 * `rows` field, for a different reason: a value that starts a line of its
 * own reads differently to a model than one buried mid-sentence, regardless
 * of whether the surrounding document is markdown or JSON. JSON's own
 * escaping keeps the document structurally valid either way; it does not by
 * itself stop injected text from reading as its own line once a model
 * attends to it. Applied once, upstream in `body` and `headers` below, so both
 * channels share this single pass rather than each doing (or forgetting to do)
 * their own. Every cell, not only the dimension ones: a metric cell is a
 * number in practice, but formatMetric returns its input verbatim when
 * Number(raw) is not finite, and a header is our own request echoed back, so
 * both were relying on an expectation about the response rather than on this
 * function. tableCell below flattens again on the markdown side, which is
 * belt and braces rather than the same thing twice: this pass is what the JSON
 * `rows` field gets.
 *
 * Exported for the one place a value reaches text *outside* the fenced block:
 * the caveat line saying what a report was filtered to, which interpolates a
 * filter value into prose (src/ga4/filters.ts and src/tools/reports.ts). That
 * value comes from the agent's own argv rather than from Google, so the risk
 * is lower, but it is the single exception to the framing discipline the rest
 * of this module enforces, and sharing this one function is what keeps the
 * two from drifting.
 */
export declare function flattenNewlines(value: string): string;
/**
 * Make a string safe to place between two `|` delimiters, by removing every
 * character that could act as one.
 *
 * Substitution, not escaping, and that is the whole point. The previous
 * implementation escaped, `cell.replace(/\|/g, "\\|")`, and it was exactly
 * backwards for a value that already contained a backslash: `\|` became `\\|`,
 * which GFM reads as an escaped backslash followed by a **live** pipe. The
 * escape converted an already-harmless pipe into a working delimiter. A visitor
 * loading any page on the site with `?q=pricing\|999999` on the end gets that
 * string into `searchTerm` verbatim; it matches no personal-data pattern, so
 * redaction passes it through, and `report search_terms` then emitted a
 * five-field row under four headers. `eventCount` read 999999 instead of 3,
 * every later metric shifted one place, and an agent relayed a fabricated
 * figure to a non-technical user as a measured number. Same reach through
 * `pagePathPlusQueryString`, `landingPagePlusQueryString`, `pageTitle` and
 * `?utm_campaign=`.
 *
 * Escaping correctly (backslash first, then pipe) would also work, but it keeps
 * the value's ability to forge structure one ordering mistake away. Removing
 * the delimiter from the value means no escape sequence is involved at all,
 * which is the property worth having on a channel a model reads: there is
 * nothing left to get wrong. The cost is that a literal `|` in a value reads as
 * a fullwidth one, which is visible, honest, and cannot shift a number.
 *
 * Newlines go too, for the reason flattenNewlines exists: a bare newline starts
 * a line that reads as a fresh `| ... |` row.
 */
export declare function tableCell(value: string): string;
/** The caveats that change how a number should be read. */
export declare function caveatsFor(metadata: ResponseMetaData | undefined, hasCurrencyMetric: boolean): string[];
/**
 * Render a report response as markdown.
 *
 * Returns the redaction count alongside the text so a tool can tell the model
 * that values were masked, rather than leaving it to infer that from
 * `[redacted:email]` appearing in a cell.
 */
export declare function formatReport(response: RunReportResponse, options: FormatOptions): FormattedReport;
