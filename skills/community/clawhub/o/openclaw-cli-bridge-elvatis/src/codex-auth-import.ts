/**
 * codex-auth-import.ts
 *
 * Auto-imports Codex CLI OAuth credentials from ~/.codex/auth.json into
 * OpenClaw's agent auth store (~/.openclaw/agents/main/agent/auth-profiles.json).
 *
 * This solves Issue #2: the provider is registered but actual API calls fail
 * because the auth store doesn't have the credentials. The user shouldn't need
 * to run `openclaw models auth login` manually when Codex CLI is already logged in.
 *
 * Strategy:
 *   1. Read credentials from ~/.codex/auth.json (via codex-auth.ts)
 *   2. Read the existing auth-profiles.json
 *   3. Upsert the "openai-codex:default" profile with fresh tokens
 *   4. Write back atomically
 *
 * This runs on plugin startup and on OAuth refresh.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import { readCodexCredentials, DEFAULT_CODEX_AUTH_PATH } from "./codex-auth.js";

/** Default path to the OpenClaw agent auth store. */
const DEFAULT_AUTH_STORE_PATH = join(
  homedir(),
  ".openclaw",
  "agents",
  "main",
  "agent",
  "auth-profiles.json"
);

/** Auth profile entry format (matches OpenClaw's auth-profiles.json schema). */
interface AuthProfile {
  type: "oauth" | "token";
  provider: string;
  access?: string;
  refresh?: string;
  expires?: number;
  email?: string;
  accountId?: string;
  token?: string;
}

interface AuthStore {
  version: number;
  profiles: Record<string, AuthProfile>;
}

/**
 * Import Codex CLI credentials into the OpenClaw agent auth store.
 *
 * Returns an object describing the result:
 *   - imported: true if credentials were written
 *   - skipped: true if credentials are already up-to-date
 *   - error: error message if import failed
 */
export async function importCodexAuth(opts?: {
  codexAuthPath?: string;
  authStorePath?: string;
  log?: (msg: string) => void;
}): Promise<{ imported: boolean; skipped: boolean; error?: string }> {
  const codexAuthPath = opts?.codexAuthPath ?? DEFAULT_CODEX_AUTH_PATH;
  const authStorePath = opts?.authStorePath ?? DEFAULT_AUTH_STORE_PATH;
  const log = opts?.log ?? (() => {});

  // Step 1: Read Codex CLI credentials
  let creds;
  try {
    creds = await readCodexCredentials(codexAuthPath);
  } catch (err) {
    const msg = `Codex auth not available: ${(err as Error).message}`;
    log(msg);
    return { imported: false, skipped: false, error: msg };
  }

  // Step 2: Read existing auth store (or create skeleton)
  let store: AuthStore;
  try {
    if (existsSync(authStorePath)) {
      store = JSON.parse(readFileSync(authStorePath, "utf8")) as AuthStore;
    } else {
      store = { version: 1, profiles: {} };
    }
  } catch (err) {
    const msg = `Cannot read auth store at ${authStorePath}: ${(err as Error).message}`;
    log(msg);
    return { imported: false, skipped: false, error: msg };
  }

  // Step 3: Check if update is needed
  const profileKey = "openai-codex:default";
  const existing = store.profiles[profileKey];

  if (
    existing &&
    existing.access === creds.accessToken &&
    existing.refresh === (creds.refreshToken ?? existing.refresh)
  ) {
    log(`Codex auth already up-to-date in ${profileKey}`);
    return { imported: false, skipped: true };
  }

  // Step 4: Upsert the profile
  store.profiles[profileKey] = {
    type: "oauth",
    provider: "openai-codex",
    access: creds.accessToken,
    ...(creds.refreshToken ? { refresh: creds.refreshToken } : {}),
    ...(creds.expiresAt ? { expires: creds.expiresAt } : {}),
    ...(creds.email ? { email: creds.email } : {}),
  };

  // Step 5: Write back atomically
  try {
    mkdirSync(dirname(authStorePath), { recursive: true });
    writeFileSync(authStorePath, JSON.stringify(store, null, 4) + "\n", "utf8");
    log(`Codex auth imported into ${profileKey}`);
    return { imported: true, skipped: false };
  } catch (err) {
    const msg = `Failed to write auth store: ${(err as Error).message}`;
    log(msg);
    return { imported: false, skipped: false, error: msg };
  }
}
