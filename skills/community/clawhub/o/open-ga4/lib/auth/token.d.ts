import { type FetchLike } from "../ga4/http.js";
import type { Credential } from "./credentials.js";
export type AccessToken = {
    value: string;
    /** Unix seconds. */
    expiresAt: number;
};
export type TokenProvider = {
    getAccessToken(signal?: AbortSignal): Promise<string>;
};
export type TokenProviderOptions = {
    fetchImpl?: FetchLike;
    /** Unix seconds. Injected so tests are deterministic. */
    now?: () => number;
};
/**
 * Build a token provider for a resolved credential.
 *
 * Concurrent callers share one in-flight request: six tools firing at once
 * during a single agent turn must not trigger six token exchanges.
 */
export declare function createTokenProvider(credential: Credential, options?: TokenProviderOptions): TokenProvider;
