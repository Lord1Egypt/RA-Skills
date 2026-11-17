import { createSign } from "node:crypto";

/**
 * The only OAuth scope this skill ever requests.
 *
 * `analytics.readonly` cannot write, cannot administer, and cannot read any
 * Google product other than Analytics. Keeping it a single exported constant
 * makes "read-only by construction" something a reviewer can grep for.
 */
export const ANALYTICS_READONLY_SCOPE = "https://www.googleapis.com/auth/analytics.readonly";

export const GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token";

export type ServiceAccount = {
  clientEmail: string;
  /** PKCS#8 PEM, exactly as it appears in a Google service-account key file. */
  privateKey: string;
  /** Present in the key file; defaults to Google's public token endpoint. */
  tokenUri?: string;
};

function base64url(input: Buffer | string): string {
  return (typeof input === "string" ? Buffer.from(input, "utf8") : input).toString("base64url");
}

/** Decode one segment of a JWT. Exported so the assertion's claims can be
 * asserted on in src/auth/jwt.test.ts; nothing that ships calls it. */
export function decodeSegment(segment: string): Record<string, unknown> {
  return JSON.parse(Buffer.from(segment, "base64url").toString("utf8")) as Record<string, unknown>;
}

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
export function buildAssertion(account: ServiceAccount, issuedAt: number): string {
  if (!/-----BEGIN [A-Z ]*PRIVATE KEY-----/.test(account.privateKey)) {
    throw new Error(
      "Service account private key is not a PEM block. Use the JSON key file Google generated, unmodified.",
    );
  }

  const audience = account.tokenUri ?? GOOGLE_TOKEN_URI;
  const header = base64url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const payload = base64url(
    JSON.stringify({
      iss: account.clientEmail,
      scope: ANALYTICS_READONLY_SCOPE,
      aud: audience,
      iat: issuedAt,
      // Google rejects assertions valid for more than one hour.
      exp: issuedAt + 3600,
    }),
  );

  const signer = createSign("RSA-SHA256");
  signer.update(`${header}.${payload}`);
  const signature = signer.sign(account.privateKey);

  return `${header}.${payload}.${base64url(signature)}`;
}
