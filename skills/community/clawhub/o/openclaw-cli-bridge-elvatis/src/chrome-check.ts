/**
 * chrome-check.ts
 *
 * Startup check for system Chrome availability.
 * Playwright's stealth mode uses `channel: "chrome"` which requires a real
 * Chrome/Chromium installation. Without it, browser launches fail silently
 * or Cloudflare flags the bundled Chromium as automation.
 */

import { execFileSync } from "node:child_process";

const CHROME_CANDIDATES = [
  "google-chrome",
  "google-chrome-stable",
  "chromium-browser",
  "chromium",
];

export interface ChromeCheckResult {
  available: boolean;
  path: string | null;
  version: string | null;
}

/**
 * Check if a system Chrome installation exists.
 * Returns the path and version if found, or null if missing.
 */
export function checkSystemChrome(): ChromeCheckResult {
  for (const candidate of CHROME_CANDIDATES) {
    try {
      const whichResult = execFileSync("which", [candidate], {
        encoding: "utf-8",
        timeout: 3000,
      }).trim();

      if (whichResult) {
        let version: string | null = null;
        try {
          version = execFileSync(candidate, ["--version"], {
            encoding: "utf-8",
            timeout: 3000,
          }).trim();
        } catch { /* version check optional */ }
        return { available: true, path: whichResult, version };
      }
    } catch {
      // candidate not found — try next
    }
  }
  return { available: false, path: null, version: null };
}
