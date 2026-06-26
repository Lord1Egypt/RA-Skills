/**
 * Hub discovery and auto-setup utilities.
 *
 * Used by the skill to detect a running PersonalDataHub and create
 * an API key for itself. All communication is over HTTP — no dependency
 * on the main PersonalDataHub source.
 */
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
/** Path to the credentials file written by `npx pdh init`. */
export const CREDENTIALS_PATH = join(homedir(), '.pdh', 'credentials.json');
/**
 * Read credentials from ~/.pdh/credentials.json.
 * Returns null if the file doesn't exist or is malformed.
 */
export function readCredentials() {
    try {
        if (!existsSync(CREDENTIALS_PATH))
            return null;
        const raw = readFileSync(CREDENTIALS_PATH, 'utf-8');
        const parsed = JSON.parse(raw);
        if (parsed.hubUrl && parsed.apiKey)
            return parsed;
        return null;
    }
    catch {
        return null;
    }
}
/**
 * Check if a PersonalDataHub is reachable at the given URL.
 * Hits GET /health and returns the result.
 */
export async function checkHub(hubUrl, timeoutMs = 3000) {
    const url = hubUrl.replace(/\/+$/, '');
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeoutMs);
        const res = await fetch(`${url}/health`, {
            signal: controller.signal,
        });
        clearTimeout(timer);
        if (!res.ok) {
            return { ok: false };
        }
        const body = await res.json();
        return {
            ok: body.ok === true,
            version: body.version,
        };
    }
    catch {
        return { ok: false };
    }
}
/**
 * Create an API key on the hub for the given application name.
 * Calls POST /api/keys — the GUI endpoint has no auth (it's owner-local).
 */
export async function createApiKey(hubUrl, appName) {
    const url = hubUrl.replace(/\/+$/, '');
    const res = await fetch(`${url}/api/keys`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: appName }),
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Failed to create API key: ${res.status} ${text}`);
    }
    return res.json();
}
/**
 * Attempt full auto-setup: check hub health, then create an API key.
 * Returns null if the hub is not reachable.
 */
export async function autoSetup(hubUrl, appName) {
    const health = await checkHub(hubUrl);
    if (!health.ok) {
        return null;
    }
    const keyResult = await createApiKey(hubUrl, appName);
    return {
        hubUrl,
        apiKey: keyResult.key,
    };
}
/** Common default hub URLs to probe during discovery. */
export const DEFAULT_HUB_URLS = [
    'http://localhost:3000',
    'http://localhost:7007',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:7007',
];
/**
 * Try to discover a running PersonalDataHub by probing common URLs.
 * Returns the first URL that responds to /health, or null.
 */
export async function discoverHub() {
    for (const url of DEFAULT_HUB_URLS) {
        const result = await checkHub(url, 2000);
        if (result.ok) {
            return url;
        }
    }
    return null;
}
