import { redactText } from "../privacy/redact.js";
/**
 * The complete set of hosts this skill is permitted to contact.
 *
 * Every outbound request goes through {@link guardedFetch}, which rejects any
 * URL whose host is not on this list. That turns "we only talk to Google" from
 * a promise in a README into an invariant with a test behind it. Adding a host
 * here is a visible, reviewable diff.
 */
export const ALLOWED_HOSTS = [
    "oauth2.googleapis.com",
    "analyticsdata.googleapis.com",
    "analyticsadmin.googleapis.com",
];
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
export class EgressBlockedError extends Error {
    host;
    constructor(host) {
        super(`Blocked a request to ${host}. This skill may only contact ${ALLOWED_HOSTS.join(", ")}.`);
        this.host = host;
        this.name = "EgressBlockedError";
    }
}
export class Ga4HttpError extends Error {
    status;
    body;
    serverDate;
    constructor(status, body, message, 
    /**
     * Google's own clock, from the response `Date` header.
     *
     * A machine whose clock has drifted more than a minute signs JWT
     * assertions Google rejects, and the only symptom is a bare
     * `invalid_grant`. Carrying the server's time makes that diagnosable.
     */
    serverDate) {
        super(message);
        this.status = status;
        this.body = body;
        this.serverDate = serverDate;
        this.name = "Ga4HttpError";
    }
}
const DEFAULT_TIMEOUT_MS = 30_000;
export function assertAllowedUrl(url) {
    let parsed;
    try {
        parsed = new URL(url);
    }
    catch {
        throw new EgressBlockedError(url);
    }
    if (parsed.protocol !== "https:") {
        throw new EgressBlockedError(`${parsed.protocol}//${parsed.host}`);
    }
    if (!ALLOWED_HOSTS.includes(parsed.host)) {
        throw new EgressBlockedError(parsed.host);
    }
    return parsed;
}
/**
 * Perform an HTTPS request against an allowlisted Google host.
 *
 * Errors carry the parsed response body so the error taxonomy can turn a
 * Google error into an actionable sentence, and every message is run through
 * credential redaction on the way out.
 */
export async function guardedFetch(url, options = {}) {
    // The parsed URL is kept and it is what gets fetched, rather than the string
    // that was handed in. Both are the same today, because validation and fetch
    // go through the same WHATWG parser, so this closes no live gap. It closes
    // the shape of one: an allowlist enforced on a parse of the input while a
    // *different* parse does the request is only correct as long as the two parses
    // agree, and this is the single place where that could stop being true, either
    // through a platform change or through an injected FetchLike whose own parsing
    // differs. Checking and fetching the same object means the question cannot
    // come up.
    const allowed = assertAllowedUrl(url);
    const fetchImpl = options.fetchImpl ?? globalThis.fetch;
    const timeout = AbortSignal.timeout(options.timeoutMs ?? DEFAULT_TIMEOUT_MS);
    const signal = options.signal ? AbortSignal.any([options.signal, timeout]) : timeout;
    const headers = {
        accept: "application/json",
        ...options.headers,
    };
    if (options.accessToken) {
        headers.authorization = `Bearer ${options.accessToken}`;
    }
    let payload;
    if (options.form !== undefined) {
        headers["content-type"] = "application/x-www-form-urlencoded";
        payload = new URLSearchParams(options.form).toString();
    }
    else if (options.body !== undefined) {
        headers["content-type"] = "application/json";
        payload = JSON.stringify(options.body);
    }
    const response = await fetchImpl(allowed.href, {
        method: options.method ?? (payload === undefined ? "GET" : "POST"),
        headers,
        body: payload,
        signal,
        // The allowlist is checked once, before the request. Following a redirect
        // would let a 302 reach a host that was never checked, so redirects are an
        // error rather than something to chase.
        redirect: "error",
    });
    const raw = await response.text();
    let parsed;
    try {
        parsed = raw ? JSON.parse(raw) : undefined;
    }
    catch {
        parsed = raw;
    }
    if (!response.ok) {
        throw new Ga4HttpError(response.status, parsed, redactText(messageFrom(parsed, response)), parseServerDate(response));
    }
    return parsed;
}
function parseServerDate(response) {
    const header = response.headers.get("date");
    if (!header) {
        return undefined;
    }
    const parsed = new Date(header);
    return Number.isNaN(parsed.getTime()) ? undefined : parsed;
}
function messageFrom(body, response) {
    if (body && typeof body === "object") {
        const error = body.error;
        if (typeof error === "string") {
            const description = body.error_description;
            return typeof description === "string" ? `${error}: ${description}` : error;
        }
        if (error && typeof error === "object" && typeof error.message === "string") {
            return error.message;
        }
    }
    if (typeof body === "string" && body.trim()) {
        return body.trim();
    }
    return `${response.status} ${response.statusText}`.trim();
}
