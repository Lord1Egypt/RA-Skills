/**
 * The complete set of hosts this skill is permitted to contact.
 *
 * Every outbound request goes through {@link guardedFetch}, which rejects any
 * URL whose host is not on this list. That turns "we only talk to Google" from
 * a promise in a README into an invariant with a test behind it. Adding a host
 * here is a visible, reviewable diff.
 */
export declare const ALLOWED_HOSTS: readonly string[];
/**
 * A request this skill refused to make.
 *
 * Deliberately a plain Error rather than a Ga4Error, unlike the other classes
 * raised before a socket is opened (PolicyError, DateRangeError,
 * Ga4RequestError). Extending Ga4Error would mean importing src/ga4/errors.ts
 * here, and errors.ts already imports this module for Ga4HttpError: a cycle
 * whose `class X extends Ga4Error` would be evaluated while errors.ts was
 * still initialising, which crashes at import time rather than misbehaving
 * later. src/ga4/errors.ts's diagnose() maps this to a named EGRESS_BLOCKED
 * Ga4Error instead, which is what that function is for, and there is a test
 * for the exit code it produces.
 */
export declare class EgressBlockedError extends Error {
    readonly host: string;
    constructor(host: string);
}
export declare class Ga4HttpError extends Error {
    readonly status: number;
    readonly body: unknown;
    /**
     * Google's own clock, from the response `Date` header.
     *
     * A machine whose clock has drifted more than a minute signs JWT
     * assertions Google rejects, and the only symptom is a bare
     * `invalid_grant`. Carrying the server's time makes that diagnosable.
     */
    readonly serverDate?: Date | undefined;
    constructor(status: number, body: unknown, message: string, 
    /**
     * Google's own clock, from the response `Date` header.
     *
     * A machine whose clock has drifted more than a minute signs JWT
     * assertions Google rejects, and the only symptom is a bare
     * `invalid_grant`. Carrying the server's time makes that diagnosable.
     */
    serverDate?: Date | undefined);
}
export type FetchLike = (input: string, init?: RequestInit) => Promise<Response>;
export type GuardedFetchOptions = {
    method?: "GET" | "POST";
    accessToken?: string;
    body?: unknown;
    /** Form-encoded body. Google's token endpoint does not accept JSON. */
    form?: Record<string, string>;
    signal?: AbortSignal;
    /** Extra headers. Never used for credentials; those go through accessToken. */
    headers?: Record<string, string>;
    fetchImpl?: FetchLike;
    timeoutMs?: number;
};
export declare function assertAllowedUrl(url: string): URL;
/**
 * Perform an HTTPS request against an allowlisted Google host.
 *
 * Errors carry the parsed response body so the error taxonomy can turn a
 * Google error into an actionable sentence, and every message is run through
 * credential redaction on the way out.
 */
export declare function guardedFetch(url: string, options?: GuardedFetchOptions): Promise<unknown>;
