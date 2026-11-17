/**
 * Value-level redaction.
 *
 * GA4 is not supposed to contain personal data, but in practice it does: a
 * checkout page path carries an order token, a password-reset link carries an
 * email, a badly built site puts a user id in the URL. Those values arrive in
 * dimension values like `pagePath` and `landingPagePlusQueryString`.
 *
 * Everything here is a pure function over strings so the guarantees in
 * PRIVACY.md are testable without a network or a credential.
 */
/** Query parameters whose values survive redaction because they carry no identity. */
export declare const DEFAULT_KEPT_QUERY_PARAMS: readonly string[];
export type RedactionOptions = {
    /** When false, values pass through untouched. */
    enabled: boolean;
    /** Query parameter names whose values are preserved. */
    keepQueryParams: readonly string[];
    /** Additional caller-supplied patterns, masked as `[redacted:custom]`. */
    extraPatterns: readonly RegExp[];
};
export type RedactionResult = {
    value: string;
    /** Number of substitutions made, so a tool can report "n values redacted". */
    redactions: number;
};
/**
 * Redact a single GA4 dimension value.
 *
 * Idempotent: running it over an already-redacted value is a no-op, which
 * matters because tools re-render cached rows.
 */
export declare function redactValue(value: string, options: RedactionOptions): RedactionResult;
/**
 * Redact credentials out of free text before it reaches a log, an error
 * message, or a tool result. Applied unconditionally; this one is not
 * configurable, because there is no legitimate reason to surface a key.
 */
export declare function redactText(text: string): string;
