/**
 * Non-blocking update checker.
 *
 * Pattern: register exit-hook + kick-off-background-fetch
 * - On startup: kick off background fetch (non-blocking)
 * - On process exit: read cache, print notice if newer version exists
 * - Check interval: 24 hours
 * - Notice appears AFTER command output, not before (same as npm/gh/yarn)
 * - Never delays or blocks the CLI command
 *
 * Cache is shared between the CLI process (writes latestVersion / latestExtensionVersion
 * via background fetch) and the daemon process (writes currentExtensionVersion /
 * extensionLastSeenAt via `recordExtensionVersion` on each hello). Writes use a
 * read-merge-write pattern so neither side clobbers the other.
 */
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import { PKG_VERSION } from './version.js';
const CACHE_DIR = path.join(os.homedir(), '.opencli');
const CACHE_FILE = path.join(CACHE_DIR, 'update-check.json');
const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000; // 24h
const EXTENSION_STALE_MS = 7 * 24 * 60 * 60 * 1000; // 7d
const NPM_REGISTRY_URL = 'https://registry.npmjs.org/@jackwener/opencli/latest';
const GITHUB_RELEASES_URL = 'https://api.github.com/repos/jackwener/OpenCLI/releases?per_page=20';
function readCacheSync() {
    try {
        return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf-8'));
    }
    catch {
        return null;
    }
}
// Read cache once at module load — shared by both exported functions
const _cache = readCacheSync();
function writeCacheMerge(updates) {
    try {
        fs.mkdirSync(CACHE_DIR, { recursive: true });
        const existing = readCacheSync() ?? {};
        const merged = { ...existing, ...updates };
        fs.writeFileSync(CACHE_FILE, JSON.stringify(merged), 'utf-8');
    }
    catch {
        // Best-effort; never fail
    }
}
/** Compare semver strings. Returns true if `a` is strictly newer than `b`. */
function isNewer(a, b) {
    const parse = (v) => v.replace(/^v/, '').split('-')[0].split('.').map(Number);
    const pa = parse(a);
    const pb = parse(b);
    if (pa.some(isNaN) || pb.some(isNaN))
        return false;
    const [aMaj, aMin, aPat] = pa;
    const [bMaj, bMin, bPat] = pb;
    if (aMaj !== bMaj)
        return aMaj > bMaj;
    if (aMin !== bMin)
        return aMin > bMin;
    return aPat > bPat;
}
function isCI() {
    return !!(process.env.CI || process.env.CONTINUOUS_INTEGRATION);
}
/** Pure function: derive notice text from cache state. Exported for tests. */
function buildUpdateNotices({ cliVersion, cache, now }) {
    if (!cache)
        return {};
    const lines = {};
    if (cache.latestVersion && isNewer(cache.latestVersion, cliVersion)) {
        lines.cli =
            `\n  Update available: v${cliVersion} → v${cache.latestVersion}\n` +
                `  Run: npm install -g @jackwener/opencli\n`;
    }
    return lines;
}
/**
 * Register a process exit hook that prints an update notice if a newer
 * version was found on the last background check.
 * Notice appears after command output — same pattern as npm/gh/yarn.
 * Skipped during --get-completions to avoid polluting shell completion output.
 */
export function registerUpdateNoticeOnExit() {
    if (isCI())
        return;
    if (process.argv.includes('--get-completions'))
        return;
    process.on('exit', (code) => {
        if (code !== 0)
            return; // Don't show update notice on error exit
        const { cli, extension } = buildUpdateNotices({
            cliVersion: PKG_VERSION,
            cache: _cache,
            now: Date.now(),
        });
        if (!cli && !extension)
            return;
        try {
            process.stderr.write(`${cli ?? ''}${extension ?? ''}\n`);
        }
        catch {
            // Ignore broken pipe (stderr closed before process exits)
        }
    });
}
function extractLatestExtensionVersionFromReleases(releases) {
    for (const release of releases) {
        for (const asset of release.assets ?? []) {
            const assetMatch = asset.name.match(/^opencli-extension-v(.+)\.zip$/);
            if (assetMatch)
                return assetMatch[1];
        }
        const tagMatch = release.tag_name.match(/^ext-v(.+)$/);
        if (tagMatch)
            return tagMatch[1];
    }
    return undefined;
}
/** Fetch the latest extension version from GitHub Releases. */
async function fetchLatestExtensionVersion() {
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 3000);
        const res = await fetch(GITHUB_RELEASES_URL, {
            signal: controller.signal,
            headers: { 'User-Agent': `opencli/${PKG_VERSION}`, Accept: 'application/vnd.github+json' },
        });
        clearTimeout(timer);
        if (!res.ok)
            return undefined;
        const releases = await res.json();
        return extractLatestExtensionVersionFromReleases(releases);
    }
    catch {
        return undefined;
    }
}
/**
 * Kick off a background fetch to npm registry. Writes to cache for next run.
 * Fully non-blocking — never awaited.
 */
export function checkForUpdateBackground() {
    if (isCI())
        return;
    if (_cache?.lastCheck && Date.now() - _cache.lastCheck < CHECK_INTERVAL_MS)
        return;
    void (async () => {
        try {
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), 3000);
            const res = await fetch(NPM_REGISTRY_URL, {
                signal: controller.signal,
                headers: { 'User-Agent': `opencli/${PKG_VERSION}` },
            });
            clearTimeout(timer);
            if (!res.ok)
                return;
            const data = await res.json();
            if (typeof data.version === 'string') {
                const updates = { lastCheck: Date.now(), latestVersion: data.version };
                writeCacheMerge(updates);
            }
        }
        catch {
            // Network error: silently skip, try again next run
        }
    })();
}
/**
 * Stash the current extension version into the shared cache. Called by the
 * daemon on each hello handshake. Lets the next CLI process compare against
 * the latest known release and print an exit notice without any extra I/O.
 */
export function recordExtensionVersion(version) {
    if (typeof version !== 'string' || !version.trim())
        return;
    writeCacheMerge({
        currentExtensionVersion: version.trim(),
        extensionLastSeenAt: Date.now(),
    });
}
/**
 * Get the cached latest extension version (if available).
 * Used by `opencli doctor` to report extension updates.
 */
export function getCachedLatestExtensionVersion() {
    return _cache?.latestExtensionVersion;
}
export { extractLatestExtensionVersionFromReleases as _extractLatestExtensionVersionFromReleases, buildUpdateNotices as _buildUpdateNotices, EXTENSION_STALE_MS as _EXTENSION_STALE_MS, };
