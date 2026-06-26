/**
 * Hub discovery and auto-setup utilities.
 *
 * Used by the skill to detect a running PersonalDataHub and create
 * an API key for itself. All communication is over HTTP — no dependency
 * on the main PersonalDataHub source.
 */
export interface HealthCheckResult {
    ok: boolean;
    version?: string;
}
export interface CreateApiKeyResult {
    ok: boolean;
    id: string;
    key: string;
}
export interface Credentials {
    hubUrl: string;
    apiKey: string;
    hubDir?: string;
}
/** Path to the credentials file written by `npx pdh init`. */
export declare const CREDENTIALS_PATH: string;
/**
 * Read credentials from ~/.pdh/credentials.json.
 * Returns null if the file doesn't exist or is malformed.
 */
export declare function readCredentials(): Credentials | null;
/**
 * Check if a PersonalDataHub is reachable at the given URL.
 * Hits GET /health and returns the result.
 */
export declare function checkHub(hubUrl: string, timeoutMs?: number): Promise<HealthCheckResult>;
/**
 * Create an API key on the hub for the given application name.
 * Calls POST /api/keys — the GUI endpoint has no auth (it's owner-local).
 */
export declare function createApiKey(hubUrl: string, appName: string): Promise<CreateApiKeyResult>;
/**
 * Attempt full auto-setup: check hub health, then create an API key.
 * Returns null if the hub is not reachable.
 */
export declare function autoSetup(hubUrl: string, appName: string): Promise<{
    hubUrl: string;
    apiKey: string;
} | null>;
/** Common default hub URLs to probe during discovery. */
export declare const DEFAULT_HUB_URLS: string[];
/**
 * Try to discover a running PersonalDataHub by probing common URLs.
 * Returns the first URL that responds to /health, or null.
 */
export declare function discoverHub(): Promise<string | null>;
