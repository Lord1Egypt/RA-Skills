import { guardedFetch } from "../ga4/http.js";
import { buildAssertion, GOOGLE_TOKEN_URI } from "./jwt.js";
/**
 * Access-token acquisition and caching.
 *
 * Two grant types, because the two credential shapes Google hands out need
 * different flows: a service-account key is exchanged via a signed JWT bearer
 * assertion, and a gcloud authorized-user file via an ordinary refresh-token
 * grant.
 *
 * Tokens live in memory only. Nothing here writes to disk; a cached Google
 * access token on disk is a credential at rest that the user did not agree to.
 */
/** Renew this many seconds before real expiry, to survive clock skew and latency. */
const EXPIRY_SKEW_SECONDS = 60;
function readTokenResponse(body, now) {
    const response = (body ?? {});
    if (typeof response.access_token !== "string" || response.access_token.length === 0) {
        throw new Error("Google returned no access token.");
    }
    const lifetime = typeof response.expires_in === "number" ? response.expires_in : 3600;
    return { value: response.access_token, expiresAt: now + lifetime };
}
/**
 * Build a token provider for a resolved credential.
 *
 * Concurrent callers share one in-flight request: six tools firing at once
 * during a single agent turn must not trigger six token exchanges.
 */
export function createTokenProvider(credential, options = {}) {
    const now = options.now ?? (() => Math.floor(Date.now() / 1000));
    let cached;
    let inFlight;
    async function exchange(signal) {
        const issuedAt = now();
        if (credential.kind === "service_account") {
            const body = await guardedFetch(credential.account.tokenUri ?? GOOGLE_TOKEN_URI, {
                form: {
                    grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    assertion: buildAssertion(credential.account, issuedAt),
                },
                fetchImpl: options.fetchImpl,
                signal,
            });
            return readTokenResponse(body, issuedAt);
        }
        const body = await guardedFetch(GOOGLE_TOKEN_URI, {
            form: {
                grant_type: "refresh_token",
                client_id: credential.clientId,
                client_secret: credential.clientSecret,
                refresh_token: credential.refreshToken,
            },
            fetchImpl: options.fetchImpl,
            signal,
        });
        return readTokenResponse(body, issuedAt);
    }
    return {
        async getAccessToken(signal) {
            if (cached && cached.expiresAt - EXPIRY_SKEW_SECONDS > now()) {
                return cached.value;
            }
            if (!inFlight) {
                inFlight = exchange(signal).finally(() => {
                    inFlight = undefined;
                });
            }
            cached = await inFlight;
            return cached.value;
        },
    };
}
