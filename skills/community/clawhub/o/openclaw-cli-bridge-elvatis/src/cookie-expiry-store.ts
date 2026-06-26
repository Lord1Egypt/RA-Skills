/**
 * cookie-expiry-store.ts
 *
 * Consolidated cookie expiry tracking for all web providers.
 * Replaces 4 separate JSON files with a single unified store:
 *   ~/.openclaw/cookie-expiry.json
 *
 * Migration: on first load, imports data from legacy per-provider files
 * and deletes them.
 */

import { readFileSync, writeFileSync, existsSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

export type ProviderName = "grok" | "gemini" | "claude" | "chatgpt";

export interface ExpiryInfo {
  expiresAt: number;   // epoch ms
  loginAt: number;     // epoch ms
  cookieName: string;
}

export interface CookieExpiryData {
  grok: ExpiryInfo | null;
  gemini: ExpiryInfo | null;
  claude: ExpiryInfo | null;
  chatgpt: ExpiryInfo | null;
}

const STORE_PATH = join(homedir(), ".openclaw", "cookie-expiry.json");

// Legacy file paths (for migration)
const LEGACY_FILES: Record<ProviderName, string> = {
  grok: join(homedir(), ".openclaw", "grok-cookie-expiry.json"),
  gemini: join(homedir(), ".openclaw", "gemini-cookie-expiry.json"),
  claude: join(homedir(), ".openclaw", "claude-cookie-expiry.json"),
  chatgpt: join(homedir(), ".openclaw", "chatgpt-cookie-expiry.json"),
};

function emptyData(): CookieExpiryData {
  return { grok: null, gemini: null, claude: null, chatgpt: null };
}

/**
 * Migrate legacy per-provider files into the consolidated store.
 * Safe to call multiple times — only imports files that exist.
 */
export function migrateLegacyFiles(): { migrated: ProviderName[] } {
  const migrated: ProviderName[] = [];
  let data = loadAll();

  for (const [provider, legacyPath] of Object.entries(LEGACY_FILES) as [ProviderName, string][]) {
    if (!existsSync(legacyPath)) continue;
    try {
      const legacy = JSON.parse(readFileSync(legacyPath, "utf-8")) as ExpiryInfo;
      // Only import if we don't already have newer data
      if (!data[provider] || legacy.loginAt > data[provider]!.loginAt) {
        data[provider] = legacy;
        migrated.push(provider);
      }
      unlinkSync(legacyPath);
    } catch {
      // Corrupted legacy file — just delete it
      try { unlinkSync(legacyPath); } catch { /* ignore */ }
    }
  }

  if (migrated.length > 0) {
    writeAll(data);
  }
  return { migrated };
}

/** Load the entire expiry store. Returns empty data if file doesn't exist. */
export function loadAll(): CookieExpiryData {
  try {
    const raw = readFileSync(STORE_PATH, "utf-8");
    const parsed = JSON.parse(raw) as Partial<CookieExpiryData>;
    return { ...emptyData(), ...parsed };
  } catch {
    return emptyData();
  }
}

/** Save a single provider's expiry info. Merges with existing data. */
export function saveProviderExpiry(provider: ProviderName, info: ExpiryInfo): void {
  const data = loadAll();
  data[provider] = info;
  writeAll(data);
}

/** Load a single provider's expiry info. */
export function loadProviderExpiry(provider: ProviderName): ExpiryInfo | null {
  return loadAll()[provider];
}

/** Write the full store to disk. */
function writeAll(data: CookieExpiryData): void {
  try {
    writeFileSync(STORE_PATH, JSON.stringify(data, null, 2));
  } catch { /* ignore write errors */ }
}

/** Get the store file path (for existsSync checks in startup restore). */
export function getStorePath(): string {
  return STORE_PATH;
}
