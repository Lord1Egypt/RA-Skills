/**
 * Persist OAuth tokens to ~/.openclaw/.otto-tokens.json with 0600 permissions.
 * Matches the ecosystem convention (OpenClaw stores its own auth-profiles.json the same way).
 */

import { readFile, writeFile, mkdir } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";

export interface StoredTokens {
  access_token: string;
  refresh_token: string;
  expires_at: number; // Unix timestamp (seconds)
  scope: string;
  client_id: string;
  server_url: string;
}

const TOKEN_DIR = join(homedir(), ".openclaw");
const TOKEN_FILE = join(TOKEN_DIR, ".otto-tokens.json");

export async function loadTokens(serverUrl: string): Promise<StoredTokens | null> {
  try {
    const raw = await readFile(TOKEN_FILE, "utf-8");
    const tokens: StoredTokens = JSON.parse(raw);
    // Only return tokens that match the configured server
    if (tokens.server_url !== serverUrl) return null;
    return tokens;
  } catch {
    return null;
  }
}

export async function saveTokens(tokens: StoredTokens): Promise<void> {
  await mkdir(TOKEN_DIR, { recursive: true });
  await writeFile(TOKEN_FILE, JSON.stringify(tokens, null, 2), { mode: 0o600 });
}

export function isExpired(tokens: StoredTokens): boolean {
  // Treat as expired 60s before actual expiry to avoid edge cases
  return Date.now() / 1000 > tokens.expires_at - 60;
}
