/**
 * The only OAuth scope this skill ever requests.
 *
 * `analytics.readonly` cannot write, cannot administer, and cannot read any
 * Google product other than Analytics. Keeping it a single exported constant
 * makes "read-only by construction" something a reviewer can grep for.
 */
export declare const ANALYTICS_READONLY_SCOPE = "https://www.googleapis.com/auth/analytics.readonly";
export declare const GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token";
export type ServiceAccount = {
    clientEmail: string;
    /** PKCS#8 PEM, exactly as it appears in a Google service-account key file. */
    privateKey: string;
    /** Present in the key file; defaults to Google's public token endpoint. */
    tokenUri?: string;
};
/** Decode one segment of a JWT. Exported so the assertion's claims can be
 * asserted on in src/auth/jwt.test.ts; nothing that ships calls it. */
export declare function decodeSegment(segment: string): Record<string, unknown>;
/**
 * Build a signed JWT bearer assertion for the OAuth 2.0 service-account flow
 * (RFC 7523, as profiled by Google).
 *
 * Implemented directly on `node:crypto` rather than pulling in
 * `google-auth-library`: it is a dozen lines, it adds no dependency, and it
 * keeps the entire credential path readable in one file.
 *
 * @param issuedAt Unix seconds. Injected so tests are deterministic.
 */
export declare function buildAssertion(account: ServiceAccount, issuedAt: number): string;
