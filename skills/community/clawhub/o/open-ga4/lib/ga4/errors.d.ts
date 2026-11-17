/**
 * Turning Google's errors into next actions.
 *
 * Two rules hold throughout:
 *
 * 1. Discriminate on machine-readable fields (HTTP status, `error.status`,
 *    and `details[].reason`), never on `error.message` prose, which is
 *    unversioned and localized.
 * 2. Build messages from an allowlist of fields. Never serialize the caught
 *    error, which on some paths carries the Authorization header.
 */
export declare class Ga4Error extends Error {
    readonly code: string;
    /** What the user should do next. Always present. */
    readonly fix: string;
    readonly retryable: boolean;
    constructor(code: string, message: string, 
    /** What the user should do next. Always present. */
    fix: string, retryable?: boolean);
    /** The whole thing, as a model or a terminal should see it. */
    toString(): string;
}
export type DiagnoseContext = {
    /** The service-account address, so "grant access to X" names the right X. */
    principal?: string;
    /** Numeric property id the request was for, when there was one. */
    propertyId?: string;
    /** Injected for tests. */
    now?: () => number;
};
/**
 * Map a transport failure onto a named cause and a fix.
 *
 * Order matters: clock skew is checked first, because it presents as a bare
 * `invalid_grant` that otherwise reads as a credential problem and sends
 * people off to regenerate perfectly good keys.
 */
export declare function diagnose(error: unknown, context?: DiagnoseContext): Ga4Error;
